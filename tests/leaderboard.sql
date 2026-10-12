-- Execute in one session. All fixtures are rolled back.
begin;
do $$
declare k text; n integer; j integer; total_questions integer; correct_questions integer;
begin
 for n in 1..3 loop
  k := gen_random_uuid()::text;
  for j in 1..case when n = 3 then 2 else 3 end loop
   total_questions := case j when 1 then 2 when 2 then 4 else 10 end;
   correct_questions := case when n = 2 then total_questions else case j when 1 then 2 when 2 then 2 else 0 end end;
   insert into public.exam_attempts (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers)
   values (gen_random_uuid(), 'LeaderboardQA-duplicate-name', k, 'QA', 1, total_questions, correct_questions,
   now(), now(), 0, (select jsonb_agg('{}'::jsonb) from generate_series(1,total_questions)));
  end loop;
 end loop;
end $$;
set local role anon;
select set_config('request.headers','{}',true);
do $$
begin
 if (select count(*) from public.exam_leaderboard where learner_name='LeaderboardQA-duplicate-name') <> 2 then
  raise exception 'Minimum attempts / separate histories failed';
 end if;
 if not exists (select 1 from public.exam_leaderboard where learner_name='LeaderboardQA-duplicate-name' and average_score=5 and attempt_count=3) then
  raise exception 'Mean must be per-exam (10 + 5 + 0) / 3 = 5';
 end if;
 if (select count(*) from public.exam_attempts) <> 0 then raise exception 'Private histories exposed'; end if;
 if has_table_privilege('anon','public.exam_leaderboard','INSERT') or has_table_privilege('anon','public.exam_leaderboard','UPDATE') or has_table_privilege('anon','public.exam_leaderboard','DELETE') then
  raise exception 'Public aggregates must be read only';
 end if;
 if has_schema_privilege('anon','private','USAGE') then raise exception 'Private mappings accessible'; end if;
end $$;
-- Check real anonymous submission still passes original history-capability RLS.
do $$
declare k text := gen_random_uuid()::text; j integer; receipt uuid;
begin
 perform set_config('request.headers',jsonb_build_object('x-client-info',k)::text,true);
 for j in 1..3 loop
  receipt := gen_random_uuid();
  insert into public.exam_attempts (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers)
  values (receipt,'LeaderboardQA-anon',k,'QA',1,1,1,now(),now(),0,'[{}]');
  begin
   insert into public.exam_attempts (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers)
   values (receipt,'LeaderboardQA-anon',k,'QA',1,1,1,now(),now(),0,'[{}]');
   raise exception 'Duplicate receipt unexpectedly inserted';
  exception when unique_violation then null;
  end;
 end loop;
 if not exists (select 1 from public.exam_leaderboard where learner_name='LeaderboardQA-anon' and attempt_count=3 and average_score=10) then
  raise exception 'Anon trigger / deduplication failed';
 end if;
end $$;
reset role;
select 'PASS: per-exam mean, 3-attempt threshold, separate histories, private data, public read-only, anon submission and duplicate receipt' as verification;
rollback;
