const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {profile:polishProfile,answerProfile,sha:polishHash,polishedExpected,unpolishedVersion,beforeAnswerVersion}=require('./helpers/editorial-polish.cjs');

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
function harness(seed=20261015) {
  const document=new Element();
  const memory=new Map();
  let now=1000000;
  const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
  const math=Object.create(Math);math.random=random;
  const context=vm.createContext({document, window:new Element(), location:{reload(){}},
    localStorage:{getItem:k=>memory.get(k)??null,setItem:(k,v)=>memory.set(k,v)},
    fetch:async()=>({ok:true,json:async()=>[]}), alert:msg=>{context.alertMessage=msg;},
    Math:math,crypto:{randomUUID:require('node:crypto').randomUUID,subtle:require('node:crypto').webcrypto.subtle,getRandomValues:a=>{for(let i=0;i<a.length;i++)a[i]=Math.floor(random()*4294967296);return a;}},TextEncoder,AbortController,setTimeout,clearTimeout,Date:class extends Date {static now(){return now;}}, setInterval:()=>1,clearInterval(){},console});
  vm.runInContext(fs.readFileSync('app.js','utf8')+'\n globalThis.app={state,els,loadQuestions,applyEditorialPolish,applyApplicationWording,applyScenarioRefinements,showSetup,startSession,createSharedExam,createSelectedExam,fingerprint,chooseFreshQuestions,parseExamCode,startSharedExam,renderQuestion,toggleAnswer,submitPractice,next,submitMock,showMockResult,showPracticeResult,reviewQuestion,checkDeadline,showFeedback,postFeedback,localFeedback,saveLocalFeedback,answerSummary};',context);
  context.app.applyAnswerReview=vm.runInContext('applyAnswerReview',context);
  return {...context.app, context, document, memory, advance:ms=>{now+=ms;}};
}
function question(id, status='active', type='single') {
  return {id,status,part:1,topic:'Kiểm tra <an toàn>',type,question:{variants:['Cách hỏi 1 '+id,'Cách hỏi 2 '+id]},answers:[{id:'A',text:'Đúng <A>',correct:true},{id:'B',text:'Sai B',correct:false},{id:'C',text:'Đúng C',correct:type==='multiple'}],explanation:'Giải thích <nội dung>',legalBasis:[{document:'Luật Công chứng số 46/2024/QH15',article:'Điều 2',url:'https://chinhphu.vn/?docid=212474&pageid=27160'}]};
}
function start(h, mode, questions, count=questions.length) {h.state.bank=questions;h.state.mode=mode;h.startSession(1,count,15);}
function assertExplanation(html,q){
  const escaped=q.explanation.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  assert.ok(q.explanation.length>=100,q.id+' substantive explanation');
  assert.ok(html.includes(escaped),q.id+' full explanation rendered');
  assert.match(html,/Giải thích:/);assert.match(html,/Căn cứ pháp lý/);
}

test('the historical 80-question editorial layer remains exact beneath the answer review',async()=>{
 const {effectiveBank}=require('../scripts/lib/effective-bank.cjs');
 const before=effectiveBank(),h=harness();
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),rows=new Map(polishProfile.questions.map(r=>[r.id,r]));
 assert.equal(rows.size,80);assert.equal(bank.length,813);
 assert.equal(bank.filter(q=>q.status==='active').length,793);
 const metadata=q=>{const x=JSON.parse(JSON.stringify(q));for(const k of ['question','answers','explanation','answerKey'])delete x[k];return x;};
 for(const old of before){
  const current=beforeAnswerVersion(bank.find(q=>q.id===old.id)),r=rows.get(old.id);
  if(!r){assert.equal(JSON.stringify(current),JSON.stringify(old),old.id+' untouched');continue;}
  assert.equal(polishHash(old),r.beforeSha256,old.id);
  assert.equal(polishHash(current),r.afterSha256,old.id);
  assert.equal(JSON.stringify(current),JSON.stringify(r.after),old.id);
  assert.equal(JSON.stringify(metadata(current)),JSON.stringify(metadata(old)),old.id+' legal/verification metadata');
  assert.equal(current.question.variants.length,old.question.variants.length);
  assert.equal(JSON.stringify(current.answers.map(a=>[a.id,a.correct])),JSON.stringify(old.answers.map(a=>[a.id,a.correct])),old.id+' key');
  assert.ok(current.answers.every(a=>a.explanation.length>=12));
 }
 const get=id=>bank.find(q=>q.id===id);
 assert.ok(get('CC-010').question.variants.every(v=>v.includes('Lan')));
 assert.ok(get('CC-046').question.variants.every(v=>v.includes('01/01/2027')));
 assert.ok(get('DEP26-016').question.variants.every(v=>!v.includes('5%')));
 assert.ok(get('CAL26-015').question.variants.every(v=>!v.includes('tách khối')&&!v.includes('bảo vệ người')));
 assert.ok(get('HARD26-013').answers.every(a=>/^\d.*triệu đồng\.$/.test(a.text)));
});

test('answer review loads exact snapshots and preserves every question field and truth value',async()=>{
 const {effectiveBank}=require('../scripts/lib/effective-bank.cjs');
 const before=effectiveBank({polish:true}),h=harness();
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),rows=new Map(answerProfile.questions.map(r=>[r.id,r]));
 assert.equal(rows.size,465);assert.equal(bank.length,813);
 const protectedAnswer=({text,explanation,...rest})=>rest;
 for(const old of before){
  const q=bank.find(q=>q.id===old.id),r=rows.get(q.id);
  if(!r){assert.equal(JSON.stringify(q),JSON.stringify(old),q.id+' retained');continue;}
  assert.equal(polishHash(old),r.beforeSha256,q.id);
  assert.equal(polishHash(q),r.afterSha256,q.id);
  assert.equal(JSON.stringify(q.answers),JSON.stringify(r.answers),q.id);
  assert.equal(JSON.stringify({...q,answers:old.answers}),JSON.stringify(old),q.id+' question metadata');
  assert.equal(JSON.stringify(q.answers.map(protectedAnswer)),JSON.stringify(old.answers.map(protectedAnswer)),q.id+' truth values');
 }
 const report=JSON.parse(fs.readFileSync('reports/answer-review-2026-10-15.json','utf8'));
 assert.equal(report.decisions.length,793);assert.equal(new Set(report.decisions.map(d=>d.id)).size,793);
 assert.equal(report.summary.reviewedOptions,3172);
 for(const d of report.decisions){
  assert.equal(d.beforeSha256,polishHash(before.find(q=>q.id===d.id)),d.id);
  assert.equal(d.afterSha256,polishHash(bank.find(q=>q.id===d.id)),d.id);
 }
});

