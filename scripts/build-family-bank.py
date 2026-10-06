"""Author family-law cases from reviewed source themes, with article evidence.

Original DOCX and official PDF inputs stay outside the repository.
"""
from pathlib import Path
import json, re, hashlib, random, collections
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT.parent
DATE='2026-10-06'; SOURCE='USER-EXAM-FAMILY'
DOC=next((WORK/'upload').glob('*HO*N*GIA*.docx'))
CONFIG={
 'HN':('Luật Hôn nhân và gia đình số 52/2014/QH13 (đối chiếu VBHN 121/VBHN-VPQH năm 2025)','OFFICIAL-HNGD-HN25','HNGD-HN-0.txt','https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/8/46059/58694-1-20251299-1300121-vbhn-vpqh.pdf',['HNGD-HN-0.pdf']),
 'CC':('Luật Công chứng số 46/2024/QH15','OFFICIAL-CC24','CC-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat46.pdf',['CC-0.pdf']),
 'DS':('Bộ luật Dân sự số 91/2015/QH13','OFFICIAL-BLDS15','BLDS-full.txt','https://vanban.chinhphu.vn/?pageid=27160&docid=183188',['BLDS-0.pdf','BLDS-1.pdf']),
 'ND':('Nghị định số 126/2014/NĐ-CP','OFFICIAL-ND126-2014','ND126-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2015/01/126-nd.signed.pdf',['ND126-0.pdf'])}
ROWS=[]
def add(origin,difficulty,refs,stem,key,wrong,reason,hint,topic='Hôn nhân và gia đình – tài sản vợ chồng'):
 ROWS.append(dict(origin=origin,difficulty=difficulty,refs=refs,stem=stem,key=key,wrong=wrong,reason=reason,hint=hint,topic=topic))
add('1.6','advanced',['CC:69:1:b','CC:69:2'],
 'Cha mẹ còn sống đã công chứng thỏa thuận tài sản. Con gái có quyền, nghĩa vụ liên quan được chứng minh, nhưng cha mẹ chưa đồng ý cấp bản sao cho con. Con yêu cầu văn phòng đang lưu bản gốc cấp ngay vì mình là người liên quan. Chỉ xét căn cứ yêu cầu này, xử lý nào đúng?',
 'Chưa đủ điều kiện cấp theo yêu cầu người liên quan; phải có sự đồng ý của người yêu cầu công chứng',
 ['Cấp ngay vì chứng minh quyền liên quan đã thay thế mọi yêu cầu về sự đồng ý','Từ chối vĩnh viễn vì người con không trực tiếp ký giao dịch','Chuyển đến bất kỳ văn phòng nào trong tỉnh, nơi lưu bản gốc không liên quan'],
 'Điểm b khoản 1 Điều 69 công nhận người có quyền, nghĩa vụ liên quan là nhóm được yêu cầu cấp bản sao, nhưng đồng thời yêu cầu sự đồng ý của người yêu cầu công chứng. Câu đã xác định cha mẹ còn sống nên không dùng cơ chế đồng ý của người thừa kế. Khoản 2 xác định nơi cấp là tổ chức đang lưu bản gốc. Không kết luận mọi người con đều bị loại hoặc mọi người liên quan đều được cấp ngay.',
 'Kiểm tra đồng thời tư cách người xin, sự đồng ý và nơi lưu bản gốc.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('1.5','advanced',['CC:42:1:b','CC:42:1:d','CC:42:7'],
 'Hồ sơ công chứng thỏa thuận tài sản có bản sao chứng thực căn cước và bản sao chứng thực giấy đăng ký kết hôn; không có bản chính hai giấy này. Tổ chức chưa khai thác được thông tin từ cơ sở dữ liệu. Giấy kết hôn thuộc nhóm giấy tờ liên quan tại điểm d khoản 1 Điều 42. Phân biệt nào đúng trước khi CCV ký lời chứng?',
 'Bản sao chứng thực giấy kết hôn có thể đáp ứng ngoại lệ tại điểm d; căn cước vẫn phải xuất trình bản chính để đối chiếu',
 ['Cả hai bản sao đều thay bản chính vì cùng có chứng thực','Cả hai đều bắt buộc có bản chính, không có ngoại lệ cho giấy kết hôn','Chỉ căn cước được dùng bản sao chứng thực, giấy kết hôn tuyệt đối không được'],
 'Khoản 7 Điều 42 yêu cầu đối chiếu bản chính các giấy tại điểm b, c, d nhưng cho phép bản sao từ sổ gốc hoặc bản sao chứng thực khi không có bản chính đối với nhóm điểm d. Ngoại lệ này không tự mở rộng sang giấy tùy thân tại điểm b. Câu loại trừ trường hợp đã khai thác được dữ liệu theo khoản 1 để tránh lẫn hai cơ chế.',
 'Phân loại giấy theo điểm b, c, d trước khi áp dụng ngoại lệ bản sao.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('1.1','application',['CC:53:2'],
 'Hai vợ chồng cùng yêu cầu công chứng văn bản chấm dứt thỏa thuận chia tài sản đã công chứng ở Văn phòng A. A vẫn hoạt động bình thường và lưu hồ sơ. Văn phòng B cùng tỉnh thuận tiện hơn. Chỉ xét nơi công chứng việc chấm dứt, hướng dẫn nào đúng?',
 'Hướng dẫn thực hiện tại tổ chức đã công chứng là A, theo khoản 2 Điều 53',
 ['B được làm vì mọi tổ chức cùng tỉnh có thể chấm dứt giao dịch đã công chứng','B được làm nếu hai vợ chồng cùng cam kết không tranh chấp','B được làm vì luật chỉ hạn chế nơi sửa đổi, không hạn chế nơi chấm dứt'],
 'Khoản 2 Điều 53 hiện hành bao gồm cả sửa đổi, bổ sung, chấm dứt và hủy bỏ giao dịch đã công chứng. Khi tổ chức cũ hoạt động bình thường, nơi đã công chứng thực hiện thủ tục này. Các cơ chế lưu hồ sơ khi tổ chức chấm dứt, chuyển đổi, giải thể hoặc tạm ngừng chưa phát sinh. Sự đồng ý của hai người không thay điều kiện về nơi thực hiện.',
 'Đọc đủ cả từ chấm dứt trong luật hiện hành, rồi kiểm tra tình trạng tổ chức cũ.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('1.4;extension','application',['HN:41:4'],
 'Việc chia tài sản trong thời kỳ hôn nhân của vợ chồng đã được quyết định bằng bản án có hiệu lực. Nay cả hai thỏa thuận chấm dứt hiệu lực việc chia và muốn chỉ công chứng thỏa thuận, không yêu cầu Tòa án công nhận. Điều kiện còn thiếu là gì?',
 'Thỏa thuận chấm dứt phải được Tòa án công nhận',
 ['Chỉ cần cả hai ký trước CCV là thay thế được việc công nhận của Tòa án','Chỉ cần cơ quan đăng ký tài sản đóng dấu lên bản án cũ','Chỉ cần nộp thỏa thuận cho cơ quan đăng ký tài sản, không cần Tòa án công nhận'],
 'Khoản 4 Điều 41 đặt điều kiện riêng cho việc chia ban đầu bằng bản án, quyết định có hiệu lực của Tòa án: thỏa thuận chấm dứt phải được Tòa án công nhận. Không được áp cách xử lý của một thỏa thuận chia thuần túy để bỏ qua điều kiện này. Câu không yêu cầu chấm dứt quan hệ hôn nhân và không coi đăng ký tài sản là việc công nhận của Tòa án.',
 'Xác định việc chia ban đầu do vợ chồng thỏa thuận hay do bản án.')
