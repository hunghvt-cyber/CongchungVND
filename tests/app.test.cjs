const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

// Minimal DOM surface for logic/HTML regression tests. No browser dependency.
class Element {
  constructor() {
    this.innerHTML=''; this.value=''; this.textContent=''; this.disabled=false; this.style={}; this.dataset={}; this.listeners={}; this.classes=new Set();
    this.classList={add: (...xs)=>xs.forEach(x=>this.classes.add(x)),remove: (...xs)=>xs.forEach(x=>this.classes.delete(x)),toggle:(x,on)=>on?this.classes.add(x):this.classes.delete(x),contains:x=>this.classes.has(x)};
    this.children=new Map();
  }
  addEventListener(type, fn) { this.listeners[type]=fn; }
  querySelector(selector) { if(!this.children.has(selector))this.children.set(selector,new Element()); return this.children.get(selector); }
  querySelectorAll() { return []; }
  scrollIntoView() {}
  insertAdjacentHTML(position, html) { this.innerHTML+=html; }
}
function harness() {
  const document=new Element();
  const memory=new Map();
  let now=1000000;
  const context=vm.createContext({document, window:new Element(), location:{reload(){}},
    localStorage:{getItem:k=>memory.get(k)??null,setItem:(k,v)=>memory.set(k,v)},
    fetch:async()=>({ok:true,json:async()=>[]}), alert:msg=>{context.alertMessage=msg;},
    crypto:require('node:crypto').webcrypto,AbortController,setTimeout,clearTimeout,Date:class extends Date {static now(){return now;}}, setInterval:()=>1,clearInterval(){},console});
  vm.runInContext(fs.readFileSync('app.js','utf8')+'\n globalThis.app={state,els,loadQuestions,showSetup,startSession,createSharedExam,parseExamCode,startSharedExam,renderQuestion,toggleAnswer,submitPractice,next,submitMock,showMockResult,showPracticeResult,reviewQuestion,checkDeadline,showFeedback,postFeedback,localFeedback,saveLocalFeedback,answerSummary};',context);
  return {...context.app, context, document, memory, advance:ms=>{now+=ms;}};
}
function question(id, status='active', type='single') {
  return {id,status,part:1,topic:'Kiểm tra <an toàn>',type,question:{variants:['Cách hỏi 1 '+id,'Cách hỏi 2 '+id]},answers:[{id:'A',text:'Đúng <A>',correct:true},{id:'B',text:'Sai B',correct:false},{id:'C',text:'Đúng C',correct:type==='multiple'}],explanation:'Giải thích <nội dung>',legalBasis:[{document:'Luật Công chứng số 46/2024/QH15',article:'Điều 2',url:'https://chinhphu.vn/?docid=212474&pageid=27160'}]};
}
function start(h, mode, questions, count=questions.length) {h.state.bank=questions;h.state.mode=mode;h.startSession(1,count,15);}

