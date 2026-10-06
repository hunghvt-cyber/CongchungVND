"""Independently authored inheritance cases; source originals stay private."""
from pathlib import Path
import json,re,random,hashlib,collections
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parent;DATE='2026-10-06';SOURCE='USER-EXAM-INHERITANCE'
CONFIG={
 'DS':('Bộ luật Dân sự số 91/2015/QH13','OFFICIAL-BLDS15','BLDS-full.txt','https://vanban.chinhphu.vn/?pageid=27160&docid=183188',['BLDS-0.pdf','BLDS-1.pdf']),
 'CC':('Luật Công chứng số 46/2024/QH15','OFFICIAL-CC24','CC-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/01/luat46.pdf',['CC-0.pdf']),
 'HN':('Luật Hôn nhân và gia đình số 52/2014/QH13 (đối chiếu VBHN 121/VBHN-VPQH năm 2025)','OFFICIAL-HNGD-HN25','HNGD-HN-0.txt','https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/8/46059/58694-1-20251299-1300121-vbhn-vpqh.pdf',['HNGD-HN-0.pdf']),
 'ND':('Nghị định số 104/2025/NĐ-CP','OFFICIAL-ND10425','ND104-0.txt','https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/5/104-ndcp.signed.pdf',['ND104-0.pdf'])}
ROWS=[]
def add(origin,level,refs,stem,key,wrong,reason,hint,topic='Thừa kế'):
 ROWS.append(dict(origin=origin,difficulty=level,refs=refs,stem=stem,key=key,wrong=wrong,reason=reason,hint=hint,topic=topic))
add('1.1','advanced',['DS:613','DS:614','DS:612','DS:652'],
 'Mẹ của Hòa sống thêm một ngày sau Hòa, có quyền hưởng 200 triệu từ di sản Hòa nhưng chưa nhận tiền thì chết. Mẹ không có tài sản, nợ hay di chúc khác; chồng và cha mẹ đều đã chết, không có quan hệ thừa kế khác. Hai con duy nhất của mẹ là Hòa và Dũng đều đã chết trước mẹ. Hòa có hai con Hảo, Hóa; Dũng có một con Thành. Các cháu đều đủ điều kiện hưởng. Xử lý 200 triệu thế nào?',
 'Đưa vào di sản của mẹ; Hảo và Hóa mỗi người 50 triệu, Thành 100 triệu',
 ['Loại khỏi di sản mẹ vì mẹ chưa ký nhận; ba cháu không được hưởng khoản này','Chia ba cháu mỗi người bằng nhau vì đều là cháu ruột của mẹ','Chỉ Hảo và Hóa hưởng mỗi người 100 triệu vì tiền ban đầu của Hòa'],
 'Mẹ còn sống khi Hòa chết nên quyền thừa kế của mẹ đã phát sinh, không chờ công chứng hoặc nhận tiền. Khi mẹ chết, quyền tài sản này thuộc di sản của mẹ. Ở lần mở thừa kế của mẹ, hai nhánh Hòa và Dũng được thế vị: mỗi nhánh 100 triệu; hai con Hòa chia 100 triệu, con Dũng nhận 100 triệu. Không chia đều theo số đầu cháu và không bỏ nhánh Dũng vì nguồn tiền ban đầu từ Hòa.',
 'Vẽ hai thời điểm mở thừa kế rồi chia theo nhánh, không theo số cháu.')
add('1.1;extension','advanced',['DS:613','DS:644:1:a','DS:651:1:a','DS:651:2'],
 'Hòa đã ly hôn bằng quyết định có hiệu lực; không kết hôn lại. Cha Hòa chết trước Hòa. Di sản ròng là 900 triệu; hàng thứ nhất chỉ có mẹ, con 12 tuổi và con 25 tuổi có khả năng lao động. Di chúc hợp pháp cho toàn bộ Thảo, người chung sống với Hòa nhưng không phải vợ hợp pháp. Không ai từ chối hoặc thuộc Điều 621. Phân bổ tối thiểu cho mẹ, con 12 tuổi và phần còn lại theo di chúc là gì?',
 'Mẹ 200 triệu, con 12 tuổi 200 triệu; Thảo hưởng 500 triệu',
 ['Mẹ 150 triệu, con 12 tuổi 150 triệu; Thảo 600 triệu vì tính thêm người cha đã chết','Mẹ và cả hai con mỗi người 200 triệu; Thảo 300 triệu vì mọi con đều có phần bắt buộc','Mẹ và con 12 tuổi mỗi người 300 triệu; Thảo 300 triệu vì phần bắt buộc bằng trọn suất luật định'],
 'Chỉ ba người còn sống nêu trong hàng thứ nhất được tính suất theo pháp luật: 900/3 = 300 triệu. Mẹ và con chưa thành niên mỗi người được 2/3 suất, tức 200 triệu. Con thành niên có khả năng lao động không thuộc nhóm bảo vệ tại Điều 644; cha đã chết trước không có suất. Thảo hưởng theo di chúc, không phải dựa vào tư cách vợ. Đây là di sản ròng, không lấy toàn bộ tài sản chung chưa tách phần để tính.',
 'Xác định ai được tính suất trước, rồi ai được bảo vệ 2/3 suất.')
add('1.1;extension','understanding',['DS:651:1:a','HN:81:1'],
 'Hòa và Liên đã ly hôn bằng quyết định có hiệu lực. Hai con đẻ còn sống: Hảo ở với Liên, Hóa ở với Hòa theo quyết định giao nuôi. Hòa chết không có di chúc, không có vợ mới; chỉ xét ba người Liên, Hảo, Hóa và không có căn cứ loại trừ quyền hưởng của các con. Nhận định nào đúng?',
 'Cả Hảo và Hóa có tư cách con để hưởng thừa kế; Liên không hưởng với tư cách vợ cũ',
 ['Chỉ Hóa có tư cách thừa kế vì được giao cho Hòa trực tiếp nuôi','Liên thay Hảo hưởng với tư cách người đã trực tiếp nuôi Hảo','Liên và Hóa có tư cách thừa kế, Hảo mất quyền sau quyết định giao nuôi'],
 'Quyết định giao trực tiếp nuôi không chấm dứt quan hệ cha con; Điều 81 vẫn bảo đảm quyền, nghĩa vụ cha mẹ sau ly hôn. Điều 651 đưa con đẻ vào hàng thứ nhất, không phân biệt ở với ai. Liên đã không còn là vợ khi Hòa chết nên không hưởng theo tư cách vợ; quyền đại diện cho con nếu có khác quyền hưởng di sản của chính mình.',
 'Tách quyền trực tiếp nuôi, quyền đại diện và quyền hưởng thừa kế.')
add('1.5;extension','application',['DS:613','DS:660:1','DS:651:2'],
 'Người cha chết không di chúc, di sản ròng 600 triệu. Hàng thứ nhất chỉ có vợ, một con đã sinh và một thai nhi đã thành thai trước khi cha chết, quan hệ cha con được xác định. Không có căn cứ loại trừ quyền hưởng. Vợ muốn chia ngay toàn bộ cho mình và con đã sinh, cam kết sẽ tự lo cho thai nhi sau. Hướng phân chia nào đúng?',
 'Dành lại 200 triệu cho thai nhi; hai người đã sinh mỗi người hưởng 200 triệu',
 ['Vợ và con đã sinh mỗi người 300 triệu, cam kết nuôi dưỡng thay phần dự phòng','Vợ 300 triệu, con đã sinh 200 triệu, thai nhi chỉ cần dự phòng 100 triệu','Chia cả 600 triệu cho vợ quản lý với tư cách chủ sở hữu, thai nhi sẽ hưởng từ tài sản riêng của vợ'],
 'Khoản 1 Điều 660 bắt buộc dành phần bằng suất của người cùng hàng cho người đã thành thai chưa sinh. Ba suất tương ứng mỗi suất 200 triệu; việc còn sống khi sinh ra quyết định hưởng theo Điều 613. Không thể chia hết rồi dùng lời hứa nuôi dưỡng để thay bảo vệ phần tài sản. Câu xét thừa kế theo pháp luật, không nhầm với mức 2/3 suất ở trường hợp di chúc.',
 'Xác định chế độ chia theo pháp luật và số suất có tính thai nhi.')
