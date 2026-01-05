@echo off
echo ========================================
echo   Deploy n8n to Railway
echo ========================================
echo.

cd n8n

echo Step 1: Linking to Railway...
echo NOTE: You'll need to manually select:
echo   - Workspace: My Projects
echo   - Project: keen-happiness
echo   - Service: Create new service
echo.
railway link

if errorlevel 1 (
    echo.
    echo ❌ Railway link failed or was cancelled
    echo.
    echo Alternative: Use Railway Dashboard instead
    pause
    exit /b 1
)

echo.
echo Step 2: Setting environment variables...
railway variables --set "N8N_BASIC_AUTH_ACTIVE=true"
railway variables --set "N8N_BASIC_AUTH_USER=admin"

set /p N8N_PASSWORD="Enter n8n admin password (or press Enter for 'admin123'): "
if "%N8N_PASSWORD%"=="" set N8N_PASSWORD=admin123

railway variables --set "N8N_BASIC_AUTH_PASSWORD=%N8N_PASSWORD%"
railway variables --set "N8N_HOST=0.0.0.0"
railway variables --set "N8N_PORT=5678"

echo.
echo Step 3: Deploying n8n...
railway up

echo.
echo Step 4: Getting n8n URL...
railway domain

echo.
echo ⚠️  IMPORTANT: Update WEBHOOK_URL with the n8n URL above:
echo    railway variables --set "WEBHOOK_URL=https://your-n8n-url.railway.app"
echo.
echo ✅ n8n deployment started!
echo.
pause