add('1.4','advanced',['HN:41:2','HN:46:2'],
 'Nhà đã chia cho vợ và đăng ký là tài sản riêng. Khi chấm dứt hiệu lực việc chia, hai người muốn thỏa thuận rõ nhà đó trở lại tài sản chung và sẵn sàng đáp ứng hình thức, thủ tục đăng ký tương ứng. Nhận định nào đúng về khả năng thỏa thuận?',
 'Có thể thỏa thuận khác với việc giữ riêng; việc đã đăng ký riêng không tự cấm nhập nhà vào tài sản chung',
 ['Đã đăng ký riêng thì luật cấm trở lại tài sản chung trong thời kỳ hôn nhân','Chấm dứt hiệu lực chia tự đủ để nhà trở thành tài sản chung dù không có nội dung nhập lại','Chỉ cần xóa tên vợ trên giấy chứng nhận, không cần thỏa thuận hay hình thức luật định'],
 'Khoản 2 Điều 41 giữ tài sản đã chia là riêng nhưng có ngoại lệ khi vợ chồng thỏa thuận khác. Khoản 2 Điều 46 yêu cầu thỏa thuận nhập tài sản phải đáp ứng hình thức luật định đối với tài sản đó. Điểm quyết định là có thỏa thuận rõ và thực hiện đúng điều kiện, không phải việc đã đăng ký riêng khiến lựa chọn này bị cấm. Câu không đồng nhất văn bản công chứng với việc đã hoàn tất đăng ký.',
 'Tìm cụm trừ trường hợp có thỏa thuận khác, rồi kiểm tra hình thức và đăng ký.')
add('2.3;extension','understanding',['HN:39:1'],
 'Hai vợ chồng lập văn bản chia một khoản tiền chung ngày 02/10, ghi rõ có hiệu lực ngày 15/10; với khoản tiền này không có yêu cầu hình thức đặc biệt. Ngày 06/10, chồng nói khoản tiền đã thành riêng chỉ vì văn bản đã được lập. Đánh giá nào đúng?',
 'Chưa thể dựa vào ngày lập để kết luận đã có hiệu lực; phải theo mốc 15/10 được ghi trong thỏa thuận',
 ['Hiệu lực luôn tính ngày lập, mọi mốc các bên ghi đều không được công nhận','Hiệu lực ngay khi một bên thông báo cho ngân hàng, dù chưa đến mốc ghi trong văn bản','Hiệu lực tính từ ngày ngân hàng đổi tên sổ trong mọi trường hợp chia tiền'],
 'Khoản 1 Điều 39 ưu tiên thời điểm vợ chồng thỏa thuận và ghi trong văn bản; ngày lập chỉ là mốc mặc định khi văn bản không xác định thời điểm. Câu giới hạn ở tài sản không có yêu cầu hình thức đặc biệt để không lẫn khoản 2. Việc chia trong thời kỳ hôn nhân không cần đợi ly hôn, và ngày đổi tên sổ không thay thế nội dung của quy tắc này.',
 'Kiểm tra văn bản có mốc hiệu lực riêng trước khi dùng mốc mặc định.')
add('3.3;extension','application',['HN:42:2:đ'],
 'Chồng có nghĩa vụ nộp thuế đã xác định. Hai vợ chồng thừa nhận chuyển toàn bộ tài sản chung sang vợ bằng việc chia tài sản nhằm làm chồng không còn tài sản thực hiện nghĩa vụ đó. Nhận định nào đúng?',
 'Việc chia nhằm trốn nghĩa vụ thuế thuộc trường hợp vô hiệu theo Điều 42',
 ['Hợp pháp nếu vợ chồng tự nguyện vì nghĩa vụ thuế không phải nợ tư nhân','Hợp pháp nếu tài sản chưa bị kê biên, dù mục đích trốn thuế đã được xác định','Chỉ vô hiệu khi vợ cũng là người trực tiếp bị ấn định thuế'],
 'Điểm đ khoản 2 Điều 42 nêu rõ chia tài sản nhằm trốn nghĩa vụ nộp thuế hoặc nghĩa vụ tài chính khác đối với Nhà nước là trường hợp vô hiệu. Câu đã xác định mục đích trốn tránh nên không phải suy đoán từ việc chia thông thường. Tự nguyện và chưa kê biên không loại bỏ điều cấm; không cần cả hai người cùng là chủ thể bị ấn định thuế.',
 'Đọc mục đích và loại nghĩa vụ, không chỉ kiểm tra có tranh chấp tư nhân hay không.')
add('3.3;extension','advanced',['HN:42:1'],
 'Vợ chồng muốn chia hết nguồn tài sản đang bảo đảm việc chữa bệnh cho con 10 tuổi. Hồ sơ xác định cách chia này ảnh hưởng nghiêm trọng quyền, lợi ích hợp pháp của con; không có mục đích trốn nợ. Hai người nói chỉ chia trốn nợ mới bị vô hiệu. Đánh giá nào đúng?',
 'Điều 42 còn có căn cứ vô hiệu do ảnh hưởng nghiêm trọng quyền, lợi ích hợp pháp của con chưa thành niên',
 ['Không trốn nợ thì việc chia luôn hợp lệ, kể cả gây ảnh hưởng nghiêm trọng cho con','Con chỉ có thể phản đối việc chia sau khi đủ 18 tuổi','Con không ký thỏa thuận nên quyền của con không phải yếu tố kiểm tra'],
 'Khoản 1 Điều 42 là căn cứ độc lập với các nghĩa vụ bị trốn tránh ở khoản 2. Bảo vệ con chưa thành niên không phụ thuộc con có là người ký hay không. Câu đã xác định mức ảnh hưởng nghiêm trọng; không suy rằng bất kỳ việc chia nào có con nhỏ cũng vô hiệu, hoặc chỉ cần cam kết chung của cha mẹ là đủ.',
 'Kiểm tra cả lợi ích gia đình, con và mục đích trốn nghĩa vụ; không bỏ một nhóm căn cứ.')
