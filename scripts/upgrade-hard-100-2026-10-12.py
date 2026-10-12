import json,copy,hashlib,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=['calibration-20-2026.json','calibration-40-2026.json','calibration-next-40-2026.json']
banks={f:json.loads(subprocess.check_output(['git','show','18a5deaa69096772ae5318b7d8162e740a9f19ed:data/'+f],cwd=ROOT)) for f in FILES}
old={q['id']:copy.deepcopy(q) for qs in banks.values() for q in qs}
qs={q['id']:q for arr in banks.values() for q in arr};changes={}
def r(n,stem,bad,reason,good=None,refs=()):
 q=qs[f'CAL26-{n:03}'];false=[a for a in q['answers'] if not a['correct']];true=[a for a in q['answers'] if a['correct']]
 assert len(bad)==len(false),(n,len(bad),len(false))
 for a,(text,explanation) in zip(false,bad):a.update(text=text,explanation=explanation)
 if good is not None:
  assert len(good)==len(true),(n,'good')
  for a,(text,explanation) in zip(true,good):a.update(text=text,explanation=explanation)
 q['question']['variants']=[stem];q['difficulty']='advanced';q['explanation']=reason;q['difficultyRationale']=reason
 q['empiricallyCalibrated']=False;q['reviewStatus']='HARD_SCENARIO_REVIEWED_ESTIMATED';q['lastVerified']='2026-10-12'
 for document,article,url in refs:q['legalBasis'].append(dict(document=document,article=article,url=url))
 q.setdefault('audit',{}).update(difficultyReview='hard_scenario_estimated_pending_trial',previousEvidenceFile=q.get('audit',{}).get('evidenceFile'),evidenceFile='reports/difficulty-upgrade-100-legal-review-2026-10-12.json',difficultyUpgradeReport='reports/difficulty-upgrade-100-2026-10-12.json')
 changes[n]=reason
CC='Luật Công chứng số 46/2024/QH15 đối chiếu VBHN 50/VBHN-VPQH ngày 17/03/2026'
CCURL='https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/3/50-vbhn-vpqh.pdf'
DS='Bộ luật Dân sự số 91/2015/QH13';DSURL='https://vanban.chinhphu.vn/?docid=183188&pageid=27160'
r(1,'Hồ sơ bán nhà đứng tên cha vợ của công chứng viên N; người ký bán là đại diện không có quan hệ với N. N dự định chỉ kiểm tra hồ sơ rồi ký lời chứng, còn đồng nghiệp M không có quan hệ thân thích sẽ tiếp khách. Các bên đề nghị làm vậy để khỏi đổi lịch. Cách xử lý nào khắc phục đúng xung đột lợi ích?',[
 ('Để M tiếp khách, N ký lời chứng vì người ký bán không phải cha vợ N.','Đổi người tiếp khách không loại việc N trực tiếp công chứng giao dịch về tài sản người thân.'),
 ('Để N ký nếu đại diện và bên mua xác nhận không có tranh chấp về giá.','Đồng thuận về giá không tạo ngoại lệ với điều cấm về tài sản người thân.'),
 ('Chuyển hồ sơ sang tổ chức khác, vì quan hệ của N làm mọi công chứng viên cùng văn phòng đều bị cấm.','Điều cấm của N không tự áp cho M; M có thể trực tiếp thực hiện khi đủ điều kiện.')],
 'Phân biệt người ký giao dịch, người ký lời chứng và chủ thể có lợi ích; chọn biện pháp xử lý đúng phạm vi điều cấm.',
 [('N không trực tiếp công chứng; có thể để M trực tiếp thực hiện nếu M đủ điều kiện và không có xung đột.','Cha vợ vẫn là chủ sở hữu; đại diện không xóa xung đột. Quan hệ của N không tự cấm M.')])
r(2,'P lập di chúc công chứng cho con H căn nhà, rồi giao H một bản gốc để giữ. P vẫn sống và chưa thay đổi di chúc; không có hợp đồng tặng cho, mua bán hoặc giao quyền sở hữu khác. H dùng bản gốc yêu cầu đăng ký sang tên, viện dẫn văn bản công chứng đã có hiệu lực. Kết luận nào giải quyết đúng hai loại hiệu lực?',[
 ('H được yêu cầu sang tên từ ngày công chứng, còn việc P chết chỉ quyết định thời điểm nhận bàn giao.','Nhầm hiệu lực văn bản công chứng với hiệu lực định đoạt thừa kế của di chúc.'),
 ('H được sang tên từ ngày nhận bản gốc nếu P chưa lập văn bản hủy di chúc.','Việc giữ bản gốc không làm thừa kế mở khi P còn sống.'),
 ('H được sang tên sau khi xác nhận chấp nhận di sản bằng văn bản, dù P còn sống.','Chấp nhận không tạo thời điểm mở thừa kế hoặc giao dịch chuyển quyền khác.')],
 'Tách hiệu lực chứng nhận với thời điểm phát sinh thừa kế; không suy sang tên từ việc nắm bản gốc.',
 [('Chưa có hiệu lực thừa kế để H sang tên bằng di chúc; hiệu lực định đoạt thừa kế bắt đầu khi mở thừa kế.','P còn sống; không có giao dịch chuyển quyền khác. Chứng nhận hợp pháp không làm mở thừa kế trước hạn.')])
r(3,'Văn phòng tại X nhận ba hồ sơ về đất tại Y: di chúc định đoạt đất; ủy quyền người khác bán đất; hợp đồng tặng cho đất có hiệu lực giữa các bên trước khi đăng ký. Các bên đều cư trú tại X. Nếu chỉ kiểm tra địa hạt công chứng, kết luận nào đúng?',[
 ('Hợp đồng tặng cho thuộc ngoại lệ vì các bên cùng cư trú tại X và chưa đăng ký chuyển quyền.','Ngoại lệ không căn cứ nơi cư trú hoặc thời điểm đăng ký; tặng cho không thuộc danh sách này.'),
 ('Có thể nhận cả ba hồ sơ vì ủy quyền và tặng cho đều chưa trực tiếp làm thay đổi đăng ký đất.','Phải phân loại văn bản theo ngoại lệ luật định, không theo hệ quả đăng ký tại thời điểm ký.')],
 'Phân biệt quyền định đoạt trực tiếp, đại diện thực hiện quyền và định đoạt sau chết; loại dữ kiện nơi cư trú, đăng ký không quyết định địa hạt.')
r(4,'A đang điều trị nội trú nhưng đi lại được trong bệnh viện; muốn công chứng hợp đồng bán tài sản tại giường bệnh. B khỏe mạnh, đã đặt xe nhưng bận lịch họp nên muốn công chứng cùng hợp đồng tại nhà. B không thuộc lý do chính đáng khác được Chính phủ quy định. Hai hồ sơ đủ điều kiện khác. Những kết luận nào đúng?',[
 ('Cả A và B đều được công chứng ngoài trụ sở nếu cùng thanh toán chi phí đi lại đã thỏa thuận.','Chi phí đi lại không tạo căn cứ công chứng ngoài trụ sở.'),
 ('Chỉ tiếp nhận A ngoài trụ sở sau khi có chứng cứ A hoàn toàn không thể đi lại.','Điều trị nội trú là nhánh căn cứ riêng; không buộc cộng thêm không thể đi lại.')],
 'Phân biệt căn cứ sức khỏe độc lập với thuận tiện cá nhân và chi phí; không cộng điều kiện của hai nhánh luật.')
r(5,'Các bên ký điện tử hợp lệ lúc 09:05; tổ chức ký số lúc 09:10; công chứng viên ký số lúc 09:20; tệp được gửi cho khách lúc 09:30. Tệp này đủ điều kiện công chứng điện tử, không thiếu chữ ký bắt buộc nào khác. Chọn mốc bắt đầu hiệu lực văn bản, phân biệt hoàn tất chứng nhận với gửi nhận tệp.',[
 ('09:10, vì chữ ký số tổ chức hoàn tất trước là mốc đóng dấu điện tử.','Lúc 09:10 còn thiếu chữ ký số công chứng viên.'),
 ('09:05, vì từ đó ý chí các bên đã được xác nhận bằng chữ ký điện tử.','Hoàn tất ý chí các bên chưa đủ chữ ký chứng nhận của công chứng viên và tổ chức.'),
 ('09:30, vì trước khi nhận tệp khách chưa có khả năng sử dụng văn bản.','Gửi nhận tệp không phải điều kiện xác định hiệu lực tại Điều 64.')],
 'Xác định chữ ký bắt buộc hoàn tất sau cùng khi thứ tự tổ chức và công chứng viên bị đảo.',
 [('09:20, khi đã có đầy đủ chữ ký số của công chứng viên và tổ chức.','Không phụ thuộc bên nào ký trước; đến 09:20 mới đủ hai chữ ký chứng nhận.')])
r(6,'Giá tài sản 1 tỷ đồng. A đặt cọc 200 triệu để bảo đảm cả giao kết và bàn giao; sau khi ký hợp đồng A thanh toán thêm 300 triệu, nhưng hai bên giữ 200 triệu ở chế độ đặt cọc cho đến bàn giao. B từ chối bàn giao do lỗi mình. Chưa xét hoàn trả 300 triệu hay thiệt hại khác, không có thỏa thuận xử lý cọc riêng. Riêng cơ chế đặt cọc làm phát sinh số tiền B phải trả nào?',[
 ('200 triệu; khoản tương đương cọc không áp dụng vì đã ký hợp đồng và đã thanh toán một phần.','Cọc còn bảo đảm thực hiện theo thỏa thuận; ký hợp đồng không tự chấm dứt bảo đảm này.'),
 ('700 triệu; cộng 200 triệu cọc, 200 triệu tương đương và 300 triệu đã thanh toán.','Đề chỉ hỏi riêng cơ chế đặt cọc, không cộng khoản thanh toán có căn cứ xử lý khác.'),
 ('500 triệu; tính khoản tương đương theo toàn bộ tiền B đang nắm ngoài khoản cọc phải trả.','Khoản tương đương căn cứ giá trị cọc 200 triệu, không căn cứ khoản thanh toán hoặc tổng tiền đã giao.')],
 'Tách hai dòng tiền và phạm vi bảo đảm; không nhầm ký hợp đồng với chấm dứt chế độ cọc.')
r(7,'A công chứng ủy quyền B quản lý, cho thuê nhà; văn bản không cho bán nhà. A sau đó đồng ý bằng văn bản cho B ủy quyền lại C thực hiện đúng công việc. B dự định dùng giấy ủy quyền lại để C ký thuê và thêm quyền bán khi cần chi tiền sửa nhà. Những nhận định nào đúng?',[
 ('C được bán nhà trong phạm vi tiền cần sửa, vì đó là việc phụ trợ cho quyền quản lý được ủy quyền lại.','Mục đích sửa nhà không tự tạo quyền bán ngoài phạm vi ban đầu.')],
 'Kiểm tra riêng căn cứ ủy quyền lại, phạm vi việc được giao và hình thức; không suy quyền định đoạt từ việc quản lý.')
r(8,'Vợ có chứng cứ thừa kế riêng căn nhà, vợ chồng chưa nhập vào tài sản chung. Nhà là nơi ở duy nhất; người chồng đồng ý giá bán và dự định tự tìm chỗ ở sau. Hồ sơ chưa chứng minh việc bảo đảm chỗ ở cho vợ chồng. Nhận định nào xử lý đồng thời nguồn tài sản và điều kiện nơi ở duy nhất đúng?',[
 ('Nhà phải xác định lại là tài sản chung vì chồng cùng sử dụng và tham gia thỏa thuận giá.','Sử dụng chung và thỏa thuận giá không tự nhập tài sản thừa kế riêng vào khối chung.'),
 ('Nguồn tài sản riêng đã rõ nên có thể kết thúc kiểm tra việc bảo đảm chỗ ở.','Tài sản riêng không loại điều kiện bảo đảm chỗ ở đối với nhà duy nhất.'),
 ('Văn bản đồng ý giá của chồng thay được việc làm rõ bảo đảm chỗ ở sau chuyển nhượng.','Đồng ý giá và bảo đảm chỗ ở là hai vấn đề khác nhau; đề chưa chứng minh điều kiện chỗ ở.')],
 'Phân biệt sự đồng ý giá, nhập tài sản và bảo đảm chỗ ở; không dùng một dữ kiện thay cả ba điều kiện.')
r(9,'Di chúc của M cho bạn toàn bộ di sản. Khi M chết, N còn 17 tuổi, P 25 tuổi không có khả năng lao động, Q 28 tuổi có khả năng lao động. Vợ M từ chối nhận di sản bằng văn bản hợp lệ trước khi phân chia, không nhằm trốn nợ; cha mẹ M đã chết. N, P, Q đủ quyền hưởng và không từ chối. Chọn những người vẫn được bảo vệ về phần bắt buộc; không đồng nhất hàng thừa kế với nhóm bảo vệ.',[
 ('Q được phần bắt buộc bằng N vì thuộc cùng hàng thừa kế và không bị truất quyền hưởng.','Cùng hàng quyết định suất giả định, không tự làm con thành niên có khả năng lao động thuộc nhóm bắt buộc.'),
 ('Vợ được phần bắt buộc vì việc từ chối chỉ loại phần chia theo pháp luật, không loại quyền theo di chúc.','Từ chối hợp lệ thuộc ngoại lệ không áp dụng bảo vệ tại khoản 2 Điều 644.')],
 'Lọc tư cách theo tuổi, khả năng lao động và từ chối hợp lệ trước khi xét suất; tránh đồng nhất hàng thừa kế với phần bắt buộc.')
r(10,'A chấm dứt ủy quyền không thù lao với B, đã báo trước B hợp lý. Thư thông báo bằng văn bản cho C bị hoàn lại, C không nhận, không biết và không phải biết việc chấm dứt. Sau đó C ký với B trong phạm vi ủy quyền cũ; giao dịch đủ điều kiện khác. Nhận định nào đúng về giao dịch với C?',[
 ('Giao dịch không ràng buộc A từ ngày A đã gửi thư, dù thư chưa đến C.','Đề nêu C không biết, không phải biết; việc gửi thư không làm điều kiện bảo vệ người thứ ba biến mất.'),
 ('Giao dịch chỉ ràng buộc A nếu C chứng minh mình đã yêu cầu A xác nhận trước khi ký.','Luật không đặt nghĩa vụ xin xác nhận lại trong nhánh C không biết, không phải biết.'),
 ('Giao dịch chuyển thành nghĩa vụ riêng của B vì quan hệ ủy quyền A–B đã chấm dứt hợp lệ.','Chấm dứt nội bộ không tự loại quy tắc bảo vệ người thứ ba tại Điều 569.')],
 'Tách chấm dứt nội bộ, gửi thông báo và nhận thức của đối tác; không coi chứng từ gửi là đủ loại bảo vệ người thứ ba.')
r(11,'A đặt cọc 200 triệu. Hợp đồng quy định hợp pháp nếu B từ chối giao kết do lỗi B thì hoàn cọc và trả thêm 100 triệu, thay mức trả thêm mặc định. B vi phạm đúng trường hợp; A đã nhận lại 50 triệu như một phần thực hiện nghĩa vụ xử lý cọc. Chọn tổng nghĩa vụ xử lý cọc phát sinh trước khi trừ khoản đã trả, không tính thiệt hại khác.',[
 ('250 triệu, vì phải trừ 50 triệu đã trả rồi mới xác định tổng nghĩa vụ phát sinh.','250 triệu là số còn phải trả, không phải tổng nghĩa vụ đề đang hỏi.'),
 ('450 triệu, vì cọc 200 triệu, khoản tương đương 200 triệu và khoản 100 triệu được cộng rồi trừ 50 triệu.','Không cộng khoản mặc định với khoản thay thế; đề cũng không hỏi số còn phải trả.'),
 ('400 triệu, vì mức trả thêm theo thỏa thuận không được dùng khi lỗi thuộc bên nhận cọc.','Điều 328 cho phép thỏa thuận khác; dữ kiện xác nhận thỏa thuận hợp pháp.')],
 'Phân biệt tổng nghĩa vụ và số dư còn trả; kiểm tra điều khoản thay thế chế tài mặc định.')
