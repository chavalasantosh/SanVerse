@echo off
REM Test setup script for Windows
REM Runs verification and basic server test

echo ==========================================
echo SanTOK Setup Test
echo ==========================================
echo.

REM Run verification
echo Running installation verification...
python verify_installation.py
if errorlevel 1 (
    echo.
    echo Verification failed. Please fix issues before testing server.
    exit /b 1
)

echo.
echo ==========================================
echo Testing server startup...
echo ==========================================
echo.

REM Check if server can start (quick test)
start /B python start.py
timeout /t 3 /nobreak >nul

REM Check if python process is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if errorlevel 1 (
    echo [ERROR] Server failed to start
    exit /b 1
) else (
    echo [SUCCESS] Server started successfully
    taskkill /F /IM python.exe >nul 2>&1
    echo [SUCCESS] Server stopped successfully
    echo.
    echo Setup test PASSED!
    exit /b 0
)

