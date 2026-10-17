# Thống kê ôn tập — 18/10/2026

Đã thêm thống kê riêng cho Ôn tập, dùng tên và số điện thoại như Thi thử.

- Lưu ngay sau mỗi câu đã chấm, kể cả chưa kết thúc buổi. Câu chưa chấm không được tính sai.
- Xem tổng lượt đã chấm, số câu khác nhau, lượt sai và tỷ lệ đúng. Theo từng chủ đề/Bài: số đúng, sai, tổng lượt, tỷ lệ sai và số câu khác nhau.
- Chủ đề nhiều lượt sai đứng trước, tỷ lệ sai phân biệt trường hợp cùng số lượt sai. Cảnh báo cỡ mẫu nhỏ khi dưới năm câu khác nhau; không coi vài câu là chẩn đoán chắc chắn điểm yếu.
- Nút Ôn lại các câu từng sai chỉ lấy câu còn đủ điều kiện trong ngân hàng. Xem lại đáp án không cộng lượt; ôn lại tạo lượt mới, kể cả khi sau đó làm đúng. Thống kê là tích lũy và có thể gồm nhiều lần làm cùng một câu.
- Xem 50 lượt chấm gần nhất, giữ bản chụp đề, lựa chọn, đáp án, giải thích và căn cứ tại lúc chấm. Tổng hợp chủ đề sử dụng toàn bộ lịch sử đã tải, không chỉ 50 lượt hiển thị.
- Đổi thiết bị dùng cùng số điện thoại sau khi đồng bộ thành công. Không phục dựng được các buổi ôn trước khi có tính năng này.
- Mất mạng có hàng chờ riêng trên thiết bị, cùng nút Gửi kết quả chưa lưu để gửi lại. Nếu chưa tải đủ lịch sử, màn hình ghi rõ thống kê chưa đầy đủ. Câu chờ gửi và đã đồng bộ trùng ID chỉ tính một lần.
- Điểm thi, lịch sử thi và bảng xếp hạng giữ nguyên. Bảng practice_answers riêng, không có trigger nối bảng xếp hạng.

## Cách xem

Vào **Thống kê ôn tập và thi thử** → nhập số điện thoại → chọn **Ôn tập** → **Xem thống kê**. Sau buổi ôn cũng có nút **Xem thống kê ôn tập của tôi**.

## Lưu dữ liệu và quyết định truy cập

Chủ dự án đã cho phép dùng số điện thoại không xác thực sau khi được giải thích: ai biết số đều có thể xem/thêm lịch sử. Không cấp quyền sửa/xóa các dòng đã lưu, không cho liệt kê toàn bộ khi không chỉ định số. Không coi số điện thoại là bí mật hoặc chứng cứ xác minh danh tính.

Đã áp dụng `supabase/practice-history.sql` trên dự án CongchungVND. RLS bật với hai policy SELECT/INSERT theo số, chỉ cấp các cột cần thiết; chỉ mục theo số, thời điểm, ID; duy nhất session_id + question_id để chống ghi trùng. SQL kiểm thử chạy trong giao dịch ROLLBACK, không để lại kết quả giả.

## Kiểm chứng

- 100/100 kiểm thử Node đạt, bao gồm 9.690 tình huống chấm điểm của 793 câu; TAP tại `reports/practice-statistics-tests-2026-10-18.tap`.
- 8 kiểm thử mới: lưu đúng một lần/bản chụp bất biến, hàng chờ offline và gửi lại cùng ID, lượt ôn mới, cộng gộp theo bài/chủ đề và khử trùng, phân trang/chỉ ghép số đang xem, thông báo thiếu dữ liệu, ngăn phản hồi cũ đè màn hình mới, ôn lại đúng người và tích hợp chấm câu/xem lại/ôn lại.
- SQL trên hệ thống thật đạt: đọc/ghi cùng số, chặn ghi sang số khác, không đọc khác số/không header, không sửa/xóa, ràng buộc chống trùng; xác nhận không có trigger bảng xếp hạng.
- Security advisor không phát sinh cảnh báo cho bảng mới; còn một thông tin có sẵn về bảng private.exam_leaderboard_profiles bật RLS không có policy.
- Không hoàn tất kiểm thử bằng trình duyệt thật: môi trường Playwright có thư viện nhưng thiếu Chromium. Kiểm thử giao diện/tương tác trên Node DOM harness và SQL đã chạy; không mô tả kết quả này là end-to-end trình duyệt.
