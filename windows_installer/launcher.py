"""
FaceFusion GUI Launcher
Professional Windows launcher with system tray integration
"""

import os
import sys
import subprocess
import json
import threading
import webbrowser
from pathlib import Path
from typing import Optional

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError as e:
    print("=" * 60)
    print("Missing Required Packages")
    print("=" * 60)
    print(f"Error: {e}")
    print()
    print("Installing required packages: pystray and Pillow...")
    print("This may take a moment...")
    print()
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "Pillow"])
        print()
        print("Installation successful! Please restart the launcher.")
        print()
        sys.exit(0)
    except subprocess.CalledProcessError as install_error:
        print()
        print("ERROR: Failed to install required packages.")
        print(f"Details: {install_error}")
        print()
        print("Please install manually:")
        print("  pip install pystray Pillow")
        print()
        sys.exit(1)


class FaceFusionLauncher:
    """Main launcher application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FaceFusion Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Application state
        self.server_process: Optional[subprocess.Popen] = None
        self.server_running = False
        self.config_file = Path.home() / ".facefusion" / "launcher_config.json"
        self.config = self.load_config()
        
        # System tray icon
        self.tray_icon = None
        
        # Setup UI
        self.setup_ui()
        self.load_saved_settings()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
    def load_config(self) -> dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "accelerator": "default",
            "auto_start": False,
            "minimize_on_launch": False,
            "server_port": 7860,
            "open_browser": True
        }
    
    def save_config(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        """Setup the main UI"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Main tab
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text='Main')
        self.setup_main_tab(main_frame)
        
        # Settings tab
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text='Settings')
        self.setup_settings_tab(settings_frame)
        
        # Console tab
        console_frame = ttk.Frame(notebook)
        notebook.add(console_frame, text='Console')
        self.setup_console_tab(console_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_main_tab(self, parent):
        """Setup main control tab"""
        # Title
        title = ttk.Label(parent, text="FaceFusion", font=('Arial', 24, 'bold'))
        title.pack(pady=20)
        
        subtitle = ttk.Label(parent, text="Industry leading face manipulation platform", 
                           font=('Arial', 10))
        subtitle.pack()
        
        # Status
        status_frame = ttk.LabelFrame(parent, text="Server Status", padding=10)
        status_frame.pack(fill='x', padx=20, pady=20)
        
        self.status_label = ttk.Label(status_frame, text="Stopped", 
                                     font=('Arial', 12, 'bold'))
        self.status_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="Start Server", 
                                    command=self.start_server, width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Server", 
                                   command=self.stop_server, width=15, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.restart_btn = ttk.Button(button_frame, text="Restart Server", 
                                     command=self.restart_server, width=15, state='disabled')
        self.restart_btn.grid(row=0, column=2, padx=5)
        
        # Open browser button
        self.browser_btn = ttk.Button(parent, text="Open in Browser", 
                                     command=self.open_browser, width=20)
        self.browser_btn.pack(pady=10)
    
    def setup_settings_tab(self, parent):
        """Setup settings tab"""
        # Accelerator selection
        accel_frame = ttk.LabelFrame(parent, text="Hardware Accelerator", padding=10)
        accel_frame.pack(fill='x', padx=20, pady=10)
        
        self.accelerator_var = tk.StringVar(value=self.config.get("accelerator", "default"))
        
        accelerators = [
            ("Default (CPU)", "default"),
            ("NVIDIA CUDA", "cuda"),
            ("AMD DirectML", "directml"),
            ("Intel OpenVINO", "openvino"),
        ]
        
        for text, value in accelerators:
            ttk.Radiobutton(accel_frame, text=text, variable=self.accelerator_var, 
                          value=value).pack(anchor='w')
        
        # Options
        options_frame = ttk.LabelFrame(parent, text="Options", padding=10)
        options_frame.pack(fill='x', padx=20, pady=10)
        
        self.auto_start_var = tk.BooleanVar(value=self.config.get("auto_start", False))
        ttk.Checkbutton(options_frame, text="Auto-start server on launch", 
                       variable=self.auto_start_var).pack(anchor='w')
        
        self.minimize_var = tk.BooleanVar(value=self.config.get("minimize_on_launch", False))
        ttk.Checkbutton(options_frame, text="Minimize to tray on launch", 
                       variable=self.minimize_var).pack(anchor='w')
        
        self.browser_var = tk.BooleanVar(value=self.config.get("open_browser", True))
        ttk.Checkbutton(options_frame, text="Open browser when server starts", 
                       variable=self.browser_var).pack(anchor='w')
        
        # Server port
        port_frame = ttk.Frame(options_frame)
        port_frame.pack(fill='x', pady=5)
        ttk.Label(port_frame, text="Server Port:").pack(side='left')
        self.port_var = tk.StringVar(value=str(self.config.get("server_port", 7860)))
        port_entry = ttk.Entry(port_frame, textvariable=self.port_var, width=10)
        port_entry.pack(side='left', padx=10)
        
        # Save button
        ttk.Button(parent, text="Save Settings", command=self.save_settings, 
                  width=20).pack(pady=20)
    
    def setup_console_tab(self, parent):
        """Setup console output tab"""
        # Console output
        console_frame = ttk.Frame(parent)
        console_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.console_text = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, 
                                                      height=20, state='disabled')
        self.console_text.pack(fill='both', expand=True)
        
        # Clear button
        ttk.Button(parent, text="Clear Console", 
                  command=lambda: self.console_text.delete(1.0, tk.END)).pack(pady=5)
    
    def log_console(self, message: str):
        """Log message to console"""
        self.console_text.config(state='normal')
        self.console_text.insert(tk.END, message + '\n')
        self.console_text.see(tk.END)
        self.console_text.config(state='disabled')
    
    def load_saved_settings(self):
        """Load saved settings into UI"""
        self.accelerator_var.set(self.config.get("accelerator", "default"))
        self.auto_start_var.set(self.config.get("auto_start", False))
        self.minimize_var.set(self.config.get("minimize_on_launch", False))
        self.browser_var.set(self.config.get("open_browser", True))
        self.port_var.set(str(self.config.get("server_port", 7860)))
    
    def save_settings(self):
        """Save current settings"""
        self.config["accelerator"] = self.accelerator_var.get()
        self.config["auto_start"] = self.auto_start_var.get()
        self.config["minimize_on_launch"] = self.minimize_var.get()
        self.config["open_browser"] = self.browser_var.get()
        try:
            self.config["server_port"] = int(self.port_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
            return
        
        self.save_config()
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.log_console("Settings saved")
    
    def start_server(self):
        """Start the FaceFusion server"""
        if self.server_running:
            return
        
        try:
            # Find Python executable and facefusion.py
            python_exe = sys.executable
            facefusion_dir = Path(__file__).parent.parent
            facefusion_script = facefusion_dir / "facefusion.py"
            
            if not facefusion_script.exists():
                messagebox.showerror("Error", f"FaceFusion script not found at {facefusion_script}")
                return
            
            # Prepare environment
            env = os.environ.copy()
            
            # Build command
            cmd = [python_exe, str(facefusion_script), "run"]
            
            self.log_console(f"Starting FaceFusion server...")
            self.log_console(f"Command: {' '.join(cmd)}")
            self.log_console(f"Accelerator: {self.config['accelerator']}")
            
            # Prepare process startup options
            popen_kwargs = {
                'stdout': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'env': env,
                'cwd': str(facefusion_dir)
            }
            
            # Hide window on Windows
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                popen_kwargs['startupinfo'] = startupinfo
            
            self.server_process = subprocess.Popen(cmd, **popen_kwargs)
            
            self.server_running = True
            self.update_ui_state()
            self.log_console("Server started successfully")
            self.status_var.set("Server running")
            
            # Start output reader thread
            threading.Thread(target=self.read_output, daemon=True).start()
            
            # Open browser if configured
            if self.config.get("open_browser", True):
                self.root.after(2000, self.open_browser)
            
        except Exception as e:
            self.log_console(f"Error starting server: {str(e)}")
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.server_running = False
            self.update_ui_state()
    
    def stop_server(self):
        """Stop the FaceFusion server"""
        if not self.server_running or not self.server_process:
            return
        
        try:
            self.log_console("Stopping server...")
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.log_console("Force killing server...")
            self.server_process.kill()
        except Exception as e:
            self.log_console(f"Error stopping server: {str(e)}")
        
        self.server_process = None
        self.server_running = False
        self.update_ui_state()
        self.log_console("Server stopped")
        self.status_var.set("Server stopped")
    
    def restart_server(self):
        """Restart the server"""
        self.log_console("Restarting server...")
        self.stop_server()
        self.root.after(1000, self.start_server)
    
    def read_output(self):
        """Read server output in background thread"""
        if not self.server_process:
            return
        
        for line in iter(self.server_process.stdout.readline, b''):
            if line:
                try:
                    text = line.decode('utf-8', errors='ignore').strip()
                    self.root.after(0, self.log_console, text)
                except Exception:
                    pass
    
    def open_browser(self):
        """Open the FaceFusion interface in browser"""
        port = self.config.get("server_port", 7860)
        url = f"http://localhost:{port}"
        self.log_console(f"Opening browser at {url}")
        webbrowser.open(url)
    
    def update_ui_state(self):
        """Update UI button states based on server status"""
        if self.server_running:
            self.status_label.config(text="Running", foreground="green")
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.restart_btn.config(state='normal')
        else:
            self.status_label.config(text="Stopped", foreground="red")
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.restart_btn.config(state='disabled')
    
    def create_tray_icon(self):
        """Create system tray icon"""
        # Create icon image
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.rectangle([16, 16, 48, 48], fill='white')
        
        # Create menu
        menu = (
            item('Show', self.show_window),
            item('Start Server', self.start_server, enabled=lambda item: not self.server_running),
            item('Stop Server', self.stop_server, enabled=lambda item: self.server_running),
            item('Restart Server', self.restart_server, enabled=lambda item: self.server_running),
            item('Open Browser', self.open_browser),
            item('Quit', self.quit_application)
        )
        
        self.tray_icon = pystray.Icon("FaceFusion", image, "FaceFusion Launcher", menu)
    
    def minimize_to_tray(self):
        """Minimize application to system tray"""
        self.root.withdraw()
        if not self.tray_icon:
            self.create_tray_icon()
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.deiconify()
    
    def quit_application(self, icon=None, item=None):
        """Quit the application"""
        if self.server_running:
            if messagebox.askyesno("Confirm Exit", 
                                  "Server is running. Stop and exit?"):
                self.stop_server()
            else:
                return
        
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
    
    def run(self):
        """Run the application"""
        # Auto-start if configured
        if self.config.get("auto_start", False):
            self.root.after(500, self.start_server)
        
        # Minimize to tray if configured
        if self.config.get("minimize_on_launch", False):
            self.root.after(1000, self.minimize_to_tray)
        
        self.root.mainloop()


def main():
    """Main entry point"""
    app = FaceFusionLauncher()
    app.run()


if __name__ == "__main__":
    main()