r(12,'Thừa kế mở ngày 12/10/2017. Đến 12/10/2026, ba yêu cầu độc lập được nêu: chia di sản nhà ở; xác nhận quyền thừa kế; buộc người thừa kế thực hiện nghĩa vụ tài sản của người chết. Không có thời gian loại trừ, bắt đầu lại hay quy định chuyển tiếp khác. Chọn bộ thời hiệu theo thứ tự để kiểm tra yêu cầu, chưa xét việc Tòa án áp dụng thời hiệu.',[
 ('30 năm; 30 năm; 3 năm — cả hai yêu cầu đầu cùng liên quan nhà nên cùng thời hiệu.','Thời hiệu xác nhận quyền không chuyển thành 30 năm vì di sản là bất động sản.'),
 ('10 năm; 10 năm; 3 năm — chia nhà và xác nhận quyền thừa kế đều dùng thời hiệu 10 năm.','Chia di sản bất động sản có thời hiệu 30 năm.'),
 ('30 năm; 3 năm; 10 năm — yêu cầu xác nhận và yêu cầu trả nghĩa vụ dùng mốc đảo nhau.','Điều 623 quy định xác nhận 10 năm, thực hiện nghĩa vụ 3 năm.')],
 'Phân loại mục đích rồi đối chiếu chín năm đã trôi qua; không dùng loại tài sản cho mọi yêu cầu thừa kế.',
 [('30 năm; 10 năm; 3 năm. Tại mốc đã nêu, hai yêu cầu đầu còn trong thời hiệu, yêu cầu thực hiện nghĩa vụ đã quá ba năm.','Từ 12/10/2017 đến 12/10/2026 là chín năm; ba loại yêu cầu có thời hiệu khác nhau, chưa xét việc Tòa áp dụng.')])
r(13,'Giới hạn ủy quyền mua máy của A cho B là 800 triệu. B ký giá 900 triệu, bên bán biết giới hạn; A sau đó đọc đầy đủ hợp đồng và ký văn bản chấp thuận toàn bộ giá 900 triệu, không đặt điều kiện. Hợp đồng không có lỗi hình thức, nội dung. Cách xác định nghĩa vụ nào đúng?',[
 ('A chịu 800 triệu, B chịu 100 triệu vì bên bán biết giới hạn nên việc A chấp thuận sau không khắc phục được.','Sự đồng ý là ngoại lệ riêng tại Điều 143, không bị loại chỉ vì đối tác biết giới hạn.'),
 ('A chỉ chịu 100 triệu vượt phạm vi vì văn bản sau chỉ có tác dụng xác nhận phần vượt.','Đề xác nhận A đồng ý toàn bộ; không tách phần hợp đồng hợp lệ thành nghĩa vụ không ràng buộc.'),
 ('Phải ký lại ủy quyền nâng mức trước khi có thể công nhận hợp đồng với bên bán.','Điều 143 cho ràng buộc bằng sự đồng ý, không bắt buộc hồi tố một ủy quyền mới.')],
 'Áp dụng ngoại lệ đồng ý sau giao dịch; phân biệt giới hạn ủy quyền với phạm vi nghĩa vụ đã được chấp thuận.')
r(14,'X và Y ủy quyền K ký một hợp đồng mua bán giữa hai pháp nhân. Mỗi ủy quyền đủ phạm vi và còn hạn; cả hai cơ quan quản lý đã duyệt giá. Không có quy định pháp luật riêng cho phép K ký hai phía. Đề xuất thay người phía Y nhưng giữ K phía X được đưa ra. Những nhận định nào đúng?',[
 ('Duyệt giá của cả hai pháp nhân đã loại xung đột nên K có thể ký hai phía theo hai ủy quyền riêng.','Đủ phạm vi và đồng thuận giá không thay ngoại lệ pháp luật cho việc đại diện hai bên cùng giao dịch.')],
 'Tách hợp lệ của từng ủy quyền và điều cấm ở cùng giao dịch; đánh giá biện pháp thay người thay vì phủ nhận mọi đại diện nhiều chủ thể.')
r(15,'Tài sản chung M–N trị giá 6 tỷ, không có tài sản riêng hoặc nghĩa vụ cần trừ; không có thỏa thuận chia khác. M chết, cha mẹ đã chết. Ba con là P 17 tuổi, Q thành niên có khả năng lao động, R thành niên không có khả năng lao động; N và các con không từ chối, không mất quyền hưởng. Di chúc cho bạn H toàn bộ phần M. Chọn các kết luận đúng sau khi tách khối tài sản và bảo vệ người bắt buộc.',[
 ('N, P, R mỗi người 1 tỷ và H không còn phần, vì lấy hai phần ba suất từ toàn bộ khối 6 tỷ.','Khối di sản chỉ 3 tỷ sau tách phần N; lấy khối chung làm di sản khiến tính phần bắt buộc gấp đôi.')],
 'Ba bước: tách tài sản chung, đếm suất giả định gồm cả Q, rồi lọc người nhận phần bắt buộc.')
r(16,'Di sản ròng M là 900 triệu. M có vợ N, con Q thành niên có khả năng lao động; con P đã chết trước M, để lại con K thành niên có khả năng lao động. Cha mẹ đã chết, không có người hưởng khác; không ai từ chối hoặc mất quyền. Di chúc cho H toàn bộ. Hồ sơ yêu cầu xác định vừa suất giả định vừa phần thực nhận. Phương án nào đúng?',[
 ('N nhận 300 triệu, H 600 triệu; bỏ nhánh P vì P không còn sống nên suất giả định chỉ có N, Q.','Nhánh P được K thế vị khi xác định chia theo pháp luật; không bỏ khỏi số suất giả định.'),
 ('N và K mỗi người 200 triệu, H 500 triệu; thế vị tự làm K có phần bắt buộc giống con chưa thành niên.','K thành niên có khả năng lao động không tự được phần bắt buộc vì là người thế vị.'),
 ('N nhận 200 triệu, Q và K mỗi người 300 triệu, H 100 triệu; bảo vệ N rồi chia theo pháp luật phần còn lại.','Di chúc hợp pháp vẫn chi phối phần còn lại; không chuyển phần còn lại sang chia theo pháp luật.')],
 'Giữ nhánh thế vị trong suất giả định nhưng không biến người thế vị thành người hưởng bắt buộc; áp dụng di chúc cho phần còn lại.')
r(17,'Hợp đồng dịch vụ đã có phần thực hiện hợp lệ chưa thanh toán. B vi phạm nghiêm trọng, A có đủ căn cứ đơn phương chấm dứt. A gửi thông báo 10/10, B nhận 12/10; điều khoản phạt, bồi thường và giải quyết tranh chấp đã có. Không xét căn cứ hủy bỏ riêng. Những nhận định nào đúng về hiệu lực và quyết toán?',[
 ('Chấm dứt từ 12/10 nhưng buộc hoàn trả mọi lợi ích đã nhận từ ngày ký theo cơ chế vô hiệu hồi tố.','Thời điểm nhận đúng nhưng hệ quả hồi tố sai; phải phân biệt đơn phương chấm dứt với hủy bỏ, vô hiệu.')],
 'Một phương án có phần thời điểm đúng nhưng hệ quả sai; tách hiệu lực tương lai, công việc đã làm và điều khoản được giữ.')
r(18,'B nợ A gốc 1 tỷ, lãi 100 triệu, phạt 50 triệu. C bảo lãnh hợp pháp tối đa 600 triệu tiền gốc, không lãi, phạt. Nợ đến hạn; B không trả nhưng còn khả năng trả. Không thỏa thuận chỉ gọi bảo lãnh khi mất khả năng, không có bù trừ. A chưa kiện B. Yêu cầu nào đúng với C?',[
 ('750 triệu, vì phạm vi gốc được giới hạn nhưng lãi và phạt vẫn đi theo nghĩa vụ bảo lãnh.','Thỏa thuận đã loại lãi và phạt; không dùng phạm vi mặc định thay thỏa thuận.'),
 ('600 triệu gốc sau khi A có bản án buộc B trả mà B không thi hành.','Nhánh thông thường không buộc phải kiện hoặc có bản án trước khi gọi bảo lãnh.'),
 ('Chưa gọi bảo lãnh vì B vẫn có khả năng trả, dù đã vi phạm nghĩa vụ đến hạn.','Không có thỏa thuận giới hạn gọi bảo lãnh theo khả năng thực hiện; áp dụng vi phạm nghĩa vụ đến hạn.')],
 'Kết hợp giới hạn về khoản bảo lãnh và điều kiện gọi; không đưa điều kiện mất khả năng hoặc kiện trước vào nhánh thông thường.')
r(19,'A thế chấp xe cá nhân không phải hàng hóa luân chuyển cho B. Hợp đồng cho phép cho thuê theo quy định luật. A thông báo B về dự định thuê và dự định tặng xe, nhưng chưa thông báo người thuê C về thế chấp; B chưa trả lời việc tặng. Không có ngoại lệ luật khác. Chọn các kết luận đúng về việc còn phải hoàn tất.',[
 ('Văn bản thông báo B về cả hai giao dịch đủ thay chấp thuận tặng cho nếu B chưa phản đối trong ba ngày.','Không có căn cứ mặc định im lặng ba ngày là chấp thuận định đoạt tài sản thế chấp.')],
 'Phân biệt thông báo hai phía khi thuê với chấp thuận khi tặng; im lặng trước thông báo không tự đáp ứng điều kiện định đoạt.')
r(20,'M lập di chúc công chứng ngày 12/06/2026 trong tình trạng nguy hiểm tính mạng, còn minh mẫn; thiếu giấy tờ được ghi rõ trong văn bản theo thủ tục đặc biệt. M hồi phục trước 12/09; đến 12/10 vẫn không nộp đủ giấy tờ. Người hưởng đề nghị giữ nguyên vì di chúc chưa phát sinh thừa kế và mốc ba tháng phải tính từ hồi phục. Nhận định nào đúng về văn bản công chứng?',[
 ('Văn bản vẫn có hiệu lực đến ngày M chết; thiếu giấy tờ chỉ cần khắc phục khi phân chia di sản.','Nhầm thời điểm hiệu lực thừa kế với điều kiện riêng của văn bản công chứng đặc biệt.'),
 ('Văn bản vẫn có hiệu lực đến ba tháng sau ngày hồi phục vì mốc bổ sung bắt đầu từ hồi phục.','Mốc luật định tính từ lập di chúc, không từ hồi phục.'),
 ('Văn bản trở thành di chúc miệng và được giữ hiệu lực nếu còn hai người biết nội dung.','Không có cơ chế tự chuyển loại văn bản do không bổ sung giấy tờ.')],
 'Tách thời điểm lập, hồi phục và mở thừa kế; áp dụng đúng hệ quả của văn bản công chứng đặc biệt thay vì cơ chế di chúc miệng.')
r(21,'Giá bán 2 tỷ trong hợp đồng gốc đúng ý chí khi ký. Nay hai bên muốn giảm còn 1,8 tỷ; đồng thời phát hiện một lỗi đánh máy tên đường, đối chiếu hồ sơ xác định sửa tên đường không ảnh hưởng quyền, nghĩa vụ. Hai bên đề nghị sửa cả hai ở lề, rồi gửi thông báo sau. Cách phân loại nào đúng?',[
 ('Cả hai là lỗi kỹ thuật vì có hồ sơ và đồng thuận của người ký.','Đồng thuận không biến thay đổi nghĩa vụ giá thành lỗi kỹ thuật.'),
 ('Cả hai phải sửa hợp đồng vì văn bản đã được công chứng nên không còn cơ chế sửa lỗi kỹ thuật.','Luật vẫn cho sửa lỗi ghi chép không ảnh hưởng quyền, nghĩa vụ.'),
 ('Giá là lỗi kỹ thuật nếu chưa trả hết; tên đường phải sửa hợp đồng vì liên quan bất động sản.','Phân loại theo ảnh hưởng quyền, nghĩa vụ và việc ghi sai, không theo chưa trả hết hoặc nhãn bất động sản.')],
 'Phân loại đồng thời hai nội dung; tránh dùng cùng một thủ tục cho sửa ý chí và sửa ghi chép.',
 [('Giá mới phải xử lý sửa đổi hợp đồng; tên đường có thể sửa lỗi kỹ thuật theo điều kiện và thủ tục tương ứng.','Giá cũ không ghi sai và giá mới đổi nghĩa vụ; lỗi đường đã được xác nhận chỉ là ghi chép không ảnh hưởng quyền, nghĩa vụ.')])
r(22,'A gửi đề nghị mua bán cho B: nếu B im lặng ba ngày thì đồng ý. B đã đọc, hai bên chưa có thỏa thuận hoặc thói quen về im lặng. Khi hết ngày thứ ba, B trả lời chỉ đồng ý nếu giảm giá; A chưa trả lời. Chỉ xét B có chấp nhận toàn bộ đề nghị ban đầu hay chưa, phương án nào đúng?',[
 ('B đã chấp nhận lúc hết ba ngày; yêu cầu giảm giá là sửa hợp đồng đã giao kết.','Im lặng không thành chấp nhận trong dữ kiện; không hình thành hợp đồng bằng điều kiện A tự đặt.'),
 ('B đã chấp nhận khi trả lời giảm giá vì đã đồng ý với đối tượng và số lượng.','Chấp nhận đề nghị đòi hỏi toàn bộ nội dung, không bỏ điều kiện giá.'),
 ('B đã chấp nhận ngay lúc đọc tin; thời hạn ba ngày chỉ dùng để thanh toán.','Đọc đề nghị không phải trả lời chấp nhận; đề không quy định thời hạn thanh toán này.')],
 'Kiểm tra cả nhánh im lặng và nội dung phản hồi có điều kiện; không suy chấp nhận từ một phần nội dung.',
 [('Chưa có chấp nhận toàn bộ đề nghị ban đầu: im lặng không được thỏa thuận, phản hồi lại đặt điều kiện giá.','Điều 393 đòi trả lời chấp nhận toàn bộ; hai sự kiện đều chưa đáp ứng.')])
r(23,'Hợp đồng ủy quyền quản lý công việc thường xuyên được hai bên xác lập trước, rồi công chứng sau. Hợp đồng không có thời hạn; pháp luật không quy định thời hạn riêng. Công việc chưa kết thúc và không có căn cứ chấm dứt sớm. B viện dẫn ngày công chứng và việc chưa thu hồi bản gốc để cho rằng vẫn được đại diện sau thời hạn mặc định. Mốc và thời hạn nào đúng?',[
 ('Một năm từ ngày công chứng; thời gian từ khi hai bên xác lập đến công chứng không tính.','Điều 563 lấy ngày xác lập việc ủy quyền, không mặc định ngày công chứng sau đó.'),
 ('Một năm từ ngày nhận bản gốc; thời hạn chỉ chạy khi người nhận có văn bản để sử dụng.','Giao nhận bản gốc không phải mốc tại Điều 563.'),
 ('Đến khi thu hồi bản gốc; mặc định một năm chỉ áp dụng khi công việc được mô tả thành một giao dịch cụ thể.','Quy tắc Điều 563 không phụ thuộc việc thu hồi bản gốc trong dữ kiện này.')],
 'Chọn đúng mốc xác lập, loại mốc chứng nhận/giao nhận và không suy kéo dài từ việc còn bản gốc.')
