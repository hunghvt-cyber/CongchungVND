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

Web tĩnh dùng GitHub Pages, không cần database hay tài khoản. `data/questions.json` có 100 câu active; `data/derived-questions.json` có 20 câu review. Chỉ active/verified được chọn vào Ôn tập và Thi thử. Trạng thái active là điều kiện kỹ thuật để chọn câu, không thay thế kiểm định pháp lý.

## Cấu trúc dữ liệu dự kiến

```text
data/
  questions.json
  derived-questions.json
  question-sources.json
```

## Triển khai

Có thể dùng GitHub Pages để xuất bản trực tiếp repository này thành website.

> Lưu ý: câu hỏi pháp luật thật chỉ được đưa vào ngân hàng sau khi kiểm tra nguồn và tình trạng hiệu lực văn bản.


## Hành vi đã sửa

- Câu hỏi, biến thể và thứ tự đáp án được chọn một lần khi bắt đầu buổi học/bài thi; xem lại giữ nguyên đề.
- Ôn tập: chọn đáp án, bấm **Kiểm tra đáp án** để đọc đúng/sai và giải thích, rồi bấm tiếp. Câu đã chấm (kể cả sai) bị khóa; có thể ôn lại câu sai sau buổi học.
- Thi thử: không hiện đáp án khi đang thi. Sau nộp bài, tất cả câu (đúng, sai, chưa trả lời) đều có lựa chọn đã làm, đáp án đúng, giải thích, căn cứ và góp ý.
- Chấm multiple choice theo tập đáp án: phải chọn đủ đáp án đúng và không chọn đáp án sai.
- Timer dùng mốc hết giờ thực tế; kiểm tra lại khi quay về tab và trước thao tác chọn/đi tiếp, tự nộp khi hết giờ.
- Góp ý lưu trong localStorage của thiết bị/trình duyệt hiện tại, không gửi đến nhóm quản lý và không tự sửa ngân hàng. Không có lịch sử thi lưu bền vững; tải lại trang sẽ mất bài đang làm.
- Tên luật được ghi đầy đủ trong dữ liệu, gồm Luật Công chứng số 46/2024/QH15 và Luật sửa đổi, bổ sung một số điều của Luật Công chứng số 04/2026/QH16. Thay đổi tên không có nghĩa là đã kiểm định toàn bộ đáp án hoặc hiệu lực áp dụng của 100 câu.

## Kiểm tra

Chạy bằng Node.js 20+:

```sh
node --check app.js
node --test tests/app.test.cjs
```

Các kiểm tra hồi quy chạy logic và HTML sinh ra với DOM tối giản; không thay thế kiểm tra bố cục/tương tác bằng trình duyệt thật.