add('1.5;extension','advanced',['DS:658:1','DS:658:3','DS:658:8','DS:615:1'],
 'Di sản chỉ có 100 triệu tiền mặt; chi phí mai táng hợp lý theo tập quán đã xác định 20 triệu, bảo quản di sản 10 triệu, nợ vay không có bảo đảm 100 triệu. Không có nghĩa vụ khác, không ai thỏa thuận trả thêm. Chủ nợ muốn nhận toàn bộ 100 triệu trước vì có giấy vay. Phương án thanh toán nào đúng?',
 'Mai táng 20 triệu, bảo quản 10 triệu, chủ nợ 70 triệu; không còn để chia',
 ['Chủ nợ 100 triệu, người thừa kế phải trả riêng toàn bộ 30 triệu chi phí','Chia ba khoản theo tỷ lệ 20:10:100 vì đều là nghĩa vụ liên quan di sản','Mai táng 20 triệu, chủ nợ 80 triệu, bỏ chi phí bảo quản vì không phải nợ vay'],
 'Điều 658 đặt mai táng hợp lý ở thứ tự 1, bảo quản ở thứ tự 3, nợ thông thường ở thứ tự 8. Vì không có các khoản xen giữa hoặc tài sản bảo đảm, thanh toán lần lượt còn 70 triệu cho nợ vay. Điều 615 giới hạn trách nhiệm trong di sản nếu không thỏa thuận khác. Không lấy ngày lập giấy vay để đảo thứ tự và không áp phép chia tỷ lệ giữa các thứ tự khác nhau.',
 'Xếp khoản vào thứ tự ưu tiên trước khi tính số tiền còn lại.')
add('5.4;6.4;8.4','application',['DS:620','DS:656:1:b','DS:656:2','DS:660:2'],
 'Liên, Hùng và Hoài là ba người thừa kế theo pháp luật duy nhất, đều thành niên, đủ năng lực; người chết không có di chúc. Trước khi chia, Liên không có nghĩa vụ cần trốn tránh và muốn Hùng nhận riêng toàn bộ phần đáng lẽ của Liên. Dự thảo ghi “từ chối nhận di sản với điều kiện phần đó chỉ thuộc Hùng”. Cách làm phù hợp mục tiêu là gì?',
 'Làm rõ và thể hiện việc nhường phần qua thỏa thuận phân chia hợp pháp; không dùng từ chối để tự chỉ định người nhận phần đó',
 ['Chỉ cần ghi tên Hùng trong văn bản từ chối thì Điều 620 tự chuyển quyền riêng cho Hùng','Phải từ chối trước, rồi mọi người còn lại bắt buộc tặng phần tăng thêm cho Hùng','Không được nhường cho Hùng theo bất kỳ thỏa thuận phân chia nào dù hai người đều đủ năng lực'],
 'Từ chối theo Điều 620 là không nhận di sản, không phải một giao dịch cho phép người từ chối chỉ định đích nhận như tặng cho. Khi mục tiêu là để một người cụ thể nhận tài sản, phải xác định ý chí, chủ thể và phương thức phân chia phù hợp Điều 656, 660, đáp ứng các điều kiện liên quan. Câu loại trừ trốn nợ và thiếu năng lực; không suy rằng mọi thỏa thuận phân chia khác tỷ lệ đều bị cấm.',
 'Hỏi người yêu cầu muốn không nhận hay muốn chuyển lợi ích cho một người xác định.')
add('6.1','understanding',['DS:616:1','DS:656:1:a','DS:656:2'],
 'Di chúc không chỉ định người quản lý di sản. Tất cả người thừa kế thành niên, đủ năng lực thống nhất bằng văn bản cử một người bạn tin cậy, không phải người thừa kế, để quản lý. CCV nói luật bắt buộc chọn trong số người thừa kế. Đánh giá nào đúng?',
 'Không có yêu cầu bắt buộc người quản lý phải là người thừa kế; không bác lựa chọn chỉ vì người bạn không có suất hưởng',
 ['CCV đúng vì chỉ người có suất thừa kế mới được cử quản lý','Người ngoài chỉ được quản lý nếu được chỉ định trước trong di chúc, không được cử sau khi người đó chết','Chỉ được chọn người ngoài qua bản án; thỏa thuận cử người quản lý không đủ căn cứ'],
 'Khoản 1 Điều 616 cho người được chỉ định trong di chúc hoặc được những người thừa kế thỏa thuận cử quản lý, không bắt buộc họ là người thừa kế. Điều 656 ghi nhận việc họp cử và yêu cầu thỏa thuận bằng văn bản. Vẫn phải kiểm tra điều kiện giao dịch, phạm vi quyền và nghĩa vụ; câu không kết luận mọi văn bản cử bất kỳ ai đều đương nhiên hợp lệ.',
 'Đọc điều kiện về cách cử, không thêm điều kiện về suất hưởng.')
add('6.4;extension','advanced',['DS:617:1:b','DS:618:1:a'],
 'Long được tất cả người thừa kế cử quản lý di sản theo khoản 1 Điều 616. Long muốn thế chấp nhà thuộc di sản để vay sửa chữa; chưa có người thừa kế nào đồng ý bằng văn bản. Long viện quyền đại diện trong quan hệ với người thứ ba để tự ký. Chỉ xét giới hạn quản lý di sản, nhận định nào đúng?',
 'Quyền đại diện không thay sự đồng ý bằng văn bản của những người thừa kế đối với việc thế chấp',
 ['Long được tự thế chấp vì khoản vay có mục đích bảo quản','Long chỉ cần tự cam kết chịu nợ là được thay sự đồng ý bằng văn bản','Quyền đại diện tại Điều 618 bao gồm tự định đoạt toàn bộ nhà mà không cần kiểm tra Điều 617'],
 'Điểm a khoản 1 Điều 618 xác định quyền đại diện, nhưng điểm b khoản 1 Điều 617 đặt giới hạn riêng đối với bán, tặng, cầm cố, thế chấp và định đoạt khác: phải được những người thừa kế đồng ý bằng văn bản. Mục đích sửa chữa hoặc cam kết chịu nợ không tự thay điều kiện này. Ngay cả có sự đồng ý vẫn phải kiểm tra điều kiện thế chấp khác; câu chỉ hỏi giới hạn từ chế định quản lý.',
 'Đọc quyền đại diện cùng nghĩa vụ không tự định đoạt.')
add('6.1;extension','understanding',['DS:616:2','DS:617:2:a','DS:618:2:a'],
 'Hùng đang thuê nhà của người chết theo hợp đồng còn hạn. Di chúc không chỉ định người quản lý và các người thừa kế chưa cử ai. Hùng tiếp tục quản lý nhà theo khoản 2 Điều 616, cho rằng như vậy mình có thể bán nhà thay cả nhóm thừa kế. Nhận định nào đúng?',
 'Tiếp tục quản lý, sử dụng theo hợp đồng không trao quyền bán nhà của nhóm thừa kế',
 ['Đang tiếp tục sử dụng thì có đầy đủ quyền đại diện như người được cử theo khoản 1 Điều 616','Có thể bán nhà nếu báo tin bằng điện thoại cho một người thừa kế','Hùng được bán nếu cam kết giá bán không thấp hơn giá thị trường, không cần căn cứ đại diện khác'],
 'Người tiếp tục chiếm hữu, sử dụng theo khoản 2 Điều 616 là nhóm khác với người được chỉ định/cử ở khoản 1. Điểm a khoản 2 Điều 618 cho tiếp tục sử dụng theo hợp đồng hoặc sự đồng ý; điểm a khoản 2 Điều 617 cấm tự bán, tặng, thế chấp hay định đoạt. Không lấy việc đang ở trong nhà để suy ra quyền bán thay những người thừa kế.',
 'Xác định người quản lý thuộc khoản 1 hay khoản 2 Điều 616.')
add('6.4;extension','understanding',['DS:618:1:b','DS:618:3'],
 'Long đã thực hiện quản lý di sản theo việc được cử hợp lệ. Văn bản cử không thỏa thuận mức thù lao; nay không đạt được thỏa thuận về mức trả. Một người thừa kế nói không có mức ghi trước thì Long không được hưởng khoản nào. Quy tắc đúng là gì?',
 'Không đạt thỏa thuận về mức thì được hưởng một khoản thù lao hợp lý',
 ['Không ghi trước mức tiền thì mọi công việc quản lý bắt buộc không có thù lao','Long được tự chọn bất kỳ mức nào và lấy ngay khỏi tài khoản di sản','Mức trả luôn bằng toàn bộ tiền thuê nhà, không phụ thuộc thỏa thuận hoặc tính hợp lý'],
 'Khoản 3 Điều 618 dự liệu chính trường hợp không đạt thỏa thuận về mức thù lao: được hưởng khoản hợp lý. Không đồng nhất việc chưa ghi mức với miễn phí tuyệt đối; cũng không cho phép người quản lý tự ấn định tùy ý rồi tự rút tiền. Nếu có tranh chấp mức hợp lý phải giải quyết theo quy định, không dùng đáp án để xác định sẵn một tỷ lệ không có trong luật.',
 'Tìm quy tắc bổ sung khi thương lượng mức thù lao không thành.')
