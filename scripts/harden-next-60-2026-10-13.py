"""Sixty independently authored cases outside the previous 296 reviewed IDs."""
import json, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=(ROOT/'scripts/harden-easy-40-2026-10-13.py').read_text()
preamble=base[:base.index("case('IMP-T60-051',")]
preamble=preamble.replace('APPLICATION40-20261013','CONTINUATION60-20261013').replace('APPLICATION_40_ESTIMATED_PENDING_TRIAL','CONTINUATION_60_ESTIMATED_PENDING_TRIAL').replace('application-40-legal-review','continuation-60-legal-review')
exec(preamble)
previous_ids=set()
for filename in ['scenario-refinements-2026','scenario-refinements-remaining-2026','scenario-priority-129-2026','scenario-application-40-2026']:
 for row in json.loads((ROOT/f'data/{filename}.json').read_text())['questions']:
  bank[row['id']]=row['after'];previous_ids.add(row['id'])
assert len(previous_ids)==296
evidence['LD:14']={'reference':{'document':'Bộ luật Lao động số 45/2019/QH14 đối chiếu VBHN 18/VBHN-VPQH năm 2026','article':'Điều 14','url':'https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-18-vbhn-vpqh-468971.htm'},'excerpt':'1. Hợp đồng lao động phải được giao kết bằng văn bản và được làm thành 02 bản, người lao động giữ 01 bản, người sử dụng lao động giữ 01 bản, trừ trường hợp quy định tại khoản 2 Điều này. Hợp đồng lao động được giao kết thông qua phương tiện điện tử dưới hình thức thông điệp dữ liệu theo quy định của pháp luật về giao dịch điện tử có giá trị như hợp đồng lao động bằng văn bản. 2. Hai bên có thể giao kết hợp đồng lao động bằng lời nói đối với hợp đồng có thời hạn dưới 01 tháng, trừ trường hợp quy định tại khoản 2 Điều 18, điểm a khoản 1 Điều 145 và khoản 1 Điều 162 của Bộ luật này.','origin':'Đối chiếu Điều 14 BLĐ với nguồn Công báo và VBHN 18 năm 2026 ngày 13/10/2026; Điều 16 là nghĩa vụ thông tin, không dùng cho yêu cầu hình thức.'}


case('COMP26-CT-015',
'A yêu cầu chứng thực chữ ký trên giấy thực chất là hợp đồng bán nhà, không thuộc ngoại lệ được chứng thực chữ ký đối với nội dung giao dịch. Người thực hiện từ chối vì sai thủ tục nhưng chỉ ghi lý do vào sổ nội bộ, không giao giải thích bằng văn bản. A đề nghị đổi tên giấy thành cam kết để ký tiếp. Hướng xử lý cả nội dung và việc từ chối?',
'Không dùng đổi tên để chứng thực chữ ký thay thủ tục giao dịch; việc từ chối phải được giải thích rõ lý do bằng văn bản cho A.',
[('Đổi tiêu đề thành cam kết thì chứng thực chữ ký được; lý do nội bộ chỉ cần giao nếu A khiếu nại sau đó.','Tên giấy không đổi bản chất giao dịch, quyền được biết lý do không chờ khiếu nại.'),
('Từ chối chứng thực chữ ký là phù hợp; chỉ ghi nội bộ đã đủ vì thiếu thẩm quyền theo thủ tục nên không có nghĩa vụ giải thích.','Nhận đúng việc từ chối nhưng bỏ nghĩa vụ giải thích bằng văn bản.'),
('Phải giao lý do bằng văn bản; sau đó chứng thực chữ ký nếu A cam kết chấp nhận rủi ro và không yêu cầu chứng thực giao dịch.','Cam kết không tạo ngoại lệ cho giao dịch không thuộc nhánh chứng thực chữ ký.')],
'Phải xét nội dung chứ không chỉ tên giấy: giao dịch bán nhà không thuộc ngoại lệ đã nêu thì không dùng chứng thực chữ ký để thay thủ tục giao dịch. Điều 25 loại nhánh này; Điều 9 yêu cầu giải thích rõ lý do từ chối bằng văn bản. Hai việc độc lập, ghi sổ nội bộ và cam kết tự chịu rủi ro không thay được.',
'CT:9 CT:25',['Nhận diện bản chất giao dịch trong giấy','Kiểm tra ngoại lệ chứng thực chữ ký','Kiểm tra nghĩa vụ giải thích việc từ chối'])

case('IMP-T60-065',
'A thế chấp nhà cho ngân hàng G. B là người thứ ba muốn bỏ tiền cải tạo; A đã đồng ý nhưng G chưa đồng ý. Không có thỏa thuận riêng thay quy tắc. Sau đó dự án làm giảm giá trị nhà thế chấp và gây thiệt hại G có chứng cứ. B nói chủ nhà đã cho phép nên G không được yêu cầu dừng hay đòi bồi thường. Kết luận đúng?',
'Đầu tư của B còn cần G đồng ý; khi giảm giá trị G có quyền yêu cầu chấm dứt, thiệt hại do vi phạm quy định đầu tư phải được xem xét bồi thường.',
[('A đồng ý đã đủ cho B đầu tư; G chỉ yêu cầu dừng khi khoản vay quá hạn, không xét thiệt hại trước ngày đến hạn.','Thiếu đồng ý của bên nhận thế chấp và đặt điều kiện quá hạn không có trong nhánh đầu tư.'),
('Phải có G đồng ý nhưng khi công trình đã làm xong G không có quyền yêu cầu chấm dứt; chỉ cộng giá đầu tư vào tài sản thế chấp.','Bỏ quyền yêu cầu chấm dứt khi đầu tư giảm giá trị và đồng nhất giá chi đầu tư với tăng giá trị.'),
('G yêu cầu chấm dứt được; vì A đồng ý nên thiệt hại không thể bồi thường dù B vi phạm điều kiện và quan hệ nhân quả đã chứng minh.','Đồng ý của chủ nhà không miễn trách nhiệm do vi phạm quy định gây thiệt hại bên nhận thế chấp.')],
'Khoản 2 Điều 20 NĐ21 yêu cầu bên nhận thế chấp đồng ý khi người thứ ba đầu tư. Khoản 3 cho yêu cầu chấm dứt nếu đầu tư giảm giá trị; khoản 4 đặt bồi thường khi không tuân thủ quy định và gây thiệt hại. Phải tách đồng ý chủ sở hữu, điều kiện bên nhận thế chấp và trách nhiệm thiệt hại, không đợi nợ quá hạn mới xét.',
'ND21:20 DS:321',['Xác định B là người thứ ba đầu tư','Kiểm tra đồng ý của bên nhận thế chấp','Xét giảm giá trị và thiệt hại do vi phạm'])

case('REFIN26-DAT-012',
'Hồ sơ I là đất chung A–W, vợ chồng không có thỏa thuận ghi một tên nhưng muốn cấp chỉ A theo mẫu chủ hộ. Hồ sơ II là quyền đất chung B,C,D, không yêu cầu một giấy chung, chưa tách thửa; B nghĩ giấy cấp riêng sẽ tạo phần đất riêng theo bản vẽ tự làm. Chỉ xét tên và số giấy, phương án xử lý cả hai đúng?',
'I phải thể hiện cả A–W khi không có thỏa thuận khác; II cấp từng người giấy thể hiện quyền chung theo luật, không tự tạo phần đất riêng của B.',
[('I chỉ ghi A vì là chủ hộ; II cấp từng người giấy nhưng mỗi giấy tự tạo một thửa theo phần họ lựa chọn.','Sai nguyên tắc tên vợ chồng và nhầm cấp giấy với phân chia quyền, thửa.'),
('I ghi cả A–W; II bắt buộc một giấy chung dù không có yêu cầu vì chưa tách thửa không thể cấp từng người giấy.','Nhận đúng tên vợ chồng nhưng bỏ cơ chế giấy cấp mỗi người cho quyền chung.'),
('I chỉ ghi A; II cấp mỗi người giấy thể hiện quyền chung, rồi B được tự quyết định ranh giới phần đất mình bán.','Sai nhánh vợ chồng và suy giấy riêng thành quyền định đoạt phần đất riêng chưa được xác lập.')],
'Điều 135 và Điều 34 HNGĐ giữ tên vợ và chồng cho đất chung khi không thỏa thuận khác. Quyền sử dụng chung nhiều người khác có thể được cấp mỗi người giấy nếu không yêu cầu chung một giấy. Hai cấu hình không nên áp cùng mẫu chủ hộ hoặc suy từ số giấy sang quyền đã chia, thửa đã tách; cấp giấy ghi nhận quyền, không tự tạo ranh giới B.',
'DD:135 HN:34',['Phân biệt quyền chung vợ chồng và nhiều người','Kiểm tra thỏa thuận tên cùng yêu cầu cấp giấy','Tách số giấy khỏi việc chia quyền và tách thửa'])

case('REFIN26-CC-030',
'P là Văn phòng DNTN đã hoạt động hợp pháp ba năm. K đã hành nghề CCV ba năm nhưng mới chấm dứt tư cách hợp danh ở Q một năm trước; K muốn mua P và thuê người khác làm Trưởng. Không có ngoại lệ luật. Hai bên cho rằng P và K đều vượt mốc hai năm nên đủ. Chỉ xét điều kiện người mua, hướng xử lý?',
'Còn thiếu thời gian hai năm sau chấm dứt hợp danh và cam kết K hành nghề làm Trưởng P; kinh nghiệm và tuổi hoạt động P không thay hai điều kiện đó.',
[('K đủ điều kiện vì đã hành nghề ba năm; thuê CCV khác làm Trưởng đáp ứng cam kết hành nghề của tổ chức được mua.','Nhầm cam kết cá nhân K làm Trưởng với việc P có người làm Trưởng, bỏ mốc chấm dứt hợp danh.'),
('K chỉ cần cam kết làm Trưởng P; mốc hai năm sau chấm dứt hợp danh được cộng với ba năm đã hành nghề để coi đủ.','Các mốc độc lập không được cộng kinh nghiệm vào thời gian kể từ chấm dứt tư cách.'),
('K chỉ cần chờ thêm một năm; đủ mốc thì được thuê người làm Trưởng vì mua lại không phải thành lập Văn phòng mới.','Đúng mốc còn thiếu nhưng bỏ cam kết người mua trực tiếp hành nghề với tư cách Trưởng.')],
'Điều 31 tách tuổi hoạt động Văn phòng, kinh nghiệm người mua, thời gian từ chấm dứt tư cách trước và cam kết hành nghề làm Trưởng nơi mua. P đủ tuổi hoạt động và K đủ kinh nghiệm không thay hai điều kiện còn thiếu. Không cộng các mốc hoặc chuyển cam kết cá nhân sang hợp đồng thuê người khác.',
'CC:31 CC:9',['Phân biệt tuổi hoạt động P và kinh nghiệm K','Tính thời gian sau chấm dứt hợp danh','Kiểm tra cam kết trực tiếp làm Trưởng nơi mua'])

case('VER26-058',
'W được giao đất theo chính sách khoản 3 Điều 16, hồ sơ xác định đất riêng. W muốn bán cho N không thuộc hàng thừa kế của W, dù N thuộc đối tượng chính sách khoản 2 Điều 16. Chồng W đã ký đồng ý. Các điều kiện khác đủ. Chỉ xét tính chất tài sản và điều kiện người nhận, kết luận đúng?',
'Đất riêng và chữ ký chồng không thay điều kiện đặc thù; N thuộc đối tượng chính sách nhưng thiếu quan hệ hàng thừa kế nên chưa đủ nhận theo nhánh này.',
[('Đất riêng W thì N được nhận khi đủ đối tượng chính sách; quan hệ hàng thừa kế chỉ cần cho tặng cho, không cần cho bán.','Điều 48 đặt điều kiện cùng cho chuyển nhượng và tặng cho thuộc nhánh được phép.'),
('N được nhận vì chồng đã đồng ý, chữ ký hai vợ chồng mở quyền chuyển nhượng cho người không thuộc hàng thừa kế.','Đồng ý của vợ chồng không tạo ngoại lệ cho chế độ đất chính sách.'),
('N chưa đủ vì đất W mặc nhiên thành tài sản chung khi chồng ký; phải chia lại tài sản vợ chồng trước xét chính sách.','Chấp thuận giao dịch không tự nhập đất riêng thành chung và không chữa điều kiện người nhận.')],
'Điều 43 phân loại đất riêng theo dữ kiện nhưng quyền định đoạt còn chịu luật đất đai. Khoản 1 Điều 48 đòi người nhận vừa thuộc hàng thừa kế vừa thuộc đối tượng khoản 2 Điều 16. N chỉ đáp ứng vế chính sách; chữ ký chồng không bổ sung quan hệ và không tự đổi nguồn quyền của đất.',
'HN:43 DD:48',['Giữ tính chất riêng của đất','Kiểm tra đồng thời hai điều kiện người nhận','Phân biệt đồng ý vợ chồng với ngoại lệ đất chính sách'])

case('FAM26-017',
'A–W có chế độ tài sản theo thỏa thuận hợp lệ. Ngày 1/10 họ ký giấy tại nhà đổi cách phân nợ, ngày 15/10 mới công chứng sửa đổi. Ngân hàng có quyền tài sản phát sinh ngày 5/10; không đồng ý sửa quyền của mình và không có thỏa thuận khác giữa các bên liên quan. A–W muốn ghi đổi chế độ từ 1/10 để loại nghĩa vụ ngân hàng. Hướng đánh giá?',
'Sửa đổi có hiệu lực từ ngày được công chứng 15/10; quyền, nghĩa vụ đã phát sinh trước đó không tự mất do giấy ký 1/10 hoặc thỏa thuận nội bộ.',
[('Sửa đổi có hiệu lực 1/10 do cả hai đã ký; công chứng 15/10 chỉ xác nhận nên quyền ngân hàng phát sinh 5/10 bị loại.','Nhầm thời điểm ký giấy thường với thời điểm công chứng hoặc chứng thực của sửa đổi.'),
('Sửa đổi có hiệu lực 15/10 nhưng từ đó xóa mọi quyền ngân hàng phát sinh trước, dù ngân hàng không đồng ý thay quyền.','Bỏ quy tắc bảo toàn quyền, nghĩa vụ phát sinh trước sửa đổi khi không có thỏa thuận khác.'),
('Chế độ không được sửa trong hôn nhân; cần ly hôn trước rồi ngân hàng mới được thông báo chế độ tài sản mới.','Luật cho sửa chế độ trong thời kỳ hôn nhân với hình thức phù hợp, không đòi ly hôn.')],
'Điều 49 và NĐ126 cho sửa nội dung chế độ trong hôn nhân nhưng phải công chứng hoặc chứng thực; Điều 18 gắn hiệu lực ngày đó và bảo toàn quyền, nghĩa vụ phát sinh trước, trừ thỏa thuận khác. Ngân hàng không đồng ý thay quyền, nên giấy 1/10 và thay đổi nội bộ không tự có hiệu lực hồi tố để loại nghĩa vụ ngày 5/10.',
'HN:49 ND126:17 ND126:18',['Phân biệt ngày ký và ngày công chứng sửa đổi','Xác định quyền ngân hàng phát sinh trước hiệu lực','Kiểm tra có thỏa thuận thay quyền với bên liên quan hay không'])

case('IMP-SEP24-039',
'P phân công CCV K hướng dẫn hai người tập sự, trong giới hạn số lượng. Nhưng K đang bị tạm đình chỉ hành nghề theo quyết định còn hiệu lực. P còn L đủ điều kiện, chưa vượt giới hạn hướng dẫn. K đề nghị vẫn nhận vì không thu tiền và L chỉ ký nhật ký thay. Hướng xử lý?',
'K phải từ chối hướng dẫn khi không đủ điều kiện; P cần bố trí L đúng thủ tục nếu đủ điều kiện, không dùng L ký thay hoạt động K hướng dẫn.',
[('K hướng dẫn được vì không thu tiền; L ký nhật ký để chịu trách nhiệm chuyên môn thay K mà không cần đổi phân công.','Miễn tiền không thay điều kiện hướng dẫn và chữ ký phải gắn hoạt động hướng dẫn thật.'),
('K hướng dẫn được vì chỉ hai người, chưa vượt số lượng; tạm đình chỉ chỉ ngăn ký chứng nhận chứ không ảnh hưởng điều kiện hướng dẫn.','Giới hạn số lượng không chữa tình trạng không đủ điều kiện hướng dẫn.'),
('K từ chối, cả hai người phải xóa thời gian đã tập sự và đăng ký lại dù P có L đủ điều kiện thay theo thủ tục.','Không được tự suy thay người hướng dẫn thành chấm dứt và xóa toàn bộ thời gian.')],
'Điều 13 TT6 yêu cầu CCV từ chối hướng dẫn nếu không đủ điều kiện Luật Công chứng; điều kiện không chỉ là số người được phân công. P có người khác phù hợp thì thực hiện việc phân công, thay đổi đúng quy định. Không dùng ký thay nhật ký để hợp thức người bị đình chỉ hoặc tự xóa thời gian tập sự vì chỉ đổi người hướng dẫn.',
'TT6:13 CC:12 TT6:6',['Kiểm tra tình trạng K ngoài giới hạn số lượng','Xác định nghĩa vụ từ chối và người có thể thay','Phân biệt đổi người hướng dẫn với xóa thời gian tập sự'])

