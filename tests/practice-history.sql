-- Run against the configured project after practice-history.sql. No data retained.
begin;
set local role anon;
set local request.headers='{"x-client-info":"0000000001"}';
insert into public.practice_answers(id,session_id,learner_key,learner_name,question_id,part,topic,is_correct,graded_at,answer) values
 ('00000000-0000-4000-8000-000000001810','00000000-0000-4000-8000-000000001811','0000000001','Practice regression','TEST-PRACTICE',1,'TEST-TOPIC',false,now(),'{"variant":"test","answers":[],"selected":["B"],"correct_ids":["A"],"explanation":"test","legal_basis":[]}'),
 ('00000000-0000-4000-8000-000000001812','00000000-0000-4000-8000-000000001813','0000000001','Practice regression','TEST-PRACTICE',1,'TEST-TOPIC',true,now(),'{"variant":"test","answers":[],"selected":["A"],"correct_ids":["A"],"explanation":"test","legal_basis":[]}');
do $$ begin
 if (select count(*) from public.practice_answers where topic='TEST-TOPIC' and id in ('00000000-0000-4000-8000-000000001810','00000000-0000-4000-8000-000000001812'))<>2 then raise exception 'Own history missing'; end if;
 if (select count(*) from public.practice_answers where id in ('00000000-0000-4000-8000-000000001810','00000000-0000-4000-8000-000000001812') and not is_correct)<>1 then raise exception 'Wrong-topic count mismatch'; end if;
 begin
  insert into public.practice_answers(id,session_id,learner_key,learner_name,question_id,part,topic,is_correct,graded_at,answer)
   select gen_random_uuid(),session_id,learner_key,learner_name,question_id,part,topic,is_correct,graded_at,answer from public.practice_answers where id='00000000-0000-4000-8000-000000001810';
  raise exception 'Duplicate session/question accepted';
 exception when unique_violation then null; end;
 begin
  insert into public.practice_answers(id,session_id,learner_key,learner_name,question_id,part,topic,is_correct,graded_at,answer)
   values(gen_random_uuid(),gen_random_uuid(),'0000000002','Other', 'Q',1,'T',false,now(),'{"variant":"test","answers":[],"selected":["B"],"correct_ids":["A"],"explanation":"test","legal_basis":[]}');
  raise exception 'Other phone insert accepted';
 exception when insufficient_privilege then null; end;
 if has_table_privilege('anon','public.practice_answers','UPDATE') or has_table_privilege('anon','public.practice_answers','DELETE') then raise exception 'Mutable practice history'; end if;
 if has_column_privilege('anon','public.practice_answers','is_correct','UPDATE') then raise exception 'Can rewrite correctness'; end if;
end $$;
set local request.headers='{"x-client-info":"0000000002"}';
do $$ begin
 if exists(select 1 from public.practice_answers where id='00000000-0000-4000-8000-000000001810') then raise exception 'Cross-phone history visible'; end if;
end $$;
set local request.headers='{}';
do $$ begin
 if exists(select 1 from public.practice_answers) then raise exception 'Unfiltered public enumeration'; end if;
end $$;
rollback;
