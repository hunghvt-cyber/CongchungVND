"""Rebuild the manually authored deposit cases and their legal evidence."""
from pathlib import Path
import json, re, hashlib, sys, collections
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent
DATE='2026-10-05'
SOURCE='USER-EXAM-DEPOSIT'
DOC=next(p for p in (WORK/'upload').glob('*.docx') if 'ĐA' in p.name)
DOC_HASH=hashlib.sha256(DOC.read_bytes()).hexdigest()
CONFIG={
 'DS':('Luật Dân sự', 'Bộ luật Dân sự số 91/2015/QH13','OFFICIAL-BLDS15','BLDS-full.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf',['BLDS-0.pdf','BLDS-1.pdf']),
 'ND':('Nghị định','Nghị định số 21/2021/NĐ-CP','OFFICIAL-ND21-2021','ND21-0.txt','https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-21-2021-nd-cp-33477.htm',['ND21-0.pdf']),
 'CC':('Luật Công chứng','Luật Công chứng số 46/2024/QH15','OFFICIAL-CC24','CC-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat46.pdf',['CC-0.pdf']),
 'HN':('Luật HNGĐ','Luật Hôn nhân và gia đình số 52/2014/QH13 (đối chiếu VBHN 121/VBHN-VPQH năm 2025)','OFFICIAL-HNGD-HN25','HNGD-HN-0.txt','https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/8/46059/58694-1-20251299-1300121-vbhn-vpqh.pdf',['HNGD-HN-0.pdf']),
 'KD':('Luật KDBĐS','Luật Kinh doanh bất động sản số 29/2023/QH15 (đối chiếu VBHN 06/VBHN-VPQH năm 2025)','OFFICIAL-KD-HN25','KD-0.txt','https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-06-vbhn-vpqh-44399.htm',['KD-0.pdf']),
}
ROWS=[]
def add(origin,difficulty,refs,stem,key,wrong,reason,hint):
 ROWS.append(dict(origin=origin,difficulty=difficulty,refs=refs,stem=stem,key=key,wrong=wrong,reason=reason,hint=hint))
add('1.1;2.1','understanding',['DS:328:1','DS:329:1'],
 'Hai giao dịch được đề nghị: A thuê xe và giao tiền cho chủ xe chỉ để bảo đảm trả lại xe; B thuê nhà và giao tiền để bảo đảm giao kết hợp đồng thuê. Cách phân loại phù hợp với mục đích đã nêu là gì?',
 'A là ký cược; B có thể là đặt cọc',
 ['Cả A và B đều là ký cược vì đều thuê tài sản','Cả A và B đều là ký quỹ vì đều dùng tiền','A là đặt cọc; B bắt buộc là ký cược'],
 'Ký cược gắn với việc thuê động sản và bảo đảm trả lại tài sản thuê. Đặt cọc có thể bảo đảm giao kết hoặc thực hiện hợp đồng, kể cả hợp đồng thuê nhà. Không phải mọi khoản tiền trong quan hệ thuê đều là ký cược; ký quỹ còn có cơ chế gửi tiền tại tổ chức tín dụng.',
 'Xác định động sản hay nhà ở và nghĩa vụ mà khoản tiền bảo đảm.')
add('1.1','application',['DS:329:2'],
 'A thuê xe, giao 120 triệu đồng ký cược để bảo đảm trả xe. Khi hết hạn thuê, chiếc xe đã bị tiêu hủy và không còn để trả lại; không có thỏa thuận khác về xử lý ký cược. Chỉ xét khoản ký cược, kết luận nào đúng?',
 'Khoản ký cược thuộc về bên cho thuê',
 ['Khoản ký cược phải trả lại vì hợp đồng thuê đã hết hạn','Bên cho thuê phải trả cho A tổng cộng 240 triệu đồng','Khoản ký cược chỉ được dùng trả tiền thuê, không liên quan việc mất xe'],
 'Điều 329 khoản 2 xử lý riêng trường hợp tài sản thuê không còn để trả lại: tài sản ký cược thuộc về bên cho thuê. Quy tắc trả cọc và khoản tương đương khi bên nhận cọc từ chối không phải quy tắc ký cược. Câu hỏi chỉ xét khoản ký cược, không kết luận khoản này đã giải quyết hết mọi nghĩa vụ khác.',
 'Phân biệt không chịu trả xe với xe không còn để trả.')
