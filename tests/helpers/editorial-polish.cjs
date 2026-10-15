const {createHash}=require('node:crypto'),assert=require('node:assert/strict');
const {read,effectiveBank}=require('../../scripts/lib/effective-bank.cjs');
const profile=read('data/editorial-polish-2026.json'),rows=new Map(profile.questions.map(r=>[r.id,r]));
const before=new Map(effectiveBank().map(q=>[q.id,q]));
const answerProfile=read('data/answer-review-2026.json'),answerRows=new Map(answerProfile.questions.map(r=>[r.id,r]));
const beforeAnswers=new Map(effectiveBank({polish:true}).map(q=>[q.id,q]));
const sha=q=>createHash('sha256').update(JSON.stringify(q)).digest('hex');
function answersExpected(q){
 const r=answerRows.get(q.id);if(!r)return q;
 assert.equal(sha(q),r.beforeSha256,q.id+' exact pre-answer snapshot');
 const after={...q,answers:r.answers};assert.equal(sha(after),r.afterSha256,q.id+' exact post-answer snapshot');
 return after;
}
function beforeAnswerVersion(q){
 const r=answerRows.get(q.id);if(!r)return q;
 assert.equal(sha(q),r.afterSha256,q.id+' current answer snapshot');
 const old=beforeAnswers.get(q.id);assert.equal(sha(old),r.beforeSha256,q.id);
 return old;
}
function polishedExpected(q){
 const r=rows.get(q.id);if(!r)return answersExpected(q);
 assert.equal(sha(q),r.beforeSha256,q.id+' exact pre-polish snapshot');
 assert.equal(sha(r.after),r.afterSha256,q.id+' exact post-polish snapshot');
 return answersExpected(r.after);
}
function unpolishedVersion(q){
 q=beforeAnswerVersion(q);
 const r=rows.get(q.id);if(!r)return q;
 assert.equal(sha(q),r.afterSha256,q.id+' current polished snapshot');
 const old=before.get(q.id);assert.equal(sha(old),r.beforeSha256,q.id);
 return old;
}
module.exports={profile,answerProfile,sha,polishedExpected,unpolishedVersion,answersExpected,beforeAnswerVersion};
