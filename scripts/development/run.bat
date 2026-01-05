@echo off
REM SOMA Run Script for Windows
REM Starts the SOMA API server

echo ==========================================
echo SOMA API Server
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [WARNING] Virtual environment not found.
    echo Running setup.bat first...
    call setup.bat
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Python dependencies are installed
echo [INFO] Checking dependencies...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo [ERROR] Dependencies not installed. Running setup...
    pip install -r requirements.txt
)

REM Get port from environment or use default
if "%PORT%"=="" set PORT=8000

REM Check if port is in use (basic check)
netstat -ano | findstr ":%PORT%" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port %PORT% may be in use.
    echo Use "set PORT=8001" and run again to use a different port
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" (
        exit /b 1
    )
)

echo [INFO] Starting SOMA API Server...
echo [INFO] Server will be available at: http://localhost:%PORT%
echo [INFO] API Documentation at: http://localhost:%PORT%/docs
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Set PORT environment variable
set PORT=%PORT%

REM Start the server
python start.py

