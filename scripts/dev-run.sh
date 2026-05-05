#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# Start backend
echo "Starting backend (FastAPI) on http://127.0.0.1:8000"
python3 -m uvicorn src.ui.backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend (Vite)"
cd "$ROOT_DIR/src/ui/frontend"
# Install dependencies if node_modules missing
if [ ! -d node_modules ]; then
  npm install --no-audit --no-fund
fi
npm run dev

# On exit, kill backend
trap "kill $BACKEND_PID" EXIT
