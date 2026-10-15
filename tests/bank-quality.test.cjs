const test=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const {historicalVersion}=require('./helpers/editorial-versions.cjs');
const files=['questions.json','derived-questions.json',...Array.from({length:5},(_,i)=>`expansion-2026-batch-0${i+1}.json`),'validated-2026.json','imported-exams-2026.json','imported-deposit-2026.json','imported-authorization-2026.json','imported-family-2026.json','imported-inheritance-2026.json','completion-2026.json','refinement-2026.json','verified-new-2026.json'];
const bank=files.flatMap(f=>read(`data/${f}`));const eligible=bank.filter(q=>['active','verified'].includes(q.status));
const legalRepairs=new Map(read('editorial/legal-transition-repairs-2026-10-10.json').repairs.map(r=>[r.id,r]));
// Historical editorial evidence stays immutable. Later statutory repairs must
// match their complete approved after-snapshot before using the old version.
const atEditorialReview=q=>{q=historicalVersion(q);const r=legalRepairs.get(q.id);if(!r)return q;assert.deepEqual(q,r.after,q.id);return r.before;};
test('100 harder scenarios replace every stem and distractor while preserving independent keys and linked legal evidence',()=>{
 const names=['calibration-20-2026','calibration-40-2026','calibration-next-40-2026'];
 const current=names.flatMap(n=>read(`data/${n}.json`));
 const commit='18a5deaa69096772ae5318b7d8162e740a9f19ed';
 const before=names.flatMap(n=>JSON.parse(require('node:child_process').execFileSync('git',['show',`${commit}:data/${n}.json`],{cwd:root,encoding:'utf8'})));
 const legal=read('reports/difficulty-upgrade-100-legal-review-2026-10-12.json');
 const report=read('reports/difficulty-upgrade-100-2026-10-12.json');
 assert.equal(current.length,100);assert.equal(report.questions.length,100);assert.equal(legal.questions.length,100);
 for(let i=0;i<100;i++){
  const q=current[i],old=before[i];assert.equal(q.id,old.id);assert.equal(q.part,old.part);assert.equal(q.type,old.type);
  assert.deepEqual(q.answerKey,old.answerKey,q.id);assert.deepEqual(q.answers.map(a=>a.correct),old.answers.map(a=>a.correct),q.id);
  assert.notDeepEqual(q.question.variants,old.question.variants,q.id);
  for(let j=0;j<4;j++)if(!q.answers[j].correct){assert.notEqual(q.answers[j].text,old.answers[j].text,q.id);assert.ok(q.answers[j].explanation);}
  assert.equal(q.difficulty,'advanced');assert.equal(q.empiricallyCalibrated,false);
  assert.equal(q.audit.evidenceFile,'reports/difficulty-upgrade-100-legal-review-2026-10-12.json');
  const decision=legal.questions.find(x=>x.id===q.id);assert.deepEqual(decision.answerKey,q.answerKey);
  assert.ok(decision.evidenceKeys.length&&decision.evidenceKeys.every(k=>legal.evidence[k]?.excerpt.length>80),q.id);
 }
 const answer=n=>current.find(q=>q.id===`CAL26-${String(n).padStart(3,'0')}`).answers.filter(a=>a.correct).map(a=>a.text).join(' ');
 assert.match(answer(5),/09:20/);assert.match(answer(11),/300 triệu/);assert.match(answer(12),/30, 10, 3 năm/);
 assert.match(answer(21),/Giá mới.*sửa đổi.*tên đường.*kỹ thuật/);
 assert.match(answer(25),/Y.*bồi thường.*Z.*tự bồi thường/);
 assert.match(answer(63),/di chúc và phí lưu giữ/);
 assert.match(answer(72),/20 năm.*văn bản.*sáu tháng/);
 assert.match(answer(89),/Không đáp ứng tự viết/);
 assert.match(answer(93),/200 triệu.*giá lúc chia/);
 const checks=read('reports/difficulty-upgrade-100-checks-2026-10-12.json');
 assert.ok(checks.correctStrictlyLongestSingleAfter<=20);assert.equal(checks.multipleSubsetsChecked,640);
});
test('60-question refinement batch retains authored variants, individual review and independent evidence keys',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const worksheet=read('editorial/variant-batch-60-2026-10-09.json');
 const drafts=read('editorial/refinement-variants-2026-10-09.json');
 const proofs=new Map(read('reports/refinement-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 const ids=[...Array.from({length:40},(_,i)=>`REFIN26-CC-${String(i+1).padStart(3,'0')}`),...Array.from({length:20},(_,i)=>`REFIN26-QT-${String(i+1).padStart(3,'0')}`)];
 assert.ok(ids.every(id=>Object.hasOwn(drafts,id)));
 assert.deepEqual(Object.keys(worksheet.reviews).sort(),ids.slice().sort());
 assert.ok(report.editoriallyReviewedQuestions>=343);
 assert.ok(report.remainingQuestions<=240);
 const batch=report.batches.find(b=>b.id==='refinement-60-2026-10-09');
 assert.equal(batch.questions,60);
 assert.deepEqual(batch.ids,ids.slice().sort());
 for(const id of ids){
  const q=historicalVersion(bank.find(q=>q.id===id)),d=report.decisions.find(d=>d.id===id);
  assert.equal(d.editorialReasoning,worksheet.reviews[id],id);
  assert.equal(d.answerKey,worksheet.answerKeys[id],id);
  assert.equal(d.answerKey,proofs.get(id).answer,id);
  assert.equal(d.before.question.variants.length,1,id);
  assert.deepEqual(q.question.variants.slice(1),drafts[id].map(v=>'Tháng 10/2026: '+v),id);
  assert.equal(q.lastVerified,d.before.lastVerified,id);
  assert.ok(!report.remainingIds.includes(id),id);
 }
});
test('100-question continuation adds exactly 200 authored stems and excludes archived completion',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const sheet=read('editorial/variant-batch-100-2026-10-09.json');
 const ids=[...read('data/completion-2026.json').filter(q=>q.status==='active').map(q=>q.id),...Array.from({length:5},(_,i)=>`REFIN26-QT-${String(i+21).padStart(3,'0')}`),...Array.from({length:15},(_,i)=>`REFIN26-DAT-${String(i+1).padStart(3,'0')}`),'INH26-015'].sort();
 assert.equal(ids.length,100);
 assert.deepEqual(Object.keys(sheet.reviews).sort(),ids);
 assert.deepEqual(Object.keys(sheet.answerKeys).sort(),ids);
 assert.ok(report.editoriallyReviewedQuestions>=443);
 assert.ok(report.remainingQuestions<=140);
 assert.equal(report.activeCount,594);
 const batch=report.batches.find(b=>b.id==='completion-refinement-inheritance-100-2026-10-09');
 assert.deepEqual(batch.ids,ids);
 assert.equal(batch.authoredVariants,200);
 const drafts={...read('editorial/completion-variants-2026-10-09.json'),...read('editorial/refinement-variants-2026-10-09.json'),...read('editorial/inheritance-variants-2026-10-09.json')};
 const proofs=new Map(['completion','refinement','inheritance'].flatMap(g=>read(`reports/${g}-legal-evidence-2026.json`).questions).map(q=>[q.id,q]));
 for(const id of ids){
  const q=atEditorialReview(bank.find(q=>q.id===id)),d=report.decisions.find(d=>d.id===id);
  assert.equal(q.status,'active',id);
  assert.equal(d.before.question.variants.length,1,id);
  assert.equal(q.question.variants[0],d.before.question.variants[0],id);
  assert.deepEqual(q.question.variants.slice(1),drafts[id].map(v=>'Tháng 10/2026: '+v),id);
  assert.equal(q.lastVerified,d.before.lastVerified,id);
  assert.deepEqual(q.source,d.before.source,id);
  assert.equal(d.editorialReasoning,sheet.reviews[id],id);
  assert.equal(d.answerKey,sheet.answerKeys[id],id);
  assert.deepEqual(q.legalBasis,proofs.get(id).provisions.map(p=>p.reference),id);
  if(proofs.get(id).answer)assert.equal(d.answerKey,proofs.get(id).answer,id);
  assert.ok(sheet.reviews[id].length>40,id);
  assert.equal(new Set(q.question.variants).size,3,id);
 }
 assert.ok(!Object.hasOwn(drafts,'COMP26-DAT-002'));
 assert.equal(bank.find(q=>q.id==='COMP26-DAT-002').question.variants.length,1);
 assert.ok(report.remainingIds.filter(id=>id.startsWith('INH26-')).every(id=>Number(id.slice(-3))>=16));
});
test('next 100-question batch preserves complete original records, independent keys and deferred scope',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const scope=read('editorial/variant-batch-next-100-scope-2026-10-09.json');
 const sheet=read('editorial/variant-batch-next-100-2026-10-09.json');
 const ids=scope.ids.slice().sort();
 assert.equal(ids.length,100);assert.equal(new Set(ids).size,100);
 assert.equal(ids.filter(id=>id.startsWith('INH26-')).length,17);
 assert.equal(ids.filter(id=>id.startsWith('IMP-')).length,83);
 assert.deepEqual(Object.keys(sheet.reviews).sort(),ids);
 assert.deepEqual(Object.keys(sheet.answerKeys).sort(),ids);
 assert.ok(report.editoriallyReviewedQuestions>=543);
 assert.ok(report.remainingQuestions<=40);
 assert.equal(report.activeCount,594);
 assert.ok(report.activeVariantStrings>=1702);
 assert.ok(report.newlyAuthoredVariants>=1086);
 assert.ok(eligible.filter(q=>q.question.variants.length===3).length>=554);
 const batch=report.batches.find(b=>b.id==='inheritance-exams-next-100-2026-10-09');
 assert.deepEqual(batch.ids,ids);
 assert.equal(batch.authoredVariants,200);
 const drafts={...read('editorial/inheritance-variants-2026-10-09.json'),...read('editorial/exams-variants-2026-10-09.json')};
 const proofs=new Map(['inheritance','exam'].flatMap(g=>read(`reports/${g}-legal-evidence-2026.json`).questions).map(q=>[q.id,q]));
 for(const id of ids){
  const q=historicalVersion(bank.find(q=>q.id===id)),d=report.decisions.find(d=>d.id===id);
  assert.equal(q.status,'active',id);assert.equal(d.before.question.variants.length,1,id);
  assert.equal(q.question.variants[0],d.before.question.variants[0],id);
  assert.deepEqual(q.question.variants.slice(1),drafts[id].map(v=>'Tháng 10/2026: '+v),id);
  assert.equal(d.answerKey,sheet.answerKeys[id],id);
  assert.equal(q.answers.find(a=>a.correct).id,sheet.answerKeys[id],id);
  assert.equal(d.editorialReasoning,sheet.reviews[id],id);
  assert.deepEqual(q.legalBasis,proofs.get(id).provisions.map(p=>p.reference),id);
  assert.ok(proofs.get(id).provisions.every(p=>p.evidenceExcerpt.length>100),id);
  const restored=structuredClone(q);restored.question.variants=d.before.question.variants;
  const addedAudit=['variantReviewDate','variantReviewStatus','variantEvidenceReport','legalReviewStatus'];
  for(const name of addedAudit)delete restored.audit[name];
  Object.assign(restored.audit,d.before.audit||{});
  if(!d.before.audit&&Object.keys(restored.audit).length===0)delete restored.audit;
  assert.deepEqual(restored,d.before,id);
  assert.ok(sheet.reviews[id].length>80,id);
 }
 assert.deepEqual(report.remainingIds.filter(id=>id.startsWith('INH26-')),[]);
 assert.ok(!ids.includes('IMP-T60-038'));assert.ok(ids.includes('IMP-T60-096'));
 const deferred=read('editorial/variant-next-100-follow-up-2026-10-09.json').items;
 assert.equal(deferred.length,5);
 for(const note of deferred){
  assert.ok(!ids.includes(note.id),note.id);
  // Their dated pre-application snapshot still proves these were deferred in
  // the previous batch, even after a later authorized repair completes them.
  assert.equal(report.decisions.find(d=>d.id===note.id).before.question.variants.length,1,note.id);
  assert.equal(note.appliedInThisBatch,false,note.id);
 }
});
test('substantive variant migration preserves each reviewed four-answer set and explicit legal certification limits',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const reviewed=new Set(report.decisions.map(d=>d.id));
 assert.equal(reviewed.size,report.editoriallyReviewedQuestions);
 assert.equal(reviewed.size+report.remainingIds.length,report.initialScope);
 assert.equal(report.allActiveLegallyRecertified,false);
 assert.equal(report.phaseStatus,'VARIANT_SCOPE_COMPLETE_LEGAL_REVIEW_NOT_CERTIFIED');
 const repairs=read('editorial/exam-explanation-repairs-final-2026-10-09.json').repairs;
 for(const d of report.decisions){
  const q=atEditorialReview(bank.find(q=>q.id===d.id));
  assert.ok(q,d.id);
  assert.deepEqual(q.answers,d.before.answers,d.id);
  assert.deepEqual(q.legalBasis,d.legalBasis,d.id);
  assert.equal(q.answers.find(a=>a.correct).id,d.answerKey,d.id);
  if(Object.hasOwn(repairs,d.id)){
   assert.equal(q.explanation,repairs[d.id].afterExplanation,d.id);
   assert.equal(d.before.explanation,repairs[d.id].beforeExplanation,d.id);
   assert.equal(d.explanationChanged,true,d.id);
  }else assert.equal(q.explanation,d.before.explanation,d.id);
  assert.deepEqual(q.question.variants,d.afterVariants,d.id);
  assert.equal(q.question.variants.length,3,d.id);
  assert.ok(q.audit.variantEvidenceReport,d.id);
  assert.equal(d.variantChecks.length,3,d.id);
  assert.ok(!report.remainingIds.includes(d.id),d.id);
 }
 const scopeCase=bank.find(q=>q.id==='CC-034');
 assert.ok(scopeCase.question.variants.every(v=>/đã từng|từng hành nghề/.test(v)));
});
test('final 40 completes exactly the original variant scope with 80 stems and no bank expansion',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const scope=read('editorial/variant-final-40-scope-2026-10-09.json');
 const sheet=read('editorial/variant-final-40-2026-10-09.json');
 const initial=read('editorial/variant-plan-2026-10-09.json');
 const drafts=read('editorial/exams-variants-2026-10-09.json');
 const proofs=new Map(read('reports/exam-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 const ids=scope.ids.slice().sort();
 assert.equal(ids.length,40);assert.equal(new Set(ids).size,40);
 assert.deepEqual(Object.keys(sheet.answerKeys).sort(),ids);
 assert.deepEqual(Object.keys(sheet.reviews).sort(),ids);
 assert.equal(report.editoriallyReviewedQuestions,583);
 assert.deepEqual(report.decisions.map(d=>d.id).sort(),initial.scopeIds.slice().sort());
 assert.equal(report.remainingQuestions,0);assert.deepEqual(report.remainingIds,[]);
 assert.equal(report.activeCount,594);assert.equal(report.activeVariantStrings,1782);
 assert.equal(report.newlyAuthoredVariants,1166);
 assert.equal(eligible.filter(q=>q.question.variants.length===3).length,594);
 assert.deepEqual(report.latestBatch.ids,ids);assert.equal(report.latestBatch.authoredVariants,80);
 assert.equal(report.allActiveLegallyRecertified,false);
 const repairs=read('editorial/exam-explanation-repairs-final-2026-10-09.json').repairs;
 for(const id of ids){
  const q=historicalVersion(bank.find(q=>q.id===id)),d=report.decisions.find(d=>d.id===id);
  assert.equal(q.status,'active',id);assert.equal(d.before.question.variants.length,1,id);
  assert.equal(q.question.variants[0],d.before.question.variants[0],id);
  assert.deepEqual(q.question.variants.slice(1),drafts[id].map(v=>'Tháng 10/2026: '+v),id);
  assert.equal(q.answers.find(a=>a.correct).id,sheet.answerKeys[id],id);
  assert.equal(d.answerKey,sheet.answerKeys[id],id);
  assert.equal(d.editorialReasoning,sheet.reviews[id],id);
  assert.deepEqual(q.legalBasis,proofs.get(id).provisions.map(p=>p.reference),id);
  const restored=structuredClone(q);restored.question.variants=d.before.question.variants;
  if(Object.hasOwn(repairs,id))restored.explanation=repairs[id].beforeExplanation;
  for(const field of ['variantReviewDate','variantReviewStatus','variantEvidenceReport','legalReviewStatus','explanationReviewDate','explanationReviewStatus','explanationRepairFile'])delete restored.audit[field];
  Object.assign(restored.audit,d.before.audit||{});
  if(!d.before.audit&&Object.keys(restored.audit).length===0)delete restored.audit;
  assert.deepEqual(restored,d.before,id);
 }
});
test('exactly five authorized explanation repairs keep independent keys and preserve pre-repair records',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const repairs=read('editorial/exam-explanation-repairs-final-2026-10-09.json').repairs;
 const ids=['IMP-T60-023','IMP-T60-038','IMP-T60-039','IMP-T60-071','IMP-T60-085'];
 assert.deepEqual(Object.keys(repairs).sort(),ids);
 assert.deepEqual(report.decisions.filter(d=>d.explanationChanged).map(d=>d.id).sort(),ids);
 assert.deepEqual(report.explanationRepairs.ids,ids);assert.equal(report.explanationRepairs.count,5);
 for(const id of ids){
  const q=historicalVersion(bank.find(q=>q.id===id)),d=report.decisions.find(d=>d.id===id),r=repairs[id];
  assert.deepEqual(d.before,r.beforeRecord,id);
  assert.equal(q.explanation,r.afterExplanation,id);
  assert.notEqual(q.explanation,r.beforeExplanation,id);
  assert.deepEqual(q.answers,r.beforeRecord.answers,id);
  assert.equal(q.answers.find(a=>a.correct).id,r.answerKey,id);
  assert.equal(q.lastVerified,r.beforeRecord.lastVerified,id);
  assert.deepEqual(q.legalBasis,r.legalBasis,id);
  assert.equal(q.audit.explanationRepairFile,d.explanationRepairFile,id);
 }
 const rental=bank.find(q=>q.id==='IMP-T60-038');
 assert.match(rental.explanation,/không quá 50% giá trị hợp đồng/);
 assert.doesNotMatch(rental.explanation,/mức thông thường là 20%/);
});
test('every previously pending stored question has a specific editorial decision and linked evidence',()=>{
 const report=read('reports/pending-review-decisions-2026.json');const evidence=new Map(read('reports/pending-review-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(report.decisions.length,36);assert.equal(new Set(report.decisions.map(q=>q.id)).size,36);assert.equal(report.promotedAfterRewrite,26);assert.equal(report.archivedAsDuplicateCompetence,10);
 assert.equal(bank.filter(q=>q.status==='review').length,0);
 for(const d of report.decisions){const q=bank.find(q=>q.id===d.id);assert.equal(q.status,d.after);if(d.after==='active'){assert.deepEqual(evidence.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.equal(evidence.get(q.id).answer,q.answers.find(a=>a.correct).id);assert.ok(evidence.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>50&&/Điều|Sửa đổi/.test(p.evidenceExcerpt)),q.id);}else{assert.ok(d.replacedBy.length);assert.ok(d.replacedBy.every(id=>eligible.some(q=>q.id===id)),q.id);}}
});
test('inheritance cases link specific source branches and verified current provisions',()=>{
 const questions=read('data/imported-inheritance-2026.json');const source=read('reports/inheritance-source-review.json');const proof=new Map(read('reports/inheritance-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,32);assert.equal(source.questions.length,45);assert.equal(source.readScope.embeddedImages,24);
 for(const q of questions){assert.equal(q.lastVerified,'2026-10-06');assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.ok(q.explanation.length>=100,q.id);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));assert.doesNotMatch(JSON.stringify(q.legalBasis),/29\/2015|04\/2026/);}
 assert.ok(source.questions.filter(s=>s.decision==='review').every(s=>s.adaptedQuestionIds.length===0));
 assert.equal(eligible.length,437+read('data/completion-2026.json').length+read('data/refinement-2026.json').length-read('reports/refinement-editorial-decisions-2026.json').archivedAsDuplicateCompetence);
});
test('family cases link reviewed source branches, current article evidence and independent keys',()=>{
 const questions=read('data/imported-family-2026.json');const source=read('reports/family-source-review.json');const proof=new Map(read('reports/family-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,26);assert.equal(source.questions.length,41);assert.equal(source.readScope.embeddedImages,44);
 for(const q of questions){assert.equal(q.lastVerified,'2026-10-06');assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.ok(q.explanation.length>=100,q.id);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 assert.equal(source.duplicateSections.length,3);assert.ok(source.questions.filter(s=>s.decision==='review').every(s=>s.adaptedQuestionIds.length===0));
});
test('authorization cases carry precise legal evidence and never duplicate the source appendix',()=>{
 const questions=read('data/imported-authorization-2026.json');const source=read('reports/authorization-source-review.json');const proof=new Map(read('reports/authorization-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,20);assert.equal(source.questions.length,31);
 for(const q of questions){assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.ok(q.explanation.length>=100,q.id);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 const appendix=source.questions.filter(s=>s.id.startsWith('AUTH-SRC-4.'));assert.equal(appendix.length,7);assert.ok(appendix.every(s=>s.decision==='duplicate_source_review'&&s.adaptedQuestionIds.length===0));
});
test('all stored IDs and answer IDs are unique; single questions have exactly one key',()=>{assert.equal(new Set(bank.map(q=>q.id)).size,bank.length);for(const q of bank){assert.equal(new Set(q.answers.map(a=>a.id)).size,q.answers.length,q.id);if(q.type==='single')assert.equal(q.answers.filter(a=>a.correct===true).length,1,q.id);}});

test('80 independently authored completion cases have exact keys and linked article evidence',()=>{
 const questions=read('data/completion-2026.json').map(atEditorialReview);const proof=new Map(read('reports/completion-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,80);assert.equal(proof.size,80);
 for(const q of questions){assert.equal(q.lastVerified,'2026-10-07');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.equal(q.status,q.id==='COMP26-DAT-002'?'archived':'active');assert.equal(q.source.type,'official');assert.deepEqual(q.legalBasis,proof.get(q.id).provisions.map(p=>p.reference));assert.equal(q.answers.find(a=>a.correct).id,proof.get(q.id).answer);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));assert.equal(new Set(q.answers.map(a=>a.text)).size,4);}
});

test('active citations are linked and future rules require an explicit application date',()=>{
 for(const q of eligible){assert.ok(q.legalBasis.every(b=>typeof b==='object'&&/^Điều \d+/.test(b.article)&&/^https:\/\//.test(b.url)),q.id);if(JSON.stringify(q.legalBasis).includes('04/2026/QH16')&&q.id!=='CC-090')for(const v of q.question.variants)assert.ok(v.includes('01/01/2027'),q.id);}
 const q=bank.find(q=>q.id==='CC-058');assert.match(q.question.variants[0],/^Từ 01\/01\/2027/);
});

test('80 refinement cases resolve every reference to statutory evidence and one dated key',()=>{
 const questions=read('data/refinement-2026.json');const registry=read('reports/refinement-provisions-2026.json');
 const proof=new Map(read('reports/refinement-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,80);assert.equal(proof.size,80);
 const keys={A:0,B:0,C:0,D:0};
 for(const q of questions){const e=proof.get(q.id);assert.equal(q.status,'active');assert.equal(q.lastVerified,'2026-10-07');assert.equal(e.applicableAt,'2026-10-07');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.deepEqual(q.legalBasis,e.provisions.map(p=>p.reference));assert.equal(q.answers.find(a=>a.correct).id,e.answer);keys[e.answer]++;
  for(const p of e.provisions){const {documentCode,article}=p.evidenceRef;const text=registry.articles[documentCode][article];assert.match(text,new RegExp(`Điều ${article}\\.`));assert.ok(text.length>100,q.id);assert.equal(registry.documents[documentCode].title,p.reference.document);assert.equal(registry.documents[documentCode].url,p.reference.url);}
  assert.doesNotMatch(JSON.stringify(q.legalBasis),/04\/2026\/QH16/);
 }
 assert.deepEqual(keys,{A:20,B:20,C:20,D:20});
});
test('later duplicate decisions retain IDs and keys while excluding all three from new sessions',()=>{
 const report=read('reports/refinement-editorial-decisions-2026.json');assert.equal(report.decisions.length,3);
 for(const d of report.decisions){const q=bank.find(q=>q.id===d.id);assert.equal(q.status,'archived');assert.equal(q.audit.reason,'duplicate_competence');assert.deepEqual(q.audit.replacedBy,d.replacedBy);assert.ok(d.replacedBy.every(id=>eligible.some(q=>q.id===id)));assert.equal(q.answers.filter(a=>a.correct).length,1);assert.ok(q.question.variants.length&&q.legalBasis.length);}
 assert.equal(eligible.length,594);
});
test('eligible questions have distinct stems, explanations, registered sources and dated future law',()=>{const seen=new Set();const sources=new Set(read('data/question-sources.json').sources.map(s=>s.id));for(const q of eligible){assert.ok(q.explanation.length>=100,q.id);assert.ok(q.legalBasis.length,q.id);assert.ok(sources.has(q.source.id),q.id);assert.match(q.lastVerified,/^\d{4}-\d{2}-\d{2}$/,q.id);assert.equal(new Date(q.lastVerified).toISOString().slice(0,10),q.lastVerified,q.id);assert.ok(q.lastVerified<='2026-10-10',q.id);assert.ok(q.difficulty&&q.questionForm,q.id);for(const v of q.question.variants){const key=v.toLocaleLowerCase('vi').replace(/[^\p{L}\p{N}]+/gu,' ').trim();assert.ok(!seen.has(key),q.id);seen.add(key);if(JSON.stringify(q.legalBasis).includes('04/2026/QH16'))assert.match(v,/2027|hiệu lực từ|có hiệu lực|thông qua|chuyển tiếp/i,q.id);}}});
test('new cases each carry traceable article evidence and precise references',()=>{const evidence=read('reports/legal-evidence-2026.json');const rows=new Map(evidence.questions.map(q=>[q.id,q]));for(const q of read('data/validated-2026.json')){assert.ok(q.question.variants.every(v=>v.startsWith('Tháng 10/2026:')),q.id);const e=rows.get(q.id);assert.ok(e,q.id);assert.equal(e.provisions.length,q.legalBasis.length,q.id);q.legalBasis.forEach((b,i)=>{assert.match(b.article,/^Điều \d+/);assert.match(b.url,/^https:\/\//);assert.deepEqual(e.provisions[i].reference,b,q.id);assert.ok(e.provisions[i].evidenceExcerpt.length>100,q.id);});}});
test('mechanical expansion cannot enter practice or exams',()=>{for(const q of bank.filter(q=>q.id.startsWith('EXP26-'))){assert.equal(q.status,'archived',q.id);assert.equal(q.lastVerified,null,q.id);assert.equal(q.audit.reason,'mechanical_paraphrase',q.id);}});

test('deposit cases have article evidence and linked source provenance; appendix stays review',()=>{
 const questions=read('data/imported-deposit-2026.json');const proof=new Map(read('reports/deposit-legal-evidence-2026.json').questions.map(q=>[q.id,q]));const source=read('reports/deposit-source-review.json');
 assert.equal(source.questions.length,25);assert.equal(questions.length,18);
 for(const q of questions){assert.equal(q.source.id,source.sourceId);assert.equal(q.part,2);assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.ok(q.explanation.length>=100,q.id);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 assert.ok(source.questions.filter(s=>s.id.includes('APP')).every(s=>s.decision==='review'&&s.adaptedQuestionIds.length===0));
});

test('imported exams preserve every source item and certify only linked adapted questions',()=>{
 const source=read('reports/exam-source-review.json');const imported=read('data/imported-exams-2026.json');const evidence=new Map(read('reports/exam-legal-evidence-2026.json').questions.map(q=>[q.id,q]));const origins=new Map(source.questions.map(q=>[q.id,q]));
 assert.equal(source.questions.length,151);assert.equal(new Set(source.questions.map(q=>q.id)).size,151);assert.equal(source.questions.filter(q=>q.sourceDocument==='Đề tháng 9/2024').length,50);assert.equal(source.questions.filter(q=>q.sourceDocument!=='Đề tháng 9/2024').length,101);
 for(const q of imported){const original=origins.get(q.id);assert.ok(original,q.id);assert.match(original.sourceSha256,/^[a-f0-9]{64}$/);assert.ok(original.originalBlock,q.id);assert.ok([1,2].includes(q.part),q.id);assert.equal(q.source.questionNumber,original.sourceQuestionNumber);assert.equal(q.source.type,'user-provided');assert.deepEqual(evidence.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(evidence.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));assert.ok(q.explanation.length>=100,q.id);if(q.status==='active')assert.equal(original.decision,'adapted_active');else {assert.equal(q.status,'archived');assert.equal(original.decision,'duplicate_bank');}}
 for(const original of source.questions.filter(q=>q.decision==='review'))assert.ok(!imported.some(q=>q.id===original.id&&q.status==='active'),original.id);
});

test('October legal audit seals all 594 questions and applies old-certificate, age and archive transitions',()=>{
 const crypto=require('node:crypto');
 const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(', ')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+': '+canonical(v[k])).join(', ')+'}';
 const digest=v=>crypto.createHash('sha256').update(canonical(v)).digest('hex');
 const audit=read('reports/legal-review-register-2026-10-10.json');
 assert.equal(audit.questions.length,594);assert.equal(audit.counts.stems,1782);
 assert.equal(audit.counts.freshFullComponentReviews,112);assert.equal(audit.counts.existingLegalDossiersRevalidated,482);
 assert.equal(audit.allActiveLegallyRecertified,false);
 for(const r of audit.questions){const q=historicalVersion(eligible.find(q=>q.id===r.id));assert.ok(q,r.id);assert.equal(digest(q),r.questionHash,r.id);assert.equal(digest(q),r.legalReviewDecision.reviewedQuestionHash,r.id);assert.deepEqual(q.answers.filter(a=>a.correct).map(a=>a.id),r.key,r.id);}
 const get=id=>eligible.find(q=>q.id===id);
 const certificate=get('COMP26-TS-005');assert.ok(certificate.question.variants.every(v=>v.includes('2020')));assert.match(certificate.answers.find(a=>a.correct).text,/chưa hết hiệu lực/);assert.ok(certificate.legalBasis.some(b=>b.article==='Điều 76'&&b.clause==='Khoản 2'));
 const archive=get('COMP26-QT-010');assert.match(archive.answers.find(a=>a.correct).text,/20 năm/);assert.doesNotMatch(archive.answers.find(a=>a.correct).text,/30 năm/);assert.ok(archive.legalBasis.some(b=>b.article==='Điều 76'&&b.clause==='Khoản 12'));
 assert.ok(get('CC-028').question.variants.every(v=>v.includes('không thuộc diện chuyển tiếp')));
});

test('100 new integrated cases link every applied provision and avoid answer-length and key-position shortcuts',()=>{
 const q=read('data/hard-integrated-100-2026.json');const legal=read('reports/hard-integrated-100-legal-review-2026-10-12.json');
 assert.equal(q.length,100);assert.equal(new Set(q.map(x=>x.id)).size,100);assert.equal(legal.questions.length,100);
 const older=['calibration-20-2026','calibration-40-2026','calibration-next-40-2026'].flatMap(n=>read(`data/${n}.json`));
 assert.ok(q.every(x=>!older.some(y=>y.id===x.id||y.question.variants[0]===x.question.variants[0])));
 const source=read('data/question-sources.json').sources.find(x=>x.id==='HARD100-20261012');assert.ok(source);
 for(const x of q){
  assert.equal(x.status,'active');assert.equal(x.empiricallyCalibrated,false);assert.equal(x.question.variants.length,1);
  assert.ok(x.rulesApplied.length>=3);assert.ok(x.integrationSteps.length>=3);assert.equal(new Set(x.rulesApplied).size,x.rulesApplied.length);
  assert.equal(x.answers.length,4);assert.equal(new Set(x.answers.map(a=>a.text)).size,4);assert.ok(x.answers.every(a=>a.explanation.length>=12));
  assert.deepEqual(x.answers.filter(a=>a.correct).map(a=>a.id),x.answerKey);
  assert.equal(x.type==='single'?x.answerKey.length===1:x.answerKey.length>=2&&x.answerKey.length<=3,true);
  const supplement=read('editorial/legal-evidence-supplement-2026-10-15.json');
  const historical=legal.questions.find(y=>y.id===x.id),amendment=supplement.questions.find(y=>y.id===x.id),row=amendment||historical;
  if(amendment)assert.deepEqual(historical.evidenceKeys,amendment.historicalEvidenceKeys);
  assert.deepEqual(row.evidenceKeys,x.rulesApplied);assert.deepEqual(row.answerKey,x.answerKey);
  for(const k of x.rulesApplied){const e=legal.evidence[k]||supplement.evidence[k];assert.ok(e&&e.excerpt.length>80,k);assert.ok(x.legalBasis.some(r=>r.document===e.document&&r.article===e.article&&r.url===e.url));}
 }
 const singles=q.filter(x=>x.type==='single');assert.equal(singles.length,60);
 for(const k of ['A','B','C','D'])assert.equal(singles.filter(x=>x.answerKey[0]===k).length,15);
 const longest=singles.filter(x=>{const right=x.answers.find(a=>a.correct).text.length;return right>Math.max(...x.answers.filter(a=>!a.correct).map(a=>a.text.length));});assert.ok(longest.length<=20);
 const text=n=>q.find(x=>x.id===`HARD26-${String(n).padStart(3,'0')}`).answers.filter(a=>a.correct).map(a=>a.text).join(' ');
 // Independent arithmetic/branch expectations, not just the boolean answer flags.
 assert.match(text(1),/3 tỷ.*2,4 tỷ.*600 triệu/);assert.match(text(2),/900.*450.*225/);assert.match(text(3),/1,2 tỷ từ B/);
 assert.match(text(5),/200 triệu/);assert.match(text(9),/400 triệu/);assert.match(text(10),/200 triệu.*giá lúc chia/);
 assert.match(text(13),/166⅔ triệu/);assert.match(text(43),/250 triệu/);assert.match(text(45),/200 triệu/);assert.match(text(47),/430 triệu/);
 assert.match(text(81),/500 triệu/);assert.match(text(92),/100 triệu.*50 triệu/);assert.match(text(95),/200 triệu/);assert.match(text(100),/900 triệu/);
});

test('67 guessability repairs have independent law evidence, three reasoning steps, plausible options and correct arithmetic',()=>{
 const profile=read('data/scenario-refinements-2026.json'),legal=read('reports/guessability-67-legal-review-2026-10-12.json');assert.equal(profile.questions.length,67);assert.equal(legal.questions.length,67);
 let cross=0;
 for(const r of profile.questions){const q=r.after,d=legal.questions.find(x=>x.id===r.id);
  assert.deepEqual(q,d.after);assert.ok(q.integrationSteps.length>=3);assert.equal(q.empiricallyCalibrated,false);
  assert.notEqual(q.question.variants[0],d.before.question.variants[0]);assert.equal(q.question.variants.length,1);assert.doesNotMatch(q.question.variants[0],/Điều\s+\d|Khoản\s+\d|quy định gì/i);
  assert.deepEqual(q.answerKey,d.answerKey);assert.deepEqual(q.answers.map(a=>[a.id,a.correct]),d.before.answers.map(a=>[a.id,a.correct]));
  assert.ok(q.answers.every(a=>a.text.length>40&&a.explanation.length>20));assert.equal(new Set(q.answers.map(a=>a.text)).size,4);
  const right=q.answers.find(a=>a.correct).text.length,wrong=q.answers.filter(a=>!a.correct).map(a=>a.text.length);assert.ok(right<=Math.max(...wrong)*1.6,r.id);
  assert.ok(d.evidenceKeys.length>=3);for(const k of d.evidenceKeys){const e=legal.evidence[k];assert.ok(e?.excerpt.length>60,k);assert.ok(q.legalBasis.some(b=>JSON.stringify(b)===JSON.stringify(e.reference)),r.id+' '+k);}
  const statutes=new Set(q.legalBasis.map(b=>/Công chứng/.test(b.document)?'CC':/Dân sự/.test(b.document)?'DS':/Hôn nhân/.test(b.document)?'HN':b.document));cross+=statutes.size>=2;
  if(q.legalBasis.some(b=>/04\/2026\/QH16/.test(b.document)))assert.match(q.question.variants[0],/^Từ 01\/01\/2027:/);
 }
 assert.equal(cross,64);
 const correct=id=>profile.questions.find(r=>r.id===id).after.answers.find(a=>a.correct).text;
 assert.match(correct('COMP26-DS-002'),/520 triệu/);assert.match(correct('IMP-SEP24-014'),/4 tỷ.*3 tỷ.*1 tỷ/);
 assert.match(correct('IMP-T60-027'),/1,8 tỷ.*600 triệu/);assert.match(correct('INH26-028'),/2 tỷ.*1,5 tỷ.*500 triệu/);
 assert.match(correct('INH26-021'),/1,5 tỷ.*750 triệu/);assert.match(correct('CC-005'),/08:40/);
});

test('60 remaining-case reviews have provision evidence, distinct scenarios, stable keys and bounded difficulty claims',()=>{
 const profile=read('data/scenario-refinements-remaining-2026.json'),legal=read('reports/remaining-60-legal-review-2026-10-13.json');
 const screening=read('reports/remaining-726-screening-2026-10-13.json'),prior=read('data/scenario-refinements-2026.json');
 assert.equal(profile.questions.length,60);assert.equal(legal.questions.length,60);assert.equal(screening.rows.length,726);
 assert.equal(screening.rewritten,60);assert.equal(screening.remainingOutsidePrevious67,666);assert.equal(screening.eligible,793);
 const oldIds=new Set(prior.questions.map(r=>r.id));let cross=0;
 for(const r of profile.questions){const q=r.after,d=legal.questions.find(x=>x.id===r.id);
  assert.ok(!oldIds.has(q.id));assert.deepEqual(q,d.after);assert.equal(q.empiricallyCalibrated,false);
  assert.equal(q.integrationSteps.length,3);assert.equal(q.question.variants.length,1);assert.match(q.question.variants[0],/^Tháng 10\/2026:/);
  assert.notEqual(q.question.variants[0],d.before.question.variants[0]);assert.doesNotMatch(q.question.variants[0],/Điều\s+\d|Khoản\s+\d|quy định gì/i);
  assert.deepEqual(q.answers.map(a=>[a.id,a.correct]),d.before.answers.map(a=>[a.id,a.correct]));assert.deepEqual(q.answerKey,d.answerKey);
  assert.equal(new Set(q.answers.map(a=>a.text)).size,4);assert.ok(q.answers.every(a=>a.text.length>=40&&a.explanation.length>20));
  const right=q.answers.find(a=>a.correct).text.length,wrong=q.answers.filter(a=>!a.correct).map(a=>a.text.length);assert.ok(right<=Math.max(...wrong)*1.6,q.id);
  assert.ok(d.evidenceKeys.length>=3);for(const k of d.evidenceKeys){const p=legal.evidence[k];assert.ok(p?.excerpt.length>60,k);assert.ok(p.reference.url.startsWith('https://'));assert.ok(q.legalBasis.some(b=>JSON.stringify(b)===JSON.stringify(p.reference)));}
  const groups=new Set(q.legalBasis.map(b=>/Công chứng/.test(b.document)?'CC':/Dân sự/.test(b.document)?'DS':/Hôn nhân/.test(b.document)?'HN':b.document));cross+=groups.size>=2;
 }
 assert.equal(cross,53);assert.equal(screening.crossStatuteNewRepairs,cross);
 assert.equal(new Set(profile.questions.map(r=>r.after.question.variants[0])).size,60);
 assert.ok(screening.rows.every(r=>r.empiricallyCalibrated===false));assert.equal(screening.trial.status,'pending');
 const right=id=>profile.questions.find(r=>r.id===id).after.answers.find(a=>a.correct).text;
 // Independent reference calculations: common-property separation, legal shares and guaranteed obligations.
 assert.match(right('FAM26-006'),new RegExp(`W tổng ${600/2+(600/2)/3} triệu`));
 assert.match(right('FAM26-026'),/mỗi người hưởng 1,5 tỷ/);assert.equal(3/2,1.5);
 assert.match(right('COMP26-DS-001'),new RegExp(`${500+20+5} triệu`));
 assert.match(right('COMP26-HN-001'),/tổng 2,5 tỷ/);assert.equal(1+(4-1)/2,2.5);
 assert.match(right('COMP26-TK-003'),new RegExp(`${(1500/2)*2/3} triệu`));
 assert.match(right('VER26-070'),new RegExp(`mỗi người ${40/2} triệu`));
 assert.match(right('AUTH26-018'),/30 triệu/);assert.equal(260-200,60);
});

test('129 priority reviews cover the exact cohort, preserve keys and dates, support arithmetic and do not claim empirical difficulty',()=>{
 const profile=read('data/scenario-priority-129-2026.json'),review=read('reports/priority-129-legal-review-2026-10-13.json');
 const target=read('reports/remaining-726-screening-2026-10-13.json').rows.filter(r=>r.disposition==='context_review_candidate').map(r=>r.id).sort();
 assert.equal(profile.questions.length,129);assert.deepEqual(profile.questions.map(r=>r.id).sort(),target);
 assert.equal(review.questions.length,129);assert.equal(review.dispositions.application_and_options_rewritten,53);assert.equal(review.dispositions.distractors_and_explanations_refined,76);
 let multiples=0;
 for(const r of profile.questions){const q=r.after,d=review.questions.find(d=>d.id===q.id);assert.deepEqual(q,d.after);assert.equal(q.empiricallyCalibrated,false);
  assert.deepEqual(q.answers.map(a=>[a.id,a.correct]),d.before.answers.map(a=>[a.id,a.correct]));assert.deepEqual(q.answerKey,d.answerKey);
  assert.equal(q.part,d.before.part);assert.equal(q.type,d.before.type);assert.equal(q.status,d.before.status);multiples+=q.type==='multiple';
  assert.equal(q.answers.length,4);assert.equal(new Set(q.answers.map(a=>a.text)).size,4);assert.ok(q.answers.every(a=>a.text.trim().length>=20&&a.explanation.length>20));
  const right=Math.max(...q.answers.filter(a=>a.correct).map(a=>a.text.length)),wrong=Math.max(...q.answers.filter(a=>!a.correct).map(a=>a.text.length));assert.ok(right<=1.6*wrong,q.id);
  assert.equal(q.integrationSteps.length,3);assert.ok(q.explanation.length>100);
  for(const k of d.evidenceKeys){const p=review.evidence[k];assert.ok(p?.excerpt.length>60,k);assert.ok(q.legalBasis.some(b=>JSON.stringify(b)===JSON.stringify(p.reference)),q.id+' '+k);assert.ok(p.reference.url.startsWith('https://'));}
  if(q.legalBasis.some(b=>b.document.includes('04/2026'))){assert.ok(q.question.variants.every(v=>v.startsWith('Từ 01/01/2027:')),q.id);}
  if(d.disposition==='application_and_options_rewritten'){assert.notDeepEqual(q.question,d.before.question);assert.doesNotMatch(q.question.variants[0],/Điều\s+\d|quy định gì/i);}
  else{assert.deepEqual(q.question,d.before.question);assert.equal(q.difficulty,d.before.difficulty);}
  assert.ok(q.answers.some((a,i)=>a.text!==d.before.answers[i].text));
 }
 assert.equal(multiples,5);
 const correct=id=>profile.questions.find(r=>r.id===id).after.answers.filter(a=>a.correct).map(a=>a.text).join(' ');
 assert.match(correct('HARD26-032'),/không biết và không phải biết/);assert.doesNotMatch(correct('HARD26-032'),/không biết hoặc phải biết/);
 assert.match(correct('VER26-061'),new RegExp(`mỗi con ${((600+.4*500)-100)/2} triệu`));
 assert.match(correct('VER26-073'),new RegExp(`${((1200-300)/3)*2/3} triệu`));
 assert.match(correct('VER26-077'),new RegExp(`mỗi ${((3600/2)/3)/2} triệu`));
 assert.match(correct('IMP-SEP24-037'),new RegExp(`${3000*.3-150} triệu`));
 assert.match(correct('CC-028'),/đến đủ 72/);assert.match(correct('HARD26-033'),/Chưa đủ ngoại lệ/);
});
