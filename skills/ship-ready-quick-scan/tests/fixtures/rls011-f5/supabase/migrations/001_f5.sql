create function public.on_signup() returns trigger language plpgsql security definer as $$ begin insert into profiles(id) values (new.id); return new; end; $$;