add('1.1','application',['DS:329:2'],
 'Xe thuê vẫn còn nhưng A không trả khi hết hạn. A đã ký cược 120 triệu đồng. Chủ xe nói nhận luôn khoản tiền này thì không còn quyền đòi xe nữa. Không có thỏa thuận chuyển quyền sở hữu xe, nhận định nào đúng theo quy tắc ký cược?',
 'Chủ xe vẫn có quyền đòi lại xe; việc không trả không tự biến ký cược thành giá mua xe',
 ['Chủ xe chỉ được lấy tiền ký cược và bắt buộc bỏ quyền đòi xe','A trở thành chủ sở hữu xe ngay khi hết hạn thuê','Chủ xe phải hoàn lại ký cược trước mới được đòi xe'],
 'Điều 329 khoản 2 cho bên cho thuê quyền đòi lại tài sản khi bên thuê không trả. Chỉ việc tài sản không còn để trả mới là căn cứ được nêu cho tài sản ký cược thuộc về bên cho thuê. Không thể suy từ một biện pháp bảo đảm sang việc mua bán hoặc chuyển sở hữu xe.',
 'Tìm điều kiện xử lý gắn với tình trạng thực tế của tài sản thuê.')
add('1.1','application',['DS:329:2'],
 'A đã trả lại xe thuê nhưng còn nợ tiền thuê đến hạn. Không có thỏa thuận khác, A đòi chủ xe hoàn ngay toàn bộ tài sản ký cược vì đã giao xe. Điều kiện nhận lại ký cược theo BLDS là gì?',
 'Trả lại tài sản thuê và trả tiền thuê',
 ['Chỉ cần trả lại xe, không cần trả tiền thuê','Chỉ cần hợp đồng thuê đã hết thời hạn','Chỉ cần bên thuê đã gửi yêu cầu hoàn tiền'],
 'Quy tắc ký cược không chỉ nhìn vào việc trả xe: bên thuê được nhận lại tài sản ký cược sau khi trả tiền thuê khi tài sản thuê được trả lại. Nợ tiền thuê còn tồn tại nên yêu cầu nhận ngay toàn bộ chỉ dựa vào việc trả xe chưa đáp ứng quy tắc này.',
 'Đọc đủ hai điều kiện, tránh bỏ phần sau của khoản 2.')
add('1.5','application',['DS:328:2'],
 'Trong một giao dịch dân sự, người mua giao 300 triệu đồng đặt cọc bảo đảm giao kết hợp đồng mua nhà. Bên nhận cọc tự ý từ chối giao kết, không có căn cứ miễn trách nhiệm và không có thỏa thuận xử lý khác. Tổng số tiền bên nhận cọc phải trả theo quy tắc mặc định là bao nhiêu?',
 '600 triệu đồng, gồm hoàn 300 triệu và trả thêm 300 triệu',
 ['300 triệu đồng là tổng nghĩa vụ hoàn và phạt','900 triệu đồng vì phải trả gấp ba trong mọi trường hợp','Không phải hoàn tiền vì khoản tiền đã giao thuộc về bên nhận'],
 'Bên nhận cọc từ chối phải trả lại tài sản đặt cọc và một khoản tương đương giá trị tài sản đặt cọc. Tổng là 600 triệu, trong đó khoản trả thêm là 300 triệu. Không nhầm tổng tiền trả với riêng phần chế tài, cũng không tự thêm mức gấp ba khi chưa thỏa thuận.',
 'Tách tiền hoàn lại với khoản trả thêm; sau đó mới cộng.')
add('1.5','application',['DS:328:2'],
 'Các bên trong giao dịch dân sự thỏa thuận rõ: nếu bên nhận 300 triệu đồng cọc tự ý từ chối giao kết, phải hoàn 300 triệu và trả thêm 900 triệu; không có căn cứ miễn trách nhiệm. Chỉ xét xử lý cọc theo thỏa thuận này, kết luận nào đúng?',
 'Tổng phải trả là 1,2 tỷ đồng; mức trả thêm khác mặc định có thể được thỏa thuận',
 ['Chỉ phải trả tổng 600 triệu vì luật cấm thỏa thuận khác','Tổng phải trả là 900 triệu vì đã bao gồm tiền hoàn cọc','Chỉ phải trả thêm tối đa 8% tiền cọc trong mọi giao dịch dân sự'],
 'Khoản 2 Điều 328 dành ngoại lệ cho thỏa thuận khác. Câu đã tách rõ tiền hoàn và tiền trả thêm nên tổng là 1,2 tỷ. Không tự áp quy tắc mặc định thay điều khoản rõ ràng, cũng không đưa trần phạt của một chế độ pháp luật khác thành trần chung cho mọi giao dịch dân sự.',
 'Kiểm tra điều khoản có nói rõ khoản trả thêm hay tổng số tiền không.')
