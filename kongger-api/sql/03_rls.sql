-- KONGGER Row Level Security Policies (PostgreSQL 14+ / Supabase compatible)

ALTER TABLE profiles      ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts         ENABLE ROW LEVEL SECURITY;
ALTER TABLE pages         ENABLE ROW LEVEL SECURITY;
ALTER TABLE page_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE neighbours    ENABLE ROW LEVEL SECURITY;
ALTER TABLE likes         ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments      ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE gifts         ENABLE ROW LEVEL SECURITY;
ALTER TABLE visitor_logs  ENABLE ROW LEVEL SECURITY;

-- Helper: resolve current user UUID from JWT claim or PG setting
CREATE OR REPLACE FUNCTION current_user_id() RETURNS UUID LANGUAGE sql STABLE AS $$
  SELECT COALESCE(
    nullif(current_setting('app.current_user_id', true), '')::uuid,
    (SELECT (current_setting('request.jwt.claims', true)::json->>'sub')::uuid)
  );
$$;

-- PROFILES
CREATE POLICY profile_select ON profiles FOR SELECT USING (
  is_private = FALSE OR id = current_user_id()
  OR EXISTS (SELECT 1 FROM neighbours WHERE status='accepted'
    AND ((requester_id=current_user_id() AND addressee_id=profiles.id)
      OR (addressee_id=current_user_id() AND requester_id=profiles.id)))
);
CREATE POLICY profile_insert ON profiles FOR INSERT WITH CHECK (id = current_user_id());
CREATE POLICY profile_update ON profiles FOR UPDATE USING (id = current_user_id());
CREATE POLICY profile_delete ON profiles FOR DELETE USING (id = current_user_id());

-- POSTS
CREATE POLICY post_select ON posts FOR SELECT USING (
  visibility = 'public' OR author_id = current_user_id()
  OR (visibility = 'neighbors' AND EXISTS (
    SELECT 1 FROM neighbours WHERE status='accepted'
      AND ((requester_id=current_user_id() AND addressee_id=posts.author_id)
        OR (addressee_id=current_user_id() AND requester_id=posts.author_id))
  ))
);
CREATE POLICY post_insert ON posts FOR INSERT WITH CHECK (author_id = current_user_id());
CREATE POLICY post_update ON posts FOR UPDATE USING (author_id = current_user_id());
CREATE POLICY post_delete ON posts FOR DELETE USING (author_id = current_user_id());

-- PAGES
CREATE POLICY page_select      ON pages FOR SELECT USING (is_published=TRUE OR owner_id=current_user_id());
CREATE POLICY page_insert      ON pages FOR INSERT WITH CHECK (owner_id = current_user_id());
CREATE POLICY page_update      ON pages FOR UPDATE USING (owner_id = current_user_id());
CREATE POLICY page_delete      ON pages FOR DELETE USING (owner_id = current_user_id());

-- PAGE SECTIONS
CREATE POLICY ps_select ON page_sections FOR SELECT USING (
  EXISTS (SELECT 1 FROM pages WHERE pages.id=page_sections.page_id
    AND (pages.is_published=TRUE OR pages.owner_id=current_user_id()))
);
CREATE POLICY ps_insert ON page_sections FOR INSERT WITH CHECK (
  EXISTS (SELECT 1 FROM pages WHERE pages.id=page_sections.page_id AND pages.owner_id=current_user_id())
);
CREATE POLICY ps_update ON page_sections FOR UPDATE USING (
  EXISTS (SELECT 1 FROM pages WHERE pages.id=page_sections.page_id AND pages.owner_id=current_user_id())
);
CREATE POLICY ps_delete ON page_sections FOR DELETE USING (
  EXISTS (SELECT 1 FROM pages WHERE pages.id=page_sections.page_id AND pages.owner_id=current_user_id())
);

-- NEIGHBOURS
CREATE POLICY nb_select ON neighbours FOR SELECT USING (
  requester_id=current_user_id() OR addressee_id=current_user_id()
);
CREATE POLICY nb_insert ON neighbours FOR INSERT WITH CHECK (requester_id=current_user_id());
CREATE POLICY nb_update ON neighbours FOR UPDATE USING (
  requester_id=current_user_id() OR addressee_id=current_user_id()
);
CREATE POLICY nb_delete ON neighbours FOR DELETE USING (
  requester_id=current_user_id() OR addressee_id=current_user_id()
);

-- LIKES (public read)
CREATE POLICY like_select ON likes FOR SELECT USING (TRUE);
CREATE POLICY like_insert ON likes FOR INSERT WITH CHECK (user_id=current_user_id());
CREATE POLICY like_delete ON likes FOR DELETE USING (user_id=current_user_id());

-- COMMENTS
CREATE POLICY comment_select ON comments FOR SELECT USING (
  EXISTS (SELECT 1 FROM posts WHERE posts.id=comments.post_id
    AND (posts.visibility='public' OR posts.author_id=current_user_id()
      OR (posts.visibility='neighbors' AND EXISTS (
        SELECT 1 FROM neighbours WHERE status='accepted'
          AND ((requester_id=current_user_id() AND addressee_id=posts.author_id)
            OR (addressee_id=current_user_id() AND requester_id=posts.author_id))
      ))))
);
CREATE POLICY comment_insert ON comments FOR INSERT WITH CHECK (author_id=current_user_id());
CREATE POLICY comment_update ON comments FOR UPDATE USING (author_id=current_user_id());

-- NOTIFICATIONS
CREATE POLICY notif_select ON notifications FOR SELECT USING (user_id=current_user_id());
CREATE POLICY notif_update ON notifications FOR UPDATE USING (user_id=current_user_id());

-- GIFTS
CREATE POLICY gift_select ON gifts FOR SELECT USING (
  sender_id=current_user_id() OR receiver_id=current_user_id()
);
CREATE POLICY gift_insert ON gifts FOR INSERT WITH CHECK (sender_id=current_user_id());

-- VISITOR LOGS
CREATE POLICY visit_select ON visitor_logs FOR SELECT USING (
  profile_id IN (SELECT id FROM profiles WHERE id=current_user_id())
);
CREATE POLICY visit_insert ON visitor_logs FOR INSERT WITH CHECK (TRUE);
