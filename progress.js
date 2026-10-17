/* Phone-based self-practice history without authentication. Names are display labels. */
(() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalizeName = name => String(name).normalize('NFC').trim().replace(/\s+/g,' ');
  const nameKey = name => encodeURIComponent(normalizeName(name).toLocaleLowerCase('vi'));
  function normalizePhone(value) {
    const raw=String(value??'').trim();
    if(/[^0-9+\s().-]/.test(raw))throw Error('Nhập số điện thoại Việt Nam gồm 10–11 chữ số.');
    let phone=raw.replace(/[\s().-]/g,'');
    if(phone.startsWith('+84'))phone='0'+phone.slice(3);
    else if(phone.startsWith('0084'))phone='0'+phone.slice(4);
    else if(phone.startsWith('84'))phone='0'+phone.slice(2);
    if(!/^0[0-9]{9,10}$/.test(phone))throw Error('Nhập số điện thoại Việt Nam gồm 10–11 chữ số.');
    return phone;
  }
  const getPhone=()=>{try{return localStorage.getItem('examLearnerPhone')||'';}catch{return '';}};
  function storedHistory(name) {
    try{const saved=JSON.parse(localStorage.getItem('examHistoryKeys')||'{}');return Object.hasOwn(saved,nameKey(name))?saved[nameKey(name)]:'';}catch{return '';}
  }
  let config, startPractice, historyRequest=0;
  const capabilities=new Map(),phoneLinks=new Map();
  function historyKey(name, supplied='') {
    const label=nameKey(name);supplied=supplied.trim().toLowerCase();
    if(supplied && !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(supplied))throw Error('Mã lịch sử không hợp lệ.');
    let saved={};try{saved=JSON.parse(localStorage.getItem('examHistoryKeys')||'{}');}catch{}
    const stored=Object.hasOwn(saved,label)&&typeof saved[label]==='string'&&/^[0-9a-f-]{36}$/.test(saved[label])?saved[label]:'';
    const key=supplied||capabilities.get(label)||stored||crypto.randomUUID();
    capabilities.set(label,key);saved={...saved,[label]:key};try{localStorage.setItem('examHistoryKeys',JSON.stringify(saved));}catch{}
    return key;
  }
  const getName = () => {try{return localStorage.getItem('examLearnerName')||'';}catch{return '';}};
  const getQueue = () => {try{const q=JSON.parse(localStorage.getItem('examAttemptQueue')||'[]');return Array.isArray(q)?q:[];}catch{return [];}};
  function setQueue(rows) {localStorage.setItem('examAttemptQueue',JSON.stringify(rows));}
  async function request(path, key, options={}) {
    if(!config) {
      const r=await fetch('./data/feedback-config.json',{cache:'no-cache'});if(!r.ok)throw Error('Chưa tải được cấu hình.');config=await r.json();
      if(!/^https:\/\/[a-z0-9]+\.supabase\.co$/.test(config.url)||!config.publishableKey?.startsWith('sb_publishable_'))throw Error('Cấu hình không hợp lệ.');
    }
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),10000);
    try {
      const r=await fetch(`${config.url}/rest/v1/${path}`,{...options,headers:{apikey:config.publishableKey,'Content-Type':'application/json','x-client-info':key,...options.headers},signal:controller.signal});
      if(!r.ok){const e=await r.json().catch(()=>({}));if(options.method==='POST'&&r.status===409&&e.code==='23505')return;throw Error('Không kết nối được nơi lưu kết quả.');}
      if(r.status!==204 && options.method!=='POST' && options.method!=='PATCH')return await r.json();
    }finally{clearTimeout(timeout);}
  }
  function nameMarkup() {return `<label class="learner-label">Tên người học<input id="learnerName" maxlength="80" autocomplete="nickname" value="${esc(getName())}" placeholder="Ví dụ: Thúy An – nhóm 1" required /></label><label class="learner-label">Số điện thoại — mã lịch sử<input id="learnerPhone" type="tel" inputmode="tel" maxlength="24" autocomplete="tel" value="${esc(getPhone())}" placeholder="Nhập số điện thoại để lưu lịch sử ôn tập / thi thử" required /></label><p class="name-note">Dùng cùng số điện thoại trên mọi thiết bị để tiếp tục lịch sử và thứ hạng. Không cần đăng nhập hay xác thực. Ai biết số này đều có thể xem và bổ sung kết quả. Tên hoặc biệt danh dùng để hiển thị trên bảng xếp hạng.</p><p class="name-note">Ôn tập có thống kê riêng, không tính vào xếp hạng. Sau ít nhất 3 bài thi thử đã lưu, tên, số lượt thi và điểm tổng hợp sẽ xuất hiện trên bảng xếp hạng chung.</p><p id="nameStatus" role="alert"></p>`;}
  async function linkPhoneHistory(name, phone, supplied='') {
    phone=normalizePhone(phone);
    const old=supplied.trim().toLowerCase()||storedHistory(name);
    if(!old || old===phone)return;
    if(!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(old)){
      if(supplied)throw Error('Mã lịch sử cũ không hợp lệ.');return;
    }
    await request(`exam_attempts?learner_key=eq.${encodeURIComponent(old)}`,`${old}:${phone}`,{method:'PATCH',headers:{Prefer:'return=minimal'},body:JSON.stringify({learner_key:phone})});
    phoneLinks.set(old,phone);
    try{
      const saved=JSON.parse(localStorage.getItem('examHistoryKeys')||'{}');
      localStorage.setItem('examHistoryKeys',JSON.stringify({...saved,[nameKey(name)]:phone}));
      setQueue(getQueue().map(row=>row.learner_key===old?{...row,learner_key:phone}:row));
      const recentKey='congchungvnd:recent-v2:',before=JSON.parse(localStorage.getItem(recentKey+old)||'[]'),after=JSON.parse(localStorage.getItem(recentKey+phone)||'[]');
      if(Array.isArray(before)&&Array.isArray(after))localStorage.setItem(recentKey+phone,JSON.stringify([...new Set([...before,...after])].slice(0,2000)));
    }catch{}
    window.ExamLeaderboard?.refresh();
  }
  async function captureName(state) {
    const field=document.querySelector('#learnerName'),name=normalizeName(field.value);
    if(!name||name.length>80){document.querySelector('#nameStatus').textContent='Nhập tên người thi (tối đa 80 ký tự).';field.focus();return false;}
    const phoneField=document.querySelector('#learnerPhone'),status=document.querySelector('#nameStatus');
    let phone;try{phone=normalizePhone(phoneField.value);}catch(error){status.textContent=error.message;phoneField.focus();return false;}
    status.textContent='Đang chuẩn bị lịch sử…';
    try{await linkPhoneHistory(name,phone);}catch{status.textContent='Chưa nối được lịch sử cũ với số điện thoại. Kiểm tra kết nối rồi thử lại.';return false;}
    status.textContent='';state.learnerName=name;state.learnerPhone=phone;state.learnerKey=phone;phoneField.value=phone;
    try{localStorage.setItem('examLearnerName',name);localStorage.setItem('examLearnerPhone',phone);}catch{}return true;
  }
  function buildAttempt(state) {
    const answers=state.questions.map(q=>({question_id:q.id,part:q.part,topic:q.topic,variant:q.variant,answers:q.answers,selected:state.answers[q.id]||[],correct_ids:q.answers.filter(a=>a.correct).map(a=>a.id),is_correct:!!state.results[q.id],explanation:q.explanation,legal_basis:q.legalBasis}));
    return {id:state.attemptId,learner_name:state.learnerName,learner_key:state.learnerKey,exam_code:state.examCode,part:state.part,total:answers.length,correct:answers.filter(a=>a.is_correct).length,started_at:state.startedAt,submitted_at:state.submittedAt,duration_seconds:Math.max(0,Math.min(state.duration*60,Math.round((Date.parse(state.submittedAt)-Date.parse(state.startedAt))/1000))),answers};
  }
  function resultMarkup(state) {return state.mode==='mock'?`<div class="save-attempt"><p>Người thi: <strong>${esc(state.learnerName)}</strong></p><p>Mã lịch sử là số điện thoại: <strong>${esc(state.learnerKey)}</strong>. Nhập lại số này trên thiết bị khác để xem và tiếp tục lịch sử.</p><p id="attemptStatus" role="status">Đang lưu kết quả…</p><button id="retryAttempt" class="secondary-button hidden">Gửi lại kết quả</button> <button id="viewMyProgress" class="secondary-button">Xem tiến bộ của tôi</button></div>`:'';}
  async function deliver(row) {
    const linked=phoneLinks.get(row.learner_key)||storedHistory(row.learner_name);
    if(/^[0-9a-f-]{36}$/.test(row.learner_key)&&/^0[0-9]{9,10}$/.test(linked))row={...row,learner_key:linked};
    await request('exam_attempts',row.learner_key,{method:'POST',headers:{Prefer:'return=minimal'},body:JSON.stringify(row)});
    try{setQueue(getQueue().filter(x=>x.id!==row.id));}catch{}
    window.ExamLeaderboard?.refresh();
  }
  async function saveResult(state) {
    if(!state.learnerName)return;
    const row=buildAttempt(state),status=document.querySelector('#attemptStatus'),retry=document.querySelector('#retryAttempt');
    document.querySelector('#viewMyProgress').onclick=()=>{document.querySelector('#progressPhone').value=row.learner_key;document.querySelector('#progressMode').value='mock';loadHistory(row.learner_key,'mock');document.querySelector('#learningProgress').scrollIntoView({behavior:'smooth'});};
    const send=async()=>{retry.disabled=true;status.textContent='Đang lưu kết quả…';try{await deliver(row);status.textContent='Đã lưu điểm và đáp án lên hệ thống.';retry.classList.add('hidden');}catch{status.textContent='Chưa gửi được. Kết quả giữ trên thiết bị để gửi lại; đừng xóa dữ liệu trình duyệt.';retry.classList.remove('hidden');}finally{retry.disabled=false;}};
    try{const queue=getQueue();if(!queue.some(x=>x.id===row.id))queue.push(row);setQueue(queue);}catch{status.textContent='Thiết bị không lưu được bản dự phòng. Hãy gửi lại trước khi rời trang.';}
    retry.onclick=send;await send();
  }
  function summarize(rows) {
    const ordered=[...rows].sort((a,b)=>a.submitted_at.localeCompare(b.submitted_at)||a.id.localeCompare(b.id));
    const points=r=>r.correct/r.total*10;
    const topics=new Map();
    for(const row of ordered.slice(-5))for(const a of row.answers){const key=`${a.part}|${a.topic}`;const t=topics.get(key)||{part:a.part,topic:a.topic,total:0,wrong:0,ids:new Set(),basis:new Set()};t.total++;if(!a.is_correct){t.wrong++;t.ids.add(a.question_id);for(const b of a.legal_basis||[])t.basis.add(typeof b==='string'?b:JSON.stringify(b));}topics.set(key,t);}
    return {ordered,points,average:ordered.length?ordered.reduce((sum,r)=>sum+points(r),0)/ordered.length:0,weak:[...topics.values()].filter(t=>t.wrong).sort((a,b)=>b.wrong/b.total-a.wrong/a.total||b.wrong-a.wrong)};
  }
  function historyMarkup(rows) {
    if(!rows.length)return '<p>Chưa có lần thi nào được lưu với số điện thoại này.</p>';
    const s=summarize(rows),points=s.ordered.map(s.points),last=s.ordered.at(-1);
    const trend=[1,2].map(part=>{const exams=s.ordered.filter(r=>r.part===part);if(exams.length<2)return '';const recent=exams.slice(-5),previous=exams.slice(Math.max(0,exams.length-10),-5);const base=previous.length?previous:[exams[0]],avg=rs=>rs.reduce((n,r)=>n+s.points(r),0)/rs.length;const delta=avg(recent)-avg(base);return `<p>Bài ${part}: trung bình ${recent.length} lần gần nhất ${avg(recent).toFixed(2)}/10${previous.length?` · ${delta>=0?'+':''}${delta.toFixed(2)} điểm so với ${base.length} lần trước`: ' · chưa đủ 6 lần thi để so sánh hai giai đoạn'}.</p>`;}).join('');
    const plotted=points.slice(-20),coords=plotted.map((v,i)=>`${20+i*460/Math.max(1,plotted.length-1)},${120-v*10}`).join(' ');
    return `<div class="progress-stats"><p><strong>${rows.length}</strong> lần thi</p><p>Trung bình <strong>${s.average.toFixed(2)}/10</strong></p><p>Gần nhất <strong>${s.points(last).toFixed(2)}/10</strong></p><p>Cao nhất <strong>${Math.max(...points).toFixed(2)}/10</strong></p></div>${trend}<p class="name-note">Điểm quy đổi về thang 10. Độ khó và phạm vi đề khác nhau nên điểm tăng chỉ là dấu hiệu tham khảo.</p><svg class="score-chart" viewBox="0 0 500 145" role="img" aria-label="Điểm của tối đa 20 lần thi gần nhất theo thứ tự thời gian"><text x="0" y="20">10</text><text x="5" y="123">0</text><path d="M20 20H480 M20 120H480" stroke="#dfe3ea"/><polyline points="${coords}" fill="none" stroke="#175cd3" stroke-width="3"/>${plotted.map((v,i)=>`<circle cx="${20+i*460/Math.max(1,plotted.length-1)}" cy="${120-v*10}" r="4" fill="#175cd3"><title>Lần ${points.length-plotted.length+i+1}: ${v.toFixed(2)}/10</title></circle>`).join('')}</svg><h3>Kiến thức cần củng cố</h3><p>Dựa trên câu sai và chưa trả lời của 5 lần thi gần nhất.</p>${s.weak.length?s.weak.map((t,i)=>`<div class="weak-topic"><strong>Bài ${t.part} · ${esc(t.topic)}</strong><p>${t.wrong}/${t.total} lượt câu chưa đúng (${Math.round(t.wrong/t.total*100)}%).</p><p>${[...t.basis].map(esc).join(' · ')}</p><button class="secondary-button strengthen" data-index="${i}">Ôn các câu cần củng cố</button></div>`).join(''):'<p>Các câu trong 5 lần thi gần nhất đều đúng. Tiếp tục luyện thêm phạm vi khác.</p>'}<h3>Lịch sử thi và đáp án</h3>${[...s.ordered].reverse().map(r=>`<details class="result-question"><summary>${esc(new Date(r.submitted_at).toLocaleString('vi-VN'))} · Bài ${r.part} · ${s.points(r).toFixed(2)}/10 · ${r.correct}/${r.total} câu</summary><p>Mã đề: ${esc(r.exam_code)}</p><p>Thời gian làm: ${Math.floor(r.duration_seconds/60)} phút ${r.duration_seconds%60} giây.</p>${r.answers.map((a,i)=>`<details class="result-question"><summary>Câu ${i+1} · ${a.is_correct?'✓ Đúng':a.selected.length?'✗ Sai':'— Chưa trả lời'} · ${esc(a.topic)}</summary><p>${esc(a.variant)}</p><p>Đã chọn: ${a.selected.length?a.selected.map(id=>esc(a.answers.find(x=>x.id===id)?.text||id)).join('; '):'Chưa trả lời'}</p><p><strong>Đáp án đúng:</strong> ${a.correct_ids.map(id=>esc(a.answers.find(x=>x.id===id)?.text||id)).join('; ')}</p><p>${esc(a.explanation)}</p><p>${(a.legal_basis||[]).map(b=>esc(typeof b==='string'?b:JSON.stringify(b))).join(' · ')}</p></details>`).join('')}</details>`).join('')}`;
  }
  async function loadHistory(phone, mode=document.querySelector('#progressMode')?.value||'mock') {
    const target=document.querySelector('#progressContent'),token=++historyRequest;
    if(mode==='practice')return window.PracticeProgress?.loadHistory(phone,startPractice,()=>token===historyRequest);
    let key;try{key=normalizePhone(phone);}catch(error){target.textContent=error.message;return;}
    target.textContent='Đang tải lịch sử…';
    try {
      const rows=[];document.querySelector('#progressPhone').value=key;
      for(let offset=0;;offset+=100){const page=await request(`exam_attempts?learner_key=eq.${encodeURIComponent(key)}&order=submitted_at.asc,id.asc&limit=100&offset=${offset}`,key);if(token!==historyRequest)return;rows.push(...page);if(page.length<100)break;}
      target.innerHTML=(rows.length?`<p>Người thi: <strong>${esc(rows.at(-1).learner_name)}</strong></p>`:'')+historyMarkup(rows);
      const weak=summarize(rows).weak;
      target.querySelectorAll('.strengthen').forEach(b=>b.onclick=()=>startPractice?.([...weak[Number(b.dataset.index)].ids],{learnerKey:key,learnerName:rows.at(-1)?.learner_name}));
    }catch{if(token===historyRequest)target.textContent='Chưa tải được lịch sử. Kiểm tra kết nối rồi bấm Xem thống kê lại.';}
  }
  function init(practice) {
    startPractice=practice;
    const root=document.querySelector('#learningProgress');
    root.innerHTML=`<h2>Thống kê ôn tập và thi thử</h2><label class="learner-label">Số điện thoại — mã lịch sử<input id="progressPhone" type="tel" inputmode="tel" maxlength="24" value="${esc(getPhone())}" autocomplete="tel" placeholder="Nhập số điện thoại đã dùng khi thi" /></label><p class="name-note">Nhập cùng số điện thoại trên mọi thiết bị. Không cần tên để tra cứu, không cần đăng nhập hay xác thực. Ai biết số này đều có thể xem và bổ sung kết quả.</p><label class="learner-label">Chế độ thống kê<select id="progressMode"><option value="mock">Thi thử</option><option value="practice">Ôn tập</option></select></label><button id="loadProgress" class="primary-button">Xem thống kê</button> <button id="retryQueued" class="secondary-button">Gửi kết quả chưa lưu</button><details><summary>Nối lịch sử cũ sang số điện thoại</summary><p>Dùng cho bài thi trước khi đổi sang số điện thoại. Trên thiết bị đã thi, nhập tên cũ; trên thiết bị khác, dán thêm mã lịch sử cũ. Kết quả cũ được giữ nguyên và cộng vào cùng thứ hạng.</p><label class="learner-label">Tên đã dùng trước đây<input id="legacyName" maxlength="80" value="${esc(getName())}" /></label><label class="learner-label">Mã lịch sử cũ (nếu đổi thiết bị)<input id="legacyCode" autocomplete="off" /></label><button id="linkLegacyHistory" class="secondary-button">Nối lịch sử cũ</button><p id="legacyStatus" role="status"></p></details><p id="queueStatus" role="status"></p><div id="progressContent"></div>`;
    document.querySelector('#loadProgress').onclick=()=>loadHistory(document.querySelector('#progressPhone').value);
    document.querySelector('#progressMode').onchange=()=>{historyRequest++;document.querySelector('#progressContent').textContent='Bấm Xem thống kê để tải chế độ đã chọn.';};
    document.querySelector('#linkLegacyHistory').onclick=async()=>{
      const button=document.querySelector('#linkLegacyHistory'),status=document.querySelector('#legacyStatus');button.disabled=true;
      try{const name=normalizeName(document.querySelector('#legacyName').value),code=document.querySelector('#legacyCode').value.trim();if(!name||(!code&&!storedHistory(name)))throw Error('Nhập tên cũ trên thiết bị đã thi, hoặc dán mã lịch sử cũ.');const phone=normalizePhone(document.querySelector('#progressPhone').value);await linkPhoneHistory(name,phone,code);try{localStorage.setItem('examLearnerPhone',phone);}catch{}status.textContent='Đã nối lịch sử cũ sang số điện thoại.';await loadHistory(phone);}catch(error){status.textContent=error.message;}finally{button.disabled=false;}
    };
    document.querySelector('#retryQueued').onclick=async()=>{const button=document.querySelector('#retryQueued'),status=document.querySelector('#queueStatus');button.disabled=true;let failed=false;try{for(const row of getQueue())await deliver(row);}catch{failed=true;}try{await window.PracticeProgress?.retryQueued();}catch{failed=true;}finally{button.disabled=false;status.textContent=failed?'Còn kết quả chưa gửi. Hãy thử lại khi có kết nối.':'Đã gửi hết kết quả đang chờ trên thiết bị.';}};
    const pending=getQueue().length+(window.PracticeProgress?.pendingCount()||0);document.querySelector('#queueStatus').textContent=pending?`Có ${pending} kết quả/câu ôn tập đang chờ gửi trên thiết bị.`:'';
  }
  window.ExamProgress={init,nameMarkup,captureName,resultMarkup,saveResult,normalizeName,normalizePhone,nameKey,historyKey,linkPhoneHistory,buildAttempt,summarize,historyMarkup,loadHistory,request};
})();