case('IMP-SEP24-047',
'K từng bị miễn nhiệm CCV do kết án tội cố ý, nay đã được xóa án tích, có giấy nhận làm việc của P và đã đáp ứng các tiêu chuẩn chung khác. L từng tự nguyện xin miễn nhiệm, hiện không thuộc căn cứ cấm, đáp ứng tiêu chuẩn và thủ tục để được xem xét lại. Chỉ xét hai căn cứ miễn nhiệm, nhận định đúng?',
'K vẫn thuộc nhánh không được bổ nhiệm lại dù xóa án tích; căn cứ tự nguyện của L không tự tạo cùng lệnh cấm, còn phải được xem xét theo điều kiện và thủ tục.',
[('K và L đều được tự khôi phục chức danh vì hiện đủ tiêu chuẩn, không còn áp dụng căn cứ miễn nhiệm cũ.','Bỏ lệnh cấm riêng của tội cố ý và nhầm xem xét bổ nhiệm lại với tự khôi phục.'),
('K được xem xét sau xóa án tích, L không được vì mọi trường hợp miễn nhiệm đều có cùng hậu quả cấm bổ nhiệm lại.','Đảo hai căn cứ, xóa án tích không loại lệnh cấm riêng ở K.'),
('K và L đều phải bị loại vĩnh viễn vì đã miễn nhiệm; giấy nhận làm việc và tiêu chuẩn hiện tại không liên quan việc xem xét lại.','Mở rộng căn cứ loại riêng thành cấm tất cả trường hợp đã miễn nhiệm.')],
'Điều 17 yêu cầu phân loại căn cứ miễn nhiệm trước khi xét bổ nhiệm lại. Nhánh bị kết án về tội cố ý bị loại kể cả đã xóa án tích; giấy làm việc không thay căn cứ này. Tự nguyện miễn nhiệm không tự đồng nhất với nhánh cấm đó; L vẫn cần đủ tiêu chuẩn, không thuộc cấm và hoàn thành thủ tục xem xét, không tự khôi phục chức danh.',
'CC:17 CC:14',['Phân loại căn cứ miễn nhiệm từng người','Kiểm tra tác động của xóa án tích','Phân biệt được xem xét lại với tự khôi phục chức danh'])

case('IMP-T60-020',
'N là cá nhân nước ngoài đủ điều kiện mua căn hộ, không có ngoại lệ hôn nhân, chưa xét gia hạn. Hợp đồng thỏa thuận sở hữu 40 năm; N đặt cọc ngày 1/2/2026, được cấp giấy ngày 1/8/2026. N muốn ghi 50 năm vì luật cho tối đa 50, tính từ đặt cọc. Chỉ xét thời hạn theo dữ kiện, cách ghi phù hợp?',
'40 năm theo thỏa thuận, tính từ cấp giấy 1/8/2026; giới hạn 50 năm không tự thay thỏa thuận 40 năm hoặc mốc đặt cọc.',
[('50 năm từ cấp giấy 1/8/2026 vì trần luật thay mọi thời hạn ngắn hơn được ghi trong hợp đồng.','Nhầm thời hạn tối đa với thời hạn bắt buộc được sở hữu.'),
('40 năm từ đặt cọc 1/2/2026 vì đã thanh toán để giữ căn hộ, ngày cấp giấy chỉ chứng minh thời hạn còn lại.','Dùng mốc đặt cọc thay ngày được cấp giấy theo nhánh sở hữu của cá nhân nước ngoài.'),
('50 năm từ đặt cọc 1/2/2026 vì cả hạn luật và mốc thanh toán đều ưu tiên so với ngày cấp giấy và hợp đồng.','Sai cả việc áp trần thay thỏa thuận và ngày bắt đầu thời hạn.')],
'Điều 20 quy định theo thỏa thuận nhưng không quá 50 năm từ ngày cấp giấy cho cá nhân nước ngoài thuộc nhánh này. Thỏa thuận 40 năm trong trần được giữ, không tự nâng thành 50. Đặt cọc không phải ngày cấp giấy và không tự khởi đầu thời hạn; đề đã loại ngoại lệ hôn nhân và gia hạn để giữ đúng phạm vi.',
'NHA:20 DS:328',['Phân biệt thỏa thuận thực tế và trần thời hạn','Chọn ngày cấp giấy thay mốc cọc','Kiểm tra không có ngoại lệ hoặc gia hạn trong đề'])

case('IMP-T60-029',
'A thuê khoán đàn gia súc của B. Không thỏa thuận khác về hoa lợi hoặc rủi ro. Trong hạn thuê có 8 con sinh ra; một sự kiện được xác định bất khả kháng gây thiệt hại 60 triệu đối với đàn thuê, A không có lỗi và không có căn cứ trách nhiệm khác. A muốn nhận cả 8 con và không chịu thiệt hại vì không có lỗi. Phân bổ mặc định đúng?',
'A hưởng 4 con và chịu 30 triệu thiệt hại theo quy tắc thuê khoán; việc không có lỗi không tự loại phần rủi ro được luật phân bổ.',
[('A hưởng 8 con và chịu 30 triệu thiệt hại; bỏ công chăm sóc cho A toàn bộ hoa lợi nhưng rủi ro vẫn chia đôi.','Bỏ quy tắc một nửa gia súc sinh ra khi không có thỏa thuận khác.'),
('A hưởng 4 con và không chịu thiệt hại; bất khả kháng miễn mọi rủi ro dù luật riêng về thuê khoán đã phân bổ.','Nhầm miễn trách nhiệm do vi phạm với phân bổ thiệt hại trong thuê khoán gia súc.'),
('A hưởng 4 con và chịu 60 triệu; người đang giữ đàn chịu toàn bộ thiệt hại vì có nghĩa vụ bảo quản.','Đề xác định bất khả kháng, không lỗi và không căn cứ khác nên không thay phân bổ một nửa bằng toàn bộ.')],
'Điều 491 đặt quy tắc mặc định trong thời hạn thuê khoán: hưởng một nửa gia súc sinh ra, chịu một nửa thiệt hại về gia súc do bất khả kháng, trừ thỏa thuận khác. Đề đã loại thỏa thuận và lỗi khác. Vì vậy là 4 con và 30 triệu; không dùng lập luận không có lỗi để bỏ cách luật riêng phân rủi ro.',
'DS:491',['Kiểm tra loại hợp đồng và không có thỏa thuận khác','Chia hoa lợi sinh trong thời hạn thuê','Phân biệt rủi ro mặc định với trách nhiệm do có lỗi'])

case('IMP-T60-085',
'A mới xin giao đất, chưa được xác lập quyền sử dụng. A muốn bảo đảm khoản vay bằng quyền đất dự kiến và máy sẽ mua, máy thuộc loại được dùng bảo đảm, mô tả xác định được. Các điều kiện khác của tài sản tương lai máy đủ. Ngân hàng đồng ý cả hai nên A cho rằng cùng là tài sản tương lai. Kết luận đúng về hai đối tượng?',
'Máy có thể xét theo cơ chế tài sản hình thành trong tương lai; không áp chính cơ chế ấy cho quyền sử dụng đất dự kiến chỉ vì ngân hàng đồng ý.',
[('Máy và quyền đất đều dùng cơ chế tương lai được vì chưa hình thành, ngân hàng đồng ý thay điều kiện của từng loại tài sản.','Bỏ ngoại lệ loại quyền sử dụng đất khỏi cơ chế tại khoản 4 Điều 10 NĐ21.'),
('Quyền đất dùng được do A đã nộp đơn, còn máy không dùng được vì A chưa mua nên chưa là chủ sở hữu hiện tại.','Đảo phạm vi tài sản tương lai được xét và trường hợp đất bị loại khỏi cơ chế này.'),
('Cả máy và quyền đất đều không dùng được trước khi A sở hữu; BLDS không chấp nhận tài sản bảo đảm hình thành sau.','Bỏ quy tắc cho tài sản bảo đảm có thể hiện có hoặc hình thành trong tương lai.')],
'Điều 295 BLDS cho tài sản bảo đảm có thể hình thành trong tương lai trong điều kiện phù hợp. Khoản 4 Điều 10 NĐ21 hướng dẫn cơ chế này nhưng không áp dụng đối với quyền sử dụng đất. Phải phân loại hai đối tượng, không suy từ ngân hàng đồng ý hoặc giấy nộp đơn giao đất để tạo quyền chưa có hay xóa ngoại lệ.',
'DS:295 ND21:10',['Phân loại máy và quyền đất dự kiến','Kiểm tra điều kiện tài sản tương lai của máy','Áp ngoại lệ không áp cơ chế này đối với quyền sử dụng đất'])

case('VER26-052',
'W có đất giao theo khoản 3 Điều 16. Hai người muốn nhận tặng cho: C là con ruột nhưng không thuộc đối tượng khoản 2 Điều 16; S là chị ruột, thuộc hàng thừa kế và đúng đối tượng khoản 2. Các điều kiện khác đủ, không có ngoại lệ khác. W nói con được ưu tiên nên C nhận được, S chỉ nhận khi không còn con. Chỉ xét điều kiện người nhận, chọn nhận định?',
'C thiếu vế đối tượng chính sách; S đáp ứng hai vế đã nêu, không bị loại chỉ vì W còn con thuộc hàng trước.',
[('C nhận được vì là con; S không nhận vì chỉ khi không có người hàng thứ nhất mới được xét chị ruột nhận tặng cho.','Nhầm điều kiện thuộc hàng thừa kế với thứ tự được gọi hưởng khi mở thừa kế, bỏ vế đối tượng chính sách.'),
('C và S đều nhận được vì đều có quan hệ thân thích, điều kiện khoản 2 Điều 16 chỉ dùng cho giao đất lần đầu.','Quan hệ thân thích không thay hai điều kiện của người nhận đất chính sách.'),
('C và S đều không nhận được vì đất chính sách chỉ tặng cho người có cùng hàng với nhau, không lựa chọn khác hàng.','Đặt điều kiện cùng hàng không có trong nhánh tặng cho của Điều 48.')],
'Khoản 1 Điều 48 dùng hai tiêu chí đồng thời: thuộc hàng thừa kế và là đối tượng khoản 2 Điều 16. Con không đủ vế chính sách thì thiếu điều kiện; chị ruột thuộc hàng thừa kế, đúng đối tượng thì không bị loại chỉ vì còn người hàng trước. Đây là tặng cho khi W sống, không phải quy tắc chỉ gọi hàng sau khi chia thừa kế tại Điều 651.',
'DD:48 DS:651',['Kiểm tra hai tiêu chí đối với từng người nhận','Phân biệt thuộc hàng thừa kế và thứ tự hưởng di sản','Áp đúng tặng cho khi người sử dụng còn sống'])

case('VER26-055',
'A có đất giao theo khoản 3 Điều 16; công ty một thành viên do con A làm chủ muốn nhận góp vốn đất. Con thuộc hàng thừa kế và đúng đối tượng chính sách. A cho rằng nhận qua công ty của con tương đương tặng đất trực tiếp cho con; DN35 cho góp vốn bằng quyền đất nên được. Chỉ xét chủ thể và hạn chế đặc thù, kết luận?',
'Công ty và người con là chủ thể khác nhau; quyền góp vốn chung không tạo ngoại lệ góp đất chính sách bị hạn chế theo Điều 48.',
[('Công ty do con làm chủ được nhận như chính con vì quyền đất chỉ đổi tên sang tài sản góp vốn, không đổi người kiểm soát.','Đồng nhất công ty với chủ sở hữu là cá nhân và mở rộng ngoại lệ tặng cho sang góp vốn.'),
('Công ty được nhận nếu con cam kết giữ vốn; góp vốn được xem là chuyển nhượng cho người thuộc hàng thừa kế.','Cam kết giữ vốn không đổi loại giao dịch hoặc tạo ngoại lệ góp vốn.'),
('Không được góp vốn nhưng nếu ghi tên con trên giấy đất, việc công ty sử dụng sẽ tự trở thành quyền đất của công ty.','Ghi tên cá nhân không tự chuyển quyền cho công ty hoặc hợp thức cấu trúc góp đất bị hạn chế.')],
'DN35 thừa nhận việc góp vốn bằng quyền sử dụng đất với điều kiện hợp pháp nhưng không loại luật đất đai đặc thù. Điều 48 hạn chế góp vốn đối với đất chính sách; ngoại lệ để thừa kế, tặng cho, chuyển nhượng cho cá nhân đủ điều kiện không tự mở sang công ty của người đó. Phải nhận đúng người nhận quyền và bản chất giao dịch.',
'DD:48 DN:35',['Phân biệt công ty và người chủ là con A','Xác định góp vốn khác tặng cho trực tiếp','Đối chiếu quyền góp vốn chung với hạn chế đất chính sách'])

case('VER26-064',
'A và con B chết trong cùng tai nạn, không xác định ai chết trước. A có 600 triệu riêng, không di chúc hoặc nợ; vợ, cha mẹ A đã chết, hàng thứ nhất chỉ con C còn sống và nhánh B có con D. Những người khác không có. Chỉ xét di sản A, kết quả đúng?',
'B không hưởng di sản A; C nhận 300 triệu, D nhận 300 triệu theo thế vị nhánh B, không chuyển phần qua di sản B.',
[('B nhận 300 triệu vì mặc định trẻ hơn chết sau; C 300 triệu, phần B mới chuyển cho D qua thừa kế của B.','Không có căn cứ mặc định tuổi quyết định thứ tự chết; hai người không thừa kế nhau theo dữ kiện.'),
('C nhận toàn bộ 600 triệu vì B không hưởng A nên nhánh B cũng bị loại, không xét thế vị D.','Bỏ ngoại lệ thừa kế thế vị được giữ trong Điều 619 và Điều 652.'),
('C và D chia 400 và 200 triệu vì D thuộc hàng sau nên hưởng nửa suất của người con còn sống.','Thế vị hưởng suất nhánh B, không tự giảm vì D là cháu.')],
'Điều 619 không cho người có quyền thừa kế nhau mà không xác định thứ tự chết hưởng di sản của nhau, nhưng giữ ngoại lệ thế vị. Điều 652 cho D thế vị nhánh B khi B chết cùng thời điểm với A theo cấu hình này. Có hai nhánh con A nên mỗi suất 300 triệu; không tạo phần B đã nhận để chuyển tiếp qua di sản B.',
'DS:619 DS:651 DS:652',['Xử lý không xác định thứ tự chết','Kiểm tra ngoại lệ thế vị nhánh B','Chia di sản A riêng không chuyển tiếp qua di sản B'])

case('VER26-091',
'Hợp đồng bằng văn bản thiếu công chứng bắt buộc; bên mua đã thực hiện đúng 2/3 nghĩa vụ, mọi điều kiện khác để áp khoản 2 Điều 129 được đáp ứng. Chưa có quyết định Tòa công nhận. Hai bên muốn CCV đóng dấu, ghi thời điểm lùi về ngày ký và xác nhận hợp đồng đã được công nhận từ đó. Hướng xử lý đúng?',
'Có căn cứ để yêu cầu Tòa án công nhận theo nhánh đã nêu; chưa có quyết định thì không coi đủ 2/3 là tự công nhận hoặc dùng dấu, ngày lùi của CCV thay Tòa.',
[('CCV được tự công nhận vì đạt đúng 2/3; đóng dấu và ghi ngày ký cũ tạo hiệu lực công chứng từ thời điểm giao kết.','Ngưỡng thực hiện không trao thẩm quyền Tòa cho CCV hoặc cho ghi sai thời điểm.'),
('Không thể yêu cầu Tòa vì phải vượt 2/3, đúng bằng 2/3 vẫn thiếu; CCV có thể nhận hồ sơ để ghi ngày lùi sau khi trả thêm tiền.','Ít nhất gồm đúng bằng 2/3; không được ghi lùi thời điểm vì trả thêm nghĩa vụ.'),
('Hợp đồng tự được công nhận khi đủ 2/3 nên chỉ cần CCV cấp lời chứng; không cần quyết định dù một bên phản đối công nhận.','Bỏ bước yêu cầu và quyết định công nhận của Tòa án theo Điều 129.')],
'Khoản 2 Điều 129 đặt ngưỡng ít nhất hai phần ba và Tòa án công nhận trên cơ sở yêu cầu, không tạo cơ chế tự công nhận hoặc công chứng hồi tố. Đề đã khóa điều kiện khác đủ nên đúng 2/3 có thể yêu cầu Tòa; chưa có quyết định không được xác nhận như đã có. Điều 47, 48 còn đòi lời chứng và thời điểm trung thực.',
'DS:129 CC:47 CC:48',['Kiểm tra ngưỡng đúng bằng hai phần ba','Phân biệt căn cứ yêu cầu và việc đã được công nhận','Giữ thẩm quyền Tòa cùng tính trung thực thời điểm công chứng'])

