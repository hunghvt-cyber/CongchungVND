# Tiến độ biến thể ngày 09/10/2026

**Chưa nghiệm thu toàn bộ phạm vi 583 câu.**

Đã biên soạn và đối chiếu với bộ bốn đáp án, giải thích, điều khoản lưu trong hồ sơ nguồn cho 283 câu: 93 CC, 14 SRC, 98 VER26, 18 DEP26, 20 AUTH26, 26 FAM26 và 14 INH26. Hai biến thể mỗi câu được viết theo từng ID, kết hợp câu hỏi quy tắc và tình huống nhận diện điều kiện hoặc lập luận sai. Không dùng phép thêm tiền tố vào cùng lời dẫn để đủ số lượng.

| Chỉ tiêu | Trước đợt này | Sau đợt này |
|---|---:|---:|
| Câu active | 594 | 594 |
| Câu thuộc phạm vi còn cần biên soạn biến thể | 583 | 300 |
| Câu lưu ba lời dẫn | 25 | 294 |
| Tổng chuỗi lời dẫn active | 644 | 1.182 |
| Biến thể mới viết trong đợt | 0 | 566 |
| Lời dẫn hình thức SRC được thay | 0 | 28 |

566 chuỗi mới bao gồm 28 chuỗi thay thế, nên tăng ròng 538 chuỗi. Trong đó đợt tiếp theo yêu cầu của Madam An xử lý 40 câu FAM26-001–026 và INH26-001–014, thêm 80 lời dẫn; xem `variant-batch-40-2026-10-09.md` và bảng nhận xét từng câu tại `editorial/variant-batch-40-2026-10-09.json`. Không nhập thêm câu độc lập, không loại câu hoặc thay bộ đáp án trong đợt này.

CC-034 được bổ sung giả thiết **đã từng hành nghề** ở cả câu gốc và hai biến thể. Luật sửa đổi tách người hiện không hành nghề nhưng đã từng hành nghề khỏi người được bổ nhiệm chưa từng hành nghề; câu cũ thiếu giới hạn này.

## Hồ sơ và giới hạn kiểm định

`substantive-variants-2026-10-09.json` giữ bản trước chỉnh của từng câu, bộ đáp án, căn cứ, đường dẫn hồ sơ điều khoản, kết luận giải thích, khóa được đối chiếu cho cả ba lời dẫn và danh sách 300 ID còn lại. Các tệp `editorial/` giữ nội dung được biên soạn riêng trước khi áp dụng.

Đã kiểm tra nguồn công bố chính thức về Luật Công chứng 46/2024/QH15, ngày hiệu lực Luật 04/2026/QH16, BLDS 91/2015/QH13, VBHN 121/VBHN-VPQH về HNGĐ, VBHN 44/VBHN-VPQH về đất đai, TT06/2025, NĐ21/2021 và khoản 5 Điều 23 Luật KDBĐS. Hồ sơ điều khoản đã lưu được dùng để đối chiếu biến thể. Một số URL văn bản gốc không đọc được qua công cụ; với luật sửa đổi đã tìm thêm bản ký tại Cổng Chính phủ. Không coi chỉ có đường dẫn hoặc trạng thái còn hiệu lực ở trang thuộc tính là đã kiểm định tất cả điều khoản, văn bản chuyên ngành và sửa đổi đến ngày hiện tại.

Trạng thái đợt là **rà soát biên tập cùng điều khoản viện dẫn**, không tự gán READY hoặc chứng nhận đã kiểm định pháp lý toàn bộ 594 câu. Việc chương trình kiểm tra đủ ba chuỗi, khóa, ID và liên kết chứng cứ không thay đánh giá pháp lý từng phương án. 300 câu còn lại thuộc các tệp đề nhập, thừa kế, completion và refinement; phạm vi pháp lý tổng thể vẫn cần hoàn thiện.

## Dung lượng và kiểm thử

Ứng dụng tải 11 tệp ngân hàng, tổng 1.611.978 byte (khoảng 1,61 MB thập phân). Tổng gzip thử nghiệm từng tệp: 209.892 byte; đây là ước lượng khả năng nén, không khẳng định máy chủ đang nén như vậy. Phân tích JSON toàn bộ 11 tệp trung bình khoảng 3,99 ms trên Node cục bộ qua 50 vòng; không phải đo thời gian mạng hoặc iPhone.

Ứng dụng không tải các tệp hồ sơ kiểm định hoặc `editorial/`. Vì thế hồ sơ dài không làm tăng dung lượng ngân hàng tải khi làm đề. Các biến thể dùng chung đáp án, giải thích và căn cứ để không nhân ba toàn bộ câu.

Kết quả kiểm thử cuối đợt được lưu tại `variant-batch-40-tests-2026-10-09.tap`; kiểm kê cấu trúc và các dấu hiệu cần rà soát tại `bank-audit-variants-2026-10-09.json`. Đây là kiểm thử Node và DOM giả lập, không phải chứng nhận thao tác thật trên điện thoại hoặc kiểm thử máy chủ phản hồi thực.

Mã CC2 ghi dấu vân tay ngân hàng. Cập nhật nội dung làm mã của phiên bản dữ liệu trước bị từ chối theo cơ chế đã có; nhóm học cần tạo mã mới khi dùng ngân hàng mới. Mã mới được kiểm thử tái tạo cùng câu, cách hỏi và thứ tự đáp án; lịch sử chống trùng không thay đề nhập bằng mã.
