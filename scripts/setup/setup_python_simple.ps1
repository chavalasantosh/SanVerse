# Simple Python Setup Script
Write-Host "Setting up Python aliases..." -ForegroundColor Cyan

# Get Python path
$pythonExe = (py -c "import sys; print(sys.executable)" 2>$null)
if (-not $pythonExe) {
    Write-Host "Error: Python not found via 'py' launcher" -ForegroundColor Red
    exit 1
}

Write-Host "Python found at: $pythonExe" -ForegroundColor Green

# Define functions in current session
function global:python { & $pythonExe $args }
function global:python3 { & $pythonExe $args }
function global:py3 { & $pythonExe $args }

# Export to profile
$profilePath = $PROFILE
$profileContent = @"
# Python aliases
`$pythonExe = "$pythonExe"
function python { & `$pythonExe `$args }
function python3 { & `$pythonExe `$args }
function py3 { & `$pythonExe `$args }
"@

# Append to profile if not exists
if (Test-Path $profilePath) {
    $existing = Get-Content $profilePath -Raw
    if ($existing -notmatch "# Python aliases") {
        Add-Content -Path $profilePath -Value "`n$profileContent"
    }
} else {
    Set-Content -Path $profilePath -Value $profileContent
}

# Create batch files
$localBin = "$env:USERPROFILE\.local\bin"
if (-not (Test-Path $localBin)) {
    New-Item -ItemType Directory -Path $localBin -Force | Out-Null
}

$batchContent = "@echo off`r`n`"$pythonExe`" %*"
Set-Content -Path "$localBin\python.bat" -Value $batchContent
Set-Content -Path "$localBin\python3.bat" -Value $batchContent
Set-Content -Path "$localBin\py3.bat" -Value $batchContent

# Add to PATH if not there
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$localBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$localBin", "User")
    $env:Path = "$env:Path;$localBin"
    Write-Host "Added $localBin to PATH" -ForegroundColor Green
}

Write-Host "`nTesting..." -ForegroundColor Yellow
python --version
python3 --version
py3 --version

Write-Host "`nSetup complete! All Python commands should now work." -ForegroundColor Green

