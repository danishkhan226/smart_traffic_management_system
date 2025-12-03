@echo off
cls
echo ====================================
echo  SMART TRAFFIC DASHBOARD - STARTUP
echo ====================================
echo.

REM Activate Python environment
echo Starting Python backend...
call venv311\Scripts\activate.bat

REM Start backend in new window
start "Backend (Port 5005)" cmd /k "python unified_backend.py"
timeout /t 3 /nobreak >nul

REM Start React frontend in new window
echo Starting React frontend...
cd react-dashboard
start "React (Port 5173)" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:5173

echo.
echo ====================================
echo  Dashboard running at:
echo  http://localhost:5173
echo ====================================
pause
