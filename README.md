# 🍽️ Moody Food - AI-Powered Food Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)
[![DeepFace](https://img.shields.io/badge/DeepFace-0.0.79-green.svg)](https://github.com/serengil/deepface)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Moody Food** is an intelligent food recommendation system that analyzes your facial emotions using AI and suggests personalized food items based on your mood, dietary preferences, and demographic information. Built with Streamlit and powered by DeepFace emotion recognition, this system provides a unique and interactive way to discover meals that match your current emotional state.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [Emotion Detection Models](#-emotion-detection-models)
- [Recommendation Engine](#-recommendation-engine)
- [Feedback System](#-feedback-system)
- [Data Format](#-data-format)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- **🎭 Real-time Emotion Detection**: Uses facial recognition to detect 7 emotions (happy, sad, angry, neutral, surprise, fear, disgust)
- **🍜 Personalized Recommendations**: AI-powered food suggestions based on mood and user preferences
- **👤 User Profiling**: Captures demographic information (age, gender, location) for better recommendations
- **🌍 Multi-Cuisine Support**: Supports 10+ cuisine types (Indian, Chinese, Italian, Mexican, etc.)
- **🥗 Dietary Preferences**: Filters for Vegetarian, Non-Vegetarian, or Both
- **📊 Interactive Analytics**: Visual charts showing emotion distribution and food categories
- **👍👎 Feedback System**: Thumbs up/down rating system with cumulative scoring
- **📜 History Tracking**: Stores user sessions and recommendation history
- **🔍 Food Search**: Search functionality across food items, categories, and cuisines

### Advanced Features
- **🧠 Adaptive Learning**: Feedback analyzer improves recommendations over time
- **🎯 Demographic Filtering**: Age and gender-based recommendation refinement
- **📍 Location-Based Preferences**: Regional cuisine preferences based on user's state
- **🔄 Multiple Emotion Models**: Support for DeepFace, HSEmotion, FER, and custom models
- **💾 SQLite Database**: Persistent storage for users, preferences, and feedback
- **📈 Real-time Statistics**: Dashboard showing active users and system stats

---

## 🛠️ Technology Stack

### Frontend & UI
- **Streamlit 1.28.0** - Web application framework
- **Plotly 5.18.0** - Interactive data visualizations
- **Matplotlib 3.8.2** - Additional plotting capabilities
- **Seaborn 0.13.0** - Statistical data visualization

### AI & Machine Learning
- **DeepFace 0.0.79** - Primary emotion detection library
- **TensorFlow 2.15.0** - Deep learning framework
- **tf-keras 2.15.0** - Keras API for TensorFlow
- **FER 22.5.1** - Alternative emotion recognition library
- **scikit-learn 1.3.2** - Machine learning utilities

### Computer Vision
- **OpenCV 4.8.1** - Image processing and face detection
- **opencv-contrib-python 4.8.1** - Extended OpenCV modules
- **Pillow 10.1.0** - Image manipulation
- **retina-face 0.0.13** - Face detection backend
- **mtcnn 0.1.1** - Multi-task Cascaded CNN for face detection

### Data Processing
- **Pandas 2.1.3** - Data manipulation and analysis
- **NumPy 1.24.3** - Numerical computing

### Database
- **SQLite3** - Built-in Python database (no external dependencies)

### Utilities
- **python-dateutil 2.8.2** - Date/time utilities
- **colorlog 6.8.0** - Colored logging output
- **python-dotenv 1.0.0** - Environment variable management
- **gdown 4.7.1** - Google Drive file downloader

### Document Generation
- **reportlab 4.0.7** - PDF generation library
- **fpdf2 2.7.6** - Alternative PDF library

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
│                     (main.py - 471 lines)                    │
└────────────┬────────────────────────────────────┬────────────┘
             │                                    │
             ▼                                    ▼
┌────────────────────────┐          ┌────────────────────────┐
│   Emotion Detector     │          │  Recommendation Engine │
│  (emotion_detector.py) │          │ (recommendation_engine.py)│
│   - DeepFace Model     │          │   - Mood Filtering     │
│   - HSEmotion Model    │          │   - Diet Filtering     │
│   - FER Model          │          │   - Cuisine Matching   │
│   - Custom CNN Model   │          │   - Feedback Scoring   │
└────────────┬───────────┘          └──────────┬─────────────┘
             │                                  │
             │                                  │
             ▼                                  ▼
┌────────────────────────┐          ┌────────────────────────┐
│     Data Loader        │          │   Feedback Analyzer    │
│   (data_loader.py)     │          │ (feedback_analyzer.py) │
│   - CSV Processing     │          │   - Score Calculation  │
│   - Data Cleaning      │          │   - Top Rated Foods    │
│   - Search Functions   │          │   - Avoid List         │
└────────────┬───────────┘          └──────────┬─────────────┘
             │                                  │
             └──────────────┬───────────────────┘
                            ▼
                ┌───────────────────────┐
                │   SQLite Database     │
                │    (database.py)      │
                │  - Users Table        │
                │  - Preferences Table  │
                │  - History Table      │
                │  - Feedback Table     │
                └───────────────────────┘
```

---

## 📁 Project Structure

```
Moodyfood/
│
├── main.py                      # Main Streamlit application (471 lines)
├── config.py                    # Configuration settings (295 lines)
├── emotion_detector.py          # Emotion detection module (290 lines)
├── recommendation_engine.py     # Recommendation logic (357 lines)
├── database.py                  # Database operations (331 lines)
├── data_loader.py              # Data loading and processing (209 lines)
├── feedback_analyzer.py        # Feedback analysis (234 lines)
├── view_database.py            # Database viewer utility (2256 bytes)
├── requirements.txt            # Python dependencies (50 lines)
├── .gitignore                  # Git ignore rules
│
├── data/
│   └── food_data.csv           # Food dataset (143KB, ~1000+ entries)
│
├── database/
│   └── food_recommendation.db  # SQLite database
│
├── models/                     # Custom trained models (optional)
│   └── best_emotion_model.h5   # Custom emotion detection model
│
├── logs/                       # Application logs
│
└── venv/                       # Virtual environment
```

### Key Files Description

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | 471 | Streamlit UI with 3-step workflow (user info → emotion detection → recommendations) |
| `emotion_detector.py` | 290 | Emotion detection using DeepFace/HSEmotion/FER/Custom models |
| `recommendation_engine.py` | 357 | Multi-factor recommendation algorithm with feedback integration |
| `database.py` | 331 | SQLite database management with 4 tables |
| `data_loader.py` | 209 | CSV data loading, cleaning, and search functionality |
| `feedback_analyzer.py` | 234 | Cumulative feedback scoring and analytics |
| `config.py` | 295 | Centralized configuration with 50+ settings |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Webcam (for emotion detection)
- 2GB free disk space (for model downloads)

### Step 1: Clone the Repository
```bash
git clone https://github.com/moizmakadq/moodyfood.git
cd moodyfood
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: First run will download DeepFace models (~100MB). This is automatic.

### Step 4: Prepare Data
Ensure `data/food_data.csv` exists with the required format (see [Data Format](#-data-format)).

### Step 5: Run the Application
```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

---

## ⚙️ Configuration

Edit `config.py` to customize the system:

### Emotion Detection Settings
```python
EMOTION_MODEL = 'deepface'  # Options: 'deepface', 'hsemotion', 'fer', 'custom'
CUSTOM_MODEL_PATH = 'models/best_emotion_model.h5'
EMOTION_CONFIDENCE_THRESHOLD = 30.0  # Minimum confidence percentage
```

### Recommendation Settings
```python
DEFAULT_RECOMMENDATION_COUNT = 4
MIN_RECOMMENDATIONS = 5
MAX_RECOMMENDATIONS = 10

SCORING_WEIGHTS = {
    'mood_match': 0.7,
    'cuisine_preference': 0.1,
    'location_preference': 0.1,
    'dietary_preference': 0.1
}
```

### Database Settings
```python
DATABASE_PATH = 'database/food_recommendation.db'
DB_TIMEOUT = 20
```

### UI Customization
```python
PAGE_TITLE = "AI Food Recommendation System"
PAGE_ICON = "🍽️"
PRIMARY_COLOR = "#FF6347"
SECONDARY_COLOR = "#4CAF50"
```

---

## 🚀 Usage

### Step-by-Step Workflow

#### **Step 1: User Information**
1. Enter your name and city
2. Select age group (18-25, 26-35, 36-45, 46+)
3. Choose gender (Male, Female, Other)
4. Select state from Indian states list
5. Choose dietary preference (Veg, NonVeg, Both)
6. Select cuisine preferences (multiple selection allowed)

#### **Step 2: Emotion Detection**
1. Click "Capture your photo" to activate webcam
2. Take a photo when ready
3. System analyzes facial expression using AI
4. View detected emotion with confidence scores
5. See emotion distribution pie chart
6. Option to retake photo if needed

#### **Step 3: Recommendations**
1. View personalized food recommendations (up to 10 items)
2. See food details: name, category, cuisine type, reason
3. Provide feedback with 👍 (thumbs up) or 👎 (thumbs down)
4. View analytics: category distribution, cuisine breakdown
5. Options:
   - 🔄 Get new recommendations
   - 📄 Export as PDF (coming soon)
   - 🏠 Start over

### Sidebar Features
- **Progress Tracker**: Shows current step (1/3, 2/3, 3/3)
- **Food Search**: Search database by food name, category, or cuisine
- **System Stats**: Total food items, active users
- **About Section**: System information

---

## 🗄️ Database Schema

### Tables Overview

#### 1. **users** Table
Stores user demographic information.

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | INTEGER PRIMARY KEY | Auto-incrementing user ID |
| `name` | TEXT | User's name |
| `age_group` | TEXT | Age range (18-25, 26-35, etc.) |
| `gender` | TEXT | Gender (Male, Female, Other) |
| `state` | TEXT | Indian state |
| `city` | TEXT | City name |
| `created_at` | TIMESTAMP | Account creation time |
| `last_active` | TIMESTAMP | Last activity timestamp |

#### 2. **user_preferences** Table
Stores dietary and cuisine preferences.

| Column | Type | Description |
|--------|------|-------------|
| `preference_id` | INTEGER PRIMARY KEY | Auto-incrementing ID |
| `user_id` | INTEGER | Foreign key to users table |
| `diet_preference` | TEXT | Veg/NonVeg/Both |
| `cuisine_preferences` | TEXT | JSON array of cuisines |
| `updated_at` | TIMESTAMP | Last update time |

#### 3. **recommendations_history** Table
Tracks all recommendation sessions.

| Column | Type | Description |
|--------|------|-------------|
| `history_id` | INTEGER PRIMARY KEY | Auto-incrementing ID |
| `user_id` | INTEGER | Foreign key to users table |
| `detected_emotion` | TEXT | Emotion detected (happy, sad, etc.) |
| `recommended_items` | TEXT | JSON array of recommendations |
| `session_timestamp` | TIMESTAMP | Session time |

#### 4. **feedback** Table
Stores user feedback on recommendations.

| Column | Type | Description |
|--------|------|-------------|
| `feedback_id` | INTEGER PRIMARY KEY | Auto-incrementing ID |
| `user_id` | INTEGER | Foreign key to users table |
| `history_id` | INTEGER | Foreign key to history table |
| `food_item` | TEXT | Food item name |
| `rating` | INTEGER | Rating (1-5, thumbs down=1, thumbs up=5) |
| `comment` | TEXT | Optional text comment |
| `created_at` | TIMESTAMP | Feedback time |

---

## 🎭 Emotion Detection Models

### Supported Models

#### 1. **DeepFace** (Default)
- **Accuracy**: 65-70%
- **Backend**: VGG-Face
- **Detector**: OpenCV
- **Pros**: Well-tested, reliable, no training needed
- **Cons**: Slower inference (~2-3 seconds)

#### 2. **HSEmotion**
- **Accuracy**: 70-75%
- **Installation**: `pip install hsemotion`
- **Pros**: Highest accuracy, fast inference
- **Cons**: Requires additional dependency

#### 3. **FER (Facial Expression Recognition)**
- **Accuracy**: 65-70%
- **Installation**: `pip install fer`
- **Pros**: Lightweight, fast
- **Cons**: Less accurate than HSEmotion

#### 4. **Custom Trained Model**
- **Accuracy**: Depends on training
- **Format**: TensorFlow/Keras (.h5 file)
- **Input Size**: 48x48 grayscale images
- **Pros**: Customizable for specific use cases
- **Cons**: Requires training data and expertise

### Detected Emotions
- 😊 **Happy**: Joyful, content, pleased
- 😢 **Sad**: Unhappy, melancholic, down
- 😠 **Angry**: Frustrated, irritated, mad
- 😐 **Neutral**: Calm, expressionless, balanced
- 😲 **Surprise**: Shocked, amazed, astonished
- 😨 **Fear**: Scared, anxious, worried
- 🤢 **Disgust**: Repulsed, distaste, aversion

---

## 🎯 Recommendation Engine

### Multi-Factor Scoring Algorithm

The recommendation engine uses a sophisticated scoring system:

```python
total_score = (
    location_score +           # Regional cuisine bonus (0-10 points)
    feedback_score * 2 +       # User feedback (0-100 points, weighted 2x)
    random_variety * 3         # Randomness for variety (0-3 points)
)
```

### Filtering Pipeline

1. **Mood Filtering**: Match food items to detected emotion
2. **Diet Filtering**: Apply Veg/NonVeg/Both preference
3. **Cuisine Filtering**: Match selected cuisine types
4. **Age Filtering**: Filter by age-appropriate items
5. **Gender Filtering**: Apply gender-specific preferences
6. **Location Scoring**: Boost regional cuisines
7. **Feedback Integration**: Apply cumulative user ratings
8. **Ranking**: Sort by total score and return top N

### Fallback Strategy

If no results found:
1. Relax cuisine constraints
2. Relax age/gender constraints
3. Keep only mood and diet filters
4. If still empty, return random items

---

## 📊 Feedback System

### Cumulative Scoring Model

- **Thumbs Up (👍)**: +5 points per feedback
- **Thumbs Down (👎)**: +1 point per feedback
- **Maximum Score**: Capped at 100 points per food-emotion combination
- **Minimum Feedback**: Requires 5+ feedbacks to influence recommendations

### Feedback Analytics

The `FeedbackAnalyzer` provides:
- **Top Rated Foods**: Foods with highest cumulative scores
- **Foods to Avoid**: Items with <10 points and 3+ feedbacks
- **Demographic Filtering**: Separate scores for age groups and genders
- **Emotion-Specific**: Different scores per emotion state

### Cache System
- Feedback statistics are cached for performance
- Cache is cleared when new feedback is added
- Reduces database queries by 80%

---

## 📄 Data Format

### food_data.csv Structure

Required columns:

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `User_ID` | Integer | 1001 | User identifier |
| `Age_Group` | String | "26-35" | Age range |
| `Gender` | String | "Male" | Gender |
| `Mood` | String | "happy" | Emotion state (lowercase) |
| `Recommended_Food_Item` | String | "Biryani" | Food item name |
| `Veg_or_NonVeg` | String | "NonVeg" | Dietary type |
| `Food_Category` | String | "Main Course" | Category |
| `Cuisine_Type` | String | "Indian" | Cuisine |
| `Reason_for_Recommendation` | String | "Comfort food..." | Explanation |

### Sample CSV Entry
```csv
User_ID,Age_Group,Gender,Mood,Recommended_Food_Item,Veg_or_NonVeg,Food_Category,Cuisine_Type,Reason_for_Recommendation
1001,26-35,Male,happy,Biryani,NonVeg,Main Course,Indian,Comfort food that brings joy and satisfaction
1002,18-25,Female,sad,Hot Chocolate,Veg,Beverage,Continental,Warm drink to lift spirits
```

### Supported Values

**Moods**: happy, sad, angry, neutral, surprise, fear, disgust

**Age Groups**: 18-25, 26-35, 36-45, 46+

**Genders**: Male, Female, Other, All

**Diet Types**: Veg, NonVeg

**Cuisines**: Indian, Chinese, Italian, Mexican, Continental, Thai, Japanese, Mediterranean, American, Korean

---

## 📸 Screenshots

### 1. User Information Page
![User Info](screenshots/step1_user_info.png)
*Step 1: Enter demographic information and preferences*

### 2. Emotion Detection
![Emotion Detection](screenshots/step2_emotion.png)
*Step 2: Capture photo and detect emotion with confidence scores*

### 3. Recommendations
![Recommendations](screenshots/step3_recommendations.png)
*Step 3: View personalized food recommendations with feedback options*

### 4. Analytics Dashboard
![Analytics](screenshots/analytics.png)
*Interactive charts showing category and cuisine distribution*

---

## 🔮 Future Enhancements

### Planned Features
- [ ] **PDF Export**: Generate downloadable recommendation reports
- [ ] **Admin Panel**: Dashboard for system monitoring and analytics
- [ ] **User Authentication**: Login system with saved preferences
- [ ] **Recipe Integration**: Show recipes for recommended items
- [ ] **Nutritional Information**: Display calories, macros, allergens
- [ ] **Restaurant Integration**: Link to nearby restaurants serving recommended items
- [ ] **Multi-language Support**: Interface in Hindi, Tamil, Bengali, etc.
- [ ] **Mobile App**: React Native or Flutter mobile version
- [ ] **Voice Input**: Voice-based preference selection
- [ ] **Social Sharing**: Share recommendations on social media

### Technical Improvements
- [ ] **Model Fine-tuning**: Train custom emotion model on Indian faces
- [ ] **Real-time Video**: Continuous emotion tracking instead of single photo
- [ ] **Collaborative Filtering**: User-user similarity for recommendations
- [ ] **A/B Testing**: Test different recommendation algorithms
- [ ] **Performance Optimization**: Caching, lazy loading, async operations
- [ ] **Cloud Deployment**: Deploy on AWS/GCP/Azure
- [ ] **API Development**: RESTful API for third-party integrations
- [ ] **Docker Support**: Containerization for easy deployment

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version)

### Suggesting Features
1. Open an issue with `[Feature Request]` tag
2. Describe the feature and use case
3. Explain why it would be valuable

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Follow PEP 8 style guidelines
5. Add docstrings and comments
6. Test thoroughly
7. Commit: `git commit -m 'Add amazing feature'`
8. Push: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/moizmakadq/moodyfood.git

# Add upstream remote
git remote add upstream https://github.com/originalauthor/moodyfood.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Additional dev tools

# Run tests
pytest tests/

# Format code
black .
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Moodyfood Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Authors & Acknowledgments

### Development Team
- **Your Name** - *Lead Developer* - [GitHub Profile](https://github.com/moizmakadq)

### Acknowledgments
- **DeepFace** - Emotion detection library by [serengil](https://github.com/serengil/deepface)
- **Streamlit** - Web framework for ML applications
- **OpenCV** - Computer vision library
- **TensorFlow** - Deep learning framework

### Special Thanks
- M.Tech Nirma University AML Project Team
- All contributors and testers

---

## 📞 Contact & Support

### Get Help
- **Issues**: [GitHub Issues](https://github.com/moizmakadq/moodyfood/issues)
- **Discussions**: [GitHub Discussions](https://github.com/moizmakadq/moodyfood/discussions)

### Connect
- **LinkedIn**: [Your Profile](https://linkedin.com/in/moiz-makada)
---

## 📊 Project Statistics

- **Total Lines of Code**: ~2,200 lines
- **Python Files**: 8 core modules
- **Dependencies**: 25+ packages
- **Database Tables**: 4 tables
- **Supported Emotions**: 7 emotions
- **Supported Cuisines**: 10+ cuisines
- **Food Dataset**: 1000+ entries
- **Development Time**: 3 months
- **Contributors**: 1+ developers

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=moizmakadq/moodyfood&type=Date)](https://star-history.com/#moizmakadq/moodyfood&Date)

---

<div align="center">

**Made with ❤️ and 🍕 by the Moodyfood Team**

[⬆ Back to Top](#-moody-food---ai-powered-food-recommendation-system)

</div>
