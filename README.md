# PortMapper 5.5 - Location-Independent Release

**PortMapper** is a network topology visualization and port mapping tool for storage systems.

## What's New in This Release

✅ **Location-Independent** - Run the application from any directory
✅ **No Installation Required** - Just install Python dependencies once
✅ **Self-Contained** - All resources (fonts, images) are included
✅ **Relative Paths** - Works correctly regardless of where the folder is placed

## Quick Start

### Option 1: Using the Launcher Script (Recommended)

```bash
./run.sh
```

The launcher script will:
- Verify Python 3.9+ is installed
- Check for required packages
- Prompt to install missing packages (if needed)
- Launch the application

### Option 2: Direct Python Execution

```bash
python3 portmapper.py
```

## Requirements

- **Python 3.9** or later
- **PyQt6** - GUI framework
- **Pillow (PIL)** - Image processing
- **pandas** - Data handling
- **requests** - HTTP library

## Installation of Dependencies

If you haven't installed the required packages yet, run:

```bash
python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages
```

Or let the `run.sh` script do it for you automatically.

## Directory Structure

```
portmapper/
├── portmapper.py          # Main application (renamed from portmapper5.5.py)
├── run.sh                 # Launcher script (recommended method)
├── README.md              # This file
├── ArialBold.ttf          # Font file (required)
├── vast-man.jpeg          # Image resource
├── base_*.png             # Network device base images
├── base_*.pxd             # Design files
├── Projects/              # User projects directory (auto-created)
│   └── {CustomerName}/
│       └── {SiteName}/
│           └── {ClusterName}/
│               ├── DesignOutput/    # Generated diagrams
│               └── SwitchOutput/    # Switch configurations
└── DesignOutput/          # Legacy output directory (for compatibility)
```

## Key Features

### Device Support
- Cisco switches (9332D, 9364D)
- Sonic switches (SN3700, SN4600HR, SN5400, SN5600)
- Arista switches (7050DX4, 7060DX5, 7060X664pef)
- VAST DBox models (Mavericks, Ceres, RAIDER)

### Functionality
- Interactive network topology visualization
- Port mapping and configuration
- Design documentation generation
- Switch configuration export
- Multi-rack cluster planning
- Cell planning (default & advanced modes)

## Usage

1. **Run the Application:**
   ```bash
   ./run.sh
   ```

2. **Create a Project:**
   - Enter Customer Name, Site Name, and Cluster Name
   - Configure your network topology
   - Add nodes and uplink configurations

3. **Generate Designs:**
   - Click "Export/Generate Design" to create diagrams
   - Output is saved to `Projects/{Customer}/{Site}/{Cluster}/DesignOutput/`

4. **Export Configurations:**
   - Generate switch configurations from your design
   - Configurations are saved to `Projects/{Customer}/{Site}/{Cluster}/SwitchOutput/`

## Moving the Application

You can move the entire `portmapper` directory to any location and it will work correctly:

```bash
# Move to Applications folder
mv portmapper /Applications/

# Or anywhere else
mv portmapper ~/MyTools/

# Run from any location
cd ~/MyTools/portmapper
./run.sh
```

The application will automatically create necessary subdirectories relative to its installation location.

## Improvements Made

### Path Handling
- **Before:** Used hardcoded paths (`'DesignOutput'`, `'Projects'`) that only worked in the current directory
- **After:** Uses absolute paths relative to the script's location, working from anywhere

### Key Changes in Code
1. Updated `resource_path()` to use script directory instead of current working directory
2. Changed `DesignOutput` path initialization to be relative to script location
3. Updated `Projects` path construction to use absolute paths
4. Fixed file dialogs to use correct default directories

### Compatibility
- Fully compatible with PyInstaller bundled versions
- Works with both direct script execution and packaged executables
- All existing projects and saved configurations remain compatible

## Troubleshooting

### "ModuleNotFoundError" for PyQt6, Pillow, pandas, or requests

**Solution:** Run the installer script:
```bash
python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages
```

Or use the launcher:
```bash
./run.sh
```

### Application won't start

1. Verify Python version: `python3 --version` (should be 3.9+)
2. Check all dependencies are installed: `python3 -m pip list`
3. Ensure file permissions: `chmod +x run.sh`

### Projects not saving in expected location

- Check that the folder has write permissions
- Verify the `Projects` subdirectory exists (created automatically on first use)
- Ensure you're not running from a read-only filesystem

## Advanced Usage

### Command Line Arguments

The application may support additional arguments (see application documentation):

```bash
python3 portmapper.py [arguments]
./run.sh [arguments]
```

### System Integration

To add a desktop shortcut or system menu item, see your OS documentation for creating launcher files.

## Support & Documentation

For more information on device configurations and advanced features, refer to the embedded help in the application.

## Version Info

- **Current Release:** 5.5 (Location-Independent Edition)
- **Python Minimum:** 3.9
- **Last Updated:** November 2025

---

**Note:** This is an improved distribution of PortMapper with enhanced portability. The application logic and functionality remain identical to the original.
