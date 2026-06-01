"""
Plant Disease Detection API
Flask app with PlantDiseaseDetector and ngrok support
"""

import os
import io
import time
import json
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import qrcode
from config import (
    FLASK_ENV, FLASK_DEBUG, SECRET_KEY, HOST, PORT,
    MODEL_PATH, DISEASE_CLASSES, USE_NGROK, NGROK_AUTHTOKEN,
    ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE, INPUT_SIZE
)
from detector import PlantDiseaseDetector

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
app.secret_key = SECRET_KEY

# Initialize detector
print("🌿 Loading plant disease model...")
detector = PlantDiseaseDetector(
    model_path=MODEL_PATH,
    labels=DISEASE_CLASSES,
    input_size=INPUT_SIZE,
    smoothing_window=5
)
print("✅ Model loaded successfully!")

# Global variable for ngrok URL
ngrok_url = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    POST /api/predict
    Accept image upload and return disease prediction
    
    Response JSON:
    {
        "disease": "Tomato___Late blight",
        "confidence": 94.32,
        "leaf_count": 1,
        "response_time_ms": 245.3
    }
    """
    start_time = time.time()
    
    try:
        # Check if image provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Use JPG, PNG, GIF, or BMP'}), 400
        
        # Read image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Get prediction
        result = detector.predict(image)
        
        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # milliseconds
        
        # Return response
        return jsonify({
            'success': True,
            'disease': result['disease'],
            'confidence': round(result['confidence'], 2),
            'leaf_count': 1 if result['leaf_detected'] else 0,
            'response_time_ms': round(response_time, 1),
            'smoothing_frames': result['smoothing_frames']
        }), 200
        
    except Exception as e:
        print(f"❌ Error in /api/predict: {str(e)}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.route('/qr-code')
def qr_code():
    """
    GET /qr-code
    Generate QR code pointing to the server URL
    """
    try:
        # Determine URL
        if ngrok_url:
            url = ngrok_url
        else:
            # Get the request host
            url = request.host_url.rstrip('/')
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return send_file(
            img_bytes,
            mimetype='image/png',
            as_attachment=False,
            download_name='qrcode.png'
        )
    
    except Exception as e:
        print(f"❌ Error generating QR code: {str(e)}")
        return jsonify({'error': 'QR code generation failed'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'loaded',
        'version': '1.0',
        'ngrok_url': ngrok_url
    }), 200


@app.route('/api/public-url', methods=['GET'])
def get_public_url():
    """Get the public ngrok URL if available"""
    global ngrok_url
    
    if ngrok_url:
        return jsonify({
            'url': ngrok_url,
            'qr_code': f'{ngrok_url}/qr-code',
            'active': True
        }), 200
    else:
        local_url = request.host_url.rstrip('/')
        return jsonify({
            'url': local_url,
            'qr_code': f'{local_url}/qr-code',
            'active': False,
            'message': 'ngrok not active. Enable with USE_NGROK=true'
        }), 200


if __name__ == '__main__':
    print("="*60)
    print("🌿 Plant Disease Detection API")
    print("="*60)
    print(f"📱 Local URL: http://{HOST}:{PORT}")
    print(f"🔍 API:       http://{HOST}:{PORT}/api/predict")
    print(f"📊 QR Code:   http://{HOST}:{PORT}/qr-code")
    print(f"💚 Health:    http://{HOST}:{PORT}/api/health")
    print("="*60)
    print()
    print("🌍 For public sharing with ngrok:")
    print("   1. In NEW terminal: ngrok http 5000")
    print("   2. Copy the public URL from ngrok (https://xxxx.ngrok.io)")
    print("   3. QR code will work automatically!")
    print()
    
    # Run server
    app.run(
        host=HOST,
        port=PORT,
        debug=FLASK_DEBUG,
        use_reloader=False,  # Prevent double model loading
        threaded=True
    )
