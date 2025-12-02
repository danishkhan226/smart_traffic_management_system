"""
Smart Traffic Management System - Unified Dashboard
Automatically uses GPU (PyTorch YOLO) if available, falls back to CPU (OpenCV YOLO)
"""
from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Try to import PyTorch and Ultralytics for GPU acceleration
USE_PYTORCH = False
try:
    import torch
    from ultralytics import YOLO
    USE_PYTORCH = True
    print("✓ PyTorch available - will attempt GPU acceleration")
except ImportError:
    print("⚠ PyTorch not available - using OpenCV YOLO")

# Global variables
current_stats = {
    'vehicle_count': 0,
    'breakdown': {},
    'fps': 0,
    'device': 'CPU',
    'last_update': datetime.now()
}
stats_lock = threading.Lock()
camera_source = 0  # Trying camera index 0 (likely iVCam or built-in webcam)

# =============================================================================
# PYTORCH YOLO IMPLEMENTATION (GPU-Accelerated)
# =============================================================================

if USE_PYTORCH:
    print("\n" + "=" * 70)
    print("INITIALIZING PYTORCH YOLO (GPU-ACCELERATED)")
    print("=" * 70)
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        device = 'cuda'
        print(f"✓ GPU ENABLED: {torch.cuda.get_device_name(0)}")
        current_stats['device'] = f"GPU: {torch.cuda.get_device_name(0)}"
    else:
        device = 'cpu'
        print("⚠ GPU not detected, using CPU with PyTorch")
        current_stats['device'] = "CPU (PyTorch)"
    
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')
    model.to(device)
    print(f"✓ YOLOv8 model loaded on {device.upper()}!")
    
    # Vehicle classes
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    vehicle_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
    
    def detect_vehicles_pytorch(frame, confidence=0.4):
        """Detect vehicles using PyTorch YOLO"""
        (H, W) = frame.shape[:2]
        
        # Run YOLO inference
        results = model(frame, conf=confidence, device=device, verbose=False)[0]
        
        vehicle_count = 0
        vehicle_breakdown = {}
        
        for detection in results.boxes.data:
            x1, y1, x2, y2, conf, cls = detection
            cls = int(cls)
            
            if cls in vehicle_classes:
                vehicle_count += 1
                vehicle_type = vehicle_names.get(cls, 'vehicle')
                vehicle_breakdown[vehicle_type] = vehicle_breakdown.get(vehicle_type, 0) + 1
                
                # Draw bounding box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Add label
                label = f"{vehicle_type} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
        
        return frame, vehicle_count, vehicle_breakdown

# =============================================================================
# OPENCV YOLO IMPLEMENTATION (CPU-Optimized)
# =============================================================================

else:
    print("\n" + "=" * 70)
    print("INITIALIZING OPENCV YOLO (CPU-OPTIMIZED)")
    print("=" * 70)
    
    yolo_dir = 'yolo'
    labels_path = f'{yolo_dir}/yolo-coco/coco.names'
    weights_path = f'{yolo_dir}/yolo-coco/yolov3.weights'
    config_path = f'{yolo_dir}/yolo-coco/yolov3.cfg'
    
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    LABELS = open(labels_path).read().strip().split("\n")
    vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
    
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
    
    current_stats['device'] = "CPU (OpenCV)"
    print("✓ YOLOv3 model loaded on CPU!")
    
    def detect_vehicles_opencv(frame, confidence=0.5, threshold=0.3):
        """Detect vehicles using OpenCV YOLO"""
        (H, W) = frame.shape[:2]
        
        # YOLO detection
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
        
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        
        boxes = []
        confidences = []
        classIDs = []
        
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                conf = scores[classID]
                
                if conf > confidence:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(conf))
                    classIDs.append(classID)
        
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)
        
        vehicle_count = 0
        vehicle_breakdown = {}
        
        if len(idxs) > 0:
            for i in idxs.flatten():
                label = LABELS[classIDs[i]]
                
                if label in vehicle_types:
                    vehicle_count += 1
                    vehicle_breakdown[label] = vehicle_breakdown.get(label, 0) + 1
                    
                    (x, y, w, h) = boxes[i]
                    color = [int(c) for c in COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{label}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.5, color, 2)
        
        return frame, vehicle_count, vehicle_breakdown

# =============================================================================
# UNIFIED DETECTION FUNCTION
# =============================================================================

def detect_vehicles_live(frame):
    """Unified detection - uses best available method"""
    (H, W) = frame.shape[:2]
    
    # Use PyTorch or OpenCV based on availability
    if USE_PYTORCH:
        frame, vehicle_count, vehicle_breakdown = detect_vehicles_pytorch(frame)
    else:
        frame, vehicle_count, vehicle_breakdown = detect_vehicles_opencv(frame)
    
    # Update global stats
    with stats_lock:
        current_stats['vehicle_count'] = vehicle_count
        current_stats['breakdown'] = vehicle_breakdown
        current_stats['last_update'] = datetime.now()
    
    # Add overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Add stats
    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    
    y_offset = 70
    for vehicle_type, count in vehicle_breakdown.items():
        cv2.putText(frame, f"{vehicle_type}: {count}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
    
    # Add device indicator
    device_color = (0, 255, 255) if 'GPU' in current_stats['device'] else (255, 255, 0)
    cv2.putText(frame, current_stats['device'], (20, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, device_color, 2)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (W - 250, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame

# =============================================================================
# FLASK ROUTES
# =============================================================================

def generate_frames():
    """Generate video frames with detection"""
    camera = cv2.VideoCapture(camera_source)
    
    # Set camera properties
    if USE_PYTORCH:
        # Smaller resolution for compact preview
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    else:
        # OpenCV uses optimized lower resolution
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    start_time = time.time()
    skip_frames = 1 if USE_PYTORCH else 2  # PyTorch can process more frames
    last_processed_frame = None
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Process frames based on capability
        if frame_count % skip_frames == 0:
            frame = detect_vehicles_live(frame)
            last_processed_frame = frame.copy()
        elif last_processed_frame is not None and not USE_PYTORCH:
            frame = last_processed_frame
        
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
    return render_template('live_camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def get_stats():
    with stats_lock:
        return jsonify({
            'vehicle_count': current_stats['vehicle_count'],
            'breakdown': current_stats['breakdown'],
            'fps': current_stats['fps'],
            'device': current_stats['device'],
            'timestamp': current_stats['last_update'].strftime("%H:%M:%S")
        })

if __name__ == '__main__':
    print("=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - UNIFIED DASHBOARD")
    print("=" * 70)
    print(f"\n🔧 Mode: {'GPU-Accelerated (PyTorch)' if USE_PYTORCH else 'CPU-Optimized (OpenCV)'}")
    print(f"🎮 Device: {current_stats['device']}")
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5005")
    print("\n📹 Camera source:", camera_source)
    print("=" * 70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5005, threaded=True)
