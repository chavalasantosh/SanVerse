Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead("soma_railway.zip")

Write-Host ""
Write-Host "=== ZIP STRUCTURE CHECK ===" -ForegroundColor Green
Write-Host "Total entries: $($zip.Entries.Count)" -ForegroundColor Yellow

Write-Host ""
Write-Host "First 20 file paths:" -ForegroundColor Cyan
$zip.Entries | Select-Object -First 20 | ForEach-Object {
    Write-Host "  $($_.FullName)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Checking folder structure..." -ForegroundColor Yellow
$hasSrc = $zip.Entries | Where-Object { $_.FullName -like "src/*" } | Select-Object -First 1
$hasBackend = $zip.Entries | Where-Object { $_.FullName -like "backend/*" } | Select-Object -First 1
$hasFrontend = $zip.Entries | Where-Object { $_.FullName -like "frontend/*" } | Select-Object -First 1

if ($hasSrc -or $hasBackend -or $hasFrontend) {
    Write-Host ""
    Write-Host "FOLDER STRUCTURE IS CORRECT!" -ForegroundColor Green
    if ($hasSrc) { Write-Host "  Found: $($hasSrc.FullName)" -ForegroundColor Cyan }
    if ($hasBackend) { Write-Host "  Found: $($hasBackend.FullName)" -ForegroundColor Cyan }
    if ($hasFrontend) { Write-Host "  Found: $($hasFrontend.FullName)" -ForegroundColor Cyan }
} else {
    Write-Host ""
    Write-Host "FILES ARE IN ROOT - STRUCTURE NOT PRESERVED!" -ForegroundColor Red
    Write-Host "  All files should be in folders like src/, backend/, frontend/" -ForegroundColor Yellow
}

$zip.Dispose()
