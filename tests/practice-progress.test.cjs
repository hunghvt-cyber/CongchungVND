const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function harness(fetcher=async()=>({ok:true,status:201})){
 const memory=new Map(),nodes=new Map(),requests=[],window={};
 const node=()=>({value:'',innerHTML:'',textContent:'',dataset:{},disabled:false,children:[],classList:{add(){},remove(){}},querySelectorAll(){return this.children;},scrollIntoView(){},focus(){}});
 const document={querySelector:s=>{if(!nodes.has(s))nodes.set(s,node());return nodes.get(s);}};
 const context=vm.createContext({window,document,localStorage:{getItem:k=>memory.get(k)||null,setItem:(k,v)=>memory.set(k,v)},crypto:require('node:crypto').webcrypto,AbortController,setTimeout,clearTimeout,console,fetch:async(url,opts)=>{
  if(url.startsWith('./'))return{ok:true,json:async()=>({url:'https://example.supabase.co',publishableKey:'sb_publishable_test'})};
  requests.push({url,opts});return fetcher(url,opts);
 }});
 for(const p of ['progress.js','practice-progress.js'])vm.runInContext(fs.readFileSync(p,'utf8'),context);
 return {api:window.PracticeProgress,progress:window.ExamProgress,context,nodes,memory,requests,document,window};
}
function state(){return{mode:'practice',attemptId:require('node:crypto').randomUUID(),learnerName:'An',learnerKey:'0000000001',answers:{Q1:['B']},results:{Q1:false},questions:[{id:'Q1',part:1,topic:'Thừa kế <test>',variant:'Chọn <đúng>',answers:[{id:'A',text:'Đúng',correct:true},{id:'B',text:'Sai',correct:false}],explanation:'Giải thích',legalBasis:[{document:'Luật',article:'1'}]}]};}
const event=(id,correct=false,extra={})=>({id,session_id:id,learner_key:'0000000001',learner_name:'An',question_id:'Q1',part:1,topic:'Thừa kế <test>',is_correct:correct,graded_at:'2026-10-18T00:00:00Z',answer:{variant:'<script>x</script>',selected:['B'],correct_ids:['A'],answers:[{id:'A',text:'Đúng'},{id:'B',text:'Sai'}],explanation:'<b>text</b>',legal_basis:[]},...extra});
test('graded practice saves once with immutable snapshot, separate table and no exam leaderboard refresh',async()=>{
 const h=harness(),s=state();let refreshes=0;h.window.ExamLeaderboard={refresh(){refreshes++;}};
 const save=h.api.recordAnswer(s,s.questions[0]);s.answers.Q1[0]='A';s.questions[0].answers[0].text='Changed';await save;await h.api.recordAnswer(s,s.questions[0]);
 assert.equal(h.requests.length,1);assert.match(h.requests[0].url,/\/practice_answers$/);const row=JSON.parse(h.requests[0].opts.body);
 assert.deepEqual(row.answer.selected,['B']);assert.equal(row.answer.answers[0].text,'Đúng');assert.equal(row.is_correct,false);assert.equal(row.session_id,s.attemptId);assert.equal(refreshes,0);assert.equal(h.api.pendingCount(),0);
 s.mode='mock';s.practiceReceipts={};await h.api.recordAnswer(s,s.questions[0]);assert.equal(h.requests.length,1);
});
test('offline receipts survive reload, retry is idempotent and repeated practice is a new session',async()=>{
 const h=harness(async()=>{throw Error('offline');}),s=state();await h.api.recordAnswer(s,s.questions[0]);
 const stored=JSON.parse(h.memory.get('practiceAnswerQueue'));assert.equal(stored.length,1);assert.match(h.document.querySelector('#practiceSaveStatus').textContent,/giữ trên thiết bị/);
 const other=harness(async()=>({ok:false,status:409,json:async()=>({code:'23505'})}));other.memory.set('practiceAnswerQueue',JSON.stringify(stored));await other.api.retryQueued();
 assert.equal(other.api.pendingCount(),0);assert.equal(JSON.parse(other.requests[0].opts.body).id,stored[0].id);
 const next=state();await other.api.recordAnswer(next,next.questions[0]);assert.notEqual(JSON.parse(other.requests[1].opts.body).session_id,stored[0].session_id);
});
test('correct, wrong, repeated questions, parts and deduplicated pending rows aggregate correctly',()=>{
 const h=harness(),a=event('a'),b=event('b',true),c=event('c',false,{part:2,question_id:'Q2'}),s=h.api.summarize([a,b,c,a]);
 assert.equal(s.total,3);assert.equal(s.correct,1);assert.equal(s.uniqueQuestions,2);assert.equal(s.topics.length,2);
 const first=s.topics.find(t=>t.part===1);assert.equal(first.total,2);assert.equal(first.wrong,1);assert.deepEqual(Array.from(first.ids),['Q1']);
});
test('practice history paginates, merges same-phone pending only and retries from the shared controls',async()=>{
 let gets=0;const first=Array.from({length:100},(_,i)=>event('r'+i));
 const h=harness(async(url,opts)=>opts?.method==='POST'?{ok:true,status:201}:{ok:true,json:async()=>++gets===1?first:[]});
 h.memory.set('practiceAnswerQueue',JSON.stringify([first[0],event('pending'),event('other',false,{learner_key:'0000000002'})]));
 h.progress.init(()=>{});await h.progress.loadHistory('0000000001','practice');
 const html=h.document.querySelector('#progressContent').innerHTML;assert.match(html,/<strong>101<\/strong> lượt câu/);assert.match(html,/Thống kê ôn tập/);assert.match(html,/&lt;script&gt;/);assert.ok(!html.includes('<script>x'));
 assert.equal(gets,2);assert.ok(h.requests.every(r=>r.opts.headers['x-client-info']==='0000000001'));
 await h.document.querySelector('#retryQueued').onclick();assert.equal(h.api.pendingCount(),0);
});
test('offline statistics explicitly say incomplete and never count an ungraded or anonymous question',async()=>{
 const h=harness(async()=>{throw Error('offline');}),s=state();s.results={};await h.api.recordAnswer(s,s.questions[0]);assert.equal(h.requests.length,0);
 s.results={Q1:false};s.learnerKey='';await h.api.recordAnswer(s,s.questions[0]);assert.equal(h.requests.length,0);
 await h.progress.loadHistory('0000000001','practice');assert.match(h.document.querySelector('#progressContent').innerHTML,/Thống kê chưa đầy đủ/);
});
test('obsolete practice responses cannot overwrite a newly selected history or exam view',async()=>{
 let finish;const h=harness(async()=>new Promise(resolve=>{finish=()=>resolve({ok:true,json:async()=>[event('old')]});}));
 const pending=h.progress.loadHistory('0000000001','practice');await new Promise(resolve=>setTimeout(resolve,0));
 h.progress.init(()=>{});h.document.querySelector('#progressMode').onchange();h.document.querySelector('#progressContent').innerHTML='new view';finish();await pending;
 assert.equal(h.document.querySelector('#progressContent').innerHTML,'new view');
});
test('strengthening uses the selected history identity, not a previous learner',async()=>{
 const h=harness(async()=>({ok:true,json:async()=>[event('one')]}));let chosen;
 h.progress.init((ids,learner)=>{chosen={ids:Array.from(ids),learner};});
 const button={dataset:{index:'0'}};h.document.querySelector('#progressContent').children=[button];
 await h.progress.loadHistory('0000000001','practice');button.onclick();
 assert.deepEqual(chosen.ids,['Q1']);assert.equal(chosen.learner.learnerKey,'0000000001');assert.equal(chosen.learner.learnerName,'An');
});
test('app grading hooks save immediately, revisit never re-saves and retry wrong creates a new receipt',async()=>{
 const {createRequire}=require('node:module');const source=fs.readFileSync('tests/app.test.cjs','utf8').split("test('the historical")[0];
 const app=new Function('require',source+'\nreturn {harness,question};')(createRequire(process.cwd()+'/tests/app.test.cjs'));
 const h=app.harness(),saved=[];h.context.window.PracticeProgress={recordAnswer(s,q){saved.push({session:s.attemptId,id:q.id,result:s.results[q.id]});},sessionMarkup(){return '';},bindResult(){}};
 h.state.bank=[app.question('one')];h.state.mode='practice';h.state.learnerName='An';h.state.learnerKey='0000000001';h.startSession(1,1,0);h.toggleAnswer('B');h.submitPractice();h.submitPractice();h.renderQuestion();
 assert.equal(saved.length,1);assert.equal(saved[0].result,false);h.showPracticeResult();h.document.querySelector('#reviewWrong').listeners.click();h.toggleAnswer('A');h.submitPractice();
 assert.equal(saved.length,2);assert.notEqual(saved[0].session,saved[1].session);assert.equal(saved[1].result,true);
});