test('answer review rejects stale, duplicate, tampered, missing and key-changing revisions',async()=>{
 const {effectiveBank}=require('../scripts/lib/effective-bank.cjs'),before=effectiveBank({polish:true}),h=harness();
 const stale=structuredClone(before);stale.find(q=>q.id===answerProfile.questions[0].id).explanation+=' changed';
 await assert.rejects(h.applyAnswerReview(stale,answerProfile),/phiên bản/);
 for(const mutate of [p=>p.questions.push(p.questions[0]),p=>p.questions[0].answers[0].correct=!p.questions[0].answers[0].correct,
  p=>p.questions[0].answers.reverse(),p=>p.questions[0].answers[0].text=' ',p=>p.questions[0].answers[1].text=p.questions[0].answers[0].text,
  p=>p.questions[0].answers[0].text+=' tampered',p=>p.questions[0].id='unknown']){
  const bad=structuredClone(answerProfile);mutate(bad);
  await assert.rejects(h.applyAnswerReview(before,bad),/không hợp lệ|phiên bản/);
 }
 h.context.fetch=async url=>url.includes('answer-review')?{ok:false}:{ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))};
 await assert.rejects(h.loadQuestions(),/Không thể tải bản biên tập phương án/);
});

test('editorial loader rejects stale sources, changed law/verification metadata, changed keys and unreviewed text',async()=>{
 const {effectiveBank}=require('../scripts/lib/effective-bank.cjs'),before=effectiveBank(),h=harness();
 const first=polishProfile.questions[0];
 const stale=structuredClone(before);stale.find(q=>q.id===first.id).explanation+=' changed';
 await assert.rejects(h.applyEditorialPolish(stale,polishProfile),/phiên bản/);
 for(const mutate of [q=>q.legalBasis[0].article='invalid',q=>q.lastVerified='2099-01-01',q=>q.source.id='unreviewed',q=>q.answers[0].correct=!q.answers[0].correct,q=>q.status='archived',q=>q.question.variants.push('Extra authored variant')]){
  const bad=structuredClone(polishProfile);mutate(bad.questions[0].after);
  bad.questions[0].afterSha256=polishHash(bad.questions[0].after);
  await assert.rejects(h.applyEditorialPolish(before,bad),/khóa|căn cứ|biến thể/);
 }
 const tampered=structuredClone(polishProfile);tampered.questions[0].after.answers[0].text+=' unreviewed';
 await assert.rejects(h.applyEditorialPolish(before,tampered),/phiên bản/);
 const offline=harness();offline.context.fetch=async url=>url.includes('editorial-polish')?{ok:false}:{ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))};
 await assert.rejects(offline.loadQuestions(),/Không thể tải bản biên tập/);
});

test('second editorial batch adds forty disjoint cases and retains every approved first-batch hash',async()=>{
 const initial=JSON.parse(fs.readFileSync('reports/natural-language-polish-2026-10-15.json','utf8'));
 const report=JSON.parse(fs.readFileSync('reports/natural-language-polish-next-2026-10-15.json','utf8'));
 const rows=new Map(polishProfile.questions.map(r=>[r.id,r]));
 assert.equal(initial.decisions.length,40);assert.equal(report.thisBatchEdited,40);
 assert.equal(report.thisBatchIds.length,40);assert.equal(new Set(report.thisBatchIds).size,40);
 assert.ok(report.thisBatchIds.every(id=>!initial.decisions.some(d=>d.id===id)));
 for(const d of initial.decisions){const r=rows.get(d.id);assert.equal(r.beforeSha256,d.beforeSha256,d.id);assert.equal(r.afterSha256,d.afterSha256,d.id);}
 const h=harness();h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),next=bank.filter(q=>report.thisBatchIds.includes(q.id));
 assert.equal(next.length,40);assert.equal(next.reduce((n,q)=>n+q.question.variants.length,0),104);
 assert.ok(next.every(q=>q.question.variants.every(v=>!v.includes('cần phân biệt')&&!v.includes('theo nhánh'))));
 for(const id of ['CC-033','CC-099'])assert.ok(bank.find(q=>q.id===id).question.variants.every(v=>v.includes('01/01/2027')));
 const firstPayment=bank.find(q=>q.id==='IMP-SEP24-037');
 const millions=3000*0.3-150;assert.equal(millions,750);
 assert.equal(firstPayment.answers.find(a=>a.correct).text,`${millions} triệu đồng.`);
 assert.ok(firstPayment.answers.every(a=>/^\d[\d.]* triệu đồng\.$/.test(a.text)));
});

test('seeded question and answer selection is reproducible and multiple seeds exercise different orders',()=>{
 const bank=Array.from({length:12},(_,i)=>question(String(i)));
 const snapshot=seed=>{const h=harness(seed);start(h,'mock',bank,10);return JSON.stringify(h.state.questions);};
 assert.equal(snapshot(42),snapshot(42));assert.notEqual(snapshot(42),snapshot(43));
});

test('all 793 effective questions score every single selection, blank and all multiple subsets in both modes',async t=>{
 const loader=harness();loader.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=(await loader.loadQuestions()).filter(q=>['active','verified'].includes(q.status));
 assert.equal(bank.length,793);assert.ok(!bank.some(q=>q.id==='CC-082'));
 let cases=0;
 for(const mode of ['practice','mock']){
  const h=harness(mode==='practice'?101:202);
  for(const q of bank){
   assert.ok(q.explanation.length>=100,q.id);
   const correct=q.answers.filter(a=>a.correct).map(a=>a.id).sort();
   const choices=q.type==='multiple'
    ?Array.from({length:2**q.answers.length},(_,mask)=>q.answers.filter((a,i)=>mask&(1<<i)).map(a=>a.id))
    :[[],...q.answers.map(a=>[a.id])];
   for(const chosen of choices){
    h.state.bank=[q];h.state.mode=mode;h.startSession(q.part,1,15);for(const id of chosen)h.toggleAnswer(id);
    if(mode==='practice'&&!chosen.length){
     assert.equal(h.submitPractice(),false,q.id+' empty practice cannot submit');
     assert.equal(h.state.results[q.id],undefined);assert.equal(h.state.score,0);assert.equal(h.state.answered,false);
     assert.match(h.els.questionArea.innerHTML,/<div id="explanation" class="explanation hidden"><\/div>/);cases++;continue;
    }
    const expected=JSON.stringify(chosen.slice().sort())===JSON.stringify(correct);
    if(mode==='practice')h.submitPractice();else h.submitMock();
    assert.equal(h.state.results[q.id],expected,`${mode} ${q.id} ${chosen}`);
    assert.equal(h.state.score,Number(expected),`${mode} ${q.id} score`);
    assertExplanation(mode==='practice'?h.document.querySelector('#explanation').innerHTML:h.els.result.innerHTML,q);
    cases++;
   }
  }
 }
 assert.equal(cases,9690);t.diagnostic(`793 effective questions; ${cases} answer/scoring cases including blank-practice rejection; zero mismatches against stored keys (not legal recertification).`);
});

