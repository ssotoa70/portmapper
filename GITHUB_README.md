# PortMapper 6.0

[![Build Status](https://img.shields.io/github/actions/workflow/status/ssotoa70/portmapper/build-releases.yml?style=flat-square)](https://github.com/ssotoa70/portmapper/actions)
[![Latest Release](https://img.shields.io/github/v/release/ssotoa70/portmapper?style=flat-square)](https://github.com/ssotoa70/portmapper/releases)
[![License](https://img.shields.io/github/license/ssotoa70/portmapper?style=flat-square)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue?style=flat-square)](https://www.python.org/downloads/)

Professional network topology visualization and port mapping tool for storage systems. **Version 6.0 features platform-specific executables for macOS, Windows, and Linux—no Python installation required!**

## Features

- **Multi-Platform Support**: Standalone executables for macOS, Windows, and Linux
- **Device Support**: Cisco, Sonic, Arista, and VAST DBox devices
- **Network Visualization**: Interactive topology diagrams
- **Design Generation**: Automatic design documentation export
- **Configuration Export**: Switch configuration file generation
- **Multi-Rack Planning**: Complex cluster topology support
- **Advanced Planning**: Default and advanced cell planning modes

## Quick Start

### Download & Run (No Installation!)

**macOS**
```bash
# Download from Releases
unzip PortMapper-6.0.app.zip
open PortMapper.app
```

**Windows**
```cmd
# Download PortMapper-6.0.exe from Releases
PortMapper-6.0.exe
```

**Linux**
```bash
# Download PortMapper-6.0-x86_64.AppImage from Releases
chmod +x PortMapper-6.0-x86_64.AppImage
./PortMapper-6.0-x86_64.AppImage
```

### Or Run from Source (Requires Python 3.9+)

```bash
# Clone repository
git clone https://github.com/ssotoa70/portmapper.git
cd portmapper

# Install dependencies
python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages

# Run
./run.sh
# or
python3 portmapper.py
```

## Releases

### Version 6.0 (Current)
**Released: November 2025**

Platform-specific distributions with bundled dependencies:
- macOS .app bundle (Universal Intel/ARM)
- Windows standalone .exe
- Linux AppImage
- Fully backward compatible with v5.5

→ [Download v6.0 →](https://github.com/ssotoa70/portmapper/releases/latest)

### Version 5.5
**Released: October 2025**

Location-independent portable edition with smart launcher.

→ [View v5.5 Release →](https://github.com/ssotoa70/portmapper/releases/tag/v5.5)

[View Full Version History →](VERSION.md)

## System Requirements

### For Executable (v6.0)
- **macOS**: 10.13+ (Intel or Apple Silicon)
- **Windows**: Windows 7+ (64-bit)
- **Linux**: glibc 2.17+ (Ubuntu 16.04+, CentOS 7+, etc.)

### For Python Source
- Python 3.9 or later
- PyQt6 6.0+
- Pillow 8.0+
- pandas 1.0+
- requests 2.20+

## Documentation

- **[User Guide](README.md)** - Installation, features, and usage
- **[What's New in v6.0](VERSION.md)** - Release notes and migration guide
- **[Improvements Overview](IMPROVEMENTS.md)** - Technical details about platform support
- **[Contributing Guide](.github/CONTRIBUTING.md)** - How to contribute

## Screenshots

Coming soon! (Application features PyQt6-based GUI)

## Architecture

```
PortMapper 6.0
├── Python Application (portmapper.py)
│   ├── GUI (PyQt6)
│   ├── Network topology visualization
│   ├── Design generation engine
│   └── Configuration export
├── Platform Builds
│   ├── macOS .app (229 MB)
│   ├── Windows .exe (180 MB)
│   └── Linux AppImage (150 MB)
└── Build System
    ├── PyInstaller bundling
    ├── GitHub Actions CI/CD
    └── Automated releases
```

## Supported Devices

### Switch Vendors
- **Cisco**: 9332D, 9364D
- **Sonic**: SN3700, SN4600HR, SN5400, SN5600
- **Arista**: 7050DX4, 7060DX5, 7060X664pef

### Storage Systems
- **VAST**: DBox Mavericks, Ceres, RAIDER

## Building from Source

### Development Setup
```bash
# Clone and navigate
git clone https://github.com/ssotoa70/portmapper.git
cd portmapper

# Install dev dependencies
python3 -m pip install PyQt6 Pillow pandas requests PyInstaller --break-system-packages

# Run in development
python3 portmapper.py
```

### Building Executables

```bash
# macOS
bash scripts/build_macos.sh
# Output: dist/PortMapper.app

# Windows (on Windows)
bash scripts/build_windows.sh
# Output: dist/windows/PortMapper.exe

# Linux
bash scripts/build_linux.sh
# Output: dist/linux/portmapper

# All platforms (requires cross-compilation setup)
bash scripts/build_all.sh all
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](.github/CONTRIBUTING.md) for:
- How to report bugs
- How to suggest features
- How to submit code changes
- Development workflow

## Development Roadmap

### Completed (v6.0)
- [x] Platform-specific executables (macOS, Windows, Linux)
- [x] PyInstaller bundling
- [x] GitHub Actions CI/CD
- [x] Automated releases

### Planned (v6.1+)
- [ ] Code signing for macOS
- [ ] Microsoft Store distribution
- [ ] Snap Store integration
- [ ] Auto-update mechanism
- [ ] Configuration file support
- [ ] Plugin architecture
- [ ] Web interface (alternative to desktop)

## FAQ

**Q: Do I need Python?**
A: Only for running from source. The v6.0 executables include everything needed.

**Q: Is it free?**
A: Yes! PortMapper is open source under the [MIT License](LICENSE).

**Q: Can I use it on my Mac with Apple Silicon?**
A: Yes! The macOS bundle includes universal support (Intel + ARM).

**Q: What if the executable is blocked by security warnings?**
A: On macOS, right-click and select "Open" to bypass warnings. Windows Defender may prompt on first run.

**Q: Can I use v5.5 and v6.0 simultaneously?**
A: Yes! They don't conflict. All projects are compatible.

**Q: How do I move projects between versions?**
A: Just copy the `Projects/` folder. No migration needed—they're 100% compatible.

## Performance

- Application startup: < 2 seconds
- Design generation: < 30 seconds (typical)
- Switch configuration export: < 10 seconds
- Supports unlimited rack configurations

## Security

- No remote telemetry
- All processing local to your machine
- No account or registration required
- Open source for transparency
- Network access only for downloading updates (optional)

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## Support & Community

- **Issues & Bugs**: [GitHub Issues](https://github.com/ssotoa70/portmapper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ssotoa70/portmapper/discussions)
- **Maintainer**: [@ssotoa70](https://github.com/ssotoa70)

## Changelog

See [VERSION.md](VERSION.md) for complete version history and changes.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for cross-platform UI
- Packaged with [PyInstaller](https://pyinstaller.org/) for standalone executables
- Image processing with [Pillow](https://python-pillow.org/)
- Data handling with [pandas](https://pandas.pydata.org/)

---

**[Download Now →](https://github.com/ssotoa70/portmapper/releases/latest)** | [Documentation →](README.md) | [Contributing →](.github/CONTRIBUTING.md)

Made with ❤️ for network engineers and system architects.
