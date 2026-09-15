-- KONGGER dev seed data
INSERT INTO users (id, email, hashed_password) VALUES
  ('11111111-1111-1111-1111-111111111111','demo@kongger.app','$2a$12$placeholder'),
  ('22222222-2222-2222-2222-222222222222','alice@kongger.app','$2a$12$placeholder')
ON CONFLICT DO NOTHING;

INSERT INTO profiles (id, display_name, handle, bio, theme_colour) VALUES
  ('11111111-1111-1111-1111-111111111111','KONGGER Demo','kongger_demo','Welcome to KONGGER','#4a90d9'),
  ('22222222-2222-2222-2222-222222222222','Alice','alice_k','Digital creator','#e91e8c')
ON CONFLICT DO NOTHING;

INSERT INTO pages (owner_id, slug, title, is_published) VALUES
  ('11111111-1111-1111-1111-111111111111','home','My Room',TRUE),
  ('11111111-1111-1111-1111-111111111111','gallery','Gallery',TRUE),
  ('22222222-2222-2222-2222-222222222222','home','Alice Room',TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO posts (author_id, title, content, mood, visibility) VALUES
  ('11111111-1111-1111-1111-111111111111','Welcome','This is KONGGER — a premium social space.','excited','public'),
  ('22222222-2222-2222-2222-222222222222','Hello KONGGER','Amazing design!','happy','public')
ON CONFLICT DO NOTHING;

INSERT INTO waitlist (email, name) VALUES
  ('beta1@example.com','Beta One'),
  ('beta2@example.com','Beta Two')
ON CONFLICT DO NOTHING;
