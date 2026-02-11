

import os
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from emotion_detector import EmotionDetector
from recommendation_engine import RecommendationEngine
from data_loader import DataLoader
from database import Database
import config

st.set_page_config(
    page_title="Food Recommendation System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'detected_emotion' not in st.session_state:
    st.session_state.detected_emotion = None
if 'emotion_data' not in st.session_state:
    st.session_state.emotion_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

@st.cache_resource
def initialize_components():
    
    try:
        db = Database()
        data_loader = DataLoader()

        emotion_model = config.EMOTION_MODEL.lower()
        
        if emotion_model == 'hsemotion':
            try:
                st.info("🚀 Loading HSEmotion pre-trained model...")
                from pretrained_models import HSEmotionDetector
                emotion_detector = HSEmotionDetector()
                st.success("✓ HSEmotion loaded! High accuracy (70-75%), fast inference")
            except Exception as e:
                st.warning(f"⚠️ HSEmotion failed: {str(e)}")
                st.info("Install with: pip install hsemotion")
                st.info("Falling back to DeepFace...")
                emotion_detector = EmotionDetector()
        
        elif emotion_model == 'fer':
            try:
                st.info("🚀 Loading FER pre-trained model...")
                from pretrained_models import FERDetector
                emotion_detector = FERDetector()
                st.success("✓ FER loaded! Good accuracy (65-70%)")
            except Exception as e:
                st.warning(f"⚠️ FER failed: {str(e)}")
                st.info("Install with: pip install fer")
                st.info("Falling back to DeepFace...")
                emotion_detector = EmotionDetector()
        
        elif emotion_model == 'custom':
            if os.path.exists(config.CUSTOM_MODEL_PATH):
                try:
                    st.info("🚀 Loading custom trained model...")
                    emotion_detector = CustomEmotionDetector(config.CUSTOM_MODEL_PATH)
                    st.success("✓ Custom model loaded successfully!")
                except Exception as e:
                    st.warning(f"⚠️ Custom model failed: {str(e)}")
                    st.info("Falling back to DeepFace...")
                    emotion_detector = EmotionDetector()
            else:
                st.warning(f"⚠️ Custom model not found: {config.CUSTOM_MODEL_PATH}")
                st.info("Falling back to DeepFace...")
                emotion_detector = EmotionDetector()
        
        else:  # deepface or any other value
            st.info("Using DeepFace for emotion detection...")
            emotion_detector = EmotionDetector()
        
        rec_engine = RecommendationEngine(data_loader, db)
        return db, data_loader, emotion_detector, rec_engine
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        return None, None, None, None

db, data_loader, emotion_detector, rec_engine = initialize_components()

if None in [db, data_loader, emotion_detector, rec_engine]:
    st.error("❌ Failed to initialize application components!")
    st.error("Please check the following:")
    st.markdown()
    st.stop()


def main_header():
    
    st.markdown('<h1 class="main-header">🍽️ Moody Food</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Discover perfect meals based on your mood and preferences</p>', unsafe_allow_html=True)
    st.markdown("---")

def step_1_user_info():
    
    st.markdown('<h2 class="sub-header">📝 Step 1: Tell Us About Yourself</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Name", placeholder="Enter your name")
        age_group = st.selectbox("🎂 Age Group", config.AGE_GROUPS)
        gender = st.selectbox("⚧ Gender", config.GENDERS)
        state = st.selectbox("📍 State", config.INDIAN_STATES)
    
    with col2:
        city = st.text_input("🏙️ City", placeholder="Enter your city")
        diet_pref = st.selectbox("🥗 Dietary Preference", config.DIET_PREFERENCES)
        cuisine_prefs = st.multiselect("🍜 Cuisine Preferences", config.CUISINE_TYPES)
        
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➡️ Next: Detect My Mood", use_container_width=True, type="primary"):
            if name and city and cuisine_prefs:
                st.session_state.user_data = {
                    'name': name,
                    'age_group': age_group,
                    'gender': gender,
                    'state': state,
                    'city': city,
                    'diet_preference': diet_pref,
                    'cuisine_preferences': cuisine_prefs
                }
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields!")

def step_2_emotion_detection():
    
    st.markdown('<h2 class="sub-header">😊 Step 2: Let\'s Detect Your Mood</h2>', unsafe_allow_html=True)
    
    st.info("📸 We'll analyze your facial expression to understand your mood better!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎥 Emotion Detection")

        camera_input = st.camera_input("Capture your photo")
        
        if camera_input:
            try:

                with st.spinner("🔍 Analyzing your emotion..."):
                    emotion_result = emotion_detector.detect_emotion(camera_input)
                
                if emotion_result:
                    st.session_state.detected_emotion = emotion_result['dominant_emotion']
                    st.session_state.emotion_data = emotion_result

                    st.markdown(f, unsafe_allow_html=True)
                    
                    st.success("✅ Emotion detected successfully!")
            except Exception as e:
                st.error(f"Error detecting emotion: {str(e)}")
    
    with col2:
        if st.session_state.emotion_data:
            st.markdown("### 📊 Emotion Breakdown")

            emotions = st.session_state.emotion_data['all_emotions']
            fig = px.pie(
                values=list(emotions.values()),
                names=list(emotions.keys()),
                title="Emotion Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("🔄 Retake Photo", use_container_width=True):
            st.session_state.detected_emotion = None
            st.session_state.emotion_data = None
            st.rerun()
    
    with col3:
        if st.session_state.detected_emotion:
            if st.button("➡️ Get Recommendations", use_container_width=True, type="primary"):
                st.session_state.step = 3
                st.rerun()

def step_3_recommendations():
    
    st.markdown('<h2 class="sub-header">🎯 Step 3: Your Personalized Recommendations</h2>', unsafe_allow_html=True)

    if st.session_state.recommendations is None:
        with st.spinner("🔮 Finding perfect meals for you..."):
            try:
                recommendations = rec_engine.get_recommendations(
                    mood=st.session_state.detected_emotion,
                    user_data=st.session_state.user_data
                )
                st.session_state.recommendations = recommendations

                user_id = db.save_user(st.session_state.user_data)
                st.session_state.user_id = user_id  # Store for feedback
                
                history_id = db.save_recommendation_history(
                    user_id,
                    st.session_state.detected_emotion,
                    recommendations
                )
                st.session_state.history_id = history_id  # Store for feedback
                
                logger.info(f"Saved user_id: {user_id}, history_id: {history_id}")
            except Exception as e:
                st.error(f"Error getting recommendations: {str(e)}")
                logger.error(f"Error in recommendations: {e}")
                return

    
    recommendations = st.session_state.recommendations
    
    if recommendations.empty:
        st.warning("😔 No recommendations found. Try adjusting your preferences!")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🍽️ Total Recommendations", len(recommendations))
    with col2:
        veg_count = len(recommendations[recommendations['Veg_or_NonVeg'] == 'Veg'])
        st.metric("🥗 Vegetarian Options", veg_count)
    with col3:
        cuisines = recommendations['Cuisine_Type'].nunique()
        st.metric("🌍 Cuisine Types", cuisines)
    with col4:
        st.metric("😊 Your Mood", st.session_state.detected_emotion.title())
    
    st.markdown("---")

    st.markdown("### 🍴 Recommended for You")

    if 'feedback_given' not in st.session_state:
        st.session_state.feedback_given = {}
    
    for idx, row in recommendations.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f, unsafe_allow_html=True)
            
            with col2:

                food_key = f"feedback_{row['Recommended_Food_Item']}_{idx}"

                if food_key in st.session_state.feedback_given:
                    st.success(f"{st.session_state.feedback_given[food_key]} Saved!")
                else:

                    col_thumbs_up, col_thumbs_down = st.columns(2)
                    
                    with col_thumbs_up:
                        if st.button("👍", key=f"thumbs_up_{idx}", use_container_width=True):

                            if 'user_id' not in st.session_state:
                                st.error("❌ Error: user_id not found. Please restart the app.")
                                logger.error("user_id not in session_state")
                            elif 'history_id' not in st.session_state:
                                st.error("❌ Error: history_id not found. Please restart the app.")
                                logger.error("history_id not in session_state")
                            elif not db:
                                st.error("❌ Error: Database not initialized")
                                logger.error("Database is None")
                            else:

                                try:
                                    db.save_feedback(
                                        user_id=st.session_state.user_id,
                                        history_id=st.session_state.history_id,
                                        food_item=row['Recommended_Food_Item'],
                                        rating=5,  # +5 points for thumbs up
                                        comment=""
                                    )
                                    st.session_state.feedback_given[food_key] = "👍"
                                    logger.info(f"Saved positive feedback (+5 points) for {row['Recommended_Food_Item']}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error saving feedback: {str(e)}")
                                    logger.error(f"Error saving feedback: {e}")
                    
                    with col_thumbs_down:
                        if st.button("👎", key=f"thumbs_down_{idx}", use_container_width=True):

                            if 'user_id' not in st.session_state:
                                st.error("❌ Error: user_id not found. Please restart the app.")
                                logger.error("user_id not in session_state")
                            elif 'history_id' not in st.session_state:
                                st.error("❌ Error: history_id not found. Please restart the app.")
                                logger.error("history_id not in session_state")
                            elif not db:
                                st.error("❌ Error: Database not initialized")
                                logger.error("Database is None")
                            else:

                                try:
                                    db.save_feedback(
                                        user_id=st.session_state.user_id,
                                        history_id=st.session_state.history_id,
                                        food_item=row['Recommended_Food_Item'],
                                        rating=1,  # +1 point for thumbs down
                                        comment=""
                                    )
                                    st.session_state.feedback_given[food_key] = "👎"
                                    logger.info(f"Saved negative feedback (+1 point) for {row['Recommended_Food_Item']}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error saving feedback: {str(e)}")
                                    logger.error(f"Error saving feedback: {e}")

    st.markdown("---")
    st.markdown("### 📊 Recommendation Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:

        category_counts = recommendations['Food_Category'].value_counts()
        fig1 = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            title="Food Categories Distribution",
            labels={'x': 'Count', 'y': 'Category'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:

        cuisine_counts = recommendations['Cuisine_Type'].value_counts()
        fig2 = px.pie(
            values=cuisine_counts.values,
            names=cuisine_counts.index,
            title="Cuisine Types Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Get New Recommendations", use_container_width=True):

            try:
                with st.spinner("Generating new recommendations..."):
                    new_recommendations = rec_engine.get_recommendations(
                        mood=st.session_state.detected_emotion,
                        user_data=st.session_state.user_data
                    )
                    st.session_state.recommendations = new_recommendations

                    if 'user_id' in st.session_state:
                        history_id = db.save_recommendation_history(
                            st.session_state.user_id,
                            st.session_state.detected_emotion,
                            new_recommendations
                        )
                        st.session_state.history_id = history_id

                    st.session_state.feedback_given = {}
                    
                    st.success("✅ New recommendations generated!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error generating new recommendations: {str(e)}")

    
    with col2:
        if st.button("📄 Export as PDF", use_container_width=True):
            st.info("PDF export feature coming soon!")
    
    with col3:
        if st.button("🏠 Start Over", use_container_width=True):
            st.session_state.step = 1
            st.session_state.user_data = {}
            st.session_state.detected_emotion = None
            st.session_state.emotion_data = None
            st.session_state.recommendations = None
            st.rerun()

def sidebar_content():
    
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        st.markdown("---")
        st.markdown("### 📍 Current Step")
        st.progress(st.session_state.step / 3)
        st.write(f"Step {st.session_state.step} of 3")
        
        st.markdown("---")

        if st.button("📜 View My History", use_container_width=True):
            st.info("History feature - view past recommendations")

        st.markdown("### 🔍 Search Food Database")
        search_query = st.text_input("Search food items", placeholder="e.g., Pizza")
        if search_query:
            results = data_loader.search_food(search_query)
            st.write(f"Found {len(results)} items")
            with st.expander("View Results"):
                st.dataframe(results)
        
        st.markdown("---")

        st.markdown("### 📊 System Stats")
        if data_loader and hasattr(data_loader, 'food_data'):
            total_foods = len(data_loader.food_data)
            st.metric("Total Food Items", total_foods)
        else:
            st.metric("Total Food Items", "N/A")
        
        if db:
            try:
                st.metric("Active Users", db.get_user_count())
            except:
                st.metric("Active Users", "N/A")
        else:
            st.metric("Active Users", "N/A")
        
        st.markdown("---")

        with st.expander("ℹ️ About"):
            st.write()

def main():
    
    main_header()
    sidebar_content()

    if st.session_state.step == 1:
        step_1_user_info()
    elif st.session_state.step == 2:
        step_2_emotion_detection()
    elif st.session_state.step == 3:
        step_3_recommendations()

if __name__ == "__main__":
    main()