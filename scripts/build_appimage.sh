#!/usr/bin/env bash
# Build a portable AppImage for GhostMEAN.
#
# Usage: ./scripts/build_appimage.sh
# Output: dist/GhostMEAN-<version>-x86_64.AppImage
#
# Pipeline: PyInstaller (onedir bundle) -> AppDir -> appimagetool.
#
# Lessons carried over from GhostPoster's build script (learned the hard
# way there, applied here from the start instead of waiting to hit the
# same bugs again):
#   - ALWAYS chmod +x appimagetool after downloading it, regardless of
#     whether the download was "fresh" -- a leftover non-executable file
#     from an earlier interrupted run must not skip this step.
#   - Verify the downloaded appimagetool is a real, complete ELF binary
#     before trying to run it, with a clear "delete and retry" message on
#     failure instead of a cryptic exec error.
#   - Delete the bundled libxkbcommon(-x11).so* files before packaging so
#     the AppImage falls back to the host system's copy at runtime --
#     bundling them risks an ABI mismatch against the system's Wayland/X11
#     stack that can SIGSEGV on window close on some distros.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"

VERSION="$(python3 -c 'import ghostmean; print(ghostmean.__version__)')"
APPDIR="$HERE/build/AppDir"
DIST="$HERE/dist"
APPIMAGETOOL="$HERE/build/appimagetool.AppImage"
APPIMAGETOOL_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"

echo "==> GhostMEAN AppImage build — v${VERSION}"

# --- 1. Clean previous build artifacts (but keep downloaded appimagetool) ---
rm -rf "$HERE/build/ghostmean" "$HERE/dist" "$APPDIR"
mkdir -p "$DIST"

# --- 2. PyInstaller onedir bundle ---
echo "==> Running PyInstaller..."
if ! command -v pyinstaller >/dev/null 2>&1; then
    echo "    pyinstaller not found, installing..."
    pip install pyinstaller --break-system-packages -q
fi
pyinstaller ghostmean.spec --noconfirm

# --- 3. Assemble the AppDir ---
echo "==> Assembling AppDir..."
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps" "$APPDIR/usr/share/metainfo"

cp -r "$HERE/dist/ghostmean/"* "$APPDIR/usr/bin/"

DESKTOP_FILE="$APPDIR/usr/share/applications/io.github.nftomczain.GhostMEAN.desktop"
cp "$HERE/packaging/io.github.nftomczain.GhostMEAN.desktop" "$DESKTOP_FILE"
cp "$DESKTOP_FILE" "$APPDIR/io.github.nftomczain.GhostMEAN.desktop"

cp "$HERE/packaging/io.github.nftomczain.GhostMEAN.metainfo.xml" "$APPDIR/usr/share/metainfo/"

python3 -c "
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt
img = QImage('$HERE/ghostmean/assets/icon.png').convertToFormat(QImage.Format_RGBA8888)
scaled = img.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
scaled.save('$APPDIR/usr/share/icons/hicolor/256x256/apps/ghostmean.png')
scaled.save('$APPDIR/ghostmean.png')
"

# libxkbcommon ABI-mismatch guard (see header comment) -- fall back to the
# host system's copy instead of bundling a possibly-incompatible one.
find "$APPDIR/usr/bin" -name "libxkbcommon*.so*" -print -delete || true

cat > "$APPDIR/AppRun" << 'APPRUN_EOF'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "${0}")")"
export LD_LIBRARY_PATH="${HERE}/usr/bin/_internal:${LD_LIBRARY_PATH:-}"
export QT_PLUGIN_PATH="${HERE}/usr/bin/_internal/PySide6/Qt/plugins:${QT_PLUGIN_PATH:-}"
exec "${HERE}/usr/bin/ghostmean" "$@"
APPRUN_EOF
chmod +x "$APPDIR/AppRun"

# --- 4. Fetch appimagetool if we don't already have a good copy ---
mkdir -p "$HERE/build"
need_download=true
if [ -f "$APPIMAGETOOL" ]; then
    # A leftover file from an earlier interrupted run might exist but not
    # be valid/executable -- verify it before trusting it, same as the
    # fresh-download check below.
    if file "$APPIMAGETOOL" 2>/dev/null | grep -q "ELF"; then
        need_download=false
    fi
fi
if [ "$need_download" = true ]; then
    echo "==> Downloading appimagetool..."
    curl -L -o "$APPIMAGETOOL" "$APPIMAGETOOL_URL"
fi

# Always chmod +x regardless of whether this run downloaded it or reused
# an existing file -- a leftover non-executable copy must not skip this.
chmod +x "$APPIMAGETOOL"

# Sanity-check: catch a corrupted/incomplete download with a clear message
# instead of a cryptic "cannot execute binary file" failure later.
if ! file "$APPIMAGETOOL" 2>/dev/null | grep -q "ELF"; then
    echo "ERROR: $APPIMAGETOOL is not a valid ELF binary (corrupted or"
    echo "incomplete download). Delete it and re-run this script:"
    echo "  rm '$APPIMAGETOOL' && ./scripts/build_appimage.sh"
    exit 1
fi

# --- 5. Build the AppImage ---
echo "==> Running appimagetool..."
OUTPUT="$DIST/GhostMEAN-${VERSION}-x86_64.AppImage"
# --appimage-extract-and-run avoids needing FUSE on the build machine
# (containers/CI often don't have it); the resulting AppImage itself does
# not require this flag to run normally on a real desktop.
ARCH=x86_64 "$APPIMAGETOOL" --appimage-extract-and-run "$APPDIR" "$OUTPUT"

echo "==> Done: $OUTPUT"
