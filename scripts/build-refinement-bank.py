#!/usr/bin/env python3
"""Serialize 80 manually authored cases and link their statutory evidence."""
import collections, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = {'CC':'Luật Công chứng – công chứng viên – TCHNCC',
 'QT':'Quy trình, thủ tục và nghiệp vụ công chứng',
 'DAT':'Đất đai, nhà ở và kinh doanh bất động sản'}
def write(path, value):
 (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def build():
 registry=json.loads((ROOT/'reports/refinement-provisions-2026.json').read_text())
 documents=registry['documents']; articles=registry['articles']
 questions=[]; proof=[]; counts=collections.Counter()
 for line_number,line in enumerate((ROOT/'scripts/refinement-cases-2026.tsv').read_text().splitlines(),1):
  if not line or line.startswith('#'):continue
  cells=line.split('|')
  if len(cells)!=10:raise ValueError(f'line {line_number}: expected 10 cells, got {len(cells)}')
  group,difficulty,form,refs,stem,key,d1,d2,d3,reason=cells
  assert difficulty in ('recognition','understanding','application','advanced')
  assert form in ('direct','true_false','choose_case','short_case','workflow','synthesis','exception')
  counts[group]+=1; qid=f'REFIN26-{group}-{counts[group]:03}'
  basis=[]; evidence=[]
  for token in refs.split(';'):
   code,article,*tail=token.split(':'); doc=documents[code]
   b={'document':doc['title'],'article':f'Điều {article}','url':doc['url']}
   if tail and tail[0]:b['clause']=f'Khoản {tail[0]}'
   if len(tail)>1 and tail[1]:b['point']=f'Điểm {tail[1]}'
   assert len(articles[code][article])>100,(qid,token)
   basis.append(b);evidence.append({'reference':b,'evidenceRef':{'documentCode':code,'article':article}})
  options=[key,d1,d2,d3]; shift=len(questions)%4
  options=options[-shift:]+options[:-shift] if shift else options
  assert len(set(options))==4 and len(reason)>=100,qid
  answers=[{'id':chr(65+i),'text':text,'correct':text==key} for i,text in enumerate(options)]
  codes=list(dict.fromkeys(t.split(':')[0] for t in refs.split(';')))
  questions.append({'id':qid,'part':1 if group=='CC' else 2,'topic':GROUPS[group],
   'type':'single','status':'active','difficulty':difficulty,'questionForm':form,
   'question':{'variants':['Tháng 10/2026: '+stem]},'answers':answers,
   'explanation':reason,'legalBasis':basis,'lastVerified':'2026-10-07',
   'source':{'type':'official','id':documents[codes[0]]['sourceId'],
    'supportingSourceIds':[documents[c]['sourceId'] for c in codes[1:]],
    'note':'Biên soạn từng tình huống; chứng cứ điều khoản tại reports/refinement-legal-evidence-2026.json và refinement-provisions-2026.json.'}})
  proof.append({'id':qid,'verifiedAt':'2026-10-07','applicableAt':'2026-10-07',
   'competence':stem,'answer':next(a['id'] for a in answers if a['correct']),
   'provisions':evidence})
 assert dict(counts)=={'CC':40,'QT':25,'DAT':15},counts
 write('data/refinement-2026.json',questions)
 # Retain only cited articles, keeping each full excerpt once.
 used=collections.defaultdict(set)
 for q in proof:
  for p in q['provisions']:used[p['evidenceRef']['documentCode']].add(p['evidenceRef']['article'])
 registry['articles']={c:{a:articles[c][a] for a in sorted(nums,key=int)} for c,nums in used.items()}
 write('reports/refinement-provisions-2026.json',registry)
 write('reports/refinement-legal-evidence-2026.json',{'date':'2026-10-07',
  'scope':'80 câu REFIN26 riêng biệt; trích điều khoản giải quyết evidenceRef tại refinement-provisions-2026.json.',
  'questions':proof})
 print(json.dumps({'new':len(questions),'groups':counts,
  'keys':dict(collections.Counter(next(a['id'] for a in q['answers'] if a['correct']) for q in questions))},ensure_ascii=False))
if __name__=='__main__':build()
