# CongchungVND

Web app nhóm nhỏ ôn thi tập sự hành nghề công chứng 2027.

## Mục tiêu

- Ngân hàng câu hỏi độc lập, có thể mở rộng lên khoảng 1.000 câu.
- Chia thành Bài 1 và Bài 2 theo cấu trúc dự kiến của kỳ kiểm tra 2027.
- Mỗi câu có 4 đáp án, hỗ trợ 1 hoặc 2 đáp án đúng.
- Có thể lưu nhiều biến thể cách hỏi cho cùng một câu.
- Mã đề có thể random câu hỏi, biến thể và thứ tự đáp án.
- Có giải thích và căn cứ pháp lý.
- Người ôn tập có thể góp ý câu hỏi/văn bản để nhóm kiểm tra và cập nhật.

## MVP hiện tại

Phiên bản đầu tiên là web tĩnh, không cần database hay tài khoản. Dữ liệu mẫu nằm trong `data/questions.json`.

## Cấu trúc dữ liệu dự kiến

```text
data/
  questions.json
  exams.json       # sẽ bổ sung khi xây module mã đề
  feedback.json    # sẽ bổ sung khi xây module góp ý
```

## Triển khai

Có thể dùng GitHub Pages để xuất bản trực tiếp repository này thành website.

> Lưu ý: câu hỏi pháp luật thật chỉ được đưa vào ngân hàng sau khi kiểm tra nguồn và tình trạng hiệu lực văn bản.
