"""Editorial decisions for the 36 pending stored questions; never auto-certify sources."""
from pathlib import Path
import json,re,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]; DATE='2026-10-06'
CONFIG={
 'CC':('Luật Công chứng số 46/2024/QH15','OFFICIAL-CC24','CC-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat46.pdf','CC-0.pdf'),
 'TT':('Thông tư số 06/2025/TT-BTP','OFFICIAL-TT06-2025','TT06-0.txt','https://vbpl.moj.gov.vn/TW/Pages/vbpq-toanvan.aspx?ItemID=178542','TT06-0.pdf'),
 'NEW':('Luật số 04/2026/QH16 sửa đổi, bổ sung một số điều của Luật Công chứng','OFFICIAL-CC26','CC26-0.txt','https://chinhphu.vn/?classid=1&docid=218099&orggroupid=1&pageid=27160','CC26-0.pdf')}
ROWS={}
def add(id,ref,stem,key,wrong,reason,level='understanding',form='short_case'):
 ROWS[id]=dict(ref=ref,stem=stem,key=key,wrong=wrong,reason=reason,level=level,form=form)
add('CC-010','CC:9:1:c','CCV Lan được đề nghị công chứng việc mẹ nuôi của chồng Lan bán tài sản riêng. Các bên tự nguyện, không có tranh chấp và đề nghị Lan làm vì đã quen hồ sơ. Chỉ xét xung đột lợi ích của Lan, hướng xử lý đúng là gì?',
 'Lan không thực hiện việc công chứng này vì người bán thuộc danh sách người thân thích luật định',
 ['Lan được thực hiện vì tài sản riêng của người bán không thuộc sở hữu Lan','Lan được thực hiện nếu các bên ký văn bản chấp nhận quan hệ thân thích','Lan được thực hiện nếu mẹ nuôi của chồng không cùng hộ gia đình với Lan'],
 'Điểm c khoản 1 Điều 9 bao gồm cha nuôi, mẹ nuôi của vợ hoặc chồng. Lệnh cấm không chỉ giới hạn tài sản thuộc sở hữu CCV, người cùng hộ hay trường hợp tranh chấp. Sự tự nguyện và văn bản chấp thuận của khách hàng không tạo ngoại lệ. Cần phân công CCV khác đủ điều kiện và kiểm tra các điều kiện công chứng còn lại.')
add('CC-011','CC:9:1:h;CC:18:2:c','CCV đang hành nghề ở X muốn tiếp tục tại X vào các ngày chẵn và ký thêm hồ sơ ở Y vào các ngày lẻ. X và Y là hai tổ chức khác nhau, đều đồng ý phân ca và không trùng giờ. Nhận định nào đúng?',
 'Việc chia ngày không loại bỏ lệnh cấm đồng thời hành nghề tại hai tổ chức',
 ['Không trùng giờ thì không phải đồng thời hành nghề ở hai tổ chức','Chỉ bị cấm khi X và Y nằm ở hai tỉnh khác nhau','Văn bản đồng ý của cả X và Y đủ thay điều kiện hành nghề tại một tổ chức'],
 'Điều 9 cấm đồng thời hành nghề tại từ hai tổ chức; Điều 18 yêu cầu hành nghề tại một tổ chức. Đồng thời ở đây không chỉ là ký hai hồ sơ đúng cùng một giờ. Phân ca hoặc cùng địa bàn không hợp pháp hóa việc duy trì tư cách hành nghề ở cả hai nơi; chuyển nơi hành nghề phải thực hiện thủ tục tương ứng.')
add('CC-012','CC:9:1:k','CCV Nam nghỉ phép, giao thẻ CCV của mình cho một CCV khác để người đó sử dụng khi thực hiện nhiệm vụ. Người nhận có thẻ riêng còn hiệu lực. Đánh giá nào đúng về việc cho sử dụng thẻ của Nam?',
 'Bị cấm dù người nhận cũng là CCV; phải sử dụng tư cách và thẻ của chính người thực hiện',
 ['Được phép nếu người nhận có quyết định bổ nhiệm riêng','Được phép nếu thẻ được trả lại ngay sau kỳ nghỉ','Được phép khi Nam không có mặt, vì hai người không sử dụng thẻ cùng lúc'],
 'Điểm k khoản 1 Điều 9 cấm cho người khác sử dụng quyết định bổ nhiệm hoặc thẻ của mình. Thẻ của người nhận không biến thẻ Nam thành tài liệu có thể cho mượn. Phân công một CCV đủ điều kiện thực hiện hồ sơ bằng tư cách riêng là việc khác với cho dùng thẻ của người nghỉ phép.')
add('CC-013','CC:9:3:đ','Một cử nhân luật được khách hàng ủy quyền nộp hồ sơ, nhưng chưa được bổ nhiệm CCV. Người này quảng bá rằng giấy ủy quyền còn cho mình quyền ký chứng nhận công chứng thay CCV. Phân biệt nào đúng?',
 'Đại diện khách hàng không trao tư cách CCV hay quyền cung cấp dịch vụ công chứng',
 ['Được ký chứng nhận nếu giấy ủy quyền ghi rõ quyền công chứng','Được ký chứng nhận nếu dự thảo do một CCV kiểm tra trước','Được ký chứng nhận cho giao dịch không bắt buộc công chứng vì chỉ là yêu cầu tự nguyện'],
 'Điểm đ khoản 3 Điều 9 cấm cá nhân không phải CCV cung cấp dịch vụ công chứng. Đại diện người yêu cầu, hỗ trợ soạn thảo hoặc nộp hồ sơ không phải tư cách chứng nhận công chứng. Việc công chứng tự nguyện vẫn là hoạt động công chứng và không làm mất điều kiện chủ thể này.')
