"""
Smart Traffic Management System - Unified Backend for React Dashboard
Combines Live Camera, Image Upload, Video Analysis, and Multi-Lane features
"""
from flask import Flask, render_template, Response, jsonify, request, send_from_directory
import cv2
import numpy as np
from datetime import datetime
import threading
import time
import os
import base64

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'web_uploads'
RESULTS_FOLDER = 'web_results'
VIDEO_FRAMES_FOLDER = 'video_frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FRAMES_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['VIDEO_FRAMES_FOLDER'] = VIDEO_FRAMES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# =============================================================================
# DUAL YOLO CONFIGURATION
# - PyTorch YOLO: For live camera detection (GPU-accelerated if available)
# - OpenCV YOLO: For image upload, video analysis, and multi-lane intersection
# =============================================================================

# Global variables for live camera
current_stats = {
    'vehicle_count': 0,
    'breakdown': {},
    'fps': 0,
    'device': 'CPU',
    'last_update': datetime.now()
}
stats_lock = threading.Lock()
camera_source = 0

print("\n" + "=" * 70)
print("INITIALIZING DUAL YOLO CONFIGURATION")
print("=" * 70)

# =============================================================================
# OPENCV YOLO IMPLEMENTATION (CPU-Optimized) - ALWAYS LOADED
# Used for: Image Upload, Video Analysis, Multi-Lane Intersection
# =============================================================================

print("\n[1/2] Loading OpenCV YOLO (for Image/Video/Multi-Lane)...")
yolo_dir = 'yolo'
labels_path = f'{yolo_dir}/yolo-coco/coco.names'
weights_path = f'{yolo_dir}/yolo-coco/yolov3.weights'
config_path = f'{yolo_dir}/yolo-coco/yolov3.cfg'

opencv_net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
opencv_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
opencv_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

print("✓ OpenCV YOLOv3 model loaded on CPU!")

def calculate_iou(box1, box2):
    """Calculate Intersection over Union (IoU) between two bounding boxes.
    Boxes are in format [x, y, width, height]"""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Calculate intersection area
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - intersection_area
    
    return intersection_area / union_area if union_area > 0 else 0.0

def detect_vehicles_opencv(frame, confidence=0.5, threshold=0.3, exclude_boxes=None):
    """Detect vehicles using OpenCV YOLO - for image/video/multi-lane
    
    Args:
        frame: Image frame to process
        confidence: Detection confidence threshold
        threshold: NMS threshold
        exclude_boxes: List of bounding boxes to exclude (e.g., emergency vehicles)
                      Format: [[x, y, w, h], ...]
    """
    (H, W) = frame.shape[:2]
    
    ln = opencv_net.getLayerNames()
    ln = [ln[i - 1] for i in opencv_net.getUnconnectedOutLayers().flatten()]
    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    opencv_net.setInput(blob)
    layerOutputs = opencv_net.forward(ln)
    
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
    detections = []
    
    if len(idxs) > 0:
        for i in idxs.flatten():
            label = LABELS[classIDs[i]]
            
            if label in vehicle_types:
                # Check if this detection overlaps with any excluded boxes (e.g., emergency vehicles)
                is_excluded = False
                if exclude_boxes:
                    current_box = boxes[i]
                    for exclude_box in exclude_boxes:
                        iou = calculate_iou(current_box, exclude_box)
                        if iou > 0.3:  # If overlap is more than 30%, skip this detection
                            is_excluded = True
                            print(f"  Skipping {label} detection (overlaps with emergency vehicle, IoU={iou:.2f})")
                            break
                
                if is_excluded:
                    continue
                
                vehicle_count += 1
                vehicle_breakdown[label] = vehicle_breakdown.get(label, 0) + 1
                
                (x, y, w, h) = boxes[i]
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                text = f"{label}: {confidences[i]:.2f}"
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
                
                detections.append({
                    'type': label,
                    'confidence': f"{confidences[i]:.2%}",
                    'bbox': [x, y, w, h]
                })
    
    return frame, vehicle_count, vehicle_breakdown, detections

# =============================================================================
# PYTORCH YOLO IMPLEMENTATION (GPU-Accelerated) - OPTIONAL
# Used for: Live Camera Detection Only
# =============================================================================

