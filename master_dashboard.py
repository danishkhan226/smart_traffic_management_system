"""
Smart Traffic Management System - Master Dashboard
Central hub for accessing all web-based features
"""
from flask import Flask, render_template, redirect
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def index():
    """Master dashboard landing page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Traffic Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .gpu-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .dashboard-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
        
        .dashboard-card .icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .dashboard-card h2 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.5em;
        }
        
        .dashboard-card p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .dashboard-card .port {
            display: inline-block;
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
            color: #667eea;
            font-weight: bold;
        }
        
        .dashboard-card .status {
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .status.gpu {
            color: #10b981;
            font-weight: bold;
        }
        
        .status.running {
            color: #10b981;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚦 Smart Traffic Management System</h1>
            <p>AI-Powered Traffic Analysis & Control</p>
            <div class="gpu-badge">⚡ GPU Accelerated | RTX 3050 | 25-40 FPS</div>
            
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">4</span>
                    <span class="stat-label">Dashboards</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">5</span>
                    <span class="stat-label">Vehicle Types</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">GPU</span>
                    <span class="stat-label">Accelerated</span>
                </div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <a href="http://localhost:5005" target="_blank" class="dashboard-card">
                <div class="icon">🎥</div>
                <h2>Live Camera Detection</h2>
                <p>Real-time vehicle detection from webcam or IP camera with GPU acceleration.</p>
                <span class="port">Port 5005</span>
                <div class="status gpu">⚡ GPU Accelerated • 25-40 FPS</div>
            </a>
            
            <a href="http://localhost:5001" target="_blank" class="dashboard-card">
                <div class="icon">🚦</div>
                <h2>4-Way Intersection</h2>
                <p>Analyze 4 lanes simultaneously and get smart signal control decisions.</p>
                <span class="port">Port 5001</span>
                <div class="status running">✓ Currently Running</div>
            </a>
            
            <a href="http://localhost:5002" target="_blank" class="dashboard-card">
                <div class="icon">🎬</div>
                <h2>Video Analysis</h2>
                <p>Upload traffic videos for frame-by-frame vehicle detection and statistics.</p>
                <span class="port">Port 5002</span>
                <div class="status">Ready to Start</div>
            </a>
            
            <a href="http://localhost:5000" target="_blank" class="dashboard-card">
                <div class="icon">📸</div>
                <h2>Single Image Upload</h2>
                <p>Quick vehicle detection on individual traffic images with detailed results.</p>
                <span class="port">Port 5000</span>
                <div class="status">Ready to Start</div>
            </a>
        </div>
        
        <div class="footer">
            <p>🤖 Powered by YOLOv8 & PyTorch • Flask Web Framework</p>
            <p style="font-size: 0.9em; margin-top: 10px;">
                GPU: NVIDIA GeForce RTX 3050 Laptop GPU | CUDA 12.1
            </p>
        </div>
    </div>
</body>
</html>
    """

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - MASTER DASHBOARD")
    print("=" * 70)
    print("\n🌐 Starting master dashboard...")
    print("📍 Open your browser and go to: http://localhost:5010")
    print("\n✨ From here you can access all 4 web dashboards!")
    print("=" * 70 + "\n")
    
    # Auto-open browser
    def open_browser():
        webbrowser.open('http://localhost:5010')
    
    threading.Timer(1.5, open_browser).start()
    
    app.run(debug=False, host='0.0.0.0', port=5010)
