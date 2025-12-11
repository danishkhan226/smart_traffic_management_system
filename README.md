# 🚦 Smart Traffic Management System

An intelligent traffic management system that uses computer vision and YOLO object detection to analyze traffic flow, detect vehicles, and optimize traffic signal timing at intersections.

## ✨ Features

- **Real-time Vehicle Detection**: Uses YOLOv8 for accurate vehicle detection and counting
- **Multi-Lane Support**: Monitors traffic across multiple lanes and intersections
- **Web Dashboard**: Interactive web interface for real-time traffic monitoring
- **Video Analysis**: Process pre-recorded traffic videos for analysis
- **Live Camera Feed**: Support for live camera feeds
- **Emergency Vehicle Detection**: Prioritize emergency vehicles in traffic flow
- **Violation Detection**: Detect traffic violations
- **Master Dashboard**: Centralized control for monitoring multiple intersections
- **Traffic State Persistence**: Save and restore traffic analysis states

## 🛠️ Technologies Used

- **Python 3.11**
- **YOLOv8**: State-of-the-art object detection
- **OpenCV**: Computer vision and video processing
- **Flask**: Web dashboard backend
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization
- **Pillow**: Image processing

## 📋 Prerequisites

- Python 3.11 or higher
- YOLO model weights (`yolov8n.pt`)
- Webcam or video files for testing

## 🚀 Installation

### Backend Setup (Python)

1. Clone the repository:
```bash
git clone https://github.com/danishkhan226/Smart-Traffic-Management-System.git
cd Smart-Traffic-Management-System
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Download road network data (for routing):
```bash
python download_network.py
```

### Frontend Setup (React Dashboard)

```bash
cd react-dashboard
npm install
cd ..
```

## 📖 Usage

### 🎯 Recommended: React Dashboard (Full-Featured)

**IMPORTANT**: You must run BOTH the backend and frontend!

#### Option 1: Quick Start (Windows)
```bash
START_DASHBOARD.bat
```

#### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
python unified_backend.py
```
Backend will run on `http://localhost:5005`

**Terminal 2 - Frontend:**
```bash
cd react-dashboard
npm run dev
```
Frontend will run on `http://localhost:5173`

**Access at**: `http://localhost:5173`

### ⚠️ Troubleshooting

**Error**: "Failed to execute 'json' on 'Response': Unexpected end of JSON input"
- **Cause**: Backend is not running
- **Solution**: Make sure `python unified_backend.py` is running in a separate terminal

---

### Legacy Dashboards (Individual Components)

#### Web Dashboard (Video Upload)
```bash
python web_dashboard.py
```
Access at: `http://localhost:5000`

#### Web Dashboard (Live Camera)
```bash
python web_dashboard_live.py
```

#### Multi-Lane Dashboard
```bash
python web_dashboard_multi.py
```

#### Unified Dashboard
```bash
python web_dashboard_unified.py
```

#### Master Dashboard (Multiple Intersections)
```bash
python master_dashboard.py
```

#### Direct Processing
```bash
python driver.py
```

## 📁 Project Structure

```
Smart-Traffic-Management-System/
├── driver.py                    # Main processing driver
├── yolo.py                      # YOLO detection implementation
├── computerVision.py            # Computer vision utilities
├── logic1.py                    # Traffic logic algorithms
├── web_dashboard*.py            # Various web dashboard implementations
├── master_dashboard.py          # Master control dashboard
├── start_all_dashboards.py      # Launch all dashboards
├── app.py                       # Flask application
├── helper.py                    # Helper functions
├── requirements.txt             # Python dependencies
├── templates/                   # HTML templates for web interface
├── yolo/                        # YOLO model files
└── MapMyIndia/                  # Map integration
```

## 🎯 Key Components

### Vehicle Detection (`yolo.py`)
- Implements YOLOv8 object detection
- Detects and counts vehicles in video frames
- Tracks vehicle positions and movements

### Traffic Logic (`logic1.py`)
- Analyzes traffic density
- Calculates optimal signal timing
- Manages intersection priorities

### Web Dashboards
- **web_dashboard.py**: Basic video upload and processing
- **web_dashboard_live.py**: Live camera feed processing
- **web_dashboard_multi.py**: Multi-lane intersection monitoring
- **web_dashboard_unified.py**: Comprehensive unified interface
- **master_dashboard.py**: Monitor multiple intersections simultaneously

## 🖼️ Screenshots

<img width="732" height="950" alt="image" src="https://github.com/user-attachments/assets/bfd32331-65e1-4727-861c-23173a60a333" />
<img width="1600" height="830" alt="image" src="https://github.com/user-attachments/assets/63c89546-86cd-4618-bf22-00f03b6b90b7" />



## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Your Name - [Your GitHub Profile](https://github.com/danishkhan226)

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- Flask framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.
