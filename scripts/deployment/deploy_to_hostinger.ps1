# PowerShell script to prepare and deploy frontend to Hostinger
# This builds the frontend as static files ready for Hostinger

$rootDir = $PSScriptRoot
$frontendDir = Join-Path $rootDir "frontend"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Preparing Frontend for Hostinger" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if frontend directory exists
if (-not (Test-Path $frontendDir)) {
    Write-Host "ERROR: frontend/ directory not found!" -ForegroundColor Red
    exit 1
}

# Step 1: Backup original next.config.js
Write-Host "Step 1: Backing up next.config.js..." -ForegroundColor Cyan
$originalConfig = Join-Path $frontendDir "next.config.js"
$backupConfig = Join-Path $frontendDir "next.config.js.backup"
if (Test-Path $originalConfig) {
    Copy-Item $originalConfig $backupConfig -Force
    Write-Host "  ✓ Backup created: next.config.js.backup" -ForegroundColor Gray
}

# Step 2: Use Hostinger config
Write-Host ""
Write-Host "Step 2: Using Hostinger config..." -ForegroundColor Cyan
$hostingerConfig = Join-Path $frontendDir "next.config.hostinger.js"
if (Test-Path $hostingerConfig) {
    Copy-Item $hostingerConfig $originalConfig -Force
    Write-Host "  ✓ Using next.config.hostinger.js" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ Hostinger config not found, using default" -ForegroundColor Yellow
}

# Step 3: Check for .env.production
Write-Host ""
Write-Host "Step 3: Checking environment variables..." -ForegroundColor Cyan
$envFile = Join-Path $frontendDir ".env.production"
if (-not (Test-Path $envFile)) {
    Write-Host "  ⚠ .env.production not found!" -ForegroundColor Yellow
    Write-Host "  Creating template..." -ForegroundColor Gray
    $backendUrl = Read-Host "Enter your Railway backend URL (e.g., https://xxx.railway.app)"
    @"
NEXT_PUBLIC_API_URL=$backendUrl
"@ | Out-File $envFile -Encoding UTF8
    Write-Host "  ✓ Created .env.production" -ForegroundColor Gray
} else {
    Write-Host "  ✓ .env.production found" -ForegroundColor Gray
}

# Step 4: Install dependencies
Write-Host ""
Write-Host "Step 4: Installing dependencies..." -ForegroundColor Cyan
Set-Location $frontendDir
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ npm install failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Dependencies installed" -ForegroundColor Gray

# Step 5: Build frontend
Write-Host ""
Write-Host "Step 5: Building frontend (static export)..." -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Build completed" -ForegroundColor Gray

# Step 6: Check output
Write-Host ""
Write-Host "Step 6: Checking build output..." -ForegroundColor Cyan
$outDir = Join-Path $frontendDir "out"
if (Test-Path $outDir) {
    $fileCount = (Get-ChildItem -Path $outDir -Recurse -File).Count
    $dirSize = [math]::Round((Get-ChildItem -Path $outDir -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    Write-Host "  ✓ Build output found in 'out' folder" -ForegroundColor Gray
    Write-Host "  ✓ Files: $fileCount" -ForegroundColor Gray
    Write-Host "  ✓ Size: $dirSize MB" -ForegroundColor Gray
} else {
    Write-Host "  ✗ Build output not found!" -ForegroundColor Red
    exit 1
}

# Step 7: Create upload instructions
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps to upload to Hostinger:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1: Via SSH" -ForegroundColor Cyan
Write-Host "  scp -r frontend/out/* your-username@your-domain.com:~/public_html/" -ForegroundColor White
Write-Host ""
Write-Host "Option 2: Via FTP (FileZilla)" -ForegroundColor Cyan
Write-Host "  1. Connect to your Hostinger FTP" -ForegroundColor White
Write-Host "  2. Navigate to public_html/" -ForegroundColor White
Write-Host "  3. Upload ALL files from frontend/out/ folder" -ForegroundColor White
Write-Host ""
Write-Host "Option 3: Via cPanel File Manager" -ForegroundColor Cyan
Write-Host "  1. Login to cPanel" -ForegroundColor White
Write-Host "  2. Go to File Manager" -ForegroundColor White
Write-Host "  3. Navigate to public_html/" -ForegroundColor White
Write-Host "  4. Upload files from frontend/out/ folder" -ForegroundColor White
Write-Host ""
Write-Host "Build output location: frontend/out/" -ForegroundColor Yellow
Write-Host ""

Set-Location $rootDir

