# 🚀 Complete Setup Guide for Friends

This guide will help you set up and run the Smart Traffic Management System from GitHub.

## Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Git** installed

## Step-by-Step Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/danishkhan226/Smart-Traffic-Management-System.git
cd Smart-Traffic-Management-System
```

### 2️⃣ Backend Setup (Python/Flask)

#### Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install ALL required packages
pip install opencv-python>=4.8.0
pip install numpy>=1.26.0
pip install flask>=2.3.0
pip install flask-cors
pip install matplotlib>=3.8.0
pip install requests>=2.31.0
pip install Pillow>=10.0.0
pip install ultralytics>=8.0.0
pip install torch torchvision
pip install osmnx>=1.6.0
pip install networkx>=3.0
```

> **Note**: The `requirements.txt` file in the repo is incomplete. Use the commands above instead!

#### Download YOLO Model (if not included)

The YOLOv8 model (`yolov8n.pt`) should be in the root directory. If it's missing:

```bash
# It will download automatically when you run the backend
# OR manually download from Ultralytics
```

#### Download Road Network Data (for Shortest Path feature)

```bash
python download_network.py
```

This will download and cache the Bangalore road network for routing.

### 3️⃣ Frontend Setup (React)

```bash
cd react-dashboard

# Install dependencies
npm install

# Go back to root
cd ..
```

## 🎮 Running the Application

You **MUST** run both the backend AND frontend together:

### Option 1: Use the Batch File (Windows)

```bash
START_DASHBOARD.bat
```

This will automatically start both servers!

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Start Backend:**
```bash
# Make sure you're in the project root
# Activate virtual environment if not already
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Start the Flask backend
python unified_backend.py
```

You should see:
```
🌐 Starting unified web server...
📍 Backend running on: http://localhost:5005
```

**Terminal 2 - Start Frontend:**
```bash
cd react-dashboard
npm run dev
```

You should see:
```
Local: http://localhost:5173
```

### 4️⃣ Access the Dashboard

Open your browser and go to:
```
http://localhost:5173
```

## 🔧 Troubleshooting

### Error: "Failed to execute 'json' on 'Response': Unexpected end of JSON input"

**Cause**: The backend (Python Flask) is not running!

**Solution**: 
1. Open a separate terminal
2. Navigate to the project root
3. Run `python unified_backend.py`
4. Make sure you see "Backend running on: http://localhost:5005"
5. Refresh the React app in your browser

### Error: Module Not Found (Python)

**Cause**: Missing Python dependencies

**Solution**: Make sure you installed ALL packages from Step 2️⃣ above, not just from `requirements.txt`

### Error: Port 5005 already in use

**Cause**: Another instance of the backend is running

**Solution**: 
- Kill the existing process
- Or change the port in `unified_backend.py` (line 644)

### Error: "Routing service not available"

**Cause**: Road network data not downloaded

**Solution**: Run `python download_network.py`

## 📦 Features

Once running, you'll have access to:

- 🎥 **Live Camera** - Real-time vehicle detection
- 📸 **Image Upload** - Analyze traffic images
- 📹 **Video Analysis** - Process traffic videos
- 🚦 **Multi-Lane** - 4-way intersection simulation
- 🗺️ **Shortest Path** - Route optimization in Bangalore

## 🆘 Still Having Issues?

1. Make sure **both terminals are running**:
   - Backend: `http://localhost:5005`
   - Frontend: `http://localhost:5173`

2. Check the terminal outputs for error messages

3. Open browser console (F12) to see frontend errors

4. Try using the batch file instead of manual start

---

**Need Help?** Open an issue on GitHub with:
- Error message
- Terminal output from both backend and frontend
- Your Python and Node.js versions
