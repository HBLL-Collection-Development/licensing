#!/usr/bin/env python3
import os
import json
import random
from datetime import date

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

# Minimal PDF writer for one-page text PDFs using Type1 fonts

def write_simple_pdf(path, lines, scanned=False):
    # Build content stream
    content_lines = ['BT', '/F1 12 Tf', '72 720 Td']
    for line in lines:
        # escape parentheses
        esc = line.replace('(', '\(').replace(')', '\)')
        content_lines.append('({}) Tj'.format(esc))
        content_lines.append('0 -14 Td')
    content_lines.append('ET')
    content = '\n'.join(content_lines) + '\n'
    # PDF objects
    objs = []
    # 1 Catalog
    objs.append(('1 0 obj', f'<< /Type /Catalog /Pages 2 0 R >>'))
    # 2 Pages
    objs.append(('2 0 obj', f'<< /Type /Pages /Kids [3 0 R] /Count 1 >>'))
    # 3 Page
    # Contents will be object 5
    objs.append(('3 0 obj', '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>'))
    # 4 Font
    objs.append(('4 0 obj', '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>'))
    # 5 Contents stream placeholder
    content_bytes = content.encode('utf-8')
    objs.append(('5 0 obj', f'<< /Length {len(content_bytes)} >>\nstream\n{content}\nendstream'))

    # assemble
    pdf_parts = ['%PDF-1.1']
    xref = []
    offset = 0
    # write objects and record offsets
    for idx, (hdr, body) in enumerate(objs):
        xref.append(offset)
        part = f"{hdr} \n{body} \nendobj\n"
        pdf_parts.append(part)
        offset += len(part.encode('utf-8'))
    # xref table
    xref_start = sum(len(p.encode('utf-8')) for p in pdf_parts)
    pdf_parts.append('xref\n0 {0}\n0000000000 65535 f \n'.format(len(objs)+1))
    for off in xref:
        pdf_parts.append(f"{off:010d} 00000 n \n")
    trailer = f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n"
    pdf_parts.append(trailer)
    # write file
    with open(path, 'wb') as f:
        for p in pdf_parts:
            if isinstance(p, str):
                f.write(p.encode('utf-8'))
            else:
                f.write(p)


MANIFEST = []

for i in range(1, 21):
    tpl = random.choice(license_templates)
    party = random.choice(parties)
    title = f"{tpl['title']} – Sample {i:02d}"
    effective = date(2015 + (i % 10), random.randint(1,12), random.randint(1,28)).isoformat()
    clauses = list(tpl['clauses'])
    if random.random() < 0.3:
        clauses.append(('Indemnity', 'Licensee shall indemnify Licensor against claims arising from use.'))
    if random.random() < 0.2 and clauses:
        clauses.pop(random.randrange(len(clauses)))

    kind = 'scanned' if random.random() < 0.35 else 'text'
    base = f"sample-{i:02d}-{kind}"
    pdf_path = os.path.join(OUT_DIR, f"{base}.pdf")

    lines = [title, '']
    lines.append(f"Effective Date: {effective}")
    lines.append(f"Parties: {party[0]} (Licensor) and {party[1]} (Licensee)")
    lines.append('')
    for clause_title, clause_text in clauses:
        lines.append(clause_title + ':')
        for j in range(0, len(clause_text), 80):
            lines.append(clause_text[j:j+80])
        lines.append('')

    write_simple_pdf(pdf_path, lines, scanned=(kind=='scanned'))

    summary = {
        'file_name': os.path.basename(pdf_path),
        'title': title,
        'licensor': party[0],
        'licensee': party[1],
        'effective_date': effective,
        'clause_count': len(clauses),
        'clauses': [{'name': t, 'text': s} for t, s in clauses],
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

with open(os.path.join(OUT_DIR, 'manifest.json'), 'w', encoding='utf-8') as mf:
    json.dump({'samples': [{'file': f, 'size': s} for f, s in MANIFEST]}, mf, indent=2)

print('Generated', len(MANIFEST), 'sample PDFs in', OUT_DIR)
