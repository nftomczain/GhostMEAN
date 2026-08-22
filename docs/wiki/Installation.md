# Installation

## Linux — AppImage (recommended, no Python needed)

1. Download `GhostMEAN-<version>-x86_64.AppImage` from the
   [Releases page](https://github.com/nftomczain/GhostMEAN/releases).
2. Make it executable and run it:

   ```bash
   chmod +x GhostMEAN-<version>-x86_64.AppImage
   ./GhostMEAN-<version>-x86_64.AppImage
   ```

That's it — no install, no Python, no Qt needed on your machine. If it
doesn't start, see **[Troubleshooting](Troubleshooting)**.

### Building the AppImage yourself

```bash
git clone https://github.com/nftomczain/GhostMEAN.git
cd GhostMEAN
./scripts/build_appimage.sh
./dist/GhostMEAN-<version>-x86_64.AppImage
```

This has been verified to work from a genuinely clean checkout — no
`pip install` step needed first. The script installs `pyinstaller`
itself if it's missing, and downloads `appimagetool` on the first run
(cached afterwards in `build/appimagetool.AppImage`).

## Windows — portable build

```powershell
.\scripts\build_portable_windows.ps1
```

Produces a folder `dist\GhostMEAN-<version>\` — copy the whole folder
anywhere (USB stick, another PC) and run the `.exe` inside. No installer,
no registry entries.

> **Note:** this script has not yet been verified on a real Windows
> machine (GhostMEAN is developed in a Linux-only environment, and
> PyInstaller doesn't cross-compile). If you try it, please report back
> what happens — see **[Troubleshooting](Troubleshooting)**.

## Running from source (any platform)

```bash
git clone https://github.com/nftomczain/GhostMEAN.git
cd GhostMEAN
pip install -e .
ghostmean-gui
```

or without installing the package at all:

```bash
pip install PySide6
python -m ghostmean
```

Check your version at any time (works even without a display):

```bash
ghostmean --version
```

## Running the test suite

```bash
pip install -e .[test]
pytest
```

97 tests covering geometry, the CSV format, GUI validation, PDF/drawing,
and all 6 languages. See the fixture files under `tests/fixtures/` if
you want to see exactly what "good" and "deliberately broken" input
looks like.
