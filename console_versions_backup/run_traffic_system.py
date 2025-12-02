"""
Simplified Traffic Management Server
Demonstrates real-time traffic monitoring and signal control

This is a simplified version that works without the module import issues.
Run this to see the smart traffic signal system in action!
"""
import os
import sys
import cv2
import numpy as np
import datetime
import random
import pickle

# Configuration
yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
labels_path = os.path.join(yolo_dir, 'yolo-coco', 'coco.names')
weights_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.weights')
config_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.cfg')
frames_base = os.path.join(yolo_dir, 'frames')

# Load YOLO model
print("Loading YOLO model...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
print("✓ Model loaded!\n")

# Initialize state file
state_file = 'traffic_state.pickle'
if not os.path.exists(state_file):
    arr = [
        0,  # tr - time remaining for emergency vehicle
        datetime.datetime.now(),  # time_at_received
        0,  # severity_index
        0,  # tr_1 - backup time
        datetime.datetime.now(),  # time_at_received_1
        0,  # severity_index_1
        1,  # crossing number
        random.randrange(0, 4)  # current signal (0-3)
    ]
    with open(state_file, 'wb') as handle:
        pickle.dump(np.array(arr), handle, protocol=pickle.HIGHEST_PROTOCOL)

def detect_vehicles(img_path, confidence=0.5, threshold=0.3):
    """Detect vehicles in an image"""
    if not os.path.exists(img_path):
        return 0
    
    image = cv2.imread(img_path)
    (H, W) = image.shape[:2]
    
    # Get YOLO output
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
    
    # Count vehicles
    count = 0
    if len(idxs) > 0:
        for i in idxs.flatten():
            if LABELS[classIDs[i]] in vehicle_types:
                count += 1
    
    return count

def make_signal_decision(density):
    """Make traffic signal decision based on vehicle density"""
    with open(state_file, 'rb') as handle:
        arr = pickle.load(handle)
    arr = arr.tolist()
    
    tr = arr[0]
    crossing = arr[6]
    signal = arr[7]
    
    # Determine signal state
    if tr == 0:  # No emergency vehicle
        crossing_str = f"crossing - {crossing}"
        print(f"\n{'='*60}")
        print("TRAFFIC SIGNAL DECISION")
        print(f"{'='*60}")
        print(f"\nCrossing: {crossing}")
        print("Status: No Emergency vehicle approaching")
        print(f"\nVehicle density per lane:")
        
        # Find lane with max density
        max_idx = 0
        max_density = density[0]
        for k in range(len(density)):
            if density[k] > max_density:
                max_density = density[k]
                max_idx = k
        
        # Display signals
        lane_names = ['North', 'East', 'South', 'West']
        for i in range(len(density)):
            if i == max_idx:
                print(f"  {lane_names[i]:6} Lane : GREEN  - {density[i]} vehicles")
            else:
                print(f"  {lane_names[i]:6} Lane : RED    - {density[i]} vehicles")
        
        print(f"\nDecision: GREEN signal to {lane_names[max_idx]} Lane (highest congestion)")
        print(f"{'='*60}\n")

print("=" * 70)
print("SMART TRAFFIC MANAGEMENT SYSTEM - LIVE DEMO")
print("=" * 70)
print("\nThis demonstrates real-time traffic monitoring and signal control.")
print("Processing frames from 3 traffic camera feeds...\n")

# Process frames in sequence (simulating real-time)
iteration = 0
max_iterations = 5  # Run for 5 cycles to demonstrate

while iteration < max_iterations:
    print(f"\n{'~'*70}")
    print(f"Cycle {iteration + 1}/{max_iterations}")
    print(f"{'~'*70}")
    
    # Analyze traffic from each camera (up to 3 lanes)
    density = []
    
    for camera_id in range(1, 4):  # Cameras 1, 2, 3
        frame_num = 10 + iteration * 50  # Sample different frames
        frame_path = os.path.join(frames_base, str(camera_id), f'{frame_num}.jpg')
        
        print(f"\n📷 Camera {camera_id} - Analyzing frame {frame_num}...")
        count = detect_vehicles(frame_path)
        density.append(count)
        print(f"   Detected {count} vehicles")
    
    # Add a 4th lane with random data (since we only have 3 videos)
    density.append(random.randint(5, 15))
    print(f"\n📷 Camera 4 - Detected {density[3]} vehicles (simulated)")
    
    # Make signal decision
    make_signal_decision(density)
    
    iteration += 1
    
    if iteration < max_iterations:
        print("Waiting for next cycle...\n")

print("\n" + "=" * 70)
print("✓ DEMO COMPLETE!")
print("=" * 70)
print("\nThe system demonstrated:")
print("- Real-time vehicle detection from camera feeds")
print("- Traffic density analysis for all lanes")
print("- Smart signal control based on congestion levels")
print("\nIn production, this would run continuously, updating signals")
print("every few seconds based on real-time traffic conditions.")
