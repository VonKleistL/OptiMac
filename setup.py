#!/usr/bin/env python3
"""
OptiMac Enhanced Setup Script
Used to create macOS app bundle and DMG for distribution
"""

from setuptools import setup
import py2app
import os
from pathlib import Path

VERSION = "2.0.0"
APP_NAME = "OptiMac Enhanced"
BUNDLE_ID = "com.vonkleistl.optimac"
ICON_FILE = "optimac_icon.icns"

# App configuration
APP = ['enhanced_macos_optimizer.py']
DATA_FILES = [
    ('', ['README.md', 'LICENSE'] if Path('LICENSE').exists() else ['README.md']),
    ('', [ICON_FILE] if Path(ICON_FILE).exists() else []),  # Include icon in bundle
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': ICON_FILE if Path(ICON_FILE).exists() else None,  # Use custom icon
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': f"{APP_NAME} v{VERSION} - Apple Silicon Mac Optimizer",
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
        'CFBundleDocumentTypes': [],
        'CFBundleURLTypes': [],
        # Custom icon info
        'CFBundleIconFile': ICON_FILE.replace('.icns', '') if Path(ICON_FILE).exists() else None,
    },
    'packages': ['rumps', 'requests'],
    'includes': ['tkinter', 'subprocess', 'threading', 'json', 'datetime', 'pathlib'],
    'excludes': ['matplotlib', 'numpy', 'scipy', 'pandas'],  # Exclude unnecessary packages
    'resources': [ICON_FILE] if Path(ICON_FILE).exists() else [],
    'optimize': 2,
    'arch': 'universal2',  # Universal binary for Intel and Apple Silicon
    'no_strip': True,  # Keep debug info for better error reporting
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
    description='Advanced macOS optimization tool for M-Series Macs with custom branding',
    long_description='OptiMac Enhanced brings powerful system optimizations to your Apple Silicon Mac through an intuitive GUI and menu bar integration.',
    url='https://github.com/VonKleistL/OptiMac',
    keywords=['macos', 'optimization', 'apple-silicon', 'm1', 'm2', 'm3', 'performance'],
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
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
)