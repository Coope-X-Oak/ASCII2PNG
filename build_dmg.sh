#!/bin/bash

# Configuration
APP_NAME="ASCII2PNG"
DIST_DIR="dist"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
DMG_FILE="$DIST_DIR/$APP_NAME.dmg"
LOG_FILE="$DIST_DIR/build_log_macos.txt"
SIGN_IDENTITY="-" # Use "-" for ad-hoc signing (local run), or replace with "Developer ID Application: Your Name (TEAMID)" for distribution

# Setup logging
mkdir -p "$DIST_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "=== Build started at $(date) ==="

# 1. Install dependencies
echo "[1/4] Installing requirements..."
pip install -r requirements.txt
pip install pyinstaller

# 2. Build .app bundle
echo "[2/4] Building .app bundle..."
# Clean previous build artifacts
rm -rf build
rm -rf "$APP_BUNDLE"
rm -f "$DMG_FILE"

# Run PyInstaller
pyinstaller ascii2png.spec --noconfirm --clean

# 3. Sign the application
echo "[3/4] Signing application..."
if [ -d "$APP_BUNDLE" ]; then
    echo "Signing with identity: $SIGN_IDENTITY"
    # --deep: Recursive signing
    # --force: Overwrite existing signature
    # --options runtime: Hardened runtime (required for notarization)
    codesign --deep --force --verify --verbose --sign "$SIGN_IDENTITY" --options runtime "$APP_BUNDLE"
else
    echo "Error: .app bundle not found at $APP_BUNDLE"
    exit 1
fi

# 4. Create DMG
echo "[4/4] Creating DMG..."

if command -v create-dmg &> /dev/null; then
    echo "Using create-dmg tool..."
    create-dmg \
      --volname "$APP_NAME" \
      --window-pos 200 120 \
      --window-size 800 400 \
      --icon-size 100 \
      --icon "$APP_NAME.app" 200 190 \
      --hide-extension "$APP_NAME.app" \
      --app-drop-link 600 185 \
      "$DMG_FILE" \
      "$APP_BUNDLE"
elif command -v hdiutil &> /dev/null; then
    echo "create-dmg not found, falling back to hdiutil..."
    # Create a temporary folder for DMG content
    DMG_SRC="$DIST_DIR/dmg_source"
    mkdir -p "$DMG_SRC"
    cp -r "$APP_BUNDLE" "$DMG_SRC/"
    ln -s /Applications "$DMG_SRC/Applications"
    
    hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_SRC" -ov -format UDZO "$DMG_FILE"
    
    # Cleanup temp folder
    rm -rf "$DMG_SRC"
else
    echo "Error: Neither create-dmg nor hdiutil found. Cannot create DMG."
    exit 1
fi

echo "=== Build finished at $(date) ==="
echo "Output: $DMG_FILE"
echo "Log: $LOG_FILE"
