"""
Smart Traffic Management System - Multi-Lane Web Dashboard
Upload 4 images simultaneously to simulate a 4-way intersection
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import cv2
import numpy as np
import base64
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'web_uploads'
RESULTS_FOLDER = 'web_results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB max

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

def detect_vehicles(image_path, confidence=0.5, threshold=0.3):
    """Detect vehicles in uploaded image"""
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
    
    # YOLO detection
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
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
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)
                
                # Add label
                text = f"{label}: {confidences[i]:.2f}"
                (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(image, (x, y - text_h - 10), (x + text_w, y), color, -1)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (255, 255, 255), 2)
    
    # Add summary overlay
    summary = f"Vehicles: {vehicle_count}"
    cv2.rectangle(image, (10, 10), (300, 50), (0, 0, 0), -1)
    cv2.putText(image, summary, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1.0, (0, 255, 0), 2)
    
    return image, vehicle_count, vehicle_breakdown

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('multi_lane_dashboard.html')

@app.route('/upload-multi', methods=['POST'])
def upload_multi():
    """Handle multiple image uploads for 4-way intersection"""
    lane_names = ['North', 'East', 'South', 'West']
    results = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for idx, lane in enumerate(lane_names):
        file_key = f'lane{idx + 1}'
        
        if file_key not in request.files:
            results.append({
                'lane': lane,
                'error': 'No image uploaded',
                'count': 0
            })
            continue
        
        file = request.files[file_key]
        if file.filename == '':
            results.append({
                'lane': lane,
                'error': 'No file selected',
                'count': 0
            })
            continue
        
        # Save uploaded file
        filename = f"{timestamp}_{lane}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect vehicles
        try:
            result_image, count, breakdown = detect_vehicles(filepath)
            
            # Save result image
            result_filename = f"result_{timestamp}_{lane}.jpg"
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            cv2.imwrite(result_path, result_image)
            
            # Convert to base64
            _, buffer = cv2.imencode('.jpg', result_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            results.append({
                'lane': lane,
                'count': count,
                'breakdown': breakdown,
                'result_image': f"data:image/jpeg;base64,{img_base64}",
                'result_filename': result_filename
            })
        except Exception as e:
            results.append({
                'lane': lane,
                'error': str(e),
                'count': 0
            })
    
    # Determine signal control
    counts = [r.get('count', 0) for r in results]
    max_idx = counts.index(max(counts)) if counts else 0
    
    signal_decision = {
        'green_lane': lane_names[max_idx],
        'green_lane_count': counts[max_idx],
        'total_vehicles': sum(counts),
        'signals': [
            {
                'lane': lane_names[i],
                'status': 'GREEN' if i == max_idx else 'RED',
                'count': counts[i]
            }
            for i in range(len(lane_names))
        ]
    }
    
    return jsonify({
        'success': True,
        'results': results,
        'signal_decision': signal_decision
    })

@app.route('/results/<filename>')
def get_result(filename):
    """Serve result images"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - MULTI-LANE DASHBOARD")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5001")
    print("\n✨ Upload 4 images to simulate a 4-way intersection!")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