case('VER26-095',
'A chỉ ủy quyền K cho thuê nhà còn thời hạn; K ký bán cho B, B biết giới hạn. Ban đầu A chưa đồng ý; sau đó A được thông tin đầy đủ, ký chấp thuận toàn bộ việc bán đúng hợp đồng. Không có lỗi hình thức, nội dung hoặc điều kiện khác. Chỉ xét phạm vi đại diện trước và sau chấp thuận, kết luận đúng?',
'Lúc ký, bán ngoài phạm vi cho thuê; chấp thuận hợp lệ toàn bộ của A là căn cứ ràng buộc A theo giao dịch, không phải cứ từng vượt quyền là không thể được chấp thuận.',
[('K có quyền bán ngay vì ủy quyền nhà còn thời hạn; chấp thuận A chỉ chứng minh quyền bán đã nằm sẵn trong quyền thuê.','Thời hạn còn không mở rộng phạm vi; sự chấp thuận sau là căn cứ riêng.'),
('K bán vượt quyền nên A không thể bị ràng buộc dù đã chấp thuận hợp lệ toàn bộ; giao dịch luôn bị loại chỉ vì thiếu quyền lúc ký.','Bỏ ngoại lệ người được đại diện đồng ý theo Điều 143.'),
('A chỉ bị ràng buộc phần giá bằng tiền thuê dự kiến; phần còn lại là nghĩa vụ K dù A chấp thuận toàn bộ không đặt điều kiện.','Không tự chia phạm vi chấp thuận toàn bộ thành phần thuê và phần bán.')],
'Điều 141 yêu cầu đối chiếu phạm vi, không lấy thời hạn còn để suy quyền bán. Điều 143 có ngoại lệ khi người được đại diện đồng ý; đề nêu A được thông tin đầy đủ và chấp thuận toàn bộ hợp lệ nên phải xét căn cứ đó. Không hồi tố phạm vi gốc thành quyền bán cũng không bỏ hiệu lực sự chấp thuận sau.',
'DS:141 DS:143',['Đối chiếu bán với phạm vi cho thuê','Tách thời hạn còn khỏi phạm vi quyền','Áp sự chấp thuận toàn bộ của người được đại diện'])

case('VER26-098',
'A ủy quyền K phát sinh quyền ngày 1/9/2025, không gắn giao dịch cụ thể, không xác định thời hạn theo văn bản hoặc luật. K lần đầu dùng giấy tại văn phòng tháng 4/2026, nay muốn ký tháng 10/2026. Không có gia hạn, quyền mới hay căn cứ ràng buộc khác. Chỉ xét thời hạn mặc định và mốc tính, nhận định đúng?',
'Mặc định một năm từ 1/9/2025, không từ lần dùng tháng 4/2026; giấy cũ không đủ chứng minh K còn quyền để ký tháng 10/2026.',
[('Một năm từ tháng 4/2026 khi lần đầu dùng tại công chứng; vì trước đó chưa dùng nên chưa khởi đầu thời hạn đại diện.','Mốc luật là phát sinh quyền, không phải lần đầu xuất trình tại công chứng.'),
('Không ghi thời hạn thì không hết trong trường hợp nào; K chỉ hết quyền khi A có văn bản hủy đã công chứng.','Bỏ quy tắc mặc định khi không xác định được theo các căn cứ khác của Điều 140.'),
('Một năm từ 1/9/2025 nhưng chưa dùng đủ một năm thực tế nên K được cộng thời gian từ tháng 4/2026 để ký tháng 10.','Không cộng hoặc tạm ngừng thời hạn vì người đại diện ít sử dụng văn bản.')],
'Điều 140 phân biệt đại diện cho giao dịch cụ thể với nhánh không xác định được thời hạn theo căn cứ khoản 1. Nhánh đề nêu mặc định một năm kể từ phát sinh quyền ngày 1/9/2025. Lần dùng đầu và số lần sử dụng không khởi động lại đồng hồ; đề loại quyền mới và căn cứ khác nên giấy này không đủ cho K ký tháng 10/2026.',
'DS:140 DS:141',['Nhận diện nhánh thời hạn mặc định','Giữ ngày phát sinh quyền thay ngày dùng đầu','Kiểm tra quyền còn tại thời điểm giao dịch mới'])

case('COMP26-CT-003',
'A nộp bản sao đã chứng thực cho thủ tục chấp nhận loại này. Cơ quan phát hiện dấu hiệu cụ thể bản sao bị sửa sau chứng thực, yêu cầu bản chính đối chiếu. A không cung cấp và muốn nộp bản photocopy của bản sao chứng thực thay thế, nói con dấu miễn mọi kiểm tra. Chỉ xét yêu cầu đối chiếu và loại bản nộp, đánh giá đúng?',
'Có căn cứ giả mạo thì được yêu cầu bản chính đối chiếu; bản photocopy của bản sao chứng thực không tự được hưởng giá trị của chính bản sao đã chứng thực.',
[('Có dấu chứng thực thì không được đòi bản chính dù có dấu hiệu sửa; photocopy giữ nguyên giá trị vì nhìn thấy dấu trong bản chụp.','Bỏ ngoại lệ kiểm tra và đồng nhất bản chụp với văn bản được chứng thực.'),
('Được đòi bản chính nhưng A nộp photocopy là đáp ứng đối chiếu; người nhận chỉ cần kiểm tra ảnh dấu chứ không giấy chính.','Photocopy không phải bản chính dùng đối chiếu, ảnh dấu không tự xác lập giá trị chứng thực mới.'),
('Được đòi bản chính chỉ sau quyết định Tòa về giả mạo; trước đó photocopy bản sao chứng thực bắt buộc được chấp nhận như bản gốc.','Đặt điều kiện phán quyết trước khi yêu cầu đối chiếu không có trong ngoại lệ Điều 6.')],
'Điều 6 cho yêu cầu bản chính khi có căn cứ bản sao giả mạo, bất hợp pháp; không chờ phán quyết Tòa. Giá trị bản sao chứng thực tại Điều 3 gắn với đúng văn bản chứng thực, không tự truyền sang bản photocopy chưa được chứng thực. Cần tách loại giấy, dấu hiệu rủi ro và phương tiện đối chiếu, không chỉ xem có ảnh con dấu.',
'CT:3 CT:6',['Xác định đúng bản sao đã được chứng thực','Kiểm tra căn cứ ngoại lệ yêu cầu bản chính','Không đồng nhất photocopy với bản chính hoặc bản sao chứng thực'])

case('COMP26-DN-007',
'A cam kết vốn 5 tỷ cho công ty TNHH một thành viên; đã góp 3 tỷ. Máy 2 tỷ còn đang vận chuyển, thời gian vận chuyển được pháp luật loại trừ đã xác định còn hiệu lực, nên thời hạn góp đủ thực tế chưa hết. Sau khi hết cả thời gian hợp lệ mà vẫn chỉ có 3 tỷ, A định giữ đăng ký 5 tỷ chờ lợi nhuận. Chỉ xét hai giai đoạn, nhận định đúng?',
'Không lấy 90 ngày lịch bỏ thời gian được loại trừ để kết luận quá hạn ngay; khi hết hạn thực tế vẫn thiếu thì phải đăng ký vốn 3 tỷ trong thời hạn luật định.',
[('Cứ qua 90 ngày lịch phải đăng ký 3 tỷ ngay dù thời gian vận chuyển còn được loại trừ; sau đó không xét mốc cuối thực tế.','Bỏ thời gian vận chuyển được loại trừ theo giả thiết và Điều 75.'),
('Thời gian vận chuyển được loại trừ nên A có thể giữ 5 tỷ vô hạn; hết thời gian hợp lệ vẫn được chờ lợi nhuận để bù vốn.','Ngoại lệ tính thời gian không tạo gia hạn vô hạn hoặc bỏ nghĩa vụ đổi đăng ký khi hết hạn.'),
('Khi hết hạn thực tế, đăng ký vốn 2 tỷ chưa góp trong 30 ngày; số 3 tỷ đã góp chỉ ghi sổ nội bộ.','Vốn đổi theo giá trị đã góp, không theo phần thiếu.')],
'Khoản 2 Điều 75 loại thời gian vận chuyển, nhập khẩu và thủ tục hành chính chuyển quyền trong điều kiện luật nêu; đề xác định thời gian hợp lệ nên phải tính hạn thực tế. Khi hạn ấy hết mà thiếu, khoản 3 yêu cầu đăng ký theo vốn đã góp, 3 tỷ, trong 30 ngày từ ngày cuối phải góp đủ. Không giữ phần thiếu bằng kỳ vọng lợi nhuận.',
'DN:75',['Tính hạn thực tế có thời gian được loại trừ','Kiểm tra số vốn đã góp khi hạn thực tế hết','Xác định giá trị và mốc đăng ký thay đổi'])

case('IMP-SEP24-002',
'Khi lập công ty, một tổ chức thẩm định giá định máy góp vốn 6 tỷ; đúng 50% thành viên sáng lập chấp thuận. Giá thực 4 tỷ, những người sáng lập cố ý dùng giá cao và thiệt hại riêng đã chứng minh. A nói có tổ chức thẩm định và nửa số thành viên nên đủ giá trị, không phải góp thêm. Cách đánh giá?',
'Đúng 50% chưa đạt yêu cầu trên 50%; việc có tổ chức thẩm định không tự loại nghĩa vụ bù chênh lệch 2 tỷ và trách nhiệm thiệt hại do cố ý định giá cao.',
[('Đúng 50% đủ vì tổ chức thẩm định chuyên nghiệp; chỉ phải sửa sổ xuống 4 tỷ, không góp bổ sung hoặc xét thiệt hại.','Sai ngưỡng thông qua và bỏ trách nhiệm do định giá cao.'),
('Đúng 50% chưa đủ; khi nâng lên trên 50% thì mọi trách nhiệm chênh lệch và thiệt hại tự được miễn do đã thông qua giá.','Thông qua giá không xóa nghĩa vụ và trách nhiệm do định giá cao.'),
('Phải có tất cả thành viên đồng ý dù do tổ chức thẩm định; nếu đạt 100% thì giá 6 tỷ được dùng thay giá thực 4 tỷ cho mọi trách nhiệm.','Áp sai ngưỡng và nhầm sự đồng thuận với miễn hậu quả định giá cao.')],
'Điều 36 tách phương thức định giá, ngưỡng chấp thuận khi tổ chức thẩm định giá thực hiện và hậu quả định giá cao. Giá do tổ chức thẩm định phải được trên 50% thành viên sáng lập chấp thuận, không phải đúng 50%. Các chủ thể luật định còn chịu nghĩa vụ liên đới bù chênh lệch và trách nhiệm thiệt hại do cố ý; thông qua giá không chữa giá cao.',
'DN:36',['Phân biệt đúng bằng và trên 50 phần trăm','Tách thẩm định giá khỏi việc thông qua','Xét hậu quả cố ý định giá cao hơn thực tế'])

case('IMP-SEP24-003',
'Một cộng đồng sử dụng đất Nhà nước giao không thu tiền. Toàn thể thống nhất để phần đất ấy cho con người đại diện khi người đại diện chết, dự kiến lập di chúc công chứng; nếu không được, họ đổi thành tặng cho ngay. Chỉ xét chủ thể sử dụng đất và hai loại giao dịch, kết luận đúng?',
'Quyền thuộc cộng đồng không thành di sản riêng người đại diện; cộng đồng không có quyền để thừa kế và nhánh giao đất không thu tiền còn bị hạn chế tặng cho.',
[
('Lập di chúc được vì mọi thành viên đồng ý, người đại diện ký thay cộng đồng; nếu tặng ngay thì cần thêm chữ ký người con.','Đồng ý thành viên không tạo quyền để thừa kế của cộng đồng hoặc di sản riêng người đại diện.'),
('Không để thừa kế được, nhưng tặng cho ngay luôn được vì hạn chế chỉ dành việc chuyển quyền sau người đại diện chết.','Bỏ hạn chế tặng cho của cộng đồng được Nhà nước giao đất không thu tiền.'),
('Tặng cho không được nhưng di chúc công chứng được vì không phải giao dịch chuyển quyền khi cộng đồng còn sống.','Công chứng không bổ sung quyền để thừa kế của chủ thể hoặc biến quyền chung thành di sản cá nhân.')],
'Điều 39 phân biệt quyền cộng đồng với cá nhân, loại quyền để thừa kế; đối với đất Nhà nước giao không thu tiền còn không được tặng cho theo nhánh này. Điều 612 chỉ tính tài sản của người chết và phần quyền trong tài sản chung, không tính toàn quyền cộng đồng do người đó đại diện. Đổi tên giao dịch, đồng thuận hoặc công chứng không chữa thiếu quyền.',
'DD:39 DS:612',['Xác định ai là chủ thể sử dụng đất','Tách quyền cộng đồng khỏi di sản người đại diện','Kiểm tra riêng hạn chế thừa kế và tặng cho'])

case('IMP-SEP24-010',
'Đã đủ căn cứ xử lý tài sản thế chấp; hợp đồng không thỏa thuận phương thức, không có luật chuyên ngành khác. Ngân hàng muốn tự nhận tài sản thay nợ vì đang giữ giấy gốc, rồi tự định giá thấp hơn khoản nợ và yêu cầu bên thế chấp trả chênh lệch. Chưa có thỏa thuận nhận tài sản thay nghĩa vụ. Trước hết phải xử lý thế nào?',
'Áp phương thức bán đấu giá mặc định; giữ giấy không tạo thỏa thuận nhận tài sản thay nợ, và không lấy giá ngân hàng tự đặt để chốt nghĩa vụ còn lại.',
[
('Ngân hàng nhận tài sản được vì đủ căn cứ xử lý; tự định giá rồi đòi chênh lệch, việc giữ giấy thay sự thỏa thuận phương thức.','Căn cứ xử lý khác với phương thức xử lý, giữ giấy không tạo thỏa thuận nhận tài sản.'),
('Bán đấu giá mặc định nhưng ngân hàng có thể nhận tài sản trước để trừ nợ, sau đó đấu giá chỉ là thủ tục bán lại tài sản mình.','Nhận tài sản thay nợ chưa có căn cứ thỏa thuận nên không được đặt trước đấu giá mặc định.'),
('Không được xử lý bằng cách nào cho đến khi ký phụ lục phương thức; BLDS không có cơ chế khi hợp đồng bỏ trống.','Điều 303 có phương thức mặc định, không làm quyền xử lý bế tắc chỉ vì thiếu thỏa thuận.')],
'Điều 303 cho bán đấu giá khi không có thỏa thuận phương thức và không có luật khác. Điều 305 yêu cầu thỏa thuận cho việc bên nhận bảo đảm nhận chính tài sản thay nghĩa vụ; nếu chưa có thì các bên có thể thỏa thuận mới, không tự suy từ giấy gốc. Giá trị xử lý phải xác định theo quy tắc Điều 306, không chốt chênh lệch bằng giá một bên tự đặt thiếu căn cứ.',
'DS:303 DS:305 DS:306',['Tách căn cứ xử lý và phương thức','Kiểm tra thỏa thuận nhận tài sản thay nghĩa vụ','Giữ yêu cầu xác định giá trị trước chốt chênh lệch'])

