# CongchungVND — Lộ trình rà soát 438 câu (15/10/2026)

## Trạng thái và phạm vi
- Ngân hàng: 813 bản ghi; 794 active, 19 archived.
- Năm tệp nâng cấp chuyên sâu chứa 356 ID riêng biệt.
- Còn 438 ID active ngoài năm nhóm.
- Phân loại sơ bộ bằng tiêu chí hình thức: **P1 viết lại sâu 27**, **P2 chỉnh cục bộ 290**, **P3 tạm giữ nguyên 121**. Các số này **chưa phải kết luận đọc thủ công**; được phép điều chỉnh nhóm khi có lý do.
- **Chỉ kiểm thử một lần sau khi hoàn thành cả bốn giai đoạn.** Không chạy kiểm thử giữa các đợt.

## Thứ tự thực hiện
1. **P1 — 27 ứng viên viết lại sâu.** Đọc từng biến thể, 4 đáp án, giải thích, căn cứ; sửa câu ghi nhớ, dễ đoán, thiếu tình huống. Không ép viết lại câu vốn đạt.
2. **P2 — 290 ứng viên chỉnh cục bộ.** Chia lô khoảng 50 câu; ưu tiên nhiễu yếu, diễn đạt cứng, quan hệ dữ kiện thiếu mượt. Chỉ sửa phần thực sự yếu; nâng lên P1 khi cần.
3. **P3 — 121 ứng viên giữ nguyên.** Đọc xác nhận; giữ nguyên nếu đạt, chuyển nhóm nếu phát hiện lỗi.
4. **P4 — kiểm tra chéo toàn bộ 438 câu**, sự nhất quán biến thể–đáp án–giải thích–căn cứ và trùng lặp; **sau khi kết thúc P4 mới chạy một đợt kiểm thử tổng thể** theo chỉ đạo.

## Tiêu chí
- Không hỏi trực diện “Điều X quy định gì?”; tăng vận dụng, không tạo độ khó giả.
- Tình huống tự nhiên, đủ dữ kiện quyết định, không rườm rà.
- Đáp án nhiễu hợp lý, đồng dạng, không lộ bằng từ tuyệt đối hay chênh độ dài.
- Bảo toàn đáp án đúng và cơ sở pháp lý; nếu có nghi ngờ pháp lý, đánh dấu LEGAL_HOLD trước khi thay đổi.
- Mỗi ID có quyết định KEEP / LOCAL_EDIT / DEEP_REWRITE / LEGAL_HOLD, lý do và commit. Không ghi DONE khi chưa thực hiện.

## Danh sách P1 đã nhận diện (ưu tiên đọc)
CC-082; VER26-067; VER26-072; IMP-SEP24-017; IMP-SEP24-020; IMP-SEP24-050; IMP-T60-005; IMP-T60-009; IMP-T60-036; IMP-T60-037; IMP-T60-053; IMP-T60-060; IMP-T60-071; IMP-T60-076; IMP-SEP24-031; IMP-T60-018; IMP-T60-056; IMP-T60-059.

**Lưu ý:** 18 ID trên là các ID P1 được khôi phục từ kết quả phân loại trước; còn 9 ID cần đối chiếu lại với bộ lọc để chốt danh sách 27. Không tự nhận đã hoàn thành 27/27 nếu chưa đối chiếu.

## Nhật ký
- 2026-10-15: Lập kế hoạch và ưu tiên, ghi yêu cầu không kiểm thử trước khi hoàn thành P4.

## Giai đoạn 1 — Nhật ký thực hiện (15/10/2026)
- **18/27 ứng viên ưu tiên đã được biên tập câu dẫn biến thể đầu tiên** theo hướng tình huống thực tế; **9 ứng viên còn lại chưa chốt ID/biên tập**.
- 15 câu trong `data/imported-exams-2026.json`: commit `0cf36368f782c00ba9c39634625579d982b55e0b`.
- 1 câu `CC-082` trong `data/questions.json`: commit `77ee92e34ca7fb01e754c139c28584fe46547cf9`.
- 2 câu `VER26-067`, `VER26-072` trong `data/validated-2026.json`: commit `d0946519e0dd0998de32c42b9b5dce0d7a5a8e64`.
- **Chưa chỉnh ba đáp án nhiễu và các biến thể còn lại của 18 câu**; cần rà tiếp trước khi đánh dấu P1 hoàn tất. Không thay đáp án đúng, giải thích hay căn cứ pháp lý trong các commit trên.
- **Chưa kiểm thử**, theo yêu cầu đợi đến sau giai đoạn 4.
- Việc phân loại cần đối chiếu lại sau khi câu gốc thay đổi; không chạy lại bộ lọc trên dữ liệu đã sửa để suy ngược danh sách P1 ban đầu.
