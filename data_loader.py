import pandas as pd
import numpy as np
import logging
import os
import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, data_path: str = config.FOOD_DATA_PATH):
        self.data_path = data_path
        self.food_data = None
        self.load_data()
        logger.info("Data Loader initialized")
    
    def load_data(self):
        
        try:
            if not os.path.exists(self.data_path):
                logger.warning(f"Data file not found at {self.data_path}")
                raise FileNotFoundError(f"Food data CSV not found at {self.data_path}")
            

            self.food_data = pd.read_csv(self.data_path)
            

            required_columns = [
                'User_ID', 'Age_Group', 'Gender', 'Mood',
                'Recommended_Food_Item', 'Veg_or_NonVeg',
                'Food_Category', 'Cuisine_Type',
                'Reason_for_Recommendation'
            ]
            
            missing_columns = [
                col for col in required_columns 
                if col not in self.food_data.columns
            ]
            
            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )
            

            self.food_data = self.clean_data(self.food_data)
            
            logger.info(f"Loaded {len(self.food_data)} food items from CSV")
            logger.info(f"Columns: {list(self.food_data.columns)}")
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            logger.info("Please ensure food_data.csv is in the data/ directory")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.drop_duplicates()
        

        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].str.strip()
        

        df = df.dropna(subset=['Recommended_Food_Item', 'Mood'])
        

        df['Reason_for_Recommendation'] = df['Reason_for_Recommendation'].fillna(
            'Recommended based on your preferences'
        )
        

        df['Mood'] = df['Mood'].str.lower()
        

        df['Veg_or_NonVeg'] = df['Veg_or_NonVeg'].str.title()
        
        logger.info(f"Data cleaned: {len(df)} records remaining")
        return df
    
    def get_food_by_mood(self, mood: str) -> pd.DataFrame:
        mood_lower = mood.lower()
        return self.food_data[
            self.food_data['Mood'].str.lower() == mood_lower
        ]
    
    def get_food_by_category(self, category: str) -> pd.DataFrame:
        return self.food_data[
            self.food_data['Food_Category'].str.lower() == category.lower()
        ]
    
    def get_food_by_cuisine(self, cuisine: str) -> pd.DataFrame:
        return self.food_data[
            self.food_data['Cuisine_Type'].str.lower() == cuisine.lower()
        ]
    
    def search_food(self, query: str) -> pd.DataFrame:
        query_lower = query.lower()
        mask = (
            self.food_data['Recommended_Food_Item'].str.lower().str.contains(query_lower, na=False) |
            self.food_data['Food_Category'].str.lower().str.contains(query_lower, na=False) |
            self.food_data['Cuisine_Type'].str.lower().str.contains(query_lower, na=False)
        )
        
        return self.food_data[mask]
    
    def get_unique_values(self, column: str) -> list:
        if column in self.food_data.columns:
            return sorted(self.food_data[column].unique().tolist())
        return []
    
    def get_statistics(self) -> dict:
        stats = {
            'total_items': len(self.food_data),
            'unique_items': self.food_data['Recommended_Food_Item'].nunique(),
            'moods': self.food_data['Mood'].nunique(),
            'categories': self.food_data['Food_Category'].nunique(),
            'cuisines': self.food_data['Cuisine_Type'].nunique(),
            'veg_items': len(self.food_data[self.food_data['Veg_or_NonVeg'] == 'Veg']),
            'non_veg_items': len(self.food_data[self.food_data['Veg_or_NonVeg'] == 'NonVeg'])
        }
        return stats
    
    def get_mood_distribution(self) -> pd.Series:
        
        return self.food_data['Mood'].value_counts()
    
    def get_cuisine_distribution(self) -> pd.Series:
        
        return self.food_data['Cuisine_Type'].value_counts()
    
    def get_category_distribution(self) -> pd.Series:
        
        return self.food_data['Food_Category'].value_counts()
    
    def filter_data(self, filters: dict) -> pd.DataFrame:
        filtered_df = self.food_data.copy()
        
        for column, value in filters.items():
            if column in filtered_df.columns:
                if isinstance(value, list):

                    filtered_df = filtered_df[
                        filtered_df[column].str.lower().isin(
                            [v.lower() for v in value]
                        )
                    ]
                else:

                    filtered_df = filtered_df[
                        filtered_df[column].str.lower() == value.lower()
                    ]
        return filtered_df
    def get_random_items(self, n: int = 10) -> pd.DataFrame:
        return self.food_data.sample(n=min(n, len(self.food_data)))
    
    def reload_data(self):
        logger.info("Reloading data from CSV...")
        self.load_data()



if __name__ == "__main__":
    try:
        loader = DataLoader()
        
        print("\n=== Dataset Statistics ===")
        stats = loader.get_statistics()
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        print("\n=== Mood Distribution ===")
        print(loader.get_mood_distribution())
        
        print("\n=== Sample Food Items ===")
        print(loader.get_random_items(5)[
            ['Recommended_Food_Item', 'Mood', 'Cuisine_Type', 'Veg_or_NonVeg']
        ])
        
        print("\n=== Search Test ===")
        results = loader.search_food('pizza')
        print(f"Found {len(results)} items matching 'pizza'")
        
        print("\n=== Filter Test ===")
        filtered = loader.filter_data({
            'Mood': 'happy',
            'Veg_or_NonVeg': 'Veg'
        })
        print(f"Found {len(filtered)} vegetarian items for happy mood")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease ensure food_data.csv exists in the data/ directory")
        print("The CSV should have these columns:")
        print("- User_ID")
        print("- Age_Group")
        print("- Gender")
        print("- Mood")
        print("- Recommended_Food_Item")
        print("- Veg_or_NonVeg")
        print("- Food_Category")
        print("- Cuisine_Type")
        print("- Reason_for_Recommendation")