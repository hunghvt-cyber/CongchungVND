"""Author 60 additional application cases; retain the separate, sealed 67-case layer."""
import copy, hashlib, json, re, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
read = lambda p: json.loads((ROOT/p).read_text())
files = re.findall(r"'([^']+\.json)'", re.search(r'const files = \[(.*?)\];', (ROOT/'app.js').read_text(), re.S).group(1))
bank = {q['id']: q for f in files for q in read('data/'+f)}
for row in read('data/application-wording-2026.json')['questions']:
    q = bank[row['id']]
    if row.get('status'): q['status'] = row['status']
    if row.get('variants'): q['question']['variants'] = row['variants']
    q['presentationReview'] = 'application-wording-2026-10-12'
for row in read('data/scenario-refinements-2026.json')['questions']:
    bank[row['id']] = row['after']
prior_ids = {r['id'] for r in read('data/scenario-refinements-2026.json')['questions']}
evidence = {}
def register(p, origin):
    ref = p.get('reference', p)
    text = p.get('excerpt') or p.get('evidenceExcerpt')
    doc, art = ref.get('document',''), str(ref.get('article',''))
    if not text or not ref.get('url','').startswith('https://'): return
    group = 'DS' if 'Dân sự' in doc else 'HN' if 'Hôn nhân' in doc else 'CC' if 'Công chứng số 46' in doc else 'ND126' if '126/2014' in doc else None
    nums = re.findall(r'\d+',art)
    if group and nums:
        k = group+':'+nums[0]
        if k not in evidence or len(text)>len(evidence[k]['excerpt']):
            evidence[k] = {'reference': {k:ref[k] for k in ('document','article','url')}, 'excerpt':text, 'origin':p.get('origin',origin)}
for path in sorted((ROOT/'reports').glob('*.json')):
    obj = json.loads(path.read_text())
    if not isinstance(obj,dict): continue
    if isinstance(obj.get('evidence'),dict):
        for p in obj['evidence'].values():
            if isinstance(p,dict): register(p,str(path.relative_to(ROOT)))
    if isinstance(obj.get('articles'),dict):
        for p in obj['articles'].values(): register(p,str(path.relative_to(ROOT)))
    for row in obj.get('questions',[]) if isinstance(obj.get('questions'),list) else []:
        for p in row.get('provisions',[]): register(p,str(path.relative_to(ROOT)))
for article, url, excerpt in [
    ('405','https://vbpl.moj.gov.vn/dongthap/Pages/vbpq-toanvan.aspx?ItemID=95942&Keyword=',
     'Điều 405. Hợp đồng theo mẫu. 2. Trường hợp hợp đồng theo mẫu có điều khoản không rõ ràng thì bên đưa ra hợp đồng theo mẫu phải chịu bất lợi khi giải thích điều khoản đó. 3. Trường hợp hợp đồng theo mẫu có điều khoản miễn trách nhiệm của bên đưa ra hợp đồng theo mẫu, tăng trách nhiệm hoặc loại bỏ quyền lợi chính đáng của bên kia thì điều khoản này không có hiệu lực, trừ trường hợp có thỏa thuận khác.'),
    ('330','https://vbpl.moj.gov.vn/hanoi/Pages/vbpq-toanvan.aspx?ItemID=95942',
     'Điều 330. Ký quỹ. 1. Ký quỹ là việc bên có nghĩa vụ gửi một khoản tiền hoặc kim khí quý, đá quý hoặc giấy tờ có giá vào tài khoản phong toả tại một tổ chức tín dụng để bảo đảm việc thực hiện nghĩa vụ. 2. Trường hợp bên có nghĩa vụ không thực hiện hoặc thực hiện không đúng nghĩa vụ thì bên có quyền được tổ chức tín dụng nơi ký quỹ thanh toán, bồi thường thiệt hại do bên có nghĩa vụ gây ra, sau khi trừ chi phí dịch vụ. 3. Thủ tục gửi và thanh toán thực hiện theo quy định của pháp luật.'),
    ('261','https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/95942/VanBanGoc_91.2015.QH13.P1.pdf',
     'Điều 261. Quyền của người hưởng dụng. 1. Tự mình hoặc cho phép người khác khai thác, sử dụng, thu hoa lợi, lợi tức từ đối tượng của quyền hưởng dụng. 2. Yêu cầu chủ sở hữu tài sản thực hiện nghĩa vụ sửa chữa đối với tài sản theo quy định tại khoản 4 Điều 263 của Bộ luật này; trường hợp thực hiện nghĩa vụ thay cho chủ sở hữu tài sản thì có quyền yêu cầu chủ sở hữu tài sản hoàn trả chi phí. 3. Cho thuê quyền hưởng dụng đối với tài sản.')]:
    evidence['DS:'+article] = {'reference':{'document':'Bộ luật Dân sự số 91/2015/QH13','article':'Điều '+article,'url':url},'excerpt':excerpt,'origin':'Đối chiếu điều khoản nguồn chính thức ItemID 95942 ngày 13/10/2026; trích đoạn phục vụ tình huống.'}
# Some older records preserve a clause citation but a complete article excerpt.
# The retained proof is reused, with its original primary-source URL and provenance.
for article, url, excerpt in [
    ('305','https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/95942/VanBanGoc_91.2015.QH13.P1.pdf',
     'Điều 305. Nhận chính tài sản bảo đảm để thay thế cho việc thực hiện nghĩa vụ của bên bảo đảm. 1. Bên nhận bảo đảm được quyền nhận chính tài sản bảo đảm để thay thế cho việc thực hiện nghĩa vụ của bên bảo đảm nếu có thỏa thuận khi xác lập giao dịch bảo đảm. 2. Trường hợp không có thỏa thuận theo quy định tại khoản 1 Điều này thì bên nhận bảo đảm chỉ được nhận chính tài sản bảo đảm để thay thế cho việc thực hiện nghĩa vụ khi bên bảo đảm đồng ý bằng văn bản.'),
    ('306','https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/95942/VanBanGoc_91.2015.QH13.P1.pdf',
     'Điều 306. Định giá tài sản bảo đảm. 1. Bên bảo đảm và bên nhận bảo đảm có quyền thỏa thuận về giá tài sản bảo đảm hoặc định giá thông qua tổ chức định giá tài sản khi xử lý tài sản bảo đảm. Trường hợp không có thỏa thuận thì tài sản được định giá thông qua tổ chức định giá tài sản. 2. Việc định giá tài sản bảo đảm phải bảo đảm khách quan, phù hợp với giá thị trường.'),
    ('348','https://vbpl.moj.gov.vn/toaannhandantoicao/Pages/vbpq-toanvan.aspx?ItemID=95942&Keyword=91%2F2015%2FQH13',
     'Điều 348. Quyền của bên cầm giữ. 1. Yêu cầu bên có nghĩa vụ phải thực hiện đầy đủ nghĩa vụ phát sinh từ hợp đồng song vụ. 2. Yêu cầu bên có nghĩa vụ phải thanh toán chi phí cần thiết cho việc bảo quản, giữ gìn tài sản cầm giữ. 3. Được khai thác tài sản cầm giữ để thu hoa lợi, lợi tức nếu được bên có nghĩa vụ đồng ý. Giá trị của việc khai thác tài sản cầm giữ được bù trừ vào giá trị nghĩa vụ của bên có nghĩa vụ.'),
    ('370','https://www.wipo.int/wipolex/en/legislation/details/17200',
     'Điều 370. Chuyển giao nghĩa vụ. 1. Bên có nghĩa vụ có thể chuyển giao nghĩa vụ cho người thế nghĩa vụ nếu được bên có quyền đồng ý, trừ trường hợp nghĩa vụ gắn liền với nhân thân của bên có nghĩa vụ hoặc pháp luật có quy định không được chuyển giao nghĩa vụ. 2. Khi được chuyển giao nghĩa vụ thì người thế nghĩa vụ trở thành bên có nghĩa vụ.'),
    ('263','https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/95942/VanBanGoc_91.2015.QH13.P1.pdf',
     'Điều 263. Quyền và nghĩa vụ của chủ sở hữu tài sản. 1. Định đoạt tài sản nhưng không được làm thay đổi quyền hưởng dụng đã được xác lập. 2. Yêu cầu Tòa án truất quyền hưởng dụng trong trường hợp người hưởng dụng vi phạm nghiêm trọng nghĩa vụ của mình. 3. Không được cản trở, thực hiện hành vi khác gây khó khăn hoặc xâm phạm đến quyền, lợi ích hợp pháp của người hưởng dụng.')]:
    evidence['DS:'+article] = {'reference':{'document':'Bộ luật Dân sự số 91/2015/QH13','article':'Điều '+article,'url':url},'excerpt':excerpt,'origin':'Đối chiếu điều khoản BLDS 91/2015 nguồn chính thức ngày 13/10/2026; trích phần áp dụng, không gồm toàn điều nếu không cần.'}
