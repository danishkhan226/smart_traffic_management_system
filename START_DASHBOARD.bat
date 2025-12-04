@echo off
echo ========================================
echo Smart Traffic Management System
echo Starting Backend and Frontend...
echo ========================================
echo.

REM Start Backend (Python Flask)
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0 && python unified_backend.py"
timeout /t 3 /nobreak >nul

REM Start Frontend (React)
echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d %~dp0react-dashboard && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo Backend:  http://localhost:5005
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
echo Press any key to close this window...
pause >nul
