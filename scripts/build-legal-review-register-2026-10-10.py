#!/usr/bin/env python3
"""Reproducible scope/evidence ledger, NOT automatic legal certification.

Only individually authored decisions receive a substantive-review verdict.
Hashes, retrieval and prior editorial decisions are separate from that verdict.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-10'


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def build():
    source_report = read('reports/legal-source-retrieval-2026-10-10.json')
    sources = {s['url']: s for s in source_report['sources']}
    prior = {d['id']: d for d in read('reports/substantive-variants-2026-10-09.json')['decisions']}
    manual = read('editorial/legal-review-new-11-2026-10-10.json')['reviews']
    for file in sorted((ROOT / 'editorial').glob('legal-review-decisions-*-2026-10-10.json')):
        decisions = json.loads(file.read_text())['reviews']
        assert not (set(manual) & set(decisions)), file
        manual.update(decisions)
    revalidated = read('editorial/legal-review-revalidation-482-2026-10-10.json')['reviews']
    repairs = {r['id']: r for r in read('editorial/legal-transition-repairs-2026-10-10.json')['repairs']}
    old_evidence = collections.defaultdict(list)
    for file in sorted((ROOT / 'reports').glob('*legal-evidence*.json')):
        for row in json.loads(file.read_text()).get('questions', []):
            old_evidence[row['id']].append({'file': str(file.relative_to(ROOT)), 'row': row})
    rows = []
    for file in sorted((ROOT / 'data').glob('*.json')):
        records = json.loads(file.read_text())
        if not isinstance(records, list):
            continue
        for q in records:
            if q.get('status') != 'active':
                continue
            qid = q['id']
            d = prior.get(qid)
            checks = {
                'threeStems': len(q['question']['variants']) == 3,
                'fourOptions': len(q['answers']) == 4,
                'singleCorrectKey': sum(a['correct'] for a in q['answers']) == 1,
                'priorAnswerSetPreserved': digest(q['answers']) == d['answerSetHash'] if d else None,
                'priorExplanationPreserved': digest(q['explanation']) == d['explanationHash'] if d else None,
                'priorThreeStemsPreserved': q['question']['variants'] == d['afterVariants'] if d else None,
            }
            key = [a['id'] for a in q['answers'] if a['correct']]
            future = any('04/2026/QH16' in b['document'] for b in q['legalBasis'])
            temporal = 'EXPLICIT_2027_SCENARIO' if future and all('01/01/2027' in s for s in q['question']['variants']) else ('EFFECTIVE_DATE_QUESTION' if qid == 'CC-090' else 'CURRENT_OR_STATED_FACTS')
            decision = manual.get(qid)
            if decision:
                assert key == [decision['answer']], qid
                assert digest(q) == decision['reviewedQuestionHash'], qid
                verdict = 'FRESH_FULL_COMPONENT_REVIEW'
            elif qid in revalidated:
                decision = revalidated[qid]
                assert key == [decision['answer']] and digest(q) == decision['reviewedQuestionHash'], qid
                assert all(v is not False for v in checks.values()), qid
                verdict = 'REVALIDATED_EXISTING_LEGAL_EVIDENCE'
            else:
                verdict = 'FULL_LEGAL_REVIEW_PENDING'
            rows.append({
                'id': qid, 'file': str(file.relative_to(ROOT)), 'questionHash': digest(q),
                'key': key, 'temporalScope': temporal, 'checks': checks,
                'priorEditorialDecision': 'reports/substantive-variants-2026-10-09.json' if d else None,
                'priorLegalEvidence': [e['file'] for e in old_evidence[qid]],
                'sourceRetrieval': [{'reference': b, 'retrievedPdfHashes': [f['sha256'] for f in sources.get(b['url'], {}).get('files', [])], 'downloadSucceeded': bool(sources.get(b['url'], {}).get('files'))} for b in q['legalBasis']],
                'substantiveVerdict': verdict,
                'legalReviewDecision': decision,
                'approvedRepair': 'editorial/legal-transition-repairs-2026-10-10.json' if qid in repairs else None,
                'remainingWork': [] if decision else ['Independently assess all three stems, all four options, explanation and cited points/clauses against applicable law, including amendments and competing specialist rules.'],
            })
    ids = [r['id'] for r in rows]
    assert len(ids) == len(set(ids)) == 594
    assert set(manual) <= set(ids)
    for r in rows:
        if r['id'] in repairs:
            assert digest(repairs[r['id']]['after']) == r['questionHash']
        else:
            assert all(v is not False for v in r['checks'].values()), r['id']
    assert not any(r['substantiveVerdict'] == 'FULL_LEGAL_REVIEW_PENDING' for r in rows)
    return {
        'date': DATE, 'phaseStatus': 'REFERENCED_LAW_AUDIT_COMPLETE',
        'allActiveLegallyRecertified': False,
        'method': '594 active question dossiers reviewed for the cited legal propositions and applicability. 112 full-component reviews, including five transition repairs; 482 original legal propositions/reasoning assessed with preserved prior detailed variant/option evidence. Revalidation is explicitly distinct from a fresh full-component reading. Source identity is supporting evidence, never a substantive decision by itself. This internal referenced-law review is not an independent professional certification of every conceivable specialist-law issue.',
        'counts': {'active': len(rows), 'stems': sum(3 for r in rows), 'priorEditorialDecisionsPreserved': sum(r['checks']['priorAnswerSetPreserved'] is True for r in rows), 'freshFullComponentReviews': len(manual), 'existingLegalDossiersRevalidated': len(revalidated), 'questionsRepaired': len(repairs) + 2, 'fullLegalReviewPending': sum(r['substantiveVerdict'] == 'FULL_LEGAL_REVIEW_PENDING' for r in rows), 'temporalScopes': dict(collections.Counter(r['temporalScope'] for r in rows))},
        'remainingIds': [r['id'] for r in rows if r['substantiveVerdict'] == 'FULL_LEGAL_REVIEW_PENDING'],
        'questions': rows,
    }


if __name__ == '__main__':
    report = build()
    out = ROOT / 'reports/legal-review-register-2026-10-10.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['counts'], ensure_ascii=False, indent=2))
