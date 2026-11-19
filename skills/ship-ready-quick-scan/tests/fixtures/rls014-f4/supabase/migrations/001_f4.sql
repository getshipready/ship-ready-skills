alter default privileges for role postgres in schema public revoke select, insert, update, delete on tables from anon, authenticated, service_role;
