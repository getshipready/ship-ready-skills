create function public.exec_sql(sql text) returns void language plpgsql security definer as $$ begin execute sql; end; $$;
