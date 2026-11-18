create table notes (id bigint primary key, user_id uuid, body text);
alter table notes enable row level security;
create policy "own notes" on notes for update to authenticated using (auth.uid() = user_id);
