"""Author application cases and record independently explainable distractors."""
import copy, hashlib, json, re, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ns={'__file__':str(ROOT/'scripts/review-priority-129-2026-10-13.py')}
base=(ROOT/'scripts/review-priority-129-2026-10-13.py').read_text()
exec(base[:base.index('ROWS, DEC, PROOFS')],ns)
bank=ns['bank'];evidence=ns['evidence']
for row in json.loads((ROOT/'data/scenario-priority-129-2026.json').read_text())['questions']:
 bank[row['id']]=row['after']
evidence['CC:41']={'reference':{'document':'Luật Công chứng số 46/2024/QH15 đối chiếu VBHN 50/VBHN-VPQH năm 2026','article':'Điều 41 khoản 2, khoản 4','url':'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/3/50-vbhn-vpqh.pdf'},'excerpt':'2. Hiệp hội công chứng viên Việt Nam ban hành Quy tắc đạo đức hành nghề công chứng để áp dụng trên phạm vi toàn quốc. Quy tắc đạo đức hành nghề công chứng không được trái với quy định của pháp luật và Điều lệ Hiệp hội công chứng viên Việt Nam. 4. Bộ Tư pháp có trách nhiệm phê duyệt Điều lệ của Hiệp hội công chứng viên Việt Nam sau khi thống nhất ý kiến với Bộ Nội vụ; đình chỉ thi hành và yêu cầu sửa đổi nghị quyết, quyết định, quy định, Quy tắc đạo đức hành nghề công chứng do Hiệp hội công chứng viên Việt Nam ban hành trái với quy định của Luật này và quy định khác của pháp luật có liên quan.','origin':'Đối chiếu Điều 41 trên VBHN chính thức ngày 13/10/2026.'}
evidence['CC:66']={'reference':{'document':'Luật Công chứng số 46/2024/QH15 đối chiếu VBHN 50/VBHN-VPQH năm 2026','article':'Điều 66 khoản 3','url':'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/3/50-vbhn-vpqh.pdf'},'excerpt':'Cơ sở dữ liệu công chứng của địa phương bao gồm thông tin về nguồn gốc tài sản, tình trạng giao dịch của tài sản, các thông tin về biện pháp ngăn chặn và cảnh báo rủi ro trong hoạt động công chứng, thông tin về giao dịch đã được công chứng, văn bản công chứng và tài liệu liên quan trong hồ sơ công chứng.','origin':'Đối chiếu Điều 66 trên VBHN chính thức ngày 13/10/2026.'}
evidence['DS:271']={'reference':{'document':'Bộ luật Dân sự số 91/2015/QH13','article':'Điều 271 khoản 2','url':'https://vietlaw.quochoi.vn/Pages/vbpq-print.aspx?ItemID=27892'},'excerpt':'Chủ thể quyền bề mặt có quyền sở hữu đối với tài sản được tạo lập theo quy định tại khoản 1 Điều này.','origin':'Đối chiếu Cơ sở dữ liệu Luật Việt Nam của Quốc hội ngày 13/10/2026; quyền sở hữu nhà và quyền sử dụng đất có thể thuộc các chủ thể khác nhau trong cấu hình quyền bề mặt hợp pháp.'}
rows=[];decisions=[];proofs={}
def case(id,stem,right,wrong,reason,refs,steps):
 old=bank[id];assert id not in {r['id'] for r in rows}
 assert old['type']=='single' and len(wrong)==3 and len(steps)>=3
 new=copy.deepcopy(old);new['question']={'variants':['Tháng 10/2026: '+stem]}
 wrong=iter(wrong);new['answers']=[]
 for a in old['answers']:
  text,why=(right,reason) if a['correct'] else next(wrong)
  new['answers'].append({'id':a['id'],'text':text,'correct':a['correct'],'explanation':why})
 new['answerKey']=[a['id'] for a in new['answers'] if a['correct']]
 new['legalBasis']=[]
 for k in refs.split():
  assert k in evidence,(id,k);proofs[k]=evidence[k]
  if evidence[k]['reference'] not in new['legalBasis']:new['legalBasis'].append(evidence[k]['reference'])
 new.update(explanation=reason,lastVerified='2026-10-13',questionForm='scenario',difficulty='advanced',empiricallyCalibrated=False,reviewStatus='APPLICATION_40_ESTIMATED_PENDING_TRIAL')
 new['integrationSteps']=[{'order':i+1,'application':s} for i,s in enumerate(steps)]
 new['difficultyRationale']='Phải kết hợp: '+'; '.join(steps)+'. Độ khó dự kiến, chưa hiệu chuẩn thực nghiệm.'
 new['source']={'type':'legal-review','id':'APPLICATION40-20261013'}
 new['audit']={**new.get('audit',{}),'evidenceFile':'reports/application-40-legal-review-2026-10-13.json','difficultyReview':'estimated_pending_trial'}
 sha=hashlib.sha256(json.dumps({k:old[k] for k in ('question','answers','legalBasis')},ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 rows.append({'id':id,'sourceSha256':sha,'after':new})
 decisions.append({'id':id,'before':old,'after':new,'answerKey':new['answerKey'],'evidenceKeys':refs.split(),'integrationSteps':new['integrationSteps'],'disposition':'scenario_and_all_distractors_rewritten','distractorRationale':{a['id']:a['explanation'] for a in new['answers'] if not a['correct']}})

case('IMP-T60-051',
'Đất được xác định là tài sản chung A–W, giấy chứng nhận chỉ ghi A. Khi thu hồi, phương án đã duyệt trả 700 triệu giá trị quyền sử dụng đất và 200 triệu cho công trình được xác định là tài sản riêng A. A đề nghị công chứng thỏa thuận xác nhận cả 900 triệu là bồi thường về đất và riêng A vì A đứng tên giấy. Chỉ xét phân loại khoản tiền và căn cứ A nêu, nhận định đúng?',
'700 triệu là bồi thường về đất; tên A không biến quyền chung thành riêng, nên không đủ căn cứ xác nhận cả 900 triệu riêng A.',
[
('900 triệu là bồi thường về đất; tài sản chung nhưng người đứng tên giấy có quyền nhận toàn bộ thành tài sản riêng.','Gộp bồi thường công trình vào bồi thường đất và biến tên trên giấy thành căn cứ sở hữu riêng.'),
('700 triệu là bồi thường về đất; vì chỉ A đứng tên giấy nên riêng khoản đất này thuộc riêng A.','Phân loại đúng khoản tiền nhưng bỏ dữ kiện đất đã được xác định là tài sản chung.'),
('700 triệu là bồi thường về đất; 200 triệu công trình riêng cũng phải nhập chung vì cùng một phương án thu hồi.','Cùng phương án thanh toán không tự đồng nhất nguồn quyền của tài sản riêng và chung.')],
'Khoản trả giá trị quyền sử dụng đất là bồi thường về đất, không gộp khoản bồi thường công trình. Quyền đối với đất đã xác định là chung; tên một người trên giấy không phủ nhận quyền của người kia. Ngược lại, thanh toán cùng một phương án không tự nhập giá trị công trình riêng thành chung. Chưa đủ căn cứ công chứng nội dung A yêu cầu.',
'DD:3 HN:33 HN:34 HN:43',['Tách đối tượng bồi thường đất/công trình','Giữ nguồn quyền chung và riêng đã xác định','Đánh giá chứng cứ một tên trên giấy'])

case('CC-013',
'A ủy quyền hợp lệ cho K ký hợp đồng bán xe đúng phạm vi; K chưa được bổ nhiệm CCV. CCV L đủ điều kiện nhưng K đề nghị tự ký cả phần bên bán và lời chứng, L chỉ đóng dấu. Hồ sơ, ý chí và giao dịch không có trở ngại khác. Cách phân công phù hợp?',
'K có thể ký phần bên bán trong phạm vi đại diện; L phải thực hiện công chứng và ký lời chứng, tổ chức đóng dấu theo luật.',
[
('K không được ký phần bên bán vì chưa là CCV; L ký thay cả bên bán và lời chứng để hoàn thành hồ sơ.','Nhầm tư cách đại diện bên giao dịch với tư cách người chứng nhận; L không tự có quyền đại diện A.'),
('K ký cả phần bên bán và lời chứng nếu L đã kiểm tra hồ sơ; L không cần ký lại lời chứng.','Kiểm tra hồ sơ không trao chức năng chứng nhận cho người chưa là CCV.'),
('K ký bên bán, L ký lời chứng; văn bản có hiệu lực công chứng ngay khi K ký dù tổ chức chưa đóng dấu.','Phân công đúng hai chủ thể nhưng nhầm mốc hiệu lực văn bản giấy.')],
'Đại diện theo ủy quyền cho phép K xác lập giao dịch trong phạm vi A giao, không trao tư cách CCV. L thực hiện công chứng, ký lời chứng và tổ chức đóng dấu. Mốc K ký hợp đồng không tự là mốc văn bản công chứng có hiệu lực; phải giữ cả điều kiện về chủ thể chứng nhận và hình thức lời chứng.',
'DS:141 CC:9 CC:48 CC:6',['Xác định phạm vi ký của người đại diện','Tách người giao dịch và người chứng nhận','Kiểm tra chữ ký lời chứng cùng dấu tổ chức'])

case('VER26-NEW-02',
'Hai doanh nghiệp giao dịch không thuộc quan hệ tiêu dùng, không có luật chuyên ngành khác. X đưa mẫu thuê máy miễn trách nhiệm X khi giao máy hỏng; Y không có thỏa thuận khác về miễn trách nhiệm. Điều khoản này tách được, không ảnh hưởng phần còn lại hợp đồng. X nói Y đã ký nên hoặc giữ miễn trách nhiệm hoặc hủy toàn bộ hợp đồng. Cách đánh giá phù hợp?',
'Điều khoản miễn trách nhiệm không có hiệu lực theo dữ kiện; không vì thế tự loại bỏ những phần hợp đồng còn lại không bị ảnh hưởng.',
[
('Điều khoản miễn trách nhiệm có hiệu lực vì chữ ký Y trên mẫu chính là thỏa thuận khác; giữ nguyên toàn bộ hợp đồng.','Không tự coi chữ ký chấp nhận mẫu là thỏa thuận khác về chính ngoại lệ đang xét; đề đã xác định không có thỏa thuận khác.'),
('Điều khoản miễn trách nhiệm không có hiệu lực nên toàn bộ hợp đồng cũng mất hiệu lực, dù phần còn lại tách được.','Bỏ điều kiện phần vô hiệu không ảnh hưởng phần còn lại theo Điều 130.'),
('Điều khoản miễn trách nhiệm giữ hiệu lực cho đến khi cơ quan hành chính hủy mẫu; phần còn lại được thực hiện bình thường.','Đặt thêm điều kiện hủy mẫu bởi cơ quan hành chính mà BLDS không quy định.')],
'Phải kiểm tra mẫu, nội dung miễn trách nhiệm và ngoại lệ có thỏa thuận khác. Đề đã loại ngoại lệ đó và quan hệ tiêu dùng/chuyên ngành. Theo Điều 405, điều khoản không có hiệu lực; theo Điều 130, phần không bị ảnh hưởng không tự vô hiệu theo. Không dùng chữ ký trên mẫu để bỏ qua các giả thiết này.',
'DS:405 DS:130',['Nhận diện điều khoản miễn trách nhiệm trong mẫu','Kiểm tra ngoại lệ và phạm vi luật áp dụng','Tách hiệu lực điều khoản khỏi phần còn lại'])

case('REFIN26-CC-039',
'Quy tắc Hiệp hội cho CCV công chứng giao dịch của mẹ mình nếu các bên đồng ý. Quy tắc đã được xác định trái Luật Công chứng; Bộ Tư pháp chưa có quyết định đình chỉ. K được giao chứng nhận nhà riêng mẹ K theo quy tắc đó. Phương án đồng thời đúng về hồ sơ và xử lý quy tắc?',
'K không công chứng giao dịch của mẹ; Bộ Tư pháp có quyền đình chỉ quy tắc trái luật và yêu cầu sửa đổi.',
[
('K được công chứng cho đến khi Bộ Tư pháp đình chỉ; Bộ có quyền đình chỉ và yêu cầu Hiệp hội sửa quy tắc.','Nhận đúng thẩm quyền xử lý nhưng coi quy tắc trái luật tạm thời cao hơn lệnh cấm của luật.'),
('K không công chứng giao dịch của mẹ; chỉ Hiệp hội được đình chỉ vì đây là quy tắc do hội tự ban hành.','Đúng về xung đột lợi ích, sai về quyền Bộ Tư pháp xử lý quy tắc trái luật.'),
('K được công chứng nếu mẹ đồng ý; Sở Tư pháp nơi đặt văn phòng đình chỉ quy tắc thay Bộ Tư pháp.','Sự đồng ý không chữa quan hệ bị cấm và đề xuất sai cơ quan đình chỉ quy tắc Hiệp hội.')],
'Quy tắc nghề nghiệp phải phù hợp Luật Công chứng. Việc chưa đình chỉ quy tắc trái luật không cho K vượt lệnh cấm công chứng tài sản của mẹ tại Điều 9. Điều 41 giao Bộ Tư pháp đình chỉ thi hành và yêu cầu sửa quy tắc trái luật; không đồng nhất quyền tự quản với quyền ưu tiên áp dụng trước luật.',
'CC:9 CC:41',['Đối chiếu quy tắc nghề nghiệp với luật','Xử lý xung đột lợi ích của người chứng nhận','Xác định chủ thể và biện pháp xử lý quy tắc'])

case('CAL26-073',
'B sở hữu một ngôi nhà theo quyền bề mặt hợp pháp trên đất C. B cho A hưởng dụng riêng ngôi nhà sáu năm; sau hai năm A mua hợp pháp quyền sử dụng đất của C, không mua nhà B. Các quyền đang xét vẫn hợp lệ. A nói mua đất làm chấm dứt hưởng dụng nhà và A trở thành chủ nhà; B muốn thu nhà ngay. Kết luận đúng?',
'A chưa trở thành chủ ngôi nhà chỉ do mua quyền sử dụng đất; hưởng dụng nhà không chấm dứt theo căn cứ hợp nhất quyền này.',
[
('A mua đất nên đồng thời thành chủ ngôi nhà; hưởng dụng nhà chấm dứt dù quyền sở hữu nhà B chưa được chuyển.','Nhầm hai đối tượng quyền và bỏ dữ kiện B sở hữu nhà theo quyền bề mặt hợp pháp.'),
('A chưa thành chủ nhà nhưng hưởng dụng tự chấm dứt vì chủ đất mới không còn là C, B được thu nhà ngay.','Thay đổi chủ thể của quyền sử dụng đất không phải căn cứ hợp nhất sở hữu nhà với hưởng dụng.'),
('A thành chủ nhà nhưng hưởng dụng vẫn còn bốn năm, trong thời gian đó B tiếp tục có quyền sở hữu nhà.','Vừa tự chuyển nhà cho A vừa giữ quyền B và bỏ căn cứ chấm dứt nếu thực sự hợp nhất sở hữu cùng đối tượng.')],
'Căn cứ người hưởng dụng trở thành chủ sở hữu chỉ áp khi A nhận sở hữu chính tài sản là đối tượng hưởng dụng. Đất và nhà trong cấu hình quyền bề mặt đã nêu là các đối tượng quyền khác nhau; mua quyền sử dụng đất không tự chuyển nhà B cho A. Vì vậy chưa phát sinh căn cứ chấm dứt hưởng dụng nhà đang xét.',
'DS:105 DS:265 DS:271',['Xác định riêng nhà và quyền sử dụng đất','Đối chiếu đối tượng hưởng dụng với tài sản được mua','Kiểm tra có thực sự hợp nhất quyền sở hữu và hưởng dụng'])

case('COMP26-DD-006',
'Văn phòng có CCV A đang chịu quyết định tạm đình chỉ còn hiệu lực, CCV B đang hành nghề bình thường. Hồ sơ bán nhà riêng của mẹ B được phân cho A vì B có quan hệ thân thích. Khách đề nghị đổi lại cho B để tránh người bị đình chỉ và chấp thuận quan hệ mẹ–con. Cách bố trí phù hợp?',
'Cả A và B đều có trở ngại khác nhau với hồ sơ; phải bố trí CCV khác đủ điều kiện, không lấy việc đổi người để bỏ một trở ngại.',
[
('B ký thay A vì đang hành nghề bình thường; sự đồng ý khách hàng khắc phục quan hệ mẹ–con trong hồ sơ này.','Hết trở ngại đình chỉ không xóa xung đột lợi ích của B.'),
('A ký vì không là con người bán; B cùng kiểm tra và ký xác nhận nội bộ để bù tình trạng đình chỉ của A.','Người không có xung đột vẫn bị cấm hành nghề khi quyết định đình chỉ còn hiệu lực.'),
('A ký phần chứng nhận, B ký phần xác nhận tài sản của mẹ; mỗi người chỉ chịu trách nhiệm phần mình đủ điều kiện.','Chia thao tác không làm cả hai người trở thành người chứng nhận hợp lệ.')],
'Phải kiểm tra điều kiện hành nghề và điều kiện riêng của từng hồ sơ. A bị tạm đình chỉ còn hiệu lực nên tổ chức không được cho thực hiện; B không được công chứng giao dịch có liên quan tài sản mẹ. Sự chấp thuận của khách hay ký kiểm tra chéo không thay hai điều kiện độc lập này. Cần CCV khác đủ điều kiện.',
'CC:9 CC:15',['Kiểm tra hiệu lực đình chỉ của A','Kiểm tra quan hệ thân thích của B','Chọn người đồng thời đủ điều kiện nghề nghiệp và hồ sơ'])

case('COMP26-DN-005',
'A góp máy là tài sản chung A–W để lập công ty, W đã đồng ý bằng văn bản, việc chuyển tài sản đúng luật. Các sáng lập viên cố ý thống nhất giá 6 tỷ trong khi giá thực 4 tỷ, gây thiệt hại 300 triệu đã chứng minh. A nói chấp thuận W và biên bản giao máy làm mọi trách nhiệm dừng ở vốn 4 tỷ. Chỉ xét định giá và thiệt hại, xử lý đúng?',
'Chấp thuận và giao máy không chữa định giá cao; các sáng lập viên liên đới góp thêm 2 tỷ và chịu trách nhiệm về thiệt hại 300 triệu.',
[
('Góp thêm 2 tỷ là đủ; thiệt hại 300 triệu đã được tính trong chênh lệch định giá nên không xét trách nhiệm riêng.','Đồng nhất khoản bù chênh lệch vốn với thiệt hại phát sinh, trong khi đề xác định thiệt hại riêng.'),
('Chỉ A góp thêm 2 tỷ và bồi thường 300 triệu; những người cùng cố ý thông qua giá không chịu trách nhiệm.','Loại trách nhiệm liên đới của các sáng lập viên đối với định giá khi thành lập.'),
('Các sáng lập viên chịu thiệt hại 300 triệu; sửa số vốn máy xuống 4 tỷ thay cho việc góp thêm 2 tỷ chênh lệch.','Điều chỉnh con số không thay nghĩa vụ góp bổ sung phần chênh lệch.')],
'Đồng ý định đoạt tài sản chung và chuyển quyền góp vốn là các điều kiện khác với định giá. Khoản 2 Điều 36 đặt nghĩa vụ liên đới góp phần chênh lệch và trách nhiệm thiệt hại do cố ý định giá cao. Chênh lệch là 2 tỷ; thiệt hại 300 triệu đề xác định riêng không tự được hấp thụ vào khoản vốn bổ sung.',
'HN:35 DN:35 DN:36',['Kiểm tra định đoạt và chuyển tài sản góp vốn','Tính chênh lệch định giá','Tách góp bổ sung khỏi bồi thường thiệt hại'])

case('COMP26-QT-005',
'A còn sống, đã gửi giữ di chúc hợp pháp cho nhà và xe tại P. A lập di chúc mới hợp pháp chỉ cho chính ngôi nhà đó, không sửa nội dung về xe, rồi yêu cầu P lưu giữ. P định niêm phong sau khi A về và cho rằng bản mới được gửi giữ sẽ làm cả nội dung xe ở bản cũ hết hiệu lực. Phương án đúng?',
'P niêm phong trước mặt A và giao giấy nhận lưu giữ; việc có di chúc mới về nhà không tự thay phần xe không bị sửa ở bản cũ.',
[
('P niêm phong trước mặt A và giao giấy nhận; di chúc mới gửi giữ thay toàn bộ bản cũ, gồm cả phần xe không được nhắc đến.','Làm đúng thủ tục lưu giữ nhưng mở rộng phạm vi thay thế của di chúc mới khác đối tượng.'),
('P được niêm phong sau khi A về nếu đã thu phí; chỉ phần nhà của di chúc cũ bị bản mới thay thế.','Tách đúng đối tượng nhưng sai yêu cầu niêm phong trước mặt người lập và giấy nhận lưu giữ.'),
('P niêm phong trước mặt A, giao giấy nhận; bản cũ lưu giữ trước nên vẫn ưu tiên cho nhà cho đến khi P trả lại bản cũ.','Thứ tự lưu giữ và việc trả lại bản cũ không quyết định hiệu lực của di chúc hợp pháp lập sau về cùng tài sản.')],
'Điều 61 yêu cầu niêm phong trước mặt người lập và giấy nhận lưu giữ, không thay bằng biên lai hoặc thao tác sau khi khách về. Hiệu lực thừa kế được xét khi mở thừa kế; đối với cùng tài sản phải xét di chúc hợp pháp sau cùng. Bản mới chỉ về nhà không tự thay nội dung xe không bị sửa của bản cũ; gửi giữ không quyết định thứ tự ưu tiên.',
'CC:61 DS:640 DS:643',['Kiểm tra thao tác nhận lưu giữ','Xác định phạm vi tài sản của bản mới','Tách thủ tục lưu giữ khỏi hiệu lực các di chúc'])

case('IMP-T60-077',
'A sở hữu máy đang cầm cố cho B, nghĩa vụ chưa chấm dứt; A muốn tự lựa chọn bán đấu giá máy. Không có luật riêng cho phép định đoạt không cần B chấp thuận. B chưa đồng ý, người đang giữ máy đề nghị tự ký thay A vì sẽ dùng tiền trả nợ. Cách đánh giá đúng?',
'Ý chí A có thể là căn cứ lựa chọn đấu giá, nhưng bán tài sản cầm cố còn cần B đồng ý; giữ máy không tự trao quyền đại diện ký cho A.',
[
('A chọn đấu giá được nên có thể bán ngay không cần B đồng ý; việc giữ máy cũng đủ trao quyền ký cho người giữ.','Bỏ điều kiện định đoạt vật cầm cố và căn cứ đại diện.'),
('Phải có B đồng ý bán máy; khi B đồng ý thì quyền ký thay A tự chuyển cho người đang giữ máy.','Đồng ý định đoạt tài sản không tự tạo ủy quyền đại diện A cho người giữ.'),
('A chỉ có thể chọn đấu giá khi đã bị xử lý tài sản theo luật; B đồng ý cũng không cho phép A tự chọn bán đấu giá.','Thu hẹp sai căn cứ đấu giá theo ý chí chủ sở hữu trong Điều 451.')],
'Điều 451 cho phép bán đấu giá theo ý chí chủ sở hữu hoặc theo luật, nhưng không miễn điều kiện định đoạt tài sản đang cầm cố. Điều 312 yêu cầu sự đồng ý của bên nhận cầm cố cho nhánh định đoạt đang xét. Người giữ tài sản muốn ký nhân danh A còn phải có quyền đại diện phù hợp, không được suy từ việc giữ tài sản hay mục đích trả nợ.',
'DS:451 DS:312 DS:141',['Nhận diện căn cứ lựa chọn đấu giá','Kiểm tra quyền định đoạt khi còn cầm cố','Kiểm tra quyền ký nhân danh chủ sở hữu'])

case('VER26-081',
'A có quyết định Tòa án tuyên mất năng lực hành vi còn hiệu lực. A mang giấy bác sĩ ghi đã hồi phục và hồ sơ nhà đầy đủ để tự ký bán; người giám hộ không tham gia, chưa có quyết định Tòa hủy tuyên bố mất năng lực. A trao đổi mạch lạc và cam kết tự chịu trách nhiệm. Cách xử lý đúng?',
'Không coi giấy bác sĩ và hồ sơ đầy đủ là đủ cho A tự ký; phải xử lý tình trạng pháp lý năng lực và đại diện phù hợp trước khi công chứng.',
[
('Cho A tự ký vì hiện giao tiếp mạch lạc; giấy bác sĩ đã thay quyết định Tòa về tình trạng năng lực.','Kết luận y khoa không tự thay quyết định Tòa hủy tuyên bố mất năng lực.'),
('Cho A tự ký và người giám hộ ký làm chứng sau; chữ ký làm chứng thay được việc tham gia giao dịch thông qua đại diện.','Người làm chứng không thay chức năng người đại diện theo pháp luật.'),
('Cho A tự ký nếu có hai người làm chứng và điểm chỉ; đầy đủ kỹ thuật ký chữa được trở ngại năng lực còn hiệu lực.','Kỹ thuật chứng kiến, ký hoặc điểm chỉ không tạo năng lực giao dịch.')],
'Điều 22 quy định việc hủy quyết định tuyên mất năng lực thuộc Tòa án; giao dịch của người mất năng lực do đại diện theo pháp luật xác lập, thực hiện. Giấy bác sĩ, khả năng giao tiếp tại quầy và giấy nhà không tự thay quyết định đó. Điều 117 và quy trình công chứng đòi kiểm tra năng lực phù hợp, không bù bằng nhân chứng hoặc cam kết.',
'DS:22 DS:117 CC:42 CC:49',['Đọc tình trạng pháp lý năng lực đang còn hiệu lực','Phân biệt chứng cứ y khoa và quyết định Tòa','Xác định chủ thể ký và điều kiện công chứng'])

case('IMP-T60-044',
'Hợp đồng lao động I được giao kết đúng thẩm quyền; một điều khoản trái luật nhưng tách được và không ảnh hưởng phần còn lại. Hợp đồng II được giao kết bởi người không đúng thẩm quyền; tình trạng này chưa được khắc phục, nội dung công việc hợp pháp. Chỉ xét các căn cứ vô hiệu đã nêu, phân loại cả hai đúng?',
'I thuộc căn cứ vô hiệu từng phần; II thuộc căn cứ vô hiệu toàn bộ do thẩm quyền giao kết, không chỉ loại chữ ký sai khỏi hợp đồng.',
[
('I vô hiệu toàn bộ vì có điều khoản trái luật; II vô hiệu từng phần vì nội dung công việc vẫn hợp pháp.','Đảo phạm vi vô hiệu giữa điều khoản tách được và căn cứ người ký không đúng thẩm quyền.'),
('I vô hiệu từng phần; II chỉ vô hiệu phần ghi tên người ký, còn quyền và nghĩa vụ lao động giữ nguyên theo văn bản.','Không thể chữa căn cứ thẩm quyền bằng loại một dòng tên khỏi hợp đồng.'),
('I có hiệu lực vì hai bên ký tự nguyện; II vô hiệu toàn bộ vì thẩm quyền giao kết chưa được khắc phục.','Đúng với II nhưng sự tự nguyện không hợp pháp hóa điều khoản trái luật ở I.')],
'Điều 49 phân biệt phần nội dung trái luật không ảnh hưởng phần còn lại với căn cứ người giao kết không đúng thẩm quyền. I thuộc khoản 2; II thuộc khoản 1 theo giả thiết chưa khắc phục. Không suy rằng nội dung công việc hợp pháp thì thẩm quyền chỉ là lỗi kỹ thuật, cũng không lấy một điều khoản tách được để hủy toàn bộ I.',
'LD:49 LD:18',['Xác định độc lập căn cứ vô hiệu ở từng hợp đồng','Kiểm tra khả năng tách phần nội dung','Phân biệt điều khoản trái luật với người ký không đúng thẩm quyền'])

case('IMP-T60-081',
'A là chủ công ty TNHH một thành viên, đăng ký 5 tỷ nhưng không góp đủ đúng hạn. Công ty đăng ký giảm vốn đúng thủ tục sau đó. Một khoản nghĩa vụ tài chính phát sinh trước ngày đăng ký thay đổi; thiệt hại 700 triệu do không góp đủ vốn đã được chứng minh riêng. A đề nghị chỉ chịu trong vốn thực góp và miễn thiệt hại sau giảm vốn. Đánh giá đúng?',
'Nghĩa vụ phát sinh trước thay đổi xét trách nhiệm A theo vốn đã cam kết; thiệt hại do không góp đủ vốn còn thuộc trách nhiệm bằng toàn bộ tài sản A.',
[
('Cả nghĩa vụ cũ và thiệt hại đều giới hạn vốn thực góp sau đăng ký giảm; thay đổi vốn làm mất căn cứ trách nhiệm trước đó.','Cho thay đổi đăng ký hồi tố xóa trách nhiệm trước ngày thay đổi và giới hạn sai thiệt hại.'),
('Nghĩa vụ cũ xét vốn 5 tỷ cam kết; riêng thiệt hại 700 triệu chỉ trả trong phần vốn chưa góp, không dùng tài sản khác.','Đúng nhánh nghĩa vụ cũ, sai phạm vi tài sản chịu thiệt hại theo khoản 4.'),
('Thiệt hại dùng toàn bộ tài sản A; nghĩa vụ cũ chỉ xét vốn thực góp vì ngày đòi nợ xảy ra sau đăng ký giảm.','Nhầm ngày đòi nợ với ngày nghĩa vụ tài chính phát sinh theo khoản 3.')],
'Khoản 3 Điều 75 gắn trách nhiệm đối với nghĩa vụ tài chính phát sinh trước đăng ký thay đổi với phần vốn đã cam kết. Khoản 4 tách trách nhiệm bằng toàn bộ tài sản đối với thiệt hại do không góp, không đủ hoặc không đúng hạn. Ngày giảm vốn hay ngày chủ nợ đòi không thay ngày nghĩa vụ phát sinh và không xóa thiệt hại đã chứng minh.',
'DN:75',['Giữ mốc nghĩa vụ phát sinh trước thay đổi vốn','Phân biệt vốn cam kết và vốn thực góp','Tách nghĩa vụ tài chính cũ khỏi thiệt hại do thiếu vốn'])

case('IMP-T60-086',
'B nợ A 300 triệu, đã trả 100 triệu. K chỉ được A ủy quyền thu tiền, không có quyền miễn nợ; K tự ghi miễn 200 triệu còn lại, B biết giới hạn đó, A không chấp thuận và không có lỗi. Sau đó A trực tiếp miễn hợp lệ toàn bộ 200 triệu. Chỉ xét trước và sau việc miễn của A, kết luận đúng?',
'Trước khi A miễn, lời K không làm hết 200 triệu; sau khi A miễn hợp lệ phần còn lại, nghĩa vụ được coi đã hoàn thành.',
[
('Nghĩa vụ hoàn thành ngay khi K ghi miễn vì đã được ủy quyền thu; lời miễn của A chỉ xác nhận việc đã hoàn thành.','Mở rộng quyền thu tiền thành quyền miễn nghĩa vụ vượt phạm vi đã biết.'),
('Lời K không làm hết 200 triệu; sau A miễn vẫn phải trả đủ bằng thực tế thì nghĩa vụ mới được coi hoàn thành.','Bỏ căn cứ hoàn thành khi một phần đã thực hiện và phần còn lại được bên có quyền miễn.'),
('Trước A miễn còn 200 triệu; sau A miễn khoản này chỉ tạm ngừng, A có thể tự khôi phục đòi nợ khi cần.','Đồng nhất miễn phần còn lại hợp lệ với tạm ngừng thực hiện nghĩa vụ.')],
'Phải xác định đúng người có quyền miễn. K chỉ được thu tiền nên nhánh vượt quyền không ràng buộc A theo các dữ kiện ở Điều 143. Sau đó chính A miễn hợp lệ toàn bộ phần còn lại, Điều 373 cho coi nghĩa vụ hoàn thành dù B không trả tiếp bằng thực tế. Không hồi tố quyền của K từ việc A tự miễn sau này.',
'DS:141 DS:143 DS:373',['Đọc phạm vi ủy quyền thu tiền','Xét hiệu lực lời miễn ngoài quyền','Áp dụng hoàn thành nghĩa vụ sau miễn hợp lệ'])

case('IMP-T60-096',
'A, B, C có quyền sử dụng đất chung không phân chia được theo phần; mỗi người được cấp giấy thể hiện quyền chung, không có tách thửa. Chỉ A ủy quyền K bán toàn bộ thửa. B, C không đồng ý, không có lỗi; bên mua biết K chỉ đại diện A. K nói mỗi người có giấy riêng nên đủ quyền bán. Kết luận đúng?',
'Các giấy riêng không tự chia quyền chung; ủy quyền A không đủ cho K định đoạt quyền B, C hoặc bán toàn bộ thửa theo dữ kiện.',
[
('Có giấy riêng nên quyền đã được chia theo phần; K được bán toàn bộ thửa rồi thanh toán lại B, C theo giá.','Nhầm số lượng giấy chứng nhận với phân chia quyền và phạm vi đại diện.'),
('Quyền vẫn chung; ủy quyền A cho phép K ký cho cả nhóm nếu tiền bán được chuyển vào tài khoản chung.','Phương thức nhận tiền không thay việc cả nhóm thực hiện hoặc ủy quyền phù hợp.'),
('K chưa bán toàn bộ được nhưng có thể tự bán một phần đất cụ thể theo giấy A mà không cần thủ tục chia quyền.','Đề xác định quyền không phân chia được theo phần và không tách thửa; không tự tạo phần đất riêng.')],
'Khoản 2 Điều 27 yêu cầu nhóm có quyền không phân chia được theo phần cùng thực hiện hoặc ủy quyền người đại diện theo luật. Giấy cấp cho từng người vẫn thể hiện quyền chung, không tự phân quyền đất thành các phần riêng. Theo Điều 141, A không tự cấp quyền B, C cho K; tài khoản nhận tiền không khắc phục việc thiếu quyền.',
'DD:27 DD:135 DS:141',['Phân biệt giấy riêng và quyền được chia riêng','Xác định cơ chế nhóm thực hiện quyền chung','Kiểm tra K có đại diện đủ chủ thể hay không'])

case('IMP-T60-097',
'A không ký được nhưng đọc, nghe và hiểu giao dịch, có năng lực phù hợp. Cả hai ngón trỏ không lấy được vân tay; ngón giữa trái vẫn điểm chỉ được. Không có căn cứ khác bắt buộc làm chứng hoặc phiên dịch. Nhân viên yêu cầu người thân ký thay vì thiếu hai ngón trỏ. Cách xử lý phù hợp?',
'A dùng ngón giữa trái điểm chỉ thay ký, lời chứng ghi ngón và bàn tay; riêng việc không ký được nhưng còn điểm chỉ được không tự buộc người làm chứng.',
[
('A dùng ngón giữa trái nhưng lời chứng không cần ghi ngón, bàn tay; hai ngón trỏ không dùng được đã đủ giải thích.','Đúng lựa chọn ngón khác, sai yêu cầu ghi rõ ngón và bàn tay.'),
('A dùng ngón giữa trái và ghi rõ lời chứng; phải thêm người làm chứng chỉ vì A không ký được dù còn điểm chỉ.','Điều 49 phân biệt trường hợp không ký được và không điểm chỉ được với chỉ không ký được.'),
('Người thân ký thay A với tư cách làm chứng; dấu ngón giữa không được dùng khi cả hai ngón trỏ không có vân tay.','Người làm chứng không tự là đại diện ký thay, luật còn cho dùng ngón khác khi không dùng được hai ngón trỏ.')],
'Điều 50 cho dùng ngón khác khi cả hai ngón trỏ không sử dụng được và phải ghi rõ ngón, bàn tay trong lời chứng. Điều 49 chỉ bắt buộc làm chứng theo nhánh này khi người yêu cầu không ký được và không điểm chỉ được; đề đã loại các căn cứ khác. Không thể thay điểm chỉ hợp lệ bằng chữ ký người thân chưa có quyền đại diện.',
'CC:49 CC:50',['Kiểm tra khả năng ký và điểm chỉ riêng biệt','Chọn ngón còn sử dụng được và nội dung lời chứng','Kiểm tra có thật sự thuộc trường hợp bắt buộc làm chứng'])

case('VER26-062',
'A chết, có 600 triệu tài sản riêng và nợ hợp pháp 100 triệu được thanh toán từ di sản; không có nghĩa vụ, chi phí khác. Không di chúc, cha mẹ A đã chết; hàng thừa kế thứ nhất chỉ có vợ W và con C. C đã thành thai trước A chết, sinh còn sống một tháng sau. Không ai từ chối hoặc bị loại. Sau trả nợ, phần W và C?',
'W và C mỗi người 250 triệu; C đủ điều kiện người thừa kế dù sinh sau thời điểm A chết.',
[
('W và C mỗi người 300 triệu; khoản nợ chỉ đòi người đang quản lý di sản, không trừ trước khi chia.','Công nhận C nhưng không thanh toán nghĩa vụ từ di sản trước chia số tiền còn lại.'),
('W nhận 500 triệu, C không có phần trực tiếp vì chưa sinh khi mở thừa kế và chỉ hưởng qua mẹ.','Bỏ điều kiện sinh còn sống sau mở thừa kế nhưng đã thành thai trước người để lại di sản chết.'),
('W nhận 300 triệu, C nhận 200 triệu vì người đã sinh trước thời điểm mở thừa kế được ưu tiên phần cao hơn.','Nhận diện đủ người và tiền còn lại nhưng đặt ưu tiên không có trong chia cùng hàng.')],
'Theo Điều 613, C đáp ứng điều kiện đã thành thai trước thời điểm A chết và sinh còn sống sau đó. Nghĩa vụ hợp pháp được thực hiện trong phạm vi di sản; còn 500 triệu sau trả 100 triệu. Hai người cùng hàng thứ nhất hưởng bằng nhau theo Điều 651, nên mỗi người 250 triệu, không có ưu tiên cho W vì sinh trước.',
'DS:613 DS:615 DS:651',['Xác định tư cách con đã thành thai','Trừ nghĩa vụ hợp pháp khỏi di sản','Chia bằng nhau cho những người cùng hàng'])

case('COMP26-DN-003',
'A góp máy không đăng ký quyền sở hữu và quyền sử dụng đất phải đăng ký vào công ty. Mọi điều kiện định đoạt, hình thức hợp đồng và giá góp vốn đã hợp lệ. Máy đã giao nhận kèm biên bản đúng nội dung; đất mới ghi vào sổ vốn, chưa làm thủ tục chuyển quyền tại cơ quan có thẩm quyền. Chỉ xét chuyển tài sản góp vốn, nhận định đúng?',
'Máy đã đáp ứng giao nhận theo dữ kiện; việc ghi sổ vốn không thay thủ tục chuyển quyền sử dụng đất cho công ty.',
[
('Máy và đất đều đã chuyển cho công ty vì đã ghi vào vốn; đăng ký chuyển quyền đất chỉ xác nhận số vốn đã có.','Áp quy tắc giao nhận tài sản không đăng ký cho quyền sử dụng đất phải chuyển quyền.'),
('Máy chưa chuyển vì phải đăng ký tên công ty tại cơ quan quản lý; đất đã chuyển khi giá trị được ghi sổ vốn.','Đảo điều kiện của tài sản không đăng ký và tài sản phải đăng ký.'),
('Máy đã chuyển theo biên bản; đất cũng chuyển ngay nếu A tiếp tục đứng tên giấy nhưng giao giấy gốc cho công ty.','Giao giấy tờ không thay thủ tục chuyển quyền sử dụng đất.')],
'Điều 35 tách tài sản không phải đăng ký, chuyển bằng giao nhận xác nhận biên bản, với tài sản phải đăng ký hoặc quyền sử dụng đất cần chuyển quyền cho công ty. Đề đã xác nhận điều kiện hình thức và định đoạt; vấn đề còn lại là thủ tục chuyển quyền đất. Sổ kế toán và giao giấy gốc không thay việc đó.',
'DN:35 DD:27',['Phân loại hai tài sản theo chế độ đăng ký','Kiểm tra giao nhận máy kèm biên bản','Kiểm tra chuyển quyền đất ngoài việc ghi sổ vốn'])

case('COMP26-QT-003',
'Văn bản ghi sai một chữ số giấy tờ nhân thân do lỗi ghi chép; đối chiếu hồ sơ gốc xác định đúng người, sửa không ảnh hưởng quyền, nghĩa vụ. Bên lề trang không đủ chỗ. Đồng thời, các bên mới muốn tăng giá giao dịch từ 4 lên 5 tỷ. Hồ sơ thuộc tổ chức đang lưu trữ hợp lệ. Cách xử lý cả hai đúng?',
'Lỗi nhân thân có thể sửa kỹ thuật bằng trang đính kèm đúng thủ tục; tăng giá là sửa nội dung giao dịch, cần thủ tục và thỏa thuận bằng văn bản phù hợp.',
[
('Cả hai đều sửa kỹ thuật ở trang đính kèm vì cùng là thay con số; văn bản người bán đề nghị đủ cho tăng giá.','Đồng nhất thay con số ảnh hưởng nghĩa vụ với lỗi ghi chép không ảnh hưởng nội dung.'),
('Tăng giá cần thỏa thuận sửa giao dịch; lỗi nhân thân không sửa được vì bên lề hết chỗ nên phải hủy văn bản cũ.','Bỏ phương án trang đính kèm mà Điều 52 cho phép.'),
('Lỗi nhân thân sửa ở trang đính kèm; giá tăng cũng ghi cùng trang nếu CCV xác nhận đã nghe hai bên nói miệng.','Lời nói miệng không thay thỏa thuận hoặc cam kết bằng văn bản cần thiết khi sửa hợp đồng.')],
'Điều 52 xét bản chất lỗi và tác động quyền, nghĩa vụ, không xét chỉ việc có thay chữ số. Lỗi đã đối chiếu có thể ghi ở trang đính kèm đủ nội dung sửa, thời điểm và xác nhận luật định. Tăng giá là thay nghĩa vụ nên áp Điều 53 với thỏa thuận hoặc cam kết bằng văn bản của các bên, không gộp vào sửa kỹ thuật.',
'CC:52 CC:53',['Xác định lỗi không ảnh hưởng quyền nghĩa vụ','Xử lý khi bên lề không đủ chỗ','Tách sửa kỹ thuật khỏi tăng giá giao dịch'])

case('IMP-T60-014',
'C 14 tuổi thừa kế nhà riêng. Cha P và mẹ M là người đại diện theo pháp luật, không có giám hộ hoặc đại diện khác. P muốn ký bên bán nhân danh C và đồng thời đứng bên mua cho chính P; M đồng ý bằng văn bản. Không có ngoại lệ luật cho P giao dịch với chính mình. Chỉ xét đại diện, hướng xử lý đúng?',
'P có tư cách đại diện C nhưng không được dùng tư cách đó ký bán cho chính P; sự đồng ý M không tự tạo ngoại lệ cho việc P giao dịch với mình.',
[
('P được ký cả hai bên vì là cha đại diện theo pháp luật; đồng ý M loại được hạn chế giao dịch với chính mình.','Tư cách đại diện không miễn hạn chế tại khoản 3 Điều 141 khi không có ngoại lệ.'),
('P không được đại diện C trong bất kỳ giao dịch nào vì C có nhà riêng; chỉ người giám hộ do Tòa chỉ định được ký.','Tài sản riêng của con không tự xóa đại diện theo pháp luật của cha mẹ.'),
('P ký cả hai bên nếu M ký làm chứng và C điểm chỉ xác nhận; kỹ thuật ký này thay việc kiểm tra xung đột đại diện.','Chứng kiến và điểm chỉ không khắc phục việc P nhân danh C giao dịch với chính mình.')],
'Điều 136 xác định cha mẹ đại diện con chưa thành niên; Điều 21 quy định điều kiện giao dịch theo tuổi. Tuy nhiên có tư cách đại diện chưa đủ: khoản 3 Điều 141 còn cấm nhân danh người được đại diện giao dịch với chính mình nếu không có ngoại lệ. Đề đã loại ngoại lệ nên không thể lấy chữ ký chấp thuận M hoặc điểm chỉ C để hợp thức phương án P ký cả hai bên.',
'DS:21 DS:136 DS:141 HN:73',['Xác định tuổi và người đại diện','Kiểm tra hai vai trò P trong cùng giao dịch','Phân biệt đồng ý của người thân với ngoại lệ giao dịch với chính mình'])

case('IMP-T60-015',
'A ủy quyền K 17 tuổi mua một vật thông thường với giá tối đa 500 nghìn; loại giao dịch không đòi người đại diện từ đủ 18 tuổi. K lại ký mua một vật giá 900 nghìn. B biết giới hạn, A không chấp thuận và không có lỗi; không thể tách giao dịch thành phần giá 500 nghìn độc lập. Chỉ xét tuổi và phạm vi, kết luận đúng?',
'Tuổi 17 không tự loại K khỏi đại diện; giao dịch 900 nghìn vượt quyền không ràng buộc A theo các dữ kiện đã nêu.',
[
('K chưa đủ 18 tuổi nên không có tư cách đại diện cho cả giao dịch 500 nghìn lẫn 900 nghìn, bất kể luật về loại giao dịch.','Điều 138 cho người từ đủ 15 đến chưa đủ 18 làm đại diện, trừ loại giao dịch luật yêu cầu đủ 18.'),
('K đủ tuổi đại diện nên giao dịch 900 nghìn ràng buộc A; trần 500 nghìn chỉ có hiệu lực giữa A và K.','Điều kiện tuổi không làm mất giới hạn quyền mà B đã biết.'),
('K đủ tuổi, A đương nhiên trả 500 nghìn và K trả 400 nghìn dù giao dịch không thể tách phần độc lập.','Không tự chia một giao dịch vượt phạm vi thành phần ràng buộc A khi đề loại khả năng tách và căn cứ chấp thuận.')],
'Điều 138 cho K làm đại diện đối với loại giao dịch đã nêu, nhưng vẫn phải xét phạm vi ở Điều 141. B biết giới hạn, A không chấp thuận, không có lỗi và giao dịch không tách được; không có căn cứ buộc A theo giao dịch vượt phạm vi tại Điều 143. Phải đánh giá độc lập tuổi, quyền và hậu quả, không dùng một điều kiện để bỏ điều kiện khác.',
'DS:138 DS:141 DS:143',['Kiểm tra ngoại lệ về tuổi theo loại giao dịch','Đối chiếu giá ký với giới hạn quyền','Xét hậu quả khi bên kia biết vượt quyền và không có phần tách được'])

case('IMP-T60-016',
'A không đọc được, yêu cầu công chứng di chúc. CCV K chính là người hưởng di sản; CCV L không có quan hệ hoặc lợi ích liên quan. A chọn X, một người khác cũng hưởng theo di chúc, làm người làm chứng; X có năng lực đầy đủ. A đồng ý với cả hai lợi ích. Phương án phù hợp về người chứng nhận và người làm chứng?',
'Không để K công chứng, có thể bố trí L nếu đủ điều kiện khác; phải thay X bằng người làm chứng đủ điều kiện, không có lợi ích liên quan.',
[
('Đổi K sang L là đủ; X vẫn làm chứng vì lợi ích của người làm chứng không thuộc hạn chế dành cho CCV.','Chỉ khắc phục người chứng nhận, bỏ điều kiện độc lập của người làm chứng và người thừa kế.'),
('Thay X bằng người không hưởng là đủ; K vẫn công chứng vì A đã chấp thuận lợi ích của K bằng văn bản.','Chấp thuận không miễn lệnh cấm công chứng di chúc của người được hưởng.'),
('K công chứng, X làm chứng nếu thêm một người không hưởng; sự có mặt của người độc lập bù lợi ích cả K và X.','Thêm người độc lập không biến người bị cấm thành người đủ điều kiện.')],
'Điều 637 không cho người thừa kế công chứng di chúc; Điều 632 và Điều 49 Luật Công chứng cũng loại người làm chứng có lợi ích thừa kế, lợi ích liên quan. Phải xử lý độc lập cả K và X, không chỉ đổi CCV. Sự đồng ý của A và việc thêm người không hưởng không tạo ngoại lệ; bố trí L còn phải kiểm tra các điều kiện công chứng khác.',
'DS:637 DS:632 CC:49',['Kiểm tra người hưởng là người chứng nhận','Kiểm tra riêng điều kiện người làm chứng','Khắc phục cả hai vai trò có lợi ích liên quan'])

case('IMP-T60-028',
'Hai cá nhân mua bán nhà có sẵn đúng luật, không thuộc giao dịch chủ đầu tư. Giá 2,4 tỷ; cọc 100 triệu được thỏa thuận khấu trừ vào giá, bên mua trả trước thêm 1 tỷ. Nhà đã bàn giao nhưng chưa thanh toán tiếp; không thỏa thuận khác về xác lập sở hữu. Chỉ xét số tiền còn thiếu và mốc sở hữu, kết luận đúng?',
'Còn 1,3 tỷ giá mua; bàn giao khi chưa trả đủ không tự xác lập quyền sở hữu theo quy tắc đang áp dụng.',
[
('Còn 1,4 tỷ vì cọc tách khỏi giá dù đã thỏa thuận khấu trừ; bàn giao đã đủ làm bên mua sở hữu.','Bỏ thỏa thuận trừ cọc và điều kiện đã trả đủ tiền.'),
('Còn 1,3 tỷ; bên mua đã sở hữu vì nhận nhà, còn tiền thiếu chuyển thành nợ riêng không ảnh hưởng mốc sở hữu.','Tính đúng tiền nhưng bỏ điều kiện trả đủ của giao dịch cá nhân theo đề.'),
('Còn 1,4 tỷ; bên mua chưa sở hữu vì chưa trả đủ, cọc chỉ bảo đảm nên không thể khấu trừ vào giá.','Giữ đúng nhánh thời điểm nhưng bỏ thỏa thuận dùng tiền cọc thanh toán giá.')],
'Phải giữ thỏa thuận cọc được khấu trừ khi thực hiện: đã thanh toán vào giá tổng 1,1 tỷ, còn 1,3 tỷ. Với hai cá nhân, nhà có sẵn và không có thỏa thuận khác, Điều 12 Luật Nhà ở đòi trả đủ tiền và nhận bàn giao để xác lập sở hữu theo nhánh này. Nhận nhà không tự thay điều kiện trả đủ; không đổi khoản cọc đã khấu trừ thành khoản nằm ngoài giá.',
'NHA:12 DS:328',['Áp dụng thỏa thuận khấu trừ cọc','Tính số giá mua còn thiếu','Kiểm tra đồng thời trả đủ và bàn giao'])

case('IMP-T60-032',
'Cơ quan có thẩm quyền cử M thay S làm giám hộ. Khi bàn giao tài sản và quyền, nghĩa vụ, S mời CCV N chứng kiến nhưng không mời cơ quan cử hoặc người giám sát G. S nói N là người có chuyên môn nên đủ thay cả hai. G sau đó gửi giấy xác nhận đã đọc bản chụp, không trực tiếp chứng kiến chuyển giao. Cách đánh giá đúng?',
'Không coi N và giấy đọc bản chụp là thay đủ thành phần chứng kiến; chuyển giao phải bảo đảm cơ quan cử, chỉ định và người giám sát theo đúng quy định.',
[
('N chứng kiến đủ thay cả cơ quan cử và G; giấy G đọc bản chụp chỉ bổ sung thông tin chứ không ảnh hưởng chuyển giao.','CCV được mời không tự thay thành phần chứng kiến pháp luật đặt ra.'),
('Phải có cơ quan cử nhưng không cần G; quyết định cử M đã chấm dứt nhiệm vụ giám sát ngay trước bàn giao.','Việc thay người giám hộ không loại yêu cầu người giám sát chứng kiến chuyển giao.'),
('Cần G nhưng không cần cơ quan cử; G đọc bản chụp sau có cùng giá trị với trực tiếp chứng kiến chuyển giao.','Bỏ một thành phần và đồng nhất đọc biên bản sau với chứng kiến việc chuyển giao.')],
'Điều 61 yêu cầu chuyển giao với sự chứng kiến của cơ quan cử, chỉ định người giám hộ và người giám sát việc giám hộ, cùng các nội dung chuyển giao luật định. Người có chuyên môn được mời thêm không tự thay hai vai trò này. Việc đọc bản chụp sau không chứng minh đã trực tiếp chứng kiến; cần tổ chức chuyển giao đúng thành phần và nội dung.',
'DS:61',['Xác định quyết định thay đổi người giám hộ','Phân biệt các thành phần chứng kiến bắt buộc','Kiểm tra chứng kiến thực tế thay vì đọc biên bản sau'])

case('IMP-T60-078',
'A ủy quyền K bán xe với giá không dưới 300 triệu, văn bản đã công chứng. A đồng ý cho K ủy quyền lại M nhưng không cho thay giới hạn giá. K ủy quyền lại cùng hình thức, cho M bán 270 triệu; M ký bán đúng 270 triệu cho B. B biết cả giới hạn ban đầu, A không chấp thuận và không có lỗi. Kết luận đúng?',
'Đồng ý ủy quyền lại và đúng hình thức không cho mở rộng phạm vi; giao dịch 270 triệu ngoài giới hạn không ràng buộc A theo dữ kiện.',
[
('A đã đồng ý ủy quyền lại nên K được đổi giới hạn giá; đúng hình thức làm giao dịch M ký ràng buộc A.','Đồng ý ủy quyền lại không đồng nghĩa đồng ý mở rộng phạm vi quyền.'),
('Ủy quyền lại đúng hình thức nên A chịu giao dịch trong giá 270 triệu; K chỉ phải bù nội bộ 30 triệu cho A.','Không thể tự dùng bù chênh lệch nội bộ để buộc A vào giao dịch vượt quyền mà B biết.'),
('M không được đại diện vì ủy quyền lại bị cấm khi văn bản gốc đã công chứng; giá bán không cần xét nữa.','BLDS cho ủy quyền lại khi có căn cứ và giữ phạm vi, hình thức; không cấm chỉ vì bản gốc công chứng.')],
'Điều 564 tách căn cứ được ủy quyền lại, giới hạn không vượt phạm vi gốc và hình thức phù hợp. Đề mới đáp ứng căn cứ đồng ý và hình thức, còn hạ sàn giá là vượt quyền. B biết, A không chấp thuận, không có lỗi, nên không có căn cứ ràng buộc A theo nhánh Điều 143. Không hợp thức bằng yêu cầu K bù tiền nội bộ.',
'DS:564 DS:141 DS:143',['Kiểm tra căn cứ được ủy quyền lại','Đối chiếu phạm vi gốc và hình thức','Xét giao dịch người nhận ủy quyền lại thực hiện vượt giới hạn'])

case('IMP-T60-089',
'A sở hữu nhà, B đang có quyền hưởng dụng hợp pháp nhà đó. C gây hư hại xâm phạm quyền A và B. Thiệt hại riêng A là 300 triệu sửa nhà, riêng B là 80 triệu lợi ích sử dụng bị mất, đều đã chứng minh, có quan hệ nhân quả và không trùng nhau. C chỉ muốn bồi thường người đứng tên nhà. Chỉ xét tư cách yêu cầu và tránh tính trùng, nhận định đúng?',
'A và B đều có quyền yêu cầu với thiệt hại riêng tương ứng; không loại B chỉ vì không là chủ sở hữu và không cộng trùng các thiệt hại.',
[
('Chỉ A được yêu cầu cả 380 triệu; quyền hưởng dụng không cho B trực tiếp yêu cầu khi nhà vẫn thuộc A.','Điều 170 bảo vệ cả chủ sở hữu và người có quyền khác; không tự chuyển yêu cầu riêng B cho A.'),
('A và B đều được yêu cầu 380 triệu mỗi người vì cùng bị xâm phạm quyền trên một ngôi nhà.','Nhận đúng tư cách nhưng tính trùng thiệt hại đã được xác định riêng.'),
('B chỉ yêu cầu được nếu đã mua lại nhà; trước đó quyền hưởng dụng cho dùng nhà nhưng không được bảo vệ bằng bồi thường.','Đặt điều kiện sở hữu không có trong quyền yêu cầu của người có quyền khác đối với tài sản.')],
'Điều 170 không giới hạn người yêu cầu ở chủ sở hữu; người có quyền khác đối với tài sản cũng được bảo vệ khi quyền bị xâm phạm. B có hưởng dụng hợp pháp, không chỉ là người giữ giấy hoặc được lợi không có quyền. Đề đã xác định thiệt hại riêng và không trùng, nên tách khoản yêu cầu tương ứng, không nhân đôi cả tổng cho mỗi người.',
'DS:170 DS:261',['Phân biệt chủ sở hữu và người hưởng dụng','Nhận diện quyền bị xâm phạm của từng người','Tách thiệt hại riêng không cộng trùng'])

case('INH26-019',
'Di sản đã chia: A nhận 800 triệu, B nhận 400 triệu tính tại lúc chia. Sau đó C là người thừa kế bị bỏ sót được xác định có phần đáng hưởng 300 triệu tại thời điểm chia. Nay tài sản A tăng giá gấp đôi, B vẫn giá cũ; không có thỏa thuận khác về xử lý. C yêu cầu lấy nhà A để chia lại. Phương án mặc định đúng?',
'A thanh toán C 200 triệu, B 100 triệu theo tỷ lệ đã nhận; không tự chia lại hiện vật vì giá tài sản A tăng sau chia.',
[
('A thanh toán 240 triệu, B 60 triệu theo giá hiện tại 1,6 tỷ và 400 triệu; không chia lại hiện vật.','Giữ đúng hình thức tiền nhưng dùng tỷ lệ giá hiện tại thay phần đã nhận tại lúc chia.'),
('A và B mỗi người trả 150 triệu vì cùng là người thừa kế cũ; mức tài sản từng người nhận không ảnh hưởng nghĩa vụ.','Thay tỷ lệ 2:1 của phần đã nhận bằng chia đều theo đầu người.'),
('A phải trả nhà để chia lại vì nhà tăng giá; B trả C 100 triệu, không cần tính nghĩa vụ tiền A theo phần cũ.','Không có thỏa thuận khác nên Điều 662 không tự cho chia lại hiện vật.')],
'Điều 662 lấy phần người mới đáng hưởng tại thời điểm chia và tỷ lệ phần các người cũ đã nhận. A:B là 800:400 = 2:1, nên phân 300 triệu thành 200 và 100 triệu. Giá tài sản thay đổi sau chia không tự thay tỷ lệ hoặc tạo quyền chia lại hiện vật khi không có thỏa thuận khác.',
'DS:662',['Giữ giá và phần đáng hưởng tại thời điểm chia','Tính tỷ lệ phần người cũ đã nhận','Phân biệt thanh toán tiền mặc định và chia lại hiện vật'])

case('REFIN26-CC-011',
'K đã được ghi nhận hành nghề hợp pháp theo hợp đồng lao động tại P, không là thành viên hợp danh. K muốn làm thêm CCV tại Q theo hợp đồng buổi tối, không chấm dứt ở P, cho rằng không góp vốn nên không bị cấm đồng thời. Chỉ xét hình thức và số nơi hành nghề, đánh giá đúng?',
'Hợp đồng lao động là hình thức hành nghề hợp pháp, không tự tạo hợp danh; K vẫn không được đồng thời hành nghề công chứng tại P và Q.',
[
('K không là hợp danh nên không có quyền thực hiện công chứng tại P; chỉ sau góp vốn mới được coi là hành nghề.','Nhầm hình thức hợp đồng lao động với việc chỉ hỗ trợ nghiệp vụ, bỏ Điều 37.'),
('K được hành nghề ở P và Q nếu không trùng giờ; cấm đồng thời chỉ dành cho người góp vốn hợp danh.','Điều 9 cấm đồng thời hành nghề tại hai tổ chức, không đặt ngoại lệ không trùng giờ hay không góp vốn.'),
('K ký hợp đồng Q thì tự trở thành thành viên hợp danh Q, nên phải chuyển vốn từ P dù chưa từng góp vốn P.','Hợp đồng lao động không tự tạo tư cách hợp danh hoặc vốn góp.')],
'Điều 37 ghi nhận CCV làm theo hợp đồng lao động là hình thức hành nghề riêng với hợp danh. Tuy nhiên Điều 9 vẫn cấm đồng thời hành nghề tại hai tổ chức trở lên; giờ buổi tối và không góp vốn không làm mất tính đồng thời. Phải tách tư cách người lao động với giới hạn nơi hành nghề, không suy từ một hình thức hợp pháp ra quyền làm ở nhiều nơi.',
'CC:37 CC:9',['Nhận đúng hình thức hợp đồng lao động','Phân biệt hợp đồng lao động với tư cách hợp danh','Kiểm tra cấm đồng thời hành nghề tại hai tổ chức'])

case('REFIN26-CC-016',
'Giấy đăng ký hoạt động P bị hỏng. Đồng thời P thay Trưởng Văn phòng hợp pháp, nội dung này chưa được đăng ký thay đổi. Không có thu hồi hoặc chấm dứt tổ chức. P muốn xin cấp lại nguyên nội dung cũ rồi chỉ thông báo tên trưởng mới cho khách. Chỉ xét giấy và nội dung đăng ký, phương án phù hợp?',
'Giấy hỏng không làm P thành tổ chức mới; phải xử lý đăng ký thay đổi Trưởng và cấp lại giấy theo nội dung phù hợp, không chỉ phục hồi thông tin cũ.',
[
('Chỉ cấp lại nguyên nội dung cũ vì lý do giấy hỏng; tên Trưởng mới cập nhật nội bộ thay cho đăng ký thay đổi.','Bỏ nghĩa vụ đăng ký thay đổi nội dung thực sự đã phát sinh.'),
('Xin thành lập lại P vì giấy hỏng kết hợp đổi Trưởng làm tổ chức cũ chấm dứt, hồ sơ cũ chuyển sang tổ chức mới.','Giấy hỏng và thay Trưởng không tự là căn cứ lập tổ chức mới hoặc chấm dứt P.'),
('Đăng ký tên Trưởng mới nhưng tiếp tục dùng bản tự in của giấy hỏng; thay đổi nội dung không cần giấy do Sở cấp lại.','Điều 26 quy định thay Trưởng được cấp lại giấy, không lấy bản tự in thay giấy được cấp.')],
'Điều 26 tách cấp lại do giấy hỏng và thay đổi nội dung đăng ký hoạt động. Khi đồng thời đổi Trưởng, không chỉ cấp lại một giấy giữ thông tin không còn đúng; phải đăng ký nội dung thay đổi và được cấp lại theo quy định. Không có dữ kiện chấm dứt, thu hồi nên không yêu cầu thành lập một tổ chức mới chỉ vì giấy bị hỏng.',
'CC:26',['Phân biệt giấy hỏng và tổ chức chấm dứt','Nhận diện thay đổi Trưởng là nội dung đăng ký','Chọn xử lý bảo đảm cả giấy và thông tin đăng ký đúng'])

case('REFIN26-QT-008',
'A bán xe với tư cách cá nhân, đã ký sẵn ở nhà. A không thuộc trường hợp đăng ký chữ ký mẫu của tổ chức. Khi đến văn phòng, A đọc hiểu và đề nghị thêm điểm chỉ cạnh chữ ký, cho rằng điểm chỉ trước CCV thay được yêu cầu ký trước CCV. Không có căn cứ miễn khác. Cách xử lý phù hợp?',
'Thực hiện việc ký trước CCV theo quy tắc thông thường; có thể điểm chỉ đồng thời theo đề nghị A, nhưng dấu điểm chỉ không tự thay điều kiện ký đã áp dụng.',
[
('Giữ chữ ký ký sẵn và thêm điểm chỉ trước CCV là đủ; dấu mới xác nhận thay cho việc ký trước người chứng nhận.','Đề nghị điểm chỉ đồng thời không tạo ngoại lệ ký trước cho cá nhân không có chữ ký mẫu theo luật.'),
('Yêu cầu ký trước CCV nhưng từ chối thêm điểm chỉ vì A ký được, trường hợp này không phải di chúc.','Điều 50 cho ký và điểm chỉ đồng thời theo đề nghị người yêu cầu, không chỉ dành di chúc.'),
('Giữ chữ ký ký sẵn nếu A gửi ảnh chữ ký để lưu làm mẫu; sau đó điểm chỉ đồng thời theo đề nghị.','Ảnh chữ ký cá nhân không tạo trường hợp đăng ký chữ ký mẫu dành cho chủ thể luật định.')],
'Khoản 1 Điều 50 đặt việc ký trước sự chứng kiến trực tiếp, ngoại lệ ký trước ở khoản 2 dành đúng chủ thể và điều kiện đăng ký chữ ký mẫu. A là cá nhân không thuộc ngoại lệ; đề nghị điểm chỉ đồng thời được phép theo khoản 4 nhưng không tự miễn yêu cầu ký. Cần xử lý hai thao tác theo hai căn cứ riêng.',
'CC:50 CC:48',['Kiểm tra cá nhân có thuộc ngoại lệ chữ ký mẫu','Áp dụng yêu cầu ký trước CCV','Phân biệt điểm chỉ đồng thời với miễn việc ký'])

case('REFIN26-QT-022',
'Hồ sơ đất I chỉ có cảnh báo rủi ro cũ chưa rõ nguồn, chưa có quyết định ngăn chặn và chưa xác minh hiện trạng. Hồ sơ II có quyết định áp dụng biện pháp khẩn cấp tạm thời cấm chuyển dịch quyền đối với đất, đã kiểm tra còn hiệu lực. Hai bên đều cam kết chịu trách nhiệm. Cách xử lý cả hai phù hợp?',
'I cần làm rõ cảnh báo và điều kiện hiện tại trước quyết định; II không được xử lý chuyển nhượng như đất đủ điều kiện chỉ dựa cam kết của các bên.',
[
('Cả hai được công chứng khi bên bán cam kết; cảnh báo và quyết định cấm chỉ là nguồn thông tin để các bên tự đánh giá.','Hạ quyết định cấm còn hiệu lực thành cảnh báo, bỏ điều kiện thực hiện quyền đất.'),
('Cả hai phải bị từ chối vĩnh viễn ngay khi có dữ liệu; cảnh báo cũ có cùng hiệu lực cấm như quyết định ở II.','Đồng nhất cảnh báo chưa rõ với quyết định ngăn chặn và bỏ việc làm rõ thông tin I.'),
('I xác minh thêm; II được công chứng nếu bên mua đồng ý nhận rủi ro, vì quyết định chỉ hạn chế bên bán tự thực hiện.','Sự đồng ý bên mua không chữa tình trạng đất đang bị áp dụng biện pháp cấm chuyển dịch.')],
'Cơ sở dữ liệu chứa cả cảnh báo và ngăn chặn, phải phân loại và kiểm tra hiệu lực nguồn. I chưa đủ thông tin để tự quyết là được hay cấm, cần làm rõ theo Điều 42 và 66. II đã có biện pháp khẩn cấp còn hiệu lực, không đáp ứng điều kiện thực hiện quyền theo Điều 45 Luật Đất đai; cam kết rủi ro không thay điều kiện đó.',
'CC:42 CC:66 DD:45',['Phân loại cảnh báo và quyết định cấm','Kiểm tra hiện trạng và hiệu lực từng nguồn','Đối chiếu điều kiện chuyển quyền thay vì dựa cam kết'])

case('REFIN26-QT-025',
'Người bán không đọc được cần người làm chứng cho hợp đồng bán xe, không phải di chúc. Có ba người đều đọc, nghe, ký và trực tiếp chứng kiến được: I là cậu, có năng lực đầy đủ nhưng được hưởng 1% giá bán nếu giao dịch hoàn tất; II là người ngoài 17 tuổi chưa có năng lực đầy đủ; III là cậu khác có năng lực đầy đủ, không quyền, lợi ích, nghĩa vụ liên quan. Chọn người đáp ứng điều kiện đã nêu?',
'III đáp ứng; I có lợi ích liên quan, II chưa có năng lực đầy đủ; riêng quan hệ cậu–cháu không tự loại III trong hợp đồng này.',
[
('I và III cùng đáp ứng vì đều có năng lực đầy đủ; khoản 1% chỉ là thỏa thuận ngoài hợp đồng không ảnh hưởng làm chứng.','Lợi ích phụ thuộc hoàn tất giao dịch là lợi ích liên quan, không mất đi do đặt ở thỏa thuận khác.'),
('II đáp ứng vì 17 tuổi được tự giao dịch thông thường; I và III bị loại chỉ vì cùng có quan hệ họ hàng.','Năng lực tự thực hiện một số giao dịch không bằng năng lực đầy đủ; luật không loại mọi người cậu.'),
('Không ai đáp ứng: III bị loại vì họ hàng, I vì lợi ích, II vì tuổi; phải chọn người không có quan hệ gia đình.','Hai loại trừ I và II đúng nhưng thêm lệnh cấm quan hệ gia đình không có trong điều kiện chung đã xét.')],
'Điều 49 đòi người làm chứng có năng lực hành vi dân sự đầy đủ và không quyền, lợi ích, nghĩa vụ liên quan. I có lợi ích trực tiếp theo giá bán, II chưa đủ năng lực đầy đủ; Điều 21 không cho đồng nhất khả năng tự giao dịch của người 17 tuổi với điều kiện làm chứng. III không bị loại chỉ vì là cậu, khi đề xác định các điều kiện khác đủ.',
'CC:49 DS:21',['Kiểm tra năng lực đầy đủ chứ không chỉ khả năng ký','Nhận diện lợi ích phụ thuộc hoàn tất giao dịch','Phân biệt họ hàng với lợi ích liên quan'])

case('VER26-002',
'A và W có nhà chung đã xác định, giấy chỉ tên A. Dự thảo bán toàn nhà do A tự ký ghi không cần sự đồng ý W vì A đứng tên. W không đồng ý bằng văn bản, không đại diện hoặc căn cứ khác cho A định đoạt toàn bộ. CCV chỉ rõ thiếu sót, A từ chối sửa và chỉ thêm câu tự chịu trách nhiệm. Cách xử lý đúng?',
'Không coi tên trên giấy và cam kết là đủ quyền định đoạt toàn nhà; nếu A không khắc phục nội dung, điều kiện vi phạm thì từ chối công chứng.',
[
('Công chứng phần A ký rồi xác nhận W chỉ có quyền đòi chia tiền; tên A trên giấy thay yêu cầu đồng ý với việc bán nhà chung.','Một tên không phủ nhận quyền chung và không tự thay chấp thuận định đoạt.'),
('Công chứng nhưng bỏ câu không cần W khỏi lời chứng; giữ dự thảo bán toàn bộ vì A chịu trách nhiệm về tài sản chung.','Loại một câu khỏi lời chứng không khắc phục quyền định đoạt còn thiếu trong giao dịch.'),
('CCV tự bổ sung W thành bên bán và ký xác nhận thay W; việc xác định nhà chung đã đủ làm phát sinh đồng ý W.','CCV không có quyền tạo ý chí hoặc ký thay người có quyền.')],
'Điều 33 và 35 yêu cầu giữ tính chất tài sản chung và điều kiện định đoạt bất động sản chung; giấy một tên không tự trao quyền toàn bộ. CCV phải chỉ rõ và yêu cầu khắc phục theo Điều 42. Khi A kiên quyết giữ giao dịch thiếu điều kiện và cam kết thay cho chấp thuận W, không được hợp thức bằng xóa câu, thêm lời chứng hoặc ký thay W.',
'HN:33 HN:34 HN:35 CC:42',['Xác định nguồn quyền chung ngoài tên giấy','Kiểm tra quyền định đoạt toàn bộ nhà','Xử lý khi người yêu cầu không khắc phục sau được giải thích'])

case('VER26-015',
'Hợp đồng giữa A và công ty F từng công chứng ở P; P đã giải thể, X đang lưu trữ hợp lệ hồ sơ. A và F muốn sửa hợp đồng bằng văn bản; K đại diện F ở lần đầu nhưng quyền K đã chấm dứt trước lần sửa, các bên biết và F không cấp quyền mới. K đề nghị ký tại X vì X giữ hồ sơ nên không cần chứng minh đại diện nữa. Kết luận phù hợp?',
'X là tổ chức phù hợp theo nhánh lưu trữ; vẫn phải có người có quyền đại diện F ở lần sửa, hồ sơ cũ không gia hạn quyền K đã hết.',
[
('X đúng nơi và K được ký tiếp vì người ký ban đầu giữ quyền sửa cho đến khi hợp đồng chấm dứt, dù đại diện đã hết.','Quyền đại diện được kiểm tra tại giao dịch sửa, không tự tồn tại theo thời hạn hợp đồng cũ.'),
('K không ký được nhưng A và F phải tìm một văn phòng bất kỳ cùng tỉnh; X giữ hồ sơ chỉ để cấp bản sao.','Nhận đúng thiếu quyền, sai ngoại lệ nơi đang lưu trữ theo Điều 53.'),
('X được để K ký nếu A đồng ý nhận rủi ro; chấp thuận của A thay sự cấp quyền từ F trong giao dịch sửa.','Bên đối tác không tự cấp quyền đại diện F hoặc bỏ yêu cầu chủ thể đúng quyền.')],
'Điều 53 xác định tổ chức đang lưu trữ thực hiện khi tổ chức cũ giải thể, nhưng không miễn kiểm tra chủ thể giao dịch sửa theo thủ tục công chứng. Điều 140, 141 đòi quyền còn phù hợp tại thời điểm ký; K đã hết quyền, hồ sơ lần đầu chỉ là chứng cứ lịch sử. Cần đại diện F có căn cứ hiện tại, không gia hạn bằng việc chọn đúng tổ chức.',
'CC:53 DS:140 DS:141',['Xác định đúng nơi lưu trữ sau giải thể','Giữ yêu cầu thỏa thuận sửa của các bên','Kiểm tra đại diện còn hiệu lực tại lần sửa'])

case('VER26-019',
'CCV K có hai hồ sơ hợp lệ khác: I bán nhà riêng của cha đẻ vợ K; II bán xe riêng của cậu K. K không có tài sản, lợi ích hoặc nghĩa vụ trong II, cậu không thuộc quan hệ nào khác trong danh sách cấm; không có trở ngại khác. Khách cả hai đồng ý K thực hiện. Chỉ xét quan hệ thân thích luật định, phân công phù hợp?',
'K không thực hiện I; riêng quan hệ cậu trong dữ kiện II không tự là căn cứ cấm K, vẫn kiểm tra các điều kiện công chứng còn lại.',
[
('K thực hiện cả hai vì tài sản không thuộc K và khách đã đồng ý; danh sách thân thích chỉ áp khi K cùng sở hữu.','Lệnh cấm còn áp tài sản, lợi ích của thân thích luật định, không cần K cùng sở hữu.'),
('K không thực hiện cả hai vì mọi người có quan hệ họ hàng đều được coi là thân thích bị cấm trong mọi giao dịch.','Mở rộng danh sách luật định sang mọi quan hệ họ hàng, trái giả thiết II.'),
('K thực hiện I vì cha vợ không phải cha K, nhưng không thực hiện II vì cậu thuộc cùng dòng máu với K.','Đảo danh sách luật định bằng phân biệt cùng dòng máu không được luật dùng ở đây.')],
'Điểm c khoản 1 Điều 9 bao gồm cha đẻ của vợ nên I thuộc cấm, bất kể đồng ý khách. Với II, phải đối chiếu danh sách thay vì cấm mọi họ hàng; đề loại quan hệ khác trong danh sách và lợi ích K nên riêng quan hệ cậu không tự cấm. Điều này không phải kết luận mọi hồ sơ người cậu đều được công chứng mà còn kiểm tra đầy đủ điều kiện khác.',
'CC:9',['Đối chiếu riêng cha vợ với danh sách','Không suy từ mọi họ hàng thành cùng trường hợp cấm','Giữ giới hạn kết luận về II theo dữ kiện loại lợi ích khác'])

case('VER26-025',
'Nhà trị giá 1,2 tỷ đang tranh chấp tính chất tài sản giữa A và W; không có căn cứ chứng minh riêng, không chế độ thỏa thuận khác. Sau đó W chết không di chúc, không nợ; cha mẹ W đã chết, hàng thứ nhất chỉ A và con C thành niên. Không ai từ chối hoặc bị loại. A muốn bán cả nhà chỉ vì giấy đứng tên A. Chỉ xét phần quyền, kết luận đúng?',
'Nhà được coi là chung; sau chia phần W, A có 900 triệu phần quyền, C có 300 triệu; giấy tên A không tự cho A bán toàn bộ.',
[
('Nhà là riêng A theo tên giấy nên không có di sản W; A có quyền bán toàn bộ mà không cần xét C.','Bỏ suy đoán chung khi không có chứng cứ riêng và dữ kiện tranh chấp đã nêu.'),
('Nhà chung nên A và C mỗi người 600 triệu sau W chết; tên giấy không quyết định toàn bộ quyền bán.','Gộp toàn nhà vào di sản rồi chia, bỏ phần 600 triệu vốn thuộc A ngoài di sản W.'),
('Nhà chung nhưng A hưởng toàn bộ phần W vì là người đang đứng tên; C chỉ có quyền yêu cầu trợ cấp chứ không phần nhà.','Tên trên giấy không tạo ưu tiên cho người cùng hàng thừa kế.')],
'Theo Điều 33, không có căn cứ chứng minh riêng trong tranh chấp thì coi chung. Chỉ phần W là di sản: 600 triệu; A và C cùng hàng nhận 300 triệu mỗi người. A giữ phần vốn có 600 cộng thừa kế 300, C 300. Điều 141 không cho A tự đại diện C, tên giấy không tự xóa phần quyền C khi bán toàn nhà.',
'HN:33 HN:66 DS:612 DS:651 DS:141',['Giải quyết tính chất chung khi không chứng minh riêng','Tách phần người sống khỏi di sản','Chia phần W và xác định ai có quyền định đoạt'])

case('VER26-028',
'W và A thỏa thuận bằng văn bản cho A đưa tài sản chung vào kinh doanh, giao dịch A ký thuộc phạm vi đó. Sau đó có khoản nợ ngân hàng được xác định hợp pháp là nghĩa vụ chung cả hai. A–W ký nội bộ chuyển toàn nghĩa vụ sang A, ngân hàng không đồng ý chuyển và không có ngoại lệ luật. W nói từ đầu A tự ký nên mình hết nghĩa vụ. Đánh giá đúng?',
'Thỏa thuận kinh doanh cho A tự giao dịch trong phạm vi, không tự biến tài sản thành riêng; thỏa thuận chuyển nợ nội bộ chưa đủ giải phóng W với ngân hàng.',
[
('A tự ký nên tài sản đã thành riêng và nợ chỉ A chịu; thỏa thuận chuyển nợ chỉ xác nhận W vốn không có nghĩa vụ.','Bỏ dữ kiện nợ đã được xác định chung và nhầm quyền tự giao dịch với sở hữu riêng.'),
('Tài sản vẫn chung nhưng W hết nghĩa vụ khi A ký nhận toàn nợ; ngân hàng chỉ cần được thông báo việc chuyển.','Chuyển nghĩa vụ cần bên có quyền đồng ý khi không có ngoại lệ, không chỉ thông báo.'),
('Thỏa thuận nợ chưa giải phóng W; giao dịch A ký ban đầu vô hiệu chỉ vì thiếu chữ ký W trong từng lần dù đúng phạm vi.','Nhận đúng chuyển nghĩa vụ nhưng bỏ cơ chế A tự giao dịch theo thỏa thuận kinh doanh.')],
'Điều 36 cho người được thỏa thuận tự thực hiện giao dịch liên quan tài sản chung đưa vào kinh doanh, không tự chuyển sở hữu riêng. Đề xác định khoản nợ là nghĩa vụ chung, không suy ngược chỉ từ chữ ký A. Theo Điều 370, thỏa thuận chuyển nghĩa vụ chưa có ngân hàng đồng ý không tự làm W hết nghĩa vụ với ngân hàng trong cấu hình không có ngoại lệ.',
'HN:36 DS:370',['Xác định phạm vi quyền tự giao dịch','Giữ tính chất tài sản và nghĩa vụ đã xác định','Kiểm tra sự đồng ý của chủ nợ khi chuyển nghĩa vụ'])

case('VER26-036',
'A–W lập bản lựa chọn chế độ tài sản trước kết hôn nhưng không công chứng, chứng thực; chưa có quyết định Tòa công nhận hoặc khắc phục hình thức. Sau kết hôn, họ muốn công chứng một văn bản chia tài sản chung cụ thể và ghi rằng việc này chứng minh bản đầu đã đủ hình thức ngay từ trước cưới. Chỉ xét hai cơ chế pháp lý, hướng phù hợp?',
'Không xác nhận bản đầu đã đủ hình thức chỉ từ việc chia tài sản sau cưới; cần tách chế độ thỏa thuận trước kết hôn với thỏa thuận chia tài sản chung trong hôn nhân.',
[
('Công chứng chia tài sản sau cưới làm bản đầu tự có đủ hình thức từ trước cưới; hai văn bản là một thủ tục áp dụng liên tục.','Thỏa thuận sau cưới không tự chứng minh sự kiện công chứng/chứng thực của văn bản trước cưới.'),
('Bản đầu thiếu hình thức nên A–W không được thỏa thuận chia bất kỳ tài sản chung nào trong hôn nhân dù điều kiện chia đều đáp ứng.','Thiếu điều kiện lựa chọn chế độ không tự loại cơ chế chia tài sản chung theo Điều 38.'),
('Chỉ cần đổi ngày văn bản sau cưới thành ngày trước cưới để áp chế độ thỏa thuận; tài sản chia và ý chí hai bên không đổi.','Không được tạo sự kiện hoặc thời điểm sai để thay điều kiện thời điểm và hình thức của văn bản.')],
'Điều 47 đặt thời điểm trước kết hôn và văn bản được công chứng hoặc chứng thực cho lựa chọn chế độ. Điều 38 là cơ chế chia tài sản chung trong thời kỳ hôn nhân với các điều kiện riêng. Hai bên có thể yêu cầu xem xét văn bản sau theo cơ chế phù hợp, nhưng không tự tạo chứng cứ bản đầu đã đủ hình thức hoặc ghi lùi ngày; đề cũng chưa có quyết định Tòa về khắc phục.',
'HN:47 HN:38',['Kiểm tra thời điểm và hình thức văn bản đầu','Tách lựa chọn chế độ với chia tài sản cụ thể','Không dùng văn bản sau để xác nhận sự kiện trước chưa có'])

case('VER26-048',
'C 17 tuổi có đất riêng được thừa kế, muốn tự ký chuyển nhượng cho một cá nhân; giao dịch không thuộc ngoại lệ kinh doanh BĐS, mọi điều kiện đất khác đều đạt. Cha mẹ là đại diện theo pháp luật không đồng ý, không có căn cứ thay thế khác. C chọn chứng thực thay công chứng vì cho rằng người 17 tuổi tự giao dịch được. Chỉ xét tuổi và hình thức, nhận định đúng?',
'Công chứng hoặc chứng thực là lựa chọn hình thức luật cho phép, nhưng không thay yêu cầu đồng ý của đại diện đối với giao dịch bất động sản của C.',
[
('Chứng thực đủ cho C tự ký không cần cha mẹ; chỉ công chứng mới yêu cầu xem xét đồng ý với người từ 15 đến dưới 18.','Điều kiện năng lực theo loại tài sản áp độc lập với lựa chọn công chứng hay chứng thực.'),
('C cần cha mẹ đồng ý nhưng khi có đồng ý vẫn bắt buộc làm cả công chứng và chứng thực cho cùng hợp đồng.','Đúng nhánh tuổi nhưng đổi lựa chọn hình thức thành hai thủ tục tích lũy.'),
('C tự ký được vì đất riêng do thừa kế; giới hạn người chưa đủ 18 chỉ áp tài sản chung với cha mẹ.','Nguồn thừa kế riêng không miễn điều kiện giao dịch bất động sản ở Điều 21.')],
'Điều 21 cho người từ đủ 15 đến chưa đủ 18 tự thực hiện nhiều giao dịch nhưng giao dịch bất động sản còn cần đồng ý đại diện theo pháp luật. Điều 27 Luật Đất đai cho hình thức công chứng hoặc chứng thực trong nhánh đề nêu; lựa chọn đó không khắc phục thiếu điều kiện năng lực. Đất riêng và đầy đủ điều kiện đất không thay sự đồng ý đang thiếu.',
'DS:21 DD:27',['Xác định loại tài sản và ngoại lệ tự giao dịch theo tuổi','Phân biệt hai hình thức được lựa chọn','Kiểm tra đồng thời năng lực và hình thức'])

case('VER26-089',
'Giao dịch ký tháng 3/2023 do người thứ ba cố ý làm A hiểu sai đối tượng, dẫn đến A xác lập giao dịch; hành vi và quan hệ nhân quả đã có chứng cứ. A chỉ biết hoặc phải biết lừa dối từ tháng 3/2026, yêu cầu Tòa tuyên vô hiệu tháng 10/2026; không có căn cứ thời hiệu khác. B nói mình không lừa và đã hơn hai năm từ ký nên A hết quyền. Kết luận đúng?',
'Lừa dối của người thứ ba vẫn thuộc căn cứ xem xét; thời hiệu nhánh này tính từ khi biết hoặc phải biết lừa dối, nên không kết luận hết chỉ theo ngày ký.',
[
('A hết thời hiệu vì hơn hai năm từ ký; ai thực hiện lừa dối không làm thay đổi mốc bắt đầu là ngày giao dịch.','Nhầm mốc thời hiệu lừa dối với ngày xác lập giao dịch.'),
('A còn trong hai năm từ biết nhưng chỉ được đòi người thứ ba, vì B không trực tiếp lừa thì giao dịch không bị xem xét vô hiệu.','BLDS bao gồm hành vi cố ý của người thứ ba dẫn đến xác lập giao dịch.'),
('Giao dịch bị lừa không bị hạn chế thời hiệu nên A yêu cầu được vào mọi thời điểm, không cần xét lúc biết.','Đồng nhất lừa dối với nhóm Điều 123, 124 không hạn chế thời hiệu.')],
'Điều 127 bao gồm hành vi cố ý của người thứ ba có quan hệ nhân quả với xác lập giao dịch; không loại căn cứ vì B không trực tiếp lừa. Điều 132 tính hai năm từ biết hoặc phải biết giao dịch do lừa dối, không mặc định từ ngày ký. Tháng 3 đến tháng 10/2026 chưa đủ hai năm theo các dữ kiện đã khóa; đây là yêu cầu Tòa xem xét, không tự coi mọi thông tin sai là vô hiệu.',
'DS:127 DS:132',['Kiểm tra cố ý và quan hệ nhân quả của người thứ ba','Chọn đúng mốc biết hoặc phải biết','Phân biệt thời hiệu lừa dối với căn cứ không hạn chế'])

case('VER26-094',
'Năm 2022, A–B lập giao dịch mua bán giả tạo để che giấu tặng cho; giao dịch tặng cho được xác định độc lập đáp ứng đầy đủ điều kiện có hiệu lực, không nhằm trốn tránh nghĩa vụ với người thứ ba. Năm 2026 có yêu cầu Tòa xem xét vô hiệu mua bán giả tạo. Chỉ xét thời hiệu và giao dịch bị che giấu, nhận định đúng?',
'Yêu cầu về giả tạo không bị giới hạn hai năm; mua bán giả tạo vô hiệu nhưng không tự kéo theo vô hiệu tặng cho đã đủ điều kiện.',
[
('Mua bán không còn bị yêu cầu vô hiệu vì quá hai năm; tặng cho cũng mất hiệu lực vì không được thể hiện trong tên văn bản mua bán.','Sai thời hiệu của giả tạo và bỏ dữ kiện tặng cho độc lập đủ điều kiện.'),
('Yêu cầu giả tạo không hạn chế thời hiệu; cả mua bán và tặng cho đều vô hiệu dù tặng cho độc lập đủ điều kiện.','Bỏ quy tắc giữ giao dịch bị che giấu nếu không có căn cứ vô hiệu của nó.'),
('Mua bán vẫn có hiệu lực vì che một tặng cho hợp pháp; chỉ tặng cho bị xét vô hiệu sau quá hai năm từ xác lập.','Giao dịch che giấu hợp pháp không hợp thức giao dịch giả tạo và không đổi nhóm thời hiệu giả tạo.')],
'Điều 124 tách giao dịch giả tạo vô hiệu khỏi giao dịch bị che giấu, giao dịch sau vẫn có hiệu lực nếu không có căn cứ vô hiệu riêng. Đề xác định tặng cho đã đáp ứng điều kiện và không có nhánh trốn nghĩa vụ. Khoản 3 Điều 132 không hạn chế thời hiệu yêu cầu đối với giả tạo, nên không lấy hai năm từ 2022 để bỏ yêu cầu năm 2026.',
'DS:124 DS:132',['Xác định giao dịch che giấu và giao dịch thực','Kiểm tra điều kiện độc lập của tặng cho','Áp đúng nhóm thời hiệu của giả tạo'])

assert len(rows)==40
profile={'version':1,'date':'2026-10-13','scope':'40 câu còn dễ: viết lại tình huống và toàn bộ nhiễu, không chứng nhận độ khó thực nghiệm','questions':rows}
report={'date':'2026-10-13','scope':profile['scope'],'questions':decisions,'evidence':proofs,'method':'Một tình huống được kiểm tra cho mỗi câu; giữ ID và khóa đúng; từng nhiễu có lý do sai riêng. Không dùng cờ từ khóa làm phép đo độ khó.','trial':{'empiricallyCalibrated':False,'syntheticCentralResultsCreated':False}}
for name,obj in [('data/scenario-application-40-2026.json',profile),('reports/application-40-legal-review-2026-10-13.json',report)]:
 (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rewritten':len(rows),'parts':dict(collections.Counter(r['after']['part'] for r in rows)),'distractors':120,'legalProvisions':len(proofs)},ensure_ascii=False))
