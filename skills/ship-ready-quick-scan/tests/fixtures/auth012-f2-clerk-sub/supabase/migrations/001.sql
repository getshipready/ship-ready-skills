create table notes (id bigint primary key, user_id text, body text);
alter table notes enable row level security;
create policy "own notes" on notes for select to authenticated using (user_id = (select auth.jwt()->>'sub'));
