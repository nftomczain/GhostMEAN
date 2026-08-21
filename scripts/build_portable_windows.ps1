# Build a portable Windows folder for GhostMEAN (no installer needed).
#
# Usage (run ON Windows, in PowerShell, from the project root):
#   .\scripts\build_portable_windows.ps1
# Output: dist\GhostMEAN-<version>\GhostMEAN-<version>.exe
#   (copy the whole GhostMEAN-<version> folder anywhere -- USB stick,
#   another PC, etc. -- and run the .exe inside; no install, no registry
#   entries, no Python/Qt needed on the target machine)
#
# IMPORTANT -- NOT TESTED ON REAL WINDOWS:
# PyInstaller does not cross-compile: this script MUST be run on an actual
# Windows machine (or a Windows CI runner). The GhostMEAN development
# sandbox is Linux-only, so unlike scripts/build_appimage.sh (built and
# run repeatedly, including hostile-scenario tests), this script has only
# been reviewed, not executed. Please run it and report back what
# happens -- especially whether the window icon loads correctly, since
# that depends on how PyInstaller resolves Path(__file__) at runtime,
# which differs from the already-verified Linux --onedir build.
#
# Uses --onedir (a folder), not --onefile (a single .exe), on purpose:
# --onedir starts faster, is less likely to trigger antivirus false
# positives, and its asset-loading behaviour matches the Linux AppImage
# build this script was modelled on (same icon-loading code path already
# verified there). If you specifically want a single .exe and are willing
# to debug an icon-loading issue yourself, swap --onedir for --onefile
# below and re-test.

$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Here

$Version = (python -c "import ghostmean; print(ghostmean.__version__)").Trim()
Write-Host "==> GhostMEAN portable Windows build -- v$Version"
Write-Host "    (this script has not been run on real Windows -- please report results)"

# --- 1. Make sure PyInstaller is available ---
python -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    pyinstaller not found, installing..."
    pip install pyinstaller -q
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: 'pip install pyinstaller' failed. Install it manually and re-run:"
        Write-Host "  pip install pyinstaller"
        exit 1
    }
}

# --- 2. Clean previous build output ---
$DistName = "GhostMEAN-$Version"
Remove-Item -Recurse -Force "$Here\build\$DistName", "$Here\dist\$DistName" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "$Here\dist" | Out-Null

# --- 3. Build the portable folder ---
# --windowed: no console window behind the GUI.
# --add-data "SRC;DEST": Windows uses a semicolon separator (Linux/macOS
#   use a colon) -- this script is Windows-only, so semicolon is correct.
pyinstaller `
    --onedir `
    --windowed `
    --name $DistName `
    --add-data "ghostmean/assets;ghostmean/assets" `
    --distpath "$Here\dist" `
    --workpath "$Here\build" `
    --noconfirm `
    ghostmean/__main__.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller failed (see output above)."
    exit 1
}

$OutputExe = "$Here\dist\$DistName\$DistName.exe"
if (Test-Path $OutputExe) {
    Write-Host "==> Done: $OutputExe"
    Write-Host "    Copy the whole '$DistName' folder anywhere and run the .exe inside."
} else {
    Write-Host "WARNING: build finished but $OutputExe was not found -- check dist\$DistName\ for the actual .exe name."
}
