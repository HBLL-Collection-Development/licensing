#!/usr/bin/env bash
set -euo pipefail
# Build script for Linux using PyInstaller. Run from project root: ./scripts/build_linux.sh
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENTRY_PY="$PROJECT_ROOT/src/exporter/exporter.py"
DIST_DIR="$PROJECT_ROOT/dist"
mkdir -p "$DIST_DIR"

echo "Installing PyInstaller..."
python3 -m pip install --upgrade pyinstaller --user || true

echo "Running PyInstaller (Linux)..."
pyinstaller --onefile --name library-installer "$ENTRY_PY" --distpath "$DIST_DIR" || {
  echo "PyInstaller failed or not available. See instructions in the script header." >&2
  exit 1
}

echo "Build complete. Artifacts in: $DIST_DIR"
