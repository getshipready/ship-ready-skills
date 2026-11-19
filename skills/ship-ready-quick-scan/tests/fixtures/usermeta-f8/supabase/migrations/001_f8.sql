create policy "team files" on storage.objects for select to authenticated
  using (bucket_id = 'docs' and (storage.foldername(name))[1] = (auth.jwt() -> 'app_metadata' ->> 'team_id'));
