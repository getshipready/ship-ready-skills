create function public.exec_sql(query text) returns void language plpgsql security definer as $$
begin execute query; end $$;
revoke all on function public.exec_sql(text) from public, anon, authenticated;
