# PowerShell script to deploy Frontend and n8n to Railway
# Make sure you're logged in: railway login

Write-Host "🚀 Deploying Frontend and n8n to Railway..." -ForegroundColor Green
Write-Host ""

# Get backend URL
$backendUrl = "https://keen-happiness-production.up.railway.app"
Write-Host "✅ Backend URL: $backendUrl" -ForegroundColor Cyan
Write-Host ""

# Deploy Frontend
Write-Host "📦 Step 1: Deploying Frontend..." -ForegroundColor Yellow
Write-Host "Navigate to frontend directory..." -ForegroundColor Gray
Set-Location frontend

Write-Host "Linking to Railway (creates new service)..." -ForegroundColor Gray
railway link

Write-Host "Setting environment variable..." -ForegroundColor Gray
railway variables set "NEXT_PUBLIC_API_URL=$backendUrl"

Write-Host "Deploying frontend..." -ForegroundColor Gray
railway up

Write-Host ""
Write-Host "✅ Frontend deployment initiated!" -ForegroundColor Green
Write-Host "Get your frontend URL with: railway domain" -ForegroundColor Cyan
Write-Host ""

# Go back to root
Set-Location ..

# Deploy n8n
Write-Host "📦 Step 2: Deploying n8n..." -ForegroundColor Yellow
Write-Host "Navigate to n8n directory..." -ForegroundColor Gray
Set-Location n8n

Write-Host "Linking to Railway (creates new service)..." -ForegroundColor Gray
railway link

Write-Host "Setting n8n environment variables..." -ForegroundColor Gray
$n8nPassword = Read-Host "Enter a secure password for n8n admin (or press Enter for default: admin123)"
if ([string]::IsNullOrWhiteSpace($n8nPassword)) {
    $n8nPassword = "admin123"
}

railway variables set "N8N_BASIC_AUTH_ACTIVE=true"
railway variables set "N8N_BASIC_AUTH_USER=admin"
railway variables set "N8N_BASIC_AUTH_PASSWORD=$n8nPassword"
railway variables set "N8N_HOST=0.0.0.0"
railway variables set "N8N_PORT=5678"

Write-Host "Deploying n8n..." -ForegroundColor Gray
railway up

Write-Host ""
Write-Host "✅ n8n deployment initiated!" -ForegroundColor Green
Write-Host "Get your n8n URL with: railway domain" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANT: After n8n deploys, update WEBHOOK_URL:" -ForegroundColor Yellow
Write-Host "   railway variables set WEBHOOK_URL=https://your-n8n-url.railway.app" -ForegroundColor Cyan
Write-Host ""

# Go back to root
Set-Location ..

Write-Host "🎉 Deployment process started!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Check Railway dashboard for deployment status" -ForegroundColor White
Write-Host "2. Get URLs: railway domain (in each service directory)" -ForegroundColor White
Write-Host "3. Update n8n WEBHOOK_URL after deployment" -ForegroundColor White
Write-Host ""

