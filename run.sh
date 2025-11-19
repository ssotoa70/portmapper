#!/bin/bash

# PortMapper Application Launcher
# This script ensures the application can run from any location
# and sets up the proper Python environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory (so relative paths work correctly)
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9 or later"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "✓ Python version check passed: $PYTHON_VERSION"
else
    echo "Error: Python $REQUIRED_VERSION or later is required (found $PYTHON_VERSION)"
    exit 1
fi

# Check for required Python packages
check_package() {
    python3 -c "import $1" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "✗ Missing package: $1"
        return 1
    else
        echo "✓ Found package: $1"
        return 0
    fi
}

echo ""
echo "Checking required packages..."
MISSING=0

check_package "PyQt6" || MISSING=1
check_package "PIL" || MISSING=1
check_package "pandas" || MISSING=1
check_package "requests" || MISSING=1

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "⚠️  Missing required packages. Install them with:"
    echo "python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages"
    echo ""
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages
    else
        echo "Cannot continue without required packages."
        exit 1
    fi
fi

echo ""
echo "Launching PortMapper..."
echo "========================"
echo ""

# Run the main application
python3 "$SCRIPT_DIR/portmapper.py" "$@"
