"""
Automated Demo - Upload 4 images simultaneously for 4-way intersection analysis
"""
import requests
from pathlib import Path

# Configuration
API_URL = "http://localhost:5001/upload-multi"
SAMPLE_IMAGES = [
    r"yolo\images\1.jpg",  # North Lane
    r"yolo\images\2.jpg",  # East Lane
    r"yolo\images\3.jpg",  # South Lane
    r"yolo\images\4.jpg",  # West Lane
]

print("=" * 70)
print("AUTOMATED 4-WAY INTERSECTION DEMO")
print("=" * 70)
print("\nUploading 4 images simultaneously to simulate a 4-way intersection")
print("This demonstrates multi-lane traffic analysis with signal control\n")

# Check if all images exist
for idx, img_path in enumerate(SAMPLE_IMAGES, 1):
    if not Path(img_path).exists():
        print(f"❌ Error: Image {idx} not found at {img_path}")
        exit(1)

# Prepare files for upload
files = {}
lane_names = ['North', 'East', 'South', 'West']

for idx, img_path in enumerate(SAMPLE_IMAGES, 1):
    with open(img_path, 'rb') as f:
        files[f'lane{idx}'] = (f'{lane_names[idx-1]}.jpg', f.read(), 'image/jpeg')

print("📤 Uploading images to multi-lane API...")
print(f"   North Lane: {SAMPLE_IMAGES[0]}")
print(f"   East Lane:  {SAMPLE_IMAGES[1]}")
print(f"   South Lane: {SAMPLE_IMAGES[2]}")
print(f"   West Lane:  {SAMPLE_IMAGES[3]}")

try:
    response = requests.post(API_URL, files=files)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "=" * 70)
        print("✅ 4-WAY INTERSECTION ANALYSIS COMPLETE!")
        print("=" * 70)
        
        # Overall summary
        print(f"\n📊 OVERALL SUMMARY:")
        print(f"   Total Vehicles Detected: {data['signal_decision']['total_vehicles']}")
        print(f"   Green Signal Assigned To: {data['signal_decision']['green_lane']} Lane")
        print(f"   Reason: Highest congestion ({data['signal_decision']['green_lane_count']} vehicles)")
        
        # Lane-by-lane results
        print(f"\n🚗 LANE-BY-LANE RESULTS:")
        for result in data['results']:
            print(f"\n   {result['lane']} Lane:")
            if 'error' in result:
                print(f"      ❌ Error: {result['error']}")
            else:
                print(f"      ✓ Vehicles: {result['count']}")
                if result.get('breakdown'):
                    for vehicle_type, count in result['breakdown'].items():
                        print(f"         • {vehicle_type}: {count}")
        
        # Traffic signal decision
        print(f"\n🚦 TRAFFIC SIGNAL CONTROL DECISION:")
        for signal in data['signal_decision']['signals']:
            status_icon = "🟢" if signal['status'] == 'GREEN' else "🔴"
            print(f"   {status_icon} {signal['lane']:6} Lane: {signal['status']:5} - {signal['count']} vehicles")
        
        print(f"\n💡 SMART DECISION:")
        print(f"   The system gave GREEN signal to {data['signal_decision']['green_lane']} Lane")
        print(f"   because it has the highest traffic density.")
        print(f"   This reduces overall waiting time and congestion!")
        
        print("\n" + "=" * 70)
        print("This is exactly what you see in the web dashboard!")
        print("=" * 70)
        
        print(f"\n🌐 View in browser:")
        print(f"   Open http://localhost:5001")
        print(f"   Upload your own 4 images to see live results!")
        
    else:
        print(f"❌ Error: Server returned status code {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to the web server.")
    print("   Make sure the server is running: python web_dashboard_multi.py")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 70)
