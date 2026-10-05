> Báo cáo mốc audit ban đầu tại commit b0a78f5, trước đợt nhập hai đề. Số liệu mới xem [báo cáo hai đề](exam-import-2026-10-05.md).

# Audit ngân hàng CongchungVND — 05/10/2026

**Trạng thái: đã rà cấu trúc toàn bộ 620 câu đầu vào và tích hợp 100 tình huống mới; chưa hoàn thành mục tiêu 400 câu chuẩn hoặc thay thế đủ 500 câu mở rộng.** Không dùng báo cáo này làm xác nhận rằng 620 câu cũ đều đã được kiểm định pháp lý.

## Số lượng và quyết định biên tập

| Chỉ tiêu | Trước | Sau |
|---|---:|---:|
| Bản ghi lưu trong repo | 620 | 720 |
| Active | 100 | 181 |
| Review | 520 | 36 |
| Archived, không được chọn luyện/thi | 0 | 503 |
| Câu mới độc lập | 0 | 100 |

- 500 EXP26: loại khỏi sử dụng toàn bộ. Mỗi điểm gốc được nhân thành năm câu bằng tiền tố; đáp án, giải thích và căn cứ giống nhau. Nhãn vận dụng/vận dụng cao của các bản sao không chứng minh năng lực được kiểm tra. Giữ ID và bản gốc ở trạng thái archived để truy vết.
- Ba câu trùng kiến thức được archived: CC-094 giữ CC-031; CC-095 giữ CC-032; SRC26-016 giữ CC-011.
- 100 câu CC được sửa giải thích, nhãn phân loại, nguồn và cách ghi mốc hiệu lực. Trong đó 81 active, 17 review vì phương án nhiễu còn yếu, hai archived. Đây là sửa biên tập 100 bản ghi, không phải 100 tình huống mới.
- 20 câu SRC được rà toàn bộ: sửa cụ thể SRC26-005, SRC26-015 và 13 nguồn gắn sai; một archived, 19 review. Chưa xác nhận đầy đủ tình trạng hiệu lực các văn bản hướng dẫn để nâng active.
- 100 câu VER26 mới kiểm tra xử lý hồ sơ, HNGĐ, đất đai, thừa kế, dân sự/đại diện. Mỗi câu có bốn đáp án, đúng một đáp án đúng; vị trí đúng được phân bố đều. Lời giải nêu điểm quyết định và giới hạn của lựa chọn sai.

## Kiến thức còn thiếu

Các chủ đề chi tiết được thống kê đầy đủ trong `bank-audit-after.json`. Phân nhóm sau theo vấn đề pháp lý chủ yếu, không tính một câu nhiều lần. Các câu di chúc/ủy quyền/thế chấp chỉ hỏi thủ tục công chứng được xếp nghiệp vụ, không dùng để lấp chỉ tiêu luật nội dung.

| Nhóm kiến thức | Mục tiêu trên 400 | Active hiện tại |
|---|---:|---:|
| Luật Công chứng, công chứng viên, TCHNCC | 60 | 35 |
| Quy trình, thủ tục, nghiệp vụ | 90 | 60 |
| Dân sự, giao dịch, đại diện, nghĩa vụ | 55 | 20 |
| Đất đai, nhà ở, BĐS | 55 | 20 |
| HNGĐ, tài sản vợ chồng | 35 | 20 |
| Thừa kế | 40 | 20 |
| Doanh nghiệp | 20 | 0 |
| Chứng thực và liên quan | 15 | 0 |
| Đạo đức, trách nhiệm, vi phạm | 15 | 2 |
| Tập sự, kiểm tra kết quả tập sự | 15 | 4 |
| Tổng | 400 | 181 |

Các nhãn độ khó là đánh giá biên tập, chưa được hiệu chỉnh bằng dữ liệu người học.

| Độ khó | Số active | Tỷ lệ | Mục tiêu |
|---|---:|---:|---:|
| Nhận biết | 68 | 37,6% | 20% |
| Hiểu luật | 13 | 7,2% | 30% |
| Vận dụng | 86 | 47,5% | 30% |
| Vận dụng cao | 14 | 7,7% | 20% |

Vận dụng cộng vận dụng cao là 55,2%, nhưng từng mức vẫn chưa cân bằng. Dạng câu active: 68 trực tiếp, 13 ngoại lệ, 68 tình huống ngắn, 18 nghiệp vụ, 14 tổng hợp. Chưa đủ bảy dạng theo ma trận yêu cầu; không đổi nhãn để làm đẹp thống kê.

## Kiểm tra pháp luật và sửa lỗi

Mốc kiểm tra: tháng 10/2026. Các tình huống mới ghi rõ mốc này. Các câu kiểm tra thay đổi của Luật 04/2026/QH16 ghi rõ năm 2027, không áp dụng nội dung sửa đổi cho tình huống tháng 10/2026.

Nguồn chính thức đã đối chiếu: Luật Công chứng 46/2024/QH15; Luật sửa đổi 04/2026/QH16; Bộ luật Dân sự 91/2015/QH13 (hai phần PDF, OCR các điều được dùng); VBHN 121/VBHN-VPQH năm 2025 về HNGĐ; VBHN 44/VBHN-VPQH năm 2026 về đất đai; Thông tư 06/2025/TT-BTP; quy định sửa đổi liên quan trong Luật Thi hành án dân sự 106/2025/QH15. Văn bản hợp nhất được dùng để đọc nội dung cập nhật, không được coi có ngày hiệu lực độc lập.

