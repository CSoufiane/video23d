#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}--- Starting MVP 3D Reconstruction Setup ---${NC}"

# 1. Check Python Version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Checking Python version: $PYTHON_VERSION"
# Simple check for 3.11+ (could be improved for strictness)
if [[ "$PYTHON_VERSION" < "3.11" ]]; then
    echo -e "${RED}Error: Python 3.11 or higher is required.${NC}"
fi

# 2. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# 3. Install Python Dependencies
echo "Installing Python packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for System Tools (COLMAP & FFmpeg)
check_tool() {
    if command -v $1 >/dev/null 2>&1; then
        echo -e "${GREEN}[OK]${NC} $1 is installed."
    else
        echo -e "${RED}[MISSING]${NC} $1 is not found. Please install it (e.g., 'brew install $1' or 'sudo apt install $1')."
    fi
}

check_tool "colmap"
check_tool "ffmpeg"

echo -e "${GREEN}--- Setup Complete ---${NC}"
echo "To activate the environment, run: source venv/bin/activate"

mkdir -p frames scripts output