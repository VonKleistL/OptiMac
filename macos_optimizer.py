#!/usr/bin/env python3
"""
OptiMac - macOS GUI Optimization Tool
Created for optimizing M-Series Mac performance

Author: VonKleistL
GitHub: https://github.com/VonKleistL/OptiMac
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
from pathlib import Path

class MacOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("OptiMac - M-Series Mac Performance Tool")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize optimizations dictionary FIRST
        self.optimizations = {}
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="OptiMac for Apple Silicon", 
                               font=('SF Pro Display', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Optimize your M-Series Mac for peak performance", 
                                  font=('SF Pro Display', 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)
        
        # Create tabs
        self.create_memory_tab()
        self.create_system_tab()
        self.create_network_tab()
        self.create_development_tab()
        self.create_advanced_tab()
        
        # Output area
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="5")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        self.run_selected_btn = ttk.Button(button_frame, text="Run Selected Optimizations", 
                                          command=self.run_selected_optimizations)
        self.run_selected_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_log_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select optimizations to run")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log initialization message
        self.log("🚀 OptiMac initialized. Ready to optimize your Apple Silicon Mac!")

    def create_memory_tab(self):
        memory_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(memory_frame, text="Memory & Performance")
        
        memory_options = [
            ("purge_memory", "Purge inactive memory", "Free up inactive memory using purge command"),
            ("clear_caches", "Clear system caches", "Clear user and system caches to free up space"),
            ("optimize_swap", "Optimize swap usage", "Configure swap settings for better performance"),
            ("disable_spotlight_indexing", "Disable Spotlight indexing", "Turn off Spotlight indexing for better performance"),
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
        self.output_text.insert(tk.END, f"{message}\n")
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

    def execute_optimizations(self, selected):
        """Execute the selected optimizations"""
        optimization_commands = {
            # Memory optimizations
            "purge_memory": ("sudo purge", "Purging inactive memory"),
            "clear_caches": ("sudo rm -rf ~/Library/Caches/* /System/Library/Caches/* /Library/Caches/*", "Clearing system caches"),
            "optimize_swap": ("sudo sysctl vm.swappiness=10", "Optimizing swap usage"),
            "disable_spotlight_indexing": ("sudo mdutil -a -i off", "Disabling Spotlight indexing"),
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


def main():
    """Main function to run the application"""
    # Check if running on macOS
    if sys.platform != 'darwin':
        print("This tool is designed specifically for macOS.")
        sys.exit(1)
    
    root = tk.Tk()
    app = MacOptimizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
