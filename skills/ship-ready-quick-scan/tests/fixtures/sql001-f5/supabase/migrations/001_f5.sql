create or replace function public.run_admin(cmd text) returns void
language plpgsql
as $$
declare stmt text;
begin
  stmt := 'delete from logs where ' || cmd;
  execute stmt;
end;
$$;
