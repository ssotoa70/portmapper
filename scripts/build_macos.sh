#!/bin/bash
# Build PortMapper 6.0 for macOS
# Creates a self-contained .app bundle

set -e

echo "════════════════════════════════════════════════════════════════"
echo "   Building PortMapper 6.0 for macOS"
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
rm -rf "$PROJECT_DIR/build" "$PROJECT_DIR/dist" "$PROJECT_DIR/PortMapper.spec" 2>/dev/null || true
mkdir -p "$PROJECT_DIR/build" "$PROJECT_DIR/dist"
echo "  ✓ Clean complete"
echo ""

# Build the application
echo "🔨 Building macOS .app bundle..."
cd "$PROJECT_DIR"

pyinstaller \
  --name "PortMapper" \
  --onedir \
  --windowed \
  --osx-bundle-identifier "com.portmapper.app" \
  --add-data "ArialBold.ttf:." \
  --add-data "vast-man.jpeg:." \
  --add-data "base_cisco_9332d.png:." \
  --add-data "base_cisco_9364d.png:." \
  --add-data "base_sn3700.png:." \
  --add-data "base_sn4600hr.png:." \
  --add-data "base_sn4600hr.pxd:." \
  --add-data "base-arista7050DX4.png:." \
  --add-data "base-arista7060DX5.png:." \
  --add-data "base-arista7060X664pef.png:." \
  --add-data "base-SN5400.png:." \
  --add-data "base-SN5600.png:." \
  --collect-all PyQt6 \
  --collect-all PIL \
  --distpath "dist/macos" \
  portmapper.py 2>&1 | grep -E "^[0-9]+ INFO:|^[0-9]+ WARNING:|Build completed|error" | tail -20

echo ""
echo "✓ Build complete!"
echo ""

# Create DMG (disk image) for distribution
if command -v create-dmg &> /dev/null; then
  echo "📀 Creating DMG installer..."
  create-dmg \
    --volname "PortMapper 6.0" \
    --window-pos 200 120 \
    --window-size 800 400 \
    --icon-size 100 \
    --text-size 16 \
    --icon "PortMapper.app" 200 190 \
    --hide-extension "PortMapper.app" \
    --app-drop-link 600 190 \
    "dist/macos/PortMapper-6.0.dmg" \
    "dist/macos/PortMapper.app" 2>/dev/null || echo "  ℹ DMG creation requires create-dmg tool"
else
  echo "ℹ DMG creation skipped (requires create-dmg tool)"
  echo "  Install with: brew install create-dmg"
fi
echo ""

# Verify the build
echo "✅ VERIFICATION:"
if [ -d "dist/macos/PortMapper.app" ]; then
  echo "  ✓ PortMapper.app created successfully"
  echo "  📊 Size: $(du -sh dist/macos/PortMapper.app | cut -f1)"
  echo ""
  echo "🚀 Ready to use! Run:"
  echo "  open dist/macos/PortMapper.app"
  echo ""
else
  echo "  ✗ Build failed - PortMapper.app not found"
  exit 1
fi

echo "════════════════════════════════════════════════════════════════"
echo "   macOS Build Complete!"
echo "════════════════════════════════════════════════════════════════"
