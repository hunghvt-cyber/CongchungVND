"""Build independently authored authorization cases; needs supplied source and official PDFs in scratch."""
from pathlib import Path
import json,re,hashlib,collections,random
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT.parent
DATE='2026-10-05'; SOURCE='USER-EXAM-AUTHORIZATION'
DOC=next((WORK/'upload').glob('*U*QUYE*.docx'))
CONFIG={
 'DS':('Bộ luật Dân sự số 91/2015/QH13','OFFICIAL-BLDS15','BLDS-full.txt','https://vanban.chinhphu.vn/?pageid=27160&docid=183188',['BLDS-0.pdf','BLDS-1.pdf']),
 'CC':('Luật Công chứng số 46/2024/QH15','OFFICIAL-CC24','CC-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat46.pdf',['CC-0.pdf']),
 'HN':('Luật Hôn nhân và gia đình số 52/2014/QH13 (đối chiếu VBHN 121/VBHN-VPQH năm 2025)','OFFICIAL-HNGD-HN25','HNGD-HN-0.txt','https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/8/46059/58694-1-20251299-1300121-vbhn-vpqh.pdf',['HNGD-HN-0.pdf'])}
ROWS=[]
def add(origin,difficulty,refs,stem,key,wrong,reason,hint):
 ROWS.append(dict(origin=origin,difficulty=difficulty,refs=refs,stem=stem,key=key,wrong=wrong,reason=reason,hint=hint))
add('1.1','advanced',['HN:107:1','DS:283'],
 'A đi học xa, vẫn là người phải cấp dưỡng theo bản án. Người có quyền nhận cấp dưỡng đồng ý để B chuyển tiền của A hằng tháng; B không nhận chuyển giao nghĩa vụ cấp dưỡng. B bỏ sót một kỳ. Chỉ xét trách nhiệm cấp dưỡng của A, kết luận nào phù hợp?',
 'A vẫn chịu trách nhiệm; nhờ B thực hiện việc trả tiền không làm chuyển nghĩa vụ cấp dưỡng sang B',
 ['B trở thành người có nghĩa vụ cấp dưỡng nên A được miễn trách nhiệm','Sự đồng ý nhận tiền qua B làm bản án cấp dưỡng tự chấm dứt','Mọi việc chuyển tiền qua người thứ ba đều bị cấm vì cấp dưỡng gắn với nhân thân'],
 'Điều 107 cấm chuyển giao nghĩa vụ cấp dưỡng. Điều 283 cho phép thực hiện nghĩa vụ qua người thứ ba khi bên có quyền đồng ý, nhưng bên có nghĩa vụ vẫn chịu trách nhiệm nếu người thứ ba không thực hiện đúng. Dữ kiện phân biệt rõ hỗ trợ thanh toán với thay thế người có nghĩa vụ; không suy rằng A được giải phóng hoặc mọi hỗ trợ trả tiền đều bị cấm.',
 'Tách người chịu nghĩa vụ khỏi người thực hiện thao tác thanh toán.')
add('1.2','application',['DS:22:2','DS:134:3'],
 'A chọn B, 30 tuổi, để nhận ủy quyền bán xe vì cho rằng chỉ cần đủ 18 tuổi. Hồ sơ có quyết định còn hiệu lực của Tòa án tuyên B mất năng lực hành vi dân sự. Chỉ xét điều kiện của B, xử lý nào đúng?',
 'Không thể dựa riêng vào tuổi để cho B tự nhận và thực hiện giao dịch này; phải xét quyết định mất năng lực',
 ['B được tự ký vì mọi người trên 18 tuổi đều có năng lực đầy đủ','Cho B nhận ủy quyền nếu A cam kết chịu mọi rủi ro thay B','Quyết định của Tòa án chỉ ảnh hưởng tài sản riêng của B, không ảnh hưởng giao dịch đại diện'],
 'Tuổi không thay thế việc kiểm tra năng lực. Khoản 2 Điều 22 yêu cầu giao dịch dân sự của người mất năng lực phải do người đại diện theo pháp luật xác lập, thực hiện; Điều 134 khoản 3 đặt yêu cầu năng lực phù hợp khi pháp luật quy định. Cam kết của A không tự khôi phục năng lực của B hoặc xóa quyết định của Tòa án.',
 'Kiểm tra tuổi cùng tình trạng năng lực, không chỉ đọc năm sinh.')
add('1.6','advanced',['DS:569:2','CC:53:1'],
 'B nhận ủy quyền không có thù lao, nay muốn ngừng làm và đã báo trước A một thời gian hợp lý. A không đồng ý ký thỏa thuận chấm dứt. B yêu cầu CCV lập văn bản ghi cả hai bên đã thỏa thuận. Phân biệt nào đúng?',
 'B có thể thực hiện quyền đơn phương chấm dứt theo luật; CCV không được ghi nhận thỏa thuận của A khi A chưa đồng ý',
 ['A không đồng ý nên B không bao giờ được đơn phương chấm dứt','B được tự ký văn bản mang tên thỏa thuận của cả hai bên mà không cần ý chí của A','Việc B đến văn phòng tự biến quyền đơn phương thành thỏa thuận chấm dứt'],
 'Khoản 2 Điều 569 cho bên được ủy quyền không có thù lao quyền đơn phương chấm dứt với báo trước hợp lý. Khoản 1 Điều 53 yêu cầu thỏa thuận hoặc cam kết bằng văn bản của tất cả người ký đối với công chứng văn bản thỏa thuận chấm dứt, trừ ngoại lệ luật định. Quyền đơn phương không phải bằng chứng A đã cùng thỏa thuận; câu không đồng nhất thủ tục công chứng hai loại văn bản.',
 'Xác định đây là ý chí một bên hay thỏa thuận của tất cả các bên.')
