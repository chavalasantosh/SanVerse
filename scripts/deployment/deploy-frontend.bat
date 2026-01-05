@echo off
echo ========================================
echo   Deploy Frontend to Railway
echo ========================================
echo.

cd frontend

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
    echo Alternative: Use Railway Dashboard instead:
    echo   1. Go to: https://railway.com/project/2a7fd91e-4260-44b2-b41e-a39d951fe026
    echo   2. Click "New" → "Empty Service"
    echo   3. Root Directory: frontend
    echo   4. Add variable: NEXT_PUBLIC_API_URL=https://keen-happiness-production.up.railway.app
    pause
    exit /b 1
)

echo.
echo Step 2: Setting environment variable...
railway variables --set "NEXT_PUBLIC_API_URL=https://keen-happiness-production.up.railway.app"

echo.
echo Step 3: Deploying frontend...
railway up

echo.
echo ✅ Frontend deployment started!
echo.
echo Check status at: https://railway.com/project/2a7fd91e-4260-44b2-b41e-a39d951fe026
echo.
pause

