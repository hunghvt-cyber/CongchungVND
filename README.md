# CongchungVND

Tiến độ 09/10/2026: đã xử lý biến thể cho **343/583 câu**, còn **240 câu**; chưa nghiệm thu hoặc kiểm định lại pháp lý toàn ngân hàng. Hiện có 594 câu active và 1.302 chuỗi cách hỏi. Đợt tiếp mới nhất thêm 120 lời dẫn cho 60 câu về tổ chức, hành nghề và thủ tục công chứng; xem [đợt 60 câu](reports/variant-batch-60-2026-10-09.md), [báo cáo tiến độ](reports/variant-progress-2026-10-09.md) và [hồ sơ từng câu](reports/substantive-variants-2026-10-09.json).

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

Web tĩnh dùng GitHub Pages. Sau lượt bổ sung tiếp ngày 07/10/2026, lưu **1.102 bản ghi: 583 active, 0 review trong data, 519 archived**. App tải 10 file với 602 bản ghi và chỉ chọn câu active. Năm file EXP cơ học vẫn không được tải. Lượt tiếp này thêm 80 câu REFIN26, ngừng dùng 3 câu trùng năng lực và giữ nguyên ID/nội dung lịch sử. Hai lô COMP26 và REFIN26 có tổng 160 câu mới lưu trữ, trong đó 159 còn active. Tính cả VER26 và các lô nguồn cung cấp, có 482 bản ghi mới ngoài bộ CC/SRC/EXP, 476 active; con số này chưa chứng minh đã hoàn thiện riêng lô EXP hoặc đã hết trùng năng lực. Xem [báo cáo lượt tiếp](reports/refinement-2026-10-07.md), [ma trận hiện tại](reports/matrix-refinement-2026-10-07.json), [hai đề luyện 40 câu và bài giải](reports/refinement-exams-2026-10-07.md) và [chứng cứ 80 câu mới](reports/refinement-legal-evidence-2026.json).

Các mục bổ sung theo ngày ở dưới là lịch sử dự án; số lượng tại các mốc cũ không phải tổng hiện tại.

## Cấu trúc dữ liệu dự kiến

