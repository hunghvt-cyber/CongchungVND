# Biên tập câu dẫn và biến thể — 18/10/2026

Phạm vi là toàn bộ **793 câu đang sử dụng, gồm 1.411 câu dẫn/biến thể**. Bản biên tập làm rõ chủ thể, bổ sung từ bị lược, tách những câu ghép khó đọc, viết đầy đủ thuật ngữ và hoàn chỉnh câu hỏi cuối. Không thêm biến thể hoặc thay đổi các phương án trả lời.

| Nội dung | Số lượng |
|---|---:|
| Câu có thay đổi | 587 |
| Câu dẫn/biến thể có thay đổi | 1.096 |
| Câu được sửa bằng các đoạn viết riêng theo tình huống | 117 |
| Biến thể có đoạn sửa riêng | 126 |
| Câu giữ nguyên toàn bộ câu dẫn | 206 |
| Câu dẫn/biến thể giữ nguyên | 315 |

Các số “sửa riêng” nằm trong tổng số thay đổi. Những phần còn lại được xử lý bằng quy tắc ngôn ngữ có giới hạn hoặc giữ nguyên. Không diễn giải kết quả này thành việc viết lại thủ công độc lập cả 1.411 biến thể.

## Những chỗ đã làm rõ

- **CC-023:** “Giấy chứng nhận” được ghi đầy đủ là giấy chứng nhận kết quả kiểm tra tập sự hành nghề công chứng. Tình trạng mất năng lực hành vi dân sự và điều kiện bổ nhiệm vẫn được giữ.
- **IMP-T60-093:** “người sử dụng” và “lao động” được viết thành “người sử dụng lao động”, “người lao động”; câu hỏi có chủ ngữ rõ ràng. Vẫn giữ cả hai dữ kiện: thông tin không được yêu cầu và không liên quan trực tiếp đến việc giao kết.
- **INH26-023:** “L mất năng lực sở hữu riêng căn hộ” được tách thành hai ý: L là người mất năng lực hành vi dân sự và sở hữu riêng căn hộ. Giữ nguyên vai trò người giám hộ, người giám sát và điều kiện giao dịch vì lợi ích của L.
- **FAM26-026:** làm rõ việc không đăng ký kết hôn, không thuộc trường hợp đặc biệt được công nhận là vợ chồng và căn nhà thuộc sở hữu chung theo phần. Giữ nguyên năm chung sống, các giá trị tài sản và người thừa kế.
- Các câu hỏi cuối như “Cách tính đúng?”, “Mốc, quyền đúng?” được viết đủ thành phần; các lệnh chọn chung được diễn đạt theo dạng câu hỏi. Phần giới hạn nội dung cần xét được giữ để không mở rộng câu hỏi ra ngoài các phương án.

## Bảo toàn đáp án và dữ kiện

Lớp mới chỉ được ghi đè `question.variants`, áp dụng sau lớp biên tập phương án. Toàn bộ 3.172 lựa chọn, thứ tự/mã lựa chọn, giá trị đúng–sai, khóa đáp án, giải thích, căn cứ pháp luật và thông tin quản lý được giữ nguyên. Số lượng và tính phân biệt của các biến thể không đổi; 20 câu đã lưu để rà soát không được sửa hoặc đưa vào sử dụng.

Mỗi biến thể được kiểm tra chuỗi số, tiền, ngày tháng và tập ký hiệu chủ thể. Với các biến thể chỉ qua quy tắc ngôn ngữ, kiểm tra thêm việc giữ các từ chỉ điều kiện như “không”, “chưa”, “trừ”, “nếu”, “ít nhất”, “tối đa”, “tối thiểu”, “duy nhất”. Mỗi bản ghi có SHA-256 trước/sau; ứng dụng dừng tải nếu dữ liệu không khớp bản đã biên tập.

Các kiểm tra cấu trúc không thay thế việc đánh giá ngữ nghĩa hay thẩm định pháp lý. Đây là lượt biên tập câu chữ, giữ khóa hiện có; **không phải chứng nhận pháp lý lại toàn ngân hàng**. Hàng đợi pháp lý trước đó, đặc biệt DEP26-006, vẫn cần xử lý riêng. CC-015 và CC-023 được làm rõ cách diễn đạt, không thay khóa hoặc căn cứ.

## Kiểm chứng

**102/102 kiểm thử Node đạt, không có kiểm thử bị bỏ qua.** Kết quả kiểm thử cuối được lưu trong [TAP](stem-fluency-tests-2026-10-18.tap). Bộ kiểm thử bao gồm toàn bộ 793 câu và 9.690 trường hợp chấm điểm trong ôn tập/thi thử, kiểm tra lớp câu dẫn, bảo toàn dữ kiện và đáp án, lịch sử các lớp biên tập, mã đề dùng chung và thống kê ôn tập. Các kiểm thử giao diện dùng mô hình DOM; chưa có kiểm tra trình duyệt thật ở lượt này.

Tạo lại dữ liệu bằng `node scripts/build-stem-fluency-2026-10-18.cjs`; đầu ra đã được kiểm tra tái tạo giống hệt. [Hồ sơ từng câu](stem-fluency-2026-10-18.json) ghi đủ bản trước/sau của mọi biến thể, cả các bản giữ nguyên. [Bản triển khai](../data/stem-fluency-2026.json) chỉ chứa câu dẫn đã đổi; [các đoạn sửa riêng](../editorial/stem-fluency-2026-10-18.cjs) và [quy tắc biên tập](../scripts/build-stem-fluency-2026-10-18.cjs) có thể đối chiếu trực tiếp.

[Kiểm kê dữ liệu](stem-fluency-audit-2026-10-18.json) không phát hiện mã trùng, câu dẫn rỗng, phương án trùng hoặc khóa không hợp lệ ở nhóm đang dùng. Công cụ này còn đọc 500 câu lịch sử đã lưu trữ ngoài 813 bản ghi ứng dụng tải nên tổng kiểm kê là 1.313; số câu đủ điều kiện vẫn là 793. Cờ 490 câu có ít hơn ba biến thể là tồn tại về số lượng, không được coi là đã giải quyết trong lượt sửa các biến thể hiện có này.
