#!/bin/bash
# Prepare SOMA for distribution
# Cleans unnecessary files and creates a distribution-ready package

set -e

echo "=========================================="
echo "SOMA Distribution Preparation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${YELLOW}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Create backup
print_info "Creating backup..."
BACKUP_DIR="soma_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
print_success "Backup directory created: $BACKUP_DIR"

# List of files/directories to clean (but keep originals)
CLEANUP_ITEMS=(
    "__pycache__"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    ".pytest_cache"
    ".coverage"
    "htmlcov"
    "*.egg-info"
    ".mypy_cache"
    ".ruff_cache"
)

print_info "Cleaning temporary files..."
for item in "${CLEANUP_ITEMS[@]}"; do
    find . -name "$item" -type f -o -name "$item" -type d | while read -r path; do
        if [ -e "$path" ]; then
            rm -rf "$path" 2>/dev/null || true
        fi
    done
done
print_success "Temporary files cleaned"

# Check for sensitive files
print_info "Checking for sensitive files..."
SENSITIVE_FILES=(
    ".env"
    "*.key"
    "*.pem"
    "secrets.json"
    "config/secrets.yaml"
)

FOUND_SENSITIVE=false
for pattern in "${SENSITIVE_FILES[@]}"; do
    if find . -name "$pattern" -not -path "./$BACKUP_DIR/*" | grep -q .; then
        print_error "Found sensitive files matching: $pattern"
        FOUND_SENSITIVE=true
    fi
done

if [ "$FOUND_SENSITIVE" = true ]; then
    print_error "WARNING: Sensitive files detected! Please review before distribution."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "No sensitive files detected"
fi

# Verify essential files exist
print_info "Verifying essential files..."
ESSENTIAL_FILES=(
    "README.md"
    "INSTALLATION.md"
    "QUICK_START.md"
    "requirements.txt"
    "setup.sh"
    "setup.bat"
    "run.sh"
    "run.bat"
    "run.py"
    "start.py"
    "verify_installation.py"
    "Dockerfile"
    "docker-compose.yml"
    ".gitignore"
)

MISSING_FILES=()
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_error "Missing essential files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    exit 1
else
    print_success "All essential files present"
fi

# Check file sizes
print_info "Checking for large files..."
LARGE_FILES=$(find . -type f -size +100M -not -path "./$BACKUP_DIR/*" -not -path "./.git/*" 2>/dev/null | head -10)
if [ -n "$LARGE_FILES" ]; then
    print_error "Large files detected (>100MB):"
    echo "$LARGE_FILES"
    echo ""
    read -p "These files may cause issues. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "No unusually large files detected"
fi

# Create distribution checklist
print_info "Creating distribution checklist..."
cat > DISTRIBUTION_CHECKLIST.md << 'EOF'
# SOMA Distribution Checklist

## Pre-Distribution Checks

- [ ] All sensitive data removed (.env, API keys, passwords)
- [ ] All essential files present (README, setup scripts, etc.)
- [ ] Dependencies listed in requirements.txt
- [ ] Documentation is up to date
- [ ] Setup scripts tested on clean environment
- [ ] Docker configuration tested
- [ ] Verification script works correctly

## Files to Include

- [x] README.md
- [x] INSTALLATION.md
- [x] QUICK_START.md
- [x] requirements.txt
- [x] setup.sh / setup.bat
- [x] run.sh / run.bat / run.py
- [x] start.py
- [x] verify_installation.py
- [x] Dockerfile
- [x] docker-compose.yml
- [x] .gitignore
- [x] src/ directory
- [x] env.example

## Files to Exclude

- [x] __pycache__/
- [x] *.pyc, *.pyo
- [x] .env files
- [x] venv/ or .venv/
- [x] node_modules/
- [x] Large data files (*.npy, *.pkl, *.zip)
- [x] workflow_output/
- [x] .git/ directory (if creating ZIP)

## Testing

- [ ] Test setup on clean Linux system
- [ ] Test setup on clean Windows system
- [ ] Test setup on clean Mac system
- [ ] Test Docker setup
- [ ] Verify all imports work
- [ ] Test basic functionality

## Distribution Methods

1. **Git Repository** (Recommended)
   - Push to GitHub/GitLab
   - Team clones: `git clone <repo-url>`

2. **ZIP Archive**
   - Create ZIP excluding .git/
   - Share ZIP file
   - Team extracts and runs setup

3. **Docker Image**
   - Build: `docker build -t soma .`
   - Push to registry
   - Team pulls: `docker pull <image>`
EOF

print_success "Distribution checklist created: DISTRIBUTION_CHECKLIST.md"

# Summary
echo ""
echo "=========================================="
print_success "Distribution preparation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review DISTRIBUTION_CHECKLIST.md"
echo "  2. Test setup on a clean system"
echo "  3. Choose distribution method:"
echo "     - Git: git push to repository"
echo "     - ZIP: Create archive (exclude .git/)"
echo "     - Docker: Build and push image"
echo ""
echo "Backup saved in: $BACKUP_DIR"
echo ""

