const test=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const files=['questions.json','derived-questions.json',...Array.from({length:5},(_,i)=>`expansion-2026-batch-0${i+1}.json`),'validated-2026.json','imported-exams-2026.json','imported-deposit-2026.json','imported-authorization-2026.json','imported-family-2026.json','imported-inheritance-2026.json','completion-2026.json','refinement-2026.json','verified-new-2026.json'];
const bank=files.flatMap(f=>read(`data/${f}`));const eligible=bank.filter(q=>['active','verified'].includes(q.status));
test('60-question refinement batch retains authored variants, individual review and independent evidence keys',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const worksheet=read('editorial/variant-batch-60-2026-10-09.json');
 const drafts=read('editorial/refinement-variants-2026-10-09.json');
 const proofs=new Map(read('reports/refinement-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 const ids=[...Array.from({length:40},(_,i)=>`REFIN26-CC-${String(i+1).padStart(3,'0')}`),...Array.from({length:20},(_,i)=>`REFIN26-QT-${String(i+1).padStart(3,'0')}`)];
 assert.deepEqual(Object.keys(drafts).sort(),ids.slice().sort());
 assert.deepEqual(Object.keys(worksheet.reviews).sort(),ids.slice().sort());
 assert.ok(report.editoriallyReviewedQuestions>=343);
 assert.ok(report.remainingQuestions<=240);
 const batch=report.batches.find(b=>b.id==='refinement-60-2026-10-09');
 assert.equal(batch.questions,60);
 assert.deepEqual(batch.ids,ids.slice().sort());
 for(const id of ids){
  const q=bank.find(q=>q.id===id),d=report.decisions.find(d=>d.id===id);
  assert.equal(d.editorialReasoning,worksheet.reviews[id],id);
  assert.equal(d.answerKey,worksheet.answerKeys[id],id);
  assert.equal(d.answerKey,proofs.get(id).answer,id);
  assert.equal(d.before.question.variants.length,1,id);
  assert.deepEqual(q.question.variants.slice(1),drafts[id].map(v=>'Tháng 10/2026: '+v),id);
  assert.equal(q.lastVerified,d.before.lastVerified,id);
  assert.ok(!report.remainingIds.includes(id),id);
 }
});
test('substantive variant migration preserves each reviewed four-answer set and retains an explicit incomplete register',()=>{
 const report=read('reports/substantive-variants-2026-10-09.json');
 const reviewed=new Set(report.decisions.map(d=>d.id));
 assert.equal(reviewed.size,report.editoriallyReviewedQuestions);
 assert.equal(reviewed.size+report.remainingIds.length,report.initialScope);
 assert.equal(report.allActiveLegallyRecertified,false);
 assert.equal(report.phaseStatus,'INCOMPLETE');
 for(const d of report.decisions){
  const q=bank.find(q=>q.id===d.id);
  assert.ok(q,d.id);
  assert.deepEqual(q.answers,d.before.answers,d.id);
  assert.deepEqual(q.legalBasis,d.legalBasis,d.id);
  assert.equal(q.answers.find(a=>a.correct).id,d.answerKey,d.id);
  assert.equal(q.explanation,d.before.explanation,d.id);
  assert.deepEqual(q.question.variants,d.afterVariants,d.id);
  assert.equal(q.question.variants.length,3,d.id);
  assert.ok(q.audit.variantEvidenceReport,d.id);
  assert.equal(d.variantChecks.length,3,d.id);
  assert.ok(!report.remainingIds.includes(d.id),d.id);
 }
 const scopeCase=bank.find(q=>q.id==='CC-034');
 assert.ok(scopeCase.question.variants.every(v=>/đã từng|từng hành nghề/.test(v)));
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
 for(const q of questions){assert.equal(q.lastVerified,'2026-10-06');assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.match(q.explanation,/Gợi ý làm bài:/);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));assert.doesNotMatch(JSON.stringify(q.legalBasis),/29\/2015|04\/2026/);}
 assert.ok(source.questions.filter(s=>s.decision==='review').every(s=>s.adaptedQuestionIds.length===0));
 assert.equal(eligible.length,437+read('data/completion-2026.json').length+read('data/refinement-2026.json').length-read('reports/refinement-editorial-decisions-2026.json').archivedAsDuplicateCompetence);
});
test('family cases link reviewed source branches, current article evidence and independent keys',()=>{
 const questions=read('data/imported-family-2026.json');const source=read('reports/family-source-review.json');const proof=new Map(read('reports/family-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,26);assert.equal(source.questions.length,41);assert.equal(source.readScope.embeddedImages,44);
 for(const q of questions){assert.equal(q.lastVerified,'2026-10-06');assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.match(q.explanation,/Gợi ý làm bài:/);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 assert.equal(source.duplicateSections.length,3);assert.ok(source.questions.filter(s=>s.decision==='review').every(s=>s.adaptedQuestionIds.length===0));
});
test('authorization cases carry precise legal evidence and never duplicate the source appendix',()=>{
 const questions=read('data/imported-authorization-2026.json');const source=read('reports/authorization-source-review.json');const proof=new Map(read('reports/authorization-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
 assert.equal(questions.length,20);assert.equal(source.questions.length,31);
 for(const q of questions){assert.equal(q.source.id,source.sourceId);assert.equal(q.status,'active');assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.match(q.explanation,/Gợi ý làm bài:/);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 const appendix=source.questions.filter(s=>s.id.startsWith('AUTH-SRC-4.'));assert.equal(appendix.length,7);assert.ok(appendix.every(s=>s.decision==='duplicate_source_review'&&s.adaptedQuestionIds.length===0));
});
test('all stored IDs and answer IDs are unique; single questions have exactly one key',()=>{assert.equal(new Set(bank.map(q=>q.id)).size,bank.length);for(const q of bank){assert.equal(new Set(q.answers.map(a=>a.id)).size,q.answers.length,q.id);if(q.type==='single')assert.equal(q.answers.filter(a=>a.correct===true).length,1,q.id);}});

test('80 independently authored completion cases have exact keys and linked article evidence',()=>{
 const questions=read('data/completion-2026.json');const proof=new Map(read('reports/completion-legal-evidence-2026.json').questions.map(q=>[q.id,q]));
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
test('eligible questions have distinct stems, explanations, registered sources and dated future law',()=>{const seen=new Set();const sources=new Set(read('data/question-sources.json').sources.map(s=>s.id));for(const q of eligible){assert.ok(q.explanation.length>=100,q.id);assert.ok(q.legalBasis.length,q.id);assert.ok(sources.has(q.source.id),q.id);assert.match(q.lastVerified,/^\d{4}-\d{2}-\d{2}$/,q.id);assert.equal(new Date(q.lastVerified).toISOString().slice(0,10),q.lastVerified,q.id);assert.ok(q.lastVerified<='2026-10-08',q.id);assert.ok(q.difficulty&&q.questionForm,q.id);for(const v of q.question.variants){const key=v.toLocaleLowerCase('vi').replace(/[^\p{L}\p{N}]+/gu,' ').trim();assert.ok(!seen.has(key),q.id);seen.add(key);if(JSON.stringify(q.legalBasis).includes('04/2026/QH16'))assert.match(v,/2027|hiệu lực từ|có hiệu lực|thông qua|chuyển tiếp/i,q.id);}}});
test('new cases each carry traceable article evidence and precise references',()=>{const evidence=read('reports/legal-evidence-2026.json');const rows=new Map(evidence.questions.map(q=>[q.id,q]));for(const q of read('data/validated-2026.json')){assert.ok(q.question.variants.every(v=>v.startsWith('Tháng 10/2026:')),q.id);const e=rows.get(q.id);assert.ok(e,q.id);assert.equal(e.provisions.length,q.legalBasis.length,q.id);q.legalBasis.forEach((b,i)=>{assert.match(b.article,/^Điều \d+/);assert.match(b.url,/^https:\/\//);assert.deepEqual(e.provisions[i].reference,b,q.id);assert.ok(e.provisions[i].evidenceExcerpt.length>100,q.id);});}});
test('mechanical expansion cannot enter practice or exams',()=>{for(const q of bank.filter(q=>q.id.startsWith('EXP26-'))){assert.equal(q.status,'archived',q.id);assert.equal(q.lastVerified,null,q.id);assert.equal(q.audit.reason,'mechanical_paraphrase',q.id);}});

test('deposit cases have article evidence and linked source provenance; appendix stays review',()=>{
 const questions=read('data/imported-deposit-2026.json');const proof=new Map(read('reports/deposit-legal-evidence-2026.json').questions.map(q=>[q.id,q]));const source=read('reports/deposit-source-review.json');
 assert.equal(source.questions.length,25);assert.equal(questions.length,18);
 for(const q of questions){assert.equal(q.source.id,source.sourceId);assert.equal(q.part,2);assert.match(q.question.variants[0],/^Tháng 10\/2026:/);assert.match(q.explanation,/Gợi ý làm bài:/);assert.ok(source.questions.some(s=>s.adaptedQuestionIds.includes(q.id)),q.id);assert.deepEqual(proof.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(proof.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));}
 assert.ok(source.questions.filter(s=>s.id.includes('APP')).every(s=>s.decision==='review'&&s.adaptedQuestionIds.length===0));
});

test('imported exams preserve every source item and certify only linked adapted questions',()=>{
 const source=read('reports/exam-source-review.json');const imported=read('data/imported-exams-2026.json');const evidence=new Map(read('reports/exam-legal-evidence-2026.json').questions.map(q=>[q.id,q]));const origins=new Map(source.questions.map(q=>[q.id,q]));
 assert.equal(source.questions.length,151);assert.equal(new Set(source.questions.map(q=>q.id)).size,151);assert.equal(source.questions.filter(q=>q.sourceDocument==='Đề tháng 9/2024').length,50);assert.equal(source.questions.filter(q=>q.sourceDocument!=='Đề tháng 9/2024').length,101);
 for(const q of imported){const original=origins.get(q.id);assert.ok(original,q.id);assert.match(original.sourceSha256,/^[a-f0-9]{64}$/);assert.ok(original.originalBlock,q.id);assert.ok([1,2].includes(q.part),q.id);assert.equal(q.source.questionNumber,original.sourceQuestionNumber);assert.equal(q.source.type,'user-provided');assert.deepEqual(evidence.get(q.id).provisions.map(p=>p.reference),q.legalBasis);assert.ok(evidence.get(q.id).provisions.every(p=>p.evidenceExcerpt.length>100));assert.match(q.explanation,/Gợi ý làm bài:/);if(q.status==='active')assert.equal(original.decision,'adapted_active');else {assert.equal(q.status,'archived');assert.equal(original.decision,'duplicate_bank');}}
 for(const original of source.questions.filter(q=>q.decision==='review'))assert.ok(!imported.some(q=>q.id===original.id&&q.status==='active'),original.id);
});
