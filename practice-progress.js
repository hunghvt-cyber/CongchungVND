/* One immutable receipt per graded question per practice session. */
(() => {
  const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const memory=new Map(),sending=new Map();
  let requestToken=0;
  const stored=()=>{try{const rows=JSON.parse(localStorage.getItem('practiceAnswerQueue')||'[]');return Array.isArray(rows)?rows:[];}catch{return [];}};
  const pending=()=>[...new Map([...stored(),...memory.values()].map(r=>[r.id,r])).values()];
  function queue(row){memory.set(row.id,row);try{localStorage.setItem('practiceAnswerQueue',JSON.stringify(pending()));return true;}catch{return false;}}
  const request=(...args)=>window.ExamProgress.request(...args);
  async function deliver(row){
    if(sending.has(row.id))return sending.get(row.id);
    const task=(async()=>{
      await request('practice_answers',row.learner_key,{method:'POST',headers:{Prefer:'return=minimal'},body:JSON.stringify(row)});
      memory.delete(row.id);
      try{localStorage.setItem('practiceAnswerQueue',JSON.stringify(stored().filter(r=>r.id!==row.id)));}catch{}
    })();
    sending.set(row.id,task);try{await task;}finally{sending.delete(row.id);}
  }
  async function recordAnswer(state,q){
    if(state.mode!=='practice'||!state.learnerName||!/^0\d{9,10}$/.test(state.learnerKey||'')||!Object.hasOwn(state.results,q.id))return;
    state.practiceReceipts??={};
    if(state.practiceReceipts[q.id])return;
    const row={id:crypto.randomUUID(),session_id:state.attemptId,learner_key:state.learnerKey,learner_name:state.learnerName,
      question_id:q.id,part:q.part,topic:q.topic,is_correct:!!state.results[q.id],graded_at:new Date().toISOString(),
      answer:JSON.parse(JSON.stringify({variant:q.variant,answers:q.answers,selected:state.answers[q.id]||[],correct_ids:q.answers.filter(a=>a.correct).map(a=>a.id),explanation:q.explanation,legal_basis:q.legalBasis}))};
    state.practiceReceipts[q.id]=row.id;
    const backedUp=queue(row),status=document.querySelector('#practiceSaveStatus');
    if(status){status.dataset.receipt=row.id;status.textContent='Đang lưu câu vừa ôn…';}
    try{await deliver(row);if(status?.dataset.receipt===row.id)status.textContent='Đã lưu câu ôn tập vào thống kê riêng.';}
    catch{if(status?.dataset.receipt===row.id)status.textContent=backedUp?'Chưa gửi được; câu đã giữ trên thiết bị. Dùng Gửi kết quả chưa lưu khi có mạng.':'Chưa lưu được trên mạng hoặc thiết bị. Đừng đóng trang; hãy bấm Gửi kết quả chưa lưu để thử lại.';}
  }
  function summarize(rows){
    const unique=[...new Map(rows.map(r=>[r.id,r])).values()].sort((a,b)=>a.graded_at.localeCompare(b.graded_at)||a.id.localeCompare(b.id));
    const topics=new Map();
    for(const r of unique){
      const key=JSON.stringify([r.part,r.topic]),t=topics.get(key)||{part:r.part,topic:r.topic,total:0,wrong:0,ids:new Set(),questions:new Set()};
      t.total++;t.questions.add(r.question_id);if(!r.is_correct){t.wrong++;t.ids.add(r.question_id);}topics.set(key,t);
    }
    return {rows:unique,total:unique.length,correct:unique.filter(r=>r.is_correct).length,uniqueQuestions:new Set(unique.map(r=>r.question_id)).size,
      topics:[...topics.values()].sort((a,b)=>b.wrong-a.wrong||b.wrong/b.total-a.wrong/a.total||a.topic.localeCompare(b.topic,'vi'))};
  }
  function topicsMarkup(s,buttons=false){
    return s.topics.map((t,i)=>`<div class="weak-topic"><strong>Bài ${t.part} · ${esc(t.topic)}</strong><p>${t.total-t.wrong} đúng · ${t.wrong} sai / ${t.total} lượt đã chấm · Tỷ lệ sai ${Math.round(t.wrong/t.total*100)}%.</p><p>${t.questions.size} câu khác nhau${t.questions.size<5?' · Mẫu còn ít, chưa đủ để kết luận đây là điểm yếu.':''}.</p>${buttons&&t.wrong?`<button class="secondary-button practice-strengthen" data-index="${i}">Ôn lại các câu từng sai</button>`:''}</div>`).join('');
  }
  function sessionMarkup(state){
    const rows=state.questions.filter(q=>Object.hasOwn(state.results,q.id)).map(q=>({id:q.id,graded_at:'',question_id:q.id,part:q.part,topic:q.topic,is_correct:state.results[q.id]}));
    return `<h3>Nội dung cần củng cố trong lượt ôn này</h3>${topicsMarkup(summarize(rows))}<p class="name-note">Chỉ tính câu đã chấm. Ôn lại là lượt mới; xem lại đáp án không cộng lượt. Không tính vào điểm thi hoặc xếp hạng.</p><button id="viewPracticeProgress" class="secondary-button">Xem thống kê ôn tập của tôi</button>`;
  }
  function bindResult(state){
    const key=state.learnerKey;
    const button=document.querySelector('#viewPracticeProgress');if(!button)return;
    button.onclick=()=>{document.querySelector('#progressPhone').value=key;document.querySelector('#progressMode').value='practice';window.ExamProgress.loadHistory(key,'practice');document.querySelector('#learningProgress').scrollIntoView({behavior:'smooth'});};
  }
  async function loadHistory(phone,startPractice,isCurrent=()=>true){
    const token=++requestToken,target=document.querySelector('#progressContent');
    let key;try{key=window.ExamProgress.normalizePhone(phone);}catch(e){target.textContent=e.message;return;}
    target.textContent='Đang tải thống kê ôn tập…';
    const rows=[];let offline=false;
    try{for(let offset=0;;offset+=100){const page=await request(`practice_answers?learner_key=eq.${encodeURIComponent(key)}&order=graded_at.asc,id.asc&limit=100&offset=${offset}`,key);if(token!==requestToken||!isCurrent())return;if(!Array.isArray(page))throw Error('Invalid history');rows.push(...page);if(page.length<100)break;}}catch{offline=true;}
    if(token!==requestToken||!isCurrent())return;
    const queued=pending().filter(r=>r.learner_key===key),s=summarize([...rows,...queued]);
    const notice=offline?'<p role="status">Chưa tải đủ lịch sử từ hệ thống; chỉ hiển thị phần đã tải và câu chờ gửi trên thiết bị. Thống kê chưa đầy đủ.</p>':queued.length?`<p role="status">Có ${queued.length} câu chờ gửi được tạm tính từ thiết bị này; chuyển thiết bị cần gửi thành công trước.</p>`:'';
    target.innerHTML=`<h3>Thống kê ôn tập</h3>${notice}<p class="name-note">Không cộng vào điểm thi thử hoặc bảng xếp hạng. Tổng hợp mọi lượt ôn đã lưu; ưu tiên chủ đề có nhiều lượt sai, kèm tỷ lệ và cỡ mẫu.</p>${s.total?`<div class="progress-stats"><p><strong>${s.total}</strong> lượt câu đã chấm</p><p><strong>${s.uniqueQuestions}</strong> câu khác nhau</p><p><strong>${s.total-s.correct}</strong> lượt sai</p><p><strong>${Math.round(s.correct/s.total*100)}%</strong> tỷ lệ đúng</p></div><h3>Nội dung hay sai</h3>${topicsMarkup(s,true)}<h3>50 lượt ôn gần nhất</h3>${[...s.rows].reverse().slice(0,50).map(r=>`<details class="result-question"><summary>${esc(new Date(r.graded_at).toLocaleString('vi-VN'))} · ${r.is_correct?'✓ Đúng':'✗ Sai'} · ${esc(r.topic)}</summary><p>${esc(r.answer?.variant)}</p><p>Bạn chọn: ${(r.answer?.selected||[]).map(id=>esc(r.answer?.answers?.find(a=>a.id===id)?.text||id)).join('; ')}</p><p>Đáp án đúng: ${(r.answer?.correct_ids||[]).map(id=>esc(r.answer?.answers?.find(a=>a.id===id)?.text||id)).join('; ')}</p><p>${esc(r.answer?.explanation)}</p><p>${(r.answer?.legal_basis||[]).map(b=>esc(typeof b==='string'?b:[b.document,b.article,b.clause,b.point].filter(Boolean).join(' · '))).join('; ')}</p></details>`).join('')}`:'<p>Chưa có câu ôn tập đã chấm. Bắt đầu ôn bằng cùng số điện thoại để ghi nhận từ bây giờ.</p>'}`;
    target.querySelectorAll('.practice-strengthen').forEach(button=>button.onclick=()=>{const t=s.topics[Number(button.dataset.index)];if(t)startPractice?.([...t.ids],{learnerKey:key,learnerName:s.rows.at(-1)?.learner_name});});
  }
  async function retryQueued(){let failed=false;for(const row of pending()){try{await deliver(row);}catch{failed=true;}}if(failed)throw Error('Practice results pending');}
  window.PracticeProgress={recordAnswer,summarize,sessionMarkup,bindResult,loadHistory,retryQueued,pendingCount:()=>pending().length};
})();
