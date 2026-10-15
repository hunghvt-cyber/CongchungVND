// Apply individually authored editorial corrections. Historical legal dossiers stay immutable.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
if(fs.existsSync(path.join(root,'editorial/post-review-repairs-2026-10-15.json'))){
 throw new Error('One-shot repair already applied; preserve its original before/after evidence.');
}
const write=(p,v)=>fs.writeFileSync(path.join(root,p),JSON.stringify(v,null,2)+'\n');
const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(', ')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+': '+canonical(v[k])).join(', ')+'}';
const digest=v=>crypto.createHash('sha256').update(canonical(v)).digest('hex');
const files=fs.readFileSync(path.join(root,'app.js'),'utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));
const batches=new Map(files.map(f=>[f,read('data/'+f)]));
const bank=new Map([...batches].flatMap(([f,qs])=>qs.map(q=>[q.id,{file:f,q}])));
const wording=read('data/application-wording-2026.json'),worded=new Map(wording.questions.map(r=>[r.id,r]));
const fixes=[];
const summaries={
 'IMP-SEP24-019':'Khoản 2 Điều 347 BLDS xác định hiệu lực đối kháng của cầm giữ từ khi bên cầm giữ chiếm giữ tài sản. Dữ kiện đã xác định đủ điều kiện cầm giữ, nên không phải chờ đăng ký hoặc bản án. Cần tách mốc đối kháng này với mốc phát sinh quyền cầm giữ do nghĩa vụ đến hạn mà không được thực hiện đúng tại khoản 1.',
 'CAL26-002':'Khoản 1 Điều 611 và khoản 1 Điều 643 BLDS gắn hiệu lực định đoạt thừa kế với thời điểm mở thừa kế. P còn sống nên H chưa được sang tên chỉ dựa vào di chúc. Việc công chứng và giao bản gốc không thay cho một giao dịch chuyển quyền giữa những người đang sống.',
 'CAL26-005':'Khoản 2 Điều 64 Luật Công chứng yêu cầu có đủ chữ ký số của công chứng viên và tổ chức hành nghề công chứng. Đến 09:20 mới đủ hai chữ ký này, nên đây là mốc hiệu lực trong dữ kiện. Chữ ký của các bên lúc 09:05 và việc gửi tệp lúc 09:30 không thay mốc hoàn tất chứng nhận.',
 'CAL26-006':'Khoản cọc 200 triệu vẫn bảo đảm việc bàn giao dù hợp đồng đã ký. Theo khoản 2 Điều 328 BLDS, bên nhận cọc từ chối thực hiện phải hoàn 200 triệu và trả khoản tương đương 200 triệu, tổng 400 triệu nếu không có thỏa thuận khác. Khoản đã thanh toán thêm 300 triệu không tự thành cọc và nằm ngoài phép tính đang hỏi.',
 'CAL26-011':'Khoản 2 Điều 328 BLDS cho phép thỏa thuận khác về xử lý cọc. Theo điều khoản hợp pháp trong đề, tổng nghĩa vụ là hoàn 200 triệu và trả thêm 100 triệu, bằng 300 triệu. Đã trả 50 triệu thì còn 250 triệu, nhưng đề hỏi tổng phát sinh trước khi trừ. Không cộng tiếp khoản tương đương cọc theo mặc định vào khoản thay thế đã thỏa thuận.',
 'CAL26-015':'Tách 3 tỷ thuộc sở hữu của N khỏi khối chung 6 tỷ, di sản M còn 3 tỷ. Nếu chia theo pháp luật có bốn suất N, P, Q, R, mỗi suất 750 triệu. Theo Điều 644 BLDS, N, P và R được bảo đảm mỗi người hai phần ba suất, tức 500 triệu. Q thành niên có khả năng lao động không thuộc nhóm bắt buộc; H còn được nhận 1,5 tỷ theo di chúc.',
 'CAL26-021':'Giá 2 tỷ phản ánh đúng ý chí khi ký; giảm xuống 1,8 tỷ là thay đổi nghĩa vụ nên phải công chứng sửa đổi theo Điều 53 Luật Công chứng. Lỗi tên đường đã được xác định không ảnh hưởng quyền, nghĩa vụ có thể xử lý theo Điều 52. Hai bên đồng ý không biến thay đổi giá thành lỗi kỹ thuật và không cho sửa cả hai theo cùng một thủ tục.',
 'CAL26-023':'Điều 563 BLDS quy định thời hạn mặc định một năm kể từ ngày xác lập việc ủy quyền khi không có thỏa thuận thời hạn và pháp luật không quy định khác. Hồ sơ xác lập trước rồi công chứng sau, nên không tự tính lại một năm từ ngày công chứng hoặc nhận bản gốc. Việc chưa thu hồi giấy và công việc chưa xong không tự kéo dài thời hạn đã hết.',
 'CAL26-041':'Theo Điều 283 BLDS, B đồng ý để C giao hàng không đồng nghĩa đồng ý chuyển nghĩa vụ từ A sang C. Khi C giao không đúng, A vẫn chịu trách nhiệm thực hiện với B. Việc A trả phí cho C hoặc B biết người giao thay không tự miễn trách nhiệm của A; quan hệ A–C cần được xử lý riêng.',
 'CAL26-047':'Khoản 1 và khoản 3 Điều 615 BLDS giới hạn trách nhiệm của người thừa kế trong phần di sản đã nhận, trừ thỏa thuận khác. Dù phân bổ khoản nợ 900 triệu theo tỷ lệ 2:1 cho ra 600 và 300 triệu, trần của A vẫn là 400 triệu, B là 200 triệu. Không có cam kết trả vượt nên không tự buộc họ bù phần thiếu bằng tài sản riêng.',
 'CAL26-061':'Khoản 1 Điều 51 Luật Công chứng dùng tiêu chí số trang: cả hai hồ sơ đều phải đánh số liên tục qua lời chứng. Khoản 2 dùng tiêu chí số tờ: hồ sơ I có hai tờ nên phải giáp lai giữa các tờ; hồ sơ II in hai mặt của một tờ không thuộc trường hợp giáp lai giữa nhiều tờ. Không đồng nhất trang với tờ giấy.',
 'CAL26-062':'Khoản 2 Điều 48 BLDS yêu cầu lựa chọn trước người giám hộ bằng văn bản có công chứng hoặc chứng thực và khi cần giám hộ phải có sự đồng ý của người được chọn. B không đồng ý nên không thể bị buộc nhận chỉ vì giấy đã công chứng; giấy chọn C lại thiếu hình thức. Kết luận này không loại việc xem xét cơ chế cử hoặc chỉ định theo căn cứ khác.',
 'CAL26-064':'Điều 47 Luật Hôn nhân và gia đình yêu cầu thỏa thuận xác lập chế độ tài sản được lập trước khi kết hôn, bằng văn bản công chứng hoặc chứng thực; chế độ được xác lập từ ngày đăng ký kết hôn. Vì vậy A,B không áp dụng chế độ vợ chồng ngay từ ngày ký. C,D không thể coi văn bản lập sau đăng ký là thỏa thuận xác lập ban đầu đã lập trước hôn nhân.',
 'CAL26-065':'Khoản 1 Điều 42 Luật Công chứng gắn ngoại lệ không nộp lại giấy tờ với việc tổ chức đã khai thác được thông tin tương ứng, không chỉ có tài khoản truy cập. Hồ sơ A đáp ứng điều kiện đối với các giấy đã khai thác và chịu phí theo luật; hồ sơ B chưa đáp ứng. Ngoại lệ đó không tự miễn dự thảo giao dịch hoặc toàn bộ phí.',
 'CAL26-068':'Khoản 2 Điều 56 Luật Công chứng yêu cầu công chứng hợp đồng thế chấp tiếp tại tổ chức đã công chứng lần đầu khi nơi đó vẫn hoạt động. Vì vậy M là nơi thực hiện theo dữ kiện. N cùng tỉnh, có bản gốc và được chủ nợ đồng ý vẫn chưa thay quy tắc riêng này; không áp cơ chế gửi bản gốc của ủy quyền hai nơi sang thế chấp tiếp.',
 'CAL26-069':'Theo Điều 22 BLDS, khi không còn căn cứ tuyên mất năng lực, phải yêu cầu Tòa án hủy quyết định đã tuyên theo cơ chế luật định. Giấy bác sĩ là tài liệu về tình trạng sức khỏe, không tự thay quyết định hủy của Tòa án. Sự đồng ý của người đại diện hoặc ngày ra viện cũng không tự làm quyết định cũ hết hiệu lực.',
 'CAL26-084':'Điều 373 BLDS cho nghĩa vụ được hoàn thành khi bên có nghĩa vụ thực hiện một phần và phần còn lại được bên có quyền miễn. A đã trả 70 triệu và B đã miễn hợp pháp 30 triệu còn lại, nên biên nhận chỉ ghi 70 triệu không duy trì khoản nợ đã được miễn. Không nhầm miễn với tạm hoãn hoặc vô hiệu toàn bộ giao dịch.',
 'CAL26-095':'Theo Điều 611 và Điều 661 BLDS, giới hạn lần đầu ba năm tính từ thời điểm mở thừa kế, không tính lại từ ngày vợ yêu cầu hoặc ngày Tòa quyết định. P chết ngày 12/10/2025 nên mốc trần lần đầu là 12/10/2028. Gia hạn không được cộng sẵn mà phải được Tòa xem xét khi đáp ứng điều kiện riêng của luật.',
 'CAL26-096':'Khoản 5 Điều 59 Luật Công chứng áp dụng thủ tục tại các khoản 2, 3, 4 cả khi chỉ có một người thừa kế. Vẫn phải kiểm tra quyền tài sản của người chết, tư cách người hưởng và hoàn tất niêm yết theo luật. Bộ giấy tờ đầy đủ hoặc việc hiện chưa ghi nhận khiếu nại không thay xác nhận đã hoàn thành niêm yết.'
};
for(const [id,explanation] of Object.entries(summaries)){
 const q=bank.get(id).q,before=structuredClone(q);q.explanation=explanation;
 fixes.push({id,reason:'Bổ sung giải thích tổng bằng dữ kiện, điều kiện và hệ quả cụ thể; giữ giải thích từng phương án và khóa.',before,after:structuredClone(q)});
}
const replacements={
 'IMP-SEP24-031':{index:1,text:'Tháng 10/2026: H đang thuê đất nông nghiệp theo điểm b khoản 1 Điều 172 và đã đến cuối kỳ thuê. H muốn tiếp tục sản xuất, nhưng chưa có quyết định giải quyết đề nghị thuê tiếp. Có thể coi nhu cầu sử dụng đủ để tự gia hạn không; cơ chế xem xét và giới hạn thời gian nào áp dụng?'},
 'IMP-T60-056':{index:1,text:'Tháng 10/2026: P chuẩn bị đầu tư xử lý ô nhiễm để phục hồi một khu đất suy thoái, không mở rộng diện tích và không xin chuyển thành đất ở. Người thẩm định định loại dự án khỏi danh mục khuyến khích chỉ vì thiếu hai yếu tố đó. Chọn cách đánh giá phù hợp với mục tiêu dự án.'},
 'IMP-T60-059':{index:1,text:'Tháng 10/2026: Dự thảo của tỉnh cho cá nhân nhận chuyển quyền từng loại đất nông nghiệp tới 20 lần hạn mức giao tương ứng tại khoản 1, 2, 3 Điều 176. Nhóm thẩm định muốn giữ mức này vì địa phương được quyết định mức cụ thể. Phương án nào nêu đúng giới hạn của quyền quyết định đó?'},
 'FAM26-002':{index:0,text:'Tháng 10/2026: Khi đối chiếu hồ sơ thỏa thuận tài sản vợ chồng, CCV chỉ nhận bản sao chứng thực căn cước và giấy kết hôn, không có bản chính; tổ chức chưa khai thác được thông tin tương ứng từ cơ sở dữ liệu. Giấy kết hôn được xác định là giấy tờ liên quan thuộc điểm d khoản 1 Điều 42. Có thể dùng hai bản sao này thay bản chính như nhau trước khi ký lời chứng không?'}
};
for(const [id,{index,text}] of Object.entries(replacements)){
 const q=bank.get(id).q,before=structuredClone(q),w=worded.get(id),presentationBefore=structuredClone(w.variants);
 // Both paths carry the same reviewed replacement; do not leave a retired stem in the source.
 q.question.variants[index]=text;w.variants[index]=text;
 fixes.push({id,reason:'Thay biến thể bị đưa lại bằng tình huống mới; giữ giả thiết quyết định và khóa.',before,after:structuredClone(q),presentationBefore,presentationAfter:structuredClone(w.variants)});
}
for(const {id} of fixes){const q=bank.get(id).q,w=worded.get(id);if(w)w.sourceSha256=crypto.createHash('sha256').update(JSON.stringify({question:q.question,answers:q.answers,legalBasis:q.legalBasis})).digest('hex');}
for(const [f,qs] of batches)if(qs.some(q=>fixes.some(r=>r.id===q.id)))write('data/'+f,qs);
write('data/application-wording-2026.json',wording);
write('editorial/post-review-repairs-2026-10-15.json',{date:'2026-10-15',scope:'19 giải thích tổng và 4 biến thể đã bị loại. Không đổi khóa, trạng thái, lastVerified hoặc các hồ sơ pháp lý lịch sử.',fixes});

// A transparent version bridge, not legal recertification. Every changed record
// must match an exact reviewed post-state before historical tests can use its predecessor.
const baseline='bb65b0ae3bb54b23ce6367c72d43f3ca5d320a3d';
const predecessor=new Map(files.flatMap(f=>JSON.parse(cp.execFileSync('git',['show',baseline+':data/'+f],{cwd:root,maxBuffer:10*1024*1024,encoding:'utf8'}))).map(q=>[q.id,q]));
const rows=[];
for(const [id,{file,q}] of bank){const before=predecessor.get(id);if(digest(q)!==digest(before))rows.push({id,file,beforeHash:digest(before),afterHash:digest(q),preservedKey:before.answers.filter(a=>a.correct).map(a=>a.id).sort(),basisChanged:JSON.stringify(before.legalBasis)!==JSON.stringify(q.legalBasis),reviewReference:fixes.some(r=>r.id===id)?'editorial/post-review-repairs-2026-10-15.json':'reports/editorial-review-437-2026-10-15.json'});}
write('editorial/editorial-version-bridge-2026-10-15.json',{date:'2026-10-15',baselineCommit:baseline,notLegalRecertification:true,historicalDossiersUnchanged:true,hashAlgorithm:'SHA-256 of sorted-key JSON, same canonical format as legal-review-register',basisAmendments:{'CAL26-027':'Bổ sung khoản 4 Điều 50; excerpt CC:50 trong hồ sơ 12/10 đã chứa đầy đủ khoản 1–4.','HARD26-041':'Bổ sung DS:296, đã đối chiếu văn bản chính thức; chứng cứ bổ sung ở editorial/legal-evidence-supplement-2026-10-15.json.'},rows});
console.log(JSON.stringify({contentFixes:fixes.length,versionBridgeRows:rows.length}));