add('5.8','application',['HN:19:1','HN:107:1','HN:115'],
 'Vợ chồng còn đang kết hôn và vừa chia tài sản. Dự thảo ghi từ nay hai bên hết nghĩa vụ chăm sóc nhau và không phải cấp dưỡng cho nhau trong bất kỳ trường hợp nào. Nhận xét nào phù hợp?',
 'Chia tài sản không xóa nghĩa vụ vợ chồng; không thể ghi điều khoản miễn toàn bộ như đề nghị',
 ['Điều khoản hợp lệ vì chia tài sản tương đương chấm dứt hôn nhân','Điều khoản hợp lệ nếu cả hai không yêu cầu quyền lợi đối với con','Điều khoản có thể miễn nghĩa vụ chăm sóc, chỉ phần miễn cấp dưỡng cần xem xét'],
 'Khoản 1 Điều 19 đặt nghĩa vụ quan tâm, chăm sóc, giúp đỡ trong hôn nhân; khoản 1 Điều 107 quy định nghĩa vụ cấp dưỡng không thể thay bằng nghĩa vụ khác hoặc chuyển giao. Điều 115 còn đặt cơ chế cấp dưỡng sau ly hôn khi đủ điều kiện. Chia tài sản không phải căn cứ xóa mọi nghĩa vụ nhân thân. Không suy rằng vợ chồng đang sống chung luôn phải trả tiền cấp dưỡng cho nhau; câu kiểm tra điều khoản miễn toàn bộ trong mọi trường hợp.',
 'Tách việc chia tài sản khỏi tình trạng hôn nhân và nghĩa vụ nhân thân.')
add('3.3','understanding',['HN:38:1','HN:42'],
 'Vợ chồng quản lý tiền khác nhau nên muốn chia một phần tài sản chung; không kinh doanh, không có nghĩa vụ riêng cần trả và không thuộc Điều 42. Chồng cho rằng luật chỉ cho chia để kinh doanh hoặc trả nghĩa vụ riêng. Kết luận nào đúng?',
 'Luật cho thỏa thuận chia một phần hoặc toàn bộ, không giới hạn vào hai lý do chồng nêu',
 ['Chỉ được chia nếu chứng minh sẽ đăng ký doanh nghiệp','Chỉ được chia nếu đã có bản án buộc trả nghĩa vụ riêng','Không được chia một phần, phải chia toàn bộ hoặc không chia'],
 'Khoản 1 Điều 38 thừa nhận quyền thỏa thuận chia một phần hoặc toàn bộ tài sản chung trong thời kỳ hôn nhân, trừ trường hợp Điều 42. Không có điều kiện chỉ nhằm kinh doanh hay thực hiện nghĩa vụ riêng. Câu đã loại trừ căn cứ vô hiệu để kiểm tra đúng sự nhầm lẫn về mục đích; hình thức và điều kiện riêng của từng tài sản vẫn phải được đáp ứng khi thực hiện.',
 'Kiểm tra điều luật hiện hành có thực sự liệt kê lý do như một điều kiện hay không.')
add('3.7;extension','advanced',['ND:14:3'],
 'Sau khi chia tài sản có hiệu lực, chồng dùng tài sản riêng khai thác và thu một khoản tiền. Hồ sơ không xác định được đó là thu nhập do lao động, sản xuất, kinh doanh hay hoa lợi, lợi tức từ tài sản riêng; không có thỏa thuận khác. Khoản tiền được xử lý theo quy tắc nào?',
 'Thuộc sở hữu chung của vợ chồng theo khoản 3 Điều 14 Nghị định 126/2014',
 ['Luôn riêng vì xuất phát từ tài sản riêng, không cần xác định loại thu nhập','Luôn riêng của người trực tiếp nhận tiền vì ngân hàng chỉ ghi một tên','Khoản thu bắt buộc phân theo tỷ lệ đóng góp kinh doanh, không áp quy tắc sở hữu chung'],
 'Khoản 3 Điều 14 xử lý riêng tình huống không phân định được thu nhập lao động, sản xuất, kinh doanh với hoa lợi, lợi tức từ tài sản riêng sau việc chia có hiệu lực: tài sản có được thuộc sở hữu chung. Không áp quy tắc mặc định về hoa lợi, lợi tức riêng khi chưa xác định được bản chất khoản thu. Tên người nhận tiền không giải quyết được điểm pháp lý này.',
 'Phân loại khoản thu trước; nếu không phân định được, đọc quy tắc chuyên biệt.')
add('3.7;extension','application',['ND:14:1','HN:33:1'],
 'Vợ chồng theo chế độ luật định chỉ chia chiếc xe chung cho chồng, không có thỏa thuận khác. Sau đó vợ nhận lương từ công việc của mình trong thời kỳ hôn nhân. Chồng nói chia xe đã làm mọi khoản thu mới của mỗi người thành riêng. Đánh giá nào đúng?',
 'Chia xe không chấm dứt chế độ luật định; tiền lương mới vẫn là tài sản chung theo dữ kiện',
 ['Mọi thu nhập mới đều riêng ngay sau bất kỳ lần chia một tài sản nào','Chỉ lương chồng là chung còn lương vợ là riêng vì vợ không được chia xe','Tiền lương chỉ trở thành chung khi chuyển vào tài khoản đứng tên cả hai người'],
 'Khoản 1 Điều 14 khẳng định chia tài sản trong thời kỳ hôn nhân không chấm dứt chế độ tài sản theo luật định. Khoản 1 Điều 33 xác định thu nhập do lao động trong thời kỳ hôn nhân là tài sản chung. Tiền lương mới trong câu khác với tài sản đã chia hoặc hoa lợi, lợi tức từ tài sản riêng. Không mở rộng hậu quả của việc chia chiếc xe sang toàn bộ thu nhập tương lai.',
 'Tách tài sản đã chia, lợi tức từ tài sản riêng và lương do lao động.')
