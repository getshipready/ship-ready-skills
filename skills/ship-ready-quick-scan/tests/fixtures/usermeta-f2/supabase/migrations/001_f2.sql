create or replace function public.is_admin() returns boolean language sql security definer set search_path = '' as $$
  select coalesce((select raw_user_meta_data ->> 'role' from auth.users where id = auth.uid()) = 'admin', false);
$$;
