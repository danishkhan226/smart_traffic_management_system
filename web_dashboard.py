"""
Smart Traffic Management System - Live Web Dashboard
Upload your own images and see real-time vehicle detection!
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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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

# Generate random colors for bounding boxes
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
    detections = []
    
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
                
                # Add label with background
                text = f"{label}: {confidences[i]:.2f}"
                (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(image, (x, y - text_h - 10), (x + text_w, y), color, -1)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (255, 255, 255), 2)
                
                detections.append({
                    'type': label,
                    'confidence': f"{confidences[i]:.2%}",
                    'bbox': [x, y, w, h]
                })
    
    # Add summary overlay
    summary = f"Total Vehicles: {vehicle_count}"
    cv2.rectangle(image, (10, 10), (400, 50), (0, 0, 0), -1)
    cv2.putText(image, summary, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1.2, (0, 255, 0), 3)
    
    return image, vehicle_count, vehicle_breakdown, detections

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and detection"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"upload_{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Detect vehicles
    try:
        result_image, count, breakdown, detections = detect_vehicles(filepath)
        
        # Save result image
        result_filename = f"result_{timestamp}_{file.filename}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)
        
        # Convert image to base64 for display
        _, buffer = cv2.imencode('.jpg', result_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'vehicle_count': count,
            'breakdown': breakdown,
            'detections': detections,
            'result_image': f"data:image/jpeg;base64,{img_base64}",
            'result_filename': result_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results/<filename>')
def get_result(filename):
    """Serve result images"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - WEB DASHBOARD")
    print("=" * 70)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("\n✨ Upload your own traffic images and see live detection!")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
