# Đợt tiếp 100 câu ngày 09/10/2026

Đã thêm **200 lời dẫn** cho **100 câu**: toàn bộ 79 COMP26 active, REFIN26-QT-021–025, REFIN26-DAT-001–015 và INH26-015. COMP26-DAT-002 archived giữ nguyên, không tính vào phạm vi này.

| Chỉ tiêu | Trước đợt | Sau đợt |
|---|---:|---:|
| Đã xử lý trong phạm vi 583 câu | 343 | 443 |
| Còn cần biến thể thực chất | 240 | 140 |
| Câu active | 594 | 594 |
| Câu active có ba lời dẫn | 354 | 454 |
| Chuỗi lời dẫn active | 1.302 | 1.502 |

Biến thể được viết từng ID, kết hợp quy tắc với hồ sơ hoặc lập luận cần xử lý: góp tài sản khác bán; DNTN khác công ty; tự định giá khác thuê thẩm định; ngưỡng đúng 35%/50%; phê duyệt khác đại diện ký; chữ ký khác nội dung kê khai; chứng thực hai người làm chứng khác công chứng; thời gian đào tạo khác tập sự; ký số cá nhân khác ký số tổ chức; cảnh báo dữ liệu khác quyết định ngăn chặn; đất thuê hằng năm khác trả một lần; thừa kế không được cấp giấy khác mất quyền hưởng giá trị.

Giữ các số 6/4 tỷ, 5/3 tỷ, 3,6 tỷ và 20 triệu khi chúng quyết định kết quả trong đáp án; giữ ba sáng lập viên, hai người đồng ý khi nhiễu nêu tỷ lệ đó. Các tình huống gia đình chỉ thay bối cảnh, không bỏ giả thiết chế độ tài sản, chủ nợ đồng ý, lỗi, năng lực lao động, số người thừa kế hoặc thời điểm hình thành tài sản.

Đã đối chiếu từng lời dẫn với cả bốn đáp án và điều khoản lưu. Khóa riêng, lý do quyết định và nguồn kiểm tra ở [bảng nhận xét 100 câu](../editorial/variant-batch-100-2026-10-09.json). Nội dung ở [79 cặp COMP26](../editorial/completion-variants-2026-10-09.json), [REFIN26](../editorial/refinement-variants-2026-10-09.json) và [INH26](../editorial/inheritance-variants-2026-10-09.json).

Kiểm tra nguồn chính thức chứng thực 753/VBHN-BTP năm 2026, Luật Doanh nghiệp 67/VBHN-VPQH năm 2025 và Đất đai 44/VBHN-VPQH năm 2026, cùng sổ điều khoản Công chứng, BLDS, HNGĐ đã lưu. Lời dẫn mới áp dụng tháng 10/2026; không áp sửa đổi Công chứng có hiệu lực 01/01/2027. Đây là rà soát biên tập và điều khoản viện dẫn, **không chứng nhận pháp lý toàn bộ ngân hàng**.

Đối chiếu Git trước–sau: đúng 100 bản ghi thay đổi, chỉ phần biến thể và audit; giữ nguyên lời dẫn gốc, ID, bốn đáp án, khóa, giải thích, căn cứ, nguồn, trạng thái và lastVerified. Chạy lại chương trình áp dụng không làm thay dữ liệu hoặc báo cáo (idempotent).

[Kiểm thử 56/56](variant-batch-100-tests-2026-10-09.tap) có kiểm tra riêng phạm vi 100 câu, 200 lời dẫn, khóa độc lập, giữ dữ liệu gốc, loại câu archived và danh sách 17 câu thừa kế còn lại. [Hồ sơ tích lũy](substantive-variants-2026-10-09.json) ghi 443 câu đã rà, 886 lời dẫn viết tích lũy và 140 ID chưa hoàn tất. Phần còn lại là 123 câu đề nhập và INH26-016–032.

[Dung lượng](variant-payload-2026-10-09.json): 11 tệp tải có 1.760.349 byte, tăng 89.860 byte. Gzip thử 231.248 byte, phân tích JSON trung bình 6,10 ms qua 50 vòng trên Node cục bộ. Không phải đo mạng, iPhone hoặc xác nhận nén máy chủ. Hồ sơ/biên tập không được ứng dụng tải khi làm đề.

[Kiểm kê ngân hàng](bank-audit-variants-2026-10-09.json) đã chạy lại; dấu hiệu cấu trúc hoặc tương đồng không tự là kết luận sai pháp lý. Kiểm thử Node/DOM giả lập không thay kiểm tra thao tác điện thoại. Dấu vân tay CC2 đổi khi ngân hàng đổi; nhóm cần tạo mã đề mới cho phiên bản này.