add('3.4;extension','application',['DS:569:2'],
 'B nhận ủy quyền có thù lao để làm thủ tục cho A. B đơn phương ngừng thực hiện; A chứng minh có thiệt hại do việc chấm dứt đó, không có căn cứ miễn trách nhiệm. B nói chỉ bên ủy quyền mới phải bồi thường. Đánh giá nào đúng?',
 'B được đơn phương chấm dứt nhưng phải bồi thường thiệt hại cho A nếu có',
 ['B chỉ phải hoàn thù lao và không bao giờ phải bồi thường','B không có quyền chấm dứt trong bất kỳ trường hợp nào vì đã nhận thù lao','A phải bồi thường cho B vì là người giao công việc'],
 'Điều 569 khoản 2 quy định riêng trách nhiệm của bên được ủy quyền: khi ủy quyền có thù lao, bên này có quyền đơn phương chấm dứt bất cứ lúc nào và phải bồi thường cho bên ủy quyền nếu có thiệt hại. Không đảo nghĩa vụ với khoản 1 dành cho bên ủy quyền, cũng không coi trả thù lao là ràng buộc vĩnh viễn.',
 'Đọc đúng khoản ứng với người đang chấm dứt và kiểm tra có thù lao hay không.')
add('1.6;extension','advanced',['DS:569:1'],
 'A đã đơn phương chấm dứt ủy quyền cho B nhưng không báo bằng văn bản cho C. Sau đó B giao kết với C trong phạm vi ghi trên giấy ủy quyền cũ; C không biết và không phải biết việc chấm dứt, các điều kiện hiệu lực khác đều đủ. A đòi phủ nhận hợp đồng với C chỉ vì đã thông báo riêng cho B. Kết luận nào đúng theo Điều 569?',
 'Hợp đồng với C vẫn có hiệu lực trong tình huống đã nêu; A không thể chỉ dựa vào thông báo riêng cho B để phủ nhận',
 ['Hợp đồng với C luôn mất hiệu lực ngay khi A gửi tin cho B','C phải chịu mọi rủi ro kể cả khi không biết và không phải biết việc chấm dứt','C chỉ được bảo vệ nếu có chữ ký mới của A trong từng hợp đồng'],
 'Đoạn thứ hai khoản 1 Điều 569 yêu cầu bên ủy quyền báo bằng văn bản cho người thứ ba. Nếu không báo thì hợp đồng với người thứ ba vẫn có hiệu lực, trừ khi người đó biết hoặc phải biết việc chấm dứt. Câu đã loại trừ ngoại lệ này và các lỗi hiệu lực khác. Việc chấm dứt trong quan hệ A–B cần được phân biệt với hậu quả đối với C.',
 'Kiểm tra thông báo đến người thứ ba và trạng thái biết hoặc phải biết của họ.')
add('1.6','application',['DS:565:1','DS:565:2'],
 'A thu hẹp quyền của B từ bán xe xuống chỉ cho thuê và yêu cầu cập nhật cho khách hàng. B đã nhận việc sửa đổi nhưng tiếp tục đưa giấy cũ cho người giao dịch, đồng thời không báo tiến độ cho A; không có thỏa thuận miễn nghĩa vụ báo cáo. Nghĩa vụ nào B đã bỏ qua?',
 'Báo A về công việc và báo người thứ ba về phạm vi, thời hạn cùng việc sửa đổi phạm vi ủy quyền',
 ['Chỉ báo tiến độ cho A, không cần cho người thứ ba biết phạm vi sửa đổi','Chỉ báo người thứ ba nếu giao dịch đã phát sinh tranh chấp','Không có nghĩa vụ báo cáo vì B tự thực hiện công việc nhân danh A'],
 'Khoản 1 Điều 565 đặt nghĩa vụ thực hiện đúng công việc và báo cho bên ủy quyền; khoản 2 yêu cầu thông tin cho người thứ ba về thời hạn, phạm vi và sửa đổi phạm vi. Đây là hai đối tượng nhận thông tin khác nhau. Tự thực hiện không đồng nghĩa được giấu thay đổi phạm vi hoặc dùng giấy cũ để làm người khác hiểu sai.',
 'Lập hai dòng kiểm tra: thông tin cho người giao việc và thông tin cho đối tác.')