add('CC-024','CC:14:2','Người đề nghị bổ nhiệm CCV đang bị truy cứu trách nhiệm hình sự, chưa có bản án kết tội. Người này viện nguyên tắc suy đoán vô tội để yêu cầu bỏ qua Điều 14. Chỉ xét trở ngại này, nhận định nào đúng?',
 'Đang bị truy cứu đã thuộc trường hợp không được bổ nhiệm; áp dụng điều kiện nghề nghiệp không phải kết luận người đó có tội',
 ['Chỉ có bản án có hiệu lực mới phát sinh trở ngại bổ nhiệm tại Điều 14 khoản 2','Chỉ hình phạt tù mới ngăn bổ nhiệm, còn việc truy cứu không ảnh hưởng','Được bổ nhiệm ngay nhưng phải cam kết xin miễn nhiệm nếu sau này bị kết án'],
 'Khoản 2 Điều 14 liệt kê riêng người đang bị truy cứu, không đợi bản án hay hình phạt tù. Phải phân biệt điều kiện bổ nhiệm với việc xác định trách nhiệm hình sự. Câu không kết luận người đang bị truy cứu đã phạm tội và cũng không tự suy ra họ bị cấm vĩnh viễn sau khi tình trạng này chấm dứt.')
add('CC-025','CC:14:4','Người đề nghị bổ nhiệm CCV có quyết định còn hiệu lực của Tòa án tuyên bị hạn chế năng lực hành vi dân sự. Người đại diện đồng ý cho người đó hành nghề và cam kết hỗ trợ. Chỉ xét khoản 4 Điều 14, kết luận nào đúng?',
 'Vẫn thuộc trường hợp không được bổ nhiệm; sự đồng ý của đại diện không loại bỏ trở ngại',
 ['Chỉ mất năng lực mới bị cấm; hạn chế năng lực luôn được bổ nhiệm','Được bổ nhiệm nếu đại diện ký cùng vào từng lời chứng','Được bổ nhiệm vì việc hạn chế chỉ ảnh hưởng giao dịch cá nhân, không ảnh hưởng chức danh'],
 'Khoản 4 Điều 14 bao gồm mất năng lực, hạn chế năng lực và khó khăn trong nhận thức, làm chủ hành vi. Quyết định Tòa án còn hiệu lực là dữ kiện đã xác định trong câu; không phải chỉ có chẩn đoán bệnh. Sự hỗ trợ hoặc đồng ý của đại diện không thay điều kiện cá nhân để được bổ nhiệm.')
add('CC-043','NEW:1:11:a;NEW:2','Từ 01/01/2027, người yêu cầu nộp bản sao điện tử giấy tờ thuộc điểm b, c, d khoản 1 Điều 42, chưa thuộc trường hợp miễn cung cấp do khai thác dữ liệu. CCV bác ngay hồ sơ chỉ vì nhóm giấy tờ này không phải bản sao giấy. Đánh giá nào đúng?',
 'Không thể bác chỉ vì dạng điện tử được luật cho phép; vẫn phải kiểm tra tính hợp lệ và bước đối chiếu áp dụng',
 ['Chỉ bản chính điện tử mới được nộp, mọi bản sao điện tử đều bị loại','Bản sao điện tử được nộp nên không còn bất kỳ bước kiểm tra, đối chiếu nào','Chỉ giấy tờ tùy thân được điện tử hóa; giấy tờ tài sản luôn phải là bản sao giấy'],
 'Điểm a khoản 11 Điều 1 sửa khoản 1 Điều 42 cho phép bản sao giấy, bản sao điện tử hoặc bản chính điện tử đối với cả ba nhóm. Cho phép dạng hồ sơ không có nghĩa mọi tệp đều hợp lệ hoặc tự được miễn đối chiếu. Phải tiếp tục xét khoản 7, 7a theo trường hợp cụ thể. Điều 2 ấn định hiệu lực từ 01/01/2027; không áp dụng quy tắc mới cho tháng 10/2026.')
add('CC-046','NEW:1:11:b;NEW:2','Từ 01/01/2027, hồ sơ là văn bản từ chối nhận di sản theo Điều 60, đã chứng minh tư cách thừa kế và việc người để lại di sản chết. Người yêu cầu không xuất trình bản chính giấy tờ tài sản ở điểm c khoản 1 Điều 42. Chỉ xét bước đối chiếu bản chính nhóm này, nhận định nào đúng?',
 'Thuộc ngoại lệ không phải xuất trình bản chính giấy hoặc điện tử của nhóm điểm c để đối chiếu',
 ['Ngoại lệ chỉ áp dụng di sản là tiền, không áp dụng di sản là đất','Không phải nộp bất cứ giấy tờ nào, kể cả chứng minh tư cách thừa kế','Ngoại lệ này áp dụng tương tự cho mọi văn bản phân chia di sản'],
 'Điểm b khoản 11 Điều 1 sửa khoản 7 Điều 42 ghi riêng ngoại lệ cho công chứng văn bản từ chối nhận di sản. Phạm vi ngoại lệ là đối chiếu bản chính giấy tờ tại điểm c; không miễn mọi thành phần hồ sơ, không giới hạn riêng tiền và không mở rộng sang phân chia di sản. Đây là quy định từ 01/01/2027 theo Điều 2.',form='exception')
