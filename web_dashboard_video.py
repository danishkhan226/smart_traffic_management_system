"""
Smart Traffic Management System - Video Upload Dashboard
Upload traffic videos and see real-time vehicle detection
"""
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import os
import cv2
import numpy as np
import base64
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'video_uploads'
RESULTS_FOLDER = 'video_results'
FRAMES_FOLDER = 'video_frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

# YOLO Configuration
yolo_dir = 'yolo'
labels_path = os.path.join(yolo_dir, 'yolo-coco', 'coco.names')
weights_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.weights')
config_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.cfg')

# Load YOLO model
print("Loading YOLO model...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
print("✓ YOLO model loaded and ready!\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

def detect_vehicles_in_frame(frame, confidence=0.5, threshold=0.3):
    """Detect vehicles in a single video frame"""
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
    
    # Add summary overlay
    summary = f"Vehicles: {vehicle_count}"
    cv2.rectangle(frame, (10, 10), (250, 50), (0, 0, 0), -1)
    cv2.putText(frame, summary, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1.0, (0, 255, 0), 2)
    
    return frame, vehicle_count, vehicle_breakdown

@app.route('/')
def index():
    """Main video dashboard page"""
    return render_template('video_dashboard.html')

@app.route('/upload-video', methods=['POST'])
def upload_video():
    """Handle video upload and processing"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded video
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"video_{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Open video
        cap = cv2.VideoCapture(filepath)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Sample frames for analysis (every 30 frames)
        sample_interval = 30
        frame_results = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every Nth frame
            if frame_count % sample_interval == 0:
                annotated_frame, count, breakdown = detect_vehicles_in_frame(frame)
                
                # Save frame
                frame_filename = f"frame_{timestamp}_{frame_count}.jpg"
                frame_path = os.path.join(app.config['FRAMES_FOLDER'], frame_filename)
                cv2.imwrite(frame_path, annotated_frame)
                
                # Convert to base64 for first few frames
                if len(frame_results) < 10:  # Only send first 10 frames
                    _, buffer = cv2.imencode('.jpg', annotated_frame)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    frame_results.append({
                        'frame_number': frame_count,
                        'timestamp': frame_count / fps if fps > 0 else 0,
                        'vehicle_count': count,
                        'breakdown': breakdown,
                        'image': f"data:image/jpeg;base64,{img_base64}"
                    })
            
            frame_count += 1
        
        cap.release()
        
        # Calculate statistics
        total_detections = sum(f['vehicle_count'] for f in frame_results)
        avg_vehicles = total_detections / len(frame_results) if frame_results else 0
        
        return jsonify({
            'success': True,
            'video_info': {
                'filename': filename,
                'fps': fps,
                'total_frames': total_frames,
                'duration': duration,
                'frames_analyzed': len(frame_results)
            },
            'statistics': {
                'total_detections': total_detections,
                'average_vehicles': round(avg_vehicles, 2),
                'max_vehicles': max((f['vehicle_count'] for f in frame_results), default=0)
            },
            'frame_results': frame_results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/frames/<filename>')
def get_frame(filename):
    """Serve frame images"""
    return send_from_directory(app.config['FRAMES_FOLDER'], filename)

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - VIDEO DASHBOARD")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5002")
    print("\n✨ Upload traffic videos and see real-time detection!")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