case('IMP-SEP24-011',
'K nộp đúng hạn đề nghị công nhận hoàn thành tập sự, báo cáo và nhật ký là bản sao có chứng thực. Nội dung hai bản không thống nhất về thời gian, cần xác minh; sau đó K bổ sung theo yêu cầu. K muốn tính hạn giải quyết từ ngày nộp đầu và cơ quan muốn bác chỉ vì không có bản chính. Nhận định đúng?',
'Bản sao có chứng thực là loại được chấp nhận; vẫn phải làm rõ nội dung, thời hạn nhánh cần bổ sung hoặc xác minh tính từ nhận kết quả theo quy định.',
[
('Phải nộp lại cả hai bản chính mới xét; bản sao chứng thực chỉ dùng khi hồ sơ không có điểm nào cần xác minh.','Điều kiện kiểm tra nội dung không tự loại hình thức bản sao được luật cho phép.'),
('Bản sao được chấp nhận nên cơ quan không được xác minh nội dung và phải công nhận trong hạn tính từ nộp đầu.','Hợp lệ loại bản không đồng nghĩa đủ điều kiện nội dung để công nhận.'),
('Bản sao được chấp nhận và cần xác minh, nhưng hạn luôn tính từ nộp đầu dù điều khoản quy định mốc nhận kết quả bổ sung.','Chọn sai mốc thời hạn đối với nhánh thông tin cần bổ sung hoặc xác minh.')],
'Điều 11 TT6 chấp nhận bản chính, bản sao chứng thực hoặc bản sao điện tử cho báo cáo và nhật ký. Điều đó không miễn kiểm tra thời gian, thông tin thống nhất và các điều kiện hoàn thành. Khi thông tin chưa đủ, chưa thống nhất hoặc cần xác minh, cơ quan yêu cầu giải trình, bổ sung hoặc xác minh; thời hạn nhánh này tính từ nhận kết quả, không dùng loại bản để bác hoặc tự công nhận.',
'TT6:11',['Kiểm tra loại bản của hai giấy tờ','Tách hình thức bản và điều kiện nội dung','Chọn mốc giải quyết khi cần bổ sung xác minh'])

case('IMP-SEP24-029',
'K không là Trưởng, rút vốn hợp pháp khỏi P: đã thông báo trước đúng hạn, đủ chấp thuận, còn đủ thành viên và hoàn thành tài chính ngày 30/9. Sở ghi nhận thay đổi ngày 10/10. P cho rằng K tự thông báo hoàn thành là đủ và đã hết tư cách từ 30/9. Chỉ xét trách nhiệm thông báo sau rút và mốc tư cách, nhận định đúng?',
'P có trách nhiệm thông báo bằng văn bản việc hoàn thành; tư cách K chấm dứt khi Sở ghi nhận ngày 10/10 theo nhánh không là Trưởng.',
[
('K thông báo hoàn thành thay P vì chính K đã yêu cầu rút; tư cách chấm dứt 30/9 khi K nhận đủ tiền.','Nhầm chủ thể thông báo hoàn thành và mốc chấm dứt tư cách.'),
('P phải thông báo hoàn thành nhưng tư cách chấm dứt 30/9; ngày ghi nhận chỉ xác nhận lại việc tài chính đã xong.','Thực hiện tài chính chưa thay mốc Sở ghi nhận của thành viên không là Trưởng.'),
('P thông báo và K chấm dứt 10/10; do không là Trưởng, chỉ một năm sau K được hợp danh nơi khác.','Hai phần đúng nhưng giảm sai thời hạn hai năm sau chấm dứt theo nhánh rút vốn đang xét.')],
'Điều 27 tách thông báo yêu cầu của thành viên và thông báo hoàn thành của Văn phòng. Thành viên không là Trưởng chấm dứt tư cách tại thời điểm Sở ghi nhận vào giấy đăng ký hoạt động, không chỉ nhận đủ tiền. Khoảng hạn hai năm sau chấm dứt phải tính theo mốc tư cách đó nếu xét tham gia hợp danh nơi khác, không dùng ngày tài chính hay tự giảm còn một năm.',
'CC:27',['Tách trách nhiệm trước và sau rút vốn','Chọn mốc ghi nhận với thành viên không là Trưởng','Giữ thời hạn sau chấm dứt theo đúng mốc tư cách'])

case('IMP-SEP24-041',
'K đã tập sự hợp lệ bốn tháng, tạm ngừng đúng thủ tục hai tháng vì sức khỏe rồi quay lại và tập sự thêm năm tháng. Không thuộc trường hợp phải đăng ký lại, không có thời gian khác được tính. K muốn công nhận đủ 11 tháng và rút ngắn một tháng còn lại; P lại muốn xóa bốn tháng trước nghỉ. Chỉ xét thời gian cần đạt 12 tháng, kết quả đúng?',
'Được tính chín tháng tập sự, không tính hai tháng tạm ngừng và không xóa bốn tháng trước; còn cần ba tháng để đạt 12.',
[
('Tính 11 tháng vì tạm ngừng đúng thủ tục nên hai tháng nghỉ cũng được tính; còn một tháng đủ 12.','Đúng thủ tục bảo toàn thời gian trước nghỉ, không biến thời gian nghỉ thành tập sự.'),
('Chỉ tính năm tháng sau quay lại; mọi tạm ngừng đều làm mất thời gian trước nên còn bảy tháng.','Đề loại đăng ký lại, nên không xóa bốn tháng tập sự hợp lệ trước nghỉ.'),
('Tính chín tháng nhưng phải bắt đầu chu kỳ 12 tháng mới từ ngày quay lại để bảo đảm tập sự liên tục.','Thêm điều kiện chu kỳ liên tục mới trái việc cộng thời gian trước nghỉ trong nhánh đã nêu.')],
'Điều 8 TT6 không tính thời gian tạm ngừng nhưng cho cộng thời gian tập sự trước tạm ngừng, trừ trường hợp phải đăng ký lại. Đề đã loại nhánh đó. Bốn cộng năm là chín tháng, cần thêm ba để đạt 12 tháng theo Luật Công chứng; thủ tục nghỉ hợp lệ không tạo hai tháng tập sự, cũng không đòi xóa hoặc khởi động lại toàn chu kỳ.',
'TT6:8 TT6:9 CC:12',['Xác định không thuộc nhánh đăng ký lại','Loại thời gian nghỉ nhưng giữ thời gian hợp lệ','Tính phần còn thiếu đến 12 tháng'])

case('IMP-SEP24-042',
'A có hợp đồng mua căn hộ thương mại hình thành trong tương lai, B có hợp đồng mua nhà ở xã hội. Cả hai muốn chuyển nhượng hợp đồng theo Mục 2 Chương VI Luật Kinh doanh BĐS; điều kiện khác của A đủ. B đã trả 60%, cho rằng tỷ lệ này cao hơn A nên được dùng cùng cơ chế. Chỉ xét phạm vi cơ chế, kết luận đúng?',
'A thuộc loại hợp đồng có thể áp cơ chế theo dữ kiện; hợp đồng nhà ở xã hội B bị loại khỏi cơ chế này, mức thanh toán không đổi phạm vi.',
[
('A và B cùng thuộc cơ chế vì đều là hợp đồng mua nhà tương lai; thanh toán trên 50% đủ làm mất khác biệt loại nhà.','Bỏ loại trừ nhà ở xã hội tại khoản 2 Điều 49.'),
('A không thuộc vì chưa có nhà bàn giao; B thuộc vì trả 60% đã được coi có phần sở hữu để chuyển hợp đồng.','Đảo phạm vi hợp đồng nhà tương lai được xét và suy từ tiền đã trả ra quyền sở hữu.'),
('A thuộc và B không thuộc cơ chế; vì vậy B có thể đổi tên giấy thành chuyển nhượng quyền thanh toán để áp nguyên thủ tục này.','Đổi tên văn bản không tự thay bản chất hợp đồng nhà ở xã hội hoặc phạm vi thủ tục.')],
'Điều 49 liệt kê hợp đồng mua bán nhà hình thành trong tương lai và các loại khác được chuyển nhượng theo Luật Kinh doanh BĐS, đồng thời loại hợp đồng mua bán, thuê mua nhà ở xã hội khỏi Mục này. Phải phân loại hợp đồng trước xét tỷ lệ thanh toán. B muốn xử lý theo cơ chế khác phải xét quy định phù hợp, không tự đổi tên để đưa vào cơ chế đang bị loại.',
'KD:49 NHA:89',['Phân biệt nhà thương mại và nhà xã hội','Kiểm tra danh mục loại hợp đồng thuộc cơ chế','Không dùng tỷ lệ thanh toán hoặc tên giấy thay phạm vi'])

case('IMP-T60-001',
'A muốn thế chấp 100 bao gạo thuộc sở hữu mình, mô tả đủ xác định và không có hạn chế đặc thù. A còn muốn đưa 50 bao gạo của B vào cùng bảo đảm; B không đồng ý, không có căn cứ khác cho A dùng gạo B. A nói hàng tiêu hao không cần xét chủ sở hữu như tài sản đặc định. Chỉ xét loại tài sản và quyền, kết luận đúng?',
'Gạo không bị loại chỉ vì tiêu hao; phải tách 100 bao thuộc A với 50 bao B mà A chưa có quyền dùng bảo đảm.',
[
('Cả 150 bao được dùng vì hàng tiêu hao chỉ cần xác định số lượng; quyền sở hữu chỉ cần cho tài sản đặc định.','Tính tiêu hao không miễn điều kiện quyền sở hữu hoặc căn cứ sử dụng tài sản B.'),
('Cả 150 bao đều bị loại vì tài sản bảo đảm phải không tiêu hao; việc A hoặc B đứng tên sở hữu không ảnh hưởng.','BLDS không cấm chung vật tiêu hao làm tài sản bảo đảm.'),
('100 bao A bị loại vì có thể ăn hoặc bán, 50 bao B được dùng nếu A đang giữ dù B không đồng ý.','Vừa áp sai loại tài sản vừa lấy chiếm giữ thay quyền dùng tài sản người khác.')],
'Điều 295 cho tài sản bảo đảm là tài sản hiện có hoặc tương lai và có thể mô tả chung nhưng phải xác định được; không loại chỉ vì gạo tiêu hao. Điều kiện quyền đối với tài sản vẫn độc lập: 100 bao A và 50 bao B khác nguồn quyền, giữ hàng không tự trao quyền bảo đảm. Đề chọn thế chấp, không dùng ngoại lệ cầm giữ hoặc bảo lưu quyền để bỏ thiếu quyền ở gạo B.',
'DS:295 DS:105',['Nhận diện không có cấm chung vật tiêu hao','Kiểm tra mô tả xác định được','Đối chiếu quyền riêng từng lô hàng'])

case('IMP-T60-038',
'Hợp đồng thuê mua nhà có giá 2 tỷ, đề nghị trả trước 1,2 tỷ, số còn lại trả hằng tháng đến năm 2030. Bên thuê mua đã có khả năng trả 60% và nhận nhà năm 2026 nên muốn ghi sở hữu từ đó; không có thỏa thuận hoặc luật riêng tạo mốc khác. Chỉ xét giới hạn trả trước và cơ chế sở hữu thuê mua, phương án phù hợp?',
'Trả trước không quá 1 tỷ theo giới hạn 50%; nhận nhà chưa tự xác lập sở hữu, còn cần hết thời hạn thuê mua và trả hết phần còn lại.',
[
('Có khả năng tài chính thì trả trước 1,2 tỷ được; nhận nhà năm 2026 đủ chuyển sở hữu vì phần còn lại là khoản vay.','Tự bỏ trần thanh toán trước và đổi thuê mua thành mua kèm vay.'),
('Trả trước tối đa 1 tỷ nhưng sở hữu chuyển ngay khi nhận nhà, hết hạn chỉ quyết định số tiền thuê còn phải trả.','Nhận đúng trần nhưng bỏ hai điều kiện hết hạn và trả hết của cơ chế thuê mua.'),
('Trả trước 1,2 tỷ được vì dưới toàn giá; sở hữu chờ năm 2030 dù khi đó chưa thanh toán hết tiền còn lại.','Sai trần và bỏ yêu cầu trả hết phần tiền còn lại.')],
'Khoản 22 Điều 2 Luật Nhà ở hiện hành giới hạn tiền trả trước không quá 50% giá hợp đồng: 2 tỷ thì tối đa 1 tỷ. Thuê mua cho sở hữu sau hết thời hạn và khi trả hết tiền còn lại, không tự từ việc nhận nhà hoặc khả năng trả cao. Không đổi cách gọi phần còn lại thành khoản vay để bỏ các điều kiện thuê mua.',
'NHA:2 NHA:12',['Tính trần tiền trả trước theo giá hợp đồng','Phân biệt bàn giao và xác lập sở hữu thuê mua','Kiểm tra đồng thời hết hạn và trả hết tiền'])

case('IMP-T60-039',
'N là cá nhân nước ngoài kết hôn với công dân Việt Nam đang sinh sống tại Việt Nam, đủ điều kiện mua nhà có sẵn của một cá nhân, không giao dịch với chủ đầu tư. Hợp đồng mua nhà đã có hiệu lực nhưng N chưa trả đủ và chưa nhận bàn giao; không thỏa thuận khác về mốc sở hữu. N muốn ghi chỉ sở hữu 50 năm từ đặt cọc, hoặc coi đã sở hữu ngay vì cơ chế như công dân Việt Nam. Chỉ xét cơ chế và mốc, kết luận đúng?',
'N thuộc cơ chế sở hữu như công dân Việt Nam theo dữ kiện hôn nhân; điều đó không tự làm phát sinh sở hữu trước khi đủ mốc của giao dịch mua nhà đang xét.',
[
('N vẫn chỉ sở hữu 50 năm vì còn quốc tịch nước ngoài; thời hạn bắt đầu đặt cọc bất kể hôn nhân và bàn giao.','Bỏ ngoại lệ hôn nhân và dùng sai mốc đặt cọc.'),
('N được sở hữu như công dân Việt Nam nên sở hữu ngay từ ký hợp đồng, không cần xét trả đủ hoặc bàn giao.','Ngoại lệ chế độ chủ thể không miễn điều kiện mốc xác lập sở hữu.'),
('N sở hữu như công dân Việt Nam chỉ sau khi đổi quốc tịch; nếu chưa đổi, hợp đồng mua nhà hợp pháp cũng không được thực hiện.','Thêm điều kiện đổi quốc tịch không có trong nhánh hôn nhân đã nêu.')],
'Điều 20 ghi ngoại lệ cá nhân nước ngoài kết hôn với công dân Việt Nam đang sinh sống tại Việt Nam có quyền sở hữu và quyền chủ sở hữu như công dân Việt Nam. Tuy nhiên phải giữ mốc giao dịch tại Điều 12 theo cấu hình phù hợp, không suy từ cơ chế chủ thể ra quyền đã phát sinh ngay. Đề chưa trả đủ, chưa bàn giao và không mốc khác nên chưa đủ để kết luận đã sở hữu.',
'NHA:20 NHA:12',['Kiểm tra đủ điều kiện ngoại lệ hôn nhân','Tách cơ chế sở hữu của chủ thể khỏi mốc giao dịch','Đối chiếu trả tiền và bàn giao thực tế'])

case('IMP-T60-054',
'Hồ sơ đất hình thành trước khi Luật Đất đai hiện hành có hiệu lực xác định A, W và con C có quyền sử dụng chung của hộ theo đúng điều kiện luật. D mới nhập cùng hộ năm 2026, không nhận chuyển quyền; C nay chuyển nơi thường trú. A muốn loại C và thêm D chỉ theo danh sách cư trú hiện tại. Chỉ xét xác định người có quyền, kết luận đúng?',
'Phải giữ căn cứ quyền chung tại thời điểm xác lập theo hồ sơ; đổi nơi cư trú không tự làm C mất quyền, nhập hộ không tự cho D có quyền đất.',
[
('Danh sách cư trú hiện tại quyết định: C mất quyền, D có quyền ngang A–W dù không có chuyển quyền.','Nhầm quản lý cư trú với căn cứ xác lập, chấm dứt quyền sử dụng đất chung.'),
('C vẫn có quyền nhưng D tự thêm phần vì quan hệ gia đình và cùng địa chỉ năm 2026 đáp ứng định nghĩa hộ sử dụng đất mới.','Định nghĩa gắn việc sống chung và có quyền chung tại thời điểm trước hiệu lực, không tạo phần mới do nhập hộ.'),
('D chưa có quyền nhưng A là chủ hộ được ký bán cả phần C vì C đã chuyển nơi ở và không giữ giấy.','Đúng về D nhưng thêm quyền đại diện C không có căn cứ.')],
'Điều 3 đòi nhận đúng hộ có quyền sử dụng chung được xác lập trước thời điểm luật có hiệu lực, không chỉ danh sách cư trú hiện tại. Quyền đã có của C không tự mất vì chuyển chỗ ở; D chưa có nguồn nhận quyền thì không tự thành đồng chủ thể do nhập hộ. Điều 141 vẫn đòi căn cứ quyền đại diện nếu A muốn ký cho người khác.',
'DD:3 DS:141',['Đọc thời điểm và thành viên có quyền theo hồ sơ','Tách biến động cư trú khỏi biến động quyền đất','Kiểm tra căn cứ đại diện cho người còn quyền'])

