#!/usr/bin/env python3
"""Apply individually authored editorial rows, preserving evidence and answer keys.

This validates structure and evidence linkage, not substantive law. Editorial
decisions and public-source checks precede this script; nothing is auto-READY.
"""
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-09'
GROUPS = [
    ('derived', 'derived-questions.json', 'pending-review-legal-evidence-2026.json'),
    ('validated', 'validated-2026.json', 'legal-evidence-2026.json'),
    ('core', 'questions.json', 'core-legal-evidence-2026-10-07.json'),
    ('deposit', 'imported-deposit-2026.json', 'deposit-legal-evidence-2026.json'),
    ('authorization', 'imported-authorization-2026.json', 'authorization-legal-evidence-2026.json'),
]

def read(path):
    return json.loads((ROOT / path).read_text())

def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def norm(text):
    return re.sub(r'\W+', ' ', text.casefold()).strip()

report_path = 'reports/substantive-variants-2026-10-09.json'
previous = read(report_path) if (ROOT / report_path).exists() else {'decisions': []}
prior = {row['id']: row for row in previous['decisions']}
decisions = []
pending_writes = []

for group, filename, evidence_file in GROUPS:
    bank = read('data/' + filename)
    additions = read(f'editorial/{group}-variants-{DATE}.json')
    evidence = read('reports/' + evidence_file)
    proofs = {q['id']: q for q in evidence['questions']}
    assert set(additions) == {q['id'] for q in bank if q['status'] == 'active'}, group
    for q in bank:
        if q['id'] not in additions:
            continue
        before = prior.get(q['id'], {}).get('before', copy.deepcopy(q))
        proof = proofs[q['id']]
        assert [p['reference'] for p in proof['provisions']] == q['legalBasis'], q['id']
        correct = [a['id'] for a in q['answers'] if a['correct']]
        if 'answer' in proof:
            expected = proof['answer'] if isinstance(proof['answer'], list) else [proof['answer']]
        else:
            # Independently checked keys in the dated editorial worksheet,
            # rather than accepting whatever the loaded answer array marks.
            reviewed_keys = read(f'editorial/{group}-answer-review-2026-10-09.json')
            expected = [reviewed_keys[q['id']]]
        assert len(correct) == 1 and correct == expected, q['id']
        assert len(q['answers']) == 4 and len(additions[q['id']]) == 2, q['id']
        original = before['question']['variants'][0]
        original_changed = False
        if q['id'] == 'CC-034':
            original = 'Từ 01/01/2027, công chứng viên đã từng hành nghề nhưng không đang hành nghề tại thời điểm xem xét miễn nhiệm. Chỉ xét nhánh thẩm quyền cho người đã từng hành nghề, thẩm quyền thuộc tỉnh nào?'
            original_changed = True
            # A never-practised appointee belongs to a different statutory branch.
            additions[q['id']] = [
                'Công chứng viên đã từng hành nghề, hiện không hành nghề khi xem xét miễn nhiệm. Tỉnh có thẩm quyền được xác định theo địa điểm nào?',
                additions[q['id']][1],
            ]
        prefix = ('Từ 01/01/2027: ' if '04/2026/QH16' in json.dumps(q['legalBasis'])
                  and q['id'] != 'CC-090' else 'Tháng 10/2026: ')
        if q['id'] == 'CC-090':
            prefix = ''  # Do not reveal the date being tested in the stem.
        variants = [original] + [v if v.startswith(('Tháng 10/2026:', 'Từ 01/01/2027:'))
                                 else prefix + v for v in additions[q['id']]]
        assert len({norm(v) for v in variants}) == 3, q['id']
        q['question']['variants'] = variants
        q.setdefault('audit', {}).update({
            'variantReviewDate': DATE,
            'variantReviewStatus': 'substantive_editorial_review',
            'variantEvidenceReport': report_path,
            'legalReviewStatus': 'referenced_provisions_reviewed_not_global_certification',
        })
        decisions.append({
            'id': q['id'], 'file': 'data/' + filename,
            'reviewedAt': DATE, 'applicableAt': '2027-01-01' if prefix.startswith('Từ') else DATE,
            'status': 'EDITORIALLY_REVIEWED_WITH_REFERENCED_PROVISIONS',
            'globalLegalCertification': False,
            'evidenceFile': 'reports/' + evidence_file,
            'evidenceQuestionId': q['id'], 'legalBasis': q['legalBasis'],
            'answerKey': correct[0],
            'answerSetHash': digest(q['answers']),
            'explanationHash': digest(q['explanation']),
            'reviewConclusion': q['explanation'],
            'variantChecks': [{'index': i, 'answer': correct[0],
                               'review': 'same_legal_conclusion_under_stated_assumptions'}
                              for i in range(3)],
            'originalChanged': original_changed,
            'originalChangeReason': ('Separate previously practising CCV from never-practised appointee; '
                                    'Article 16(3) as amended has distinct jurisdiction branches.'
                                    if original_changed else None),
            'before': before, 'afterVariants': variants,
        })
    pending_writes.append(('data/' + filename, bank))

bank_all = []
replacements = dict(pending_writes)
for path in sorted((ROOT / 'data').glob('*.json')):
    value = replacements.get('data/' + path.name, read('data/' + path.name))
    if isinstance(value, list) and value and isinstance(value[0], dict) and 'answers' in value[0]:
        bank_all.extend(value)
assert len({q['id'] for q in bank_all}) == len(bank_all)
active = [q for q in bank_all if q['status'] in ('active', 'verified')]
seen = {}
for q in active:
    for variant in q['question']['variants']:
        key = norm(variant)
        assert key not in seen, (q['id'], seen.get(key))
        seen[key] = q['id']
initial = read('editorial/variant-plan-2026-10-09.json')
done = {q['id'] for q in decisions}
remaining = [qid for qid in initial['scopeIds'] if qid not in done]
report = {'date': DATE, 'phaseStatus': 'INCOMPLETE', 'initialScope': len(initial['scopeIds']),
          'editoriallyReviewedQuestions': len(done), 'remainingQuestions': len(remaining),
          'newlyAuthoredVariants': len(done)*2, 'activeCount': len(active),
          'activeVariantStrings': sum(len(q['question']['variants']) for q in active),
          'allActiveLegallyRecertified': False, 'remainingIds': remaining, 'decisions': decisions}
for path, value in pending_writes:
    write(path, value)
write(report_path, report)
print(json.dumps({k:v for k,v in report.items() if k not in ('remainingIds', 'decisions')}, ensure_ascii=False))
