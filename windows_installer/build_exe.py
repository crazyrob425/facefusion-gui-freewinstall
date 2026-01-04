"""
Build script for creating Windows executable
Uses PyInstaller to create standalone launcher executable
"""

import PyInstaller.__main__
import sys
from pathlib import Path

def build_launcher():
    """Build the launcher executable"""
    
    script_dir = Path(__file__).parent
    launcher_script = script_dir / "launcher.py"
    icon_file = script_dir.parent / "facefusion.ico"
    
    # PyInstaller arguments
    args = [
        str(launcher_script),
        '--name=FaceFusionLauncher',
        '--onefile',
        '--windowed',  # No console window
        '--icon=' + str(icon_file) if icon_file.exists() else '',
        '--add-data=../facefusion.ico;.',
        '--hidden-import=pystray',
        '--hidden-import=PIL',
        '--hidden-import=PIL._imagingtk',
        '--hidden-import=PIL._tkinter_finder',
        '--collect-all=pystray',
        '--collect-all=PIL',
        '--noconsole',
        '--clean',
    ]
    
    # Remove empty strings
    args = [arg for arg in args if arg]
    
    print("Building FaceFusion Launcher executable...")
    print(f"Script: {launcher_script}")
    print(f"Icon: {icon_file}")
    print()
    
    PyInstaller.__main__.run(args)
    
    print()
    print("Build complete!")
    print("Executable location: dist/FaceFusionLauncher.exe")

def build_installer_wizard():
    """Build the installer wizard executable"""
    
    script_dir = Path(__file__).parent
    wizard_script = script_dir / "install_wizard.py"
    icon_file = script_dir.parent / "facefusion.ico"
    
    # PyInstaller arguments
    args = [
        str(wizard_script),
        '--name=FaceFusionInstaller',
        '--onefile',
        '--windowed',
        '--icon=' + str(icon_file) if icon_file.exists() else '',
        '--add-data=../facefusion.ico;.',
        '--noconsole',
        '--clean',
    ]
    
    # Remove empty strings
    args = [arg for arg in args if arg]
    
    print("Building FaceFusion Installer executable...")
    print(f"Script: {wizard_script}")
    print(f"Icon: {icon_file}")
    print()
    
    PyInstaller.__main__.run(args)
    
    print()
    print("Build complete!")
    print("Executable location: dist/FaceFusionInstaller.exe")

def build_all():
    """Build all executables"""
    print("=" * 60)
    print("Building FaceFusion Windows Executables")
    print("=" * 60)
    print()
    
    try:
        build_launcher()
        print()
        print("-" * 60)
        print()
        build_installer_wizard()
        
        print()
        print("=" * 60)
        print("All builds completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Test the executables in the 'dist' folder")
        print("2. Use Inno Setup to create the installer package")
        print("3. Copy executables to installer directory")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller
    
    build_all()
