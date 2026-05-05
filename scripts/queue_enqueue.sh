#!/usr/bin/env bash
# Usage: ./scripts/queue_enqueue.sh /path/to/file
if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/input_file"
  exit 1
fi
python - <<PY
from src.queue import db
jid = db.enqueue(r"$1")
print(jid)
PY
