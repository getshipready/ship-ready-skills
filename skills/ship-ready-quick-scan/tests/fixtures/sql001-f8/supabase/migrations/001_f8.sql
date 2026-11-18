create function public.exec_sql(query text) returns void language plpgsql security definer as $$
begin execute query; end $$;
revoke execute on function public.exec_sql(text) from anon, authenticated;