```text
data/
  questions.json
  derived-questions.json
  validated-2026.json
  completion-2026.json
  refinement-2026.json
  imported-*-2026.json
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
- Góp ý mới gửi tập trung về Supabase, có bản dự phòng localStorage; không tự sửa ngân hàng. Bài đang làm chưa được lưu; bài đã nộp có bản chụp và lịch sử theo cơ chế progress bên dưới.
- Tên luật được ghi đầy đủ trong dữ liệu, gồm Luật Công chứng số 46/2024/QH15 và Luật sửa đổi, bổ sung một số điều của Luật Công chứng số 04/2026/QH16. Thay đổi tên không có nghĩa là đã kiểm định toàn bộ đáp án hoặc hiệu lực áp dụng của 100 câu.

## Kiểm tra

Đã bổ sung 18 câu biên soạn từ nguồn đặt cọc do Madam An cung cấp, ID DEP26-001–DEP26-018. Xem [đề luyện 18 câu và bài giải](reports/deposit-exam-2026-10-05.md), [rà soát nguồn](reports/deposit-source-review.json) và [kiểm kê ngân hàng sau bổ sung](reports/bank-audit-deposit-after.json). App tải `imported-deposit-2026.json` vào Bài 2; tổng ngân hàng đủ điều kiện tại mốc đó là 322 câu. Đây chưa phải mốc 400 câu chuẩn.

Chạy bằng Node.js 20+:

```sh
node --check app.js
node --test tests/app.test.cjs
```

Các kiểm tra hồi quy chạy logic và HTML sinh ra với DOM tối giản; không thay thế kiểm tra bố cục/tương tác bằng trình duyệt thật.


## Cùng làm bằng mã đề

Trong **Thi thử**, người tạo chọn bài/số câu/thời gian, bấm **Tạo đề mới & bắt đầu**, sau đó **Sao chép mã đề** và gửi mã cho nhóm. Thành viên mở **Thi thử**, dán mã vào ô **Mã đề người khác chia sẻ**, bấm **Nhập mã & bắt đầu thi**. Cấu hình từ mã được dùng thay cho các lựa chọn tạo đề mới.

Đề mới dùng mã CC2 ghi chính xác danh sách câu được chọn, seed, bài, số câu thực tế, thời lượng và dấu vân tay ngân hàng. Lịch sử riêng chỉ tác động lúc tạo đề; nhập mã luôn tái tạo đúng đề đã chia sẻ. Mã CC1 vẫn được đọc bằng thuật toán cũ khi ngân hàng khớp phiên bản. Cùng mã/cùng phiên bản ngân hàng tạo cùng thứ tự câu, biến thể và thứ tự đáp án. Mã có phần kiểm tra lỗi nhập; không phải cơ chế bảo mật hay mã phòng thi. Mã CC cũ chỉ là nhãn nên không nhập được. Nếu ngân hàng thay đổi, mã cũ bị từ chối; tải lại trang hoặc tạo mã mới cho cả nhóm.

Mỗi người có đáp án, điểm và đồng hồ riêng, tính từ lúc bắt đầu. Sau nộp, mở cùng số câu trong kết quả để đối chiếu đáp án và giải thích. Không đồng bộ giờ bắt đầu, không có chat/bảng điểm chung hay phòng thi trực tiếp. Góp ý mới được gửi về Supabase để rà soát chung.


## Góp ý tập trung

Góp ý mới được gửi bằng Data API đến bảng `public.question_feedback` trong dự án Supabase **CongchungVND**. `data/feedback-config.json` chỉ chứa URL và publishable key; không dùng secret/service-role trong frontend. `supabase/schema.sql` ghi cấu trúc đã áp dụng (migration `central_question_feedback`).

Người dùng chọn loại, nhập nội dung rồi bấm **Gửi góp ý** ngay tại câu/đáp án. Chỉ hiện “đã gửi” sau phản hồi thành công. Lưu mã câu, mã đề, thứ tự đáp án, nội dung câu/giải thích/căn cứ tại lúc gửi và thời gian máy chủ. RLS và quyền cột chỉ cho anon INSERT các trường gửi góp ý; không cho đọc/sửa/xóa hoặc tự đánh dấu đã xử lý. Chủ dự án xem/rà soát bằng Supabase Dashboard → Table Editor → question_feedback. Không có màn hình quản trị mới trong web và không tự sửa ngân hàng.

LocalStorage giữ bản dự phòng có delivery=pending/sent. Gửi lỗi thì giữ nội dung và cho thử lại; mở nút góp ý để gửi lại các bản mới đang chờ. Mỗi góp ý có UUID được giữ nguyên khi thử lại nhằm tránh trùng sau khi mất phản hồi mạng. Góp ý cũ chỉ lưu local (chưa có UUID/snapshot) không được tự tải lên. Bản dự phòng không phải bằng chứng máy chủ đã nhận; việc xóa dữ liệu trình duyệt sẽ mất bản chưa gửi. Nếu không lưu local được, web vẫn thử gửi trung tâm và báo rõ nếu cả hai thất bại.

Cơ chế gửi không yêu cầu đăng nhập; đây là dữ liệu góp ý chưa được xác minh danh tính. Các ràng buộc kiểm tra loại, độ dài và định dạng; chưa triển khai CAPTCHA hay chống spam theo người dùng.

### Lưu kết quả thi và theo dõi tiến bộ

- Thi thử yêu cầu tên người thi, không cần tài khoản. Mỗi tên được chuẩn hóa khoảng trắng/chữ hoa-thường trên thiết bị và gắn với mã lịch sử UUID ngẫu nhiên; tên trùng ở hai thiết bị không tự gộp.
- Sau nộp bài hoặc hết giờ, Supabase lưu mã đề, thời điểm, thời gian làm, điểm và bản chụp câu hỏi/đáp án đã chọn/đáp án đúng/lời giải/căn cứ. Thay đổi ngân hàng sau này không làm mất lời giải lúc thi.
- Mục “Tiến bộ của người thi” có điểm trung bình, gần nhất, cao nhất, biểu đồ 20 lần gần nhất, so sánh điểm theo bài và chủ đề cần củng cố từ 5 lần gần nhất; có thể xem lại từng bài và ôn các câu sai. Điểm giữa các đề khác nhau chỉ mang tính tham khảo.
- Muốn tiếp tục trên thiết bị khác, nhập cùng tên và mã lịch sử trong mục thống kê trước khi thi. Mã được hiển thị ở kết quả và mục thống kê. Giữ riêng mã: ai có mã có thể đọc và bổ sung lịch sử. Không thể khôi phục chỉ bằng tên sau khi mất mã và xóa dữ liệu trình duyệt.
- Khi mất kết nối, bài thi chờ trong localStorage; nút “Gửi kết quả chưa lưu” gửi lại cùng UUID để tránh trùng bài. Chỉ thông báo đã lưu khi server xác nhận.
- Schema: `supabase/exam-results.sql`. RLS chỉ cho đọc/ghi khi header `x-client-info` khớp mã lịch sử, không cho sửa/xóa; không có danh sách công khai theo tên. Đây là dữ liệu tự luyện do trình duyệt gửi, không xác minh danh tính hoặc dùng làm chứng nhận điểm thi.
- Chạy kiểm tra: `node --test tests/*.test.cjs`.
### Bổ sung nguồn ủy quyền ngày 05/10/2026

20 câu tình huống mới đã được đối chiếu BLDS 2015, Luật Công chứng 2024 và Luật Hôn nhân và gia đình (VBHN 121/2025). Tổng active tăng từ 322 lên 342. App tải `data/imported-authorization-2026.json` cùng các file ngân hàng hiện có, giữ nguyên dữ liệu kết quả/progress.

Đề luyện 35 phút và bài giải: [reports/authorization-exam-2026-10-05.md](reports/authorization-exam-2026-10-05.md). Nguồn gồm 24 câu lớn và 7 mục phụ lục trùng tài liệu đặt cọc; chỉ chứng nhận câu đã biên soạn, các nhánh chưa xác minh giữ review. Hồ sơ điều khoản: [reports/authorization-legal-evidence-2026.json](reports/authorization-legal-evidence-2026.json).

## Lượt Work ngày 08/10/2026 — chưa nghiệm thu toàn bộ ngân hàng

App tải 11 file, 613 bản ghi: **594 active**, 19 archived. Tính cả 500 câu EXP không được tải, repository lưu 1.113 bản ghi, 519 archived.

Đã khôi phục mã chia sẻ cho đề chống trùng bằng CC2, dùng chung lịch sử ôn/thi theo mã người học trên thiết bị, ưu tiên câu chưa thấy và dùng lại câu lâu nhất khi cần. Phân bổ chủ đề/độ khó theo tỷ trọng ngân hàng; tránh trùng kiến thức khi có competenceId hoặc căn cứ + đáp án đúng giống nhau. Đây là nhận diện một phần; chưa thay thế rà soát trùng nội dung bởi người biên soạn.

Kiểm thử 3 đề liên tiếp ở mỗi bài, với 5/10/20/50/100 câu. 53 kiểm thử Node đạt. Với 20 câu/đề, ba đề không lặp ở cả hai bài. Với 50 câu/đề ở Bài 1, 143 câu không đủ cho 150 lượt nên phải lặp 7 câu. Lịch sử chống trùng chưa đồng bộ giữa các thiết bị; nếu chặn lưu trữ, vẫn tạo và chia sẻ được đề nhưng không nhớ lần trước.

569 câu chỉ có một biến thể; 14 câu SRC có ba chuỗi nhưng hai chuỗi chỉ thêm câu dẫn. **583 câu vẫn cần biên soạn biến thể thực chất**. Nhóm 11 câu mới có sửa lời dẫn để phù hợp bốn đáp án; không có câu mới được nâng lên active trong lượt này. Chưa chứng nhận READY hoặc kiểm định lại toàn bộ 594 câu.

Xem [báo cáo lượt Work](reports/work-release-2026-10-08.md), [sổ rà soát từng câu](reports/work-review-register-2026-10-08.json) và [đo trùng đề](reports/anti-repeat-tests-2026-10-08.json).