add('6.6;extension','application',['DS:618:1:b','DS:618:1:c'],
 'Theo thỏa thuận hợp lệ, Long quản lý di sản miễn thù lao. Long đã ứng 8 triệu cho chi phí bảo quản cần thiết, hợp lý và được các người thừa kế xác nhận. Họ từ chối hoàn chi phí vì đã thỏa thuận không trả thù lao; không có thỏa thuận Long chịu riêng chi phí. Đánh giá nào đúng?',
 'Miễn thù lao không tự loại quyền được thanh toán chi phí bảo quản đã xác định',
 ['Không trả thù lao thì mọi chi phí bảo quản cũng do Long tự chịu','Long chỉ được hoàn chi phí nếu trở thành người thừa kế','Chi phí chỉ được hoàn nếu trước khi chi đã ấn định cả mức thù lao quản lý'],
 'Điều 618 tách quyền hưởng thù lao tại điểm b khỏi quyền thanh toán chi phí bảo quản tại điểm c. Dữ kiện đã xác nhận tính cần thiết, hợp lý và không có thỏa thuận chịu riêng nên không thể dùng điều khoản miễn thù lao để từ chối hoàn 8 triệu. Câu không hợp thức hóa mọi khoản chi sửa chữa tùy ý hoặc chi không được chứng minh.',
 'Lập hai khoản riêng: tiền công quản lý và khoản đã ứng để bảo quản.')
add('6.5','advanced',['DS:616:1','DS:617:1:b'],
 'Nhà thuộc di sản đang thế chấp bảo đảm một khoản vay còn tồn tại. Các người thừa kế chỉ muốn cử Long quản lý, không bán, tặng, chuyển quyền hay lập thế chấp mới; quyền của bên nhận thế chấp được giữ nguyên. CCV cho rằng phải giải chấp trước mọi văn bản liên quan, kể cả cử người quản lý. Chỉ xét lý do này, hướng đánh giá nào đúng?',
 'Không có căn cứ từ việc thế chấp để cấm tuyệt đối việc cử người quản lý; phân biệt quản lý với định đoạt và tiếp tục bảo đảm quyền chủ nợ',
 ['Mọi thỏa thuận cử người quản lý tự chuyển nhà sang sở hữu người đó nên phải giải chấp','Cử người quản lý tự xóa thế chấp, vì vậy chủ nợ phải được thanh toán trước','Có thế chấp thì pháp luật không cho bất kỳ ai quản lý di sản cho đến khi trả hết nợ'],
 'Điều 616 cho cử người quản lý di sản; Điều 617 tách việc bảo quản khỏi các hành vi định đoạt bị giới hạn. Chỉ cử quản lý không làm đổi chủ sở hữu, xóa bảo đảm hay cho phép bán nhà. Vì vậy không thể suy từ việc tài sản đang thế chấp thành cấm tuyệt đối văn bản cử quản lý. Điều kiện bán, thế chấp mới, chuyển quyền hoặc rút tiền trả nợ phải được xét riêng.',
 'Xác định văn bản chỉ quản lý hay có nội dung định đoạt tài sản bảo đảm.')
add('6.5;extension','application',['DS:615:1','DS:615:2'],
 'Di sản chưa chia chỉ có 500 triệu tiền mặt, nợ thông thường 700 triệu, không có chi phí hay nghĩa vụ khác. Long là người được cử quản lý, không phải người thừa kế; các người thừa kế thống nhất dùng di sản trả nợ, không ai thỏa thuận gánh thêm. Chủ nợ đòi Long trả 200 triệu còn thiếu bằng tài sản riêng vì Long quản lý. Kết luận nào đúng?',
 'Long thực hiện thanh toán theo thỏa thuận trong phạm vi 500 triệu di sản; không tự gánh 200 triệu chỉ vì làm người quản lý',
 ['Long phải trả toàn bộ 700 triệu vì người quản lý trở thành người mắc nợ thay người chết','Mọi người quản lý không phải thừa kế đều không được dùng di sản trả nợ','Phải chia hết 500 triệu cho người thừa kế trước rồi mới xem xét trả nợ'],
 'Khoản 2 Điều 615 giao người quản lý thực hiện nghĩa vụ tài sản theo thỏa thuận những người thừa kế khi di sản chưa chia và trong phạm vi di sản. Khoản 1 không mặc định dùng tài sản riêng trả vượt di sản khi không thỏa thuận khác. Quản lý không phải việc nhận thay toàn bộ nghĩa vụ cá nhân của người chết; cũng không được chia hết để bỏ qua nghĩa vụ còn phải thanh toán.',
 'Kiểm tra di sản đã chia chưa và có cam kết chịu thêm nghĩa vụ hay không.')
add('2.6;extension','advanced',['DS:615:3'],
 'Di sản đã chia: A nhận 300 triệu, B nhận 100 triệu. Sau đó xác định khoản nợ 200 triệu của người chết cần thanh toán; không có nghĩa vụ khác và không có thỏa thuận khác. Chủ nợ đề nghị phân bổ cả khoản nợ cho A chỉ vì A nhận nhiều hơn. Mức trách nhiệm theo tỷ lệ của A, B là gì?',
 'A 150 triệu, B 50 triệu',
 ['A 200 triệu, B không chịu vì B nhận ít hơn khoản nợ','A 100 triệu, B 100 triệu vì hai người là đồng thừa kế','A 300 triệu, B 100 triệu vì phải trả lại toàn bộ di sản đã nhận dù nợ chỉ 200 triệu'],
 'Khoản 3 Điều 615 phân bổ tương ứng phần đã nhận và không vượt phần đó, trừ thỏa thuận khác. Tỷ lệ nhận 300:100 = 3:1 nên khoản 200 triệu phân bổ 150:50, đều nằm trong giới hạn. Số người thừa kế không phải căn cứ chia đều khi phần thực nhận khác nhau; việc một người nhận nhiều không khiến người còn lại hết nghĩa vụ.',
 'Lấy tỷ lệ phần thực nhận, rồi kiểm tra trần trách nhiệm từng người.')
add('5.4;6.4','application',['DS:611:1','DS:612','DS:457'],
 'Sau khi Lân chết, một người bạn tặng riêng 20 triệu cho vợ Lân bằng thỏa thuận rõ và đã giao tiền, không tặng cho Lân hay cho nhóm người thừa kế. Con Lân muốn liệt kê khoản này là di sản Lân chỉ vì được trao trong đám tang. Chỉ xét khoản đã xác định này, đánh giá nào đúng?',
 'Không phải di sản Lân; việc nhận trong đám tang không thay nguồn sở hữu của khoản tặng riêng cho vợ',
 ['Mọi tiền trao trong đám tang tự là di sản của người chết, bất kể người được tặng','Khoản tiền tự thuộc sở hữu tất cả người thừa kế theo tỷ lệ thừa kế','Người đang quản lý đám tang có quyền đưa khoản tặng riêng vào di sản chỉ bằng danh mục của mình'],
 'Di sản theo Điều 612 là tài sản của người chết, gồm phần của người chết trong tài sản chung. Điều 611 xác định thời điểm mở thừa kế khi chết; khoản tặng riêng cho người vợ sau đó theo dữ kiện không từng thuộc người chết. Điều 457 xác định giao dịch tặng cho. Không khái quát mọi tiền phúng viếng đều thuộc một người; phải xét ý chí người đưa tiền, người nhận và mục đích từng khoản.',
 'Truy nguồn sở hữu, không chỉ nhìn nơi và dịp giao tiền.')
