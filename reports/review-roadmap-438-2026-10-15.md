# CongchungVND — Hoàn tất bốn giai đoạn biên tập (15/10/2026)

## Kết quả hiện tại

**Đã hoàn tất P1 → P2 → P3 → P4 về nội dung; chưa chạy kiểm thử tự động, kiểm tra trình duyệt hoặc kiểm tra web triển khai. Chưa đẩy các commit của phiên này lên GitHub.**

| Phạm vi | Số lượng |
|---|---:|
| Bản ghi ngân hàng | 813 |
| Active sau lớp trình bày | 793 |
| Archived sau lớp trình bày | 20 |
| ID thuộc năm nhóm đã nâng cấp riêng | 356 |
| Active ngoài năm nhóm, rà trong đợt này | 437 |
| Viết lại sâu (quyết định cuối) | 26 |
| Chỉnh cục bộ (quyết định cuối) | 163 |
| Giữ nguyên (quyết định cuối) | 248 |

### Sửa số liệu của kế hoạch cũ

Số 438 trước đây đã tính cả `CC-082`. Câu này có trạng thái active ở tệp gốc nhưng đã được lớp `application-wording-2026.json` chuyển sang archived vì chỉ hỏi số điều luật. Không khôi phục câu này. Phạm vi thực tế còn **437 active**.

Kế hoạch cũ ghi 27 P1, 290 P2, 121 P3 nhưng chỉ lưu 18 ID P1; không có bảng ID đầy đủ cho các nhóm. Đợt này giữ dấu vết đó, lấy 17 P1 còn active và bổ sung 9 ứng viên được đọc chọn lại. Không tuyên bố đã khôi phục 9 ID lịch sử. Danh sách P2/P3 được chốt công khai theo thứ tự tệp nạp sau khi tách P1, phục vụ kiểm đếm; không dùng nó làm kết luận chất lượng tự động.

## Bốn giai đoạn

| Giai đoạn | Công việc và trạng thái |
|---|---|
| P1 | Hoàn thiện 26 ứng viên active; thay câu hỏi thuộc luật, tình huống lộ đáp án và nhiễu xa chủ đề. Rà các biến thể đang hiển thị. `CC-082` giữ archived. Commit `77ecb76`. |
| P2 | Đọc 290 ứng viên. Chỉnh riêng 47 bộ phương án, đồng thời làm gọn giải thích; tổng 139 ID ngoài P1 được sửa ở commit `1235b7c`. Các câu đủ chất lượng được giữ, không ép sửa để đạt số lượng. |
| P3 | Đọc 121 ứng viên dự kiến giữ. Giữ 116; sửa cục bộ 5 câu: `CAL26-070`, `HARD26-024`, `HARD26-074`, `HARD26-081`, `HARD26-096`. Commit `a6ba79e`. |
| P4 | Đối chiếu câu dẫn, biến thể thực tế sau lớp trình bày, phương án, khóa, giải thích và căn cứ trong toàn bộ 437 ID. Sửa 42 ID về trình bày; bổ sung khoản 4 Điều 50 cho `CAL26-027`, Điều 296 BLDS cho `HARD26-041`; làm rõ hai giải thích khác. Đã hoàn tất phần biên tập; kiểm thử vẫn để sau. |

Các số ở từng giai đoạn có giao nhau. Quyết định cuối tính một lần mỗi ID là **26 + 163 + 248 = 437**. Chỉnh dấu câu, rút giải thích không được tính là tăng độ khó thực chất.

## Những điểm đã xử lý

- Sửa nhầm vai người nhận thế chấp trong `IMP-T60-037`; không để người vay bị nhầm thành bên nhận thế chấp.
- Thay nhiễu “Sở Tư pháp tùy ý chấm dứt” trong `IMP-T60-076` bằng việc chủ sở hữu bán nhà đang có quyền hưởng dụng.
- Phân biệt phần W được chia ban đầu và khoản bổ sung phần bắt buộc ở `HARD26-081`.
- Làm rõ T nhận cọc của người mua ở `HARD26-096`; khớp “cho thuê” trong đáp án với câu dẫn `CAL26-070`.
- Rà lớp `application-wording`: sửa câu bị gãy sau khi lược số điều luật, giữ giả thiết chính sách đất ở `VER26-051` và nhóm giấy tờ tại `FAM26-002`.
- Đồng bộ dấu vân tay nguồn cho những câu gốc đã sửa, kể cả lỗi tồn từ đợt sửa 18 câu trước. Đây là phần cập nhật dữ liệu, **không phải kết quả kiểm thử cơ chế tải**.
- Giữ ID, khóa đúng và trạng thái các câu đang hoạt động. Không thay `lastVerified` để giả lập một đợt kiểm định pháp lý mới.

## Giới hạn và việc còn để sau

1. **Không có bộ kiểm thử nào được chạy trong phiên này.** Cần chạy một đợt kiểm thử tổng thể khi Madam An yêu cầu: tải đủ các lớp dữ liệu và dấu vân tay; khóa/chấm điểm ở cả hai chế độ; biến thể; mã đề; các kiểm tra hồi quy sẵn có. Chưa có chứng cứ trình duyệt hay web triển khai cho các sửa đổi này.
2. Đối chiếu nội bộ và tra trực tiếp các điều khoản cần sửa không phải xác minh lại toàn bộ hiệu lực mọi văn bản. Độ khó vẫn là đánh giá biên tập, chưa có kết quả thử nghiệm người học.
3. `CAL26-093` và `HARD26-010` còn gần nhau về mô hình người thừa kế mới, giá lúc chia; đã ghi nhận, chưa loại hoặc viết lại thêm. Không tuyên bố ngân hàng hết trùng ý. Các cặp cùng chủ đề khác có lý do giữ trong nhật ký.
4. **GitHub đang bị chặn công bố:** auto-review từ chối `git push origin main`, nêu việc đẩy nhánh mặc định là thay đổi bên ngoài có thể công bố dữ liệu chưa kiểm thử và yêu cầu lần này chưa được xác định bao gồm quyền công bố. Không thử đường vòng; cần Madam An xác nhận việc đẩy các commit đã hoàn thiện.

## Hồ sơ từng ID

[`editorial-review-437-2026-10-15.json`](editorial-review-437-2026-10-15.json) ghi đủ danh sách P2/P3, quyết định từng ID, lý do, bản trước/sau khi sửa, biến thể thực tế trước/sau, nguồn đối chiếu, giao nhau giữa các giai đoạn và trạng thái chưa kiểm thử.

## Lịch sử cần giữ

- `bb65b0ae3bb54b23ce6367c72d43f3ca5d320a3d`: lưu kế hoạch sơ bộ 438.
- `0cf36368f782c00ba9c39634625579d982b55e0b`: sửa câu dẫn đầu tiên 15 câu imported.
- `77ee92e34ca7fb01e754c139c28584fe46547cf9`: sửa câu gốc `CC-082`, sau đó phát hiện câu vẫn archived ở lớp trình bày.
- `d0946519e0dd0998de32c42b9b5dce0d7a5a8e64`: sửa câu dẫn đầu tiên hai câu validated.
- `db1519c`: nhật ký xác nhận mới sửa 18 câu dẫn, chưa hoàn tất các biến thể và nhiễu. Đó là mốc đầu vào của phiên này, không phải P1 hoàn thành.
