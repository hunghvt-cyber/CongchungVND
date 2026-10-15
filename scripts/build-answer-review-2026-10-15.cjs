// Compile authored option edits and a complete language-review register.
// This is an editorial build, not an application/scoring test run.
const fs=require('node:fs'),path=require('node:path'),{createHash}=require('node:crypto');
const {root,effectiveBank}=require('./lib/effective-bank.cjs');
const baseline=effectiveBank({polish:true});
const drafts=['answer-improvements-2026-10-15.cjs','answer-improvements-single-2026-10-15.cjs'];
const edits={};
for(const file of drafts)for(const [id,options] of Object.entries(require(path.join(root,'editorial',file)).edits)){
 for(const [key,edit] of Object.entries(options)){
  if(edits[id]?.[key])throw Error('Duplicate authored edit: '+id+'/'+key);
  (edits[id]??={})[key]=edit;
 }
}
const abbreviations={CCV:'công chứng viên',HĐTV:'Hội đồng thành viên',HĐQT:'Hội đồng quản trị',ĐHĐCĐ:'Đại hội đồng cổ đông',DNTN:'doanh nghiệp tư nhân',BĐS:'bất động sản',BLDS:'Bộ luật Dân sự',UBND:'Ủy ban nhân dân',VPCC:'Văn phòng công chứng'};
function wording(text){
 let out=text.trim().replace(/\s+/g,' ');
 // Unicode boundaries avoid matching an abbreviation inside a longer word.
 for(const [short,long] of Object.entries(abbreviations))out=out.replace(new RegExp('(?<![\\p{L}\\p{N}_])'+short+'(?![\\p{L}\\p{N}_])','gu'),long);
 out=out.replace(/(\d)(triệu|tỷ|tuổi|ngày|tháng|năm)(?!\p{L})/gu,'$1 $2');
 if(out && !/[.!?…:;]$/.test(out))out+='.';
 return out.charAt(0).toLocaleUpperCase('vi')+out.slice(1);
}
const sha=q=>createHash('sha256').update(JSON.stringify(q)).digest('hex');
const rows=[],decisions=[];
const known=new Set();
for(const q of baseline){
 if(!['active','verified'].includes(q.status))continue;
 known.add(q.id);
 const after=structuredClone(q),authored=edits[q.id]||{},changes=[];
 if(q.answers.length!==4)throw Error('Expected four options: '+q.id);
 for(const [key,edit] of Object.entries(authored)){
  if(!q.answers.some(a=>a.id===key))throw Error('Unknown option: '+q.id+'/'+key);
  if(typeof edit.text!=='string'||!edit.text.trim()||
     (edit.explanation!==null&&(typeof edit.explanation!=='string'||!edit.explanation.trim())))throw Error('Incomplete authored edit: '+q.id+'/'+key);
 }
 for(let i=0;i<q.answers.length;i++){
  const old=q.answers[i],a=after.answers[i],edit=authored[a.id];
  a.text=wording(edit?edit.text:old.text);
  if(edit?.explanation)a.explanation=edit.explanation;
  if(JSON.stringify(a)!==JSON.stringify(old))changes.push({id:a.id,kind:edit?'authored_revision':'wording_only',beforeText:old.text,afterText:a.text,
   ...(edit?{rationale:edit.explanation||'Cân đối các lựa chọn số học; giữ nguyên giá trị và giải thích đã có.'}:{rationale:'Chuẩn hóa khoảng trắng, thuật ngữ viết tắt, chữ đầu câu hoặc dấu kết thúc.'})});
  if(JSON.stringify(Object.fromEntries(Object.entries(a).filter(([k])=>!['text','explanation'].includes(k))))!==JSON.stringify(Object.fromEntries(Object.entries(old).filter(([k])=>!['text','explanation'].includes(k)))))throw Error('Protected answer metadata: '+q.id);
 }
 if(new Set(after.answers.map(a=>a.text.toLocaleLowerCase('vi'))).size!==4)throw Error('Duplicate option text: '+q.id);
 const {answers:oldAnswers,...oldMetadata}=q,{answers:newAnswers,...newMetadata}=after;
 if(JSON.stringify(oldMetadata)!==JSON.stringify(newMetadata))throw Error('Protected question metadata: '+q.id);
 const beforeSha256=sha(q),afterSha256=sha(after);
 const kind=changes.some(c=>c.kind==='authored_revision')?'authored_revision':changes.length?'wording_only':'retained';
 if(changes.length)rows.push({id:q.id,beforeSha256,afterSha256,answers:after.answers});
 decisions.push({id:q.id,type:q.type||'single',optionCount:q.answers.length,decision:kind,beforeSha256,afterSha256,changes});
}
for(const id of Object.keys(edits))if(!known.has(id))throw Error('Unknown/ineligible authored ID: '+id);
const count=kind=>decisions.filter(d=>d.decision===kind).length;
const optionCount=kind=>decisions.reduce((n,d)=>n+d.changes.filter(c=>c.kind===kind).length,0);
const summary={reviewedQuestions:decisions.length,reviewedOptions:decisions.reduce((n,d)=>n+d.optionCount,0),
 singleQuestions:decisions.filter(d=>d.type==='single').length,multipleQuestions:decisions.filter(d=>d.type==='multiple').length,
 changedQuestions:rows.length,authoredRevisionQuestions:count('authored_revision'),wordingOnlyQuestions:count('wording_only'),retainedQuestions:count('retained'),
 changedOptions:optionCount('authored_revision')+optionCount('wording_only'),authoredRevisionOptions:optionCount('authored_revision'),wordingOnlyOptions:optionCount('wording_only')};
