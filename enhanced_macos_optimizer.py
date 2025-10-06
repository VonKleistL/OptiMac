#!/usr/bin/env python3
"""
OptiMac Enhanced - macOS GUI Optimization Tool with Menu Bar Support
Created for optimizing M-Series Mac performance
Author: VonKleistL
GitHub: https://github.com/VonKleistL/OptiMac
Version: 2.0.0
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import sys
import json
import requests
from pathlib import Path
import rumps  # For menu bar functionality
from datetime import datetime
# Configuration
CURRENT_VERSION = "2.0.0"
UPDATE_URL = "https://api.github.com/repos/VonKleistL/OptiMac/releases/latest"
PROFILES_DIR = Path.home() / ".optimac_profiles"
ICON_PATH = Path(__file__).parent / "optimac_icon.icns"  # Custom icon path
class OptiMacMenuBar(rumps.App):
    """Menu bar application for OptiMac"""

    def __init__(self):
        # Use custom icon if available, otherwise use text
        icon_path = str(ICON_PATH) if ICON_PATH.exists() else None
        super(OptiMacMenuBar, self).__init__("OptiMac", icon=icon_path, title="")
        self.main_app = None
        self.profiles = self.load_profiles()
        self.setup_menu()

    def setup_menu(self):
        """Setup the menu bar interface"""
        # Quick actions
        self.menu = [
            "Quick Actions",
            rumps.separator,
            rumps.MenuItem("Purge Memory", callback=self.quick_purge_memory),
            rumps.MenuItem("Clear Caches", callback=self.quick_clear_caches),
            rumps.MenuItem("Flush DNS", callback=self.quick_flush_dns),
            rumps.MenuItem("Re-index Spotlight", callback=self.quick_reindex_spotlight),
            rumps.separator,
            "Profiles",
            rumps.separator,
            rumps.MenuItem("Open OptiMac", callback=self.open_main_app),
            rumps.MenuItem("Settings", callback=self.show_settings),
            rumps.MenuItem("Check for Updates", callback=self.check_updates),
            rumps.separator,
            rumps.MenuItem("Quit OptiMac", callback=self.quit_app)
        ]

        # Add profile menu items
        profile_menu_items = []
        for profile_name in self.profiles.keys():
            profile_menu_items.append(
                rumps.MenuItem(f"{profile_name}", callback=lambda sender, p=profile_name: self.run_profile(p))
            )

        # Insert profile items after "Profiles" separator
        self.menu[8:8] = profile_menu_items

    def load_profiles(self):
        """Load saved optimization profiles"""
        PROFILES_DIR.mkdir(exist_ok=True)
        profiles_file = PROFILES_DIR / "profiles.json"

        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default profiles
        return {
            "Performance Boost": {
                "optimizations": ["purge_memory", "clear_caches", "disable_dock_animation", "reduce_motion"],
                "description": "Quick performance improvements"
            },
            "Developer Setup": {
                "optimizations": ["optimize_python", "optimize_git", "optimize_homebrew", "optimize_node"],
                "description": "Optimize development environment"
            }
        }

    def save_profiles(self):
        """Save profiles to disk"""
        PROFILES_DIR.mkdir(exist_ok=True)
        profiles_file = PROFILES_DIR / "profiles.json"

        with open(profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)

    @rumps.clicked("Purge Memory")
    def quick_purge_memory(self, sender):
        """Quick memory purge"""
        self.run_quick_command("sudo purge", "Memory purged successfully!")

    @rumps.clicked("Clear Caches")
    def quick_clear_caches(self, sender):
        """Quick cache clearing"""
        self.run_quick_command("rm -rf ~/Library/Caches/com.apple.*", "Caches cleared!")

    @rumps.clicked("Flush DNS")
    def quick_flush_dns(self, sender):
        """Quick DNS flush"""
        self.run_quick_command("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", "DNS cache flushed!")

    @rumps.clicked("Re-index Spotlight")
    def quick_reindex_spotlight(self, sender):
        """Re-index Spotlight"""
        self.run_quick_command("sudo mdutil -E /", "Spotlight re-indexing started!")

    def run_quick_command(self, command, success_message):
        """Run a quick command with notification"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                rumps.notification("OptiMac", "Success", success_message)
            else:
                rumps.notification("OptiMac", "Error", f"Command failed: {result.stderr[:100]}")
        except Exception as e:
            rumps.notification("OptiMac", "Error", f"Exception: {str(e)[:100]}")

    def run_profile(self, profile_name):
        """Run a saved profile"""
        if profile_name in self.profiles:
            profile = self.profiles[profile_name]
            # Here you would run the profile optimizations
            rumps.notification("OptiMac", "Profile Running", f"Running {profile_name} profile...")
            # Implementation would go here to actually run the optimizations

    @rumps.clicked("Open OptiMac")
    def open_main_app(self, sender):
        """Open the main OptiMac GUI"""
        if self.main_app is None or not self.main_app.root.winfo_exists():
            root = tk.Tk()
            self.main_app = MacOptimizer(root, menu_bar_app=self)
            root.mainloop()

    @rumps.clicked("Settings")
    def show_settings(self, sender):
        """Show settings dialog"""
        # This would open a settings window
        rumps.alert("Settings", "Settings panel would open here")

    @rumps.clicked("Check for Updates")
    def check_updates(self, sender):
        """Check for application updates"""
        try:
            response = requests.get(UPDATE_URL, timeout=10)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name'].lstrip('v')

                if latest_version > CURRENT_VERSION:
                    if rumps.alert("Update Available", 
                                 f"Version {latest_version} is available.\nCurrent: {CURRENT_VERSION}\n\nWould you like to download it?",
                                 ok="Download", cancel="Later"):
                        import webbrowser
                        webbrowser.open(latest_release['html_url'])
                else:
                    rumps.alert("Up to Date", f"You have the latest version ({CURRENT_VERSION})")
            else:
                rumps.alert("Update Check Failed", "Could not check for updates")
        except Exception as e:
            rumps.alert("Update Check Failed", f"Error: {str(e)}")

    @rumps.clicked("Quit OptiMac")
    def quit_app(self, sender):
        """Quit the application"""
        rumps.quit_application()