add('3.7','understanding',['HN:40:1','ND:14:2'],
 'Chia nhà chung cho vợ, hai người ghi rõ tiền thuê phát sinh sau ngày chia có hiệu lực vẫn là tài sản chung. Chồng nay nói nhà riêng thì tiền thuê bắt buộc riêng, điều khoản trên không có giá trị. Nhận định nào đúng?',
 'Luật cho thỏa thuận khác; không thể phủ nhận điều khoản tiền thuê chung chỉ vì nhà đã chia riêng',
 ['Tiền thuê bắt buộc riêng trong mọi trường hợp, không được thỏa thuận khác','Tiền thuê chung làm việc chia nhà tự mất hiệu lực','Tiền thuê chung bắt buộc nhà trở lại sở hữu chung dù các bên không thỏa thuận nhập nhà'],
 'Khoản 1 Điều 40 và khoản 2 Điều 14 xác định phần tài sản chia, hoa lợi, lợi tức theo quy tắc riêng khi không có thỏa thuận khác. Dữ kiện có thỏa thuận tiền thuê chung nên không áp mặc định riêng. Việc xác định tiền thuê chung không tự thay quyền sở hữu riêng đối với căn nhà và không tự chấm dứt việc chia.',
 'Tìm ngoại lệ thỏa thuận khác và phân biệt tài sản gốc với lợi tức.')
add('7.1','advanced',['HN:36','HN:38:1','HN:40:1'],
 'Vợ chồng muốn nhà vẫn thuộc tài sản chung nhưng cho chồng tự thực hiện giao dịch kinh doanh liên quan nhà theo thỏa thuận rõ. Dự thảo lại ghi chia toàn bộ nhà cho chồng làm tài sản riêng. Hướng xử lý nào phù hợp mục tiêu hai bên?',
 'Làm rõ và chọn thỏa thuận đưa tài sản chung vào kinh doanh; không ghi chia riêng trái mục tiêu giữ chung',
 ['Giữ nội dung chia riêng vì hai giao dịch luôn có cùng hậu quả sở hữu','Ghi chồng thành chủ sở hữu duy nhất nhưng giải thích miệng rằng nhà vẫn chung','Chỉ cần xác định nhà chung trong lời chứng, không cần sửa dự thảo chia riêng'],
 'Điều 36 điều chỉnh thỏa thuận bằng văn bản về đưa tài sản chung vào kinh doanh, trao quyền tự thực hiện giao dịch liên quan tài sản đó. Điều 38 và khoản 1 Điều 40 điều chỉnh việc chia, với hậu quả phần chia là riêng nếu không có thỏa thuận khác. Mục tiêu giữ chung khác nội dung chia riêng. Thỏa thuận giữa vợ chồng không tự thay thế hợp đồng góp vốn với doanh nghiệp hoặc thủ tục chuyển quyền cho doanh nghiệp.',
 'Chọn loại giao dịch từ hậu quả sở hữu mong muốn trước khi soạn văn bản.')
add('1.4;extension','application',['HN:46:3'],
 'Chồng có tài sản riêng và một nghĩa vụ liên quan trực tiếp tài sản đó. Vợ chồng thỏa thuận nhập tài sản vào khối chung; không có thỏa thuận khác về thực hiện nghĩa vụ và không có quy định pháp luật khác. Sau khi nhập, nguồn tài sản thực hiện nghĩa vụ liên quan được xác định thế nào?',
 'Thực hiện bằng tài sản chung theo khoản 3 Điều 46',
 ['Luôn chỉ bằng tài sản riêng còn lại của chồng vì nghĩa vụ có trước việc nhập','Nghĩa vụ tự chấm dứt vì tài sản không còn là riêng','Chỉ thực hiện bằng phần tài sản riêng của vợ vì vợ đồng ý việc nhập'],
 'Khoản 3 Điều 46 quy định nghĩa vụ liên quan tài sản riêng đã nhập vào tài sản chung được thực hiện bằng tài sản chung, trừ thỏa thuận khác hoặc quy định khác. Câu đã loại trừ hai ngoại lệ. Đây là quy tắc về nguồn tài sản thực hiện, không phải tự xóa nghĩa vụ hoặc tự đổi người có nghĩa vụ trong quan hệ với chủ nợ.',
 'Phân biệt nguồn tài sản trả nghĩa vụ với việc thay người có nghĩa vụ.')
add('8.1;extension','application',['HN:47','HN:49:1'],
 'Vợ chồng đã đăng ký kết hôn hai năm và chưa từng lập thỏa thuận chế độ tài sản trước khi kết hôn. Nay họ muốn công chứng lần đầu thỏa thuận theo Điều 47, ghi có hiệu lực hồi tố từ ngày cưới; họ viện dẫn quyền sửa đổi ở Điều 49. Đánh giá nào đúng?',
 'Không thể dùng quyền sửa đổi một thỏa thuận để bỏ điều kiện lập trước khi kết hôn đối với việc xác lập lần đầu',
 ['Điều 49 cho phép xác lập lần đầu sau kết hôn và hồi tố trong mọi trường hợp','Chỉ cần gọi văn bản là sửa đổi thì được coi đã có thỏa thuận trước kết hôn','Có thể hồi tố nếu văn bản hiện tại có chữ ký cả hai và hai người chưa có tranh chấp'],
 'Điều 47 yêu cầu thỏa thuận xác lập chế độ tài sản được lập trước khi kết hôn với hình thức luật định. Điều 49 cho sửa đổi, bổ sung thỏa thuận, không biến một văn bản chưa từng tồn tại thành thỏa thuận trước hôn nhân. Câu phân biệt xác lập lần đầu với sửa đổi chế độ theo thỏa thuận đã được lựa chọn hợp lệ; không phủ nhận các giao dịch chia hay nhập tài sản khi đủ điều kiện riêng.',
 'Kiểm tra có thỏa thuận gốc hợp lệ trước khi áp dụng quyền sửa đổi.')
add('8.2','application',['HN:49:2','ND:17:2','ND:18:1'],
 'Vợ chồng có chế độ theo thỏa thuận hợp lệ và đang kết hôn. Cả hai ký giấy tại nhà sửa nội dung tài sản, chưa công chứng hoặc chứng thực, rồi yêu cầu coi chế độ đã đổi từ ngày ký giấy. Điều gì cần xử lý?',
 'Thỏa thuận sửa đổi phải được công chứng hoặc chứng thực; không lấy ngày ký giấy tại nhà làm mốc hiệu lực sửa đổi',
 ['Đủ chữ ký của cả hai thì mọi thay đổi chế độ đã có hiệu lực từ ngày ký giấy','Chỉ cần công chứng chữ ký một bên vì văn bản gốc đã đủ hai người','Chỉ được sửa đổi sau khi đã ly hôn, không được sửa trong thời kỳ hôn nhân'],
 'Khoản 2 Điều 49 dẫn yêu cầu hình thức ở Điều 47; khoản 2 Điều 17 yêu cầu công chứng hoặc chứng thực thỏa thuận sửa đổi. Khoản 1 Điều 18 xác định hiệu lực sửa đổi từ ngày được công chứng hoặc chứng thực. Đây là thỏa thuận sửa đổi chế độ đã có, khác ngày xác lập chế độ lần đầu tại ngày đăng ký kết hôn.',
 'Phân biệt mốc của việc sửa chế độ đang áp dụng với mốc xác lập ban đầu.')
