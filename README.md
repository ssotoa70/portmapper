# PortMapper 6.0

**Professional network topology visualization and port mapping tool for storage systems.**

Version 6.0 features platform-specific executables for macOS, Windows, and Linux—no Python installation required!

## Quick Links

- 📥 **[Download Latest Release](https://github.com/ssotoa70/portmapper/releases/latest)**
- 📖 **[Documentation](https://github.com/ssotoa70/portmapper#documentation)**
- 🐛 **[Report Issues](https://github.com/ssotoa70/portmapper/issues)**
- 💬 **[Discussions](https://github.com/ssotoa70/portmapper/discussions)**

## Features

✅ **Multi-Platform Executables** - macOS, Windows, Linux (no Python needed!)
✅ **Device Support** - Cisco, Sonic, Arista, VAST DBox devices
✅ **Network Visualization** - Interactive topology diagrams
✅ **Design Generation** - Automatic design documentation
✅ **Configuration Export** - Switch config file generation
✅ **Multi-Rack Planning** - Complex cluster support
✅ **Cross-Platform** - Works on macOS, Windows, Linux

## Installation

### macOS (No Python Required)
```bash
# Download PortMapper-6.0.0.app.zip from Releases
unzip PortMapper-6.0.0.app.zip
open PortMapper.app
```

### Windows (No Python Required)
```cmd
# Download PortMapper-6.0.0.exe from Releases
PortMapper-6.0.0.exe
```

### Linux (No Python Required)
```bash
# Download PortMapper-6.0.0-x86_64.AppImage from Releases
chmod +x PortMapper-6.0.0-x86_64.AppImage
./PortMapper-6.0.0-x86_64.AppImage
```

### From Source (Requires Python 3.9+)
```bash
git clone https://github.com/ssotoa70/portmapper.git
cd portmapper

python3 -m pip install PyQt6 Pillow pandas requests --break-system-packages
./run.sh
```

## Supported Devices

### Switch Vendors
- **Cisco**: 9332D, 9364D
- **Sonic**: SN3700, SN4600HR, SN5400, SN5600
- **Arista**: 7050DX4, 7060DX5, 7060X664pef

### Storage Systems
- **VAST**: DBox Mavericks, Ceres, RAIDER

## System Requirements

### Executables (v6.0)
- **macOS**: 10.13+ (Intel or Apple Silicon)
- **Windows**: Windows 7+ (64-bit)
- **Linux**: glibc 2.17+ (Ubuntu 16.04+, CentOS 7+, etc.)

### Python Source
- Python 3.9 or later
- PyQt6, Pillow, pandas, requests

## Documentation

- **[User Guide](START_HERE.txt)** - Getting started
- **[Version History](VERSION.md)** - Release notes and what's new
- **[What's New in v6.0](IMPROVEMENTS.md)** - Platform improvements
- **[Contributing Guide](.github/CONTRIBUTING.md)** - How to contribute

## Building from Source

### Development Setup
```bash
git clone https://github.com/ssotoa70/portmapper.git
cd portmapper

python3 -m pip install PyQt6 Pillow pandas requests PyInstaller --break-system-packages
python3 portmapper.py
```

### Building Executables

```bash
# macOS
bash scripts/build_macos.sh
# Output: dist/PortMapper.app

# Windows
bash scripts/build_windows.sh
# Output: dist/windows/PortMapper.exe

# Linux
bash scripts/build_linux.sh
# Output: dist/linux/portmapper
```

## Project Structure

```
portmapper/
├── portmapper.py           # Main application
├── run.sh                  # Launcher script
├── README.md               # This file
├── VERSION.md              # Version history
├── LICENSE                 # MIT License
├── scripts/
│   ├── build_macos.sh     # macOS build script
│   ├── build_windows.sh   # Windows build script
│   └── build_linux.sh     # Linux build script
├── .github/
│   ├── workflows/         # GitHub Actions CI/CD
│   └── CONTRIBUTING.md    # Contributing guidelines
├── dist/                  # Built distributions
├── build/                 # Build artifacts
└── Projects/              # User work directory

```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting code
- Development workflow

## FAQ

**Q: Do I need to install Python?**
A: Not for v6.0! Download the executable for your OS and run it directly.

**Q: Is it free?**
A: Yes! PortMapper is open source under the MIT License.

**Q: Works with M1/M2 Macs?**
A: Yes! The macOS build is universal (Intel + Apple Silicon).

**Q: Can I use v5.5 and v6.0 together?**
A: Yes! They don't conflict. Projects are 100% compatible.

**Q: How do I move projects between versions?**
A: Just copy the `Projects/` folder - no migration needed!

## Security

- No remote telemetry
- All processing local to your machine
- No account or registration required
- Open source for transparency

## Performance

- Application startup: < 2 seconds
- Design generation: < 30 seconds (typical)
- Supports unlimited rack configurations

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

## Support

- **Issues & Bugs**: [GitHub Issues](https://github.com/ssotoa70/portmapper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ssotoa70/portmapper/discussions)
- **Maintainer**: [@ssotoa70](https://github.com/ssotoa70)

## Changelog

See [VERSION.md](VERSION.md) for complete version history.

## Acknowledgments

Built with:
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Cross-platform UI
- [PyInstaller](https://pyinstaller.org/) - Standalone executables
- [Pillow](https://python-pillow.org/) - Image processing
- [pandas](https://pandas.pydata.org/) - Data handling

---

**[⬇️ Download Now](https://github.com/ssotoa70/portmapper/releases/latest)** | **[📖 Docs](START_HERE.txt)** | **[🤝 Contribute](.github/CONTRIBUTING.md)**

Made with ❤️ for network engineers and system architects.
