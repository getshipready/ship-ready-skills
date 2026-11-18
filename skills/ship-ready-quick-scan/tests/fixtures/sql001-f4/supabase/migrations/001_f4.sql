create function public.get_by_status(s text) returns setof orders language plpgsql as $fn$
begin return query execute 'select * from orders where status = $1' using s; end $fn$;
