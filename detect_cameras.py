"""
Quick script to detect available camera sources
"""
import cv2

print("Testing camera sources (0-5)...")
print("=" * 60)

for i in range(6):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # Use DirectShow for better name detection on Windows if possible
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✓ Camera {i}: Available ({frame.shape[1]}x{frame.shape[0]})")
        else:
            print(f"⚠ Camera {i}: Opened but can't read (might be in use)")
        cap.release()
    else:
        print(f"✗ Camera {i}: Not available")

print("=" * 60)
print("\nUsually:")
print("  0 = Built-in laptop webcam")
print("  1 = External webcam / ivcam")
print("\nTry camera index 1 for ivcam!")
