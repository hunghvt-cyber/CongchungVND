-- Random per-history UUID capability; names alone do not grant access. No account required.
create table public.exam_attempts (
 id uuid primary key,
 learner_name text not null check (char_length(btrim(learner_name)) between 1 and 80),
 learner_key text not null check (learner_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'),
 exam_code text not null check (char_length(exam_code) between 1 and 120),
 part smallint not null check (part in (1,2)),
 total integer not null check (total between 1 and 1000),
 correct integer not null check (correct between 0 and total),
 started_at timestamptz not null,
 submitted_at timestamptz not null check (submitted_at >= started_at),
 duration_seconds integer not null check (duration_seconds between 0 and 5400),
 answers jsonb not null check (jsonb_typeof(answers)='array' and jsonb_array_length(answers)=total and octet_length(answers::text)<=2000000),
 created_at timestamptz not null default now()
);
create index exam_attempts_learner_history_idx on public.exam_attempts(learner_key,submitted_at,id);
alter table public.exam_attempts enable row level security;
revoke all on public.exam_attempts from anon,authenticated;
grant select on public.exam_attempts to anon;
grant insert (id,learner_name,learner_key,exam_code,part,total,correct,started_at,submitted_at,duration_seconds,answers) on public.exam_attempts to anon;
-- x-client-info is a CORS-supported header. Prevent unfiltered public enumeration.
-- Only possession of the unguessable history capability permits access.
create policy exam_name_read on public.exam_attempts for select to anon using (learner_key = (select coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info','')));
create policy exam_name_submit on public.exam_attempts for insert to anon with check (learner_key = (select coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info','')));
comment on table public.exam_attempts is 'Lịch sử thi bảo vệ bởi mã UUID ngẫu nhiên trên thiết bị, không tài khoản; kết quả tự luyện, không dùng làm chứng nhận thi.';
