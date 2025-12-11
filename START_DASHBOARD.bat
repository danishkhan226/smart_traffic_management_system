@echo off
echo ========================================
echo Smart Traffic Management System
echo Starting Backend (GPU) and Frontend...
echo ========================================
echo.

REM Start Backend with GPU support (Python 3.11 + CUDA)
echo [1/2] Starting Backend Server with GPU...
echo Using: Python 3.11 + PyTorch CUDA 12.1
echo GPU: NVIDIA GeForce RTX 3050 Laptop GPU
start "Backend Server (GPU)" cmd /k "cd /d %~dp0 && venv_gpu\Scripts\python.exe unified_backend.py"
timeout /t 3 /nobreak >nul

REM Start Frontend (React)
echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d %~dp0react-dashboard && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo Backend:  http://localhost:5005 (GPU-accelerated)
echo Frontend: http://localhost:5173
echo ========================================
echo.
echo [3/3] Waiting for servers to initialize...
timeout /t 8 /nobreak >nul

echo Opening dashboard in browser...
start http://localhost:5173

echo.
echo ========================================
echo Dashboard opened in your default browser!
echo ========================================
echo.
echo NOTE: Live Camera will use GPU acceleration!
echo Expected FPS: 30-60 FPS (vs 5-10 on CPU)
echo.
echo Press any key to close this window...
pause >nul
