"""
FaceFusion Windows Installer Package

This package contains the Windows professional installer components:
- GUI Launcher with system tray integration
- Installation Wizard
- Uninstaller
- Dependency installers
- Helper scripts
"""

__version__ = "1.0.0"
__author__ = "FaceFusion Team"

from pathlib import Path

INSTALLER_DIR = Path(__file__).parent
ROOT_DIR = INSTALLER_DIR.parent
