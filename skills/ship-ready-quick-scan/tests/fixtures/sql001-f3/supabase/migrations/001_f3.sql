create function public.count_rows(tbl text) returns bigint language plpgsql as $$
declare n bigint;
begin execute format('select count(*) from %I', tbl) into n; return n; end $$;
