# Báo cáo hoàn thiện ngân hàng — lượt tiếp 07/10/2026

Đã bổ sung 80 câu REFIN26 và tích hợp vào loader. Sau khi ngừng dùng ba câu trùng năng lực, ngân hàng tăng từ 506 lên 583 câu active. Đây là báo cáo một lượt tiếp có phạm vi rõ, chưa phải tuyên bố hoàn tất mục tiêu 500 câu thay thế.

| Chỉ tiêu | Trước lượt tiếp | Sau lượt tiếp |
|---|---:|---:|
| Tổng bản ghi lưu | 1.022 | 1.102 |
| Active | 506 | 583 |
| Archived | 516 | 519 |
| Review trong các file ngân hàng | 0 | 0 |
| File được app tải | 9 | 10 |
| Bản ghi app tải trước lọc | 522 | 602 |

Thêm mới: 80. Chuyển từ EXP sang active: 0. Ngừng dùng do trùng năng lực: 3, lưu archived thay vì xóa ID. Viết lại câu cũ: 0; một bản nháp mới được xây lại vì lặp năng lực, 19 bản nháp cải thiện nhiễu trước khi xuất bản. Các số này không cộng thêm vào 80 câu mới.

Ba câu ngừng dùng: VER26-008 → SRC26-012; VER26-057 → VER26-021; COMP26-DAT-002 → VER26-055. Câu COMP26-DAT-002 thuộc lô vừa thêm trước đó nhưng vẫn bị loại khỏi bộ active khi phát hiện trùng; không coi đã có hồ sơ pháp lý là lý do phải giữ.

## Phân bố kiến thức

Phân nhóm chính kế thừa từng ID từ ma trận trước. Câu giao thoa chỉ tính một nhóm chính để không làm tổng vượt 100%.

| Nhóm | Số câu | Tỷ lệ | Mục tiêu |
|---|---:|---:|---:|
| Luật Công chứng – công chứng viên – TCHNCC | 76 | 13.04% | 15% |
| Quy trình, thủ tục và nghiệp vụ công chứng | 116 | 19.90% | 22.5% |
| Dân sự – giao dịch – đại diện – nghĩa vụ | 111 | 19.04% | 13.75% |
| Đất đai – nhà ở – kinh doanh BĐS | 77 | 13.21% | 13.75% |
| Hôn nhân và gia đình – tài sản vợ chồng | 53 | 9.09% | 8.75% |
| Thừa kế | 58 | 9.95% | 10% |
| Doanh nghiệp và giao dịch liên quan | 25 | 4.29% | 5% |
| Chứng thực và pháp luật liên quan | 16 | 2.74% | 3.75% |
| Đạo đức nghề nghiệp – trách nhiệm – xử lý vi phạm | 19 | 3.26% | 3.75% |
| Tập sự, kiểm tra kết quả tập sự HNCC | 26 | 4.46% | 3.75% |
| Ngoài 10 nhóm mục tiêu (lao động) | 6 | 1.03% | 0% |

Tỷ trọng Luật Công chứng/tổ chức hành nghề tăng từ 7,11% lên 13,04%; thủ tục tăng từ 18,18% lên 19,90%. Dân sự vẫn cao hơn mục tiêu; chứng thực, doanh nghiệp và thủ tục còn cần bổ sung. Không đổi nhãn của câu cũ để làm đẹp tỷ lệ.

## Độ khó và dạng câu

| Độ khó | Số câu | Tỷ lệ |
|---|---:|---:|
| Nhận biết | 89 | 15.27% |
| Hiểu luật | 119 | 20.41% |
| Vận dụng | 296 | 50.77% |
| Vận dụng cao | 79 | 13.55% |

Vận dụng và vận dụng cao: 375/583 = 64.32%. Vận dụng cao vẫn dưới mục tiêu 20%. Nhãn chưa hiệu chỉnh bằng thống kê người học; không chứng nhận độ khó bằng tỷ lệ nhãn.

Dạng câu toàn ngân hàng: direct: 92, short_case: 296, exception: 46, integrated: 28, synthesis: 20, workflow: 87, true_false: 5, choose_case: 9. Một số nhãn lịch sử `integrated`/`synthesis` chưa được chuẩn hóa theo một rubric chung; không gộp máy móc để tuyên bố đã đạt ma trận dạng câu.

