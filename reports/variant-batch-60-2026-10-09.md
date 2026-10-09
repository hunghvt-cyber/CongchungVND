# Đợt tiếp 60 câu ngày 09/10/2026

Đã viết thêm **120 lời dẫn** cho **60 câu**: 40 câu REFIN26-CC-001–040 về tổ chức, hành nghề và 20 câu REFIN26-QT-001–020 về thủ tục công chứng. Mỗi câu có ba lời dẫn dùng chung bốn đáp án, giải thích và căn cứ.

| Chỉ tiêu | Trước đợt | Sau đợt |
|---|---:|---:|
| Đã xử lý trong phạm vi 583 câu | 283 | 343 |
| Còn cần biến thể thực chất | 300 | 240 |
| Tổng câu active | 594 | 594 |
| Câu active có ba lời dẫn | 294 | 354 |
| Tổng chuỗi lời dẫn active | 1.182 | 1.302 |

Các lời dẫn mới dùng phân biệt điều kiện và tình huống nghiệp vụ: nội quy biểu quyết theo vốn, tuyển CCV theo hợp đồng, giấy đăng ký bị rách, rút vốn chưa đủ thời hạn, tiếp nhận thừa kế vào hợp danh chỉ có 2/4 người đồng ý, tạm ngừng do một phần CCV bị đình chỉ, rà soát hồ sơ, làm chứng không nghe được, bổ sung lời chứng và chuyển giao di chúc khi giải thể. Không chỉ thêm tiền tố cho câu gốc.

Đã rà lại từng lời dẫn với cả bốn đáp án và điều khoản viện dẫn. Các giả thiết quyết định được giữ rõ: loại Văn phòng hợp danh/DNTN; rút vốn tự nguyện khác mất thành viên do chết hoặc miễn nhiệm; chuyển toàn bộ vốn khác giao dịch nội bộ; tạm ngừng bất khả kháng khác đình chỉ toàn bộ CCV; chính bên giao dịch khác người liên quan xin bản sao; công chứng giấy khác điện tử. Câu REFIN26-CC-020 giữ giá trị vốn 900 triệu và nghĩa vụ 200 triệu để bốn phương án tương thích.

Các tình tiết thay đổi vẫn dẫn đến cùng khóa. Chẳng hạn, một hoặc hai trong ba/bốn CCV bị đình chỉ đều chưa phải toàn bộ; chết, Tòa tuyên chết hoặc miễn nhiệm thuộc nhánh bổ sung người ở khoản 2 Điều 33; người làm chứng không đọc hoặc không nghe được đều không đáp ứng điều kiện đang xét. Không dùng sự kiện trở ngại khách quan ở biến thể CC-032 vì đáp án hiện có nêu riêng bất khả kháng.

Giữ nguyên ID, số câu active, bốn đáp án, khóa, giải thích, căn cứ, nguồn và `lastVerified`. Mọi lời dẫn mới ghi **Tháng 10/2026**. Ngày rà soát biến thể được lưu riêng trong `audit`; không biến lần sửa lời dẫn thành một chứng nhận mới cho toàn bộ ngân hàng.

## Hồ sơ và kiểm tra

- [120 lời dẫn biên soạn theo ID ở mốc đợt 60](https://github.com/hunghvt-cyber/CongchungVND/blob/251932916a9ea5f1422338a82bf734b3fe482960/editorial/refinement-variants-2026-10-09.json).
- [Khóa đối chiếu, nhận xét 60 câu và nguồn chính thức](../editorial/variant-batch-60-2026-10-09.json).
- [Hồ sơ cùng bản trước chỉnh và 240 ID còn lại ở mốc đợt 60](https://github.com/hunghvt-cyber/CongchungVND/blob/251932916a9ea5f1422338a82bf734b3fe482960/reports/substantive-variants-2026-10-09.json).
- [Chứng cứ điều khoản gốc của REFIN26](refinement-legal-evidence-2026.json) và [sổ điều khoản](refinement-provisions-2026.json).
- [Kiểm thử ứng dụng, ngân hàng và lịch sử tiến bộ](variant-batch-60-tests-2026-10-09.tap); có thêm kiểm tra riêng cho phạm vi 60 câu, lời dẫn, khóa và hồ sơ.

Đã mở bản Luật Công chứng 46/2024 công bố chính thức và kiểm tra ngày hiệu lực của Luật sửa đổi 04/2026: 01/01/2027. Lời dẫn tháng 10/2026 không được trả lời bằng sửa đổi năm 2027. Đây là rà soát biên tập và điều khoản viện dẫn, không tự gán READY hoặc chứng nhận pháp lý toàn bộ 594 câu.

[Kiểm kê tại mốc đợt 60](https://github.com/hunghvt-cyber/CongchungVND/blob/251932916a9ea5f1422338a82bf734b3fe482960/reports/bank-audit-variants-2026-10-09.json) và [đo dung lượng tại mốc đó](https://github.com/hunghvt-cyber/CongchungVND/blob/251932916a9ea5f1422338a82bf734b3fe482960/reports/variant-payload-2026-10-09.json) được chạy lại. 11 tệp ngân hàng có 1.670.489 byte, tăng 58.511 byte so với đợt 40 câu. Gzip thử khoảng 218.366 byte; JSON được phân tích trung bình khoảng 4,34 ms trên Node cục bộ qua 50 vòng. Các số đo này không xác nhận nén máy chủ hay tốc độ mạng, điện thoại. Ứng dụng không tải tệp hồ sơ/biên tập khi làm đề.

Kiểm thử là Node và DOM giả lập, không thay kiểm tra tương tác thực trên điện thoại. Cập nhật ngân hàng thay dấu vân tay CC2; cần tạo mã đề mới để cả nhóm sử dụng cùng phiên bản.
