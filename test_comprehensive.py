#!/usr/bin/env python3
"""
Comprehensive Test Suite for OptiMac
Run this on your M2 Mac to verify everything works
"""

import sys
import platform
import subprocess
import importlib
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"🔍 {title}")
    print('=' * 60)

def print_result(test_name, success, details=""):
    """Print test result with emoji"""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")

def test_system_compatibility():
    """Test system compatibility"""
    print_header("SYSTEM COMPATIBILITY TEST")
    
    # Check macOS
    is_macos = platform.system() == 'Darwin'
    print_result("Running on macOS", is_macos, 
                f"Platform: {platform.platform()}")
    
    # Check architecture
    is_arm64 = platform.machine() == 'arm64'
    print_result("Apple Silicon (ARM64)", is_arm64, 
                f"Architecture: {platform.machine()}")
    
    # Check Python version
    python_version = platform.python_version()
    version_parts = [int(x) for x in python_version.split('.')]
    python_ok = version_parts >= [3, 6]
    print_result("Python 3.6+", python_ok, 
                f"Python version: {python_version}")
    
    return is_macos and python_ok

def test_required_modules():
    """Test required Python modules"""
    print_header("PYTHON MODULES TEST")
    
    required_modules = [
        ('tkinter', 'GUI framework'),
        ('tkinter.ttk', 'Themed widgets'),
        ('tkinter.scrolledtext', 'Scrolled text widget'),
        ('subprocess', 'Shell command execution'),
        ('threading', 'Background operations'),
        ('pathlib', 'Path operations'),
        ('os', 'Operating system interface'),
        ('sys', 'System-specific parameters')
    ]
    
    all_modules_ok = True
    for module_name, description in required_modules:
        try:
            importlib.import_module(module_name)
            print_result(f"{module_name}", True, description)
        except ImportError as e:
            print_result(f"{module_name}", False, f"Import error: {e}")
            all_modules_ok = False
    
    return all_modules_ok

def test_gui_creation():
    """Test GUI creation without displaying"""
    print_header("GUI CREATION TEST")
    
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext
        
        # Test root window creation (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        print_result("Root window creation", True)
        
        # Test themed widgets
        frame = ttk.Frame(root)
        print_result("TTK Frame creation", True)
        
        # Test notebook (tabs)
        notebook = ttk.Notebook(frame)
        print_result("TTK Notebook creation", True)
        
        # Test scrolled text
        text_widget = scrolledtext.ScrolledText(frame)
        print_result("ScrolledText widget creation", True)
        
        # Test variables
        bool_var = tk.BooleanVar()
        string_var = tk.StringVar()
        print_result("Tkinter variables", True)
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print_result("GUI creation", False, f"Error: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 OptiMac - Quick Test Suite")
    print(f"Running on: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    
    tests = [
        ("System Compatibility", test_system_compatibility),
        ("Python Modules", test_required_modules),
        ("GUI Creation", test_gui_creation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        print_result(test_name, result)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your system is fully compatible with OptiMac")
        print("\n🚀 Ready to run: python3 macos_optimizer.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("❌ Please fix the issues before using OptiMac")

if __name__ == "__main__":
    main()