ROWS, DEC, PROOFS = [], [], {}
def rev(id, stem, right, wrong, reason, refs, steps):
    old = bank[id]
    assert id not in prior_ids and old['type']=='single' and len(wrong)==3 and len(steps)>=3
    new = copy.deepcopy(old)
    new['question'] = {'variants':['Tháng 10/2026: '+stem]}
    wi = iter(wrong)
    new['answers'] = []
    for a in old['answers']:
        text, why = (right,reason) if a['correct'] else next(wi)
        new['answers'].append({'id':a['id'],'correct':a['correct'],'text':text,'explanation':why})
    new['answerKey'] = [a['id'] for a in new['answers'] if a['correct']]
    new['explanation'] = reason
    new['legalBasis'] = []
    keys = refs.split()
    for k in keys:
        assert k in evidence,(id,k)
        p = evidence[k]
        PROOFS[k] = p
        if p['reference'] not in new['legalBasis']: new['legalBasis'].append(p['reference'])
    new.update(difficulty='advanced',empiricallyCalibrated=False,questionForm='scenario',
               lastVerified='2026-10-13',reviewStatus='MULTIRULE_REVIEWED_ESTIMATED_PENDING_TRIAL')
    new['integrationSteps'] = [{'order':i+1,'application':s} for i,s in enumerate(steps)]
    new['difficultyRationale'] = 'Kết hợp: '+'; '.join(steps)+'.'
    new['source'] = {'type':'legal-review','id':'REMAIN60-20261013'}
    new['audit'] = {**new.get('audit',{}),'evidenceFile':'reports/remaining-60-legal-review-2026-10-13.json','difficultyReview':'multi_rule_estimated_pending_trial'}
    source = {k:old[k] for k in ('question','answers','legalBasis')}
    sha = hashlib.sha256(json.dumps(source,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    ROWS.append({'id':id,'sourceSha256':sha,'after':new})
    DEC.append({'id':id,'before':old,'after':new,'answerKey':new['answerKey'],'evidenceKeys':keys,'integrationSteps':new['integrationSteps']})

rev('AUTH26-002','A đã ủy quyền B bán xe trước khi Tòa tuyên B mất năng lực. Quyết định đang có hiệu lực; giám hộ G của B đến văn phòng, muốn dùng giấy cũ để ký bán thay B cho A. Không có quyền mới từ A. Cần xử lý tư cách ký thế nào?',
'Quyền cũ của B đã chấm dứt; giám hộ B không tự thành đại diện bán xe cho A.',[
('G được ký nếu xuất trình quyết định giám hộ B và giấy ủy quyền A–B còn ghi thời hạn.','Giám hộ đại diện B, không kế thừa quyền B đại diện A.'),
('B có thể điểm chỉ trước G để duy trì quyền, vì xe bán thuộc A chứ không thuộc B.','Mất năng lực ảnh hưởng tư cách thực hiện đại diện, không chỉ tài sản B.'),
('Chỉ cần G đồng ý giá bán bằng văn bản thì B vẫn ký, vì quyền chưa hết hạn trên giấy.','Hạn trên giấy không loại căn cứ chấm dứt do không còn điều kiện đại diện.')],
'DS22,134 xác định B không đủ điều kiện tự thực hiện đại diện; DS140 đặt căn cứ chấm dứt này độc lập với hạn ghi trên giấy. G đại diện B không mặc nhiên đại diện A. CC42 yêu cầu kiểm tra quyền thực tế, cần quyền hợp lệ mới chứ không chứng nhận dựa giấy cũ.','DS:22 DS:134 DS:140 CC:42',['Đọc quyết định mất năng lực','Xét chấm dứt quyền trước hạn','Phân biệt giám hộ B với đại diện A'])

rev('AUTH26-004','A thuê B đại diện nhận tiền bán xe. B chấm dứt ủy quyền có thù lao, gây thiệt hại đã xác định 12 triệu, không được miễn; B còn giữ 40 triệu thu đúng quyền trước đó. B đề nghị giữ tiền để tự trừ chi phí nhưng chưa có căn cứ đối trừ hoặc thỏa thuận cho hưởng. Phương án đúng?',
'B phải giao lại 40 triệu cho A và bồi thường 12 triệu; chấm dứt không chuyển tiền thành thù lao.',[
('B bồi thường 12 triệu rồi được giữ 40 triệu vì đã trực tiếp thu trong quá trình làm việc.','Tiền thu cho A không thành sở hữu B chỉ vì B trực tiếp nhận.'),
('B giao lại 40 triệu là đủ; khoản thiệt hại được coi đã bao gồm trong việc hoàn tiền của A.','Hoàn tài sản và bồi thường là hai nghĩa vụ khác nhau.'),
('B giữ 12 triệu trong khoản thu, giao 28 triệu và coi khoản giữ là bồi thường cho A.','Giữ thêm tiền A không phải trả bồi thường A; cũng thiếu căn cứ tự đối trừ.')],
'DS569 cho B chấm dứt hợp đồng có thù lao nhưng phải bồi thường thiệt hại nếu có. DS565 buộc giao tài sản, lợi ích nhận trong đại diện theo thỏa thuận hoặc luật. 40 triệu tiền A và 12 triệu thiệt hại có căn cứ khác nhau; không tự đổi thành thù lao hoặc bù trừ.','DS:569 DS:565 DS:568',['Xác định quyền chấm dứt của B','Tách tiền nhận thay và thù lao','Xử lý nghĩa vụ bồi thường độc lập'])

rev('AUTH26-005','A báo B chấm dứt ủy quyền bán máy, chưa báo C bằng văn bản. Trước lúc ký, C đã đọc tin nhắn A gửi B và xác nhận biết quyền đã chấm dứt; A không đồng ý giao dịch mới, không có căn cứ ràng buộc khác. C vẫn ký với B và xin công chứng, viện thiếu thông báo riêng. Xử lý đúng?',
'C đã biết chấm dứt nên không được bảo vệ bằng việc A chưa gửi văn bản riêng; phải kiểm tra quyền mới.',[
('Chưa có thư riêng cho C thì B vẫn ràng buộc A; công chứng viên chỉ kiểm tra giá và giấy máy.','DS569 có ngoại lệ người thứ ba biết hoặc phải biết, không chỉ hình thức thư riêng.'),
('C biết chấm dứt nhưng giấy B còn hạn nên chỉ cần bổ sung tin nhắn vào hồ sơ để tiếp tục ký.','Hạn ghi trên giấy không duy trì quyền sau một căn cứ chấm dứt khác.'),
('C xác nhận đã đọc tin khiến giao dịch tự chuyển thành hợp đồng giữa A và C, khỏi xét B.','Biết quyền chấm dứt không tạo sự chấp thuận hoặc chữ ký đại diện mới của A.')],
'DS569 bảo vệ người thứ ba khi chưa được thông báo, trừ trường hợp biết hoặc phải biết; C đã biết. DS140 chốt quyền B đã chấm dứt; CC42 không thể lấy giấy còn hạn thay việc kiểm tra quyền hiện tại. Dữ kiện loại các căn cứ ràng buộc A khác, cần đại diện hợp lệ mới.','DS:569 DS:140 CC:42',['Xét thông tin thực tế C đã biết','Tách hạn trên giấy khỏi chấm dứt','Kiểm tra quyền ký tại giao dịch mới'])

rev('AUTH26-007','A ủy quyền B cho thuê căn hộ riêng, tự gia hạn một lần 12 tháng nếu A ở nước ngoài và công việc chưa xong. Cả hai điều kiện xảy ra, chưa có chấm dứt khác. B muốn ký bán căn hộ trong kỳ gia hạn; không quyền bán mới. Gia hạn tác động thế nào?',
'Kỳ gia hạn được xét theo thỏa thuận; quyền vẫn chỉ cho thuê, B chưa được ký bán.',[
('Gia hạn giữ quyền B thêm 12 tháng và chuyển sang mọi giao dịch cần thiết để kết thúc công việc.','Thời hạn và phạm vi là hai giới hạn khác nhau.'),
('Gia hạn có điều kiện không được dùng nên B phải dừng cả cho thuê lẫn bán dù điều kiện xảy ra.','Không có căn cứ loại thỏa thuận thời hạn đã xác định hợp lệ.'),
('A còn ở nước ngoài nên B được bán trong 12 tháng, nhưng chỉ nếu giá bán cao hơn tiền thuê.','Lợi ích kinh tế dự kiến không tự mở rộng quyền từ thuê sang bán.')],
'DS563,140 cho xác định thời hạn từ toàn bộ thỏa thuận, kể cả gia hạn có điều kiện. DS141 giữ phạm vi cho thuê; CC42 phải kiểm tra cả thời hạn và loại giao dịch. Đủ kỳ gia hạn không tạo quyền bán căn hộ.','DS:563 DS:140 DS:141 CC:42',['Đối chiếu điều kiện gia hạn','Giữ giới hạn loại giao dịch','Đánh giá quyền ký bán tại thời điểm mới'])

rev('AUTH26-008','W đồng ý bằng văn bản cho H đại diện thế chấp nhà chung tại ngân hàng X, đúng các điều kiện khác. H được phép ủy quyền lại nhưng giao C giấy viết tay để bán nhà cho Y; giấy quyền H đã công chứng, không có thỏa thuận bán của W. C xin chứng nhận bán. Thiếu gì?',
'Ủy quyền lại sai phạm vi và hình thức; đồng ý thế chấp của W cũng không thay đồng ý bán.',[
('Chỉ công chứng giấy H–C là đủ vì W đã cho dùng nhà vào giao dịch có bảo đảm tại X.','Chữa hình thức không mở quyền bán hoặc thay ý chí W.'),
('W ký bổ sung đồng ý bán là đủ; C dùng giấy viết tay vì H đã có quyền ủy quyền lại.','Còn phải xử lý phạm vi và hình thức quyền hợp lệ đến C.'),
('Đổi tên ngân hàng X thành người mua Y trong giấy gốc là sửa kỹ thuật, rồi C được ký.','Đổi loại giao dịch và chủ thể nhận quyền không là lỗi kỹ thuật.')],
'DS564 yêu cầu quyền lại không vượt quyền gốc và hình thức phù hợp; DS141 không cho C bán từ quyền thế chấp. HN35 đòi thỏa thuận định đoạt nhà chung cho giao dịch đang xét. CC52 không dùng sửa kỹ thuật để đổi quyền, CC42 phải kiểm tra đủ cả ba tầng.','DS:564 DS:141 HN:35 CC:42 CC:52',['So quyền gốc với quyền lại','Kiểm tra hình thức quyền lại','Đối chiếu ý chí W cho giao dịch bán'])

rev('AUTH26-011','H đã bán nhà cho vợ chồng A–W; giao dịch xong, A–W chỉ nhờ H nộp hồ sơ đăng ký. Khi phát hiện tên đường đánh máy sai không ảnh hưởng quyền nghĩa vụ, H muốn tự ký thỏa thuận giảm giá mua cũ để bù công đi nộp; không có quyền sửa giá. Phân biệt đúng?',
'Nộp hồ sơ không bị cấm chỉ vì H là người bán cũ; H chưa được nhân danh A–W sửa giá với chính mình.',[
('H được sửa giá nếu công nộp hồ sơ hợp lý, vì đó là quyền phụ đi cùng công việc đăng ký.','Không suy quyền sửa giá từ quyền nộp và không bỏ xung đột với chính H.'),
('H bị cấm cả việc nộp hồ sơ nên mọi lỗi đường phải chờ A–W tự sửa bằng hợp đồng mới.','Không phải mọi công việc sau bán đều là giao dịch với chính mình; lỗi kỹ thuật có cơ chế riêng.'),
('Lỗi đường và giảm giá đều có thể sửa kỹ thuật, H ký đại diện vì hồ sơ vẫn là căn nhà cũ.','Giảm giá thay nghĩa vụ nên khác lỗi đánh máy; vẫn thiếu quyền và có xung đột.')],
'DS141 không cấm nộp hồ sơ chỉ vì H từng là bên bán, nhưng việc H nhân danh người mua sửa giá với chính H là giao dịch khác, ngoài phạm vi và có xung đột không được loại trừ. CC52,53 tách lỗi kỹ thuật không đổi quyền với sửa giá cần ý chí và thủ tục đúng.','DS:141 CC:52 CC:53',['Phân loại công việc nộp hồ sơ','Tách sửa kỹ thuật và sửa giá','Kiểm tra phạm vi cùng giao dịch với chính H'])

rev('AUTH26-013','B nhận đúng quyền 100 triệu tiền thuê nhà chung của A–W và giấy nhà. A chỉ giao B nhận, bảo quản; W không đồng ý bán. B muốn giữ tiền làm thù lao và dùng giấy để ký bán nhà cho C, không có quyền mới hay thỏa thuận tiền công. Cách xử lý đúng?',
'B phải giao tiền, bảo quản giấy; việc đang giữ giấy không tạo quyền bán hoặc quyền hưởng tiền.',[
('B giao lại giấy nhưng giữ tiền vì đã đi nhận; C có thể mua nếu A đồng ý riêng với B.','Thiếu căn cứ tiền công và còn quyền định đoạt nhà chung của W.'),
('B giao đủ tiền thì được giữ giấy để ký bán, vì hoàn tiền đã kết thúc trách nhiệm đại diện.','Hoàn tiền không mở rộng quyền từ nhận tiền sang bán.'),
('B dùng 100 triệu trả trước cho W thì được coi W đã đồng ý bán và B được hưởng phần chênh.','Chuyển tiền thu hộ không thay thỏa thuận định đoạt, không tạo quyền bán hay hưởng chênh.')],
'DS565,568 phân biệt tài sản thu hộ với thù lao có căn cứ. DS141 giới hạn quyền nhận, bảo quản; giữ giấy không tạo đại diện bán. HN35 vẫn yêu cầu ý chí định đoạt nhà chung. Cần xử lý giao lại tài sản và quyền ký riêng biệt.','DS:565 DS:568 DS:141 HN:35',['Xác định tiền thu hộ và căn cứ thù lao','Giữ phạm vi đại diện','Kiểm tra ý chí định đoạt nhà chung'])

rev('AUTH26-018','A cho B quyền mua máy tối đa 200 triệu. B–C biết hạn này, thông đồng ký giá 260 triệu để gây thiệt hại A; thiệt hại 30 triệu đã xác định. A phản đối ngay, không có căn cứ ràng buộc phần vượt. B đề nghị thêm phụ lục công chứng để buộc A nhận cả giá. Nhận định đúng?',
'Phần vượt chưa ràng buộc A; B,C liên đới bồi thường 30 triệu, công chứng phụ lục không tạo ý chí A.',[
('B,C trả 30 triệu thì toàn bộ giá 260 triệu tự ràng buộc A vì hậu quả vượt quyền đã được khắc phục.','Bồi thường không là sự đồng ý hoặc căn cứ ràng buộc A phần vượt.'),
('C chỉ trả 30 triệu, B được miễn vì có giấy quyền gốc; phụ lục đủ chữ ký B,C thay được A.','Người đại diện thông đồng cũng chịu liên đới; chữ ký B,C không mở quyền.'),
('A trả giá 260 triệu rồi tự đòi B; phụ lục công chứng sẽ xác nhận hồi tố mọi quyền B đã có.','Không mặc nhiên ràng buộc A phần vượt; công chứng không hồi tố cấp quyền.')],
'DS143 tách phần vượt quyền không ràng buộc với trách nhiệm liên đới do thông đồng; DS141 giữ mức 200 triệu. Thiệt hại 30 triệu không phải phần giá vượt 60 triệu. CC42 không cho chứng nhận phụ lục thiếu quyền để biến thành chấp thuận của A.','DS:143 DS:141 CC:42',['Tính phần vượt 60 triệu','Tách thiệt hại thực tế 30 triệu','Giữ điều kiện ý chí A khi sửa giao dịch'])

rev('DEP26-004','M thuê xe, ký cược 20 triệu, đã trả xe nguyên trạng nhưng còn 3 triệu tiền thuê đến hạn. Không có mất cọc, bồi thường hoặc căn cứ bù trừ; M đòi cả 20 triệu và đề nghị gọi chậm tiền thuê là từ chối giao kết. Cách xử lý đúng?',
'Xe đã trả; M trả tiền thuê rồi nhận lại ký cược, không áp mất cọc do từ chối giao kết.',[
('Chủ xe giữ cả 20 triệu như phạt cọc vì 3 triệu thuê chưa thanh toán đúng hạn khi giao lại xe.','Ký cược và đặt cọc có điều kiện xử lý khác; chậm tiền thuê không thành từ chối giao kết.'),
('M nhận ngay 20 triệu, chủ xe đòi 3 triệu riêng vì việc trả xe đã đáp ứng đầy đủ mọi điều kiện.','DS329 còn yêu cầu trả tiền thuê trước khi nhận lại ký cược.'),
('Chủ xe được giữ 17 triệu làm khoản bảo đảm mới và trả 3 triệu để kết thúc việc ký cược.','Không có thỏa thuận cho đổi ký cược sang bảo đảm mới hoặc tính đảo nghĩa vụ như vậy.')],
'DS329 đặt điều kiện nhận lại ký cược khi đã trả tài sản thuê và trả tiền thuê. DS328 không áp mất cọc vì một hợp đồng đã giao kết, thực hiện rồi chậm tiền thuê. Dữ kiện không cho tự bù trừ, cần thanh toán nghĩa vụ thuê và hoàn ký cược đúng cơ chế.','DS:329 DS:328 DS:117',['Phân biệt ký cược với đặt cọc','Kiểm tra trả xe và tiền thuê','Không tự tạo chế tài hoặc bảo đảm mới'])

rev('DEP26-010','A đề nghị dùng quyền sử dụng đất riêng làm tài sản đặt cọc, chỉ giao giấy chứng nhận cho B. A đồng thời đề nghị phương án khác: giao 100 triệu tiền riêng bảo đảm giao kết mua máy. Chưa chuyển quyền hoặc xác lập thế chấp đất. Phân biệt hai phương án?',
'Không coi quyền đất hoặc việc giữ giấy là cọc đã giao; 100 triệu có thể làm cọc khi thỏa thuận hợp lệ.',[
('Cả hai đều là cọc đã giao vì giấy chứng nhận đại diện cho đất và tiền đều có thể định giá.','Tài sản theo BLDS rộng hơn nhóm tài sản đặt cọc; giấy không thay giao quyền đất làm cọc.'),
('Giữ giấy tạo thế chấp đất nên phương án đất hợp lệ, còn cọc tiền phải công chứng mới có giá trị.','Không tự phát sinh thế chấp từ giữ giấy và không mặc nhiên bắt công chứng mọi cọc tiền.'),
('Tiền chỉ là trả trước, quyền đất mới là cọc vì giấy gốc có giá trị lớn hơn 100 triệu.','Bản chất bảo đảm dựa thỏa thuận và đối tượng, không chỉ giá trị hoặc loại giấy gốc.')],
'DS105,115 công nhận quyền tài sản nhưng DS328 quy định đối tượng và việc giao cọc cụ thể. Giữ giấy chứng nhận không tự giao quyền sử dụng đất làm cọc hoặc tạo thế chấp. Tiền giao theo thỏa thuận bảo đảm giao kết có thể là cọc; không suy mọi tiền giao đều chỉ trả trước.','DS:105 DS:115 DS:328',['Phân biệt quyền đất với giấy chứng nhận','Đọc đối tượng và việc giao cọc','Phân loại tiền theo mục đích bảo đảm'])

rev('DEP26-013','A giao B 200 triệu tiền riêng làm cọc để ký mua căn nhà riêng B đang thế chấp X. B cam kết chỉ bán khi X đồng ý hoặc giải chấp; chưa có việc nào. A muốn dùng giấy cọc công chứng để ký mua ngay và cho rằng nhà là tài sản cọc đang bảo đảm thêm nợ. Phân biệt đúng?',
'Cọc là 200 triệu, nhà là đối tượng mua dự kiến; công chứng cọc không thay điều kiện bán nhà thế chấp.',[
('Nhà là tài sản cọc thứ hai nên chỉ cần áp bảo đảm nhiều nghĩa vụ; tiền 200 triệu là phí giải chấp.','Sai đối tượng cọc và không có dữ kiện chuyển tiền thành phí.'),
('Cọc tiền riêng hợp lệ thì B được bán ngay, vì giấy cọc đã công chứng ghi rõ người mua A.','Công chứng cọc không thay giải chấp hoặc đồng ý của bên nhận thế chấp.'),
('B phải hoàn cọc gấp đôi ngay khi X chưa đồng ý, dù thời hạn cam kết bán chưa đến và B chưa từ chối.','Chưa đủ dữ kiện kích hoạt chế tài từ chối giao kết; cần xét thời hạn và vi phạm thực tế.')],
'DS328 phân biệt tài sản cọc được giao với tài sản dự kiến mua. DS321 hạn chế bán tài sản thế chấp theo điều kiện luật. CC42 kiểm tra giao dịch chính, không suy công chứng cọc đã cấp quyền bán; thiếu đồng ý hiện tại cũng chưa tự chứng minh B từ chối trước hạn.','DS:328 DS:321 CC:42',['Xác định tiền cọc và nhà mua','Kiểm tra điều kiện bán tài sản thế chấp','Tách hiệu lực cọc và căn cứ xử lý vi phạm'])

rev('DEP26-017','A giao B 100 triệu cọc mua nhà X; giấy cọc được công chứng tại V còn hoạt động. Hai bên đổi sang nhà Y, cùng giá, đồng ý giữ tiền và mục đích bảo đảm. Họ đề nghị CCV sửa tên nhà bằng thủ tục lỗi đánh máy để khỏi lập sửa đổi. Cách xử lý đúng?',
'Có thể thỏa thuận đổi đối tượng nếu hợp lệ; phải sửa nội dung tại V đúng thủ tục, không sửa kỹ thuật.',[
('Giá và tiền cọc không đổi nên tên nhà được sửa kỹ thuật tại V, không cần ý chí bằng văn bản hai bên.','Đổi đối tượng làm thay quyền nghĩa vụ dù giá bằng nhau.'),
('Hai bên đã đồng ý thì sửa ở bất kỳ nơi nào bằng bản photo, vì cọc tiền không gắn với nhà cụ thể.','Cọc đang gắn đối tượng và văn bản công chứng có quy tắc sửa tại nơi cũ khi không ngoại lệ.'),
('Phải hoàn cọc và phạt B trước khi cọc nhà Y, vì đổi đối tượng tự là B từ chối nhà X.','Đổi theo đồng thuận không tự là vi phạm từ chối giao kết; không mặc nhiên phát sinh phạt cọc.')],
'DS3,421 cho sửa đổi theo thỏa thuận đáp ứng điều kiện và hình thức áp dụng. DS328 không tự phát sinh phạt khi hai bên cùng đổi đối tượng. CC52 không dùng cho thay quyền; CC53 điều chỉnh sửa nội dung tại nơi cũ còn hoạt động, dữ kiện không ngoại lệ.','DS:3 DS:421 DS:328 CC:52 CC:53',['Xác định ý chí cùng sửa đối tượng','Phân biệt sửa nội dung và lỗi kỹ thuật','Giữ thủ tục văn bản công chứng và mục đích cọc'])

rev('DEP26-018','Cọc 50 triệu chỉ bảo đảm ký hợp đồng thuê đã được ký; hai bên có văn bản hoàn cọc, không chuyển sang bảo đảm thực hiện. Người thuê chậm một kỳ 8 triệu; không có căn cứ bù trừ hoặc phạt khác. Chủ nhà gọi 50 triệu là ký cược để giữ vì chưa trả tiền thuê. Đánh giá đúng?',
'Phải xét hoàn cọc và đòi 8 triệu thuê riêng; không tự đổi cọc giao kết thành ký cược hoặc phạt cọc.',[
('Có tiền thuê chưa trả thì 50 triệu tự thành ký cược, chủ nhà giữ đến khi người thuê trả nhà.','Ký cược có đối tượng thuê là động sản; tiền cọc thuê nhà không tự chuyển chế định.'),
('Chủ nhà giữ 50 triệu theo mất cọc vì người thuê đã từ chối thực hiện một kỳ tiền thuê.','Cọc chỉ bảo đảm giao kết đã hoàn thành, không bảo đảm thực hiện theo dữ kiện.'),
('Người thuê được miễn 8 triệu vì khoản cọc phải hoàn chứng minh chủ nhà không còn quyền nào từ hợp đồng.','Hoàn cọc không xóa nghĩa vụ trả tiền thuê từ hợp đồng chính.')],
'DS328 đọc mục đích cọc giao kết và thỏa thuận hoàn, không tự áp chế tài cho nghĩa vụ ngoài phạm vi. DS329 không biến thuê nhà thành ký cược động sản. DS421 yêu cầu thỏa thuận hợp lệ nếu đổi cơ chế; nghĩa vụ thuê vẫn phải thực hiện, không tự bù trừ khi dữ kiện loại điều đó.','DS:328 DS:329 DS:421',['Chốt phạm vi cọc đã hoàn thành','Loại suy chuyển sang ký cược','Giữ nghĩa vụ thuê độc lập với hoàn cọc'])

rev('FAM26-001','Cha mẹ từng công chứng thỏa thuận nhà ở X. Mẹ đã chết; con C là người có quyền liên quan và các người thừa kế mẹ đã đồng ý cấp bản sao. Cha còn sống, chưa đồng ý. C đến Y chỉ có bản photo, yêu cầu cấp vì đã được mọi người thừa kế mẹ cho phép. Điều còn phải xét?',
'Cần đồng ý của cha còn sống; nơi cấp là nơi lưu bản gốc, Y giữ photo chưa có thẩm quyền cấp.',[
('Đồng ý của các người thừa kế mẹ thay cả đồng ý cha; Y cấp từ photo khi C cam đoan bản đó đúng.','Cơ chế người thừa kế thay người đã chết, không thay người còn sống; photo không là hồ sơ gốc.'),
('Cha đồng ý thì Y cấp từ photo vì C đã chứng minh quyền liên quan đến nhà của cha mẹ.','Đủ tư cách và đồng ý không thay điều kiện nơi lưu bản gốc.'),
('X cấp ngay vì đang giữ gốc, còn ý kiến cha chỉ cần khi C muốn đăng ký quyền sở hữu nhà.','Cấp bản sao cho người liên quan cũng phải đáp ứng đồng ý theo luật.')],
'CC69 tách tư cách liên quan, đồng ý của người yêu cầu công chứng và nơi lưu bản gốc. Sự đồng ý của người thừa kế chỉ thay cơ chế đối với mẹ đã chết; cha còn sống vẫn phải được xét riêng. DS611 xác định sự kiện mở thừa kế không chuyển quyền đồng ý của cha sang nhóm thừa kế mẹ.','CC:69 DS:611 DS:613',['Tách người yêu cầu đã chết và còn sống','Kiểm tra đủ đồng ý cho người liên quan','Xác định nơi lưu bản gốc có quyền cấp'])

rev('FAM26-004','Bản án có hiệu lực đã chia nhà riêng cho H trong hôn nhân. H–W thỏa thuận chấm dứt việc chia, chỉ công chứng, chưa được Tòa công nhận. H chết sau đó không di chúc; nhà là tài sản cần kiểm kê. Chỉ xét tác động của văn bản mới, hướng xử lý đúng?',
'Chưa có công nhận của Tòa nên không coi nhà đã trở lại chung chỉ do công chứng; kiểm kê theo quyền hợp lệ.',[
('Nhà trở lại chung ngay khi công chứng vì cả H–W đồng ý; W tự giữ nửa trước khi kiểm kê di sản.','Bỏ điều kiện Tòa công nhận khi việc chia gốc bằng bản án.'),
('H chết khiến thỏa thuận tự được công nhận hồi tố, nên chỉ phần nửa nhà của H là di sản.','Sự kiện chết không thay điều kiện công nhận thỏa thuận chấm dứt việc chia.'),
('Nhà riêng H làm W mất cả quyền yêu cầu hưởng di sản, dù W vẫn là vợ hợp pháp lúc H chết.','Tài sản riêng vào di sản không tự loại tư cách người thừa kế của vợ.')],
'HN41 khoản 4 yêu cầu Tòa công nhận thỏa thuận chấm dứt việc chia do bản án. CC42 không cho công chứng thay điều kiện này. DS611,612,651 tách xác định tài sản di sản với tư cách người hưởng; không coi tài sản riêng làm vợ mất quyền thừa kế.','HN:41 CC:42 DS:611 DS:612 DS:651',['Nhận diện nguồn chia bằng bản án','Kiểm tra điều kiện chấm dứt việc chia','Tách tài sản di sản và tư cách W'])

rev('FAM26-006','H–W có 600 triệu chung, văn bản chia cho H toàn bộ ghi hiệu lực 15/10, hình thức hợp lệ, không điều kiện đặc biệt. H chết 10/10, không di chúc; chỉ W và hai con là hàng thừa kế thứ nhất, không nợ, công sức hoặc thỏa thuận khác. Phân bổ đúng?',
'Di sản H là 300 triệu; W tổng 400 triệu, mỗi con 100 triệu, không lấy ngày lập thay mốc hiệu lực.',[
('Di sản là 600 triệu vì văn bản đã lập; W và mỗi con nhận 200 triệu như ba suất bằng nhau.','Việc chia chưa có hiệu lực tại mở thừa kế; bỏ phần chung sẵn có của W.'),
('W giữ 300 triệu, hai con mỗi người 150 triệu vì W đã có phần chung nên không hưởng di sản.','Vợ có phần chung vẫn thuộc hàng thừa kế thứ nhất.'),
('W giữ cả 600 triệu vì H chết trước mốc chia làm văn bản mất hiệu lực và không còn di sản.','Chưa chia theo văn bản không loại phần quyền H trong tài sản chung khi chết.')],
'HN39 ưu tiên mốc 15/10 đã ghi, không ngày lập; lúc mở thừa kế 10/10 tài sản còn chung. HN66 tách 300 triệu W khỏi di sản H 300 triệu. DS611,651 chia di sản cho ba người, mỗi suất 100 triệu; W có 300+100=400 triệu.','HN:39 HN:66 DS:611 DS:651',['Chốt hiệu lực tại ngày H chết','Tách phần chung của W','Tính ba suất di sản H'])

rev('FAM26-011','Sau chia tài sản hợp lệ, H thu 240 triệu từ khai thác tài sản riêng; không phân định được thu nhập lao động, kinh doanh với hoa lợi, lợi tức. Khoản tiền là nguồn thu chủ yếu đang có của gia đình; H muốn đem toàn bộ bảo đảm khoản vay riêng, W chưa đồng ý bằng văn bản. Hướng kiểm tra đúng?',
'Xét 240 triệu là chung theo quy tắc không phân định; còn phải kiểm tra thỏa thuận định đoạt nguồn thu chủ yếu.',[
('Tiền thuộc riêng vì tài sản nguồn là riêng; H ký bảo đảm không cần xét ý chí W khi giấy vay chỉ tên H.','Bỏ quy tắc chuyên biệt khi không phân định được bản chất khoản thu.'),
('Tiền là chung nhưng H trực tiếp tạo ra nên đủ quyền định đoạt, W chỉ được chia khi ly hôn.','Tài sản chung tạo thu nhập chủ yếu vẫn chịu yêu cầu thỏa thuận bằng văn bản.'),
('W ký văn bản thì mọi khoản thu sau chia tự trở lại chung, bất kể có xác định rõ là hoa lợi riêng hay không.','Ý chí giao dịch cụ thể không thay quy tắc phân loại mọi khoản thu về sau.')],
'ND126 Điều 14 khoản 3 xác định khoản không phân định được thuộc chung; việc chia không chấm dứt chế độ luật định. HN35 kiểm tra bằng văn bản khi định đoạt tài sản chung tạo thu nhập chủ yếu. CC42 nếu được yêu cầu phải xét loại tài sản và quyền ký, không chỉ tên trên hợp đồng vay.','ND126:14 HN:35 CC:42',['Áp quy tắc khoản thu không phân định','Xác định điều kiện định đoạt tài sản chung','Kiểm tra quyền cho giao dịch vay riêng'])

rev('FAM26-014','H–W muốn nhà tiếp tục chung nhưng cho H tự giao dịch kinh doanh liên quan nhà. Văn bản dự thảo ghi chia toàn bộ nhà cho H thành riêng; giấy quyền K do H cấp còn cho K bán nhà như tài sản riêng H. W chưa ký dự thảo. Cần sửa hướng nào?',
'Chọn thỏa thuận đưa tài sản chung vào kinh doanh đúng mục tiêu; quyền K phải dựa quyền H thực tế được trao.',[
('Giữ bản chia riêng rồi ghi chú nhà vẫn chung; quyền K bán toàn nhà không cần đối chiếu văn bản W.','Nội dung sở hữu mâu thuẫn mục tiêu; quyền K không tự vượt quyền gốc H.'),
('W đồng ý cho H kinh doanh miệng đủ để K bán; không cần sửa bản chia vì chưa dùng để đăng ký.','HN36 yêu cầu văn bản, việc chưa đăng ký không giải quyết nội dung và phạm vi quyền.'),
('H cấp giấy quyền K thì đã thay được thỏa thuận vợ chồng, vì K đại diện cả lợi ích gia đình.','H không tự cấp quyền của W chỉ bằng ý định vì lợi ích chung.')],
'HN36 tách trao quyền giao dịch kinh doanh liên quan tài sản chung với chia riêng theo HN38,40. Phải có văn bản phù hợp mục tiêu; DS141 xác định K theo quyền H đã được trao, không theo lời tự nhận tài sản riêng. CC42 kiểm tra nội dung và quyền, không chứng nhận một dự thảo trái ý chí thực tế.','HN:36 HN:38 HN:40 DS:141 CC:42',['Chọn đúng hậu quả sở hữu mong muốn','Hoàn thiện thỏa thuận kinh doanh bằng văn bản','Đối chiếu quyền đại diện K với quyền gốc H'])

rev('FAM26-016','H–W cưới năm 2024, không thỏa thuận tài sản trước hôn nhân. Nay muốn lập lần đầu chế độ theo thỏa thuận, ghi hồi tố từ cưới và dùng để coi đất mua bằng lương năm 2025 là riêng H; hợp đồng thế chấp chung cũ còn hiệu lực, ngân hàng không đồng ý thay quyền. Tư vấn đúng?',
'Không dùng quyền sửa đổi để lập hồi tố chế độ chưa có; giao dịch tài sản hiện tại vẫn phải xét quyền ngân hàng.',[
('Công chứng thỏa thuận lần đầu đủ hồi tố từ cưới; ngân hàng phải theo phân loại riêng mới của H–W.','HN47,49 không cho biến thỏa thuận chưa có thành chế độ trước hôn nhân và xóa quyền người thứ ba.'),
('Chỉ ghi ngày trước cưới trên văn bản sẽ đủ; giữ số công chứng hiện tại để bảo đảm hồ sơ thống nhất.','Không được ghi sai thời điểm để đáp ứng điều kiện xác lập trước hôn nhân.'),
('Không lập chế độ hồi tố được nên H–W cũng không được chia hoặc nhập bất kỳ tài sản hiện có nào.','Vẫn có cơ chế giao dịch tài sản hợp lệ; không đồng nhất với xác lập chế độ lần đầu hồi tố.')],
'HN47 yêu cầu xác lập trước kết hôn; HN49 sửa thỏa thuận đã có, không tạo hồi tố lần đầu. HN38,40 còn có cơ chế chia hiện tại nhưng phải xét quyền, nghĩa vụ đã xác lập với ngân hàng. CC42 không chứng nhận sai ngày hoặc dùng nhãn chế độ tài sản để xóa quyền người thứ ba.','HN:47 HN:49 HN:38 HN:40 CC:42',['Xét tồn tại thỏa thuận gốc','Tách xác lập chế độ và giao dịch tài sản hiện tại','Bảo toàn quyền đã xác lập với ngân hàng'])

rev('FAM26-019','H–W có chế độ theo thỏa thuận; phần giới hạn quyền ký của H liên quan trực tiếp hợp đồng sắp công chứng với C. H–W chỉ cho CCV xem, không cho C biết; lại muốn đăng toàn bộ hồ sơ gia đình để chứng minh minh bạch. Cách xử lý phù hợp?',
'Cung cấp cho C thông tin liên quan giao dịch; không suy nghĩa vụ đó thành công khai toàn bộ hồ sơ.',[
('CCV đã xem thì C được coi đã biết mọi giới hạn; đăng toàn bộ là bước thay thế cung cấp riêng cho C.','Cần thực hiện nghĩa vụ với người thứ ba, không suy biết từ việc CCV xem.'),
('Giữ bí mật toàn bộ với C nhưng H được ký theo giới hạn nội bộ; quyền lợi C xử lý sau nếu tranh chấp.','Vi phạm nghĩa vụ cung cấp thông tin không được hợp thức bằng giới hạn nội bộ.'),
('C biết giới hạn thì Văn phòng được tự đăng mọi tài liệu còn lại vì nghĩa vụ thông tin đã hoàn thành.','Thông tin giao dịch cho C không tạo quyền công khai hồ sơ của tổ chức công chứng.')],
'ND126 Điều 16 yêu cầu thông tin liên quan cho người thứ ba, và quy tắc ngay tình khi vi phạm. DS141 đòi đọc giới hạn quyền ký thực tế. CC9 về bảo mật không bị thay bằng việc cung cấp cho C; CC42 kiểm tra quyền, không biến nghĩa vụ thông tin thành đăng hồ sơ.','ND126:16 DS:141 CC:9 CC:42',['Xác định thông tin liên quan quyền ký','Cung cấp đúng người thứ ba C','Tách nghĩa vụ thông tin khỏi quyền công khai hồ sơ'])

rev('FAM26-023','G là giám hộ hợp lệ của W mất năng lực, muốn bán nhà riêng giá trị lớn của W cho C để trả viện phí. Giám sát S chưa đồng ý. W đang nội trú, ký được nhưng không có năng lực; C mời nhân chứng độc lập M để xin công chứng tại bệnh viện. Hướng xử lý đúng?',
'Có thể xét địa điểm nội trú; vẫn cần đúng đại diện và đồng ý S, nhân chứng không thay hai điều kiện này.',[
('M độc lập và W ký được thì chứng nhận tại bệnh viện, G chỉ ký xác nhận mục đích trả viện phí.','Ký được không là đủ năng lực; người làm chứng không thay đại diện theo pháp luật.'),
('G ký đại diện là đủ vì trả viện phí có lợi W; S chỉ đồng ý khi người mua chính là G.','Giao dịch tài sản giá trị lớn với C vẫn cần đồng ý người giám sát.'),
('S đồng ý miệng trước M thì có thể bỏ việc kiểm tra đại diện G và để W tự ký vì đang minh mẫn tạm thời.','Quyết định mất năng lực còn hiệu lực; ý kiến S không cho W tự ký thay cơ chế đại diện.')],
'DS22 yêu cầu giao dịch qua đại diện; DS59 đặt giám sát riêng với tài sản giá trị lớn dù mục đích có lợi. CC46 cho xét địa điểm nội trú, CC49 người làm chứng có chức năng khác. Cần kiểm tra đủ quyền và giám sát, không dùng hỗ trợ hình thức chữa trở ngại năng lực.','DS:22 DS:59 CC:46 CC:49',['Giữ cơ chế đại diện theo quyết định năng lực','Xét giám sát giao dịch giá trị lớn','Phân biệt địa điểm và nhân chứng với quyền ký'])

rev('FAM26-025','Dự thảo chế độ tài sản trước cưới có điều khoản được xác định vi phạm nghiêm trọng quyền cấp dưỡng, thừa kế của con chưa thành niên. Hai bên đề nghị công chứng và ghi tất cả di chúc sau này được miễn phần bắt buộc của con. CCV cần xử lý thế nào?',
'Yêu cầu sửa nội dung vi phạm; tự nguyện và công chứng không loại quyền được pháp luật bảo vệ của con.',[
('Công chứng nếu hai bên ký riêng cam kết tự chịu; phần bắt buộc chỉ phát sinh khi có di chúc công chứng.','Cam kết không chữa vi phạm nghiêm trọng; phần bắt buộc không phụ thuộc công chứng di chúc.'),
('Bỏ chữ cấp dưỡng là đủ, giữ quyền loại mọi thừa kế vì chưa có người nào chết tại lúc lập thỏa thuận.','Sự kiện chưa mở thừa kế không hợp pháp hóa nội dung đã xác định vi phạm nghiêm trọng.'),
('Chỉ cần cha mẹ ký thay con đồng ý thì điều khoản hợp lệ và ràng buộc con trong mọi lần thừa kế sau.','Không dùng chữ ký cha mẹ để tước quyền được luật bảo vệ bằng thỏa thuận trái luật.')],
'HN50 đặt căn cứ vô hiệu khi vi phạm nghiêm trọng quyền cấp dưỡng, thừa kế của con. DS644 bảo vệ con chưa thành niên trong điều kiện luật định, không do cha mẹ tự miễn bằng thỏa thuận. CC42 phải yêu cầu sửa nội dung trái luật, không lấy tự nguyện hoặc cam kết để bỏ kiểm tra.','HN:50 DS:644 CC:42',['Nhận diện nội dung vi phạm quyền con','Phân biệt thỏa thuận tài sản với phần thừa kế bắt buộc','Xử lý nội dung trước khi chứng nhận'])

rev('FAM26-026','A–B chung sống từ 2006, không đăng ký, không căn cứ hôn nhân đặc biệt. Nhà chung theo phần 4 tỷ đã xác định A góp 3 tỷ, B góp 1 tỷ, không thỏa thuận khác. A chết không di chúc; chỉ hai con chung là hàng thứ nhất, cha mẹ A đã chết, A không vợ hợp pháp, không nợ. Kết quả đúng?',
'B giữ 1 tỷ phần sở hữu, không hưởng suất vợ; hai con mỗi người hưởng 1,5 tỷ di sản A.',[
('B có phần riêng 1 tỷ và thêm suất vợ 1 tỷ; hai con mỗi người 1 tỷ vì đã có giấy khai sinh chung.','Quan hệ cha mẹ con không tạo quan hệ vợ chồng được công nhận.'),
('B và hai con mỗi người nhận một phần ba của 4 tỷ vì nhà dùng chung suốt thời gian sống cùng.','Phải tách quyền sở hữu B và di sản A; không chia toàn tài sản thành di sản.'),
('B giữ 2 tỷ như vợ, hai con mỗi người 1 tỷ vì thu nhập gia đình được chia đôi khi một người chết.','Không áp cơ chế tài sản vợ chồng để thay phần quyền đã xác định trong chung sống không đăng ký.')],
'HN9,14,16 không tự công nhận vợ chồng từ chung sống và có con, giải quyết tài sản theo thỏa thuận và dân sự. DS612 chỉ đưa phần A 3 tỷ vào di sản; DS651 cho hai con 1,5 tỷ mỗi người. B giữ 1 tỷ quyền sở hữu, không có suất vợ theo dữ kiện.','HN:9 HN:14 HN:16 DS:612 DS:651',['Xác định quan hệ hôn nhân không được công nhận','Tách phần quyền sở hữu trước thừa kế','Chia di sản A cho hai con'])

rev('INH26-006','L,H,T là ba người thừa kế duy nhất, đủ năng lực; di sản tiền 900 triệu, không nợ, không di chúc. L muốn H nhận cả phần L; T đồng ý vẫn nhận 300 triệu, các bên nhất trí mục tiêu. Dự thảo lại ghi L từ chối với điều kiện H hưởng riêng phần đó. Nên lập nội dung nào?',
'Ghi thỏa thuận phân chia để H 600 triệu, T 300 triệu; không dùng từ chối có điều kiện để chỉ định H.',[
('Ghi L từ chối là đủ để H hưởng 600 triệu, vì H đã được L nêu tên trong đơn nên T không liên quan.','Từ chối không là công cụ chuyển riêng phần cho một người được chỉ định.'),
('Ghi L từ chối rồi chia 450 triệu mỗi người H,T; cách này vẫn đạt mục tiêu L dù H nhận ít hơn.','Chia lại sau từ chối không đáp ứng ý chí đã thống nhất H nhận phần L.'),
('L phải nhận 300 triệu trước mới được để H hưởng; văn bản phân chia không được thỏa thuận khác suất.','DS656,660 cho thỏa thuận phân chia phù hợp, không bắt buộc nhận trước trong mọi trường hợp.')],
'DS620 tách không nhận di sản với việc chuyển lợi ích cho một người cụ thể. DS656,660 cho các người thừa kế thỏa thuận bằng văn bản về phân chia; CC59 kiểm tra quyền và ý chí. Với dữ kiện đủ, thể hiện H nhận 600 và T 300 theo thỏa thuận, không gán hậu quả đó cho từ chối có điều kiện.','DS:620 DS:656 DS:660 CC:59',['Nhận diện mục tiêu riêng H nhận phần L','Chọn thỏa thuận phân chia thay từ chối có điều kiện','Tính và thể hiện phần H,T đúng ý chí'])

rev('INH26-008','L được cử quản lý nhà di sản, đại diện các người thừa kế trong quan hệ người thứ ba. L xin công chứng thế chấp nhà để vay sửa mái; chỉ một trong ba người thừa kế đồng ý bằng văn bản, hai người chưa trả lời. Ngân hàng đề nghị coi im lặng là đồng ý, không có thỏa thuận hoặc thói quen ấy. Xử lý đúng?',
'Chưa đủ đồng ý bằng văn bản của người thừa kế; quyền quản lý và im lặng không cấp quyền thế chấp.',[
('Một người đồng ý đủ để L thế chấp vì sửa mái bảo quản di sản, các người còn lại hưởng lợi chung.','Lợi ích bảo quản không thay điều kiện đồng ý bằng văn bản để định đoạt.'),
('Hai người im lặng được coi đồng ý sau thời hạn ngân hàng tự ấn định; L có quyền ký từ việc được cử.','Không có căn cứ coi im lặng là chấp thuận; quyền đại diện quản lý có giới hạn.'),
('Ngân hàng ký cam kết chỉ đòi L là đủ, nhà vẫn thế chấp dù hai người thừa kế chưa đồng ý.','Cam kết nghĩa vụ của L không cấp quyền dùng nhà di sản làm bảo đảm.')],
'DS617 giới hạn định đoạt nhà di sản, phải có những người thừa kế đồng ý bằng văn bản; DS618 quyền đại diện không xóa giới hạn. DS393 không mặc nhiên coi im lặng là chấp nhận. CC42,59 phải kiểm tra quyền, không chứng nhận chỉ từ mục đích sửa mái hoặc cam kết ngân hàng.','DS:617 DS:618 DS:393 CC:42 CC:59',['Đọc quyền quản lý cùng giới hạn định đoạt','Kiểm tra ý chí từng người thừa kế','Loại suy đồng ý từ im lặng'])

rev('INH26-010','L quản lý di sản hợp lệ, chưa thỏa thuận thù lao; các người thừa kế không thống nhất được mức. L tự giữ 10% di sản và ký chuyển xe di sản cho mình thay tiền công, chưa được họ đồng ý bằng văn bản. Tư vấn đúng?',
'L có quyền yêu cầu thù lao hợp lý; chưa có quyền tự giữ 10% hoặc chuyển xe di sản cho mình.',[
('L được giữ 10% vì pháp luật cho thù lao hợp lý; công chứng chuyển xe chỉ cần giấy cử quản lý.','Quyền thù lao không ấn định tỷ lệ 10% và không tự tạo quyền định đoạt di sản.'),
('Không ghi mức trước thì L mất quyền thù lao; muốn giữ xe phải từ chối toàn bộ vai trò quản lý.','DS618 dự liệu mức hợp lý khi không đạt thỏa thuận, không phải miễn phí bắt buộc.'),
('Chỉ cần một người thừa kế ký xác nhận công sức thì L được chuyển xe cho mình, người khác thanh toán sau.','Công sức và một xác nhận không thay quyền, ý chí cần có đối với định đoạt xe di sản.')],
'DS618 cho khoản thù lao hợp lý khi không đạt thỏa thuận mức, không cho tự ấn định tỷ lệ. DS617 giữ giới hạn định đoạt; DS141 còn kiểm tra giao dịch với chính mình. CC42 không chứng nhận chuyển xe từ quyền quản lý đơn thuần, cần giải quyết mức và quyền riêng biệt.','DS:618 DS:617 DS:141 CC:42',['Xác định quyền thù lao hợp lý','Tách quyền được thanh toán và quyền tự định đoạt','Kiểm tra xung đột khi chuyển xe cho chính L'])

rev('INH26-023','Sau chia thừa kế, L mất năng lực sở hữu riêng căn hộ; mẹ B là giám hộ hợp lệ muốn đổi căn hộ lấy nhà riêng B. Hồ sơ xác định giao dịch vì lợi ích L, giám sát S đã đồng ý đúng quy định; các điều kiện khác đều đủ. B ký cả bên mình và đại diện L. Chỉ xét trở ngại giao dịch giữa giám hộ và người được giám hộ, nhận định đúng?',
'Có thể áp ngoại lệ riêng vì lợi ích L và có đồng ý S; phải kiểm tra đủ điều kiện, không cấm chỉ vì B ký hai vai.',[
('Phải từ chối do giao dịch với chính mình, dù đã đủ lợi ích và giám sát; ngoại lệ chỉ dành người không là mẹ.','DS59 có ngoại lệ khi đủ điều kiện, không loại vì quan hệ mẹ con.'),
('Có đồng ý S nên khỏi kiểm tra lợi ích L; người giám sát quyết định thay cả ý chí và quyền sở hữu.','Hai điều kiện lợi ích và đồng ý giám sát là đồng thời, không thay nhau.'),
('L từng nhận di sản thì B không cần giám sát cho lần đổi; chữ ký giám hộ tự tạo quyền định đoạt mới.','Nguồn thừa kế không loại giới hạn giám hộ; phải áp ngoại lệ đủ điều kiện như dữ kiện.')],
'DS59 có ngoại lệ giao dịch tài sản giữa giám hộ và người được giám hộ khi vì lợi ích người đó và được giám sát đồng ý. DS141 cho xét quy định pháp luật khác với cấm giao dịch với chính mình. CC42 phải kiểm tra đầy đủ các điều kiện đã nêu; không áp một lệnh cấm máy móc hoặc bỏ một điều kiện.','DS:59 DS:141 CC:42',['Xác định giao dịch giữa hai bên giám hộ','Kiểm tra đồng thời lợi ích và giám sát','Áp quy tắc riêng vào giới hạn giao dịch với chính mình'])

rev('INH26-031','P là cha A, còn sống lúc A chết; P chết hai tháng sau. Gia đình xin chia di sản A bỏ tên P vì P hiện đã chết, chỉ nộp cam đoan và chưa làm rõ người hưởng phần P. CCV chưa có đủ giấy hoặc dữ liệu xác thực quan hệ, thời điểm. Hướng xử lý đúng?',
'Làm rõ P sống tại mở thừa kế A và quyền phần P chuyển sang lần thừa kế sau; cam đoan không thay xác minh.',[
('P hiện đã chết nên loại khỏi lần A; những người còn sống lúc công chứng tự chia cả phần P.','Tư cách người hưởng căn cứ lúc mở thừa kế, không lúc công chứng.'),
('Giữ tên P nhưng cho người đang quản lý giấy nhà ký nhận toàn phần P, không cần xác định thừa kế P.','Quản lý giấy không tạo quyền nhận phần thuộc lần thừa kế sau.'),
('Chỉ cần cam đoan không bỏ sót của nhóm A; lần P riêng biệt nên quyền phần P không ảnh hưởng hồ sơ A.','Phải xác định quyền của P và người kế thừa, không bỏ qua vì hồ sơ hai lần khác nhau.')],
'DS611,613 chốt thời điểm mở và người sống lúc đó; DS651 xác định cha thuộc hàng thứ nhất theo điều kiện. P chết sau không mất ngược quyền đã phát sinh. CC59 yêu cầu chứng cứ quan hệ, sự kiện chết và kiểm tra đúng người; cần làm rõ lần thừa kế phần P, không thay bằng cam đoan.','DS:611 DS:613 DS:651 CC:59',['Chốt thứ tự chết A rồi P','Giữ phần quyền P đã phát sinh','Xác minh người kế thừa phần P cho hồ sơ hiện tại'])

rev('COMP26-DS-001','H–W đã đồng ý thế chấp nhà chung bảo đảm khoản vay hợp lệ. Hợp đồng không giới hạn phạm vi, luật không giới hạn riêng; nợ đến hạn gồm gốc 500, lãi 20, phạt hợp lệ 5 triệu. H muốn sửa ghi bảo đảm chỉ gốc, W và ngân hàng chưa đồng ý, đề nghị sửa kỹ thuật. Kết luận đúng?',
'Phạm vi hiện tại gồm 525 triệu; thu hẹp không là lỗi kỹ thuật và cần xử lý ý chí, thủ tục sửa nội dung.',[
('Phạm vi chỉ 500 triệu vì lãi và phạt là nghĩa vụ cá nhân H; CCV có thể sửa kỹ thuật để ghi rõ.','Phạm vi mặc định toàn bộ nghĩa vụ theo DS293, không tự loại lãi và phạt hợp lệ.'),
('Phạm vi 525 triệu nhưng H ký thông báo đủ giảm xuống 500, vì giá trị nhà không đổi sau sửa.','Giảm quyền bảo đảm thay quyền nghĩa vụ, không chỉ giá trị tài sản.'),
('W đồng ý giảm xuống 500 là đủ; ngân hàng phải chấp nhận vì đó là thỏa thuận quản lý tài sản chung.','Quyền bên nhận bảo đảm không bị thay đơn phương bởi thỏa thuận vợ chồng.')],
'DS293 mặc định bảo đảm toàn bộ khi không giới hạn: 500+20+5=525 triệu. HN35 kiểm tra định đoạt nhà chung; CC52 không áp cho thu hẹp quyền ngân hàng. CC53 yêu cầu ý chí các bên và thủ tục sửa nội dung, không dùng thông báo hoặc sửa kỹ thuật để giảm phạm vi.','DS:293 HN:35 CC:52 CC:53',['Tính phạm vi nghĩa vụ mặc định','Phân loại thu hẹp là đổi quyền','Kiểm tra ý chí đồng chủ và bên nhận bảo đảm'])

rev('COMP26-DS-003','Nhà riêng H đang thế chấp X; điều kiện xử lý đã phát sinh, hợp đồng hợp lệ cho X nhận chính nhà thay nghĩa vụ. Chưa có thỏa thuận định giá, các bên cũng không thỏa thuận khác. X tự chọn giá 1,8 tỷ và nói văn bản công chứng đã cho quyền nhận nên giá không phải kiểm tra. Hướng đúng?',
'Có thể nhận nhà theo phương thức đã thỏa thuận; định giá phải đúng cơ chế, công chứng không xác nhận sẵn giá tự chọn.',[
('Phải đấu giá dù đã chọn nhận nhà; nhưng nếu X muốn nhận thì mức 1,8 tỷ của X là giá bắt buộc.','DS303 cho nhận chính tài sản, nhưng không cho X tự bỏ cơ chế định giá.'),
('Phương thức nhận nhà hợp lệ nên giá X chọn được dùng ngay, H chỉ được phản đối sau sang tên.','Đủ phương thức xử lý không thay điều kiện định giá khi chưa thỏa thuận.'),
('H ký xác nhận đã nghe giá là đủ để coi có thỏa thuận giá, dù H không đồng ý giá được nêu.','Biết giá và đồng ý giá khác nhau; không suy ý chí chấp thuận từ xác nhận đã nghe.')],
'DS303 cho phương thức nhận chính tài sản theo thỏa thuận. DS306 yêu cầu định giá theo thỏa thuận hoặc tổ chức định giá khi không thỏa thuận, trừ thỏa thuận khác; DS305 điều chỉnh nhận thay nghĩa vụ. CC42 phải kiểm tra nội dung giao dịch được yêu cầu, không coi công chứng cũ đã duyệt giá X tự đặt.','DS:303 DS:305 DS:306 CC:42',['Kiểm tra phương thức và điều kiện xử lý','Xác định cơ chế định giá chưa thỏa thuận','Tách biết thông tin và đồng ý giá'])

rev('COMP26-DS-004','S đang giữ hợp pháp máy M để sửa, phí sửa chưa đến hạn. M lại nợ S tiền vay riêng đã đến hạn, không thỏa thuận dùng máy bảo đảm. S muốn cầm giữ máy rồi bán để thu nợ vay. Nhận định đúng?',
'Nợ vay riêng đến hạn không kích hoạt cầm giữ từ hợp đồng sửa chưa đến hạn; cầm giữ cũng không tự cho quyền bán.',[
('S được cầm giữ do có một khoản nợ đến hạn, nhưng chỉ cần báo M trước khi bán máy.','Phải là nghĩa vụ từ hợp đồng song vụ liên quan tài sản đang giữ; không tự có quyền bán.'),
('S được giữ máy đến hạn phí sửa và tự cộng nợ vay vào phạm vi cầm giữ khi phí sửa phát sinh.','Không tự nhập nghĩa vụ vay khác vào chế định cầm giữ hợp đồng sửa.'),
('M sở hữu máy nên S không được cầm giữ kể cả phí sửa đến hạn chưa trả; chỉ có thể kiện khoản vay.','DS346,347 có cơ chế cầm giữ khi đủ điều kiện, không cấm chỉ vì M sở hữu máy.')],
'DS346,347 gắn cầm giữ với nắm giữ hợp pháp và nghĩa vụ đến hạn từ hợp đồng song vụ có tài sản làm đối tượng. Nợ vay khác không thay khoản phí sửa chưa đến hạn. DS348 quy định quyền của bên cầm giữ, không tự tạo quyền bán như một phương thức xử lý thế chấp đã thỏa thuận.','DS:346 DS:347 DS:348',['Xác định hợp đồng làm căn cứ đang giữ máy','Đối chiếu đúng nghĩa vụ đến hạn','Tách cầm giữ và quyền tự bán'])

rev('COMP26-HN-001','Khi ly hôn, nhà chung trị giá 4 tỷ có 1 tỷ tài sản riêng W trộn vào đã xác định; W yêu cầu hoàn giá trị, không thỏa thuận khác, phần còn lại chia đôi theo dữ kiện. Giấy nhà chỉ tên H. H đề nghị công chứng toàn nhà riêng H rồi trả W 2 tỷ. Cách tính và xử lý đúng?',
'W được 1 tỷ giá trị riêng và 1,5 tỷ phần chung, tổng 2,5 tỷ; tên H không thay thỏa thuận hoặc quyết định chia.',[
('W nhận 2 tỷ vì toàn nhà đã thành chung khi trộn; H giữ 2 tỷ và ký nhận nhà như tài sản riêng.','HN59 bảo vệ phần giá trị riêng có căn cứ, không tự xóa do trộn.'),
('W nhận 1 tỷ, H 3 tỷ vì giấy chỉ tên H; phần chung sau hoàn giá trị thuộc người đứng tên.','Tên một người không làm phần chung còn lại thành riêng.'),
('W nhận 3 tỷ gồm 1 tỷ riêng cộng nửa tổng 4 tỷ; H nhận 1 tỷ, không cần ý chí H về phương thức chia.','Tính lặp giá trị riêng vào nền chia đôi và bỏ yêu cầu thỏa thuận hoặc quyết định hợp lệ.')],
'HN59 thanh toán phần giá trị riêng đã đóng góp, không thỏa thuận khác; sau hoàn 1 tỷ, 3 tỷ còn lại chia đôi theo dữ kiện. W=1+1,5=2,5 tỷ; H=1,5 tỷ. HN34 không cho tên H thay căn cứ quyền; CC42 phải kiểm tra ý chí hoặc quyết định chia trước chứng nhận quyền riêng.','HN:59 HN:34 CC:42',['Tách giá trị riêng có chứng cứ','Tính phần còn lại chia đôi không lặp','Kiểm tra căn cứ quyền thay vì tên giấy'])

rev('COMP26-HN-003','H–W ly hôn, nợ chung 300 triệu đã có thỏa thuận ba bên hợp lệ: W tiếp tục trả, ngân hàng X giải phóng H. Sau đó W cấp K quyền nhận thông báo, chưa cho quyền sửa nợ. K muốn ký phụ lục chuyển nợ lại H vì H từng là đồng nghĩa vụ. Phân biệt đúng?',
'Có thể xét việc giải phóng H theo thỏa thuận với X; K chưa có quyền ký sửa để đưa H trở lại nghĩa vụ.',[
('Ly hôn không đổi nợ nên thỏa thuận ba bên vô hiệu; K được đưa H trở lại bằng quyền nhận thông báo.','HN60 cho xét thỏa thuận giữa vợ chồng và chủ nợ; nhận thông báo không là sửa nợ.'),
('Thỏa thuận giải phóng H có hiệu lực nên K cũng kế thừa quyền sửa nợ từ quyền của W nhận giấy.','Phạm vi quyền nhận thông báo không bao gồm sửa nghĩa vụ.'),
('W tự ký lại nghĩa vụ H là đủ vì khoản nợ từng chung, không cần ý chí H hoặc bên nhận chuyển nghĩa vụ.','Không tự tái lập nghĩa vụ một người đã được giải phóng bằng ý chí W riêng.')],
'HN60 duy trì quyền nghĩa vụ với người thứ ba sau ly hôn trừ thỏa thuận hợp lệ; DS370 xét chuyển nghĩa vụ có đồng ý bên có quyền. DS141 giới hạn K; CC42 kiểm tra quyền và ý chí giao dịch mới, không suy từ lịch sử nợ chung hoặc quyền nhận giấy.','HN:60 DS:370 DS:141 CC:42',['Xét hiệu lực thỏa thuận có chủ nợ','Chốt tình trạng nghĩa vụ H sau giải phóng','Đối chiếu phạm vi K khi sửa lần mới'])

rev('COMP26-TK-002','Nhà chung H–W 6 tỷ, H chết 01/10/2023 không di chúc; chỉ W và hai con là hàng thứ nhất, không nợ. Tòa đã hạn chế chia để bảo vệ W ba năm; nay W chứng minh vẫn ảnh hưởng nghiêm trọng, chưa gia hạn lần nào. Các con muốn CCV tự gia hạn và coi W sở hữu cả nhà. Kết luận đúng?',
'W có thể yêu cầu Tòa gia hạn một lần tối đa ba năm; hạn chế chia không chuyển phần di sản thành sở hữu W.',[
('CCV được gia hạn ba năm và chuyển toàn nhà cho W vì W đang ở; các con chỉ nhận sau W chết.','Thẩm quyền gia hạn thuộc Tòa; trì hoãn chia không thay quyền sở hữu.'),
('Hết ba năm phải chia ngay, W không được yêu cầu tiếp; mỗi người được một phần ba toàn nhà 6 tỷ.','Có quyền yêu cầu gia hạn theo điều kiện; phải tách phần chung W khỏi di sản H.'),
('W tự thông báo gia hạn là đủ; vì W có 3 tỷ riêng trong khối chung nên phần H cũng tạm thuộc W.','Không có tự gia hạn và không biến quyền chưa chia thành quyền sở hữu của W.')],
'HN66 tách 3 tỷ của W, di sản H 3 tỷ; DS651 ba suất mỗi suất 1 tỷ. DS661 cho W yêu cầu Tòa gia hạn một lần không quá ba năm khi đủ điều kiện, không tự động. Việc chưa chia giữ phần hưởng đã xác định, không chuyển cả nhà cho W hoặc trao quyền gia hạn cho CCV.','HN:66 DS:651 DS:661',['Tách phần chung W khỏi di sản','Giữ quyền hưởng khi tạm chưa chia','Xét điều kiện và thẩm quyền gia hạn'])

rev('COMP26-TK-003','Nhà chung P–W 3 tỷ. P biết con B thành niên có khả năng lao động vi phạm nghiêm trọng nghĩa vụ nuôi dưỡng, vẫn lập di chúc hợp lệ cho B 200 triệu, còn lại cho C. P chết; chỉ W và B là hàng thứ nhất, W không bị truất quyền, không từ chối, không nợ. Quyền B và W đúng?',
'B hưởng 200 triệu theo ý chí biết rõ của P, không có suất bắt buộc; W có tối thiểu 500 triệu từ di sản.',[
('B bị loại cả 200 triệu vì vi phạm nuôi dưỡng; W hưởng bắt buộc 1 tỷ trên toàn nhà 3 tỷ.','DS621 có ngoại lệ người để lại biết vẫn cho hưởng; tính trên di sản 1,5 tỷ, không toàn nhà.'),
('B hưởng 500 triệu bắt buộc vì là con; W chỉ giữ 1,5 tỷ phần chung và không nhận di sản.','Con thành niên có khả năng lao động không thuộc nhóm này; W vẫn thuộc nhóm bắt buộc.'),
('B hưởng 200 triệu và thêm 500 triệu bắt buộc; W,C chia phần còn lại của 1,5 tỷ.','Không cộng suất bắt buộc cho B ngoài nhóm chỉ vì có quan hệ con.')],
'HN66 tách di sản P 1,5 tỷ; DS651 giả định hai suất 750 triệu, DS644 cho W tối thiểu 2/3=500 triệu. B thành niên có khả năng lao động không thuộc nhóm bắt buộc; DS621 cho hưởng theo di chúc khi P biết hành vi vẫn cho hưởng. Hai cơ chế không đồng nhất.','HN:66 DS:621 DS:644 DS:651',['Tách di sản và tính suất pháp luật giả định','Xét ngoại lệ người không được hưởng theo ý chí biết rõ','Xác định đúng nhóm hưởng bắt buộc'])

rev('COMP26-TK-004','Di sản A gồm một máy không chia được, chỉ B,C hưởng theo pháp luật, đủ năng lực, không hạn chế chia. Họ không thống nhất giá hoặc người nhận. B quản lý máy, muốn tự giữ và đặt giá trả C, còn thuê K chỉ nộp hồ sơ nhưng muốn K ký thay C vào văn bản chia. Cách xử lý đúng?',
'Không thống nhất thì bán hiện vật để chia; quản lý máy và quyền nộp hồ sơ không thay ý chí hoặc quyền ký C.',[
('B đang quản lý nên được tự chọn giá trả C; K ký C để hoàn tất thủ tục vì không đổi người thừa kế.','Quản lý không trao quyền tự nhận hiện vật và quyền nộp hồ sơ không là đại diện C.'),
('K chỉ cần đưa hồ sơ gốc để ký thay C; nếu C phản đối giá thì CCV tự chọn giá thị trường.','Hồ sơ gốc không tạo quyền ký; CCV không tự quyết phương án chia tranh chấp.'),
('Giữ nguyên máy vô thời hạn vì hiện vật không chia được; cả B,C không được bán dù không hạn chế chia.','DS660 có phương thức bán để chia khi không thống nhất, không bắt buộc giữ mãi.')],
'DS660 yêu cầu thỏa thuận giá và người nhận hiện vật, nếu không thống nhất thì bán để chia. DS617 quản lý không tự tạo quyền định đoạt; DS141 kiểm tra quyền K. CC59 kiểm tra ý chí đúng người, không dùng nộp giấy hoặc giá do CCV chọn để thay đồng thuận.','DS:660 DS:617 DS:141 CC:59',['Kiểm tra thỏa thuận nhận hiện vật','Áp phương thức khi không thống nhất','Đối chiếu quyền quản lý và quyền ký của K'])

rev('VER26-021','Nhà 4 tỷ mua bằng lương trong hôn nhân H–W, giấy chỉ tên H. H lập di chúc hợp lệ để toàn nhà cho C, rồi chết; không thỏa thuận chia khác hoặc nợ. W và một con thành niên có khả năng lao động là hàng thứ nhất; W không từ chối, không mất quyền. Khi kiểm kê và tính phần W đúng là gì?',
'Di sản H 2 tỷ; W có 2 tỷ phần chung và tối thiểu 2/3 tỷ từ di sản, không lấy toàn nhà làm di sản.',[
('Di sản là 4 tỷ vì giấy tên H; W hưởng bắt buộc 4/3 tỷ, không có phần sở hữu ngoài di sản.','Giấy một tên không làm mất phần chung W, nền tính phần bắt buộc phải là di sản H.'),
('W giữ 2 tỷ chung, C hưởng cả 2 tỷ di sản vì H đã công chứng di chúc và con không thuộc phần bắt buộc.','W là vợ thuộc nhóm bắt buộc theo điều kiện đã nêu, công chứng không loại quyền đó.'),
('W nhận 3 tỷ gồm nửa nhà và suất pháp luật 1 tỷ; di chúc không được dùng khi còn vợ hợp pháp.','Di chúc vẫn được xét, phần W tối thiểu là hai phần ba suất pháp luật, không tự cả suất.')],
'HN33,34,66 xác định nhà chung và tách 2 tỷ W, 2 tỷ di sản H. DS651 giả định hai suất 1 tỷ; DS644 cho W tối thiểu 2/3 tỷ nếu di chúc không cho hưởng. Quyền lập di chúc chỉ trong phần H, không vì giấy một tên hoặc công chứng mà chuyển cả phần W.','HN:33 HN:34 HN:66 DS:651 DS:644 DS:612',['Xác định nguồn tiền thay vì tên giấy','Tách tài sản W trước nền thừa kế','Tính phần bắt buộc trên di sản H'])

rev('VER26-026','Xe ô tô chung H–W phải đăng ký; H có văn bản W cho bán chiếc X, nay muốn bán chiếc Y khác cũng là xe chung. H ủy quyền K ký bán Y, xuất trình văn bản W về X và đề nghị công chứng theo mẫu chữ ký K đã lưu nhưng K không thuộc nhóm ngoại lệ ký trước. Cần xử lý gì?',
'Cần ý chí bằng văn bản về xe Y và đúng quyền K; mẫu chữ ký không tự miễn ký trước CCV.',[
('W đã cho bán một xe thì H được chọn xe Y thay X, K được ký trước vì văn phòng có mẫu chữ ký.','Phạm vi đồng ý về X không tự mở sang Y; lưu mẫu không đủ ngoại lệ.'),
('K có quyền H cấp về Y là đủ, vì đại diện ký thay khiến yêu cầu thỏa thuận vợ chồng không còn áp dụng.','Quyền từ H không tự chuyển quyền định đoạt W cho K.'),
('W ký văn bản về Y là đủ cho toàn thủ tục; K có thể gửi chữ ký scan vì X,Y đều là xe đăng ký.','Chữa ý chí đồng chủ không thay điều kiện ký công chứng và kiểm tra quyền.')],
'HN35 yêu cầu thỏa thuận bằng văn bản đối với động sản chung phải đăng ký, theo giao dịch và tài sản cụ thể. DS141 đọc quyền K từ quyền H hợp lệ. CC50 có điều kiện riêng cho ký trước, không miễn chỉ vì đã lưu mẫu. Phải kiểm tra độc lập ý chí W, quyền K và thủ tục ký.','HN:35 DS:141 CC:50',['So tài sản X trong đồng ý với Y đang bán','Kiểm tra quyền gốc H và quyền K','Đối chiếu điều kiện ký trước thay vì có mẫu'])

rev('VER26-027','Máy không phải đăng ký là tài sản chung H–W, tạo thu nhập chủ yếu gia đình. Hai người đồng ý bằng văn bản cho thuê một năm; K chỉ được đại diện H nhận tiền thuê. K muốn bán máy cho bên thuê, viện máy không đăng ký nên không cần văn bản W và quyền phụ bán kèm. Xử lý đúng?',
'Tài sản tạo thu nhập chủ yếu vẫn cần thỏa thuận bằng văn bản để bán; quyền nhận tiền không cho K ký bán.',[
('Không đăng ký thì W đồng ý thuê đã đủ bán; K được ký bán để thu trọn khoản tiền giao dịch.','Bỏ tiêu chí thu nhập chủ yếu và mở phạm vi quyền nhận tiền.'),
('Chỉ cần W đồng ý bán miệng trước nhân chứng; K ký vì người thuê là đối tác đã quen của gia đình.','Quen đối tác không chữa hình thức thỏa thuận và thiếu quyền K.'),
('H ký thêm quyền bán K thì có thể bỏ ý chí W, vì văn bản thuê chung đã thể hiện máy được dùng kinh doanh.','Quyền H cấp không tự thay thỏa thuận định đoạt chung cho lần bán.')],
'HN35 còn áp cho tài sản chung tạo thu nhập chủ yếu, không chỉ bất động sản hoặc động sản đăng ký. DS141 giới hạn K nhận tiền; thỏa thuận thuê không tự thành bán. CC42 phải kiểm tra quyền và nội dung yêu cầu nếu công chứng, không suy từ quan hệ đối tác hoặc quyền phụ.','HN:35 DS:141 CC:42',['Nhận diện tài sản tạo thu nhập chủ yếu','Tách đồng ý thuê và bán','Giữ phạm vi đại diện nhận tiền'])

rev('VER26-029','Nhà riêng H cho thuê, tiền thuê là nguồn sống duy nhất gia đình. H cho K quyền quản lý, thu tiền; W chưa đồng ý định đoạt. K muốn tặng nhà cho C và xin công chứng, nói tặng không làm H có thu nhập nên không cần W. Cách xử lý đúng?',
'Định đoạt nhà vẫn cần đồng ý W theo điều kiện nguồn sống; quyền quản lý, thu tiền cũng chưa cho K tặng.',[
('Tặng không thu tiền nên ngoài điều kiện đồng ý W; K ký được vì đang quản lý nhà nguồn sống.','Điều kiện áp với định đoạt tài sản, không chỉ giao dịch làm phát sinh tiền bán.'),
('W đồng ý cho C tiếp tục trả tiền thuê là đủ tặng; không cần đổi quyền K từ quản lý sang định đoạt.','Đồng ý tiếp tục thuê không phải đồng ý tặng và không mở quyền đại diện K.'),
('H có tài sản riêng nên được tặng qua K; chỉ cần C cam kết cho W vay khi gia đình thiếu tiền.','Tài sản riêng còn chịu ngoại lệ nguồn sống và K phải có quyền đúng phạm vi.')],
'HN44 khoản 4 yêu cầu đồng ý vợ/chồng khi định đoạt tài sản riêng có hoa lợi, lợi tức là nguồn sống duy nhất. DS141 tách quản lý, thu tiền với tặng; CC42 kiểm tra cả điều kiện gốc H và quyền K, không vì giao dịch không thu tiền mà bỏ yêu cầu.','HN:44 DS:141 CC:42',['Kiểm tra ngoại lệ định đoạt tài sản riêng','Phân biệt quản lý và tặng tài sản','Đọc ý chí W theo loại giao dịch'])

rev('VER26-030','Nhà riêng W ở tỉnh B là chỗ ở duy nhất H–W; W đã bảo đảm chỗ ở thay thế phù hợp. W trực tiếp xin công chứng bán tại Văn phòng tỉnh A, không thuộc ngoại lệ địa hạt. H đòi chia nửa quyền sở hữu chỉ vì đang ở. Chỉ xét quyền nhà, chỗ ở và nơi công chứng, phương án đúng?',
'Không tự biến nhà riêng thành chung vì là nơi ở duy nhất; vẫn phải xét chỗ ở và công chứng đúng địa hạt B.',[
('H tự có nửa nhà do cùng cư trú; W chỉ được bán nửa còn lại nhưng chọn tỉnh A vì nhà là riêng.','Cư trú không tự tạo sở hữu chung, tài sản riêng không là ngoại lệ địa hạt bán.'),
('Đã bảo đảm chỗ ở thì W được công chứng bán tại A vì yêu cầu nơi ở là hạn chế duy nhất của nhà riêng.','Đủ yêu cầu chỗ ở không thay quy tắc địa hạt hợp đồng bán bất động sản.'),
('Phải chia nhà thành chung trước rồi H–W ký tại B; không được bán nhà riêng là nơi ở duy nhất.','HN31 không bắt chuyển sở hữu thành chung, chủ sở hữu có quyền nhưng phải bảo đảm chỗ ở.')],
'HN31 phân biệt quyền chủ sở hữu riêng và yêu cầu bảo đảm chỗ ở; HN43 giữ căn cứ tài sản riêng, không tự chia đôi vì cư trú. CC44 yêu cầu nơi công chứng bán thông thường theo địa hạt; đủ chỗ ở không tạo ngoại lệ nơi ký.','HN:31 HN:43 CC:44',['Giữ căn cứ sở hữu riêng','Kiểm tra bảo đảm chỗ ở thay thế','Áp địa hạt riêng cho hợp đồng bán'])

rev('VER26-031','H–W xin công chứng chia 500 triệu chung cho W; hồ sơ xác định mục đích trốn nghĩa vụ trả nợ hợp pháp của H và giao dịch giả nhằm che việc H vẫn giữ, sử dụng toàn tiền. Các bên tự nguyện, văn bản ghi hiệu lực ngay. Cách xử lý đúng?',
'Không chứng nhận nội dung trốn nghĩa vụ; tự nguyện, hình thức và ghi hiệu lực ngay không chữa mục đích trái luật.',[
('Công chứng được vì chia tiền chỉ cần văn bản; chủ nợ phải đợi hết hôn nhân mới yêu cầu xử lý.','HN42 đặt vô hiệu do trốn nghĩa vụ, độc lập hình thức chia.'),
('Đổi mốc hiệu lực sang tháng sau thì hợp lệ; mục đích trốn nợ chỉ ảnh hưởng khi chủ nợ có mặt ký.','Thay mốc không chữa mục đích đã xác định trái luật, không bắt chủ nợ dự mới được bảo vệ.'),
('W ký cam kết chịu nợ thay H đủ hợp lệ dù chủ nợ chưa đồng ý và giao dịch giả vẫn giữ nguyên.','Cam kết đơn phương không thay chuyển nghĩa vụ hoặc chữa giả tạo, trốn nợ.')],
'HN38,42 tách quyền chia tài sản với trường hợp chia để trốn nghĩa vụ; DS124 xử lý giả tạo nhằm trốn nghĩa vụ với người thứ ba. CC42 phải yêu cầu sửa nội dung trái luật, nếu không sửa thì từ chối; chữ ký, ngày hiệu lực hoặc cam kết không thay điều kiện nội dung.','HN:38 HN:42 DS:124 CC:42',['Kiểm tra mục đích thực tế việc chia','Đối chiếu nội dung giả tạo với người thứ ba','Tách đúng hình thức và ngày khỏi điều kiện nội dung'])

rev('VER26-032','H–W có nợ chung hợp lệ 300 triệu với X, rồi chia toàn tiền 400 triệu cho W bằng văn bản có hiệu lực. H–W còn ghi W trả hết nợ, X chưa đồng ý giải phóng H, không có thỏa thuận khác. H đề nghị sửa tên người nợ trong hợp đồng công chứng theo lỗi kỹ thuật. Đánh giá đúng?',
'Việc chia không tự giải phóng H trước X; đổi người chịu nợ là sửa nội dung, không phải lỗi kỹ thuật.',[
('W nhận hết tài sản thì H được giải phóng nợ; CCV sửa kỹ thuật vì tổng nợ vẫn là 300 triệu.','Quyền chủ nợ không tự đổi theo tài sản phân chia; thay người nợ làm đổi quyền.'),
('Việc chia có hiệu lực nên X phải đòi W; chỉ cần gửi bản chia để thay văn bản đồng ý chuyển nợ.','Thông báo không thay sự đồng ý của bên có quyền trong chuyển nghĩa vụ.'),
('X chưa đồng ý thì văn bản chia toàn tiền tự vô hiệu, H phải lấy lại 200 triệu trước khi trả nợ.','Không mặc nhiên vô hiệu mọi việc chia do chủ nợ chưa giải phóng H; cần xét căn cứ riêng.')],
'HN39,40 giữ quyền nghĩa vụ với người thứ ba đã phát sinh trước chia, trừ thỏa thuận khác. DS370 yêu cầu đồng ý bên có quyền khi chuyển nghĩa vụ. CC52 không áp cho thay chủ thể nợ; CC53 đòi ý chí và thủ tục sửa nội dung hợp lệ. Không suy việc chia vô hiệu hoặc miễn H chỉ từ một dữ kiện.','HN:39 HN:40 DS:370 CC:52 CC:53',['Chốt quyền X trước khi chia','Tách phân chia tài sản và chuyển nghĩa vụ','Phân loại sửa người nợ là đổi nội dung'])

rev('VER26-035','H có quyền đất riêng, muốn nhập vào chung H–W; việc nhập thuộc giao dịch có hình thức luật định bắt buộc, chưa hoàn tất. H mới ký giấy tự viết, nay W cấp K quyền bán toàn đất như tài sản chung; H chưa ủy quyền bán hoặc trực tiếp tham gia. Chỉ xét việc nhập và quyền ký, xử lý đúng?',
'Chưa coi nhập chung đã hoàn tất chỉ bằng giấy tự viết; quyền W cấp không đủ để K bán toàn quyền của H.',[
('Giấy tự viết có chữ H đủ nhập chung; W được tự bán cả đất nên K cũng được ký theo quyền W.','Bỏ hình thức luật định và quyền định đoạt của các chủ thể, không tự được bán cả chỉ từ W.'),
('Đã có ý chí nhập thì quyền K được công chứng sẽ chữa mọi thiếu hình thức của việc nhập trước đó.','Công chứng ủy quyền không thay giao dịch nhập hoặc cấp quyền thuộc H.'),
('W ký xác nhận đã nhận đất là đủ nhập chung; K dùng văn bản đó thay quyền bán từ H.','Nhận giấy không thay hình thức giao dịch và phạm vi đại diện H.')],
'HN46 yêu cầu nhập tài sản riêng vào chung theo thỏa thuận và hình thức luật định khi tài sản thuộc loại phải tuân thủ. DS117 kiểm tra điều kiện hiệu lực; DS141 không cho quyền W cấp tự bao gồm quyền của H. CC42 phải làm rõ việc nhập và đại diện, không dùng giấy quyền để chữa một giao dịch khác.','HN:46 DS:117 DS:141 CC:42',['Kiểm tra hình thức việc nhập tài sản','Chốt căn cứ quyền H,W tại lúc bán','So quyền K với người thực cấp quyền'])

rev('VER26-038','Chế độ tài sản theo thỏa thuận của H–W không nói cách xử lý nhà riêng W là nơi ở duy nhất. W muốn bán, chưa bảo đảm chỗ ở; K được W giao chỉ tìm khách nhưng xin công chứng bán thay. H cho rằng chỗ trống trong thỏa thuận cho W tự quyết mọi việc và K làm mọi thủ tục. Phân biệt đúng?',
'Áp quy tắc bổ sung về nhà ở và quyền ký; chỗ trống không miễn bảo đảm chỗ ở hoặc mở quyền K.',[
('Thỏa thuận không hạn chế bán thì W bỏ yêu cầu chỗ ở; K được ký vì tìm khách là bước đầu của bán.','HN48 dẫn áp quy tắc bổ sung, DS141 không suy quyền bán từ tìm khách.'),
('K được ký nếu cam kết giúp H–W tìm nhà sau; ý kiến của K thay thỏa thuận và việc bảo đảm chỗ ở.','Cam kết của đại diện thiếu quyền không tự đáp ứng yêu cầu về quyền ký hoặc chỗ ở.'),
('Văn bản tài sản không nói thì toàn chế độ thỏa thuận vô hiệu; chỉ cần chia đôi nhà rồi K ký bán.','Chỗ chưa thỏa thuận có cơ chế bổ sung, không tự làm toàn chế độ vô hiệu hoặc cấp quyền K.')],
'HN48 khoản 2 dẫn quy tắc tương ứng khi chưa thỏa thuận hoặc không rõ; HN31 vẫn đặt yêu cầu nhà ở duy nhất. DS141 giới hạn K tìm khách, không ký bán; CC42 kiểm tra điều kiện giao dịch thực tế. Không suy khoảng trống là miễn luật hoặc vô hiệu toàn chế độ.','HN:48 HN:31 DS:141 CC:42',['Tìm quy tắc bổ sung cho chỗ chưa thỏa thuận','Áp điều kiện nhà ở duy nhất','Giữ phạm vi tìm khách khác quyền ký bán'])

rev('VER26-070','A thành niên tự viết, ký di chúc hợp lệ cho C chiếc máy riêng 60 triệu; không công chứng, không định đoạt 40 triệu tiền riêng còn lại. A chết, chỉ B,D là hàng thứ nhất; không nợ, người bắt buộc hoặc căn cứ loại hưởng. C xin công chứng nhận cả 100 triệu vì là người duy nhất ghi trong di chúc. Phân chia đúng?',
'C hưởng máy 60 triệu theo di chúc; 40 triệu chưa định đoạt chia B,D mỗi người 20 triệu.',[
('C hưởng toàn 100 triệu vì di chúc hợp lệ chỉ có tên C; B,D không còn tư cách đối với tài sản chưa ghi.','Di chúc về chiếc máy không tự định đoạt tiền chưa được đề cập.'),
('B,D mỗi người 50 triệu vì di chúc không công chứng nên chiếc máy cũng phải chia theo pháp luật.','Không mặc nhiên vô hiệu di chúc tự viết, ký đủ điều kiện chỉ do không công chứng.'),
('C hưởng 60 triệu, B,D mỗi người 50 triệu vì phải chia toàn tài sản trước rồi giao riêng chiếc máy C.','Tính lặp chiếc máy trong phần chia pháp luật, vượt tổng di sản.')],
'DS630,633 chấp nhận di chúc tự viết, ký đủ điều kiện không bắt công chứng trong trường hợp này. DS650 chia phần chưa định đoạt theo pháp luật, DS651 hai suất 20 triệu. CC59 phải kiểm tra phạm vi tài sản và người hưởng, không lấy một tên trong di chúc làm quyền nhận toàn di sản.','DS:630 DS:633 DS:650 DS:651 CC:59',['Kiểm tra hình thức di chúc tự viết','Tách phần định đoạt và chưa định đoạt','Tính phần hưởng và giới hạn yêu cầu công chứng'])

rev('VER26-071','A có di chúc công chứng cho C nhà riêng X. Sau đó A tự viết, ký di chúc mới hợp lệ, ghi thay thế toàn bản cũ, cho D nhà X. A chết, D còn sống; không người bắt buộc hoặc trở ngại khác. C giữ bản gốc cũ, xin Văn phòng sửa tên D trong bản mới thành C như lỗi đánh máy. Xử lý đúng?',
'Xét bản mới hợp lệ đã thay bản cũ; giữ gốc công chứng không duy trì quyền C, đổi người hưởng không là lỗi kỹ thuật.',[
('Bản cũ công chứng ưu tiên bản mới tự viết, CCV có thể sửa tên về C để giữ cùng nội dung hồ sơ lưu.','Loại hình công chứng không làm bản cũ ưu tiên khi đã được thay hợp lệ.'),
('D,C cùng nhận một nửa X vì cả hai văn bản đều hợp lệ về hình thức và C còn giữ bản gốc trước.','Dữ kiện nêu thay thế toàn bản cũ, không giữ cả hai quyền hưởng.'),
('C ký xác nhận tên D là nhầm thì sửa được, vì người giữ giấy gốc có quyền yêu cầu sửa nội dung di chúc.','Người hưởng cũ không được tự sửa ý chí A; đổi người hưởng không là lỗi kỹ thuật.')],
'DS640 cho người lập thay thế di chúc, bản cũ bị hủy bỏ khi thay bằng bản mới hợp lệ; DS643 xét hiệu lực tại mở thừa kế. CC52 chỉ sửa lỗi không ảnh hưởng quyền nghĩa vụ, không đổi người hưởng sau chết theo ý C. CC59 kiểm tra di chúc thực có hiệu lực, không ưu tiên người giữ giấy.','DS:640 DS:643 CC:52 CC:59',['Đối chiếu việc thay thế toàn bản cũ','Xét bản có hiệu lực lúc A chết','Phân biệt đổi người hưởng với lỗi kỹ thuật'])

rev('VER26-088','Hợp đồng công chứng A–B ghi nhầm một số seri máy, khiến hiểu sang máy khác; các bên có thể khắc phục ngay để mục đích đạt được và đều đồng ý bằng văn bản. Việc đổi seri ở đây ảnh hưởng xác định đối tượng, không là lỗi đánh máy vô hại. A muốn tự tuyên vô hiệu hoặc yêu cầu sửa kỹ thuật. Hướng đúng?',
'Xét cơ chế khắc phục nhầm lẫn; đổi đối tượng phải theo sửa nội dung, CCV không tự tuyên vô hiệu.',[
('Có nhầm lẫn thì hợp đồng tự vô hiệu toàn bộ, CCV ghi nhận vô hiệu và hoàn phí thay thủ tục sửa.','DS126 có ngoại lệ khi mục đích đạt hoặc có thể khắc phục; thẩm quyền tuyên không thuộc CCV.'),
('Các bên đồng ý thì sửa kỹ thuật dù seri quyết định máy nào được giao, không cần văn bản sửa nội dung.','Đổi xác định đối tượng ảnh hưởng quyền nghĩa vụ nên không là lỗi kỹ thuật vô hại.'),
('A thông báo vô hiệu là đủ làm B mất quyền nhận máy; việc có thể khắc phục chỉ xét nếu B đã trả hết tiền.','Không có điều kiện phải trả hết để áp khả năng khắc phục; không tự tuyên bằng thông báo.')],
'DS126 không mặc nhiên vô hiệu mọi nhầm lẫn, cần xét khả năng khắc phục đạt mục đích. CC52,53 tách lỗi không ảnh hưởng quyền với sửa đối tượng cần thủ tục sửa nội dung. CC54 giữ cơ chế yêu cầu Tòa khi có căn cứ, không cho CCV hoặc A tự tuyên thay.','DS:126 CC:52 CC:53 CC:54',['Kiểm tra khả năng khắc phục đạt mục đích','Đánh giá seri có ảnh hưởng đối tượng','Chọn thủ tục sửa hoặc yêu cầu đúng thẩm quyền'])

rev('VER26-090','A chưa từng bị tuyên mất năng lực nhưng có chứng cứ ký bán nhà đúng lúc không nhận thức, làm chủ hành vi. Nhà đã công chứng; nay A minh mẫn, xin CCV tự hủy và ghi rằng A mất năng lực vĩnh viễn từ ngày ký. B không đồng ý sửa hoặc hủy. Hướng đúng?',
'Xét quyền yêu cầu Tòa về giao dịch tại thời điểm ký; không tự suy mất năng lực vĩnh viễn hoặc để CCV hủy.',[
('Đã công chứng thì không được yêu cầu vô hiệu; chứng cứ không nhận thức chỉ ảnh hưởng giao dịch chưa ký.','Công chứng không loại quyền yêu cầu Tòa khi có căn cứ luật định.'),
('CCV tự hủy theo chứng cứ A cung cấp và thay Tòa tuyên A mất năng lực từ trước ngày ký.','Tách vô hiệu theo thời điểm với thủ tục tuyên mất năng lực; CCV không có thẩm quyền này.'),
('A minh mẫn hiện tại khiến giao dịch trước tự hợp lệ, dù tại đúng lúc ký A không nhận thức được.','Điều kiện ở thời điểm xác lập không tự được chữa bởi trạng thái hiện tại.')],
'DS128 xét người có năng lực nhưng không nhận thức, làm chủ tại đúng lúc xác lập; DS22 là thủ tục tuyên mất năng lực khác. CC53 không cho hủy theo thỏa thuận khi B không đồng ý, CC54 có cơ chế yêu cầu Tòa. Cần đánh giá chứng cứ thời điểm, không suy vĩnh viễn hoặc đã công chứng thì miễn xét.','DS:128 DS:22 CC:53 CC:54',['Chốt trạng thái tại đúng lúc ký','Tách mất năng lực theo quyết định và trở ngại nhất thời','Chọn cơ chế Tòa khi không có đồng thuận hủy'])

rev('VER26-092','Hợp đồng công chứng có phần dịch vụ A và phần chuyển tài sản B; Tòa đã xác định riêng phần B vô hiệu, không ảnh hưởng A. Cơ quan lưu giữ ghi sai địa chỉ không đổi quyền nghĩa vụ; các bên muốn đồng thời tăng giá phần A và gọi cả ba việc là sửa kỹ thuật. Phân loại đúng?',
'Giữ phần A theo phán quyết; địa chỉ sửa kỹ thuật, tăng giá sửa nội dung, không dùng sửa lỗi thay phán quyết.',[
('Phần B vô hiệu khiến phần A mất theo dù Tòa đã xác định độc lập; chỉ còn địa chỉ để sửa kỹ thuật.','DS130 giữ phần còn lại khi không bị ảnh hưởng; phải theo phạm vi phán quyết.'),
('Địa chỉ và tăng giá đều sửa kỹ thuật vì phần A còn hiệu lực, chỉ phần B cần Tòa xử lý tiếp.','Tăng giá thay nghĩa vụ, không thành lỗi kỹ thuật do phần còn lại có hiệu lực.'),
('CCV sửa phần B thành hợp lệ theo ý các bên rồi bỏ phán quyết; mọi sửa đồng thuận đều có giá trị hồi tố.','Không dùng sửa lỗi hoặc ý chí mới để tự gạt phán quyết đã xác định vô hiệu.')],
'DS130 tách vô hiệu từng phần với phần không ảnh hưởng. CC52 áp địa chỉ không đổi quyền, CC53 áp tăng giá có đủ ý chí và thủ tục. CC54 không trao CCV quyền sửa để thay kết luận Tòa; ba việc có căn cứ, hậu quả khác nhau.','DS:130 CC:52 CC:53 CC:54',['Giữ phạm vi vô hiệu từng phần','Phân loại địa chỉ và tăng giá','Tôn trọng cơ chế Tòa khác thủ tục sửa'])

rev('VER26-099','Công ty có hai đại diện theo pháp luật P,Q. Điều lệ quy định P chỉ ký hợp đồng đến 1 tỷ, Q ký trên 1 tỷ; K chỉ được P giao nộp hồ sơ. Hợp đồng bán tài sản 2 tỷ đã được cấp nội bộ chấp thuận, K xin ký công chứng, viện P là đại diện và đã có nghị quyết. Chỉ xét quyền ký đúng?',
'Phải kiểm tra người có quyền theo điều lệ và quyền cấp K; chấp thuận nội bộ, giao nộp hồ sơ chưa cho K ký.',[
('P là một đại diện nên được cấp K mọi quyền bán; nghị quyết làm hạn mức 1 tỷ của P hết tác dụng.','Phạm vi theo điều lệ và phê duyệt nội bộ không tự thay nhau.'),
('K có giấy nộp hồ sơ thì ký được nếu tài sản đã được duyệt giá 2 tỷ; việc ký chỉ hoàn thành thủ tục.','Nộp hồ sơ khác đại diện xác lập hợp đồng, không phụ thuộc giá đã duyệt.'),
('Cả P,Q phải cùng ký mọi giao dịch vì có hai đại diện; không được ủy quyền dù điều lệ phân rõ.','Không mặc nhiên buộc hai chữ ký cho mọi giao dịch hoặc cấm đại diện theo ủy quyền hợp lệ.')],
'DS137 cho pháp nhân có nhiều đại diện theo pháp luật, DS141 xác định phạm vi theo điều lệ và nội dung quyền. Dữ kiện phân rõ hạn mức, K chỉ nộp hồ sơ; CC42 kiểm tra quyền ký chứ không coi nghị quyết duyệt là quyền đại diện. Cần chủ thể và quyền hợp lệ cho hợp đồng 2 tỷ.','DS:137 DS:141 CC:42',['Đọc phân quyền P,Q theo điều lệ','Tách phê duyệt nội bộ khỏi quyền ký','Đối chiếu quyền nộp hồ sơ của K'])

rev('VER26-NEW-01','Doanh nghiệp A soạn hợp đồng theo mẫu đề nghị công chứng với B. Điều khoản phí có hai nghĩa, không thể làm rõ bằng bối cảnh; một điều khoản độc lập khác đã xác định vô hiệu, không ảnh hưởng phần còn lại. A muốn giải thích phí có lợi mình và tuyên cả hợp đồng vô hiệu để khỏi giao hàng. Hướng đúng?',
'A chịu bất lợi khi giải thích phí không rõ; vô hiệu phần độc lập không tự làm phần còn lại mất hiệu lực.',[
('B ký mẫu thì mọi nghĩa do A chọn đều ràng buộc; phần vô hiệu độc lập kéo theo toàn hợp đồng.','DS405 đặt bất lợi cho bên đưa mẫu, DS130 không tự vô hiệu toàn khi phần còn lại độc lập.'),
('CCV chọn cách có lợi A vì A trả phí soạn; chỉ cần B biết có điều khoản vô hiệu là toàn hợp đồng hợp lệ.','Ai trả phí không quyết định nguyên tắc giải thích, biết không chữa phần vô hiệu đã xác định.'),
('Phí không rõ tự làm toàn hợp đồng vô hiệu; không cần xét phần độc lập hoặc khả năng tiếp tục giao hàng.','Không rõ nghĩa có quy tắc giải thích, không mặc nhiên hủy toàn giao dịch.')],
'DS405 khoản 2 đặt bất lợi cho bên đưa hợp đồng theo mẫu khi điều khoản không rõ; DS130 giữ phần không ảnh hưởng bởi vô hiệu từng phần. CC42 phải làm rõ dự thảo và nội dung được chứng nhận, không chọn theo bên trả phí hoặc coi chữ ký B chữa mọi điều khoản.','DS:405 DS:130 CC:42',['Áp nguyên tắc giải thích mẫu không rõ','Tách vô hiệu từng phần độc lập','Kiểm tra dự thảo thay vì ai trả phí'])

rev('VER26-NEW-28','A ký quỹ tại X để bảo đảm nghĩa vụ với B; vi phạm và thiệt hại đủ căn cứ đã được xác định. B chỉ ủy quyền K nộp yêu cầu thanh toán, chưa cho nhận tiền. K muốn X trả vào tài khoản riêng mình, bỏ trừ chi phí dịch vụ, nói chữ ký công chứng trên quyền đã đủ mọi điều kiện. Nhận định đúng?',
'Thanh toán ký quỹ theo cơ chế qua X sau chi phí dịch vụ; quyền nộp yêu cầu không tự cho K nhận tiền riêng.',[
('X trả toàn số dư vào K vì quyền đã công chứng; chi phí dịch vụ chỉ thu A sau, không liên quan thanh toán.','Bỏ cơ chế sau trừ chi phí và mở phạm vi quyền nộp sang nhận tiền.'),
('K tự lấy tiền trực tiếp từ A là ký quỹ; X chỉ xác nhận A vi phạm rồi hết nghĩa vụ thanh toán.','Ký quỹ có cơ chế qua tổ chức tín dụng nơi phong tỏa, không đổi thành tự thu ngoài tài khoản.'),
('X chỉ cần kiểm tra số dư đủ; quyền K và thiệt hại không cần đối chiếu vì công chứng đã bảo đảm mức thanh toán.','Công chứng quyền không xác định thay điều kiện, phạm vi khoản được nhận và người nhận.')],
'DS330 quy định ký quỹ và thanh toán, bồi thường qua tổ chức tín dụng sau trừ chi phí dịch vụ, theo thủ tục luật. DS141 giới hạn K nộp yêu cầu; CC42 về kiểm tra quyền không biến công chứng thành quyền nhận vào tài khoản riêng hoặc chứng cứ mọi điều kiện thanh toán.','DS:330 DS:141 CC:42',['Kiểm tra điều kiện thanh toán ký quỹ','Áp cơ chế chi phí qua tổ chức tín dụng','Đối chiếu quyền nộp yêu cầu và nhận tiền'])

rev('VER26-NEW-67','B sở hữu vườn cây, A có quyền hưởng dụng còn hiệu lực. A cho C khai thác, thu quả; B muốn bán vườn cho D, đề nghị CCV ghi sale tự chấm dứt quyền A và C phải giao toàn quả từ hôm chuyển sở hữu. Không thỏa thuận chấm dứt hoặc căn cứ khác. Phân biệt đúng?',
'A có thể cho C khai thác trong quyền hưởng dụng; B bán nhưng không tự làm mất quyền hưởng dụng đã xác lập.',[
('B bán là quyền chủ sở hữu nên A,C mất quyền từ lúc ký, mọi quả sau đó tự thuộc D.','DS263 giới hạn định đoạt không được thay đổi quyền hưởng dụng đã xác lập.'),
('A đã cho C khai thác thì A thành chủ vườn, B không còn quyền bán cho D trong thời hạn hưởng dụng.','Quyền hưởng dụng không chuyển quyền sở hữu vườn sang A.'),
('C được thu quả nên được ký bán vườn thay B; CCV chỉ cần giấy A cho khai thác, không cần quyền B.','Quyền khai thác không là quyền sở hữu hoặc quyền đại diện định đoạt B.')],
'DS261 cho người hưởng dụng tự hoặc cho người khác khai thác, thu hoa lợi; DS263 giữ quyền chủ sở hữu định đoạt nhưng không thay đổi hưởng dụng đã xác lập. CC42 phải kiểm tra quyền và nội dung, không ghi việc chuyển sở hữu tự xóa quyền A hoặc coi C được bán từ quyền khai thác.','DS:261 DS:263 CC:42',['Tách hưởng dụng và quyền sở hữu','Giữ hưởng dụng khi chủ sở hữu chuyển quyền','Kiểm tra nội dung công chứng không tự tạo chấm dứt'])

rev('CC-001','A trả phí và đưa hợp đồng do luật sư soạn, muốn CCV chỉ xác nhận chữ ký vì đã tự chịu trách nhiệm nội dung. A không đọc được; bên mua B xin làm chứng vì hiểu dự thảo. Các bên đều tự nguyện. Công chứng viên phải phân biệt những việc gì?',
'Dịch vụ công vẫn phải kiểm tra tính hợp pháp giao dịch; luật sư soạn và trả phí không thay người làm chứng đủ điều kiện.',[
('Trả phí cho phép chọn phạm vi chỉ xác nhận chữ ký; B hiểu dự thảo nên đủ làm chứng nếu A đồng ý.','Tính chất công chứng và điều kiện người làm chứng không do phí hoặc sự hiểu văn bản quyết định.'),
('Vẫn kiểm tra tính hợp pháp nhưng B làm chứng được vì có năng lực, không cần xét B là bên giao dịch.','Bên tham gia giao dịch không đáp ứng tính độc lập của người làm chứng theo luật.'),
('Thay B bằng người độc lập là đủ để CCV bỏ kiểm tra nội dung, vì luật sư và A đã chịu trách nhiệm.','Đủ người làm chứng không miễn nghĩa vụ kiểm tra tính hợp pháp trong công chứng.')],
'CC2 xác định công chứng là dịch vụ công chứng nhận tính xác thực, hợp pháp giao dịch, không thu hẹp thành chữ ký theo bên trả phí. CC42 yêu cầu kiểm tra nội dung; CC49 loại bên tham gia khỏi tư cách làm chứng. Dự thảo luật sư soạn, cam kết và nhân chứng là các yếu tố riêng, không thay chức năng kiểm tra.','CC:2 CC:42 CC:49',['Xác định chức năng công chứng dù dự thảo bên ngoài','Kiểm tra người làm chứng không tham gia giao dịch','Tách tự nguyện và trả phí khỏi điều kiện hợp pháp'])

rev('CC-073','Hợp đồng công chứng ghi giá bằng ký hiệu tự đặt; hai bên nay hiểu khác nhau giữa 100 triệu và 1 tỷ, chưa có căn cứ xác định số nào đúng. Họ đề nghị tẩy ký hiệu, ghi số theo ý người đang giữ bản gốc, gọi đó là lỗi chữ viết và báo bên kia sau. Xử lý phù hợp?',
'Làm rõ ý chí, giá và ảnh hưởng quyền; không tự tẩy hoặc sửa kỹ thuật khi nội dung nghĩa vụ còn tranh chấp.',[
('Người giữ gốc chọn giá rồi CCV sửa kỹ thuật, vì mục tiêu chỉ thay ký hiệu thành chữ dễ đọc.','Thay ký hiệu đang tranh chấp có thể đổi nghĩa vụ, không căn cứ chọn giá theo người giữ giấy.'),
('Hai bên từng ký đủ thì CCV được chọn giá cao hơn để bảo đảm quyền bán; thông báo sau thay được đồng ý.','Không có quyền chọn giá thay các bên hoặc suy chữ ký cũ là đồng ý nghĩa mới.'),
('Chỉ cần viết đè ký hiệu thành số 100 triệu, không tẩy thì đúng quy tắc chữ viết và không phải sửa nội dung.','Viết đè bị cấm theo quy tắc; cách thao tác không thay việc xác định nội dung thực và quyền.')],
'CC47 yêu cầu chữ rõ, dễ đọc, không ký hiệu trái quy tắc, không tẩy xóa hoặc viết đè. CC52 chỉ sửa lỗi không ảnh hưởng quyền nghĩa vụ; khi giá chưa rõ phải làm rõ theo CC42, nếu đổi nội dung thì CC53 đòi ý chí và thủ tục. Không dùng việc thay cách viết để chọn giá thay một bên.','CC:47 CC:52 CC:53 CC:42',['Làm rõ nghĩa giá đang bất đồng','Đánh giá ảnh hưởng nghĩa vụ trước phân loại lỗi','Giữ cách ghi và thủ tục sửa đúng bản chất'])

rev('IMP-T60-031','G giám hộ người chưa thành niên M, quản lý 600 triệu riêng M. G muốn tặng 200 triệu cho người họ hàng, giám sát S đã đồng ý, nói khoản đó chỉ một phần tài sản. G cũng muốn bán máy giá trị lớn của M vì lợi ích M, nhưng S chưa đồng ý việc bán. Phân biệt đúng?',
'Đồng ý S không mở quyền tặng tài sản M; việc bán vì lợi ích M vẫn cần giám sát và đúng quyền, thủ tục.',[
('Tặng 200 triệu được vì S đã đồng ý và M còn 400 triệu; bán máy không cần S do đã chứng minh lợi ích.','DS59 cấm giám hộ đem tài sản người được giám hộ tặng người khác; bán lớn còn điều kiện giám sát.'),
('Không tặng được nên G cũng không được bán máy vì giám hộ chỉ được bảo quản, không định đoạt có lợi.','Luật cho giao dịch vì lợi ích người được giám hộ theo điều kiện, không cấm mọi định đoạt.'),
('S đồng ý tặng được coi đồng ý thay cho bán máy; CCV chỉ cần kiểm tra tổng tài sản M vẫn đủ nuôi dưỡng.','Ý chí giám sát gắn giao dịch, không chuyển từ việc tặng bị cấm sang bán khác.')],
'DS59 tách cấm tặng tài sản người được giám hộ khỏi giao dịch vì lợi ích có thể được thực hiện; bán tài sản lớn cần đồng ý giám sát. DS141 kiểm tra quyền theo luật, CC42 không chứng nhận chỉ dựa tổng tài sản còn lại hoặc chuyển đồng ý giữa hai giao dịch.','DS:59 DS:141 CC:42',['Tách điều cấm tặng khỏi quyền giao dịch có lợi','Kiểm tra giám sát đúng việc bán lớn','Đối chiếu quyền, không suy từ tài sản còn lại'])

rev('IMP-T60-033','A hưởng quyền lối đi hợp lệ qua đất B, không thỏa thuận cho mở rộng. Lối cũ đáp ứng nhu cầu hợp lý; A muốn tăng gấp đôi gây thiệt hại không cần thiết và tự xin sửa văn bản công chứng như lỗi kích thước. B lại muốn khóa cả lối cũ để phản đối. Hướng đúng?',
'A không được lạm dụng mở rộng; B không tự ngăn lối hợp lệ, đổi kích thước ảnh hưởng quyền không là lỗi kỹ thuật.',[
('B khóa được cả lối để buộc A dừng mở rộng; khi A trả tiền thì CCV sửa kỹ thuật kích thước theo ý A.','Vi phạm đề xuất mở rộng không tạo quyền ngăn lối cũ; đổi quyền không là lỗi kỹ thuật.'),
('A có quyền đi thì được chọn mọi kích thước cần kinh doanh; B chỉ được yêu cầu bồi thường sau mở rộng.','DS248 yêu cầu nhu cầu hợp lý và không lạm dụng, không ưu tiên tuyệt đối nhu cầu A.'),
('CCV tăng kích thước nếu A cam kết không tranh chấp; B phải theo vì văn bản cũ đã công chứng quyền đi.','Công chứng quyền cũ không cho CCV tự tạo phạm vi mới hoặc thay ý chí các bên.')],
'DS248 đặt nhu cầu hợp lý, không lạm dụng và không ngăn cản việc thực hiện quyền hợp lệ. CC52 không áp thay kích thước làm đổi quyền; CC53 đòi ý chí và thủ tục sửa nội dung. Phải giữ lối hợp lệ trong khi xử lý đề xuất mở rộng, không chọn hành vi vi phạm để đáp trả.','DS:248 CC:52 CC:53',['Giữ nhu cầu hợp lý của lối đi đã có','Tách chống lạm dụng và ngăn quyền hợp lệ','Phân loại đổi kích thước là đổi nội dung quyền'])

rev('IMP-T60-080','A không biết chữ, minh mẫn, muốn di chúc. M độc lập viết lại lời A, hai nhân chứng đủ điều kiện đã ký, A điểm chỉ; chưa công chứng hoặc chứng thực. A muốn ủy quyền M mang giấy rồi ký thay mọi việc khi A vắng mặt để hoàn thiện. Cần xử lý thế nào?',
'Còn yêu cầu công chứng hoặc chứng thực cho di chúc người không biết chữ; không hoàn thiện bằng người khác lập, ký thay A.',[
('Hai nhân chứng đủ nên dùng như di chúc văn bản có người chứng, bỏ công chứng; M ký thay nếu có giấy quyền.','DS630 khoản 3 đặt điều kiện riêng cho người không biết chữ, không chỉ quy tắc chung nhân chứng.'),
('Chỉ cần chứng thực chữ ký M là đủ vì M viết văn bản; ý chí A đã thể hiện bằng điểm chỉ trước đó.','Chứng thực chữ ký người viết không thay công chứng hoặc chứng thực di chúc theo luật.'),
('M đem giấy có hai nhân chứng đến công chứng thay A; CCV chỉ cần đối chiếu chữ ký họ và ghi ngày mới.','DS637,CC58 giữ việc người lập tự thực hiện, không ủy quyền M hoàn thiện lập di chúc thay.')],
'DS630 khoản 3 yêu cầu người làm chứng lập văn bản và có công chứng hoặc chứng thực khi người lập không biết chữ. DS632,634 về nhân chứng không loại điều kiện riêng đó. DS637,CC58 không cho ủy quyền người khác lập, ký di chúc thay; cần hoàn thiện thủ tục trực tiếp đúng nhánh áp dụng.','DS:630 DS:632 DS:634 DS:637 CC:58',['Áp hình thức riêng người không biết chữ','Tách đủ nhân chứng và đủ công chứng hoặc chứng thực','Giữ hành vi trực tiếp người lập di chúc'])

rev('IMP-T60-084','Máy là tài sản chung H–W tạo thu nhập chủ yếu, đã cầm cố hợp lệ cho X. X đồng ý H tặng máy cho C; W chỉ đồng ý giao dịch cầm cố cũ, chưa đồng ý tặng bằng văn bản. K được H giao lấy giấy máy nhưng muốn ký hợp đồng tặng công chứng. Thiếu gì?',
'Đồng ý X chưa thay ý chí W cho việc tặng; quyền lấy giấy của K cũng chưa đủ ký định đoạt máy.',[
('X đồng ý là đủ vì đang giữ máy; W đã đồng ý cầm cố nên được coi cho phép mọi định đoạt tiếp.','DS312 điều kiện bên nhận cầm cố khác điều kiện ý chí chủ thể tài sản chung theo HN35.'),
('W đồng ý tặng thì K ký được từ quyền lấy giấy, vì máy không thuộc loại phải đăng ký sở hữu.','Lấy giấy không là quyền ký tặng; không đăng ký không loại điều kiện tài sản tạo thu nhập chủ yếu.'),
('H cấp quyền tặng K là đủ, X đồng ý sẽ chữa thiếu thỏa thuận W vì chủ nợ đang kiểm soát tài sản.','Quyền H và đồng ý chủ nợ không tự gồm quyền định đoạt W.')],
'DS312 cho xét tặng tài sản cầm cố khi bên nhận đồng ý theo điều kiện luật. HN35 vẫn đòi văn bản với tài sản chung tạo thu nhập chủ yếu; đồng ý lần cầm cố không tự cho phép tặng. DS141 giới hạn K lấy giấy, CC42 kiểm tra đủ các tầng quyền, không chỉ người đang giữ tài sản.','DS:312 HN:35 DS:141 CC:42',['Kiểm tra đồng ý bên nhận cầm cố','Tách ý chí W cho lần định đoạt mới','So quyền nhận giấy và ký tặng của K'])

assert len(ROWS)==60 and len({r['id'] for r in ROWS})==60
profile={'version':1,'date':'2026-10-13','baseCommit':'ac4fc13e07d88196e1c6a27af72db2bdc952f8ba','questions':ROWS}
(ROOT/'data/scenario-refinements-remaining-2026.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n')
legal={'date':'2026-10-13','scope':'60 câu ngoài nhóm 67; viết tình huống, lựa chọn và lời giải áp dụng mới.',
       'retrievalLimits':'Tái sử dụng chứng cứ điều khoản từ nguồn chính thức đã lưu; đối chiếu danh tính luật hiện hành và truy xuất bổ sung các điều DS261,263,305,306,330,348,370,405. Chưa hiệu chỉnh bằng lượt làm thử.',
       'evidence':PROOFS,'questions':DEC}
(ROOT/'reports/remaining-60-legal-review-2026-10-13.json').write_text(json.dumps(legal,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(ROWS),'additional cases;',len(PROOFS),'article records')

