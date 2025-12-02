"""
Frame extraction script for traffic videos
This prepares video data for the traffic management system
"""
import os
import cv2

def extract_frames(video_path, output_folder, max_frames=700):
    """Extract frames from video file"""
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return False
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open video
    vs = cv2.VideoCapture(video_path)
    video_name = os.path.basename(video_path)
    
    print(f"📹 Processing {video_name}...")
    
    count = 0
    while True:
        (grabbed, frame) = vs.read()
        if not grabbed or count >= max_frames:
            break
        
        # Save frame
        frame_path = os.path.join(output_folder, f'{count}.jpg')
        cv2.imwrite(frame_path, frame)
        count += 1
        
        # Progress indicator
        if count % 100 == 0:
            print(f"   Extracted {count} frames...")
    
    vs.release()
    print(f"   ✓ Extracted {count} frames total\n")
    return count

# Main execution
print("=" * 60)
print("SMART TRAFFIC MANAGEMENT SYSTEM - FRAME EXTRACTION")
print("=" * 60)
print("\nExtracting frames from traffic camera videos...")
print("This prepares the data for real-time traffic analysis.\n")

yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
videos_dir = os.path.join(yolo_dir, 'videos_raw')
frames_base = os.path.join(yolo_dir, 'frames')

# Process each video (1.mp4, 2.mp4, 3.mp4)
for video_num in range(1, 4):
    video_file = f'{video_num}.mp4'
    video_path = os.path.join(videos_dir, video_file)
    output_folder = os.path.join(frames_base, str(video_num))
    
    total = extract_frames(video_path, output_folder)

print("=" * 60)
print("✓ FRAME EXTRACTION COMPLETE!")
print("=" * 60)
print("\nFrames are now ready for traffic analysis.")
print("The system can now process these frames to detect vehicles")
print("and make real-time traffic signal decisions.\n")