## Nội dung pháp lý và chất lượng

80 câu mới có stem tháng 10/2026, khóa duy nhất, giải thích, Điều/Khoản/Điểm tương ứng và chứng cứ điều khoản liên kết. Các cụm cùng điều kiểm tra nhánh khác nhau: người xin bản sao là bên giao dịch/người liên quan/người thừa kế/chủ thể kế thừa pháp nhân; thừa kế đất có toàn bộ người không thuộc diện cấp giấy, nhóm tư cách hỗn hợp và giai đoạn chưa chuyển nhượng. Không chỉ đổi tên người để nhân câu.

Đối chiếu luật hiện hành với mốc 01/01/2027. Lô mới không dùng Luật 04/2026 để giải tình huống hiện tại. Kiểm tra Nghị định 104/2025 đã bị bãi bỏ Điều 64; hai câu niêm yết viện dẫn Điều 44 không bị loại theo trạng thái chung. Kiểm tra Nghị định 18/2026 bị bãi bỏ Điều 7 bởi khoản 4 điểm b Điều 21 Nghị định 65/2026, thuộc quản tài viên; không tự kết luận các quy định chứng thực trong VBHN 753 hết hiệu lực. Không phát hiện cần sửa khóa pháp lý mới trong lượt này; ba thay đổi câu cũ là quyết định trùng năng lực. Chi tiết tại effectiveness-refinement-2026-10-07.json.

Kiểm tra cấu trúc trên toàn 1.102 bản ghi: không trùng ID, không trùng chính xác stem, single có đúng một khóa, không có cờ cấu trúc/nguồn/căn cứ ở bộ active. Sáu cặp gần stem là các cặp cũ đã có quyết định tại near-stem-decisions-2026-10-07.json. Kết quả heuristic không chứng minh đã hết mọi trùng năng lực hoặc mọi lỗi pháp luật.

## Tích hợp và kiểm thử

App tải refinement-2026.json cùng chín file trước, vẫn loại archived và không tải EXP. Không đổi progress.js hoặc schema kết quả. Các bài đã nộp giữ bản chụp; mã chia sẻ của phiên bản ngân hàng cũ có thể bị từ chối theo cơ chế kiểm tra phiên bản đã có, cần tạo mã đề mới cho lần thi mới.

45/45 kiểm thử Node đã đạt; node --check app.js và git diff --check đều đạt. Log tại refinement-tests-2026-10-07.tap. Kiểm tra tải GitHub Pages được ghi riêng trong báo cáo phát hành. Kiểm thử dùng DOM giả lập, không được trình bày như đã thao tác giao diện trình duyệt thật.

## Phần chưa hoàn tất

- 500 câu EXP cơ học vẫn archived; hai lô COMP26 và REFIN26 có 160 bản ghi mới, 159 còn active. Để có 500 câu mở rộng active có giá trị còn thiếu 341, không phải chỉ cần bật lại EXP.
- Các nhánh nguồn DOCX chưa chứng nhận trong báo cáo nguồn tiếp tục review ở danh mục nguồn, dù các file ngân hàng không còn status review.
- Không cập nhật lastVerified hàng loạt cho câu cũ. 93 câu core, 79 câu COMP26 còn active và 80 câu REFIN26 có hồ sơ kiểm định ngày 07/10; các câu còn lại không được coi đã kiểm định lại toàn nội dung trong lượt này.
- Tiếp tục cân bằng thủ tục, chứng thực, doanh nghiệp và các tình huống giao thoa khó; rà năng lực toàn bộ bộ cũ theo rubric thống nhất.

Tài liệu thực hành: [Hai đề luyện 40 câu và bài giải](refinement-exams-2026-10-07.md). Căn cứ: [chứng cứ lô mới](refinement-legal-evidence-2026.json), [trích điều khoản](refinement-provisions-2026.json), [quyết định biên tập](refinement-editorial-decisions-2026.json), [audit cấu trúc](bank-audit-refinement-after.json).
