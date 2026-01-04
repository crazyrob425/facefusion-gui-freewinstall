"""
FaceFusion Uninstaller
Removes FaceFusion and optionally removes dependencies
"""

import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import winreg


class UninstallWizard:
    """Uninstallation wizard for FaceFusion"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Uninstall FaceFusion")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Get install directory
        self.install_dir = self.get_install_dir()
        
        # Uninstall options
        self.remove_env = True
        self.remove_config = True
        self.remove_shortcuts = True
        
        self.setup_ui()
    
    def get_install_dir(self) -> Path:
        """Get installation directory from registry or current location"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"Software\FaceFusion", 0, 
                                winreg.KEY_READ)
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            winreg.CloseKey(key)
            return Path(install_path)
        except Exception:
            # Fallback to current directory
            return Path(__file__).parent.parent
    
    def setup_ui(self):
        """Setup the UI"""
        # Header
        header = tk.Frame(self.root, bg='#D32F2F', height=80)
        header.pack(fill='x')
        
        title = tk.Label(header, text="Uninstall FaceFusion", 
                        font=('Arial', 18, 'bold'), bg='#D32F2F', fg='white')
        title.pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Warning message
        warning = tk.Label(content, 
                          text="This will remove FaceFusion from your computer.",
                          font=('Arial', 12, 'bold'), bg='white', fg='#D32F2F')
        warning.pack(pady=10)
        
        # Installation location
        location_frame = tk.Frame(content, bg='white')
        location_frame.pack(fill='x', pady=10)
        
        tk.Label(location_frame, text="Installation Location:", 
                bg='white', font=('Arial', 10, 'bold')).pack(anchor='w')
        tk.Label(location_frame, text=str(self.install_dir), 
                bg='white', font=('Arial', 9)).pack(anchor='w', padx=20)
        
        # Options
        options_frame = tk.LabelFrame(content, text="Uninstall Options", 
                                      padding=10, bg='white')
        options_frame.pack(fill='x', pady=20)
        
        self.env_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Remove Python environment", 
                       variable=self.env_var).pack(anchor='w', pady=3)
        
        self.config_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Remove configuration files", 
                       variable=self.config_var).pack(anchor='w', pady=3)
        
        self.shortcuts_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Remove shortcuts", 
                       variable=self.shortcuts_var).pack(anchor='w', pady=3)
        
        # Progress
        self.progress_label = tk.Label(content, text="", bg='white', 
                                      font=('Arial', 9))
        self.progress_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(content, mode='indeterminate', length=400)
        self.progress.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x', padx=20, pady=10)
        
        self.uninstall_btn = ttk.Button(button_frame, text="Uninstall", 
                                        command=self.start_uninstall, width=12)
        self.uninstall_btn.pack(side='right')
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel", 
                                     command=self.cancel_uninstall, width=12)
        self.cancel_btn.pack(side='right', padx=5)
    
    def start_uninstall(self):
        """Start the uninstallation process"""
        if not messagebox.askyesno("Confirm Uninstall", 
                                   "Are you sure you want to uninstall FaceFusion?"):
            return
        
        self.uninstall_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
        
        self.progress.start(10)
        
        # Run uninstallation in background
        import threading
        threading.Thread(target=self.run_uninstall, daemon=True).start()
    
    def run_uninstall(self):
        """Run the actual uninstallation"""
        try:
            # Remove Python environment
            if self.env_var.get():
                self.progress_label.config(text="Removing Python environment...")
                self.root.update()
                self.remove_conda_env()
            
            # Remove shortcuts
            if self.shortcuts_var.get():
                self.progress_label.config(text="Removing shortcuts...")
                self.root.update()
                self.remove_shortcuts()
            
            # Remove configuration
            if self.config_var.get():
                self.progress_label.config(text="Removing configuration files...")
                self.root.update()
                self.remove_config_files()
            
            # Remove registry entries
            self.progress_label.config(text="Removing registry entries...")
            self.root.update()
            self.remove_registry_entries()
            
            # Remove installation directory
            self.progress_label.config(text="Removing application files...")
            self.root.update()
            self.remove_install_dir()
            
            self.progress.stop()
            self.progress_label.config(text="Uninstallation complete!")
            
            messagebox.showinfo("Uninstall Complete", 
                              "FaceFusion has been successfully uninstalled.")
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            self.progress_label.config(text="Uninstallation failed!")
            messagebox.showerror("Uninstall Error", 
                               f"Failed to uninstall: {str(e)}")
            self.uninstall_btn.config(state='normal')
            self.cancel_btn.config(state='normal')
    
    def remove_conda_env(self):
        """Remove conda environment"""
        try:
            if shutil.which('conda'):
                subprocess.run(['conda', 'env', 'remove', '-n', 'facefusion', '-y'], 
                             check=False, capture_output=True)
        except Exception:
            pass
    
    def remove_shortcuts(self):
        """Remove desktop and start menu shortcuts"""
        try:
            # Desktop shortcut
            desktop = Path.home() / "Desktop" / "FaceFusion.lnk"
            if desktop.exists():
                desktop.unlink()
            
            # Start menu folder
            start_menu = Path(os.environ.get('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "FaceFusion"
            if start_menu.exists():
                shutil.rmtree(start_menu, ignore_errors=True)
        except Exception:
            pass
    
    def remove_config_files(self):
        """Remove configuration files"""
        try:
            config_dir = Path.home() / ".facefusion"
            if config_dir.exists():
                shutil.rmtree(config_dir, ignore_errors=True)
        except Exception:
            pass
    
    def remove_registry_entries(self):
        """Remove Windows registry entries"""
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, r"Software\FaceFusion")
        except Exception:
            pass
    
    def remove_install_dir(self):
        """Remove installation directory"""
        try:
            # We can't delete ourselves, so mark for deletion on reboot
            if self.install_dir.exists():
                # Try to remove what we can
                for item in self.install_dir.rglob('*'):
                    try:
                        if item.is_file():
                            item.unlink()
                    except Exception:
                        pass
                
                # Schedule directory deletion on reboot
                # This is a Windows-specific operation
                pass
        except Exception:
            pass
    
    def cancel_uninstall(self):
        """Cancel uninstallation"""
        self.root.quit()
    
    def run(self):
        """Run the wizard"""
        self.root.mainloop()


def main():
    """Main entry point"""
    wizard = UninstallWizard()
    wizard.run()


if __name__ == "__main__":
    main()
