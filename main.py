#!/usr/bin/env python3
"""
Plant Disease Detection - Main App Launcher
Run this to start the server
"""

if __name__ == '__main__':
    from app import app
    
    print("\n" + "="*60)
    print("🌿 Plant Disease Detection App")
    print("="*60)
    print("📱 Local:     http://localhost:5000")
    print("📊 QR Code:   http://localhost:5000/qr-code")
    print("\n🌍 For public sharing:")
    print("   New terminal: ngrok http 5000")
    print("   Copy public URL and generate QR code")
    print("\n📌 Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

