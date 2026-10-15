const state = {
  bank: [], feedbackConfig: null, mode: null, part: null, questions: [], current: 0,
  selected: new Set(), answers: {}, results: {}, score: 0, answered: false,
  examCode: '', duration: 0, remaining: 0, timerId: null, submitted: false, reviewing: false, deadline: 0, startedAt: '', submittedAt: '', learnerName: '', learnerKey: '', attemptId: ''
};

const els = {
  setup: document.querySelector('#setup'), quiz: document.querySelector('#quiz'), result: document.querySelector('#result'),
  questionArea: document.querySelector('#questionArea'), quizMode: document.querySelector('#quizMode'), quizTitle: document.querySelector('#quizTitle'),
  examCode: document.querySelector('#examCode'), timer: document.querySelector('#timer'), progressText: document.querySelector('#progressText'),
  scoreText: document.querySelector('#scoreText'), progressBar: document.querySelector('#progressBar'), examShare: document.querySelector('#examShare'), prev: document.querySelector('#prevQuestion'), next: document.querySelector('#nextQuestion')
};

const shuffle = (items, random = Math.random) => { const a = [...items]; for (let i=a.length-1;i>0;i--) { const j=Math.floor(random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const eligibleQuestion = q => ['active', 'verified'].includes(q.status);
const hasResult = q => Object.hasOwn(state.results, q.id);
const isReviewing = () => state.submitted || state.reviewing;
const correctIds = q => new Set(q.answers.filter(a => a.correct).map(a => a.id));
const sameSet = (a,b) => a.size === b.size && [...a].every(x => b.has(x));

// CC1 fixes both the PRNG and draw order. Change the code version if either changes.
function seededRandom(seed) {
  let value = seed >>> 0;
  return () => {
    value = (value + 0x6D2B79F5) >>> 0;
    let t = Math.imul(value ^ (value >>> 15), 1 | value);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function fingerprint(text) {
  let hash = 0xcbf29ce484222325n;
  for (let i=0;i<text.length;i++) hash = BigInt.asUintN(64, (hash ^ BigInt(text.charCodeAt(i))) * 0x100000001b3n);
  return hash.toString(16).padStart(16,'0').toUpperCase();
}
function examPool(bank, part) {
  return bank.filter(q=>eligibleQuestion(q) && q.part===part).sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);
}
function bankVersion(pool) { return fingerprint(JSON.stringify(pool)); }
function createSharedExam(bank, part, count, duration, seed) {
  const pool=examPool(bank, part);
  if (!pool.length) throw new Error('Chưa có câu hỏi đủ điều kiện cho bài này.');
  const actualCount=Math.min(count,pool.length), random=seededRandom(seed);
  const questions=shuffle(pool,random).slice(0,actualCount).map(q=>({
    ...q, variant:q.question.variants[Math.floor(random()*q.question.variants.length)], answers:shuffle(q.answers,random)
  }));
  const body=`CC1-${part}-${actualCount}-${duration}-${(seed>>>0).toString(16).padStart(8,'0').toUpperCase()}-${bankVersion(pool)}`;
  return {questions,code:`${body}-${fingerprint(body).slice(0,8)}`};
}
// CC2 records selected pool positions; its seed fixes variants and answer order.
// Unlike CC1, reproduction never depends on a learner's local history.
function createSelectedExam(bank, part, selected, duration, seed) {
  const pool=examPool(bank,part), positions=new Map(pool.map((q,i)=>[q.id,i]));
  const indices=selected.map(q=>positions.get(q.id));
  if (!indices.length || indices.some(i=>i===undefined) || new Set(indices).size!==indices.length) throw new Error('Bộ câu hỏi không hợp lệ.');
  const random=seededRandom(seed);
  const questions=indices.map(i=>{const q=pool[i];return {...q,variant:q.question.variants[Math.floor(random()*q.question.variants.length)],answers:shuffle(q.answers,random)};});
  const body=`CC2-${part}-${indices.length}-${duration}-${(seed>>>0).toString(16).padStart(8,'0').toUpperCase()}-${bankVersion(pool)}-${indices.map(i=>i.toString(36).toUpperCase()).join('.')}`;
  return {questions,code:`${body}-${fingerprint(body).slice(0,8)}`};
}
function parseExamCode(raw, bank) {
  const code=raw.trim().toUpperCase();
  if (code.startsWith('CC2-')) {
    const match=/^CC2-([12])-([1-9]\d{0,3})-(15|30|60|90)-([0-9A-F]{8})-([0-9A-F]{16})-([0-9A-Z]+(?:\.[0-9A-Z]+)*)-([0-9A-F]{8})$/.exec(code);
    if (!match || code.length>8192) throw new Error('Mã đề không hợp lệ. Hãy sao chép đầy đủ mã CC2.');
    const body=code.slice(0,code.lastIndexOf('-'));
    if(fingerprint(body).slice(0,8)!==match[7]) throw new Error('Mã đề bị sai hoặc thiếu ký tự.');
    const part=Number(match[1]),count=Number(match[2]),duration=Number(match[3]),seed=parseInt(match[4],16),pool=examPool(bank,part);
    if(bankVersion(pool)!==match[5]) throw new Error('Ngân hàng câu hỏi khác phiên bản của mã đề. Người tạo cần tạo mã mới.');
    const indices=match[6].split('.').map(x=>parseInt(x,36));
    if(indices.length!==count || new Set(indices).size!==count || indices.some(i=>!Number.isSafeInteger(i)||i<0||i>=pool.length)) throw new Error('Mã đề chứa bộ câu hỏi không hợp lệ.');
    return {part,count,duration,seed,indices,code};
  }
  const match=/^CC1-([12])-([1-9]\d{0,3})-(15|30|60|90)-([0-9A-F]{8})-([0-9A-F]{16})-([0-9A-F]{8})$/.exec(code);
  if (!match) throw new Error('Mã đề không hợp lệ. Hãy sao chép đầy đủ mã CC1 mới từ người tạo đề.');
  const body=code.slice(0,code.lastIndexOf('-'));
  if (fingerprint(body).slice(0,8)!==match[6]) throw new Error('Mã đề bị sai hoặc thiếu ký tự. Hãy sao chép lại mã.');
  const part=Number(match[1]),count=Number(match[2]),duration=Number(match[3]),seed=parseInt(match[4],16),pool=examPool(bank,part);
  if (bankVersion(pool)!==match[5]) throw new Error('Ngân hàng câu hỏi khác phiên bản của mã đề. Hãy tải lại trang; nếu vẫn lỗi, người tạo cần tạo mã mới để cả nhóm dùng cùng phiên bản.');
  if (count>pool.length) throw new Error('Mã đề yêu cầu nhiều câu hơn ngân hàng hiện có.');
  return {part,count,duration,seed,code};
}
function startSharedExam(raw) {
  const params=parseExamCode(raw,state.bank);
  state.mode='mock'; startSession(params.part,params.count,params.duration,params.seed,params.indices);
}
function shareMarkup() {
  return `<div class="share-exam"><label>Mã đề để cùng làm<textarea class="share-code" rows="2" readonly aria-label="Mã đề để chia sẻ">${escapeHtml(state.examCode)}</textarea></label><button class="copy-code secondary-button">Sao chép mã đề</button><p class="copy-status" role="status">Gửi mã này cho nhóm. Mỗi người có thời gian riêng từ lúc bắt đầu.</p></div>`;
}
function bindShare(root) {
  const button=root.querySelector('.copy-code'); if(!button)return;
  const field=root.querySelector('.share-code'),status=root.querySelector('.copy-status');
  button.addEventListener('click',async()=>{
    try { await navigator.clipboard.writeText(field.value); status.textContent='Đã sao chép mã đề. Dán mã để gửi cho nhóm.'; }
    catch { field.focus(); field.select(); status.textContent='Hãy nhấn giữ hoặc chọn và sao chép mã trong ô phía trên.'; }
  });
}

async function loadQuestions() {
  const files = ['questions.json', 'derived-questions.json', 'validated-2026.json', 'imported-exams-2026.json', 'imported-deposit-2026.json', 'imported-authorization-2026.json', 'imported-family-2026.json', 'imported-inheritance-2026.json', 'completion-2026.json', 'refinement-2026.json', 'verified-new-2026.json', 'calibration-20-2026.json', 'calibration-40-2026.json', 'calibration-next-40-2026.json', 'hard-integrated-100-2026.json'];
  const batches = await Promise.all(files.map(async file => {
    const response = await fetch(`./data/${file}`, {cache: 'no-cache'});
    if (!response.ok) throw new Error(`Không thể tải ngân hàng câu hỏi (${file}).`);
    const questions = await response.json();
    if (!Array.isArray(questions)) throw new Error(`Ngân hàng câu hỏi không hợp lệ (${file}).`);
    return questions;
  }));
  const all = batches.flat(), ids = new Set();
  for (const q of all) {
    if (!q || typeof q.id !== 'string' || ids.has(q.id)) throw new Error('Ngân hàng có mã câu thiếu hoặc trùng.');
    ids.add(q.id);
  }
  const response = await fetch('./data/application-wording-2026.json', {cache: 'no-cache'});
  if (!response.ok) throw new Error('Không thể tải bản câu hỏi tình huống.');
  const worded = await applyApplicationWording(all, await response.json());
  const refinements = await fetch('./data/scenario-refinements-2026.json', {cache: 'no-cache'});
  if (!refinements.ok) throw new Error('Không thể tải tình huống đã rà soát.');
  const reviewed = await applyScenarioRefinements(worded, await refinements.json());
  const remaining = await fetch('./data/scenario-refinements-remaining-2026.json', {cache: 'no-cache'});
  if (!remaining.ok) throw new Error('Không thể tải tình huống bổ sung đã rà soát.');
  const enhanced = await applyScenarioRefinements(reviewed, await remaining.json());
  const priority = await fetch('./data/scenario-priority-129-2026.json', {cache: 'no-cache'});
  if (!priority.ok) throw new Error('Không thể tải nhóm câu hỏi ưu tiên đã rà soát.');
  const prioritized = await applyScenarioRefinements(enhanced, await priority.json());
  const application = await fetch('./data/scenario-application-40-2026.json', {cache: 'no-cache'});
  if (!application.ok) throw new Error('Không thể tải nhóm tình huống nâng độ khó.');
  const applied = await applyScenarioRefinements(prioritized, await application.json());
  const continuation = await fetch('./data/scenario-continuation-60-2026.json', {cache: 'no-cache'});
  if (!continuation.ok) throw new Error('Không thể tải nhóm 60 tình huống nâng độ khó tiếp theo.');
  const continued = await applyScenarioRefinements(applied, await continuation.json());
  const polish = await fetch('./data/editorial-polish-2026.json', {cache:'no-cache'});
  if (!polish.ok) throw new Error('Không thể tải bản biên tập câu hỏi.');
  const polished = await applyEditorialPolish(continued, await polish.json());
  const answers = await fetch('./data/answer-review-2026.json', {cache:'no-cache'});
  if (!answers.ok) throw new Error('Không thể tải bản biên tập phương án trả lời.');
  return applyAnswerReview(polished, await answers.json());
}

async function applyApplicationWording(bank, profile) {
  if (!profile || profile.version !== 1 || !Array.isArray(profile.questions))
    throw new Error('Bản câu hỏi tình huống không hợp lệ.');
  const originals = new Map(bank.map(q => [q.id, q])), revisions = new Map();
  await Promise.all(profile.questions.map(async row => {
    const q = originals.get(row?.id);
    if (!q || revisions.has(row.id) || !/^[a-f0-9]{64}$/.test(row.sourceSha256 || ''))
      throw new Error('Bản câu hỏi tình huống có mã thiếu, trùng hoặc nguồn không hợp lệ.');
    if (row.status !== undefined && row.status !== 'archived')
      throw new Error('Bản câu hỏi tình huống không được tự thay trạng thái kiểm định.');
    if (row.status !== 'archived' && (!Array.isArray(row.variants) || !row.variants.length ||
        row.variants.some(v => typeof v !== 'string' || !v.trim()) || new Set(row.variants).size !== row.variants.length))
      throw new Error('Cách hỏi tình huống không hợp lệ.');
    revisions.set(row.id, row);
    const bytes = new TextEncoder().encode(JSON.stringify({question:q.question, answers:q.answers, legalBasis:q.legalBasis}));
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const sha = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    if (sha !== row.sourceSha256)
      throw new Error('Nguồn câu hỏi đã thay đổi; cần rà soát lại cách hỏi tình huống.');
  }));
  return bank.map(q => {
    const row = revisions.get(q.id);
    if (!row) return q;
    return {...q, ...(row.status === 'archived' ? {status:'archived'} :
      {question:{...q.question, variants:row.variants.slice()}}),
      presentationReview:'application-wording-2026-10-12'};
  });
}


async function applyScenarioRefinements(bank, profile) {
  if (!profile || profile.version !== 1 || !Array.isArray(profile.questions))
    throw new Error('Bản tình huống đã rà soát không hợp lệ.');
  const byId = new Map(bank.map(q => [q.id,q]));
  for (const row of profile.questions) {
    const old = byId.get(row?.id), q = row?.after;
    if (!old || !q || q.id !== old.id || q.part !== old.part || q.type !== old.type ||
        q.status !== old.status || !eligibleQuestion(old) || !Array.isArray(q.answers) || q.answers.length !== 4 ||
        q.answers.some(a => typeof a.id !== 'string' || typeof a.text !== 'string' || !a.text.trim() ||
          typeof a.correct !== 'boolean' || typeof a.explanation !== 'string' || !a.explanation.trim()) ||
        new Set(q.answers.map(a=>a.id)).size !== 4 ||
        JSON.stringify(q.answers.map(a=>a.id).slice().sort()) !== JSON.stringify(old.answers.map(a=>a.id).slice().sort()) ||
        JSON.stringify(q.answers.filter(a=>a.correct).map(a=>a.id).sort()) !== JSON.stringify(old.answers.filter(a=>a.correct).map(a=>a.id).sort()) ||
        !Array.isArray(q.answerKey) || JSON.stringify(q.answerKey.slice().sort()) !== JSON.stringify(q.answers.filter(a=>a.correct).map(a=>a.id).sort()) ||
        !Array.isArray(q.legalBasis) || !q.legalBasis.length || q.legalBasis.some(r=>!r.document || !r.article || !r.url?.startsWith('https://')))
      throw new Error('Tình huống không hợp lệ hoặc thay đổi khóa, bài, loại hay trạng thái chưa được phép.');
  }
  // Reuse the immutable-source check, including duplicate IDs and valid authored stems.
  await applyApplicationWording(bank, {version:1,questions:profile.questions.map(r=>({
    id:r.id, sourceSha256:r.sourceSha256, variants:r.after.question?.variants
  }))});
  const revisions = new Map(profile.questions.map(r=>[r.id,r.after]));
  return bank.map(q=>revisions.has(q.id) ? JSON.parse(JSON.stringify(revisions.get(q.id))) : q);
}

async function applyEditorialPolish(bank, profile) {
  const result = await applyScenarioRefinements(bank, profile);
  const originals = new Map(bank.map(q=>[q.id,q]));
  const metadata = q => {
    const {question,answers,explanation,answerKey,...rest}=q;
    const {variants,...questionRest}=question;
    return {...rest,question:questionRest,answers:answers.map(({text,explanation,...a})=>a)};
  };
  const sha = async q => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',
    new TextEncoder().encode(JSON.stringify(q)))),b=>b.toString(16).padStart(2,'0')).join('');
  await Promise.all(profile.questions.map(async row=>{
    const old=originals.get(row.id);
    if (JSON.stringify(metadata(old))!==JSON.stringify(metadata(row.after)) ||
        old.question.variants.length!==row.after.question.variants.length)
      throw new Error('Bản biên tập không được thay căn cứ, dữ kiện quản lý hoặc số biến thể.');
    if (await sha(old)!==row.beforeSha256 || await sha(row.after)!==row.afterSha256)
      throw new Error('Nội dung biên tập không khớp phiên bản đã rà soát.');
  }));
  return result;
}

async function applyAnswerReview(bank, profile) {
  if (!profile || profile.version !== 1 || !Array.isArray(profile.questions))
    throw new Error('Bản biên tập phương án trả lời không hợp lệ.');
  const originals = new Map(bank.map(q=>[q.id,q])), revisions = new Map();
  const sha = async q => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',
    new TextEncoder().encode(JSON.stringify(q)))),b=>b.toString(16).padStart(2,'0')).join('');
  const protectedAnswer = ({text,explanation,...rest})=>rest;
  await Promise.all(profile.questions.map(async row=>{
    const old=originals.get(row?.id), answers=row?.answers;
    if (!old || revisions.has(row.id) || !eligibleQuestion(old) || !Array.isArray(answers) || answers.length!==4 ||
        answers.some((a,i)=>!a || typeof a.text!=='string' || !a.text.trim() ||
          JSON.stringify(protectedAnswer(a))!==JSON.stringify(protectedAnswer(old.answers[i])) ||
          (a.explanation!==undefined && (typeof a.explanation!=='string' || !a.explanation.trim())) ||
          (old.answers[i].explanation!==undefined && a.explanation===undefined)) ||
        new Set(answers.map(a=>a.text.trim().toLocaleLowerCase('vi'))).size!==4)
      throw new Error('Phương án không hợp lệ hoặc thay đổi mã, thứ tự, khóa đáp án.');
    // Reserve before awaiting so duplicate rows cannot race through validation.
    revisions.set(row.id,{...old,answers:JSON.parse(JSON.stringify(answers))});
    if (await sha(old)!==row.beforeSha256 || await sha(revisions.get(row.id))!==row.afterSha256)
      throw new Error('Phương án trả lời không khớp phiên bản đã biên tập.');
  }));
  return bank.map(q=>revisions.get(q.id)||q);
}