const profile={version:1,date:'2026-10-15',scope:'answer-text-and-option-feedback-only',questions:rows};
const report={version:1,date:'2026-10-15',baselineCommit:'e5c60863cf8a10633675420728d5417820dda1fa',baselineTree:'25fe7dafb8b23442d0ee13b238e432cf96454ced',
 scope:'Language and distractor review of all active options; not a new legal certification of every stem.',summary,
 protectedFields:['question','answerKey','answer IDs/order/truth values','legalBasis','status','source','lastVerified','all remaining question metadata'],
 archivedQuestionsUntouched:baseline.length-decisions.length,testsDeferred:true,
 validation:'Editorial compilation: identifiers, unique option text, immutable question metadata and truth values, full-record SHA-256. No test suite, browser check, scoring replay or similarity audit rerun.',
 difficulty:'Estimated editorial improvement only; no empirical recalibration claimed.',decisions};
const write=(p,x)=>fs.writeFileSync(path.join(root,p),JSON.stringify(x,null,2)+'\n');
write('data/answer-review-2026.json',profile);write('reports/answer-review-2026-10-15.json',report);
fs.writeFileSync(path.join(root,'reports/answer-review-2026-10-15.md'),`# Rà toàn bộ phương án trả lời — 15/10/2026\n\n`+
 `Đã đọc ${summary.reviewedOptions} phương án của ${summary.reviewedQuestions} câu đang dùng (${summary.singleQuestions} câu một đáp án, ${summary.multipleQuestions} câu nhiều đáp án).\n\n`+
 `- Viết lại có chủ đích: ${summary.authoredRevisionOptions} phương án thuộc ${summary.authoredRevisionQuestions} câu.\n`+
 `- Chỉ chuẩn hóa câu chữ: ${summary.wordingOnlyOptions} phương án; ${summary.wordingOnlyQuestions} câu không có sửa nội dung phương án.\n`+
 `- Tổng cộng thay đổi ${summary.changedOptions} phương án trong ${summary.changedQuestions} câu; giữ nguyên ${summary.retainedQuestions} câu đã đạt yêu cầu.\n`+
 `- Giữ nguyên câu dẫn, khóa, thứ tự/mã phương án, căn cứ, trạng thái và dữ kiện quản lý; không sửa ${report.archivedQuestionsUntouched} câu lưu để rà soát.\n\n`+
 `Nhiễu được sửa theo ngộ nhận cụ thể; câu nhiều đáp án giảm ghép nhiều ý; bốn câu số học bỏ lời giải trong lựa chọn và giữ giải thích sau trả lời. Chuẩn hóa dấu câu/viết tắt được thống kê riêng, không coi là tăng độ khó. Hồ sơ JSON ghi quyết định cho từng câu và văn bản trước/sau của từng phương án đổi.\n\n`+
 `Chưa chạy lại kiểm thử, trình duyệt, chấm điểm mô phỏng hay kiểm toán tương đồng theo yêu cầu. Chỉ biên dịch dữ liệu và kiểm tra tính toàn vẹn khi tạo bản biên tập. Chưa đo lại độ khó bằng kết quả người làm. Đây là rà ngôn ngữ/phương án, không phải chứng nhận pháp lý mới cho toàn bộ câu dẫn.\n`);
console.log(JSON.stringify(summary,null,2));
