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
    ('family', 'imported-family-2026.json', 'family-legal-evidence-2026.json'),
    ('inheritance', 'imported-inheritance-2026.json', 'inheritance-legal-evidence-2026.json'),
    ('refinement', 'refinement-2026.json', 'refinement-legal-evidence-2026.json'),
    ('completion', 'completion-2026.json', 'completion-legal-evidence-2026.json'),
    ('exams', 'imported-exams-2026.json', 'exam-legal-evidence-2026.json'),
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
worksheets = [
    ('editorial/variant-batch-40-2026-10-09.json', 40),
    ('editorial/variant-batch-60-2026-10-09.json', 60),
    ('editorial/variant-batch-100-2026-10-09.json', 100),
    ('editorial/variant-batch-next-100-2026-10-09.json', 100),
]
batch_reviews = {}
batch_keys = {}
worksheet_by_id = {}
for worksheet, size in worksheets:
    review = read(worksheet)
    assert len(review['reviews']) == size, worksheet
    assert not (set(review['reviews']) & set(batch_reviews)), worksheet
    batch_reviews.update(review['reviews'])
    if 'answerKeys' in review:
        assert set(review['answerKeys']) == set(review['reviews']), worksheet
        batch_keys.update(review['answerKeys'])
    worksheet_by_id.update({qid: worksheet for qid in review['reviews']})
batch_scope = set(batch_reviews)
next_scope = read('editorial/variant-batch-next-100-scope-2026-10-09.json')
next_review = read('editorial/variant-batch-next-100-2026-10-09.json')
next_ids = set(next_scope['ids'])
assert len(next_scope['ids']) == len(next_ids) == 100
assert next_ids == set(next_review['reviews']) == set(next_review['answerKeys'])
assert next_ids <= set(previous['remainingIds']) | set(prior)
assert len([qid for qid in next_ids if qid.startswith('INH26-')]) == 17
assert len([qid for qid in next_ids if qid.startswith('IMP-')]) == 83
assert 'IMP-T60-038' not in next_ids and 'IMP-T60-096' in next_ids
deferred_ids = {row['id'] for row in read('editorial/variant-next-100-follow-up-2026-10-09.json')['items']}
assert len(deferred_ids) == 5 and not (deferred_ids & next_ids)
registry = read('reports/refinement-provisions-2026.json')
decisions = []
pending_writes = []

for group, filename, evidence_file in GROUPS:
    bank = read('data/' + filename)
    additions = read(f'editorial/{group}-variants-{DATE}.json')
    evidence = read('reports/' + evidence_file)
    proofs = {q['id']: q for q in evidence['questions']}
    active_ids = {q['id'] for q in bank if q['status'] == 'active'}
    expected_ids = active_ids & batch_scope if group in ('family', 'inheritance', 'refinement', 'exams') else active_ids
    assert set(additions) == expected_ids, group
    if group in ('family', 'inheritance'):
        assert len(additions) == (26 if group == 'family' else 32), group
    if group == 'refinement':
        assert len(additions) == 80, group
    if group == 'exams':
        assert len(additions) == 83, group
    for q in bank:
        if q['id'] not in additions:
            continue
        current_before = copy.deepcopy(q)
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
        if q['id'] in batch_keys:
            assert correct == [batch_keys[q['id']]], q['id']
        if group == 'refinement':
            for p in proof['provisions']:
                ref = p['evidenceRef']
                document = registry['documents'][ref['documentCode']]
                article = registry['articles'][ref['documentCode']][ref['article']]
                assert len(article) > 100 and f"Điều {ref['article']}." in article, q['id']
                assert document['title'] == p['reference']['document'], q['id']
                assert document['url'] == p['reference']['url'], q['id']
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
        # Compare the full loaded record, not only the key/answer array. A dated
        # variants-only continuation must never change the original or metadata.
        if q['id'] in next_ids:
            restored = copy.deepcopy(q)
            restored['question']['variants'] = current_before['question']['variants']
            if 'audit' in current_before:
                restored['audit'] = current_before['audit']
            else:
                restored.pop('audit', None)
            assert restored == current_before, q['id']
            assert original == current_before['question']['variants'][0], q['id']
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
        if q['id'] in batch_scope:
            decisions[-1].update({
                'editorialReasoning': batch_reviews[q['id']],
                'editorialWorksheet': worksheet_by_id[q['id']],
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
assert batch_scope <= done
report['batches'] = [
    {'id': {
        'editorial/variant-batch-40-2026-10-09.json': 'family-inheritance-40-2026-10-09',
        'editorial/variant-batch-60-2026-10-09.json': 'refinement-60-2026-10-09',
        'editorial/variant-batch-100-2026-10-09.json': 'completion-refinement-inheritance-100-2026-10-09',
        'editorial/variant-batch-next-100-2026-10-09.json': 'inheritance-exams-next-100-2026-10-09',
    }[worksheet],
     'questions': size, 'authoredVariants': size * 2,
     'ids': sorted(read(worksheet)['reviews']), 'worksheet': worksheet}
    for worksheet, size in worksheets
]
report['latestBatch'] = report['batches'][-1]
assert (len(done), len(remaining), len(active)) == (543, 40, 594)
assert report['activeVariantStrings'] == 1702
for path, value in pending_writes:
    write(path, value)
write(report_path, report)
print(json.dumps({k:v for k,v in report.items() if k not in ('remainingIds', 'decisions')}, ensure_ascii=False))
