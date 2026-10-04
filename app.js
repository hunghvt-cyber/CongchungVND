const state = {
  bank: [], mode: null, part: null, questions: [], current: 0,
  selected: new Set(), answers: {}, results: {}, score: 0, answered: false,
  examCode: '', duration: 0, remaining: 0, timerId: null, submitted: false
};

const els = {
  setup: document.querySelector('#setup'), quiz: document.querySelector('#quiz'), result: document.querySelector('#result'),
  questionArea: document.querySelector('#questionArea'), quizMode: document.querySelector('#quizMode'), quizTitle: document.querySelector('#quizTitle'),
  examCode: document.querySelector('#examCode'), timer: document.querySelector('#timer'), progressText: document.querySelector('#progressText'),
  scoreText: document.querySelector('#scoreText'), progressBar: document.querySelector('#progressBar'), prev: document.querySelector('#prevQuestion'), next: document.querySelector('#nextQuestion')
};

const shuffle = items => { const a = [...items]; for (let i=a.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
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
  state.mode = mode;
  els.quiz.classList.add('hidden'); els.result.classList.add('hidden');
  els.setup.classList.remove('hidden');
  const available = state.bank.length;
  els.setup.innerHTML = mode === 'practice' ? `
    <p class="eyebrow">Ôn tập</p><h2>Chọn nội dung</h2>
    <p class="lead">Ngân hàng hiện có <strong>${available}</strong> câu; câu vòng 2 đang ở trạng thái rà soát.</p>
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
  state.part = part; state.current = 0; state.selected = new Set(); state.answers = {}; state.results = {}; state.score = 0; state.submitted = false;
  const pool = state.bank.filter(q => part === null || q.part === part);
  state.questions = shuffle(pool).slice(0, Math.min(count, pool.length)).map(q => ({...q, answers: shuffle(q.answers), question: {...q.question, variants: [...q.question.variants]}}));
  state.examCode = state.mode === 'mock' ? makeExamCode() : '';
  state.duration = duration; state.remaining = duration * 60;
  els.setup.classList.add('hidden'); els.result.classList.add('hidden'); els.quiz.classList.remove('hidden');
  if (state.mode === 'mock') startTimer(); else stopTimer();
  renderQuestion(); els.quiz.scrollIntoView({behavior:'smooth', block:'start'});
}

function makeExamCode() { return `CC-${Date.now().toString(36).slice(-5).toUpperCase()}-${Math.floor(100+Math.random()*900)}`; }
function startTimer() { stopTimer(); updateTimer(); state.timerId = setInterval(() => { state.remaining--; updateTimer(); if (state.remaining <= 0) submitMock(true); }, 1000); }
function stopTimer() { if (state.timerId) clearInterval(state.timerId); state.timerId = null; }
function updateTimer() { if (state.mode !== 'mock') { els.timer.textContent=''; return; } const m=Math.floor(state.remaining/60), s=state.remaining%60; els.timer.textContent=`⏱ ${m}:${String(s).padStart(2,'0')}`; els.timer.classList.toggle('danger', state.remaining <= 60); }

function renderQuestion() {
  const q = state.questions[state.current]; if (!q) return;
  state.selected = new Set(state.answers[q.id] || []); state.answered = state.mode === 'practice' && !!state.results[q.id];
  const variant = q.question.variants[Math.floor(Math.random()*q.question.variants.length)];
  els.quizMode.textContent = state.mode === 'practice' ? 'Ôn tập' : 'Thi thử';
  els.quizTitle.textContent = q.topic;
  els.examCode.textContent = state.examCode ? `Mã đề ${state.examCode}` : '';
  els.progressText.textContent = `Câu ${state.current+1} / ${state.questions.length}`;
  els.scoreText.textContent = state.mode === 'practice' ? `Đúng ${state.score}` : `Đã làm ${Object.keys(state.answers).length}`;
  els.progressBar.style.width = `${((state.current+1)/state.questions.length)*100}%`;
  els.prev.disabled = state.current === 0;
  els.next.textContent = state.current === state.questions.length-1 ? (state.mode === 'mock' ? 'Nộp bài' : 'Hoàn thành') : (state.mode === 'practice' ? 'Trả lời & tiếp →' : 'Câu tiếp →');
  const selected = state.selected;
  els.questionArea.innerHTML = `<p class="question-text">${escapeHtml(variant)}</p>
    <p class="answer-hint">${q.type === 'multiple' ? 'Chọn tất cả đáp án đúng.' : 'Chọn một đáp án.'}</p>
    <div class="answers">${q.answers.map((a,i)=>`<button class="answer ${selected.has(a.id)?'selected':''}" data-answer-id="${escapeHtml(a.id)}"><span class="answer-key">${String.fromCharCode(65+i)}.</span><span>${escapeHtml(a.text)}</span></button>`).join('')}</div>
    <div id="explanation" class="explanation ${state.answered?'':'hidden'}"></div>
    <button id="feedbackButton" class="feedback-button">⚠ Góp ý câu hỏi</button><div id="feedbackBox" class="feedback-box hidden"></div>`;
  els.questionArea.querySelectorAll('.answer').forEach(b=>b.addEventListener('click',()=>toggleAnswer(b.dataset.answerId)));
  document.querySelector('#feedbackButton').addEventListener('click',()=>showFeedback(q));
  if (state.answered) renderReview(q, state.results[q.id]);
}

function toggleAnswer(id) {
  if (state.mode === 'practice' && state.answered) return;
  if (state.mode === 'mock' && state.submitted) return;
  if (state.questions[state.current].type === 'single') state.selected = new Set([id]);
  else state.selected.has(id) ? state.selected.delete(id) : state.selected.add(id);
  state.answers[state.questions[state.current].id] = [...state.selected];
  els.questionArea.querySelectorAll('.answer').forEach(b=>b.classList.toggle('selected',state.selected.has(b.dataset.answerId)));
}

function submitPractice() {
  if (state.answered || !state.selected.size) return !!state.answered;
  const q=state.questions[state.current], correct=correctIds(q), ok=sameSet(correct,state.selected);
  state.results[q.id]=ok; if(ok) state.score++; state.answered=true; state.answers[q.id]=[...state.selected]; renderReview(q,ok); els.scoreText.textContent=`Đúng ${state.score}`; return true;
}
function renderReview(q, ok) {
  els.questionArea.querySelectorAll('.answer').forEach(b=>{const a=q.answers.find(x=>x.id===b.dataset.answerId); b.classList.toggle('correct',a.correct); b.classList.toggle('wrong',!a.correct && state.selected.has(a.id));});
  const e=document.querySelector('#explanation'); e.classList.remove('hidden');
  e.innerHTML=`<strong>${ok?'✓ Đúng':'✗ Chưa chính xác'}</strong><p>${escapeHtml(q.explanation||'Chưa có giải thích.')}</p>${q.legalBasis?.length?`<div class="legal"><strong>Căn cứ pháp lý</strong>${q.legalBasis.map(x=>`<div>${escapeHtml(typeof x==='string'?x:[x.document,x.article,x.clause].filter(Boolean).join(' · '))}</div>`).join('')}</div>`:''}`;
}
function next() { if(state.mode==='practice'){if(!submitPractice()) return; if(state.current<state.questions.length-1){state.current++;renderQuestion();}else showPracticeResult();} else { if(state.current<state.questions.length-1){state.current++;renderQuestion();}else submitMock(false); } }
function submitMock(auto=false){ if(state.submitted)return; stopTimer(); state.submitted=true; state.questions.forEach(q=>{const sel=new Set(state.answers[q.id]||[]); state.results[q.id]=sameSet(correctIds(q),sel);}); state.score=Object.values(state.results).filter(Boolean).length; showMockResult(auto); }
function showPracticeResult(){els.quiz.classList.add('hidden');els.result.classList.remove('hidden');const wrong=state.questions.filter(q=>!state.results[q.id]);els.result.innerHTML=`<p class="eyebrow">Hoàn thành</p><h2>Kết quả ôn tập</h2><div class="result-score">${state.score}/${state.questions.length}</div><p>${Math.round(state.score/state.questions.length*100)}% câu trả lời đúng.</p><p>${wrong.length?`Bạn có <strong>${wrong.length}</strong> câu sai để ôn lại.`:'Tuyệt vời! Bạn không có câu sai.'}</p><button id="reviewWrong" class="secondary-button" ${wrong.length?'':'disabled'}>Ôn lại câu sai</button> <button id="homeResult" class="primary-button">Về trang chính</button>`;document.querySelector('#reviewWrong').addEventListener('click',()=>{state.questions=wrong;state.current=0;state.score=0;state.results={};state.answers={};state.mode='practice';els.result.classList.add('hidden');els.quiz.classList.remove('hidden');renderQuestion();});document.querySelector('#homeResult').addEventListener('click',()=>location.reload());}
function showMockResult(auto){els.quiz.classList.add('hidden');els.result.classList.remove('hidden');const wrong=state.questions.filter(q=>!state.results[q.id]);els.result.innerHTML=`<p class="eyebrow">${auto?'Hết giờ':'Đã nộp bài'}</p><h2>Kết quả thi thử</h2><p>Mã đề <strong>${state.examCode}</strong></p><div class="result-score">${state.score}/${state.questions.length}</div><p>${Math.round(state.score/state.questions.length*100)}% câu trả lời đúng.</p><div class="result-list"><h3>Danh sách câu sai</h3>${wrong.length?wrong.map((q,i)=>`<button class="result-question" data-qid="${q.id}">Câu ${state.questions.indexOf(q)+1}: ${escapeHtml(q.topic)}</button>`).join(''):'Không có câu sai.'}</div><button id="homeResult" class="primary-button">Về trang chính</button>`;document.querySelectorAll('.result-question').forEach(b=>b.addEventListener('click',()=>reviewQuestion(b.dataset.qid)));document.querySelector('#homeResult').addEventListener('click',()=>location.reload());}
function reviewQuestion(id){const idx=state.questions.findIndex(q=>q.id===id);if(idx<0)return;state.current=idx;els.result.classList.add('hidden');els.quiz.classList.remove('hidden');renderQuestion();}
function showFeedback(q){const box=document.querySelector('#feedbackBox');box.classList.remove('hidden');box.innerHTML=`<select id="feedbackType"><option value="law_expired">Văn bản hết hiệu lực</option><option value="law_changed">Điều khoản thay đổi</option><option value="answer_wrong">Đáp án sai</option><option value="explanation_wrong">Giải thích sai</option><option value="unclear">Câu hỏi chưa rõ</option><option value="missing_basis">Thiếu căn cứ</option><option value="suggest_new_law">Đề xuất văn bản mới</option><option value="other">Khác</option></select><textarea id="feedbackText" rows="3" placeholder="Nội dung góp ý..."></textarea><button id="sendFeedback" class="secondary-button">Gửi góp ý</button>`;document.querySelector('#sendFeedback').addEventListener('click',()=>{const item={questionId:q.id,category:document.querySelector('#feedbackType').value,content:document.querySelector('#feedbackText').value.trim(),createdAt:new Date().toISOString()};if(!item.content)return;const list=JSON.parse(localStorage.getItem('questionFeedback')||'[]');list.push(item);localStorage.setItem('questionFeedback',JSON.stringify(list));box.innerHTML='<strong>✓ Đã ghi nhận góp ý.</strong><p>Góp ý không tự động thay đổi câu hỏi.</p>';});}

document.querySelector('#practiceMode').addEventListener('click',()=>showSetup('practice'));
document.querySelector('#mockMode').addEventListener('click',()=>showSetup('mock'));
document.querySelector('#exitQuiz').addEventListener('click',()=>{stopTimer();els.quiz.classList.add('hidden');});
els.prev.addEventListener('click',()=>{if(state.current>0){state.current--;renderQuestion();}});
els.next.addEventListener('click',next);
loadQuestions().then(q=>{state.bank=q;}).catch(e=>document.querySelector('main').insertAdjacentHTML('beforeend',`<p class="result-panel">${escapeHtml(e.message)}</p>`));
