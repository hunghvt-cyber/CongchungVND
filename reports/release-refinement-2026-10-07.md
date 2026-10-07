# Phát hành lô REFIN26 — 07/10/2026

Commit dữ liệu và ứng dụng: `fade4e04cec686dea5cc194dafe98e723f00a716`.

- GitHub Pages: [lần triển khai](https://github.com/hunghvt-cyber/CongchungVND/actions/runs/37653915189) đã hoàn thành thành công, run `37653915189`.
- 45/45 kiểm thử Node đạt. `node --check app.js` và `git diff --check` đạt.
- Hai đề luyện 40 câu đã kiểm tra 80/80 ánh xạ chữ cái sau xáo phương án với nội dung đáp án đúng trong JSON.
- Sau triển khai, kiểm tra HTTP 12/12 file có SHA-256 khớp bản đã kiểm định: index, app.js và 10 file ngân hàng. App tải 602 bản ghi, có 583 active; không tải năm file EXP.
- 80 câu mới, 3 câu trùng ngừng dùng và giữ archived. Lịch sử/khóa của câu cũ không bị xóa; progress.js và schema kết quả không đổi.

Chứng cứ HTTP: [refinement-pages-verification-2026-10-07.json](refinement-pages-verification-2026-10-07.json). Có thể chạy lại bằng `python scripts/verify-pages.py --commit <commit>`.

Kiểm thử ứng dụng dùng DOM giả lập và kiểm tra HTTP, chưa xác nhận thao tác trình duyệt thật hoặc ghi kết quả lên backend thực tế trong lượt này. Các báo cáo nguồn còn nhánh review; không coi 583 active là đã hoàn thiện riêng 500 EXP hay đã kiểm định lại mọi câu cũ trong ngày này.

Báo cáo đầy đủ: [refinement-2026-10-07.md](refinement-2026-10-07.md). Tài liệu: [hai đề luyện và bài giải](refinement-exams-2026-10-07.md).