test('all repaired pending questions work in practice and mock; retired duplicates stay excluded',()=>{
 const decisions=JSON.parse(fs.readFileSync('reports/pending-review-decisions-2026.json','utf8')).decisions;
 const ids=new Set(decisions.map(d=>d.id));const bank=['questions','derived-questions'].flatMap(n=>JSON.parse(fs.readFileSync(`data/${n}.json`,'utf8'))).filter(q=>ids.has(q.id));
 for(const part of [1,2]){const expected=bank.filter(q=>q.part===part&&q.status==='active').length;
  const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(part,100,15);assert.equal(practice.state.questions.length,expected);
  for(let i=0;i<expected;i++){const q=practice.state.questions[i];practice.state.current=i;practice.renderQuestion();practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);assert.match(practice.document.querySelector('#explanation').innerHTML,/Điều/);}assert.equal(practice.state.score,expected);
  const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(part,100,15);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,expected);assert.ok(mock.state.questions.every(q=>q.status==='active'));
 }
});

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
  const all=['questions','derived-questions','validated-2026','imported-exams-2026','imported-deposit-2026','imported-authorization-2026','imported-family-2026','imported-inheritance-2026','completion-2026','refinement-2026','verified-new-2026','calibration-20-2026','calibration-40-2026','calibration-next-40-2026','hard-integrated-100-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
  assert.equal(new Set(all.map(q=>q.id)).size,all.length);
  assert.equal(all.filter(q=>q.id.startsWith('VER26-') && ['active','verified'].includes(q.status)).length,109);
  assert.doesNotMatch(JSON.stringify(all),/Luật [0-9]/);assert.ok(all.every(q=>q.explanation&&q.legalBasis.length));
  const h=harness();start(h,'mock',all,100);assert.ok(h.state.questions.every(q=>['active','verified'].includes(q.status)));
});

test('loader loads validated bank, rejects corrupt/duplicate data, and leaves stored history intact',async()=>{
  const h=harness(); await new Promise(resolve=>setImmediate(resolve));
  h.memory.set('exam-history-proof','saved snapshot'); const seen=[];
  h.context.fetch=async url=>{seen.push(url);return {ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))};};
  const all=await h.loadQuestions();assert.equal(all.length,220+JSON.parse(fs.readFileSync('data/imported-exams-2026.json','utf8')).length+JSON.parse(fs.readFileSync('data/imported-deposit-2026.json','utf8')).length+JSON.parse(fs.readFileSync('data/imported-authorization-2026.json','utf8')).length+26+32+JSON.parse(fs.readFileSync('data/completion-2026.json','utf8')).length+JSON.parse(fs.readFileSync('data/refinement-2026.json','utf8')).length+11+200);assert.ok(all.some(q=>q.id==='FAM26-026'));assert.ok(all.some(q=>q.id==='VER26-100'));
  assert.equal(seen.length,23);assert.equal(new Set(seen).size,23);assert.ok(seen.includes('./data/editorial-polish-2026.json'));assert.ok(seen.includes('./data/answer-review-2026.json'));assert.ok(seen.includes('./data/calibration-20-2026.json'));assert.ok(seen.includes('./data/verified-new-2026.json'));assert.ok(seen.includes('./data/completion-2026.json'));assert.ok(seen.includes('./data/refinement-2026.json'));assert.ok(seen.includes('./data/imported-inheritance-2026.json'));assert.ok(all.some(q=>q.id==='INH26-032'));assert.ok(seen.includes('./data/imported-family-2026.json'));assert.ok(seen.includes('./data/imported-authorization-2026.json'));assert.ok(seen.every(url=>!url.includes('expansion')));assert.equal(h.memory.get('exam-history-proof'),'saved snapshot');
  h.context.fetch=async()=>({ok:true,json:async()=>[question('duplicate')]});await assert.rejects(h.loadQuestions(),/trùng/);
  h.context.fetch=async()=>({ok:true,json:async()=>({questions:[]})});await assert.rejects(h.loadQuestions(),/không hợp lệ/);
  h.context.fetch=async()=>({ok:false});await assert.rejects(h.loadQuestions(),/Không thể tải/);
});


test('one shared code reproduces full exam in independent sessions with separate answers/deadlines',()=>{
  const bank=['questions','derived-questions','validated-2026','imported-exams-2026','imported-deposit-2026','imported-authorization-2026','imported-family-2026','imported-inheritance-2026','completion-2026','refinement-2026','verified-new-2026','calibration-20-2026','calibration-40-2026','calibration-next-40-2026','hard-integrated-100-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
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
  const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(part,5,15);const first=practice.state.questions[0];practice.toggleAnswer(first.answers.find(a=>a.correct).id);practice.submitPractice();assert.equal(practice.state.score,1);assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);
  const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(part,100,15);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,mock.state.questions.length);assert.ok(mock.state.questions.every(q=>q.status==='active'&&q.source.type==='user-provided'));mock.state.questions.forEach(q=>assertExplanation(mock.els.result.innerHTML,q));assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);
 }
});

test('deposit bank practices with explanations and grades a complete 18-question mock',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-deposit-2026.json','utf8'));
 const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(2,18,30);const first=practice.state.questions[0];practice.toggleAnswer(first.answers.find(a=>a.correct).id);practice.submitPractice();assert.equal(practice.state.score,1);assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);
 const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(2,18,30);assert.equal(mock.state.questions.length,18);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,18);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);assert.match(mock.els.result.innerHTML,/Nghị định số 21/);
});

test('authorization bank grades all 20 cases and retains explanations in practice and mock',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-authorization-2026.json','utf8'));
 const practice=harness();practice.state.bank=bank;practice.state.mode='practice';practice.startSession(2,20,30);
 for(let i=0;i<20;i++){const q=practice.state.questions[i];practice.state.current=i;practice.renderQuestion();practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);}
 assert.equal(practice.state.score,20);
 const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(2,20,30);assert.equal(mock.state.questions.length,20);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,20);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);assert.match(mock.els.result.innerHTML,/Luật Công chứng số 46/);
});

test('family bank grades all 26 cases, explains incorrect answers and preserves saved history',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-family-2026.json','utf8'));
 const practice=harness();practice.memory.set('existing-history','unchanged');practice.state.bank=bank;practice.state.mode='practice';practice.startSession(2,26,45);
 for(let i=0;i<26;i++){const q=practice.state.questions[i];practice.state.current=i;practice.renderQuestion();practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);assert.match(practice.document.querySelector('#explanation').innerHTML,/Điều/);}
 assert.equal(practice.state.score,26);assert.equal(practice.memory.get('existing-history'),'unchanged');
 const wrong=harness();wrong.state.bank=[bank[0]];wrong.state.mode='practice';wrong.startSession(2,1,45);wrong.toggleAnswer(wrong.state.questions[0].answers.find(a=>!a.correct).id);wrong.submitPractice();assert.equal(wrong.state.score,0);assert.match(wrong.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);
 const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(2,26,45);assert.equal(mock.state.questions.length,26);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,26);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);assert.match(mock.els.result.innerHTML,/Hôn nhân và gia đình/);
});

test('inheritance bank grades all 32 cases and explains wrong practice answers without modifying existing keys',()=>{
 const bank=JSON.parse(fs.readFileSync('data/imported-inheritance-2026.json','utf8'));
 const practice=harness();practice.memory.set('exam-history-proof','existing snapshot');practice.state.bank=bank;practice.state.mode='practice';practice.startSession(2,32,60);
 for(let i=0;i<32;i++){const q=practice.state.questions[i];practice.state.current=i;practice.renderQuestion();practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();assertExplanation(practice.document.querySelector('#explanation').innerHTML,practice.state.questions[practice.state.current]);assert.match(practice.document.querySelector('#explanation').innerHTML,/Điều/);}
 assert.equal(practice.state.score,32);assert.equal(practice.memory.get('exam-history-proof'),'existing snapshot');
 const wrong=harness();wrong.state.bank=[bank[0]];wrong.state.mode='practice';wrong.startSession(2,1,60);wrong.toggleAnswer(wrong.state.questions[0].answers.find(a=>!a.correct).id);wrong.submitPractice();assert.equal(wrong.state.score,0);assert.match(wrong.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);
 const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(2,32,60);assert.equal(mock.state.questions.length,32);for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);mock.submitMock();assert.equal(mock.state.score,32);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);assert.match(mock.els.result.innerHTML,/Bộ luật Dân sự/);
});

