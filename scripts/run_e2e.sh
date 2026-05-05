#!/usr/bin/env bash
set -euo pipefail
# Run end-to-end tests (Playwright + pytest) after browsers are installed
echo "Running full test suite including e2e..."
PYTHONPATH=. uv run pytest -q tests/e2e -q || exit 1
