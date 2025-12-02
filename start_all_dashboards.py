"""
Smart Traffic Management System - All-in-One Launcher
Starts ALL dashboards simultaneously
"""
import subprocess
import sys
import time
import webbrowser
import threading

# Dashboard configurations
DASHBOARDS = [
    {
        'name': 'Master Dashboard',
        'script': 'master_dashboard.py',
        'port': 5010,
        'url': 'http://localhost:5010',
        'description': 'Main Hub - Access All Features'
    },
    {
        'name': 'Live Camera Detection',
        'script': 'web_dashboard_unified.py',
        'port': 5005,
        'url': 'http://localhost:5005',
        'description': 'GPU-Accelerated Real-Time Detection'
    },
    {
        'name': '4-Way Intersection',
        'script': 'web_dashboard_multi.py',
        'port': 5001,
        'url': 'http://localhost:5001',
        'description': 'Multi-Lane Traffic Analysis'
    },
    {
        'name': 'Video Analysis',
        'script': 'web_dashboard_video.py',
        'port': 5002,
        'url': 'http://localhost:5002',
        'description': 'Upload & Analyze Traffic Videos'
    },
    {
        'name': 'Single Image Upload',
        'script': 'web_dashboard.py',
        'port': 5000,
        'url': 'http://localhost:5000',
        'description': 'Quick Vehicle Detection'
    }
]

def start_dashboard(dashboard):
    """Start a dashboard in a new process"""
    print(f"  ▶ Starting {dashboard['name']} on port {dashboard['port']}...")
    
    # Start the dashboard
    process = subprocess.Popen(
        [sys.executable, dashboard['script']],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    return process

def open_browsers():
    """Open all dashboard URLs in browser"""
    print("\n🌐 Opening dashboards in your browser...")
    time.sleep(3)  # Wait for servers to start
    
    # Open master dashboard first
    webbrowser.open('http://localhost:5010')
    print("  ✓ Opened Master Dashboard")

if __name__ == '__main__':
    print("=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM")
    print("ALL-IN-ONE LAUNCHER - STARTING ALL DASHBOARDS")
    print("=" * 70)
    print()
    
    processes = []
    
    print("🚀 Starting all dashboards...\n")
    
    for dashboard in DASHBOARDS:
        try:
            process = start_dashboard(dashboard)
            processes.append({
                'name': dashboard['name'],
                'process': process,
                'port': dashboard['port']
            })
            time.sleep(1)  # Small delay between starts
        except Exception as e:
            print(f"  ✗ Error starting {dashboard['name']}: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ALL DASHBOARDS STARTED!")
    print("=" * 70)
    print("\n📍 Access your dashboards at:\n")
    
    for dashboard in DASHBOARDS:
        print(f"  • {dashboard['name']}")
        print(f"    {dashboard['url']}")
        print(f"    {dashboard['description']}\n")
    
    print("=" * 70)
    print("⭐ RECOMMENDED: Start with the Master Dashboard")
    print("   http://localhost:5010")
    print("=" * 70)
    
    # Open master dashboard in browser
    threading.Timer(2, open_browsers).start()
    
    print("\n💡 TIP: Each dashboard is running in its own window")
    print("🛑 To stop all dashboards: Close this window or press Ctrl+C\n")
    
    try:
        # Keep the main script running
        print("Press Ctrl+C to stop all dashboards...\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all dashboards...")
        for proc_info in processes:
            try:
                proc_info['process'].terminate()
                print(f"  ✓ Stopped {proc_info['name']}")
            except:
                pass
        print("\n✅ All dashboards stopped!")