USE_PYTORCH_LIVE = False
try:
    print("\n[2/2] Loading PyTorch YOLO (for Live Camera)...")
    import torch
    from ultralytics import YOLO
    
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
    
    pytorch_model = YOLO('yolov8n.pt')
    pytorch_model.to(device)
    print(f"✓ PyTorch YOLOv8 model loaded on {device.upper()}!")
    
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    vehicle_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
    
    USE_PYTORCH_LIVE = True
    
    def detect_vehicles_pytorch(frame, confidence=0.4):
        """Detect vehicles using PyTorch YOLO - for live camera only"""
        (H, W) = frame.shape[:2]
        results = pytorch_model(frame, conf=confidence, device=device, verbose=False)[0]
        
        vehicle_count = 0
        vehicle_breakdown = {}
        detections = []
        
        for detection in results.boxes.data:
            x1, y1, x2, y2, conf, cls = detection
            cls = int(cls)
            
            if cls in vehicle_classes:
                vehicle_count += 1
                vehicle_type = vehicle_names.get(cls, 'vehicle')
                vehicle_breakdown[vehicle_type] = vehicle_breakdown.get(vehicle_type, 0) + 1
                
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                label = f"{vehicle_type} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
                
                detections.append({
                    'type': vehicle_type,
                    'confidence': f"{conf:.2%}",
                    'bbox': [x1, y1, x2-x1, y2-y1]
                })
        
        return frame, vehicle_count, vehicle_breakdown, detections
    
except ImportError as e:
    print(f"⚠ PyTorch not available: {e}")
    print("→ Live camera will use OpenCV YOLO (CPU)")
    current_stats['device'] = "CPU (OpenCV)"
    USE_PYTORCH_LIVE = False

# =============================================================================
# EMERGENCY VEHICLE DETECTION (best.pt model)
# Used for: Emergency Vehicle Detection Feature
# =============================================================================

EMERGENCY_MODEL_AVAILABLE = False
emergency_model = None

try:
    print("\n[EMERGENCY] Loading Emergency Vehicle Detection Model...")
    import torch
    from ultralytics import YOLO
    
    # Load the custom trained best.pt model for ambulance detection
    emergency_model = YOLO('best.pt')
    
    if torch.cuda.is_available():
        emergency_device = 'cuda'
        emergency_model.to(emergency_device)
        print(f"✓ Emergency vehicle model (best.pt) loaded on GPU!")
    else:
        emergency_device = 'cpu'
        print("✓ Emergency vehicle model (best.pt) loaded on CPU")
    
    EMERGENCY_MODEL_AVAILABLE = True
    
    def detect_emergency_vehicles(frame, confidence=0.4):
        """Detect emergency vehicles (ambulances) using custom best.pt model"""
        (H, W) = frame.shape[:2]
        results = emergency_model(frame, conf=confidence, device=emergency_device, verbose=False)[0]
        
        emergency_count = 0
        emergency_detections = []
        
        for detection in results.boxes.data:
            x1, y1, x2, y2, conf, cls = detection
            
            # Assuming class 0 is ambulance/emergency vehicle in best.pt model
            emergency_count += 1
            
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw RED bounding box for emergency vehicles
            color = (0, 0, 255)  # Red color for emergency vehicles
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            
            label = f"AMBULANCE {conf:.2f}"
            # Add text with background for better visibility
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (255, 255, 255), 2)
            
            emergency_detections.append({
                'type': 'ambulance',
                'confidence': f"{conf:.2%}",
                'bbox': [x1, y1, x2-x1, y2-y1]
            })
        
        return frame, emergency_count, emergency_detections
    
except Exception as e:
    print(f"⚠ Emergency vehicle model not available: {e}")
    print("→ Emergency vehicle detection will not be available")
    EMERGENCY_MODEL_AVAILABLE = False

# =============================================================================
# UNIFIED DETECTION FUNCTIONS
# =============================================================================