r(24,'Di sản mở tám tháng trước, chưa phân chia. H được chỉ định hưởng theo di chúc, muốn từ chối bằng văn bản gửi các chủ thể luật định, không nhằm trốn nghĩa vụ của mình. Người quản lý cho rằng phải nhận trước rồi mới chuyển phần cho người khác vì đã quá sáu tháng. Hướng xử lý nào đúng về thời điểm từ chối?',[
 ('H chỉ còn quyền nhận rồi tặng cho vì hạn sáu tháng đã qua.','BLDS 2015 dùng mốc trước phân chia, không hạn sáu tháng như kết luận này.'),
 ('H phải từ chối trước khi được công bố di chúc, nên tám tháng sau mở thừa kế đã muộn.','Công bố di chúc không thay mốc trước phân chia tại Điều 620.'),
 ('H có thể từ chối cả sau khi đã phân chia xong nếu lập văn bản có công chứng.','Công chứng không khắc phục điều kiện từ chối trước phân chia.')],
 'Phân biệt từ chối, nhận rồi chuyển tài sản và giai đoạn công bố; dùng mốc thủ tục thực tế thay số tháng.')
r(25,'Có hai hồ sơ thiệt hại do lỗi nhân viên trực tiếp gây ra khi công chứng. Hồ sơ thứ nhất thuộc X đã sáp nhập vào Y, Y kế thừa quyền, nghĩa vụ. Hồ sơ thứ hai thuộc Z đã giải thể, không có tổ chức kế thừa thuộc nhánh sáp nhập. Hai người trực tiếp gây thiệt hại đều đã nghỉ việc. Nhận định nào xác định đúng chủ thể bồi thường và hoàn trả?',[
 ('Cả hai nhân viên tự bồi thường cho khách vì đều đã nghỉ việc trước khi khách yêu cầu.','Nghỉ việc không bỏ trách nhiệm tổ chức kế thừa trong trường hợp sáp nhập.'),
 ('Y bồi thường cả hai hồ sơ; mọi trường hợp tổ chức cũ không còn hoạt động đều chuyển nghĩa vụ sang tổ chức gần nhất.','Không có cơ chế tổ chức gần nhất nhận trách nhiệm của Z đã giải thể.'),
 ('Tổ chức kế thừa chỉ bồi thường nếu còn giữ người gây lỗi, còn hoàn trả chấm dứt khi người ấy nghỉ.','Điều 40 không đặt điều kiện người gây lỗi vẫn làm việc; nghỉ việc không xóa hoàn trả.')],
 'Đối chiếu hai cơ chế chấm dứt tổ chức và quan hệ hoàn trả, không dùng nghỉ việc làm điều kiện loại trách nhiệm.',
 [('Y bồi thường hồ sơ X và có quyền hoàn trả theo luật; người trực tiếp gây lỗi ở Z tự bồi thường, kể cả đã nghỉ.','Sáp nhập và giải thể có nhánh trách nhiệm khác nhau tại Điều 40.')])
r(26,'A không đọc được nhưng nghe, ký và nhận thức bình thường. W được mời làm chứng, có quyền đòi một khoản tiền phát sinh từ chính giao dịch dù không hưởng tài sản được chuyển. A không mời được người khác. Chỉ xét người làm chứng, không xét phiên dịch. Những nhận định nào đúng?',[
 ('W đủ điều kiện vì chỉ có quyền đòi tiền, không phải bên nhận tài sản trong giao dịch.','Quyền hoặc nghĩa vụ liên quan cũng loại tư cách, không chỉ nhận tài sản.'),
 ('Có thể để W ký xác nhận dựa trên bản ghi âm mà không trực tiếp chứng kiến nếu A đồng ý.','Người làm chứng phải trực tiếp chứng kiến; đồng thuận không bỏ điều kiện đó.')],
 'Kiểm tra căn cứ phải có chứng và lợi ích gián tiếp của người được mời; xử lý nhánh chỉ định khi không mời được.')
r(27,'A ký được nhưng đề nghị ký kèm điểm chỉ; B không ký được và cả hai ngón trỏ không dùng được, ngón giữa phải dùng được. Đây là văn bản giấy, không có ngoại lệ ký trước theo chữ ký mẫu. Những nhận định nào đúng về hai trường hợp?',[
 ('A phải ký đơn thuần, B phải chờ phục hồi một ngón trỏ; không được dùng ngón khác hoặc phối hợp ký, điểm chỉ.','Ký kèm điểm chỉ có thể theo đề nghị; khi không dùng hai ngón trỏ được phép ngón khác với thông tin lời chứng.')],
 'Đối chiếu hai nhánh ký kèm điểm chỉ và điểm chỉ thay ký; không cộng yêu cầu ngón trỏ thành điều cấm ngón khác.',
 [('B có thể dùng ngón giữa phải và lời chứng phải ghi rõ ngón, bàn tay.','Hai ngón trỏ không sử dụng được nên chuyển sang ngón khác theo khoản 3 Điều 50.'),
  ('Điểm chỉ thay ký áp dụng với B; A có thể ký kèm điểm chỉ theo đề nghị.','Khoản 3 và 4 Điều 50 điều chỉnh hai tình huống khác nhau.'),
  ('Việc ký trước sự chứng kiến của công chứng viên phải được chụp ảnh và lưu hồ sơ.','Không có ngoại lệ ký trước theo dữ kiện; quy định ảnh áp dụng cho việc ký này.')])
r(28,'Hợp đồng vay công chứng ở X đang hoạt động, lưu hồ sơ. Các bên muốn sửa thời hạn tại Y, mang đủ bản gốc, văn bản đồng thuận và cùng có mặt. Không có quy định đặc thù khác. Y cho rằng đủ hồ sơ gốc sẽ thay yêu cầu về nơi công chứng. Cách xử lý nào đúng?',[
 ('Y thực hiện vì tất cả người ký cùng có mặt và xuất trình bản gốc.','Đủ chủ thể, hồ sơ không thay quy định về tổ chức thực hiện.'),
 ('Y thực hiện nếu gửi bản sửa về X lưu sau khi công chứng, như thủ tục di chúc.','Không áp ngoại lệ sửa di chúc cho hợp đồng vay.'),
 ('Các bên chỉ ký giấy gia hạn tại Y, bỏ công chứng vì không đổi số tiền vay.','Thời hạn là nội dung hợp đồng; không đổi tiền không loại thủ tục sửa giao dịch đã công chứng.')],
 'Tách ba điều kiện: đồng thuận, hồ sơ và nơi thực hiện; không dùng ngoại lệ di chúc hoặc bản gốc để thay thẩm quyền.')
r(29,'X đã chứng nhận đề nghị ủy quyền trên bản gốc. Bên nhận ở xa muốn Y chứng nhận việc chấp nhận trên bản sao có chứng thực, rồi ghép vào bản gốc tại X. X và Y đều do các bên chọn đúng quy định. Cách tổ chức chuỗi chứng nhận và lưu hồ sơ nào đúng?',[
 ('Y chứng nhận trên bản sao có chứng thực; X ghép hai bản nên vẫn đạt điều kiện có hai chữ ký, dấu.','Hai chứng nhận không thay yêu cầu chứng nhận tiếp vào bản gốc cùng hợp đồng.'),
 ('Y lập hợp đồng riêng chỉ có bên nhận, hai bản độc lập cùng ngày là đủ hoàn thành ủy quyền.','Thủ tục là chứng nhận tiếp việc chấp nhận vào bản gốc, không ghép hai hợp đồng độc lập.'),
 ('Y chứng nhận tiếp vào bản gốc nhưng chỉ cần gửi bản sao về X vì X đã lưu phần đề nghị.','Điều 57 yêu cầu gửi một bản gốc văn bản đã hoàn thành về tổ chức bên ủy quyền.')],
 'Theo dõi tính liên tục của bản gốc và bản lưu tại hai tổ chức; không đánh đồng bản chứng thực với bản gốc hợp đồng.')
r(30,'A đề nghị dùng tài sản tương lai thuộc quyền của mình, mô tả chung nhưng xác định được, giá ước tính thấp hơn khoản vay. B yêu cầu tài sản phải hiện hữu và đủ giá trị mới xem xét bảo đảm. Chưa xét điều kiện riêng của từng tài sản. Những nhận định nào đúng về các tiêu chí đang tranh luận?',[
 ('Phải loại hồ sơ do vừa là tài sản tương lai vừa thấp hơn khoản vay; chỉ một thiếu hụt trong hai tiêu chí mới được chấp nhận.','Hai tiêu chí đều được Điều 295 cho phép; không có quy tắc cộng thiếu hụt để loại bỏ.')],
 'Kiểm tra ba tiêu chí độc lập: hiện hữu, xác định được và giá trị; không suy một giới hạn không có từ tổ hợp dữ kiện.')
r(31,'Hợp đồng bằng văn bản thiếu công chứng bắt buộc; chủ thể, ý chí, nội dung đủ hợp pháp. Một bên đã thực hiện 75% nghĩa vụ được xác định trong hồ sơ, bên kia đề nghị công chứng viên xác nhận hiệu lực từ ngày ký để khỏi ra Tòa. Những nhận định nào đúng về cơ chế công nhận và giới hạn khắc phục?',[
 ('Đạt 75% thì hợp đồng tự được coi có công chứng từ ngày ký; công chứng viên chỉ cần bổ sung lời chứng xác nhận.','Ngưỡng thực hiện không trao quyền thay Tòa án cho công chứng viên hoặc tự có hiệu lực công chứng.')],
 'Phân biệt ngưỡng thực hiện, quyết định công nhận và chữa lỗi hình thức; không biến điều kiện đủ yêu cầu thành công chứng hồi tố.')
r(32,'A mua máy với phụ kiện có mã ghi nhầm trong hợp đồng. Hai bên phát hiện ngay trước khi giao, khắc phục ngay mã và giao đúng bộ để mục đích cả hai đạt được. A sau đó muốn tuyên vô hiệu chỉ vì bản ban đầu từng nhầm. Không có lừa dối hoặc căn cứ khác. Nhận định nào đúng?',[
 ('Có quyền tuyên vô hiệu vì xét nhầm lẫn tại lúc ký, không được tính việc sửa ngay sau đó.','Điều 126 có nhánh khắc phục ngay hoặc đạt mục đích, không chỉ đóng băng dữ kiện lúc ký.'),
 ('Việc sửa chỉ cứu giao dịch nếu A từ bỏ quyền yêu cầu vô hiệu bằng văn bản có công chứng.','Không có điều kiện từ bỏ có công chứng trong ngoại lệ Điều 126.'),
 ('Không vô hiệu vì máy đã giao, bất kể sửa nhầm lẫn có làm mục đích giao kết đạt được hay không.','Giao tài sản riêng lẻ không thay điều kiện đạt mục đích hoặc khắc phục ngay đạt mục đích.')],
 'Xác định quan hệ giữa khắc phục và mục đích giao kết; không dùng hoàn tất giao tài sản hoặc hình thức từ bỏ làm điều kiện thay.')
r(33,'A ký 10/01/2024 do B lừa dối. Hồ sơ chứng minh A không biết, không phải biết trước 10/01/2026; A yêu cầu Tòa tuyên vô hiệu 10/10/2026. B đề nghị tính hai năm từ ngày ký; A viện dẫn vô hiệu do lừa dối không hạn chế thời hiệu. Chỉ xét việc xác định thời hiệu, phương án nào đúng?',[
 ('Theo B: hai năm từ ngày ký vì lừa dối đã tồn tại ngay lúc giao kết.','Lừa dối dùng mốc biết hoặc phải biết, không mặc định ngày ký.'),
 ('Theo A: không hạn chế thời hiệu vì nội dung có yếu tố gian dối.','Không hạn chế thời hiệu tại Điều 123, 124 không tự áp cho lừa dối Điều 127.'),
 ('Tính từ lúc B thừa nhận; khi B phủ nhận thì thời hiệu chưa bắt đầu.','Sự thừa nhận của người lừa dối không phải mốc luật định.')],
 'Đánh giá hai lập luận cùng sai và chọn mốc nhận thức; không nhầm giả tạo với lừa dối trong giao kết.')
r(34,'Giao dịch đã bị tuyên vô hiệu. A nhận tài sản của B, nay không thể trả bằng hiện vật; A ngay tình khi thu hoa lợi. B có lỗi gây thiệt hại đã xác định. B muốn chỉ trả bồi thường để thay cả việc hoàn trả và thu hồi hoa lợi của A. Những kết luận nào đúng?',[
 ('Bồi thường theo lỗi thay toàn bộ nghĩa vụ hoàn trả, còn mọi hoa lợi phải cộng vào số tiền bồi thường.','Hoàn trả và bồi thường là hai hệ quả riêng; hoa lợi thu ngay tình được luật xử lý riêng.')],
 'Tách ba dòng xử lý: hoàn trả tài sản, hoa lợi ngay tình và thiệt hại có lỗi; không bù trừ bằng cách nhập mọi khoản.')
r(35,'M 16 tuổi muốn mua xe đạp thường bằng tiền của mình, không phải động sản phải đăng ký và không dùng vào kinh doanh; luật không đặt yêu cầu riêng. Người bán đòi áp quy tắc chỉ được tự giao dịch nhu cầu hằng ngày của trẻ 6–15 tuổi. Hướng xác định chủ thể ký đúng là gì?',[
 ('Cha mẹ phải ký thay vì giá xe lớn hơn khoản M dùng hằng ngày.','Nhóm 15–18 không chỉ bị giới hạn ở nhu cầu hằng ngày của nhóm nhỏ tuổi hơn.'),
 ('M cần đồng ý của đại diện vì mọi phương tiện đi lại đều là động sản phải đăng ký.','Đề đã xác định xe thường không thuộc nhóm phải đăng ký; không suy từ công dụng đi lại.'),
 ('M được ký xe đạp và được ký cả mọi xe phải đăng ký bằng cùng nguồn tiền riêng.','Nguồn tiền riêng không bỏ ngoại lệ động sản phải đăng ký.')],
 'Phân loại nhóm tuổi và tính chất tài sản thay vì giá trị hoặc công dụng; không mở rộng kết luận sang xe phải đăng ký.')
r(36,'Chồng thừa kế riêng nhà trong thời kỳ hôn nhân; chưa chia tài sản chung, chưa nhập nhà và không có thỏa thuận khác. Nhà phát sinh tiền thuê; chồng muốn ghi cả nhà và toàn bộ tiền thuê là riêng chỉ vì cùng một nguồn. Chọn các kết luận đúng khi phân biệt tài sản gốc, tài sản thay thế và dòng lợi tức.',[
 ('Nhà và tiền thuê cùng riêng; thu nhập từ tài sản riêng chỉ thành chung nếu vợ trực tiếp quản lý việc cho thuê.','Tiền thuê là lợi tức trong thời kỳ hôn nhân theo nhánh đề; không phụ thuộc vợ trực tiếp quản lý.')],
 'Kiểm tra nguồn sở hữu và loại dòng tài sản; không gộp lợi tức với tài sản hình thành từ nguồn riêng.')