add('1.6;3.6','advanced',['DS:563','DS:140:1'],
 'Hợp đồng từ đầu quy định rõ: ủy quyền 12 tháng; nếu đến mốc đó A vẫn ở nước ngoài và công việc chưa hoàn tất thì thời hạn tự kéo dài một lần thêm 12 tháng. Hai điều kiện đều xảy ra, không có căn cứ chấm dứt khác hay quy định chuyên ngành trái với điều khoản. Nhận định nào phù hợp?',
 'Phải xác định thời hạn theo toàn bộ điều khoản đã thỏa thuận, gồm phần gia hạn có điều kiện',
 ['Mọi điều khoản gia hạn tự động đều bị cấm vì trên giấy có số 12 tháng','Cứ có công việc chưa xong thì mọi giấy ủy quyền đều tự kéo dài dù không thỏa thuận','Chỉ tình trạng A ở nước ngoài đủ để gia hạn vô hạn'],
 'Điều 563 cho các bên thỏa thuận thời hạn và khoản 1 Điều 140 xác định thời hạn theo văn bản ủy quyền. Với điều khoản rõ, đã có ngay từ đầu và thỏa mãn điều kiện, không được chỉ đọc phần 12 tháng rồi bỏ phần gia hạn. Kết luận này không áp cho văn bản không có điều khoản gia hạn, không cho phép B tự kéo dài, và không loại trừ các căn cứ chấm dứt khác.',
 'Đọc đủ điều kiện, số lần và giới hạn gia hạn trước khi xác định ngày hết hạn.')
add('2.6','advanced',['DS:564:2','DS:564:3'],
 'A đồng ý cho B ủy quyền lại việc nộp hồ sơ đăng ký nhà; hợp đồng ban đầu đã công chứng và không cho quyền bán nhà. B lập giấy viết tay cho C cả quyền nộp hồ sơ lẫn bán nhà, cho rằng A đã đồng ý ủy quyền lại nên mọi điều kiện đều đủ. Đánh giá nào đúng?',
 'Sự đồng ý chưa đủ: phải giữ phạm vi ban đầu và hình thức ủy quyền lại phù hợp với hình thức ban đầu',
 ['Có sự đồng ý thì C đương nhiên được bán nhà dù A chỉ giao nộp hồ sơ','Chỉ cần sửa hình thức; phạm vi có thể mở rộng vì C là người nhận lại','Chỉ cần giữ phạm vi; hình thức ủy quyền lại không chịu yêu cầu nào'],
 'Khoản 2 và khoản 3 Điều 564 là điều kiện độc lập với sự đồng ý ở khoản 1. B không được giao cho C quyền bán vượt quá quyền mình nhận; giấy viết tay không thể được coi là đã đáp ứng hình thức chỉ vì có sự đồng ý chung. Hồ sơ cần xử lý đồng thời phạm vi và hình thức, không chọn sửa một lỗi rồi bỏ lỗi còn lại.',
 'Sau điều kiện được ủy quyền lại, kiểm tra tiếp phạm vi và hình thức.')
add('2.6','application',['DS:564:1:b'],
 'B nhận ủy quyền nộp hồ sơ nhưng bận công việc thường ngày. A chưa đồng ý cho ủy quyền lại; không có sự kiện bất khả kháng. B định giao toàn bộ việc cho chồng mình. Chỉ xét căn cứ được ủy quyền lại, nhận định nào đúng?',
 'B chưa có căn cứ ủy quyền lại; việc bận và quan hệ vợ chồng không tự thay sự đồng ý hoặc bất khả kháng',
 ['Được vì chồng của B đương nhiên kế tiếp mọi quyền của B','Được vì mọi việc bận đều là bất khả kháng','Được nếu giữ nguyên thời hạn, không cần căn cứ theo khoản 1'],
 'Điều 564 khoản 1 cho hai nhóm căn cứ: có sự đồng ý của bên ủy quyền hoặc trường hợp bất khả kháng đáp ứng điều kiện đặc biệt. Câu đã loại trừ cả hai. Tình trạng bận thông thường và quan hệ hôn nhân với người nhận lại không tự tạo quyền; giữ thời hạn hoặc phạm vi đúng cũng không bù việc thiếu căn cứ.',
 'Kiểm tra lý do trước; không dùng quan hệ thân thích để thay quyền của người giao việc.')
add('3.6','application',['DS:564:1:b'],
 'B bị cô lập do một sự kiện đã được xác định là bất khả kháng. Nếu không ủy quyền lại ngay thì mục đích thực hiện giao dịch vì lợi ích của A không thể đạt được. A không thể liên lạc; phạm vi và hình thức ủy quyền lại đều phù hợp. Điều khoản ban đầu không quy định khác. Có bắt buộc chờ A đồng ý mới được ủy quyền lại không?',
 'Không; trường hợp đã đủ điều kiện bất khả kháng theo điểm b khoản 1 Điều 564 là căn cứ được ủy quyền lại',
 ['Có, pháp luật chỉ cho phép ủy quyền lại khi nhận được sự đồng ý trực tiếp','Không, nhưng chỉ vì mọi người nhận ủy quyền luôn được tùy ý chọn người thay','Có, vì bất khả kháng chỉ áp dụng hợp đồng mua bán, không áp dụng ủy quyền'],
 'Điểm b khoản 1 Điều 564 là căn cứ khác với sự đồng ý tại điểm a. Đề đã xác định sự kiện bất khả kháng và hậu quả không thể đạt mục đích vì lợi ích A nếu không ủy quyền lại, đồng thời đáp ứng hình thức, phạm vi. Không biến ngoại lệ này thành quyền giao việc tùy ý trong các tình huống bận thông thường.',
 'Đọc đủ cả bất khả kháng lẫn hậu quả đối với mục đích ủy quyền.')
