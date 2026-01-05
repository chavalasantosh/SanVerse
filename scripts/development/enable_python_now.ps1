# Quick script to enable python, python3, py3 in current PowerShell session
$pythonExe = "C:\Users\SCHAVALA\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"

# Set aliases
Set-Alias -Name python -Value $pythonExe -Scope Global -Force
Set-Alias -Name python3 -Value $pythonExe -Scope Global -Force
Set-Alias -Name py3 -Value $pythonExe -Scope Global -Force

# Also ensure PATH includes batch files
$localBin = "$env:USERPROFILE\.local\bin"
if ($env:Path -notlike "*$localBin*") {
    $env:Path = "$localBin;$env:Path"
}

Write-Host "Python commands enabled in this session!" -ForegroundColor Green
Write-Host "Testing..." -ForegroundColor Yellow
python --version
python3 --version
py3 --version
py --version

