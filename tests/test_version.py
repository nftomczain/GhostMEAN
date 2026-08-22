"""
--version tests: the version string must come from exactly one place
(ghostmean/__init__.py) and be reachable without touching Qt at all, so
it works in headless/no-display environments too.
"""

import subprocess
import sys

from ghostmean import __version__


def test_version_string_is_nonempty_and_dotted():
    assert __version__
    parts = __version__.split(".")
    assert len(parts) >= 2
    assert all(p.isdigit() for p in parts)


def test_pyproject_toml_version_matches_package(tmp_path):
    """Guards against the exact mismatch bug seen during development
    (v0.4.8 shown when 0.4.10 was current) -- pyproject.toml's version
    must always equal ghostmean.__version__."""
    import re
    from pathlib import Path
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    text = pyproject.read_text()
    match = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)
    assert match is not None
    assert match.group(1) == __version__


def test_cli_version_flag_prints_and_exits_zero_without_display():
    """Runs `python -m ghostmean --version` as a real subprocess with NO
    QT_QPA_PLATFORM set and no display -- if --version touched Qt before
    checking sys.argv, this would hang or fail in a true headless
    environment (SSH session, CI runner)."""
    result = subprocess.run(
        [sys.executable, "-m", "ghostmean", "--version"],
        capture_output=True, text=True, timeout=10,
        env={"PATH": "/usr/bin:/bin"},  # deliberately no QT_QPA_PLATFORM
    )
    assert result.returncode == 0
    assert __version__ in result.stdout
    assert "GhostMEAN" in result.stdout