add('2.1','application',['DS:141:3'],
 'Hợp đồng bán nhà từ H cho vợ chồng A đã hoàn tất. Nay A nhờ H chỉ nộp và nhận hồ sơ đăng ký cho A; không đàm phán lại, không ký giao dịch giữa A với H, không đại diện bên đối lập. CCV nói cứ là người bán cũ thì bị cấm nhận ủy quyền. Chỉ xét xung đột theo khoản 3 Điều 141, đánh giá nào đúng?',
 'Không thể cấm chỉ vì H là người bán cũ; cần xét công việc hiện tại có phải giao dịch với chính H hoặc bên H cũng đại diện hay không',
 ['Mọi người từng bán tài sản đều vĩnh viễn bị cấm đại diện người mua','H phải đứng tên người mua thì mới có thể làm thủ tục đăng ký','Quan hệ mua bán cũ tự làm mọi công việc hành chính sau đó thành giao dịch với chính mình'],
 'Khoản 3 Điều 141 cấm nhân danh người được đại diện giao dịch với chính mình hoặc với bên thứ ba mà mình cũng đại diện, trừ ngoại lệ luật định. Việc từng là người bán không tự chứng minh điều cấm trong một công việc đăng ký thuần túy đã được giới hạn. Câu chỉ kết luận về căn cứ xung đột này, không xác nhận toàn bộ hồ sơ, năng lực và thủ tục khác đã đủ.',
 'Nhận diện bên giao dịch và công việc hiện tại, không suy từ vai trò trong giao dịch đã kết thúc.')
add('2.5','application',['DS:566:2','DS:567:3'],
 'A ủy quyền không có thù lao cho B làm đăng ký. B đã ứng 8 triệu đồng thuế, phí hợp lý đúng công việc, có chứng từ; không có thỏa thuận B chịu thay chi phí. A từ chối hoàn vì hợp đồng ghi không có thù lao. Nhận định nào đúng?',
 'Không có thù lao không loại bỏ quyền được thanh toán chi phí hợp lý B đã bỏ ra',
 ['Không có thù lao nghĩa là B phải tự chịu cả thuế, phí','B chỉ được hoàn nếu có mức thù lao bằng đúng 8 triệu đồng','Mọi khoản ứng của B đều tự chuyển thành thù lao'],
 'Điều 566 khoản 2 và Điều 567 khoản 3 tách thanh toán chi phí hợp lý khỏi hưởng thù lao. Đề đã xác định chi phí đúng công việc, hợp lý và không có thỏa thuận chịu thay, nên A không thể dùng việc miễn thù lao để phủ nhận nghĩa vụ hoàn. Không phải mọi khoản chi ngoài phạm vi đều được hoàn; các điều kiện của câu quyết định kết luận.',
 'Tách thù lao, khoản ứng và người chịu nghĩa vụ cuối cùng.')
add('2.4;extension','application',['DS:565:3','DS:565:5','DS:568:2'],
 'B nhận tiền hoàn phí và giấy chứng nhận sau khi làm thủ tục cho A. Không có thỏa thuận cho B hưởng khoản hoàn phí. B muốn giữ cả tiền và giấy để dùng cho giao dịch riêng, nói rằng mình trực tiếp đi làm nên được sở hữu. Nghĩa vụ nào phù hợp?',
 'Bảo quản giấy tờ và giao lại tài sản, lợi ích đã nhận cho A theo thỏa thuận hoặc luật',
 ['B đương nhiên sở hữu tiền hoàn phí vì trực tiếp nhận từ cơ quan','B được giữ giấy để dùng riêng miễn không bán nhà của A','B chỉ phải giao giấy, mọi lợi ích bằng tiền thuộc người đi làm thủ tục'],
 'Điều 565 khoản 3 yêu cầu bảo quản tài liệu, khoản 5 yêu cầu giao lại tài sản và lợi ích đã nhận theo thỏa thuận hoặc luật; Điều 568 khoản 2 cho A quyền yêu cầu giao lại, trừ thỏa thuận khác. Tư cách nhận thay không tạo quyền sở hữu lợi ích hoặc quyền dùng giấy tờ cho mục đích riêng. Đề đã loại trừ thỏa thuận cho B hưởng khoản hoàn phí.',
 'Phân biệt nhận thay với được hưởng; kiểm tra điều khoản phân chia lợi ích.')