function showSetup(mode) {
  document.querySelector('#learningProgress')?.classList.remove('hidden');
  document.querySelector('#sharedLeaderboard')?.classList.remove('hidden');
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
    <p class="eyebrow">Thi thử</p><h2>Cấu hình bài thi</h2>${window.ExamProgress?.nameMarkup() || ''}
    <div class="setup-grid"><label>Bài<select id="setupPart"><option value="1">Bài 1 · Pháp luật</option><option value="2">Bài 2 · Kỹ năng</option></select></label>
    <label>Số câu<select id="setupCount"><option>5</option><option>10</option><option>20</option><option>50</option><option>100</option></select></label>
    <label>Thời gian<select id="setupDuration"><option value="15">15 phút</option><option value="30">30 phút</option><option value="60">60 phút</option><option value="90">90 phút</option></select></label></div>
    <button id="startSetup" class="primary-button">Tạo đề mới & bắt đầu</button>
    <div class="join-exam"><h3>Cùng làm một đề</h3><label for="joinExamCode">Mã đề người khác chia sẻ</label><input id="joinExamCode" type="text" maxlength="8192" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="Dán mã CC2-... hoặc CC1-... vào đây" />
    <p>Mã quyết định bài, số câu và thời lượng. Mỗi người tự bắt đầu, rồi đối chiếu cùng số câu và đáp án để thảo luận.</p>
    <button id="joinExam" class="secondary-button">Nhập mã & bắt đầu thi</button><p id="joinStatus" role="alert"></p></div>`;
  document.querySelector('#startSetup').addEventListener('click', async () => {
    if (mode==='mock' && window.ExamProgress && !await window.ExamProgress.captureName(state)) return;
    const part = document.querySelector('#setupPart').value;
    const count = Number(document.querySelector('#setupCount').value);
    const duration = mode === 'mock' ? Number(document.querySelector('#setupDuration').value) : 0;
    startSession(part === 'all' ? null : Number(part), count, duration);
  });
  if (mode==='mock') document.querySelector('#joinExam').addEventListener('click',async()=>{
    try { if(window.ExamProgress && !await window.ExamProgress.captureName(state))return; startSharedExam(document.querySelector('#joinExamCode').value); }
    catch(error) { document.querySelector('#joinStatus').textContent=error.message; }
  });
}

// Recent-question history applies to independently generated sessions only.
// Shared exam codes retain their exact deterministic question order.
function historyKey() {
  return 'congchungvnd:recent-v2:' + (state.learnerKey || 'device');
}
function recentQuestionHistory(part) {
  let history=[];
  try {const saved=JSON.parse(localStorage.getItem(historyKey())||'[]');if(Array.isArray(saved))history=saved.filter(id=>typeof id==='string');} catch (_) {}
  // Preserve legacy history for anonymous users, including all-part practice.
  if (!state.learnerKey) for(const scope of new Set(['all',String(part)])) {
    try {const old=JSON.parse(localStorage.getItem('congchungvnd:recent-questions:'+scope)||'[]');if(Array.isArray(old))history.push(...old.filter(id=>typeof id==='string'));} catch (_) {}
  }
  return [...new Set(history)];
}
function recordQuestionHistory(questions, part) {
  const ids=questions.map(q=>q.id),picked=new Set(ids);
  try {localStorage.setItem(historyKey(),JSON.stringify([...ids,...recentQuestionHistory(part).filter(id=>!picked.has(id))].slice(0,2000)));} catch (_) {}
}
function competenceKey(q) {
  if(q.competenceId) return q.competenceId;
  // A shared article alone is too broad: also require the same legal answer.
  return JSON.stringify([q.legalBasis,q.answers.filter(a=>a.correct).map(a=>a.text.trim().toLocaleLowerCase('vi')).sort()]);
}
function chooseFreshQuestions(pool, count, part) {
  const history=recentQuestionHistory(part),rank=new Map(history.map((id,i)=>[id,i]));
  const picked=[],used=new Set(),topics=new Map(),levels=new Map();
  const candidates=shuffle(pool),competences=new Map(pool.map(q=>[q.id,competenceKey(q)]));
  const totalTopics=new Map(),totalLevels=new Map();
  for(const q of pool){totalTopics.set(q.topic,(totalTopics.get(q.topic)||0)+1);totalLevels.set(q.difficulty,(totalLevels.get(q.difficulty)||0)+1);}
  while(picked.length<Math.min(count,pool.length)) {
    const fresh=candidates.filter(q=>!rank.has(q.id));
    const available=fresh.length?fresh:candidates;
    const distinct=available.filter(q=>!used.has(competences.get(q.id)));
    const options=distinct.length?distinct:available;
    options.sort((a,b)=>{
      if(!fresh.length){const recency=(rank.get(b.id)??-1)-(rank.get(a.id)??-1);if(recency)return recency;}
      const balance=q=>(topics.get(q.topic)||0)/totalTopics.get(q.topic)+(levels.get(q.difficulty)||0)/totalLevels.get(q.difficulty);
      return balance(a)-balance(b);
    });
    const q=options[0];picked.push(q);candidates.splice(candidates.indexOf(q),1);used.add(competences.get(q.id));
    topics.set(q.topic,(topics.get(q.topic)||0)+1);levels.set(q.difficulty,(levels.get(q.difficulty)||0)+1);
  }
  return picked;
}

function startSession(part, count, duration, seed = null, indices = null) {
  stopTimer();
  const pool = state.bank.filter(q => eligibleQuestion(q) && (part === null || q.part === part));
  if (!pool.length) { alert('Chưa có câu hỏi đủ điều kiện cho bài này.'); return; }
  state.attemptId = crypto.randomUUID();
  state.reviewing = false; state.startedAt = new Date().toISOString(); state.submittedAt = '';
  state.part = part; state.current = 0; state.selected = new Set(); state.answers = {}; state.results = {}; state.score = 0; state.submitted = false;
  if (state.mode==='mock') {
    if (seed === null) {
      const chosen=chooseFreshQuestions(pool,count,part);
      const randomSeed=crypto.getRandomValues(new Uint32Array(1))[0];
      const shared=createSelectedExam(state.bank,part,chosen,duration,randomSeed);
      state.questions=shared.questions; state.examCode=shared.code;
    } else {
      const shared=indices
        ? createSelectedExam(state.bank,part,indices.map(i=>examPool(state.bank,part)[i]),duration,seed)
        : createSharedExam(state.bank,part,count,duration,seed);
      state.questions=shared.questions; state.examCode=shared.code;
    }
  } else {
    state.questions=chooseFreshQuestions(pool,count,part).map(q=>({...q,answers:shuffle(q.answers),variant:q.question.variants[Math.floor(Math.random()*q.question.variants.length)]}));
    state.examCode='';
  }
  recordQuestionHistory(state.questions,part);
  state.duration = duration; state.remaining = duration * 60; state.deadline = Date.now() + state.remaining * 1000;
  document.querySelector('#learningProgress')?.classList.add('hidden');
  document.querySelector('#sharedLeaderboard')?.classList.add('hidden');
  els.setup.classList.add('hidden'); els.result.classList.add('hidden'); els.quiz.classList.remove('hidden');
  if (state.mode === 'mock') startTimer(); else stopTimer();
  els.examShare.classList.toggle('hidden',state.mode!=='mock');
  els.examShare.innerHTML=state.mode==='mock'?shareMarkup():'';
  if (state.mode==='mock') bindShare(els.examShare);
  renderQuestion(); els.quiz.scrollIntoView({behavior:'smooth', block:'start'});
}

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
    <p><strong>Giải thích:</strong> ${escapeHtml(q.explanation || 'Chưa có giải thích.')}</p>
    ${q.answers.some(a=>a.explanation)?`<div class="option-explanations"><strong>Giải thích từng phương án</strong>${q.answers.map((a,i)=>`<p><strong>${String.fromCharCode(65+i)}. ${a.correct?'Đúng':'Sai'}</strong> · ${escapeHtml(a.text)}<br>${escapeHtml(a.explanation || '')}</p>`).join('')}</div>`:''}${basisMarkup(q)}`;
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
  document.querySelector('#learningProgress')?.classList.remove('hidden');
  document.querySelector('#sharedLeaderboard')?.classList.remove('hidden');
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
  document.querySelector('#learningProgress')?.classList.remove('hidden');
  document.querySelector('#sharedLeaderboard')?.classList.remove('hidden');
  els.quiz.classList.add('hidden'); els.result.classList.remove('hidden');
  const unanswered=state.questions.filter(q=>!state.answers[q.id]?.length).length;
  els.result.innerHTML=`<p class="eyebrow">${auto?'Hết giờ':'Đã nộp bài'}</p><h2>Kết quả thi thử</h2>${shareMarkup()}<div class="result-score">${state.score}/${state.questions.length}</div><p>${Math.round(state.score/state.questions.length*100)}% câu trả lời đúng · Điểm: ${(state.score/state.questions.length*10).toFixed(2)}/10.</p><p>Đúng: ${state.score} · Sai: ${state.questions.length-state.score-unanswered} · Chưa trả lời: ${unanswered}</p>
    ${window.ExamProgress?.resultMarkup(state) || ''}${resultQuestionsMarkup()}<button id="homeResult" class="primary-button">Về trang chính</button>`;
  bindResultFeedback(); bindShare(els.result);
  window.ExamProgress?.saveResult(state);
}
function reviewQuestion(id) {
  const idx=state.questions.findIndex(q=>q.id===id); if(idx<0)return;
  state.current=idx; state.reviewing=true; els.result.classList.add('hidden'); els.quiz.classList.remove('hidden'); renderQuestion();
}
function feedbackMarkup() { return '<button class="feedback-button">⚠ Góp ý câu hỏi / đáp án</button><div class="feedback-box hidden"></div>'; }
function bindFeedback(root, q) { root.querySelector('.feedback-button').addEventListener('click',()=>showFeedback(q, root)); }
const feedbackCategories=['law_expired','law_changed','answer_wrong','explanation_wrong','unclear','missing_basis','suggest_new_law','other'];
async function loadFeedbackConfig() {
  const response=await fetch('./data/feedback-config.json',{cache:'no-cache'});
  if (!response.ok) throw new Error('Chưa tải được cấu hình góp ý.');
  const config=await response.json();
  if (!/^https:\/\/[a-z0-9]+\.supabase\.co$/.test(config.url) || !config.publishableKey?.startsWith('sb_publishable_')) throw new Error('Cấu hình góp ý không hợp lệ.');
  state.feedbackConfig=config;
}
function localFeedback() {
  try { const rows=JSON.parse(localStorage.getItem('questionFeedback')||'[]'); return Array.isArray(rows)?rows:[]; }
  catch { return []; }
}
function saveLocalFeedback(item) {
  try {
    const rows=localFeedback(),index=rows.findIndex(x=>x.id===item.id);
    if(index<0)rows.push(item);else rows[index]=item;
    localStorage.setItem('questionFeedback',JSON.stringify(rows)); return true;
  } catch { return false; }
}
function feedbackPayload(item) {
  return {id:item.id,question_id:item.questionId,category:item.category,content:item.content,exam_code:item.examCode,mode:item.mode,variant:item.variant,answer_order:item.answerOrder,question_snapshot:item.questionSnapshot,client_created_at:item.createdAt};
}
async function postFeedback(item) {
  if(!state.feedbackConfig) await loadFeedbackConfig();
  const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),10000);
  try {
    const response=await fetch(`${state.feedbackConfig.url}/rest/v1/question_feedback`,{
      method:'POST',headers:{apikey:state.feedbackConfig.publishableKey,'Content-Type':'application/json',Prefer:'return=minimal'},
      body:JSON.stringify(feedbackPayload(item)),signal:controller.signal
    });
    if(!response.ok) {
      // A retry of the same receipt after a lost response must not create another row.
      const error=await response.json().catch(()=>({}));
      if (!(response.status===409 && error.code==='23505')) throw new Error('Không gửi được góp ý.');
    }
  } finally { clearTimeout(timeout); }
}
function showFeedback(q, root) {
  const box=root.querySelector('.feedback-box');box.classList.remove('hidden');
  const pending=localFeedback().filter(x=>x.id && x.delivery==='pending' && x.questionSnapshot);
  box.innerHTML=`<label>Loại góp ý<select class="feedback-type"><option value="law_expired">Văn bản hết hiệu lực</option><option value="law_changed">Điều khoản thay đổi</option><option value="answer_wrong">Đáp án sai</option><option value="explanation_wrong">Giải thích sai</option><option value="unclear">Câu hỏi chưa rõ</option><option value="missing_basis">Thiếu căn cứ</option><option value="suggest_new_law">Đề xuất văn bản mới</option><option value="other">Khác</option></select></label><label>Nội dung góp ý<textarea class="feedback-text" rows="3" maxlength="3000" placeholder="Nội dung cần kiểm tra hoặc đề xuất sửa..."></textarea></label><p>Góp ý được gửi về nơi rà soát chung, không tự thay đổi câu hỏi. Không nhập thông tin cá nhân nhạy cảm.</p><button class="send-feedback secondary-button">Gửi góp ý</button>${pending.length?`<button class="retry-feedback secondary-button">Gửi lại ${pending.length} góp ý đang chờ trên thiết bị</button>`:''}<p class="feedback-status" role="status"></p>`;
  let draft=null;
  const button=box.querySelector('.send-feedback'),status=box.querySelector('.feedback-status');
  button.addEventListener('click',async()=>{
    if(button.disabled)return;
    const content=box.querySelector('.feedback-text').value.trim(),category=box.querySelector('.feedback-type').value;
    if(!content || content.length>3000 || !feedbackCategories.includes(category)) {status.textContent='Vui lòng nhập nội dung góp ý từ 1 đến 3.000 ký tự và chọn loại góp ý.';return;}
    if(!draft || draft.content!==content || draft.category!==category) draft={
      id:crypto.randomUUID(),questionId:q.id,category,content,createdAt:new Date().toISOString(),examCode:state.examCode,mode:state.mode,
      variant:q.variant,answerOrder:q.answers.map(a=>a.id),questionSnapshot:{question:q.variant,topic:q.topic,answers:q.answers,explanation:q.explanation,legalBasis:q.legalBasis},delivery:'pending'
    };
    const saved=saveLocalFeedback(draft);button.disabled=true;status.textContent='Đang gửi góp ý...';
    try {
      await postFeedback(draft);draft.delivery='sent';saveLocalFeedback(draft);
      box.innerHTML=`<strong>✓ Đã gửi góp ý về nơi rà soát chung.</strong><p>Mã ghi nhận: ${escapeHtml(draft.id)}</p><p>Góp ý không tự động thay đổi câu hỏi.</p>`;
    } catch {
      button.disabled=false;status.textContent=saved?'Chưa gửi được. Đã giữ góp ý trên thiết bị; bấm Gửi góp ý để thử lại hoặc mở lại nút góp ý để gửi các góp ý đang chờ.':'Chưa gửi được và không lưu được trên thiết bị. Hãy sao chép nội dung trước khi rời trang rồi thử lại.';
    }
  });
  const retry=box.querySelector('.retry-feedback');
  if(retry)retry.addEventListener('click',async()=>{
    retry.disabled=true;button.disabled=true;let sent=0;
    for(const item of pending) {
      try {await postFeedback(item);item.delivery='sent';saveLocalFeedback(item);sent++;}catch {break;}
    }
    status.textContent=`Đã gửi ${sent}/${pending.length} góp ý đang chờ.`;
    button.disabled=false;if(sent===pending.length)retry.classList.add('hidden');else retry.disabled=false;
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
loadQuestions().then(q=>{state.bank=q;window.ExamProgress?.init(ids=>{const bank=state.bank;state.bank=bank.filter(q=>ids.includes(q.id));state.mode='practice';startSession(null,20,0);state.bank=bank;});modeButtons.forEach(b=>{b.disabled=false;});}).catch(e=>document.querySelector('main').insertAdjacentHTML('beforeend',`<p class="result-panel" role="alert">${escapeHtml(e.message)} Vui lòng tải lại trang.</p>`));

loadFeedbackConfig().catch(()=>{});
