"""
Plant Disease Detector
Detects plant diseases using MobileNetV2 with temporal smoothing
"""

import numpy as np
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
except ImportError:
    from keras.models import load_model
    from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import io
from collections import deque


class PlantDiseaseDetector:
    """Plant disease detector with temporal smoothing"""
    
    def __init__(self, model_path, labels, input_size=224, smoothing_window=5):
        """
        Initialize detector
        
        Args:
            model_path: Path to .h5 model file
            labels: List of disease class names
            input_size: Input image size (224)
            smoothing_window: Number of frames for temporal smoothing
        """
        self.model = load_model(model_path)
        self.labels = labels
        self.input_size = input_size
        self.smoothing_window = smoothing_window
        self.prediction_queue = deque(maxlen=smoothing_window)
        
    def preprocess_image(self, image_data):
        """
        Preprocess image to 224x224 RGB and normalize
        
        Args:
            image_data: PIL Image or image bytes
            
        Returns:
            Preprocessed numpy array ready for model
        """
        # Open image if bytes
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 224x224
        image = image.resize((self.input_size, self.input_size))
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float32)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Preprocess using MobileNetV2 preprocessing
        img_array = preprocess_input(img_array)
        
        return img_array
    
    def predict(self, image_data):
        """
        Predict disease from image with temporal smoothing
        
        Args:
            image_data: PIL Image or image bytes
            
        Returns:
            Dictionary with prediction, confidence, and all scores
        """
        # Preprocess
        img_array = self.preprocess_image(image_data)
        
        # Get raw prediction
        raw_prediction = self.model.predict(img_array, verbose=0)[0]
        
        # Add to smoothing queue
        self.prediction_queue.append(raw_prediction)
        
        # Average predictions in queue (temporal smoothing)
        smoothed_prediction = np.mean(list(self.prediction_queue), axis=0)
        
        # Get top prediction
        pred_idx = np.argmax(smoothed_prediction)
        pred_label = self.labels[pred_idx]
        confidence = float(smoothed_prediction[pred_idx]) * 100
        
        # Get all predictions for debugging
        all_predictions = {
            self.labels[i]: float(smoothed_prediction[i]) * 100 
            for i in range(len(self.labels))
        }
        
        return {
            'disease': pred_label,
            'confidence': confidence,
            'all_predictions': all_predictions,
            'leaf_detected': True,  # In real app, could use detection model
            'smoothing_frames': len(self.prediction_queue)
        }
    
    def reset_smoothing(self):
        """Reset temporal smoothing queue"""
        self.prediction_queue.clear()