add('1.5;extension','application',['DS:565:4','DS:565:6'],
 'Trong khi làm công việc ủy quyền, B biết thông tin riêng của A và tự đăng công khai để quảng bá dịch vụ, không có sự đồng ý hay căn cứ pháp luật cho phép. A bị thiệt hại được chứng minh. Chỉ xét nghĩa vụ của B theo hợp đồng ủy quyền, kết luận nào đúng?',
 'B vi phạm nghĩa vụ giữ bí mật và phải bồi thường thiệt hại do vi phạm nghĩa vụ đó',
 ['B được dùng mọi thông tin vì đã được giao giấy tờ','Chỉ công chứng viên mới có nghĩa vụ giữ bí mật, người nhận ủy quyền thì không','B được miễn trách nhiệm nếu công việc chính đã làm xong'],
 'Khoản 4 Điều 565 đặt nghĩa vụ giữ bí mật đối với chính bên được ủy quyền, không chỉ với CCV. Khoản 6 quy định bồi thường thiệt hại do vi phạm các nghĩa vụ của điều này. Hoàn thành việc chính hoặc nhận được tài liệu để làm việc không tự cho phép công khai thông tin; đề đã xác định không có căn cứ cho phép và có thiệt hại.',
 'Xét nghĩa vụ của đúng chủ thể và mối liên hệ giữa tiết lộ với thiệt hại.')
add('3.6','understanding',['DS:138:1','DS:140:3:a','DS:140:3:d'],
 'A đã ủy quyền B làm một công việc, nay muốn trực tiếp ủy quyền thêm C nhưng không chấm dứt quyền của B. Thư ký gọi việc A giao quyền cho C là ủy quyền lại của B và cho rằng B tự mất quyền. Cần sửa điều nào?',
 'A trực tiếp giao quyền cho C là một việc ủy quyền mới; phải kiểm tra riêng các căn cứ chấm dứt quyền của B',
 ['A không được giao quyền cho C nếu B chưa đồng ý','A giao quyền cho C luôn là ủy quyền lại của B dù B không tham gia','C nhận quyền thì mọi giao dịch B đã làm tự bị hủy từ đầu'],
 'Điều 138 khoản 1 cho cá nhân, pháp nhân quyền ủy quyền cho chủ thể khác. A đang là người giao quyền trực tiếp, không phải B giao tiếp quyền đã nhận. Điều 140 khoản 3 yêu cầu xét thỏa thuận hoặc việc đơn phương chấm dứt và các căn cứ khác; không có quy tắc rằng sự xuất hiện C tự hủy mọi quyền hoặc giao dịch của B. Khi soạn thảo cần làm rõ phạm vi phối hợp để tránh xung đột.',
 'Xác định ai giao quyền cho ai trước khi dùng thuật ngữ ủy quyền lại.')
add('3.6;extension','advanced',['DS:140:3:đ'],
 'A ủy quyền B bán xe trong 24 tháng. Sau 6 tháng A chết, chưa bán xe. B trình giấy còn ngày hết hạn trong tương lai và yêu cầu tiếp tục ký bán nhân danh A, không có căn cứ đại diện mới. Chỉ xét quyền từ giấy ủy quyền này, kết luận nào đúng?',
 'Quyền đại diện theo ủy quyền đã chấm dứt khi A chết; ngày hết hạn trên giấy không đủ cho B tiếp tục bán nhân danh A',
 ['B được bán đến hết 24 tháng vì thời hạn trên giấy được ưu tiên tuyệt đối','Giấy ủy quyền tự trở thành di chúc để B bán xe','B tự đại diện toàn bộ người thừa kế chỉ vì đã đại diện A'],
 'Điểm đ khoản 3 Điều 140 quy định đại diện theo ủy quyền chấm dứt khi người được đại diện hoặc người đại diện là cá nhân chết. Căn cứ này độc lập với thời hạn còn lại. Hồ sơ cần chuyển sang xác định di sản, chủ thể có quyền và đại diện hợp lệ mới; không biến giấy cũ thành di chúc hoặc quyền đại diện người thừa kế.',
 'Kiểm tra sự kiện chấm dứt quyền ngoài ngày hết hạn ghi trên văn bản.')
add('1.5;extension','advanced',['DS:143:1:a'],
 'A giao B mua thiết bị với giá tối đa 200 triệu đồng. B giao kết giá 220 triệu, vượt phạm vi; sau đó A biết đầy đủ và đồng ý rõ ràng với phần vượt. Các điều kiện hiệu lực khác đều đáp ứng. Chỉ xét việc vượt phạm vi, kết luận nào đúng?',
 'Không thể phủ nhận phần vượt chỉ vì vượt hạn mức ban đầu, vì A đã đồng ý theo ngoại lệ luật định',
 ['Phần vượt luôn vô hiệu dù A đồng ý sau đó','A chỉ có thể đồng ý nếu B chưa giao kết với đối tác','Sự đồng ý của A tự biến mọi người khác thành người đại diện'],
 'Điểm a khoản 1 Điều 143 là ngoại lệ khi người được đại diện đồng ý. Quy tắc không phát sinh quyền, nghĩa vụ đối với phần vượt không được áp máy móc sau khi A đã biết và chấp thuận rõ. Câu giả định các điều kiện hiệu lực khác đầy đủ nên không dùng sự chấp thuận để hợp thức hóa giao dịch có điều cấm hoặc sai hình thức.',
 'Sau khi phát hiện vượt phạm vi, kiểm tra đủ các ngoại lệ trước khi kết luận hậu quả.')