test('completion cases load in both parts, grade correctly after shuffling, and keep prior snapshots',()=>{
 const bank=JSON.parse(fs.readFileSync('data/completion-2026.json','utf8'));
 for(const part of [1,2]){
  const expected=bank.filter(q=>q.part===part&&q.status==='active').length;
  const practice=harness();practice.memory.set('previous-snapshot','original');practice.state.bank=bank;practice.state.mode='practice';practice.startSession(part,100,60);
  assert.equal(practice.state.questions.length,expected);
  for(let i=0;i<expected;i++){
   practice.state.current=i;practice.renderQuestion();const q=practice.state.questions[i];practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();
   const html=practice.document.querySelector('#explanation').innerHTML;assert.match(html,/Căn cứ pháp lý/);assert.match(html,/Xem văn bản/);assert.ok(html.includes(q.explanation.replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))));
  }
  assert.equal(practice.state.score,expected);assert.equal(practice.memory.get('previous-snapshot'),'original');
  const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(part,100,60);
  for(const q of mock.state.questions)mock.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);
  mock.submitMock();assert.equal(mock.state.score,expected);assert.match(mock.els.result.innerHTML,/Căn cứ pháp lý/);
  const wrong=harness();wrong.state.bank=[bank.find(q=>q.part===part)];wrong.state.mode='practice';wrong.startSession(part,1,60);wrong.toggleAnswer(wrong.state.questions[0].answers.find(a=>!a.correct).id);wrong.submitPractice();assert.equal(wrong.state.score,0);assert.match(wrong.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);
 }
});

test('all refinement cases work in practice, mixed-answer mocks and unchanged previous history',()=>{
 const bank=JSON.parse(fs.readFileSync('data/refinement-2026.json','utf8'));
 for(const part of [1,2]){
  const expected=bank.filter(q=>q.part===part).length;
  const practice=harness();practice.memory.set('old-exam-snapshot','existing');practice.state.bank=bank;practice.state.mode='practice';practice.startSession(part,100,60);
  for(let i=0;i<expected;i++){practice.state.current=i;practice.renderQuestion();const q=practice.state.questions[i];practice.toggleAnswer(q.answers.find(a=>a.correct).id);practice.submitPractice();assert.match(practice.document.querySelector('#explanation').innerHTML,/Căn cứ pháp lý/);assert.match(practice.document.querySelector('#explanation').innerHTML,/Xem văn bản/);}
  assert.equal(practice.state.score,expected);assert.equal(practice.memory.get('old-exam-snapshot'),'existing');
  const mock=harness();mock.state.bank=bank;mock.state.mode='mock';mock.startSession(part,100,60);
  for(let i=0;i<expected;i++){const q=mock.state.questions[i];mock.state.answers[q.id]=[q.answers.find(a=>i%2===0?a.correct:!a.correct).id];}
  mock.submitMock();assert.equal(mock.state.score,Math.ceil(expected/2));assert.equal(Object.keys(mock.state.results).length,expected);assert.match(mock.els.result.innerHTML,/✗ Sai/);
  const wrong=harness();wrong.state.bank=[bank.find(q=>q.part===part)];wrong.state.mode='practice';wrong.startSession(part,1,60);wrong.toggleAnswer(wrong.state.questions[0].answers.find(a=>!a.correct).id);wrong.submitPractice();assert.equal(wrong.state.score,0);assert.match(wrong.document.querySelector('#explanation').innerHTML,/Đáp án đúng/);
 }
});


test('three successive exams avoid repeats until exhausted, in both actual parts',()=>{
 const files=['questions','derived-questions','validated-2026','imported-exams-2026','imported-deposit-2026','imported-authorization-2026','imported-family-2026','imported-inheritance-2026','completion-2026','refinement-2026','verified-new-2026'];
 const bank=files.flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
 const measurements=[];
 for(const part of [1,2])for(const count of [5,10,20,50,100]){
  const h=harness();h.state.bank=bank;h.state.mode='mock';const seen=new Set(),exams=[];
  const pool=bank.filter(q=>['active','verified'].includes(q.status)&&q.part===part);
  for(let i=0;i<3;i++){
   h.startSession(part,count,60);const ids=h.state.questions.map(q=>q.id);
   const repeated=ids.filter(id=>seen.has(id)).length;
   assert.equal(repeated,Math.max(0,Math.min(count,pool.length)-(pool.length-seen.size)),`part ${part} / count ${count} / exam ${i+1}`);
   assert.equal(new Set(ids).size,ids.length);assert.match(h.state.examCode,/^CC2-/);
   const joiner=harness();joiner.state.bank=[...bank].reverse();joiner.startSharedExam(h.state.examCode);
   assert.equal(JSON.stringify(h.state.questions),JSON.stringify(joiner.state.questions));
   measurements.push({part,count,exam:i+1,pool:pool.length,overlapWithEarlierUnion:repeated,overlapWithEachEarlierExam:exams.map(previous=>ids.filter(id=>previous.includes(id)).length),codeReproduction:'exact'});
   exams.push(ids);ids.forEach(id=>seen.add(id));
  }
 }
 fs.writeFileSync('reports/anti-repeat-tests-2026-10-08.json',JSON.stringify({testedAt:'2026-10-08',scope:'Node DOM harness, real loaded bank, three consecutive exams',measurements},null,2)+'\n');
});
test('shared joins record history but do not let history change reproduced exam',()=>{
 const h=harness(),peer=harness(),bank=Array.from({length:30},(_,i)=>question(`q${i}`));
 start(h,'mock',bank,10);start(peer,'mock',bank,10);peer.startSharedExam(h.state.examCode);
 assert.equal(JSON.stringify(h.state.questions),JSON.stringify(peer.state.questions));
 const shared=new Set(peer.state.questions.map(q=>q.id));peer.startSession(1,10,15);
 assert.equal(peer.state.questions.filter(q=>shared.has(q.id)).length,0);
});
test('learner histories are isolated and all-part practice shares its recent questions with mocks',()=>{
 const h=harness(),bank=Array.from({length:60},(_,i)=>question(`q${i}`));
 h.state.learnerKey='alice';start(h,'practice',bank,20);const first=new Set(h.state.questions.map(q=>q.id));
 h.state.mode='mock';h.startSession(1,20,15);assert.equal(h.state.questions.filter(q=>first.has(q.id)).length,0);
 const alice=h.memory.get('congchungvnd:recent-v2:alice');h.state.learnerKey='bob';h.startSession(1,20,15);
 assert.equal(h.memory.get('congchungvnd:recent-v2:alice'),alice);assert.ok(h.memory.has('congchungvnd:recent-v2:bob'));
 const anonymous=harness();start(anonymous,'practice',bank,20);const seen=new Set(anonymous.state.questions.map(q=>q.id));
 anonymous.startSession(null,20,0);assert.equal(anonymous.state.questions.filter(q=>seen.has(q.id)).length,0);
});
test('legacy anonymous history migrates and storage corruption/unavailability cannot block an exam',()=>{
 const h=harness(),bank=Array.from({length:20},(_,i)=>question(`q${i}`));
 h.memory.set('congchungvnd:recent-questions:all',JSON.stringify(bank.slice(0,10).map(q=>q.id)));
 start(h,'mock',bank,10);assert.ok(h.state.questions.every(q=>Number(q.id.slice(1))>=10));
 h.memory.set('congchungvnd:recent-v2:device','bad JSON');assert.doesNotThrow(()=>h.startSession(1,10,15));
 h.context.localStorage.getItem=()=>{throw Error('blocked');};h.context.localStorage.setItem=()=>{throw Error('quota');};
 assert.doesNotThrow(()=>h.startSession(1,10,15));assert.match(h.state.examCode,/^CC2-/);
});
test('CC1 compatibility remains exact with the original generator',()=>{
 const h=harness(),bank=Array.from({length:30},(_,i)=>question(`q${i}`));
 const old=h.createSharedExam(bank,1,20,30,12345);h.state.bank=bank;h.startSharedExam(old.code);
 assert.equal(JSON.stringify(h.state.questions),JSON.stringify(old.questions));assert.equal(h.state.examCode,old.code);
});
test('CC2 rejects duplicate/out-of-range positions and wrong counts even with a valid checksum',()=>{
 const h=harness();start(h,'mock',[question('one'),question('two')]);
 const body=h.state.examCode.slice(0,h.state.examCode.lastIndexOf('-')),bits=body.split('-');
 const before=JSON.stringify(h.state.questions),deadline=h.state.deadline;
 for(const positions of ['0.0','0.ZZZZ','0']){bits[6]=positions;const forged=bits.join('-');assert.throws(()=>h.startSharedExam(forged+'-'+h.fingerprint(forged).slice(0,8)),/Mã đề/);}
 assert.equal(JSON.stringify(h.state.questions),before);assert.equal(h.state.deadline,deadline);
});
test('same legal competence is avoided where alternatives exist; balanced selection includes each topic',()=>{
 const h=harness();const bank=Array.from({length:12},(_,i)=>({...question(`q${i}`),topic:i<6?'Topic A':'Topic B',difficulty:i%2?'basic':'advanced',competenceId:`competence-${Math.floor(i/2)}`}));
 start(h,'mock',bank,6);assert.equal(new Set(h.state.questions.map(q=>q.competenceId)).size,6);
 assert.equal(h.state.questions.filter(q=>q.topic==='Topic A').length,3);
});

