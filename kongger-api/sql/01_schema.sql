-- KONGGER PostgreSQL Schema v1.0
-- Compatible with Supabase / PgBouncer / direct PostgreSQL 16+

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- USERS
CREATE TABLE IF NOT EXISTS users (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email           TEXT UNIQUE NOT NULL,
  hashed_password TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- PROFILES
CREATE TABLE IF NOT EXISTS profiles (
  id              UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  display_name    TEXT NOT NULL,
  handle          TEXT UNIQUE NOT NULL,
  bio             TEXT,
  avatar_url      TEXT,
  cover_url       TEXT,
  music_url       TEXT,
  music_title     TEXT,
  music_artist    TEXT,
  ad_title        TEXT,
  ad_description  TEXT,
  ad_link_url     TEXT,
  theme_colour    TEXT DEFAULT '#4a90d9',
  is_private      BOOLEAN DEFAULT FALSE,
  total_visitors  INTEGER DEFAULT 0,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- POST TYPES
DO $$ BEGIN
  CREATE TYPE post_visibility AS ENUM ('public', 'neighbors', 'private');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
  CREATE TYPE post_mood AS ENUM (
    'happy','calm','moved','thinking','nostalgic','everyday',
    'excited','sad','grateful','anxious'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- POSTS
CREATE TABLE IF NOT EXISTS posts (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  author_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title           TEXT,
  content         TEXT NOT NULL,
  mood            post_mood DEFAULT 'everyday',
  visibility      post_visibility DEFAULT 'neighbors',
  media_urls      TEXT[],
  like_count      INTEGER DEFAULT 0,
  comment_count   INTEGER DEFAULT 0,
  is_pinned       BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- PAGE SECTION TYPES
DO $$ BEGIN
  CREATE TYPE page_section_type AS ENUM (
    'text', 'image_gallery', 'video', 'music_widget',
    'social_feed', 'ad_board', 'custom_html'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- PAGES
CREATE TABLE IF NOT EXISTS pages (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  slug            TEXT NOT NULL,
  title           TEXT NOT NULL,
  description     TEXT,
  background_url  TEXT,
  background_colour TEXT,
  layout_json     JSONB,
  is_published    BOOLEAN DEFAULT TRUE,
  sort_order      INTEGER DEFAULT 0,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (owner_id, slug)
);

-- PAGE SECTIONS
CREATE TABLE IF NOT EXISTS page_sections (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  page_id         UUID NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
  section_type    page_section_type DEFAULT 'text',
  title           TEXT,
  content_json    JSONB NOT NULL DEFAULT '{}',
  position_x      FLOAT DEFAULT 0,
  position_y      FLOAT DEFAULT 0,
  width           FLOAT DEFAULT 1,
  height          FLOAT DEFAULT 1,
  z_index         INTEGER DEFAULT 0,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- NEIGHBOURS
DO $$ BEGIN
  CREATE TYPE neighbour_status AS ENUM ('pending', 'accepted', 'blocked');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS neighbours (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  requester_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  addressee_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status          neighbour_status DEFAULT 'pending',
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (requester_id, addressee_id),
  CHECK (requester_id <> addressee_id)
);

-- LIKES
CREATE TABLE IF NOT EXISTS likes (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (user_id, post_id)
);

-- COMMENTS
CREATE TABLE IF NOT EXISTS comments (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  author_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  parent_id       UUID REFERENCES comments(id) ON DELETE CASCADE,
  content         TEXT NOT NULL,
  is_deleted      BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- VISITOR LOGS
CREATE TABLE IF NOT EXISTS visitor_logs (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  visitor_id      UUID REFERENCES users(id) ON DELETE SET NULL,
  ip_hash         TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- GIFTS
CREATE TABLE IF NOT EXISTS gifts (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  sender_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  receiver_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  gift_type       TEXT NOT NULL,
  message         TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- NOTIFICATIONS
DO $$ BEGIN
  CREATE TYPE notification_type AS ENUM (
    'new_neighbour','neighbour_accepted','new_like','new_comment',
    'new_visitor','new_gift','mention'
  );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
CREATE TABLE IF NOT EXISTS notifications (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  actor_id          UUID REFERENCES users(id) ON DELETE SET NULL,
  notification_type notification_type NOT NULL,
  entity_id         UUID,
  is_read           BOOLEAN DEFAULT FALSE,
  created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- WAITLIST
CREATE TABLE IF NOT EXISTS waitlist (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email       TEXT UNIQUE NOT NULL,
  name        TEXT,
  message     TEXT,
  invite_code TEXT UNIQUE DEFAULT encode(gen_random_bytes(6), 'hex'),
  is_invited  BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
