# macOS Build Instructions for ASCII2PNG

This project includes a fully automated script to build and package the application for macOS.

## Prerequisites

1.  **Python 3.8+**: Ensure Python is installed.
2.  **Node.js (Optional)**: Required if you want to use `create-dmg` for a professional installer look.
    *   Install Node.js from https://nodejs.org/
    *   Install `create-dmg`: `npm install -g create-dmg`

## How to Build

1.  **Open Terminal** and navigate to the project root directory.
2.  **Make the script executable**:
    ```bash
    chmod +x build_dmg.sh
    ```
3.  **Run the build script**:
    ```bash
    ./build_dmg.sh
    ```

## Output

*   **Application Bundle**: `dist/ASCII2PNG.app` (Can be run directly on this machine)
*   **Disk Image**: `dist/ASCII2PNG.dmg` (The final installer file for distribution)
*   **Build Log**: `dist/build_log_macos.txt`

## Signing

The script uses ad-hoc signing (`-`) by default, which allows the app to run locally.
For public distribution (to avoid "Unidentified Developer" warnings), you need an Apple Developer ID.
Edit `build_dmg.sh` and update the `SIGN_IDENTITY` variable:
```bash
SIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)"
```

## Troubleshooting

*   **"Damaged" or "Move to Bin" error**: This is a Gatekeeper security feature.
    *   Right-click the app and select "Open".
    *   Or remove the quarantine attribute: `xattr -cr dist/ASCII2PNG.app`
