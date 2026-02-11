import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)

MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

FOOD_DATA_PATH = os.path.join(DATA_DIR, 'food_data.csv')
DATABASE_PATH = os.path.join(DB_DIR, 'food_recommendation.db')


EMOTION_MODEL = 'deepface'  

CUSTOM_MODEL_PATH = os.path.join(MODELS_DIR, 'best_emotion_model.h5')
MODEL_INPUT_SIZE = (48, 48)  # Input size for custom model

EMOTIONS = [
    'happy',
    'sad',
    'angry',
    'neutral',
    'surprise',
    'fear',
    'disgust'
]

EMOTION_DISPLAY_NAMES = {
    'happy': 'Happy',
    'sad': 'Sad',
    'angry': 'Angry',
    'neutral': 'Neutral',
    'surprise': 'Surprise',
    'fear': 'Fear',
    'disgust': 'Disgust'
}

EMOTION_TO_FOOD_MOOD = {
    'happy': 'Happy',
    'sad': 'Sad',
    'angry': 'Angry',
    'neutral': 'Neutral',
    'surprise': 'Surprise',
    'fear': 'Fear',
    'disgust': 'Disgust'
}


EMOTION_DETECTION_DURATION = 5  # seconds
EMOTION_CONFIDENCE_THRESHOLD = 30.0  # minimum confidence percentage

AGE_GROUPS = [
    '18-25',
    '26-35',
    '36-45',
    '46+'
]


GENDERS = [
    'Male',
    'Female',
    'Other'
]


DIET_PREFERENCES = [
    'Veg',
    'NonVeg',
    'Both'
]


CUISINE_TYPES = [
    'Indian',
    'Chinese',
    'Italian',
    'Mexican',
    'Continental',
    'Thai',
    'Japanese',
    'Mediterranean',
    'American',
    'Korean'
]


INDIAN_STATES = [
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal'
]

DEFAULT_RECOMMENDATION_COUNT = 4

MIN_RECOMMENDATIONS = 5

MAX_RECOMMENDATIONS = 10

SCORING_WEIGHTS = {
    'mood_match': 0.7,
    'cuisine_preference': 0.1,
    'location_preference': 0.1,
    'dietary_preference': 0.1
}

HAAR_CASCADE_PATH = 'haarcascade_frontalface_default.xml'

CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30


DEEPFACE_DETECTOR_BACKEND = 'opencv'

DEEPFACE_MODEL = 'VGG-Face'

ENFORCE_DETECTION = False
PAGE_TITLE = "AI Food Recommendation System"
PAGE_ICON = "🍽️"
LAYOUT = "wide"


PRIMARY_COLOR = "#FF6347"
SECONDARY_COLOR = "#4CAF50"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#333333"

DB_TIMEOUT = 20
DB_CHECK_SAME_THREAD = False

LOG_LEVEL = 'INFO'


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


LOG_FILE_PATH = os.path.join(BASE_DIR, 'app.log')

ENABLE_WEBCAM_DETECTION = True
ENABLE_USER_HISTORY = True
ENABLE_FEEDBACK = True
ENABLE_ANALYTICS = True
ENABLE_PDF_EXPORT = False  # Not implemented yet
ENABLE_ADMIN_PANEL = False  # Not implemented yet

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 50
MIN_CITY_LENGTH = 2
MAX_CITY_LENGTH = 50

API_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 3

ERROR_MESSAGES = {
    'camera_not_found': 'Camera not accessible. Please check permissions.',
    'data_not_found': 'Food data CSV not found. Please add food_data.csv to data/ folder.',
    'no_recommendations': 'No recommendations found. Try adjusting your preferences.',
    'invalid_input': 'Please fill in all required fields.',
    'emotion_detection_failed': 'Could not detect emotion. Please try again.',
    'database_error': 'Database error occurred. Please try again.'
}


SUCCESS_MESSAGES = {
    'emotion_detected': 'Emotion detected successfully!',
    'recommendations_generated': 'Recommendations generated!',
    'feedback_saved': 'Thank you for your feedback!',
    'user_saved': 'User information saved successfully!'
}

FOOD_CATEGORIES = [
    'Appetizer',
    'Main Course',
    'Dessert',
    'Beverage',
    'Snack',
    'Breakfast',
    'Lunch',
    'Dinner',
    'Salad',
    'Soup',
    'Street Food',
    'Fast Food',
    'Healthy',
    'Comfort Food'
]





PDF_FONT_SIZE = 12
PDF_TITLE_FONT_SIZE = 18
PDF_MARGIN = 20





DEBUG_MODE = False


SHOW_ERROR_DETAILS = True


CACHE_TIMEOUT = 3600





MAX_CONCURRENT_USERS = 100


SESSION_TIMEOUT = 30


DATA_REFRESH_INTERVAL = 300




def validate_config():
    
    errors = []
    

    if not os.path.exists(DATA_DIR):
        errors.append(f"Data directory not found: {DATA_DIR}")
    

    if not os.path.exists(FOOD_DATA_PATH):
        errors.append(f"Food data CSV not found: {FOOD_DATA_PATH}")
    

    if not EMOTIONS:
        errors.append("EMOTIONS list is empty")
    

    if not AGE_GROUPS:
        errors.append("AGE_GROUPS list is empty")
    
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True



if __name__ == "__main__":
    print("=== Configuration Validation ===")
    if validate_config():
        print("✓ Configuration is valid")
    else:
        print("✗ Configuration has errors")
    
    print("\n=== Configuration Summary ===")
    print(f"Data Path: {FOOD_DATA_PATH}")
    print(f"Database Path: {DATABASE_PATH}")
    print(f"Supported Emotions: {', '.join(EMOTIONS)}")
    print(f"Supported Cuisines: {', '.join(CUISINE_TYPES)}")
    print(f"Default Recommendations: {DEFAULT_RECOMMENDATION_COUNT}")