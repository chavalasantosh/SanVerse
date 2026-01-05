@echo off
REM SOMA Automated Setup Script for Windows
REM This script sets up the development environment and installs all dependencies

echo ==========================================
echo SOMA Setup Script
echo ==========================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.11 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Found Python version: %PYTHON_VERSION%

REM Check Python version (basic check)
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>nul
if errorlevel 1 (
    echo [ERROR] Python 3.11 or higher is required. Found: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo [SUCCESS] Python version is compatible

REM Check if pip is installed
echo [INFO] Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

echo [SUCCESS] pip is available

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [SUCCESS] pip upgraded

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip in virtual environment
echo [INFO] Upgrading pip in virtual environment...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo [INFO] Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo [SUCCESS] Dependencies installed
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Check if Node.js is needed (optional, for frontend)
if exist "frontend\package.json" (
    echo [INFO] Frontend directory detected. Node.js dependencies are optional.
    where npm >nul 2>&1
    if not errorlevel 1 (
        set /p INSTALL_NODE="Install Node.js dependencies? (y/N): "
        if /i "%INSTALL_NODE%"=="y" (
            echo [INFO] Installing Node.js dependencies...
            cd frontend
            call npm install
            cd ..
            echo [SUCCESS] Node.js dependencies installed
        )
    )
)

REM Verify installation
echo [INFO] Verifying installation...
if exist "verify_installation.py" (
    python verify_installation.py
) else (
    echo [INFO] Running basic verification...
    python -c "import sys; print(f'Python: {sys.version}')"
    python -c "import fastapi; print('FastAPI: OK')" 2>nul || echo [ERROR] FastAPI not installed
    python -c "import uvicorn; print('Uvicorn: OK')" 2>nul || echo [ERROR] Uvicorn not installed
)

echo.
echo ==========================================
echo [SUCCESS] Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the server: run.bat
echo   3. Or manually: python start.py
echo.
echo The server will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
pause