test('new bank includes four answers, substantive variant review metadata and unchanged correct keys',()=>{
 const rows=JSON.parse(fs.readFileSync('data/verified-new-2026.json','utf8'));
 for(const q of rows){assert.equal(q.answers.length,4);assert.equal(q.answers.filter(a=>a.correct).length,1);assert.equal(q.question.variants.length,3);assert.equal(new Set(q.question.variants).size,3);assert.ok(q.competenceId);assert.ok(q.audit.variantReviewDate);}
 assert.ok(!rows.find(q=>q.id==='VER26-NEW-50').question.variants.some(v=>v.includes('theo hình thức nào')));
});

 test('20 standard questions join both exams, enforce exact multiple sets, preserve shared codes and option explanations',()=>{
  const bank=JSON.parse(fs.readFileSync('data/calibration-20-2026.json','utf8'));assert.equal(bank.length,20);
  for(const part of [1,2]){const h=harness();h.state.bank=bank;h.state.mode='mock';h.startSession(part,20,30);const expected=part===1?12:8;assert.equal(h.state.questions.length,expected);
   for(const q of h.state.questions)h.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);const code=h.state.examCode;h.submitMock();assert.equal(h.state.score,expected);assert.match(h.els.result.innerHTML,/Giải thích từng phương án/);
   const other=harness();other.state.bank=bank;other.startSharedExam(code);assert.deepEqual(Array.from(other.state.questions,q=>q.id),Array.from(h.state.questions,q=>q.id));
  }
  const multi=bank.filter(q=>q.type==='multiple');assert.equal(multi.length,8);
  for(const base of multi){for(let mask=0;mask<16;mask++){const h=harness();h.state.mode='mock';h.state.bank=[base];h.startSession(base.part,1,15);h.state.answers[base.id]=base.answers.filter((a,i)=>mask&(1<<i)).map(a=>a.id);h.submitMock();const expected=base.answerKey.slice().sort().join(',')===h.state.answers[base.id].slice().sort().join(',');assert.equal(h.state.score,expected?1:0,base.id+' '+mask);}}
 });

test('all 100 improved questions use the common practice/mock bank without a batch selector',()=>{
 const bank=['calibration-20-2026','calibration-40-2026','calibration-next-40-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')));
 assert.equal(bank.length,100);assert.equal(new Set(bank.map(q=>q.id)).size,100);
 const sources=JSON.parse(fs.readFileSync('data/question-sources.json','utf8')).sources;
 for(const q of bank){assert.equal(q.status,'active');assert.equal(q.answers.length,4);assert.deepEqual(q.answers.filter(a=>a.correct).map(a=>a.id),q.answerKey);assert.ok(q.answers.every(a=>a.explanation));assert.ok(sources.some(s=>s.id===q.source.id));}
 const app=fs.readFileSync('app.js','utf8');assert.doesNotMatch(app,/setupScope|questionScope|calibration20/);assert.doesNotMatch(fs.readFileSync('index.html','utf8'),/Bộ 20 câu chuẩn|Phạm vi câu hỏi/);
 for(const mode of ['practice','mock'])for(const part of [1,2]){
  const h=harness();h.state.bank=bank;h.state.mode=mode;h.startSession(part,100,mode==='mock'?30:0);const expected=part===1?60:40;
  assert.equal(h.state.questions.length,expected);assert.ok(h.state.questions.some(q=>q.id==='CAL26-'+(part===1?'061':'085')));
  if(mode==='mock'){
   for(const q of h.state.questions)h.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);
   const code=h.state.examCode;h.submitMock();assert.equal(h.state.score,expected);assert.match(h.els.result.innerHTML,/Giải thích từng phương án/);
   const other=harness();other.state.bank=bank;other.startSharedExam(code);assert.deepEqual(Array.from(other.state.questions,q=>q.id),Array.from(h.state.questions,q=>q.id));
  }else{
   for(let i=0;i<expected;i++){h.state.current=i;h.renderQuestion();h.state.selected=new Set(h.state.questions[i].answers.filter(a=>a.correct).map(a=>a.id));assert.equal(h.submitPractice(),true);}
   assert.equal(h.state.score,expected);
  }
 }
});

