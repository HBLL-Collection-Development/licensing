#!/usr/bin/env python3
import os
import random
import json
from datetime import date

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
except ImportError:
    raise SystemExit('reportlab is required')

OUT_DIR = os.path.join(os.getcwd(), 'data', 'sample-agreements')
os.makedirs(OUT_DIR, exist_ok=True)

parties = [
    ('Alpha Corp', 'Beta LLC'),
    ('Gamma University', 'Delta Foundation'),
    ('City Library', 'Open Source Initiative'),
    ('Publisher A', 'Distributor B'),
    ('Lender X', 'Borrower Y'),
]

license_templates = [
    {
        'title': 'Standard License Agreement',
        'clauses': [
            ('Grant of License', 'Licensor grants Licensee a non-exclusive, worldwide license to use the Work.'),
            ('Term', 'This Agreement begins on the Effective Date and continues for five (5) years.'),
            ('Restrictions', 'Licensee shall not distribute or sublicense the Work without prior written consent.'),
            ('Governing Law', 'This Agreement is governed by the laws of the State of New York.')
        ]
    },
    {
        'title': 'Open Use License',
        'clauses': [
            ('License', 'Licensor grants a royalty-free, perpetual license to use, reproduce, and display the Work.'),
            ('Attribution', 'Attribution to the Licensor is required in all redistributions.'),
            ('Warranties', 'The Work is provided "as is" without warranties.'),
            ('Termination', 'Breach of the terms results in automatic termination of the license.')
        ]
    },
    {
        'title': 'Restricted License',
        'clauses': [
            ('Scope', 'Licensee may use the Work for internal research only.'),
            ('Prohibitions', 'No commercial use is allowed.'),
            ('Confidentiality', 'Certain sections of the Work are confidential and must be redacted.'),
            ('Dispute Resolution', 'Arbitration in San Francisco governs disputes.')
        ]
    },
]

# Variation helper
def make_agreement(idx):
    tpl = random.choice(license_templates)
    party = random.choice(parties)
    title = f"{tpl['title']} – Sample {idx:02d}"
    effective = date(2015 + (idx % 10), random.randint(1,12), random.randint(1,28)).isoformat()
    clauses = list(tpl['clauses'])

    # add or remove clauses to vary structure
    if random.random() < 0.3:
        clauses.append(('Indemnity', 'Licensee shall indemnify Licensor against claims arising from use.'))
    if random.random() < 0.2 and clauses:
        clauses.pop(random.randrange(len(clauses)))

    return {
        'title': title,
        'parties': {'licensor': party[0], 'licensee': party[1]},
        'effective_date': effective,
        'clauses': clauses,
        'notes': 'Auto-generated sample for testing.'
    }


def render_pdf(text_lines, path, scanned=False):
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER
    y = height - 1*inch
    if scanned:
        c.setFont('Helvetica-Bold', 20)
        c.drawString(1*inch, y, 'SCANNED IMAGE (simulated)')
        y -= 0.5*inch
    c.setFont('Helvetica', 12)
    for line in text_lines:
        if y < 1*inch:
            c.showPage()
            y = height - 1*inch
            c.setFont('Helvetica', 12)
        c.drawString(1*inch, y, line)
        y -= 0.25*inch
    c.save()


MANIFEST = []

for i in range(1, 21):
    sample = make_agreement(i)
    # create a variety of file names
    kind = 'scanned' if random.random() < 0.35 else 'text'
    base = f"sample-{i:02d}-{kind}"
    pdf_path = os.path.join(OUT_DIR, f"{base}.pdf")

    # prepare text lines
    lines = [sample['title'], '']
    lines.append(f"Effective Date: {sample['effective_date']}")
    lines.append(f"Parties: {sample['parties']['licensor']} (Licensor) and {sample['parties']['licensee']} (Licensee)")
    lines.append('')
    for clause_title, clause_text in sample['clauses']:
        lines.append(clause_title + ':')
        # wrap clause text roughly
        for j in range(0, len(clause_text), 80):
            lines.append(clause_text[j:j+80])
        lines.append('')

    # render PDF
    try:
        render_pdf(lines, pdf_path, scanned=(kind=='scanned'))
    except Exception as e:
        print('Failed to render PDF:', e)
        continue

    # write JSON license_summary_form-like
    summary = {
        'file_name': os.path.basename(pdf_path),
        'title': sample['title'],
        'licensor': sample['parties']['licensor'],
        'licensee': sample['parties']['licensee'],
        'effective_date': sample['effective_date'],
        'clause_count': len(sample['clauses']),
        'clauses': [{'name': t, 'text': s} for t, s in sample['clauses']],
        'scanned_pdf': (kind=='scanned')
    }
    json_path = os.path.join(OUT_DIR, f"license_summary_{i:02d}.json")
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(summary, jf, indent=2)

    size = os.path.getsize(pdf_path)
    MANIFEST.append((os.path.basename(pdf_path), size))

# write LICENSE
license_text = '''Sample Agreements Dataset License

This dataset of sample agreements was created for research and testing purposes.
You may use, modify, and distribute the files for non-commercial research, testing,
and academic purposes only, provided that you retain this notice and give
attribution to the creators.

DO NOT use these samples for legal advice or to make legal decisions.
Some samples are synthetic and may not reflect real legal agreements.
'''
with open(os.path.join(OUT_DIR, 'LICENSE'), 'w', encoding='utf-8') as lf:
    lf.write(license_text)

# write manifest
with open(os.path.join(OUT_DIR, 'manifest.json'), 'w', encoding='utf-8') as mf:
    json.dump({'samples': [{'file': f, 'size': s} for f, s in MANIFEST]}, mf, indent=2)

print('Generated', len(MANIFEST), 'sample PDFs in', OUT_DIR)
