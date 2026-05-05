#!/usr/bin/env bash
set -euo pipefail
# Run exporter with project src on PYTHONPATH
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHONPATH="$REPO_ROOT/src"
PYTHONPATH="$PYTHONPATH" python3 -m exporter "$@"