case('REFIN26-CC-005',
'P là Văn phòng hợp danh có K làm Trưởng hợp pháp. K thuê M không phải CCV: hợp đồng I chỉ hỗ trợ lưu trữ, hành chính dưới điều hành K; hợp đồng II giao M toàn quyền điều hành P, K chỉ ký lời chứng, M còn dùng thẻ K để ký chứng nhận khi K vắng. Chỉ xét ranh giới hỗ trợ, điều hành và chứng nhận, đánh giá đúng?',
'Không đồng nhất hỗ trợ hành chính với điều hành thay; II không được hợp thức bằng tên hợp đồng, M cũng không được dùng thẻ K ký chứng nhận.',
[
('I và II đều được vì K vẫn là Trưởng trên giấy; dùng thẻ K cho M ký là phân công nội bộ có người chịu trách nhiệm.','Trưởng trên giấy không chữa thuê người điều hành hoặc cho người khác dùng thẻ, ký công chứng.'),
('I và II đều bị cấm vì người không là CCV không được làm bất kỳ công việc hành chính nào tại Văn phòng.','Mở rộng cấm điều hành, chứng nhận thành cấm mọi hỗ trợ hành chính.'),
('II chỉ cần đổi thành hợp đồng tư vấn quản lý; M ký chứng nhận được nếu K ký kiểm tra lại cuối ngày.','Tên hợp đồng và kiểm tra sau không đổi bản chất điều hành thay hoặc tư cách chứng nhận.')],
'Điều 23 không cho thuê người khác điều hành Văn phòng, phải đọc quyền thực giao chứ không chỉ tên tư vấn. Hoạt động hỗ trợ hành chính không tự là giao toàn quyền điều hành. Điều 9 còn cấm cho dùng thẻ và người không là CCV cung cấp dịch vụ công chứng; K ký lại sau không biến M thành người chứng nhận đủ điều kiện.',
'CC:23 CC:9',['Phân loại hỗ trợ và quyền điều hành thực tế','Kiểm tra tên hợp đồng có che bản chất hay không','Kiểm tra độc lập việc dùng thẻ và ký chứng nhận'])

case('REFIN26-CC-034',
'P hợp danh có hai thành viên; một người chết ngày 1/6, chỉ còn K. Ngày 1/10, P chưa bổ sung hợp danh nhưng thuê một CCV đủ điều kiện theo hợp đồng lao động, cho rằng đã có hai CCV nên hết nghĩa vụ bổ sung. Không có căn cứ thu hồi khác. Chỉ xét nhánh giảm thành viên do chết và loại người bổ sung, nhận định đúng?',
'Chưa hết sáu tháng nên không tự thu hồi ngay chỉ vì còn một hợp danh; CCV hợp đồng không thay việc bổ sung ít nhất một thành viên hợp danh trong hạn.',
[
('Phải thu hồi ngay từ 1/6 vì còn một hợp danh; việc thuê thêm CCV không ảnh hưởng do không có thời hạn bổ sung.','Bỏ ngoại lệ sáu tháng trong nhánh chết của Điều 33.'),
('Không thu hồi, CCV hợp đồng đủ thay thành viên mới vì chỉ cần hai người có thẻ, không cần tư cách hợp danh.','Nhầm số CCV làm việc với số thành viên hợp danh phải duy trì.'),
('CCV hợp đồng chưa đủ nhưng P được thêm sáu tháng mới từ ngày thuê người này; thời hạn được khởi động lại khi có CCV.','Mốc sáu tháng từ lúc còn một thành viên, không phải từ hợp đồng thuê người khác.')],
'Khoản 2 Điều 33 cho bổ sung ít nhất một thành viên hợp danh trong sáu tháng từ lúc chỉ còn một người theo nhánh chết đang xét; không có căn cứ khác nên không thu hồi ngay ngày giảm người. Điều 37 tách hợp danh và làm theo hợp đồng lao động, thuê CCV không tự tạo hợp danh hoặc bắt đầu lại hạn bổ sung.',
'CC:33 CC:37',['Nhận diện đúng nguyên nhân được thời hạn bổ sung','Tính hạn từ lúc còn một thành viên','Phân biệt thành viên hợp danh và CCV theo hợp đồng'])

case('REFIN26-CC-038',
'K đang hành nghề hợp pháp tại tỉnh A, là hội viên Hội A. K muốn chuyển hành nghề sang B và chỉ giữ thẻ Hội A để khỏi gia nhập Hội B; chưa hoàn thành thay đổi đăng ký hành nghề. K nói mọi Hội đều thuộc tổ chức toàn quốc nên thẻ nào cũng đủ. Chỉ xét hội viên và nơi hành nghề, cách đánh giá đúng?',
'Phải duy trì hội viên phù hợp địa phương nơi hành nghề và làm thủ tục chuyển hành nghề theo quy định; thẻ Hội A không tự cho K hành nghề ở B.',
[
('Thẻ Hội A dùng cho B vì cùng tổ chức toàn quốc; K ký tại B được ngay khi ký hợp đồng làm việc, không cần thay đổi đăng ký.','Đồng nhất tổ chức toàn quốc với yêu cầu Hội tại địa phương và bỏ thủ tục hành nghề.'),
('K thôi hội viên A được và ký tại B trước khi gia nhập Hội B; điều kiện hội viên chỉ kiểm tra một lần lúc bổ nhiệm.','Bỏ yêu cầu duy trì tư cách hội viên trong quá trình hành nghề.'),
('K phải tham gia Hội B nhưng sau đó được đồng thời ký ở A và B; hai thẻ hội viên thay được giới hạn số nơi hành nghề.','Điều kiện hội viên không miễn cấm đồng thời hành nghề tại hai tổ chức.')],
'Điều 18 yêu cầu gia nhập Hội nơi hành nghề và duy trì tư cách; Điều 37 xác định hình thức hành nghề, điều kiện chuyển còn theo đăng ký. Điều 9 cấm đồng thời hành nghề tại hai tổ chức. Vì vậy không lấy thẻ Hội cũ hoặc việc cùng tổ chức toàn quốc để thay thủ tục, cũng không biến đủ hội viên hai nơi thành quyền hành nghề hai nơi.',
'CC:18 CC:19 CC:9',['Xác định Hội gắn nơi hành nghề','Tách hội viên khỏi đăng ký hành nghề','Giữ cấm đồng thời tại hai tổ chức'])

case('REFIN26-DAT-009',
'Người sử dụng đất A được đổi tên hợp pháp thành K; chính người này và thửa đất không đổi. Giấy đất còn tên A, giao dịch chuyển nhượng mới dự kiến ký tên K; hồ sơ có quyết định đổi tên và đối chiếu nhân thân phù hợp. K muốn bỏ cập nhật đăng ký, hoặc coi đổi tên là chuyển đất sang người mới để đăng ký lần đầu. Hướng xử lý phù hợp?',
'Đổi tên là biến động đăng ký của cùng chủ thể, không tự chuyển quyền cho người mới; vẫn xử lý cập nhật và kiểm tra điều kiện giao dịch, không thay bằng việc CCV đối chiếu tên.',
[
('Đổi tên tạo chủ thể sử dụng đất mới nên phải đăng ký lần đầu như lần đầu được giao đất; quyết định đổi tên là căn cứ chuyển quyền.','Nhầm thay tên của cùng người với chuyển quyền hoặc xác lập quyền mới.'),
('Cùng người nên không cần cập nhật đăng ký; CCV ghi cả tên A và K đã hoàn thành mọi thủ tục biến động đất đai.','Đối chiếu người ký không thay nghĩa vụ đăng ký biến động theo Điều 133.'),
('Cập nhật đổi tên đủ làm đất đủ điều kiện chuyển nhượng ngay, không cần xét tranh chấp hoặc ngăn chặn tại thời điểm giao dịch.','Thủ tục tên không miễn điều kiện thực hiện quyền đất ở Điều 45.')],
'Điều 133 nhận việc người sử dụng được phép đổi tên là biến động đăng ký, không phải chuyển quyền sang một người khác. Quyết định đổi tên giúp đối chiếu nhân thân nhưng CCV không thay cơ quan đăng ký thực hiện cập nhật. Khi chuyển nhượng còn phải kiểm tra các điều kiện đất tại Điều 45, không suy đủ quyền giao dịch chỉ từ xử lý tên.',
'DD:133 DD:45',['Đối chiếu cùng một chủ thể qua quyết định đổi tên','Chọn biến động thay vì đăng ký lần đầu','Tách cập nhật tên khỏi điều kiện giao dịch dự kiến'])

case('REFIN26-QT-009',
'A đang điều trị nội trú, không đi lại được, không thông thạo tiếng Việt. Văn phòng đủ điều kiện nhận hồ sơ ngoài trụ sở, đã bố trí người phiên dịch không lợi ích liên quan và người làm chứng đúng căn cứ, đầy đủ điều kiện khác. Dự thảo lời chứng chỉ ghi địa chỉ bệnh viện, còn lý do và thông tin phiên dịch, làm chứng ghi ở biên bản riêng. Cách hoàn thiện?',
'Căn cứ sức khỏe cho phép xét ngoài trụ sở; lời chứng vẫn phải có lý do và thông tin làm chứng, phiên dịch phù hợp, không chỉ giữ ở biên bản riêng.',
[
('Chỉ giữ địa chỉ trong lời chứng là đủ vì biên bản riêng đã ghi lý do và chủ thể; lời chứng không được ghi thông tin đó.','Bỏ nội dung lời chứng luật yêu cầu trong trường hợp ngoài trụ sở có làm chứng, phiên dịch.'),
('Bổ sung thông tin lời chứng nhưng phải từ chối ngoài trụ sở vì dùng phiên dịch làm mất căn cứ sức khỏe của A.','Phiên dịch không xóa trường hợp ngoài trụ sở theo sức khỏe, đề đã xác định đủ các điều kiện.'),
('Ghi lý do ngoài trụ sở và tên người làm chứng là đủ; phiên dịch chỉ là người hỗ trợ nên không ghi trong lời chứng.','Điều 48 còn đòi thông tin về việc phiên dịch, không tự loại vì gọi là hỗ trợ.')],
'Điều 46 cho xét ngoài trụ sở vì tình trạng điều trị, đi lại đã nêu; Điều 49 đặt điều kiện phiên dịch, làm chứng theo trường hợp. Điều 48 yêu cầu lời chứng ghi thông tin về lý do ngoài trụ sở và việc làm chứng, phiên dịch. Biên bản nghiệp vụ hỗ trợ chứng cứ, không tự thay nội dung lời chứng; cần hoàn thiện cả căn cứ và nội dung chứng nhận.',
'CC:46 CC:48 CC:49',['Kiểm tra căn cứ ngoài trụ sở','Giữ điều kiện người làm chứng và phiên dịch','Kiểm tra nội dung bắt buộc ngay trong lời chứng'])

case('VER26-022',
'W được tặng cho riêng đất trong hôn nhân, có hồ sơ đủ chứng minh, chưa nhập chung. A là chồng chỉ được W ủy quyền cho thuê đến cuối năm, lại muốn ký bán đất cho B. B biết phạm vi, W không chấp thuận và không có lỗi; không ngoại lệ khác về định đoạt. A nói là chồng và giữ giấy nên được bán. Kết luận đúng?',
'Đất vẫn riêng W theo dữ kiện; tư cách chồng và quyền cho thuê không tạo quyền bán, không có căn cứ ràng buộc W theo giao dịch bán vượt quyền này.',
[
('Đất thành chung vì A hỗ trợ quản lý sau cưới; A bán được nếu hứa chia tiền cho W, không cần đúng phạm vi giấy thuê.','Hỗ trợ quản lý không tự nhập riêng thành chung hoặc tạo quyền định đoạt.'),
('Đất riêng W nhưng giấy cho thuê còn hạn nên A có thể bán; thời hạn còn là căn cứ đủ thay việc xét loại giao dịch được giao.','Nhầm còn thời hạn với có phạm vi bán.'),
('Đất riêng và A vượt quyền; W vẫn buộc bán vì B đã biết A là chồng và người giữ giấy gốc của W.','Biết quan hệ vợ chồng, giữ giấy không tạo ngoại lệ khi B biết vượt quyền và W không chấp thuận, không lỗi.')],
'Điều 43, 44 giữ quyền riêng và quyền định đoạt W theo các dữ kiện đã loại ngoại lệ. Điều 24 cho vợ chồng đại diện theo căn cứ hợp lệ, không biến quan hệ hôn nhân thành quyền bán mọi tài sản. Điều 141, 143 đòi đúng phạm vi hoặc căn cứ ràng buộc khác; ở đây chỉ cho thuê, B biết và W không chấp thuận nên không hợp thức bằng giữ giấy.',
'HN:43 HN:44 HN:24 DS:141 DS:143',['Xác định nguồn đất riêng được chứng minh','Đọc phạm vi đại diện thay vì chỉ thời hạn','Kiểm tra căn cứ ràng buộc chủ tài sản khi vượt quyền'])

case('VER26-042',
'Đất I từng tranh chấp nhưng đã có bản án giải quyết có hiệu lực; thời hạn sử dụng còn, có giấy, không kê biên hoặc biện pháp cấm khác. Đất II cũng có bản án giải quyết tranh chấp có hiệu lực nhưng đang bị áp dụng biện pháp khẩn cấp tạm thời cấm chuyển dịch còn hiệu lực. Chỉ xét các trở ngại nêu, hướng xử lý đúng?',
'Không loại I chỉ vì từng tranh chấp; bản án giải quyết tranh chấp chưa đủ loại biện pháp cấm hiện hành của II, nên không coi II đủ điều kiện chuyển nhượng.',
[
('Cả I và II đều đủ vì bản án giải quyết tranh chấp có hiệu lực ưu tiên mọi dữ liệu cấm, không xét tình trạng hiện tại.','Bỏ điều kiện độc lập không bị biện pháp khẩn cấp tạm thời.'),
('Cả I và II đều không được chuyển vì mọi đất từng tranh chấp đều bị hạn chế sau bản án, không có cơ chế khắc phục.','Luật nhận trường hợp tranh chấp đã giải quyết có hiệu lực, không tạo cấm vĩnh viễn.'),
('I đủ và II đủ nếu bên mua ký nhận rủi ro; chỉ người yêu cầu áp biện pháp cấm mới có quyền phản đối công chứng.','Cam kết bên mua không chữa biện pháp cấm chuyển dịch còn hiệu lực.')],
'Điều 45 nhận đất không tranh chấp hoặc đã được giải quyết theo bản án, quyết định có hiệu lực, nhưng còn các điều kiện độc lập về kê biên, biện pháp khẩn cấp và thời hạn. I đạt theo các dữ kiện; II còn biện pháp cấm nên không lấy việc giải quyết tranh chấp làm điều kiện duy nhất. Công chứng phải kiểm tra, không chỉ nhận cam kết bỏ qua của người mua.',
'DD:45 CC:42',['Kiểm tra hiệu lực bản án giải quyết tranh chấp','Tách trở ngại tranh chấp và biện pháp cấm','Đối chiếu điều kiện hiện tại của từng hồ sơ'])

case('VER26-083',
'A có khó khăn trong nhận thức; Tòa chỉ định K giám hộ và xác định K chỉ đại diện cho A quản lý một khoản tiền, không đại diện bán nhà. K muốn ký bán nhà A, kèm giấy bác sĩ cho rằng tình trạng tốt hơn; chưa có quyết định thay phạm vi của Tòa, A không tự xác lập hợp lệ việc bán, không căn cứ khác. Kết luận đúng?',
'Phải đọc quyết định và phạm vi đã xác định; danh nghĩa giám hộ cùng giấy bác sĩ không đủ trao K quyền bán nhà ngoài phạm vi.',
[
('K được bán vì mọi người giám hộ tự là đại diện toàn bộ tài sản; Tòa chỉ nêu khoản tiền để hướng dẫn, không giới hạn.','Điều 136 với người khó khăn nhận thức gắn đại diện theo Tòa chỉ định, không suy quyền toàn bộ.'),
('Giấy bác sĩ mở rộng phạm vi cho K bán vì A đã tốt hơn; không cần quyết định thay phạm vi khi hồ sơ nhà đầy đủ.','Tình trạng y khoa không tự sửa quyền giám hộ và đại diện đang được Tòa xác định.'),
('K chỉ quản lý tiền nhưng người thân đồng ý là đủ cho bán nhà nhân danh A; sự đồng thuận gia đình thay thẩm quyền Tòa về phạm vi.','Gia đình không tự mở rộng phạm vi đại diện đã được Tòa giới hạn.')],
'Điều 23 và 136 yêu cầu căn cứ quyết định Tòa về giám hộ, quyền và nghĩa vụ khi người có khó khăn nhận thức. Điều 141 còn kiểm tra phạm vi đối với giao dịch cụ thể. K chỉ được quản lý khoản tiền theo quyết định; giấy bác sĩ và sự đồng ý gia đình không tự cấp quyền bán nhà. Cần căn cứ hợp lệ khác hoặc xử lý phạm vi theo đúng thẩm quyền, không đồng nhất với giám hộ toàn quyền.',
'DS:23 DS:136 DS:141',['Nhận đúng tình trạng khó khăn nhận thức','Đọc quyền cụ thể Tòa giao','Đối chiếu bán nhà với phạm vi đang còn hiệu lực'])