r(37,'Vợ chồng thỏa thuận bằng văn bản cho chồng đưa máy sản xuất chung vào kinh doanh, phạm vi bao gồm giao dịch đang đề nghị. Chồng muốn ký giao dịch về máy; người tiếp nhận yêu cầu vợ đồng ký từng lần hoặc trước đó phải chuyển máy thành riêng. Chưa xét điều kiện chuyên ngành khác. Những nhận định nào đúng?',[
 ('Phải có chữ ký vợ ở mọi lần vì thỏa thuận chỉ cho sử dụng, không thể tạo quyền tự giao dịch theo Điều 36.','Điều 36 cho tự thực hiện giao dịch liên quan tài sản đưa vào kinh doanh theo thỏa thuận bằng văn bản.'),
 ('Chỉ được tự ký sau khi thỏa thuận được hiểu là nhập toàn bộ máy vào tài sản riêng của chồng.','Quyền tự giao dịch không cần chuyển chế độ sở hữu sang riêng.')],
 'Đánh giá thỏa thuận về phạm vi kinh doanh và tư cách ký; không đồng nhất quyền giao dịch với chuyển sở hữu.')
r(38,'Vợ chồng chia hợp pháp một phần tài sản chung, không thỏa thuận hậu quả khác. Họ còn một tài sản chưa chia và khoản nợ đã xác lập với C trước đó. C không đồng ý đổi nghĩa vụ. Một người đề nghị coi tài sản chưa chia thành sở hữu riêng theo tỷ lệ và chỉ đòi bên nhận tài sản. Phương án nào đúng?',[
 ('Phần đã chia riêng, phần còn lại riêng mỗi bên một nửa; nợ C chia theo tỷ lệ tài sản đã nhận.','Phần chưa chia vẫn chung; không tự đổi nghĩa vụ với C theo tỷ lệ tài sản.'),
 ('Phần đã chia và chưa chia đều vẫn chung đối với C, vì bảo vệ chủ nợ làm mất hiệu lực mọi việc chia.','Bảo vệ nghĩa vụ có trước không mặc nhiên làm việc chia hợp pháp vô hiệu hoặc mọi tài sản vẫn chung.'),
 ('C chỉ còn quyền đòi bên giữ giấy chứng nhận nếu thỏa thuận chia được công chứng.','Hình thức chia không tự sửa quyền của người thứ ba đã xác lập.')],
 'Giữ ranh giới sở hữu nội bộ và nghĩa vụ bên ngoài; không lấy bảo vệ chủ nợ để phủ nhận việc chia hợp pháp.')
r(39,'Vợ chồng chia toàn bộ tài sản chung cho vợ bằng văn bản công chứng, mục đích được chứng minh là né khoản nợ đến hạn với cá nhân C. Vợ viện dẫn không ký giấy vay và C chưa đăng ký biện pháp bảo đảm nên việc chia vẫn hợp pháp. Chỉ xét căn cứ vô hiệu của việc chia nhằm trốn nợ, phương án nào đúng?',[
 ('Chia hợp pháp vì C không có quyền bảo đảm đã đăng ký đối kháng.','Căn cứ trốn nghĩa vụ trả nợ không đòi chủ nợ có biện pháp bảo đảm đăng ký.'),
 ('Chia hợp pháp vì công chứng đã hoàn tất trước khi C kiện.','Công chứng hoặc kiện sau không chữa mục đích trốn nghĩa vụ được chứng minh.'),
 ('Chia hợp pháp nếu khoản nợ đứng tên chồng, vì vợ không ký nên không cần kiểm tra mục đích chia.','Mục đích chia trốn nghĩa vụ là căn cứ phải kiểm tra, không bị loại chỉ vì một người ký nợ.')],
 'Tách căn cứ vô hiệu do mục đích khỏi đăng ký bảo đảm, thời điểm khởi kiện và người đứng tên khoản nợ.')
r(40,'Vợ có tài sản riêng kèm nghĩa vụ liên quan; hai người thỏa thuận nhập vào tài sản chung. Loại tài sản này có yêu cầu hình thức giao dịch theo luật. Không có ngoại lệ về nghĩa vụ hoặc thỏa thuận khác. Một người đề nghị chỉ sử dụng chung để miễn hình thức và để khoản nợ tự chấm dứt. Những nhận định nào đúng?',[
 ('Việc cùng sử dụng lâu dài thay được hình thức bắt buộc của thỏa thuận nhập tài sản.','Yêu cầu hình thức ở khoản 2 Điều 46 không bị thay bằng sử dụng thực tế trong đề.'),
 ('Nghĩa vụ vẫn chỉ được thực hiện bằng tài sản riêng cũ dù đã nhập, vì chủ nợ chưa cho vay lại.','Khoản 3 Điều 46 quy định thực hiện bằng tài sản chung trừ ngoại lệ; không cần tạo khoản vay mới.')],
 'Kiểm tra ý chí, hình thức nhập và khối tài sản chịu nghĩa vụ; không nhầm nhập tài sản với xóa hoặc tái lập khoản nợ.')
r(41,'A phải giao hàng cho B. B đồng ý cho C thực hiện thay nhưng không đồng ý chuyển nghĩa vụ hoặc miễn A. C giao sai; A cho rằng sự đồng ý của B đủ để B chỉ đòi C, còn B muốn chuyển cả quyền sở hữu hàng lỗi sang C để quyết toán. Chỉ xét trách nhiệm thực hiện qua người thứ ba, kết luận nào đúng?',[
 ('B chỉ được yêu cầu C vì việc đồng ý người giao thay đã tạo chuyển giao nghĩa vụ.','Đồng ý cách thực hiện khác với đồng ý thay chủ thể có nghĩa vụ.'),
 ('A hết trách nhiệm nếu chứng minh đã trả đủ tiền thuê C thực hiện đúng công việc.','Trả phí cho C không thay kết quả thực hiện nghĩa vụ với B.'),
 ('B chịu phần sai hàng do đã đồng ý C, còn A chỉ chịu phần chưa thuê C thực hiện.','Sự đồng ý cho thực hiện qua người thứ ba không chuyển rủi ro làm sai sang B.')],
 'Phân biệt sự đồng ý về cách thực hiện và thay chủ thể nghĩa vụ; giữ trách nhiệm với bên có quyền.')
r(42,'Gara giữ hợp pháp xe A để sửa theo hợp đồng song vụ; sửa xong, tiền sửa đến hạn A chưa trả. Gara còn nắm một giấy tờ của A không phải đối tượng hợp đồng và muốn dùng cả hai để cầm giữ. Không có thỏa thuận loại trừ hay luật riêng. Chọn các kết luận đúng về căn cứ, đối tượng và hiệu lực cầm giữ.',[
 ('Giấy tờ khác của A cũng thuộc quyền cầm giữ chỉ vì gara đã có xe hợp pháp và tiền sửa đến hạn.','Không mở rộng đối tượng cầm giữ sang tài sản ngoài đối tượng hợp đồng song vụ.')],
 'Kiểm tra cả nguồn nắm giữ, đối tượng hợp đồng và mốc đến hạn; không mở rộng quyền sang mọi vật đang giữ.')
r(43,'A thuê máy khoan, ký cược 3 triệu để bảo đảm trả máy; tiền thuê là nghĩa vụ riêng. Máy mất, không còn để trả, không có thỏa thuận khác. B muốn cộng tiền thuê vào tiền ký cược hoặc dùng chế tài đặt cọc để quyết toán. Chưa xét bồi thường, tiền thuê hay bù trừ, chỉ xác định phần ký cược 3 triệu theo luật. Phương án nào đúng?',[
 ('B chỉ giữ phần tiền thuê trong 3 triệu, phải trả số dư vì ký cược cũng là tiền thuê ứng trước.','Ký cược bảo đảm trả tài sản, không tự biến thành tiền thuê ứng trước.'),
 ('B nhận 6 triệu riêng theo ký cược, vì mất máy được xử lý bằng mức gấp đôi như đặt cọc.','Nhầm biện pháp bảo đảm và hướng chế tài; Điều 329 không đặt mức gấp đôi này.'),
 ('B chỉ giữ 3 triệu sau khi kiện đòi máy không thành, dù hồ sơ đã xác định máy không còn.','Nhánh tài sản thuê không còn không đặt điều kiện đã kiện và không thu hồi được mới giữ ký cược.')],
 'Tách ký cược, tiền thuê và bồi thường; không nhập chế tài đặt cọc hoặc kiện trước vào nhánh mất tài sản thuê.')
r(44,'C bảo lãnh với điều kiện chỉ thực hiện thay khi A không có khả năng thực hiện. Nợ đến hạn, A chậm trả nhưng có tài sản và khả năng trả; B đã gửi yêu cầu trả cả A và C, chưa có nhánh bù trừ. B cho rằng gửi yêu cầu đồng thời là đủ gọi bảo lãnh. Chỉ xét điều kiện bảo lãnh đã thỏa thuận, kết luận nào đúng?',[
 ('C phải trả vì nợ đến hạn và B đã yêu cầu A trước hoặc đồng thời.','Yêu cầu trả không thay điều kiện không có khả năng thực hiện đã thỏa thuận.'),
 ('C phải trả phần gốc nhưng không phải lãi, vì điều kiện khả năng chỉ giới hạn khoản phụ.','Điều kiện thỏa thuận giới hạn thời điểm thực hiện bảo lãnh, không chỉ khoản phụ.'),
 ('C hết nghĩa vụ bảo lãnh vì A có khả năng tại lần yêu cầu đầu tiên.','Chưa đủ điều kiện lần này không làm bảo lãnh chấm dứt nếu điều kiện phát sinh sau.')],
 'Tách đến hạn, vi phạm và khả năng thực hiện; không coi chưa đáp ứng lần đầu là chấm dứt hẳn bảo lãnh.')
r(45,'Di chúc 2024 hợp pháp cho nhà X cho A, tiền Y cho B. Văn bản 2026 hợp pháp ghi là bổ sung, chỉ thay người nhận nhà thành C; không thay toàn bộ. Tài sản, người nhận còn tồn tại khi mở thừa kế, không có phần bắt buộc. C cho rằng bản mới xóa luôn phần tiền Y; A cho rằng bản gốc được công chứng trước nên ưu tiên. Chọn cách chia đúng.',[
 ('C nhận cả X và Y vì bản bổ sung lập sau luôn thay toàn bộ bản gốc.','Bổ sung chỉ ưu tiên nội dung mâu thuẫn, không xóa phần độc lập còn lại.'),
 ('A nhận X, B nhận Y vì phải sửa ngay trên bản gốc mới có thể thay người nhận nhà.','Bổ sung hợp pháp có hiệu lực ở chỗ mâu thuẫn, không bắt buộc chỉ ghi sửa trên bản cũ.'),
 ('X chia theo pháp luật, B nhận Y vì mâu thuẫn người nhận nhà làm phần X không giải thích được.','Mâu thuẫn bản gốc và bổ sung đã có quy tắc giải quyết; không tự coi phần đó không giải thích được.')],
 'Xác định loại văn bản sau và phạm vi mâu thuẫn; phân biệt bổ sung với thay thế, không chuyển sang chia pháp luật quá sớm.')
r(46,'Di chúc hợp pháp chỉ định A nhận nhà, B nhận xe, tổ chức K nhận tiền; từng phần độc lập. A chết trước người lập, K chấm dứt tồn tại trước mở thừa kế, B và xe còn. Hồ sơ chưa có thỏa thuận thay đổi phân chia. Chọn các kết luận đúng về từng phần.',[
 ('B nhận cả phần nhà và tiền vì là người được chỉ định còn sống duy nhất; không cần xét chia theo pháp luật phần mất hiệu lực.','Phần mất hiệu lực không tự tăng cho B; cần áp dụng cơ chế tương ứng cho phần đó.')],
 'Kiểm tra điều kiện tồn tại ở từng phần và tránh suy người nhận còn lại tự hưởng phần không hiệu lực.')
r(47,'Di sản 600 triệu đã chia A 400, B 200. Khoản nợ 900 triệu được xác định sau khi chia; không có thỏa thuận gánh vượt phần đã nhận. Chủ nợ đề nghị tính A hai phần ba nợ và B một phần ba, rồi dùng tài sản riêng bù thiếu. Chỉ xét giới hạn trách nhiệm mỗi người, phương án nào đúng?',[
 ('A phải trả 600 triệu, B 300 triệu vì áp tỷ lệ đã nhận trực tiếp lên toàn bộ nợ.','Tỷ lệ phải đi cùng giới hạn không vượt phần đã nhận.'),
 ('A và B mỗi người trả 300 triệu, phần nợ còn thiếu xóa vì di sản chỉ 600 triệu.','Không chia đều nghĩa vụ bất chấp phần đã nhận; cũng không tự tuyên xóa nợ trong câu hỏi giới hạn.'),
 ('A trả tối đa 400 triệu nhưng B miễn trả vì nhận tiền thay vì nhận hiện vật.','Dạng di sản nhận được không loại nghĩa vụ trong phạm vi phần đã nhận.')],
 'Kết hợp tương ứng theo tỷ lệ và trần trách nhiệm; không dùng tỷ lệ để mở sang tài sản riêng.')
r(48,'P lập di chúc cho con công chứng viên N hưởng tiền; N không hưởng phần nào và người con chưa nhận tiền thực tế. N đề nghị để đồng nghiệp đọc nội dung còn mình ký lời chứng. Chỉ xét điều kiện của người trực tiếp công chứng di chúc, những nhận định nào đúng?',[
 ('N được ký lời chứng khi đồng nghiệp đọc và người con chưa nhận tiền thực tế.','Xung đột căn cứ tư cách người thừa kế, không việc đã nhận tiền hay người đọc.'),
 ('N được thực hiện nếu phần người con thấp hơn phần của các người thừa kế còn lại và P đồng ý.','Tỷ lệ hưởng và đồng thuận không tạo ngoại lệ Điều 637.')],
 'Nhận diện lợi ích qua người thân và người ký chứng nhận; không lấy phần hưởng nhỏ hoặc chưa nhận thực tế để loại điều cấm.')
r(49,'M 16 tuổi muốn định đoạt tài sản mình bằng di chúc. Cha mẹ đồng ý về việc lập, nhưng đề nghị cha tự viết, ký thay M hoặc M ghi âm để tránh văn bản. M minh mẫn, ý chí tự nguyện. Chỉ xét yêu cầu với người 15–18 và tư cách người lập, hướng làm nào đúng?',[
 ('Cha lập và ký thay M vì sự đồng ý của cha mẹ đồng thời là đại diện lập di chúc.','Đồng ý việc lập không chuyển quyền thể hiện ý chí cuối cùng sang người đại diện.'),
 ('M có thể ghi âm thay văn bản vì cha mẹ cùng đồng ý và tài sản là riêng của M.','Nhóm 15–18 phải lập bằng văn bản, không miễn vì nguồn tài sản riêng.'),
 ('M lập văn bản nhưng cha mẹ quyết định toàn bộ nội dung thay M vì có quyền đồng ý.','Sự đồng ý không bỏ điều kiện ý chí của chính người lập.')],
 'Tách đồng ý về việc lập, hình thức bắt buộc và ý chí định đoạt; không suy cơ chế đại diện từ quyền của cha mẹ.')
r(50,'P nguy hiểm tính mạng, không thể lập văn bản, nói ý chí cuối cùng trước hai người làm chứng đủ điều kiện; họ ghi lại ngay, cùng ký. Một người đề nghị xác nhận chữ ký sau năm ngày lịch, người kia cho rằng chỉ cần P chết trong ba tháng. Chọn các nhận định đúng về hoàn tất hình thức và hậu quả nếu P sống minh mẫn sau ba tháng.',[
 ('Hai chữ ký ghi ngay đủ bảo đảm hợp pháp nếu P chết sớm; xác nhận trong thời hạn chỉ cần khi P còn sống.','Xác nhận trong năm ngày làm việc là một điều kiện hợp pháp, không tùy việc P chết sớm.')],
 'Kết hợp hoàn cảnh đặc biệt, thời hạn làm việc và cơ chế hủy khi sống minh mẫn; không lấy chết sớm thay điều kiện hình thức.')
