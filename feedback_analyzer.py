import pandas as pd
import sqlite3
import logging
from typing import Dict, List, Optional
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeedbackAnalyzer:

    def __init__(self, database):
        self.database = database
        self.db_path = database.db_path
        self._stats_cache = None  # Cache for feedback statistics
        self._cache_timestamp = None
        logger.info("Feedback Analyzer initialized with cumulative scoring")
    
    def get_feedback_statistics(self, use_cache: bool = True) -> pd.DataFrame:

        if use_cache and self._stats_cache is not None:
            logger.info("Using cached feedback statistics")
            return self._stats_cache
        
        try:
            query = 
            
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql(query, conn)
            conn.close()

            self._stats_cache = df
            
            logger.info(f"Retrieved and cached feedback stats for {len(df)} combinations")
            return df
            
        except Exception as e:
            logger.error(f"Error getting feedback statistics: {e}")
            return pd.DataFrame()
    
    def clear_cache(self):
        
        self._stats_cache = None
        logger.info("Feedback cache cleared")

    def get_food_score(
        self,
        food_item: str,
        emotion: str,
        age_group: str = None,
        gender: str = None
    ) -> float:
        try:
            stats = self.get_feedback_statistics()
            
            if stats.empty:
                return 0.0  # No score if no feedback

            filtered = stats[
                (stats['food_item'] == food_item) &
                (stats['detected_emotion'].str.lower() == emotion.lower())
            ]

            if age_group and not filtered.empty:
                demo_filtered = filtered[filtered['age_group'] == age_group]
                if not demo_filtered.empty:
                    filtered = demo_filtered
            
            if gender and not filtered.empty:
                demo_filtered = filtered[filtered['gender'] == gender]
                if not demo_filtered.empty:
                    filtered = demo_filtered
            
            if filtered.empty:
                return 0.0  # No score if no matching feedback

            total_score = filtered['total_score'].sum()
            capped_score = min(100.0, total_score)
            
            logger.debug(f"{food_item}: total={total_score}, capped={capped_score}")
            return float(capped_score)
            
        except Exception as e:
            logger.error(f"Error calculating food score: {e}")
            return 0.0  # No score on error
    
    def get_top_rated_foods(
        self,
        emotion: str,
        age_group: str = None,
        gender: str = None,
        limit: int = 10
    ) -> pd.DataFrame:
        try:
            stats = self.get_feedback_statistics()
            
            if stats.empty:
                return pd.DataFrame()

            filtered = stats[stats['detected_emotion'].str.lower() == emotion.lower()]

            if age_group:
                filtered = filtered[filtered['age_group'] == age_group]
            
            if gender:
                filtered = filtered[filtered['gender'] == gender]
            
            if filtered.empty:
                return pd.DataFrame()

            filtered['capped_score'] = filtered['total_score'].apply(lambda x: min(100, x))
            top_foods = filtered.sort_values('capped_score', ascending=False)
            
            return top_foods.head(limit)
            
        except Exception as e:
            logger.error(f"Error getting top rated foods: {e}")
            return pd.DataFrame()
    
    def get_foods_to_avoid(
        self,
        emotion: str,
        age_group: str = None,
        gender: str = None,
        limit: int = 10
    ) -> List[str]:
        try:
            stats = self.get_feedback_statistics()
            
            if stats.empty:
                return []

            filtered = stats[stats['detected_emotion'].str.lower() == emotion.lower()]

            if age_group:
                filtered = filtered[filtered['age_group'] == age_group]
            
            if gender:
                filtered = filtered[filtered['gender'] == gender]
            
            if filtered.empty:
                return []


            low_rated = filtered[
                (filtered['total_score'] < 10) &
                (filtered['feedback_count'] >= 3)
            ]
            
            avoid_list = low_rated.sort_values('total_score')['food_item'].head(limit).tolist()
            
            return avoid_list
            
        except Exception as e:
            logger.error(f"Error getting foods to avoid: {e}")
            return []
    
    def get_feedback_summary(self) -> Dict:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM feedback")
            total_feedback = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM feedback WHERE rating >= 4")
            positive_feedback = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM feedback WHERE rating <= 2")
            negative_feedback = cursor.fetchone()[0]

            cursor.execute()
            emotion_feedback = dict(cursor.fetchall())
            
            conn.close()
            
            summary = {
                'total_feedback': total_feedback,
                'positive_feedback': positive_feedback,
                'negative_feedback': negative_feedback,
                'neutral_feedback': total_feedback - positive_feedback - negative_feedback,
                'positive_rate': (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0,
                'emotion_breakdown': emotion_feedback
            }
            
            logger.info(f"Generated feedback summary: {total_feedback} total feedbacks")
            return summary
            
        except Exception as e:
            logger.error(f"Error getting feedback summary: {e}")
            return {
                'total_feedback': 0,
                'positive_feedback': 0,
                'negative_feedback': 0,
                'neutral_feedback': 0,
                'positive_rate': 0,
                'emotion_breakdown': {}
            }
    
    def has_sufficient_feedback(self, min_feedback: int = 10) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM feedback")
            count = cursor.fetchone()[0]
            
            conn.close()
            
            return count >= min_feedback
            
        except Exception as e:
            logger.error(f"Error checking feedback count: {e}")
            return False

if __name__ == "__main__":
    from database import Database
    
    db = Database()
    analyzer = FeedbackAnalyzer(db)

    stats = analyzer.get_feedback_statistics()
    print(f"\nFeedback Statistics:\n{stats}")

    score = analyzer.get_food_score("Biryani", "Happy", "Gen Z", "Female")
    print(f"\nBiryani cumulative score for Happy Gen Z Female: {score}/100")

    top_foods = analyzer.get_top_rated_foods("Happy", "Gen Z", "Female")
    print(f"\nTop rated foods for Happy Gen Z Female:\n{top_foods}")

    summary = analyzer.get_feedback_summary()
    print(f"\nFeedback Summary:\n{summary}")
