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
- Góp ý mới gửi tập trung về Supabase, có bản dự phòng localStorage; không tự sửa ngân hàng. Không có lịch sử thi lưu bền vững; tải lại trang sẽ mất bài đang làm.
- Tên luật được ghi đầy đủ trong dữ liệu, gồm Luật Công chứng số 46/2024/QH15 và Luật sửa đổi, bổ sung một số điều của Luật Công chứng số 04/2026/QH16. Thay đổi tên không có nghĩa là đã kiểm định toàn bộ đáp án hoặc hiệu lực áp dụng của 100 câu.

## Kiểm tra

Chạy bằng Node.js 20+:

```sh
node --check app.js
node --test tests/app.test.cjs
```

Các kiểm tra hồi quy chạy logic và HTML sinh ra với DOM tối giản; không thay thế kiểm tra bố cục/tương tác bằng trình duyệt thật.


## Cùng làm bằng mã đề

Trong **Thi thử**, người tạo chọn bài/số câu/thời gian, bấm **Tạo đề mới & bắt đầu**, sau đó **Sao chép mã đề** và gửi mã cho nhóm. Thành viên mở **Thi thử**, dán mã vào ô **Mã đề người khác chia sẻ**, bấm **Nhập mã & bắt đầu thi**. Cấu hình từ mã được dùng thay cho các lựa chọn tạo đề mới.

Mã CC1 cố định seed, bài, số câu thực tế, thời lượng và dấu vân tay của ngân hàng đủ điều kiện trong bài đã chọn. Cùng mã/cùng phiên bản ngân hàng tạo cùng thứ tự câu, biến thể và thứ tự đáp án. Mã có phần kiểm tra lỗi nhập; không phải cơ chế bảo mật hay mã phòng thi. Mã CC cũ chỉ là nhãn nên không nhập được. Nếu ngân hàng thay đổi, mã cũ bị từ chối; tải lại trang hoặc tạo mã mới cho cả nhóm.

Mỗi người có đáp án, điểm và đồng hồ riêng, tính từ lúc bắt đầu. Sau nộp, mở cùng số câu trong kết quả để đối chiếu đáp án và giải thích. Không đồng bộ giờ bắt đầu, không có chat/bảng điểm chung hay phòng thi trực tiếp. Góp ý mới được gửi về Supabase để rà soát chung.


## Góp ý tập trung

Góp ý mới được gửi bằng Data API đến bảng `public.question_feedback` trong dự án Supabase **CongchungVND**. `data/feedback-config.json` chỉ chứa URL và publishable key; không dùng secret/service-role trong frontend. `supabase/schema.sql` ghi cấu trúc đã áp dụng (migration `central_question_feedback`).

Người dùng chọn loại, nhập nội dung rồi bấm **Gửi góp ý** ngay tại câu/đáp án. Chỉ hiện “đã gửi” sau phản hồi thành công. Lưu mã câu, mã đề, thứ tự đáp án, nội dung câu/giải thích/căn cứ tại lúc gửi và thời gian máy chủ. RLS và quyền cột chỉ cho anon INSERT các trường gửi góp ý; không cho đọc/sửa/xóa hoặc tự đánh dấu đã xử lý. Chủ dự án xem/rà soát bằng Supabase Dashboard → Table Editor → question_feedback. Không có màn hình quản trị mới trong web và không tự sửa ngân hàng.

LocalStorage giữ bản dự phòng có delivery=pending/sent. Gửi lỗi thì giữ nội dung và cho thử lại; mở nút góp ý để gửi lại các bản mới đang chờ. Mỗi góp ý có UUID được giữ nguyên khi thử lại nhằm tránh trùng sau khi mất phản hồi mạng. Góp ý cũ chỉ lưu local (chưa có UUID/snapshot) không được tự tải lên. Bản dự phòng không phải bằng chứng máy chủ đã nhận; việc xóa dữ liệu trình duyệt sẽ mất bản chưa gửi. Nếu không lưu local được, web vẫn thử gửi trung tâm và báo rõ nếu cả hai thất bại.

Cơ chế gửi không yêu cầu đăng nhập; đây là dữ liệu góp ý chưa được xác minh danh tính. Các ràng buộc kiểm tra loại, độ dài và định dạng; chưa triển khai CAPTCHA hay chống spam theo người dùng.