add('CC-054','NEW:1:13;NEW:2','Từ 01/01/2027, A muốn lập văn bản ủy quyền thực hiện quyền về nhà ở tỉnh B tại tổ chức ở tỉnh C; sau đó người được ủy quyền định ký hợp đồng bán nhà cũng tại C. Chỉ xét ngoại lệ địa bàn được Điều 44 mới quy định, phân biệt nào đúng?',
 'Văn bản ủy quyền thuộc ngoại lệ; hợp đồng bán nhà không tự được hưởng ngoại lệ của văn bản ủy quyền',
 ['Cả hai văn bản thuộc ngoại lệ vì hợp đồng bán được ký qua người đại diện','Cả hai văn bản đều bị cấm ngoài tỉnh B, kể cả ủy quyền','Ngoại lệ tùy nơi cư trú của người đại diện, không tùy loại giao dịch'],
 'Khoản 13 Điều 1 sửa Điều 44, ghi văn bản ủy quyền liên quan thực hiện quyền về bất động sản trong danh sách ngoại lệ. Việc người đại diện ký không đổi hợp đồng bán nhà thành văn bản ủy quyền. Không lấy khoản 2 về lộ trình toàn quốc để mặc định mọi giao dịch đã được làm toàn quốc; câu chỉ xét ngoại lệ khoản 1, chưa giả định lộ trình đã triển khai.',form='integrated')
add('CC-063','NEW:1:16;NEW:2','Từ 01/01/2027, thiết kế cơ sở dữ liệu công chứng chỉ lưu thông tin CCV, tổ chức và giao dịch đã công chứng; loại toàn bộ dữ liệu tình trạng giao dịch tài sản, ngăn chặn, cảnh báo rủi ro và hồ sơ vì cho rằng đó đều nằm ngoài Điều 66 mới. Đánh giá nào đúng?',
 'Thiếu các nhóm dữ liệu được khoản 1 Điều 66 mới liệt kê, bao gồm tình trạng tài sản, ngăn chặn/cảnh báo và văn bản, tài liệu hồ sơ',
 ['Đủ vì Điều 66 mới chỉ cho lưu thông tin giao dịch đã hoàn thành','Chỉ thiếu dữ liệu ngăn chặn, còn tình trạng tài sản và hồ sơ luôn nằm ngoài Điều 66','Chỉ thiếu tình trạng tài sản; cảnh báo và tài liệu hồ sơ không thuộc cơ sở dữ liệu'],
 'Khoản 16 Điều 1 sửa khoản 1 Điều 66 thành bốn nhóm: thông tin CCV/tổ chức/giao dịch; tình trạng giao dịch tài sản; ngăn chặn/cảnh báo; văn bản công chứng và tài liệu hồ sơ. Vì vậy không thể loại cả ba nhóm sau. Quy định nhóm dữ liệu không cho phép công khai tùy ý; khoản 2 vẫn yêu cầu bảo mật, bảo vệ đời sống riêng tư. Mốc áp dụng quy định mới là 01/01/2027.',form='synthesis')
add('CC-073','CC:47:1','Dự thảo văn bản công chứng sử dụng ký hiệu viết tắt tự đặt cho nghĩa vụ bàn giao, chưa có quy định pháp luật cho phép ngoại lệ. Các bên đều hiểu ký hiệu và ký xác nhận đồng ý. Hướng xử lý nào phù hợp về cách viết?',
 'Yêu cầu thể hiện rõ, dễ đọc và không dùng cách viết tắt/ký hiệu trái quy tắc chung',
 ['Có thể giữ ký hiệu vì sự đồng ý của các bên tự tạo ngoại lệ','Chỉ cần CCV hiểu ký hiệu, người tham gia không phải đọc lại nội dung đầy đủ','Được giữ mọi ký hiệu miễn ghi chú đó là thỏa thuận tự nguyện'],
 'Khoản 1 Điều 47 cấm viết tắt hoặc bằng ký hiệu theo quy tắc chung và chỉ chừa ngoại lệ do pháp luật quy định. Câu đã loại trừ ngoại lệ; hiểu nội dung và cùng đồng ý không đủ thay quy tắc hình thức. Cần sửa dự thảo trước khi chứng nhận, tránh dùng ý chí của các bên để miễn yêu cầu pháp luật.')
