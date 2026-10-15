# Rà câu còn gượng và nhiễu yếu — lượt tiếp theo, 15/10/2026

Đã biên tập thủ công thêm **40 câu, 104 cách hỏi**, nằm ngoài 40 câu của lượt trước. Bản biên tập tích lũy hiện có 80 câu, 184 cách hỏi. 713 câu khác không thay đổi trong hai lượt này; đây không phải kết luận rằng tất cả đã đạt chất lượng đồng đều.

## Những điểm sửa chính

- Bỏ lời dẫn yêu cầu người làm phân biệt các quy tắc đã được gọi tên sẵn; đưa câu hỏi về thao tác và kết quả xử lý hồ sơ.
- Nhiễu tập trung vào nhầm thời điểm, loại giấy tờ, phạm vi đại diện, chấp thuận nội bộ và thủ tục thực hiện; giảm lựa chọn sai vì lý do không liên quan.
- Giữ các dữ kiện cần thiết để kết luận: kết quả tập sự đã bị hủy, biện pháp khẩn cấp còn hiệu lực, hình thức việc nhập tài sản chưa hoàn tất, phạm vi chỉ nộp hồ sơ và các thời hạn.
- Giữ mốc áp dụng từ 01/01/2027 cho CC-033, CC-099; không đưa quy định tương lai vào tình huống áp dụng tháng 10/2026.
- IMP-SEP24-037 dùng bốn lựa chọn là số tiền; lý do tính sai nằm trong giải thích sau khi trả lời. Người làm tự xác định phần cọc đã nhận phải tính vào giới hạn thanh toán đầu.
- DEP26-002 hỏi riêng 120 triệu ký cược, tránh suy kết quả xử lý khoản này thành kết quả của mọi nghĩa vụ bồi thường liên quan chiếc xe.
- Viết lại các giải thích còn dùng ghi chú ngắn như mã luật, mã nhánh thành đoạn dành cho người học.

Trong nhóm 40 câu mới, số câu có đáp án đúng dài nhất giảm từ **29 xuống 10**. Đây là chỉ báo về cách trình bày, không phải độ khó thực nghiệm hoặc bằng chứng mọi nhiễu đã đủ sức phân loại người làm.

## Bảo toàn nội dung đã duyệt

Giữ nguyên mã, bài, loại, khóa, trạng thái, nguồn, căn cứ pháp lý, ngày xác minh và số cách hỏi. Toàn bộ 40 bản biên tập trước vẫn giữ hash trước/sau đã lưu trong báo cáo lượt đầu. Hồ sơ pháp lý và bản thảo lượt đầu không bị sửa.

Không thêm lớp tải dữ liệu mới. Mở rộng bản biên tập hiện có lên 80 câu; trình nạp tiếp tục kiểm tra nguồn, hash và phạm vi trường được phép biên tập. Kiểm thử lịch sử vẫn đối chiếu phiên bản cũ, còn việc chấm điểm dùng ngân hàng hiện hành.

## Kết quả kiểm tra

- `node --test --test-reporter=tap tests/*.test.cjs`: **90/90 đạt**, 0 lỗi, 0 bỏ qua; khoảng 54,38 giây.
- 9.690 trường hợp chọn đáp án/chấm điểm, kể cả từ chối nộp trắng trong luyện tập, trên toàn bộ 793 câu đang dùng qua trình nạp thực tế.
- Kiểm thử mới xác nhận nhóm thêm có đúng 40 mã riêng, 104 cách hỏi và 40 câu trước giữ nguyên hash. Có đối chiếu độc lập phép tính 30% × 3 tỷ − 150 triệu = 750 triệu cho IMP-SEP24-037.
- Kiểm kê sau sửa: 793 câu hoạt động, không trùng mã hoặc câu dẫn đầu, không có cờ giải thích ngắn trong nhóm hoạt động. Cờ dưới ba biến thể vẫn được giữ theo thiết kế tình huống đã duyệt.
- Kiểm tra cú pháp bản thảo và `git diff --check`: đạt.

## Tệp đối chiếu

- `editorial/natural-language-polish-next-2026-10-15.cjs`: bản thảo thủ công lượt mới, lý do sửa và giải thích nhiễu.
- `data/editorial-polish-2026.json`: bản tích lũy đưa vào ứng dụng.
- `reports/natural-language-polish-next-2026-10-15.json`: phạm vi, 40 mã mới và hash phiên bản.
- `reports/natural-language-polish-next-tests-2026-10-15.tap`: toàn bộ đầu ra kiểm thử.
- `reports/natural-language-polish-next-audit-2026-10-15.json`: kết quả kiểm kê.

Đây là lượt biên tập nội dung và kiểm thử logic/HTML bằng DOM mô phỏng. Chưa đo độ khó qua người làm thật, chưa kiểm thử trình duyệt thật và không tái chứng nhận pháp lý toàn ngân hàng trong lượt này.
