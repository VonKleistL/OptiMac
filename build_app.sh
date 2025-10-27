#!/bin/bash

# OptiMac App Bundle Builder
# This script creates a proper macOS app bundle for easy distribution

echo "🏗️  Building OptiMac App Bundle"
echo "=============================="

APP_NAME="OptiMac"
BUNDLE_NAME="OptiMac.app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Clean previous builds
if [ -d "$BUNDLE_NAME" ]; then
    echo "🗑️  Removing existing app bundle..."
    rm -rf "$BUNDLE_NAME"
fi

# Create app bundle structure
echo "📁 Creating app bundle structure..."
mkdir -p "$BUNDLE_NAME/Contents/MacOS"
mkdir -p "$BUNDLE_NAME/Contents/Resources"

# Create Info.plist
cat > "$BUNDLE_NAME/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>OptiMac</string>
    <key>CFBundleDisplayName</key>
    <string>OptiMac</string>
    <key>CFBundleIdentifier</key>
    <string>com.vonkleistl.optimac</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>optimac</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>OPMAC</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSArchitecturePriority</key>
    <array>
        <string>arm64</string>
        <string>x86_64</string>
    </array>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# Create launcher script
cat > "$BUNDLE_NAME/Contents/MacOS/optimac" << 'LAUNCHER_EOF'
#!/bin/bash
cd "$(dirname "$0")/../Resources"
exec python3 macos_optimizer.py
LAUNCHER_EOF

# Make launcher executable
chmod +x "$BUNDLE_NAME/Contents/MacOS/optimac"

# Copy Python script and resources
cp macos_optimizer.py "$BUNDLE_NAME/Contents/Resources/"
cp README.md "$BUNDLE_NAME/Contents/Resources/"
cp LICENSE "$BUNDLE_NAME/Contents/Resources/"

# Create simple icon placeholder
echo "🎨 Creating app icon placeholder..."
touch "$BUNDLE_NAME/Contents/Resources/AppIcon.icns"

echo "✅ App bundle created successfully!"
echo "📦 Location: $SCRIPT_DIR/$BUNDLE_NAME"
echo ""
echo "🚀 To distribute:"
echo "   1. Zip the app bundle: zip -r 'OptiMac.zip' '$BUNDLE_NAME'"
echo "   2. Users can drag the app to Applications folder"
echo "   3. Right-click and 'Open' first time to bypass Gatekeeper"
echo ""
echo "💡 Optional improvements:"
echo "   - Add a proper AppIcon.icns file"
echo "   - Code sign the app bundle"
echo "   - Create a DMG installer"