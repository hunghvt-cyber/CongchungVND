const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const {bridge,digest,historicalVersion}=require('./helpers/editorial-versions.cjs');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const files=fs.readFileSync('app.js','utf8').match(/const files = \[(.*?)\];/s)[1].match(/'([^']+)'/g).map(s=>s.slice(1,-1));
const bank=files.flatMap(f=>read('data/'+f));
test('current editorial bridge authenticates all 191 changes without changing historical certificates or keys',()=>{
 assert.equal(bank.length,813);assert.equal(new Set(bank.map(q=>q.id)).size,813);
 assert.equal(bridge.rows.length,191);assert.equal(new Set(bridge.rows.map(r=>r.id)).size,191);
 assert.equal(bridge.notLegalRecertification,true);assert.equal(bridge.historicalDossiersUnchanged,true);
 assert.deepEqual(bridge.rows.filter(r=>r.basisChanged).map(r=>r.id).sort(),['CAL26-027','HARD26-041']);
 for(const row of bridge.rows){
  const q=bank.find(q=>q.id===row.id),old=historicalVersion(q);
  assert.equal(digest(q),row.afterHash,q.id);assert.equal(digest(old),row.beforeHash,q.id);
  assert.ok(fs.existsSync(row.reviewReference),q.id);
 }
});
test('historical fallback rejects mutations of current stem, key, explanation, status and legal basis',()=>{
 const q=bank.find(q=>q.id===bridge.rows[0].id);
 for(const mutate of [x=>x.question.variants[0]+=' changed',x=>x.answers[0].correct=!x.answers[0].correct,x=>x.explanation+=' changed',x=>x.status='archived',x=>x.legalBasis[0].article='invalid']){
  const corrupted=structuredClone(q);mutate(corrupted);assert.throws(()=>historicalVersion(corrupted),/current approved snapshot/);
 }
});
test('23 content repairs retain exact before/after records, keys, status and verification dates',()=>{
 const fixes=read('editorial/post-review-repairs-2026-10-15.json').fixes;
 assert.equal(fixes.length,23);assert.equal(new Set(fixes.map(r=>r.id)).size,23);
 for(const r of fixes){
  const q=bank.find(q=>q.id===r.id);assert.deepEqual(q,r.after,r.id);
  for(const k of ['status','lastVerified','legalBasis','source'])assert.deepEqual(r.before[k],q[k],r.id+' '+k);
  assert.deepEqual(r.before.answers,q.answers,r.id+' options and independent key');
  assert.ok(q.explanation.length>=100,r.id);
 }
 const supplement=read('editorial/legal-evidence-supplement-2026-10-15.json');
 assert.deepEqual(supplement.questions.map(r=>r.id).sort(),Object.keys(bridge.basisAmendments).sort());
 const cal=supplement.questions.find(r=>r.id==='CAL26-027');
 const report=read(cal.historicalReport),decision=report.questions.find(r=>r.id===cal.id);
 assert.deepEqual(cal.answerKey,decision.answerKey);assert.deepEqual(cal.evidenceKeys,decision.evidenceKeys);
 assert.match(report.evidence['CC:50'].excerpt,/4\./);
});
