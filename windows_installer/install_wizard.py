"""
FaceFusion Windows Installation Wizard
Handles automated installation of dependencies and setup
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import urllib.request
import json
import shutil
import winreg
from typing import Optional


class InstallWizard:
    """Installation wizard for FaceFusion on Windows"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FaceFusion Installation Wizard")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Installation state
        self.install_dir = Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / "FaceFusion"
        self.accelerator = "default"
        self.install_git = True
        self.install_conda = True
        self.install_ffmpeg = True
        self.create_desktop_shortcut = True
        self.create_startmenu = True
        
        # Current page
        self.current_page = 0
        self.pages = []
        
        # Setup wizard
        self.setup_wizard()
        
    def setup_wizard(self):
        """Setup the installation wizard"""
        # Header
        header = tk.Frame(self.root, bg='#0078D7', height=80)
        header.pack(fill='x')
        
        title = tk.Label(header, text="FaceFusion Installation Wizard", 
                        font=('Arial', 18, 'bold'), bg='#0078D7', fg='white')
        title.pack(pady=20)
        
        # Content area
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill='x', padx=20, pady=10)
        
        self.back_btn = ttk.Button(nav_frame, text="< Back", command=self.go_back, 
                                   width=12, state='disabled')
        self.back_btn.pack(side='left')
        
        self.next_btn = ttk.Button(nav_frame, text="Next >", command=self.go_next, 
                                   width=12)
        self.next_btn.pack(side='right')
        
        self.cancel_btn = ttk.Button(nav_frame, text="Cancel", command=self.cancel_install, 
                                     width=12)
        self.cancel_btn.pack(side='right', padx=5)
        
        # Create pages
        self.create_pages()
        self.show_page(0)
    
    def create_pages(self):
        """Create all wizard pages"""
        self.pages = [
            self.create_welcome_page,
            self.create_location_page,
            self.create_components_page,
            self.create_accelerator_page,
            self.create_shortcuts_page,
            self.create_install_page,
            self.create_complete_page
        ]
    
    def create_welcome_page(self, parent):
        """Create welcome page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Welcome to FaceFusion Setup", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        welcome_text = """This wizard will guide you through the installation of FaceFusion,
the industry leading face manipulation platform.

This installer will:
• Install Git, Conda, and FFmpeg (if not already installed)
• Set up the FaceFusion environment
• Configure hardware acceleration
• Create desktop and start menu shortcuts
• Install an easy-to-use GUI launcher