add('2.6','application',['ND:37'],
 'A giao B 200 triệu đồng khi thỏa thuận mua tài sản. Các bên không xác định rõ khoản này là đặt cọc hay trả trước. B đòi áp dụng ngay cơ chế mất cọc. Theo quy tắc phân loại khoản tiền, phải coi khoản đã giao là gì?',
 'Tiền trả trước',
 ['Tiền đặt cọc vì đã giao trước ngày ký hợp đồng','Tiền ký cược vì B đang giữ khoản tiền','Tiền phạt vì A chưa trả hết giá mua'],
 'Điều 37 Nghị định 21/2021 quy định khoản tiền không được xác định rõ là cọc hay trả trước được coi là trả trước. Thời điểm giao sớm không đủ biến khoản tiền thành cọc. Không được dùng riêng cơ chế mất cọc khi chưa xác định được bản chất bảo đảm.',
 'Phân loại khoản tiền trước khi chọn chế tài.')
add('3.6','application',['DS:293:1','DS:328:1'],
 'Hợp đồng thuê nhà kéo dài 36 tháng. Hai bên thỏa thuận đặt cọc chỉ bảo đảm những nghĩa vụ đã xác định trong 24 tháng đầu, sau đó hoàn cọc nếu các nghĩa vụ này hoàn tất. Không có quy định chuyên ngành bắt buộc khác. CCV yêu cầu thời hạn cọc phải ít nhất 36 tháng. Đánh giá nào đúng?',
 'Yêu cầu đó không có căn cứ chỉ vì thời hạn cọc ngắn hơn; nghĩa vụ có thể được bảo đảm một phần',
 ['CCV đúng vì mọi biện pháp bảo đảm phải dài bằng hợp đồng chính','CCV đúng vì đặt cọc thuê nhà phải kéo dài thêm 12 tháng sau thuê','Hợp đồng thuê phải giảm còn 24 tháng để khớp thời hạn cọc'],
 'Điều 293 khoản 1 cho phép bảo đảm một phần nghĩa vụ, còn Điều 328 xác định đặt cọc trong một thời hạn. Dữ kiện đã làm rõ phạm vi 24 tháng đầu, nên không thể chỉ lấy thời hạn thuê 36 tháng để bắt buộc kéo dài cọc. Phải ghi rõ nghĩa vụ nào còn được bảo đảm sau mốc hoàn cọc.',
 'So sánh phạm vi bảo đảm, không chỉ so hai con số thời hạn.')
add('3.4','advanced',['DS:328:1'],
 'Hợp đồng thuê nhà đã ký và đang được thực hiện. Hai bên yêu cầu lập đặt cọc để bảo đảm việc trả tiền thuê trong 24 tháng tiếp theo. Dự thảo lại ghi cọc chỉ bảo đảm việc giao kết hợp đồng thuê và hoàn cọc ngay khi ký hợp đồng thuê. Lỗi cần sửa trước tiên là gì?',
 'Mục đích bảo đảm và điều kiện hoàn cọc không khớp nghĩa vụ thực hiện đã được yêu cầu',
 ['Phải đổi tên người thuê thành người mua nhà','Phải kéo thời hạn cọc lên đúng 36 tháng trong mọi trường hợp','Phải ghi cọc thành tiền trả trước vì hợp đồng thuê đã ký'],
 'Đặt cọc có thể bảo đảm giao kết hoặc thực hiện. Yêu cầu đang nhắm tới nghĩa vụ thực hiện sau khi giao kết, nhưng mẫu chỉ nhắm một sự kiện đã xảy ra và hoàn cọc ngay ở sự kiện đó. Giữ mẫu này sẽ không thể hiện đúng thỏa thuận cần công chứng; phải sửa nội dung bảo đảm và điều kiện hoàn cọc, không chỉ sửa tiêu đề.',
 'Đối chiếu sự kiện cần bảo đảm với sự kiện được mẫu dùng để hoàn cọc.')
