# Kiểm thử sau công bố main — 15/10/2026

## Bản đã công bố

- Commit GitHub: `d19332e8b77f0da5c41863983ef94eeabaa3d310`.
- Tree: `8725cd7118385e1b3665a71e723344b6a99031c3`, khớp tuyệt đối tree của commit cục bộ `66438f8`.
- Kết nối GitHub công bố gộp nội dung bốn commit `77ecb76`, `1235b7c`, `a6ba79e`, `66438f8`, nối tiếp `db1519c`; không ghi đè lịch sử remote. Git push thông thường không có thông tin xác thực.
- Madam An đã cho phép công bố lên main rồi chạy kiểm thử. Đây là cập nhật trạng thái sau báo cáo biên tập ghi chưa kiểm thử, không sửa lại hồ sơ lịch sử đó.

## Kết quả

**Chưa đạt toàn bộ bộ kiểm thử. Không sửa câu hỏi, khóa, chương trình hay kiểm thử để làm xanh kết quả trong phiên này.**

| Phép kiểm tra | Kết quả |
|---|---|
| Bộ hiện có trước khi công bố thành công | 82 bài: 60 đạt, 22 không đạt |
| Bộ hiện có chạy lại sau khi main cập nhật | 82 bài: 62 đạt, 20 không đạt; không hủy hoặc bỏ qua bài nào |
| Tải ngân hàng bằng loadQuestions thực tế qua DOM giả lập | 813 bản ghi, 793 active, 20 archived; tải qua đầy đủ lớp nguồn thành công |
| Chấm điểm bổ sung trên toàn ngân hàng active | 9.690 trường hợp ở ôn tập và thi thử; 0 lệch điểm so với correct flags lưu trong dữ liệu |
| ID và câu dẫn đầu trùng chính xác trong bản kiểm kê | Không ghi nhận nhóm trùng |
| Chất lượng theo dấu hiệu hình thức | 19 câu active có giải thích tổng dưới 100 ký tự; 490 câu active chưa đủ 3 biến thể |
| Trình duyệt thật / GitHub Pages sau triển khai | Chưa kiểm tra; không dùng Node DOM thay bằng chứng trình duyệt |

Lệnh sau công bố: `node --test --test-reporter=tap tests/*.test.cjs`.

## 20 bài không đạt ở lượt sau công bố

| Nhóm | Số bài | Nhận định và hướng xử lý |
|---|---:|---|
| Kiểm thử bắt buộc cụm “Gợi ý làm bài:” | 9 | Bản biên tập đã lược cụm này. Cần đánh giá lại tiêu chí hiển thị giải thích, không thêm văn mẫu chỉ để vượt regex. Các bài: 1, 21, 22, 23, 52, 53, 54, 63, 64. |
| Đối chiếu nguyên văn snapshot lịch sử | 6 | Chưa đi qua các quyết định biên tập mới; ví dụ đáp án `COMP26-QT-010` và giải thích `SRC26-001`, `IMP-T60-071` đã thay đổi. Cần xác minh từng thay đổi trước khi cập nhật cơ chế đối chiếu. Bài 46, 47, 48, 49, 50, 56. |
| Hồ sơ kiểm định cũ chưa khớp dữ liệu mới | 2 | `COMP26-DN-009` khác hash kiểm định cũ; `HARD26-041` đã thêm DS:296 nhưng hồ sơ chứng cứ cũ chưa đồng bộ. Không tự cập nhật hash để giả chứng nhận pháp lý. Bài 65, 66. |
| Regex nhận diện người không là cộng tác viên | 1 | Bài 43 đòi “không là cộng tác viên”, câu hiện viết “không phải cộng tác viên”. Lỗi kỳ vọng nguyên văn; bài đã chạy các vòng chấm điểm trước khi dừng tại regex này. |
| Biến thể đã bị loại được đưa lại | 1 | Bài 38 báo `IMP-SEP24-031 retired wording`. Cần rà lại lịch sử loại biến thể và thay bằng câu tình huống đạt yêu cầu; chưa coi là lỗi kiểm thử vô hại. |
| Giải thích tổng không đạt độ dài tối thiểu | 1 | Bài 60 dừng tại `IMP-SEP24-019`; kiểm kê đầy đủ ghi 19 ứng viên. Không coi số ký tự tự nó chứng minh chất lượng hay tính đúng luật. |

Đây là 20 **bài kiểm thử**, không phải kết luận có đúng 20 câu hỏi sai. Một bài có thể dừng ở lỗi đầu và che các lỗi phía sau. Không kết luận các nhóm snapshot/regex đã sạch mọi lỗi chức năng.

Hai lượt không có thay đổi nguồn nhưng khác 60/62 bài đạt. Cụ thể bài kiểm thử imported và deposit không đạt ở lượt đầu nhưng đạt ở lượt sau; cần cố định dữ liệu chọn/ngẫu nhiên trong kiểm thử để tái hiện ổn định.

## Kiểm tra chấm điểm bổ sung

Tái sử dụng DOM harness của `tests/app.test.cjs`, nạp `app.js` và tất cả các lớp JSON qua `loadQuestions`. Với mỗi câu single, thử bỏ trống và bốn lựa chọn; với mỗi câu multiple, thử cả 16 tập lựa chọn. Thực hiện cả ôn tập và thi thử, so điểm thực tế với tập đáp án correct trong dữ liệu. Tổng 9.690 trường hợp, không có sai khác.

Giới hạn: kiểm tra này phát hiện chấm lệch khóa đã lưu, **không chứng minh khóa đúng về pháp luật**, không đo độ khó, không kiểm tra trình duyệt hoặc dữ liệu Supabase thật. Mã kiểm tra chỉ dùng cơ chế phản hồi giả lập của bộ hiện có, không gửi phản hồi thật.

## Kiểm kê và việc còn tồn

Script `scripts/audit-bank.py` còn đọc 500 câu mở rộng đã archived, nên báo tổng 1.313 và 520 archived. Đây không phải tổng đang được app tải. Phần active của script vẫn là 793, trùng bộ nạp thật. Các cờ active chỉ gồm 490 câu ít hơn ba biến thể và 19 giải thích tổng ngắn; không có cờ cấu trúc khóa, URL căn cứ hoặc ngày luật tương lai trên active.

18 trong 19 giải thích ngắn thuộc nhóm CAL có giải thích riêng cho từng phương án; vẫn cần đọc nội dung hiển thị trước khi quyết định bổ sung. Không thể kết luận cả 19 đều thiếu giải thích pháp lý chỉ bằng ngưỡng 100 ký tự.

Các bước cần được Madam An cho thực hiện tiếp: xử lý biến thể bị đưa lại; bổ sung giải thích thực sự thiếu; đối chiếu lại chứng cứ và hash các câu đã sửa; cập nhật kiểm thử theo quyết định biên tập đã được kiểm chứng; làm ổn định lựa chọn ngẫu nhiên; chạy lại toàn bộ và kiểm tra trình duyệt/triển khai.

## Hồ sơ kèm theo

- `post-publication-tests-2026-10-15.tap`: kết quả nguyên vẹn lượt sau công bố.
- `post-publication-scoring-2026-10-15.json`: kết quả 9.690 trường hợp chấm điểm.
- Bản kiểm kê đầy đủ được tạo trong scratch; chỉ các kết luận cần thiết được ghi ở báo cáo này, tránh nhầm phạm vi 1.313 với 813 bản ghi được nạp.
