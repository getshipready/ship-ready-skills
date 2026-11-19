alter default privileges in schema public revoke execute on functions from public;
alter default privileges in schema public revoke execute on functions from anon, authenticated;
create or replace function public.dash_push(k text) returns void language plpgsql security definer set search_path = public as $$ begin delete from dash where key = k; end; $$;
