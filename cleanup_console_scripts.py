# Cleanup Script - Remove Console Versions
# Run this to clean up redundant console scripts

import os
import shutil

# Files to remove (console versions that have web equivalents)
files_to_remove = [
    'test_detection.py',           # Has web_dashboard.py
    'test_multiple_images.py',     # Has web_dashboard_multi.py
    'run_traffic_system.py',       # Covered by other dashboards
    'demo_multi_lane.py',          # Duplicate
    'demo_web_upload.py',          # Old version
    'create_visualizations.py',    # Will integrate into dashboard
]

# Backup folder
backup_folder = 'console_versions_backup'
os.makedirs(backup_folder, exist_ok=True)

print("=" * 70)
print("CLEANING UP PROJECT - KEEPING ONLY WEB DASHBOARDS")
print("=" * 70)
print("\nMoving console scripts to backup folder...\n")

for filename in files_to_remove:
    if os.path.exists(filename):
        # Move to backup instead of delete
        shutil.move(filename, os.path.join(backup_folder, filename))
        print(f"✓ Moved: {filename} → {backup_folder}/")
    else:
        print(f"⚠ Not found: {filename}")

print("\n" + "=" * 70)
print("CLEANUP COMPLETE!")
print("=" * 70)
print("\n✅ Removed redundant console scripts")
print(f"📁 Backup available in: {backup_folder}/")
print("\n🌐 Your project now has ONLY web dashboards:")
print("   - web_dashboard_unified.py (Live Camera + GPU)")
print("   - web_dashboard_multi.py (4-Way Intersection)")
print("   - web_dashboard_video.py (Video Analysis)")
print("   - web_dashboard.py (Single Image)")
print("\n" + "=" * 70)