add('1.5;extension','advanced',['DS:143:4'],
 'B và C đều biết B chỉ được mua tối đa 200 triệu cho A nhưng cố ý lập giao dịch vượt quyền để gây thiệt hại cho A. Thiệt hại do sự thông đồng đã được xác định; A không đồng ý và không có căn cứ ràng buộc A đối với phần vượt. Trách nhiệm bồi thường nào phù hợp?',
 'B và C phải liên đới bồi thường thiệt hại cho A',
 ['Chỉ B phải bồi thường; C biết và thông đồng cũng luôn được miễn','Chỉ C phải bồi thường vì B mang danh người đại diện','A tự chịu thiệt hại trong mọi trường hợp vì đã từng giao quyền cho B'],
 'Khoản 4 Điều 143 quy định trách nhiệm liên đới khi người đại diện và người giao dịch cố ý xác lập, thực hiện giao dịch vượt phạm vi, gây thiệt hại cho người được đại diện. Câu đã xác định cả lỗi cố ý, sự thông đồng và thiệt hại, nên không chia trách nhiệm thành chỉ một người chịu hoặc mặc nhiên đẩy sang A.',
 'Kiểm tra sự cố ý của cả hai bên và thiệt hại đối với người được đại diện.')
add('5.2','application',['HN:24:2','DS:139:1'],
 'Nhà là tài sản chung của A và vợ B. A ủy quyền hợp lệ cho B cùng bán toàn bộ nhà cho C trong phạm vi xác định; các điều kiện chuyển nhượng khác đều đủ. Khi soạn hợp đồng mua bán, cách ghi tư cách bên bán nào phù hợp?',
 'Ghi A và B là các chủ thể bên bán; B tham gia cho mình và đại diện A theo văn bản ủy quyền',
 ['Chỉ ghi B là chủ sở hữu duy nhất vì B trực tiếp ký','Chỉ ghi A là bên bán, bỏ quyền của B đối với tài sản chung','Ghi B là bên nhận chuyển nhượng vì đang đại diện A'],
 'Khoản 2 Điều 24 cho vợ chồng ủy quyền cho nhau trong giao dịch cần đồng ý cả hai. Khoản 1 Điều 139 xác định giao dịch trong phạm vi đại diện làm phát sinh quyền, nghĩa vụ của người được đại diện. B ký hai tư cách không xóa vai trò chủ sở hữu của A hoặc phần quyền của chính B; cần soạn đúng hợp đồng bán nhà đang được yêu cầu, không nhầm sang một hợp đồng ủy quyền mới.',
 'Tách chủ thể giao dịch khỏi người trực tiếp ký và thể hiện đầy đủ tư cách đại diện.')
add('5.5','application',['CC:50:3'],
 'B tham gia giao dịch cho chính mình nhưng gãy tay phải, không ký được. B có thể điểm chỉ bằng ngón trỏ trái; các điều kiện công chứng khác đã được đáp ứng. Chồng B không có quyền đại diện nhưng đề nghị ký tên B thay. Chỉ xét cách ký hoặc điểm chỉ, phương án đúng là gì?',
 'Để B tự điểm chỉ thay ký theo thứ tự ngón tay luật định; không cho chồng ký tên B thay khi không có quyền đại diện',
 ['Cho chồng ký tên B vì quan hệ hôn nhân tự tạo quyền ký thay','Không thể công chứng trong mọi trường hợp nếu ngón trỏ phải không dùng được','Cho chồng tự điểm chỉ và ghi đó là dấu điểm chỉ của B'],
 'Khoản 3 Điều 50 cho điểm chỉ thay ký khi không ký được: dùng ngón trỏ phải, nếu không dùng được thì ngón trỏ trái, tiếp đó mới đến ngón khác với lời chứng ghi rõ. B vẫn là người tham gia và tự thể hiện ý chí; quan hệ vợ chồng không cho phép giả chữ ký hoặc dấu điểm chỉ. Câu đã giả định đáp ứng các điều kiện khác, không kết luận mọi hồ sơ chỉ cần điểm chỉ là đủ.',
 'Phân biệt không ký được với không thể tự thể hiện ý chí; kiểm tra đúng người thực hiện dấu điểm chỉ.')

def provision(spec):
 p=spec.split(':');cfg=CONFIG[p[0]];number=p[1]
 b={'document':cfg[0],'article':'Điều '+number,'url':cfg[3]}
 if len(p)>2:b['clause']='Khoản '+p[2]
 if len(p)>3:b['point']='Điểm '+p[3]
 t=(WORK/'legal'/cfg[2]).read_text()
 m=re.search(r'(?m)^[ \t]*Điều[ \t]+'+number+r'[.,]',t);assert m,spec
 nxt=re.search(r'(?m)^[ \t]*Điều[ \t]+\d+[.,]',t[m.end():])
 excerpt=t[m.start():m.end()+nxt.start() if nxt else len(t)].strip();assert len(excerpt)>100
 return b,{'reference':b,'sourceId':cfg[1],'evidenceExcerpt':excerpt}
