-- Phone numbers identify self-practice histories without authentication, by user choice.
-- UUID histories remain compatible and can be linked only with their original code.
alter table public.exam_attempts drop constraint exam_attempts_learner_key_check;
alter table public.exam_attempts add constraint exam_attempts_learner_key_check check (
 learner_key ~ '^0[0-9]{9,10}$' or
 learner_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
);
drop policy exam_name_read on public.exam_attempts;
create policy exam_name_read on public.exam_attempts for select to anon using (
 learner_key = (select split_part(coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''), ':', 1))
 or (
  (select coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info','')) ~ '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}:0[0-9]{9,10}$'
  and learner_key = (select split_part(coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''), ':', 2))
 )
);
grant update (learner_key) on public.exam_attempts to anon;
create policy exam_link_legacy_phone on public.exam_attempts for update to anon using (
 learner_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
 and learner_key = (select split_part(coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''), ':', 1))
) with check (
 learner_key ~ '^0[0-9]{9,10}$'
 and learner_key = (select split_part(coalesce(current_setting('request.headers',true)::jsonb->>'x-client-info',''), ':', 2))
);
comment on table public.exam_attempts is 'Self-practice histories identified by phone without authentication. Anyone knowing the number can read/add results. Legacy UUID records may be linked with their old code. No unfiltered enumeration.';
notify pgrst, 'reload schema';
