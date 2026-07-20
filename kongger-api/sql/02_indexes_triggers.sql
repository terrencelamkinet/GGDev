-- KONGGER Indexes, Triggers, Materialized View

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_profiles_handle    ON profiles (handle);
CREATE INDEX IF NOT EXISTS idx_posts_author       ON posts (author_id);
CREATE INDEX IF NOT EXISTS idx_posts_created      ON posts (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_visibility   ON posts (visibility);
CREATE INDEX IF NOT EXISTS idx_posts_author_vis   ON posts (author_id, visibility);
CREATE INDEX IF NOT EXISTS idx_pages_owner        ON pages (owner_id);
CREATE INDEX IF NOT EXISTS idx_pages_slug         ON pages (owner_id, slug);
CREATE INDEX IF NOT EXISTS idx_page_sections_page ON page_sections (page_id);
CREATE INDEX IF NOT EXISTS idx_neighbours_req     ON neighbours (requester_id, status);
CREATE INDEX IF NOT EXISTS idx_neighbours_addr    ON neighbours (addressee_id, status);
CREATE INDEX IF NOT EXISTS idx_likes_post         ON likes (post_id);
CREATE INDEX IF NOT EXISTS idx_comments_post      ON comments (post_id, created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications (user_id, is_read, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_visitor_profile    ON visitor_logs (profile_id, created_at DESC);

-- TRIGGER: updated_at
CREATE OR REPLACE FUNCTION trg_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;

DO $$
DECLARE t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['users','profiles','posts','pages','page_sections','neighbours','comments'] LOOP
    EXECUTE format(
      'DROP TRIGGER IF EXISTS set_updated_at ON %I;
       CREATE TRIGGER set_updated_at BEFORE UPDATE ON %I
       FOR EACH ROW EXECUTE FUNCTION trg_set_updated_at();', t, t);
  END LOOP;
END; $$;

-- TRIGGER: like_count sync
CREATE OR REPLACE FUNCTION trg_sync_like_count()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE posts SET like_count = like_count + 1 WHERE id = NEW.post_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE posts SET like_count = GREATEST(0, like_count - 1) WHERE id = OLD.post_id;
  END IF;
  RETURN NULL;
END; $$;
DROP TRIGGER IF EXISTS sync_like_count ON likes;
CREATE TRIGGER sync_like_count AFTER INSERT OR DELETE ON likes
FOR EACH ROW EXECUTE FUNCTION trg_sync_like_count();

-- TRIGGER: comment_count sync
CREATE OR REPLACE FUNCTION trg_sync_comment_count()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'INSERT' AND NEW.is_deleted = FALSE THEN
    UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
  ELSIF TG_OP = 'UPDATE' AND NEW.is_deleted = TRUE AND OLD.is_deleted = FALSE THEN
    UPDATE posts SET comment_count = GREATEST(0, comment_count - 1) WHERE id = NEW.post_id;
  END IF;
  RETURN NULL;
END; $$;
DROP TRIGGER IF EXISTS sync_comment_count ON comments;
CREATE TRIGGER sync_comment_count AFTER INSERT OR UPDATE ON comments
FOR EACH ROW EXECUTE FUNCTION trg_sync_comment_count();

-- TRIGGER: Neighbour limit (Dunbar = 30)
CREATE OR REPLACE FUNCTION trg_neighbour_limit()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE cnt INTEGER;
BEGIN
  SELECT COUNT(*) INTO cnt FROM neighbours
  WHERE (requester_id = NEW.requester_id OR addressee_id = NEW.requester_id)
    AND status = 'accepted';
  IF cnt >= 30 THEN RAISE EXCEPTION 'Neighbour limit reached (max 30)'; END IF;
  RETURN NEW;
END; $$;
DROP TRIGGER IF EXISTS neighbour_limit ON neighbours;
CREATE TRIGGER neighbour_limit BEFORE INSERT ON neighbours
FOR EACH ROW EXECUTE FUNCTION trg_neighbour_limit();

-- TRIGGER: visitor counter
CREATE OR REPLACE FUNCTION trg_visitor_count()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  UPDATE profiles SET total_visitors = total_visitors + 1 WHERE id = NEW.profile_id;
  RETURN NULL;
END; $$;
DROP TRIGGER IF EXISTS visitor_count ON visitor_logs;
CREATE TRIGGER visitor_count AFTER INSERT ON visitor_logs
FOR EACH ROW EXECUTE FUNCTION trg_visitor_count();

-- MATERIALIZED VIEW: public feed (refresh every minute via pg_cron)
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_public_feed AS
SELECT p.id, p.author_id, pr.display_name, pr.handle, pr.avatar_url,
       p.title, p.content, p.mood, p.like_count, p.comment_count,
       p.media_urls, p.created_at
FROM posts p
JOIN profiles pr ON pr.id = p.author_id
WHERE p.visibility = 'public'
ORDER BY p.created_at DESC
LIMIT 500;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_public_feed ON mv_public_feed (id);
-- Schedule: SELECT cron.schedule('refresh-feed','* * * * *',
--   'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_public_feed');
