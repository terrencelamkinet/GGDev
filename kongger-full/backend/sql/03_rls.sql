-- sql/03_rls.sql  Row Level Security
-- Enable RLS on sensitive tables
ALTER TABLE posts           ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles        ENABLE ROW LEVEL SECURITY;
ALTER TABLE pages           ENABLE ROW LEVEL SECURITY;
ALTER TABLE visitor_logs    ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications   ENABLE ROW LEVEL SECURITY;
ALTER TABLE gifts           ENABLE ROW LEVEL SECURITY;

-- POSTS: public visible to all; neighbors-only visible to accepted neighbours; private only owner
CREATE POLICY posts_read ON posts FOR SELECT USING (
  is_deleted = FALSE AND (
    visibility='public'
    OR author_id = current_setting('app.user_id', TRUE)::UUID
    OR (visibility='neighbors' AND EXISTS (
      SELECT 1 FROM neighbours n WHERE
        ((n.from_user=current_setting('app.user_id',TRUE)::UUID AND n.to_user=posts.author_id)
        OR (n.to_user=current_setting('app.user_id',TRUE)::UUID AND n.from_user=posts.author_id))
        AND n.status='accepted'))
  )
);
CREATE POLICY posts_write ON posts FOR ALL USING (
  author_id = current_setting('app.user_id', TRUE)::UUID
);

-- PROFILES: public profiles visible to all; private only owner + accepted neighbours
CREATE POLICY profiles_read ON profiles FOR SELECT USING (
  is_private = FALSE
  OR id = current_setting('app.user_id', TRUE)::UUID
  OR EXISTS (
    SELECT 1 FROM neighbours n WHERE
      ((n.from_user=current_setting('app.user_id',TRUE)::UUID AND n.to_user=profiles.id)
      OR (n.to_user=current_setting('app.user_id',TRUE)::UUID AND n.from_user=profiles.id))
      AND n.status='accepted')
);
CREATE POLICY profiles_write ON profiles FOR ALL USING (
  id = current_setting('app.user_id', TRUE)::UUID
);

-- PAGES: published pages visible to all; unpublished only owner
CREATE POLICY pages_read ON pages FOR SELECT USING (
  is_published = TRUE
  OR owner_id = current_setting('app.user_id', TRUE)::UUID
);
CREATE POLICY pages_write ON pages FOR ALL USING (
  owner_id = current_setting('app.user_id', TRUE)::UUID
);

-- NOTIFICATIONS: only the owner
CREATE POLICY notif_rw ON notifications FOR ALL USING (
  user_id = current_setting('app.user_id', TRUE)::UUID
);

-- VISITOR_LOGS: only the profile owner can read their visitors
CREATE POLICY visitor_read ON visitor_logs FOR SELECT USING (
  profile_id = current_setting('app.user_id', TRUE)::UUID
);
CREATE POLICY visitor_insert ON visitor_logs FOR INSERT WITH CHECK (TRUE);

-- GIFTS
CREATE POLICY gifts_read ON gifts FOR SELECT USING (
  to_user = current_setting('app.user_id', TRUE)::UUID
  OR from_user = current_setting('app.user_id', TRUE)::UUID
);
CREATE POLICY gifts_write ON gifts FOR INSERT WITH CHECK (
  from_user = current_setting('app.user_id', TRUE)::UUID
);
