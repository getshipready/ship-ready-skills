create table public.notes(id int, user_id uuid, email text);
alter table public.notes enable row level security;
create policy "p" on public.notes for select to anon, authenticated using (true);
