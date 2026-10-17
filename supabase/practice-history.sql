-- Separate from exam_attempts: practice never changes the exam leaderboard.
create table public.practice_answers (
 id uuid primary key,
 session_id uuid not null,
 learner_key text not null check (learner_key ~ '^0[0-9]{9,10}$'),
 learner_name text not null check (char_length(btrim(learner_name)) between 1 and 80),
 question_id text not null check (char_length(question_id) between 1 and 100),
 part smallint not null check (part in (1,2)),
 topic text not null check (char_length(topic) between 1 and 300),
 is_correct boolean not null,
 graded_at timestamptz not null,
 answer jsonb not null check (jsonb_typeof(answer)='object' and octet_length(answer::text)<=100000
   and answer ?& array['variant','answers','selected','correct_ids','explanation','legal_basis']
   and jsonb_typeof(answer->'selected')='array' and jsonb_typeof(answer->'correct_ids')='array'
   and jsonb_typeof(answer->'answers')='array' and jsonb_array_length(answer->'selected') between 1 and 4),
 created_at timestamptz not null default now(),
 unique(session_id,question_id)
);
create index practice_answers_learner_history_idx on public.practice_answers(learner_key,graded_at,id);
alter table public.practice_answers enable row level security;
revoke all on public.practice_answers from public,anon,authenticated;
grant select on public.practice_answers to anon;
grant insert (id,session_id,learner_key,learner_name,question_id,part,topic,is_correct,graded_at,answer) on public.practice_answers to anon;
create policy practice_phone_read on public.practice_answers for select to anon using (
 learner_key = (select coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''))
);
create policy practice_phone_submit on public.practice_answers for insert to anon with check (
 learner_key = (select coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''))
);
comment on table public.practice_answers is 'Self-practice graded answers, isolated from exam scores and leaderboard. No authentication by owner choice: anyone knowing a phone can read/add its practice history. No public enumeration, update or delete.';
notify pgrst, 'reload schema';