test('100 additional integrated scenarios enter both common modes, keep shuffled keys and shared-exam identity',()=>{
 const bank=JSON.parse(fs.readFileSync('data/hard-integrated-100-2026.json','utf8'));
 for(const mode of ['practice','mock'])for(const part of [1,2]){
  const h=harness();h.state.bank=bank;h.state.mode=mode;h.startSession(part,100,30);
  const expected=part===1?60:40;assert.equal(h.state.questions.length,expected);
  if(mode==='practice'){
   for(let i=0;i<expected;i++){h.state.current=i;h.renderQuestion();h.state.selected=new Set(h.state.questions[i].answers.filter(a=>a.correct).map(a=>a.id));assert.equal(h.submitPractice(),true);}
  }else{
   const code=h.state.examCode;const other=harness();other.state.bank=bank;other.startSharedExam(code);
   assert.equal(JSON.stringify(other.state.questions),JSON.stringify(h.state.questions));
   for(const q of h.state.questions)h.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);
   h.submitMock();assert.match(h.els.result.innerHTML,/Giải thích từng phương án/);
  }
  assert.equal(h.state.score,expected);
 }
 const app=fs.readFileSync('app.js','utf8');assert.match(app,/hard-integrated-100-2026.json/);assert.doesNotMatch(app,/setupScope|questionScope/);
});
test('all 640 subsets of integrated multi-select questions are scored exactly, including omission and extras',()=>{
 const bank=JSON.parse(fs.readFileSync('data/hard-integrated-100-2026.json','utf8')).filter(q=>q.type==='multiple');assert.equal(bank.length,40);
 for(const base of bank)for(let mask=0;mask<16;mask++){
  const h=harness();h.state.mode='mock';h.state.bank=[base];h.startSession(base.part,1,15);
  const selected=base.answers.filter((a,i)=>mask&(1<<i)).map(a=>a.id);h.state.answers[base.id]=selected;h.submitMock();
  assert.equal(h.state.score,selected.slice().sort().join(',')===base.answerKey.slice().sort().join(',')?1:0,base.id+' subset '+mask);
 }
});

test('application wording loader removes every retired recall variant from both modes and rejects stale sources',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 const files=fs.readFileSync('app.js','utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));
 const base=files.flatMap(f=>JSON.parse(fs.readFileSync('data/'+f,'utf8')));
 const profile=JSON.parse(fs.readFileSync('data/application-wording-2026.json','utf8'));
 const review=JSON.parse(fs.readFileSync('reports/application-wording-review-2026-10-12.json','utf8'));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const worded=await h.applyApplicationWording(base,profile);
 const bank=await h.loadQuestions();assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 assert.equal(bank.find(q=>q.id==='CC-082').status,'archived');
 const reachable=new Set(bank.filter(q=>['active','verified'].includes(q.status)).flatMap(q=>q.question.variants));
 for(const d of review.decisions){const effective=worded.find(q=>q.id===d.id);const original=base.find(q=>q.id===d.id);
  assert.equal(JSON.stringify(effective.answers),JSON.stringify(original.answers));assert.equal(JSON.stringify(effective.legalBasis),JSON.stringify(original.legalBasis));assert.equal(effective.explanation,original.explanation);
  for(const v of d.beforeVariants)if(!d.afterVariants?.includes(v))assert.ok(!reachable.has(v),d.id+' retired wording');
 }
 assert.ok(![...reachable].some(v=>/Điều nào được quy định|Đọc riêng|Theo định nghĩa tại Điều|Công chứng theo Luật Công chứng là gì/i.test(v)));
 const focus=bank.filter(q=>['CC-001','CC-007','CC-018','SRC26-001','CC-082'].includes(q.id));
 for(const mode of ['practice','mock']){
  const t=harness();t.state.bank=focus;t.state.mode=mode;t.startSession(1,100,15);assert.equal(t.state.questions.length,4);assert.ok(t.state.questions.every(q=>q.id!=='CC-082'));
  for(const q of t.state.questions)assert.ok(reachable.has(q.variant));
  if(mode==='mock'){const other=harness();other.state.bank=focus;other.startSharedExam(t.state.examCode);assert.equal(JSON.stringify(other.state.questions),JSON.stringify(t.state.questions));}
 }
 const corrupted=JSON.parse(JSON.stringify(base));corrupted.find(q=>q.id==='CC-018').answers[0].text='Changed legal answer';
 await assert.rejects(h.applyApplicationWording(corrupted,profile),/Nguồn câu hỏi đã thay đổi/);
 await assert.rejects(h.applyApplicationWording(base,{...profile,questions:[profile.questions[0],profile.questions[0]]}),/trùng/);
 await assert.rejects(h.applyApplicationWording(base,{...profile,questions:[{...profile.questions[0],id:'unknown'}]}),/mã thiếu/);
 await assert.rejects(h.applyApplicationWording(base,{...profile,questions:[{...profile.questions[0],variants:[]}]}),/không hợp lệ/);
 await assert.rejects(h.applyApplicationWording(base,{...profile,questions:[{...profile.questions[0],status:'verified'}]}),/trạng thái kiểm định/);
});

test('67 reviewed refinements load after application wording, grade in both modes, and reject stale or altered keys',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions();assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 const profile=JSON.parse(fs.readFileSync('data/scenario-refinements-2026.json','utf8'));const ids=new Set(profile.questions.map(r=>r.id));const edited=bank.filter(q=>ids.has(q.id));assert.equal(edited.length,67);
 for(const row of profile.questions)assert.equal(JSON.stringify(bank.find(q=>q.id===row.id)),JSON.stringify(polishedExpected(row.after)));
 for(const mode of ['practice','mock'])for(const part of [1,2]){
  const t=harness();t.state.bank=edited;t.state.mode=mode;t.startSession(part,100,30);const expected=edited.filter(q=>q.part===part).length;assert.equal(t.state.questions.length,expected);
  if(mode==='practice'){for(let i=0;i<expected;i++){t.state.current=i;t.renderQuestion();t.state.selected=new Set(t.state.questions[i].answers.filter(a=>a.correct).map(a=>a.id));assert.equal(t.submitPractice(),true);}}
  else{for(const q of t.state.questions)t.state.answers[q.id]=q.answers.filter(a=>a.correct).map(a=>a.id);const code=t.state.examCode;t.submitMock();const other=harness();other.state.bank=edited;other.startSharedExam(code);assert.equal(JSON.stringify(t.state.questions),JSON.stringify(other.state.questions));}
  assert.equal(t.state.score,expected);
 }
 const baseFiles=fs.readFileSync('app.js','utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));const raw=baseFiles.flatMap(f=>JSON.parse(fs.readFileSync('data/'+f,'utf8')));
 const styled=await h.applyApplicationWording(raw,JSON.parse(fs.readFileSync('data/application-wording-2026.json','utf8')));
 const bad=JSON.parse(JSON.stringify(profile));bad.questions[0].after.answers[0].correct=!bad.questions[0].after.answers[0].correct;await assert.rejects(h.applyScenarioRefinements(styled,bad),/khóa/);
 const stale=JSON.parse(JSON.stringify(styled));stale.find(q=>q.id===profile.questions[0].id).question.variants[0]+=' Changed';await assert.rejects(h.applyScenarioRefinements(stale,profile),/Nguồn câu hỏi đã thay đổi/);
 await assert.rejects(h.applyScenarioRefinements(styled,{...profile,questions:[profile.questions[0],profile.questions[0]]}),/trùng/);
});

