
import cv2
import numpy as np
from PIL import Image
import logging
from deepface import DeepFace
import config
import os

try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    logging.warning("TensorFlow not available. Custom model will not work.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmotionDetector:
    
    def __init__(self):
        
        self.emotions = config.EMOTIONS
        logger.info("Emotion Detector initialized")
    
    def detect_emotion(self, image_input):
        try:

            if hasattr(image_input, 'read'):

                image_bytes = image_input.read()
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif isinstance(image_input, str):

                img = cv2.imread(image_input)
            else:
                img = image_input
            
            if img is None:
                raise ValueError("Failed to load image")

            if len(img.shape) == 3 and img.shape[2] == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = img


            logger.info("Analyzing emotions with DeepFace...")
            result = DeepFace.analyze(
                img_rgb,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            if isinstance(result, list):
                result = result[0]  # Take first face
            
            emotions = result['emotion']
            dominant_emotion = result['dominant_emotion']
            
            emotion_mapping = {
                'happy': 'happy',
                'sad': 'sad',
                'angry': 'angry',
                'neutral': 'neutral',
                'surprise': 'surprise',
                'fear': 'fear',
                'disgust': 'disgust'
            }
            
            mapped_emotions = {}
            for key, value in emotions.items():
                mapped_key = emotion_mapping.get(key.lower(), key.lower())
                mapped_emotions[mapped_key] = value
            
            dominant_mapped = emotion_mapping.get(
                dominant_emotion.lower(), 
                dominant_emotion.lower()
            )

            emotion_result = {
                'dominant_emotion': dominant_mapped,
                'confidence': mapped_emotions.get(dominant_mapped, 0),
                'all_emotions': mapped_emotions
            }
            
            logger.info(f"Detected emotion: {dominant_mapped} "
                       f"with {emotion_result['confidence']:.2f}% confidence")
            
            return emotion_result
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {str(e)}")

            return {
                'dominant_emotion': 'neutral',
                'confidence': 50.0,
                'all_emotions': {
                    'happy': 14.3,
                    'sad': 14.3,
                    'angry': 14.3,
                    'neutral': 14.3,
                    'surprise': 14.3,
                    'fear': 14.3,
                    'disgust': 14.2
                },
                'error': str(e)
            }
    
    def detect_emotion_from_video(self, duration=5):
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                raise Exception("Cannot access camera")
            
            emotion_history = []
            start_time = cv2.getTickCount()
            
            logger.info(f"Capturing emotions for {duration} seconds...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                current_time = cv2.getTickCount()
                elapsed = (current_time - start_time) / cv2.getTickFrequency()
                
                if elapsed >= duration:
                    break

                if int(elapsed * 2) > len(emotion_history):
                    result = self.detect_emotion(frame)
                    if 'error' not in result:
                        emotion_history.append(result)

                if emotion_history:
                    last_emotion = emotion_history[-1]['dominant_emotion']
                    cv2.putText(
                        frame,
                        f"Emotion: {last_emotion}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
                
                cv2.imshow('Emotion Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()

            if not emotion_history:
                raise Exception("No emotions detected")

            emotion_counts = {}
            for result in emotion_history:
                emotion = result['dominant_emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)

            avg_emotions = {}
            for emotion in self.emotions:
                scores = [r['all_emotions'].get(emotion, 0) 
                         for r in emotion_history]
                avg_emotions[emotion] = np.mean(scores) if scores else 0
            
            return {
                'dominant_emotion': dominant_emotion,
                'confidence': avg_emotions.get(dominant_emotion, 0),
                'all_emotions': avg_emotions,
                'frame_count': len(emotion_history)
            }
            
        except Exception as e:
            logger.error(f"Error in video emotion detection: {str(e)}")
            raise
    
    def validate_emotion(self, emotion):
        return emotion.lower() in [e.lower() for e in self.emotions]


class CustomEmotionDetector:
    def __init__(self, model_path=None):

        if not TF_AVAILABLE:
            raise ImportError("TensorFlow is required for CustomEmotionDetector. "
                            "Install it with: pip install tensorflow")

        if model_path is None:
            model_path = os.path.join(config.MODELS_DIR, 'best_emotion_model.h5')
        
        self.model_path = model_path
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.img_size = (48, 48)  # Model was trained on 48x48 images

        try:
            logger.info(f"Loading custom model from {model_path}...")
            self.model = keras.models.load_model(model_path)
            logger.info("✓ Custom emotion model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load custom model: {str(e)}")
            raise
    
    def detect_emotion(self, image_input):
        try:

            if hasattr(image_input, 'read'):

                image_bytes = image_input.read()
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif isinstance(image_input, str):

                img = cv2.imread(image_input)
            else:

                img = image_input
            
            if img is None:
                raise ValueError("Failed to load image")

            img = cv2.resize(img, self.img_size)
            img = img / 255.0  # Normalize to [0, 1]
            img = np.expand_dims(img, axis=0)  # Add batch dimension

            predictions = self.model.predict(img, verbose=0)
            emotion_idx = np.argmax(predictions[0])

            result = {
                'dominant_emotion': self.emotions[emotion_idx],
                'confidence': float(predictions[0][emotion_idx] * 100),
                'all_emotions': {
                    emotion: float(prob * 100) 
                    for emotion, prob in zip(self.emotions, predictions[0])
                }
            }
            
            logger.info(f"Detected emotion: {result['dominant_emotion']} "
                       f"with {result['confidence']:.2f}% confidence")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in custom emotion detection: {str(e)}")

            return {
                'dominant_emotion': 'neutral',
                'confidence': 50.0,
                'all_emotions': {emotion: 14.3 for emotion in self.emotions},
                'error': str(e)
            }
    
    def validate_emotion(self, emotion):
        return emotion.lower() in [e.lower() for e in self.emotions]

if __name__ == "__main__":

    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--custom':
        print("Testing Custom Emotion Detector...")
        detector = CustomEmotionDetector()
    else:
        print("Testing DeepFace Emotion Detector...")
        detector = EmotionDetector()

    print("Testing emotion detection from camera...")
    print("Press 'q' to quit")
    
    try:
        result = detector.detect_emotion_from_video(duration=5) if hasattr(detector, 'detect_emotion_from_video') else None
        if result:
            print("\nDetection Result:")
            print(f"Dominant Emotion: {result['dominant_emotion']}")
            print(f"Confidence: {result['confidence']:.2f}%")
            print(f"All Emotions: {result['all_emotions']}")
    except Exception as e:
        print(f"Error: {str(e)}")