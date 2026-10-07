#!/usr/bin/env python3
"""Preserve prior primary-topic assignments and report the actual current bank."""
import collections, json, pathlib, sys
sys.dont_write_bytecode=True
from importlib.machinery import SourceFileLoader
ROOT=pathlib.Path(__file__).resolve().parents[1]
audit=SourceFileLoader('audit_bank',str(ROOT/'scripts/audit-bank.py')).load_module()
def write(path,value):(ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def build():
 prior=json.loads((ROOT/'reports/matrix-2026-10-07.json').read_text())
 primary={q['id']:q['primaryGroup'] for q in prior['questions']}
 bank=[q for f in audit.FILES for q in json.loads((ROOT/'data'/f).read_text())]
 active=[q for q in bank if q['status'] in ('active','verified')]
 rows=[]
 for q in active:
  group=primary.get(q['id'],q['topic'])
  if q['id'].startswith('REFIN26-DAT'):group='Đất đai – nhà ở – kinh doanh BĐS'
  rows.append({'id':q['id'],'rawTopic':q['topic'],'primaryGroup':group,'difficulty':q['difficulty'],'questionForm':q['questionForm']})
 counts=collections.Counter(q['primaryGroup'] for q in rows)
 groups=[]
 for old in prior['groups']:
  g=old.copy();g['count']=counts[g['group']];g['percent']=round(100*g['count']/len(active),2)
  if g.get('targetPercent') is not None:g['gapPercentagePoints']=round(g['percent']-g['targetPercent'],2)
  groups.append(g)
 assert sum(g['count'] for g in groups)==len(active),(counts,groups)
 out={'date':'2026-10-07','scope':'Sau 80 câu REFIN26 và ngừng dùng ba câu trùng năng lực; phân nhóm chính kế thừa từng ID, không relabel để khớp tỷ lệ.',
  'totalStored':len(bank),'active':len(active),'status':dict(collections.Counter(q['status'] for q in bank)),
  'groups':groups,'difficulty':dict(collections.Counter(q['difficulty'] for q in active)),
  'questionForms':dict(collections.Counter(q['questionForm'] for q in active)),
  'difficultyQualification':'Nhãn độ khó là đánh giá biên soạn, chưa hiệu chỉnh bằng dữ liệu làm bài thực tế.',
  'questions':rows}
 write('reports/matrix-refinement-2026-10-07.json',out)
 print(json.dumps({k:out[k] for k in ['totalStored','active','status','groups','difficulty','questionForms']},ensure_ascii=False))
if __name__=='__main__':build()
