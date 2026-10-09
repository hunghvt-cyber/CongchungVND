# Hoàn tất 40 câu và sửa năm giải thích — 09/10/2026

Theo yêu cầu “Sửa 5 giải thích rồi làm nốt 40 câu”, đã sửa đúng năm giải thích và thêm 80 lời dẫn cho đúng 40 ID còn lại ở commit nền `342a1a108873b64fd82cbdba0fd1166eec99fa3c`. Hoàn tất phạm vi biến thể 583/583; **chưa chứng nhận kiểm định pháp lý toàn ngân hàng**.

| Chỉ tiêu | Trước | Sau |
|---|---:|---:|
| Câu đã xử lý trong phạm vi | 543 | 583 |
| Câu còn lại | 40 | 0 |
| Câu active | 594 | 594 |
| Câu có ba lời dẫn | 554 | 594 |
| Tổng chuỗi lời dẫn active | 1.702 | 1.782 |
| Biến thể viết tích lũy | 1.086 | 1.166 |

Danh sách 40 ID được lưu **trước khi sửa** tại `editorial/variant-final-40-scope-2026-10-09.json`, khớp chính xác `remainingIds` của báo cáo ở commit nền. Không xử lý câu archived hoặc thêm câu độc lập.

## Năm giải thích đã sửa

| ID | Khóa giữ nguyên | Nội dung sửa |
|---|---|---|
| IMP-T60-023 | A | Nghĩa vụ chung khi sử dụng tài sản riêng để duy trì tài sản chung; bỏ nhận xét về phương án cũ không còn phù hợp. |
| IMP-T60-038 | C | Tiền trả trước thuê mua do các bên thỏa thuận, không quá 50%; bỏ khẳng định có mức thông thường bắt buộc 20%. |
| IMP-T60-039 | D | Ngoại lệ về quyền sở hữu nhà ở của cá nhân nước ngoài kết hôn với công dân Việt Nam và sinh sống tại Việt Nam. |
| IMP-T60-071 | A | Phân biệt cá nhân nước ngoài với các nhóm người sử dụng đất được liệt kê; bỏ nhận xét về bộ nhiễu cũ. |
| IMP-T60-085 | B | Ngoại lệ quyền sử dụng đất đối với tài sản hình thành trong tương lai dùng bảo đảm; bỏ giải thích về bảo lưu/truy đòi không tương ứng. |

Bản ghi trước sửa, giải thích trước–sau, lý do và khóa nằm tại `editorial/exam-explanation-repairs-final-2026-10-09.json`. Không đổi bốn đáp án, khóa đúng hoặc lastVerified.

## Biên soạn và đối chiếu

Hai bảng nội dung `editorial/variant-final-40-authored-a-2026-10-09.json` và `editorial/variant-final-40-authored-b-2026-10-09.json` chứa 20 câu mỗi bảng. Khóa đối chiếu và nhận xét của cả 40 câu nằm tại `editorial/variant-final-40-2026-10-09.json`, đồng thời cập nhật hồ sơ đề nhập lên 123 câu.

Biến thể thay cách đặt vấn đề hoặc tình huống: trả tiền đất hàng năm so với một lần; cá nhân nước ngoài so với tổ chức có vốn nước ngoài; thuê mua và chuyển nhượng hợp đồng nhà ở xã hội; thời hạn năm/sáu năm; đợt thanh toán đầu gồm cả tiền đặt cọc; giới hạn 15/20 ngày; trách nhiệm hai năm đối với nghĩa vụ cũ của thành viên hợp danh. Mỗi biến thể được đối chiếu với toàn bộ bộ đáp án hiện có, không thay từ hoặc thêm tiền tố để đủ số lượng.

Đã tải lại chín nguồn chính thức liên quan; mọi HTTP 200 và SHA-256 PDF khớp hồ sơ chứng cứ. Kết quả tại `variant-final-40-source-checks-2026-10-09.json`; điều khoản tại `exam-legal-evidence-2026.json`. Dùng pháp luật tương ứng tình huống tháng 10/2026; không áp dụng Luật Công chứng sửa đổi 04/2026/QH16 có hiệu lực 01/01/2027. Xác minh nguồn này không chứng nhận đã kiểm tra mọi sửa đổi hoặc toàn ngân hàng.

Script áp dụng giữ các kiểm tra phạm vi, khóa độc lập, liên kết chứng cứ, trùng lời dẫn và bảo toàn bản ghi. Giải thích chỉ được chuyển từ giá trị trước sang giá trị sau đã duyệt trong đúng năm ID, với bản ghi trước sửa phải khớp hoàn toàn.

## Bảo toàn và kiểm thử

`variant-final-40-preservation-2026-10-09.json` xác nhận:

- Đúng 40 bản ghi thay đổi, thêm đúng 80 lời dẫn và sửa đúng năm giải thích.
- Giữ nguyên câu gốc, ID, trạng thái, bốn đáp án, khóa, căn cứ, nguồn và lastVerified; các thay đổi còn lại là metadata audit đã giới hạn.
- Những bản ghi ngân hàng khác và 543 quyết định đã có giữ nguyên.
- Áp dụng lại không đổi dữ liệu hoặc báo cáo.

**59/59 kiểm thử đạt**, kết quả tại `variant-final-40-tests-2026-10-09.tap`:

```sh
node --test --test-isolation=none --test-reporter=tap tests/*.test.cjs
python scripts/audit-bank.py bank-audit-variants-2026-10-09.json
git diff --check
```

Kiểm thử dùng Node và DOM giả lập, chưa thay thao tác thật trên điện thoại hoặc kiểm thử máy chủ thực.

Ứng dụng tải 11 file ngân hàng tổng **1.892.301 byte**; gzip thử 246.707 byte, không khẳng định máy chủ nén như vậy. Phân tích JSON trung bình khoảng 3,82 ms trên Node24 cục bộ qua 50 vòng. Hồ sơ reports/editorial không được tải khi làm đề. Ngân hàng mới đổi dấu vân tay mã CC2; cần tạo mã mới.

Trạng thái cuối: `VARIANT_SCOPE_COMPLETE_LEGAL_REVIEW_NOT_CERTIFIED`, `remainingIds: []`, `allActiveLegallyRecertified: false`; không tự đánh dấu READY.
