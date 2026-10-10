# Bối cảnh chuyển khỏi Codex Cloud — 10/10/2026

Madam An tạm ngừng dùng Codex Cloud và yêu cầu chuyển toàn bộ công việc còn ở workspace lên repository. Đợt này lưu hồ sơ và bản nháp, không nhập thêm câu vào ngân hàng active.

## Điểm bắt đầu phiên sau

- Repo: https://github.com/hunghvt-cyber/CongchungVND ; nhánh `main`.
- Website: https://hunghvt-cyber.github.io/CongchungVND/ ; HTML/CSS/JavaScript, GitHub Pages.
- Commit ngân hàng cuối: `e77a8afa1744c108c560e78b2fce93b0b2cfe469` — `Complete remaining 40 substantive variants and repair five explanations`.
- Commit lưu hồ sơ chuyển phiên nằm sau commit ngân hàng trên. Khi tiếp tục, clone/fetch và đọc trạng thái thực tế; không phụ thuộc đường dẫn hay quyền xác thực của Cloud cũ.
- Gọi người dùng là Madam An. Đưa gợi ý tiếp tục ngắn. Ưu tiên chất lượng ngân hàng và hạn chế mở rộng tính năng không cần thiết.
- Madam An đã cho phép commit/đẩy công việc hoàn thành và yêu cầu đẩy các bản nháp trong đợt lưu này. Vẫn phải kiểm tra thay đổi, bảo toàn nội dung, không vượt hạn chế quyền hoặc quy trình bảo vệ.

## Ngân hàng đã hoàn tất phạm vi biến thể

| Chỉ tiêu | Hiện tại |
|---|---:|
| Phạm vi đã xử lý | 583/583 |
| ID còn chờ bổ sung biến thể | 0 |
| Câu active | 594 |
| Câu active có ba lời dẫn | 594 |
| Tổng chuỗi lời dẫn active | 1.782 |
| Biến thể viết tích lũy | 1.166 |
| Trong đó thay chuỗi hình thức | 28 |
| Tăng ròng chuỗi lời dẫn | 1.138 |

Các nhóm: CC 93, SRC 14, VER26 98, DEP26 18, AUTH26 20, FAM26 26, INH26 32, REFIN26 80, COMP26 79, đề nhập 123. Có 11 câu ngoài phạm vi 583 đã đủ ba lời dẫn. Không tăng số câu độc lập trong các đợt biến thể. COMP26-DAT-002 archived không được xử lý.

Đợt cuối thêm 80 lời dẫn cho 40 ID cuối và sửa đúng năm giải thích `IMP-T60-023`, `IMP-T60-038`, `IMP-T60-039`, `IMP-T60-071`, `IMP-T60-085`. Giữ nguyên câu gốc, ID, trạng thái, bốn đáp án, khóa đúng, căn cứ, nguồn và lastVerified. Đối chiếu trước–sau xác nhận các bản ghi khác cùng 543 quyết định trước không đổi; áp dụng lại không thay dữ liệu/báo cáo.

Trạng thái là `VARIANT_SCOPE_COMPLETE_LEGAL_REVIEW_NOT_CERTIFIED`, `remainingIds: []`, `allActiveLegallyRecertified: false`. Không tự đánh dấu READY hoặc tuyên bố đã kiểm định pháp lý toàn bộ 594 câu.

## Hồ sơ cần đọc

- [Tiến độ hiện tại](variant-progress-2026-10-09.md).
- [Đợt cuối 40 câu](variant-final-40-2026-10-09.md).
- `reports/substantive-variants-2026-10-09.json`: hồ sơ từng câu và phạm vi cuối.
- `reports/variant-final-40-preservation-2026-10-09.json`: đối chiếu bảo toàn.
- `reports/variant-final-40-source-checks-2026-10-09.json`: truy xuất nguồn.
- `editorial/variant-final-40-scope-2026-10-09.json`: danh sách 40 ID lưu trước sửa.
- `editorial/variant-final-40-2026-10-09.json`: khóa độc lập và nhận xét.
- `editorial/exam-explanation-repairs-final-2026-10-09.json`: năm giải thích trước–sau và bản ghi trước sửa.
- `scripts/apply-substantive-variants-2026-10-09.py`: đã cập nhật hết phạm vi, vẫn giữ kiểm tra khóa, phạm vi, chứng cứ, trùng và bảo toàn.

