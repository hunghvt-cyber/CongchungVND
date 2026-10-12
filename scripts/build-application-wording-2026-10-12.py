"""Curated presentation revisions; original sealed legal snapshots remain traceable."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
names=re.findall(r"'([^']+\.json)'",re.search(r'const files = \[(.*?)\];',(ROOT/'app.js').read_text(),re.S).group(1))
# Editorial decisions: discard direct recall; retain independently authored applications.
prune={}
for q in json.loads((ROOT/'data/questions.json').read_text()):
 if q.get('status') in ('active','verified'):prune[q['id']]={0}
for n in [1,7,18,21,28,31,36,37,38,41,42,51,52,60,62,65,66,67,70,72,75,76,90,91,93,96,99]:prune[f'CC-{n:03}'].add(1)
for key,indices in {
'SRC26-001':[0,1],'SRC26-006':[1],
'VER26-036':[1],'VER26-053':[1],'VER26-055':[1],'VER26-058':[1],'VER26-089':[1],
'IMP-SEP24-017':[0],
'IMP-T60-005':[0],'IMP-T60-006':[0],'IMP-T60-008':[0],'IMP-T60-019':[0],
'IMP-T60-027':[0],'IMP-T60-030':[0],'IMP-T60-036':[0],'IMP-T60-041':[0],
'IMP-T60-051':[0],'IMP-T60-052':[0],'IMP-T60-053':[0],'IMP-T60-060':[0],
'IMP-T60-071':[0],'IMP-T60-076':[0],'IMP-T60-077':[0],'IMP-T60-085':[0],
'IMP-T60-099':[0],'IMP-T60-017':[0],'IMP-T60-018':[0],
'VER26-NEW-48':[1],'VER26-NEW-49':[1],'VER26-NEW-66':[1],
}.items():prune.setdefault(key,set()).update(indices)
# Replacements keep all choices and legal conditions; no new legal conclusion.
manual={
'CC-001':['Tháng 10/2026: Khách hàng cho rằng thu phí khiến việc công chứng trở thành kinh doanh pháp lý thuần túy. Công chứng viên cần giải thích tính chất hoạt động này như thế nào?'],
'CC-007':['Tháng 10/2026: Hai bên đều biết tiếng Anh và muốn dùng tiếng Anh cho toàn bộ quá trình công chứng tại Việt Nam. Văn phòng phải sử dụng tiếng nói, chữ viết nào để thực hiện công chứng?'],
'CC-018':['Tháng 10/2026: Luật sư A đã hành nghề ba năm và muốn vào khóa đào tạo nghề công chứng rút ngắn sáu tháng. Bộ phận tuyển sinh yêu cầu A tiếp tục tích lũy kinh nghiệm. Tổng thời gian hành nghề ít nhất A phải có trước khi thuộc nhóm học khóa này là bao nhiêu?'],
'CC-017':['Tháng 10/2026: Cơ sở đào tạo dự kiến mở khóa nghề công chứng sáu tháng cho mọi học viên, kể cả người không thuộc diện đào tạo rút ngắn. Để sửa kế hoạch cho nhóm học thông thường, phải bố trí khóa dài bao lâu?'],
'SRC26-001':['Tháng 10/2026: Một tài liệu hướng dẫn dự kiểm tra kết quả tập sự ghi rằng cả hai bài đều làm trắc nghiệm trên máy tính. Người tổ chức cần sửa tài liệu thành tổ hợp hình thức và thời gian nào của hai bài theo văn bản đang áp dụng, chưa áp dụng phương án trong dự thảo sửa đổi?'],
'CC-089':['Tháng 10/2026: Nhân viên dùng một quy trình nội bộ duy nhất cho cả ủy quyền và lập di chúc, không kiểm tra thủ tục riêng của từng loại. Khi hướng dẫn xử lý hồ sơ, công chứng viên phải kết hợp những nhóm quy định nào?'],
}
# Pure citation hints can move to the explanation; substantive qualifiers stay explicit.
ref=r'(?:điểm\s+[a-zđ]\s+)?(?:khoản\s+\d+[a-z]?\s+)?Điều\s+\d+[a-z]?(?:\(\d+[a-z]?\))?'
doc=r'(?:\s+(?:TT06/2025|TT06/2025/TT-BTP|BLDS|Luật HNGĐ|Luật Đất đai|Luật Công chứng))?'
def style(v):
 v=re.sub(r'(?:Theo|Đối chiếu riêng|Khi đối chiếu)\s+'+ref+doc+r'(?:\s+(?:mới|đang áp dụng))?\s*,\s*','',v,flags=re.I)
 v=re.sub(r'\s+theo\s+'+ref+doc+r'(?:\s+(?:mới|đang áp dụng))?(?=[,?.])','',v,flags=re.I)
 v=re.sub(r'\s+tại\s+'+ref+doc+r'(?=[,?.])','',v,flags=re.I)
 v=re.sub(r'Chỉ xét\s+'+ref+doc+r'(?:\s+mới)?\s*,\s*','Chỉ xét các dữ kiện trên, ',v,flags=re.I)
 return re.sub(r' {2,}',' ',v).strip()
rows=[];decisions=[];removed=0;affected=set();archive=[]
for name in names:
 for q in json.loads((ROOT/'data'/name).read_text()):
  if q.get('status') not in ('active','verified'):continue
  if q['id']=='CC-082':
   rows.append({'id':q['id'],'sourceSha256':hashlib.sha256(json.dumps({'question':q['question'],'answers':q['answers'],'legalBasis':q['legalBasis']},ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'status':'archived','reason':'Các phương án chỉ là số điều luật; không kiểm tra cách xử lý tình huống.'});archive.append(q['id']);removed+=len(q['question']['variants']);decisions.append({'id':q['id'],'sourceFile':name,'beforeVariants':q['question']['variants'],'afterStatus':'archived','legalBasis':q['legalBasis'],'answerKey':q.get('answerKey',[a['id'] for a in q['answers'] if a['correct']]),'reason':'Loại câu yêu cầu nhớ số điều, không sửa kết luận pháp lý.'});continue
  before=q['question']['variants'];selected=[v for i,v in enumerate(before) if i not in prune.get(q['id'],set())]
  if q['id'] in manual:selected=manual[q['id']]
  assert selected,q['id']
  after=list(dict.fromkeys(style(v) for v in selected))
  if before!=after:
   affected.add(q['id']);removed+=max(0,len(before)-len(after));rows.append({'id':q['id'],'sourceSha256':hashlib.sha256(json.dumps({'question':q['question'],'answers':q['answers'],'legalBasis':q['legalBasis']},ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'variants':after})
   decisions.append({'id':q['id'],'sourceFile':name,'beforeVariants':before,'afterVariants':after,'legalBasis':q['legalBasis'],'answerKey':q.get('answerKey',[a['id'] for a in q['answers'] if a['correct']]),'answerSha256':hashlib.sha256(json.dumps(q['answers'],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'reason':'Giữ tình huống áp dụng, bỏ cách hỏi học thuộc; chuyển gợi dẫn điều khoản thuần túy ra khỏi cách hỏi. Khóa, phương án và giải thích pháp lý không đổi.'})
profile={'version':1,'date':'2026-10-12','purpose':'Only application wording is available to random selection in practice and exams. Original legal snapshots retained for traceability.','questions':rows}
(ROOT/'data/application-wording-2026.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n')
report={'date':'2026-10-12','sourceCommit':'f06a7b406d997d4f83b9299e7f633ebe9a0035ed','policy':'Không hỏi nội dung/số điều để học thuộc. Giữ tình huống xác định quyền, điều kiện, trình tự hoặc hệ quả. Một số điều kiện giới hạn pháp lý trong tình huống vẫn giữ tham chiếu để tránh thay đổi nghĩa của giả thiết; không dùng tham chiếu đó làm đáp án số điều.','changedQuestionCount':len(affected),'removedWordingSlots':removed,'archivedIds':archive,'eligibleBefore':794,'eligibleAfter':793,'decisions':decisions}
(ROOT/'reports/application-wording-review-2026-10-12.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in report.items() if k not in ['decisions','policy']})