add('3.1','understanding',['DS:105:1','DS:115','DS:328:1'],
 'A muốn dùng chính quyền sử dụng đất, không phải tiền bán đất, làm tài sản đặt cọc. A nói mọi tài sản theo BLDS đều là tài sản đặt cọc. Nhận định nào phù hợp?',
 'Quyền sử dụng đất là quyền tài sản nhưng không thuộc nhóm tiền, kim khí quý, đá quý hoặc vật có giá trị khác của đặt cọc',
 ['Đúng vì mọi quyền tài sản đều là vật có giá trị','Đúng nếu A giao bản gốc giấy chứng nhận thay cho quyền sử dụng đất','Sai vì quyền sử dụng đất không phải tài sản theo BLDS'],
 'BLDS phân biệt vật và quyền tài sản; quyền sử dụng đất được xác định là quyền tài sản. Điều 328 liệt kê nhóm đối tượng đặt cọc hẹp hơn khái niệm tài sản ở Điều 105. Giao giấy chứng nhận không tự biến quyền sử dụng đất thành một vật đặt cọc hay một biện pháp thế chấp hợp lệ.',
 'Không đồng nhất tài sản nói chung với đối tượng của từng biện pháp bảo đảm.')
add('3.5','application',['ND:38:2:d'],
 'A đặt cọc bằng vàng cho B. Chưa có sự đồng ý của A, B muốn đem số vàng này cho người khác vay trong thời hạn giữ cọc. Quy tắc nào phù hợp?',
 'B không được tự xác lập giao dịch sử dụng số vàng khi chưa có sự đồng ý của A',
 ['B được cho vay vì nhận cọc là nhận quyền sở hữu ngay','B được cho vay nếu hứa mua vàng khác để hoàn sau','B được cho vay nếu lợi nhuận chỉ thuộc về B'],
 'Điểm d khoản 2 Điều 38 Nghị định 21/2021 cấm bên nhận cọc xác lập giao dịch dân sự, khai thác, sử dụng tài sản cọc khi chưa có sự đồng ý của bên đặt. Lời hứa hoàn vật khác hay mục đích kiếm lợi không thay thế sự đồng ý; nhận giữ cọc chưa tự tạo quyền định đoạt vô hạn.',
 'Tìm sự đồng ý của đúng bên đối với đúng tài sản cọc.')
add('2.4','application',['ND:38:1:b'],
 'A đã giao vàng đặt cọc và muốn lấy lại vàng để thay bằng tiền có giá trị tương đương. B chưa đồng ý. A cho rằng tương đương giá trị là đủ để tự thay thế. Kết luận nào đúng?',
 'Việc thay tài sản đặt cọc cần sự đồng ý của B',
 ['A được tự thay vì mình là người giao tài sản','A được tự thay nếu có giấy định giá vàng','A chỉ phải báo sau khi đã lấy vàng đi'],
 'Điểm b khoản 1 Điều 38 cho bên đặt cọc trao đổi, thay thế tài sản cọc khi bên nhận cọc đồng ý. Điều kiện tương đương giá trị không thay thế sự đồng ý ấy. Đây là thay chính tài sản bảo đảm, khác với việc thương lượng mua một căn nhà khác.',
 'Phân biệt thay tài sản cọc với thay tài sản sẽ được mua.')
add('2.5','advanced',['DS:328:1','DS:321:5'],
 'Nhà của B đang thế chấp ngân hàng. A dự kiến giao tiền riêng của mình làm cọc để bảo đảm ký hợp đồng mua nhà sau khi đáp ứng điều kiện giải chấp hoặc được ngân hàng đồng ý theo luật. Thư ký nói chính căn nhà đang là tài sản cọc nên bắt buộc áp dụng quy tắc một tài sản bảo đảm nhiều nghĩa vụ. Lập luận nào cần sửa?',
 'Tài sản đặt cọc là tiền A giao; nhà dự kiến mua và nghĩa vụ thế chấp cần được kiểm tra riêng',
 ['Căn nhà luôn là tài sản cọc vì được nhắc đến trong hợp đồng','Tiền A giao trở thành tài sản thế chấp của ngân hàng ngay khi giao','Nhận cọc tự giải chấp nhà nên không cần kiểm tra ngân hàng nữa'],
 'Điều 328 xác định tài sản cọc là tài sản được giao để bảo đảm, ở đây là tiền của A. Căn nhà là đối tượng dự kiến mua và vẫn chịu ràng buộc thế chấp; Điều 321 khoản 5 đặt điều kiện bán tài sản thế chấp. Không thể dùng cơ chế một tài sản bảo đảm nhiều nghĩa vụ chỉ vì cả hai hồ sơ đều nhắc căn nhà, cũng không thể coi cọc đã xóa thế chấp. Câu chỉ sửa lập luận về đối tượng, không chứng nhận cả hồ sơ đã đủ điều kiện công chứng.',
 'Vẽ riêng tài sản cọc, tài sản thế chấp và đối tượng hợp đồng dự kiến.')
