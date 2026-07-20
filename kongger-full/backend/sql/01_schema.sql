-- sql/01_schema.sql  KONGGER PostgreSQL Schema
-- Run: psql -U kongger_user -d kongger_db -f sql/01_schema.sql

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS profiles (
  id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  handle         TEXT UNIQUE NOT NULL CHECK (handle ~ '^[a-z0-9_]{3,30}$'),
  display_name   TEXT NOT NULL,
  bio            TEXT,
  avatar_url     TEXT,
  cover_url      TEXT,
  music_url      TEXT,
  music_title    TEXT,
  music_artist   TEXT,
  ad_title       TEXT,
  ad_description TEXT,
  ad_link_url    TEXT,
  is_private     BOOLEAN NOT NULL DEFAULT FALSE,
  total_visitors INTEGER NOT NULL DEFAULT 0,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS posts (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title        TEXT,
  content      TEXT NOT NULL CHECK (char_length(content) BETWEEN 1 AND 500),
  mood         TEXT NOT NULL DEFAULT 'everyday'
                 CHECK (mood IN ('happy','calm','moved','thinking','nostalgic','everyday','excited','sad','grateful','anxious')),
  visibility   TEXT NOT NULL DEFAULT 'neighbors'
                 CHECK (visibility IN ('public','neighbors','private')),
  media_urls   TEXT[] NOT NULL DEFAULT '{}',
  like_count   INTEGER NOT NULL DEFAULT 0,
  comment_count INTEGER NOT NULL DEFAULT 0,
  is_deleted   BOOLEAN NOT NULL DEFAULT FALSE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pages (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  slug          TEXT NOT NULL,
  title         TEXT NOT NULL DEFAULT 'My Page',
  layout_json   JSONB NOT NULL DEFAULT '{"cols":12,"rows":[]}'::jsonb,
  theme_json    JSONB NOT NULL DEFAULT '{}'::jsonb,
  is_published  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (owner_id, slug)
);

CREATE TABLE IF NOT EXISTS page_sections (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page_id     UUID NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
  section_key TEXT NOT NULL,
  type        TEXT NOT NULL,
  content     JSONB NOT NULL DEFAULT '{}'::jsonb,
  grid_pos    JSONB NOT NULL DEFAULT '{"x":0,"y":0,"w":6,"h":4}'::jsonb,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (page_id, section_key)
);

CREATE TABLE IF NOT EXISTS neighbours (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_user  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  to_user    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status     TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','accepted','blocked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (from_user, to_user),
  CHECK (from_user <> to_user)
);

CREATE TABLE IF NOT EXISTS likes (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  post_id    UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, post_id)
);

CREATE TABLE IF NOT EXISTS comments (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id    UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  author_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content    TEXT NOT NULL CHECK (char_length(content) BETWEEN 1 AND 300),
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS visitor_logs (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id   UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  visitor_id   UUID REFERENCES users(id) ON DELETE SET NULL,
  visitor_ip   INET,
  visited_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gifts (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  from_user  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  to_user    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  gift_type  TEXT NOT NULL,
  message    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notifications (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type        TEXT NOT NULL CHECK (type IN ('like','comment','neighbour_request','neighbour_accept','visit','gift')),
  actor_id    UUID REFERENCES users(id) ON DELETE SET NULL,
  ref_post_id UUID REFERENCES posts(id) ON DELETE SET NULL,
  is_read     BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS waitlist (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT UNIQUE NOT NULL,
  name       TEXT,
  message    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
