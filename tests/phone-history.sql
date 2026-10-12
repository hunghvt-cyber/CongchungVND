begin;
-- Set up three legacy attempts and keep their IDs/scores exactly as originally saved.
do $$ declare k text := gen_random_uuid()::text; j integer;
begin
 perform set_config('test.phone_legacy_key',k,true);
 for j in 1..3 loop
  insert into public.exam_attempts (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers)
  values (gen_random_uuid(),'PhoneHistoryQA',k,'QA-PHONE',1,1,case when j=3 then 0 else 1 end,now(),now(),0,'[{}]');
 end loop;
end $$;
set local role anon;
select set_config('request.headers',jsonb_build_object('x-client-info',current_setting('test.phone_legacy_key')||':0000000001')::text,true);
update public.exam_attempts set learner_key='0000000001' where learner_key=current_setting('test.phone_legacy_key');
select set_config('request.headers','{"x-client-info":"0000000001"}',true);
do $$
begin
 if (select count(*) from public.exam_attempts where exam_code='QA-PHONE')<>3 then raise exception 'Legacy history was not linked'; end if;
 if (select sum(correct) from public.exam_attempts where exam_code='QA-PHONE')<>2 then raise exception 'Scores changed during linking'; end if;
 if (select count(*) from public.exam_leaderboard where learner_name='PhoneHistoryQA')<>1 then raise exception 'Duplicate leaderboard profiles after merge'; end if;
 if not exists (select 1 from public.exam_leaderboard where learner_name='PhoneHistoryQA' and attempt_count=3 and abs(average_score-20.0/3)<0.00001) then raise exception 'Merged ranking incorrect'; end if;
 if has_column_privilege('anon','public.exam_attempts','correct','UPDATE') then raise exception 'Linking must not grant score edits'; end if;
 -- Any browser may read and append using the same phone, without a login.
 insert into public.exam_attempts (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers)
 values (gen_random_uuid(),'PhoneHistoryQA','0000000001','QA-PHONE',1,1,1,now(),now(),0,'[{}]');
 if (select count(*) from public.exam_attempts where exam_code='QA-PHONE')<>4 then raise exception 'Phone append failed'; end if;
 if not exists (select 1 from public.exam_leaderboard where learner_name='PhoneHistoryQA' and attempt_count=4 and average_score=7.5) then raise exception 'Phone ranking update failed'; end if;
end $$;
select set_config('request.headers','{"x-client-info":"0000000002"}',true);
do $$ begin
 if exists(select 1 from public.exam_attempts where exam_code='QA-PHONE')then raise exception 'Different phones must keep separate histories';end if;
end $$;
reset role;
select 'PASS: legacy merge, preserved scores, single leaderboard profile, phone read/append without auth, separate phones, no score edits' as verification;
rollback;
