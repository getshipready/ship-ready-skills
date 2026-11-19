create function public.mine() returns void language plpgsql security invoker as $$ begin delete from notes where uid = auth.uid(); end; $$;