r(51,'Di chúc định A 60%, B 40% tổng di sản; không phần bắt buộc hay thỏa thuận khác. Khối lúc mở thừa kế là 1 tỷ, lúc phân chia còn ròng 800 triệu sau giải quyết nghĩa vụ. A muốn giữ 600 triệu vì mức tại mở thừa kế, B muốn chia đều số còn lại do cả hai đều đủ quyền. Số hưởng đúng là bao nhiêu?',[
 ('A 600 triệu, B 200 triệu; giữ phần định theo giá mở thừa kế của A rồi cho B số dư.','Tỷ lệ phải cùng tính trên giá trị khối còn tại phân chia.'),
 ('A 400 triệu, B 400 triệu; giảm giá trị làm mất tỷ lệ di chúc và chuyển sang chia đều.','Giảm khối không tự mất hiệu lực tỷ lệ.'),
 ('A 500 triệu, B 300 triệu; chia đều 200 triệu hao hụt cho mỗi bên rồi trừ phần lúc mở.','Không phân bổ hao hụt đều theo người; áp tỷ lệ lên khối còn.')],
 'Chọn cơ sở định giá và phương thức phân bổ hao hụt; không giữ một phần ở giá cũ rồi dồn giảm cho người khác.')
r(52,'K không di chúc, chỉ có vợ, một con đã sinh và một con đã thành thai trước khi K chết nhưng chưa sinh. Di sản ròng 900 triệu. Vợ đề nghị nhận ngay 450 triệu, con đã sinh 450 triệu rồi sau sinh sẽ tặng lại phần nếu em sống. Những nhận định nào đúng khi chia trước lúc sinh?',[
 ('Có thể chia ngay 450/450 nếu hai người cam kết hoàn lại khi em sống, không cần dành phần hiện tại.','Cam kết hoàn lại không thay yêu cầu dành lại một suất theo Điều 660.'),
 ('Dành 150 triệu là đủ vì chưa sinh chỉ được tạm tính nửa suất của con đã sinh.','Luật yêu cầu phần bằng suất người thừa kế cùng hàng, không nửa suất.')],
 'Phân biệt dành phần bắt buộc trước phân chia với cam kết tặng lại; tính suất có điều kiện, không chiết giảm vì chưa sinh.')
r(53,'P có di sản ròng 1,2 tỷ, di chúc cho F 600 triệu và con S 600 triệu. S chết trước P, chỉ có con G; P còn con D. Cha mẹ, vợ P đã chết; D,G thành niên có khả năng lao động, không người bắt buộc; F còn sống. G yêu cầu nhận nguyên phần di chúc của S, D yêu cầu chia toàn bộ 1,2 tỷ theo luật. Cách chia nào đúng?',[
 ('F 600 triệu, G 600 triệu; thế vị áp trực tiếp vào người hưởng theo di chúc.','Phần S trước hết mất hiệu lực rồi phần đó chia theo pháp luật, không thế vị trực tiếp trong di chúc.'),
 ('F 400 triệu, D 400 triệu, G 400 triệu; thêm hai nhánh pháp luật vào toàn bộ di sản.','Phần di chúc F hợp pháp vẫn giữ; không chia toàn khối theo luật.'),
 ('F 600 triệu, D 600 triệu, G không hưởng vì cha không còn sống ở mở thừa kế.','Bỏ qua thế vị nhánh S trong phần chia theo pháp luật.')],
 'Tách phạm vi di chúc còn hiệu lực, xác định phần chuyển sang pháp luật rồi áp thế vị; không chọn hai yêu cầu cực đoan.')
r(54,'S có hành vi thuộc nhóm không được quyền hưởng ở khoản 1 Điều 621. Sau khi biết rõ hành vi, P vẫn lập di chúc hợp pháp cho S một phần; chưa chết ở thời điểm lập. Không có căn cứ khác. Người nhà đề nghị loại S do hành vi cũ hoặc cho S hưởng mọi phần theo pháp luật. Những nhận định nào đúng?',[
 ('P đã biết và cho S hưởng thì S tự được khôi phục quyền hưởng mọi phần theo pháp luật, không chỉ phần P định đoạt.','Ngoại lệ được hỏi gắn với việc người lập biết mà vẫn cho hưởng theo di chúc; không tự mở thành mọi phần pháp luật.')],
 'Xác định phạm vi ngoại lệ và điều kiện di chúc, không biến sự tha thứ thành khôi phục quyền hưởng không giới hạn.')
r(55,'Di sản 120 triệu; chỉ có mai táng hợp lý 20, cấp dưỡng thiếu 40, bảo quản 10 và tiền công 80 triệu. Không bảo đảm hoặc ưu tiên khác. Người lao động đề nghị trả theo tỷ lệ vì tổng yêu cầu 150 triệu, người quản lý đề nghị trả tiền công trước bảo quản. Riêng số còn để trả tiền công theo thứ tự luật là bao nhiêu?',[
 ('64 triệu, bằng 120/150 nhân 80 triệu tiền công theo tỷ lệ tất cả chủ nợ.','Các nhóm có thứ tự khác nhau, không chia ngay toàn bộ di sản theo tỷ lệ.'),
 ('60 triệu, trả mai táng, cấp dưỡng rồi tiền công, hoãn bảo quản sau.','Bảo quản đứng trước tiền công.'),
 ('80 triệu, đủ tiền công vì người lao động có yêu cầu trước chủ nợ cấp dưỡng.','Thời điểm yêu cầu không đảo thứ tự ưu tiên nêu ở Điều 658.')],
 'Sắp xếp khoản theo thứ tự trước khi tính thiếu hụt; phân biệt ưu tiên theo luật với tỷ lệ và thứ tự gửi yêu cầu.')
r(56,'A,B ký mua bán giả tạo để che giấu tặng cho; giao dịch thật đáp ứng đầy đủ chủ thể, ý chí, nội dung và hình thức, không trốn nghĩa vụ người thứ ba. Họ viện dẫn đã ký và thực hiện thanh toán giả để giữ mua bán. Chọn các kết luận đúng về hai tầng giao dịch.',[
 ('Mua bán có hiệu lực vì đã thực hiện một phần; việc che giấu chỉ chuyển thành vi phạm nghĩa vụ khai thông tin.','Thực hiện một phần không chữa sự giả tạo của giao dịch theo Điều 124.')],
 'Đánh giá độc lập giao dịch giả và giao dịch bị che; không dùng mức thực hiện chữa căn cứ vô hiệu do giả tạo.')
r(57,'N được mua tối đa 500 triệu nhưng ký 650 triệu. Bên bán biết giới hạn và việc vượt, vẫn ký. Chủ thể ủy quyền không đồng ý, không biết để im lặng và không gây lỗi làm bên bán nhầm. Bên bán đòi N trả phần 150 triệu theo trách nhiệm người đại diện vượt phạm vi. Chỉ xét cơ chế này, nhận định nào đúng?',[
 ('Chủ thể ủy quyền trả đủ 650 triệu vì bên bán đã chấp nhận việc vượt nên ràng buộc hai phía.','Bên bán không thay chủ thể ủy quyền đồng ý; các ngoại lệ làm ràng buộc chủ thể ủy quyền đã bị loại.'),
 ('N phải trả phần vượt bất kể bên bán biết, vì trách nhiệm mặc định không có ngoại lệ nhận thức.','Khoản 2 Điều 143 có ngoại lệ đối tác biết hoặc phải biết mà vẫn giao dịch.'),
 ('N không chịu bất kỳ trách nhiệm nào theo mọi căn cứ pháp luật, vì bên bán biết giới hạn.','Chỉ kết luận trong cơ chế khoản 2; không suy miễn mọi trách nhiệm độc lập khác.')],
 'Giữ phạm vi kết luận của ngoại lệ nhận thức, tránh cả ràng buộc chủ thể ủy quyền và miễn mọi trách nhiệm của đại diện.')
r(58,'Đánh giá bốn sự kiện ở các quan hệ đại diện theo ủy quyền độc lập: hết hạn; hoàn thành công việc; cá nhân được đại diện chết; một thành viên quản lý không thuộc quan hệ ủy quyền chết nhưng pháp nhân được đại diện còn tồn tại. Chưa xét bảo vệ người thứ ba. Những sự kiện nào làm chấm dứt theo dữ kiện?',[
 ('Thành viên quản lý chết làm mọi ủy quyền của pháp nhân chấm dứt, dù người này không là người đại diện và pháp nhân còn tồn tại.','Không đồng nhất cá nhân thành viên với pháp nhân được đại diện; đề loại các căn cứ khác.')],
 'Nhận diện đúng chủ thể và sự kiện pháp lý; không dùng cái chết của người trong tổ chức thay sự chấm dứt pháp nhân.')
r(59,'Hồ sơ không phức tạp được ghi sổ hợp lệ. Tổng từ tiếp nhận đến trả là sáu ngày làm việc; đúng bốn ngày xác minh liên quan giao dịch có hồ sơ chứng minh, không trùng hai ngày xử lý còn lại. Khách cho rằng vượt hai ngày, văn phòng cho rằng có xác minh nên toàn thời gian đều không tính. Cách tính nào đúng?',[
 ('Sáu ngày; loại trừ xác minh chỉ áp dụng hồ sơ phức tạp.','Khoản 1 Điều 45 không giới hạn loại trừ theo nhãn phức tạp.'),
 ('Không ngày nào được tính; việc có xác minh làm toàn bộ hồ sơ nằm ngoài thời hạn.','Chỉ bốn ngày xác minh bị loại, không cả thời gian xử lý.'),
 ('Bốn ngày; chỉ tính thời gian xác minh vì đó là nội dung quyết định việc công chứng.','Đảo phần được loại trừ và phần được tính.')],
 'Đánh giá hai lập luận đối lập cùng sai; tách thời gian trôi qua và thời hạn tính, không áp điều kiện phức tạp không có.')
r(60,'Văn bản giấy có lỗi đánh máy thuần túy, sửa không ảnh hưởng quyền, nghĩa vụ. X đã công chứng nay giải thể; Y lưu hồ sơ, thu hồi được tất cả bản gốc. Khách chỉ muốn sửa bản mình giữ; công chứng viên cũ của X sẵn sàng sửa. Phương án nào đúng về người sửa, phạm vi bản gốc và thông báo?',[
 ('Công chứng viên cũ X sửa bản khách giữ, Y chỉ lưu thông báo vì người cũ biết hồ sơ rõ nhất.','Tổ chức lưu hồ sơ là nơi thực hiện; phải sửa tất cả bản gốc thu hồi được.'),
 ('Y sửa riêng bản khách giữ rồi thông báo đủ để các bản khác tự có nội dung mới.','Thông báo không thay việc sửa các bản gốc khi có thể thu hồi đầy đủ.'),
 ('Y sửa đủ bản gốc nhưng chỉ thông báo khi bên nào yêu cầu, vì lỗi không ảnh hưởng quyền.','Luật vẫn yêu cầu thông báo bằng văn bản trong ba ngày làm việc từ hoàn thành sửa.')],
 'Kiểm tra đồng thời chủ thể kế tiếp, việc thu hồi bản gốc và mốc thông báo; không dùng một bước thay hai bước khác.')
r(61,'Hồ sơ giấy I có giao dịch ba trang và lời chứng một trang, in hai tờ. Hồ sơ II có giao dịch một trang và lời chứng một trang, in trên hai mặt cùng một tờ. Chỉ xét đánh số trang và giáp lai, phương án xử lý cả hai đúng là gì?',[
 ('I đánh số giao dịch 1–3, lời chứng lại số 1; II liên tục 1–2; cả hai giáp lai vì đều nhiều trang.','I phải liên tục đến lời chứng; giáp lai căn cứ nhiều tờ, không chỉ nhiều trang.'),
 ('Cả hai đánh số liên tục và đều giáp lai, vì chữ ký từng trang không thay giáp lai trên văn bản nhiều trang.','II chỉ có một tờ nên không thuộc yêu cầu giáp lai giữa nhiều tờ.'),
 ('I đánh số liên tục và giáp lai; II không cần đánh số vì chỉ dùng một tờ giấy.','II có hai trang vẫn phải đánh số liên tục, dù chỉ một tờ.')],
 'Xử lý hai cấu hình in, phân biệt tiêu chí trang với tờ; không áp cùng một yêu cầu cho cả hai.',
 [('Cả hai đánh số liên tục từ giao dịch đến hết lời chứng; I phải giáp lai giữa hai tờ, II không thuộc yêu cầu giáp lai nhiều tờ.','Khoản 1 dùng số trang, khoản 2 dùng số tờ theo dữ kiện.')])
r(62,'A đủ năng lực đã lập văn bản công chứng lựa chọn B làm giám hộ khi cần. Khi A ở tình trạng cần giám hộ, B không đồng ý nhận. Một hồ sơ khác chỉ có giấy lựa chọn C không công chứng, chứng thực. Chỉ xét cơ chế lựa chọn trước, không xét cử hoặc chỉ định theo căn cứ khác. Kết luận nào đúng?',[
 ('B phải nhận vì văn bản lựa chọn đã công chứng; giấy chọn C được khắc phục bằng việc C đồng ý.','Công chứng không thay sự đồng ý của người được chọn; đồng ý không tự chữa hình thức lựa chọn trước.'),
 ('B không phải nhận, còn C đương nhiên thành người giám hộ chỉ cần giấy lựa chọn ký tay và đủ điều kiện.','Việc chọn trước phải có công chứng hoặc chứng thực.'),
 ('B phải nhận cho đến khi có văn bản công chứng hủy lựa chọn; C chỉ bị loại nếu A đã chọn thêm người khác.','Điều 48 đặt sự đồng ý B; giấy C thiếu hình thức chứ không phụ thuộc việc chọn nhiều người.')],
 'Đánh giá hai hồ sơ: hình thức lựa chọn và sự đồng ý khi phát sinh giám hộ là điều kiện độc lập.',
 [('Không thể buộc B nhận theo giấy lựa chọn; hồ sơ chọn C chưa đáp ứng hình thức của cơ chế lựa chọn trước.','B không đồng ý, C thiếu công chứng/chứng thực. Không kết luận về cơ chế cử hoặc chỉ định khác.')])
r(63,'X nhận lưu giữ di chúc hợp lệ của P. Trước giải thể, X liên hệ được P nhưng hai bên không thỏa thuận việc chuyển tổ chức khác lưu giữ. X đề nghị tự chuyển cùng toàn bộ hồ sơ vì đã niêm phong bản di chúc trước mặt P khi nhận. Cách xử lý đúng trong nhánh đã liên hệ nhưng không thỏa thuận được là gì?',[
 ('Chuyển di chúc cho tổ chức nhận hồ sơ vì mọi trường hợp giải thể đều xử lý giống không liên hệ được P.','Chuyển cho tổ chức nhận hồ sơ là nhánh không liên hệ được; ở đây đã liên hệ nhưng không thỏa thuận.'),
 ('Trả di chúc cho P nhưng giữ phí lưu giữ vì phí không đi cùng hồ sơ công chứng.','Khoản 2 Điều 61 yêu cầu trả di chúc và phí lưu giữ trong nhánh này.'),
 ('Tự mở niêm phong, sao lưu rồi gửi cho người được hưởng, vì người ấy tiếp nhận thay P.','Chưa có căn cứ để chuyển di chúc cho người hưởng thay người lập trong thủ tục này.')],
 'Phân biệt không thỏa thuận được với không liên hệ được; không áp một cơ chế chuyển hồ sơ cho mọi trường hợp.',
 [('Trả lại di chúc và phí lưu giữ cho P, thay vì tự chuyển theo nhánh không liên hệ được.','Khoản 2 Điều 61 quy định riêng khi không có hoặc không đạt thỏa thuận.')],[(CC,'Khoản 2 Điều 61',CCURL)])