add('CC-096','NEW:3:1;NEW:2','Từ 01/01/2027, một CCV đã được bổ nhiệm trước ngày này nói quy định chuyển tiếp cho mình tiếp tục hành nghề nên mọi nghĩa vụ hành nghề mới và căn cứ tạm đình chỉ đều không áp dụng. Chỉ xét ý nghĩa khoản 1 Điều 3, đánh giá nào đúng?',
 'Được tiếp tục theo quy định chuyển tiếp nhưng vẫn phải tuân thủ pháp luật; điều khoản không tạo miễn trừ chung',
 ['Tiếp tục hành nghề có nghĩa được miễn mọi nghĩa vụ luật mới','Phải xin bổ nhiệm lại chỉ vì luật sửa đổi bắt đầu có hiệu lực','Chỉ được tiếp tục nếu trong sáu tháng đã công chứng đủ số lượng hồ sơ tối thiểu luật định'],
 'Khoản 1 Điều 3 cho người đã được bổ nhiệm, bổ nhiệm lại trước ngày hiệu lực tiếp tục hành nghề và thực hiện nhiệm vụ chứng thực theo pháp luật được dẫn chiếu. Đây không phải miễn trừ nghĩa vụ hoặc đình chỉ; cũng không đặt điều kiện số hồ sơ giả định trong đáp án nhiễu. Không yêu cầu bổ nhiệm lại chỉ do mốc đổi luật.',form='exception')
add('SRC26-001','TT:15:2','Đọc riêng khoản 2 Điều 15 Thông tư 06/2025/TT-BTP trong bản đã ban hành, không thay bằng phương án trong dự thảo sửa đổi, tổ hợp hình thức và thời gian nào được quy định?',
 'Bài kiểm tra viết 180 phút và bài kiểm tra trắc nghiệm trên máy vi tính 60 phút',
 ['Hai bài kiểm tra trắc nghiệm trên máy vi tính, mỗi bài 60 phút','Bài kiểm tra viết 60 phút và bài trắc nghiệm trên máy vi tính 180 phút','Bài kiểm tra viết 180 phút và bài vấn đáp 60 phút'],
 'Khoản 2 Điều 15 trong bản Thông tư đã ban hành quy định một bài viết 180 phút và một bài trắc nghiệm máy vi tính 60 phút. Nguồn Bộ Tư pháp tháng 6–7/2026 về hai bài trắc nghiệm là đề xuất/hồ sơ dự thảo, không tự sửa điều khoản đã ban hành. Câu giới hạn rõ bản văn được hỏi; không dùng câu này để suy ra lịch, hình thức riêng của mọi kỳ kiểm tra sau này.',level='recognition',form='direct')
add('SRC26-002','TT:29:3:c','Theo khoản 3 Điều 29 Thông tư 06/2025/TT-BTP, giả sử số câu hỏi của một đề trắc nghiệm theo quy định là 60. Nhóm xây dựng đã có 150 câu đúng thiết kế phần mềm. Chỉ xét ngưỡng số câu được xây dựng, cần bổ sung tối thiểu bao nhiêu?',
 '30 câu để đạt ít nhất 180 câu',
 ['Không cần bổ sung vì 150 lớn hơn 60','10 câu vì số lượng chỉ cần nhiều hơn đề 100 câu','60 câu vì chỉ được tính đủ khi có bốn lần số câu đề'],
 'Điểm c khoản 3 Điều 29 yêu cầu số câu xây dựng tối thiểu gấp ba số câu theo quy định: 60 × 3 = 180; 150 còn thiếu 30. Đúng định dạng phần mềm là điều kiện khác, không thay ngưỡng số lượng. Dữ kiện 60 là giả định trong bài toán, không tuyên bố mọi đề thi chính thức đều có 60 câu.',level='application')
add('SRC26-003','TT:29:3:b','Một câu single trong đề kiểm tra có bốn phương án, nhưng đối chiếu luật cho thấy hai phương án đều đúng trong toàn bộ giả thiết của câu dẫn. Nhóm soạn đề muốn giữ câu bằng cách chỉ đánh dấu một phương án trên phần mềm. Chỉ xét tiêu chuẩn khoản 3 Điều 29 TT06/2025, đánh giá nào đúng?',
 'Cần sửa hoặc loại câu; việc đặt một khóa trên phần mềm không khắc phục nội dung thiếu chính xác, chặt chẽ',
 ['Có thể giữ nếu phần mềm không cho thí sinh chọn hai phương án','Có thể giữ nếu khóa được Ban Đề thi lựa chọn ngẫu nhiên trong hai đáp án đúng','Chỉ cần ghi một đáp án trong hướng dẫn chấm, không cần chỉnh câu dẫn'],
 'Điểm b khoản 3 Điều 29 đòi nội dung chính xác, chặt chẽ, rõ ràng và có tính suy luận, phân tích. Giới hạn thao tác chọn một đáp án không biến câu có hai đáp án hợp pháp thành câu có đáp án duy nhất. Cần bổ sung giả thiết hoặc thay phương án sao cho kiểm tra được một kết luận xác định, rồi phản biện lại khóa đáp án.')