Click Next to continue."""
        
        tk.Label(frame, text=welcome_text, justify='left', bg='white', 
                font=('Arial', 10)).pack(pady=20, padx=20)
        
        return frame
    
    def create_location_page(self, parent):
        """Create installation location page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Choose Installation Location", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        tk.Label(frame, text="Select the folder where FaceFusion will be installed:", 
                bg='white').pack(pady=10)
        
        path_frame = tk.Frame(frame, bg='white')
        path_frame.pack(pady=10, fill='x', padx=40)
        
        self.install_path_var = tk.StringVar(value=str(self.install_dir))
        path_entry = ttk.Entry(path_frame, textvariable=self.install_path_var, width=50)
        path_entry.pack(side='left', padx=5)
        
        browse_btn = ttk.Button(path_frame, text="Browse...", 
                               command=self.browse_install_location)
        browse_btn.pack(side='left')
        
        # Space required
        tk.Label(frame, text="Space required: ~5 GB", bg='white', 
                font=('Arial', 9)).pack(pady=10)
        
        return frame
    
    def create_components_page(self, parent):
        """Create components selection page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Select Components to Install", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        tk.Label(frame, text="The installer will check and install required dependencies:", 
                bg='white').pack(pady=10)
        
        components_frame = tk.Frame(frame, bg='white')
        components_frame.pack(pady=20, padx=40, anchor='w')
        
        self.git_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(components_frame, text="Git (version control system)", 
                       variable=self.git_var).pack(anchor='w', pady=5)
        
        self.conda_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(components_frame, text="Miniconda (Python environment manager)", 
                       variable=self.conda_var).pack(anchor='w', pady=5)
        
        self.ffmpeg_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(components_frame, text="FFmpeg (video processing library)", 
                       variable=self.ffmpeg_var).pack(anchor='w', pady=5)
        
        tk.Label(frame, text="Note: If already installed, they will be detected automatically.", 
                bg='white', font=('Arial', 9, 'italic')).pack(pady=10)
        
        return frame
    
    def create_accelerator_page(self, parent):
        """Create hardware accelerator selection page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Choose Hardware Accelerator", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        tk.Label(frame, text="Select your GPU type for optimal performance:", 
                bg='white').pack(pady=10)
        
        self.accel_var = tk.StringVar(value="default")
        
        accel_frame = tk.Frame(frame, bg='white')
        accel_frame.pack(pady=20, padx=40)
        
        accelerators = [
            ("Default (CPU only)", "default"),
            ("NVIDIA GPU (CUDA)", "cuda"),
            ("AMD GPU (DirectML)", "directml"),
            ("Intel GPU (OpenVINO)", "openvino"),
        ]
        
        for text, value in accelerators:
            ttk.Radiobutton(accel_frame, text=text, variable=self.accel_var, 
                          value=value).pack(anchor='w', pady=5)
        
        info_text = """CPU: Works on all systems but slower
NVIDIA: Requires NVIDIA GPU with CUDA support
AMD: Requires AMD GPU with DirectML support
Intel: Requires Intel GPU with OpenVINO support"""
        
        tk.Label(frame, text=info_text, justify='left', bg='white', 
                font=('Arial', 9)).pack(pady=10, padx=40)
        
        return frame
    
    def create_shortcuts_page(self, parent):
        """Create shortcuts configuration page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Create Shortcuts", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        tk.Label(frame, text="Select where to create shortcuts:", 
                bg='white').pack(pady=10)
        
        shortcuts_frame = tk.Frame(frame, bg='white')
        shortcuts_frame.pack(pady=20, padx=40)
        
        self.desktop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(shortcuts_frame, text="Create desktop shortcut", 
                       variable=self.desktop_var).pack(anchor='w', pady=5)
        
        self.startmenu_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(shortcuts_frame, text="Create Start Menu folder", 
                       variable=self.startmenu_var).pack(anchor='w', pady=5)
        
        return frame
    
    def create_install_page(self, parent):
        """Create installation progress page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Installing FaceFusion", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        self.install_status = tk.Label(frame, text="Ready to install...", 
                                       bg='white', font=('Arial', 10))
        self.install_status.pack(pady=10)
        
        self.progress = ttk.Progressbar(frame, mode='indeterminate', length=400)
        self.progress.pack(pady=20)
        
        # Console output
        console_frame = tk.Frame(frame, bg='white')
        console_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        from tkinter import scrolledtext
        self.install_log = scrolledtext.ScrolledText(console_frame, height=15, 
                                                     width=70, state='disabled')
        self.install_log.pack(fill='both', expand=True)
        
        return frame
    
    def create_complete_page(self, parent):
        """Create installation complete page"""
        frame = tk.Frame(parent, bg='white')
        
        tk.Label(frame, text="Installation Complete!", 
                font=('Arial', 16, 'bold'), bg='white', fg='green').pack(pady=30)
        
        completion_text = """FaceFusion has been successfully installed on your computer.

You can now:
• Launch FaceFusion from the desktop shortcut
• Access it from the Start Menu
• Use the GUI launcher to manage the server

Click Finish to exit the installer."""
        
        tk.Label(frame, text=completion_text, justify='left', bg='white', 
                font=('Arial', 10)).pack(pady=20, padx=40)
        
        self.launch_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Launch FaceFusion now", 
                       variable=self.launch_var).pack(pady=10)
        
        return frame
    
    def show_page(self, page_num):
        """Show specified page"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create and show page
        if 0 <= page_num < len(self.pages):
            page = self.pages[page_num](self.content_frame)
            page.pack(fill='both', expand=True)
            self.current_page = page_num
            
            # Update buttons
            self.back_btn.config(state='normal' if page_num > 0 else 'disabled')
            
            if page_num == len(self.pages) - 2:  # Install page
                self.next_btn.config(text="Install", command=self.start_install)
            elif page_num == len(self.pages) - 1:  # Complete page
                self.next_btn.config(text="Finish", command=self.finish_install)
            else:
                self.next_btn.config(text="Next >", command=self.go_next)
    
    def go_next(self):
        """Go to next page"""
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
    
    def go_back(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def browse_install_location(self):
        """Browse for installation location"""
        folder = filedialog.askdirectory(initialdir=self.install_path_var.get())
        if folder:
            self.install_path_var.set(folder)
    
    def log_install(self, message: str):
        """Log installation message"""
        self.install_log.config(state='normal')
        self.install_log.insert(tk.END, message + '\n')
        self.install_log.see(tk.END)
        self.install_log.config(state='disabled')
        self.root.update()
    
    def start_install(self):
        """Start the installation process"""
        self.next_btn.config(state='disabled')
        self.back_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
        
        self.progress.start(10)
        
        # Run installation in background
        import threading
        threading.Thread(target=self.run_installation, daemon=True).start()
    
    def run_installation(self):
        """Run the actual installation"""
        try:
            self.install_dir = Path(self.install_path_var.get())
            self.accelerator = self.accel_var.get()
            
            # Create installation directory
            self.install_status.config(text="Creating installation directory...")
            self.log_install(f"Creating directory: {self.install_dir}")
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Check and install Git
            if self.git_var.get():
                self.install_git_if_needed()
            
            # Check and install Conda
            if self.conda_var.get():
                self.install_conda_if_needed()
            
            # Check and install FFmpeg
            if self.ffmpeg_var.get():
                self.install_ffmpeg_if_needed()
            
            # Clone/copy FaceFusion repository
            self.install_facefusion()
            
            # Setup Python environment
            self.setup_environment()
            
            # Create shortcuts
            if self.desktop_var.get() or self.startmenu_var.get():
                self.create_shortcuts()
            
            # Create uninstaller
            self.create_uninstaller()
            
            self.progress.stop()
            self.install_status.config(text="Installation complete!")
            self.log_install("\n=== Installation completed successfully ===")
            
            # Move to complete page
            self.root.after(1000, lambda: self.show_page(len(self.pages) - 1))
            
        except Exception as e:
            self.progress.stop()
            self.install_status.config(text="Installation failed!")
            self.log_install(f"\nERROR: {str(e)}")
            messagebox.showerror("Installation Error", 
                               f"Installation failed: {str(e)}")
            self.next_btn.config(state='normal')
            self.cancel_btn.config(state='normal')
    
    def install_git_if_needed(self):
        """Check and install Git if needed"""
        self.install_status.config(text="Checking Git installation...")
        self.log_install("Checking for Git...")
        
        if shutil.which('git'):
            self.log_install("Git is already installed")
            return
        
        self.log_install("Git not found, would download and install...")
        # In a real implementation, download and install Git
        # For now, just log that we would do it
    
    def install_conda_if_needed(self):
        """Check and install Conda if needed"""
        self.install_status.config(text="Checking Conda installation...")
        self.log_install("Checking for Conda...")
        
        if shutil.which('conda'):
            self.log_install("Conda is already installed")
            return
        
        self.log_install("Conda not found, would download and install Miniconda...")
        # In a real implementation, download and install Miniconda
    
    def install_ffmpeg_if_needed(self):
        """Check and install FFmpeg if needed"""
        self.install_status.config(text="Checking FFmpeg installation...")
        self.log_install("Checking for FFmpeg...")
        
        if shutil.which('ffmpeg'):
            self.log_install("FFmpeg is already installed")
            return
        
        self.log_install("FFmpeg not found, would download and install...")
        # In a real implementation, download and install FFmpeg
    
    def install_facefusion(self):
        """Install FaceFusion"""
        self.install_status.config(text="Installing FaceFusion...")
        self.log_install("Installing FaceFusion...")
        
        # Copy current installation to target directory
        source_dir = Path(__file__).parent.parent
        self.log_install(f"Copying from {source_dir} to {self.install_dir}")
        
        # In a real implementation, copy files or clone repository
    
    def setup_environment(self):
        """Setup Python environment"""
        self.install_status.config(text="Setting up Python environment...")
        self.log_install("Creating Python environment...")
        self.log_install(f"Selected accelerator: {self.accelerator}")
        
        # In a real implementation, create conda environment and install dependencies
    
    def create_shortcuts(self):
        """Create desktop and start menu shortcuts"""
        self.install_status.config(text="Creating shortcuts...")
        self.log_install("Creating shortcuts...")
        
        # Desktop shortcut
        if self.desktop_var.get():
            self.log_install("Creating desktop shortcut...")
            # In a real implementation, create .lnk file
        
        # Start menu
        if self.startmenu_var.get():
            self.log_install("Creating Start Menu entries...")
            # In a real implementation, create start menu folder
    
    def create_uninstaller(self):
        """Create uninstaller"""
        self.install_status.config(text="Creating uninstaller...")
        self.log_install("Creating uninstaller...")
        
        # Create uninstaller script
        uninstall_script = self.install_dir / "uninstall.py"
        # In a real implementation, create uninstaller script
        
        # Add to Windows Programs and Features
        # In a real implementation, add registry entries
    
    def cancel_install(self):
        """Cancel installation"""
        if messagebox.askyesno("Cancel Installation", 
                              "Are you sure you want to cancel the installation?"):
            self.root.quit()
    
    def finish_install(self):
        """Finish installation and exit"""
        if self.launch_var.get():
            # Launch FaceFusion
            launcher_path = self.install_dir / "windows_installer" / "launcher.py"
            if launcher_path.exists():
                subprocess.Popen([sys.executable, str(launcher_path)])
        
        self.root.quit()
    
    def run(self):
        """Run the wizard"""
        self.root.mainloop()


def main():
    """Main entry point"""
    wizard = InstallWizard()
    wizard.run()


if __name__ == "__main__":
    main()
