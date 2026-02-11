import sqlite3
import pandas as pd
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('database/food_recommendation.db')

print("=" * 60)
print("MOODYFOOD DATABASE VIEWER")
print("=" * 60)

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nAvailable Tables:")
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "=" * 60)
print("USERS")
print("=" * 60)
users = pd.read_sql("SELECT * FROM users", conn)
print(users.to_string())

print("\n" + "=" * 60)
print("FEEDBACK")
print("=" * 60)
feedback_query = 
try:
    feedback = pd.read_sql(feedback_query, conn)
    print(feedback.to_string())
except:
    print("No feedback data yet")

print("\n" + "=" * 60)
print("RECOMMENDATIONS HISTORY")
print("=" * 60)
history_query = 
try:
    history = pd.read_sql(history_query, conn)
    print(history.to_string())
except:
    print("No recommendation history yet")

print("\n" + "=" * 60)
print("STATISTICS")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"Total Users: {user_count}")

cursor.execute("SELECT COUNT(*) FROM recommendations_history")
rec_count = cursor.fetchone()[0]
print(f"Total Recommendations: {rec_count}")

cursor.execute("SELECT COUNT(*) FROM feedback")
feedback_count = cursor.fetchone()[0]
print(f"Total Feedbacks: {feedback_count}")

if feedback_count > 0:
    cursor.execute("SELECT COUNT(*) FROM feedback WHERE rating >= 4")
    positive = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM feedback WHERE rating <= 2")
    negative = cursor.fetchone()[0]
    
    print(f"\nFeedback Breakdown:")
    print(f"  Positive (👍): {positive} ({positive/feedback_count*100:.1f}%)")
    print(f"  Negative (👎): {negative} ({negative/feedback_count*100:.1f}%)")
    print(f"  Neutral (😐): {feedback_count - positive - negative}")

    print("\nFeedback by Emotion:")
    emotion_stats = pd.read_sql(, conn)
    print(emotion_stats.to_string())

conn.close()
print("\n" + "=" * 60)
print("✅ Database viewer completed!")
print("=" * 60)
