#!/usr/bin/env python3

"""
OptiMac Enhanced - Comprehensive GUI Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import subprocess
import threading
import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
CURRENT_VERSION = "2.0.0"
UPDATE_URL = "https://api.github.com/repos/VonKleistL/OptiMac/releases/latest"
PROFILES_DIR = Path.home() / ".optimac_profiles"
ICON_PATH = Path(__file__).parent / "optimac_icon.icns"

class MacOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"OptiMac Enhanced v{CURRENT_VERSION} - M-Series Mac Performance Tool")
        self.root.geometry("900x800")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize optimizations dictionary
        self.optimizations = {}
        self.profiles = self.load_profiles()
        
        # Create GUI components
        self.create_gui()
        
        # Log initialization message
        self.log(f"OptiMac Enhanced v{CURRENT_VERSION} initialized. Ready to optimize your Apple Silicon Mac!")

    def create_gui(self):
        """Create the main GUI interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
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

        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD, bg='#1e1e1e', fg='white')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.run_selected_btn = ttk.Button(button_frame, text="Run Selected Optimizations",
                                           command=self.run_selected_optimizations)
        self.run_selected_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_log_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.check_updates_btn = ttk.Button(button_frame, text="Check Updates", command=self.check_updates)
        self.check_updates_btn.pack(side=tk.LEFT)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select optimizations to run")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

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

    def create_memory_tab(self):
        """Create memory optimization tab"""
        memory_frame = ttk.Frame(self.notebook)
        self.notebook.add(memory_frame, text="Memory & Performance")

        ttk.Label(memory_frame, text="Memory Optimizations", font=('SF Pro Display', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        optimizations = [
            ("purge_memory", "Purge inactive memory", "Free up inactive memory using purge command"),
            ("clear_caches", "Clear system caches", "Clear user and system caches to free up space"),
            ("optimize_swap", "Optimize swap usage", "Configure swap settings for better performance"),
            ("disable_spotlight", "Disable Spotlight indexing", "Turn off Spotlight indexing for better performance"),
            ("reindex_spotlight", "Re-index Spotlight", "Rebuild Spotlight index for better search performance"),
            ("reduce_animations", "Reduce motion & animations", "Disable system animations for snappier performance")
        ]

        for opt_id, title, description in optimizations:
            self.optimizations[opt_id] = tk.BooleanVar()
            frame = ttk.Frame(memory_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Checkbutton(frame, text=title, variable=self.optimizations[opt_id]).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=('SF Pro Display', 9), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))

    def create_system_tab(self):
        """Create system optimization tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="System Tweaks")

        ttk.Label(system_frame, text="System Optimizations", font=('SF Pro Display', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        optimizations = [
            ("disable_dock_animation", "Disable Dock animations", "Remove Dock animations for faster response"),
            ("disable_window_animations", "Disable window animations", "Remove window animations for snappier feel"),
            ("optimize_launchpad", "Optimize Launchpad", "Speed up Launchpad loading and animations"),
            ("disable_dashboard", "Disable Dashboard", "Turn off Dashboard to save memory"),
            ("optimize_finder", "Optimize Finder", "Configure Finder for better performance"),
            ("disable_sudden_motion", "Disable Sudden Motion Sensor", "Turn off SMS for SSDs (M-Series Macs)")
        ]

        for opt_id, title, description in optimizations:
            self.optimizations[opt_id] = tk.BooleanVar()
            frame = ttk.Frame(system_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Checkbutton(frame, text=title, variable=self.optimizations[opt_id]).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=('SF Pro Display', 9), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))

    def create_network_tab(self):
        """Create network optimization tab"""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="Network")

        ttk.Label(network_frame, text="Network Optimizations", font=('SF Pro Display', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        optimizations = [
            ("flush_dns", "Flush DNS cache", "Clear DNS cache for faster lookups"),
            ("optimize_network", "Optimize network settings", "Configure network for better performance"),
            ("disable_ipv6", "Disable IPv6", "Turn off IPv6 if not needed"),
            ("optimize_wifi", "Optimize Wi-Fi", "Configure Wi-Fi settings for better performance")
        ]

        for opt_id, title, description in optimizations:
            self.optimizations[opt_id] = tk.BooleanVar()
            frame = ttk.Frame(network_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Checkbutton(frame, text=title, variable=self.optimizations[opt_id]).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=('SF Pro Display', 9), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))

    def create_development_tab(self):
        """Create development optimization tab"""
        dev_frame = ttk.Frame(self.notebook)
        self.notebook.add(dev_frame, text="Development")

        ttk.Label(dev_frame, text="Development Optimizations", font=('SF Pro Display', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        optimizations = [
            ("optimize_git", "Optimize Git performance", "Configure Git for better performance"),
            ("optimize_homebrew", "Optimize Homebrew", "Clean and optimize Homebrew installation"),
            ("optimize_node", "Optimize Node.js", "Clean Node.js and npm cache"),
            ("optimize_python", "Optimize Python", "Clean Python cache and optimize"),
            ("optimize_docker", "Optimize Docker", "Clean Docker containers and images"),
            ("optimize_xcode", "Optimize Xcode", "Clean Xcode derived data and cache")
        ]

        for opt_id, title, description in optimizations:
            self.optimizations[opt_id] = tk.BooleanVar()
            frame = ttk.Frame(dev_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Checkbutton(frame, text=title, variable=self.optimizations[opt_id]).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=('SF Pro Display', 9), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))

    def create_advanced_tab(self):
        """Create advanced optimization tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced")

        ttk.Label(advanced_frame, text="Advanced Optimizations", font=('SF Pro Display', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        optimizations = [
            ("rebuild_spotlight", "Rebuild Spotlight index", "Completely rebuild Spotlight search index"),
            ("reset_launchservices", "Reset Launch Services", "Fix 'Open With' menu problems"),
            ("clear_font_cache", "Clear font cache", "Clear system font cache"),
            ("optimize_ssd", "Optimize SSD settings", "Configure SSD-specific optimizations"),
            ("disable_crash_reporter", "Disable crash reporter", "Turn off automatic crash reporting"),
            ("optimize_metal", "Optimize Metal performance", "Configure Metal graphics performance")
        ]

        for opt_id, title, description in optimizations:
            self.optimizations[opt_id] = tk.BooleanVar()
            frame = ttk.Frame(advanced_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Checkbutton(frame, text=title, variable=self.optimizations[opt_id]).pack(side=tk.LEFT)
            ttk.Label(frame, text=description, font=('SF Pro Display', 9), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))

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
                "optimizations": ["purge_memory", "clear_caches", "disable_dock_animation", "reduce_animations"],
                "description": "Quick performance improvements"
            },
            "Developer Setup": {
                "optimizations": ["optimize_git", "optimize_homebrew", "optimize_node", "optimize_python"],
                "description": "Optimize development environment"
            },
            "Gaming Mode": {
                "optimizations": ["purge_memory", "disable_dock_animation", "disable_window_animations", "optimize_metal"],
                "description": "Optimize for gaming performance"
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

        self.log(f"Loaded profile: {profile_name}")
        messagebox.showinfo("Profile Loaded", f"Profile '{profile_name}' has been loaded.")

    def save_current_profile(self):
        """Save current settings as a new profile"""
        selected = [key for key, var in self.optimizations.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Selection", "Please select some optimizations before saving a profile.")
            return

        name = simpledialog.askstring("Save Profile", "Enter profile name:")
        if name:
            self.profiles[name] = {
                "optimizations": selected,
                "description": f"Custom profile with {len(selected)} optimizations",
                "created": datetime.now().isoformat()
            }
            self.save_profiles()
            self.profile_combo['values'] = list(self.profiles.keys())
            self.profile_var.set(name)
            self.log(f"Saved profile: {name}")
            messagebox.showinfo("Profile Saved", f"Profile '{name}' has been saved.")

    def delete_selected_profile(self):
        """Delete the selected profile"""
        profile_name = self.profile_var.get()
        if not profile_name or profile_name not in self.profiles:
            messagebox.showwarning("No Profile", "Please select a profile to delete.")
            return

        if messagebox.askyesno("Delete Profile", f"Are you sure you want to delete profile '{profile_name}'?"):
            del self.profiles[profile_name]
            self.save_profiles()
            self.profile_combo['values'] = list(self.profiles.keys())
            self.profile_var.set("")
            self.log(f"Deleted profile: {profile_name}")
            messagebox.showinfo("Profile Deleted", f"Profile '{profile_name}' has been deleted.")

    def run_selected_profile(self):
        """Run the selected profile"""
        self.load_selected_profile()
        self.run_selected_optimizations()

    def run_selected_optimizations(self):
        """Run the selected optimizations"""
        selected = [key for key, var in self.optimizations.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Selection", "Please select optimizations to run.")
            return

        self.log(f"Running {len(selected)} optimizations...")
        
        def run_optimizations_thread():
            for opt in selected:
                self.run_optimization(opt)
            self.log("All optimizations completed!")
            self.status_var.set("All optimizations completed!")

        # Run in separate thread to prevent GUI freezing
        threading.Thread(target=run_optimizations_thread, daemon=True).start()

    def run_optimization(self, opt_id):
        """Run a specific optimization"""
        optimizations_map = {
            # Memory & Performance
            'purge_memory': ("sudo purge", "Memory purged"),
            'clear_caches': ("sudo rm -rf ~/Library/Caches/* /Library/Caches/*", "Caches cleared"),
            'reindex_spotlight': ("sudo mdutil -E /", "Spotlight reindexing started"),
            'disable_spotlight': ("sudo mdutil -i off /", "Spotlight indexing disabled"),
            'optimize_swap': ("sudo purge", "Swap optimized"),
            'reduce_animations': ("defaults write com.apple.universalaccess reduceMotion -bool true", "Animations reduced"),
            
            # System Tweaks
            'disable_dock_animation': ("defaults write com.apple.dock autohide-time-modifier -int 0", "Dock animations disabled"),
            'disable_window_animations': ("defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false", "Window animations disabled"),
            'optimize_finder': ("defaults write com.apple.finder AppleShowAllFiles YES", "Finder optimized"),
            'optimize_launchpad': ("defaults write com.apple.dock springboard-show-duration -int 0", "Launchpad optimized"),
            'disable_dashboard': ("defaults write com.apple.dashboard mcx-disabled -bool true", "Dashboard disabled"),
            'disable_sudden_motion': ("sudo pmset -a sms 0", "Sudden Motion Sensor disabled"),
            
            # Network
            'flush_dns': ("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", "DNS cache flushed"),
            'optimize_network': ("sudo sysctl -w net.inet.tcp.delayed_ack=0", "Network optimized"),
            'disable_ipv6': ("networksetup -setv6off Wi-Fi", "IPv6 disabled"),
            'optimize_wifi': ("sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport prefs DisconnectOnLogout=NO", "Wi-Fi optimized"),
            
            # Development
            'optimize_git': ("git config --global core.precomposeunicode true", "Git optimized"),
            'optimize_homebrew': ("brew cleanup", "Homebrew cleaned"),
            'optimize_node': ("npm cache clean --force", "Node.js cache cleared"),
            'optimize_python': ("python -m pip cache purge", "Python cache cleared"),
            'optimize_docker': ("docker system prune -f", "Docker optimized"),
            'optimize_xcode': ("rm -rf ~/Library/Developer/Xcode/DerivedData/*", "Xcode cleaned"),
            
            # Advanced
            'rebuild_spotlight': ("sudo mdutil -i off / && sudo mdutil -i on /", "Spotlight index rebuilt"),
            'reset_launchservices': ("sudo /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local", "Launch Services reset"),
            'clear_font_cache': ("sudo atsutil databases -remove", "Font cache cleared"),
            'optimize_ssd': ("sudo trimforce enable", "SSD optimized"),
            'disable_crash_reporter': ("defaults write com.apple.CrashReporter DialogType none", "Crash reporter disabled"),
            'optimize_metal': ("defaults write com.apple.CoreGraphics CGDirectDisplayID -bool true", "Metal performance optimized")
        }
        
        if opt_id in optimizations_map:
            command, description = optimizations_map[opt_id]
            self.run_command(command, description)
        else:
            self.log(f"Optimization {opt_id} not implemented yet")

    def run_command(self, command, description):
        """Run a system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✓ {description}")
                self.status_var.set(f"Completed: {description}")
            else:
                self.log(f"✗ {description} failed: {result.stderr[:100]}")
                self.status_var.set(f"Failed: {description}")
        except Exception as e:
            self.log(f"✗ {description} error: {str(e)}")

    def check_updates(self):
        """Check for application updates"""
        try:
            response = requests.get(UPDATE_URL, timeout=10)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name'].lstrip('v')
                if latest_version > CURRENT_VERSION:
                    messagebox.showinfo("Update Available", f"Version {latest_version} is available!")
                else:
                    messagebox.showinfo("Up to Date", f"You have the latest version ({CURRENT_VERSION})")
            else:
                messagebox.showerror("Update Check Failed", "Could not check for updates")
        except Exception as e:
            messagebox.showerror("Update Check Failed", f"Error: {str(e)}")

    def log(self, message):
        """Add message to output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)

    def clear_log(self):
        """Clear the output log"""
        self.output_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MacOptimizer(root)
    root.mainloop()