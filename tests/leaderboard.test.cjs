const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const tick=()=>new Promise(resolve=>setImmediate(resolve));
const row=(name='An')=>({learner_name:name,attempt_count:3,average_score:8.123456,best_score:10});
function harness(fetcher){
 const nodes=new Map(),window={};
 const node=()=>({innerHTML:'',textContent:'',disabled:false,classList:{toggle(){}},querySelector:selector=>nodes.get(selector)});
 ['#sharedLeaderboard','#leaderboardStatus','#leaderboardContent','#refreshLeaderboard','#leaderboardPrevious','#leaderboardNext'].forEach(s=>nodes.set(s,node()));
 const requests=[];
 const context=vm.createContext({window,document:{querySelector:s=>nodes.get(s)},AbortController,setTimeout,clearTimeout,fetch:async(url,opts)=>{requests.push({url,opts});return url.startsWith('./')?{ok:true,json:async()=>({url:'https://example.supabase.co',publishableKey:'sb_publishable_test'})}:fetcher(url,opts);}});
 vm.runInContext(fs.readFileSync('leaderboard.js','utf8'),context);
 return {window,nodes,requests};
}
test('leaderboard reads only aggregates without history keys; escapes public names',async()=>{
 const h=harness(async()=>({ok:true,json:async()=>[row('<img src=x onerror=alert(1)>')]}));await tick();
 const request=h.requests.find(r=>r.url.startsWith('https:'));
 assert.match(request.url,/exam_leaderboard\?select=learner_name,attempt_count,average_score,best_score/);
 assert.ok(!request.url.includes('learner_key'));assert.ok(!('x-client-info' in request.opts.headers));
 const html=h.nodes.get('#leaderboardContent').innerHTML;assert.match(html,/8\.12/);assert.ok(!html.includes('<img'));assert.match(html,/&lt;img/);
});
test('pagination fetches next page and keeps global positions',async()=>{
 const h=harness(async url=>({ok:true,json:async()=>url.includes('offset=100')?[row('Page2')]:Array.from({length:101},()=>row())}));await tick();
 await h.nodes.get('#leaderboardNext').onclick();assert.match(h.nodes.get('#leaderboardContent').innerHTML,/<td>101<\/td>/);
 await h.nodes.get('#leaderboardPrevious').onclick();assert.match(h.requests.at(-1).url,/offset=0$/);
});
test('empty board explains minimum submissions and offline refresh preserves last data',async()=>{
 let fail=false;const h=harness(async()=>{if(fail)throw Error('offline');return{ok:true,json:async()=>[]};});await tick();
 assert.match(h.nodes.get('#leaderboardContent').innerHTML,/đủ 3 bài/);fail=true;await h.window.ExamLeaderboard.refresh();
 assert.match(h.nodes.get('#leaderboardStatus').textContent,/Chưa tải được/);assert.equal(h.nodes.get('#refreshLeaderboard').disabled,false);
});
test('stale response cannot overwrite newer successful refresh',async()=>{
 let resolveFirst,count=0;const h=harness(async()=>{if(++count===1)return new Promise(resolve=>{resolveFirst=resolve;});return {ok:true,json:async()=>[row('New')]};});await tick();
 await h.window.ExamLeaderboard.refresh();resolveFirst({ok:true,json:async()=>[row('Old')]});await tick();
 assert.match(h.nodes.get('#leaderboardContent').innerHTML,/New/);assert.ok(!h.nodes.get('#leaderboardContent').innerHTML.includes('Old'));
});
