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

class OptiMacMenuBar(rumps.App):
    """Menu bar application for OptiMac"""
    
    def __init__(self):
        super(OptiMacMenuBar, self).__init__("⚡", title="OptiMac")
        self.main_app = None
        self.profiles = self.load_profiles()
        self.setup_menu()
    
    def setup_menu(self):
        """Setup the menu bar interface"""
        # Quick actions
        self.menu = [
            "Quick Actions",
            rumps.separator,
            rumps.MenuItem("🧹 Purge Memory", callback=self.quick_purge_memory),
            rumps.MenuItem("🗂️ Clear Caches", callback=self.quick_clear_caches),
            rumps.MenuItem("🔍 Flush DNS", callback=self.quick_flush_dns),
            rumps.MenuItem("🔄 Re-index Spotlight", callback=self.quick_reindex_spotlight),
            rumps.separator,
            "Profiles",
            rumps.separator,
            rumps.MenuItem("📊 Open OptiMac", callback=self.open_main_app),
            rumps.MenuItem("⚙️ Settings", callback=self.show_settings),
            rumps.MenuItem("🔄 Check for Updates", callback=self.check_updates),
            rumps.separator,
            rumps.MenuItem("❌ Quit OptiMac", callback=self.quit_app)
        ]
        
        # Add profile menu items
        profile_menu_items = []
        for profile_name in self.profiles.keys():
            profile_menu_items.append(
                rumps.MenuItem(f"▶️ {profile_name}", callback=lambda sender, p=profile_name: self.run_profile(p))
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
    
    @rumps.clicked("🧹 Purge Memory")
    def quick_purge_memory(self, sender):
        """Quick memory purge"""
        self.run_quick_command("sudo purge", "Memory purged successfully!")
    
    @rumps.clicked("🗂️ Clear Caches")
    def quick_clear_caches(self, sender):
        """Quick cache clearing"""
        self.run_quick_command("rm -rf ~/Library/Caches/com.apple.*", "Caches cleared!")
    
    @rumps.clicked("🔍 Flush DNS")
    def quick_flush_dns(self, sender):
        """Quick DNS flush"""
        self.run_quick_command("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", "DNS cache flushed!")
    
    @rumps.clicked("🔄 Re-index Spotlight")
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
    
    @rumps.clicked("📊 Open OptiMac")
    def open_main_app(self, sender):
        """Open the main OptiMac GUI"""
        if self.main_app is None or not self.main_app.root.winfo_exists():
            root = tk.Tk()
            self.main_app = MacOptimizer(root, menu_bar_app=self)
            root.mainloop()
    
    @rumps.clicked("⚙️ Settings")
    def show_settings(self, sender):
        """Show settings dialog"""
        # This would open a settings window
        rumps.alert("Settings", "Settings panel would open here")
    
    @rumps.clicked("🔄 Check for Updates")
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
    
    @rumps.clicked("❌ Quit OptiMac")
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
        self.log(f"🚀 OptiMac Enhanced v{CURRENT_VERSION} initialized. Ready to optimize your Apple Silicon Mac!")
    
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
        
        self.log(f"📋 Loaded profile: {profile_name} - {profile['description']}")
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
            
            self.log(f"💾 Saved profile: {name} with {len(selected)} optimizations")
            messagebox.showinfo("Profile Saved", f"Profile '{name}' has been saved.")
    
    def delete_selected_profile(self):
        """Delete the selected profile"""
        profile_name = self.profile_var.get()
        if not profile_name or profile_name not in self.profiles:
            messagebox.showwarning("No Profile", "Please select a profile to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the profile '{profile_name}'?"):
            del self.profiles[profile_name]
            self.save_profiles()
            self.profile_combo['values'] = list(self.profiles.keys())
            self.profile_var.set('')
            
            self.log(f"🗑️ Deleted profile: {profile_name}")
            messagebox.showinfo("Profile Deleted", f"Profile '{profile_name}' has been deleted.")
    
    def run_selected_profile(self):
        """Run the selected profile"""
        profile_name = self.profile_var.get()
        if not profile_name or profile_name not in self.profiles:
            messagebox.showwarning("No Profile", "Please select a profile to run.")
            return
        
        # Load and run the profile
        self.load_selected_profile()
        self.run_selected_optimizations()

    def create_memory_tab(self):
        memory_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(memory_frame, text="Memory & Performance")
        
        memory_options = [
            ("purge_memory", "Purge inactive memory", "Free up inactive memory using purge command"),
            ("clear_caches", "Clear system caches", "Clear user and system caches to free up space"),
            ("optimize_swap", "Optimize swap usage", "Configure swap settings for better performance"),
            ("disable_spotlight_indexing", "Disable Spotlight indexing", "Turn off Spotlight indexing for better performance"),
            ("reindex_spotlight", "Re-index Spotlight", "Rebuild Spotlight index for better search performance"),
            ("reduce_motion", "Reduce motion & animations", "Disable system animations for snappier performance"),
        ]
        
        self.create_option_checkboxes(memory_frame, memory_options, "Memory Optimizations")
    
    def create_system_tab(self):
        system_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(system_frame, text="System Tweaks")
        
        system_options = [
            ("disable_dock_animation", "Disable Dock animations", "Remove Dock show/hide animations"),
            ("disable_finder_animation", "Disable Finder animations", "Remove Finder window animations"),
            ("optimize_launchpad", "Optimize Launchpad", "Speed up Launchpad animations"),
            ("disable_dashboard", "Disable Dashboard", "Turn off Dashboard to save resources"),
            ("optimize_mission_control", "Optimize Mission Control", "Speed up Mission Control animations"),
            ("enable_trim", "Enable TRIM (SSD optimization)", "Enable TRIM support for third-party SSDs"),
        ]
        
        self.create_option_checkboxes(system_frame, system_options, "System Tweaks")
    
    def create_network_tab(self):
        network_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(network_frame, text="Network")
        
        network_options = [
            ("flush_dns", "Flush DNS cache", "Clear DNS cache for better connectivity"),
            ("optimize_tcp", "Optimize TCP settings", "Tune TCP settings for better performance"),
            ("disable_ipv6", "Disable IPv6 (if issues)", "Disable IPv6 to resolve connectivity issues"),
            ("optimize_wifi", "Optimize Wi-Fi settings", "Configure Wi-Fi for better performance"),
        ]
        
        self.create_option_checkboxes(network_frame, network_options, "Network Optimizations")
    
    def create_development_tab(self):
        dev_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(dev_frame, text="Development")
        
        dev_options = [
            ("optimize_python", "Optimize Python/Conda", "Configure Python and Conda for M-Series Macs"),
            ("optimize_git", "Optimize Git performance", "Configure Git for better performance"),
            ("optimize_homebrew", "Optimize Homebrew", "Clean and optimize Homebrew installation"),
            ("optimize_node", "Optimize Node.js", "Configure Node.js for Apple Silicon"),
        ]
        
        self.create_option_checkboxes(dev_frame, dev_options, "Development Environment")
    
    def create_advanced_tab(self):
        advanced_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(advanced_frame, text="Advanced")
        
        advanced_options = [
            ("thermal_optimization", "Thermal optimization", "Configure thermal management for sustained performance"),
            ("power_management", "Power management tweaks", "Optimize power settings for performance"),
            ("kernel_optimization", "Kernel parameter tweaks", "Advanced kernel optimizations"),
            ("create_backup", "Create system backup", "Create a backup before applying optimizations"),
        ]
        
        self.create_option_checkboxes(advanced_frame, advanced_options, "Advanced Settings")
        
        # Warning label
        warning_label = ttk.Label(advanced_frame, 
                                 text="⚠️  Advanced options may affect system stability. Use with caution!",
                                 foreground='red', font=('SF Pro Display', 10, 'bold'))
        warning_label.grid(row=10, column=0, columnspan=2, pady=(20, 0))

    def create_option_checkboxes(self, parent, options, section_title):
        section_label = ttk.Label(parent, text=section_title, font=('SF Pro Display', 12, 'bold'))
        section_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        for i, (key, title, description) in enumerate(options, 1):
            var = tk.BooleanVar()
            self.optimizations[key] = var
            
            checkbox = ttk.Checkbutton(parent, text=title, variable=var)
            checkbox.grid(row=i, column=0, sticky=tk.W, pady=2)
            
            desc_label = ttk.Label(parent, text=description, foreground='gray', font=('SF Pro Display', 9))
            desc_label.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)

    def log(self, message):
        """Add message to output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        """Clear the output log"""
        self.output_text.delete(1.0, tk.END)

    def run_command(self, command, description):
        """Run a shell command and log the output"""
        try:
            self.log(f"🔄 Running: {description}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✅ Success: {description}")
                if result.stdout.strip():
                    self.log(f"Output: {result.stdout.strip()}")
            else:
                self.log(f"❌ Error: {description}")
                if result.stderr.strip():
                    self.log(f"Error: {result.stderr.strip()}")
        except Exception as e:
            self.log(f"❌ Exception running {description}: {str(e)}")

    def run_selected_optimizations(self):
        """Run all selected optimizations"""
        selected = [key for key, var in self.optimizations.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one optimization to run.")
            return
        
        # Confirm before running
        if not messagebox.askyesno("Confirm Optimizations", 
                                  f"Are you sure you want to run {len(selected)} optimization(s)?\n\nSelected:\n" + 
                                  "\n".join([f"• {key.replace('_', ' ').title()}" for key in selected])):
            return
        
        self.status_var.set("Running optimizations...")
        self.run_selected_btn.configure(state='disabled')
        
        # Run optimizations in a separate thread
        def run_optimizations():
            try:
                self.execute_optimizations(selected)
            finally:
                self.root.after(0, self.optimization_complete)
        
        threading.Thread(target=run_optimizations, daemon=True).start()

    def optimization_complete(self):
        """Called when optimizations are complete"""
        self.status_var.set("✅ Optimizations complete!")
        self.run_selected_btn.configure(state='normal')
        self.log("🎉 All optimizations completed! Some changes may require a restart to take effect.")

    def check_for_updates(self):
        """Check for application updates"""
        self.log("🔍 Checking for updates...")
        
        def check_updates_thread():
            try:
                response = requests.get(UPDATE_URL, timeout=10)
                if response.status_code == 200:
                    latest_release = response.json()
                    latest_version = latest_release['tag_name'].lstrip('v')
                    
                    if latest_version > CURRENT_VERSION:
                        self.root.after(0, lambda: self.show_update_dialog(latest_release))
                    else:
                        self.root.after(0, lambda: self.log(f"✅ You have the latest version ({CURRENT_VERSION})"))
                else:
                    self.root.after(0, lambda: self.log("❌ Could not check for updates"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"❌ Update check failed: {str(e)}"))
        
        threading.Thread(target=check_updates_thread, daemon=True).start()
    
    def show_update_dialog(self, release_info):
        """Show update dialog"""
        latest_version = release_info['tag_name'].lstrip('v')
        
        if messagebox.askyesno("Update Available", 
                             f"Version {latest_version} is available.\nCurrent: {CURRENT_VERSION}\n\nWould you like to download it?"):
            import webbrowser
            webbrowser.open(release_info['html_url'])
            self.log(f"🌐 Opened download page for v{latest_version}")

    def execute_optimizations(self, selected):
        """Execute the selected optimizations"""
        optimization_commands = {
            # Memory optimizations
            "purge_memory": ("sudo purge", "Purging inactive memory"),
            "clear_caches": ("sudo rm -rf ~/Library/Caches/* /System/Library/Caches/* /Library/Caches/*", "Clearing system caches"),
            "optimize_swap": ("sudo sysctl vm.swappiness=10", "Optimizing swap usage"),
            "disable_spotlight_indexing": ("sudo mdutil -a -i off", "Disabling Spotlight indexing"),
            "reindex_spotlight": ("sudo mdutil -E /", "Re-indexing Spotlight"),
            "reduce_motion": ("defaults write com.apple.universalaccess reduceMotion -bool true", "Reducing motion and animations"),
            
            # System tweaks
            "disable_dock_animation": ("defaults write com.apple.dock autohide-time-modifier -float 0", "Disabling Dock animations"),
            "disable_finder_animation": ("defaults write com.apple.finder DisableAllAnimations -bool true", "Disabling Finder animations"),
            "optimize_launchpad": ("defaults write com.apple.dock springboard-show-duration -float 0", "Optimizing Launchpad"),
            "disable_dashboard": ("defaults write com.apple.dashboard mcx-disabled -bool true", "Disabling Dashboard"),
            "optimize_mission_control": ("defaults write com.apple.dock expose-animation-duration -float 0", "Optimizing Mission Control"),
            "enable_trim": ("sudo trimforce enable", "Enabling TRIM support"),
            
            # Network optimizations
            "flush_dns": ("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", "Flushing DNS cache"),
            "optimize_tcp": ("sudo sysctl -w net.inet.tcp.delayed_ack=0", "Optimizing TCP settings"),
            "disable_ipv6": ("networksetup -setv6off Wi-Fi", "Disabling IPv6"),
            "optimize_wifi": ("sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -z", "Optimizing Wi-Fi"),
            
            # Development optimizations
            "optimize_python": ("conda clean --all -y", "Optimizing Python/Conda"),
            "optimize_git": ("git config --global core.preloadindex true; git config --global core.fscache true", "Optimizing Git"),
            "optimize_homebrew": ("brew cleanup; brew doctor", "Optimizing Homebrew"),
            "optimize_node": ("npm cache clean --force", "Optimizing Node.js"),
            
            # Advanced optimizations
            "thermal_optimization": ("sudo pmset -a thermalstate 0", "Configuring thermal management"),
            "power_management": ("sudo pmset -a standby 0; sudo pmset -a autopoweroff 0", "Optimizing power management"),
            "kernel_optimization": ("echo 'kern.maxfiles=65536' | sudo tee -a /etc/sysctl.conf", "Applying kernel tweaks"),
            "create_backup": ("sudo tmutil startbackup", "Creating system backup"),
        }
        
        self.log(f"🚀 Starting optimization of {len(selected)} items...")
        
        for optimization in selected:
            if optimization in optimization_commands:
                command, description = optimization_commands[optimization]
                self.run_command(command, description)
            else:
                self.log(f"⚠️  Unknown optimization: {optimization}")

class ProfileDialog:
    """Dialog for creating/editing profiles"""
    
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.desc_text = tk.Text(frame, width=40, height=4)
        self.desc_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2)
        
        ttk.Button(button_frame, text="Save", command=self.save_profile).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT)
        
        self.name_entry.focus()
        self.dialog.wait_window()
    
    def save_profile(self):
        name = self.name_entry.get().strip()
        description = self.desc_text.get(1.0, tk.END).strip()
        
        if not name:
            messagebox.showwarning("Invalid Input", "Please enter a profile name.")
            return
        
        self.result = (name, description or "No description provided")
        self.dialog.destroy()

def main():
    """Main function to run the application"""
    # Check if running on macOS
    if sys.platform != 'darwin':
        print("This tool is designed specifically for macOS.")
        sys.exit(1)
    
    # Check if we should run menu bar only
    if len(sys.argv) > 1 and sys.argv[1] == '--menubar':
        app = OptiMacMenuBar()
        app.run()
    else:
        # Run full GUI application
        root = tk.Tk()
        app = MacOptimizer(root)
        root.mainloop()

if __name__ == "__main__":
    main()