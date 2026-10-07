#!/usr/bin/env python3
"""One-time editorial migration of legacy string citations; retain question IDs."""
import json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def write(path,value): (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def review():
 path=ROOT/'data/questions.json'; bank=json.loads(path.read_text())
 sources={s['id']:s for s in json.loads((ROOT/'data/question-sources.json').read_text())['sources']}
 changes=[]
 for q in bank:
  if q['status']!='active':continue
  before=json.loads(json.dumps(q)); refs=[]
  for old in q['legalBasis']:
   if isinstance(old,dict):refs.append(old);continue
   code='OFFICIAL-CC26' if '04/2026/QH16' in old and not old.startswith('Luật Công chứng') else 'OFFICIAL-CC24'
   doc=sources[code]; article=re.search(r'Điều (\d+)',old)[1]
   clauses=re.findall(r'khoản (\d+)',old.split(';')[0],re.I)
   if q['id']=='CC-047': clauses=['11']  # 7a is a clause of the amended Article 42, not Article 1.
   point=re.search(r'điểm ([a-zđ])',old,re.I)
   for clause in clauses or [None]:
    b={'document':doc['title'],'article':'Điều '+article,'url':doc['url']}
    if clause:b['clause']='Khoản '+clause
    if point:b['point']='Điểm '+point[1]
    refs.append(b)
  if q['id']=='CC-018':
   refs=[{'document':sources['OFFICIAL-CC24']['title'],'article':'Điều 11','clause':'Khoản 3','point':'Điểm b','url':sources['OFFICIAL-CC24']['url']}]
  if q['id']=='CC-082':
   refs=[{'document':sources['OFFICIAL-CC24']['title'],'article':'Điều 56','clause':'Khoản 1','url':sources['OFFICIAL-CC24']['url']},
    {'document':sources['OFFICIAL-CC26']['title'],'article':'Điều 1','clause':'Khoản 13','url':sources['OFFICIAL-CC26']['url']}]
  if any('04/2026/QH16' in r['document'] for r in refs):
   if not any(r['article']=='Điều 2' for r in refs if '04/2026/QH16' in r['document']):
    refs.append({'document':sources['OFFICIAL-CC26']['title'],'article':'Điều 2','url':sources['OFFICIAL-CC26']['url']})
  q['legalBasis']=refs
  if q['id']=='CC-058':
   q['question']['variants']=['Từ 01/01/2027, văn bản công chứng hợp đồng ủy quyền theo trình tự chứng nhận tại hai tổ chức có hiệu lực khi nào?']
   q['answers'][3]['text']='Khi tổ chức chứng nhận bên ủy quyền gửi bản sao hồ sơ cho tổ chức còn lại'
  if q['id']=='CC-098':
   q['question']['variants']=['Từ 01/01/2027, Điều 3 khoản 6 Luật số 04/2026/QH16 dành thời hạn bao lâu, tính từ ngày luật có hiệu lực, để Chính phủ tổ chức rà soát và xử lý quy định về giao dịch phải công chứng?']
  if q['id']=='CC-097':
   q['question']['variants']=['Từ 01/01/2027, cơ sở dữ liệu công chứng địa phương có trước ngày này được quản lý, khai thác theo cơ chế chuyển tiếp nào?']
  if q['id']=='CC-044':
   q['question']['variants']=['Từ 01/01/2027, người yêu cầu đồng ý toàn bộ dự thảo giao dịch giấy, không áp dụng điểm chỉ. Yêu cầu về ký và dấu của tổ chức tham gia giao dịch tại khoản 7 Điều 42 mới là gì?']
   q['answers'][0]['text']='Ký từng trang; ký và ghi đủ họ tên cá nhân, đóng dấu của tổ chức (nếu có) vào trang cuối giao dịch'
   q['explanation']='Quy tắc này nói về chữ ký người yêu cầu và dấu của tổ chức tham gia giao dịch nếu có. Phải ký từng trang, ký và ghi đủ họ tên vào trang cuối; không nhầm dấu của bên là tổ chức với dấu tổ chức hành nghề công chứng tại lời chứng. Trường hợp điểm chỉ thực hiện theo Điều 50.'
  if q['id']=='CC-100':
   q['question']['variants']=['Từ 01/01/2027, xét riêng nguyên tắc địa bàn tại khoản 1 Điều 44 mới, một giao dịch chuyển nhượng đất không thuộc ngoại lệ có đất ở tỉnh khác nơi tổ chức hành nghề công chứng đặt trụ sở. Kết luận nào phù hợp?']
  if not any('04/2026/QH16' in r['document'] for r in refs) and not any('2026' in v or '2027' in v for v in q['question']['variants']):
   q['question']['variants']=['Tháng 10/2026: '+v for v in q['question']['variants']]
  q['lastVerified']='2026-10-07'
  if before!=q:
   changes.append({'id':q['id'],'changedFields':[k for k in q if q[k]!=before.get(k)],'before':before,'after':q,
    'decision':'Giữ active sau rà câu dẫn, đáp án và điều khoản; chuẩn hóa đường dẫn, mốc luật và phạm vi căn cứ.'})
 write('data/questions.json',bank)
 write('reports/core-review-decisions-2026-10-07.json',{'date':'2026-10-07','scope':'93 câu active trong questions.json; không cập nhật ngày kiểm định hàng loạt cho các file khác.','questions':changes})
 print(len(changes),'legacy active questions reviewed')
if __name__=='__main__':review()
