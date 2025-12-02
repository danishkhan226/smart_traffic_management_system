"""
Test vehicle detection on multiple images to simulate different traffic scenarios
This shows how the system would analyze different lanes/directions at an intersection
"""
import os
import cv2
import numpy as np
from datetime import datetime

# Set paths
yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
labels_path = os.path.join(yolo_dir, 'yolo-coco', 'coco.names')
weights_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.weights')
config_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.cfg')

# Test images representing 4 different lanes at intersection
test_images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']

print("=" * 70)
print("SMART TRAFFIC MANAGEMENT SYSTEM - MULTI-LANE DETECTION TEST")
print("=" * 70)
print("\nSimulating a 4-way intersection with traffic cameras on each lane...")
print("This represents the real-world scenario where the system analyzes")
print("congestion from all 4 directions to make smart signal decisions.\n")

# Load YOLO once
print("Loading YOLO model...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
print("✓ Model loaded!\n")

# Process each lane
results = []
lane_names = ['North Lane', 'East Lane', 'South Lane', 'West Lane']

for idx, img_name in enumerate(test_images):
    img_path = os.path.join(yolo_dir, 'images', img_name)
    
    if not os.path.exists(img_path):
        print(f"⚠️  {lane_names[idx]}: Image not found, skipping...")
        continue
    
    print(f"📷 Analyzing {lane_names[idx]} ({img_name})...")
    
    # Load and process image
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
            confidence = scores[classID]
            
            if confidence > 0.5:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    
    # Apply NMS
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    
    # Count vehicles
    vehicle_count = 0
    if len(idxs) > 0:
        for i in idxs.flatten():
            if LABELS[classIDs[i]] in vehicle_types:
                vehicle_count += 1
    
    results.append({
        'lane': lane_names[idx],
        'image': img_name,
        'count': vehicle_count
    })
    
    print(f"   ✓ Detected {vehicle_count} vehicles\n")

# Display results and make traffic signal decision
print("=" * 70)
print("TRAFFIC ANALYSIS RESULTS")
print("=" * 70)
print("\nVehicle count per lane:\n")

max_count = 0
max_lane_idx = 0

for idx, result in enumerate(results):
    bar = "█" * (result['count'] // 2)  # Visual bar chart
    print(f"  {result['lane']:12} : {result['count']:3} vehicles  {bar}")
    
    if result['count'] > max_count:
        max_count = result['count']
        max_lane_idx = idx

print("\n" + "=" * 70)
print("SMART SIGNAL CONTROL DECISION")
print("=" * 70)

if results:
    print(f"\n🚦 Signal Status:")
    for idx, result in enumerate(results):
        if idx == max_lane_idx:
            print(f"   {result['lane']:12} : 🟢 GREEN  (Highest congestion: {result['count']} vehicles)")
        else:
            print(f"   {result['lane']:12} : 🔴 RED    ({result['count']} vehicles)")
    
    print(f"\n💡 Decision: Give GREEN signal to {results[max_lane_idx]['lane']}")
    print(f"   Reason: Highest traffic density ({max_count} vehicles)")
    print(f"   This reduces overall waiting time and congestion!")

print("\n" + "=" * 70)
print("✓ MULTI-LANE TEST COMPLETE!")
print("=" * 70)
print("\nThis demonstrates how the system automatically prioritizes")
print("the lane with highest congestion for optimal traffic flow.")
