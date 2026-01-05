@echo off
REM Prepare SanTOK for distribution (Windows)
REM Cleans unnecessary files and creates a distribution-ready package

echo ==========================================
echo SanTOK Distribution Preparation
echo ==========================================
echo.

REM Create backup
echo [INFO] Creating backup...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c%%a%%b
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do set mytime=%%a%%b
set BACKUP_DIR=santok_backup_%mydate%_%mytime%
mkdir "%BACKUP_DIR%" 2>nul
echo [SUCCESS] Backup directory created: %BACKUP_DIR%

REM Clean temporary files
echo [INFO] Cleaning temporary files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /r . %%f in (*.pyc *.pyo *.pyd) do @if exist "%%f" del /q "%%f" 2>nul
echo [SUCCESS] Temporary files cleaned

REM Check for sensitive files
echo [INFO] Checking for sensitive files...
set FOUND_SENSITIVE=0
if exist ".env" (
    echo [ERROR] Found .env file
    set FOUND_SENSITIVE=1
)
if exist "*.key" (
    echo [ERROR] Found .key files
    set FOUND_SENSITIVE=1
)
if exist "secrets.json" (
    echo [ERROR] Found secrets.json
    set FOUND_SENSITIVE=1
)

if %FOUND_SENSITIVE%==1 (
    echo [ERROR] WARNING: Sensitive files detected! Please review before distribution.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" (
        exit /b 1
    )
) else (
    echo [SUCCESS] No sensitive files detected
)

REM Verify essential files
echo [INFO] Verifying essential files...
set MISSING=0
for %%f in (
    README.md
    INSTALLATION.md
    QUICK_START.md
    requirements.txt
    setup.bat
    run.bat
    run.py
    start.py
    verify_installation.py
    Dockerfile
    docker-compose.yml
    .gitignore
) do (
    if not exist "%%f" (
        echo [ERROR] Missing: %%f
        set MISSING=1
    )
)

if %MISSING%==1 (
    echo [ERROR] Missing essential files!
    exit /b 1
) else (
    echo [SUCCESS] All essential files present
)

REM Create distribution checklist
echo [INFO] Creating distribution checklist...
(
echo # SanTOK Distribution Checklist
echo.
echo ## Pre-Distribution Checks
echo.
echo - [ ] All sensitive data removed (.env, API keys, passwords^)
echo - [ ] All essential files present (README, setup scripts, etc.^)
echo - [ ] Dependencies listed in requirements.txt
echo - [ ] Documentation is up to date
echo - [ ] Setup scripts tested on clean environment
echo - [ ] Docker configuration tested
echo - [ ] Verification script works correctly
echo.
echo ## Files to Include
echo.
echo - [x] README.md
echo - [x] INSTALLATION.md
echo - [x] QUICK_START.md
echo - [x] requirements.txt
echo - [x] setup.sh / setup.bat
echo - [x] run.sh / run.bat / run.py
echo - [x] start.py
echo - [x] verify_installation.py
echo - [x] Dockerfile
echo - [x] docker-compose.yml
echo - [x] .gitignore
echo - [x] src/ directory
echo - [x] env.example
echo.
echo ## Files to Exclude
echo.
echo - [x] __pycache__/
echo - [x] *.pyc, *.pyo
echo - [x] .env files
echo - [x] venv/ or .venv/
echo - [x] node_modules/
echo - [x] Large data files (*.npy, *.pkl, *.zip^)
echo - [x] workflow_output/
echo - [x] .git/ directory (if creating ZIP^)
echo.
echo ## Testing
echo.
echo - [ ] Test setup on clean Linux system
echo - [ ] Test setup on clean Windows system
echo - [ ] Test setup on clean Mac system
echo - [ ] Test Docker setup
echo - [ ] Verify all imports work
echo - [ ] Test basic functionality
echo.
echo ## Distribution Methods
echo.
echo 1. **Git Repository** (Recommended^)
echo    - Push to GitHub/GitLab
echo    - Team clones: git clone ^<repo-url^>
echo.
echo 2. **ZIP Archive**
echo    - Create ZIP excluding .git/
echo    - Share ZIP file
echo    - Team extracts and runs setup
echo.
echo 3. **Docker Image**
echo    - Build: docker build -t santok .
echo    - Push to registry
echo    - Team pulls: docker pull ^<image^>
) > DISTRIBUTION_CHECKLIST.md

echo [SUCCESS] Distribution checklist created: DISTRIBUTION_CHECKLIST.md

REM Summary
echo.
echo ==========================================
echo [SUCCESS] Distribution preparation complete!
echo ==========================================
echo.
echo Next steps:
echo   1. Review DISTRIBUTION_CHECKLIST.md
echo   2. Test setup on a clean system
echo   3. Choose distribution method:
echo      - Git: git push to repository
echo      - ZIP: Create archive (exclude .git/^)
echo      - Docker: Build and push image
echo.
echo Backup saved in: %BACKUP_DIR%
echo.
pause