add('SRC26-004','TT:16:1:a;TT:16:2:a','A đã được công nhận hoàn thành tập sự nhưng quyết định công nhận sau đó bị hủy bỏ. A dùng bản sao quyết định cũ để đăng ký kiểm tra và nói chỉ cần đã từng hoàn thành tập sự. Chỉ xét tình trạng này, hướng xử lý đúng là gì?',
 'Không thuộc diện được đăng ký vì kết quả đã được công nhận nhưng bị hủy bỏ',
 ['Được đăng ký vì việc hủy sau này không ảnh hưởng quyền từ quyết định cũ','Được đăng ký nếu chưa thi lần nào, dù quyết định đã bị hủy','Được đăng ký khi tổ chức từng nhận tập sự xác nhận đã đủ số tháng'],
 'Điểm a khoản 1 Điều 16 ghi nhóm đã được công nhận hoàn thành, nhưng điểm a khoản 2 loại người có kết quả công nhận bị hủy. Phải đọc cả điều kiện được đăng ký và trường hợp không được đăng ký. Bản sao quyết định cũ hay số tháng tập sự không khôi phục hiệu lực kết quả đã bị hủy.')
add('SRC26-005','TT:16:1:b;TT:16:2:c','A đã dự và không đạt ba kỳ kiểm tra kết quả tập sự, các kỳ này không liên tiếp. A chưa tập sự lại, cho rằng chỉ trượt ba kỳ liên tiếp mới bị hạn chế đăng ký. Nhận định nào đúng theo Điều 16 TT06/2025?',
 'Chưa được đăng ký lại trong tình trạng đã trượt ba kỳ mà chưa tập sự lại; điều khoản không thêm điều kiện liên tiếp',
 ['Được đăng ký vì các kỳ không liên tiếp nên không tính đủ ba kỳ','Chỉ trượt hai kỳ mới phải tập sự lại, sau ba kỳ thì được miễn điều kiện','Được đăng ký nếu đổi tỉnh nộp hồ sơ dù chưa tập sự lại'],
 'Điểm b khoản 1 và điểm c khoản 2 Điều 16 dùng số ba kỳ không đạt và tình trạng chưa tập sự lại, không quy định ba kỳ phải liên tiếp. Không tự thêm điều kiện để né giới hạn; thay địa phương đăng ký không thay lịch sử dự thi. Câu không nói người này bị cấm đăng ký vĩnh viễn sau khi đã tập sự lại đúng quy định.',form='exception')
add('SRC26-006','TT:5:1:h;TT:5:2','Người hướng dẫn tập sự chỉ giao người tập sự chép mẫu hợp đồng và lưu giấy, không hướng dẫn tra cứu luật mới hay khai thác cơ sở dữ liệu dù tổ chức có điều kiện thực hiện. Người hướng dẫn nói đây chỉ là kỹ năng tự học, không thuộc nội dung phải hướng dẫn. Đánh giá nào đúng theo Điều 5 TT06/2025?',
 'Tra cứu, áp dụng văn bản và cập nhật, khai thác cơ sở dữ liệu là nội dung tập sự người hướng dẫn có trách nhiệm hướng dẫn',
 ['Các kỹ năng này hoàn toàn nằm ngoài nội dung Điều 5','Chỉ kỹ năng kế toán của tổ chức là bắt buộc thay cho tra cứu luật','Chỉ cần hướng dẫn nội dung mẫu hợp đồng, không cần các nhóm kỹ năng khác của khoản 1'],
 'Điểm h khoản 1 Điều 5 ghi tra cứu, áp dụng văn bản, cập nhật/khai thác cơ sở dữ liệu và ứng dụng CNTT. Khoản 2 giao người hướng dẫn trách nhiệm hướng dẫn các nội dung khoản 1. Chép mẫu có thể hỗ trợ một kỹ năng nhưng không thay tất cả nhóm còn lại, đặc biệt cập nhật quy định và kiểm tra dữ liệu.',form='workflow')
add('SRC26-007','CC:44','Tháng 10/2026, một hợp đồng chuyển nhượng duy nhất có đối tượng là hai thửa đất ở hai tỉnh khác nhau, thuộc hai chủ sở hữu đã đủ điều kiện bán. Người yêu cầu chọn văn phòng ở tỉnh của một thửa và đề nghị công chứng toàn bộ vì ít nhất một tài sản cùng địa bàn. Chỉ xét Điều 44, nhận định nào đúng?',
 'Không được dựa vào một thửa cùng địa bàn để công chứng cả phần chuyển nhượng bất động sản ở tỉnh khác',
 ['Được công chứng toàn bộ nếu hai chủ sở hữu cùng ký tại trụ sở văn phòng','Được công chứng toàn bộ nếu thửa cùng tỉnh có giá trị lớn hơn','Được công chứng toàn bộ nếu ghi việc đăng ký từng thửa sẽ do các cơ quan địa phương thực hiện'],
 'Điều 44 hiện hành giới hạn giao dịch về bất động sản theo tỉnh nơi tổ chức đặt trụ sở, trừ danh sách ngoại lệ. Hợp đồng chuyển nhượng trong câu không phải ngoại lệ. Sự có mặt, giá trị tài sản hay nơi đăng ký không mở rộng phạm vi địa bàn. Phải lựa chọn cấu trúc giao dịch và tổ chức có thẩm quyền phù hợp; không chứng nhận cả hợp đồng theo đề nghị này.',level='application',form='workflow')
