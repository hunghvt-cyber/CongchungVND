# Tiến độ biến thể ngày 09/10/2026

**Hoàn tất phạm vi biến thể 583/583 câu; chưa chứng nhận kiểm định pháp lý toàn ngân hàng.**

Các nhóm đã xử lý: CC 93, SRC 14, VER26 98, DEP26 18, AUTH26 20, FAM26 26, INH26 32, REFIN26 80, COMP26 79 và đề nhập 123. Mỗi câu trong phạm vi có hai biến thể được biên soạn theo từng ID và đối chiếu với cả bốn đáp án, giải thích, điều khoản viện dẫn.

| Chỉ tiêu | Đầu phạm vi | Hiện tại |
|---|---:|---:|
| Câu active | 594 | 594 |
| Câu còn cần biên soạn biến thể | 583 | 0 |
| Câu có ba lời dẫn | 25 | 594 |
| Tổng chuỗi lời dẫn active | 644 | 1.782 |
| Biến thể viết tích lũy | 0 | 1.166 |
| Lời dẫn hình thức SRC được thay | 0 | 28 |

1.166 chuỗi viết mới gồm 28 chuỗi thay thế, tăng ròng 1.138 chuỗi. Có 11 câu ngoài phạm vi 583 đã đủ ba lời dẫn. Không tăng số câu độc lập. COMP26-DAT-002 đang archived không được xử lý.

Các đợt bổ sung gần đây được ghi tại `variant-batch-40-2026-10-09.md`, `variant-batch-60-2026-10-09.md`, `variant-batch-100-2026-10-09.md`, `variant-batch-next-100-2026-10-09.md` và [đợt cuối 40 câu](variant-final-40-2026-10-09.md). Đợt cuối thêm 80 lời dẫn và sửa riêng năm giải thích IMP-T60-023, 038, 039, 071, 085 theo yêu cầu Madam An. Giữ nguyên câu gốc, bốn đáp án, khóa, căn cứ, nguồn, trạng thái và lastVerified của cả 40 câu.

CC-034 từng được bổ sung giả thiết **đã từng hành nghề** ở đợt trước để phân biệt đúng trường hợp; đợt cuối không sửa câu này.

## Hồ sơ và giới hạn rà soát

`substantive-variants-2026-10-09.json` giữ bản trước chỉnh, khóa đối chiếu, nhận xét và liên kết chứng cứ theo từng ID; `remainingIds` hiện rỗng. Trạng thái là `VARIANT_SCOPE_COMPLETE_LEGAL_REVIEW_NOT_CERTIFIED`, không phải READY. Kế hoạch giữ `allActiveLegallyRecertified: false`.

Năm giải thích được sửa có hồ sơ trước–sau đầy đủ tại `editorial/exam-explanation-repairs-final-2026-10-09.json`. Hồ sơ hoãn ở đợt 100 trước được giữ như lịch sử và ghi nhận đã giải quyết ở đợt cuối.

Đợt cuối tải lại chín nguồn chính thức liên quan; HTTP 200 và SHA-256 của các PDF khớp hồ sơ chứng cứ. Xem `variant-final-40-source-checks-2026-10-09.json` và `exam-legal-evidence-2026.json`. Đối chiếu gồm Luật Công chứng 46/2024/QH15, BLDS, VBHN đất đai 44/2026, HNGĐ 121/2025, Nhà ở 79/2026, Lao động 18/2026, KDBĐS 06/2025, TT06/2025 và NĐ21/2021. Không áp dụng Luật 04/2026/QH16 có hiệu lực từ 01/01/2027 vào tình huống tháng 10/2026.

Đây là rà soát biên tập và điều khoản viện dẫn. Xác minh nguồn cùng kiểm thử cấu trúc không chứng nhận đã kiểm tra mọi sửa đổi hoặc pháp lý toàn bộ 594 câu.

## Kiểm thử và dung lượng

Đợt cuối đạt **59/59 kiểm thử**, lưu tại `variant-final-40-tests-2026-10-09.tap`. Đối chiếu trước–sau xác nhận đúng 40 bản ghi thay đổi, đúng năm giải thích được sửa, 543 quyết định trước giữ nguyên và áp dụng lại không đổi dữ liệu/báo cáo. Xem `variant-final-40-preservation-2026-10-09.json`. Kiểm kê tại `bank-audit-variants-2026-10-09.json`; đây là kiểm thử Node và DOM giả lập, chưa thay kiểm thử thao tác thật trên điện thoại.

Ứng dụng tải 11 file ngân hàng: **1.892.301 byte**, khoảng 1,89 MB. Gzip thử từng file tổng 246.707 byte; không khẳng định máy chủ nén như vậy. Phân tích JSON trung bình khoảng 3,82 ms qua 50 vòng trên Node24 cục bộ, không phải thời gian mạng hoặc iPhone. `reports/` và `editorial/` không được tải khi làm đề.

Nội dung mới đổi dấu vân tay mã CC2; nhóm học cần tạo mã mới cho phiên bản ngân hàng này.
