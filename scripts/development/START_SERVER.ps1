# Start SOMA Backend Server with WebSocket Support
# This fixes the WebSocket connection error

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting SOMA Backend Server" -ForegroundColor Cyan
Write-Host "  (WebSocket Support Enabled)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Run: .\enable_python_now.ps1" -ForegroundColor Yellow
    exit 1
}

# Find server file
$serverFile = $null
$possiblePaths = @(
    "src\servers\main_server.py",
    "backend\src\servers\main_server.py"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $serverFile = $path
        break
    }
}

if (-not $serverFile) {
    Write-Host "✗ Server file not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Server file: $serverFile" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host "  - HTTP: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - WebSocket: ws://localhost:8000/ws/execute" -ForegroundColor Cyan
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start server
python $serverFile

