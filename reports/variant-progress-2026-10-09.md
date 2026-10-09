# Tiến độ biến thể ngày 09/10/2026

**Chưa nghiệm thu toàn bộ phạm vi 583 câu.**

Đã biên soạn và đối chiếu với bộ bốn đáp án, giải thích, điều khoản lưu trong hồ sơ nguồn cho 443 câu: 93 CC, 14 SRC, 98 VER26, 18 DEP26, 20 AUTH26, 26 FAM26, 15 INH26, 80 REFIN26 và 79 COMP26. Hai biến thể mỗi câu được viết theo từng ID, kết hợp câu hỏi quy tắc và tình huống nhận diện điều kiện hoặc lập luận sai. Không dùng phép thêm tiền tố vào cùng lời dẫn để đủ số lượng.

| Chỉ tiêu | Trước đợt này | Sau đợt này |
|---|---:|---:|
| Câu active | 594 | 594 |
| Câu thuộc phạm vi còn cần biên soạn biến thể | 583 | 140 |
| Câu lưu ba lời dẫn | 25 | 454 |
| Tổng chuỗi lời dẫn active | 644 | 1.502 |
| Biến thể mới viết tích lũy | 0 | 886 |
| Lời dẫn hình thức SRC được thay | 0 | 28 |

886 chuỗi mới bao gồm 28 chuỗi thay thế, nên tăng ròng 858 chuỗi. Các đợt tiếp theo yêu cầu của Madam An gồm 40 câu FAM26-001–026 và INH26-001–014 (80 lời dẫn), 60 câu REFIN26-CC-001–040 và REFIN26-QT-001–020 (120 lời dẫn), rồi 100 câu: 79 COMP26 active, 20 REFIN26 còn lại và INH26-015 (200 lời dẫn). Xem `variant-batch-40-2026-10-09.md`, `variant-batch-60-2026-10-09.md`, `variant-batch-100-2026-10-09.md` và các bảng nhận xét từng câu cùng tên trong `editorial/`. COMP26-DAT-002 đang archived không được xử lý. Không nhập thêm câu độc lập, không loại câu hoặc thay bộ đáp án trong các đợt này.

CC-034 được bổ sung giả thiết **đã từng hành nghề** ở cả câu gốc và hai biến thể. Luật sửa đổi tách người hiện không hành nghề nhưng đã từng hành nghề khỏi người được bổ nhiệm chưa từng hành nghề; câu cũ thiếu giới hạn này.

## Hồ sơ và giới hạn kiểm định

`substantive-variants-2026-10-09.json` giữ bản trước chỉnh của từng câu, bộ đáp án, căn cứ, đường dẫn hồ sơ điều khoản, kết luận giải thích, khóa được đối chiếu cho cả ba lời dẫn và danh sách 140 ID còn lại. Các tệp `editorial/` giữ nội dung được biên soạn riêng trước khi áp dụng.

Đã kiểm tra nguồn công bố chính thức về Luật Công chứng 46/2024/QH15, ngày hiệu lực Luật 04/2026/QH16, BLDS 91/2015/QH13, VBHN 121/VBHN-VPQH về HNGĐ, VBHN 44/VBHN-VPQH về đất đai, TT06/2025, NĐ21/2021 và khoản 5 Điều 23 Luật KDBĐS. Hồ sơ điều khoản đã lưu được dùng để đối chiếu biến thể. Một số URL văn bản gốc không đọc được qua công cụ; với luật sửa đổi đã tìm thêm bản ký tại Cổng Chính phủ. Không coi chỉ có đường dẫn hoặc trạng thái còn hiệu lực ở trang thuộc tính là đã kiểm định tất cả điều khoản, văn bản chuyên ngành và sửa đổi đến ngày hiện tại.

Đợt 100 câu còn kiểm tra bản hợp nhất chứng thực 753/VBHN-BTP năm 2026 và Luật Doanh nghiệp 67/VBHN-VPQH năm 2025; đọc các điều khoản trong sổ completion/refinement và đối chiếu từng khóa. Không nhầm văn bản trùng số khác năm hoặc văn bản liên quan ở cuối trang với sửa đổi của luật đang xét.

Trạng thái đợt là **rà soát biên tập cùng điều khoản viện dẫn**, không tự gán READY hoặc chứng nhận đã kiểm định pháp lý toàn bộ 594 câu. Việc chương trình kiểm tra đủ ba chuỗi, khóa, ID và liên kết chứng cứ không thay đánh giá pháp lý từng phương án. 140 câu còn lại gồm 123 câu đề nhập và 17 câu thừa kế INH26-016–032; phạm vi pháp lý tổng thể vẫn cần hoàn thiện.

## Dung lượng và kiểm thử

Ứng dụng tải 11 tệp ngân hàng, tổng 1.760.349 byte (khoảng 1,76 MB thập phân). Tổng gzip thử nghiệm từng tệp: 231.248 byte; đây là ước lượng khả năng nén, không khẳng định máy chủ đang nén như vậy. Phân tích JSON toàn bộ 11 tệp trung bình khoảng 6,10 ms trên Node cục bộ qua 50 vòng; không phải đo thời gian mạng hoặc iPhone.

Ứng dụng không tải các tệp hồ sơ kiểm định hoặc `editorial/`. Vì thế hồ sơ dài không làm tăng dung lượng ngân hàng tải khi làm đề. Các biến thể dùng chung đáp án, giải thích và căn cứ để không nhân ba toàn bộ câu.

Kết quả kiểm thử cuối đợt: 56/56, lưu tại `variant-batch-100-tests-2026-10-09.tap`; kiểm kê cấu trúc và các dấu hiệu cần rà soát tại `bank-audit-variants-2026-10-09.json`. Đây là kiểm thử Node và DOM giả lập, không phải chứng nhận thao tác thật trên điện thoại hoặc kiểm thử máy chủ phản hồi thực.

Mã CC2 ghi dấu vân tay ngân hàng. Cập nhật nội dung làm mã của phiên bản dữ liệu trước bị từ chối theo cơ chế đã có; nhóm học cần tạo mã mới khi dùng ngân hàng mới. Mã mới được kiểm thử tái tạo cùng câu, cách hỏi và thứ tự đáp án; lịch sử chống trùng không thay đề nhập bằng mã.
