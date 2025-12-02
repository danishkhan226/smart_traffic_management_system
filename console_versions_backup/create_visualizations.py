"""
Smart Traffic Management System - Visualization Demo
Creates visual outputs showing vehicle detection and signal control decisions
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

# Configuration
yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
labels_path = os.path.join(yolo_dir, 'yolo-coco', 'coco.names')
weights_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.weights')
config_path = os.path.join(yolo_dir, 'yolo-coco', 'yolov3.cfg')
output_dir = os.path.join(yolo_dir, 'visualization_output')
os.makedirs(output_dir, exist_ok=True)

print("=" * 70)
print("SMART TRAFFIC MANAGEMENT SYSTEM - VISUALIZATION")
print("=" * 70)
print("\nGenerating visual demonstrations of vehicle detection...")
print("This will create annotated images showing detected vehicles.\n")

# Load YOLO
print("Loading YOLO model...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
LABELS = open(labels_path).read().strip().split("\n")
vehicle_types = {'car', 'truck', 'bus', 'bicycle', 'motorbike', 'motorcycle'}
print("✓ Model loaded!\n")

# Colors for bounding boxes (BGR format for OpenCV)
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

def detect_and_visualize(img_path, output_path, confidence=0.5, threshold=0.3):
    """Detect vehicles and create annotated image"""
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
    
    # Count vehicles and draw boxes
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
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                
                # Add label
                text = f"{label}: {confidences[i]:.2f}"
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
    
    # Add summary text at top
    summary = f"Total Vehicles: {vehicle_count}"
    cv2.putText(image, summary, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               1, (0, 255, 0), 2)
    
    # Save annotated image
    cv2.imwrite(output_path, image)
    
    return vehicle_count, vehicle_breakdown, image

# Visualize detection on sample images
test_images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
results = []

for idx, img_name in enumerate(test_images):
    img_path = os.path.join(yolo_dir, 'images', img_name)
    
    if not os.path.exists(img_path):
        continue
    
    output_path = os.path.join(output_dir, f'detected_{img_name}')
    
    print(f"📷 Processing {img_name}...")
    count, breakdown, annotated_img = detect_and_visualize(img_path, output_path)
    results.append({
        'name': img_name,
        'count': count,
        'breakdown': breakdown,
        'image': cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    })
    print(f"   ✓ Detected {count} vehicles - Saved to {output_path}")

print("\n" + "=" * 70)
print("Creating visual dashboard...")
print("=" * 70)

# Create comprehensive visualization dashboard
fig = plt.figure(figsize=(16, 12))
gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

# Main title
fig.suptitle('Smart Traffic Management System - Vehicle Detection Dashboard', 
             fontsize=16, fontweight='bold')

# Display annotated images in grid
for idx, result in enumerate(results[:4]):
    ax = fig.add_subplot(gs[idx // 2, idx % 2])
    ax.imshow(result['image'])
    lane_names = ['North Lane', 'East Lane', 'South Lane', 'West Lane']
    ax.set_title(f"{lane_names[idx]}: {result['count']} Vehicles", 
                fontsize=12, fontweight='bold')
    ax.axis('off')

# Add traffic signal decision visualization
ax_signal = fig.add_subplot(gs[2, :])
ax_signal.set_title('Traffic Signal Control Decision', fontsize=14, fontweight='bold')
ax_signal.axis('off')

# Find lane with max vehicles
max_idx = 0
max_count = results[0]['count']
for i, r in enumerate(results):
    if r['count'] > max_count:
        max_count = r['count']
        max_idx = i

# Draw signal visualization
lane_names = ['North Lane', 'East Lane', 'South Lane', 'West Lane']
colors_map = ['red', 'red', 'red', 'red']
colors_map[max_idx] = 'green'

y_positions = [0.7, 0.5, 0.3, 0.1]
for idx, (lane, color, result) in enumerate(zip(lane_names, colors_map, results)):
    # Traffic light circle
    circle = patches.Circle((0.15, y_positions[idx]), 0.05, 
                           color=color, ec='black', linewidth=2)
    ax_signal.add_patch(circle)
    
    # Lane name and vehicle count
    status = "GREEN" if color == 'green' else "RED"
    text = f"{lane}: {status} - {result['count']} vehicles"
    ax_signal.text(0.25, y_positions[idx], text, 
                  fontsize=12, va='center', fontweight='bold')
    
    # Vehicle bar chart
    bar_width = result['count'] / max_count * 0.3 if max_count > 0 else 0
    rect = patches.Rectangle((0.6, y_positions[idx] - 0.03), bar_width, 0.06, 
                            color='blue', alpha=0.6)
    ax_signal.add_patch(rect)
    ax_signal.text(0.95, y_positions[idx], str(result['count']), 
                  fontsize=10, va='center', ha='right')

ax_signal.set_xlim(0, 1)
ax_signal.set_ylim(0, 1)

# Add decision explanation
decision_text = f"\nDecision: GREEN signal to {lane_names[max_idx]} (highest congestion: {max_count} vehicles)"
ax_signal.text(0.5, 0.95, decision_text, 
              fontsize=11, ha='center', style='italic', 
              bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

# Save dashboard
dashboard_path = os.path.join(output_dir, 'traffic_dashboard.png')
plt.savefig(dashboard_path, dpi=150, bbox_inches='tight')
print(f"\n✓ Dashboard saved to: {dashboard_path}")

# Create individual detection example
fig2, ax2 = plt.subplots(1, 1, figsize=(12, 8))
ax2.imshow(results[0]['image'])
ax2.set_title(f'Vehicle Detection Example - {results[0]["count"]} Vehicles Detected', 
             fontsize=14, fontweight='bold')
ax2.axis('off')

# Add legend
breakdown_text = "Detected Vehicles:\n"
for vehicle_type, count in results[0]['breakdown'].items():
    breakdown_text += f"  • {vehicle_type}: {count}\n"
ax2.text(0.02, 0.98, breakdown_text, transform=ax2.transAxes, 
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

detection_example_path = os.path.join(output_dir, 'detection_example.png')
plt.savefig(detection_example_path, dpi=150, bbox_inches='tight')
print(f"✓ Detection example saved to: {detection_example_path}")

print("\n" + "=" * 70)
print("VISUALIZATION COMPLETE!")
print("=" * 70)
print(f"\nGenerated visualizations:")
print(f"  📊 Traffic Dashboard: {dashboard_path}")
print(f"  🚗 Detection Example: {detection_example_path}")
print(f"  📷 Annotated Images: {output_dir}")
print(f"\nOpen these files to see:")
print("  - Bounding boxes around detected vehicles")
print("  - Vehicle counts and classifications")
print("  - Smart traffic signal decisions")
print("  - Real-time congestion analysis")