add('8.2;extension','advanced',['ND:18:2'],
 'Theo chế độ tài sản đang áp dụng, vợ chồng đã phát sinh nghĩa vụ với chủ nợ C. Sau đó hai người sửa chế độ để chồng không còn chịu nghĩa vụ đó. C không tham gia, không chấp thuận thay đổi quan hệ nghĩa vụ. Chỉ xét tác động của việc sửa chế độ đối với nghĩa vụ đã có, kết luận nào đúng?',
 'Nghĩa vụ phát sinh trước việc sửa chế độ có hiệu lực vẫn có giá trị; thỏa thuận riêng không tự giải phóng chồng đối với C',
 ['Mọi nghĩa vụ với C tự chuyển sang vợ ngay khi sửa chế độ được công chứng','C bắt buộc tuân theo mọi phân bổ nợ mới giữa hai vợ chồng','Nghĩa vụ cũ chỉ tồn tại nếu C đã dự họp khi hai vợ chồng sửa chế độ'],
 'Khoản 2 Điều 18 giữ giá trị quyền, nghĩa vụ về tài sản phát sinh trước thời điểm sửa đổi có hiệu lực, trừ trường hợp các bên có thỏa thuận khác. Thỏa thuận nội bộ của vợ chồng không phải sự chấp thuận của chủ nợ đối với việc giải phóng một người có nghĩa vụ. Câu không bàn việc hoàn trả nội bộ giữa vợ chồng mà kiểm tra quan hệ với người thứ ba đã phát sinh.',
 'Tách phân bổ trách nhiệm nội bộ khỏi quyền của chủ nợ đã có trước.')
add('8.1','advanced',['ND:16'],
 'Vợ chồng theo chế độ tài sản thỏa thuận có nội dung liên quan giao dịch dự định với C. Hai người muốn giữ bí mật toàn bộ thỏa thuận và không cung cấp cho C bất kỳ thông tin liên quan nào, cho rằng bí mật gia đình loại trừ nghĩa vụ thông tin. Hướng tư vấn đúng là gì?',
 'Phải cung cấp thông tin liên quan chế độ tài sản cho người thứ ba khi xác lập, thực hiện giao dịch',
 ['Có quyền giấu mọi thông tin liên quan và tự chuyển rủi ro sang C','Chỉ cần công chứng viên biết, C không có quyền nhận thông tin liên quan','Phải công khai toàn bộ thỏa thuận trên mạng thay cho thông tin cho C'],
 'Điều 16 yêu cầu vợ chồng cung cấp cho người thứ ba thông tin liên quan khi giao dịch dưới chế độ theo thỏa thuận; nếu vi phạm, người thứ ba được coi ngay tình và được bảo vệ theo BLDS. Nghĩa vụ này không đồng nghĩa công khai mọi chi tiết gia đình cho toàn xã hội. Cam kết giữ bí mật giữa hai người không loại trừ thông tin cần thiết cho đối tác.',
 'Xác định thông tin nào liên quan giao dịch và đối tượng phải được cung cấp.')
add('8.1','application',['CC:44'],
 'Hai người chưa kết hôn yêu cầu công chứng thỏa thuận xác lập chế độ tài sản, có nội dung về một nhà ở tỉnh A. Văn phòng họ chọn ở tỉnh B; không phải yêu cầu công chứng mua bán hay chia nhà thông thường. Chỉ xét giới hạn địa bàn ở Điều 44, nhận định nào đúng?',
 'Thỏa thuận xác lập chế độ tài sản vợ chồng về bất động sản thuộc ngoại lệ địa bàn theo Điều 44',
 ['Cứ có mô tả nhà cụ thể thì thỏa thuận này bắt buộc công chứng ở tỉnh A','Chỉ được công chứng tại tỉnh nơi một trong hai người thường trú','Ngoại lệ chỉ có khi thỏa thuận không nêu bất động sản nào'],
 'Điều 44 Luật Công chứng 2024 bổ sung rõ thỏa thuận xác lập chế độ tài sản của vợ chồng về bất động sản trong nhóm ngoại lệ giới hạn địa bàn. Câu kiểm tra đúng loại thỏa thuận, không mở rộng ngoại lệ sang mọi việc chia, nhập hay bán bất động sản giữa vợ chồng. Đáp án chỉ kết luận về địa bàn; vẫn phải kiểm tra các điều kiện công chứng khác.',
 'Nhận diện đúng tên và bản chất giao dịch trước khi áp dụng giới hạn tỉnh.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('8.2','advanced',['HN:28:2','HN:30:2','ND:15:2'],
 'Chế độ theo thỏa thuận hợp lệ xác định vợ chồng không có tài sản chung. Khi không đủ tài sản đáp ứng nhu cầu thiết yếu gia đình, chồng có khả năng kinh tế nhưng từ chối góp tài sản riêng chỉ vì đã chọn chế độ này. Kết luận nào đúng?',
 'Vợ chồng vẫn có nghĩa vụ đóng góp tài sản riêng theo khả năng kinh tế để đáp ứng nhu cầu thiết yếu',
 ['Không có tài sản chung thì mọi nghĩa vụ đáp ứng nhu cầu gia đình tự hết','Chỉ vợ phải dùng tài sản riêng vì chồng không giữ khoản tiền chung','Nghĩa vụ đóng góp chỉ tồn tại nếu được lặp lại trong thỏa thuận tài sản'],
 'Khoản 2 Điều 28 áp dụng các Điều 29–32 không phụ thuộc chế độ được lựa chọn. Khoản 2 Điều 30 yêu cầu đóng góp tài sản riêng theo khả năng kinh tế khi không có hoặc không đủ tài sản chung đáp ứng nhu cầu thiết yếu. Khoản 2 Điều 15 cũng yêu cầu thỏa thuận phù hợp các điều này. Chế độ riêng không phải công cụ miễn nghĩa vụ bảo đảm nhu cầu gia đình.',
 'Tìm các quy định bắt buộc áp dụng cho cả hai chế độ tài sản.')