r(64,'A,B lập thỏa thuận chế độ tài sản bằng văn bản công chứng hợp pháp trước ngày đăng ký kết hôn; dự định dùng từ ngày ký. C,D chỉ lập văn bản sau khi đăng ký và muốn hồi tố như thỏa thuận xác lập ban đầu trước hôn nhân. Chỉ xét cơ chế xác lập ban đầu, không xét sửa thỏa thuận đã có. Phương án nào đúng?',[
 ('A,B áp dụng từ ngày ký; C,D áp dụng từ ngày đăng ký nếu văn bản sau cũng được công chứng.','Mốc xác lập là đăng ký; văn bản sau không đáp điều kiện lập trước của cơ chế xác lập ban đầu.'),
 ('A,B chỉ áp dụng khi có tài sản chung đầu tiên; C,D được hồi tố đến cùng mốc có tài sản.','Điều 47 không dùng mốc tạo tài sản chung.'),
 ('A,B cần lập lại sau đăng ký để có hiệu lực; C,D đã lập sau nên đúng trình tự.','Đảo điều kiện lập trước kết hôn với mốc xác lập từ đăng ký.')],
 'Tách thời điểm lập văn bản và xác lập chế độ; không lẫn xác lập ban đầu với sửa thỏa thuận về sau.',
 [('Chế độ của A,B xác lập từ đăng ký kết hôn; C,D không thể dùng văn bản lập sau để đáp điều kiện lập trước của cơ chế này.','Điều 47 yêu cầu hình thức, thời điểm lập trước và mốc đăng ký, không kết luận mọi thỏa thuận lập sau đều vô hiệu theo mọi căn cứ.')])
r(65,'Tổ chức có tài khoản truy cập cơ sở dữ liệu. Với hồ sơ A, đã khai thác hợp pháp đủ thông tin tương ứng giấy tờ b,c,d; với hồ sơ B, chưa khai thác được thông tin, khách chỉ nói dữ liệu có sẵn. Cả hai có dự thảo. Chỉ xét ngoại lệ nộp giấy tờ do khai thác dữ liệu và phí liên quan, xử lý nào đúng?',[
 ('Cả A,B đều miễn giấy tờ b,c,d vì tổ chức đã có tài khoản truy cập.','Có khả năng truy cập không đồng nghĩa đã khai thác được thông tin.'),
 ('A miễn cả dự thảo và phí, B miễn b,c,d nếu khách cam đoan thông tin có sẵn.','Ngoại lệ không gồm dự thảo, không miễn phí khai thác, không dựa cam đoan thay khai thác.'),
 ('A vẫn phải nộp toàn bộ bản sao vì dữ liệu chỉ hỗ trợ tra cứu, B chỉ cần bản chụp màn hình do khách cung cấp.','Trái ngoại lệ của A; ảnh khách cung cấp không tự thành khai thác hợp pháp của tổ chức.')],
 'Phân biệt quyền truy cập và kết quả khai thác; giữ đúng phạm vi ngoại lệ hồ sơ và phí.',
 [('A không nộp các giấy tờ tương ứng đã khai thác nhưng chịu phí theo luật; B chưa đáp điều kiện ngoại lệ chỉ vì dữ liệu có sẵn.','Điều 42 dùng điều kiện tổ chức đã khai thác được, không chỉ có tài khoản hoặc thông tin khách nói.')])
r(66,'Hồ sơ có điều khoản trái luật đã được chỉ rõ nhưng người yêu cầu không sửa. Đồng thời dấu hiệu cưỡng ép chưa làm rõ; người yêu cầu từ chối xác minh, giám định. Người làm chứng cho biết các bên ký trôi chảy và muốn dùng điều đó thay kiểm tra. Chọn các kết luận đúng về tiếp tục hay từ chối.',[
 ('Có thể nhận vì người làm chứng xác nhận ký tự nguyện sẽ khắc phục cả điều khoản trái luật và nghi ngờ cưỡng ép.','Lời làm chứng không thay sửa điều khoản hoặc làm rõ dấu hiệu theo thủ tục Điều 42.')],
 'Hai căn cứ từ chối độc lập không bị một lời xác nhận thay thế; phải kiểm tra nội dung và ý chí riêng.')
r(67,'W trực tiếp làm chứng văn bản, có căn cứ công chứng vi phạm luật; H có quyền, nghĩa vụ tài sản liên quan. N là công chứng viên khác không thực hiện văn bản này, không có tư cách liên quan khác, muốn tự ra quyết định vô hiệu. Chỉ xét quyền đề nghị và thẩm quyền theo luật, những kết luận nào đúng?',[
 ('W cần ủy quyền của người ký mới được đề nghị Tòa, vì tư cách làm chứng chưa tạo quyền yêu cầu độc lập.','Điều 54 liệt kê người làm chứng có quyền đề nghị khi có căn cứ.'),
 ('N có quyền tự tuyên vô hiệu bằng nghiệp vụ vì cùng nghề, còn H phải chờ các bên ký yêu cầu.','Công chứng viên không có thẩm quyền tự tuyên; H thuộc nhóm có quyền đề nghị Tòa.')],
 'Phân biệt tư cách yêu cầu độc lập và thẩm quyền quyết định; không suy quyền từ cùng nghề hoặc cần ủy quyền người ký.')
r(68,'Nhà đã thế chấp lần đầu công chứng ở M. Nay tiếp tục thế chấp trong phạm vi pháp luật cho phép, M vẫn hoạt động và giữ hồ sơ. N cùng tỉnh có bản gốc hợp đồng cũ, sẵn sàng gửi hồ sơ mới về M; các chủ nợ đồng ý. Chỉ xét nơi công chứng lần tiếp, phương án nào đúng?',[
 ('N thực hiện vì vừa đúng địa hạt vừa có bản gốc và các chủ nợ đồng ý.','Các điều kiện này không thay quy tắc riêng tại tổ chức lần đầu.'),
 ('N thực hiện nếu gửi một bản gốc về M, áp giống công chứng ủy quyền ở hai tổ chức.','Không lấy quy trình ủy quyền hai tổ chức thay thủ tục thế chấp tiếp theo.'),
 ('N thực hiện vì giao dịch bảo đảm nghĩa vụ mới nên không bị ràng buộc nơi hợp đồng cũ.','Điều 56 quy định đúng trường hợp tiếp tục thế chấp bảo đảm nghĩa vụ khác.')],
 'Kết hợp địa hạt và quy tắc nơi lần đầu; không dùng lưu hồ sơ hoặc quy trình ủy quyền tạo ngoại lệ.')
r(69,'P đã bị Tòa tuyên mất năng lực. Bác sĩ kết luận hồi phục; người đại diện đồng ý P tự ký, nhưng Tòa chưa hủy quyết định cũ. P đề nghị chỉ lưu hai giấy này là đủ. Chưa xét giao dịch hay căn cứ khác. Phương án xử lý tình trạng pháp lý đã được tuyên đúng là gì?',[
 ('Bác sĩ hồi phục và đại diện đồng ý cùng thay được quyết định hủy, vì đã đủ chứng cứ và ý chí.','Hai tài liệu là căn cứ yêu cầu, không thay thẩm quyền Tòa hủy quyết định.'),
 ('Đại diện có thể lập văn bản công chứng trả quyền ký cho P mà không cần Tòa.','Đại diện không có thẩm quyền hủy tình trạng Tòa đã tuyên bằng văn bản riêng.'),
 ('P tự ký được từ ngày ra viện, quyết định Tòa chỉ còn cần sửa đăng ký hộ tịch.','Tự đưa mốc ra viện và giới hạn thủ tục mà Điều 22 không quy định.')],
 'Tách chứng cứ hồi phục, sự đồng ý đại diện và quyết định làm thay đổi tình trạng pháp lý.')
r(70,'G giám hộ P mất năng lực; dự định cho thuê tài sản giá trị lớn để lấy tiền chăm sóc, tặng một tài sản cho người ngoài, và mua một tài sản của P cho mình. Người giám sát sẵn sàng đồng ý mọi việc. Chọn các kết luận đúng về từng nhóm, không gộp tất cả thành quyền định đoạt.',[
 ('Người giám sát đồng ý thì cả cho thuê, tặng người ngoài và giao dịch với G đều được khắc phục bằng cùng một điều kiện.','Tặng người khác có điều cấm riêng; giao dịch với G còn đòi vì lợi ích P, không chỉ có đồng ý.')],
 'Ba giao dịch có cơ chế khác nhau: chấp thuận, điều cấm và ngoại lệ có hai điều kiện; không dùng đồng ý làm chìa khóa chung.')
r(71,'P được Tòa tuyên có khó khăn nhận thức, không tuyên mất năng lực. Quyết định chỉ định G xác định phạm vi quản lý cụ thể, không trao quyền bán tài sản đang đề nghị. G viện dẫn giấy giám hộ để áp toàn bộ quyền của giám hộ người mất năng lực. Những nhận định nào đúng?',[
 ('G tự có toàn bộ quyền quản lý của giám hộ mất năng lực; phạm vi Tòa ghi chỉ hướng dẫn, không ràng buộc.','Điều 23 và khoản 2 Điều 59 buộc xét phạm vi Tòa xác định cho tình trạng này.')],
 'Đọc phạm vi quyết định và phân biệt hai tình trạng nhận thức; không suy mọi quyền từ tên giấy giám hộ.')
r(72,'Đất chỉ còn thời hạn sử dụng 20 năm. Hai bên muốn quyền bề mặt 30 năm; phương án dự phòng là không xác định thời hạn và chấm dứt bằng thông báo một tháng. Chỉ xét giới hạn thời hạn và thông báo trong hai phương án, kết luận nào đúng?',[
 ('30 năm được phép do thỏa thuận; nếu không ghi hạn thì báo trước một tháng là đủ.','Thỏa thuận không vượt thời hạn đất; nhánh không xác định hạn phải báo văn bản ít nhất sáu tháng.'),
 ('Tối đa 20 năm; không xác định hạn thì mỗi bên được chấm dứt ngay bằng lời nói.','Đúng giới hạn 20 nhưng sai yêu cầu văn bản và ít nhất sáu tháng.'),
 ('Tối đa 30 năm nếu được chủ đất đồng ý; phương án không ghi hạn bắt buộc Tòa quyết định mới được chấm dứt.','Đồng ý không bỏ giới hạn thời hạn đất; Điều 270 cho mỗi bên chấm dứt theo thông báo luật định.')],
 'Đánh giá hai phương án, không lấy đúng giới hạn tài sản nền để bỏ yêu cầu của nhánh không xác định hạn.',
 [('Không vượt 20 năm; nếu không xác định thời hạn thì có quyền chấm dứt nhưng phải báo bằng văn bản trước ít nhất sáu tháng.','Kết hợp khoản 1 và 2 Điều 270; không chấp nhận riêng một nửa đúng của phương án.')],[(DS,'Khoản 2 Điều 270',DSURL)])
r(73,'A hưởng dụng tài sản B. Sau đó A nhận quyền sở hữu chính tài sản ấy bằng giao dịch hợp pháp; thời hạn hưởng dụng cũ còn năm năm. B muốn giữ quyền hưởng dụng cũ cho mình, A cho rằng phải chờ hết hạn mới được dùng theo sở hữu. Nhận định nào đúng?',[
 ('Hưởng dụng còn năm năm nên A chỉ có sở hữu trên giấy, quyền sở hữu sử dụng chờ hết hạn.','Người hưởng dụng thành chủ sở hữu là căn cứ chấm dứt quyền hưởng dụng cũ.'),
 ('Hưởng dụng tự chuyển cho B như một khoản bảo lưu vì B đã là chủ sở hữu trước.','Không có nhánh tự chuyển quyền cho chủ cũ.'),
 ('Chỉ chấm dứt nếu cả hai ký thỏa thuận riêng ngoài giao dịch chuyển sở hữu.','Thành chủ sở hữu là căn cứ độc lập, không bắt buộc thêm thỏa thuận chấm dứt riêng.')],
 'Tách căn cứ chấm dứt độc lập và thời hạn còn lại; không suy bảo lưu quyền cho chủ cũ.')
r(74,'Nghĩa vụ bảo đảm hợp pháp gồm gốc 500, lãi 20, phạt 10 và thiệt hại 5 triệu đã xác định; không thỏa thuận phạm vi, không luật riêng. Một người đề nghị chỉ cộng lãi do khoản phụ khác không ghi riêng, người khác lấy giá tài sản để chặn mức nghĩa vụ. Chọn các kết luận đúng về phạm vi nghĩa vụ, chưa xét số thu xử lý tài sản.',[
 ('Phạm vi là 520 triệu vì lãi tự đi theo, phạt và bồi thường chỉ có bảo đảm nếu văn bản liệt kê riêng.','Mặc định toàn bộ tại Điều 293 gồm cả phạt và bồi thường khi không thỏa thuận hoặc luật riêng.')],
 'Phân biệt mặc định phạm vi và mức thu tài sản; không tự chia các khoản phụ thành nhóm được, không được bảo đảm.')
r(75,'P muốn bổ sung di chúc đã công chứng và lưu ở X đang hoạt động. P chọn Y, người hưởng theo bản cũ phản đối; Y dự định yêu cầu họ đồng ý và cho rằng chuyển tổ chức là đủ thay thông báo X. Chỉ xét thủ tục sửa di chúc theo yêu cầu người lập, hướng làm nào đúng?',[
 ('P phải về X vì X chưa chấm dứt, Y chỉ có thẩm quyền khi tiếp nhận hồ sơ do giải thể.','Di chúc có ngoại lệ bất kỳ tổ chức, không phải chỉ nơi cũ hoặc nơi tiếp nhận.'),
 ('P được đến Y sau khi người hưởng cũ đồng ý bằng văn bản để bảo vệ quyền đã được định đoạt.','Khoản 4 Điều 58 không đặt chấp thuận người hưởng thay ý chí người lập.'),
 ('P đến Y thì không cần báo X vì hai tổ chức độc lập và bản bổ sung mới hơn.','Luật vẫn đòi thông báo cho tổ chức đang lưu giữ bản trước.')],
 'Tách quyền sửa của người lập, ngoại lệ về nơi và thông báo nơi lưu; không suy người hưởng cũ có quyền phủ quyết.')
r(76,'Nhà đã xác định là tài sản chung nhưng giấy chứng nhận chỉ tên chồng. Chồng mang bản gốc và đề nghị bán, vợ chưa có thỏa thuận bằng văn bản. Các bên cho rằng bản gốc, nguồn tiền do chồng nắm và tên trên giấy đủ xác định quyền ký. Những kết luận nào đúng?',[
 ('Tên trên giấy và giữ bản gốc cho phép chồng ký, trừ khi vợ có quyết định của Tòa xác nhận lại quyền.','Tính chung đã được xác định; không buộc vợ kiện trước mới kiểm tra đồng thuận.'),
 ('Để giao dịch thì mọi trường hợp phải cấp lại giấy ghi hai tên, kể cả có thỏa thuận khác hợp pháp.','Điều 34 có ngoại lệ thỏa thuận khác; không đưa yêu cầu tuyệt đối về hai tên.')],
 'Không đồng nhất giấy chứng nhận, việc giữ bản gốc và quyền định đoạt; phân biệt điều kiện ký với thông tin đăng ký.')
