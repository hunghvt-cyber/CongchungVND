#!/usr/bin/env python3
"""Serialize individually authored cases. Does not generate paraphrase batches."""
import collections, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = {
 'DN': 'Doanh nghiệp và giao dịch liên quan',
 'CT': 'Chứng thực và pháp luật liên quan',
 'DD': 'Đạo đức nghề nghiệp và trách nhiệm',
 'TS': 'Tập sự và kiểm tra kết quả tập sự',
 'QT': 'Quy trình, thủ tục và nghiệp vụ công chứng',
 'DS': 'Dân sự – giao dịch – đại diện – nghĩa vụ',
 'HN': 'Hôn nhân và gia đình – tài sản vợ chồng',
 'TK': 'Thừa kế', 'DAT': 'Đất đai, nhà ở và kinh doanh bất động sản',
}
def write(path, value):
 (ROOT/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def build():
 registry=json.loads((ROOT/'reports/completion-provisions-2026.json').read_text())
 documents=registry['documents']; articles=registry['articles']
 questions=[]; proof=[]; counts=collections.Counter()
 for line_number,line in enumerate((ROOT/'scripts/completion-cases-2026.tsv').read_text().splitlines(),1):
  if not line or line.startswith('#'): continue
  cells=line.split('|')
  if len(cells)!=10: raise ValueError(f'line {line_number}: expected 10 cells, got {len(cells)}')
  group,difficulty,form,refs,stem,key,d1,d2,d3,reason=cells
  counts[group]+=1; qid=f'COMP26-{group}-{counts[group]:03}'
  basis=[]; evidence=[]
  for token in refs.split(';'):
   code,article,*tail=token.split(':'); doc=documents[code]
   b={'document':doc['title'],'article':f'Điều {article}','url':doc['url']}
   if tail and tail[0]: b['clause']=f'Khoản {tail[0]}'
   if len(tail)>1 and tail[1]: b['point']=f'Điểm {tail[1]}'
   excerpt=articles[code][article]
   assert len(excerpt)>100, (qid,token)
   basis.append(b); evidence.append({'reference':b,'evidenceExcerpt':excerpt})
  options=[key,d1,d2,d3]; shift=(len(questions)%4)
  options=options[-shift:]+options[:-shift] if shift else options
  answers=[{'id':chr(65+i),'text':text,'correct':text==key} for i,text in enumerate(options)]
  assert len(set(options))==4 and len(reason)>=100, qid
  source_codes=list(dict.fromkeys(t.split(':')[0] for t in refs.split(';')))
  questions.append({'id':qid,'part':1 if group in ('DD','TS') else 2,
   'topic':GROUPS[group],'type':'single','status':'active','difficulty':difficulty,'questionForm':form,
   'question':{'variants':['Tháng 10/2026: '+stem]},'answers':answers,
   'explanation':reason,'legalBasis':basis,'lastVerified':'2026-10-07',
   'source':{'type':'official','id':documents[source_codes[0]]['sourceId'],
    'supportingSourceIds':[documents[c]['sourceId'] for c in source_codes[1:]],
    'note':'Tình huống độc lập, biên soạn từng dòng; chứng cứ tại reports/completion-legal-evidence-2026.json.'}})
  proof.append({'id':qid,'verifiedAt':'2026-10-07','applicableAt':'2026-10-07',
    'competence':stem,'answer':next(a['id'] for a in answers if a['correct']),
    'review':'Đối chiếu giả thiết, khóa, từng nhiễu và giới hạn điều khoản; không chứng nhận toàn bộ tài liệu DOCX.',
    'provisions':evidence})
 assert len(questions)==80, len(questions)
 write('data/completion-2026.json',questions)
 write('reports/completion-legal-evidence-2026.json',{'date':'2026-10-07','scope':'80 câu độc lập COMP26; không phải 500 câu mới đã hoàn tất.','questions':proof})
 print(json.dumps({'new':len(questions),'groups':counts,'keys':dict(collections.Counter(next(a['id'] for a in q['answers'] if a['correct']) for q in questions))},ensure_ascii=False))
if __name__=='__main__': build()
