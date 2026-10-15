const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {createHash}=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const bridge=JSON.parse(fs.readFileSync(path.join(root,'editorial/editorial-version-bridge-2026-10-15.json'),'utf8'));
const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(', ')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+': '+canonical(v[k])).join(', ')+'}';
const digest=v=>createHash('sha256').update(canonical(v)).digest('hex');
const rows=new Map(bridge.rows.map(r=>[r.id,r])),cache=new Map();
function historicalVersion(q){
 assert.ok(q,'question exists');const r=rows.get(q.id);if(!r)return q;
 // A changed current record is never silently replaced with historical data.
 assert.equal(digest(q),r.afterHash,q.id+' current approved snapshot');
 if(!cache.has(r.file))cache.set(r.file,JSON.parse(execFileSync('git',['show',`${bridge.baselineCommit}:data/${r.file}`],{cwd:root,encoding:'utf8',maxBuffer:10*1024*1024})));
 const old=cache.get(r.file).find(x=>x.id===q.id);assert.ok(old,q.id);
 assert.equal(digest(old),r.beforeHash,q.id+' historical snapshot');
 for(const field of ['id','part','type','status','lastVerified','source'])assert.deepEqual(q[field],old[field],q.id+' '+field);
 const key=x=>x.answers.filter(a=>a.correct).map(a=>a.id).sort();
 assert.deepEqual(key(q),key(old),q.id+' unchanged answer key');assert.deepEqual(key(q),r.preservedKey,q.id);
 assert.equal(digest(q.legalBasis)!==digest(old.legalBasis),r.basisChanged,q.id);
 if(r.basisChanged)assert.ok(bridge.basisAmendments[q.id],q.id+' declared basis amendment');
 return structuredClone(old);
}
module.exports={bridge,digest,historicalVersion};