`legal-evidence-2026.json` lưu URL chính thức, SHA-256 bản PDF và trích điều khoản cho từng câu VER26. Phạm vi bằng chứng này là 100 câu mới, không phải xác nhận mọi câu cũ. Việc điều khoản có mặt trong legalBasis không tự đủ để chuyển active.

Sửa cụ thể:

- SRC26-015: bảo mật tại Điều 18 khoản 2 điểm e và Điều 9 khoản 1 điểm a Luật Công chứng, thay viện dẫn sai Điều 12 khoản 2 điểm e.
- SRC26-005: bỏ điều kiện tự thêm “03 kỳ liên tiếp”; Điều 16 khoản 2 điểm c TT06 không quy định “liên tiếp”. Câu vẫn review.
- 13 SRC có nguồn TT06 nhưng căn cứ là Luật Công chứng được gắn đúng nguồn luật.
- CC-018: cập nhật thuật ngữ Thừa hành viên và dẫn Điều 114 khoản 2, Điều 115 khoản 1 Luật 106/2025/QH15, quy định áp dụng từ 01/07/2026.
- CC-045, CC-050: làm rõ phạm vi quy tắc chung và ngoại lệ, tránh khẳng định tuyệt đối.
- CC-069: làm rõ ngoại lệ cơ quan tố tụng yêu cầu hồ sơ gốc để xác minh/giám định.
- CC-073: đáp án phản ánh ngoại lệ pháp luật cho phép.
- CC-082: tách mốc quy định hiện tại và từ 2027.
- VER26-045: xác định rõ đất thương mại dịch vụ của tổ chức đã hết hạn, không thuộc tự động tiếp tục sử dụng và chưa được gia hạn, tránh lẫn trường hợp đất nông nghiệp có cơ chế riêng.

Tình trạng sửa đổi văn bản hướng dẫn, gồm TT06 và các văn bản liên quan, chưa được kiểm định hết. Vì vậy 19 SRC chưa được nâng active. Không có kết luận “đã rà toàn bộ hiệu lực mọi văn bản”.

## Rà cấu trúc và chống trùng

`bank-audit-before.json` ghi đầu vào nguyên trạng. `bank-audit-after.json` ghi trạng thái sau sửa với hash từng file. Script `scripts/audit-bank.py` thống kê part, topic, difficulty, dạng câu, căn cứ, nguồn, ID và các cụm trùng; cờ tự động là dấu hiệu cần đọc, không phải kết luận pháp lý.

Trước sửa: 500 bản sao cơ học; 120 câu chưa có nhãn độ khó; 620 chưa có dạng câu; 527 giải thích ngắn; 13 nguồn không khớp; các dấu hiệu mốc hiệu lực cần rà. Các cờ giải thích ngắn/paraphrase còn lại chủ yếu thuộc bản ghi archived giữ để truy vết, không lọt vào ngân hàng được chọn. Sau sửa, không có cờ cấu trúc của script đối với active. So khớp gần trùng còn nêu các cặp CC-044/SRC26-018, CC-071/SRC26-019, CC-075/SRC26-010; các SRC tương ứng đều review. Không coi chúng là câu mới có giá trị chỉ vì khác câu chữ.

Không thấy trùng ID trong 720 bản ghi; câu single đúng một khóa; không có câu dẫn trùng chuẩn hóa trong active. Kiểm tra này không thay thế việc đọc vấn đề pháp lý để nhận diện trùng kiến thức.

## Tích hợp và kiểm tra

App tải 220 bản ghi từ `questions.json`, `derived-questions.json`, `validated-2026.json`; bộ lọc chỉ cho 181 active vào luyện/thi. Không tải 500 EXP archived. Loader báo lỗi nếu file không phải mảng, thiếu ID hoặc trùng ID; không âm thầm giữ một câu bất kỳ.

Không sửa `progress.js`, khóa localStorage hoặc schema Supabase. Bản chụp bài đã nộp vẫn giữ câu hỏi/lời giải thời điểm thi. Mã đề CC1 gắn dấu vân tay ngân hàng; sau thay đổi dữ liệu phải tạo mã mới cho nhóm, đúng cơ chế hiện có.

Kiểm tra Node: 27/27 đạt, gồm chấm điểm, random đề, bộ lọc trạng thái, mã đề, thời gian, review đáp án, loader, nguồn/evidence và lưu kết quả/offline. Kiểm tra trình duyệt và triển khai được ghi bổ sung sau khi xác minh; không lấy test DOM tối giản làm bằng chứng đã mở web thật.

## Phần chưa hoàn thành

Cần bổ sung 400 câu mới độc lập nữa nếu giữ đích 500 câu mở rộng; cần tối thiểu 219 câu đạt chuẩn nữa để đạt mốc 400 active. Đồng thời cần bổ sung nhóm đang trống, viết lại 36 câu review, kiểm tra hiệu lực hướng dẫn và cân bằng ma trận. Đây là kết quả một đợt xử lý toàn ngân hàng và tích hợp phần đã kiểm định, chưa đạt tiêu chí hoàn thành toàn bộ dự án của Madam An.