test('only active/verified questions enter either mode, unavailable part stays in setup',()=>{
  for(const mode of ['practice','mock']) {
    const h=harness();start(h,mode,['active','verified','review','needs_review','draft','archived'].map((s,i)=>question(String(i),s)));
    assert.equal(h.state.questions.length,2);assert.ok(h.state.questions.every(q=>['active','verified'].includes(q.status)));
    h.startSession(2,5,15);assert.match(h.context.alertMessage,/Chưa có câu hỏi/);assert.equal(h.state.timerId,null);
  }
});
test('question variants and displayed answer order stay fixed on revisit',()=>{
  const h=harness();start(h,'mock',[question('one'),question('two')]);
  const original=h.els.questionArea.innerHTML;
  const snapshot=JSON.stringify(h.state.questions);
  for(let i=0;i<20;i++){h.state.current=1;h.renderQuestion();h.state.current=0;h.renderQuestion();assert.equal(h.els.questionArea.innerHTML,original);}
  assert.equal(JSON.stringify(h.state.questions),snapshot);
  assert.match(h.document.querySelector('#explanation').innerHTML,/^$/);
});
test('incorrect practice answers stay locked on revisit and cannot change score',()=>{
  const h=harness();start(h,'practice',[question('one'),question('two')]);const q=h.state.questions[0];
  h.toggleAnswer('B');h.next();assert.equal(h.state.current,0);assert.equal(h.state.results[q.id],false);assert.equal(h.state.score,0);
  assert.match(h.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);
  h.next();h.state.current=0;h.renderQuestion();assert.equal(h.state.answered,true);
  h.toggleAnswer('A');h.submitPractice();assert.equal(h.state.results[q.id],false);assert.equal(h.state.score,0);
});
test('multiple choice scoring requires the entire correct set with no extras',()=>{
  const h=harness();start(h,'mock',[question('complete','active','multiple'),question('partial','active','multiple'),question('extra','active','multiple'),question('blank')]);
  h.state.answers={complete:['A','C'],partial:['A'],extra:['A','B','C']};h.submitMock();
  assert.equal(h.state.score,1);assert.equal(h.state.results.complete,true);assert.equal(h.state.results.partial,false);assert.equal(h.state.results.extra,false);assert.equal(h.state.results.blank,false);
});
test('results include correct, wrong and unanswered questions with explanations/basis/feedback',()=>{
  const h=harness();start(h,'mock',[question('right'),question('wrong'),question('blank')]);
  h.state.answers={right:['A'],wrong:['B']};h.submitMock();const html=h.els.result.innerHTML;
  assert.equal((html.match(/<details /g)||[]).length,3);assert.equal((html.match(/Đáp án đúng:/g)||[]).length,3);assert.equal((html.match(/Giải thích:/g)||[]).length,3);assert.equal((html.match(/Góp ý câu hỏi \/ đáp án/g)||[]).length,3);
  assert.match(html,/✓ Đúng/);assert.match(html,/✗ Sai/);assert.match(html,/Chưa trả lời/);assert.match(html,/Luật Công chứng số 46\/2024\/QH15/);assert.match(html,/Giải thích &lt;nội dung&gt;/);
  const before=h.state.score;h.reviewQuestion('right');assert.match(h.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);h.toggleAnswer('B');h.next();h.next();h.next();assert.equal(h.state.score,before);assert.ok(!h.els.result.classList.contains('hidden'));
});
test('answer labels in review follow shuffled positions instead of original IDs',()=>{
  const h=harness();const q=question('one');q.answers=[q.answers[1],q.answers[2],q.answers[0]];
  assert.equal(h.answerSummary(q,['A']),'C. Đúng &lt;A&gt;');
});
test('deadline uses elapsed time, auto-submits once and rejects late selections',()=>{
  const h=harness();start(h,'mock',[question('one')]);h.advance(15*60*1000+10000);h.toggleAnswer('A');
  assert.equal(h.state.submitted,true);assert.equal(h.state.remaining,0);assert.equal(h.state.score,0);assert.equal(h.state.timerId,null);assert.match(h.els.result.innerHTML,/Hết giờ/);
  h.submitMock();assert.equal(h.state.score,0);
});
test('deselecting all multiple answers removes answered count, switching mode stops timer',()=>{
  const h=harness();start(h,'mock',[question('one','active','multiple')]);h.toggleAnswer('A');assert.match(h.els.scoreText.textContent,/1$/);h.toggleAnswer('A');assert.equal(Object.keys(h.state.answers).length,0);assert.match(h.els.scoreText.textContent,/0$/);
  h.showSetup('practice');assert.equal(h.state.timerId,null);
});
test('feedback on separate answer cards sends central receipt, validates text and handles offline/local failure',async()=>{
  const h=harness();start(h,'mock',[question('one'),question('two')]);h.submitMock();
  h.state.feedbackConfig={url:'https://test.supabase.co',publishableKey:'sb_publishable_test'};
  for(const q of h.state.questions) {
    const root=new Element();h.showFeedback(q,root);const box=root.querySelector('.feedback-box');
    await box.querySelector('.send-feedback').listeners.click();assert.match(box.querySelector('.feedback-status').textContent,/Vui lòng/);
    box.querySelector('.feedback-text').value=' Cần kiểm tra '+q.id;box.querySelector('.feedback-type').value='answer_wrong';await box.querySelector('.send-feedback').listeners.click();
  }
  const stored=JSON.parse(h.memory.get('questionFeedback'));assert.equal(stored.length,2);assert.notEqual(stored[0].questionId,stored[1].questionId);assert.ok(stored.every(x=>x.examCode===h.state.examCode && x.variant && x.answerOrder.length===3));
  h.context.localStorage.setItem=()=>{throw Error('blocked');};h.context.fetch=async()=>{throw Error('offline');};const root=new Element();h.showFeedback(h.state.questions[0],root);const box=root.querySelector('.feedback-box');box.querySelector('.feedback-text').value='Không mất nội dung';box.querySelector('.feedback-type').value='other';await box.querySelector('.send-feedback').listeners.click();assert.match(box.querySelector('.feedback-status').textContent,/không lưu được/);
});
test('real published bank has unique IDs and only reviewed content enters either mode',()=>{
  const all=['questions','derived-questions','validated-2026','imported-exams-2026','imported-deposit-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
  assert.equal(new Set(all.map(q=>q.id)).size,all.length);
  assert.equal(all.filter(q=>q.id.startsWith('VER26-') && ['active','verified'].includes(q.status)).length,100);
  assert.doesNotMatch(JSON.stringify(all),/Luật [0-9]/);assert.ok(all.every(q=>q.explanation&&q.legalBasis.length));
  const h=harness();start(h,'mock',all,100);assert.ok(h.state.questions.every(q=>['active','verified'].includes(q.status)));
});

test('loader loads validated bank, rejects corrupt/duplicate data, and leaves stored history intact',async()=>{
  const h=harness(); await new Promise(resolve=>setImmediate(resolve));
  h.memory.set('exam-history-proof','saved snapshot'); const seen=[];
  h.context.fetch=async url=>{seen.push(url);return {ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))};};
  const all=await h.loadQuestions();assert.equal(all.length,220+JSON.parse(fs.readFileSync('data/imported-exams-2026.json','utf8')).length+JSON.parse(fs.readFileSync('data/imported-deposit-2026.json','utf8')).length);assert.ok(all.some(q=>q.id==='VER26-100'));
  assert.equal(seen.length,5);assert.ok(seen.every(url=>!url.includes('expansion')));assert.equal(h.memory.get('exam-history-proof'),'saved snapshot');
  h.context.fetch=async()=>({ok:true,json:async()=>[question('duplicate')]});await assert.rejects(h.loadQuestions(),/trùng/);
  h.context.fetch=async()=>({ok:true,json:async()=>({questions:[]})});await assert.rejects(h.loadQuestions(),/không hợp lệ/);
  h.context.fetch=async()=>({ok:false});await assert.rejects(h.loadQuestions(),/Không thể tải/);
});


