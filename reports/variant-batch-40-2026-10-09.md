# Đợt tiếp 40 câu ngày 09/10/2026

Đã bổ sung hai lời dẫn mới cho **40 câu** theo yêu cầu của Madam An: **26 câu hôn nhân–gia đình FAM26-001–026** và **14 câu thừa kế INH26-001–014**. Mỗi câu hiện có ba lời dẫn dùng chung bộ bốn đáp án, giải thích và căn cứ.

| Chỉ tiêu | Trước đợt 40 câu | Sau đợt 40 câu |
|---|---:|---:|
| Đã xử lý trong phạm vi 583 câu | 243 | 283 |
| Còn cần biến thể thực chất | 340 | 300 |
| Lời dẫn mới viết riêng trong đợt | 0 | 80 |
| Tổng câu active | 594 | 594 |
| Câu active có ba lời dẫn | 254 | 294 |
| Tổng chuỗi lời dẫn active | 1.102 | 1.182 |

Các lời dẫn khai thác quy tắc, điều kiện quyết định và việc rà soát hồ sơ hoặc lập luận của một bên. Một số tình huống được thay đổi: chủ nợ xin bản sao thay người con; giấy tờ trong hồ sơ mua nhà; chấm dứt thỏa thuận nhập tài sản; chia nguồn bảo đảm học và sinh hoạt của con 16 tuổi; cho thuê tài sản lớn của người được giám hộ; tặng tài sản người được giám hộ cho tổ chức từ thiện. Các câu tính tiền thừa kế giữ số liệu và quan hệ thừa kế để bốn đáp án hiện có vẫn dùng được, nhưng hỏi theo bước tính hoặc sửa phương án phân chia sai.

Đã đối chiếu cả bốn phương án cho từng câu với giả thiết của các lời dẫn và điều khoản trong hồ sơ nguồn. Các điểm kiểm tra bao gồm ngoại lệ giấy tờ điểm d Điều 42, phạm vi địa bàn Điều 44, tài sản sau chia và chế độ thỏa thuận, lựa chọn giám hộ, phần thừa kế bắt buộc, thế vị qua hai lần mở thừa kế, dành phần cho thai nhi, ưu tiên thanh toán và giới hạn người quản lý. Các phép tính được rà lại: 200 triệu chia hai nhánh 100 triệu; hai suất bắt buộc 200 triệu trên di sản 900 triệu; dành 200 triệu trong 600 triệu cho thai nhi; 70 triệu còn trả nợ sau chi phí; trách nhiệm 150/50 triệu theo tỷ lệ 3:1.

Giữ nguyên ID, số câu active, đáp án, khóa, giải thích và căn cứ. Mọi lời dẫn mới ghi **Tháng 10/2026**. Không thay `lastVerified` thành một ngày mới chỉ vì bổ sung lời dẫn. Không tự gán READY hay chứng nhận pháp lý toàn bộ ngân hàng.

## Hồ sơ

- [Lời dẫn hôn nhân–gia đình](../editorial/family-variants-2026-10-09.json) và [khóa đối chiếu](../editorial/family-answer-review-2026-10-09.json).
- [Lời dẫn thừa kế](../editorial/inheritance-variants-2026-10-09.json) và [khóa đối chiếu](../editorial/inheritance-answer-review-2026-10-09.json).
- [Nhận xét từng câu và kiểm tra nguồn](../editorial/variant-batch-40-2026-10-09.json).
- [Hồ sơ tích lũy, bản trước chỉnh và 300 ID còn lại tại mốc đợt 40 câu](https://github.com/hunghvt-cyber/CongchungVND/blob/923156f846d43021accacf5e300fdda3e3566c4d/reports/substantive-variants-2026-10-09.json).

Một số trang CSDL toàn văn mở gặp lỗi; hồ sơ nhận xét ghi rõ nguồn nào đọc trực tiếp, nguồn nào dùng thêm chứng cứ điều khoản đã lưu. Phạm vi bãi bỏ của NĐ126 được đối chiếu riêng, không xem trạng thái hết hiệu lực một phần là toàn nghị định đã hết hoặc vẫn còn hiệu lực. Quy định sửa Luật Công chứng có hiệu lực 01/01/2027 không được dùng để trả lời câu tháng 10/2026.

## Kiểm tra dữ liệu và ứng dụng

Kết quả tại [bản ghi kiểm thử](variant-batch-40-tests-2026-10-09.tap); chạy bộ Node/DOM giả lập gồm ứng dụng, dữ liệu và lịch sử tiến bộ. Đây không phải kiểm thử trực tiếp trên điện thoại.

[Kiểm kê tại mốc đợt 40 câu](https://github.com/hunghvt-cyber/CongchungVND/blob/923156f846d43021accacf5e300fdda3e3566c4d/reports/bank-audit-variants-2026-10-09.json) xác nhận 594 active, không trùng ID hoặc lời dẫn nguyên văn; còn 300 câu được đánh dấu cần biến thể thực chất. [Đo dung lượng tại cùng mốc](https://github.com/hunghvt-cyber/CongchungVND/blob/923156f846d43021accacf5e300fdda3e3566c4d/reports/variant-payload-2026-10-09.json) ghi 11 tệp ngân hàng với 1.611.978 byte, tăng 45.162 byte so với đợt trước. Gzip thử khoảng 209.892 byte; không phải xác nhận cấu hình nén máy chủ. Thời gian phân tích JSON trung bình khoảng 3,99 ms trên Node cục bộ, không phải đo mạng hay iPhone.

Các tệp hồ sơ và biên tập không được ứng dụng tải khi làm đề. Mã CC2 của phiên bản ngân hàng trước cần được tạo lại khi dùng phiên bản dữ liệu mới theo cơ chế kiểm tra phiên bản đã có.
