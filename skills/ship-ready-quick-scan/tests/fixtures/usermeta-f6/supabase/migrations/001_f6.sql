create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, role) values (new.id, new.raw_user_meta_data ->> 'role');
  return new;
end;
$$;