test('one shared code reproduces full exam in independent sessions with separate answers/deadlines',()=>{
  const bank=['questions','derived-questions','validated-2026','imported-exams-2026','imported-deposit-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
  const creator=harness(),participant=harness();start(creator,'mock',bank,20);
  participant.state.bank=[...bank].reverse();participant.advance(5000);participant.startSharedExam('  '+creator.state.examCode.toLowerCase()+'  ');
  assert.equal(creator.state.examCode,participant.state.examCode);
  assert.equal(JSON.stringify(creator.state.questions),JSON.stringify(participant.state.questions));
  assert.equal(creator.state.duration,participant.state.duration);assert.equal(participant.state.deadline-creator.state.deadline,5000);
  creator.toggleAnswer(creator.state.questions[0].answers[0].id);assert.equal(Object.keys(participant.state.answers).length,0);
  assert.equal(participant.state.mode,'mock');assert.equal(participant.state.questions.length,20);
});
test('sharing records actual capped count and supports both parts and all durations',()=>{
  const h=harness();const bank=[question('one'),{...question('two'),part:2}];
  for(const part of [1,2])for(const duration of [15,30,60,90])for(const seed of [0,1,4294967295]){
    const exam=h.createSharedExam(bank,part,100,duration,seed),params=h.parseExamCode(exam.code,bank);
    assert.equal(params.count,1);assert.equal(params.part,part);assert.equal(params.duration,duration);assert.equal(params.seed,seed);
    assert.equal(h.createSharedExam(bank,params.part,params.count,params.duration,params.seed).code,exam.code);
  }
});
test('bad codes, old codes and changed bank are rejected without starting/resetting an attempt',()=>{
  const h=harness();start(h,'mock',[question('one'),question('two')]);const code=h.state.examCode;
  h.toggleAnswer('B');const saved=JSON.stringify(h.state.answers),deadline=h.state.deadline;
  for(const bad of ['', 'CC-OLD-123',code+'A',code.replace('-15-','-30-')]) assert.throws(()=>h.startSharedExam(bad),/Mã đề/);
  assert.equal(JSON.stringify(h.state.answers),saved);assert.equal(h.state.deadline,deadline);
  h.state.bank[0].explanation='Pháp luật đã cập nhật';assert.throws(()=>h.startSharedExam(code),/khác phiên bản/);
  assert.equal(JSON.stringify(h.state.answers),saved);assert.equal(h.state.deadline,deadline);
});
test('changes to pending questions cannot change a shared eligible exam',()=>{
  const h=harness(),bank=[question('one'),question('pending','review')];const exam=h.createSharedExam(bank,1,5,15,123);
  bank[1].explanation='Đang rà soát';assert.doesNotThrow(()=>h.parseExamCode(exam.code,bank));
  bank[1].status='verified';assert.throws(()=>h.parseExamCode(exam.code,bank),/khác phiên bản/);
});


test('offline feedback stays pending; retry uses same UUID and duplicate acknowledgement is accepted',async()=>{
  const h=harness();start(h,'mock',[question('one')]);h.state.feedbackConfig={url:'https://test.supabase.co',publishableKey:'sb_publishable_test'};
  const root=new Element();h.showFeedback(h.state.questions[0],root);const box=root.querySelector('.feedback-box');
  box.querySelector('.feedback-text').value='Kiểm tra đáp án';box.querySelector('.feedback-type').value='answer_wrong';
  let payloads=[];h.context.fetch=async(url,options)=>{payloads.push(JSON.parse(options.body));throw Error('offline');};
  await box.querySelector('.send-feedback').listeners.click();
  assert.equal(h.localFeedback()[0].delivery,'pending');assert.match(box.querySelector('.feedback-status').textContent,/Chưa gửi được/);
  h.context.fetch=async(url,options)=>{payloads.push(JSON.parse(options.body));return {ok:false,status:409,json:async()=>({code:'23505'})};};
  await box.querySelector('.send-feedback').listeners.click();
  assert.equal(payloads[0].id,payloads[1].id);assert.equal(h.localFeedback()[0].delivery,'sent');assert.match(box.innerHTML,/Đã gửi góp ý về nơi rà soát chung/);
  assert.equal(payloads[1].question_snapshot.question,h.state.questions[0].variant);assert.ok(!('review_status' in payloads[1]));
});
test('server error does not falsely acknowledge feedback, local storage failure still permits central send',async()=>{
  const h=harness();start(h,'mock',[question('one')]);h.state.feedbackConfig={url:'https://test.supabase.co',publishableKey:'sb_publishable_test'};
  h.context.localStorage.setItem=()=>{throw Error('quota');};h.context.fetch=async()=>({ok:false,status:500,json:async()=>({})});
  const root=new Element();h.showFeedback(h.state.questions[0],root);const box=root.querySelector('.feedback-box');box.querySelector('.feedback-text').value='Góp ý';box.querySelector('.feedback-type').value='other';
  await box.querySelector('.send-feedback').listeners.click();assert.doesNotMatch(box.innerHTML,/✓ Đã gửi/);assert.equal(box.querySelector('.send-feedback').disabled,false);
  h.context.fetch=async()=>({ok:true,status:201});await box.querySelector('.send-feedback').listeners.click();assert.match(box.innerHTML,/✓ Đã gửi/);
});

test('imported questions work in both parts, practice explanations and full mock scoring',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-exams-2026.json','utf8'));
 for(const part of [1,2]){
  const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(part,5,15);const first=practice.state.questions[0];practice.toggleAnswer(first.answers.find(a=>a.correct).id);practice.submitPractice();assert.equal(practice.state.score,1);assert.match(practice.document.querySelector('#explanation').innerHTML,/Gợi ý làm bài:/);
  const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(part,100,15);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,mock.state.questions.length);assert.ok(mock.state.questions.every(q=>q.status==='active'&&q.source.type==='user-provided'));assert.match(mock.els.result.innerHTML,/Gợi ý làm bài:/);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);
 }
});

test('deposit bank practices with explanations and grades a complete 18-question mock',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-deposit-2026.json','utf8'));
 const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(2,18,30);const first=practice.state.questions[0];practice.toggleAnswer(first.answers.find(a=>a.correct).id);practice.submitPractice();assert.equal(practice.state.score,1);assert.match(practice.document.querySelector('#explanation').innerHTML,/Gợi ý làm bài:/);
 const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(2,18,30);assert.equal(mock.state.questions.length,18);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,18);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);assert.match(mock.els.result.innerHTML,/Nghị định số 21/);
});