add('3.5;extension','application',['DS:659:2'],
 'Di chúc hợp pháp cho Hân riêng một căn nhà theo hiện vật. Nhà có giá 1 tỷ khi mở thừa kế, còn 800 triệu khi chia do thị trường; tiền thuê thuần phát sinh từ nhà trong thời gian chờ chia là 60 triệu, chưa chia cho ai. Không có nợ, phần bắt buộc hay thỏa thuận khác. Quyền của Hân theo cơ chế chia hiện vật là gì?',
 'Nhận căn nhà cùng 60 triệu tiền thuê và chịu giảm giá thị trường của nhà',
 ['Chỉ nhận nhà; 60 triệu bắt buộc chia đều mọi người thừa kế vì phát sinh sau khi chết','Nhận nhà và buộc các người thừa kế khác bù 200 triệu giảm giá thị trường','Không nhận nhà nữa vì giá thay đổi làm di chúc mất hiệu lực toàn bộ'],
 'Khoản 2 Điều 659 gắn hiện vật được chỉ định với hoa lợi, lợi tức thu được từ hiện vật, đồng thời người nhận chịu phần giá trị bị giảm sút đến lúc chia. Giá giảm do thị trường không phải lỗi người khác làm tiêu hủy để đòi bồi thường. Câu đã loại trừ nghĩa vụ và quyền bắt buộc có thể ảnh hưởng phép phân bổ.',
 'Phân biệt chia một hiện vật với cho một số tiền cố định.')
add('3.5;extension','advanced',['DS:659:3'],
 'Di chúc chỉ cho Hân 1/3 tổng giá trị khối di sản, không ấn định tiền hoặc hiện vật. Giá trị ròng khi mở thừa kế 1,2 tỷ, đến khi chia còn 900 triệu do biến động giá hợp pháp. Không có người hưởng phần bắt buộc, tranh chấp hay thỏa thuận khác. Hân muốn khóa mức 400 triệu tại ngày chết. Áp dụng đúng là gì?',
 'Tính 1/3 trên 900 triệu còn tại thời điểm chia, tức 300 triệu',
 ['Hân nhận 400 triệu vì mọi tỷ lệ được khóa thành khoản tiền tại ngày chết','Hân nhận 600 triệu vì phải bù thêm phần giảm giá cho người hưởng theo di chúc','Chuyển toàn bộ sang chia theo pháp luật vì giá trị di sản đã giảm'],
 'Khoản 3 Điều 659 quy định tỷ lệ được tính trên giá trị khối di sản đang còn tại thời điểm phân chia. Di chúc không cho khoản tiền cố định 400 triệu và không định đoạt một hiện vật cụ thể, nên không dùng giá ngày chết để cố định phần hưởng. Sự thay đổi giá hợp pháp tự nó không làm di chúc mất hiệu lực.',
 'Xác định di chúc ghi hiện vật, số tiền hay tỷ lệ trước khi chọn mốc định giá.')
add('3.1;extension','understanding',['DS:659:1'],
 'Di chúc hợp pháp chỉ định Hân, Hoài và một người bạn nhận toàn bộ di sản, không ghi phần mỗi người. Không có người hưởng phần bắt buộc, nghĩa vụ tài sản hoặc thỏa thuận khác. Người bạn không có quan hệ gia đình. Quy tắc chia mặc định là gì?',
 'Chia đều cho cả ba người được chỉ định trong di chúc',
 ['Chỉ chia cho Hân và Hoài vì người bạn không thuộc hàng thừa kế theo pháp luật','Chuyển toàn bộ sang chia theo pháp luật vì di chúc không ghi tỷ lệ','Hân và Hoài mỗi người nhận 40%, người bạn 20% vì quan hệ gia đình quyết định ưu tiên'],
 'Khoản 1 Điều 659 đặt quy tắc chia đều giữa những người được chỉ định trong di chúc khi không xác định rõ phần và không có thỏa thuận khác. Không tự thay danh sách này bằng các hàng tại Điều 651. Quan hệ gia đình không làm tăng tỷ lệ trong tình huống đã loại trừ phần bắt buộc.',
 'Lấy danh sách người được chỉ định, không thay bằng hàng thừa kế theo pháp luật.')
add('3.5;5.6','advanced',['DS:662:1'],
 'Di sản đã chia cho A và B, mỗi người nhận tài sản trị giá 600 triệu tại lúc chia. Sau đó C được xác định là người thừa kế bị bỏ sót, phần C đáng hưởng tại lúc chia là 400 triệu. Hiện tài sản A, B tăng gấp đôi; không có thỏa thuận khác. Phương án mặc định đúng là gì?',
 'A và B mỗi người thanh toán 200 triệu cho C; không chia lại bằng hiện vật',
 ['A và B mỗi người thanh toán 400 triệu vì phải lấy giá thị trường hiện tại','C buộc A và B trả lại toàn bộ hiện vật để chia từ đầu trong mọi trường hợp','Chỉ người đang giữ nhà trả 400 triệu, người nhận tiền trước đây không có trách nhiệm'],
 'Khoản 1 Điều 662 không chia lại bằng hiện vật mà thanh toán khoản tương ứng phần người mới tại thời điểm chia, theo tỷ lệ phần đã nhận, trừ thỏa thuận khác. A và B nhận tỷ lệ 1:1 nên mỗi người trả 200 triệu. Không lấy giá tăng hiện tại để nâng phần C lên 800 triệu và không tự chuyển toàn bộ nghĩa vụ cho người giữ một loại tài sản.',
 'Giữ đúng hai mốc: phần người mới tại lúc chia và tỷ lệ người cũ đã nhận.')
add('5.6;extension','advanced',['DS:662:2'],
 'Sau khi chia, D bị bác bỏ quyền thừa kế bằng quyết định có hiệu lực. D đã nhận 300 triệu tiền mặt nhưng nay dùng hết; không có thỏa thuận khác về hoàn trả. D nói chỉ còn 50 triệu tài sản riêng nên chỉ hoàn 50 triệu vì Điều 615 giới hạn trách nhiệm. Nhận định nào đúng?',
 'D phải trả lại di sản hoặc thanh toán giá trị tương đương 300 triệu tại thời điểm chia; việc đã dùng hết không giảm nghĩa vụ hoàn trả',
 ['D chỉ phải hoàn 50 triệu vì trần hoàn trả luôn bằng tài sản còn giữ','D không phải hoàn nếu tiền đã được tiêu dùng trước khi quyết định bác bỏ có hiệu lực','D chỉ phải hoàn 2/3 của 300 triệu vì đây là phần bắt buộc của người bị bác bỏ'],
 'Khoản 2 Điều 662 điều chỉnh riêng việc người đã nhận bị bác bỏ quyền: trả lại di sản hoặc khoản tiền tương đương giá trị đã hưởng tại thời điểm chia. Đây không phải khoản nợ của người chết được phân bổ theo Điều 615. Việc dùng tiền không tạo quyền giữ phần đã nhận sai; khả năng thi hành thực tế khác với xác định mức nghĩa vụ.',
 'Phân biệt trả nợ của người chết với hoàn trả tài sản do bị bác bỏ quyền hưởng.')
add('7.2','advanced',['DS:22:1','DS:613','DS:651:1:a','CC:59:3'],
 'Lan là con đẻ còn sống của người chết. Gia đình xuất trình giấy chẩn đoán bệnh tâm thần, chưa có quyết định Tòa án tuyên mất năng lực; không có căn cứ loại trừ quyền hưởng di sản. Họ muốn bỏ Lan khỏi danh sách vì Lan không thể tự ký thuận lợi. Hướng xử lý đúng là gì?',
 'Không bỏ quyền hưởng chỉ vì bệnh; làm rõ năng lực và cơ chế tham gia/đại diện theo pháp luật, không coi chẩn đoán tự thay quyết định Tòa án',
 ['Bệnh tâm thần tự làm mất cả năng lực và quyền thừa kế nên không cần ghi Lan','Chỉ người tự ký được mới có thể là người thừa kế theo Điều 613','Người thân được tự chọn người ký thay Lan mà không cần xác định căn cứ đại diện'],
 'Điều 613 không đòi mọi người thừa kế có đầy đủ năng lực hành vi; Lan vẫn có tư cách con theo Điều 651. Điều 22 gắn việc tuyên mất năng lực với quyết định của Tòa án trên cơ sở kết luận giám định, không phải mọi giấy chẩn đoán. CCV phải làm rõ điều kiện tham gia/đại diện; không được bỏ người hưởng để làm hồ sơ thuận tiện. Câu không kết luận Lan đương nhiên có đủ năng lực chỉ vì chưa có quyết định.',
 'Tách quyền hưởng, đánh giá năng lực và người có quyền ký đại diện.')
