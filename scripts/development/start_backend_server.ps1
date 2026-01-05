# Start Backend Server with WebSocket Support
# This script starts the FastAPI server that supports WebSocket connections

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting SanTOK Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python or run .\enable_python_now.ps1" -ForegroundColor Red
    exit 1
}

# Check if port 8000 is already in use
$portInUse = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
if ($portInUse) {
    Write-Host "⚠ Warning: Port 8000 is already in use" -ForegroundColor Yellow
    Write-Host "This might be another server. The WebSocket endpoint requires the FastAPI server." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Do you want to continue anyway? (y/n)"
    if ($response -ne 'y') {
        exit 0
    }
}

# Determine which server file to use
$serverFiles = @(
    "src\servers\main_server.py",
    "backend\src\servers\main_server.py"
)

$serverFile = $null
foreach ($file in $serverFiles) {
    if (Test-Path $file) {
        $serverFile = $file
        break
    }
}

if (-not $serverFile) {
    Write-Host "Error: Could not find main_server.py" -ForegroundColor Red
    Write-Host "Searched for:" -ForegroundColor Yellow
    foreach ($file in $serverFiles) {
        Write-Host "  - $file" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "Found server file: $serverFile" -ForegroundColor Green
Write-Host ""
Write-Host "Starting FastAPI server with WebSocket support..." -ForegroundColor Yellow
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "WebSocket endpoint: ws://localhost:8000/ws/execute" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
try {
    python $serverFile
} catch {
    Write-Host ""
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure all dependencies are installed: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "2. Check if port 8000 is available" -ForegroundColor Yellow
    Write-Host "3. Try running: python -m src.servers.main_server" -ForegroundColor Yellow
    exit 1
}

