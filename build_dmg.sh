#!/bin/bash
"""
OptiMac Enhanced DMG Build Script
This script builds the macOS app bundle and creates a distributable DMG

Usage: ./build_dmg.sh
"""

set -e  # Exit on any error

# Configuration
APP_NAME="OptiMac Enhanced"
VERSION="2.0.0"
DMG_NAME="OptiMac-Enhanced-v${VERSION}"
BUILD_DIR="build"
DIST_DIR="dist"
DMG_DIR="dmg_temp"

echo "🚀 Building OptiMac Enhanced v${VERSION}..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "${BUILD_DIR}" "${DIST_DIR}" "${DMG_DIR}" *.dmg

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if create-dmg is installed
if ! command -v create-dmg &> /dev/null; then
    echo "⚠️  create-dmg not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    brew install create-dmg
fi

# Build the app bundle
echo "🔨 Building app bundle..."
python3 setup.py py2app

# Verify app bundle was created
if [ ! -d "${DIST_DIR}/${APP_NAME}.app" ]; then
    echo "❌ App bundle creation failed!"
    exit 1
fi

echo "✅ App bundle created successfully!"

# Create DMG staging directory
echo "📦 Preparing DMG..."
mkdir -p "${DMG_DIR}"
cp -R "${DIST_DIR}/${APP_NAME}.app" "${DMG_DIR}/"

# Add additional files to DMG
cp README.md "${DMG_DIR}/README.txt" 2>/dev/null || echo "README.md not found, skipping..."
cp LICENSE "${DMG_DIR}/LICENSE.txt" 2>/dev/null || echo "LICENSE not found, skipping..."

# Create Applications symlink for easy installation
ln -s /Applications "${DMG_DIR}/Applications"

# Create the DMG
echo "💿 Creating DMG..."
create-dmg \
    --volname "${APP_NAME} v${VERSION}" \
    --volicon "${APP_NAME}.app/Contents/Resources/app.icns" \
    --background "background.png" \
    --window-pos 200 120 \
    --window-size 800 600 \
    --icon-size 100 \
    --icon "${APP_NAME}.app" 200 190 \
    --hide-extension "${APP_NAME}.app" \
    --icon "Applications" 600 190 \
    --hdiutil-quiet \
    "${DMG_NAME}.dmg" \
    "${DMG_DIR}/" || {
    # Fallback: create simple DMG without fancy options
    echo "⚠️  Fancy DMG creation failed, creating simple DMG..."
    hdiutil create -volname "${APP_NAME} v${VERSION}" -srcfolder "${DMG_DIR}" -ov -format UDZO "${DMG_NAME}.dmg"
}

# Clean up temporary files
echo "🧹 Cleaning up..."
rm -rf "${DMG_DIR}"

# Verify DMG was created
if [ -f "${DMG_NAME}.dmg" ]; then
    DMG_SIZE=$(du -h "${DMG_NAME}.dmg" | cut -f1)
    echo "✅ DMG created successfully!"
    echo "📦 File: ${DMG_NAME}.dmg (${DMG_SIZE})"
    echo "🎉 OptiMac Enhanced v${VERSION} is ready for distribution!"
    
    # Optional: Open the DMG to test
    read -p "🔍 Would you like to test the DMG? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "${DMG_NAME}.dmg"
    fi
else
    echo "❌ DMG creation failed!"
    exit 1
fi

echo "🚀 Build complete! You can now distribute ${DMG_NAME}.dmg"
echo "📤 Consider uploading to GitHub Releases for automatic updates"