add('1.6','advanced',['CC:42:4','HN:35:1','HN:35:2:a'],
 'Dự thảo ghi cả vợ chồng B cam kết bán căn nhà là tài sản chung. Chỉ chồng đến ký nhận cọc; hồ sơ chưa chứng minh ý chí của vợ hoặc quyền đại diện, nhưng chồng yêu cầu ghi vợ cũng đã cam kết. CCV nên xử lý thế nào?',
 'Yêu cầu làm rõ sự đồng ý và quyền đại diện; không chứng nhận cam kết của vợ chỉ từ lời chồng',
 ['Chứng nhận ngay vì chỉ chồng đang nhận tiền','Chứng nhận ngay rồi tự bổ sung chữ ký vợ sau','Tuyên ngay mọi hợp đồng cọc do một người có vợ hoặc chồng ký đều vô hiệu'],
 'Vấn đề là dự thảo đang ghi nhận cam kết của một người chưa chứng minh tham gia hoặc được đại diện. Điều 35 Luật HNGĐ yêu cầu thỏa thuận vợ chồng khi định đoạt tài sản chung và thỏa thuận bằng văn bản đối với bất động sản. Điều 42 khoản 4 LCC yêu cầu làm rõ khi hồ sơ có vấn đề chưa rõ, từ chối nếu không làm rõ được. Không được giả định vợ đồng ý, cũng không suy thành mọi giao dịch cọc một người ký đều đương nhiên vô hiệu.',
 'Kiểm tra ai bị ràng buộc trong dự thảo và chứng cứ về ý chí/đại diện của họ.')
add('2.6','advanced',['DS:357:1','DS:357:2'],
 'Theo thỏa thuận chấm dứt giao dịch, B phải hoàn 300 triệu đồng cho A vào ngày xác định nhưng đã quá hạn và B chưa trả. Không có căn cứ miễn trách nhiệm. B nói tiền vốn là cọc nên không bao giờ có lãi chậm trả. Nhận định nào đúng?',
 'Nghĩa vụ hoàn tiền đã đến hạn có thể phát sinh lãi chậm trả theo Điều 357',
 ['B đúng vì chỉ hợp đồng vay mới có lãi do chậm trả','B đúng nếu trước đó tiền cọc không có lãi trong thời hạn giữ','A mặc nhiên được tính lãi từ ngày giao cọc, không cần xét ngày phải hoàn'],
 'Điều 357 áp dụng trách nhiệm chậm thực hiện nghĩa vụ trả tiền, không giới hạn ở hợp đồng vay. Khi nghĩa vụ hoàn tiền đã đến hạn và bị chậm, phải xem lãi chậm trả, thời gian chậm và lãi suất theo khoản 2. Điều này không đồng nghĩa mọi khoản cọc tự sinh lãi trong toàn bộ thời hạn đặt cọc.',
 'Xác định thời điểm phát sinh và đến hạn nghĩa vụ hoàn tiền, không chỉ tên khoản tiền ban đầu.')
add('2.6;extension','application',['KD:23:5'],
 'Chủ đầu tư dự án bán căn hộ hình thành trong tương lai đã đủ điều kiện đưa vào kinh doanh, giá ghi rõ là 4 tỷ đồng. Chủ đầu tư đề nghị thu cọc 300 triệu và nói mức cọc hoàn toàn tự do thỏa thuận theo BLDS. Chỉ xét mức cọc, xử lý nào đúng?',
 'Mức thu vượt trần 5% giá bán; tối đa 200 triệu đồng trong trường hợp này',
 ['Được thu 300 triệu nếu khách hàng đồng ý bằng văn bản','Được thu 300 triệu vì dưới trần 30% thanh toán lần đầu','Không được nhận bất kỳ khoản cọc nào dù căn hộ đủ điều kiện'],
 'Khoản 5 Điều 23 Luật KDBĐS đặt quy tắc riêng cho chủ đầu tư ở nhóm giao dịch này: chỉ thu cọc không quá 5% giá bán và phải đủ điều kiện kinh doanh. 5% của 4 tỷ là 200 triệu; 300 triệu vượt trần. Trần thanh toán lần đầu là một quy tắc khác, không thay trần cọc. Không áp trần 5% máy móc cho mọi mua bán nhà có sẵn giữa cá nhân.',
 'Kiểm tra chủ thể và loại bất động sản để chọn luật chuyên ngành trước tính tỷ lệ.')
