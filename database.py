import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = config.DATABASE_PATH):

        self.db_path = db_path
        self.conn = None
        self.create_connection()
        self.create_tables()
        logger.info(f"Database initialized at {db_path}")
    
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            logger.info("Database connection established")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            

            cursor.execute()
            

            cursor.execute()
            

            cursor.execute()
            

            cursor.execute()
            
            self.conn.commit()
            logger.info("Database tables created successfully")
            
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def save_user(self, user_data: Dict) -> int:

        try:
            cursor = self.conn.cursor()
            

            cursor.execute(
                "SELECT user_id FROM users WHERE name = ? AND city = ?",
                (user_data['name'], user_data.get('city', ''))
            )
            existing_user = cursor.fetchone()
            
            if existing_user:

                user_id = existing_user[0]
                cursor.execute( (
                    user_data.get('age_group'),
                    user_data.get('gender'),
                    user_data.get('state'),
                    user_id
                ))
                logger.info(f"Updated existing user: {user_id}")
            else:

                cursor.execute(, (
                    user_data['name'],
                    user_data.get('age_group'),
                    user_data.get('gender'),
                    user_data.get('state'),
                    user_data.get('city')
                ))
                user_id = cursor.lastrowid
                logger.info(f"Created new user: {user_id}")
            

            self.save_user_preferences(user_id, user_data)
            
            self.conn.commit()
            return user_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving user: {e}")
            self.conn.rollback()
            return -1
    
    def save_user_preferences(self, user_id: int, user_data: Dict):
        try:
            cursor = self.conn.cursor()
            

            cuisine_prefs = json.dumps(user_data.get('cuisine_preferences', []))
            

            cursor.execute(
                "SELECT preference_id FROM user_preferences WHERE user_id = ?",
                (user_id,)
            )
            existing_pref = cursor.fetchone()
            
            if existing_pref:

                cursor.execute(, (
                    user_data.get('diet_preference'),
                    cuisine_prefs,
                    user_id
                ))
            else:

                cursor.execute(, (
                    user_id,
                    user_data.get('diet_preference'),
                    cuisine_prefs
                ))
            
            self.conn.commit()
            logger.info(f"Saved preferences for user: {user_id}")
            
        except sqlite3.Error as e:
            logger.error(f"Error saving preferences: {e}")
            self.conn.rollback()
    
    def save_recommendation_history(
        self,
        user_id: int,
        emotion: str,
        recommendations: pd.DataFrame
    ) -> int:
        try:
            cursor = self.conn.cursor()
            

            rec_json = recommendations.to_json(orient='records')
            
            cursor.execute(, (user_id, emotion, rec_json))
            
            history_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"Saved recommendation history: {history_id}")
            return history_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving history: {e}")
            self.conn.rollback()
            return -1
    
    def save_feedback(
        self,
        user_id: int,
        history_id: int,
        food_item: str,
        rating: int,
        comment: str = ""
    ):
        try:
            cursor = self.conn.cursor()
            
            cursor.execute(, (user_id, history_id, food_item, rating, comment))
            
            self.conn.commit()
            logger.info(f"Saved feedback for item: {food_item}")
            
        except sqlite3.Error as e:
            logger.error(f"Error saving feedback: {e}")
            self.conn.rollback()
    
    def get_user_history(self, user_id: int) -> List[Dict]:
        try:
            cursor = self.conn.cursor()
            
            cursor.execute(, (user_id,))
            
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    'history_id': row['history_id'],
                    'emotion': row['detected_emotion'],
                    'recommendations': json.loads(row['recommended_items']),
                    'timestamp': row['session_timestamp']
                })
            
            return history
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching history: {e}")
            return []
    
    def get_user_by_name(self, name: str) -> Optional[Dict]:
        try:
            cursor = self.conn.cursor()
            
            cursor.execute(
                "SELECT * FROM users WHERE name = ? ORDER BY last_active DESC",
                (name,)
            )
            
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching user: {e}")
            return None
    
    def get_user_count(self) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            logger.error(f"Error getting user count: {e}")
            return 0
    
    def get_total_recommendations(self) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM recommendations_history")
            count = cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            logger.error(f"Error getting recommendation count: {e}")
            return 0
    
    def get_emotion_statistics(self) -> Dict:
        try:
            cursor = self.conn.cursor()
            
            cursor.execute()
            
            rows = cursor.fetchall()
            
            stats = {}
            for row in rows:
                stats[row['detected_emotion']] = row['count']
            
            return stats
            
        except sqlite3.Error as e:
            logger.error(f"Error getting emotion stats: {e}")
            return {}
    
    def get_all_feedback(self) -> List[Dict]:
        try:
            cursor = self.conn.cursor()
            
            cursor.execute()
            
            rows = cursor.fetchall()
            
            feedback_list = []
            for row in rows:
                feedback_list.append({
                    'feedback_id': row['feedback_id'],
                    'user_id': row['user_id'],
                    'history_id': row['history_id'],
                    'food_item': row['food_item'],
                    'rating': row['rating'],
                    'comment': row['comment'],
                    'created_at': row['created_at'],
                    'detected_emotion': row['detected_emotion'],
                    'age_group': row['age_group'],
                    'gender': row['gender']
                })
            
            return feedback_list
            
        except sqlite3.Error as e:
            logger.error(f"Error getting all feedback: {e}")
            return []
    
    def get_feedback_count(self) -> int:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM feedback")
            count = cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            logger.error(f"Error getting feedback count: {e}")
            return 0
    
    def close(self):
        
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")




if __name__ == "__main__":
    db = Database()

    test_user = {
        'name': 'Test User',
        'age_group': '26-35',
        'gender': 'Male',
        'state': 'Gujarat',
        'city': 'Ahmedabad',
        'diet_preference': 'Veg',
        'cuisine_preferences': ['Indian', 'Chinese']
    }
    
    user_id = db.save_user(test_user)
    print(f"Created user ID: {user_id}")

    user = db.get_user_by_name('Test User')
    print(f"Retrieved user: {user}")

    print(f"Total users: {db.get_user_count()}")
    print(f"Total recommendations: {db.get_total_recommendations()}")
    
    db.close()