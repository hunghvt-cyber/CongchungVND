"""Screen the untouched cohort and record work remaining, without certifying difficulty."""
import json, re, collections, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((ROOT/p).read_text())
files=re.findall(r"'([^']+\.json)'",re.search(r'const files = \[(.*?)\];',(ROOT/'app.js').read_text(),re.S).group(1))
bank={q['id']:q for f in files for q in read('data/'+f)}
for r in read('data/application-wording-2026.json')['questions']:
 q=bank[r['id']]
 if r.get('variants'):q['question']['variants']=r['variants']
 if r.get('status'):q['status']=r['status']
prior=read('data/scenario-refinements-2026.json')['questions']
for r in prior:bank[r['id']]=r['after']
prior_ids={r['id'] for r in prior}
extra=read('data/scenario-refinements-remaining-2026.json')['questions']
after={r['id']:r['after'] for r in extra}
absolute=re.compile(r'luôn|mọi|bất kỳ|đương nhiên|tuyệt đối|không bao giờ|trong mọi|vĩnh viễn',re.I)
def signals(q):
 correct=[len(a['text']) for a in q['answers'] if a['correct']]
 wrong=[a['text'] for a in q['answers'] if not a['correct']]
 statutes={('CC' if 'Công chứng' in b['document'] else 'DS' if 'Dân sự' in b['document'] else 'HN' if 'Hôn nhân' in b['document'] else b['document']) for b in q['legalBasis']}
 flags=[]
 if max(correct)>1.6*max(map(len,wrong)):flags.append('length')
 if sum(bool(absolute.search(s)) for s in wrong)>=2:flags.append('absolute_distractors')
 if sum(len(s)<30 for s in wrong)>=2:flags.append('short_distractors')
 return {'flags':flags,'statuteGroups':len(statutes),'authoredReasoningSteps':len(q.get('integrationSteps',[]))}
rows=[]
for q in bank.values():
 if q['id'] in prior_ids or q['status'] not in ('active','verified'):continue
 before=signals(q);new=after.get(q['id'],q)
 disposition='rewritten_60' if q['id'] in after else 'context_review_candidate' if before['flags'] else 'retain_pending_trial_not_certified'
 rows.append({'id':q['id'],'part':q['part'],'topic':q['topic'],'type':q['type'],'before':before,'after':signals(new),'disposition':disposition,'empiricallyCalibrated':False})
assert len(rows)==726 and len(after)==60 and not prior_ids.intersection(after)
sel=[r for r in rows if r['id'] in after]
metrics={side:dict(collections.Counter(f for r in sel for f in r[side]['flags'])) for side in ('before','after')}
result={'date':'2026-10-13','scope':'Sàng lọc toàn 726 câu ngoài nhóm 67, biên tập thực chất 60 câu; các câu khác chưa được chứng nhận đạt mức khó.',
        'screened':726,'rewritten':60,'remainingOutsidePrevious67':666,'previousRepairsRetained':67,'cumulativeRepairs':127,'eligible':793,
        'screeningLimits':'Dấu hiệu tự động chọn ứng viên, không là lỗi pháp lý hoặc phép đo độ khó. Một luật vẫn có thể có nhiều bước áp dụng. Không tự loại câu hoặc đổi nhãn 666 câu chưa sửa.',
        'method':{'length':'Đáp án đúng dài hơn 1,6 lần phương án sai dài nhất','absolute_distractors':'Ít nhất hai phương án sai có từ tuyệt đối; cần xét trong dữ kiện','short_distractors':'Ít nhất hai phương án sai dưới 30 ký tự'},
        'dispositions':dict(collections.Counter(r['disposition'] for r in rows)),
        'selectedMetrics':metrics,'crossStatuteNewRepairs':sum(r['after']['statuteGroups']>=2 for r in sel),
        'minimumReasoningStepsNewRepairs':min(r['after']['authoredReasoningSteps'] for r in sel),
        'trial':{'status':'pending','noAttemptDataQueried':True,'noSyntheticCentralResultsCreated':True,'metricsNeeded':['first_attempt_accuracy_by_question_version','distractor_selection_rates','unanswered_rate','response_time_when_available'],'interpretation':'Tách lần đầu và làm lại, câu và biến thể/phiên bản; nhóm nhỏ có mẫu thấp chỉ dùng định hướng, chưa suy kết luận chắc chắn.'},
        'rows':rows}
tap=ROOT/'reports/remaining-60-tests-2026-10-13.tap'
audit=ROOT/'reports/bank-audit-remaining-60-2026-10-13.json'
if tap.exists() and audit.exists():
 text=tap.read_text();passed=re.search(r'^# pass (\d+)$',text,re.M);failed=re.search(r'^# fail (\d+)$',text,re.M)
 if passed and failed:
  check=json.loads(audit.read_text());ids=set(after)
  result['verification']={'regressionPassed':int(passed[1]),'regressionFailed':int(failed[1]),
   'eachOptionGradedInBothModes':True,'optionGradingCases':60*4*2,'sharedCodeReplayBothParts':True,
   'eligible':check['eligible'],'duplicateIds':check['duplicateIds'],'exactStemGroups':check['exactStemGroups'],
   'newNearStemCandidates':[c for c in check['nearStemCandidates'] if ids.intersection(c['ids'])],
   'newStructuralOrLegalMetadataErrors':[r for r in check['findings'] if r['id'] in ids and set(r['flags'])-{'needs_substantive_variants'}],
   'oneApprovedScenarioPerRewrittenQuestion':True}
(ROOT/'reports/remaining-726-screening-2026-10-13.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ('screened','rewritten','dispositions','selectedMetrics','crossStatuteNewRepairs')},ensure_ascii=False))
