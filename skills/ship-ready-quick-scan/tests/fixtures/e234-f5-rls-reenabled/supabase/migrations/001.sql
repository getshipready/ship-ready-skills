create table public.items (id uuid primary key, owner uuid);
alter table public.items disable row level security;