case('CC-024',
'K đủ tiêu chuẩn chung xin bổ nhiệm lần đầu, đang bị truy cứu trách nhiệm hình sự, chưa có bản án kết tội. Hồ sơ không thuộc căn cứ loại khác. K viện dẫn suy đoán vô tội và đề nghị bổ nhiệm rồi sẽ miễn nhiệm nếu có tội. P còn đề nghị cho K ký lời chứng trong lúc chờ. Cách xử lý phù hợp?',
'Đang bị truy cứu là trở ngại bổ nhiệm theo luật, không phải kết luận có tội; chưa được bổ nhiệm thì K cũng không được ký với tư cách CCV.',
[
('Bổ nhiệm được vì chưa có bản án; K ký trước lời chứng trong lúc chờ nếu P bảo đảm sẽ có quyết định sau.','Bỏ trở ngại đang truy cứu và không thể tạo tư cách CCV bằng dự kiến quyết định.'),
('Chưa bổ nhiệm vì phải coi K có tội ngay khi truy cứu; K chỉ được ký lời chứng không thu phí khi chờ Tòa.','Áp điều kiện nghề không đồng nghĩa kết luận có tội, miễn phí không chữa tư cách chưa bổ nhiệm.'),
('Bổ nhiệm được nhưng không cho ký đến khi Tòa xét xong; điều kiện không được bổ nhiệm chỉ áp người bị phạt tù.','Đổi cấm bổ nhiệm thành việc treo quyền hành nghề sau bổ nhiệm, thu hẹp sai căn cứ Điều 14.')],
'Điều 14 đặt điều kiện không được bổ nhiệm cho người đang bị truy cứu, không cần chờ bản án kết tội và không kết luận tội bằng kiểm tra điều kiện nghề. Điều 2, 9 còn tách tư cách CCV đã được bổ nhiệm và người chưa có tư cách. Không chữa bằng cam kết miễn nhiệm tương lai, không thu phí hoặc cho ký trước trong lúc chờ.',
'CC:14 CC:2 CC:9',['Tách điều kiện bổ nhiệm và kết luận có tội','Kiểm tra thời điểm có tư cách CCV','Loại phương án ký trước hoặc bổ nhiệm có điều kiện trái luật'])

case('CC-025',
'K bị Tòa tuyên hạn chế năng lực bằng quyết định còn hiệu lực. Người đại diện đồng ý bằng văn bản cho K tự ký một giao dịch tài sản không phải sinh hoạt hằng ngày, điều kiện khác đủ. K suy ra sự đồng ý ấy cũng chữa trở ngại xin bổ nhiệm CCV, vì mọi lời chứng sẽ có đại diện ký cùng. Chỉ xét hai việc, nhận định đúng?',
'Sự đồng ý có thể đáp ứng nhánh giao dịch tài sản đã nêu, nhưng không loại trở ngại bổ nhiệm; đại diện ký cùng không thay tiêu chuẩn của chức danh CCV.',
[
('Đồng ý giao dịch không có tác dụng vì mọi người bị hạn chế đều bị cấm mọi giao dịch; bổ nhiệm cũng phải loại.','Mở rộng hạn chế giao dịch quá quy tắc sự đồng ý đại diện ở Điều 24.'),
('Đồng ý đủ cho cả giao dịch và bổ nhiệm; người đại diện ký cùng từng lời chứng là hình thức hành nghề đặc biệt cho K.','Điều kiện thực hiện giao dịch cá nhân không thay điều kiện bổ nhiệm hoặc tạo hình thức hành nghề mới.'),
('Giao dịch đủ theo dữ kiện, bổ nhiệm cũng được nếu K chỉ công chứng tài sản thấp hơn giá trị giao dịch được đại diện đồng ý.','Không có ngoại lệ giới hạn giá trị tài sản để bỏ trở ngại bổ nhiệm theo Điều 14.')],
'Điều 24 BLDS đặt sự đồng ý đại diện cho giao dịch tài sản thuộc nhánh đã nêu; Điều 14 Luật Công chứng độc lập loại người bị hạn chế năng lực khỏi bổ nhiệm khi quyết định còn hiệu lực. Không lấy đáp ứng điều kiện giao dịch riêng để suy năng lực chức danh, không tạo ngoại lệ lời chứng ký cùng hoặc giá trị nhỏ.',
'DS:24 CC:14',['Kiểm tra điều kiện giao dịch của người bị hạn chế','Tách giao dịch cá nhân và tiêu chuẩn chức danh','Không suy sự đồng ý đại diện thành ngoại lệ bổ nhiệm'])

case('IMP-T60-064',
'Nhà là tài sản chung A–W. W ủy quyền hợp lệ A bán, văn bản còn hạn nhưng chỉ giá không dưới 3 tỷ. A muốn ký bán 2,8 tỷ; bên mua biết giới hạn, W không chấp thuận giá này, không có lỗi hoặc căn cứ ràng buộc khác. A viện dẫn vợ chồng được đại diện nhau nên vẫn bán được. Nhận định đúng?',
'Vợ chồng có thể ủy quyền nhau, nhưng quyền này vẫn chịu giới hạn giá; không đủ căn cứ dùng giấy cũ để định đoạt cả quyền W ở giá 2,8 tỷ.',
[
('Vợ chồng không được ủy quyền giao dịch tài sản chung nên cả bán 3 tỷ cũng không dùng giấy đã công chứng của W.','HNGĐ cho cơ chế ủy quyền giữa vợ chồng, không cấm chỉ vì tài sản chung.'),
('Ủy quyền còn hạn và A là chồng nên giá 2,8 tỷ được phép; sàn giá chỉ hướng dẫn nội bộ không áp với bên mua.','Thời hạn và quan hệ hôn nhân không mở phạm vi, bên mua đã biết sàn giá.'),
('A được bán 2,8 tỷ nếu cam kết tự bù 200 triệu sau; cam kết với bên mua thay được sự đồng ý W về vượt quyền.','Cam kết riêng của A không tự thay quyền hoặc sự chấp thuận cần thiết của W.')],
'Điều 24 cho vợ chồng đại diện theo ủy quyền, nhưng phải đọc phạm vi hợp lệ để định đoạt tài sản chung theo Điều 35. Điều 141, 143 không cho suy từ thời hạn còn sang quyền hạ sàn, đặc biệt bên mua biết và W không chấp thuận, không có lỗi. Cam kết bù tiền là đề xuất khác, không tự tạo căn cứ ràng buộc W.',
'HN:24 HN:35 DS:141 DS:143',['Nhận cơ chế vợ chồng đại diện nhau','Đối chiếu phạm vi giá và tài sản chung','Xét thiếu căn cứ ràng buộc người được đại diện khi vượt quyền'])

case('IMP-T60-067',
'B nợ chủ nợ C 300 triệu đến hạn; đồng thời C nợ B 300 triệu cùng loại đã đến hạn, đủ điều kiện bù trừ và không thuộc trường hợp cấm. G bảo lãnh nợ B cho C. C muốn giữ khoản mình nợ B riêng, đòi G trả đủ vì B chưa chuyển tiền. Chỉ xét bảo lãnh trong cấu hình bù trừ đủ điều kiện, kết luận đúng?',
'G không phải thực hiện bảo lãnh trong trường hợp C có thể bù trừ đủ nghĩa vụ với B; không chỉ nhìn việc B chưa chuyển tiền để đòi G.',
[
('G trả đủ trước rồi mới cho C bù trừ với B; bảo lãnh luôn được ưu tiên thu trước các khoản đối ứng.','Điều 339 không đặt thứ tự buộc bảo lãnh trả trước trong trường hợp có thể bù trừ.'),
('G trả 150 triệu vì nghĩa vụ đối ứng chỉ giảm một nửa bảo lãnh; số còn lại chờ B và C tự xác nhận.','Đặt mức giảm một nửa không có trong quy tắc và bỏ dữ kiện bù trừ đủ 300 triệu.'),
('G được miễn chỉ khi văn bản bù trừ đã công chứng; đủ điều kiện và cùng đến hạn chưa có ý nghĩa đối với bảo lãnh.','BLDS không đặt công chứng làm điều kiện chung của nhánh bên nhận bảo lãnh có thể bù trừ.')],
'Khoản 3 Điều 339 nói bên bảo lãnh không phải thực hiện khi bên nhận bảo lãnh có thể bù trừ với bên được bảo lãnh. Đề khóa đủ điều kiện, không thuộc cấm và giá trị đối ứng bằng toàn nợ; không dùng việc B chưa chuyển tiền thực tế hoặc chưa công chứng để bỏ ngoại lệ. Cần xét cấu trúc nghĩa vụ đối ứng trước kết luận bảo lãnh phải trả.',
'DS:339',['Đối chiếu chủ thể và nghĩa vụ đối ứng','Kiểm tra đã khóa đủ điều kiện bù trừ','Áp hệ quả với bảo lãnh thay vì chỉ nhìn chưa trả tiền'])

case('IMP-T60-069',
'Công ty TNHH hai thành viên có điều lệ đặt HĐTV thông qua bán tài sản từ 40% tổng tài sản. I bán giá trị 45% theo báo cáo gần nhất, II bán 35%; không căn cứ khác yêu cầu HĐTV với II. Giám đốc là đại diện hợp pháp nhưng chưa được HĐTV thông qua I, nói luật chỉ dùng 50% nên tự ký cả hai. Chỉ xét ngưỡng phê duyệt và tư cách đại diện, nhận định đúng?',
'I cần HĐTV thông qua theo ngưỡng 40% của điều lệ; tư cách đại diện không thay phê duyệt. II không thuộc yêu cầu ngưỡng này theo dữ kiện.',
[
('Cả I và II không cần HĐTV vì Giám đốc là đại diện; ngưỡng luật chỉ dùng khi người ký không có tư cách đại diện.','Đồng nhất quyền ký đại diện với thẩm quyền quyết định, thông qua giao dịch.'),
('I không cần HĐTV vì chưa đạt 50%; điều lệ không được hạ ngưỡng luật xuống 40% dù công ty đã thông qua hợp lệ.','Điều 55 cho điều lệ đặt tỷ lệ hoặc giá trị thấp hơn ngưỡng luật.'),
('Cả I và II cần HĐTV vì điều lệ đã hạ xuống 40%; mọi hợp đồng dưới 50% từ đó cùng phải thông qua.','Hạ ngưỡng không bỏ giới hạn số: II 35% dưới 40% và đề loại căn cứ khác.')],
'Điều 55 cho HĐTV thông qua loại hợp đồng đạt ngưỡng luật hoặc ngưỡng thấp hơn trong điều lệ. Phải dùng báo cáo gần nhất, đối chiếu riêng 45 và 35 với 40. Đại diện hợp pháp theo Điều 12 không tự thay quyết định thuộc HĐTV; không coi điều lệ vô hiệu vì hạ ngưỡng hoặc mở yêu cầu sang mọi hợp đồng dưới 50%.',
'DN:55 DN:12',['Chọn ngưỡng điều lệ hợp lệ','Đối chiếu hai giá trị theo cùng báo cáo','Tách tư cách đại diện ký với cơ quan thông qua'])

case('IMP-T60-070',
'A mua nhà ở xã hội là căn hộ, đã trả đủ sáu năm và có giấy chứng nhận; điều kiện khác để bán theo thị trường đủ. B mua căn hộ xã hội, đặt cọc sáu năm trước nhưng mới trả đủ bốn năm, chưa có ngoại lệ cho bán tự do. Cả hai muốn bán cho người không thuộc diện mua nhà xã hội. Chỉ xét mốc thời gian và cơ chế bán lại, kết luận đúng?',
'A có thể xét bán theo cơ chế thị trường với nghĩa vụ luật định; B chưa đủ năm tính từ trả đủ nên không lấy ngày đặt cọc để áp cùng nhánh.',
[
('A và B cùng bán thị trường vì đều đặt cọc hơn năm năm; trả đủ và giấy chứng nhận chỉ là giấy tờ kiểm tra tại lúc bán.','Sai mốc năm năm và bỏ điều kiện nhánh thị trường.'),
('A vẫn chỉ bán cho chủ đầu tư bằng giá mua cũ; mọi nhà xã hội luôn bị giữ cùng hạn chế dù trả đủ sáu năm và có giấy.','Mở giới hạn thời kỳ đầu thành hạn chế vĩnh viễn, bỏ nhánh sau năm năm đủ giấy.'),
('A bán thị trường được không cần xét thuế vì căn hộ; B cũng bán tự do khi bên mua cam kết giữ nhà đủ một năm còn thiếu.','Căn hộ không miễn nghĩa vụ thuế luật định; cam kết của người mới không làm B đủ mốc từ trả đủ.')],
'Điều 89 tính năm năm từ ngày thanh toán đủ tiền, không từ cọc. Sau thời hạn này và có giấy, A có thể bán căn hộ theo thị trường nếu đủ điều kiện, vẫn thực hiện nghĩa vụ thuế phù hợp. B mới bốn năm từ trả đủ thuộc nhánh hạn chế, không dùng cam kết người mua hoặc ngày giữ chỗ để đổi cơ chế; đề đã loại ngoại lệ khác.',
'NHA:89 DS:328',['Chọn ngày trả đủ thay ngày cọc','Kiểm tra thời hạn và giấy của mỗi căn hộ','Tách cơ chế bán thị trường khỏi nghĩa vụ vẫn phải thực hiện'])

case('IMP-T60-090',
'A giao máy cho B sửa theo hợp đồng song vụ; B giữ máy hợp pháp, máy là đối tượng hợp đồng. Nghĩa vụ trả tiền sửa của A đến hạn 1/10 nhưng chưa thực hiện. B đã sửa đúng hợp đồng. A nói B có quyền cầm giữ ngay từ lúc nhận máy tháng 9, hoặc chỉ phát sinh khi có bản án buộc trả tiền. Chỉ xét mốc phát sinh và đối kháng, nhận định đúng?',
'Cầm giữ phát sinh từ khi tiền sửa đến hạn không được thực hiện; việc giữ máy trước hạn không tự tạo cầm giữ, còn đối kháng gắn việc chiếm giữ theo luật.',
[
('Cầm giữ phát sinh ngay tháng 9 vì B có máy; tiền sửa chưa đến hạn chỉ ảnh hưởng lúc B được bán máy lấy tiền.','Chiếm giữ hợp pháp trước hạn chưa đủ cho phát sinh cầm giữ, không tự có quyền bán máy từ căn cứ này.'),
('Cầm giữ chỉ phát sinh sau bản án, dù tiền đã đến hạn và B giữ đúng đối tượng; trước đó B bắt buộc trả máy ngay.','Đặt điều kiện phán quyết Tòa không có trong mốc phát sinh tại Điều 347.'),
('Cầm giữ phát sinh 1/10 nhưng chỉ đối kháng khi đăng ký như thế chấp; B giữ máy không có ý nghĩa đối kháng.','Cầm giữ đối kháng từ chiếm giữ theo Điều 347, không mặc định đòi đăng ký như thế chấp.')],
'Điều 346 yêu cầu tài sản là đối tượng hợp đồng song vụ và đang được giữ hợp pháp. Điều 347 tách mốc đến hạn nghĩa vụ không được thực hiện với hiệu lực đối kháng từ chiếm giữ. Phải có cấu hình cầm giữ đủ điều kiện mới áp mốc, không lấy việc nhận máy trước hạn để phát sinh sớm hoặc thêm bản án, đăng ký như một điều kiện chung.',
'DS:346 DS:347',['Kiểm tra máy đúng đối tượng hợp đồng song vụ','Chọn mốc đến hạn nghĩa vụ không được thực hiện','Phân biệt chiếm giữ và đăng ký ở hiệu lực đối kháng'])

