create policy "admins read all" on public.orders for select using ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
