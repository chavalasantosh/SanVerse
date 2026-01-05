@echo off
echo 🎯 Starting SanTOK Main Server...
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing backend requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

REM Start the server
echo 🚀 Starting FastAPI server...
echo 📡 Server will be available at: http://localhost:8000
echo 📚 API Documentation at: http://localhost:8000/docs
echo 🔄 Press Ctrl+C to stop the server
echo ================================================

python main_server.py

pause