case('IMP-T60-092',
'Văn bản mang tên cộng tác viên giao K làm việc trả lương, chịu quản lý, điều hành, giám sát của P trong sáu tháng. Các bên không thuộc ngoại lệ hình thức, P muốn chỉ thỏa thuận miệng vì tên cộng tác và dự kiến ký sau tháng thứ hai. K nói gọi cộng tác thì không được hưởng chế độ lao động. Chỉ xét bản chất và hình thức cần thực hiện, kết luận đúng?',
'Đủ dấu hiệu thì coi là hợp đồng lao động bất kể tên; thời hạn sáu tháng trong dữ kiện cần giao kết bằng văn bản, không dùng tên hoặc dự kiến ký sau để bỏ yêu cầu.',
[
('Không là hợp đồng lao động vì tên cộng tác; trả lương và quản lý chỉ làm phát sinh nghĩa vụ dân sự cho tới lúc đổi tiêu đề.','Điều 13 xác định theo nội dung làm việc, trả lương và quản lý, không chỉ tiêu đề.'),
('Là hợp đồng lao động nhưng sáu tháng được nói miệng; chỉ từ 12 tháng mới bắt buộc văn bản và áp chế độ lao động.','Sai ngưỡng hình thức và không thể trì hoãn bản chất quan hệ theo thời hạn tự đặt.'),
('Là lao động, cần văn bản nhưng phải công chứng mới áp chế độ; nếu chưa công chứng thì vẫn cộng tác dù đã ký cả hai.','BLĐ không đặt công chứng làm điều kiện chung để nhận bản chất hợp đồng lao động.')],
'Điều 13 nhận nội dung thực của việc làm có trả công, tiền lương và quản lý, giám sát, kể cả tên khác. Điều 14 đặt hình thức văn bản và ngoại lệ nói miệng theo điều kiện; sáu tháng không thuộc ngoại lệ đề đã loại. Không dùng tên cộng tác, thiếu công chứng hoặc kế hoạch ký sau để tự loại quyền, nghĩa vụ lao động; cần giao kết đúng hình thức.',
'LD:13 LD:14',['Đọc nội dung thực thay tiêu đề','Đối chiếu thời hạn với ngoại lệ hình thức','Không dùng công chứng hoặc kế hoạch ký sau thay yêu cầu hiện tại'])

case('IMP-T60-094',
'Nhóm lao động đều đủ 18 tuổi làm vụ mùa tám tháng, ủy quyền K là người trong nhóm ký hợp đồng. K muốn ủy quyền lại M theo BLDS vì nhóm đồng ý; hồ sơ M ký không kèm danh sách và chữ ký từng lao động. Không có việc từng người trực tiếp ủy quyền hợp lệ M theo thủ tục khác. Hướng xử lý cả hai vấn đề?',
'Quy tắc lao động không cho K ủy quyền lại việc giao kết; nhánh nhóm còn cần hợp đồng văn bản kèm danh sách và chữ ký luật định, không chỉ chữ ký M.',
[
('Nhóm đồng ý thì ủy quyền lại được theo BLDS; M ký là đủ thay danh sách vì đại diện đã được nhóm thừa nhận.','Bỏ cấm ủy quyền lại đặc thù và thành phần văn bản kèm danh sách, chữ ký.'),
('K không được ủy quyền lại nhưng M vẫn ký đủ nếu bổ sung danh sách không cần chữ ký người lao động.','Danh sách không tự chữa người ký thiếu căn cứ và chữ ký từng người vẫn thuộc yêu cầu.'),
('M thiếu danh sách nhưng ủy quyền lại hợp lệ khi chỉ một lần, K vẫn chịu trách nhiệm như người ký ban đầu.','Không có ngoại lệ chỉ ủy quyền lại một lần để bỏ khoản 5 Điều 18.')],
'Điều 18 BLĐ cho nhóm đủ 18, công việc dưới 12 tháng ủy quyền người trong nhóm và yêu cầu hợp đồng văn bản kèm danh sách nội dung, chữ ký từng người. Khoản 5 không cho người được ủy quyền giao kết ủy quyền lại. Không lấy quy tắc chung Điều 564 BLDS hoặc nhóm đồng ý để bỏ luật đặc thù; đề cũng loại căn cứ ủy quyền trực tiếp khác cho M.',
'LD:18 DS:564',['Kiểm tra cấu hình nhóm được phép ủy quyền','Áp cấm ủy quyền lại của luật lao động','Kiểm tra hợp đồng kèm danh sách và chữ ký từng người'])

case('VER26-034',
'A–W đã chia tài sản chung hợp lệ cho A chiếc xe thành riêng. Sau đó chấm dứt hiệu lực việc chia đúng hình thức, không thỏa thuận nhập lại xe; từ sau đó có lương mới của W trong hôn nhân, không ngoại lệ riêng. A nói xe tự chung trở lại, lương W riêng vì W từng không nhận xe. Nhận định đúng?',
'Xe đã chia vẫn riêng A nếu không thỏa thuận khác; lương mới xác định chung theo chế độ và dữ kiện, không đổi theo việc trước đó W không nhận xe.',
[
('Xe nhập lại chung ngay khi chấm dứt chia; lương W riêng vì quy tắc mới chỉ áp tài sản đã từng được chia cho W.','Đảo việc giữ tài sản đã chia riêng và căn cứ xác định thu nhập mới.'),
('Xe vẫn riêng A và lương mới W cũng riêng; bất kỳ lần chia trước đây làm chế độ thu nhập riêng tồn tại mãi.','Bỏ quy tắc xác định tài sản mới theo Điều 33 sau chấm dứt hiệu lực và không có ngoại lệ riêng.'),
('Xe chung trở lại và lương chung; chỉ cần cùng tài khoản mới giữ xe là riêng nếu muốn dùng tiếp như tài sản riêng.','Nhận đúng lương nhưng đặt việc nhập lại xe và điều kiện tài khoản không có trong luật.')],
'Điều 41 tách tài sản đã được chia vẫn riêng trừ thỏa thuận khác với việc xác định tài sản chung, riêng sau mốc chấm dứt theo Điều 33, 43. Đề không nhập lại xe và lương mới không có ngoại lệ riêng, nên xe riêng A, lương mới chung. Không suy phần W từng được chia, tên tài khoản hoặc một sự kiện chấm dứt thành căn cứ đồng nhất hai nhóm tài sản.',
'HN:41 HN:33 HN:43',['Giữ phần tài sản đã chia trước mốc','Áp cơ chế xác định thu nhập mới sau mốc','Kiểm tra có thỏa thuận nhập lại hoặc ngoại lệ riêng hay không'])

case('VER26-063',
'Di sản đã chia cho A 200 triệu, B 400 triệu; không có thỏa thuận khác về nghĩa vụ. Người chết còn nợ hợp pháp 900 triệu; không tài sản di sản khác, không nghĩa vụ ưu tiên khác. Chủ nợ muốn A trả 300 và B 600 vì tỷ lệ nhận là 1:2, dùng cả tài sản riêng bù thiếu. Chỉ xét giới hạn Điều 615, kết luận đúng?',
'Trách nhiệm theo phần đã nhận không vượt 200 của A và 400 của B; tỷ lệ 1:2 không tự làm mỗi người trả vượt giá trị di sản nhận.',
[
('A trả 300, B 600 vì tỷ lệ đúng; nhận di sản đồng nghĩa nhận toàn bộ nợ dù tổng nợ lớn hơn tổng tài sản.','Áp tỷ lệ mà bỏ giới hạn không vượt phần tài sản đã nhận của từng người.'),
('A trả toàn 900 vì nhận ít hơn nên còn nhiều tài sản riêng; B được miễn vì đã nhận phần di sản lớn hơn.','Không có cơ chế phân theo tài sản riêng hoặc miễn người nhận nhiều trong nhánh này.'),
('A và B đều không trả vì nợ được phát hiện sau chia; chủ nợ chỉ được yêu cầu người chết hoặc người giữ di sản chưa chia.','Phát hiện sau chia không tự xóa nghĩa vụ trong phạm vi di sản mỗi người đã nhận.')],
'Khoản 3 Điều 615 yêu cầu mỗi người thực hiện nghĩa vụ tương ứng nhưng không vượt phần tài sản đã nhận, trừ thỏa thuận khác. Đề loại thỏa thuận và di sản khác: tổng giới hạn 600 triệu, riêng A 200 và B 400. Tính tỷ lệ trên toàn nợ không chữa giới hạn, cũng không xóa nợ vì đã chia xong. Không suy nghĩa vụ thiếu còn lại phải dùng tài sản riêng trả.',
'DS:615',['Xác định đã chia và phần từng người nhận','Tách phân bổ tương ứng khỏi trần mỗi người','Kiểm tra không có thỏa thuận nhận thêm nghĩa vụ'])

case('VER26-065',
'A đã nhận và được chia đất thừa kế hợp pháp, muốn chuyển cho em B qua văn bản từ chối di sản ghi chỉ định B nhận. Chưa có chuyển quyền khác; các điều kiện để A xét tặng cho đất đều đáp ứng. A muốn dùng tên từ chối để bỏ thủ tục hình thức giao dịch đất. Cách xử lý đúng?',
'Không dùng từ chối sau phân chia để tự chuyển cho B; cần xét giao dịch tặng cho hoặc cơ chế phù hợp với quyền A đã nhận, cùng thủ tục đất đai.',
[
('A từ chối được sau chia nếu chỉ định B; công chứng tên từ chối làm B có quyền đất không cần xét hình thức tặng cho.','Sai thời điểm từ chối và không thể dùng tên văn bản thay giao dịch chuyển quyền.'),
('A không từ chối nhưng chỉ cần giao giấy gốc B; sau chia người giữ giấy được coi có quyền đất, không cần hợp đồng.','Giữ giấy không tự xác lập quyền đất hoặc thay hình thức chuyển quyền.'),
('A phải hủy toàn bộ phân chia cũ rồi B mới được nhận; không thể tặng cho đất đã nhận dù điều kiện tặng cho đủ.','Cấm một giao dịch hợp lệ không có căn cứ chỉ vì tài sản có nguồn thừa kế.')],
'Điều 620 yêu cầu từ chối trước khi phân chia, không dùng sau khi đã nhận quyền để chỉ định người mới. Đối với phần đã nhận, A có thể xét giao dịch phù hợp như tặng cho khi đủ điều kiện, áp Điều 27 Luật Đất đai về hình thức và thủ tục tương ứng. Không tự chuyển quyền bằng tiêu đề từ chối hoặc giao giấy gốc, không đòi hủy mọi phân chia chỉ để thực hiện tặng cho mới.',
'DS:620 DD:27',['Kiểm tra đã qua thời điểm từ chối','Nhận diện việc chuyển tài sản đã thuộc A','Áp hình thức và thủ tục đúng loại giao dịch đất'])

case('VER26-066',
'A được gọi nhận di sản chưa phân chia, đang có khoản nợ riêng phải trả. Hồ sơ chứng minh A từ chối đất để trốn nghĩa vụ với chủ nợ mình, không phải để tránh nợ người chết; các đồng thừa kế đồng ý và muốn chia đất đó cho em A. A nói chưa chia nên mọi từ chối đều hợp lệ. Kết luận đúng?',
'Trước chia chỉ đáp ứng điều kiện thời điểm; mục đích trốn nghĩa vụ riêng đã chứng minh vẫn loại quyền từ chối trong nhánh này, đồng thuận không chữa được.',
[
('A từ chối hợp lệ vì trước chia; hạn chế trốn nợ chỉ áp khoản nợ người chết chứ không nghĩa vụ riêng người từ chối.','Khoản 1 Điều 620 nhắm nghĩa vụ tài sản của chính người từ chối đối với người khác.'),
('A từ chối được nếu đồng thừa kế nhận phần đó thay A, vì người thân hưởng vẫn giữ tài sản trong gia đình.','Giữ tài sản trong gia đình không tạo ngoại lệ mục đích trốn nghĩa vụ đã xác định.'),
('A được từ chối riêng đất còn nhận tiền; giới hạn chỉ áp từ chối toàn bộ nên chủ nợ tự đòi trên phần tiền.','Không dùng phạm vi từ chối hoặc phần nhận còn lại để chữa mục đích trốn nghĩa vụ đã chứng minh.')],
'Điều 620 đặt điều kiện không nhằm trốn tránh nghĩa vụ tài sản của mình với người khác, ngoài yêu cầu thời điểm và văn bản. Đề xác định rõ nghĩa vụ A và mục đích, không chỉ suy từ việc A có nợ. Vì vậy đáp ứng trước chia hoặc đồng thừa kế đồng ý không đủ; không đổi thành từ chối một loại tài sản để giữ nguyên mục đích bị loại.',
'DS:620',['Tách nghĩa vụ người thừa kế khỏi nợ người chết','Kiểm tra mục đích đã có chứng cứ thay suy đoán','Đối chiếu thời điểm và đồng thuận với điều kiện độc lập'])

case('VER26-076',
'A chết không di chúc; tài sản riêng 900 triệu, nợ hợp pháp 300 triệu được trả từ di sản, không khoản ưu tiên khác. Cha mẹ và vợ A đã chết; hàng thứ nhất chỉ con đẻ B và con nuôi hợp pháp C, cả hai đủ điều kiện, không từ chối. B chăm sóc A lâu hơn và muốn nhận gấp đôi C, chưa có thỏa thuận chia khác. Phần mặc định đúng?',
'Sau trả nợ còn 600 triệu; B và C mỗi người 300 triệu, không tự tăng phần B chỉ vì là con đẻ hoặc chăm sóc lâu hơn.',
[
('B 400, C 200 triệu vì con đẻ gấp đôi con nuôi; khoản nợ vẫn được trả trước nhưng quan hệ con quyết tỷ lệ khác.','Cùng hàng theo Điều 651 hưởng bằng nhau, không đặt tỷ lệ 2:1 cho con đẻ và nuôi.'),
('B và C mỗi người 450 triệu; nợ 300 chỉ do người quản lý di sản trả bằng tài sản riêng, không trừ phần chia.','Bỏ thực hiện nghĩa vụ trong phạm vi di sản trước chia số còn lại.'),
('B toàn 600, C không hưởng khi còn con đẻ; con nuôi chỉ thay vào hàng thứ nhất nếu con đẻ không nhận.','Đặt thứ tự ưu tiên giữa con đẻ và con nuôi không có trong hàng thừa kế.')],
'Điều 651 liệt kê con đẻ, con nuôi hợp pháp cùng hàng và chia bằng nhau trong nhánh luật định. Điều 615 yêu cầu thực hiện nghĩa vụ từ di sản trong phạm vi, nên còn 600 triệu sau trả nợ. Không có khoản chăm sóc riêng đã được xác định hoặc thỏa thuận khác trong đề, không tự chuyển việc chăm sóc lâu hơn thành tăng suất thừa kế; mỗi người 300 triệu.',
'DS:651 DS:615',['Xác định con đẻ và con nuôi cùng hàng','Tách thanh toán nợ khỏi giá trị chia','Giữ chia bằng nhau khi chưa có căn cứ hoặc thỏa thuận khác'])

case('VER26-084',
'K có quyết định hạn chế năng lực còn hiệu lực, Tòa xác định P là đại diện. I mua đồ ăn hằng ngày phù hợp sinh hoạt; II bán máy giá lớn là tài sản K, không giao dịch sinh hoạt hoặc ngoại lệ luật. P chỉ đồng ý miệng cho I, không đồng ý II; người mua II tự cam kết chịu trách nhiệm. Chỉ xét điều kiện đại diện, kết luận đúng?',
'I thuộc ngoại lệ sinh hoạt hằng ngày; II phải có sự đồng ý P theo nhánh đã nêu, không lấy cam kết người mua thay người đại diện.',
[
('Cả I và II đều tự làm được vì K còn hạn chế, chưa mất năng lực; người mua nhận trách nhiệm đủ thay mọi chấp thuận.','Hạn chế khác mất năng lực nhưng vẫn có yêu cầu đại diện cho nhánh tài sản II.'),
('Cả I và II bị cấm cho đến khi P đứng tên sở hữu tài sản; sự đồng ý đại diện không cho K giữ hoặc giao dịch tài sản.','Đại diện không cần trở thành chủ sở hữu và luật còn ngoại lệ sinh hoạt I.'),
('I cần đồng ý P vì mọi tài sản đều bị hạn chế; II chỉ cần công chứng để thay đồng ý của P.','Đảo ngoại lệ sinh hoạt và nhầm công chứng với điều kiện ý chí đại diện.')],
'Điều 24 yêu cầu đồng ý đại diện đối với giao dịch liên quan tài sản của người bị hạn chế, trừ giao dịch phục vụ nhu cầu sinh hoạt hằng ngày hoặc luật có quy định khác. Phải phân loại từng việc, không coi hạn chế là mất quyền sở hữu hoặc cấm mọi giao dịch. Người mua cam kết và thủ tục công chứng không tự thay sự đồng ý còn thiếu của P ở II.',
'DS:24 CC:49',['Đọc quyết định hạn chế và người đại diện','Phân loại ngoại lệ sinh hoạt riêng cho I','Kiểm tra ai có quyền đồng ý giao dịch II'])