class MacOptimizer:
    def __init__(self, root, menu_bar_app=None):
        self.root = root
        self.menu_bar_app = menu_bar_app
        self.root.title(f"OptiMac Enhanced v{CURRENT_VERSION} - M-Series Mac Performance Tool")
        self.root.geometry("900x800")
        self.root.configure(bg='#f0f0f0')

        # Set custom icon for GUI if available (prefer .png via iconphoto; fallback to .icns via iconbitmap)
        try:
            if ICON_PATH.exists():
                try:
                    self.root.iconbitmap(str(ICON_PATH))
                except Exception:
                    pass
                png_icon = ICON_PATH.with_suffix('.png')
                if png_icon.exists():
                    icon_img = tk.PhotoImage(file=str(png_icon))
                    self.root.iconphoto(True, icon_img)
        except Exception:
            pass

        # Initialize optimizations dictionary FIRST
        self.optimizations = {}
        self.profiles = self.load_profiles()

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text=f"OptiMac Enhanced v{CURRENT_VERSION}", 
                               font=('SF Pro Display', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Optimize your M-Series Mac for peak performance", 
                                  font=('SF Pro Display', 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Profile management frame
        self.create_profile_management(main_frame)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(3, weight=1)

        # Create tabs
        self.create_memory_tab()
        self.create_system_tab()
        self.create_network_tab()
        self.create_development_tab()
        self.create_advanced_tab()

        # Output area
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="5")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.run_selected_btn = ttk.Button(button_frame, text="Run Selected Optimizations", 
                                          command=self.run_selected_optimizations)
        self.run_selected_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_log_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.check_updates_btn = ttk.Button(button_frame, text="Check Updates", command=self.check_for_updates)
        self.check_updates_btn.pack(side=tk.LEFT)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select optimizations to run")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Log initialization message
        self.log(f"OptiMac Enhanced v{CURRENT_VERSION} initialized with custom icon. Ready to optimize your Apple Silicon Mac!")

    def create_profile_management(self, parent):
        """Create profile management interface"""
        profile_frame = ttk.LabelFrame(parent, text="Profile Management", padding="5")
        profile_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Profile selection
        ttk.Label(profile_frame, text="Profile:").grid(row=0, column=0, padx=(0, 5))

        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.profile_var, 
                                         values=list(self.profiles.keys()), state="readonly")
        self.profile_combo.grid(row=0, column=1, padx=(0, 10))

        # Profile buttons
        ttk.Button(profile_frame, text="Load Profile", command=self.load_selected_profile).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(profile_frame, text="Save Profile", command=self.save_current_profile).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(profile_frame, text="Delete Profile", command=self.delete_selected_profile).grid(row=0, column=4, padx=(0, 5))
        ttk.Button(profile_frame, text="Run Profile", command=self.run_selected_profile).grid(row=0, column=5)

    def load_profiles(self):
        """Load saved optimization profiles"""
        PROFILES_DIR.mkdir(exist_ok=True)
        profiles_file = PROFILES_DIR / "profiles.json"

        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default profiles
        return {
            "Performance Boost": {
                "optimizations": ["purge_memory", "clear_caches", "disable_dock_animation", "reduce_motion"],
                "description": "Quick performance improvements"
            },
            "Developer Setup": {
                "optimizations": ["optimize_python", "optimize_git", "optimize_homebrew", "optimize_node"],
                "description": "Optimize development environment"
            },
            "Network Optimization": {
                "optimizations": ["flush_dns", "optimize_tcp", "optimize_wifi"],
                "description": "Network performance tweaks"
            }
        }

    def save_profiles(self):
        """Save profiles to disk"""
        PROFILES_DIR.mkdir(exist_ok=True)
        profiles_file = PROFILES_DIR / "profiles.json"

        with open(profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)

    def load_selected_profile(self):
        """Load the selected profile settings"""
        profile_name = self.profile_var.get()
        if not profile_name or profile_name not in self.profiles:
            messagebox.showwarning("No Profile", "Please select a profile to load.")
            return

        profile = self.profiles[profile_name]

        # Clear all checkboxes first
        for var in self.optimizations.values():
            var.set(False)

        # Set checkboxes based on profile
        for optimization in profile['optimizations']:
            if optimization in self.optimizations:
                self.optimizations[optimization].set(True)

        self.log(f"Loaded profile: {profile_name} - {profile['description']}")
        messagebox.showinfo("Profile Loaded", f"Profile '{profile_name}' has been loaded.")

    def save_current_profile(self):
        """Save current settings as a new profile"""
        selected = [key for key, var in self.optimizations.items() if var.get()]

        if not selected:
            messagebox.showwarning("No Selection", "Please select some optimizations before saving a profile.")
            return

        # Get profile name and description
        dialog = ProfileDialog(self.root, "Save Profile")
        if dialog.result:
            name, description = dialog.result

            self.profiles[name] = {
                "optimizations": selected,
                "description": description,
                "created": datetime.now().isoformat()
            }

            self.save_profiles()
            self.profile_combo['values'] = list(self.profiles.keys())
            self.profile_var.set(name)

            self.log(f"Saved profile: {name} with {len(selected)} optimizations")
            messagebox.showinfo("Profile Saved", f"Profile '{name}' has been saved.")

    def delete_selected_profile(self):
        """Delete the selected profile"""
        profile_name = self.profile_var.get
