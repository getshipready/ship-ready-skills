create or replace function public.dash_push(k text) returns void language plpgsql security definer set search_path = public as $$ begin delete from dash where key = k; end; $$;
revoke execute on function public.dash_push(text) from public, anon;
