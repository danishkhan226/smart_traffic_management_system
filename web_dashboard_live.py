"""
Smart Traffic Management System - Live Camera Feed Dashboard
Real-time vehicle detection from webcam or IP camera
"""
from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from datetime import datetime
import threading
import time

app = Flask(__name__)

# YOLO Configuration
yolo_dir = 'yolo'
labels_path = f'{yolo_dir}/yolo-coco/coco.names'
weights_path = f'{yolo_dir}/yolo-coco/yolov3.weights'
config_path = f'{yolo_dir}/yolo-coco/yolov3.cfg'

# Load YOLO model
print("Loading YOLO model...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# Try to enable GPU acceleration
# Check if CUDA is available in OpenCV build
cuda_available = cv2.cuda.getCudaEnabledDeviceCount() > 0 if hasattr(cv2, 'cuda') else False

if cuda_available:
    try:
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        print("✓ GPU acceleration ENABLED (CUDA)")
    except:
        cuda_available = False

if not cuda_available:
    print("⚠ GPU not available, using CPU (optimized)")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
print("✓ YOLO model loaded!\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

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
# Example: camera_source = "rtsp://username:password@ip:port/stream"

def detect_vehicles_live(frame, confidence=0.5, threshold=0.3):
    """Detect vehicles in live frame"""
    (H, W) = frame.shape[:2]
    
    # YOLO detection
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    
    # Process detections
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
    
    # Apply NMS
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)
    
    # Draw boxes and count vehicles
    vehicle_count = 0
    vehicle_breakdown = {}
    
    if len(idxs) > 0:
        for i in idxs.flatten():
            label = LABELS[classIDs[i]]
            
            if label in vehicle_types:
                vehicle_count += 1
                vehicle_breakdown[label] = vehicle_breakdown.get(label, 0) + 1
                
                # Draw bounding box
                (x, y, w, h) = boxes[i]
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                # Add label
                text = f"{label}"
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
    
    # Update global stats
    with stats_lock:
        current_stats['vehicle_count'] = vehicle_count
        current_stats['breakdown'] = vehicle_breakdown
        current_stats['last_update'] = datetime.now()
    
    # Add overlay
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
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (W - 250, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame

def generate_frames():
    """Generate video frames with detection"""
    camera = cv2.VideoCapture(camera_source)
    
    # Set camera properties (lower resolution for better performance)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    start_time = time.time()
    last_processed_frame = None
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Process every 2nd frame for better performance (skip frames)
        # Display the last processed frame for smooth video
        if frame_count % 2 == 0:
            frame = detect_vehicles_live(frame)
            last_processed_frame = frame.copy()
        elif last_processed_frame is not None:
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
            'timestamp': current_stats['last_update'].strftime("%H:%M:%S")
        })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - LIVE CAMERA FEED")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5003")
    print("\n📹 Camera source:", camera_source)
    print("   (0 = Webcam, or set RTSP URL for IP camera)")
    print("\n✨ Live vehicle detection with real-time streaming!")
    print("=" * 70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5003, threaded=True)
