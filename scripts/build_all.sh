#!/bin/bash
# Master build script for PortMapper 6.0
# Builds all platforms and creates release packages

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        PortMapper 6.0 - Multi-Platform Build System            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Parse arguments
BUILD_MACOS=false
BUILD_WINDOWS=false
BUILD_LINUX=false
BUILD_ALL=false

if [ $# -eq 0 ]; then
  echo "Usage: ./build_all.sh [platform|all]"
  echo ""
  echo "Platforms:"
  echo "  macos      - Build macOS .app bundle"
  echo "  windows    - Build Windows .exe executable"
  echo "  linux      - Build Linux AppImage/snap"
  echo "  all        - Build for all platforms (requires multiple OS)"
  echo ""
  echo "Examples:"
  echo "  ./build_all.sh macos"
  echo "  ./build_all.sh all"
  exit 1
fi

case "$1" in
  macos)
    BUILD_MACOS=true
    ;;
  windows)
    BUILD_WINDOWS=true
    ;;
  linux)
    BUILD_LINUX=true
    ;;
  all)
    BUILD_ALL=true
    BUILD_MACOS=true
    BUILD_WINDOWS=true
    BUILD_LINUX=true
    ;;
  *)
    echo "Unknown platform: $1"
    exit 1
    ;;
esac

echo "📋 Build Configuration:"
echo "  Platform: $([ "$BUILD_ALL" = true ] && echo 'All' || echo "${1^}")"
echo "  Project: $PROJECT_DIR"
echo ""

# Verify project structure
echo "✓ Verifying project structure..."
required_files=(
  "portmapper.py"
  "ArialBold.ttf"
  "vast-man.jpeg"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$PROJECT_DIR/$file" ]; then
    echo "✗ Missing required file: $file"
    exit 1
  fi
done
echo "  ✓ All required files present"
echo ""

# macOS build
if [ "$BUILD_MACOS" = true ]; then
  echo "▶ Starting macOS build..."
  bash "$SCRIPT_DIR/build_macos.sh"
  echo ""
fi

# Windows build
if [ "$BUILD_WINDOWS" = true ]; then
  echo "▶ Starting Windows build..."
  bash "$SCRIPT_DIR/build_windows.sh"
  echo ""
fi

# Linux build
if [ "$BUILD_LINUX" = true ]; then
  echo "▶ Starting Linux build..."
  bash "$SCRIPT_DIR/build_linux.sh"
  echo ""
fi

# Create release summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    BUILD SUMMARY                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [ "$BUILD_MACOS" = true ]; then
  if [ -d "$PROJECT_DIR/dist/macos/PortMapper.app" ]; then
    SIZE=$(du -sh "$PROJECT_DIR/dist/macos/PortMapper.app" | cut -f1)
    echo "✓ macOS     : dist/macos/PortMapper.app ($SIZE)"
  fi
fi

if [ "$BUILD_WINDOWS" = true ]; then
  if [ -f "$PROJECT_DIR/dist/windows/PortMapper.exe" ]; then
    SIZE=$(du -sh "$PROJECT_DIR/dist/windows/PortMapper.exe" | cut -f1)
    echo "✓ Windows   : dist/windows/PortMapper.exe ($SIZE)"
  fi
fi

if [ "$BUILD_LINUX" = true ]; then
  if [ -d "$PROJECT_DIR/dist/linux/portmapper" ]; then
    SIZE=$(du -sh "$PROJECT_DIR/dist/linux/portmapper" | cut -f1)
    echo "✓ Linux     : dist/linux/portmapper ($SIZE)"
  fi
fi

echo ""
echo "📦 All builds completed! Ready for release."
echo ""
echo "Next steps:"
echo "  1. Test each platform build on target OS"
echo "  2. Create GitHub releases with built artifacts"
echo "  3. Update documentation with download links"
echo ""
echo "════════════════════════════════════════════════════════════════"
