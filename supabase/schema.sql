-- Anonymous clients can submit suggestions only. Review in Supabase Dashboard.
create table public.question_feedback (
  id uuid primary key,
  question_id text not null check (question_id ~ '^[A-Za-z0-9-]{1,80}$'),
  category text not null check (category in ('law_expired','law_changed','answer_wrong','explanation_wrong','unclear','missing_basis','suggest_new_law','other')),
  content text not null check (char_length(btrim(content)) between 1 and 3000),
  exam_code text not null default '' check (char_length(exam_code) <= 120),
  mode text not null check (mode in ('practice','mock')),
  variant text not null check (char_length(variant) between 1 and 5000),
  answer_order jsonb not null check (jsonb_typeof(answer_order) = 'array' and jsonb_array_length(answer_order) between 1 and 10),
  question_snapshot jsonb not null check (jsonb_typeof(question_snapshot) = 'object' and octet_length(question_snapshot::text) <= 30000),
  client_created_at timestamptz not null,
  created_at timestamptz not null default now(),
  review_status text not null default 'pending' check (review_status in ('pending','reviewed','resolved','dismissed'))
);
create index question_feedback_question_id_idx on public.question_feedback(question_id);
create index question_feedback_created_at_idx on public.question_feedback(created_at desc);
alter table public.question_feedback enable row level security;
revoke all on public.question_feedback from anon, authenticated;
grant insert (id, question_id, category, content, exam_code, mode, variant, answer_order, question_snapshot, client_created_at) on public.question_feedback to anon;
create policy feedback_submit_only on public.question_feedback for insert to anon with check (review_status = 'pending');
comment on table public.question_feedback is 'Góp ý câu hỏi/đáp án tập trung; không tự cập nhật ngân hàng. Chỉ chủ dự án rà soát trong Dashboard.';
