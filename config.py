"""
Configuration for Plant Disease Detection App
All constants in one place
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Settings
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = FLASK_ENV == 'development'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
HOST = '0.0.0.0'
PORT = int(os.getenv('PORT', 5000))

# Model Settings
MODEL_PATH = 'plant_disease_model.h5'
INPUT_SIZE = 224
SMOOTHING_WINDOW = 5  # Temporal smoothing for predictions

# Disease Classes (MUST match model training - currently 15 classes)
DISEASE_CLASSES = [
    'Apple___Apple scab',
    'Apple___Black rot',
    'Apple___Cedar apple rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery mildew',
    'Corn_(maize)___Cercospora leaf spot Gray leaf spot',
    'Corn_(maize)___Common rust',
    'Corn_(maize)___Northern Leaf Blight',
    'Corn_(maize)___healthy',
    'Grape___Black rot',
    'Grape___Esca (Black Measles)',
    'Grape___Leaf blight (Isariopsis Leaf Spot)',
    'Grape___healthy',
    'Peach___Bacterial spot'
]

# Server Configuration
USE_NGROK = os.getenv('USE_NGROK', 'false').lower() == 'true'
NGROK_AUTHTOKEN = os.getenv('NGROK_AUTHTOKEN', None)

# File Upload
MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

# Webcam Settings
WEBCAM_INTERVAL = 350  # milliseconds between frames
CONFIDENCE_THRESHOLD = 30  # Only show predictions above this %
