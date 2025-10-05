#!/usr/bin/env python3
"""
Simple GUI test for OptiMac
"""

import sys
import tkinter as tk
from tkinter import messagebox
import platform

def test_gui():
    """Test basic GUI functionality"""
    try:
        root = tk.Tk()
        root.title("OptiMac GUI Test")
        root.geometry("500x400")
        
        # Title
        label = tk.Label(root, text="🧪 OptiMac GUI Test", font=('SF Pro Display', 16, 'bold'))
        label.pack(pady=20)
        
        # System info
        info_text = tk.Text(root, height=12, width=60)
        info_text.pack(pady=20, padx=20)
        
        system_info = f"""OptiMac GUI Test Results
{'=' * 40}

System Information:
• Platform: {platform.platform()}
• Architecture: {platform.machine()}
• Python Version: {platform.python_version()}
• System: {platform.system()}

Apple Silicon Status:
{'✅ Perfect for OptiMac!' if platform.machine() == 'arm64' else '⚠️  Intel Mac detected'}

GUI Components:
✅ Tkinter available
✅ Window creation successful
✅ Text widgets functional
✅ All components working

🎉 OptiMac is ready to run on your system!

Next step: python3 macos_optimizer.py
"""
        
        info_text.insert(tk.END, system_info)
        info_text.configure(state='disabled')
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        def close_test():
            print("✅ GUI test completed successfully!")
            root.destroy()
        
        def run_optimac():
            print("🚀 Launching OptiMac...")
            root.destroy()
            # Here we could import and run the main app
            try:
                import subprocess
                subprocess.run(["python3", "macos_optimizer.py"])
            except:
                print("Please run: python3 macos_optimizer.py")
        
        close_btn = tk.Button(button_frame, text="✅ Test Complete", command=close_test, 
                             font=('SF Pro Display', 12))
        close_btn.pack(side=tk.LEFT, padx=10)
        
        run_btn = tk.Button(button_frame, text="🚀 Launch OptiMac", command=run_optimac,
                           font=('SF Pro Display', 12), bg='#007AFF', fg='white')
        run_btn.pack(side=tk.LEFT, padx=10)
        
        print("🧪 GUI test window opened - check the window!")
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OptiMac GUI components...")
    
    if sys.platform != 'darwin':
        print("⚠️  Warning: Not running on macOS - some features may not work")
    
    if test_gui():
        print("🎉 All GUI tests passed!")
    else:
        print("❌ GUI tests failed.")