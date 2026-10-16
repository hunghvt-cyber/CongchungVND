# Chốt kiểm thử và rà pháp lý — 16/10/2026

## Kiểm thử

Đạt **92/92** kiểm thử Node; **9.690** ca chấm điểm trên **793** câu không lệch khóa. Đã lưu TAP đầy đủ. Kiểm toán không trùng ID. Đây là DOM harness/mạng giả lập, chưa chạy trình duyệt thật hoặc kiểm thử SQL trên cơ sở dữ liệu.

Lượt trước có 91/92 đạt do bản thảo completion-variants bị cắt cụt. Phần thiếu đã được khôi phục đúng bản Git, không sửa ý nghĩa; bản chạy hiện tại đạt đủ 92.

## Pháp lý

Đã đối chiếu 30 câu ưu tiên, chưa xác định cần đổi khóa. Hai câu cần làm rõ: CC-015 dùng thuật ngữ năng lực hành vi dân sự; CC-023 ghi rõ tên giấy chứng nhận kết quả kiểm tra tập sự. Không coi kết quả này là kiểm định toàn bộ ngân hàng. Hồ sơ JSON lưu điều khoản, nguồn, hạn chế truy xuất và hash từng câu.

### Ưu tiên khẩn: DEP26-006

Nguồn của Tạp chí TAND cho biết Nghị quyết 03/2026/NQ-HĐTP có hiệu lực 15/10/2026 và có hướng dẫn giới hạn mức phạt cọc theo giá trị hợp đồng. Câu DEP26-006 ghi chung tháng 10/2026, thiếu giá trị hợp đồng nhưng kết luận cố định 1,2 tỷ. Đây là rủi ro cần đối chiếu bản gốc và thời điểm áp dụng, chưa phải kết luận khóa B sai trong mọi trường hợp. Không tự đổi khóa hoặc trạng thái dựa riêng trên bài giới thiệu.

Nguồn phát hiện: [Tạp chí TAND](https://www.tapchitoaan.vn/nghi-quyet-cua-hoi-dong-tham-phan-tandtc-huong-dan-ap-dung-phap-luat-trong-giai-quyet-tranh-chap-ve-dat-coc16557.html).

Đã lập hàng đợi 25 câu có chủ đề/căn cứ liên quan cọc để tiếp tục rà; đây là danh sách ứng viên, chưa phải số câu sai. Chưa sửa dữ liệu/nguyên tắc chấm điểm trong lượt này. Các hồ sơ kiểm định cũ và lastVerified được giữ nguyên.
