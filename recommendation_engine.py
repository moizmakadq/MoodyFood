import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from feedback_analyzer import FeedbackAnalyzer
    FEEDBACK_AVAILABLE = True
except ImportError:
    FEEDBACK_AVAILABLE = False
    logger.warning("Feedback analyzer not available")



class RecommendationEngine:
    def __init__(self, data_loader, database):
        self.data_loader = data_loader
        self.database = database
        self.food_data = data_loader.food_data

        if FEEDBACK_AVAILABLE:
            self.feedback_analyzer = FeedbackAnalyzer(database)
            logger.info("Feedback analyzer initialized")
        else:
            self.feedback_analyzer = None
        
        logger.info("Recommendation Engine initialized")

    
    def get_recommendations(
        self,
        mood: str,
        user_data: Dict,
        top_n: int = 10
    ) -> pd.DataFrame:
        try:
            logger.info(f"Getting recommendations for mood: {mood}")

            filtered_data = self.food_data.copy()

            filtered_data = self._filter_by_mood(filtered_data, mood)

            if 'diet_preference' in user_data:
                filtered_data = self._filter_by_diet(
                    filtered_data,
                    user_data['diet_preference']
                )

            if 'cuisine_preferences' in user_data:
                filtered_data = self._filter_by_cuisine(
                    filtered_data,
                    user_data['cuisine_preferences']
                )

            if 'age_group' in user_data:
                filtered_data = self._filter_by_age(
                    filtered_data,
                    user_data['age_group']
                )

            if 'gender' in user_data:
                filtered_data = self._filter_by_gender(
                    filtered_data,
                    user_data['gender']
                )

            if 'state' in user_data:
                filtered_data = self._apply_location_preferences(
                    filtered_data,
                    user_data['state'],
                    user_data.get('city', '')
                )

            if filtered_data.empty:
                logger.warning("No results found, relaxing constraints...")
                filtered_data = self._fallback_recommendations(mood, user_data)

            recommendations = self._rank_recommendations(
                filtered_data,
                top_n,
                mood,
                user_data
            )
            
            logger.info(f"Returning {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return pd.DataFrame()
    
    def _filter_by_mood(self, data: pd.DataFrame, mood: str) -> pd.DataFrame:
        
        mood_lower = mood.lower()
        filtered = data[data['Mood'].str.lower() == mood_lower]
        
        if filtered.empty:
            logger.warning(f"No items found for mood: {mood}, "
                          f"using all moods")
            return data
        
        return filtered
    
    def _filter_by_diet(self, data: pd.DataFrame, diet_pref: str) -> pd.DataFrame:
        
        if diet_pref.lower() == 'both':
            return data
        
        return data[data['Veg_or_NonVeg'].str.lower() == diet_pref.lower()]
    
    def _filter_by_cuisine(
        self,
        data: pd.DataFrame,
        cuisine_prefs: List[str]
    ) -> pd.DataFrame:
        
        if not cuisine_prefs:
            return data

        cuisine_prefs_lower = [c.lower() for c in cuisine_prefs]
        filtered = data[
            data['Cuisine_Type'].str.lower().isin(cuisine_prefs_lower)
        ]
        
        if filtered.empty:
            logger.warning("No items found for selected cuisines, "
                          "showing all cuisines")
            return data
        
        return filtered
    
    def _filter_by_age(self, data: pd.DataFrame, age_group: str) -> pd.DataFrame:
        

        filtered = data[
            (data['Age_Group'] == age_group) |
            (data['Age_Group'] == 'All Ages')
        ]
        
        if filtered.empty:
            return data
        
        return filtered
    
    def _filter_by_gender(self, data: pd.DataFrame, gender: str) -> pd.DataFrame:
        

        filtered = data[
            (data['Gender'] == gender) |
            (data['Gender'] == 'All')
        ]
        
        if filtered.empty:
            return data
        
        return filtered
    
    def _apply_location_preferences(
        self,
        data: pd.DataFrame,
        state: str,
        city: str
    ) -> pd.DataFrame:
        

        state_cuisine_map = {
            'Gujarat': ['Indian', 'Gujarati'],
            'Maharashtra': ['Indian', 'Maharashtrian'],
            'Punjab': ['Indian', 'Punjabi'],
            'Tamil Nadu': ['Indian', 'South Indian'],
            'Karnataka': ['Indian', 'South Indian'],
            'Kerala': ['Indian', 'South Indian'],
            'West Bengal': ['Indian', 'Bengali'],
            'Rajasthan': ['Indian', 'Rajasthani']
        }

        regional_cuisines = state_cuisine_map.get(state, ['Indian'])
        data = data.copy()
        data['location_score'] = data['Cuisine_Type'].apply(
            lambda x: 10 if x in regional_cuisines else 0
        )
        
        return data
    
    def _fallback_recommendations(
        self,
        mood: str,
        user_data: Dict
    ) -> pd.DataFrame:
        

        filtered = self._filter_by_mood(self.food_data, mood)
        
        if not filtered.empty:
            return filtered

        if 'diet_preference' in user_data:
            filtered = self._filter_by_diet(
                self.food_data,
                user_data['diet_preference']
            )
            if not filtered.empty:
                return filtered

        logger.warning("Using random recommendations as fallback")
        return self.food_data.sample(
            n=min(20, len(self.food_data))
        )
    
    def _rank_recommendations(
        self,
        data: pd.DataFrame,
        top_n: int,
        mood: str = None,
        user_data: Dict = None
    ) -> pd.DataFrame:
        if data.empty:
            return data

        data = data.copy()

        if 'location_score' not in data.columns:
            data['location_score'] = 0

        feedback_score = 0
        if self.feedback_analyzer and mood and user_data:
            try:

                if self.feedback_analyzer.has_sufficient_feedback(min_feedback=5):
                    logger.info("Using feedback data for personalized recommendations")

                    stats = self.feedback_analyzer.get_feedback_statistics(use_cache=True)
                    
                    if not stats.empty:

                        age_group = user_data.get('age_group')
                        gender = user_data.get('gender')

                        emotion_stats = stats[stats['detected_emotion'].str.lower() == mood.lower()]

                        if age_group and not emotion_stats.empty:
                            demo_stats = emotion_stats[emotion_stats['age_group'] == age_group]
                            if not demo_stats.empty:
                                emotion_stats = demo_stats
                        
                        if gender and not emotion_stats.empty:
                            demo_stats = emotion_stats[emotion_stats['gender'] == gender]
                            if not demo_stats.empty:
                                emotion_stats = demo_stats

                        food_scores = {}
                        for _, row in emotion_stats.iterrows():
                            food = row['food_item']
                            avg_rating = row['avg_rating']
                            score = (avg_rating - 1) * 2.5  # Convert 1-5 to 0-10
                            food_scores[food] = score

                        data['feedback_score'] = data['Recommended_Food_Item'].map(
                            lambda food: food_scores.get(food, 0.0)  # No score for unrated foods
                        )

                        avoid_foods = emotion_stats[
                            (emotion_stats['total_score'] < 10) &
                            (emotion_stats['feedback_count'] >= 3)
                        ]['food_item'].tolist()

                        if avoid_foods:
                            data.loc[data['Recommended_Food_Item'].isin(avoid_foods), 'feedback_score'] = 0
                            logger.info(f"Avoiding {len(avoid_foods)} low-rated foods")
                    else:
                        data['feedback_score'] = 0.0  # No score
                else:
                    data['feedback_score'] = 0.0  # No score
                    logger.info("Insufficient feedback, using zero scores")
            except Exception as e:
                logger.error(f"Error calculating feedback scores: {e}")
                data['feedback_score'] = 0.0  # No score
        else:
            data['feedback_score'] = 0.0  # No score if no feedback

        data['total_score'] = (
            data['location_score'] +
            data['feedback_score'] * 2 +  # Weight feedback heavily
            np.random.rand(len(data)) * 3  # Add randomness for variety
        )

        ranked = data.sort_values('total_score', ascending=False)

        columns_to_drop = ['location_score', 'feedback_score', 'total_score']
        ranked = ranked.drop(
            columns=[c for c in columns_to_drop if c in ranked.columns]
        )
        
        return ranked.head(top_n).reset_index(drop=True)

    
    def search_food_items(self, query: str) -> pd.DataFrame:
        query_lower = query.lower()
        
        mask = (
            self.food_data['Recommended_Food_Item'].str.lower().str.contains(query_lower, na=False) |
            self.food_data['Food_Category'].str.lower().str.contains(query_lower, na=False) |
            self.food_data['Cuisine_Type'].str.lower().str.contains(query_lower, na=False)
        )
        
        return self.food_data[mask]
    
    def get_popular_items(self, top_n: int = 10) -> pd.DataFrame:

        popular = self.food_data['Recommended_Food_Item'].value_counts()
        popular_items = popular.head(top_n).index.tolist()

        return self.food_data[
            self.food_data['Recommended_Food_Item'].isin(popular_items)
        ].drop_duplicates(subset=['Recommended_Food_Item']).head(top_n)
    
    def get_recommendations_by_category(
        self,
        category: str,
        limit: int = 10
    ) -> pd.DataFrame:
        filtered = self.food_data[
            self.food_data['Food_Category'].str.lower() == category.lower()
        ]
        return filtered.sample(n=min(limit, len(filtered)))

if __name__ == "__main__":
    from data_loader import DataLoader
    from database import Database

    data_loader = DataLoader()
    database = Database()
    engine = RecommendationEngine(data_loader, database)

    test_user_data = {
        'name': 'Test User',
        'age_group': '26-35',
        'gender': 'Male',
        'state': 'Gujarat',
        'city': 'Ahmedabad',
        'diet_preference': 'Veg',
        'cuisine_preferences': ['Indian', 'Chinese']
    }
    
    recommendations = engine.get_recommendations(
        mood='happy',
        user_data=test_user_data,
        top_n=5
    )
    
    print("\nTop 5 Recommendations:")
    print(recommendations[['Recommended_Food_Item', 'Food_Category', 
                          'Cuisine_Type', 'Mood']].to_string())