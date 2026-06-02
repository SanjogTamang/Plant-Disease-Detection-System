# 🌿 Plant Disease Detection App

Real-time plant disease detection using AI with QR code sharing.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python main.py
```
Open: `http://localhost:5000`

## 📱 Share with QR Code

### Option 1: Manual ngrok
```bash
# Terminal 1
python main.py

# Terminal 2
ngrok http 5000

# Copy ngrok URL and open in browser
# Click "Generate QR Code"
```

### Option 2: Auto-Connect
```bash
$env:USE_NGROK='true'
$env:NGROK_AUTHTOKEN='your_token_here'
python main.py
```

Get token: https://dashboard.ngrok.com/auth/your-authtoken

## 📁 Project Structure

```
Plant disease/
├── app.py                     # Main Flask app
├── main.py                    # Launcher
├── config.py                  # Settings
├── detector.py                # AI model
├── templates/index.html       # Web UI
├── plant_disease_model.h5     # Model file
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🎯 How to Use

1. **Upload image** → Click predict
2. **Get diagnosis** → See disease & confidence
3. **Generate QR** → Share with others
4. **Users scan** → App opens on their phone!

## 📋 API Endpoints

- `POST /api/predict` - Predict disease from image
- `GET /qr-code` - Get QR code image
- `GET /api/public-url` - Get current public URL
- `GET /api/health` - Health check

## 🔧 Configuration

Create `.env` file (copy from `.env.example`):
```
USE_NGROK=false
NGROK_AUTHTOKEN=your_token_here
```

## ✨ Features

✓ AI-powered disease detection  
✓ QR code generation  
✓ Public sharing with ngrok  
✓ Real-time predictions  
✓ Mobile-friendly interface  

---

**Quick troubleshooting:**

- Model not found? Check `plant_disease_model.h5` exists
- Port in use? Change PORT in `config.py`
- QR not working? Use `ngrok http 5000` in new terminal

**Happy detecting! 🚀**



### GET /qr-code
Generate QR code for server URL

```bash
# Download QR code image
curl http://localhost:5000/qr-code > qr.png
```

### GET /api/health
Health check endpoint

```json
{"status": "healthy", "model": "loaded", "version": "1.0"}
```

## 🏗️ Architecture

### Files
```
Plant disease/
├── app.py              ← Flask API with /predict & /qr-code endpoints
├── detector.py         ← PlantDiseaseDetector class with temporal smoothing
├── config.py           ← All constants (model path, disease classes, settings)
├── main.py             ← Launcher script
├── templates/
│   └── index.html      ← Webcam UI with getUserMedia & AJAX
├── requirements.txt    ← Dependencies
└── plant_disease_model.h5  ← Your trained model
```

### PlantDiseaseDetector Class

Features:
- **Input:** PIL Image → 224×224 RGB normalization
- **Preprocessing:** MobileNetV2.preprocess_input()
- **Temporal Smoothing:** Sliding window (default=5) averages predictions
- **Output:** Disease label + confidence %

```python
detector = PlantDiseaseDetector(
    model_path='plant_disease_model.h5',
    labels=DISEASE_CLASSES,
    input_size=224,
    smoothing_window=5
)
result = detector.predict(image)
```

### Frontend

**Webcam Capture:**
- `getUserMedia` API for camera access
- Auto-capture every 350ms (configurable)
- Canvas → blob → AJAX to /api/predict
- Displays: disease name, confidence %, response time, leaf count

## 🔧 Configuration

**config.py:**
```python
MODEL_PATH = 'plant_disease_model.h5'
INPUT_SIZE = 224
SMOOTHING_WINDOW = 5
DISEASE_CLASSES = [...]  # 35 classes
USE_NGROK = False  # Set via environment variable
WEBCAM_INTERVAL = 350  # milliseconds
CONFIDENCE_THRESHOLD = 30
```

**Environment Variables:**
```bash
USE_NGROK=true         # Enable ngrok tunnel
FLASK_ENV=development  # or production
SECRET_KEY=your-key
PORT=5000
```

## 📱 Mobile Testing

### Local Network
```bash
# Find your IP
ipconfig  # Windows
ifconfig  # Mac/Linux

# Access from mobile
http://192.168.x.x:5000
```

### ngrok Tunnel
```bash
USE_NGROK=true python main.py
# Copy public URL, scan with QR code
```

## 🌾 Supported Diseases (35 classes)

Apple (4), Blueberry (1), Cherry (1), Corn (4), Grape (4), Peach (2), Pepper (2), Potato (3), Raspberry (1), Soybean (1), Squash (1), Strawberry (1), Tomato (10)

## 🚀 Deployment

### Docker
```bash
docker-compose up
```

### Cloud (Heroku/Railway/Render)
```bash
git push heroku main
# QR Code available at: <app-url>/qr-code
```

### Linux Server
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Camera not working | Check browser permissions |
| No predictions | Verify model file exists |
| Slow predictions | Reduce smoothing window |
| Port in use | Change PORT in config.py |
| ngrok error | Install: `pip install pyngrok` |

## 📚 See Also

- **SETUP.md** - Detailed installation guide
- **NGROK_GUIDE.md** - Online deployment guide
- **00_QUICK_START.txt** - Quick reference

---

**Build:** Reference Architecture (Facial Emotion Detection)  
**Status:** Production Ready ✅


## Project Structure

```
Plant disease/
├── app.py                          # Flask backend
├── plant_disease_model.h5          # Trained MobileNetV2 model
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── script.js              # Frontend logic
└── uploads/                        # Temporary uploaded images (auto-created)
```

## Deployment Guide

### For Local Network Access (Mobile Testing)

Find your computer's IP address:
```bash
ipconfig  # Windows
ifconfig  # macOS/Linux
```

Run Flask with network access:
```bash
python app.py
```

Access from mobile:
```
http://YOUR_IP_ADDRESS:5000
```

### QR Code Deployment

1. Generate QR code for your local IP address
2. Scan with mobile device
3. Use the app without installation

## Troubleshooting

### Model Not Loading
```
FileNotFoundError: plant_disease_model.h5 not found
```
**Solution:** Ensure `plant_disease_model.h5` is in the same directory as `app.py`

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:** Use a different port:
```bash
python -c "from app import app; app.run(port=5001)"
```


This project uses:
- TensorFlow/Keras (Apache 2.0)
- Flask (BSD)
- PlantVillage Dataset (Public Use)

## References

- **PlantVillage Dataset:** https://plantvillage.psu.edu/
- **MobileNetV2:** https://arxiv.org/abs/1801.04381
- **Web Speech API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- **Flask Documentation:** https://flask.palletsprojects.com/