case('VER26-093',
'Tòa tuyên giao dịch vô hiệu. B không thể trả hiện vật, giá trị cần hoàn trả đã xác định 400 triệu; B có lỗi gây thiệt hại riêng A 70 triệu, không trùng giá trị tài sản, mọi căn cứ bồi thường đủ. A cũng phải trả lại B khoản 300 triệu đã nhận. Không có thỏa thuận khác. Chỉ xét hoàn trả và thiệt hại, nhận định đúng?',
'Hai bên hoàn trả những gì nhận: B trả giá trị 400, A trả 300 triệu; B còn bồi thường 70 triệu thiệt hại riêng có lỗi, không thay hoặc tính trùng hoàn trả.',
[
('B chỉ trả 70 triệu vì hiện vật không còn, A vẫn trả 300; bồi thường đã thay toàn bộ nghĩa vụ hoàn trả của B.','Không thể trả hiện vật phải trị giá thành tiền, bồi thường không tự thay khoản này.'),
('B trả 400 và A trả 300; thiệt hại 70 được coi luôn nằm trong 400 nên không cần xem riêng dù đề xác định không trùng.','Đồng nhất hoàn trả giá trị tài sản với thiệt hại riêng do lỗi.'),
('B trả 400 và A trả 300, mỗi bên bồi thường 35 triệu vì giao dịch vô hiệu đồng nghĩa hai bên có lỗi bằng nhau.','Không mặc định chia lỗi đều từ sự kiện vô hiệu, đề đã khóa lỗi và thiệt hại riêng của B.')],
'Điều 131 tách khôi phục, hoàn trả tài sản nhận; không thể bằng hiện vật thì trị giá tiền, và bên có lỗi gây thiệt hại phải bồi thường. Đề xác định 70 triệu độc lập, không trùng 400 nên không gộp hoặc mặc định chia lỗi. Nghĩa vụ A hoàn 300 vẫn được xét, không vì B có lỗi mà A tự giữ khoản đã nhận; các bước cần tách trước bù trừ hoặc thanh toán thực tế.',
'DS:131',['Xác định những gì mỗi bên đã nhận','Chuyển hoàn trả hiện vật thành tiền khi không thể trả','Tách thiệt hại có lỗi và tránh cộng trùng hoặc chia lỗi mặc định'])

case('VER26-097',
'A ủy quyền K bán riêng xe X, giấy ghi đến 31/12. K đã hoàn thành việc bán X hợp lệ tháng 8. Tháng 10, A mua xe Y, K muốn dùng giấy X để bán Y giá thấp hơn X, chưa có quyền mới; bên mua biết sự việc, A không chấp thuận và không có lỗi. Chỉ xét quyền đại diện, kết luận đúng?',
'Việc được giao đã hoàn thành là căn cứ chấm dứt; giấy còn ngày 31/12 không tự tạo quyền bán Y, giá Y thấp hơn không thay phạm vi hoặc quyền mới.',
[
('Giấy còn hạn nên K bán Y được, vì Y cùng loại xe và giá thấp hơn giao dịch X đã hoàn thành.','Thời hạn tối đa không bỏ căn cứ việc đã hoàn thành hoặc tự mở đối tượng được ủy quyền.'),
('K chưa hết quyền vì CCV chưa đóng dấu hủy; nhưng được bán Y chỉ khi trả tiền bán cho A sau đó.','Không cần dấu hủy mới có căn cứ chấm dứt, cách chuyển tiền không tạo quyền bán Y.'),
('K hết quyền với X nhưng tự có quyền với Y do A mua tài sản cùng loại sau đó; giá thấp làm giao dịch nằm trong hạn cũ.','Quyền đại diện đối với tài sản cụ thể không tự theo sang tài sản mua mới.')],
'Điều 140 liệt kê công việc được ủy quyền hoàn thành là căn cứ chấm dứt, không chỉ hết ngày ghi trên giấy. Điều 141 giữ đối tượng X, không coi tài sản mới Y hoặc giá thấp là quyền kế tiếp. Đề còn loại chấp thuận và lỗi A, bên kia biết nên không có căn cứ ràng buộc khác theo Điều 143; cần quyền mới phù hợp thay dùng giấy đã xong việc.',
'DS:140 DS:141 DS:143',['Xác định việc X đã hoàn thành','Tách ngày ghi tối đa khỏi căn cứ chấm dứt khác','Kiểm tra đối tượng mới Y và căn cứ quyền mới'])

case('COMP26-CT-013',
'D không là cộng tác viên, tự dịch giấy phục vụ mục đích cá nhân; đủ giấy tờ, tiêu chuẩn ngôn ngữ và năng lực. D xin CCV K chứng thực chữ ký, đã ký sẵn ở nhà và muốn đối chiếu ảnh; không thuộc ngoại lệ khoản 3 Điều 24, không có chữ ký mẫu để áp nhánh cộng tác viên. K cho rằng chỉ cơ quan nhà nước được chứng thực người dịch. Chỉ xét thẩm quyền và thao tác ký theo nhánh không mẫu, kết luận đúng?',
'CCV có thẩm quyền chứng thực chữ ký người dịch theo quy định hiện hành; D chưa có mẫu phải ký theo thủ tục trước người thực hiện, không lấy ảnh chữ ký làm mẫu hợp lệ.',
[
('K không có thẩm quyền dù D ký trước mặt; chỉ cơ quan đại diện nước ngoài được làm chữ ký người dịch.','Điều 5 hiện hành giao CCV các điểm a,b,c, gồm chữ ký người dịch.'),
('K có thẩm quyền nên chữ ký sẵn và ảnh D gửi đã đủ; thẩm quyền rộng miễn mọi yêu cầu ký trước mặt khi chưa đăng ký mẫu.','Nhận đúng chủ thể nhưng bỏ thao tác tại Điều 31 đối với người chưa có chữ ký mẫu.'),
('K được thực hiện nếu tự công chứng nội dung bản dịch, rồi dùng lời chứng nội dung thay việc chứng thực chữ ký D.','Công chứng nội dung và chứng thực chữ ký là thủ tục khác, không được tự đổi yêu cầu để bỏ điều kiện ký.')],
'Khoản 4 Điều 5 hiện hành dẫn chiếu cả chứng thực chữ ký người dịch. Điều 31 vẫn phải thực hiện theo trường hợp có hoặc chưa đăng ký chữ ký mẫu; đề chưa có mẫu nên không thay ký theo thủ tục bằng ảnh chữ ký. Phải tách tư cách người thực hiện, điều kiện người dịch và thao tác chứng thực; không dùng công chứng nội dung như thủ tục thay thế.',
'CT:5 CT:31',['Xác định thẩm quyền CCV theo văn bản hiện hành','Kiểm tra nhánh người dịch chưa đăng ký chữ ký mẫu','Phân biệt chữ ký sẵn và thủ tục chứng thực chữ ký'])

case('COMP26-QT-008',
'Các bên đã ký văn bản công chứng điện tử theo thủ tục. CCV ký số 10:00, tổ chức ký số 10:05; bản PDF gửi cho các bên 10:10. Một bên muốn lấy 10:00 hoặc lúc nhận email làm mốc; không có điều kiện hiệu lực khác đang thiếu. Chỉ xét hiệu lực văn bản theo hai chữ ký số, mốc đúng?',
'Đủ chữ ký số CCV và tổ chức lúc 10:05; không lấy riêng chữ ký CCV 10:00 hoặc việc gửi PDF 10:10 thay mốc này.',
[
('10:00 vì người chứng nhận đã ký số, chữ ký tổ chức chỉ để quản lý hồ sơ không quyết định hiệu lực văn bản.','Bỏ yêu cầu chữ ký số của tổ chức trong mốc văn bản điện tử.'),
('10:10 vì phải có email đến các bên; trước nhận PDF, đủ hai chữ ký số cũng không làm văn bản có hiệu lực.','Đặt điều kiện gửi PDF thay mốc luật định theo hai chữ ký số.'),
('00:00 ngày sau vì văn bản điện tử chỉ có hiệu lực khi đồng bộ dữ liệu cuối ngày, dù ký số đã đủ 10:05.','Không có căn cứ nhánh hiệu lực phải chờ ngày sau hoặc đồng bộ cuối ngày trong đề.')],
'Khoản 2 Điều 64 gắn mốc có chữ ký số CCV và tổ chức hành nghề. Điều 48 cũng yêu cầu hai chữ ký số ở lời chứng điện tử, không chỉ chữ ký người chứng nhận. Đề khóa điều kiện khác đủ: lúc 10:05 đủ cả hai, còn gửi PDF là bước cung cấp bản, không tự tạo mốc 10:10 hoặc chuyển sang ngày kế tiếp.',
'CC:64 CC:48',['Đọc đủ hai chủ thể ký số','Sắp mốc ký số cuối cùng','Tách việc gửi bản và đồng bộ khỏi mốc đã được luật xác định'])

case('COMP26-QT-009',
'P muốn đưa kho hồ sơ sang địa điểm ngoài trụ sở đã đáp ứng an ninh, an toàn, chủ nhà đồng ý, nhưng chưa có đồng ý bằng văn bản Sở Tư pháp. P đã số hóa hồ sơ nên đề nghị chỉ đưa file cho kho mới và hủy bản giấy thuộc diện phải lưu, không có căn cứ tiêu hủy. Chỉ xét địa điểm và bản lưu, phương án đúng?',
'Kho ngoài trụ sở còn cần đồng ý bằng văn bản của Sở; số hóa không tự miễn lưu hồ sơ giấy bắt buộc hoặc cho tiêu hủy khi chưa có căn cứ.',
[
('Chủ nhà và điều kiện an toàn thay ý kiến Sở; số hóa đủ để hủy bản giấy ngay vì nội dung file không đổi.','Hai điều kiện thiếu không được thay bằng đồng ý dân sự hoặc file số hóa.'),
('Cần ý kiến Sở nhưng khi Sở đồng ý địa điểm thì mọi bản giấy tự được tiêu hủy, dù chưa có căn cứ lưu trữ cho phép.','Chấp thuận nơi lưu không là quyết định cho tiêu hủy hoặc miễn nghĩa vụ lưu hồ sơ.'),
('Phải giữ bản giấy, nhưng kho ngoài chỉ cần thông báo email sau chuyển vì cùng tỉnh; văn bản đồng ý chỉ áp ngoài tỉnh.','Điều 68 không đặt ngoại lệ cùng tỉnh để thay đồng ý trước bằng thông báo sau.')],
'Điều 68 yêu cầu đồng ý bằng văn bản Sở nơi đặt trụ sở khi lưu ngoài và vẫn đòi lưu trữ hồ sơ theo loại, thời hạn luật định. Đề xác định bản giấy thuộc diện phải lưu và không căn cứ tiêu hủy, nên số hóa không tự xóa nghĩa vụ. Phải kiểm tra địa điểm và bản lưu độc lập, không lấy đạt an toàn hoặc chủ nhà đồng ý thay thẩm quyền nhà nước.',
'CC:68',['Kiểm tra chấp thuận ngoài các điều kiện kho','Tách bản số hóa với hồ sơ giấy phải lưu','Không suy chấp thuận nơi lưu thành quyền tiêu hủy'])

case('COMP26-QT-011',
'A ở nước ngoài muốn cơ quan đại diện Việt Nam xử lý hai văn bản: I hợp đồng bán nhà tại Việt Nam; II ủy quyền hợp lệ K ở Việt Nam bán chính nhà ấy. Không trở ngại nội dung, chủ thể khác. A nói hai văn bản cùng nhà nên hoặc đều bị cấm hoặc đều công chứng được. Chỉ xét loại giao dịch theo thẩm quyền, kết luận đúng?',
'I thuộc hợp đồng bất động sản Việt Nam bị loại; II không bị loại chỉ vì liên quan cùng nhà, có thể xét công chứng ủy quyền nếu đủ các điều kiện khác.',
[
('I và II cùng bị loại vì đều nhắc căn nhà Việt Nam; không có ngoại lệ cho ủy quyền liên quan bất động sản.','Điều 73 loại các hợp đồng trực tiếp đã liệt kê, không loại mọi văn bản ủy quyền cùng đối tượng.'),
('I và II cùng thực hiện được nếu người mua là công dân Việt Nam; quốc tịch người mua mở thẩm quyền cho bán nhà.','Không có ngoại lệ quốc tịch bên mua để bỏ loại trừ hợp đồng bán BĐS tại Việt Nam.'),
('I không được nhưng II làm A mất quyền sở hữu ngay khi công chứng; K từ đó bán như chủ nhà không cần xét phạm vi.','Ủy quyền trao đại diện trong phạm vi, không tự chuyển quyền sở hữu nhà cho K.')],
'Điều 73 cho công chứng các văn bản ủy quyền nhưng loại hợp đồng bán, chuyển nhượng và các hợp đồng bất động sản tại Việt Nam đã liệt kê. Phải đọc bản chất từng văn bản, không chỉ đối tượng nhà giống nhau. Điều 141 vẫn kiểm tra phạm vi K khi thực hiện ủy quyền; công chứng II không tự cho K thành chủ sở hữu hoặc thay quyền A.',
'CC:73 DS:141',['Phân biệt bán trực tiếp và trao đại diện','Đối chiếu đúng danh mục loại trừ','Giữ phạm vi đại diện và quyền sở hữu sau ủy quyền'])

case('FAM26-012',
'A–W theo chế độ luật định đã chia hợp lệ xe chung cho A thành riêng, không thỏa thuận khác về thu nhập sau chia. W sau đó nhận lương do công việc; A cho thuê xe riêng, có tiền thuê phát sinh sau chia. Không có ngoại lệ khác. A cho rằng cả hai khoản đều riêng vì đã chia tài sản một lần. Phân loại đúng?',
'Lương W vẫn chung theo dữ kiện; tiền thuê là lợi tức từ xe đã chia riêng được xét riêng theo quy tắc sau chia, không gộp mọi thu nhập vào một nhánh.',
[
('Cả lương W và tiền thuê xe đều riêng vì việc chia xe đã chấm dứt toàn bộ chế độ luật định và tách mọi thu nhập mới.','Chia một tài sản không chấm dứt chế độ, không làm tiền lương tự riêng.'),
('Cả hai đều chung vì phát sinh trong hôn nhân; nguồn từ xe đã chia riêng không ảnh hưởng quy tắc lợi tức sau chia.','Bỏ ngoại lệ hoa lợi, lợi tức từ tài sản đã chia trong thời kỳ hôn nhân theo nhánh không thỏa thuận khác.'),
('Lương W riêng vì tài khoản W, tiền thuê xe chung vì người thuê chuyển tiền vào tài khoản A–W cùng tên.','Tên tài khoản không tự thay nguồn thu và căn cứ chế độ tài sản đã xác định.')],
'Điều 14 NĐ126 nói chia tài sản không làm chấm dứt chế độ luật định; tiền lương W vẫn áp Điều 33 trong dữ kiện. Tuy nhiên Điều 40 và quy tắc hướng dẫn giữ riêng hoa lợi, lợi tức từ tài sản đã chia nếu không thỏa thuận khác, nên tiền thuê xe A khác tiền lương W. Không dùng một mốc chia hoặc tài khoản để đồng nhất nguồn thu khác chế độ.',
'ND126:14 HN:33 HN:40',['Giữ chế độ luật định sau chia một tài sản','Phân biệt lương lao động và lợi tức tài sản đã chia','Kiểm tra thỏa thuận khác cùng nguồn tiền thay vì tên tài khoản'])

assert len(rows)==60 and len({r['id'] for r in rows})==60
assert not {r['id'] for r in rows}.intersection(previous_ids)
profile={'version':1,'date':'2026-10-13','scope':'60 câu ngoài 296 mã đã rà: tình huống nhiều điều kiện và 180 nhiễu có căn cứ sai riêng','questions':rows}
report={'date':'2026-10-13','scope':profile['scope'],'questions':decisions,'evidence':proofs,'method':'Giữ mã, bài, trạng thái, loại câu và khóa đúng. Một tình huống đã kiểm tra mỗi câu; từng nhiễu giải thích độc lập. Nhãn độ khó dự kiến không là kết quả đo thực nghiệm.','trial':{'empiricallyCalibrated':False,'syntheticCentralResultsCreated':False}}
for path,obj in [('data/scenario-continuation-60-2026.json',profile),('reports/continuation-60-legal-review-2026-10-13.json',report)]:
 (ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rewritten':len(rows),'parts':dict(collections.Counter(r['after']['part'] for r in rows)),'replacedDistractors':180,'evidenceProvisions':len(proofs)},ensure_ascii=False))
