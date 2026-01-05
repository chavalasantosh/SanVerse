# Railway Deployment Script
# This script copies Railway configuration files to the project root for deployment

Write-Host "🚂 Preparing Railway deployment files..." -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $PSScriptRoot
$railwayFolder = $PSScriptRoot

# Files to copy
$files = @(
    "railway.json",
    "Procfile",
    "runtime.txt"
)

foreach ($file in $files) {
    $source = Join-Path $railwayFolder $file
    $destination = Join-Path $projectRoot $file
    
    if (Test-Path $source) {
        Copy-Item $source $destination -Force
        Write-Host "✅ Copied $file to project root" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: $file not found in railway folder" -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Railway files are now in the project root!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. railway login" -ForegroundColor White
Write-Host "  2. railway link -p 2a7fd91e-4260-44b2-b41e-a39d951fe026" -ForegroundColor White
Write-Host "  3. railway up" -ForegroundColor White