add('SRC26-008','CC:45:1;CC:45:2','Hồ sơ thông thường đã được tiếp nhận hợp lệ. Tổ chức muốn áp dụng mặc định thời hạn mười ngày làm việc cho mọi hồ sơ, kể cả không phức tạp, không có thời gian xác minh, niêm yết hoặc lý do cho thỏa thuận kéo dài. Đánh giá nào đúng?',
 'Không được mặc định mười ngày cho mọi hồ sơ; quy tắc thông thường không quá hai ngày làm việc',
 ['Mười ngày là thời hạn chung, hai ngày chỉ là mức khuyến khích','Mọi hồ sơ đều được kéo dài mười ngày nếu người yêu cầu không phản đối','Hai ngày là ngày theo lịch, còn mười ngày mới được tính theo ngày làm việc'],
 'Khoản 2 Điều 45 đặt trần thông thường hai ngày làm việc; hồ sơ phức tạp có thể kéo dài nhưng không quá mười ngày làm việc. Khoản 1 loại thời gian xác minh, giám định, niêm yết khỏi cách tính. Câu đã loại các tình huống đó và lý do thỏa thuận bằng văn bản, nên không lấy trần dành cho hồ sơ phức tạp làm thời hạn chung.')
add('SRC26-010','CC:48:1:c','Khách hàng đề nghị lời chứng chỉ xác nhận chữ ký đúng, bỏ nội dung về tự nguyện, năng lực và tính hợp pháp vì cho rằng CCV không tham gia đàm phán. Theo Điều 48 khoản 1, hướng xử lý nào đúng?',
 'Lời chứng giao dịch vẫn phải thể hiện các nội dung về tự nguyện, năng lực, mục đích và nội dung không trái pháp luật, đạo đức xã hội',
 ['Chỉ xác nhận chữ ký là đủ cho mọi giao dịch công chứng','Chỉ cần nội dung về năng lực nếu người tham gia đã trên 18 tuổi','Được bỏ các nội dung này khi khách hàng đã tự soạn dự thảo'],
 'Điểm c khoản 1 Điều 48 đặt các nội dung chứng nhận nêu trên trong lời chứng giao dịch. Việc không tham gia đàm phán hoặc khách tự soạn không biến công chứng giao dịch thành chứng thực chữ ký đơn thuần. CCV phải kiểm tra theo quy trình để có cơ sở chứng nhận, không ghi công thức hình thức mà bỏ việc đánh giá thực chất.')
add('SRC26-011','CC:49:1','Một tổ chức cử nhân viên đưa hồ sơ công chứng, nhưng người này không phải đại diện theo pháp luật và chưa có ủy quyền. Nhân viên muốn nhân danh tổ chức xác lập giao dịch vì được giao nhiệm vụ mang giấy tờ. Chỉ xét tư cách người yêu cầu cho tổ chức, kết luận nào đúng?',
 'Mang hồ sơ không tự tạo quyền đại diện; phải xác định đại diện theo pháp luật hoặc đại diện theo ủy quyền hợp lệ',
 ['Bất kỳ nhân viên nào mang đủ giấy tờ đều được nhân danh tổ chức xác lập giao dịch','Chỉ cần người này biết rõ nội dung giao dịch là có quyền đại diện','Chỉ người đại diện theo pháp luật mới được yêu cầu; luật không cho tổ chức dùng đại diện theo ủy quyền'],
 'Khoản 1 Điều 49 cho tổ chức thực hiện yêu cầu thông qua đại diện theo pháp luật hoặc theo ủy quyền. Phải phân biệt việc chuyển/nộp giấy tờ với quyền nhân danh tổ chức tham gia giao dịch. Không suy từ quan hệ lao động ra quyền đại diện, và cũng không loại đại diện theo ủy quyền mà luật thừa nhận.')
add('SRC26-012','CC:49:2','Người yêu cầu không đọc được, cần người làm chứng. Họ chỉ mời bên mua đang tham gia chính giao dịch đó làm chứng vì người này có đủ năng lực. Chỉ xét điều kiện làm chứng, hướng xử lý đúng là gì?',
 'Không chọn bên mua làm chứng vì có quyền, lợi ích hoặc nghĩa vụ liên quan; phải có người làm chứng đáp ứng đầy đủ điều kiện',
 ['Đủ năng lực là đủ, lợi ích trong giao dịch không ảnh hưởng tư cách làm chứng','Bên mua được làm chứng nếu bên bán đồng ý bằng văn bản','CCV có thể miễn người làm chứng vì bên mua đã đọc dự thảo giúp'],
 'Khoản 2 Điều 49 vừa xác định trường hợp bắt buộc có người làm chứng vừa yêu cầu người đó không có quyền, lợi ích hoặc nghĩa vụ liên quan. Bên mua là chủ thể có lợi ích trực tiếp, nên đủ năng lực vẫn chưa đủ. Khi người yêu cầu không mời được thì CCV chỉ định; nếu không chỉ định được thì từ chối công chứng.',form='workflow')
