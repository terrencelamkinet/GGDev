-- sql/02_indexes_triggers.sql
-- Indexes
CREATE INDEX IF NOT EXISTS idx_posts_author       ON posts(author_id, created_at DESC) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_posts_public_feed  ON posts(created_at DESC)            WHERE visibility='public' AND is_deleted=FALSE;
CREATE INDEX IF NOT EXISTS idx_posts_visibility   ON posts(visibility, author_id)      WHERE is_deleted=FALSE;
CREATE INDEX IF NOT EXISTS idx_likes_post         ON likes(post_id);
CREATE INDEX IF NOT EXISTS idx_likes_user         ON likes(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_post      ON comments(post_id, created_at)     WHERE is_deleted=FALSE;
CREATE INDEX IF NOT EXISTS idx_neighbours_from    ON neighbours(from_user, status);
CREATE INDEX IF NOT EXISTS idx_neighbours_to      ON neighbours(to_user, status);
CREATE INDEX IF NOT EXISTS idx_visitor_logs_date  ON visitor_logs(profile_id, visited_at DESC);
CREATE INDEX IF NOT EXISTS idx_notif_user_unread  ON notifications(user_id, is_read, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_profiles_handle    ON profiles(handle);
CREATE INDEX IF NOT EXISTS idx_pages_owner_slug   ON pages(owner_id, slug) WHERE is_published=TRUE;
CREATE INDEX IF NOT EXISTS idx_gifts_to_user      ON gifts(to_user, created_at DESC);

-- auto updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;

DO $$ DECLARE t TEXT;
BEGIN FOR t IN SELECT unnest(ARRAY['users','profiles','posts','pages','page_sections','neighbours','comments'])
  LOOP EXECUTE format('DROP TRIGGER IF EXISTS trg_updated_at ON %I;
    CREATE TRIGGER trg_updated_at BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION set_updated_at();',t,t);
  END LOOP; END; $$;

-- Auto-sync like_count
CREATE OR REPLACE FUNCTION sync_like_count() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP='INSERT' THEN UPDATE posts SET like_count=like_count+1 WHERE id=NEW.post_id;
  ELSIF TG_OP='DELETE' THEN UPDATE posts SET like_count=GREATEST(like_count-1,0) WHERE id=OLD.post_id; END IF;
  RETURN NULL; END; $$;
DROP TRIGGER IF EXISTS trg_like_count ON likes;
CREATE TRIGGER trg_like_count AFTER INSERT OR DELETE ON likes FOR EACH ROW EXECUTE FUNCTION sync_like_count();

-- Auto-sync comment_count
CREATE OR REPLACE FUNCTION sync_comment_count() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP='INSERT' THEN UPDATE posts SET comment_count=comment_count+1 WHERE id=NEW.post_id;
  ELSIF TG_OP='UPDATE' AND NEW.is_deleted AND NOT OLD.is_deleted THEN UPDATE posts SET comment_count=GREATEST(comment_count-1,0) WHERE id=OLD.post_id; END IF;
  RETURN NULL; END; $$;
DROP TRIGGER IF EXISTS trg_comment_count ON comments;
CREATE TRIGGER trg_comment_count AFTER INSERT OR UPDATE ON comments FOR EACH ROW EXECUTE FUNCTION sync_comment_count();

-- Auto-increment total_visitors
CREATE OR REPLACE FUNCTION sync_visitor_count() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN UPDATE profiles SET total_visitors=total_visitors+1 WHERE id=NEW.profile_id; RETURN NULL; END; $$;
DROP TRIGGER IF EXISTS trg_visitor_count ON visitor_logs;
CREATE TRIGGER trg_visitor_count AFTER INSERT ON visitor_logs FOR EACH ROW EXECUTE FUNCTION sync_visitor_count();

-- Dunbar rule: max 30 accepted neighbours per user
CREATE OR REPLACE FUNCTION enforce_dunbar() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.status='accepted' THEN
    IF (SELECT COUNT(*) FROM neighbours WHERE from_user=NEW.from_user AND status='accepted')>=30 THEN
      RAISE EXCEPTION 'Maximum 30 neighbours (Dunbar rule)'; END IF; END IF;
  RETURN NEW; END; $$;
DROP TRIGGER IF EXISTS trg_dunbar ON neighbours;
CREATE TRIGGER trg_dunbar BEFORE UPDATE ON neighbours FOR EACH ROW EXECUTE FUNCTION enforce_dunbar();
