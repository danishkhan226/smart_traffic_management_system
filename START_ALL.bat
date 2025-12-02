@echo off
echo Starting Master Dashboard...
call venv311\Scripts\activate.bat
start "Master Dashboard" cmd /k "python master_dashboard.py"
timeout /t 2 /nobreak >nul

start "Live Camera" cmd /k "python web_dashboard_unified.py"
timeout /t 2 /nobreak >nul

start "4-Way Intersection" cmd /k "python web_dashboard_multi.py"
timeout /t 2 /nobreak >nul

start "Video Analysis" cmd /k "python web_dashboard_video.py"
timeout /t 2 /nobreak >nul

start "Single Image" cmd /k "python web_dashboard.py"

timeout /t 3 /nobreak >nul
start http://localhost:5010

echo.
echo ========================================
echo All dashboards started!
echo ========================================
echo.
echo Master Dashboard: http://localhost:5010
echo Live Camera: http://localhost:5005
echo 4-Way Intersection: http://localhost:5001
echo Video Analysis: http://localhost:5002
echo Single Image: http://localhost:5000
echo.
echo Close the individual dashboard windows to stop them.
echo.
pause
