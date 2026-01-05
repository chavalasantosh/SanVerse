# Setup Python Aliases Script
# This script sets up aliases so python, python3, py, and py3 all work

Write-Host "Setting up Python aliases..." -ForegroundColor Cyan

# Get the actual Python executable path
$pythonPath = (py -c "import sys; print(sys.executable)" 2>$null)
if (-not $pythonPath) {
    Write-Host "Error: Could not find Python installation. Make sure 'py' launcher works." -ForegroundColor Red
    exit 1
}

Write-Host "Found Python at: $pythonPath" -ForegroundColor Green

# PowerShell Profile path
$profilePath = $PROFILE

# Check if profile exists, create if not
if (-not (Test-Path $profilePath)) {
    $profileDir = Split-Path $profilePath -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    New-Item -ItemType File -Path $profilePath -Force | Out-Null
    Write-Host "Created PowerShell profile at: $profilePath" -ForegroundColor Yellow
}

# Read existing profile content
$existingContent = ""
if (Test-Path $profilePath) {
    $existingContent = Get-Content $profilePath -Raw
}

# Check if Python aliases already exist
$needsUpdate = $true
if ($existingContent -match "# Python aliases") {
    Write-Host "Python aliases already exist in profile. Updating..." -ForegroundColor Yellow
    # Remove old Python alias section
    $lines = Get-Content $profilePath
    $newLines = @()
    $skipSection = $false
    foreach ($line in $lines) {
        if ($line -match "# Python aliases") {
            $skipSection = $true
            continue
        }
        if ($skipSection -and $line -match "# End Python aliases") {
            $skipSection = $false
            continue
        }
        if (-not $skipSection) {
            $newLines += $line
        }
    }
    $existingContent = $newLines -join [Environment]::NewLine
}

# Add Python aliases
$pythonAliases = @"

# Python aliases - Added by setup_python_aliases.ps1
# Make python, python3, and py3 all point to the same Python installation
`$pythonExe = "$pythonPath"
if (Test-Path `$pythonExe) {
    function python { & `$pythonExe `$args }
    function python3 { & `$pythonExe `$args }
    function py3 { & `$pythonExe `$args }
    Set-Alias -Name python -Value python -Force -ErrorAction SilentlyContinue
    Set-Alias -Name python3 -Value python3 -Force -ErrorAction SilentlyContinue
    Set-Alias -Name py3 -Value py3 -Force -ErrorAction SilentlyContinue
}
# End Python aliases
"@

# Append aliases to profile
if ($existingContent -and $existingContent.Trim() -ne "") {
    $newContent = $existingContent.Trim() + [Environment]::NewLine + [Environment]::NewLine + $pythonAliases
} else {
    $newContent = $pythonAliases
}

# Write to profile
Set-Content -Path $profilePath -Value $newContent -Encoding UTF8
Write-Host "✓ Added Python aliases to PowerShell profile" -ForegroundColor Green

# Create batch files in user's local bin directory (if it exists in PATH)
$localBin = "$env:USERPROFILE\.local\bin"
if (-not (Test-Path $localBin)) {
    New-Item -ItemType Directory -Path $localBin -Force | Out-Null
    Write-Host "Created directory: $localBin" -ForegroundColor Yellow
}

# Create batch files
$batchContent = "@echo off`r`n`"$pythonPath`" %*"
$batchFiles = @("python.bat", "python3.bat", "py3.bat")

foreach ($batchName in $batchFiles) {
    $batchPath = Join-Path $localBin $batchName
    Set-Content -Path $batchPath -Value $batchContent -Encoding ASCII
    Write-Host "✓ Created $batchName" -ForegroundColor Green
}

# Check if local bin is in PATH
$pathEntries = $env:PATH -split ';'
if ($localBin -notin $pathEntries) {
    Write-Host ""
    Write-Host "⚠ Warning: $localBin is not in your PATH" -ForegroundColor Yellow
    Write-Host "To add it, run:" -ForegroundColor Yellow
    Write-Host "  [Environment]::SetEnvironmentVariable('Path', `$env:Path + ';$localBin', 'User')" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or manually add it to your system PATH." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python aliases setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use:" -ForegroundColor Yellow
Write-Host "  - python" -ForegroundColor White
Write-Host "  - python3" -ForegroundColor White
Write-Host "  - py" -ForegroundColor White
Write-Host "  - py3" -ForegroundColor White
Write-Host ""
Write-Host "Note: You may need to restart your PowerShell session for aliases to take effect." -ForegroundColor Yellow
Write-Host "Or run: . `$PROFILE" -ForegroundColor Cyan