bank=[];proof=[]
for i,r in enumerate(ROWS,1):
 pairs=[provision(s) for s in r['refs']];answers=[r['key']]+r['wrong'];random.Random(260500+i).shuffle(answers)
 q={'id':f'AUTH26-{i:03d}','part':2,'topic':'Dân sự – giao dịch – đại diện – nghĩa vụ','type':'single','status':'active','difficulty':r['difficulty'],'questionForm':'workflow' if r['difficulty']=='advanced' else 'short_case','question':{'variants':['Tháng 10/2026: '+r['stem']]},'answers':[{'id':chr(65+j),'text':a,'correct':a==r['key']} for j,a in enumerate(answers)],'explanation':'Gợi ý làm bài: '+r['hint']+'\n\n'+r['reason'],'legalBasis':[b for b,e in pairs],'lastVerified':DATE,'source':{'type':'user-provided','id':SOURCE,'questionNumber':r['origin'],'supportingSourceIds':list(dict.fromkeys(e['sourceId'] for b,e in pairs))}}
 if i==1:q['topic']='Hôn nhân và gia đình – tài sản vợ chồng'
 if i in [3,20]:q['topic']='Quy trình, thủ tục và nghiệp vụ công chứng'
 bank.append(q);proof.append({'id':q['id'],'provisions':[e for b,e in pairs]})
