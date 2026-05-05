#!/usr/bin/env bash
set -euo pipefail
# Convert data/llm-training/train.jsonl into OpenAI fine-tune JSONL format
IN=data/llm-training/train.jsonl
OUT=data/llm-training/openai_finetune.jsonl
python3 - <<'PY'
import json
from pathlib import Path
inpath = Path('data/llm-training/train.jsonl')
outpath = Path('data/llm-training/openai_finetune.jsonl')
with inpath.open() as inf, outpath.open('w') as outf:
    for line in inf:
        ex = json.loads(line)
        prompt = f"Summarize the agreement and list critical terms.\n\nAgreement:\n{ex['agreement_text']}\n\nSummary:\n"
        # completion should start with space per OpenAI format
        completion = ex['summary'] + "\n\nLabels: " + json.dumps(ex['labels']) + "\n"
        obj = {'prompt': prompt, 'completion': ' ' + completion}
        outf.write(json.dumps(obj) + '\n')
print('wrote', outpath)
PY
