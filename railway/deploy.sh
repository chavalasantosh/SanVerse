#!/bin/bash
# Railway Deployment Script
# This script copies Railway configuration files to the project root for deployment

echo "🚂 Preparing Railway deployment files..."

# Get the project root (parent of railway folder)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAILWAY_FOLDER="$(cd "$(dirname "$0")" && pwd)"

# Files to copy
FILES=("railway.json" "Procfile" "runtime.txt")

for file in "${FILES[@]}"; do
    SOURCE="$RAILWAY_FOLDER/$file"
    DESTINATION="$PROJECT_ROOT/$file"
    
    if [ -f "$SOURCE" ]; then
        cp "$SOURCE" "$DESTINATION"
        echo "✅ Copied $file to project root"
    else
        echo "⚠️  Warning: $file not found in railway folder"
    fi
done

echo ""
echo "✨ Railway files are now in the project root!"
echo ""
echo "Next steps:"
echo "  1. railway login"
echo "  2. railway link -p 2a7fd91e-4260-44b2-b41e-a39d951fe026"
echo "  3. railway up"