add('7.3;8.5;extension','application',['DS:21:4','HN:77:2'],
 'Cháu 16 tuổi được hưởng riêng một phần quyền sử dụng đất và muốn tự ký giao dịch chuyển nhượng phần đó sau khi đã hoàn tất thừa kế. Cháu có mẹ là người đại diện hợp lệ; mẹ chưa đồng ý bằng văn bản. Chỉ xét điều kiện định đoạt tài sản của người chưa thành niên, đánh giá nào đúng?',
 'Chưa đáp ứng điều kiện; định đoạt bất động sản của con 15–dưới 18 tuổi phải có sự đồng ý bằng văn bản của cha mẹ hoặc người giám hộ',
 ['Đủ 15 tuổi thì được tự định đoạt mọi bất động sản mà không cần ai đồng ý','Tài sản nhận do thừa kế luôn được tự bán bất kể tuổi','Chỉ cần mẹ đồng ý miệng và tham gia buổi công chứng, không cần sự đồng ý bằng văn bản'],
 'Khoản 4 Điều 21 loại giao dịch bất động sản khỏi nhóm người 15–dưới 18 tự xác lập thông thường. Khoản 2 Điều 77 cụ thể hóa điều kiện đồng ý bằng văn bản của cha mẹ hoặc người giám hộ đối với tài sản loại này. Nguồn gốc thừa kế không miễn điều kiện do tuổi; câu không hỏi chuyển nhượng đất có đáp ứng toàn bộ điều kiện đất đai hay không.',
 'Xác định tuổi và loại tài sản, không chỉ nguồn gốc được thừa kế.')
add('7.2;7.3;extension','advanced',['DS:59:1'],
 'Bích là người giám hộ hợp lệ của Lan mất năng lực và cũng là đồng thừa kế. Bích muốn nhân danh Lan thỏa thuận đổi phần tài sản của Lan lấy chính tài sản của Bích; giao dịch có liên quan tài sản Lan. Dù hồ sơ xác định lợi ích cho Lan, người giám sát chưa đồng ý. Bích nói quan hệ mẹ con đủ để bỏ giám sát. Nhận định nào đúng?',
 'Chưa đủ điều kiện ngoại lệ cho giao dịch giữa giám hộ và người được giám hộ; phải có sự đồng ý của người giám sát cùng điều kiện vì lợi ích Lan',
 ['Quan hệ mẹ con thay sự đồng ý của giám sát trong mọi giao dịch chia di sản','Có lợi ích cho Lan thì sự đồng ý của giám sát không còn cần thiết','Người giám hộ là đồng thừa kế có thể tự đại diện hai phía mà không cần xét giao dịch cụ thể'],
 'Khoản 1 Điều 59 xác định giao dịch giữa người giám hộ và người được giám hộ liên quan tài sản là vô hiệu, trừ trường hợp vì lợi ích người được giám hộ và có sự đồng ý của người giám sát. Hai điều kiện là đồng thời; quan hệ mẹ con và tư cách đồng thừa kế không thay điều kiện còn thiếu. Đây là nhánh xung đột lợi ích, không chỉ câu thuần nhận biết có người giám hộ.',
 'Kiểm tra có giao dịch giữa hai bên giám hộ và ngoại lệ đủ cả hai điều kiện chưa.')
add('1.1;3.1;extension','advanced',['DS:643:2:a','DS:650:2:c','DS:651:2','DS:652'],
 'Ông P lập di chúc cho toàn bộ 600 triệu tài sản riêng cho con A. A chết trước P, để lại con C. Khi P chết, con B còn sống; ngoài B và nhánh A không có người hưởng theo pháp luật, không có nghĩa vụ tài sản, di chúc thay thế hay người hưởng khác. C muốn nhận toàn bộ 600 triệu bằng cách “thế vị trực tiếp trong di chúc”. Kết quả đúng là gì?',
 'Phần chỉ định A không có hiệu lực và được chia theo pháp luật; B 300 triệu, C thế vị nhánh A 300 triệu',
 ['C tự thay A trong di chúc nên hưởng toàn bộ 600 triệu, B không có phần','B hưởng toàn bộ 600 triệu vì người được di chúc cho hưởng đã chết','C và B đều không hưởng vì di chúc không chỉ định tên họ'],
 'Người hưởng theo di chúc chết trước làm phần chỉ định đó không có hiệu lực theo Điều 643. Phần này chuyển sang thừa kế theo pháp luật theo điểm c khoản 2 Điều 650; khi đó Điều 652 mới được áp dụng cho nhánh A. B và nhánh A chia hai suất bằng nhau. Không dùng thế vị để tự thay tên người hưởng trong một di chúc vẫn có hiệu lực cho A.',
 'Giải quyết hiệu lực phần di chúc trước, rồi mới xét thế vị trong chia theo pháp luật.')
add('3.5;extension','application',['DS:645:2','DS:615:1'],
 'Di sản tổng cộng 500 triệu, nghĩa vụ tài sản đã xác định 600 triệu. Di chúc dành 100 triệu để thờ cúng, phần còn lại cho con; không có thỏa thuận chủ nợ miễn nợ. Con đề nghị giữ nguyên 100 triệu thờ cúng rồi chỉ dùng 400 triệu trả nợ. Xử lý đúng là gì?',
 'Không được dành riêng phần thờ cúng vì toàn bộ di sản không đủ thanh toán nghĩa vụ tài sản',
 ['Luôn giữ phần thờ cúng trước mọi khoản nợ vì đó là ý chí trong di chúc','Giữ được khoản thờ cúng nếu người quản lý cam kết không bán, dù di sản không đủ trả nghĩa vụ','Phải lấy 100 triệu tài sản riêng của con trả bù để giữ phần thờ cúng, dù không ai cam kết'],
 'Khoản 2 Điều 645 không cho dành một phần di sản dùng vào thờ cúng khi toàn bộ di sản không đủ thanh toán nghĩa vụ tài sản. Ý chí thờ cúng không vượt điều kiện này. Điều 615 không tự buộc con lấy tài sản riêng trả vượt di sản khi không thỏa thuận khác. Câu đã xác định nghĩa vụ và tổng giá trị, không tranh luận về chứng minh nợ.',
 'Kiểm tra khả năng thanh toán nghĩa vụ trước khi tách phần thờ cúng.')
add('3.5;extension','advanced',['DS:646:3'],
 'Di sản tổng cộng 300 triệu: di chúc ghi rõ di tặng bạn 100 triệu, 200 triệu còn lại cho người thừa kế. Nghĩa vụ tài sản của người lập di chúc là 350 triệu, không có khoản ưu tiên khác hoặc thỏa thuận miễn nợ. Sau khi dùng 200 triệu ngoài phần di tặng vẫn thiếu 150 triệu. Người được di tặng đòi giữ nguyên 100 triệu vì “di tặng không phải trả nợ”. Nhận định nào đúng?',
 'Phần di tặng 100 triệu cũng được dùng thực hiện nghĩa vụ còn lại; không bảo toàn khoản này',
 ['Di tặng luôn miễn tuyệt đối nên chủ nợ chỉ nhận 200 triệu','Người được di tặng bắt buộc dùng tài sản riêng trả toàn bộ 350 triệu','Chỉ được dùng phần di tặng trả nợ nếu di chúc ghi rõ đồng ý cho chủ nợ dùng khoản này'],
 'Khoản 3 Điều 646 cho người được di tặng không thực hiện nghĩa vụ với phần di tặng, nhưng có ngoại lệ khi toàn bộ di sản không đủ thanh toán nghĩa vụ: dùng phần di tặng thực hiện phần còn lại. Tổng 300 triệu không đủ trả 350 triệu nên phần di tặng 100 triệu cũng được sử dụng sau 200 triệu, vẫn còn thiếu 50 triệu. Không mở rộng thành trách nhiệm toàn bộ bằng tài sản riêng và không dùng khẩu hiệu miễn nợ để bỏ ngoại lệ.',
 'Đọc ngoại lệ của quy tắc di tặng không phải thực hiện nghĩa vụ.')
