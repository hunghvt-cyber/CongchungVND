# Kết quả sửa lỗi và kiểm thử lại — 15/10/2026

## Kết quả

- `node --test --test-reporter=tap tests/*.test.cjs`: **87/87 đạt**, 0 lỗi, 0 bỏ qua; Node v24.19.0, khoảng 50,35 giây.
- 793 câu đang sử dụng qua trình nạp thực tế; 9.690 trường hợp chọn đáp án/chấm điểm ở hai chế độ, gồm từ chối nộp trắng trong luyện tập, không sai lệch so với khóa lưu. Đây không phải xác nhận lại tính đúng pháp lý của mọi khóa.
- Kiểm kê: 1.313 bản ghi kể cả kho lưu trữ, 793 hoạt động, 520 lưu trữ; không trùng mã hoặc câu dẫn đầu. Nhóm hoạt động không còn cờ giải thích ngắn.
- `git diff --check` và kiểm tra cú pháp JavaScript: đạt.

## Những gì đã sửa

1. Thay 4 biến thể đã bị loại nhưng xuất hiện lại; cập nhật bản trình bày và hash nguồn tương ứng.
2. Bổ sung 19 giải thích tổng bằng điều kiện pháp lý và dữ kiện cụ thể. Giữ nguyên phương án, khóa, trạng thái và ngày xác minh.
3. Thêm cầu nối phiên bản cho 191 bản ghi thay đổi sau mốc lịch sử. Kiểm thử chỉ được dùng bản cũ sau khi bản hiện tại khớp chính xác hash đã duyệt; thử sửa trái phép câu dẫn, khóa, giải thích, trạng thái và căn cứ đều bị từ chối.
4. Bổ sung chứng cứ Điều 296 BLDS cho HARD26-041 và ghi nhận phạm vi khoản 4 Điều 50 cho CAL26-027. Không sửa hồ sơ chứng cứ lịch sử hoặc tuyên bố tái kiểm định toàn bộ ngân hàng.
5. Kiểm thử hiển thị kiểm tra đầy đủ giải thích thật được mã hóa HTML và căn cứ, không bắt buộc nhãn “Gợi ý làm bài:”. Kiểm thử lịch sử vẫn kiểm tra bản lịch sử và khóa độc lập; kiểm thử hiện tại kiểm tra bản mới riêng.
6. Cố định hạt giống ngẫu nhiên trong môi trường kiểm thử, có thêm kiểm thử tái lập và đổi thứ tự khi đổi hạt giống. Không đổi cơ chế ngẫu nhiên của ứng dụng thật.

## Bằng chứng

- `reports/post-repair-tests-2026-10-15.tap`: toàn bộ đầu ra kiểm thử cuối cùng.
- `reports/post-repair-audit-2026-10-15.json`: kiểm kê hiện tại.
- `editorial/post-review-repairs-2026-10-15.json`: 23 bản ghi trước/sau chính xác.
- `editorial/editorial-version-bridge-2026-10-15.json`: hash và cầu nối lịch sử.
- `editorial/legal-evidence-supplement-2026-10-15.json`: phạm vi bổ sung căn cứ.

## Giới hạn

Đây là kiểm thử logic/HTML bằng môi trường DOM mô phỏng, không phải kiểm thử giao diện bằng trình duyệt thật hoặc chứng nhận pháp lý toàn bộ. Kiểm kê vẫn gắn cờ 490 câu có dưới ba cách hỏi theo quy tắc heuristic cũ; việc giữ tình huống một biến thể đã được duyệt không được tự sửa bằng sinh biến thể hàng loạt. Các cờ khác ngoài nhóm hoạt động thuộc kho lưu trữ và không được đưa lại vào bài làm. Báo cáo kiểm thử thất bại trước sửa được giữ nguyên để đối chiếu.