def detect_vehicles_live(frame):
    """
    Detection for live camera - uses PyTorch YOLO if available, otherwise OpenCV YOLO
    """
    (H, W) = frame.shape[:2]
    
    # Use PyTorch for live camera if available, otherwise fall back to OpenCV
    if USE_PYTORCH_LIVE:
        frame, vehicle_count, vehicle_breakdown, _ = detect_vehicles_pytorch(frame)
    else:
        frame, vehicle_count, vehicle_breakdown, _ = detect_vehicles_opencv(frame)
    
    with stats_lock:
        current_stats['vehicle_count'] = vehicle_count
        current_stats['breakdown'] = vehicle_breakdown
        current_stats['last_update'] = datetime.now()
    
    # Add overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    
    y_offset = 70
    for vehicle_type, count in vehicle_breakdown.items():
        cv2.putText(frame, f"{vehicle_type}: {count}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 25
    
    device_color = (0, 255, 255) if 'GPU' in current_stats['device'] else (255, 255, 0)
    cv2.putText(frame, current_stats['device'], (20, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, device_color, 2)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (W - 250, H - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame

def detect_vehicles_image(image_path):
    """
    Detection for uploaded images - ALWAYS uses OpenCV YOLO for more accurate results
    Used by: Image Upload, Video Analysis, Multi-Lane Intersection
    """
    image = cv2.imread(image_path)
    
    # ALWAYS use OpenCV YOLO for image/video/multi-lane (more accurate)
    result_image, count, breakdown, detections = detect_vehicles_opencv(image)
    
    # Add summary overlay
    summary = f"Total Vehicles: {count}"
    cv2.rectangle(result_image, (10, 10), (400, 50), (0, 0, 0), -1)
    cv2.putText(result_image, summary, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1.2, (0, 255, 0), 3)
    
    return result_image, count, breakdown, detections

# =============================================================================
# FLASK ROUTES - LIVE CAMERA
# =============================================================================

def generate_frames():
    """Generate video frames with detection"""
    camera = cv2.VideoCapture(camera_source)
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    start_time = time.time()
    skip_frames = 1 if USE_PYTORCH_LIVE else 2  # PyTorch processes faster
    last_processed_frame = None
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        if frame_count % skip_frames == 0:
            frame = detect_vehicles_live(frame)
            last_processed_frame = frame.copy()
        elif last_processed_frame is not None and not USE_PYTORCH_LIVE:
            frame = last_processed_frame
        
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            with stats_lock:
                current_stats['fps'] = round(fps, 1)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()

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

# =============================================================================
# FLASK ROUTES - IMAGE UPLOAD
# =============================================================================

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Handle single image upload and detection"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"upload_{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        result_image, count, breakdown, detections = detect_vehicles_image(filepath)
        
        result_filename = f"result_{timestamp}_{file.filename}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)
        
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

# =============================================================================
# FLASK ROUTES - MULTI-LANE
# =============================================================================

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
        
        filename = f"{timestamp}_{lane}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result_image, count, breakdown, _ = detect_vehicles_image(filepath)
            
            result_filename = f"result_{timestamp}_{lane}.jpg"
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            cv2.imwrite(result_path, result_image)
            
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

# =============================================================================
# FLASK ROUTES - EMERGENCY VEHICLE DETECTION
# =============================================================================

@app.route('/upload-emergency', methods=['POST'])
def upload_emergency():
    """Handle emergency vehicle detection for 4-way intersection with priority logic"""
    if not EMERGENCY_MODEL_AVAILABLE:
        return jsonify({'error': 'Emergency vehicle detection model not available'}), 503
    
    lane_names = ['North', 'East', 'South', 'West']
    results = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for idx, lane in enumerate(lane_names):
        file_key = f'lane{idx + 1}'
        
        if file_key not in request.files:
            results.append({
                'lane': lane,
                'error': 'No image uploaded',
                'count': 0,
                'emergency_count': 0
            })
            continue
        
        file = request.files[file_key]
        if file.filename == '':
            results.append({
                'lane': lane,
                'error': 'No file selected',
                'count': 0,
                'emergency_count': 0
            })
            continue
        
        filename = f"{timestamp}_emergency_{lane}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read the image
            print(f"Processing {filename}...")
            image = cv2.imread(filepath)
            if image is None:
                raise ValueError(f"Failed to read image: {filepath}")
                
            result_image = image.copy()
            
            # Step 1: Detect emergency vehicles using best.pt model
            print("Running emergency vehicle detection...")
            result_image, emergency_count, emergency_detections = detect_emergency_vehicles(result_image.copy())
            print(f"Emergency count: {emergency_count}")
            
            # Extract bounding boxes of emergency vehicles to exclude from regular detection
            emergency_bboxes = [det['bbox'] for det in emergency_detections]
            
            # Step 2: Detect regular vehicles using OpenCV YOLO (excluding emergency vehicle regions)
            print("Running regular vehicle detection...")
            result_image, vehicle_count, vehicle_breakdown, _ = detect_vehicles_opencv(result_image, exclude_boxes=emergency_bboxes)
            print(f"Regular count: {vehicle_count}")
            
            # Add summary overlay
            summary = f"Total: {vehicle_count} | Emergency: {emergency_count}"
            cv2.rectangle(result_image, (10, 10), (450, 50), (0, 0, 0), -1)
            cv2.putText(result_image, summary, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.0, (0, 255, 0), 2)
            
            # Save result image (full resolution)
            result_filename = f"result_{timestamp}_emergency_{lane}.jpg"
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            cv2.imwrite(result_path, result_image)
            
            # Optimization: Resize for display and compress
            height, width = result_image.shape[:2]
            max_display_width = 800
            if width > max_display_width:
                scale = max_display_width / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                display_image = cv2.resize(result_image, (new_width, new_height))
            else:
                display_image = result_image

            # Encode image to base64 with optimization
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            _, buffer = cv2.imencode('.jpg', display_image, encode_param)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            results.append({
                'lane': lane,
                'count': vehicle_count,
                'emergency_count': emergency_count,
                'breakdown': vehicle_breakdown,
                'result_image': f"data:image/jpeg;base64,{img_base64}",
                'result_filename': result_filename
            })
        except Exception as e:
            import traceback
            print(f"ERROR processing {lane}: {str(e)}")
            print(traceback.format_exc())
            results.append({
                'lane': lane,
                'error': str(e),
                'count': 0,
                'emergency_count': 0
            })
    
    # PRIORITY SIGNAL CONTROL LOGIC
    # Priority 1: Lanes with emergency vehicles
    # Priority 2: If multiple lanes have emergency vehicles, use vehicle count as tiebreaker
    # Priority 3: If no emergency vehicles, use normal traffic density
    
    emergency_lanes = [(i, r) for i, r in enumerate(results) if r.get('emergency_count', 0) > 0]
    
    if emergency_lanes:
        # At least one lane has emergency vehicle(s)
        # Sort by emergency count first, then by regular vehicle count
        emergency_lanes.sort(key=lambda x: (x[1].get('emergency_count', 0), x[1].get('count', 0)), reverse=True)
        green_idx = emergency_lanes[0][0]
        priority_reason = f"Emergency vehicle detected in {lane_names[green_idx]} lane. Priority given to emergency vehicles."
        
        if len(emergency_lanes) > 1:
            priority_reason += f" Multiple emergency vehicles detected. {lane_names[green_idx]} has highest priority based on vehicle count."
    else:
        # No emergency vehicles, use normal traffic density logic
        counts = [r.get('count', 0) for r in results]
        green_idx = counts.index(max(counts)) if counts else 0
        priority_reason = "No emergency vehicles detected. Signal assigned based on traffic density."
    
    total_vehicles = sum(r.get('count', 0) for r in results)
    total_emergency = sum(r.get('emergency_count', 0) for r in results)
    
    signal_decision = {
        'green_lane': lane_names[green_idx],
        'green_lane_count': results[green_idx].get('count', 0),
        'total_vehicles': total_vehicles,
        'total_emergency': total_emergency,
        'priority_reason': priority_reason,
        'signals': [
            {
                'lane': lane_names[i],
                'status': 'GREEN' if i == green_idx else 'RED',
                'count': results[i].get('count', 0),
                'emergency_count': results[i].get('emergency_count', 0),
                'has_emergency': results[i].get('emergency_count', 0) > 0
            }
            for i in range(len(lane_names))
        ]
    }
    
    return jsonify({
        'success': True,
        'results': results,
        'signal_decision': signal_decision
    })


# =============================================================================
# FLASK ROUTES - VIDEO UPLOAD
# =============================================================================

@app.route('/upload-video', methods=['POST'])
def upload_video():
    """Handle video upload and frame-by-frame detection"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"video_{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Open video
        cap = cv2.VideoCapture(filepath)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Process every nth frame to speed up
        frame_skip = max(1, fps // 2)  # Process 2 frames per second
        
        frame_results = []
        max_vehicles = 0  # Track peak vehicles in a single frame
        total_vehicles_sum = 0  # For calculating average
        overall_breakdown = {}
        frame_count = 0
        processed_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Only process every nth frame
            if frame_count % frame_skip == 0:
                # Detect vehicles using OpenCV YOLO (more accurate)
                processed_frame, count, breakdown, _ = detect_vehicles_opencv(frame.copy())
                
                # Save processed frame
                frame_filename = f"frame_{timestamp}_{processed_count:04d}.jpg"
                frame_path = os.path.join(app.config['VIDEO_FRAMES_FOLDER'], frame_filename)
                cv2.imwrite(frame_path, processed_frame)
                
                # Update statistics
                max_vehicles = max(max_vehicles, count)  # Track peak
                total_vehicles_sum += count  # For average calculation
                
                for vtype, vcount in breakdown.items():
                    overall_breakdown[vtype] = overall_breakdown.get(vtype, 0) + vcount
                
                frame_results.append({
                    'frame_number': frame_count,
                    'vehicle_count': count,
                    'breakdown': breakdown,
                    'frame_image': frame_filename
                })
                
                processed_count += 1
            
            frame_count += 1
        
        cap.release()
        
        avg_vehicles = round(total_vehicles_sum / processed_count, 1) if processed_count > 0 else 0
        
        return jsonify({
            'success': True,
            'total_frames': total_frames,
            'processed_frames': processed_count,
            'fps': fps,
            'total_vehicles': max_vehicles,  # Now shows peak instead of cumulative
            'avg_vehicles_per_frame': avg_vehicles,
            'overall_breakdown': overall_breakdown,
            'frames': frame_results[:20]  # Return first 20 frames
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================================================
# FLASK ROUTES - FILE SERVING
# =============================================================================

@app.route('/results/<filename>')
def get_result(filename):
    """Serve result images"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/frames/<filename>')
def get_frame(filename):
    """Serve video frames"""
    return send_from_directory(app.config['VIDEO_FRAMES_FOLDER'], filename)

# =============================================================================
# SHORTEST PATH ROUTING
# =============================================================================

from shortest_path import ShortestPathFinder

# Initialize shortest path finder
try:
    path_finder = ShortestPathFinder('data/bangalore_network.pkl')
    if path_finder.is_ready():
        print("✓ Bangalore road network loaded for routing")
        print(f"  Network stats: {path_finder.get_network_stats()}")
    else:
        path_finder = None
        print("⚠ Road network not found - run 'python download_network.py'")
except Exception as e:
    path_finder = None
    print(f"⚠ Could not load road network: {e}")

@app.route('/api/geocode', methods=['POST'])
def geocode_address():
    """Convert address to coordinates"""
    if not path_finder or not path_finder.is_ready():
        return jsonify({'error': 'Routing service not available'}), 503
    
    data = request.json
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    try:
        coords = path_finder.geocode(address)
        if coords:
            return jsonify({
                'success': True,
                'lat': coords[0],
                'lng': coords[1],
                'address': address
            })
        else:
            return jsonify({'error': 'Address not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-route', methods=['POST'])
def calculate_route():
    """Calculate shortest path between two points"""
    if not path_finder or not path_finder.is_ready():
        return jsonify({'error': 'Routing service not available'}), 503
    
    data = request.json
    origin = data.get('origin')  # {lat, lng}
    destination = data.get('destination')  # {lat, lng}
    
    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400
    
    try:
        result = path_finder.calculate_route(
            origin['lat'], origin['lng'],
            destination['lat'], destination['lng']
        )
        
        return jsonify({
            'success': True,
            **result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/network-stats', methods=['GET'])
def get_network_stats():
    """Get statistics about the loaded road network"""
    if not path_finder or not path_finder.is_ready():
        return jsonify({'error': 'Routing service not available'}), 503
    
    stats = path_finder.get_network_stats()
    return jsonify({
        'success': True,
        **stats
    })

# =============================================================================
# MAIN
# =============================================================================


if __name__ == '__main__':
    print("=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - UNIFIED BACKEND")
    print("=" * 70)
    print("\n🎯 YOLO CONFIGURATION:")
    print(f"   📹 Live Camera: {'PyTorch YOLOv8 (GPU)' if USE_PYTORCH_LIVE else 'OpenCV YOLOv3 (CPU)'}")
    print(f"   🖼️  Image Upload: OpenCV YOLOv3 (CPU)")
    print(f"   🎬 Video Analysis: OpenCV YOLOv3 (CPU)")
    print(f"   🚦 Multi-Lane: OpenCV YOLOv3 (CPU)")
    print(f"\n🎮 Device: {current_stats['device']}")
    print("\n🌐 Starting unified web server...")
    print("📍 Backend running on: http://localhost:5005")
    print("\n📹 Camera source:", camera_source)
    print("=" * 70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5005, threaded=True)

