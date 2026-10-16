// Record a bounded legal review separately from automated scoring verification.
const fs=require('node:fs'),path=require('node:path'),{createHash}=require('node:crypto');
const {root,effectiveBank}=require('./lib/effective-bank.cjs');
const bank=effectiveBank({polish:true,answers:true}),byId=new Map(bank.map(q=>[q.id,q]));
const sha=x=>createHash('sha256').update(typeof x==='string'?x:JSON.stringify(x)).digest('hex');
const sources={
 CC:{url:'https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/3/50-vbhn-vpqh.pdf',mode:'official_consolidated_pdf_text',document:'Luật Công chứng, VBHN 50/VBHN-VPQH ngày 17/03/2026',scope:'Các điều được ghi riêng tại từng câu; không áp sửa đổi hiệu lực 01/01/2027 cho tình huống tháng 10/2026.'},
 DS:{url:'https://datafiles.chinhphu.vn/cpp/files/vbpq/2016/01/91.signed.pdf',mode:'official_pdf_and_indexed_official_reproductions',document:'Bộ luật Dân sự số 91/2015/QH13',limitations:'PDF gốc không có lớp văn bản trích xuất trong công cụ; dùng các đoạn điều luật được lập chỉ mục từ các cổng cơ quan nhà nước. Không coi mở trang thất bại là đã đọc toàn văn.',checkedMirrors:[
  'https://congan.gialai.gov.vn/vi/news/cac-dao-luat-quan-trong/bo-luat-dan-su-2015-773.html',
  'https://btllang.mod.gov.vn/van-ban/vbpq-do-nha-nuoc-ban-hanh/5001-bo-luat-dan-su-2015.html',
  'https://vbpl.vn/bokehoachvadautu/Pages/ivbpq-toanvan.aspx?ItemID=95942',
  'https://vbpl.moj.gov.vn/dongthap/Pages/vbpq-toanvan.aspx?ItemID=95942',
  'https://vbpl.moj.gov.vn/bokhoahoccongnghe/Pages/vbpq-print.aspx?ItemID=95942',
  'https://vbpl.moj.gov.vn/daknong/Pages/vbpq-toanvan.aspx?ItemID=95942&Keyword=']},
 HN:{url:'https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-121-vbhn-vpqh-46059.htm',mode:'official_listing_and_indexed_statutory_text',document:'Luật Hôn nhân và gia đình số 52/2014/QH13; VBHN 121/VBHN-VPQH năm 2025',checkedMirrors:[
  'https://vbpl.vn/boyte/Pages/vbpq-toanvan.aspx?ItemID=36870',
  'https://vbpl.moj.gov.vn/Toaannhandantoicao/Pages/vbpq-print.aspx?ItemID=36870',
  'https://moj.gov.vn/vbpq/Lists/Vn%20bn%20php%20lut/Attachments/29058/VanBanGoc_52.2014.QH13.pdf'],limitations:'Đường dẫn tải PDF hợp nhất từ Công báo lỗi khi truy xuất; chỉ đối chiếu các điều được nêu, không xác nhận đã đọc trọn bản hợp nhất.'},
 NQ03:{url:'https://www.tapchitoaan.vn/nghi-quyet-cua-hoi-dong-tham-phan-tandtc-huong-dan-ap-dung-phap-luat-trong-giai-quyet-tranh-chap-ve-dat-coc16557.html',mode:'issuing_court_journal_digest_not_signed_original',document:'Thông tin về Nghị quyết 03/2026/NQ-HĐTP',effectiveFrom:'2026-10-15',publishedAt:'2026-10-15',scope:'Nguồn phát hiện rủi ro và xếp hàng đối chiếu, chưa dùng thay bản gốc để sửa khóa.',
  finding:'Bài của cơ quan TANDTC nêu hướng dẫn về giới hạn mức phạt cọc theo giá trị hợp đồng. Cần kiểm tra bản gốc và phạm vi áp dụng trước khi cập nhật câu thiếu dữ kiện.'}
};
// Authored decisions after reading the current stems and all four options.
const reviewed=[
 ['CC-014',['CC:10','CC:12'],'Không quá 70 tuổi khác với bị loại ngay khi đủ 70; đạt kiểm tra tập sự vẫn là điều kiện độc lập.'],
 ['CC-015',['CC:10','CC:14','DS:22'],'Bằng thạc sĩ luật thuộc nhóm được xét; giấy bác sĩ không thay quyết định của Tòa. Nên thay cách nói năng lực pháp lý bằng năng lực hành vi dân sự.','clarify_terminology'],
 ['CC-016',['CC:10'],'Chỉ hai năm sáu tháng sau bằng chưa đủ ba năm công tác theo dữ kiện; học nghề không tự bù thời gian công tác.'],
 ['CC-017',['CC:11'],'Không thuộc nhóm được rút ngắn thì học 12 tháng; kinh nghiệm pháp chế thông thường không tự tạo nhóm sáu tháng.'],
 ['CC-018',['CC:11','CC:12'],'Chưa đủ năm năm hành nghề ở thời điểm xét; rút ngắn đào tạo không đồng nghĩa rút thời gian tập sự.'],
 ['CC-022',['CC:12.3'],'Giới hạn hai người tính cùng một thời điểm; chia lịch có mặt không tạo suất thứ ba khi quan hệ tập sự chưa kết thúc.'],
 ['CC-023',['CC:12.5','CC:14','DS:22'],'Mốc năm năm là của giấy chứng nhận kết quả kiểm tra tập sự; cần ghi đủ tên giấy trong câu dẫn, không để nhầm với giấy tốt nghiệp đào tạo. Khóa hiện tại không đổi.','clarify_certificate_type'],
 ['CC-026',['CC:15.2','CC:16.2.e'],'Không gia hạn tạm đình chỉ vượt 12 tháng; hết hạn mà lý do còn là căn cứ miễn nhiệm, không tự hành nghề lại.'],
 ['CC-029',['CC:16.2.đ'],'Tách trường hợp chưa hành nghề sau bổ nhiệm và ngoại lệ không hành nghề do tạm đình chỉ.'],
 ['CC-074',['CC:47.2','DS:140','DS:141','DS:142'],'Giờ phút không bắt buộc cho mọi văn bản. Tuy nhiên bỏ hoặc ghi lùi giờ không khôi phục quyền đã hết theo dữ kiện.'],
 ['CC-075',['CC:48.1'],'Thông tin việc làm chứng, phiên dịch và lý do ngoài trụ sở thuộc lời chứng; chữ ký không thay nội dung phải ghi.'],
 ['CC-076',['CC:6.1','CC:48.2'],'Dấu tổ chức hoặc chữ ký người quản lý không thay chữ ký công chứng viên thực hiện chứng nhận.'],
 ['CC-079',['CC:46','CC:49.2','CC:58.1','DS:632'],'Không ký và không điểm chỉ được không đồng nghĩa chỉ còn di chúc miệng; phải dùng cơ chế người làm chứng đủ điều kiện, không để người hưởng lập thay.'],
 ['CC-080',['CC:58.1','CC:58.2'],'Dấu hiệu đe dọa chưa làm rõ không được khắc phục bằng giấy đồng ý hoặc ủy quyền người khác ký.'],
 ['CC-089',['CC:58.1','DS:625.2','DS:630.2'],'Người 17 tuổi có thể lập di chúc bằng văn bản với sự đồng ý luật định, nhưng không được ủy quyền lập thay.'],
 ['CAL26-005',['CC:64.2'],'Đến 09:20 mới đủ chữ ký số của cả công chứng viên và tổ chức; gửi tệp sau đó không phải mốc khởi đầu hiệu lực.'],
 ['CAL26-006',['DS:328'],'200 triệu vẫn là cọc bảo đảm thực hiện; cơ chế mặc định riêng cọc là 400 triệu, không cộng 300 triệu trả trước. Đã có giá hợp đồng 1 tỷ; không thấy mâu thuẫn với rủi ro trần phạt nêu trong nguồn NQ03.'],
 ['CAL26-011',['DS:328'],'Dữ kiện đã xác nhận thỏa thuận thay mức mặc định là hợp pháp. Tổng phát sinh 300 triệu, không phải số dư 250 triệu; không xác nhận chung mọi mức thỏa thuận đều hợp pháp.'],
 ['CAL26-026',['CC:49.2'],'Không đọc được là căn cứ có người làm chứng; quyền đòi tiền liên quan cũng loại tư cách. Chỉ định không bỏ điều kiện độc lập.'],
 ['CAL26-048',['DS:637'],'Con công chứng viên hưởng thừa kế là căn cứ không được chứng nhận; đồng nghiệp đọc hồ sơ hoặc người lập chấp thuận không tạo ngoại lệ.'],
 ['CAL26-067',['CC:54'],'Chỉ công chứng viên đã thực hiện việc công chứng thuộc tư cách nghề được liệt kê; người làm chứng và người liên quan có quyền đề nghị riêng, không cần ủy quyền người ký.'],
 ['CAL26-082',['HN:77.2'],'Cả định đoạt động sản có đăng ký và dùng tài sản để kinh doanh đều thuộc nhóm cần sự đồng ý bằng văn bản; tiền riêng không làm mất ngoại lệ kinh doanh.'],
 ['HARD26-029',['DS:141','DS:143','DS:328'],'A chấp thuận sau khi đọc đầy đủ hợp đồng tạo căn cứ ràng buộc phần vượt; không dùng vượt quyền ban đầu để loại hậu quả cọc.'],
 ['HARD26-058',['CC:64.2','DS:140','DS:141','DS:142'],'Đủ chữ ký số không chữa quyền đại diện hết trước lúc K ký. Điều 142 là căn cứ bổ sung nên đưa vào hồ sơ nếu sửa tiếp.'],
 ['HARD26-061',['HN:33','HN:34','HN:35','DS:141','DS:142','DS:328'],'K tự nhân danh W không tự tạo quyền nhận cọc cho W. Khi giảng giải phải giữ các ngoại lệ công nhận, biết không phản đối hợp lý hoặc lỗi ở Điều 142; không khẳng định cứ thiếu văn bản ủy quyền là luôn không ràng buộc.'],
 ['HARD26-063',['DS:564','DS:141','DS:143'],'Quyền cấp lại không được hạ giới hạn gốc. B biết vượt quyền thì phải áp cả ngoại lệ về trách nhiệm người đại diện; không chỉ xét A chưa đồng ý.'],
 ['CAL26-086',['DS:617.1'],'Được cử quản lý không tự có quyền bán; thông báo và cam kết bồi thường không thay chấp thuận định đoạt bằng văn bản.'],
 ['HARD26-093',['DS:654','DS:651'],'Đã xác định chăm sóc như cha con thì không đặt thêm điều kiện nhận nuôi; với khối di sản ròng và số người đã cho, mỗi người 300 triệu.'],
 ['CAL26-054',['DS:621.2','DS:630'],'Biết hành vi mà vẫn cho hưởng theo di chúc là ngoại lệ có phạm vi; không tự khôi phục mọi phần theo pháp luật.'],
 ['HARD26-081',['HN:66','DS:644','DS:650','DS:651'],'Tách di sản 2 tỷ; phần chưa định đoạt chia W và B mỗi người 500 triệu trước bổ sung. Mức bắt buộc W là tổng 666⅔ triệu, chỉ thiếu 166⅔ triệu, không cộng lại cả mức.']
];
const decisions=reviewed.map(([id,provisions,note,decision='retain_key'])=>{
 const q=byId.get(id);if(!q)throw Error('Unknown reviewed ID '+id);
 return {id,questionSha256:sha(q),applicableAt:q.applicableAt,answerKey:q.answers.filter(a=>a.correct).map(a=>a.id),provisions,
  decision,note,sourceIds:[...new Set(provisions.map(p=>p.split(':')[0]))],dataChanged:false};
});
const depositCandidates=bank.filter(q=>['active','verified'].includes(q.status)&&(q.topic.includes('cọc')||q.legalBasis.some(b=>/328/.test(b.article)))).map(q=>q.id);
const tap=fs.readFileSync(path.join(root,'reports/full-verification-2026-10-16.tap'),'utf8');
if(!/# tests 92\s/.test(tap)||!/# pass 92\s/.test(tap)||!/# fail 0\s/.test(tap)||!tap.includes('9690 answer/scoring cases'))throw Error('Full suite not confirmed');
const report={version:1,date:'2026-10-16',timezone:'Asia/Ho_Chi_Minh',baselineMain:'f9a9d46d811b12eaf8c22146b1515748873675b3',
 baselineTree:'bbed46dc190192c48c82ffa2fe40ff4548f04689',bankSha256:sha(bank),sources,
 verification:{command:'node --test --test-reporter=tap tests/*.test.cjs',tests:92,passed:92,failed:0,questionsExercised:793,scoringCases:9690,
  tap:'reports/full-verification-2026-10-16.tap',tapSha256:sha(tap),scope:'All Node test files, DOM harness and mocked network/storage; not a live browser or production database test.',
  notRun:['live browser end-to-end','SQL integration scripts against a database','production network/API mutations']},
 audit:{file:'reports/answer-review-full-audit-2026-10-16.json',eligible:793,duplicateIds:0,remainingHeuristic:'490 câu bị nhắc về số biến thể; đây là tiêu chí biên tập, không phải 490 đáp án sai hay 490 kiểm thử thất bại.'},
 legalScope:{reviewedQuestions:decisions.length,retainedKeys:decisions.length,terminologyClarifications:2,legalCertificationOfWholeBank:false,dataOrKeysChanged:false,
  limitations:'Đối chiếu các điều và dữ kiện nêu trong hồ sơ, không chứng nhận mọi điều luật hoặc toàn bộ 793 câu. Nguồn lập chỉ mục được phân biệt với văn bản đã mở toàn văn.'},
 decisions,
 urgentFinding:{id:'DEP26-006',questionSha256:sha(byId.get('DEP26-006')),decision:'pending_signed_resolution_and_temporal_scope',priority:'high',currentKey:['B'],
  note:'Câu ghi chung tháng 10/2026, không cho giá trị hợp đồng được bảo đảm, nhưng kết luận chắc tổng hoàn và phạt là 1,2 tỷ. Nguồn từ cơ quan TANDTC về NQ03 mới hiệu lực nêu giới hạn phạt theo giá trị hợp đồng. Vì thiếu dữ kiện, cần kiểm tra bản gốc, mốc xét xử và phạm vi áp dụng trước khi giữ hoặc sửa kết luận. Chưa xác định khóa hiện tại sai trong mọi trường hợp; chưa đổi nội dung hay trạng thái active.',
  nextAction:'Lấy bản gốc nghị quyết; chốt thời điểm pháp luật áp dụng và giá trị hợp đồng trong tình huống; rà giải thích/nhiễu rồi mới cập nhật dữ liệu và kiểm thử lại.'},
 nextQueue:{reason:'Rà tác động NQ03; danh sách tìm theo chủ đề/căn cứ chỉ là ứng viên, không đồng nghĩa tất cả bị ảnh hưởng hoặc đã sai.',candidateIds:depositCandidates,
  alsoCheck:['CC-015: dùng đúng thuật ngữ năng lực hành vi dân sự','CC-023: ghi đầy đủ tên giấy chứng nhận kết quả kiểm tra tập sự','HARD26-058/HARD26-061: bổ sung căn cứ Điều 142 vào hồ sơ khi biên tập tiếp']}};
fs.writeFileSync(path.join(root,'reports/legal-checkpoint-2026-10-16.json'),JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(path.join(root,'reports/legal-checkpoint-2026-10-16.md'),`# Chốt kiểm thử và rà pháp lý — 16/10/2026\n\n`+
 `## Kiểm thử\n\nĐạt **92/92** kiểm thử Node; **9.690** ca chấm điểm trên **793** câu không lệch khóa. Đã lưu TAP đầy đủ. Kiểm toán không trùng ID. Đây là DOM harness/mạng giả lập, chưa chạy trình duyệt thật hoặc kiểm thử SQL trên cơ sở dữ liệu.\n\n`+
 `Lượt trước có 91/92 đạt do bản thảo completion-variants bị cắt cụt. Phần thiếu đã được khôi phục đúng bản Git, không sửa ý nghĩa; bản chạy hiện tại đạt đủ 92.\n\n`+
 `## Pháp lý\n\nĐã đối chiếu 30 câu ưu tiên, chưa xác định cần đổi khóa. Hai câu cần làm rõ: CC-015 dùng thuật ngữ năng lực hành vi dân sự; CC-023 ghi rõ tên giấy chứng nhận kết quả kiểm tra tập sự. Không coi kết quả này là kiểm định toàn bộ ngân hàng. Hồ sơ JSON lưu điều khoản, nguồn, hạn chế truy xuất và hash từng câu.\n\n`+
 `### Ưu tiên khẩn: DEP26-006\n\n`+
 `Nguồn của Tạp chí TAND cho biết Nghị quyết 03/2026/NQ-HĐTP có hiệu lực 15/10/2026 và có hướng dẫn giới hạn mức phạt cọc theo giá trị hợp đồng. Câu DEP26-006 ghi chung tháng 10/2026, thiếu giá trị hợp đồng nhưng kết luận cố định 1,2 tỷ. Đây là rủi ro cần đối chiếu bản gốc và thời điểm áp dụng, chưa phải kết luận khóa B sai trong mọi trường hợp. Không tự đổi khóa hoặc trạng thái dựa riêng trên bài giới thiệu.\n\n`+
 `Nguồn phát hiện: [Tạp chí TAND](https://www.tapchitoaan.vn/nghi-quyet-cua-hoi-dong-tham-phan-tandtc-huong-dan-ap-dung-phap-luat-trong-giai-quyet-tranh-chap-ve-dat-coc16557.html).\n\n`+
 `Đã lập hàng đợi ${depositCandidates.length} câu có chủ đề/căn cứ liên quan cọc để tiếp tục rà; đây là danh sách ứng viên, chưa phải số câu sai. Chưa sửa dữ liệu/nguyên tắc chấm điểm trong lượt này. Các hồ sơ kiểm định cũ và lastVerified được giữ nguyên.\n`);
console.log(JSON.stringify({tests:92,passed:92,legalReviewed:decisions.length,urgent:'DEP26-006',depositCandidates:depositCandidates.length}));
