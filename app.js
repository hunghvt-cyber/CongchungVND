const state = {
  bank: [], mode: null, part: null, questions: [], current: 0,
  selected: new Set(), answers: {}, results: {}, score: 0, answered: false,
  examCode: '', duration: 0, remaining: 0, timerId: null, submitted: false, reviewing: false, deadline: 0, startedAt: '', submittedAt: ''
};

const els = {
  setup: document.querySelector('#setup'), quiz: document.querySelector('#quiz'), result: document.querySelector('#result'),
  questionArea: document.querySelector('#questionArea'), quizMode: document.querySelector('#quizMode'), quizTitle: document.querySelector('#quizTitle'),
  examCode: document.querySelector('#examCode'), timer: document.querySelector('#timer'), progressText: document.querySelector('#progressText'),
  scoreText: document.querySelector('#scoreText'), progressBar: document.querySelector('#progressBar'), prev: document.querySelector('#prevQuestion'), next: document.querySelector('#nextQuestion')
};

const shuffle = items => { const a = [...items]; for (let i=a.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const eligibleQuestion = q => ['active', 'verified'].includes(q.status);
const hasResult = q => Object.hasOwn(state.results, q.id);
const isReviewing = () => state.submitted || state.reviewing;
const correctIds = q => new Set(q.answers.filter(a => a.correct).map(a => a.id));
const sameSet = (a,b) => a.size === b.size && [...a].every(x => b.has(x));

async function loadQuestions() {
  const [base, round2] = await Promise.all([
    fetch('./data/questions.json').then(r => { if(!r.ok) throw new Error('Không thể tải ngân hàng câu hỏi.'); return r.json(); }),
    fetch('./data/derived-questions.json').then(r => { if(!r.ok) throw new Error('Không thể tải ngân hàng câu hỏi vòng 2.'); return r.json(); })
  ]);
  const all = [...base, ...round2];
  return all.filter((q, i, arr) => arr.findIndex(x => x.id === q.id) === i);
}

function showSetup(mode) {
  stopTimer();
  state.mode = mode;
  els.quiz.classList.add('hidden'); els.result.classList.add('hidden');
  els.setup.classList.remove('hidden');
  const available = state.bank.filter(eligibleQuestion).length;
  const pending = state.bank.length - available;
  els.setup.innerHTML = mode === 'practice' ? `
    <p class="eyebrow">Ôn tập</p><h2>Chọn nội dung</h2>
    <p class="lead">Ngân hàng hiện có <strong>${available}</strong> câu được phép luyện/thi; ${pending} câu chưa đủ điều kiện đang được giữ để rà soát.</p>
    <div class="setup-grid"><label>Bài<select id="setupPart"><option value="all">Tất cả</option><option value="1">Bài 1 · Pháp luật</option><option value="2">Bài 2 · Kỹ năng</option></select></label>
    <label>Số câu<select id="setupCount"><option>5</option><option>10</option><option>20</option><option>50</option><option value="100">100</option></select></label></div>
    <button id="startSetup" class="primary-button">Bắt đầu ôn</button>` : `
    <p class="eyebrow">Thi thử</p><h2>Cấu hình bài thi</h2>
    <div class="setup-grid"><label>Bài<select id="setupPart"><option value="1">Bài 1 · Pháp luật</option><option value="2">Bài 2 · Kỹ năng</option></select></label>
    <label>Số câu<select id="setupCount"><option>5</option><option>10</option><option>20</option><option>50</option><option>100</option></select></label>
    <label>Thời gian<select id="setupDuration"><option value="15">15 phút</option><option value="30">30 phút</option><option value="60">60 phút</option><option value="90">90 phút</option></select></label></div>
    <button id="startSetup" class="primary-button">Sinh mã đề & bắt đầu</button>`;
  document.querySelector('#startSetup').addEventListener('click', () => {
    const part = document.querySelector('#setupPart').value;
    const count = Number(document.querySelector('#setupCount').value);
    const duration = mode === 'mock' ? Number(document.querySelector('#setupDuration').value) : 0;
    startSession(part === 'all' ? null : Number(part), count, duration);
  });
}

function startSession(part, count, duration) {
  stopTimer();
  const pool = state.bank.filter(q => eligibleQuestion(q) && (part === null || q.part === part));
  if (!pool.length) { alert('Chưa có câu hỏi đủ điều kiện cho bài này.'); return; }
  state.reviewing = false; state.startedAt = new Date().toISOString(); state.submittedAt = '';
  state.part = part; state.current = 0; state.selected = new Set(); state.answers = {}; state.results = {}; state.score = 0; state.submitted = false;
  state.questions = shuffle(pool).slice(0, Math.min(count, pool.length)).map(q => ({...q, answers: shuffle(q.answers), variant: q.question.variants[Math.floor(Math.random()*q.question.variants.length)]}));
  state.examCode = state.mode === 'mock' ? makeExamCode() : '';
  state.duration = duration; state.remaining = duration * 60; state.deadline = Date.now() + state.remaining * 1000;
  els.setup.classList.add('hidden'); els.result.classList.add('hidden'); els.quiz.classList.remove('hidden');
  if (state.mode === 'mock') startTimer(); else stopTimer();
  renderQuestion(); els.quiz.scrollIntoView({behavior:'smooth', block:'start'});
}

function makeExamCode() { return `CC-${Date.now().toString(36).slice(-5).toUpperCase()}-${Math.floor(100+Math.random()*900)}`; }
function checkDeadline() {
  if (state.mode !== 'mock' || state.submitted || !state.timerId) return false;
  state.remaining = Math.max(0, Math.ceil((state.deadline - Date.now()) / 1000));
  updateTimer();
  if (state.remaining === 0) { submitMock(true); return true; }
  return false;
}
function startTimer() { stopTimer(); updateTimer(); state.timerId = setInterval(checkDeadline, 250); }
function stopTimer() { if (state.timerId) clearInterval(state.timerId); state.timerId = null; }
function updateTimer() { if (state.mode !== 'mock') { els.timer.textContent=''; return; } const m=Math.floor(state.remaining/60), s=state.remaining%60; els.timer.textContent=`⏱ ${m}:${String(s).padStart(2,'0')}`; els.timer.classList.toggle('danger', state.remaining <= 60); }

function renderQuestion() {
  const q = state.questions[state.current]; if (!q) return;
  state.selected = new Set(state.answers[q.id] || []); state.answered = isReviewing() || (state.mode === 'practice' && hasResult(q));
  const variant = q.variant;
  updateTimer();
  els.quizMode.textContent = isReviewing() ? 'Xem lại đáp án' : (state.mode === 'practice' ? 'Ôn tập' : 'Thi thử');
  els.quizTitle.textContent = q.topic;
  els.examCode.textContent = state.examCode ? `Mã đề ${state.examCode}` : '';
  els.progressText.textContent = `Câu ${state.current+1} / ${state.questions.length}`;
  els.scoreText.textContent = state.mode === 'practice' ? `Đúng ${state.score}` : `Đã làm ${Object.keys(state.answers).length}`;
  els.progressBar.style.width = `${((state.current+1)/state.questions.length)*100}%`;
  els.prev.disabled = state.current === 0;
  const last = state.current === state.questions.length-1;
  els.next.textContent = isReviewing() ? (last ? 'Về kết quả' : 'Câu tiếp →')
    : state.mode === 'mock' ? (last ? 'Nộp bài' : 'Câu tiếp →')
    : !state.answered ? 'Kiểm tra đáp án' : (last ? 'Hoàn thành' : 'Câu tiếp →');
  const selected = state.selected;
  els.questionArea.innerHTML = `<p class="question-text">${escapeHtml(variant)}</p>
    <p class="answer-hint">${q.type === 'multiple' ? 'Chọn tất cả đáp án đúng.' : 'Chọn một đáp án.'}</p>
    <div class="answers">${q.answers.map((a,i)=>`<button class="answer ${selected.has(a.id)?'selected':''}" ${state.answered?'disabled':''} data-answer-id="${escapeHtml(a.id)}"><span class="answer-key">${String.fromCharCode(65+i)}.</span><span>${escapeHtml(a.text)}</span></button>`).join('')}</div>
    <div id="explanation" class="explanation ${state.answered?'':'hidden'}"></div>
    ${feedbackMarkup()}`;
  els.questionArea.querySelectorAll('.answer').forEach(b=>b.addEventListener('click',()=>toggleAnswer(b.dataset.answerId)));
  bindFeedback(els.questionArea, q);
  if (state.answered) renderReview(q, state.results[q.id]);
}

function toggleAnswer(id) {
  if (checkDeadline() || isReviewing() || (state.mode === 'practice' && state.answered)) return;
  if (state.mode === 'mock' && state.submitted) return;
  if (state.questions[state.current].type === 'single') state.selected = new Set([id]);
  else state.selected.has(id) ? state.selected.delete(id) : state.selected.add(id);
  const qid=state.questions[state.current].id;
  if (state.selected.size) state.answers[qid] = [...state.selected]; else delete state.answers[qid];
  if (state.mode === 'mock') els.scoreText.textContent=`Đã làm ${Object.keys(state.answers).length}`;
  els.questionArea.querySelectorAll('.answer').forEach(b=>b.classList.toggle('selected',state.selected.has(b.dataset.answerId)));
}

function submitPractice() {
  if (state.answered || !state.selected.size) return !!state.answered;
  const q=state.questions[state.current], correct=correctIds(q), ok=sameSet(correct,state.selected);
  state.results[q.id]=ok; if(ok) state.score++; state.answered=true; state.answers[q.id]=[...state.selected]; renderReview(q,ok); els.scoreText.textContent=`Đúng ${state.score}`; return true;
}
function renderReview(q, ok) {
  els.questionArea.querySelectorAll('.answer').forEach(b=>{const a=q.answers.find(x=>x.id===b.dataset.answerId); b.classList.toggle('correct',a.correct); b.classList.toggle('wrong',!a.correct && state.selected.has(a.id));});
  els.questionArea.querySelectorAll('.answer').forEach(b=>{b.disabled=true;});
  const e=document.querySelector('#explanation'); e.classList.remove('hidden');
  e.innerHTML=reviewMarkup(q, ok);
}
function answerSummary(q, ids) {
  const selected = new Set(ids);
  return q.answers.map((a,i) => selected.has(a.id) ? `${String.fromCharCode(65+i)}. ${a.text}` : null).filter(Boolean).map(escapeHtml).join('<br>') || 'Chưa trả lời';
}
function basisMarkup(q) {
  return q.legalBasis?.length ? `<div class="legal"><strong>Căn cứ pháp lý</strong>${q.legalBasis.map(x => {
    const label = typeof x === 'string' ? x : [x.document,x.article,x.clause,x.point].filter(Boolean).join(' · ');
    const url = typeof x === 'object' ? x.url : null;
    return `<div>${escapeHtml(label)}${url && /^https?:\/\//i.test(url) ? ` · <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">Xem văn bản</a>` : ''}</div>`;
  }).join('')}</div>` : '<p>Chưa có căn cứ pháp lý.</p>';
}
function reviewMarkup(q, ok) {
  return `<strong>${ok?'✓ Đúng':(state.answers[q.id]?.length?'✗ Chưa chính xác':'— Chưa trả lời')}</strong>
    <p><strong>Bạn chọn:</strong><br>${answerSummary(q, state.answers[q.id] || [])}</p>
    <p><strong>Đáp án đúng:</strong><br>${answerSummary(q, correctIds(q))}</p>
    <p><strong>Giải thích:</strong> ${escapeHtml(q.explanation || 'Chưa có giải thích.')}</p>${basisMarkup(q)}`;
}
function next() {
  if (checkDeadline()) return;
  if (isReviewing()) {
    if (state.current < state.questions.length-1) { state.current++; renderQuestion(); }
    else state.mode === 'mock' ? showMockResult(false) : showPracticeResult();
    return;
  }
  if (state.mode === 'practice') {
    if (!state.answered) { if (submitPractice()) { els.next.textContent=state.current===state.questions.length-1?'Hoàn thành':'Câu tiếp →'; } return; }
    if (state.current < state.questions.length-1) { state.current++; renderQuestion(); } else showPracticeResult();
  } else if (state.current < state.questions.length-1) { state.current++; renderQuestion(); } else submitMock(false);
}

function submitMock(auto=false){ if(state.submitted)return; stopTimer(); state.submitted=true; state.submittedAt=new Date().toISOString(); state.questions.forEach(q=>{const sel=new Set(state.answers[q.id]||[]); state.results[q.id]=sameSet(correctIds(q),sel);}); state.score=Object.values(state.results).filter(Boolean).length; showMockResult(auto); }
function resultQuestionsMarkup() {
  return `<div class="result-list"><h3>Đáp án và giải thích tất cả câu hỏi</h3>${state.questions.map((q,i) => `
    <details class="result-question" data-qid="${escapeHtml(q.id)}">
      <summary>Câu ${i+1} · ${state.results[q.id]?'✓ Đúng':(state.answers[q.id]?.length?'✗ Sai':'— Chưa trả lời')} · ${escapeHtml(q.topic)}</summary>
      <p class="question-text">${escapeHtml(q.variant)}</p>
      <div class="explanation">${reviewMarkup(q, state.results[q.id])}</div>${feedbackMarkup()}
    </details>`).join('')}</div>`;
}
function bindResultFeedback() {
  els.result.querySelectorAll('[data-qid]').forEach(root => bindFeedback(root, state.questions.find(q=>q.id===root.dataset.qid)));
  document.querySelector('#homeResult').addEventListener('click',()=>location.reload());
}
function showPracticeResult() {
  els.quiz.classList.add('hidden'); els.result.classList.remove('hidden');
  const wrong=state.questions.filter(q=>!state.results[q.id]);
  els.result.innerHTML=`<p class="eyebrow">Hoàn thành</p><h2>Kết quả ôn tập</h2><div class="result-score">${state.score}/${state.questions.length}</div><p>${Math.round(state.score/state.questions.length*100)}% câu trả lời đúng.</p><p>Đúng: ${state.score} · Sai: ${wrong.length}</p>
    ${resultQuestionsMarkup()}<button id="reviewWrong" class="secondary-button" ${wrong.length?'':'disabled'}>Ôn lại câu sai</button> <button id="homeResult" class="primary-button">Về trang chính</button>`;
  document.querySelector('#reviewWrong').addEventListener('click',()=>{
    state.questions=wrong; state.current=0; state.score=0; state.results={}; state.answers={}; state.mode='practice'; state.reviewing=false; state.submitted=false;
    els.result.classList.add('hidden'); els.quiz.classList.remove('hidden'); renderQuestion();
  });
  bindResultFeedback();
}
function showMockResult(auto) {
  els.quiz.classList.add('hidden'); els.result.classList.remove('hidden');
  const unanswered=state.questions.filter(q=>!state.answers[q.id]?.length).length;
  els.result.innerHTML=`<p class="eyebrow">${auto?'Hết giờ':'Đã nộp bài'}</p><h2>Kết quả thi thử</h2><p>Mã đề <strong>${escapeHtml(state.examCode)}</strong></p><div class="result-score">${state.score}/${state.questions.length}</div><p>${Math.round(state.score/state.questions.length*100)}% câu trả lời đúng · Điểm: ${(state.score/state.questions.length*10).toFixed(2)}/10.</p><p>Đúng: ${state.score} · Sai: ${state.questions.length-state.score-unanswered} · Chưa trả lời: ${unanswered}</p>
    ${resultQuestionsMarkup()}<button id="homeResult" class="primary-button">Về trang chính</button>`;
  bindResultFeedback();
}
function reviewQuestion(id) {
  const idx=state.questions.findIndex(q=>q.id===id); if(idx<0)return;
  state.current=idx; state.reviewing=true; els.result.classList.add('hidden'); els.quiz.classList.remove('hidden'); renderQuestion();
}
function feedbackMarkup() { return '<button class="feedback-button">⚠ Góp ý câu hỏi / đáp án</button><div class="feedback-box hidden"></div>'; }
function bindFeedback(root, q) { root.querySelector('.feedback-button').addEventListener('click',()=>showFeedback(q, root)); }
function showFeedback(q, root) {
  const box=root.querySelector('.feedback-box'); box.classList.remove('hidden');
  box.innerHTML=`<label>Loại góp ý<select class="feedback-type"><option value="law_expired">Văn bản hết hiệu lực</option><option value="law_changed">Điều khoản thay đổi</option><option value="answer_wrong">Đáp án sai</option><option value="explanation_wrong">Giải thích sai</option><option value="unclear">Câu hỏi chưa rõ</option><option value="missing_basis">Thiếu căn cứ</option><option value="suggest_new_law">Đề xuất văn bản mới</option><option value="other">Khác</option></select></label><label>Nội dung góp ý<textarea class="feedback-text" rows="3" placeholder="Nội dung góp ý..."></textarea></label><button class="send-feedback secondary-button">Lưu góp ý trên thiết bị</button><p class="feedback-status" role="status"></p>`;
  box.querySelector('.send-feedback').addEventListener('click',()=>{
    const content=box.querySelector('.feedback-text').value.trim();
    if(!content) { box.querySelector('.feedback-status').textContent='Vui lòng nhập nội dung góp ý.'; return; }
    const item={questionId:q.id,category:box.querySelector('.feedback-type').value,content,createdAt:new Date().toISOString(),examCode:state.examCode,variant:q.variant,answerOrder:q.answers.map(a=>a.id)};
    try {
      const list=JSON.parse(localStorage.getItem('questionFeedback')||'[]');
      if (!Array.isArray(list)) throw new Error('Invalid feedback');
      list.push(item); localStorage.setItem('questionFeedback',JSON.stringify(list));
      box.innerHTML='<strong>✓ Đã lưu góp ý trên thiết bị này.</strong><p>Góp ý không tự động thay đổi câu hỏi.</p>';
    } catch { box.querySelector('.feedback-status').textContent='Không thể lưu góp ý. Hãy sao chép nội dung trước khi rời trang.'; }
  });
}

document.querySelector('#practiceMode').addEventListener('click',()=>showSetup('practice'));
document.querySelector('#mockMode').addEventListener('click',()=>showSetup('mock'));
document.querySelector('#exitQuiz').addEventListener('click',()=>{stopTimer();els.quiz.classList.add('hidden');});
els.prev.addEventListener('click',()=>{if(state.current>0){state.current--;renderQuestion();}});
els.next.addEventListener('click',next);
document.addEventListener('visibilitychange',checkDeadline);
window.addEventListener('focus',checkDeadline);
const modeButtons = [document.querySelector('#practiceMode'), document.querySelector('#mockMode')];
modeButtons.forEach(b=>{b.disabled=true;});
loadQuestions().then(q=>{state.bank=q;modeButtons.forEach(b=>{b.disabled=false;});}).catch(e=>document.querySelector('main').insertAdjacentHTML('beforeend',`<p class="result-panel" role="alert">${escapeHtml(e.message)} Vui lòng tải lại trang.</p>`));
