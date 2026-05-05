#!/usr/bin/env python3
import json
import random
from pathlib import Path

OUT_DIR = Path('data/llm-training')
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOTAL = 900
TRAIN = 700
VAL = 100
TEST = TOTAL - TRAIN - VAL

critical_keywords = ['liability', 'data-sharing', 'termination', 'confidentiality', 'indemnify']

def make_example(i):
    agreement_text = f"Agreement sample {i}: This contract includes standard clauses."
    # inject keywords probabilistically
    labels = {"critical_terms": [], "dealbreaker": False}
    # every 15th is liability/dealbreaker
    if i % 15 == 0:
        agreement_text += " The vendor accepts liability for breaches."
        labels['critical_terms'].append('liability')
        labels['dealbreaker'] = True
    if i % 10 == 0:
        agreement_text += " This contract contains data-sharing provisions."
        labels['critical_terms'].append('data-sharing')
    if i % 23 == 0:
        agreement_text += " The agreement has strict confidentiality terms."
        labels['critical_terms'].append('confidentiality')
    if i % 37 == 0:
        agreement_text += " The agreement allows termination for convenience."
        labels['critical_terms'].append('termination')
        labels['dealbreaker'] = True
    summary = f"Summary of agreement {i}: key points captured."
    return {
        'id': f'ex-{i:04d}',
        'agreement_text': agreement_text,
        'summary': summary,
        'labels': labels,
        'provenance': {'source': 'sample-data or synthetic', 'generated_by': 'generate_dataset.py'}
    }


def write_split(start, end, path):
    with open(path, 'w') as f:
        for i in range(start, end):
            ex = make_example(i)
            f.write(json.dumps(ex) + '\n')

if __name__ == '__main__':
    # train: 0..TRAIN-1, val: TRAIN..TRAIN+VAL-1, test: remaining
    write_split(0, TRAIN, OUT_DIR / 'train.jsonl')
    write_split(TRAIN, TRAIN+VAL, OUT_DIR / 'val.jsonl')
    write_split(TRAIN+VAL, TOTAL, OUT_DIR / 'test.jsonl')
    # also write a small metadata file
    metadata = {
        'license': 'CC-BY-4.0',
        'provenance': 'Generated from sample-data and synthetic augmentation by scripts/generate_dataset.py',
        'total_examples': TOTAL,
        'splits': {'train': TRAIN, 'val': VAL, 'test': TEST}
    }
    with open(OUT_DIR / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print('wrote dataset', TOTAL)
