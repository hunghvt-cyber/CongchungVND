#!/usr/bin/env python3
"""Inventory and triage. Heuristics flag review candidates, never certify law."""
import collections, difflib, hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = ['questions.json', 'derived-questions.json'] + [f'expansion-2026-batch-{i:02}.json' for i in range(1, 6)]
FILES += [p.name for p in sorted((ROOT/'data').glob('validated-*.json'))]
FILES += [p.name for p in sorted((ROOT/'data').glob('imported-*.json'))]
PREFIXES = [
 'Chọn phương án đúng theo quy định pháp luật: ',
 'Trong quá trình xử lý hồ sơ, cần xác định đúng vấn đề sau: ',
 'Người tập sự được yêu cầu giải quyết câu hỏi sau. Phương án nào đúng? ',
 'Để tránh áp dụng sai quy định, hãy chọn đáp án đúng: ',
 'Xét theo căn cứ pháp lý được viện dẫn, phương án nào chính xác? ',
]
def norm(s):
 for prefix in PREFIXES:
  if s.startswith(prefix): s=s[len(prefix):]
 return re.sub(r'\W+', ' ', s.casefold()).strip()
def groups(items, key):
 out=collections.defaultdict(list)
 for q in items: out[key(q)].append(q['id'])
 return [v for v in out.values() if len(v)>1]
def count(items,key): return dict(sorted(collections.Counter(str(q.get(key,'unclassified')) for q in items).items()))
def audit():
 bank=[]; counts={}; hashes={}; findings=[]
 for f in FILES:
  p=ROOT/'data'/f; raw=p.read_bytes(); a=json.loads(raw); counts[f]=len(a); hashes[f]=hashlib.sha256(raw).hexdigest(); bank.extend(a)
 source=json.loads((ROOT/'data/question-sources.json').read_text())
 sources={s['id']:s for s in source['sources']}
 for q in bank:
  flags=[]; answers=q.get('answers',[]); variants=q.get('question',{}).get('variants',[])
  if not variants or any(not isinstance(s,str) or not s.strip() for s in variants):flags.append('invalid_stem')
  if len(set(a['id'] for a in answers))!=len(answers):flags.append('duplicate_answer_id')
  if q.get('type')=='single' and sum(a.get('correct') is True for a in answers)!=1:flags.append('invalid_single_key')
  if len(answers)!=4:flags.append('not_four_answers')
  if len(q.get('explanation',''))<100:flags.append('short_explanation_candidate')
  if q.get('difficulty') is None:flags.append('missing_difficulty')
  if q.get('questionForm') is None:flags.append('missing_question_form')
  basis=json.dumps(q.get('legalBasis',[]),ensure_ascii=False)
  if not q.get('legalBasis'):flags.append('missing_basis')
  if '04/2026/QH16' in basis and not all(re.search(r'2027|hiệu lực từ|có hiệu lực|thông qua|chuyển tiếp',v,re.I) for v in variants):flags.append('future_rule_without_date_candidate')
  src=q.get('source',{}); sid=src.get('id')
  if sid and sid not in sources:flags.append('unknown_source_id')
  if sid=='OFFICIAL-TT06-2025' and '06/2025/TT-BTP' not in basis:flags.append('source_basis_mismatch')
  if q['id'].startswith('EXP26-') and any(v.startswith(tuple(PREFIXES)) for v in variants):flags.append('mechanical_prefix_paraphrase')
  if q['id']=='SRC26-015' and 'Điều 12' in basis:flags.append('wrong_article_confidentiality_should_be_18_2_e')
  # A scenario may quote the learner's mistaken "consecutive" argument and reject it.
  if q['id']=='SRC26-005' and any('liên tiếp' in v for v in variants) and 'không quy định ba kỳ phải liên tiếp' not in q.get('explanation',''):flags.append('extra_condition_consecutive_not_in_article_16')
  if flags:findings.append({'id':q['id'],'status':q['status'],'flags':flags})
 eligible=[q for q in bank if q.get('status') in ('active','verified')]
 near=[]
 for i,q in enumerate(bank):
  if q['id'].startswith('EXP26-'):continue
  for r in bank[i+1:]:
   if r['id'].startswith('EXP26-'):continue
   a=norm(q['question']['variants'][0]);b=norm(r['question']['variants'][0]);matcher=difflib.SequenceMatcher(None,a,b)
   if matcher.quick_ratio()<.78:continue
   ratio=matcher.ratio()
   if ratio>=.78 and a!=b:near.append({'ids':[q['id'],r['id']],'similarity':round(ratio,3),'requiresEditorialReview':True})
 return {'total':len(bank),'eligible':len(eligible),'fileCounts':counts,'sha256':hashes,'status':count(bank,'status'),'part':count(bank,'part'),'topic':count(bank,'topic'),'difficultyLabelsNotCertified':count(bank,'difficulty'),'questionForm':count(bank,'questionForm'),'eligibleTopic':count(eligible,'topic'),'eligibleDifficulty':count(eligible,'difficulty'),'eligibleQuestionForm':count(eligible,'questionForm'),'basis':dict(collections.Counter(b if isinstance(b,str) else json.dumps(b,ensure_ascii=False,sort_keys=True) for q in bank for b in q.get('legalBasis',[]))),'duplicateIds':groups(bank,lambda q:q['id']),'exactStemGroups':groups(bank,lambda q:q['question']['variants'][0]),'prefixNormalizedGroups':groups(bank,lambda q:norm(q['question']['variants'][0])),'identicalAnswersExplanationBasisGroups':groups(bank,lambda q:json.dumps([q['answers'],q['explanation'],q['legalBasis']],ensure_ascii=False,sort_keys=True)),'nearStemCandidates':near,'findings':findings,'flagCounts':dict(collections.Counter(f for q in findings for f in q['flags']))}
if __name__=='__main__':
 result=audit();path=ROOT/'reports'/(sys.argv[1] if len(sys.argv)>1 else 'bank-audit-current.json');path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['total','eligible','status','flagCounts']},ensure_ascii=False,indent=2))
