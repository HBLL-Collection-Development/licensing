#!/usr/bin/env bash
set -euo pipefail
# Attempt Playwright installation using existing environment tools.
# Use uv run if available, otherwise fall back to python -m playwright
if command -v uv >/dev/null 2>&1; then
  uv run playwright install --with-deps || true
fi
python3 -m playwright install --with-deps || true

echo "Playwright browsers install attempted. Check output above for errors."