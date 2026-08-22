# Troubleshooting

Only things that can actually happen, based on real reports and real
testing — not a generic checklist.

## AppImage doesn't start

1. Make sure it's executable: `chmod +x GhostMEAN-<version>-x86_64.AppImage`.
2. If you get a FUSE-related error, your system may not have FUSE
   installed (common on some minimal/containerized Linux setups). Run it
   with the extraction fallback instead, which doesn't need FUSE:

   ```bash
   ./GhostMEAN-<version>-x86_64.AppImage --appimage-extract-and-run
   ```

3. If you built it yourself and it fails to start with a
   `cannot open shared object file` error mentioning `libpython`, you're
   very likely on an old build — this was a real bug (PyInstaller 6.x
   puts its shared libraries under an `_internal/` subfolder that an
   early version of `AppRun` didn't account for). It's fixed in the
   current `scripts/build_appimage.sh`; rebuild from a fresh checkout.
4. If the build script itself fails with `ModuleNotFoundError: No module
   named 'PIL'` — that was a real undeclared-dependency bug, fixed by
   switching icon resizing to `PySide6.QtGui.QImage` (already a required
   dependency). Update to the latest source if you hit this.

## `ghostmean --version` doesn't work / hangs

It's designed to print the version and exit **before touching Qt at
all**, specifically so it works over SSH or in a container with no
display. If it hangs, you're likely running an older version — the
current one has been verified in a genuinely headless subprocess (no
`QT_QPA_PLATFORM` set, no display).

## CSV rejected

GhostMEAN gives a specific error rather than a generic failure:

- **Empty file** (no panel rows) → a clear "no panel rows" error.
- **Missing file** → a normal file-not-found error.
- **Missing column** (e.g. you deleted `sweep_deg`) → an error naming
  the missing field.
- **Missing metadata comment line** (the `# ghostmean_csv v1; ...`
  header) → not an error — GhostMEAN falls back to `unit=mm` and
  `ac_percent=25.0` and loads the rest normally.

None of these crash the app — they show a dialog and leave your current
geometry untouched. See [CSV Format](CSV-Format) for the exact expected
shape, and `tests/fixtures/test_err.csv` for an example of geometrically
*bad but syntactically valid* data (which loads fine and just produces
warnings — see [Validation & Warnings](Validation)).

## PDF looks wrong

- **Wing looks tiny or absurdly large** — the PDF uses a fixed scale, not
  auto-fit (see [Export PDF](Export-PDF)); a very small or very large
  wing relative to the ~2000mm reference will look correspondingly small
  or maximally shrunk-to-fit. This is intentional.
- **Unexpected step in the trailing edge** — check for a
  `Major ≠ previous panel's Minor` warning; this is very likely a real,
  intentional-per-your-data discontinuity, not a rendering bug — see
  [Panel Geometry](Panel-Geometry).
- **Numbers in the wrong unit** — the PDF uses whichever unit (mm/in)
  the GUI was showing at export time; switch units before exporting if
  you need the other one.
- **Wrong language** — same idea: the PDF is generated in whichever
  interface language was active when you clicked export.

## Qt / display problems (window glitches after maximizing, etc.)

If maximizing the window causes visible corruption that also affects
*other*, unrelated applications afterward (requiring a session or system
restart to clear) — this pattern (seen on MATE/Marco, X11) matches a
known class of X11 issue: the **MIT-SHM** shared-memory extension used
by Qt for rendering can get stuck on a window-state change on certain
driver/compositor combinations, and the corruption can outlive the
triggering app.

As a test, try launching with MIT-SHM disabled:

```bash
QT_XCB_NO_MITSHM=1 ghostmean-gui
```

or with the AppImage:

```bash
QT_XCB_NO_MITSHM=1 ./GhostMEAN-<version>-x86_64.AppImage
```

> This workaround is based on the known behavior of this class of X11
> bug, not on a confirmed fix specific to GhostMEAN — if you try it,
> please report back (via an issue) whether it resolves the problem, so
> this page can be updated with a confirmed answer either way.

## Windows portable build

`scripts/build_portable_windows.ps1` produces a portable folder (not a
single `.exe` — see [Installation](Installation) for why: it matches the
already-verified Linux build's asset-loading behavior). This script has
**not yet been verified on a real Windows machine**. If you run it and
hit an issue — especially the window icon not loading — please open an
issue with the exact error; it's very likely fixable the same way the
AppImage script's real bugs were (see the AppImage section above), just
needs a real Windows report to diagnose against.