add('1.5','application',['DS:3:2','DS:421:1'],
 'Hai bên đã đặt cọc mua nhà X. Sau đó cùng thống nhất bằng văn bản sửa thỏa thuận để mua nhà Y thay thế; đã xác định rõ nhà Y, giá, nghĩa vụ và đáp ứng các yêu cầu pháp luật, hình thức áp dụng. Một người nói không bao giờ được sửa vì ban đầu đã chọn nhà X. Đánh giá nào đúng?',
 'Không có lệnh cấm chung việc cùng thỏa thuận sửa hợp đồng; phải tuân thủ các điều kiện pháp luật áp dụng',
 ['Không được sửa trong bất cứ trường hợp nào sau khi đã giao cọc','Bên bán được tự thay nhà X bằng bất kỳ nhà nào mà không cần bên mua','Chỉ cần giá trị tương đương thì không cần kiểm tra điều kiện nhà Y'],
 'BLDS tôn trọng thỏa thuận không vi phạm điều cấm, không trái đạo đức xã hội và cho các bên thỏa thuận sửa đổi hợp đồng. Dữ kiện đã có đồng thuận và yêu cầu pháp luật được đáp ứng nên không thể cấm tuyệt đối việc đổi đối tượng dự kiến mua. Đây không phải quyền đơn phương tự thay nhà, cũng không phải thay chính số tiền đặt cọc.',
 'Phân biệt cùng thỏa thuận sửa với một bên tự thay tài sản.')
add('3.4;3.5','advanced',['DS:328:1','DS:328:2'],
 'Cọc chỉ bảo đảm giao kết hợp đồng thuê. Hợp đồng thuê đã được giao kết, hai bên đã thống nhất hoàn cọc và không chuyển cọc sang bảo đảm thực hiện. Sau đó người thuê chậm trả một kỳ tiền thuê. Chủ nhà muốn giữ khoản đang phải hoàn theo cơ chế mất cọc. Nhận định nào đúng?',
 'Không tự áp cơ chế mất cọc cho nghĩa vụ thực hiện ngoài phạm vi đã bảo đảm; nợ tiền thuê được xử lý riêng',
 ['Cọc bảo đảm giao kết mặc nhiên bảo đảm mọi vi phạm về sau','Chủ nhà được giữ cọc cho đến hết thuê dù đã thỏa thuận hoàn','Người thuê không phải trả tiền thuê vì từng giao cọc'],
 'Mục đích cọc đã giới hạn ở giao kết và sự kiện này đã hoàn tất. Dữ kiện loại trừ việc chuyển sang bảo đảm thực hiện, đồng thời xác định nghĩa vụ hoàn cọc. Vi phạm trả tiền thuê vẫn có thể bị xử lý theo hợp đồng và luật, nhưng không tự mở rộng phạm vi cọc để áp mất cọc cho nghĩa vụ không được bảo đảm.',
 'Xác định phạm vi cọc còn tồn tại ở thời điểm vi phạm; không dùng một chế tài cho mọi nghĩa vụ.')

def provision(spec):
 p=spec.split(':');code=p[0];number=p[1];cfg=CONFIG[code]
 b={'document':cfg[1],'article':'Điều '+number,'url':cfg[4]}
 if len(p)>2:b['clause']='Khoản '+p[2]
 if len(p)>3:b['point']='Điểm '+p[3]
 text=(WORK/'legal'/cfg[3]).read_text()
 m=re.search(r'(?:Điều|Điêu|Điểu|Điền)\s+'+number+r'[.,]',text)
 assert m,(code,number)
 nxt=re.search(r'(?:Điều|Điêu|Điểu|Điền)\s+\d+[.,]',text[m.end():])
 excerpt=text[m.start():m.end()+nxt.start() if nxt else len(text)].strip()
 assert len(excerpt)>100
 return b,{'reference':b,'sourceId':cfg[2],'evidenceExcerpt':excerpt}
