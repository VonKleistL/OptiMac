#!/usr/bin/env python3
"""
OptiMac Enhanced Setup Script
Used to create macOS app bundle and DMG for distribution
"""

from setuptools import setup
import py2app
import os
import plist

VERSION = "2.0.0"
APP_NAME = "OptiMac Enhanced"
BUNDLE_ID = "com.vonkleistl.optimac"

# App configuration
APP = ['enhanced_macos_optimizer.py']
DATA_FILES = [
    ('', ['README.md', 'LICENSE']),
    ('resources', []),  # Add any resource files here
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Add icon file here if available
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': f"{APP_NAME} v{VERSION}",
        'CFBundleIdentifier': BUNDLE_ID,
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'LSMinimumSystemVersion': '10.15.0',  # macOS Catalina minimum
        'LSUIElement': False,  # Set to True for menu bar only app
        'NSRequiresAquaSystemAppearance': False,
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSAppleEventsUsageDescription': 'OptiMac needs to run system commands to optimize your Mac.',
        'NSSystemAdministrationUsageDescription': 'OptiMac requires administrator privileges to perform system optimizations.',
    },
    'packages': ['rumps', 'requests'],
    'includes': ['tkinter', 'subprocess', 'threading', 'json', 'datetime', 'pathlib'],
    'excludes': ['matplotlib', 'numpy', 'scipy'],  # Exclude unnecessary packages
    'resources': [],
    'optimize': 2,
}

setup(
    app=APP,
    name=APP_NAME,
    version=VERSION,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    author='VonKleistL',
    author_email='your.email@example.com',
    description='Advanced macOS optimization tool for M-Series Macs',
    url='https://github.com/VonKleistL/OptiMac',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)