r(77,'Tài sản được chia bằng bản án có hiệu lực. Vợ chồng ký văn bản chấm dứt hiệu lực chia nhưng chưa được Tòa công nhận; không thỏa thuận nhập lại phần đã chia, không sửa nghĩa vụ có trước với người thứ ba. Chọn các kết luận đúng về bước công nhận và hậu quả, không suy hồi tố từ chữ ký.',[
 ('Văn bản hai người ký đủ tự hủy hiệu lực phần tài sản của bản án và nhập tất cả phần đã chia lại thành chung.','Thiếu Tòa công nhận trong nhánh này; chấm dứt chia cũng không tự nhập lại phần đã chia nếu không thỏa thuận.')],
 'Theo dõi căn cứ Tòa chia, yêu cầu công nhận và phần tài sản đã chia; không suy hồi tố hoặc nhập tự động.')
r(78,'Vợ chồng có nợ chung với C. Khi ly hôn, họ giao nội bộ chồng trả; C không đồng ý đổi nghĩa vụ nhưng đã nhận một phần tiền từ chồng, không miễn nghĩa vụ ai. Vợ viện dẫn việc C nhận tiền là chấp thuận chỉ đòi chồng. Nhận định nào đúng về quyền C sau ly hôn?',[
 ('C nhận tiền chồng là đủ chấp thuận chuyển toàn bộ nghĩa vụ, vợ hết trách nhiệm phần còn lại.','Nhận thanh toán không đồng nghĩa thỏa thuận thay nghĩa vụ; đề xác nhận không có chấp thuận, miễn.'),
 ('C chỉ đòi vợ phần đúng tỷ lệ tài sản vợ được chia, dù nghĩa vụ cũ chưa được thay đổi.','Không tự đổi quan hệ với C theo tỷ lệ chia nội bộ.'),
 ('C phải tham gia lại vụ ly hôn mới giữ quyền đòi khoản nợ còn lại.','Quyền, nghĩa vụ với người thứ ba vẫn có hiệu lực theo Điều 60, không đòi xác lập lại như vậy.')],
 'Phân biệt nhận thanh toán với chấp thuận đổi nghĩa vụ; không dùng phân công nội bộ hoặc tỷ lệ tài sản thay quyền chủ nợ.')
r(79,'Có đủ căn cứ xử lý tài sản thế chấp; không thỏa thuận phương thức, không luật riêng. Bên nhận đã thuê thẩm định giá, muốn tự nhận tài sản theo giá thẩm định và bù chênh lệch mà chưa đạt thỏa thuận. Phương án nào đúng?',[
 ('Được tự nhận theo giá thẩm định vì bù chênh lệch đã loại việc xâm hại bên bảo đảm.','Thẩm định và bù chênh lệch không thay thỏa thuận về phương thức nhận chính tài sản.'),
 ('Được tự bán vì phương thức không thỏa thuận do bên nhận chọn khi đã phát sinh vi phạm.','Quy tắc mặc định là bán đấu giá, không tự chọn phương thức.'),
 ('Không thể xử lý cho đến khi hai bên đồng thuận một phương thức, dù có căn cứ xử lý.','Luật đặt phương thức mặc định khi không thỏa thuận.')],
 'Tách căn cứ, định giá và quyền chọn phương thức; không lấy một bước thẩm định chữa thiếu thỏa thuận.')
r(80,'A cầm cố tài sản cho B, nghĩa vụ còn. A đã thông báo dự định tặng C, B chưa trả lời; không luật riêng cho phép định đoạt không cần chấp thuận. Sau đó dự kiến nghĩa vụ sẽ chấm dứt hợp pháp. Những kết luận nào đúng về quyền trước và sau mốc này?',[
 ('A có thể tặng sau thông báo vì chủ sở hữu vẫn là A và B không phản đối ngay.','Sở hữu còn không bỏ điều kiện B đồng ý; thông báo và im lặng không tự là chấp thuận.')],
 'Đối chiếu quyền sở hữu, điều kiện định đoạt và quyền đòi trả lại khi nghĩa vụ chấm dứt; không gộp các thời điểm.')
r(81,'C 13 tuổi có nhà riêng, cha mẹ quản lý, không có người giám hộ khác. Cha muốn bán để chi việc học C; mẹ chưa thỏa thuận, C muốn giữ nhà. Cha cho rằng vì lợi ích học tập nên không cần mẹ và ý kiến C chỉ xét khi C đủ 15. Chỉ xét quyền cha mẹ và nguyện vọng con, hướng xử lý nào đúng?',[
 ('Cha được bán vì mục đích vì lợi ích đã đáp ứng, mẹ chỉ cần tham gia khi tài sản là chung của cha mẹ.','Bất động sản của con vẫn cần thỏa thuận cha mẹ, không chỉ tài sản chung cha mẹ.'),
 ('C được tự quyết bán hoặc không bán vì đã trên 9, nên cha mẹ không còn quyền định đoạt.','Xem xét nguyện vọng không đồng nghĩa chuyển quyền tự định đoạt cho con 13 tuổi.'),
 ('Cha mẹ thỏa thuận là đủ; nguyện vọng C chỉ xét từ nhóm 15–18 có quyền tự định đoạt.','Điều 77 yêu cầu xem nguyện vọng con từ đủ 9 trong nhánh dưới 15.')],
 'Kiểm tra đồng thời người đại diện, loại tài sản, lợi ích và tuổi xét nguyện vọng; không lấy một yếu tố đáp ứng thay tất cả.')
r(82,'M 17 tuổi có tiền riêng, xe máy phải đăng ký và định dùng tiền vào kinh doanh. M muốn áp quyền tự định đoạt người 15–18 cho cả bán xe và đưa tiền kinh doanh; cha mẹ chỉ đồng ý miệng. Chọn các kết luận đúng về ngoại lệ và hình thức đồng ý.',[
 ('Tiền không phải tài sản đăng ký nên đưa tiền vào kinh doanh không cần văn bản; bán xe chỉ cần đồng ý miệng của cha mẹ.','Ngoại lệ dùng tài sản kinh doanh là nhánh riêng, không phụ thuộc đăng ký; cả hai cần văn bản theo Điều 77.')],
 'Tách ngoại lệ theo tài sản và theo mục đích; không dùng tính chất tiền để bỏ yêu cầu kinh doanh hoặc hình thức.')
r(83,'A phải giao đúng tranh gốc đặc định cho B. Do vi phạm A, tranh đã hủy, còn gây thiệt hại khác có chứng cứ. A có bản in cùng kích thước, muốn giao thay và chỉ trả chênh lệch giá. Không có thỏa thuận thay thế hay căn cứ miễn trách nhiệm. Cách quyết toán đúng là gì?',[
 ('A giao bản in và trả chênh lệch; nghĩa vụ giao vật tự chuyển thành vật cùng loại khi gốc mất.','Không tự đổi vật đặc định thành vật cùng loại hoặc bản in.'),
 ('B chỉ đòi bồi thường thiệt hại khác, giá trị tranh đã nằm trong khoản này nên không cần xác định riêng.','Phải thanh toán giá trị vật không còn; không mặc định nhập với thiệt hại khác.'),
 ('A thanh toán giá trị tranh rồi miễn thiệt hại khác vì không được áp hai hệ quả trong cùng vi phạm.','Điều 356 cho thanh toán giá trị cùng bồi thường thiệt hại do vi phạm khi có căn cứ.')],
 'Phân loại vật và hai dòng trách nhiệm; không nhập giá trị vật, chênh lệch bản thay và thiệt hại khác.')
r(84,'A nợ 100 triệu, đã trả 70; B miễn hợp pháp toàn bộ 30 còn lại, không đặt điều kiện hay giữ nghĩa vụ phụ. Biên nhận chỉ ghi đã trả 70. A muốn coi nghĩa vụ hoàn thành, B sau đổi ý viện biên nhận chưa đủ 100. Chỉ xét dữ kiện miễn đã có hiệu lực, nhận định nào đúng?',[
 ('Chưa hoàn thành vì biên nhận phải ghi đủ tổng tiền 100 mới thay việc trả thực tế.','Điều 373 cho hoàn thành bằng thực hiện một phần và miễn phần còn lại, không bắt nhận đủ tiền.'),
 ('Chỉ tạm hoãn 30 triệu, mọi việc miễn mặc định có thể đòi lại khi bên có quyền đổi ý.','Đề đã xác nhận miễn hợp pháp không điều kiện, không phải tạm hoãn.'),
 ('Toàn giao dịch vô hiệu do thực trả khác số nợ, A được đòi lại 70 triệu.','Miễn phần còn lại không làm nghĩa vụ trước vô hiệu hoặc hoàn trả phần đã thực hiện.')],
 'Đọc bản chất và hiệu lực miễn thay vì số trên biên nhận; phân biệt hoàn thành, hoãn và vô hiệu.')
r(85,'P chết, không chỉ định người quản lý trong di chúc. Người thừa kế chưa thống nhất cử ai; B tự nhận là người quản lý vì hưởng phần lớn nhất. A đang quản lý hợp pháp từ trước. Một cơ quan cũng đề nghị nhận ngay vì người thừa kế còn tranh luận. Theo cơ chế người quản lý di sản, hướng xác định đúng là gì?',[
 ('B quản lý vì tỷ lệ hưởng lớn nhất thay được sự thống nhất cử của người thừa kế.','Tỷ lệ di sản không tự tạo việc cử người quản lý.'),
 ('Cơ quan nhà nước quản lý vì tranh luận giữa người thừa kế tương đương chưa xác định được người thừa kế.','Đã có người quản lý khoản 2; không đồng nhất chưa cử với điều kiện nhánh nhà nước.'),
 ('A giữ luôn quyền sở hữu di sản vì chưa có người khác được cử trong một thời gian.','Tiếp tục quản lý không tự chuyển sở hữu di sản.')],
 'Phân biệt chưa thống nhất cử, chưa xác định người thừa kế và quyền sở hữu; chọn đúng nhánh quản lý đang có.')
r(86,'Các người thừa kế cử A quản lý di sản bằng văn bản; văn bản chưa chấp thuận bán tài sản. A muốn bán vì thuận tiện, viện việc đã được cử và phải chịu trách nhiệm bồi thường nếu bán sai để cho rằng không cần xin thêm. Chọn các kết luận đúng về quyền, nghĩa vụ.',[
 ('Văn bản cử cộng trách nhiệm bồi thường đã đủ thay đồng ý định đoạt; người thừa kế chỉ có quyền đòi thiệt hại về sau.','Quyền chấp thuận định đoạt trước không bị thay bằng trách nhiệm bồi thường sau.')],
 'Tách cử quản lý, chấp thuận bán và trách nhiệm vi phạm; không dùng khả năng bồi thường như quyền tự định đoạt.')
r(87,'A được cử quản lý và đã làm công việc, phát sinh chi phí bảo quản đủ căn cứ thanh toán. Hai bên không đạt thỏa thuận mức thù lao. Người thừa kế chỉ chấp nhận hoàn chi phí, A tự đặt thù lao bằng phần trăm di sản. Chỉ xét thù lao khi không đạt thỏa thuận và phân biệt với chi phí, nhận định nào đúng?',[
 ('Hoàn chi phí đồng nghĩa đã trả công, A không còn được xét thù lao nếu chưa chốt mức từ đầu.','Chi phí và thù lao là các quyền khác nhau; khoản 3 đặt thù lao hợp lý.'),
 ('A tự chốt mức phần trăm và khấu trừ vào di sản vì đã thực hiện công việc.','Thù lao hợp lý không đồng nghĩa quyền tự định mức tùy ý hoặc khấu trừ không căn cứ.'),
 ('Chỉ xét thù lao sau khi A trở thành người thừa kế; người ngoài không có quyền này.','Quyền thù lao thuộc người quản lý theo luật, không đòi đồng thời là người thừa kế.')],
 'Phân biệt hoàn chi phí với trả công và mức hợp lý với tự định mức; không đưa điều kiện tư cách thừa kế không có.')
r(88,'Di chúc không cử quản lý hoặc phân chia; các người thừa kế họp để cử và thống nhất cách chia. Một người đề nghị chỉ ghi âm cuộc họp; người khác muốn công chứng mọi nội dung và để nhóm tham dự định luôn phần người vắng. Chọn các kết luận đúng theo yêu cầu họp mặt, chưa xét hình thức chuyên biệt từng tài sản.',[
 ('Mọi thỏa thuận phải công chứng chỉ vì có bất động sản trong khối, ngay cả nội dung cử người quản lý không xét quy định khác.','Điều 656 yêu cầu văn bản; không tự đặt công chứng cho mọi loại nội dung cuộc họp.'),
 ('Nhóm có mặt được dùng biên bản họp thay sự tham gia của người vắng để loại phần hưởng của người ấy.','Họp mặt không tự tạo căn cứ tước quyền hoặc thay ý chí người vắng.')],
 'Tách hình thức chung của thỏa thuận, hình thức giao dịch chuyên biệt và quyền người không tham dự; không dùng ghi âm hoặc biên bản thay tất cả.')
r(89,'P nhờ người khác viết hộ di chúc rồi tự ký; không có người làm chứng, không công chứng, chứng thực. Hồ sơ xác nhận nội dung đúng ý chí, không bị ép. P muốn áp hình thức văn bản không có người làm chứng vì đã có chữ ký mình. Chỉ xét yêu cầu của hình thức này, phương án nào đúng?',[
 ('Đủ hình thức không có người làm chứng vì chữ ký P xác nhận nội dung đúng ý chí.','Điều 633 còn đòi tự viết, không chỉ tự ký.'),
 ('Đủ hình thức nếu người viết hộ cam đoan sau rằng mình không hưởng tài sản.','Cam đoan sau không biến người viết hộ thành P tự viết hoặc hoàn tất hình thức khác.'),
 ('Mọi văn bản di chúc không công chứng đều vô hiệu nên không cần phân biệt tự viết hay viết hộ.','Luật cho hình thức không công chứng hợp pháp khi đủ điều kiện; không dùng quy tắc tuyệt đối này.')],
 'Đánh giá đúng hình thức đang viện dẫn và giới hạn kết luận; không dùng ý chí đúng chữa yêu cầu tự viết hoặc phủ nhận mọi hình thức không công chứng.',
 [('Chưa đáp ứng hình thức không có người làm chứng vì P không tự viết; không suy rằng mọi di chúc không công chứng đều vô hiệu.','Điều 633 yêu cầu người lập tự viết và ký; những hình thức khác có điều kiện riêng.')])
r(90,'Di chúc hợp pháp dành 200 triệu thờ cúng trong di sản 500 triệu; nghĩa vụ tài sản người chết 600 triệu. Người được cử quản lý đòi giữ 200 trước rồi chỉ trả nợ bằng 300; đồng thời cho rằng sau này nếu mình làm sai, phần thờ cúng sẽ chia cho người hưởng. Chọn kết luận đúng về giới hạn và cơ chế quản lý.',[
 ('Giữ phần thờ cúng trước là bắt buộc do di chúc hợp pháp; thiếu nợ chỉ ảnh hưởng phần còn được chia thừa kế.','Khoản 2 Điều 645 không cho dành phần thờ cúng khi toàn bộ di sản không đủ thanh toán.')],
 'Kiểm tra đủ tài sản trả nghĩa vụ trước khi áp quản lý thờ cúng; không nhầm đổi người quản lý với chia phần đó.')
