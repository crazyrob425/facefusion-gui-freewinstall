# Windows Installation Guide

This guide covers the new Windows Professional GUI Installer for FaceFusion.

## Overview

The Windows Professional Installer provides an easy, automated way to install and run FaceFusion on Windows without manual command-line setup.

### Key Features

- 🎯 **One-Click Installation**: Automated setup wizard handles everything
- 🚀 **GUI Launcher**: Modern interface with system tray integration
- 🔧 **Auto-Dependency Installation**: Automatically installs Git, Conda, FFmpeg
- 🎮 **Hardware Acceleration**: Easy GPU selection (NVIDIA, AMD, Intel)
- 📦 **Desktop Shortcuts**: Instant access from desktop and Start Menu
- 🗑️ **Easy Uninstaller**: Complete removal with one click

## Installation Methods

### Method 1: Installation Wizard (Easiest)

1. **Navigate to the installer directory**:
   ```
   cd windows_installer
   ```

2. **Install required packages**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the installation wizard**:
   ```
   python install_wizard.py
   ```

4. **Follow the wizard steps**:
   - Choose installation location
   - Select components (Git, Conda, FFmpeg)
   - Choose hardware accelerator
   - Configure shortcuts
   - Wait for installation to complete

5. **Launch FaceFusion**:
   - Use desktop shortcut, or
   - Start Menu → FaceFusion

### Method 2: PowerShell Automated Setup

1. **Open PowerShell as Administrator**

2. **Navigate to the repository**:
   ```powershell
   cd path\to\facefusion-gui-freewinstall\windows_installer
   ```

3. **Install dependencies automatically**:
   ```powershell
   .\dependency_installer.ps1 -InstallAll
   ```

4. **Setup environment**:
   ```batch
   setup_environment.bat
   ```

5. **Launch**:
   ```batch
   launch_facefusion.bat
   ```

### Method 3: Build and Distribute Installer (Advanced)

For creating a distributable installer package:

1. **Install Inno Setup**: Download from https://jrsoftware.org/isinfo.php

2. **Install Python dependencies**:
   ```
   pip install -r windows_installer/requirements.txt
   pip install pyinstaller
   ```

3. **Build executables**:
   ```
   cd windows_installer
   python build_exe.py
   ```

4. **Compile Inno Setup installer**:
   - Open `facefusion_installer.iss` in Inno Setup
   - Click "Compile"
   - Installer will be created in `output/` folder

5. **Distribute**:
   - Share `FaceFusion-Setup-3.0.0.exe` with users
   - Users run installer and follow wizard

## Using the GUI Launcher

### Starting FaceFusion

After installation, launch FaceFusion using:

1. **Desktop Shortcut**: Double-click FaceFusion icon
2. **Start Menu**: Windows → FaceFusion → FaceFusion
3. **Batch File**: Run `launch_facefusion.bat`
4. **Direct Python**: `python windows_installer\launcher.py`

### Launcher Interface

The launcher has three tabs:

#### Main Tab
- **Server Status**: Shows if server is running or stopped
- **Start Server**: Launches the FaceFusion backend
- **Stop Server**: Stops the backend
- **Restart Server**: Restarts for troubleshooting
- **Open in Browser**: Opens web interface

#### Settings Tab
- **Hardware Accelerator**: Select CPU, CUDA, DirectML, or OpenVINO
- **Auto-start**: Start server automatically on launch
- **Minimize to Tray**: Hide window on launch
- **Open Browser**: Auto-open browser when server starts
- **Server Port**: Configure port (default 7860)
- **Save Settings**: Apply configuration

#### Console Tab
- **Real-time Logs**: View server output
- **Error Messages**: Monitor for issues
- **Clear Console**: Clean up output

### System Tray

When minimized, the launcher shows in the system tray:

**Right-click menu**:
- Show/Hide window
- Start/Stop/Restart server
- Open in browser
- Quit application

## Hardware Accelerators

### NVIDIA CUDA
**Best for**: NVIDIA GPUs (GeForce, RTX, Quadro)
- Requires: NVIDIA GPU with CUDA 11.0+
- Performance: Excellent
- Compatibility: Most NVIDIA GPUs

### AMD DirectML
**Best for**: AMD Radeon GPUs
- Requires: AMD GPU with DirectML support
- Performance: Good
- Compatibility: Most modern AMD GPUs

### Intel OpenVINO
**Best for**: Intel integrated graphics and CPUs
- Requires: Intel hardware
- Performance: Good for Intel CPUs/GPUs
- Compatibility: Intel processors

### Default (CPU)
**Best for**: Systems without GPU or for testing
- Requires: Nothing special
- Performance: Slower
- Compatibility: All systems

## Configuration Files

### Launcher Configuration
Location: `%USERPROFILE%\.facefusion\launcher_config.json`

Contains:
- Selected accelerator
- Auto-start preference
- Window behavior
- Server port
- Browser settings

### Installation Configuration
Location: `[Install Directory]\install_config.txt`

Contains:
- Selected accelerator during installation
- Used by `setup_environment.bat`

### FaceFusion Configuration
Location: `[Install Directory]\facefusion.ini`

Contains:
- Face detection settings
- Output quality settings
- Processor configurations
- UI preferences

## Troubleshooting

### Installation Issues