Không sinh lại ngân hàng bằng các script xây dựng cũ: có nguy cơ ghi đè nội dung đã chỉnh. Biến thể mới phải khác thực chất và khớp toàn bộ đáp án, giải thích, căn cứ; không chỉ thêm tiền tố hoặc thay từ.

## Kiểm thử và triển khai ngân hàng

59/59 kiểm thử đạt ở commit ngân hàng; kết quả tại `reports/variant-final-40-tests-2026-10-09.tap`. `git diff --check` đạt. Kiểm kê tại `reports/bank-audit-variants-2026-10-09.json`.

```sh
node --test --test-isolation=none --test-reporter=tap tests/*.test.cjs
python scripts/audit-bank.py bank-audit-variants-2026-10-09.json
```

Đối số của audit-bank là tên báo cáo đầu ra. Kiểm thử dùng Node và DOM giả lập, chưa thay thao tác thật trên điện thoại.

GitHub Pages triển khai thành công cho `e77a8af`; đã tải trực tiếp `data/imported-exams-2026.json` trên website và đối chiếu từng byte. SHA-256: `1ee63f2139675664e879495de3ca5c0d68608b105ddec6732bb61caa9a4d3442`, 407.674 byte.

Ứng dụng tải 11 file ngân hàng tổng 1.892.301 byte. Gzip thử 246.707 byte, không khẳng định máy chủ nén như vậy. Reports/editorial không được tải khi làm đề. Ngân hàng mới đổi dấu vân tay mã CC2; nhóm học cần tạo mã mới.

## Công việc học từ bộ ảnh 20 câu

Madam An cung cấp ảnh phần làm bài và kết quả của một hệ thống có Credit/watermark riêng; không đồng nhất hệ thống đó với app trong repo. Yêu cầu học cách ra đề, mức khó, logic, căn cứ và khả năng đảo/tạo câu tương tự.

Đã lưu đầy đủ phần công việc biên tập hiện có:

- [Phân tích 20 câu](screenshot-question-design-2026-10-09.md): ma trận chủ đề/độ khó/căn cứ, cách đảo, nhận xét thiết kế và các điểm cần đối chiếu.
- [Tám câu mẫu và giải thích](screenshot-inspired-drafts-2026-10-09.md).
- `editorial/screenshot-inspired-drafts-2026-10-09.json`: tám bản ghi, 32 lựa chọn và 32 giải thích riêng; trạng thái `EDITORIAL_REFERENCE_COMPLETE`.

Tám câu chưa nhập active. Chủ đề: xung đột lợi ích với cha vợ; khoản nhận/thu bị cấm; giao dịch liên quan và ngưỡng Điều lệ; mốc hiệu lực văn bản điện tử; bản chuyển đổi thiếu chữ ký công chứng viên; đất nông nghiệp khác xã cùng tỉnh với yêu cầu chọn ý sai; đảo bài toán tìm số liệu năm còn thiếu; phân biệt doanh nghiệp/cá nhân/góp tài sản.

Ảnh gốc không có đường dẫn file truy cập được trong workspace. Đã chuyển nội dung thành [một file text đủ 20 câu](screenshot-reference-20-2026-10-09.txt): 80 lựa chọn, khóa hiển thị, lựa chọn người làm, lời giải và căn cứ nhìn thấy; đánh dấu phần bị cắt/thu gọn. Có thể tiếp tục từ repo mà không cần Codex Cloud hay ảnh đính kèm.

## Kết luận thiết kế để giữ khi tiếp tục