test('60 additional cases preserve 67 repairs, load both modes, grade every option and replay shared codes',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),extra=JSON.parse(fs.readFileSync('data/scenario-refinements-remaining-2026.json','utf8'));
 const legal=JSON.parse(fs.readFileSync('reports/remaining-60-legal-review-2026-10-13.json','utf8'));
 const prior=JSON.parse(fs.readFileSync('data/scenario-refinements-2026.json','utf8'));
 assert.equal(extra.questions.length,60);assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 const ids=new Set(extra.questions.map(r=>r.id));assert.ok(prior.questions.every(r=>!ids.has(r.id)));
 for(const r of prior.questions)assert.equal(JSON.stringify(bank.find(q=>q.id===r.id)),JSON.stringify(polishedExpected(r.after)));
 for(const r of extra.questions){
  const q=bank.find(q=>q.id===r.id),key=legal.questions.find(d=>d.id===r.id).answerKey;
  assert.equal(JSON.stringify(q),JSON.stringify(polishedExpected(r.after)));
  for(const mode of ['practice','mock'])for(const option of q.answers){
   const t=harness();t.state.bank=[q];t.state.mode=mode;t.startSession(q.part,1,15);
   const expected=key.includes(option.id)?1:0;
   if(mode==='practice'){t.toggleAnswer(option.id);assert.equal(t.submitPractice(),true);}
   else{t.state.answers[q.id]=[option.id];t.submitMock();}
   assert.equal(t.state.score,expected,r.id+' '+mode+' '+option.id);
  }
 }
 const edited=bank.filter(q=>ids.has(q.id));
 for(const part of [1,2]){
  const t=harness();t.state.bank=edited;t.state.mode='mock';t.startSession(part,100,30);
  const code=t.state.examCode,other=harness();other.state.bank=edited;other.startSharedExam(code);
  assert.equal(JSON.stringify(t.state.questions),JSON.stringify(other.state.questions));
 }
 const baseFiles=fs.readFileSync('app.js','utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));
 const raw=baseFiles.flatMap(f=>JSON.parse(fs.readFileSync('data/'+f,'utf8')));
 const styled=await h.applyApplicationWording(raw,JSON.parse(fs.readFileSync('data/application-wording-2026.json','utf8')));
 const previous=await h.applyScenarioRefinements(styled,prior);
 const stale=JSON.parse(JSON.stringify(previous));stale.find(q=>q.id===extra.questions[0].id).answers[0].text+=' changed';
 await assert.rejects(h.applyScenarioRefinements(stale,extra),/Nguồn câu hỏi đã thay đổi/);
 const corrupt=JSON.parse(JSON.stringify(extra));corrupt.questions[0].after.answerKey=['not-a-key'];
 await assert.rejects(h.applyScenarioRefinements(previous,corrupt),/khóa/);
});

test('all 129 priority revisions load without replacing previous repairs; every answer set grades in both modes',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),profile=JSON.parse(fs.readFileSync('data/scenario-priority-129-2026.json','utf8'));
 const review=JSON.parse(fs.readFileSync('reports/priority-129-legal-review-2026-10-13.json','utf8'));
 assert.equal(profile.questions.length,129);assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 const prior=['data/scenario-refinements-2026.json','data/scenario-refinements-remaining-2026.json'].flatMap(p=>JSON.parse(fs.readFileSync(p,'utf8')).questions);
 for(const r of prior)assert.equal(JSON.stringify(bank.find(q=>q.id===r.id)),JSON.stringify(polishedExpected(r.after)));
 let gradingCases=0;
 for(const r of profile.questions){const q=bank.find(q=>q.id===r.id),key=review.questions.find(d=>d.id===q.id).answerKey.slice().sort();
  assert.equal(JSON.stringify(q),JSON.stringify(polishedExpected(r.after)));
  const selections=q.type==='single'?q.answers.map(a=>[a.id]):Array.from({length:16},(_,mask)=>q.answers.filter((_,i)=>mask&(1<<i)).map(a=>a.id));
  for(const mode of ['practice','mock'])for(const selected of selections){
   const t=harness();t.state.bank=[q];t.state.mode=mode;t.startSession(q.part,1,15);
   const expected=JSON.stringify(selected.slice().sort())===JSON.stringify(key)?1:0;
   if(mode==='practice'){for(const id of selected)t.toggleAnswer(id);t.submitPractice();}
   else{t.state.answers[q.id]=selected;t.submitMock();}
   assert.equal(t.state.score,expected,q.id+' '+mode+' '+selected.join(','));gradingCases++;
  }
 }
 assert.equal(gradingCases,124*4*2+5*16*2);
 for(const part of [1,2]){const t=harness();t.state.bank=bank;t.state.mode='mock';t.startSession(part,100,30);const other=harness();other.state.bank=bank;other.startSharedExam(t.state.examCode);assert.equal(JSON.stringify(t.state.questions),JSON.stringify(other.state.questions));}
 const before=bank.map(q=>profile.questions.some(r=>r.id===q.id)?review.questions.find(d=>d.id===q.id).before:q);
 const stale=JSON.parse(JSON.stringify(before));stale.find(q=>q.id===profile.questions[0].id).question.variants[0]+='changed';
 await assert.rejects(h.applyScenarioRefinements(stale,profile),/Nguồn câu hỏi đã thay đổi/);
 const bad=JSON.parse(JSON.stringify(profile));bad.questions[0].after.answers[0].correct=!bad.questions[0].after.answers[0].correct;
 await assert.rejects(h.applyScenarioRefinements(before,bad),/khóa/);
 await assert.rejects(h.applyScenarioRefinements(before,{...profile,questions:[profile.questions[0],profile.questions[0]]}),/trùng/);
});

