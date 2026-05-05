#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

testfile = Path('data/llm-training/test.jsonl')
results = {
    'critical_terms': {'tp':0,'fp':0,'fn':0},
    'dealbreaker': {'tp':0,'fp':0,'fn':0},
    'redline_quality': {'scores':[]}
}

keywords = ['liability','data-sharing','termination','confidentiality','indemnify']

def predict(ex):
    text = ex['agreement_text'].lower()
    pred_terms = [k for k in keywords if k in text]
    pred_deal = any(k in text for k in ['liability','termination'])
    # naive summary: take the provided gold summary but drop every 3rd word to simulate model output
    words = ex['summary'].split()
    pred_summary = ' '.join(w for i,w in enumerate(words) if (i % 3) != 0)
    return {'pred_terms':pred_terms, 'pred_deal':pred_deal, 'pred_summary':pred_summary}


def f1_score(pred_set, gold_set):
    p = len(pred_set & gold_set) / (len(pred_set) or 1)
    r = len(pred_set & gold_set) / (len(gold_set) or 1)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


n = 0
with testfile.open() as f:
    for line in f:
        n += 1
        ex = json.loads(line)
        gold_terms = set(ex['labels'].get('critical_terms', []))
        gold_deal = ex['labels'].get('dealbreaker', False)
        pred = predict(ex)
        pred_terms = set(pred['pred_terms'])
        # count term metrics at term-level
        # TP/FP/FN for terms
        for t in pred_terms:
            if t in gold_terms:
                results['critical_terms']['tp'] += 1
            else:
                results['critical_terms']['fp'] += 1
        for t in gold_terms:
            if t not in pred_terms:
                results['critical_terms']['fn'] += 1
        # dealbreaker
        if pred['pred_deal'] and gold_deal:
            results['dealbreaker']['tp'] += 1
        if pred['pred_deal'] and not gold_deal:
            results['dealbreaker']['fp'] += 1
        if not pred['pred_deal'] and gold_deal:
            results['dealbreaker']['fn'] += 1
        # redline quality: use token-level F1 between pred_summary and gold summary
        ps = set(pred['pred_summary'].split())
        gs = set(ex['summary'].split())
        q = f1_score(ps, gs)
        results['redline_quality']['scores'].append(q)

# aggregate
def precision(tp,fp):
    return tp / (tp+fp) if (tp+fp)>0 else 0.0

def recall(tp,fn):
    return tp / (tp+fn) if (tp+fn)>0 else 0.0

ct = results['critical_terms']
d = results['dealbreaker']
summary_scores = results['redline_quality']['scores']
out = {
    'critical_terms': {
        'precision': precision(ct['tp'], ct['fp']),
        'recall': recall(ct['tp'], ct['fn']),
        'tp': ct['tp'],'fp':ct['fp'],'fn':ct['fn']
    },
    'dealbreaker': {
        'precision': precision(d['tp'], d['fp']),
        'recall': recall(d['tp'], d['fn']),
        'tp': d['tp'],'fp':d['fp'],'fn':d['fn']
    },
    'redline_quality': {
        'mean_f1': sum(summary_scores)/len(summary_scores) if summary_scores else 0.0,
        'count': len(summary_scores)
    }
}

Path('data/llm-training').mkdir(parents=True, exist_ok=True)
with open('data/llm-training/eval.json','w') as f:
    json.dump(out, f, indent=2)
print('wrote data/llm-training/eval.json')
