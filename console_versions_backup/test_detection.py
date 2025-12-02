"""
Quick test of YOLO vehicle detection - Standalone version
Run this from the project root directory
"""
import os
import cv2
import numpy as np

# Set paths
yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
test_image_path = os.path.join(yolo_dir, 'images', '1.jpg')
labels_path = os.path.join(yolo_dir, 'yolo-coco', 'coco.names')
weights_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.weights')
config_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.cfg')

print("=" * 60)
print("SMART TRAFFIC MANAGEMENT SYSTEM - VEHICLE DETECTION TEST")
print("=" * 60)

# Check if files exist
print("\n1. Checking required files...")
if not os.path.exists(test_image_path):
    print(f"   ❌ Test image not found: {test_image_path}")
    exit(1)
if not os.path.exists(weights_path):
    print(f"   ❌ YOLO weights not found: {weights_path}")
    exit(1)
if not os.path.exists(config_path):
    print(f"   ❌ YOLO config not found: {config_path}")
    exit(1)
if not os.path.exists(labels_path):
    print(f"   ❌ YOLO labels not found: {labels_path}")
    exit(1)

print("   ✓ All required files found!")

# Load YOLO
print("\n2. Loading YOLO model... (this may take a moment)")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
LABELS = open(labels_path).read().strip().split("\n")
print(f"   ✓ YOLO model loaded successfully!")
print(f"   ✓ {len(LABELS)} object classes available")

# Load and process image
print(f"\n3. Processing image: {os.path.basename(test_image_path)}")
image = cv2.imread(test_image_path)
(H, W) = image.shape[:2]
print(f"   Image size: {W}x{H} pixels")

# Get YOLO output layers
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Create blob and forward pass
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
layerOutputs = net.forward(ln)
print("   ✓ YOLO detection complete!")

# Process detections
boxes = []
confidences = []
classIDs = []

for output in layerOutputs:
    for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        
        if confidence > 0.5:  # Confidence threshold
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

# Apply non-maxima suppression
idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

# Count vehicles
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
vehicle_count = 0
detections = {}

if len(idxs) > 0:
    for i in idxs.flatten():
        label = LABELS[classIDs[i]]
        if label in vehicle_types:
            vehicle_count += 1
            detections[label] = detections.get(label, 0) + 1

# Display results
print("\n" + "=" * 60)
print("DETECTION RESULTS")
print("=" * 60)
print(f"\n📊 Total vehicles detected: {vehicle_count}")
if detections:
    print("\nBreakdown by vehicle type:")
    for vehicle_type, count in sorted(detections.items()):
        print(f"   • {vehicle_type}: {count}")
else:
    print("   (No vehicles detected in this image)")

print("\n" + "=" * 60)
print("✓ TEST COMPLETE!")
print("=" * 60)
