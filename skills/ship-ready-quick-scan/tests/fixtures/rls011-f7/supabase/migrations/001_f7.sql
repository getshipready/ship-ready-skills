create function public.get_stats() returns int language sql security definer as $$ select count(*)::int from profiles $$;