add('8.4;extension','advanced',['DS:48:2','DS:53:1'],
 'Khi còn đầy đủ năng lực, vợ đã lựa chọn chị ruột đủ điều kiện làm người giám hộ bằng văn bản được công chứng. Nay vợ bị tuyên mất năng lực, cần được giám hộ và chị ruột đồng ý. Chồng đủ điều kiện nhưng nói mình luôn là giám hộ đương nhiên, bất kể lựa chọn hợp lệ trước đó. Đánh giá nào đúng?',
 'Phải xét người giám hộ đã được lựa chọn hợp lệ; cơ chế đương nhiên ở Điều 53 áp dụng khi không có người theo khoản 2 Điều 48',
 ['Chồng luôn ưu tiên tuyệt đối vì quan hệ hôn nhân loại bỏ mọi lựa chọn trước đó','Người được lựa chọn chỉ được giám hộ nếu không có vợ hoặc chồng','Văn bản lựa chọn tự hết hiệu lực ngay khi người lựa chọn mất năng lực'],
 'Khoản 2 Điều 48 cho lựa chọn người giám hộ bằng văn bản công chứng hoặc chứng thực, khi cần giám hộ và người đó đồng ý. Phần mở đầu Điều 53 chỉ dùng người giám hộ đương nhiên khi không có người theo khoản 2 Điều 48. Câu đã xác định lựa chọn hợp lệ, đủ điều kiện, có sự đồng ý; không thể chỉ xem giấy kết hôn rồi bỏ qua việc lựa chọn này.',
 'Kiểm tra lựa chọn giám hộ hợp lệ trước khi áp dụng thứ tự đương nhiên.')
add('8.4','advanced',['DS:59:1'],
 'Chồng là giám hộ hợp lệ của vợ mất năng lực, muốn bán tài sản giá trị lớn của vợ vì lợi ích của vợ. Người giám sát giám hộ chưa đồng ý, nhưng người mua mời một người làm chứng và đề nghị thay sự đồng ý đó bằng chữ ký người làm chứng. Xử lý nào đúng?',
 'Chữ ký người làm chứng không thay sự đồng ý của người giám sát giám hộ theo Điều 59',
 ['Người làm chứng luôn được thay người giám sát nếu không nhận thù lao','Chồng là giám hộ nên chỉ cần chứng minh quan hệ hôn nhân để miễn giám sát','Người mua cam kết bồi thường là đủ thay cả giám sát lẫn điều kiện đại diện'],
 'Khoản 1 Điều 59 yêu cầu sự đồng ý của người giám sát đối với giao dịch tài sản giá trị lớn của người được giám hộ. Người làm chứng và người giám sát có chức năng khác nhau; việc có người làm chứng không tự đáp ứng điều kiện kiểm soát giám hộ. Câu giả định chồng đã là giám hộ hợp lệ và mục đích vì lợi ích vợ, vẫn phải kiểm tra yêu cầu độc lập này.',
 'Lập riêng điều kiện đại diện, lợi ích người được giám hộ và sự giám sát.')
add('8.4;extension','application',['DS:59:1'],
 'Chồng là giám hộ của vợ mất năng lực. Chồng muốn nhân danh vợ tặng tài sản riêng của vợ cho cháu và đã xin người giám sát đồng ý. Chỉ xét quyền tặng cho tài sản của người được giám hộ, nhận định nào đúng?',
 'Người giám hộ không được đem tài sản của người được giám hộ tặng cho người khác',
 ['Được tặng nếu người giám sát đồng ý vì sự đồng ý loại bỏ mọi giới hạn','Được tặng cho người thân dù không được tặng cho người ngoài gia đình','Được tặng nếu ghi tài sản riêng của vợ thành tài sản chung ngay trong hợp đồng'],
 'Khoản 1 Điều 59 cấm người giám hộ đem tài sản người được giám hộ tặng cho người khác. Không áp điều kiện đồng ý của người giám sát đối với giao dịch tài sản giá trị lớn để suy rằng nó hợp thức hóa mọi loại giao dịch. Quan hệ thân thích của người nhận không tạo ngoại lệ cho việc tặng. Không được thay bản chất sở hữu bằng một ghi nhận không có căn cứ.',
 'Kiểm tra giao dịch có thuộc điều cấm riêng trước khi xét sự đồng ý giám sát.')
add('8.1;extension','advanced',['HN:50:1:c'],
 'Dự thảo chế độ tài sản trước hôn nhân có nội dung được xác định là vi phạm nghiêm trọng quyền được cấp dưỡng, quyền được thừa kế của con. Hai bên yêu cầu chứng nhận vì cả hai tự nguyện và cho rằng chỉ sai hình thức mới làm thỏa thuận vô hiệu. Nhận định nào đúng?',
 'Nội dung vi phạm nghiêm trọng các quyền này là căn cứ để Tòa án tuyên thỏa thuận vô hiệu theo Điều 50',
 ['Tự nguyện của vợ chồng loại bỏ mọi căn cứ vô hiệu về quyền của con','Chỉ cần công chứng thì Tòa án không được xem xét nội dung nữa','Con không ký nên mọi điều khoản liên quan quyền của con đều không bị kiểm tra'],
 'Điểm c khoản 1 Điều 50 là căn cứ vô hiệu về nội dung, độc lập với điều kiện hiệu lực, hình thức và các nguyên tắc tại Điều 29–32. Câu đã xác định mức vi phạm nghiêm trọng, không coi mọi thỏa thuận phân chia khác nhau là vi phạm. Tự nguyện của hai bên không cho phép tước các quyền được pháp luật bảo vệ của thành viên gia đình; công chứng không loại trừ quyền xem xét của Tòa án.',
 'Kiểm tra quyền của người ngoài hai bên ký, đặc biệt cấp dưỡng và thừa kế.')
add('3.8','advanced',['HN:9:1','HN:14:1','HN:16:1'],
 'A và B bắt đầu chung sống năm 2006, chưa đăng ký kết hôn đến nay. Chỉ có giấy khai sinh con ghi tên cả hai và giấy cư trú, không có căn cứ công nhận hôn nhân đặc biệt khác. Họ muốn áp ngay Điều 38 để chia tài sản chung vợ chồng. Hướng xử lý đúng là gì?',
 'Không mặc nhiên coi là vợ chồng; giải quyết tài sản theo thỏa thuận và quy định tại Điều 16 đối với việc chung sống không đăng ký',
 ['Có con chung thì tự phát sinh hôn nhân từ ngày sinh con và bắt buộc áp Điều 38','Giấy cư trú ghi cùng địa chỉ thay thế đăng ký kết hôn trong mọi trường hợp','Bắt buộc chia đôi như tài sản vợ chồng nếu đã chung sống đủ ba năm'],
 'Khoản 1 Điều 9 yêu cầu đăng ký kết hôn; khoản 1 Điều 14 xác định chung sống đủ điều kiện nhưng không đăng ký không làm phát sinh quyền, nghĩa vụ vợ chồng. Khoản 1 Điều 16 giải quyết tài sản theo thỏa thuận; nếu không thỏa thuận thì theo BLDS và pháp luật liên quan. Giấy khai sinh chứng minh quan hệ cha mẹ con không thay đăng ký kết hôn. Câu xác định thời điểm 2006 và loại trừ căn cứ đặc biệt để tránh áp nhầm hôn nhân thực tế lịch sử.',
 'Xác định quan hệ hôn nhân được công nhận trước khi chọn cơ chế chia tài sản.')

