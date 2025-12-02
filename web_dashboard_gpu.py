"""
Smart Traffic Management System - GPU-Accelerated Live Camera Feed
Real-time vehicle detection using PyTorch YOLO with automatic GPU support
"""
from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from datetime import datetime
import threading
import time
import torch
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model with automatic GPU detection
print("Loading YOLO model...")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"✓ GPU ENABLED: {torch.cuda.get_device_name(0)}")
    device = 'cuda'
else:
    print("⚠ GPU not available, using CPU")
    device = 'cpu'

# Load YOLOv8 model (smaller 'n' model for faster inference)
model = YOLO('yolov8n.pt')
model.to(device)
print(f"✓ YOLO model loaded on {device.upper()}!\n")

# Vehicle classes in COCO dataset
vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
vehicle_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

# Global variables for statistics
current_stats = {
    'vehicle_count': 0,
    'breakdown': {},
    'fps': 0,
    'last_update': datetime.now()
}
stats_lock = threading.Lock()

# Camera source (0 for webcam, or RTSP URL for IP camera)
camera_source = 0  # Change to RTSP URL if using IP camera

def detect_vehicles_live(frame, confidence=0.4):
    """Detect vehicles in live frame using PyTorch YOLO"""
    (H, W) = frame.shape[:2]
    
    # Run YOLO inference
    results = model(frame, conf=confidence, device=device, verbose=False)[0]
    
    # Process detections
    vehicle_count = 0
    vehicle_breakdown = {}
    
    for detection in results.boxes.data:
        x1, y1, x2, y2, conf, cls = detection
        cls = int(cls)
        
        # Check if it's a vehicle
        if cls in vehicle_classes:
            vehicle_count += 1
            vehicle_type = vehicle_names.get(cls, 'vehicle')
            vehicle_breakdown[vehicle_type] = vehicle_breakdown.get(vehicle_type, 0) + 1
            
            # Draw bounding box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            color = (0, 255, 0)  # Green
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"{vehicle_type} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, color, 2)
    
    # Update global stats
    with stats_lock:
        current_stats['vehicle_count'] = vehicle_count
        current_stats['breakdown'] = vehicle_breakdown
        current_stats['last_update'] = datetime.now()
    
    # Add overlay with statistics
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Add text
    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    
    y_offset = 70
    for vehicle_type, count in vehicle_breakdown.items():
        cv2.putText(frame, f"{vehicle_type}: {count}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
    
    # Add GPU/CPU indicator
    device_text = f"Device: {device.upper()}"
    cv2.putText(frame, device_text, (W - 150, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (W - 250, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame

def generate_frames():
    """Generate video frames with detection"""
    camera = cv2.VideoCapture(camera_source)
    
    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    frame_count = 0
    start_time = time.time()
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Process every frame (GPU is fast enough!)
        frame = detect_vehicles_live(frame)
        
        # Calculate FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            with stats_lock:
                current_stats['fps'] = round(fps, 1)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()

@app.route('/')
def index():
    """Main live camera page"""
    return render_template('live_camera.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def get_stats():
    """Get current detection statistics"""
    with stats_lock:
        return jsonify({
            'vehicle_count': current_stats['vehicle_count'],
            'breakdown': current_stats['breakdown'],
            'fps': current_stats['fps'],
            'timestamp': current_stats['last_update'].strftime("%H:%M:%S"),
            'device': device.upper()
        })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - GPU-ACCELERATED")
    print("=" * 70)
    print(f"\n🎮 Device: {device.upper()}")
    if torch.cuda.is_available():
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5004")
    print("\n📹 Camera source:", camera_source)
    print("   (0 = Webcam, or set RTSP URL for IP camera)")
    print("\n✨ GPU-accelerated vehicle detection with real-time streaming!")
    print("=" * 70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5004, threaded=True)