add('2.6;7.5;extension','application',['DS:661','HN:66:3'],
 'Chia di sản nhà ở sẽ ảnh hưởng nghiêm trọng đời sống của người vợ còn sống và gia đình; các người thừa kế không thống nhất trì hoãn. Người vợ muốn vẫn xác định phần từng người nhưng chưa chia một thời gian. Hướng yêu cầu phù hợp pháp luật là gì?',
 'Yêu cầu Tòa án xác định phần di sản được hưởng nhưng chưa cho chia trong thời hạn luật định',
 ['Vợ tự tuyên bố hoãn vô thời hạn vì đang ở trong nhà, không cần thỏa thuận hoặc Tòa án','Yêu cầu CCV tước tư cách thừa kế của các con để bảo đảm nơi ở cho vợ','Chỉ có thể trì hoãn nếu vợ trở thành chủ sở hữu toàn bộ nhà và xóa phần mọi người khác'],
 'Điều 661 cho bên vợ/chồng còn sống yêu cầu Tòa án xác định phần mà người thừa kế hưởng nhưng chưa chia nếu chia ảnh hưởng nghiêm trọng đời sống. Điều 66 khoản 3 Luật HNGĐ dẫn cơ chế hạn chế này. Không đồng nhất chưa chia với tước quyền hưởng hoặc quyền tự hoãn vô thời hạn; thời hạn và việc gia hạn vẫn theo điều kiện luật định.',
 'Tách xác định phần quyền với thời điểm được chia hiện vật.')
add('2.1;extension','understanding',['DS:654'],
 'Thuận không nhận con riêng của vợ làm con nuôi. Hồ sơ đã chứng minh Thuận và người con riêng chăm sóc, nuôi dưỡng nhau như cha con; Thuận chết không di chúc. Một người phản đối chỉ vì chưa đăng ký nhận con nuôi. Chỉ xét tư cách trong quan hệ này, kết luận nào đúng?',
 'Không thể loại tư cách thừa kế chỉ vì không có đăng ký con nuôi; phải áp quan hệ chăm sóc, nuôi dưỡng như cha con theo Điều 654',
 ['Con riêng chỉ có quyền thừa kế bố dượng sau khi hoàn tất đăng ký con nuôi','Chỉ cần là con riêng của vợ thì đương nhiên hưởng, không cần quan hệ chăm sóc','Không có di chúc thì con riêng tuyệt đối không được thừa kế bố dượng'],
 'Điều 654 đặt căn cứ quan hệ chăm sóc, nuôi dưỡng nhau như cha con, mẹ con, không đồng nhất với việc phải đăng ký nhận con nuôi. Dữ kiện đã chứng minh điều kiện này nên không bác chỉ vì thiếu quan hệ nuôi con nuôi. Ngược lại, việc đơn thuần là con riêng của vợ mà không có điều kiện chăm sóc nêu trong luật cũng không tự đủ.',
 'Phân biệt con nuôi với con riêng có quan hệ chăm sóc theo Điều 654.')
add('3.1','application',['CC:59:1','DS:659:2'],
 'Hân và Hoài là hai người thừa kế theo di chúc hợp pháp, ghi rõ Hân nhận tiền, Hoài nhận nhà. Họ yêu cầu công chứng văn bản phân chia đúng nội dung đó trong tháng 10/2026, các điều kiện khác đều đáp ứng. CCV bác vì “di chúc đã xác định rõ phần từng người thì không được yêu cầu loại văn bản này”. Đánh giá nào đúng?',
 'Không được bác chỉ vì phần hưởng đã rõ; khoản 1 Điều 59 hiện hành cho người thừa kế theo di chúc yêu cầu công chứng văn bản phân chia',
 ['Phải bác vì luật hiện hành chỉ cho thỏa thuận khi di chúc không ghi rõ phần','Phải sửa di chúc thành không ghi phần trước khi yêu cầu công chứng','Phải bỏ di chúc và chia theo pháp luật để có thể lập văn bản phân chia'],
 'Khoản 1 Điều 59 Luật Công chứng 2024 không còn đặt giới hạn yêu cầu của người hưởng theo di chúc vào trường hợp di chúc không xác định rõ phần từng người như cách viện dẫn luật cũ. CCV vẫn kiểm tra phân chia đúng BLDS, ở đây đúng ý chí định đoạt hiện vật theo Điều 659. Không suy ra các bên được tùy tiện bỏ mọi quyền bắt buộc hoặc điều kiện hồ sơ.',
 'Kiểm tra điều luật công chứng đang áp dụng, không giữ nguyên giới hạn của luật cũ.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('2.4;5.6;8.3','advanced',['CC:59:4','ND:44:6'],
 'Tổ chức đã nhận xác nhận hoàn thành niêm yết, chưa ký văn bản phân chia. Ngay trước lúc ký, Phương khiếu nại kèm tài liệu về việc mình là con của người chết bị bỏ sót. Các người đang xin công chứng muốn ký ngay vì hết thời gian niêm yết. Xử lý phù hợp là gì?',
 'Tạm dừng việc công chứng để xử lý thông tin khiếu nại; không ký chỉ dựa vào xác nhận niêm yết đã có',
 ['Ký ngay vì sau ngày kết thúc niêm yết mọi khiếu nại tự mất giá trị','Ký rồi yêu cầu Phương nhận tiền từ một người thừa kế, không cần làm rõ','Bỏ tài liệu của Phương vì Phương chưa có tên trên bản niêm yết'],
 'Khoản 4 Điều 59 chỉ cho công chứng sau xác nhận hoàn thành niêm yết và không nhận khiếu nại, tố cáo liên quan. Khoản 6 Điều 44 NĐ104 dự liệu khiếu nại sau xác nhận nhưng trước công chứng: phải tạm dừng để xử lý thông tin. Xác nhận thủ tục không chứng minh danh sách tuyệt đối đúng; CCV không thay Tòa án phán quyết ngay khi quyền còn tranh chấp.',
 'Xác định khiếu nại đến trước hay sau thời điểm công chứng, không chỉ ngày hết niêm yết.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('1.6;5.5','advanced',['CC:59:2:a','CC:59:2:b','CC:59:3'],
 'Để bỏ cha của người chết khỏi danh sách, nhóm yêu cầu chỉ nộp lý lịch tự khai ghi người cha “đã chết”, chưa có giấy chứng tử hoặc giấy tờ khác theo pháp luật chứng minh việc chết, cũng chưa xác định được chết trước hay sau. CCV chưa khai thác được dữ liệu xác thực. Họ đề nghị dùng cam đoan không bỏ sót thay mọi xác minh. Hướng xử lý đúng là gì?',
 'Yêu cầu làm rõ hoặc xác minh chứng cứ và thứ tự chết; cam đoan không thay kiểm tra tư cách người hưởng và chuỗi thừa kế',
 ['Chấp nhận ngay vì cam đoan của tất cả người có tên trong hồ sơ đủ loại mọi người khác','Bỏ người cha dù chưa biết thứ tự chết vì tại ngày làm hồ sơ người cha đã chết','Chỉ cần chứng minh người cha không có tên trên giấy chứng nhận nhà là đủ loại khỏi thừa kế'],
 'Điều 59 yêu cầu chứng cứ việc chết, quan hệ thừa kế và CCV kiểm tra đúng người hưởng; nếu chưa rõ phải yêu cầu làm rõ hoặc xác minh. Thứ tự chết quyết định cha không hưởng vì chết trước hay đã có quyền rồi phát sinh lần thừa kế tiếp. Câu không khẳng định chỉ giấy chứng tử mới được dùng; luật cho giấy tờ khác theo pháp luật, nhưng dữ kiện chưa có căn cứ ấy. Cam đoan không thay trách nhiệm kiểm tra.',
 'Đối chiếu từng quan hệ và từng sự kiện chết, nhất là trước/sau.','Quy trình, thủ tục và nghiệp vụ công chứng')
add('2.5;8.2','advanced',['ND:44:2','ND:44:3'],
 'Người để lại di sản có nơi thường trú cuối cùng xác định tại xã A ở Việt Nam, có nhà tại xã B và tiền gửi ngân hàng tại xã C; ba xã khác nhau. Tổ chức đã tiếp nhận hồ sơ phân chia cả nhà và tiền, hỏi nơi niêm yết theo các khoản 2, 3 Điều 44 NĐ104. Chọn phương án đúng.',
 'Niêm yết tại trụ sở UBND xã A và xã B; vị trí chi nhánh ngân hàng ở C không tự tạo thêm nơi niêm yết',
 ['Chỉ niêm yết tại xã B vì có bất động sản thì thay nơi thường trú cuối cùng','Niêm yết tại cả A, B, C vì mọi nơi có tài sản đều bắt buộc như nhau','Chỉ niêm yết tại xã C vì ngân hàng giữ giấy tờ về di sản tiền gửi'],
 'Khoản 2 Điều 44 xác định nơi thường trú cuối cùng; khoản 3 thêm UBND cấp xã nơi có bất động sản khi di sản có bất động sản, kể cả cùng động sản. Vì vậy cần A và B. Quy định không tự yêu cầu thêm xã đặt chi nhánh ngân hàng chỉ vì có tiền gửi; câu đã xác định thường trú và các xã khác nhau, không xét trường hợp không xác định nơi cư trú hoặc ở nước ngoài.',
 'Tách nơi cư trú cuối cùng, nơi có bất động sản và nơi ngân hàng giữ tiền.','Quy trình, thủ tục và nghiệp vụ công chứng')

