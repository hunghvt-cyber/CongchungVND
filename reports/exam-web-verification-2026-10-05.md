# Kiểm tra tích hợp hai đề — 05/10/2026

Bản mã và dữ liệu đã kiểm tra: `ab65527e089d4d5ce88e91743903c40db395fe63`.

- 29/29 test Node đạt: JSON/ID/single-key, truy vết 151 mục, evidence, bộ lọc trạng thái, trộn đề, mã đề, chấm điểm, giải thích/căn cứ, snapshot kết quả và lưu offline.
- Các câu nhập chạy được ở cả part 1 và 2; archived không vào đề.
- Không sửa progress.js, khóa localStorage, schema kết quả hoặc dữ liệu người học.
- Toàn ngân hàng: 846 bản ghi, 304 active, 36 review, 506 archived. Không có trùng ID, cờ cấu trúc active hay cặp câu dẫn active gần trùng ở ngưỡng so khớp 0,78. So khớp tự động không thay rà năng lực pháp lý; đã bỏ thêm 3 câu trùng năng lực với ngân hàng cũ.
- GitHub Pages workflow 37266760771, `pages build and deployment`: success.

## Kiểm tra trên trình duyệt

Trang: https://hunghvt-cyber.github.io/CongchungVND/

1. Tải lại trang sau triển khai; setup hiển thị **304 câu được phép luyện/thi**, 42 bản ghi tải về chưa đủ điều kiện. Số 42 gồm review và archived trong 346 bản ghi app tải; không bao gồm 500 EXP archived không được tải.
2. Bắt đầu ôn 5 câu; câu đầu lấy từ hai đề (`IMP-T60-036`, phân biệt nhà ở riêng lẻ và căn hộ chung cư).
3. Chọn “Căn hộ trong nhà chung cư”, kiểm tra: hiện **✓ Đúng**, điểm đúng tăng 0 → 1, đáp án khóa, giải thích và gợi ý hiện đầy đủ. AX tree có Điều 2 khoản 2 và khoản 3 Luật Nhà ở/VBHN 79 năm 2026, hai liên kết văn bản chính thức.
4. Mở thi thử Bài 2, 5 câu, 15 phút; mã đề được sinh và đồng hồ giảm 15:00 → 14:53.
5. Chọn đáp án câu thừa kế, chuyển sang câu mới từ đề (`IMP-T60-029`, thuê khoán gia súc); chọn đáp án rồi quay lại. Bộ đếm “Đã làm” bằng 2, lựa chọn 200 triệu của câu đầu vẫn có class `selected` trên DOM.
6. Thoát bài để dừng đồng hồ và trở về setup ôn tập. Không nộp kết quả thử vào hệ thống người học. Chấm điểm toàn đề, snapshot và gửi/lưu offline được kiểm tra trong Node.

Log quan sát có lỗi từ extension trình duyệt, không phải bằng chứng lỗi ứng dụng. Không lấy kiểm tra giao diện này làm kết luận mọi kết nối backend đã được kiểm tra trên production.

[Ảnh câu mới được chấm đúng và hiển thị giải thích](exam-practice-proof-1791177303987.jpg)