bank=[];evidence=[]
for i,row in enumerate(ROWS,1):
 ident=f'DEP26-{i:03d}';basis=[];proof=[]
 for ref in row['refs']:
  b,e=provision(ref);basis.append(b);proof.append(e)
 choices=[row['key']]+row['wrong'];shift=(i-1)%4;choices=choices[-shift:]+choices[:-shift] if shift else choices
 q={'id':ident,'part':2,'topic':'Dân sự – giao dịch – đại diện – nghĩa vụ' if i!=16 else 'Đất đai, nhà ở và kinh doanh bất động sản','type':'single','status':'active','difficulty':row['difficulty'],'questionForm':'workflow' if row['difficulty']=='advanced' else 'short_case','question':{'variants':['Tháng 10/2026: '+row['stem']]},'answers':[{'id':chr(65+k),'text':a,'correct':a==row['key']} for k,a in enumerate(choices)],'explanation':'Gợi ý làm bài: '+row['hint']+'\n\n'+row['reason'],'legalBasis':basis,'lastVerified':DATE,'source':{'type':'user-provided','id':SOURCE,'questionNumber':row['origin'],'supportingSourceIds':list(dict.fromkeys(e['sourceId'] for e in proof))}}
 bank.append(q);evidence.append({'id':ident,'provisions':proof})