def provision(spec):
 p=spec.split(':');cfg=CONFIG[p[0]];b={'document':cfg[0],'article':'Điều '+p[1],'url':cfg[3]}
 if len(p)>2:b['clause']='Khoản '+p[2]
 if len(p)>3:b['point']='Điểm '+p[3]
 t=(WORK/'legal'/cfg[2]).read_text();m=re.search(r'(?m)^[ \t]*Điều[ \t]+'+p[1]+r'[.,]',t);assert m,spec
 n=re.search(r'(?m)^[ \t]*Điều[ \t]+\d+[.,]',t[m.end():]);excerpt=t[m.start():m.end()+n.start() if n else len(t)].strip();assert len(excerpt)>100
 return b,{'reference':b,'sourceId':cfg[1],'evidenceExcerpt':excerpt}
bank=[];proof=[]
for i,r in enumerate(ROWS,1):
 pairs=[provision(s) for s in r['refs']];ans=[r['key']]+r['wrong'];assert len(set(ans))==4
 random.Random(2610060+i).shuffle(ans)
 q={'id':f'INH26-{i:03d}','part':2,'topic':r['topic'],'type':'single','status':'active','difficulty':r['difficulty'],'questionForm':'workflow' if r['difficulty']=='advanced' else 'short_case','question':{'variants':['Tháng 10/2026: '+r['stem']]},'answers':[{'id':chr(65+j),'text':a,'correct':a==r['key']} for j,a in enumerate(ans)],'explanation':'Gợi ý làm bài: '+r['hint']+'\n\n'+r['reason'],'legalBasis':[b for b,e in pairs],'lastVerified':DATE,'source':{'type':'user-provided','id':SOURCE,'questionNumber':r['origin'],'supportingSourceIds':list(dict.fromkeys(e['sourceId'] for b,e in pairs))}}
 bank.append(q);proof.append({'id':q['id'],'provisions':[e for b,e in pairs]})