**Problem**: Conda not found after installation
```
Solution:
1. Restart terminal
2. Run: conda init powershell
3. Restart terminal again
```

**Problem**: Git not found
```
Solution:
1. Ensure Git was installed (check Add to PATH option)
2. Restart terminal
3. Verify: git --version
```

**Problem**: FFmpeg not found
```
Solution:
1. Check if FFmpeg is in PATH
2. Restart terminal
3. Manually add FFmpeg to PATH if needed
```

### Runtime Issues

**Problem**: Server won't start
```
Solutions:
1. Check Console tab for errors
2. Verify conda environment: conda activate facefusion
3. Recreate environment: setup_environment.bat
4. Check port availability (default 7860)
```

**Problem**: GPU not detected
```
Solutions:
1. Verify GPU drivers are installed and up to date
2. Check selected accelerator matches your GPU
3. Restart after driver installation
4. Try reinstalling with correct accelerator
```

**Problem**: Port already in use
```
Solutions:
1. Change port in Settings tab
2. Close other applications using port 7860
3. Check for other FaceFusion instances
```

### Performance Issues

**Problem**: Slow processing
```
Solutions:
1. Verify correct GPU accelerator is selected
2. Check GPU is actually being used (Task Manager)
3. Update GPU drivers
4. Close other GPU-intensive applications
5. Reduce thread count if system is overloaded
```

**Problem**: Out of memory errors
```
Solutions:
1. Close other applications
2. Reduce batch size
3. Use smaller resolution
4. Enable video_memory_strategy in settings
5. Add more RAM if possible
```

## Uninstalling

### Via Start Menu
1. Start → FaceFusion → Uninstall FaceFusion
2. Follow wizard prompts
3. Choose what to remove:
   - Python environment
   - Configuration files
   - Shortcuts

### Via Windows Settings
1. Settings → Apps → Apps & features
2. Find "FaceFusion"
3. Click Uninstall
4. Follow prompts

### Manual Uninstall
1. Run: `python windows_installer\uninstall.py`
2. Or delete installation directory manually
3. Remove conda environment: `conda env remove -n facefusion`
4. Delete config: `%USERPROFILE%\.facefusion`

## Advanced Usage

### Command Line

The GUI launcher is optional. You can still use command line:

```batch
REM Activate environment
conda activate facefusion

REM Run with web UI
python facefusion.py run

REM Run headless
python facefusion.py headless-run --source source.jpg --target target.mp4 --output output.mp4

REM Batch processing
python facefusion.py batch-run
```

### Environment Variables

Set in Windows Environment Variables or before launching:

```batch
REM Select specific GPU
set CUDA_VISIBLE_DEVICES=0

REM Control threads
set OMP_NUM_THREADS=8

REM Custom model path
set FACEFUSION_MODEL_PATH=C:\Models
```

### Custom Installation Path

To install to a custom location:

1. During installation wizard, click "Browse"
2. Select desired installation folder
3. Ensure folder has write permissions
4. Continue installation

### Multiple Installations

You can have multiple FaceFusion installations:

1. Install to different directories
2. Each has its own conda environment
3. Each can use different accelerators
4. Shortcuts will point to latest installation

## Building from Source

### Prerequisites

- Python 3.10 or 3.12
- pip
- Git (if building from repository)

### Build Steps

1. **Clone repository**:
   ```bash
   git clone https://github.com/crazyrob425/facefusion-gui-freewinstall.git
   cd facefusion-gui-freewinstall
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r windows_installer/requirements.txt
   ```

3. **Build executables** (optional):
   ```bash
   cd windows_installer
   python build_exe.py
   ```

4. **Compile installer** (optional):
   - Install Inno Setup
   - Open `facefusion_installer.iss`
   - Compile

## Support

### Getting Help

- **Documentation**: See `windows_installer/README.md` and `windows_installer/QUICK_START.md`
- **Issues**: https://github.com/facefusion/facefusion/issues
- **Discord**: https://discord.gg/facefusion

### Reporting Issues

When reporting problems, include:

1. Windows version
2. GPU type and driver version
3. Error messages from Console tab
4. Steps to reproduce
5. FaceFusion version

### Contributing

Contributions to the Windows installer are welcome:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly on Windows
5. Submit pull request

## Frequently Asked Questions

**Q: Do I need to install Git, Conda, and FFmpeg separately?**
A: No, the installer can do this automatically if you select those options.

**Q: Can I use this without GPU?**
A: Yes, select "Default (CPU)" accelerator. It will be slower but functional.

**Q: How do I update FaceFusion?**
A: Pull latest changes with Git, then run `setup_environment.bat` again.

**Q: Can I run multiple instances?**
A: Yes, but use different ports for each instance.

**Q: Where are my processed files saved?**
A: By default in the output folder specified in the web interface.

**Q: How do I change GPU type after installation?**
A: Open launcher → Settings → Select new accelerator → Save → Restart server.

**Q: Is internet required?**
A: Only during installation for downloading dependencies. After setup, can run offline.

**Q: Can I use custom models?**
A: Yes, see FaceFusion documentation for custom model setup.

## License

The Windows installer follows the same license as FaceFusion. See LICENSE.md.

---

**Need more help?** Check the [Quick Start Guide](windows_installer/QUICK_START.md) or the [detailed installer documentation](windows_installer/README.md).
