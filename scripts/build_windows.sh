#!/usr/bin/env bash
set -euo pipefail
# Build script for Windows. Recommended: run on Windows with Python and PyInstaller.
# On macOS/Linux you may be able to cross-build using wine/pyinstaller-windows, but that is outside this script's scope.
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENTRY_PY="$PROJECT_ROOT/src/exporter/exporter.py"
DIST_DIR="$PROJECT_ROOT/dist"
mkdir -p "$DIST_DIR"

if [[ "$(uname -s)" != *"NT"* && "$(uname -s)" != "MINGW" && "$(uname -s)" != "CYGWIN" ]]; then
  echo "Not running on Windows. Cross-building Windows executables is not supported in this script. Run on Windows." >&2
  exit 1
fi

python -m pip install --upgrade pyinstaller || true
pyinstaller --onefile --name library-installer.exe "$ENTRY_PY" --distpath "$DIST_DIR"

echo "Build complete. Artifacts in: $DIST_DIR"