assert len(bank)==32
def write(p,obj):(ROOT/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('data/imported-inheritance-2026.json',bank)
docs=[{'sourceId':c[1],'url':c[3],'pdfSha256':[{'file':f,'sha256':hashlib.sha256((WORK/'legal'/f).read_bytes()).hexdigest()} for f in c[4]]} for c in CONFIG.values()]
effect=[{'document':'BLDS 91/2015/QH13','status':'Còn hiệu lực; kiểm tra CSDL Bộ Tư pháp, phần thừa kế dùng các Điều 611–662.','url':'https://vbpl.moj.gov.vn/botuphap/Pages/vbpq-thuoctinh.aspx?ItemID=95942'}, {'document':'NĐ104/2025/NĐ-CP','status':'Hết hiệu lực một phần: Điều 64 bị bãi bỏ từ 01/11/2025 bởi điểm c khoản 2 Điều 3 NĐ280/2025. Điều 44 sử dụng trong bộ này không thuộc phần bãi bỏ.','url':'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/753-vbhn-btp.pdf'}, {'document':'Luật Công chứng','status':'Dùng Luật 46/2024 áp dụng tháng 10/2026; không đưa sửa đổi 04/2026 có hiệu lực 01/01/2027 hoặc dự thảo nghị định tháng 9/2026 vào đáp án hiện hành.','url':'https://chinhphu.vn/?classid=1&docid=218099&pageid=27160&typegroupid=3'}, {'document':'NĐ29/2015/NĐ-CP','status':'Đã được thay thế bởi NĐ104/2025 từ 01/07/2025, khoản 2 Điều 65; không dùng làm căn cứ hiện hành.'}]
write('reports/inheritance-legal-evidence-2026.json',{'date':DATE,'scope':'Xác minh riêng 32 câu biên soạn, không chứng nhận mọi lời giải nguồn','documents':docs,'method':'Đối chiếu PDF chính thức và tình trạng hiệu lực; BLDS OCR kiểm tra ảnh trang in 152–165 và các điều liên quan, CC PDF có lớp chữ, NĐ104 Điều 44 OCR đối chiếu ảnh trang 32–33.','effectivityNotes':effect,'questions':proof})
doc=next((WORK/'upload').glob('*THU*docx'));sha=hashlib.sha256(doc.read_bytes()).hexdigest()
groups=[{'number':1,'title':'Hòa: di chúc, mẹ chết sau, con và hồ sơ','questions':6,'images':[]},{'number':2,'title':'Thuận: phân chia, niêm yết, nội dung thỏa thuận','questions':6,'images':[1,2]},{'number':3,'title':'Hân/Hoài: di chúc, phân chia, thỏa thuận và vàng','questions':6,'images':[]},{'number':5,'title':'Lân: xác định di sản, thế vị và bỏ sót','questions':6,'images':[3,4]},{'number':6,'title':'Vượng/Long: cử người quản lý di sản','questions':6,'images':[5,6]},{'number':7,'title':'Kiểm tra lần hai: đạo đức, An/Bích và đại diện','questions':5,'ethics':2,'images':list(range(7,17))},{'number':8,'title':'Kiểm tra lần ba: nhiều lần thừa kế, thời hiệu, người ở nước ngoài','questions':6,'ethics':1,'draft':1,'images':list(range(17,25))}]
items=[]
for g in groups:
 origins=[str(g['number'])+'.'+str(n) for n in range(1,g['questions']+1)]+[str(g['number'])+'.ETHICS'+str(n) for n in range(1,g.get('ethics',0)+1)]+([str(g['number'])+'.DRAFT'] if g.get('draft') else [])
 for o in origins:
  ids=[q['id'] for q in bank if o in q['source']['questionNumber'].split(';')]
  items.append({'id':'INH-SRC-'+o,'sourceGroup':g['number'],'questionNumber':o,'decision':'adapted_partial' if ids else 'review','adaptedQuestionIds':ids,'originalAnswerCertified':False,'note':'Chỉ chứng nhận câu biên soạn liên kết, không chứng nhận toàn bộ các nhánh của câu lớn.'})
assert len(items)==45
issues=['Mẫu đưa người cha chết trước vào người hưởng phần bắt buộc; phải xét còn sống tại thời điểm mở thừa kế.','Mẹ chết sau con: quyền phát sinh rồi đi vào di sản mẹ, khác thế vị trực tiếp ở lần mở thừa kế của con.','Giới hạn chọn người quản lý trong số người thừa kế không có trong Điều 616.','Quyền đại diện quản lý không đồng nghĩa quyền tự định đoạt; phải phân biệt người được cử và người tiếp tục chiếm hữu.','Không tự coi mọi khoản phúng viếng là di sản; phải truy nguồn sở hữu, người nhận và mục đích.','Từ chối nhận di sản không tự chỉ định người thụ hưởng cụ thể như tặng cho/nhường phần.','Chia hiện vật và thanh toán chênh lệch không tự là giao dịch giả tạo chỉ vì có tiền thanh toán.','Luật Công chứng 2014 và NĐ29/2015 không dùng làm căn cứ hiện hành cho thủ tục tháng 10/2026.','Không tự coi chẩn đoán tâm thần là quyết định tuyên mất năng lực; tư cách hưởng khác cơ chế đại diện.','Mẫu nhầm Điều 66 BLDS thành Điều 660, nhầm tên, năm ly hôn, người để lại di chúc và số tiền bằng chữ.','Các kết luận cấm thỏa thuận lợi tức chung chỉ vì không phải vợ chồng, hoặc cấm mọi giao dịch trước giải chấp, quá rộng.','Nguồn đề 8 có lỗi câu năm xuất cảnh/mất, áp dụng thời hiệu lịch sử; không áp máy móc đáp án tại kỳ thi cũ cho tháng 10/2026.']
write('reports/inheritance-source-review.json',{'date':DATE,'sourceId':SOURCE,'sourceSha256':sha,'readScope':{'paragraphs':493,'tables':0,'embeddedImages':24,'method':'Đọc chữ, OCR tất cả ảnh, xem ảnh đề và bố cục lời giải; không công bố DOCX gốc.'},'sourceQuestionCount':45,'groups':groups,'duplicateSections':[{'section':'Ảnh 5–6 và phần chữ Đề 6','duplicateOf':'Đề quản lý di sản Vượng/Long','note':'Cùng 6 câu, không đếm hai lần.'}], 'numberingNote':'Tài liệu không có cụm Đề 4 riêng; giữ số nguồn 1,2,3,5,6,7,8. Đề 7 có 2 câu đạo đức ngoài 5 câu nghiệp vụ; Đề 8 có 1 mục đạo đức và 1 yêu cầu soạn thảo ngoài 6 câu nghiệp vụ.','questions':items,'activeAdded':32,'sourceIssues':issues,'unverifiedBranches':['Thời hiệu lịch sử mở thừa kế năm 1978/1987 và việc quản lý tài sản qua nhiều thời kỳ: giữ review, cần kiểm tra chuyển tiếp/án lệ và ngày chết chính xác.','Nhận nhà/đất của người định cư ở nước ngoài: không tự nhập đáp án Luật Nhà ở 2014, NĐ99/2015.','Quy định quản lý, mua bán và thanh toán bằng vàng SJC sau sửa đổi pháp luật về vàng: chưa biên soạn active từ nhánh nguồn này.','Nội dung hạn chế chuyển quyền vô thời hạn, hưởng lợi tức chung sau chia và cam kết một người thanh toán cho người mới chưa xác định: cần phân tích hiệu lực đối với người thứ ba.','Quy tắc đạo đức/biện pháp trách nhiệm ở phần ngoài chuyên đề thừa kế, các mẫu tự luận nguyên văn và các mức phí chưa được chứng nhận.']})
reg=json.loads((ROOT/'data/question-sources.json').read_text());reg['sources']=[s for s in reg['sources'] if s['id']!=SOURCE]+[{'id':SOURCE,'type':'user-provided','title':'Đề thi và bài giải thừa kế do Madam An cung cấp','sha256':sha,'use':'Nguồn chủ đề 7 cụm đề, 45 yêu cầu lớn gồm phần đạo đức/soạn thảo; chỉ 32 câu biên soạn có chứng cứ riêng được active.'}]
if not any(s['id']=='OFFICIAL-ND10425' for s in reg['sources']):reg['sources'].append({'id':'OFFICIAL-ND10425','type':'official','title':CONFIG['ND'][0],'url':CONFIG['ND'][3],'use':'Điều 44 về niêm yết; Điều 64 đã bị bãi bỏ, không sử dụng phần này.'})
write('data/question-sources.json',reg)
lines=['# Đề luyện thừa kế và nghiệp vụ công chứng','','32 câu, một đáp án đúng mỗi câu; thời gian gợi ý 60 phút. Pháp luật áp dụng tháng 10/2026. Đề luyện được biên soạn độc lập từ các chủ đề tài liệu, không phải đề thi chính thức.','','## Câu hỏi','']
for i,q in enumerate(bank,1):lines+=['### Câu '+str(i),'',q['question']['variants'][0],'']+[a['id']+'. '+a['text'] for a in q['answers']]+['']
lines+=['## Đáp án và bài giải','','| Câu | Đáp án |','|---|---|']+[f'| {i} | '+next(a['id'] for a in q['answers'] if a['correct'])+' |' for i,q in enumerate(bank,1)]+['']
for i,q in enumerate(bank,1):lines+=['### Giải câu '+str(i),'',q['explanation'],'','Căn cứ: '+'; '.join(b['document']+', '+b['article']+(', '+b['clause'] if 'clause' in b else '')+(', '+b['point'] if 'point' in b else '')+' ([nguồn]('+b['url']+'))' for b in q['legalBasis'])+'.','']
lines+=['## Báo cáo nghiên cứu và phạm vi','','Đọc 493 đoạn và 24 ảnh. Có 7 cụm đề khác nhau, 45 yêu cầu lớn kể cả đạo đức và soạn thảo. Bản ảnh và bản chữ Đề 6 là cùng một đề; không có Đề 4 riêng. Chỉ chứng nhận đáp án các câu mới liên kết, không chứng nhận mọi kết luận của tài liệu gốc. DOCX gốc không được đưa lên repo.','','### Các lỗi/nhận định nguồn đã xử lý','']+['- '+s for s in issues]+['','### Các nhánh còn review','']+['- '+s for s in json.loads((ROOT/'reports/inheritance-source-review.json').read_text())['unverifiedBranches']]+['','### Số lượng và ma trận','','Đợt này: 32 câu mới biên soạn; 0 câu cũ bị xóa, 0 câu cũ đổi đáp án. Phân bố độ khó (ước lượng biên tập): '+str(dict(collections.Counter(q['difficulty'] for q in bank)))+'. Chủ đề: '+str(dict(collections.Counter(q['topic'] for q in bank)))+'.','','Trước: 910 câu lưu trữ, 368 active. Sau: 942 câu lưu trữ, 400 active, 36 review, 506 archived. App tải 442 bản ghi trong 8 file; 42 bản ghi không đủ điều kiện không vào ôn tập/thi thử. Giữ nguyên ID cũ, khóa và cấu trúc lưu tiến trình/lịch sử. 500 EXP cơ học vẫn archived.','','400 active là số lượng đạt sau đợt này, không đồng nghĩa ma trận toàn ngân hàng đã đạt mọi tỷ lệ hay toàn bộ 45 yêu cầu nguồn được kiểm định. Báo cáo audit kèm theo cung cấp phân bố thực tế; còn cần cân đối toàn ngân hàng. Không bù số bằng paraphrase.','','Rà trùng: không nhập lại câu thuần tư cách thai nhi VER26-062, trần trách nhiệm VER26-063, chết cùng thời điểm VER26-064, thời điểm từ chối VER26-065, ngoại lệ Điều 621 VER26-067, di chúc không công chứng VER26-070, hiệu lực từng phần VER26-072, tính 2/3 một suất đơn VER26-073, tính thế vị đơn VER26-077 và một người thừa kế vẫn niêm yết VER26-079. Câu mới khai thác nhánh kế tiếp, hồ sơ, các chế độ chia khác nhau, xung đột đại diện và mốc định giá.','']
all_questions=[]
for f in [ROOT/'data/questions.json',ROOT/'data/derived-questions.json',*sorted((ROOT/'data').glob('validated-*.json')),*sorted((ROOT/'data').glob('imported-*.json'))]:all_questions+=json.loads(f.read_text())
active=[q for q in all_questions if q['status'] in ['active','verified']]
counts=collections.Counter(q['difficulty'] for q in active)
lines+=['### Phân bố độ khó toàn bộ active (nhãn biên tập, chưa hiệu chuẩn bằng kết quả làm bài)','','| Mức | Số câu | Tỷ lệ | Mục tiêu |','|---|---:|---:|---:|']
for key,label,target in [('recognition','Nhận biết',20),('understanding','Hiểu luật',30),('application','Vận dụng',30),('advanced','Vận dụng cao',20)]:lines.append(f'| {label} | {counts[key]} | {100*counts[key]/len(active):.1f}% | {target}% |')
lines+=['','Ngân hàng còn lệch về nhãn vận dụng, thiếu hiểu luật và vận dụng cao so với ma trận; không dùng con số 400 thay cho kết luận đã cân bằng. Nhãn độ khó cần tiếp tục được hiệu chuẩn. Phân bố topic nguyên bản của toàn ngân hàng nằm trong bank-audit-inheritance-after.json; taxonomy cũ có nhiều cách ghi cùng một nhóm nên không giả coi từng nhãn là một nhóm ma trận độc lập.','','### Phân bố 32 câu chuyên đề','','| Chủ đề | Số câu |','|---|---:|']+[f'| {t} | {n} |' for t,n in collections.Counter(q['topic'] for q in bank).items()]+['','### Kiểm tra tích hợp','','37/37 kiểm thử tự động đạt: JSON, ID/đáp án duy nhất, nguồn/căn cứ, loader 8 file, chấm 32/32 chuyên đề, phản hồi đáp án sai, hai chế độ, timer, mã đề chia sẻ và hàng đợi kết quả cũ. Audit không có cặp trùng/gần trùng hoặc cờ dữ liệu liên quan INH26. Cờ heuristic của 500 EXP archived không phải lỗi của bộ mới. Kiểm chứng bản triển khai thực tế được ghi riêng sau deploy.','']
(ROOT/'reports/inheritance-exam-2026-10-06.md').write_text('\n'.join(lines))
print(json.dumps({'added':len(bank),'difficulty':dict(collections.Counter(q['difficulty'] for q in bank)),'sourceItems':len(items)},ensure_ascii=False))
