"""
Automated Demo - Upload and analyze a sample image via the API
This demonstrates the web dashboard functionality programmatically
"""
import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000/upload"
SAMPLE_IMAGE = r"yolo\images\1.jpg"

print("=" * 70)
print("AUTOMATED WEB DASHBOARD DEMO")
print("=" * 70)
print(f"\nUploading sample image: {SAMPLE_IMAGE}")
print("This simulates what happens when you upload an image via the web UI\n")

# Check if image exists
if not Path(SAMPLE_IMAGE).exists():
    print(f"❌ Error: Sample image not found at {SAMPLE_IMAGE}")
    exit(1)

# Upload image to the API
try:
    with open(SAMPLE_IMAGE, 'rb') as f:
        files = {'image': ('1.jpg', f, 'image/jpeg')}
        print("📤 Sending image to detection API...")
        response = requests.post(API_URL, files=files)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "=" * 70)
        print("✅ DETECTION SUCCESSFUL!")
        print("=" * 70)
        
        print(f"\n📊 RESULTS:")
        print(f"   Total Vehicles Detected: {data['vehicle_count']}")
        
        if data['breakdown']:
            print(f"\n🚗 Vehicle Breakdown:")
            for vehicle_type, count in data['breakdown'].items():
                print(f"   • {vehicle_type.capitalize()}: {count}")
        
        if data['detections']:
            print(f"\n🔍 Individual Detections ({len(data['detections'])} total):")
            for idx, det in enumerate(data['detections'][:5], 1):  # Show first 5
                print(f"   {idx}. {det['type']} - Confidence: {det['confidence']}")
            if len(data['detections']) > 5:
                print(f"   ... and {len(data['detections']) - 5} more")
        
        print(f"\n💾 Result Image: {data['result_filename']}")
        print(f"   View at: http://localhost:5000/results/{data['result_filename']}")
        
        print("\n" + "=" * 70)
        print("This is exactly what you see in the web dashboard!")
        print("=" * 70)
        
        # Save response for reference
        with open('demo_response.json', 'w') as f:
            # Remove base64 image data for readability
            save_data = data.copy()
            if 'result_image' in save_data:
                save_data['result_image'] = '[base64 image data - removed for brevity]'
            json.dump(save_data, f, indent=2)
        
        print(f"\n📄 Full API response saved to: demo_response.json")
        
    else:
        print(f"❌ Error: Server returned status code {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to the web server.")
    print("   Make sure the server is running: python web_dashboard.py")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 70)
print("🌐 To use the web interface manually:")
print("   1. Open http://localhost:5000 in your browser")
print("   2. Drag & drop any traffic image")
print("   3. Click 'Analyze Traffic'")
print("   4. See the same results with visual annotations!")
print("=" * 70)
