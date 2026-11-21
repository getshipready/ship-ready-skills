alter table public.items enable row level security;
create policy "own" on public.items for select using (auth.uid() = owner);