def provision(spec):
 p=spec.split(':'); cfg=CONFIG[p[0]]; b={'document':cfg[0],'article':'Điều '+p[1],'url':cfg[3]}
 if len(p)>2:b['clause']='Khoản '+p[2]
 if len(p)>3:b['point']='Điểm '+p[3]
 t=(WORK/'legal'/cfg[2]).read_text();m=re.search(r'(?m)^[ \t]*Điều[ \t]+'+p[1]+r'[.,]',t);assert m,spec
 n=re.search(r'(?m)^[ \t]*Điều[ \t]+\d+[.,]',t[m.end():]);excerpt=t[m.start():m.end()+n.start() if n else len(t)].strip();assert len(excerpt)>100
 return b,{'reference':b,'sourceId':cfg[1],'evidenceExcerpt':excerpt}
bank=[];proof=[]
for i,r in enumerate(ROWS,1):
 pairs=[provision(s) for s in r['refs']];answers=[r['key']]+r['wrong'];assert len(set(answers))==4
 random.Random(261006+i).shuffle(answers)
 q={'id':f'FAM26-{i:03d}','part':2,'topic':r['topic'],'type':'single','status':'active','difficulty':r['difficulty'],'questionForm':'workflow' if r['difficulty']=='advanced' else 'short_case','question':{'variants':['Tháng 10/2026: '+r['stem']]},'answers':[{'id':chr(65+j),'text':a,'correct':a==r['key']} for j,a in enumerate(answers)],'explanation':'Gợi ý làm bài: '+r['hint']+'\n\n'+r['reason'],'legalBasis':[b for b,e in pairs],'lastVerified':DATE,'source':{'type':'user-provided','id':SOURCE,'questionNumber':r['origin'],'supportingSourceIds':list(dict.fromkeys(e['sourceId'] for b,e in pairs))}}
 bank.append(q);proof.append({'id':q['id'],'provisions':[e for b,e in pairs]})