- Ước lượng bộ ảnh: 7 dễ, 10 trung bình, 3 khá; chưa đo độ khó thực nghiệm.
- Cấu trúc hữu ích: tình huống cụ thể → dữ kiện quyết định → lập luận cần kiểm tra → yêu cầu rõ.
- Phân biệt chọn một đúng, chọn một đầy đủ/phù hợp nhất và chọn tất cả ý đúng.
- Nhiễu nên dựa vào nhầm lẫn thật về chủ thể, ngưỡng, thời điểm, ngoại lệ; tránh đáp án đúng luôn dài nhất, nhiễu chỉ có từ tuyệt đối hoặc con số tự đặt.
- Đổi thứ tự không đổi bản chất; khóa phải theo ID. Đổi chủ thể/điều kiện hoặc hỏi ý sai phải tính lại khóa và giải thích.
- App đã chọn biến thể và đảo vị trí đáp án một lần khi bắt đầu bài; CC2 tái lập đề. Các nhãn A/B/C/D hiện vẫn theo ID gốc sau khi đảo vị trí.
- Tám mẫu đã hoàn tất rà cấu trúc, khóa, giải thích và nội dung trùng, chưa phải chứng nhận pháp lý toàn bộ ngân hàng.

## Pháp luật và việc còn cần hoàn thiện

Dùng phiên bản tương ứng thời điểm: Luật Công chứng 46/2024; không áp Luật sửa đổi 04/2026/QH16 có hiệu lực 01/01/2027 vào tháng 10/2026. Khi đọc chứng thực dùng VBHN753/VBHN-BTP năm 2026 cùng các sửa đổi; doanh nghiệp VBHN67/2025; đất đai VBHN44/2026. Văn bản hợp nhất không có hiệu lực độc lập; không nhầm số văn bản ở năm khác.

Các câu mẫu đã đối chiếu căn cứ chính: Công chứng Điều 9/64; NĐ104 Điều 10/47; Doanh nghiệp Điều 4/167; Đất đai Điều 27/47; TT09/2015 Điều 1–3. Đã đọc hai trang PDF ký TT09 trên Cổng Chính phủ và ghi SHA-256 trong bản nháp. Việc này không xác nhận đã rà mọi văn bản sửa đổi.

Đã hoàn tất ba việc của đợt tư liệu ảnh: (1) biên tập và rà nội dung trùng của tám mẫu; (2) đọc trực tiếp NĐ45/2020 và điều dẫn chiếu câu 19; (3) chuẩn hóa nguồn thiếu điểm/khoản/năm. Kết quả, dẫn chiếu, SHA-256 và quyết định từng mẫu tại [hồ sơ hoàn tất](screenshot-review-completion-2026-10-10.md). Các mẫu được giữ làm tư liệu thiết kế đề, không tự nhập thêm vào active.

Cập nhật sau bàn giao: đã hoàn tất kiểm định nội bộ căn cứ viện dẫn của 594 hồ sơ, gồm 112 câu đọc lại đầy đủ và 482 câu đối chiếu lại lập luận cùng hồ sơ biến thể đã kiểm tra. Sửa 7 câu, giữ nguyên khóa đúng; 60/60 kiểm thử đạt. Đọc [báo cáo kiểm định 594 câu](legal-audit-594-2026-10-10.md) và [sổ quyết định](legal-review-register-2026-10-10.json). Đây không phải chứng nhận pháp lý chuyên môn độc lập; trường chứng nhận rộng `allActiveLegallyRecertified` vẫn là `false`. Thử thao tác thật trên điện thoại vẫn chưa hoàn tất. Không còn việc lưu/chuyển nội dung bộ ảnh chờ ở Codex Cloud.

Điểm tiếp tục: đọc repo và hồ sơ này; nếu làm đợt mới, xác định phạm vi kiểm định pháp lý hoặc kiểm tra điện thoại. Không cần làm lại bản chép hoặc rà tám mẫu.
