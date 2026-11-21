create or replace function public.give_credits(uid uuid, n int) returns void language plpgsql security definer set search_path = '' as $$
begin update public.profiles set credits = credits + n where id = uid; end $$;
revoke execute on function public.give_credits(uuid,int) from anon;
