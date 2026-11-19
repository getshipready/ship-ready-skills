create policy tenant_rw on public.docs for all using (tenant_id::text = current_setting('request.jwt.claims', true)::json -> 'user_metadata' ->> 'tenant_id');
