# Contributing to PortMapper

Thank you for your interest in contributing to PortMapper! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors from all backgrounds.

## Ways to Contribute

### 1. Report Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your OS and PortMapper version
- Error logs or screenshots

### 2. Suggest Features

Feature suggestions are welcome! Please:
- Clearly describe the feature
- Explain the use case
- Provide examples if possible
- Check existing issues first

### 3. Submit Code Changes

#### Getting Started

```bash
# Clone the repository
git clone https://github.com/ssotoa70/portmapper.git
cd portmapper

# Install development dependencies
python3 -m pip install PyQt6 Pillow pandas requests PyInstaller --break-system-packages

# Run tests (if available)
python3 -m pytest tests/ || python3 -m unittest discover tests/
```

#### Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes:
   - Follow PEP 8 style guidelines
   - Add comments for complex logic
   - Update docstrings as needed

3. Test your changes:
   ```bash
   # Run the application
   python3 portmapper.py
   ./run.sh

   # Test on different platforms if possible
   ```

4. Commit with clear messages:
   ```bash
   git commit -m "feat: add new device model support"
   git commit -m "fix: correct port mapping calculation"
   git commit -m "docs: update installation guide"
   ```

5. Push and create a Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

#### Commit Message Format

Use conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `build:` Build system changes
- `chore:` Maintenance tasks

### 4. Improve Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify instructions
- Add examples
- Translate to other languages

## Building Releases

### macOS

```bash
bash scripts/build_macos.sh
# Creates: dist/PortMapper.app
```

### Windows

```bash
bash scripts/build_windows.sh
# Creates: dist/windows/PortMapper.exe
```

### Linux

```bash
bash scripts/build_linux.sh
# Creates: dist/linux/portmapper (+ AppImage if available)
```

### All Platforms

```bash
bash scripts/build_all.sh all
```

## Project Structure

```
portmapper/
├── portmapper.py           # Main application
├── run.sh                  # Launcher script
├── README.md               # User documentation
├── VERSION.md              # Version history
├── scripts/                # Build scripts
│   ├── build_macos.sh     # macOS build
│   ├── build_windows.sh   # Windows build
│   ├── build_linux.sh     # Linux build
│   └── build_all.sh       # Master build script
├── .github/
│   ├── workflows/         # GitHub Actions
│   └── CONTRIBUTING.md    # This file
├── dist/                  # Built distributions
├── build/                 # Build artifacts
└── Projects/              # User work directory
```

## Testing

Before submitting changes:

1. **Test the main application:**
   ```bash
   python3 portmapper.py
   ```

2. **Test with launcher:**
   ```bash
   ./run.sh
   ```

3. **Test built executables** (if modifying build scripts):
   ```bash
   # macOS
   open dist/PortMapper.app

   # Windows (on Windows)
   dist/windows/PortMapper.exe

   # Linux
   ./dist/linux/portmapper/portmapper
   ```

## Pull Request Process

1. Update documentation if needed
2. Add tests if applicable
3. Ensure existing tests pass
4. Create PR with clear description
5. Link related issues with `#issue_number`
6. Wait for review and feedback

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to public functions
- Include type hints where helpful

## Performance Considerations

- Avoid unnecessary file I/O
- Use efficient algorithms
- Cache computed values when appropriate
- Profile before optimizing

## Security

- Never commit secrets or credentials
- Report security issues privately to maintainers
- Validate user input
- Follow secure coding practices

## Release Process

1. Update VERSION.md
2. Update CHANGELOG (if maintained)
3. Create git tag: `git tag v6.0.1`
4. Push tag: `git push origin v6.0.1`
5. GitHub Actions builds releases
6. Create GitHub Release with notes
7. Announce on relevant channels

## Questions?

- Check existing issues and discussions
- Create a new discussion if needed
- Contact maintainer: @ssotoa70

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT or as specified in LICENSE).

---

**Thank you for contributing to PortMapper! 🙏**
