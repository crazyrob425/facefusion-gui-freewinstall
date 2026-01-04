# FaceFusion Windows Quick Start Guide

Get FaceFusion up and running on Windows in minutes!

## Quick Install (Recommended)

### Option 1: Using the Installer (Easiest)

1. **Download the installer** (when available)
2. **Run** `FaceFusion-Setup.exe`
3. **Follow the wizard**:
   - Choose installation location
   - Select components (Git, Conda, FFmpeg)
   - Choose your GPU type
   - Select shortcut options
4. **Wait for installation** to complete
5. **Launch FaceFusion** from desktop shortcut or Start Menu

### Option 2: Manual Setup

1. **Install Dependencies**
   ```powershell
   # Run PowerShell as Administrator
   cd windows_installer
   .\dependency_installer.ps1 -InstallAll
   ```

2. **Setup Environment**
   ```batch
   setup_environment.bat
   ```

3. **Launch FaceFusion**
   ```batch
   launch_facefusion.bat
   ```

## First Time Setup

After installation, the GUI launcher will open:

1. **Select Hardware Accelerator**
   - Go to Settings tab
   - Choose your GPU type:
     - NVIDIA GPU → Select "NVIDIA CUDA"
     - AMD GPU → Select "AMD DirectML"
     - Intel GPU → Select "Intel OpenVINO"
     - No GPU → Select "Default (CPU)"
   - Click "Save Settings"

2. **Configure Options**
   - Auto-start server on launch (optional)
   - Minimize to tray (optional)
   - Auto-open browser (recommended)

3. **Start Server**
   - Go to Main tab
   - Click "Start Server"
   - Wait for server to start
   - Browser will open automatically

## Daily Usage

### Starting FaceFusion

**Method 1: Desktop Shortcut**
- Double-click the FaceFusion icon on your desktop

**Method 2: Start Menu**
- Press Windows key
- Type "FaceFusion"
- Click on FaceFusion

**Method 3: System Tray**
- If already running, look for icon in system tray
- Right-click → Show

### Using the GUI Launcher

**Main Controls:**
- **Start Server**: Launches the FaceFusion backend
- **Stop Server**: Stops the backend (saves resources)
- **Restart Server**: Restarts if experiencing issues
- **Open in Browser**: Opens FaceFusion web interface

**System Tray:**
- Click the tray icon to show/hide window
- Right-click for quick actions:
  - Start/Stop/Restart server
  - Open in browser
  - Quit application

**Console:**
- Switch to Console tab to see server logs
- Useful for troubleshooting
- Click "Clear Console" to clean up

## Common Tasks

### Changing GPU Type

1. Open FaceFusion Launcher
2. Go to Settings tab
3. Select different accelerator
4. Click "Save Settings"
5. Restart server for changes to take effect

### Running Without GUI

```batch
# Activate environment
conda activate facefusion

# Run headless
python facefusion.py headless-run [options]

# Or run with web UI
python facefusion.py run
```

### Updating FaceFusion

```batch
# Navigate to installation directory
cd C:\Program Files\FaceFusion

# Pull latest changes (if installed via Git)
git pull

# Update dependencies
conda activate facefusion
python install.py --onnxruntime [your-accelerator]
```

## Performance Tips

### For Best Performance:

1. **Use GPU Acceleration**
   - Select the correct GPU type in settings
   - Ensure GPU drivers are up to date

2. **Close Other Applications**
   - Free up RAM and GPU memory
   - Stop unnecessary background processes

3. **Adjust Thread Count**
   - More threads = faster processing
   - Too many threads = system slowdown
   - Recommended: Number of CPU cores - 2

### For Stability:

1. **Monitor Resources**
   - Check Task Manager for memory usage
   - Ensure adequate free disk space (temp files)

2. **Keep Updated**
   - Update Windows regularly
   - Update GPU drivers
   - Update FaceFusion when new versions available

## Troubleshooting

### Server Won't Start

**Check:**
1. Is conda environment activated? (Should be automatic)
2. Are all dependencies installed? (Run `setup_environment.bat`)
3. Is port 7860 available? (Change port in Settings if needed)
4. Check Console tab for error messages

**Fix:**
```batch
# Recreate environment
setup_environment.bat
```

### Poor Performance

**Check:**
1. Is correct GPU selected in Settings?
2. Are GPU drivers up to date?
3. Is GPU actually being used? (Check Task Manager → Performance)

**Fix:**
1. Update GPU drivers
2. Verify accelerator selection matches your hardware
3. Close other GPU-intensive applications

### Installation Failed

**Check:**
1. Do you have Administrator rights?
2. Is antivirus blocking installation?
3. Do you have enough disk space (5+ GB)?

**Fix:**
1. Run installer as Administrator (right-click → Run as administrator)
2. Temporarily disable antivirus
3. Free up disk space

### Can't Find Installation

**Default Locations:**
- `C:\Program Files\FaceFusion`
- Check Start Menu shortcuts for actual path

**Find Installation:**
```powershell
# Search for facefusion.py
Get-ChildItem -Path C:\ -Filter "facefusion.py" -Recurse -ErrorAction SilentlyContinue
```

## Getting Help

### Resources

- **Documentation**: https://docs.facefusion.io
- **GitHub Issues**: https://github.com/facefusion/facefusion/issues
- **Discord Community**: https://discord.gg/facefusion

### Before Asking for Help

1. Check Console tab for error messages
2. Verify all dependencies are installed
3. Ensure you're using the latest version
4. Try recreating the environment
5. Search existing issues on GitHub

### Providing Information

When reporting issues, include:
- Windows version
- GPU type and driver version
- Error messages from Console
- Steps to reproduce
- FaceFusion version

## Advanced Usage

### Command Line Options

```batch
# Activate environment first
conda activate facefusion

# Show all options
python facefusion.py --help

# Run headless with specific options
python facefusion.py headless-run ^
  --source source.jpg ^
  --target target.mp4 ^
  --output output.mp4

# Batch processing
python facefusion.py batch-run
```

### Custom Configuration

Edit `facefusion.ini` in installation directory to set defaults:
- Face detection settings
- Output quality
- Processor options
- And more...

### Environment Variables

Set in Windows Environment Variables:
- `CUDA_VISIBLE_DEVICES`: Select specific GPU
- `OMP_NUM_THREADS`: Control thread count
- Custom model paths

## Uninstalling

### Complete Removal

1. **Start Menu Method**:
   - Start → FaceFusion → Uninstall FaceFusion
   - Follow uninstall wizard
   - Choose what to remove

2. **Windows Settings Method**:
   - Settings → Apps → Apps & features
   - Find "FaceFusion"
   - Click "Uninstall"

### Keeping Configuration

To preserve settings for reinstall:
- Uncheck "Remove configuration files" in uninstaller
- Your settings in `%USERPROFILE%\.facefusion` will be kept

## Next Steps

1. **Explore the Interface**: Try different processors and options
2. **Read Documentation**: Learn about advanced features
3. **Join Community**: Connect with other users
4. **Experiment**: Try different face swapping scenarios
5. **Share Feedback**: Help improve FaceFusion

---

**Enjoy using FaceFusion!** 🎭✨
