#!/usr/bin/env python3
import rumps
import subprocess
import sys
import os
from pathlib import Path

# Icon path
ICON_PATH = Path(__file__).parent / "optimac_icon.icns"

class OptiMacMenuBar(rumps.App):
    def __init__(self):
        # Use custom icon if available
        icon_path = str(ICON_PATH) if ICON_PATH.exists() else None
        super().__init__("OptiMac", icon=icon_path, title="" if icon_path else "⚡")

    @rumps.clicked("Quick Memory Purge")
    def purge_memory(self, _):
        try:
            subprocess.run("sudo purge", shell=True)
            rumps.notification("OptiMac", "Success", "Memory purged successfully!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to purge memory")

    @rumps.clicked("Clear System Caches")  
    def clear_caches(self, _):
        try:
            commands = [
                "rm -rf ~/Library/Caches/com.apple.*",
                "sudo rm -rf /Library/Caches/*"
            ]
            for cmd in commands:
                subprocess.run(cmd, shell=True)
            rumps.notification("OptiMac", "Success", "System caches cleared!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to clear caches")

    @rumps.clicked("Flush DNS Cache")
    def flush_dns(self, _):
        try:
            subprocess.run("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", shell=True)
            rumps.notification("OptiMac", "Success", "DNS cache flushed!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to flush DNS")

    @rumps.clicked("Re-index Spotlight")
    def reindex_spotlight(self, _):
        try:
            subprocess.run("sudo mdutil -E /", shell=True)
            rumps.notification("OptiMac", "Success", "Spotlight re-indexing started!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to re-index Spotlight")

    @rumps.clicked("Open Full GUI")
    def open_gui(self, _):
        try:
            # Use AppleScript to open Terminal and run the GUI script
            gui_path = os.path.join(os.path.dirname(__file__), "optimac_gui.py")
            
            # Create AppleScript to launch GUI in new Terminal window
            applescript = f'''
            tell application "Terminal"
                do script "cd '{os.path.dirname(__file__)}' && python optimac_gui.py"
                activate
            end tell
            '''
            
            subprocess.run(['osascript', '-e', applescript])
            rumps.notification("OptiMac", "GUI Opened", "Full interface launched in Terminal!")
            
        except Exception as e:
            # Fallback: try direct subprocess
            try:
                gui_path = os.path.join(os.path.dirname(__file__), "optimac_gui.py")
                subprocess.Popen([sys.executable, gui_path])
                rumps.notification("OptiMac", "GUI Opened", "Full interface launched!")
            except:
                rumps.notification("OptiMac", "Error", "Could not open GUI")

    @rumps.clicked("Performance Profile")
    def performance_profile(self, _):
        try:
            commands = [
                "sudo purge",
                "rm -rf ~/Library/Caches/com.apple.*",
                "sudo dscacheutil -flushcache"
            ]
            for cmd in commands:
                subprocess.run(cmd, shell=True)
            rumps.notification("OptiMac", "Profile Complete", "Performance boost applied!")
        except:
            rumps.notification("OptiMac", "Error", "Performance profile failed")

    @rumps.clicked("About OptiMac")
    def about(self, _):
        rumps.alert("OptiMac Enhanced v2.0.0", 
                   "Professional macOS optimization tool for M-Series Macs\n\n✓ Menu bar quick actions\n✓ Comprehensive GUI interface\n✓ System optimization profiles\n✓ Memory and cache management\n\nAuthor: VonKleistL")

if __name__ == "__main__":
    OptiMacMenuBar().run()