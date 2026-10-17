const fs=require('node:fs'),path=require('node:path'),{createHash}=require('node:crypto');
const {root,effectiveBank}=require('./lib/effective-bank.cjs');
const authored=require('../editorial/stem-fluency-2026-10-18.cjs');
const bank=effectiveBank({polish:true,answers:true}),sha=q=>createHash('sha256').update(JSON.stringify(q)).digest('hex');
const numeric=s=>(s.match(/\d+(?:[.,:/]\d+)*/g)||[]);
const actors=s=>[...new Set(s.match(/(?<![\p{L}\p{N}])[A-Z][0-9]?(?![\p{L}\p{N}])/gu)||[])].sort();
const abbreviations={CCV:'công chứng viên',VPCC:'Văn phòng công chứng',DNTN:'doanh nghiệp tư nhân',BĐS:'bất động sản',BLDS:'Bộ luật Dân sự',HNGĐ:'Hôn nhân và gia đình',UBND:'Ủy ban nhân dân',HĐTV:'Hội đồng thành viên',HĐQT:'Hội đồng quản trị',ĐHĐCĐ:'Đại hội đồng cổ đông'};
const rules=[
 ['mốc_thời_gian',/^Tháng (\d+\/\d+): /u,'Tháng $1, '],
 ['mốc_hiệu_lực',/^Từ (\d+\/\d+\/\d+): /u,'Từ ngày $1, '],
 ['mốc_hiệu_lực',/^Từ (\d+\/\d+\/\d+), /u,'Từ ngày $1, '],
 ['mốc_áp_dụng',/^Áp dụng pháp luật tại tháng (\d+\/\d+)\. /u,'Áp dụng pháp luật trong tháng $1. '],
 ['đủ_từ',/không nợ(?=[,.; ]|$)/gu,'không có nợ'],
 ['đủ_từ',/không di chúc/gu,'không để lại di chúc'],
 ['đủ_từ',/không tài sản khác/gu,'không có tài sản khác'],
 ['đủ_từ',/không khoản ưu tiên khác/gu,'không có khoản ưu tiên khác'],
 ['đủ_từ',/không luật riêng/gu,'không có quy định riêng của pháp luật'],
 ['đủ_từ',/không người bắt buộc/gu,'không có người được hưởng phần di sản bắt buộc'],
 ['đủ_từ',/không người thay thế/gu,'không có người thay thế'],
 ['đủ_từ',/không người thứ hai/gu,'không có người thứ hai'],
 ['đủ_từ',/không người khác/gu,'không có người khác'],
 ['đủ_từ',/không vợ hợp pháp/gu,'không có vợ hợp pháp'],
 ['đủ_từ',/không nghĩa vụ khác/gu,'không có nghĩa vụ khác'],
 ['đủ_từ',/không căn cứ /gu,'không có căn cứ '],
 ['đủ_từ',/không phần bắt buộc/gu,'không có phần di sản bắt buộc'],
 ['đủ_từ',/không miễn nợ/gu,'không có việc miễn nợ'],
 ['đủ_từ',/không nghĩa vụ bồi thường/gu,'không có nghĩa vụ bồi thường'],
 ['đủ_từ',/không thỏa thuận khác/gu,'không có thỏa thuận khác'],
 ['đủ_từ',/không thỏa thuận phạm vi/gu,'không có thỏa thuận về phạm vi'],
 ['đủ_từ',/không thỏa thuận phương thức/gu,'không có thỏa thuận về phương thức'],
 ['đủ_từ',/nhà riêng ([A-Z][0-9]?)(?![\p{L}\p{N}])/gu,'nhà riêng của $1'],
 ['đủ_từ',/phần quyền ([A-Z][0-9]?)(?![\p{L}\p{N}])/gu,'phần quyền của $1'],
 ['đủ_từ',/ý chí ([A-Z][0-9]?)(?![\p{L}\p{N}])/gu,'ý chí của $1'],
 ['đủ_từ',/(?<!thừa kế )hàng thứ nhất/gu,'hàng thừa kế thứ nhất'],
 ['đủ_từ',/trong hôn nhân/gu,'trong thời kỳ hôn nhân'],
 ['đủ_từ',/giấy chứng nhận chỉ tên /gu,'giấy chứng nhận chỉ ghi tên '],
 ['đủ_từ',/giấy chỉ tên /gu,'giấy tờ chỉ ghi tên '],
 ['đủ_từ',/nợ riêng ([A-Z][0-9]?)(?![\p{L}\p{N}])/gu,'nợ riêng của $1'],
 ['thuật_ngữ',/TT06\/2025(?!\/TT-BTP)/gu,'Thông tư 06/2025/TT-BTP'],
 ['thuật_ngữ',/NĐ21\/2021(?!\/NĐ-CP)/gu,'Nghị định 21/2021/NĐ-CP'],
 ['dấu_câu',/,([A-Z][0-9]?)(?=[,;. ]|$)/gu,', $1'],
 ['tách_câu',/; ([A-Z][0-9]? (?:muốn|đề nghị|cho rằng|yêu cầu|đã|đang|chưa|không) )/gu,'. $1'],
];
const endings=new Map([
 ['Phương án đúng?','Phương án nào sau đây đúng?'],['Nhận định đúng?','Nhận định nào sau đây đúng?'],
 ['Cách xử lý đúng?','Cách xử lý nào phù hợp với tình huống này?'],['Xử lý đúng?','Tình huống này cần được xử lý như thế nào?'],
 ['Kết luận đúng?','Kết luận nào sau đây đúng?'],['Hướng xử lý đúng?','Hướng xử lý nào phù hợp?'],
 ['Phân biệt đúng?','Nhận định nào phân biệt đúng các trường hợp trên?'],['Đánh giá đúng?','Nhận định nào đánh giá đúng tình huống này?'],
 ['Hướng đúng?','Hướng xử lý nào phù hợp?'],['Cần xử lý?','Cần xử lý tình huống này như thế nào?'],
 ['Cần bổ sung?','Cần bổ sung nội dung nào?'],['Phân chia đúng?','Di sản được phân chia như thế nào?'],
 ['Chia thế nào?','Di sản được chia như thế nào?'],['Tư vấn đúng?','Nội dung tư vấn nào phù hợp?'],
 ['Kết quả đúng?','Kết quả nào sau đây đúng?'],['Phân bổ đúng?','Tài sản được phân bổ như thế nào?'],
 ['Phương án chia đúng?','Phương án phân chia nào đúng?'],['Ai nhận gì?','Mỗi người được nhận phần tài sản nào?'],
 ['Kết luận phù hợp?','Kết luận nào phù hợp với tình huống trên?'],['Cách xử lý phù hợp?','Cách xử lý nào phù hợp với tình huống trên?'],
 ['Xử lý phù hợp?','Cách xử lý nào phù hợp với tình huống trên?'],['Xử lý giới hạn đúng?','Giới hạn này cần được áp dụng như thế nào?'],
 ['Phương án đúng về chủ thể và điều kiện?','Phương án nào xác định đúng chủ thể và điều kiện trong trường hợp này?'],
 ['Phương án xử lý đồng thời đúng?','Phương án nào xử lý đúng các vấn đề nêu trên?'],
 ['Công chứng viên xử lý?','Công chứng viên cần xử lý yêu cầu này như thế nào?'],
 ['Phân biệt nào đúng?','Nhận định nào phân biệt đúng các trường hợp trên?'],
 ['Chọn đánh giá đúng.','Nhận định nào đánh giá đúng tình huống trên?'],
 ['Cách tính đúng?','Cách tính nào sau đây đúng?'],['Lựa chọn đúng?','Phương án nào sau đây đúng?'],
 ['Lựa chọn phù hợp?','Phương án nào phù hợp với tình huống này?'],['Hướng xử lý luật định?','Hướng xử lý nào phù hợp với quy định pháp luật?'],
 ['Cách đánh giá phù hợp?','Nhận định nào đánh giá đúng tình huống này?'],['Cách phân loại phù hợp?','Cách phân loại nào phù hợp?'],
 ['Thiếu gì?','Hồ sơ này còn thiếu điều kiện nào?'],['Điều còn phải xét?','Cần xem xét thêm điều kiện nào?'],
 ['Phân biệt hai phương án?','Hai phương án trên được phân biệt như thế nào?'],['Hướng kiểm tra đúng?','Cần kiểm tra hồ sơ theo hướng nào?'],
 ['Áp dụng đúng là gì?','Quy định này được áp dụng như thế nào trong tình huống trên?'],['Bước xử lý phù hợp?','Bước xử lý tiếp theo nào phù hợp?'],
 ['Cách phân biệt trách nhiệm đúng?','Trách nhiệm của các chủ thể được phân biệt như thế nào?'],
 ['Cách xử lý việc hướng dẫn đúng?','Việc hướng dẫn tập sự cần được xử lý như thế nào?'],
 ['Cách sửa đúng?','Cần sửa nội dung trên như thế nào?'],['Xử lý di chúc và phí lưu giữ?','Di chúc và phí lưu giữ cần được xử lý như thế nào?'],
 ['Phân biệt thẩm quyền đúng?','Thẩm quyền giải quyết các việc trên được xác định như thế nào?'],
 ['Phân biệt nghĩa vụ đúng?','Nghĩa vụ của các chủ thể được phân biệt như thế nào?'],
 ['Hướng đánh giá đúng?','Nhận định nào đánh giá đúng tình huống trên?'],['Cách giải quyết đúng?','Cách giải quyết nào phù hợp?'],
 ['Phân loại và xử lý?','Giao dịch được phân loại và xử lý như thế nào?'],['Đánh giá pháp lý?','Nhận định nào đánh giá đúng tình huống trên?'],
 ['Hiệu lực việc ủy quyền?','Việc ủy quyền có hiệu lực như thế nào?'],['Mốc, quyền đúng?','Thời điểm và quyền liên quan được xác định như thế nào?'],
 ['Phương án xử lý hai việc đúng?','Phương án nào xử lý đúng cả hai việc trên?'],
 ['Chọn kết luận.','Nhận định nào sau đây đúng?'],['Chọn kết luận đúng?','Nhận định nào sau đây đúng?'],
 ['Chọn kết quả đúng.','Kết quả nào sau đây đúng?'],['Chọn nhận xét đúng.','Nhận định nào sau đây đúng?'],
 ['Chọn cách chia đúng.','Di sản được chia như thế nào?']
]);
function normalize(s,q,changes){
 const replace=(name,re,to)=>{const next=s.replace(re,to);if(next!==s){changes.push(name);s=next;}};
 replace('khoảng_trắng',/\s+/gu,' ');s=s.trim();
 for(const [name,re,to]of rules)replace(name,re,to);
 for(const [short,long]of Object.entries(abbreviations))replace('viết_đầy_đủ',new RegExp('(?<![\\p{L}\\p{N}_])'+short+'(?![\\p{L}\\p{N}_])','gu'),long);
 // Lowercase ordinary role/noun words after the date comma, preserving names,
 // named institutions and document titles (Nam, Hân, Tòa án, Bộ luật, ...).
 replace('đầu_mệnh_đề',/^((?:Tháng \d+\/\d+|Từ ngày \d+\/\d+\/\d+), )(Một|Hai|Các|Người|Bên|Nhà|Hợp|Giao|Sau|Khi|Với|Nhân|Khách|Việc|Chỉ|Nếu|Không|Bất|Yêu|Tài|Trong|Chồng|Máy|Lợi|Thỏa|Ngày|Chế|Đất|Quyền|Cha|Ngân|Doanh|Đối|Chủ|Tuân|Những|Ông|Gia|Con|Chưa|Hàng|Toàn|Trẻ|Nghĩa|Bảng|Bốn|Khai|Đâu|Chi|Thành|Thời|Cộng|Tiền|Biên|Đặt|Cọc|Bản|Chia|Quy|Chọn|Giám|Tính|Xác|Cháu|Cần|Bạn|Phương|Thủ|Pháp|Giả|Môi|Lỗi|Kho|Khối|Mốc|Tên|Hình|Quyết|Căn|Kết|Ngoài|Phiên|Xét|Nơi|Thẩm|Phân|Tất|Cùng)(?= )/u,(_,prefix,word)=>prefix+word.toLocaleLowerCase('vi'));
 replace('đầu_mệnh_đề',/^((?:Tháng \d+\/\d+|Từ ngày \d+\/\d+\/\d+), )(Công chứng viên|Luật sư|Ứng viên|Tỉnh|Lệnh|Ngoại lệ|Đơn|Danh mục|Khoản|Điểm|Phạm vi)(?= )/u,(_,prefix,word)=>prefix+word.charAt(0).toLocaleLowerCase('vi')+word.slice(1));
 replace('đầu_mệnh_đề',/^((?:Tháng \d+\/\d+|Từ ngày \d+\/\d+\/\d+), )(Xã|Cá nhân|Dự thảo|Di chúc|Hồ sơ)(?= )/u,(_,prefix,word)=>prefix+word.charAt(0).toLocaleLowerCase('vi')+word.slice(1));
 replace('đầu_mệnh_đề',/^((?:Tháng \d+\/\d+|Từ ngày \d+\/\d+\/\d+), )(Giấy|Dữ|Theo|Hệ|Đề|Cơ|Tổ|Từ|Nhầm|Vợ|Xe|Bà|Hộ|Đã|Kế|Mẹ|Di|Áp|Tư|Cổ|Ai|Phó|Sự|Ba|So|Đo)(?= )/u,(_,prefix,word)=>prefix+word.toLocaleLowerCase('vi'));
 replace('đầu_mệnh_đề',/^((?:Tháng \d+\/\d+|Từ ngày \d+\/\d+\/\d+), )(Văn bản|Thông tin|Điều khoản|Ủy quyền)(?= )/u,(_,prefix,word)=>prefix+word.charAt(0).toLocaleLowerCase('vi')+word.slice(1));
 // Expanded abbreviations may also start a sentence. Repair observed lowercase
 // sentence starts without treating decimal points or document numbers as stops.
 replace('đầu_câu',/([.!?] )(công chứng viên|có thể|chọn|di sản|yêu cầu|kết luận|cần thực hiện|ai có thẩm quyền)(?= )/gu,(_,stop,word)=>stop+word.charAt(0).toLocaleUpperCase('vi')+word.slice(1));
 replace('đủ_từ',/nhà riêng ([A-Z][0-9]?)(?![\p{L}\p{N}])/gu,'nhà riêng của $1');
 // Instructions that repeat an immediately preceding question carry no facts.
 replace('bỏ_lệnh_lặp',/\? Chọn (?:nhận định|kết luận|phương án) (?:đúng|phù hợp)\.$/u,'?');
 for(const [old,next]of endings){
  if(s.endsWith(' '+old)){replace('câu_hỏi_đủ_thành_phần',new RegExp(old.replace(/[?]/g,'\\?')+'$','u'),next);break;}
 }
 const plural=q.type==='multiple';
 replace('câu_hỏi_chọn_đáp_án',/Chọn (?:các |những |tất cả )?(?:nhận định|kết luận) (?:đúng|phù hợp) về ([^.?]+)\.$/u,(_,subject)=>(plural?'Những nhận định nào sau đây đúng về ':'Nhận định nào sau đây đúng về ')+subject+'?');
 replace('câu_hỏi_chọn_đáp_án',/(?:Chọn (?:các |những |tất cả )?(?:nhận định|kết luận|phương án) đúng)\.$/u,plural?'Những nhận định nào sau đây đúng?':'Nhận định nào sau đây đúng?');
 replace('câu_hỏi_chọn_đáp_án',/Chọn (?:nhận định|kết luận|phương án) phù hợp\.$/u,plural?'Những nhận định nào sau đây phù hợp?':'Nhận định nào sau đây phù hợp?');
 replace('câu_hỏi_đủ_thành_phần',/nhận định đúng\?$/u,'nhận định nào đúng?');
 replace('câu_hỏi_đủ_thành_phần',/(?:cách )?xử lý đúng\?$/u,'cách xử lý nào phù hợp?');
 if(plural){
  replace('lệnh_chọn_nhiều',/Nhận định nào sau đây đúng\?$/u,'Những nhận định nào sau đây đúng?');
  replace('lệnh_chọn_nhiều',/Kết luận nào sau đây đúng\?$/u,'Những kết luận nào sau đây đúng?');
  replace('lệnh_chọn_nhiều',/Phương án nào sau đây đúng\?$/u,'Những phương án nào sau đây đúng?');
 }
 return s.charAt(0).toLocaleUpperCase('vi')+s.slice(1);
}
const revisions=[],decisions=[],used=new Set();
for(const q of bank){
 if(!['active','verified'].includes(q.status))continue;
 const variants=q.question.variants.slice(),records=variants.map((before,i)=>({index:i,before,operations:[]}));
 const pairs=authored[q.id]||[];
 for(const [from,to]of pairs){
  let count=0;for(let i=0;i<variants.length;i++){if(variants[i].includes(from)){variants[i]=variants[i].replaceAll(from,to);records[i].operations.push('authored_clause_repair');count++;}}
  if(!count)throw Error('Missing authored phrase: '+q.id+' '+from);used.add(q.id);
 }
 for(let i=0;i<variants.length;i++){
  variants[i]=normalize(variants[i],q,records[i].operations);records[i].after=variants[i];
  if(JSON.stringify(numeric(records[i].before))!==JSON.stringify(numeric(variants[i])))throw Error('Changed numeric/date sequence '+q.id+'/'+i);
  if(JSON.stringify(actors(records[i].before))!==JSON.stringify(actors(variants[i])))throw Error('Changed actor labels '+q.id+'/'+i);
  if(!variants[i].trim())throw Error('Empty variant '+q.id);
 }
 if(new Set(variants).size!==variants.length)throw Error('Collapsed variants '+q.id);
 const after={...q,question:{...q.question,variants}},beforeSha256=sha(q),afterSha256=sha(after);
 const changed=records.filter(r=>r.before!==r.after);
 if(changed.length)revisions.push({id:q.id,beforeSha256,afterSha256,variants});
 decisions.push({id:q.id,type:q.type||'single',answerKey:q.answers.filter(a=>a.correct).map(a=>a.id),
  beforeSha256,afterSha256,decision:used.has(q.id)?'authored_clause_repair':changed.length?'controlled_language_edit':'retained',
  protectedMetadataSha256:sha({...q,question:{...q.question,variants:[]}}),variants:records.map(r=>({...r,operations:[...new Set(r.operations)]}))});
}
for(const id of Object.keys(authored))if(!used.has(id))throw Error('Unknown authored question '+id);
const summary={activeQuestions:decisions.length,variants:decisions.reduce((n,d)=>n+d.variants.length,0),changedQuestions:revisions.length,
 changedVariants:decisions.reduce((n,d)=>n+d.variants.filter(v=>v.before!==v.after).length,0),authoredQuestions:used.size,
 authoredVariants:decisions.reduce((n,d)=>n+d.variants.filter(v=>v.operations.includes('authored_clause_repair')).length,0),
 retainedQuestions:decisions.length-revisions.length};
const write=(p,x)=>fs.writeFileSync(path.join(root,p),JSON.stringify(x,null,2)+'\n');
write('data/stem-fluency-2026.json',{version:1,date:'2026-10-18',scope:'question-variants-only',questions:revisions});
write('reports/stem-fluency-2026-10-18.json',{version:1,date:'2026-10-18',baselineCommit:'6da09f6eb9ef3cec4c731a2493487dd735e5261d',summary,
 reviewMethod:'Targeted authored clause repairs plus controlled grammar/abbreviation/prompt rules across every active variant. This is not a claim that all variants were independently rewritten by hand.',
 guards:['Exact variant count and distinctness','Exact numeric/date sequence in each variant','Same Latin actor-label set in each variant','All answers, truth values, explanation, legalBasis, source and lastVerified unchanged','Full record before/after SHA-256'],
 semanticLimit:'These guards detect data drift, not every possible semantic error. Keys are retained, not newly legally certified. Existing legal review queue, including DEP26-006, remains open.',decisions});
console.log(JSON.stringify(summary,null,2));
