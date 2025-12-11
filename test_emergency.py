import requests
import os

url = 'http://localhost:5005/upload-emergency'
if not os.path.exists('video_frames/frame_20251128_120619_0.jpg'):
    print("Error: Test image not found!")
    exit(1)

files = {
    'lane1': open('video_frames/frame_20251128_120619_0.jpg', 'rb')
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print(f"Response Content: {response.text}")
