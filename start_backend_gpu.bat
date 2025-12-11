@echo off
echo ========================================
echo   Starting Backend with GPU Support
echo ========================================
echo.
echo Using Python 3.11 with CUDA-enabled PyTorch
echo GPU: NVIDIA GeForce RTX 3050 Laptop GPU
echo.

cd /d "%~dp0"
call venv_gpu\Scripts\activate.bat
python unified_backend.py

pause