assert len(bank)==20
def write(p,obj):(ROOT/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('data/imported-authorization-2026.json',bank)
sha=hashlib.sha256(DOC.read_bytes()).hexdigest()
docs=[{'sourceId':cfg[1],'url':cfg[3],'pdfSha256':[{'file':f,'sha256':hashlib.sha256((WORK/'legal'/f).read_bytes()).hexdigest()} for f in cfg[4]],'extraction':'Điều khoản trích từ PDF chính thức; BLDS OCR được đối chiếu bản scan, đặc biệt các trang in 139–141 (Điều 562–569).'} for cfg in CONFIG.values()]
write('reports/authorization-legal-evidence-2026.json',{'date':DATE,'scope':'Chỉ xác minh 20 câu đã biên soạn; không xác nhận toàn bộ bài giải nguồn','documents':docs,'questions':proof})
titles={1:['Cấp dưỡng, thăm nom','Điều kiện người nhận','Thẩm quyền xe','Hồ sơ xe','Soạn ủy quyền xe','Chấm dứt, báo cáo, gia hạn'],2:['Người bán cũ làm thủ tục','Thẩm quyền nhà đất','Hồ sơ đăng ký','Soạn ủy quyền đăng ký','Chi phí, khiếu nại, sử dụng nhà','Ủy quyền lại cho chồng'],3:['Đại diện tố tụng','Thẩm quyền công chứng','Hồ sơ khởi kiện','Soạn ủy quyền tố tụng','Phạm vi khởi kiện và tố tụng','Ủy quyền lại, thêm người, gia hạn'],5:['Hồ sơ bán nhà chung','Soạn bán nhà qua đại diện','Nhà 5 tầng chưa cập nhật','Thanh toán, phạt, chuộc lại','Gãy tay và ký thay','Hủy giao dịch giả tạo']}
items=[]
for exam,t in titles.items():
 for number,title in enumerate(t,1):
  ref=f'{exam}.{number}';linked=[q['id'] for q in bank if ref in q['source']['questionNumber'].split(';')]
  items.append({'id':'AUTH-SRC-'+ref,'topic':title,'decision':'adapted_partial' if linked else 'review','adaptedQuestionIds':linked,'originalAnswerCertified':False,'note':'Chỉ câu biên soạn đã liên kết được xác minh; các nhánh còn lại chưa được chuyển active.'})
for i,title in enumerate(['Đạo đức và lợi ích người thân','Thế chấp doanh nghiệp và đại diện','Hộ gia đình và trẻ em','Đổi ngân hàng, ủy quyền và cọc','Thừa kế và tài khoản Hàn Quốc','Xử lý thế chấp có cọc','Soạn tổng hợp']):
 items.append({'id':f'AUTH-SRC-4.{i}','topic':title,'decision':'duplicate_source_review','adaptedQuestionIds':[],'duplicateOf':f'DEP-SRC-APP-{i}','originalAnswerCertified':False,'note':'Phụ lục đã có trong nguồn đặt cọc; không nhân đôi câu hỏi.'})
assert len(items)==31
write('reports/authorization-source-review.json',{'date':DATE,'sourceId':SOURCE,'sourceSha256':sha,'sourceQuestionCount':31,'sourceLayout':'Đề 1,2 mỗi đề 6 câu bằng chữ; đề 3 có 2 ảnh và bài giải; đề 4 có 3 ảnh phụ lục 7 mục; đề 5 có 6 câu và bài giải. Tổng 24 câu chính, 7 mục phụ lục lặp nguồn đặt cọc.','questions':items,'activeAdded':20})
reg=json.loads((ROOT/'data/question-sources.json').read_text());reg['sources']=[s for s in reg['sources'] if s['id']!=SOURCE]+[{'id':SOURCE,'type':'user-provided','title':'Đề thi và bài giải ủy quyền do Madam An cung cấp','sha256':sha,'use':'Nguồn tình huống 24 câu chính và phụ lục 7 mục lặp nguồn đặt cọc; biên soạn 20 câu độc lập và xác minh căn cứ, không mặc nhiên chấp nhận lời giải.'}];write('data/question-sources.json',reg)
lines=['# Đề luyện đại diện và ủy quyền','', '20 câu trắc nghiệm, một đáp án đúng mỗi câu; thời gian gợi ý 35 phút. Pháp luật áp dụng tháng 10/2026. Đây là đề luyện biên soạn, không phải đề thi chính thức.','', '## Câu hỏi','']
for i,q in enumerate(bank,1):lines+=['### Câu '+str(i),'',q['question']['variants'][0],'']+[a['id']+'. '+a['text'] for a in q['answers']]+['']
lines+=['## Đáp án và hướng dẫn','', '| Câu | Đáp án |','|---|---|']+[f'| {i} | '+next(a['id'] for a in q['answers'] if a['correct'])+' |' for i,q in enumerate(bank,1)]+['']
for i,q in enumerate(bank,1):lines+=['### Giải câu '+str(i),'',q['explanation'],'','Căn cứ: '+'; '.join(b['document']+', '+b['article']+(', '+b['clause'] if 'clause' in b else '')+(', '+b['point'] if 'point' in b else '')+' ([nguồn]('+b['url']+'))' for b in q['legalBasis'])+'.','']
lines+=['## Rà soát nguồn','', 'Đã đọc toàn bộ phần chữ, 3 bảng chữ ký và 5 ảnh. Tài liệu có 24 câu lớn trong 4 cụm đề và 7 mục phụ lục trùng với nguồn đặt cọc. Không chuyển một câu lớn thành nhiều câu paraphrase; 20 câu mới kiểm tra các nhánh pháp lý khác nhau. Các câu đã có trong ngân hàng về tuổi 15–18, thời hạn mặc định, tự giao dịch với mình, ủy quyền vợ chồng và sự đồng ý ủy quyền lại không được nhân bản.','', '- Cập nhật Luật Công chứng 2014 sang Luật 46/2024, áp dụng từ 01/07/2025. Không đưa quy định áp dụng từ 2027 vào câu tháng 10/2026.', '- Không đồng nhất việc hỗ trợ trả tiền cấp dưỡng với chuyển nghĩa vụ cấp dưỡng. Câu chỉ kiểm tra việc trả tiền khi người có quyền đồng ý, không cho phép ủy quyền toàn bộ quyền thăm nom.', '- Không coi người đủ 18 tuổi luôn đủ điều kiện; phải kiểm tra tình trạng năng lực theo quyết định Tòa án và loại công việc.', '- Không đồng nhất quyền đơn phương chấm dứt với quyền tự lập văn bản ghi cả hai đã thỏa thuận. Không khẳng định tuyệt đối không thể chấm dứt khi đã làm một phần công việc.', '- Lời giải gia hạn có nhận xét mâu thuẫn. Câu mới giới hạn vào điều khoản rõ đã được thỏa thuận từ đầu; không mặc nhiên gia hạn mọi giấy ủy quyền.', '- Không đồng nhất thù lao với thuế, phí đã ứng. Việc người nhận ủy quyền nộp thay không tự thay đổi người chịu nghĩa vụ cuối cùng.', '- Đề bán nhà qua vợ được ủy quyền yêu cầu soạn hợp đồng bán, nhưng mẫu giải lại là hợp đồng ủy quyền. Câu mới kiểm tra đúng tư cách trong hợp đồng bán.', '- Mẫu giải còn sử dụng CMND, sổ hộ khẩu và điều luật đất đai cũ; không nhập nguyên danh mục này làm đáp án hiện hành.', '- Phần tố tụng, khiếu nại, nhà xây tăng tầng, chuộc lại và phụ lục thế chấp/thừa kế chưa được xác minh đầy đủ trong đợt này; giữ review, không giả định đã kiểm định vì có bài giải.', '', '## Chất lượng và tích hợp','', '20 câu mới: '+str(dict(collections.Counter(q['difficulty'] for q in bank)))+'. Có giải thích áp dụng tình huống, phương án nhiễu và căn cứ cụ thể; mỗi câu một khóa. Đã giữ nguồn gốc câu lớn và hồ sơ điều khoản. Không công bố DOCX gốc. Ngân hàng active trước đợt: 322; sau bổ sung: 342. Tổng lưu trữ 884 câu, gồm 342 active, 36 review, 506 archived. App tải 384 bản ghi trong 6 file, chọn 342 câu đủ điều kiện và loại 42 câu chưa đủ điều kiện. 500 câu mở rộng cơ học tiếp tục archived.','']
(ROOT/'reports/authorization-exam-2026-10-05.md').write_text('\n'.join(lines))
print(json.dumps({'added':len(bank),'sourceItems':len(items),'difficulty':dict(collections.Counter(q['difficulty'] for q in bank))},ensure_ascii=False))