test('40 application cases preserve prior cohorts, reject stale sources and grade every mock subset',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),profile=JSON.parse(fs.readFileSync('data/scenario-application-40-2026.json','utf8'));
 const review=JSON.parse(fs.readFileSync('reports/application-40-legal-review-2026-10-13.json','utf8'));
 assert.equal(profile.questions.length,40);assert.equal(review.questions.length,40);
 assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 assert.equal(new Set(profile.questions.map(r=>r.id)).size,40);
 for(const f of ['scenario-refinements-2026','scenario-refinements-remaining-2026','scenario-priority-129-2026']){
  for(const r of JSON.parse(fs.readFileSync(`data/${f}.json`,'utf8')).questions)assert.equal(JSON.stringify(bank.find(q=>q.id===r.id)),JSON.stringify(polishedExpected(r.after)));
 }
 let cases=0;
 for(const row of profile.questions){
  const q=bank.find(q=>q.id===row.id),d=review.questions.find(r=>r.id===q.id),key=d.answerKey.slice().sort();
  assert.equal(JSON.stringify(q),JSON.stringify(polishedExpected(row.after)));assert.equal(q.empiricallyCalibrated,false);
  assert.equal(q.type,'single');assert.equal(q.question.variants.length,1);
  assert.notEqual(q.question.variants[0],d.before.question.variants[0]);
  assert.ok(d.evidenceKeys.every(k=>review.evidence[k]?.excerpt&&review.evidence[k]?.reference.url.startsWith('https://')));
  for(const a of q.answers)if(!a.correct){assert.notEqual(a.text,d.before.answers.find(b=>b.id===a.id).text);assert.equal(unpolishedVersion(q).answers.find(old=>old.id===a.id).explanation,d.distractorRationale[a.id]);}
  for(const selected of [[],...q.answers.map(a=>[a.id])]){
   const t=harness();t.state.bank=[q];t.state.mode='practice';t.startSession(q.part,1,15);
   for(const id of selected)t.toggleAnswer(id);t.submitPractice();
   assert.equal(t.state.score,JSON.stringify(selected)===JSON.stringify(key)?1:0,q.id+' practice');cases++;
  }
  for(let mask=0;mask<16;mask++){
   const selected=q.answers.filter((_,i)=>mask&(1<<i)).map(a=>a.id),t=harness();t.state.bank=[q];t.state.mode='mock';t.startSession(q.part,1,15);
   t.state.answers[q.id]=selected;t.submitMock();
   assert.equal(t.state.score,JSON.stringify(selected.slice().sort())===JSON.stringify(key)?1:0,q.id+' mock '+mask);cases++;
  }
 }
 assert.equal(cases,840);
 const stage=bank.map(q=>review.questions.find(d=>d.id===q.id)?.before||q);
 const stale=JSON.parse(JSON.stringify(stage));stale.find(q=>q.id===profile.questions[0].id).answers[0].text+=' changed';
 await assert.rejects(h.applyScenarioRefinements(stale,profile),/Nguồn câu hỏi đã thay đổi/);
 const broken=JSON.parse(JSON.stringify(profile));broken.questions[0].after.answerKey=['unknown'];
 await assert.rejects(h.applyScenarioRefinements(stage,broken),/khóa/);
 for(const part of [1,2]){const t=harness();t.state.bank=bank;t.state.mode='mock';t.startSession(part,100,30);const other=harness();other.state.bank=bank;other.startSharedExam(t.state.examCode);assert.equal(JSON.stringify(t.state.questions),JSON.stringify(other.state.questions));}
});

test('60 continuation cases load after all reviewed layers and keep independent keys for both modes',async()=>{
 const h=harness();await new Promise(resolve=>setImmediate(resolve));
 h.context.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.replace('./',''),'utf8'))});
 const bank=await h.loadQuestions(),profile=JSON.parse(fs.readFileSync('data/scenario-continuation-60-2026.json','utf8'));
 const review=JSON.parse(fs.readFileSync('reports/continuation-60-legal-review-2026-10-13.json','utf8'));
 assert.equal(profile.questions.length,60);assert.equal(review.questions.length,60);
 assert.equal(new Set(profile.questions.map(r=>r.id)).size,60);
 assert.equal(bank.filter(q=>['active','verified'].includes(q.status)).length,793);
 const oldRows=['scenario-refinements-2026','scenario-refinements-remaining-2026','scenario-priority-129-2026','scenario-application-40-2026'].flatMap(name=>JSON.parse(fs.readFileSync(`data/${name}.json`,'utf8')).questions);
 assert.equal(oldRows.length,296);
 for(const r of oldRows)assert.equal(JSON.stringify(bank.find(q=>q.id===r.id)),JSON.stringify(polishedExpected(r.after)));
 let cases=0;
 for(const row of profile.questions){
  const q=bank.find(q=>q.id===row.id),d=review.questions.find(r=>r.id===q.id),key=d.answerKey.slice().sort();
  assert.equal(JSON.stringify(q),JSON.stringify(polishedExpected(row.after)));assert.equal(q.empiricallyCalibrated,false);
  assert.equal(q.type,'single');assert.equal(q.question.variants.length,1);
  assert.equal(JSON.stringify(key),JSON.stringify(d.before.answers.filter(a=>a.correct).map(a=>a.id).sort()));
  assert.notEqual(q.question.variants[0],d.before.question.variants[0]);
  assert.ok(d.evidenceKeys.every(k=>review.evidence[k]?.excerpt&&review.evidence[k]?.reference.url.startsWith('https://')));
  for(const a of q.answers)if(!a.correct){assert.notEqual(a.text,d.before.answers.find(b=>b.id===a.id).text);assert.equal(unpolishedVersion(q).answers.find(old=>old.id===a.id).explanation,d.distractorRationale[a.id]);}
  for(const selected of [[],...q.answers.map(a=>[a.id])]){
   const t=harness();t.state.bank=[q];t.state.mode='practice';t.startSession(q.part,1,15);for(const id of selected)t.toggleAnswer(id);t.submitPractice();
   assert.equal(t.state.score,JSON.stringify(selected)===JSON.stringify(key)?1:0,q.id+' practice');cases++;
  }
  for(let mask=0;mask<16;mask++){
   const selected=q.answers.filter((_,i)=>mask&(1<<i)).map(a=>a.id),t=harness();t.state.bank=[q];t.state.mode='mock';t.startSession(q.part,1,15);t.state.answers[q.id]=selected;t.submitMock();
   assert.equal(t.state.score,JSON.stringify(selected.slice().sort())===JSON.stringify(key)?1:0,q.id+' mock '+mask);cases++;
  }
 }
 assert.equal(cases,1260);
 // Anchor the tricky distinctions separately from answer-letter preservation.
 const right=id=>bank.find(q=>q.id===id).answers.find(a=>a.correct).text;
 assert.match(right('IMP-T60-029'),/4 con.*30 triệu/);
 assert.match(right('IMP-SEP24-041'),/chín tháng.*ba tháng/);
 assert.match(right('VER26-064'),/C nhận 300 triệu.*D nhận 300 triệu/);
 assert.match(right('VER26-063'),/200.*400/);
 assert.match(right('COMP26-QT-008'),/10:05/);
 assert.match(right('IMP-T60-094'),/không cho K ủy quyền lại/);
 const labor=bank.find(q=>q.id==='IMP-T60-092');assert.ok(labor.legalBasis.some(b=>b.article==='Điều 14'));
 const translator=bank.find(q=>q.id==='COMP26-CT-013');assert.match(translator.question.variants[0],/không (?:là|phải) cộng tác viên/);
 const stage=bank.map(q=>review.questions.find(d=>d.id===q.id)?.before||q),stale=JSON.parse(JSON.stringify(stage));
 stale.find(q=>q.id===profile.questions[0].id).legalBasis[0].article+=' changed';
 await assert.rejects(h.applyScenarioRefinements(stale,profile),/Nguồn câu hỏi đã thay đổi/);
 const bad=JSON.parse(JSON.stringify(profile));bad.questions[0].after.answerKey=['unknown'];
 await assert.rejects(h.applyScenarioRefinements(stage,bad),/khóa/);
 await assert.rejects(h.applyScenarioRefinements(stage,{...profile,questions:[profile.questions[0],profile.questions[0]]}),/trùng/);
 for(const part of [1,2]){const t=harness();t.state.bank=bank;t.state.mode='mock';t.startSession(part,100,30);const other=harness();other.state.bank=bank;other.startSharedExam(t.state.examCode);assert.equal(JSON.stringify(t.state.questions),JSON.stringify(other.state.questions));}
});
