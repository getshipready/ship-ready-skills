create table public.notes (id int primary key, body text);
alter table public.notes enable row level security;
create policy "own" on public.notes for select using (auth.uid() is not null);
create or replace function public.notify() returns trigger language plpgsql security definer set search_path = '' as $$
begin
  perform net.http_post(
    url := 'https://abc.supabase.co/functions/v1/hook',
    headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name='sb_secret_key')),
    body := '{}'::jsonb);
  return new;
end $$;