assert len(bank)==18 and len({q['question']['variants'][0] for q in bank})==18
(ROOT/'data/imported-deposit-2026.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
documents=[]
for code,cfg in CONFIG.items():
 documents.append({'sourceId':cfg[2],'url':cfg[4],'pdfSha256':[{'file':f,'sha256':hashlib.sha256((WORK/'legal'/f).read_bytes()).hexdigest()} for f in cfg[5]],'extraction':'OCR tiếng Việt BLDS đối chiếu bản chính; pdftotext các PDF có lớp chữ. Trích điều đầy đủ để truy vết, không coi OCR là nguồn độc lập.'})
(ROOT/'reports/deposit-legal-evidence-2026.json').write_text(json.dumps({'date':DATE,'scope':'18 câu đã biên tập độc lập theo pháp luật tháng 10/2026; không xác nhận nguyên bài giải nguồn','documents':documents,'questions':evidence},ensure_ascii=False,indent=2)+'\n')
p=ROOT/'data/question-sources.json';registry=json.loads(p.read_text())
entry={'id':SOURCE,'type':'user-provided','title':'Đề thi và bài giải đặt cọc do Madam An cung cấp','sha256':DOC_HASH,'use':'Nguồn tình huống: 3 đề/18 câu lớn và phụ lục ảnh 7 câu lớn. Biên tập đáp án độc lập, không coi bài giải là đáp án chính thức.'}
registry['sources']=[s for s in registry['sources'] if s['id']!=SOURCE]+[entry]
if not any(s['id']==CONFIG['ND'][2] for s in registry['sources']):registry['sources'].append({'id':CONFIG['ND'][2],'type':'official','title':CONFIG['ND'][1],'url':CONFIG['ND'][4],'use':'Đối chiếu Điều 37, 38; kiểm tra tình trạng còn hiệu lực tại CSDL quốc gia, ngày 05/10/2026.'})
p.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
titles=[['Ký cược thuê xe','Thẩm quyền đặt cọc','Hồ sơ công chứng','Soạn hợp đồng','Giá, đổi nhà, phạt cọc','Vợ vắng mặt và cam kết bán nhà'],['Đặt cọc và ký cược','Thẩm quyền đặt cọc','Hồ sơ công chứng','Soạn hợp đồng','Nhà đang thế chấp','Không cho thuê, chế tài và giá'],['Quyền sử dụng đất làm cọc','Thẩm quyền đặt cọc','Hồ sơ công chứng','Soạn hợp đồng','Sử dụng cọc, vi phạm và chuyển nhà','Thời hạn cọc ngắn hơn thuê']]
origins=[]
for exam,t in enumerate(titles,1):
 for number,title in enumerate(t,1):
  ref=f'{exam}.{number}';linked=[q['id'] for q in bank if ref in q['source']['questionNumber'].split(';')]
  origins.append({'id':'DEP-SRC-'+ref,'topic':title,'decision':'adapted_partial' if linked else 'review','adaptedQuestionIds':linked,'originalAnswerCertified':False,'lastVerified':None,'note':'Chỉ xác minh câu đã viết lại; phần thẩm quyền địa hạt, hồ sơ chi tiết và hạn chế chuyển nhà chưa được xác nhận hoàn tất.'})
for number,title in enumerate(['Đạo đức và lợi ích người thân','Thế chấp bảo đảm doanh nghiệp và đại diện','Quyền hộ gia đình, trẻ em và hồ sơ','Đổi ngân hàng, ủy quyền và cọc','Thừa kế, tài khoản Hàn Quốc và tư vấn','Xử lý thế chấp khi đã có cọc','Soạn thảo tổng hợp'],0):
 origins.append({'id':f'DEP-SRC-APP-{number}','topic':title,'decision':'review','adaptedQuestionIds':[],'originalAnswerCertified':False,'lastVerified':None,'note':'Phụ lục 3 ảnh, chỉ có đề; chưa kiểm định hoàn tất, không tạo câu active từ phần này.'})
assert len(origins)==25
(ROOT/'reports/deposit-source-review.json').write_text(json.dumps({'date':DATE,'sourceId':SOURCE,'sourceSha256':DOC_HASH,'sourceQuestionCount':25,'questions':origins,'activeAdded':18},ensure_ascii=False,indent=2)+'\n')
lines=['# Đề luyện đặt cọc và ký cược','', '18 câu trắc nghiệm, mỗi câu có một đáp án đúng. Thời gian gợi ý: 30 phút. Pháp luật áp dụng: tháng 10/2026. Đây là đề luyện được biên soạn, không phải đề chính thức.','', '## Câu hỏi','']
for i,q in enumerate(bank,1):
 lines+=['### Câu '+str(i),'',q['question']['variants'][0],'']+[a['id']+'. '+a['text'] for a in q['answers']]+['']
lines+=['## Đáp án và hướng dẫn','', '| Câu | Đáp án |','|---|---|']+[f'| {i} | '+next(a['id'] for a in q['answers'] if a['correct'])+' |' for i,q in enumerate(bank,1)]+['']
for i,q in enumerate(bank,1):
 lines+=['### Giải câu '+str(i),'',q['explanation'],'','Căn cứ: '+ '; '.join(b['document']+', '+b['article']+(', '+b['clause'] if 'clause' in b else '')+(', '+b['point'] if 'point' in b else '')+' ([nguồn]('+b['url']+'))' for b in q['legalBasis'])+'.','']
lines+=['## Những lỗi nguồn đã xử lý','', '- Đề 1 mở đầu ngày 20/8/2016 nhưng giải bằng BLDS 2015, chỉ có hiệu lực từ 01/01/2017. Đề luyện chuyển rõ sang tháng 10/2026; không xác nhận lời giải lịch sử.', '- Sửa nhầm Nghị định 21/2022 thành Nghị định 21/2021; cập nhật thủ tục theo Luật Công chứng 2024.', '- Mẫu đề 3 bảo đảm giao kết dù hợp đồng thuê đã ký; lời chứng còn ghi hợp đồng thuê thay vì hợp đồng đặt cọc. Mẫu đề 2 ghi bên A giao tiền cho chính bên A và ngày bằng chữ không khớp ngày bằng số.', '- Không cấm tuyệt đối cùng thỏa thuận thay nhà; phân biệt sửa đối tượng dự kiến mua với thay chính tài sản cọc.', '- Không mặc định mọi cọc đều bảo đảm toàn bộ nghĩa vụ, mọi vi phạm đều mất cọc, hoặc chỉ hợp đồng vay mới có lãi do chậm trả.', '- Không coi nhà đang thế chấp là chính tài sản cọc khi người mua giao tiền riêng; không lấy Điều 296 để giải tình huống sai đối tượng.', '- Không nhập lời giải địa hạt đặt cọc mua nhà khi chưa đủ căn cứ kết luận duy nhất; không tự tuyên mọi cọc một người vợ/chồng ký vô hiệu.', '', '## Kiểm soát chất lượng','', '18 câu mới: '+str(dict(collections.Counter(q['difficulty'] for q in bank)))+'. Cả 18 có khóa đơn, giải thích riêng, căn cứ và hồ sơ điều khoản. Không thêm biến thể diễn đạt để tăng số câu. Phụ lục ảnh 7 câu và những nhánh chưa xác minh tiếp tục review. Không tải tài liệu Word gốc lên repo.','']
(ROOT/'reports/deposit-exam-2026-10-05.md').write_text('\n'.join(lines))
print(json.dumps({'activeAdded':len(bank),'sourceQuestions':len(origins),'difficulty':dict(collections.Counter(q['difficulty'] for q in bank))},ensure_ascii=False))
