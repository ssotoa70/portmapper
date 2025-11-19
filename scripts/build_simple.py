#!/usr/bin/env python3
"""
Simple build script for PortMapper 6.0
Avoids PyQt6 symlink issues during bundling
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command and return success status"""
    if description:
        print(f"→ {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"  Exception: {e}")
        return False

def build_macos():
    """Build macOS .app bundle"""
    print("\n════════════════════════════════════════════════════════════════")
    print("   Building PortMapper 6.0 for macOS")
    print("════════════════════════════════════════════════════════════════\n")

    project_dir = Path(__file__).parent.parent.absolute()
    os.chdir(project_dir)

    print(f"📁 Project: {project_dir}")
    print(f"🐍 Python: {sys.version}")

    # Clean
    print("\n🧹 Cleaning previous builds...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    os.makedirs("dist/macos", exist_ok=True)

    # Build without spec file to avoid symlink issues
    print("\n🔨 Building with PyInstaller...")

    # Simpler PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "PortMapper",
        "--onedir",
        "--windowed",
        "--osx-bundle-identifier", "com.portmapper.app",
    ]

    # Add data files
    data_files = [
        "ArialBold.ttf",
        "vast-man.jpeg",
        "base_cisco_9332d.png",
        "base_cisco_9364d.png",
        "base_sn3700.png",
        "base_sn4600hr.png",
        "base_sn4600hr.pxd",
        "base-arista7050DX4.png",
        "base-arista7060DX5.png",
        "base-arista7060X664pef.png",
        "base-SN5400.png",
        "base-SN5600.png",
    ]

    for data_file in data_files:
        cmd.extend(["--add-data", f"{data_file}:."])

    cmd.extend(["--distpath", "dist/macos", "portmapper.py"])

    # Run build
    result = subprocess.run(cmd)

    if result.returncode == 0 and Path("dist/macos/PortMapper.app").exists():
        print("\n✅ macOS build successful!")
        print(f"📦 Location: dist/macos/PortMapper.app")
        size = subprocess.check_output(["du", "-sh", "dist/macos/PortMapper.app"]).decode().split()[0]
        print(f"📊 Size: {size}")
        return True
    else:
        print("\n❌ macOS build failed!")
        return False

def build_windows():
    """Build Windows .exe"""
    print("\n════════════════════════════════════════════════════════════════")
    print("   Building PortMapper 6.0 for Windows (requires Windows)")
    print("════════════════════════════════════════════════════════════════\n")

    print("ℹ️  Note: Windows .exe should be built on Windows with this command:")
    print("   python3 -m PyInstaller --name PortMapper --onefile --windowed --distpath dist/windows portmapper.py")
    print("")
    return False

def build_linux():
    """Build Linux AppImage"""
    print("\n════════════════════════════════════════════════════════════════")
    print("   Building PortMapper 6.0 for Linux (requires Linux)")
    print("════════════════════════════════════════════════════════════════\n")

    print("ℹ️  Note: Linux AppImage should be built on Linux with:")
    print("   python3 -m PyInstaller --name portmapper --onedir --distpath dist/linux portmapper.py")
    print("")
    return False

def main():
    """Main build function"""
    if len(sys.argv) < 2:
        print("Usage: python build_simple.py [macos|windows|linux|all]")
        sys.exit(1)

    platform = sys.argv[1].lower()

    if platform in ["macos", "all"]:
        build_macos()
    elif platform in ["windows"]:
        build_windows()
    elif platform in ["linux"]:
        build_linux()
    elif platform == "all":
        build_macos()
        build_windows()
        build_linux()
    else:
        print(f"Unknown platform: {platform}")
        sys.exit(1)

if __name__ == "__main__":
    main()
