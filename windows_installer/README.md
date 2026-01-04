# FaceFusion Windows Professional Installer

This directory contains the Windows professional GUI installer and setup wizard for FaceFusion.

## Features

### Installation Wizard
- **Automated Dependency Installation**: Automatically installs Git, Conda, and FFmpeg if not already present
- **Hardware Accelerator Selection**: Choose between CPU, NVIDIA CUDA, AMD DirectML, or Intel OpenVINO
- **Custom Installation Path**: Select where to install FaceFusion
- **Shortcuts Creation**: Automatically creates desktop and Start Menu shortcuts
- **Uninstaller**: Easy removal via Windows Programs and Features or Start Menu

### GUI Launcher
- **System Tray Integration**: Minimize to tray with full control from taskbar icon
- **Server Management**: Start, Stop, and Restart the FaceFusion server with one click
- **Hidden Backend**: Server runs in background without terminal windows
- **Auto-start Options**: Configure to start server automatically on launch
- **Console Output**: View server logs and status in real-time
- **Browser Integration**: Automatically opens FaceFusion in your default browser

## Installation

### Using Inno Setup (Recommended)

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `facefusion_installer.iss` in Inno Setup
3. Click "Compile" to build the installer
4. The installer will be created in the `output` folder
5. Run `FaceFusion-Setup-3.0.0.exe` to install

### Manual Installation

1. Run the dependency installer:
   ```powershell
   .\dependency_installer.ps1 -InstallAll
   ```

2. Run the installation wizard:
   ```bash
   python install_wizard.py
   ```

3. Follow the on-screen instructions

## Usage

### Launching FaceFusion

After installation, you can launch FaceFusion in several ways:

1. **Desktop Shortcut**: Double-click the FaceFusion icon on your desktop
2. **Start Menu**: Start → FaceFusion → FaceFusion
3. **Batch File**: Run `launch_facefusion.bat` from the installation directory
4. **Direct**: Run `python windows_installer\launcher.py`

### GUI Launcher Features

#### Main Tab
- View server status (Running/Stopped)
- Start/Stop/Restart server with one click
- Open FaceFusion in browser

#### Settings Tab
- **Hardware Accelerator**: Choose CPU, NVIDIA CUDA, AMD DirectML, or Intel OpenVINO
- **Auto-start**: Start server automatically when launcher opens
- **Minimize to Tray**: Hide window on launch
- **Browser**: Automatically open browser when server starts
- **Port**: Configure server port (default: 7860)

#### Console Tab
- View real-time server output
- Monitor for errors and warnings
- Clear console output

### System Tray Menu

Right-click the tray icon to access:
- Show/Hide main window
- Start/Stop/Restart server
- Open in browser
- Quit application

## Uninstallation

### Via Start Menu
1. Start → FaceFusion → Uninstall FaceFusion
2. Follow the uninstall wizard
3. Choose what to remove:
   - Python environment
   - Configuration files
   - Shortcuts

### Via Windows Settings
1. Settings → Apps → Apps & features
2. Find "FaceFusion"
3. Click "Uninstall"

## File Structure

```
windows_installer/
├── launcher.py                    # GUI launcher application
├── install_wizard.py              # Installation wizard
├── uninstall.py                   # Uninstaller
├── facefusion_installer.iss       # Inno Setup script
├── launch_facefusion.bat          # Batch launcher script
├── setup_environment.bat          # Environment setup script
├── dependency_installer.ps1       # PowerShell dependency installer
└── README.md                      # This file
```

## Requirements

### System Requirements
- Windows 10 or later (64-bit)
- 8 GB RAM minimum (16 GB recommended)
- 5 GB free disk space
- Internet connection for dependency downloads

### Optional Hardware
- NVIDIA GPU (for CUDA acceleration)
- AMD GPU (for DirectML acceleration)
- Intel GPU (for OpenVINO acceleration)

## Accelerator Support

### NVIDIA CUDA
- Requires NVIDIA GPU with CUDA support
- Automatically installs CUDA-enabled ONNX Runtime
- Provides best performance for NVIDIA GPUs

### AMD DirectML
- Works with most modern AMD GPUs
- Uses DirectML for hardware acceleration
- Good performance on AMD hardware

### Intel OpenVINO
- Optimized for Intel GPUs and CPUs
- Uses OpenVINO toolkit
- Provides acceleration on Intel hardware

### Default (CPU)
- Works on all systems
- No GPU required
- Slower than GPU acceleration

## Troubleshooting

### Installation Issues

**Conda not found after installation**
- Restart your terminal or computer
- Run `conda init powershell` manually
- Check that Conda is in your PATH

**Git not found**
- Restart your terminal
- Manually install Git from https://git-scm.com/
- Ensure Git is added to PATH during installation

**FFmpeg not found**
- Restart your terminal
- Check PATH environment variable includes FFmpeg directory
- Manually download from https://ffmpeg.org/

### Runtime Issues

**Server won't start**
- Check that the conda environment is activated
- Run `setup_environment.bat` to recreate environment
- Check console tab for error messages

**Port already in use**
- Change the port in Settings tab
- Close other applications using port 7860
- Check for other FaceFusion instances

**GPU not detected**
- Verify GPU drivers are up to date
- Ensure correct accelerator is selected in Settings
- Reinstall with correct accelerator option

## Development

### Building the Installer

1. Ensure all files are in place
2. Update version numbers in `facefusion_installer.iss`
3. Compile with Inno Setup:
   ```
   iscc facefusion_installer.iss
   ```

### Testing

Test the installer on a clean Windows system to ensure:
- All dependencies install correctly
- Shortcuts are created properly
- Application launches successfully
- Uninstaller works completely

## Support

For issues and support:
- GitHub Issues: https://github.com/facefusion/facefusion/issues
- Documentation: https://docs.facefusion.io
- Community: https://discord.gg/facefusion

## License

This installer is part of the FaceFusion project and follows the same license.
See LICENSE.md in the root directory for details.
