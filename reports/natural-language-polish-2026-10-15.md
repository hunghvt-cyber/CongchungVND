# Biên tập câu văn và phương án nhiễu — 15/10/2026

Đã sàng lọc ngân hàng 793 câu đang dùng và biên tập thủ công 40 câu ưu tiên, gồm 80 cách hỏi. 753 câu còn lại giữ nguyên trong lần cập nhật này; việc sàng lọc không đồng nghĩa chứng nhận tất cả đã mượt hoặc đủ khó.

## Thay đổi nội dung

- Viết lại câu dẫn theo tình huống và yêu cầu xử lý; bỏ các lời nhắc như “tách khối tài sản”, “bảo vệ người bắt buộc”, “áp dụng trần 5%” ở những câu đang chỉ sẵn cách giải.
- Giữ các dữ kiện quyết định kết quả: tuổi, mốc thời gian, phạm vi đại diện, tình trạng hồ sơ, ngoại lệ đã loại trừ và điều kiện áp dụng. CC-046 vẫn ghi rõ thời điểm áp dụng từ 01/01/2027.
- Thay phương án sai dễ loại bằng nhầm lẫn gần nội dung hỏi: thời điểm chấm dứt ủy quyền, giới hạn điều lệ, phê duyệt nội bộ so với quyền ký, hồ sơ sao chụp so với thẩm quyền địa bàn, cách tính phần thừa kế.
- Giới thiệu Lan nhất quán trong CC-010; rút câu nhiều mệnh đề ở COMP26-CT-013 và IMP-T60-069.
- Đưa bốn lựa chọn của HARD26-013 về cùng cách trình bày số tiền; lý do tính sai vẫn xuất hiện trong phần giải thích sau khi trả lời.
- Bổ sung giải thích riêng cho các lựa chọn trong những câu trước đây mới có giải thích tổng; chỉnh các ghi chú viết tắt thành đoạn văn dành cho người học.

Ví dụ, CAL26-015 không còn hướng dẫn người làm phải tách khối tài sản và bảo vệ phần bắt buộc ngay trong câu hỏi. Người làm phải tự nhận diện các bước từ dữ kiện. Với HARD26-041, phương án nhiễu thay vì cấm tuyệt đối thế chấp tiếp nay thử các cách xử lý như xin chủ nợ đồng ý đổi nơi công chứng hoặc trao đổi hồ sơ giữa hai tổ chức.

## Dấu vết và phạm vi bảo toàn

Các tệp nguồn và hồ sơ pháp lý trước đây được giữ nguyên. Bản biên tập lưu riêng tại `data/editorial-polish-2026.json`, có hash bản trước/sau và lý do sửa từng câu; bản thảo thủ công nằm ở `editorial/natural-language-polish-2026-10-15.cjs`.

Trình nạp kiểm tra khóa, mã câu, bài, loại, trạng thái, căn cứ, nguồn, ngày xác minh, số cách hỏi và hash phiên bản trước khi đưa nội dung mới vào luyện tập/thi thử. Kiểm thử hồ sơ lịch sử tiếp tục đối chiếu bản lịch sử; kiểm thử hiện tại đối chiếu bản biên tập và chấm điểm trên nội dung mới.

## Chỉ báo biên tập

Trong 38 câu một đáp án thuộc nhóm được sửa, số câu có đáp án đúng dài nhất giảm từ 24 xuống 10. Đây chỉ là chỉ báo về hình thức, không phải số đo độ khó.

Số câu trong toàn ngân hàng khớp các cụm cần xem xét giảm từ 156 xuống 126. Các cụm như “chỉ xét” có thể cần thiết để giới hạn một vấn đề pháp lý, nên không bị xóa hàng loạt. Không dùng bộ dò từ khóa để kết luận các câu còn lại đều có lỗi.

## Kiểm tra

- `node --test --test-reporter=tap tests/*.test.cjs`: **89/89 đạt**, 0 lỗi, 0 bỏ qua; lượt cuối khoảng 60,75 giây.
- Kiểm tra cú pháp JavaScript và `git diff --check`: đạt.
- Đầu ra toàn bộ kiểm thử: `reports/natural-language-polish-tests-2026-10-15.tap`.
- Có lượt kiểm tra 9.690 trường hợp chọn đáp án/chấm điểm và từ chối nộp trắng trong luyện tập trên toàn bộ 793 câu qua trình nạp thực tế.
- Có kiểm thử chặn nguồn cũ, khóa hoặc căn cứ bị đổi, ngày xác minh bị đổi, văn bản chưa khớp hash và trường hợp không tải được bản biên tập.
- Kiểm kê sau biên tập: `reports/natural-language-polish-audit-2026-10-15.json`.

Chưa đo độ khó bằng kết quả người làm thật và chưa kiểm thử trình duyệt thật. Không tuyên bố cả 793 câu đã đạt cùng một mức khó hoặc được tái kiểm định pháp lý trong đợt biên tập này.
