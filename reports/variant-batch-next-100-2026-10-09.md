# Đợt tiếp 100/140 câu ngày 09/10/2026

Đã áp dụng **200 lời dẫn thực chất cho đúng 100 câu**: 17 INH26-016–032 và 83 câu trong `data/imported-exams-2026.json`. Đã xử lý tích lũy **543/583**, còn **40 câu đề nhập**. Không tăng câu độc lập hoặc tự đánh dấu READY.

| Chỉ tiêu | Trước | Sau |
|---|---:|---:|
| Câu đã xử lý trong phạm vi 583 | 443 | 543 |
| Câu còn cần biến thể | 140 | 40 |
| Câu active | 594 | 594 |
| Câu active có ba lời dẫn | 454 | 554 |
| Chuỗi lời dẫn active | 1.502 | 1.702 |
| Biến thể áp dụng viết tích lũy, gồm 28 thay thế | 886 | 1.086 |

Danh sách 100 ID được lưu trước khi sửa và có lịch sử điều chỉnh ở [phạm vi](../editorial/variant-batch-next-100-scope-2026-10-09.json). Năm câu hoãn vì giải thích cần sửa riêng, không tính hoàn thành: IMP-T60-038, IMP-T60-023, IMP-T60-039, IMP-T60-071, IMP-T60-085. Câu đầu còn ghi mức trả trước thông thường 20% không có trong khoản 22 Điều 2 VBHN Nhà ở 79/2026 đang lưu; bốn câu sau còn nhận xét chữ đáp án của bộ nhiễu cũ. Thay tương ứng bằng IMP-T60-096, IMP-T60-097, IMP-T60-099, IMP-T60-100, IMP-SEP24-005. Cả năm bản ghi hoãn giữ nguyên toàn bộ so với commit gốc; xem [sổ việc cần sửa](../editorial/variant-next-100-follow-up-2026-10-09.json). Bốn cặp nháp chưa áp dụng được lưu riêng, không tính vào 200 lời dẫn.

Hai biến thể mỗi câu được viết theo vấn đề cụ thể: yêu cầu không đúng của người hưởng, kiểm tra hồ sơ, phân loại quan hệ, phân biệt mốc thời gian hoặc quy tắc với ngoại lệ. Giữ tên, số liệu, loại tài sản và giả thiết quyết định đáp án. Thừa kế phân biệt hiện vật/tỷ lệ, giá lúc chia/giá hiện tại, thế vị sau khi phần di chúc mất hiệu lực, nợ người chết/hoàn trả do bác quyền, giám hộ/giám sát và khiếu nại trước công chứng. Đề nhập phân biệt đối kháng/hiệu lực hợp đồng, quyền cầm giữ/đối kháng cầm giữ, thuê/thuê mua, chủ hộ/đại diện, cơ quan chấp thuận/người ký, và quy tắc lao động/ngoại lệ.

[Bảng nhận xét](../editorial/variant-batch-next-100-2026-10-09.json) giữ khóa được đọc và ghi riêng cùng lý do chấp nhận hoặc loại cả bốn phương án. Nội dung cặp lời dẫn ở [thừa kế](../editorial/inheritance-variants-2026-10-09.json) và [đề nhập](../editorial/exams-variants-2026-10-09.json). Script áp dụng được cập nhật phạm vi và số lượng, giữ kiểm tra độc lập khóa, nguồn chứng cứ, toàn bộ trường gốc và trùng lời dẫn; không chạy script sinh ngân hàng cũ.

[Nguồn kiểm tra](variant-next-100-source-checks-2026-10-09.json): tải lại 10 nguồn công bố chính thức và các PDF tương ứng, SHA-256 đều khớp hồ sơ đã lưu. Gồm BLDS, Công chứng 46/2024, NĐ104/2025, NĐ21/2021, TT06/2025, VBHN Đất đai 44/2026, Doanh nghiệp 67/2025, HNGĐ 121/2025, Nhà ở 79/2026 và Lao động 18/2026. Nội dung điều khoản đã được đọc từ hồ sơ để đối chiếu từng câu. Không áp Luật Công chứng sửa đổi 04/2026 có hiệu lực 01/01/2027 vào tháng 10/2026. Xác nhận PDF khớp không chứng minh đã tìm hết mọi sửa đổi hoặc kiểm định toàn bộ ngân hàng.

[Đối chiếu commit gốc](variant-next-100-preservation-2026-10-09.json) `744d8a6f5e72deafa061e9c15bd338e3f2e0f89d`: đúng 100 bản ghi thay, chỉ biến thể và audit; giữ lời dẫn gốc, ID, bốn đáp án, khóa, giải thích, căn cứ, nguồn, trạng thái, lastVerified và các trường khác. Mọi bản ghi ngân hàng ngoài phạm vi cùng 443 quyết định cũ đều không đổi. Chạy lại áp dụng không đổi dữ liệu/báo cáo.

[Kiểm thử 57/57](variant-batch-next-100-tests-2026-10-09.tap), gồm kiểm tra phạm vi, bản ghi nguyên vẹn, khóa độc lập, 5 câu hoãn, tổng 543/40/594/1.702 và các luồng mã đề/thi/góp ý/progress. Lệnh dùng Node24:

```sh
node --test --test-isolation=none --test-reporter=tap tests/*.test.cjs
python scripts/audit-bank.py bank-audit-variants-2026-10-09.json
git diff --check
```

Lệnh `node --test tests/*.test.cjs` cũng đạt ở lượt trước điều chỉnh phạm vi, nhưng môi trường Node24 chỉ xuất ba kết quả tệp; dùng `--test-isolation=none` để lưu rõ 57 ca kiểm thử trên phạm vi cuối. Kiểm thử Node/DOM giả lập không thay kiểm tra thao tác thật trên điện thoại. Kiểm kê còn 40 câu cần biến thể; các cờ tương đồng/giải thích ngắn là dấu hiệu cần xem, không tự kết luận pháp lý.

[Dung lượng](variant-payload-2026-10-09.json): app tải 11 tệp, 1.853.353 byte, tăng 93.004 byte. Gzip thử 240.880 byte; parse JSON trung bình 5,45 ms qua 50 vòng Node24 cục bộ. Không phải đo mạng/iPhone hoặc xác nhận máy chủ nén. Hồ sơ reports/editorial không được tải khi làm đề. Dấu vân tay CC2 đổi; nhóm cần mã đề mới cho bản ngân hàng này.

Trước đợt, GitHub main đúng commit gốc và GitHub Pages build thành công tại [run 37921652816](https://github.com/hunghvt-cyber/CongchungVND/actions/runs/37921652816). File COMP26 tải trực tiếp từ website khớp từng byte với repo, giải quyết nghi ngờ dữ liệu cũ ở lần kiểm tra ngay sau đợt trước. Việc triển khai đợt mới phải được xác nhận riêng sau đẩy.

Trạng thái là **rà soát biên tập cùng điều khoản viện dẫn**, chưa nghiệm thu pháp lý toàn bộ 594 câu. Danh sách 40 ID còn lại nằm trong `remainingIds` của [hồ sơ tích lũy](substantive-variants-2026-10-09.json); 5 câu hoãn cần sửa giải thích trước khi viết/áp dụng biến thể.
