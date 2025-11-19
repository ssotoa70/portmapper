# PortMapper Version History

## Version 6.0 (Current) - November 2025

### 🎉 Major Release: Platform-Specific Distributions

This release introduces production-ready, platform-specific executables for macOS, Windows, and Linux, eliminating the need for Python installation on end-user systems.

#### What's New

**Platform-Specific Bundles**
- ✅ macOS: Self-contained `.app` bundle (Universal/Intel compatible)
- ✅ Windows: Standalone `.exe` executable (single file)
- ✅ Linux: AppImage and Snap packages (portable across distributions)

**No Python Required**
- Users no longer need Python installed
- All dependencies bundled into the executable
- Download, extract, and run immediately

**Improved Distribution**
- Smaller download sizes (optimized PyInstaller bundles)
- Code signing for macOS security (future)
- Windows installer (.msi) ready for enterprise deployment

**Development Improvements**
- Build scripts for each platform (scripts/build_*.sh)
- Master build automation (scripts/build_all.sh)
- GitHub Releases with automated publishing

#### Technical Details

**Build Process**
- PyInstaller 6.16.0 for cross-platform bundling
- Optimized data file inclusion (fonts, images)
- Platform-specific optimizations:
  - macOS: .app bundle with codesigning support
  - Windows: Single .exe with UPX compression
  - Linux: AppImage for universal distribution

**Installation Methods**
| Platform | Method | Size | Notes |
|----------|--------|------|-------|
| macOS | Download .app | ~200MB | Universal (Intel/ARM) |
| Windows | Download .exe | ~180MB | Windows 7+ supported |
| Linux | Download AppImage | ~150MB | Works on most distros |
| Any | Python package | ~500KB | `python3 portmapper.py` |

#### Breaking Changes

None! Version 6.0 is fully backward compatible with version 5.x.

#### Migration Path

**From v5.5 to v6.0:**
- Keep v5.5 projects in place
- Download appropriate v6.0 bundle for your OS
- Extract and run
- Projects continue to work seamlessly

#### Known Limitations

- macOS: Currently unsigned (add to Security exceptions if needed)
- Windows: UAC may prompt on first run
- Linux: Requires FUSE for AppImage (glibc 2.17+)

#### Future Roadmap

- Code signing for macOS (Apple Developer Program)
- Microsoft Store distribution (Windows)
- Snap Store (Linux)
- Auto-update functionality
- Configuration file support

---

## Version 5.5 - October 2025

### Location-Independent Edition

#### Features

- Works from any directory
- No hardcoded paths
- Self-contained resources
- Smart launcher script (`./run.sh`)
- Comprehensive documentation

#### Improvements

- Fixed all path handling issues
- Relative path resolution
- Better file dialog handling
- Professional documentation

---

## Version 5.0 and Earlier

- Original PortMapper releases
- Hardcoded paths requiring specific directory structure
- Dependent on system Python installation

---

## Version Comparison

| Feature | v5.5 | v6.0 |
|---------|------|------|
| Python Required | Yes (3.9+) | No |
| Size | 20MB | 150-200MB (executable) |
| Installation | Pip + script | Download & run |
| Distribution | Portable folder | Platform-specific binary |
| Setup Time | 5 minutes | < 1 minute |
| Users | Tech-savvy | Anyone |

---

## Download & Install

### macOS
```bash
# Download PortMapper-6.0.app.zip from Releases
unzip PortMapper-6.0.app.zip
open PortMapper.app
```

### Windows
```cmd
# Download PortMapper-6.0.exe from Releases
PortMapper-6.0.exe
```

### Linux
```bash
# Download PortMapper-6.0-x86_64.AppImage from Releases
chmod +x PortMapper-6.0-x86_64.AppImage
./PortMapper-6.0-x86_64.AppImage
```

### Any System (Python)
```bash
# Clone or extract source
cd portmapper
python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages
./run.sh
```

---

## Support & Issues

For issues, feature requests, or contributions:
- [GitHub Issues](https://github.com/ssotoa70/portmapper/issues)
- [GitHub Discussions](https://github.com/ssotoa70/portmapper/discussions)

---

**Last Updated:** November 19, 2025
**Maintainer:** Sergio Soto (@ssotoa70)
