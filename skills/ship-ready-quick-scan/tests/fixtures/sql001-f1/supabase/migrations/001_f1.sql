create or replace function public.exec_sql(query text) returns json
language plpgsql security definer as $$
declare r json;
begin
  execute 'select json_agg(t) from (' || query || ') t' into r;
  return r;
end $$;
