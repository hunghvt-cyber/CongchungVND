/* Name-based learning history. Names are labels; a random history capability controls access without accounts. */
(() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalizeName = name => String(name).normalize('NFC').trim().replace(/\s+/g,' ');
  const nameKey = name => encodeURIComponent(normalizeName(name).toLocaleLowerCase('vi'));
  let config, startPractice, historyRequest=0;
  const capabilities=new Map();
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
      if(options.method!=='POST')return await r.json();
    }finally{clearTimeout(timeout);}
  }
  function nameMarkup() {return `<label class="learner-label">Tên người thi<input id="learnerName" maxlength="80" autocomplete="nickname" value="${esc(getName())}" placeholder="Ví dụ: Thúy An – nhóm 1" required /></label><p class="name-note">Dùng cùng một tên mỗi lần thi để theo dõi tiến bộ. Lịch sử được bảo vệ bằng mã riêng tự lưu trên thiết bị. Khi đổi thiết bị, dùng lại tên và mã lịch sử. Không cần tài khoản.</p><p id="nameStatus" role="alert"></p>`;}
  function captureName(state) {
    const field=document.querySelector('#learnerName'),name=normalizeName(field.value);
    if(!name||name.length>80){document.querySelector('#nameStatus').textContent='Nhập tên người thi (tối đa 80 ký tự).';field.focus();return false;}
    document.querySelector('#nameStatus').textContent='';state.learnerName=name;state.learnerKey=historyKey(name);try{localStorage.setItem('examLearnerName',name);}catch{}return true;
  }
  function buildAttempt(state) {
    const answers=state.questions.map(q=>({question_id:q.id,part:q.part,topic:q.topic,variant:q.variant,answers:q.answers,selected:state.answers[q.id]||[],correct_ids:q.answers.filter(a=>a.correct).map(a=>a.id),is_correct:!!state.results[q.id],explanation:q.explanation,legal_basis:q.legalBasis}));
    return {id:state.attemptId,learner_name:state.learnerName,learner_key:state.learnerKey,exam_code:state.examCode,part:state.part,total:answers.length,correct:answers.filter(a=>a.is_correct).length,started_at:state.startedAt,submitted_at:state.submittedAt,duration_seconds:Math.max(0,Math.min(state.duration*60,Math.round((Date.parse(state.submittedAt)-Date.parse(state.startedAt))/1000))),answers};
  }
  function resultMarkup(state) {return state.mode==='mock'?`<div class="save-attempt"><p>Người thi: <strong>${esc(state.learnerName)}</strong></p><details><summary>Mã lịch sử để xem trên thiết bị khác</summary><p>Giữ mã riêng, không chia sẻ công khai. Mã này cho phép xem và bổ sung lịch sử.</p><input class="history-code" readonly value="${esc(state.learnerKey)}" aria-label="Mã lịch sử" /></details><p id="attemptStatus" role="status">Đang lưu kết quả…</p><button id="retryAttempt" class="secondary-button hidden">Gửi lại kết quả</button> <button id="viewMyProgress" class="secondary-button">Xem tiến bộ của tôi</button></div>`:'';}
  async function deliver(row) {
    await request('exam_attempts',row.learner_key,{method:'POST',headers:{Prefer:'return=minimal'},body:JSON.stringify(row)});
    try{setQueue(getQueue().filter(x=>x.id!==row.id));}catch{}
  }
  async function saveResult(state) {
    if(!state.learnerName)return;
    const row=buildAttempt(state),status=document.querySelector('#attemptStatus'),retry=document.querySelector('#retryAttempt');
    document.querySelector('#viewMyProgress').onclick=()=>{document.querySelector('#progressName').value=row.learner_name;document.querySelector('#historyCode').value=row.learner_key;loadHistory(row.learner_name);document.querySelector('#learningProgress').scrollIntoView({behavior:'smooth'});};
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
    if(!rows.length)return '<p>Chưa có lần thi nào được lưu với tên này.</p>';
    const s=summarize(rows),points=s.ordered.map(s.points),last=s.ordered.at(-1);
    const trend=[1,2].map(part=>{const exams=s.ordered.filter(r=>r.part===part);if(exams.length<2)return '';const recent=exams.slice(-5),previous=exams.slice(Math.max(0,exams.length-10),-5);const base=previous.length?previous:[exams[0]],avg=rs=>rs.reduce((n,r)=>n+s.points(r),0)/rs.length;const delta=avg(recent)-avg(base);return `<p>Bài ${part}: trung bình ${recent.length} lần gần nhất ${avg(recent).toFixed(2)}/10${previous.length?` · ${delta>=0?'+':''}${delta.toFixed(2)} điểm so với ${base.length} lần trước`: ' · chưa đủ 6 lần thi để so sánh hai giai đoạn'}.</p>`;}).join('');
    const plotted=points.slice(-20),coords=plotted.map((v,i)=>`${20+i*460/Math.max(1,plotted.length-1)},${120-v*10}`).join(' ');
    return `<div class="progress-stats"><p><strong>${rows.length}</strong> lần thi</p><p>Trung bình <strong>${s.average.toFixed(2)}/10</strong></p><p>Gần nhất <strong>${s.points(last).toFixed(2)}/10</strong></p><p>Cao nhất <strong>${Math.max(...points).toFixed(2)}/10</strong></p></div>${trend}<p class="name-note">Điểm quy đổi về thang 10. Độ khó và phạm vi đề khác nhau nên điểm tăng chỉ là dấu hiệu tham khảo.</p><svg class="score-chart" viewBox="0 0 500 145" role="img" aria-label="Điểm của tối đa 20 lần thi gần nhất theo thứ tự thời gian"><text x="0" y="20">10</text><text x="5" y="123">0</text><path d="M20 20H480 M20 120H480" stroke="#dfe3ea"/><polyline points="${coords}" fill="none" stroke="#175cd3" stroke-width="3"/>${plotted.map((v,i)=>`<circle cx="${20+i*460/Math.max(1,plotted.length-1)}" cy="${120-v*10}" r="4" fill="#175cd3"><title>Lần ${points.length-plotted.length+i+1}: ${v.toFixed(2)}/10</title></circle>`).join('')}</svg><h3>Kiến thức cần củng cố</h3><p>Dựa trên câu sai và chưa trả lời của 5 lần thi gần nhất.</p>${s.weak.length?s.weak.map((t,i)=>`<div class="weak-topic"><strong>Bài ${t.part} · ${esc(t.topic)}</strong><p>${t.wrong}/${t.total} lượt câu chưa đúng (${Math.round(t.wrong/t.total*100)}%).</p><p>${[...t.basis].map(esc).join(' · ')}</p><button class="secondary-button strengthen" data-index="${i}">Ôn các câu cần củng cố</button></div>`).join(''):'<p>Các câu trong 5 lần thi gần nhất đều đúng. Tiếp tục luyện thêm phạm vi khác.</p>'}<h3>Lịch sử thi và đáp án</h3>${[...s.ordered].reverse().map(r=>`<details class="result-question"><summary>${esc(new Date(r.submitted_at).toLocaleString('vi-VN'))} · Bài ${r.part} · ${s.points(r).toFixed(2)}/10 · ${r.correct}/${r.total} câu</summary><p>Mã đề: ${esc(r.exam_code)}</p><p>Thời gian làm: ${Math.floor(r.duration_seconds/60)} phút ${r.duration_seconds%60} giây.</p>${r.answers.map((a,i)=>`<details class="result-question"><summary>Câu ${i+1} · ${a.is_correct?'✓ Đúng':a.selected.length?'✗ Sai':'— Chưa trả lời'} · ${esc(a.topic)}</summary><p>${esc(a.variant)}</p><p>Đã chọn: ${a.selected.length?a.selected.map(id=>esc(a.answers.find(x=>x.id===id)?.text||id)).join('; '):'Chưa trả lời'}</p><p><strong>Đáp án đúng:</strong> ${a.correct_ids.map(id=>esc(a.answers.find(x=>x.id===id)?.text||id)).join('; ')}</p><p>${esc(a.explanation)}</p><p>${(a.legal_basis||[]).map(b=>esc(typeof b==='string'?b:JSON.stringify(b))).join(' · ')}</p></details>`).join('')}</details>`).join('')}`;
  }
  async function loadHistory(name) {
    const target=document.querySelector('#progressContent'),token=++historyRequest;
    name=normalizeName(name);if(!name||name.length>80){target.textContent='Nhập tên người thi để tra cứu.';return;}
    target.textContent='Đang tải lịch sử…';
    try {
      const key=historyKey(name,document.querySelector('#historyCode').value.trim()),rows=[];document.querySelector('#historyCode').value=key;
      for(let offset=0;;offset+=100){const page=await request(`exam_attempts?learner_key=eq.${encodeURIComponent(key)}&order=submitted_at.asc,id.asc&limit=100&offset=${offset}`,key);if(token!==historyRequest)return;rows.push(...page);if(page.length<100)break;}
      target.innerHTML=historyMarkup(rows);
      const weak=summarize(rows).weak;
      target.querySelectorAll('.strengthen').forEach(b=>b.onclick=()=>startPractice?.([...weak[Number(b.dataset.index)].ids]));
    }catch{if(token===historyRequest)target.textContent='Chưa tải được lịch sử. Kiểm tra kết nối rồi bấm Xem thống kê lại.';}
  }
  function init(practice) {
    startPractice=practice;
    const root=document.querySelector('#learningProgress');
    root.innerHTML=`<h2>Tiến bộ của người thi</h2><label class="learner-label">Tên đã dùng khi thi<input id="progressName" maxlength="80" value="${esc(getName())}" autocomplete="nickname" /></label><p class="name-note">Không cần đăng nhập. Thiết bị này nhớ mã lịch sử theo tên. Trên thiết bị khác, nhập lại mã riêng bên dưới; chỉ nhập tên sẽ tạo lịch sử mới.</p><details><summary>Mã lịch sử / xem trên thiết bị khác</summary><label class="learner-label">Mã lịch sử riêng<input id="historyCode" autocomplete="off" placeholder="Tự tạo trên thiết bị này; dán mã cũ để tiếp tục" /></label><p class="name-note">Giữ mã riêng. Ai có mã có thể xem và bổ sung lịch sử. Mất mã và xóa dữ liệu trình duyệt sẽ không tra cứu được bằng tên.</p></details><button id="loadProgress" class="primary-button">Xem thống kê</button> <button id="retryQueued" class="secondary-button">Gửi kết quả chưa lưu</button><p id="queueStatus" role="status"></p><div id="progressContent"></div>`;
    document.querySelector('#progressName').addEventListener('input',()=>{document.querySelector('#historyCode').value='';});
    document.querySelector('#loadProgress').onclick=()=>loadHistory(document.querySelector('#progressName').value);
    document.querySelector('#retryQueued').onclick=async()=>{const button=document.querySelector('#retryQueued'),status=document.querySelector('#queueStatus');button.disabled=true;let failed=false;try{for(const row of getQueue())await deliver(row);}catch{failed=true;}finally{button.disabled=false;status.textContent=failed?'Còn kết quả chưa gửi. Hãy thử lại khi có kết nối.':'Đã gửi hết kết quả đang chờ trên thiết bị.';}};
    const pending=getQueue().length;document.querySelector('#queueStatus').textContent=pending?`Có ${pending} kết quả đang chờ gửi trên thiết bị.`:'';
  }
  window.ExamProgress={init,nameMarkup,captureName,resultMarkup,saveResult,normalizeName,nameKey,historyKey,buildAttempt,summarize,historyMarkup,loadHistory};
})();
