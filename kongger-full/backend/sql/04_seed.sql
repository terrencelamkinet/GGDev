-- sql/04_seed.sql  Development seed data
-- Run AFTER schema + triggers (for development only)
DO $$ BEGIN

INSERT INTO users(id, email, password_hash) VALUES
  ('11111111-1111-1111-1111-111111111111','demo@kongger.hk','$2b$12$PLACEHOLDER_HASH')
ON CONFLICT DO NOTHING;

INSERT INTO profiles(id, handle, display_name, bio, is_private) VALUES
  ('11111111-1111-1111-1111-111111111111','kongger_demo','KONGGER Demo','歡迎來到 KONGGER！',FALSE)
ON CONFLICT DO NOTHING;

INSERT INTO waitlist(email, name) VALUES
  ('test@example.com','Test User')
ON CONFLICT DO NOTHING;

END $$;
