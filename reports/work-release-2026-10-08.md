# CongchungVND — lượt Work 08/10/2026

**Trạng thái: hoàn thành sửa thuật toán ở mức kiểm thử Node; chưa nghiệm thu toàn bộ dự án.**

## Dữ liệu xác minh

| Chỉ tiêu | Trước | Sau |
|---|---:|---:|
| File ứng dụng tải | 11 | 11 |
| Bản ghi được tải | 613 | 613 |
| Câu active | 594 | 594 |
| Câu Bài 1 / Bài 2 | 143 / 451 | 143 / 451 |
| Câu có một chuỗi cách hỏi | 569 | 569 |
| Câu có ba chuỗi cách hỏi | 25 | 25 |
| Câu có biến thể cơ học trong nhóm SRC | 14 | 14 |
| Câu cần viết biến thể thực chất | 583 | 583 |
| Câu mới nâng lên active / câu loại | 0 / 0 | 0 / 0 |

Số chuỗi biến thể đang lưu trong ngân hàng active: 644; trong đó 28 chuỗi SRC chỉ thêm câu dẫn. Không đồng nhất số chuỗi với số biến thể chất lượng. Đã sửa lời dẫn ở 7 câu trong nhóm 11 câu mới và chuẩn hóa điểm/khoản, đăng ký nguồn. Giữ nguyên bốn đáp án và khóa chấm.

## Thuật toán và chia sẻ

- Đề mới CC2 ghi vị trí câu trong ngân hàng đã sắp ID; seed quyết định biến thể và thứ tự đáp án. Mã có dấu vân tay ngân hàng và phần kiểm tra lỗi. Không phải mã bảo mật.
- CC1 vẫn tái tạo theo thuật toán cũ, khi cùng phiên bản ngân hàng. Cập nhật nội dung ngân hàng làm mã phiên bản cũ bị từ chối theo thiết kế sẵn có.
- Lịch sử chung ôn/thi theo learnerKey trên cùng thiết bị, di chuyển lịch sử ẩn danh cũ. Đề nhập bằng mã không bị lịch sử thay đổi nhưng vẫn ghi nhận câu đã gặp.
- Câu chưa gặp được ưu tiên; khi hết câu mới thì chọn câu lâu nhất. Cân đối tỷ trọng chủ đề/độ khó; tránh competenceId hoặc căn cứ + nội dung đáp án đúng trùng nhau khi có lựa chọn khác.
- Chưa đồng bộ lịch sử chống trùng giữa thiết bị; chưa nhận diện được tất cả câu trùng kiến thức khác lời văn.

## Kiểm thử

53/53 kiểm thử Node đạt, gồm chấm điểm, xem lại, giải thích/căn cứ, góp ý với phản hồi giả lập, lưu kết quả với phản hồi giả lập, CC1, CC2, mã hỏng, thay phiên bản ngân hàng, lưu trữ hỏng/bị chặn, tách người học và ngân hàng thật. Không coi DOM giả lập là kiểm thử trình duyệt hoặc máy chủ thật.

| Bài | Câu/đề | Câu trùng với toàn bộ đề trước: đề 1 / 2 / 3 |
|---|---:|---|
| 1 | 5 | 0 / 0 / 0 |
| 1 | 10 | 0 / 0 / 0 |
| 1 | 20 | 0 / 0 / 0 |
| 1 | 50 | 0 / 0 / 7 |
| 1 | 100 | 0 / 57 / 100 |
| 2 | 5 | 0 / 0 / 0 |
| 2 | 10 | 0 / 0 / 0 |
| 2 | 20 | 0 / 0 / 0 |
| 2 | 50 | 0 / 0 / 0 |
| 2 | 100 | 0 / 0 / 0 |

Mọi cấu hình tái tạo CC2 giống hệt bộ câu, cách hỏi và thứ tự đáp án của người tạo. Số lặp với hợp các đề trước đạt mức tối thiểu bắt buộc theo dung lượng ngân hàng. Đo này không chứng minh mọi đề có tỷ trọng chủ đề/độ khó hoàn hảo.

## Kiểm định pháp lý và phần chưa hoàn thành

Đã đối chiếu điều khoản chính thức BLDS Điều 405, 330, 260, 261; Luật HNGĐ Điều 95, 96 để sửa các lời dẫn lệch bộ đáp án. Một số trang chính thức mở trực tiếp lỗi 403/502; nội dung điều khoản trong kết quả tìm kiếm chính thức có thể đọc được. Không tự coi việc có đường dẫn là READY.

583 câu còn cần biên soạn biến thể thực chất, và 594 câu chưa được kiểm định lại toàn diện trong phiên Work. Sổ rà soát ghi đầy đủ ID, tệp, chủ đề, số biến thể và các bước bắt buộc; không chứng nhận pháp lý bằng thuật toán. Các kết quả hiệu lực/sửa đổi, phạm vi chuyên ngành, trùng kiến thức và đánh giá từng phương án vẫn cần hoàn thiện.

## Triển khai

Nhánh sao lưu trước sửa: backup/pre-work-2026-10-08 tại 4259c2235abb3c0ef89383cb07c2cbfa1332495d. Bằng chứng triển khai và thao tác trình duyệt sẽ được lưu riêng sau khi cập nhật main.

Website: https://hunghvt-cyber.github.io/CongchungVND/
