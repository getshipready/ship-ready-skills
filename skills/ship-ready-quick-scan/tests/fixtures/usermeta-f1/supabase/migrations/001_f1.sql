create policy "admins read all" on public.orders for select using ((auth.jwt() -> 'user_metadata' ->> 'role') = 'admin');