r(91,'Di sản tổng 800 triệu gồm phần di tặng A 200 và phần khác 600; nợ hợp pháp 900, không còn chi phí, nghĩa vụ khác hay thỏa thuận nhận trách nhiệm vượt di sản. Dùng 600 trả nợ, chủ nợ yêu cầu A bù đủ 300 còn thiếu; A đề nghị giữ toàn phần vì là di tặng. Chỉ xét phần di tặng và giới hạn theo dữ kiện, cách xử lý nào đúng?',[
 ('Dùng 100 triệu di tặng, để A 100 vì chỉ phải chịu một nửa khoản được cho.','Không có quy tắc nửa phần; nợ còn thiếu 300 nên dùng đủ 200 di tặng.'),
 ('A giữ đủ 200 vì khoản nợ không được liệt kê trong di chúc cho A.','Ngoại lệ Điều 646 phụ thuộc di sản không đủ, không việc di chúc liệt kê nợ.'),
 ('A dùng 200 di tặng và 100 tiền riêng để đủ phần 300 chưa trả cho chủ nợ.','Không có thỏa thuận gánh vượt; không suy thiếu di sản thành nghĩa vụ tiền riêng của A.')],
 'Tính thiếu hụt rồi áp ngoại lệ di tặng và trần trách nhiệm; tránh cả miễn tuyệt đối lẫn bù thiếu bằng tài sản riêng.')
r(92,'P và con S chết cùng tai nạn, không xác định được ai chết trước. S có con G còn sống. Một người muốn cộng di sản P vào di sản S rồi chia cho người thừa kế S; người khác loại G vì S không sống tại mở thừa kế P. Chỉ xét quan hệ hai di sản và thế vị, kết luận nào đúng?',[
 ('Cộng phần S lẽ ra hưởng của P vào di sản S trước khi chia, rồi G hưởng từ khối S.','P,S không thừa kế của nhau trong nhánh chết cùng thời điểm; thế vị không phải chuyển qua di sản S.'),
 ('G chỉ có thể hưởng di sản S, vì việc không thừa kế nhau cũng loại nhánh thế vị ở P.','Điều 619 bảo lưu ngoại lệ thế vị, Điều 652 áp cả chết cùng thời điểm.')],
 'Tách hai khối di sản và đường hưởng thế vị, không giả định thứ tự chết hoặc nhập di sản qua người đã chết.')
r(93,'Di sản ròng 1,2 tỷ đã chia A,B mỗi người 600 triệu theo pháp luật. Sau đó xác định con C cùng hàng hưởng ngang nhau; tài sản A giữ tăng giá, cả khối hiện 1,8 tỷ còn B nhận tiền. Không có thỏa thuận khác. Chọn cách thanh toán cho C theo giá và tỷ lệ luật định, không chia lại hiện vật.',[
 ('A,B mỗi người trả 300 triệu theo một suất 600 tính trên giá hiện tại.','Điều 662 dùng phần tại thời điểm chia, không định lại theo giá tăng.'),
 ('A trả toàn 400 triệu vì còn giữ hiện vật, B đã nhận tiền nên không phải thanh toán.','Nghĩa vụ chia theo tỷ lệ đã nhận, không loại người nhận tiền.'),
 ('A,B mỗi người trả 100 triệu vì C chỉ nhận phần chênh lệch sau khi trừ hai suất cũ đã hoàn tất.','Suất C là 400 triệu từ 1,2 tỷ chia ba; không coi các suất cũ được giữ nguyên rồi chỉ chia dư.')],
 'Đọc đúng thời điểm giá trị, tỷ lệ đã nhận và dạng tài sản; không dùng giá tăng hoặc hiện vật để chuyển toàn nghĩa vụ.')
r(94,'C là con riêng của vợ P, chưa được P nhận làm con nuôi. Chứng cứ xác nhận P,C chăm sóc, nuôi dưỡng như cha con; không chỉ cùng địa chỉ. Có người yêu cầu giấy nhận con nuôi, có người coi hôn nhân với mẹ đủ thay chứng cứ nuôi dưỡng. Chọn các kết luận đúng về quan hệ thừa kế được hỏi.',[
 ('Không nhận con nuôi thì chỉ mẹ C được hưởng, C không thể dùng chứng cứ chăm sóc để xác định quan hệ này.','Điều 654 là nhánh con riêng–bố dượng, không buộc trở thành con nuôi.'),
 ('Chỉ cần P kết hôn mẹ C, nên có thể bỏ toàn bộ chứng cứ chăm sóc, nuôi dưỡng.','Quan hệ hôn nhân xác định tư cách, không thay điều kiện chăm sóc, nuôi dưỡng như cha con.')],
 'Phân biệt hai quan hệ pháp lý và chứng cứ thực tế; không lấy giấy con nuôi hoặc địa chỉ/hôn nhân làm điều kiện thay.')
r(95,'P chết 12/10/2025. Vợ yêu cầu 12/10/2026 vì chia ngay ảnh hưởng nghiêm trọng đời sống mình và gia đình, điều kiện được chứng minh. Hồ sơ đề nghị tính ba năm từ ngày yêu cầu hoặc từ ngày Tòa quyết định; cũng muốn cộng sẵn một lần gia hạn. Chỉ xác định trần lần đầu theo luật, mốc nào đúng?',[
 ('12/10/2029, tính từ ngày yêu cầu để bảo đảm đủ ba năm chưa chia.', 'Luật tính lần đầu từ mở thừa kế, không bảo đảm luôn đủ ba năm sau yêu cầu.'),
 ('Ba năm từ ngày quyết định của Tòa, vì trước đó chưa có hạn chế có hiệu lực.', 'Mốc luật định vẫn là mở thừa kế dù quyết định ban hành sau.'),
 ('12/10/2031, cộng ngay hai lần ba năm vì điều kiện nghiêm trọng hiện đã được chứng minh.', 'Gia hạn phải có yêu cầu và chứng minh điều kiện tiếp tục khi hết hạn, không tự cộng sẵn.')],
 'Tách mốc mở thừa kế, ngày yêu cầu, ngày quyết định và giai đoạn gia hạn có điều kiện.')
r(96,'Hồ sơ nhà đã xác định chỉ một người thừa kế, có giấy tử, giấy quan hệ và giấy quyền sở hữu đủ kiểm tra. Chưa có xác nhận hoàn thành niêm yết. Người nhận viện không có ai cùng chia để yêu cầu công chứng ngay; không có khiếu nại đã ghi nhận. Chọn kết luận đúng về những bước vẫn phải có.',[
 ('Không có khiếu nại và chỉ một người thì đủ thay xác nhận niêm yết; bộ giấy tờ đầy đủ đã loại nguy cơ người khác.','Khoản 4,5 Điều 59 vẫn yêu cầu thủ tục niêm yết và xác nhận; không chỉ việc hiện chưa có khiếu nại.')],
 'Không đồng nhất hồ sơ đủ, ít người hưởng và chưa có khiếu nại với đã hoàn thành niêm yết.')
r(97,'A,B ký hợp đồng vì lợi ích C. C đã đồng ý hưởng nhưng chưa nhận gì; A,B cùng muốn sửa bỏ lợi ích C, C không đồng ý. Họ viện quyền sửa theo thỏa thuận và việc chưa thực hiện để giải quyết. Chỉ xét giới hạn này, nhận định nào đúng?',[
 ('A,B được sửa vì đồng thuận hai người giao kết đủ theo quy tắc chung, C chưa thực hiện nghĩa vụ nào.', 'Điều 417 đặt giới hạn riêng sau C đồng ý hưởng, không đòi C có nghĩa vụ hoặc đã nhận.'),
 ('A,B được hủy để lập hợp đồng mới, vì giới hạn chỉ cấm sửa chứ không cấm hủy trước khi thực hiện.', 'Điều 417 cấm cả sửa hoặc hủy theo nhánh này nếu không được C đồng ý.'),
 ('C chỉ có quyền đòi bồi thường về sau, không thể giới hạn việc sửa trước khi nhận lợi ích.', 'Luật bảo vệ quyền hưởng đã được chấp thuận ngay cả trước thực hiện, không chỉ bồi thường sau.')],
 'Áp quy tắc riêng trước quyền sửa chung; đánh giá sửa và hủy, không lấy chưa nhận thực tế để xóa quyền của C.')
r(98,'A ủy quyền B thu tiền, B đã nhận tài sản và lợi ích; không thỏa thuận cho B giữ. B báo tổng số, tự khấu trừ mọi lợi ích làm công rồi chia sẻ thông tin cho người ngoài để chứng minh đã làm. Chọn các kết luận đúng về giao lại, thông báo đầy đủ và giữ bí mật.',[
 ('B có thể giữ toàn lợi ích nếu đã báo tổng thu; nghĩa vụ giao lại chỉ áp tài sản A giao ban đầu.','Điều 565,568 áp tài sản và lợi ích thu được khi thực hiện, không chỉ tài sản được giao từ đầu.')],
 'Tách nghĩa vụ báo cáo, giao tài sản và giữ bí mật; không coi một nghĩa vụ đã làm đủ thay hai nghĩa vụ khác.')
r(99,'A,B thỏa thuận ủy quyền không thù lao. B bỏ ba triệu chi phí hợp lý cần thiết, thực hiện đúng việc, có chứng từ; đòi hoàn chi phí và hai triệu tiền công vì A đã hưởng lợi. Không thỏa thuận khác. Tổng khoản có căn cứ trong yêu cầu này và phân loại nào đúng?',[
 ('Không khoản nào, vì miễn thù lao bao gồm mọi chi phí người thực hiện tự bỏ ra.', 'Không thù lao không miễn hoàn chi phí hợp lý theo luật.'),
 ('Năm triệu, vì hưởng lợi từ công việc tự phát sinh cả hoàn phí lẫn thù lao dù chưa thỏa thuận.', 'Thù lao cần thỏa thuận, khác khoản hoàn chi phí hợp lý.'),
 ('Hai triệu tiền công; chi phí B tự chi không thuộc nghĩa vụ A vì A không trực tiếp thanh toán.', 'Chi phí hợp lý người nhận bỏ ra đúng công việc thuộc nghĩa vụ hoàn, không cần A trực tiếp chi.')],
 'Phân biệt căn cứ hoàn phí và tiền công; không dùng giá trị A hưởng hoặc người trực tiếp chi thay thỏa thuận thù lao.')
r(100,'G được thay hợp pháp bằng H, G còn sống; người được giám hộ cũng còn sống, không thuộc nhánh chuyển do G chết. Có tài sản và quyền, nghĩa vụ từ việc giám hộ cần bàn giao. G đề nghị chỉ ký biên nhận giấy tờ, không ghi tình trạng tài sản hoặc mời chủ thể chứng kiến, sau ba tháng mới quyết toán. Cách làm đúng là gì?',[
 ('G có ba tháng, biên nhận giấy tờ của H đủ thay văn bản về tình trạng tài sản nếu không tranh chấp.', 'Nhánh thay người giám hộ theo khoản 1,2 Điều 61 có hạn 15 ngày và yêu cầu văn bản, chứng kiến.'),
 ('G bàn giao trong 15 ngày nhưng tự chuyển sở hữu tài sản sang H để H chịu toàn bộ nghĩa vụ.', 'Chuyển giao giám hộ không chuyển tài sản người được giám hộ thành sở hữu người mới.'),
 ('G,H tự ký văn bản có đủ tài sản là đủ; việc chứng kiến chỉ cần nếu G không đồng ý thay.', 'Khoản 2 đặt việc cơ quan cử/chỉ định và người giám sát chứng kiến, không phụ thuộc G phản đối.')],
 'Xác định đúng nhánh thay, thời hạn và nội dung bàn giao; phân biệt quản lý với sở hữu, không bỏ chứng kiến vì đồng thuận.')
# Keep correct options concise where long answers previously disclosed the key.
short={
 12:'30, 10, 3 năm; còn thời hiệu hai yêu cầu đầu, đã hết ở yêu cầu thứ ba.',
 22:'Chưa chấp nhận: im lặng không có thỏa thuận, phản hồi còn điều kiện giá.',
 33:'Chưa hết hai năm tính từ 10/01/2026, mốc A biết việc lừa dối.',
 47:'Trần trách nhiệm: A 400 triệu, B 200 triệu; không đòi bù bằng tiền riêng.',
 60:'Y sửa đủ bản gốc và báo bằng văn bản trong 3 ngày làm việc từ hoàn tất.',
 61:'Cả hai đánh số liên tục qua lời chứng; I giáp lai hai tờ, II chỉ một tờ.',
 64:'A,B áp dụng từ đăng ký; C,D thiếu điều kiện lập trước của cơ chế ban đầu.',
 65:'A miễn giấy tờ đã khai thác, chịu phí theo luật; B chưa đáp ứng ngoại lệ.',
 72:'Không quá 20 năm; khi không định hạn, báo bằng văn bản trước ít nhất sáu tháng.',
 79:'Không thỏa thuận thì bán đấu giá; nhận chính tài sản cần thỏa thuận theo nhánh này.',
 89:'Không đáp ứng tự viết, ký của hình thức không có người làm chứng đang viện dẫn.',
 93:'Mỗi A,B trả C 200 triệu theo giá lúc chia, không chia lại hiện vật.',
 100:'Trong 15 ngày, G bàn giao bằng văn bản đủ nội dung, có chủ thể luật định chứng kiến.'}
for n,text in short.items():
 q=qs[f'CAL26-{n:03}'];assert q['type']=='single'
 next(a for a in q['answers'] if a['correct'])['text']=text

assert set(changes)==set(range(1,101))
# A revised distractor in 46 now also tests destination of the ineffective portion.
qs['CAL26-046']['legalBasis'].append(dict(document=DS,article='Khoản 2 Điều 650',url=DSURL))
def digest(q):return hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
register=[]
for key,q in qs.items():
 before=old[key]
 assert q['answerKey']==before['answerKey']
 assert q['part']==before['part'] and q['type']==before['type']
 assert [a['correct'] for a in q['answers']]==[a['correct'] for a in before['answers']]
 assert q['question']['variants']!=before['question']['variants']
 assert any(a['text']!=b['text'] for a,b in zip(q['answers'],before['answers']))
 assert len({a['text'] for a in q['answers']})==4
 assert all(a['explanation'] for a in q['answers'])
 register.append({'id':key,'answerKeyBefore':before['answerKey'],'answerKeyAfter':q['answerKey'],
  'beforeSHA256':digest(before),'afterSHA256':digest(q),'stemRewritten':True,
  'changedOptions':[a['id'] for a,b in zip(q['answers'],before['answers']) if a['text']!=b['text']],
  'cognitiveTask':q['difficultyRationale'],'basis':q['legalBasis']})
assert len({q['question']['variants'][0] for q in qs.values()})==100
for f,arr in banks.items():(ROOT/'data'/f).write_text(json.dumps(arr,ensure_ascii=False,indent=2)+'\n')
report={'date':'2026-10-12','beforeCommit':'18a5deaa69096772ae5318b7d8162e740a9f19ed',
 'scope':'CAL26-001 through CAL26-100; 100 stems rewritten and option sets substantively revised; no expansion of eligible bank.',
 'difficulty':'100 advanced scenario targets; estimated, not empirically calibrated. A longer stem alone is not counted as improvement.',
 'answerPolicy':'Preserved question IDs, part, single/multiple type and original correct sets. Each changed distractor has a matched explanation; true text updated where the tested factual branch changed.',
 'questions':register}
(ROOT/'reports/difficulty-upgrade-100-2026-10-12.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rewritten':len(qs),'changedOptions':sum(len(x['changedOptions']) for x in register),'unchangedCorrectSets':100},ensure_ascii=False))
