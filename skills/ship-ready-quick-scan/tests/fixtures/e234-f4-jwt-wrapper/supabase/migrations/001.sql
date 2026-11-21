create table public.docs (id uuid primary key, body text);
alter table public.docs enable row level security;
create policy "admins" on public.docs for select using (((select auth.jwt()) -> 'user_metadata' ->> 'role') = 'admin');
