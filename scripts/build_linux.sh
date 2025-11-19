#!/bin/bash
# Build PortMapper 6.0 for Linux
# Creates AppImage and snap packages

set -e

echo "════════════════════════════════════════════════════════════════"
echo "   Building PortMapper 6.0 for Linux"
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
echo "🔨 Building Linux executable..."
cd "$PROJECT_DIR"

pyinstaller \
  --name "portmapper" \
  --onedir \
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
  -d all \
  --distpath "dist/linux" \
  portmapper.py 2>&1 | tail -30

echo ""
echo "✓ Build complete!"
echo ""

# Create AppImage (if appimagetool is available)
if command -v appimagetool &> /dev/null; then
  echo "📦 Creating AppImage..."

  # Create AppDir structure
  APPDIR="dist/linux/portmapper.AppDir"
  mkdir -p "$APPDIR/usr/bin"
  mkdir -p "$APPDIR/usr/share/applications"
  mkdir -p "$APPDIR/usr/share/pixmaps"

  # Copy the executable
  cp -r "dist/linux/portmapper/"* "$APPDIR/usr/bin/" 2>/dev/null || true

  # Create desktop entry
  cat > "$APPDIR/usr/share/applications/portmapper.desktop" << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=PortMapper
Exec=portmapper
Icon=portmapper
Categories=Utility;
Comment=Network port mapping tool for storage systems
DESKTOP

  # Build AppImage
  appimagetool "$APPDIR" "dist/linux/PortMapper-6.0-x86_64.AppImage" || echo "  ⚠ AppImage creation failed"
else
  echo "ℹ AppImage creation skipped (requires appimagetool)"
  echo "  Install with: apt-get install appimagetool"
fi
echo ""

# Create Snap (if snapcraft is available)
if command -v snapcraft &> /dev/null; then
  echo "📦 Creating Snap package..."

  # Create snap structure
  mkdir -p snap/gui

  cat > snap/snapcraft.yaml << 'SNAP'
name: portmapper
version: '6.0'
summary: Network port mapping tool for storage systems
description: |
  PortMapper is a professional network topology visualization and port
  mapping tool designed for storage systems. It supports multiple switch
  models and provides advanced network design capabilities.

grade: stable
confinement: strict

apps:
  portmapper:
    command: usr/bin/portmapper/portmapper
    plugs:
      - home
      - network
      - x11
      - opengl

parts:
  portmapper:
    plugin: dump
    source: dist/linux/
    organize:
      portmapper: usr/bin/portmapper
SNAP

  snapcraft 2>&1 | tail -20 || echo "  ⚠ Snap creation failed"
else
  echo "ℹ Snap creation skipped (requires snapcraft)"
  echo "  Install with: apt-get install snapcraft"
fi
echo ""

# Verify the build
echo "✅ VERIFICATION:"
if [ -d "dist/linux/portmapper" ]; then
  echo "  ✓ portmapper executable created successfully"
  echo "  📊 Size: $(du -sh dist/linux/portmapper | cut -f1)"
  echo ""
  echo "🚀 Ready to use on Linux!"
  echo "  Run: ./dist/linux/portmapper/portmapper"
  echo ""
else
  echo "  ✗ Build failed - portmapper not found"
  exit 1
fi

echo "════════════════════════════════════════════════════════════════"
echo "   Linux Build Complete!"
echo "════════════════════════════════════════════════════════════════"
