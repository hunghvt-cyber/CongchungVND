// Match the application's ordered presentation layers for editorial tooling.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const layers=['scenario-refinements-2026','scenario-refinements-remaining-2026','scenario-priority-129-2026','scenario-application-40-2026','scenario-continuation-60-2026'];
function effectiveBank({polish=false}={}){
 const files=fs.readFileSync(path.join(root,'app.js'),'utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));
 let bank=files.flatMap(f=>read('data/'+f));
 const wording=new Map(read('data/application-wording-2026.json').questions.map(r=>[r.id,r]));
 bank=bank.map(q=>{const r=wording.get(q.id);return !r?q:{...q,...(r.status?{status:r.status}:{question:{...q.question,variants:r.variants.slice()}}),presentationReview:'application-wording-2026-10-12'};});
 for(const name of [...layers,...(polish?['editorial-polish-2026']:[])]){
  const revisions=new Map(read('data/'+name+'.json').questions.map(r=>[r.id,r.after]));
  bank=bank.map(q=>revisions.get(q.id)||q);
 }
 return structuredClone(bank);
}
module.exports={root,read,layers,effectiveBank};
