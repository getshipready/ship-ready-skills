create function private.exec_sql(query text) returns void language plpgsql security definer as $$ begin execute query; end $$;
create function public.hello(name text) returns text language sql as $$ select 'hi ' || name $$;
