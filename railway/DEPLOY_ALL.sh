#!/bin/bash
# Bash script to deploy Frontend and n8n to Railway
# Make sure you're logged in: railway login

echo "🚀 Deploying Frontend and n8n to Railway..."
echo ""

# Get backend URL
BACKEND_URL="https://keen-happiness-production.up.railway.app"
echo "✅ Backend URL: $BACKEND_URL"
echo ""

# Deploy Frontend
echo "📦 Step 1: Deploying Frontend..."
echo "Navigate to frontend directory..."
cd frontend

echo "Linking to Railway (creates new service)..."
railway link

echo "Setting environment variable..."
railway variables set "NEXT_PUBLIC_API_URL=$BACKEND_URL"

echo "Deploying frontend..."
railway up

echo ""
echo "✅ Frontend deployment initiated!"
echo "Get your frontend URL with: railway domain"
echo ""

# Go back to root
cd ..

# Deploy n8n
echo "📦 Step 2: Deploying n8n..."
echo "Navigate to n8n directory..."
cd n8n

echo "Linking to Railway (creates new service)..."
railway link

echo "Setting n8n environment variables..."
read -p "Enter a secure password for n8n admin (or press Enter for default: admin123): " N8N_PASSWORD
if [ -z "$N8N_PASSWORD" ]; then
    N8N_PASSWORD="admin123"
fi

railway variables set "N8N_BASIC_AUTH_ACTIVE=true"
railway variables set "N8N_BASIC_AUTH_USER=admin"
railway variables set "N8N_BASIC_AUTH_PASSWORD=$N8N_PASSWORD"
railway variables set "N8N_HOST=0.0.0.0"
railway variables set "N8N_PORT=5678"

echo "Deploying n8n..."
railway up

echo ""
echo "✅ n8n deployment initiated!"
echo "Get your n8n URL with: railway domain"
echo ""
echo "⚠️  IMPORTANT: After n8n deploys, update WEBHOOK_URL:"
echo "   railway variables set WEBHOOK_URL=https://your-n8n-url.railway.app"
echo ""

# Go back to root
cd ..

echo "🎉 Deployment process started!"
echo ""
echo "Next steps:"
echo "1. Check Railway dashboard for deployment status"
echo "2. Get URLs: railway domain (in each service directory)"
echo "3. Update n8n WEBHOOK_URL after deployment"
echo ""