add('SRC26-014','CC:57:1','Tháng 10/2026, bên ủy quyền đã được chứng nhận đề nghị ủy quyền ở X; bên được ủy quyền được Y chứng nhận tiếp vào bản gốc để hoàn thành công chứng. Y nói chỉ gửi bản chụp cho X là đủ thủ tục lưu hồ sơ. Theo khoản 1 Điều 57 đang áp dụng, nhận định nào đúng?',
 'Phải gửi một bản gốc văn bản công chứng đó cho tổ chức bên ủy quyền đã công chứng để lưu hồ sơ',
 ['Chỉ cần bản chụp không xác nhận vì X đã giữ hồ sơ đề nghị ban đầu','Không phải gửi tài liệu nào sau khi Y công chứng tiếp','Bắt buộc gửi toàn bộ mọi bản gốc cho X và không giao bản nào cho người yêu cầu'],
 'Khoản 1 Điều 57 hiện hành ghi việc chứng nhận tiếp vào bản gốc và gửi một bản gốc văn bản công chứng hoàn tất cho tổ chức nơi bên ủy quyền công chứng để lưu. Không thay nghĩa vụ gửi bằng bản chụp theo ý chí của Y. Câu hỏi rõ tháng 10/2026; không lấy quy định sửa từ 01/01/2027 để giải thủ tục đang áp dụng.',form='workflow')
add('SRC26-018','CC:42:7','Dự thảo giao dịch giấy ba trang đã được người yêu cầu đồng ý đầy đủ. Không áp dụng điểm chỉ hay ngoại lệ chữ ký mẫu. Người yêu cầu muốn chỉ ký trang cuối, cho rằng các trang đầu đã được đóng dấu giáp lai nên khỏi ký. Chỉ xét cách ký của người yêu cầu tại khoản 7 Điều 42, xử lý nào đúng?',
 'Vẫn phải ký từng trang và ký, ghi đủ họ tên vào trang cuối; giáp lai không thay chữ ký từng trang',
 ['Chỉ trang cuối cần ký vì dấu giáp lai thay chữ ký tất cả trang đầu','Chỉ cần ký trang đầu để thể hiện đã đọc toàn bộ dự thảo','Có thể chọn ký từng trang hoặc đóng dấu giáp lai thay thế tùy thỏa thuận'],
 'Khoản 7 Điều 42 quy định người yêu cầu ký từng trang và ký, ghi đủ họ tên tại trang cuối (đóng dấu tổ chức nếu có). Dấu giáp lai phục vụ tính toàn vẹn văn bản không tự là phương thức thay chữ ký cá nhân. Câu đã loại điểm chỉ và ngoại lệ nên cần hoàn thiện đúng cách ký trước khi CCV ký lời chứng.',form='workflow')
add('SRC26-020','TT:20:4;TT:29:4:a;TT:29:4:c','Theo TT06/2025, Ban Thư ký và Ban Đề thi đều giúp việc Hội đồng kiểm tra. Đơn vị nào quyết định số lượng, cơ cấu câu hỏi và chỉ đạo đặt chuyên gia xây dựng Bộ câu hỏi trắc nghiệm theo khoản 4 Điều 20?',
 'Hội đồng kiểm tra',
 ['Ban Thư ký tự quyết định cơ cấu mà không theo chỉ đạo Hội đồng','Ban Đề thi là cơ quan duy nhất có thẩm quyền quyết định số lượng, cơ cấu Bộ câu hỏi','Sở Tư pháp nơi có nhiều thí sinh nhất quyết định thay Hội đồng'],
 'Khoản 4 Điều 20 giao nhiệm vụ cho Hội đồng. Điểm a khoản 4 Điều 29 quy định Hội đồng chỉ đạo Ban Thư ký đặt hàng; điểm c quy định Ban Đề thi nhận Bộ câu hỏi và rà soát để xây dựng đề. Phân biệt vai trò quyết định/chỉ đạo, đặt hàng giúp việc và rà soát đề; không gộp tất cả thành thẩm quyền riêng của Ban Thư ký hay Ban Đề thi.',form='direct')
ARCHIVE={
 'CC-009':('VER26-020','Cùng năng lực xác định ngoại lệ bảo mật; câu hiện có tình huống và nhiễu tốt hơn.'),
 'CC-049':('CC-047;CC-050','Cùng cơ chế dữ liệu và điều kiện yêu cầu bổ sung từ 2027; không giữ thêm câu có/không.'),
 'CC-064':('CC-063','Gộp nhóm ngăn chặn/cảnh báo vào câu kiểm tra đầy đủ các nhóm dữ liệu, tránh tách thành câu có/không.'),
 'CC-077':('VER26-012','Đã có tình huống loại trừ trách nhiệm trong lời chứng, không bổ sung paraphrase.'),
 'CC-078':('VER26-100','Đã có tình huống phân biệt ủy quyền tài sản với tự lập di chúc.'),
 'SRC26-009':('VER26-007;CC-072','Nội trú/ngoài trụ sở đã có câu rõ; chỉ thay tên người bệnh không tạo năng lực mới.'),
 'SRC26-013':('VER26-016','Cùng quy tắc tổ chức công chứng thế chấp lần tiếp; câu tình huống hiện có tốt hơn.'),
 'SRC26-015':('VER26-020','Căn cứ đúng là Điều 18 khoản 2 điểm e và Điều 9 khoản 1 điểm a; trùng kiểm tra bảo mật với câu đã active.'),
 'SRC26-017':('FAM26-002','Danh mục giấy tờ và bước đối chiếu đã được hỏi qua tình huống bản sao/bản chính rõ hơn.'),
 'SRC26-019':('VER26-007;CC-072','Nguyên tắc trụ sở/ngoại lệ đã có; không tạo thêm câu nhận biết lặp.')}
