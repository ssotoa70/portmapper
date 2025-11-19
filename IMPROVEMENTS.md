# PortMapper 5.5 - Location-Independent Edition
## Improvements & Technical Details

### Overview
This is an improved version of PortMapper 5.5 that can be run from **any location** without requiring installation or configuration adjustments. All resources (fonts, images) are bundled with the application.

---

## Problems Fixed

### 1. **Hardcoded Paths**
**Original Issue:**
- Application only worked when run from the same directory containing the script
- Paths like `'DesignOutput'` and `'Projects'` were relative to the current working directory
- Moving the folder broke all file references

**Solution:**
```python
# Before
base = os.path.abspath('.')
self.out_dir = os.path.abspath('DesignOutput')

# After
base = os.path.dirname(os.path.abspath(__file__))
self.out_dir = os.path.join(script_dir, 'DesignOutput')
```

### 2. **Resource Loading**
**Original Issue:**
- Font file (ArialBold.ttf) couldn't be found if script wasn't in same directory
- Image files (base_*.png) lookup failed from different locations

**Solution:**
- Updated `resource_path()` function to use script directory instead of current working directory
- Now works with both direct script execution and PyInstaller bundles

### 3. **Project Directory Structure**
**Original Issue:**
- Projects always created relative to current working directory
- Using `'Projects'` in `os.path.join()` created relative paths

**Solution:**
```python
# Before
base_path = os.path.join('Projects', customer, site, cluster)

# After
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(script_dir, 'Projects', customer, site, cluster)
```

### 4. **File Dialogs**
**Original Issue:**
- Default directory in file dialogs was hardcoded to `'DesignOutput'`
- Failed to navigate if run from different location

**Solution:**
```python
# Before
d = QFileDialog.getExistingDirectory(self, 'Select Base Output Directory', 'DesignOutput')

# After
script_dir = os.path.dirname(os.path.abspath(__file__))
default_dir = os.path.join(script_dir, 'DesignOutput')
d = QFileDialog.getExistingDirectory(self, 'Select Base Output Directory', default_dir)
```

---

## Technical Changes

### Modified Function: `resource_path()`
**Location:** Line 644-656

```python
def resource_path(rel: str) -> str:
    """
    Get the absolute path to a resource file.
    Works whether script is run directly or packaged with PyInstaller.
    Paths are resolved relative to the script's directory location.
    """
    try:
        # If bundled with PyInstaller
        base = sys._MEIPASS
    except Exception:
        # If running as a script, use the directory containing this script
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)
```

### Modified Section: `__init__()` method
**Location:** Line 1977-1980

Changed DesignOutput path initialization from:
```python
self.out_dir = os.path.abspath('DesignOutput')
```

To:
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
self.out_dir = os.path.join(script_dir, 'DesignOutput')
```

### Modified Function: `_update_output_paths()`
**Location:** Line 2125-2131

Changed Projects path construction from:
```python
base_path = os.path.join('Projects', customer, site, cluster)
```

To:
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(script_dir, 'Projects', customer, site, cluster)
```

### Modified Function: `select_output_directory()`
**Location:** Line 10134-10139

Changed file dialog default directory from:
```python
d = QFileDialog.getExistingDirectory(self, 'Select Base Output Directory', 'DesignOutput')
```

To:
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
default_dir = os.path.join(script_dir, 'DesignOutput')
d = QFileDialog.getExistingDirectory(self, 'Select Base Output Directory', default_dir)
```

---

## New Files Added

### 1. **run.sh** - Smart Launcher Script
Provides:
- Automatic Python version checking (requires 3.9+)
- Dependency verification
- Interactive package installation if needed
- Cross-platform compatibility hints

Usage:
```bash
./run.sh
```

### 2. **README.md** - Comprehensive Documentation
Includes:
- Quick start guide
- Feature overview
- Directory structure explanation
- Troubleshooting section
- Migration instructions

### 3. **INSTALL_QUICK.txt** - Quick Reference
Simple 3-step installation guide:
1. Verify Python version
2. Install dependencies (one-time)
3. Run the application

### 4. **IMPROVEMENTS.md** - This File
Documents all technical improvements and changes.

---

## Compatibility

### ✅ Fully Compatible With
- Direct script execution: `python3 portmapper.py`
- Launcher script: `./run.sh`
- PyInstaller bundles (when built)
- All existing project files and configurations
- Cross-platform (macOS, Linux, Windows with WSL)

### ✅ Python Version Support
- Python 3.9+
- Tested with Python 3.13.7

### ✅ Dependency Versions
- PyQt6 - Any recent version
- Pillow (PIL) - Any recent version
- pandas - Any recent version
- requests - Any recent version

---

## Usage Examples

### Basic Usage
```bash
cd /Users/sergio.soto/portmapper
./run.sh
```

### From Different Locations
```bash
# From home directory
~/portmapper/run.sh

# From Applications
/Applications/portmapper/run.sh

# After adding to PATH
portmapper
```

### Move Anywhere
```bash
# Move to /Applications
cp -r /Users/sergio.soto/portmapper /Applications/

# Run from new location
/Applications/portmapper/run.sh  # ✓ Works!
```

### Direct Python Execution
```bash
python3 /Users/sergio.soto/portmapper/portmapper.py
python3 ~/portmapper/portmapper.py
python3 /opt/tools/portmapper/portmapper.py
```

---

## Testing Results

✅ **Import Test:** Application modules load correctly
✅ **Path Resolution:** Script directory correctly identified
✅ **Resource Loading:** Font and image files found via resource_path()
✅ **Project Directory:** Creates Projects folder relative to script location
✅ **File Dialogs:** Correct default directories set

---

## Advantages of This Release

| Feature | Before | After |
|---------|--------|-------|
| **Relocatable** | ✗ Must be in working directory | ✓ Works from any location |
| **Easy Setup** | ✗ Manual path configuration | ✓ Automatic path resolution |
| **Installation** | ✗ Complex instructions | ✓ One-liner pip install |
| **Resource Finding** | ✗ Failed if moved | ✓ Automatic resource discovery |
| **Project Storage** | ✗ Current working directory only | ✓ Always relative to app folder |
| **File Dialogs** | ✗ Failed navigation | ✓ Correct default directories |

---

## Future Enhancements (Optional)

These improvements could make it even better:

1. **PyInstaller Bundle**
   - Single executable file
   - No Python installation needed
   - Easier for end users

2. **Platform-Specific Launchers**
   - `.app` file for macOS
   - `.exe` installer for Windows
   - Snap/AppImage for Linux

3. **Config File**
   - User preferences persistence
   - Custom default locations
   - Theme settings

4. **Auto-Update**
   - Check for newer versions
   - One-click updates
   - Changelog display

---

## Support

For issues or questions:
1. Check README.md for troubleshooting
2. Verify Python version: `python3 --version`
3. Check dependencies: `python3 -m pip list | grep -E 'PyQt6|Pillow|pandas|requests'`
4. Review INSTALL_QUICK.txt for setup

---

## Version Information

- **Version:** 5.5 (Location-Independent Edition)
- **Release Date:** November 2025
- **Previous Version:** 5.5
- **Changes:** Path handling improvements for portability
- **Compatibility:** Fully backward compatible

---

## Summary

This release transforms PortMapper from a location-dependent application into a truly portable one. Users can now:

1. **Install once** - Run the pip install command once
2. **Move anywhere** - Copy the folder to any location
3. **Run instantly** - No additional configuration needed
4. **Use flexibly** - From command line or scripts

The improvements are transparent to users while providing significant benefits for deployment, backup, and sharing.
