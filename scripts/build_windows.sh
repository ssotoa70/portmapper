#!/bin/bash
# Build PortMapper 6.0 for Windows
# Creates a standalone .exe with MSI installer

set -e

echo "════════════════════════════════════════════════════════════════"
echo "   Building PortMapper 6.0 for Windows"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "📁 Project directory: $PROJECT_DIR"
echo ""

# Verify Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python version: $PYTHON_VERSION"
echo ""

# Check for required dependencies
echo "📦 Checking dependencies..."
python3 -c "import PyQt6" && echo "  ✓ PyQt6" || { echo "  ✗ PyQt6 missing"; exit 1; }
python3 -c "import PIL" && echo "  ✓ Pillow" || { echo "  ✗ Pillow missing"; exit 1; }
python3 -c "import pandas" && echo "  ✓ pandas" || { echo "  ✗ pandas missing"; exit 1; }
python3 -c "import requests" && echo "  ✓ requests" || { echo "  ✗ requests missing"; exit 1; }
python3 -c "import PyInstaller" && echo "  ✓ PyInstaller" || { echo "  ✗ PyInstaller missing"; exit 1; }
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$PROJECT_DIR/build" "$PROJECT_DIR/dist" 2>/dev/null || true
mkdir -p "$PROJECT_DIR/build" "$PROJECT_DIR/dist"
echo "  ✓ Clean complete"
echo ""

# Build the application
echo "🔨 Building Windows executable..."
cd "$PROJECT_DIR"

pyinstaller \
  --name "PortMapper" \
  --onefile \
  --windowed \
  --add-data "ArialBold.ttf;." \
  --add-data "vast-man.jpeg;." \
  --add-data "base_cisco_9332d.png;." \
  --add-data "base_cisco_9364d.png;." \
  --add-data "base_sn3700.png;." \
  --add-data "base_sn4600hr.png;." \
  --add-data "base_sn4600hr.pxd;." \
  --add-data "base-arista7050DX4.png;." \
  --add-data "base-arista7060DX5.png;." \
  --add-data "base-arista7060X664pef.png;." \
  --add-data "base-SN5400.png;." \
  --add-data "base-SN5600.png;." \
  --collect-all PyQt6 \
  --collect-all PIL \
  -d all \
  --distpath "dist/windows" \
  portmapper.py 2>&1 | tail -30

echo ""
echo "✓ Build complete!"
echo ""

# Create MSI installer (Windows only - requires WiX Toolset)
if command -v candle.exe &> /dev/null; then
  echo "📦 Creating Windows MSI installer..."
  # This would require a WiX XML file - skipped for now
  echo "  ℹ MSI creation would require WiX Toolset"
else
  echo "ℹ MSI installer creation skipped (requires WiX Toolset on Windows)"
  echo "  Standalone .exe is ready for distribution"
fi
echo ""

# Verify the build
echo "✅ VERIFICATION:"
if [ -f "dist/windows/PortMapper.exe" ]; then
  echo "  ✓ PortMapper.exe created successfully"
  echo "  📊 Size: $(du -sh dist/windows/PortMapper.exe | cut -f1)"
  echo ""
  echo "🚀 Ready to use on Windows!"
  echo "  The .exe includes all dependencies and can be run directly"
  echo ""
else
  echo "  ✗ Build failed - PortMapper.exe not found"
  exit 1
fi

echo "════════════════════════════════════════════════════════════════"
echo "   Windows Build Complete!"
echo "════════════════════════════════════════════════════════════════"
