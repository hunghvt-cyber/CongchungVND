-- Public aggregates only. History capabilities and answer snapshots remain private.
create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create table private.exam_leaderboard_profiles (
 learner_key text primary key,
 public_id uuid not null unique default gen_random_uuid()
);
alter table private.exam_leaderboard_profiles enable row level security;
revoke all on private.exam_leaderboard_profiles from public, anon, authenticated;

create table public.exam_leaderboard (
 id uuid primary key,
 learner_name text not null,
 attempt_count integer not null check (attempt_count > 0),
 average_score numeric not null check (average_score between 0 and 10),
 best_score numeric not null check (best_score between 0 and 10)
);
alter table public.exam_leaderboard enable row level security;
revoke all on public.exam_leaderboard from public, anon, authenticated;
grant select on public.exam_leaderboard to anon, authenticated;
create policy leaderboard_public_read on public.exam_leaderboard
 for select to anon, authenticated using (attempt_count >= 3);
create index exam_leaderboard_order_idx on public.exam_leaderboard
 (average_score desc, attempt_count desc, id asc) where attempt_count >= 3;

-- Called only by the database trigger and administrative backfill, never by the API.
-- Definer is necessary to aggregate histories while keeping exam_attempts RLS intact.
create function private.refresh_exam_leaderboard(history_key text) returns void
 language plpgsql security definer set search_path = '' as $$
declare profile_id uuid; exams integer; avg_score numeric; max_score numeric; display_name text;
begin
 -- Lock one profile to serialize concurrent submissions for the same history.
 insert into private.exam_leaderboard_profiles as p (learner_key) values (history_key)
 on conflict (learner_key) do update set learner_key = excluded.learner_key
 returning p.public_id into profile_id;
 select count(*)::integer, avg(10.0 * a.correct / a.total), max(10.0 * a.correct / a.total)
 into exams, avg_score, max_score from public.exam_attempts a where a.learner_key = history_key;
 if exams = 0 then
  delete from public.exam_leaderboard where id = profile_id;
  delete from private.exam_leaderboard_profiles where learner_key = history_key;
  return;
 end if;
 select a.learner_name into display_name from public.exam_attempts a
 where a.learner_key = history_key order by a.submitted_at desc, a.id desc limit 1;
 insert into public.exam_leaderboard (id, learner_name, attempt_count, average_score, best_score)
 values (profile_id, display_name, exams, avg_score, max_score)
 on conflict (id) do update set learner_name = excluded.learner_name,
 attempt_count = excluded.attempt_count, average_score = excluded.average_score, best_score = excluded.best_score;
end;
$$;
revoke all on function private.refresh_exam_leaderboard(text) from public, anon, authenticated;

create function private.on_exam_attempt_leaderboard() returns trigger
 language plpgsql security definer set search_path = '' as $$
begin
 if tg_op = 'DELETE' then
  perform private.refresh_exam_leaderboard(old.learner_key);
 else
  if tg_op = 'UPDATE' and old.learner_key is distinct from new.learner_key then
   perform private.refresh_exam_leaderboard(old.learner_key);
  end if;
  perform private.refresh_exam_leaderboard(new.learner_key);
 end if;
 return null;
end;
$$;
revoke all on function private.on_exam_attempt_leaderboard() from public, anon, authenticated;
create trigger exam_attempt_leaderboard_sync after insert or update or delete on public.exam_attempts
 for each row execute function private.on_exam_attempt_leaderboard();

do $$ declare history_key text; begin
 for history_key in select distinct learner_key from public.exam_attempts loop
  perform private.refresh_exam_leaderboard(history_key);
 end loop;
end $$;
comment on table public.exam_leaderboard is 'Public self-practice ranking: arithmetic mean of submitted exam scores on scale 10, minimum 3 attempts. No history keys or answers.';
notify pgrst, 'reload schema';
