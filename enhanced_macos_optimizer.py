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
        super().__init__("OptiMac", icon=icon_path, title="")

    @rumps.clicked("Purge Memory")
    def purge_memory(self, _):
        try:
            subprocess.run("sudo purge", shell=True)
            rumps.notification("OptiMac", "Success", "Memory purged!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to purge memory")

    @rumps.clicked("Clear Caches")
    def clear_caches(self, _):
        try:
            subprocess.run("rm -rf ~/Library/Caches/com.apple.*", shell=True)
            rumps.notification("OptiMac", "Success", "Caches cleared!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to clear caches")

    @rumps.clicked("Flush DNS")
    def flush_dns(self, _):
        try:
            subprocess.run("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", shell=True)
            rumps.notification("OptiMac", "Success", "DNS cache flushed!")
        except:
            rumps.notification("OptiMac", "Error", "Failed to flush DNS")

    @rumps.clicked("Open Full GUI")
    def open_gui(self, _):
        try:
            gui_path = os.path.join(os.path.dirname(__file__), "optimac_gui.py")
            subprocess.Popen([sys.executable, gui_path])
            rumps.notification("OptiMac", "GUI Opened", "Full interface launched!")
        except Exception as e:
            rumps.notification("OptiMac", "Error", f"Could not open GUI: {str(e)}")

if __name__ == "__main__":
    OptiMacMenuBar().run()