create table public.notes(id uuid primary key, user_id uuid);
grant select, insert on public.notes to authenticated;
alter table public.notes enable row level security;
