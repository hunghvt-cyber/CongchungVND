#!/usr/bin/env python3
"""Build two printable practice papers, independently shuffling their options."""
import json, pathlib, random
ROOT=pathlib.Path(__file__).resolve().parents[1]
def build():
 questions=json.loads((ROOT/'data/refinement-2026.json').read_text())
 rng=random.Random(20261007)
 out=['# Hai đề luyện bổ sung — 07/10/2026','',
  '80 câu đã tích hợp ngân hàng. Hai đề này phục vụ tự luyện theo chủ đề, không phải cấu trúc hoặc đề chính thức của kỳ kiểm tra. Mỗi đề 40 câu; thời gian tự luyện gợi ý 60 phút. Mỗi câu chọn đúng một phương án. Quy định áp dụng tháng 10/2026.',
  '', 'Thứ tự phương án đã xáo riêng cho hai đề này. Chữ cái đáp án trong tài liệu có thể khác chữ cái lưu trong JSON hoặc hiển thị ở phiên ôn tập trên web; nội dung đáp án đúng giữ nguyên.','']
 for part,title in [(1,'Đề 1 — Tổ chức hành nghề và công chứng viên'),(2,'Đề 2 — Xử lý hồ sơ và đất đai')]:
  chosen=[q for q in questions if q['part']==part];assert len(chosen)==40
  keys={};out+=['## '+title,'']
  for number,q in enumerate(chosen,1):
   options=list(q['answers']);rng.shuffle(options)
   out += [f"**Câu {number} ({q['id']}).** {q['question']['variants'][0]}",'']
   for position,answer in enumerate(options):
    label=chr(65+position);out.append(f"- {label}. {answer['text']}")
    if answer['correct']:keys[q['id']]=label
   out+=['']
  out+=['## Đáp án và lời giải — '+('Đề 1' if part==1 else 'Đề 2'),'']
  for number,q in enumerate(chosen,1):
   out += [f"**Câu {number}: {keys[q['id']]} — {q['id']}.** {q['explanation']}",'']
   for basis in q['legalBasis']:
    ref=', '.join(basis[k] for k in ['document','article','clause','point'] if k in basis)
    out.append(f"- [{ref}]({basis['url']})")
   out+=['']
 (ROOT/'reports/refinement-exams-2026-10-07.md').write_text('\n'.join(out)+'\n')
if __name__=='__main__':build()