def evidence(code):
 p=code.split(':');d=CONFIG[p[0]];txt=(ROOT.parent/'legal'/d[2]).read_text();a=p[1]
 m=re.search(r'(?m)^\s*Điều\s+'+a+r'\.',txt);assert m,code
 n=re.search(r'(?m)^\s*Điều\s+\d+\.',txt[m.end():]);excerpt=' '.join(txt[m.start():m.end()+n.start() if n else len(txt)].split())
 if p[0]=='NEW' and a=='1' and len(p)>2:
  section=re.search(r'(?m)^\s*'+p[2]+r'\.\s',txt)
  end=re.search(r'(?m)^\s*'+str(int(p[2])+1)+r'\.\s',txt[section.end():])
  excerpt=' '.join(txt[section.start():section.end()+end.start() if end else len(txt)].split())
 b={'document':d[0],'article':'Điều '+a,'url':d[3]}
 if len(p)>2:b['clause']='Khoản '+p[2]
 if len(p)>3:b['point']='Điểm '+p[3]
 return {'reference':b,'evidenceExcerpt':excerpt,'sourceId':d[1]}
def main():
 proof=[];decisions=[];before={};seen=set()
 for filename in ['questions.json','derived-questions.json']:
  path=ROOT/'data'/filename;qs=json.loads(path.read_text())
  for q in qs:
   if q['status']!='review' and q.get('audit',{}).get('reason') not in ('independently_rewritten_and_verified','duplicate_competence_after_review'):continue
   id=q['id'];seen.add(id);before[id]=q
   if id in ARCHIVE:
    link,note=ARCHIVE[id];q['status']='archived';q['audit']={'reason':'duplicate_competence_after_review','reviewedAt':DATE,'replacedBy':link.split(';'),'note':note}
    decisions.append({'id':id,'file':filename,'before':'review','after':'archived','reason':note,'replacedBy':link.split(';')});continue
   row=ROWS[id];prov=[evidence(c) for c in row['ref'].split(';')];prefix='' if row['stem'].startswith(('Tháng 10/2026','Từ 01/01/2027')) else 'Tháng 10/2026: '
   q['question']={'variants':[prefix+row['stem']]};options=row['wrong'].copy();options.insert(len(proof)%4,row['key'])
   q['answers']=[{'id':'ABCD'[i],'text':a,'correct':a==row['key']} for i,a in enumerate(options)]
   q['explanation']='Gợi ý làm bài: Xác định đúng mốc thời gian, tư cách chủ thể và phạm vi điều khoản được hỏi.\n\n'+row['reason']
   q['legalBasis']=[p['reference'] for p in prov];q['status']='active';q['lastVerified']=DATE;q['difficulty']=row['level'];q['questionForm']=row['form']
   q['source']={'type':'official','id':CONFIG[row['ref'].split(':')[0]][1],'supportingSourceIds':list(dict.fromkeys(p['sourceId'] for p in prov)),'note':'Đáp án và nhiễu viết lại sau rà soát; chứng cứ điều khoản tại reports/pending-review-legal-evidence-2026.json.'}
   if id.startswith('SRC26-') and row['ref'].startswith('TT'):q['topic']='Tập sự và kiểm tra kết quả tập sự'
   if id in ['CC-010','CC-011','CC-012','CC-013']:q['topic']='Đạo đức nghề nghiệp và trách nhiệm'
   q['audit']={'reason':'independently_rewritten_and_verified','reviewedAt':DATE}
   proof.append({'id':id,'provisions':prov,'answer':q['answers'][len(proof)%4]['id']});decisions.append({'id':id,'file':filename,'before':'review','after':'active','rewritten':True,'referenceCodes':row['ref'].split(';')})
  path.write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n')
 assert seen==set(ROWS)|set(ARCHIVE),(len(seen),len(ROWS),len(ARCHIVE))
 sources=[]
 for code,d in CONFIG.items():
  sources.append({'sourceId':d[1],'url':d[3],'sha256':hashlib.sha256((ROOT.parent/'legal'/d[4]).read_bytes()).hexdigest(),'scope': 'Quy định tương lai từ 01/01/2027.' if code=='NEW' else 'Các điều khoản được trích, không chứng nhận mọi điều của văn bản.', 'effectivenessNote':'Luật 106/2025 thay thuật ngữ thừa phát lại từ 01/07/2026; câu biên soạn không dùng thuật ngữ cũ. Dự thảo sửa TT06 chưa được dùng làm căn cứ.'})
 (ROOT/'reports/pending-review-legal-evidence-2026.json').write_text(json.dumps({'date':DATE,'sources':sources,'questions':proof},ensure_ascii=False,indent=2)+'\n')
 (ROOT/'reports/pending-review-decisions-2026.json').write_text(json.dumps({'date':DATE,'scope':'Toàn bộ 36 câu review đang lưu trong ngân hàng trước đợt này; không bao gồm việc chứng nhận trọn bộ câu lớn DOCX.','before':36,'promotedAfterRewrite':len(ROWS),'archivedAsDuplicateCompetence':len(ARCHIVE),'newIds':0,'remainingStoredReview':0,'decisions':decisions},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'rewritten':len(ROWS),'archived':len(ARCHIVE)},ensure_ascii=False))
if __name__=='__main__':main()