assert len(bank)==26
def write(path,obj):(ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('data/imported-family-2026.json',bank)
docs=[{'sourceId':cfg[1],'url':cfg[3],'pdfSha256':[{'file':f,'sha256':hashlib.sha256((WORK/'legal'/f).read_bytes()).hexdigest()} for f in cfg[4]],'extraction':'PDF chính thức; ND126 OCR đối chiếu trang in 5–6, BLDS đối chiếu trang in 15, 16 và 18. HNGĐ dùng VBHN năm 2025; Luật Công chứng dùng quy định áp dụng tháng 10/2026.'} for cfg in CONFIG.values()]
write('reports/family-legal-evidence-2026.json',{'date':DATE,'scope':'Xác minh 26 câu biên soạn; không chứng nhận toàn bộ đáp án nguồn','documents':docs,'effectivityNotes':[{'document':'Nghị định 126/2014/NĐ-CP','status':'Hết hiệu lực một phần; các Điều 14–18 sử dụng trong đợt này không thuộc phần bãi bỏ bởi Điều 45 khoản 2 điểm đ NĐ123/2015.','officialStatusUrl':'https://vbpl.vn/TW/Pages/vbpq-thuoctinh.aspx?ItemID=47412','repealUrl':'https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/92897/VanBanGoc_123_2015_N%C4%90-CP.pdf'},{'document':'Luật Công chứng','note':'Không áp dụng các sửa đổi có hiệu lực từ 01/01/2027 vào câu tháng 10/2026.'}],'questions':proof})
sha=hashlib.sha256(DOC.read_bytes()).hexdigest()
groups=[{'number':1,'title':'Chấm dứt hiệu lực việc chia tài sản','questions':6,'images':[]}, {'number':2,'title':'Chia tài sản, hạn chế định đoạt và quyền ly hôn','questions':6,'images':[1,2]}, {'number':3,'title':'Trà Vinh: tài sản, nghĩa vụ vợ chồng, không đăng ký kết hôn','questions':8,'images':list(range(3,14))}, {'number':5,'title':'Tây Ninh: tài sản trước hôn nhân, chia tài sản, quyền của con','questions':8,'images':[22,23,24]}, {'number':7,'title':'Đưa tài sản chung vào kinh doanh','questions':6,'images':[33,34]}, {'number':8,'title':'Đề kiểm tra lần thứ tư và các bài giải','questions':7,'images':list(range(35,45))}]
items=[]
for g in groups:
 for number in range(1,g['questions']+1):
  origin=str(g['number'])+'.'+str(number);linked=[q['id'] for q in bank if origin in q['source']['questionNumber'].split(';')]
  items.append({'id':'FAM-SRC-'+origin,'sourceGroup':g['number'],'questionNumber':number,'decision':'adapted_partial' if linked else 'review','adaptedQuestionIds':linked,'originalAnswerCertified':False,'note':'Các nhánh ngoài câu biên soạn liên kết chưa được chứng nhận. Phần I đạo đức của đề 8 được tách riêng, số 8.1–8.6 là Phần II.'})
# Group 8 contains one unnumbered ethics item plus six numbered professional cases.
items[-1]['id']='FAM-SRC-8.ETHICS';items[-1]['questionNumber']='ETHICS';items[-1]['note']='Phần I đạo đức; chưa cập nhật/xác minh trong bộ tài sản vợ chồng.'
write('reports/family-source-review.json',{'date':DATE,'sourceId':SOURCE,'sourceSha256':sha,'readScope':{'paragraphs':529,'tables':3,'embeddedImages':44,'method':'Đọc phần chữ, bảng, OCR toàn bộ ảnh; xem ảnh nguồn để kiểm tra bố cục và các cụm lặp.'},'sourceQuestionCount':41,'groups':groups,'duplicateSections':[{'section':'Đề 4 và bài giải ảnh 14–21','duplicateOf':'Đề 1','note':'Cùng tình huống Phương/Lân; không thêm câu vì lặp bản chụp.'},{'section':'Ảnh 25–32, không có tiêu đề Đề 6 trong phần chữ','duplicateOf':'Đề 5','note':'Bài giải Tây Ninh; không coi là đề mới.'},{'section':'Ảnh 42–44 và Bài giải 2','duplicateOf':'Đề 8','note':'Cùng đề với các nhận xét khác nhau; không đếm hai đề.'}],'questions':items,'activeAdded':26,'unverifiedBranches':['Các mức phí, thù lao theo quyết định địa phương cũ','Thẩm quyền đối với nhiều bất động sản khác tỉnh và thủ tục chuyển quyền cụ thể chưa viết thành câu','Hạn chế định đoạt vô thời hạn và cam kết chuyển vốn cho con khi ly hôn','Đạo đức, tập sự trong đề 8','Các nhánh đặt cọc, đất nông nghiệp và bảo đảm đã có nguồn chuyên đề; không nhập lại'],'sourceIssues':['Lời giải dùng Luật Công chứng 2014, Luật Đất đai 2013 và giấy tờ cũ.','Đề 4 trùng Đề 1 nhưng bài giải có kết luận khác về nơi chấm dứt.','Một số lời giải phủ nhận nhập lại tài sản đã đăng ký riêng; cần đọc ngoại lệ thỏa thuận khác tại Điều 41.','Không phân biệt bản sao nhóm điểm d với giấy tùy thân, giấy tài sản theo Điều 42 hiện hành.','Không chỉ vì là con mà được cấp bản sao; không chỉ vì là người liên quan mà được bỏ điều kiện đồng ý.','Lời giải chế độ tài sản có nội dung mâu thuẫn về thời điểm, lương, nhà được tặng và thẩm quyền.','Nhầm Nghị định 126/2015 thành văn bản thật 126/2014; phần bí mật phải xét Điều 16.','Thỏa thuận đưa tài sản chung vào kinh doanh khác hợp đồng góp vốn với doanh nghiệp.','Mẫu giải nhầm tên, năm văn bản và tên loại giao dịch.']})
reg=json.loads((ROOT/'data/question-sources.json').read_text())
reg['sources']=[s for s in reg['sources'] if s['id'] not in [SOURCE,'OFFICIAL-ND126-2014']]+[{'id':SOURCE,'type':'user-provided','title':'Đề thi và bài giải hôn nhân và gia đình do Madam An cung cấp','sha256':sha,'use':'Nguồn tình huống có phần chữ, bảng và 44 ảnh; các phần lặp được gộp. Chỉ 26 câu biên soạn được xác minh riêng.'},{'id':'OFFICIAL-ND126-2014','type':'official','title':'Nghị định 126/2014/NĐ-CP','url':CONFIG['ND'][3],'use':'Điều 14–18 về chế độ tài sản. Văn bản hết hiệu lực một phần; không sử dụng phần hộ tịch đã bãi bỏ.'}]
write('data/question-sources.json',reg)
lines=['# Đề luyện tài sản vợ chồng và nghiệp vụ công chứng','','26 câu, một đáp án đúng mỗi câu; thời gian gợi ý 45 phút. Pháp luật áp dụng tháng 10/2026. Đây là đề luyện biên soạn từ chủ đề nguồn, không phải đề thi chính thức.','','## Câu hỏi','']
for i,q in enumerate(bank,1):lines+=['### Câu '+str(i),'',q['question']['variants'][0],'']+[a['id']+'. '+a['text'] for a in q['answers']]+['']
lines+=['## Đáp án và bài giải','','| Câu | Đáp án |','|---|---|']+[f'| {i} | '+next(a['id'] for a in q['answers'] if a['correct'])+' |' for i,q in enumerate(bank,1)]+['']
for i,q in enumerate(bank,1):lines+=['### Giải câu '+str(i),'',q['explanation'],'','Căn cứ: '+'; '.join(b['document']+', '+b['article']+(', '+b['clause'] if 'clause' in b else '')+(', '+b['point'] if 'point' in b else '')+' ([nguồn]('+b['url']+'))' for b in q['legalBasis'])+'.','']
lines+=['## Kết quả nghiên cứu nguồn','','Đọc 529 đoạn, 3 bảng và 44 ảnh. Sáu cụm đề khác nhau chứa 41 câu lớn (kể cả mục đạo đức của đề 8); Đề 4 lặp Đề 1, ảnh 25–32 là bài giải Đề 5, bản chụp thứ hai của đề 8 không được tính thêm. Nhiều câu lớn có nhiều yêu cầu; chỉ những nhánh đã biên soạn, có đáp án duy nhất và căn cứ được kiểm tra mới đưa vào ngân hàng. Không công bố DOCX gốc.','','### Những điểm cần sửa so với bài giải cũ','']+['- '+s for s in json.loads((ROOT/'reports/family-source-review.json').read_text())['sourceIssues']]+['','### Phạm vi và kiểm soát chất lượng','','26 câu mới, 0 câu cũ bị xóa hoặc đổi đáp án trong đợt này. Phân bố: '+str(dict(collections.Counter(q['difficulty'] for q in bank)))+'; chủ đề: '+str(dict(collections.Counter(q['topic'] for q in bank)))+'. Các câu về cùng chế định kiểm tra nhánh khác nhau: thời điểm, hình thức, ngoại lệ, quyền người thứ ba, lợi ích con, nguồn nghĩa vụ; không nhân bản một câu dẫn bằng tên người khác.','','Rà trùng với ngân hàng: không viết lại các câu mặc định giữ riêng sau chấm dứt (VER26-034), điều kiện nhập tài sản (VER26-035), hình thức và ngày xác lập chế độ ban đầu (VER26-036/037), giấy chứng nhận một tên, tài sản được tặng riêng, lương thông thường và điều kiện giám sát thuần nhận biết (IMP-T60-031). Câu mới về giám sát kiểm tra việc thay người giám sát bằng người làm chứng, và các nhánh lựa chọn giám hộ/tặng cho tài sản.','','Trước: 884 câu lưu trữ, 342 active. Sau: 910 câu lưu trữ, 368 active, 36 review, 506 archived. App đọc 410 bản ghi trong 7 file; 42 bản ghi không đủ điều kiện vẫn không vào ôn tập hoặc thi thử. 500 câu mở rộng cơ học tiếp tục archived. Giữ nguyên khóa lưu lịch sử/progress và ID câu cũ.','','Mục tiêu 400 câu và ma trận toàn ngân hàng vẫn cần tiếp tục hoàn thiện; đợt chuyên đề này không có nghĩa đã kiểm định toàn bộ các nhánh trong tài liệu hay đạt cân bằng tổng thể. Những nhánh chưa xác minh được ghi review ở báo cáo nguồn, không tạo bản ghi active để giữ đủ số.','']
(ROOT/'reports/family-exam-2026-10-06.md').write_text('\n'.join(lines))
print(json.dumps({'added':len(bank),'difficulty':dict(collections.Counter(q['difficulty'] for q in bank))},ensure_ascii=False))
