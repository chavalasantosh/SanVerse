@echo off
echo ========================================
echo   SOMA Backend Server - Quick Start
echo ========================================
echo.

cd /d "%~dp0"
cd src\servers

echo Starting server...
echo.

py main_server.py

pause

