/**
 * server.js — KONGGER API Server
 * Node.js 20 + Express + pg (PostgreSQL)
 * Endpoints: /api/v1/*
 */
import express from 'express';
import pg from 'pg';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { readFileSync } from 'fs';
import 'dotenv/config';

const { Pool } = pg;
const app = express();
const PORT = process.env.PORT ?? 3001;
const JWT_SECRET = process.env.JWT_SECRET ?? 'dev_secret_change_in_prod';
const BCRYPT_ROUNDS = parseInt(process.env.BCRYPT_ROUNDS ?? '12');
const pool = new Pool({ connectionString: process.env.PG_CONNECTION_STRING });

app.use(cors({ origin: process.env.FRONTEND_ORIGIN ?? '*', credentials: true }));
app.use(express.json({ limit: '2mb' }));
app.use(rateLimit({ windowMs: 60000, max: 120, standardHeaders: true }));

// ── Auth middleware ────────────────────────────────────────────
function auth(req, res, next) {
  const h = req.headers.authorization;
  if (!h?.startsWith('Bearer ')) return res.status(401).json({ error: 'Unauthorized' });
  try { req.user = jwt.verify(h.slice(7), JWT_SECRET); next(); }
  catch { res.status(401).json({ error: 'Invalid token' }); }
}

// Set app.user_id for RLS
async function withRLS(client, userId) {
  await client.query(`SET LOCAL app.user_id = '${userId}'`);
}

// ── Health ─────────────────────────────────────────────────────
app.get('/health', async (_, res) => {
  try { await pool.query('SELECT 1'); res.json({ status: 'ok', ts: new Date().toISOString() }); }
  catch { res.status(500).json({ status: 'db_error' }); }
});

// ── Auth ───────────────────────────────────────────────────────
app.post('/api/v1/auth/register', async (req, res) => {
  const { email, password, display_name, handle } = req.body ?? {};
  if (!email || !password || !display_name || !handle)
    return res.status(400).json({ error: 'Missing required fields' });
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);
    const { rows: [u] } = await client.query(
      `INSERT INTO users(email,password_hash) VALUES($1,$2) RETURNING id`, [email.toLowerCase(), hash]);
    await client.query(
      `INSERT INTO profiles(id,handle,display_name) VALUES($1,$2,$3)`, [u.id, handle.toLowerCase(), display_name]);
    await client.query('COMMIT');
    const token = jwt.sign({ id: u.id, handle }, JWT_SECRET, { expiresIn: '30d' });
    res.status(201).json({ token, user_id: u.id, handle });
  } catch (e) {
    await client.query('ROLLBACK');
    if (e.code === '23505') return res.status(409).json({ error: 'Email or handle already taken' });
    res.status(500).json({ error: e.message });
  } finally { client.release(); }
});

app.post('/api/v1/auth/login', async (req, res) => {
  const { email, password } = req.body ?? {};
  if (!email || !password) return res.status(400).json({ error: 'Missing credentials' });
  const { rows: [u] } = await pool.query(
    `SELECT u.id, u.password_hash, p.handle FROM users u JOIN profiles p ON p.id=u.id WHERE u.email=$1 AND u.is_active=TRUE`,
    [email.toLowerCase()]);
  if (!u || !(await bcrypt.compare(password, u.password_hash)))
    return res.status(401).json({ error: 'Invalid credentials' });
  const token = jwt.sign({ id: u.id, handle: u.handle }, JWT_SECRET, { expiresIn: '30d' });
  res.json({ token, user_id: u.id, handle: u.handle });
});

// ── Profiles ───────────────────────────────────────────────────
app.get('/api/v1/profiles/me', auth, async (req, res) => {
  const { rows: [p] } = await pool.query(
    `SELECT p.*,(SELECT COUNT(*) FROM visitor_logs vl WHERE vl.profile_id=p.id AND vl.visited_at>NOW()-INTERVAL '1 day') AS visitors_today FROM profiles p WHERE p.id=$1`,
    [req.user.id]);
  if (!p) return res.status(404).json({ error: 'Profile not found' });
  res.json(p);
});

app.get('/api/v1/profiles/:handle', async (req, res) => {
  const { rows: [p] } = await pool.query(
    `SELECT p.*,(SELECT COUNT(*) FROM visitor_logs vl WHERE vl.profile_id=p.id AND vl.visited_at>NOW()-INTERVAL '1 day') AS visitors_today FROM profiles p WHERE p.handle=$1`,
    [req.params.handle]);
  if (!p) return res.status(404).json({ error: 'Profile not found' });
  if (p.is_private) return res.status(403).json({ error: 'Private profile' });
  res.json(p);
});

app.patch('/api/v1/profiles/me', auth, async (req, res) => {
  const allowed = ['display_name','bio','avatar_url','cover_url','music_url','music_title','music_artist','ad_title','ad_description','ad_link_url','is_private'];
  const fields = Object.entries(req.body ?? {}).filter(([k]) => allowed.includes(k));
  if (!fields.length) return res.status(400).json({ error: 'No valid fields' });
  const sets = fields.map(([k], i) => `${k}=$${i + 2}`).join(',');
  const vals = [req.user.id, ...fields.map(([, v]) => v)];
  const { rows: [p] } = await pool.query(`UPDATE profiles SET ${sets} WHERE id=$1 RETURNING *`, vals);
  res.json(p);
});

app.post('/api/v1/profiles/:id/visit', async (req, res) => {
  try {
    await pool.query(`INSERT INTO visitor_logs(profile_id,visitor_id,visitor_ip) VALUES($1,$2,$3)`,
      [req.params.id, req.user?.id ?? null, req.ip]);
  } catch {} // swallow duplicate errors
  res.json({ ok: true });
});

app.get('/api/v1/profiles/:id/visitors', auth, async (req, res) => {
  const period = req.query.period === 'today' ? '1 day' : '7 days';
  const { rows: [r] } = await pool.query(
    `SELECT COUNT(*) AS count FROM visitor_logs WHERE profile_id=$1 AND visited_at>NOW()-INTERVAL '${period}'`,
    [req.params.id]);
  res.json({ count: parseInt(r.count) });
});

// ── Posts ──────────────────────────────────────────────────────
app.get('/api/v1/posts/feed', auth, async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit ?? 20), 50);
  const cursor = req.query.cursor;
  const { rows } = await pool.query(
    `SELECT po.*, pr.handle, pr.display_name, pr.avatar_url
     FROM posts po JOIN profiles pr ON pr.id=po.author_id
     WHERE po.is_deleted=FALSE AND po.visibility IN ('public','neighbors')
       AND (po.author_id=$1 OR EXISTS(
         SELECT 1 FROM neighbours n WHERE
           ((n.from_user=$1 AND n.to_user=po.author_id) OR (n.to_user=$1 AND n.from_user=po.author_id))
           AND n.status='accepted'))
       ${cursor ? `AND po.created_at < $3` : ''}
     ORDER BY po.created_at DESC LIMIT $2`,
    cursor ? [req.user.id, limit, cursor] : [req.user.id, limit]);
  const next = rows.length === limit ? rows[rows.length - 1].created_at : null;
  res.json({ posts: rows, next_cursor: next });
});

app.get('/api/v1/posts', async (req, res) => {
  const authorId = req.query.author;
  if (!authorId) return res.status(400).json({ error: 'author param required' });
  const limit = Math.min(parseInt(req.query.limit ?? 20), 50);
  const cursor = req.query.cursor;
  const { rows } = await pool.query(
    `SELECT po.*, pr.handle, pr.display_name, pr.avatar_url
     FROM posts po JOIN profiles pr ON pr.id=po.author_id
     WHERE po.author_id=$1 AND po.is_deleted=FALSE AND po.visibility IN ('public','neighbors')
       ${cursor ? `AND po.created_at < $3` : ''}
     ORDER BY po.created_at DESC LIMIT $2`,
    cursor ? [authorId, limit, cursor] : [authorId, limit]);
  const next = rows.length === limit ? rows[rows.length - 1].created_at : null;
  res.json({ posts: rows, next_cursor: next });
});

app.post('/api/v1/posts', auth, async (req, res) => {
  const { content, title, mood='everyday', visibility='neighbors', media_urls=[] } = req.body ?? {};
  if (!content) return res.status(400).json({ error: 'content required' });
  const { rows: [p] } = await pool.query(
    `INSERT INTO posts(author_id,title,content,mood,visibility,media_urls) VALUES($1,$2,$3,$4,$5,$6) RETURNING *`,
    [req.user.id, title, content, mood, visibility, media_urls]);
  try {
    await pool.query(
      `INSERT INTO notifications(user_id,type,actor_id,ref_post_id) SELECT n.to_user,$1,$2,$3 FROM neighbours n WHERE n.from_user=$2 AND n.status='accepted' ON CONFLICT DO NOTHING`,
      ['like', req.user.id, p.id]);
  } catch {}
  res.status(201).json(p);
});

app.patch('/api/v1/posts/:id', auth, async (req, res) => {
  const { content, title, mood, visibility } = req.body ?? {};
  const { rows: [p] } = await pool.query(
    `UPDATE posts SET content=COALESCE($2,content),title=COALESCE($3,title),mood=COALESCE($4,mood),visibility=COALESCE($5,visibility) WHERE id=$1 AND author_id=$6 AND is_deleted=FALSE RETURNING *`,
    [req.params.id, content, title, mood, visibility, req.user.id]);
  if (!p) return res.status(404).json({ error: 'Post not found or not yours' });
  res.json(p);
});

app.delete('/api/v1/posts/:id', auth, async (req, res) => {
  await pool.query(`UPDATE posts SET is_deleted=TRUE WHERE id=$1 AND author_id=$2`, [req.params.id, req.user.id]);
  res.json({ ok: true });
});

app.post('/api/v1/posts/:id/like', auth, async (req, res) => {
  try {
    await pool.query(`INSERT INTO likes(user_id,post_id) VALUES($1,$2)`, [req.user.id, req.params.id]);
    const { rows: [post] } = await pool.query(`SELECT author_id FROM posts WHERE id=$1`, [req.params.id]);
    if (post && post.author_id !== req.user.id) {
      await pool.query(`INSERT INTO notifications(user_id,type,actor_id,ref_post_id) VALUES($1,'like',$2,$3) ON CONFLICT DO NOTHING`,
        [post.author_id, req.user.id, req.params.id]);
    }
  } catch (e) { if (e.code !== '23505') return res.status(400).json({ error: e.message }); }
  res.json({ ok: true });
});

app.delete('/api/v1/posts/:id/like', auth, async (req, res) => {
  await pool.query(`DELETE FROM likes WHERE user_id=$1 AND post_id=$2`, [req.user.id, req.params.id]);
  res.json({ ok: true });
});

// ── Pages ──────────────────────────────────────────────────────
app.get('/api/v1/pages', async (req, res) => {
  const ownerId = req.query.owner;
  if (!ownerId) return res.status(400).json({ error: 'owner param required' });
  const { rows } = await pool.query(`SELECT * FROM pages WHERE owner_id=$1 AND is_published=TRUE ORDER BY created_at DESC`, [ownerId]);
  res.json({ pages: rows });
});

app.get('/api/v1/pages/:ownerId/:slug', async (req, res) => {
  const { rows: [p] } = await pool.query(
    `SELECT pa.*,array_agg(row_to_json(ps)) FILTER(WHERE ps.id IS NOT NULL) AS sections FROM pages pa LEFT JOIN page_sections ps ON ps.page_id=pa.id WHERE pa.owner_id=$1 AND pa.slug=$2 AND pa.is_published=TRUE GROUP BY pa.id`,
    [req.params.ownerId, req.params.slug]);
  if (!p) return res.status(404).json({ error: 'Page not found' });
  res.json(p);
});

app.post('/api/v1/pages', auth, async (req, res) => {
  const { slug, title='My Page', is_published=false } = req.body ?? {};
  if (!slug) return res.status(400).json({ error: 'slug required' });
  const { rows: [p] } = await pool.query(
    `INSERT INTO pages(owner_id,slug,title,is_published) VALUES($1,$2,$3,$4) RETURNING *`,
    [req.user.id, slug, title, is_published]);
  res.status(201).json(p);
});

app.patch('/api/v1/pages/:id/layout', auth, async (req, res) => {
  const { layout_json } = req.body ?? {};
  const { rows: [p] } = await pool.query(
    `UPDATE pages SET layout_json=$2 WHERE id=$1 AND owner_id=$3 RETURNING *`,
    [req.params.id, layout_json, req.user.id]);
  if (!p) return res.status(404).json({ error: 'Page not found' });
  res.json(p);
});

app.patch('/api/v1/pages/:id/sections', auth, async (req, res) => {
  const { sections = [] } = req.body ?? {};
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    for (const s of sections) {
      await client.query(
        `INSERT INTO page_sections(page_id,section_key,type,content,grid_pos) VALUES($1,$2,$3,$4,$5) ON CONFLICT(page_id,section_key) DO UPDATE SET type=EXCLUDED.type,content=EXCLUDED.content,grid_pos=EXCLUDED.grid_pos`,
        [req.params.id, s.key, s.type, s.content, s.grid_pos]);
    }
    await client.query('COMMIT');
    res.json({ ok: true });
  } catch (e) { await client.query('ROLLBACK'); res.status(500).json({ error: e.message }); }
  finally { client.release(); }
});

app.delete('/api/v1/pages/:id', auth, async (req, res) => {
  await pool.query(`DELETE FROM pages WHERE id=$1 AND owner_id=$2`, [req.params.id, req.user.id]);
  res.json({ ok: true });
});

// ── Neighbours ─────────────────────────────────────────────────
app.get('/api/v1/neighbours', auth, async (req, res) => {
  const { rows } = await pool.query(
    `SELECT n.*,pr.handle,pr.display_name,pr.avatar_url FROM neighbours n JOIN profiles pr ON pr.id=CASE WHEN n.from_user=$1 THEN n.to_user ELSE n.from_user END WHERE (n.from_user=$1 OR n.to_user=$1) ORDER BY n.created_at DESC`,
    [req.user.id]);
  res.json({ neighbours: rows });
});

app.post('/api/v1/neighbours/:userId', auth, async (req, res) => {
  try {
    await pool.query(`INSERT INTO neighbours(from_user,to_user) VALUES($1,$2)`, [req.user.id, req.params.userId]);
    await pool.query(`INSERT INTO notifications(user_id,type,actor_id) VALUES($1,'neighbour_request',$2)`, [req.params.userId, req.user.id]);
  } catch (e) { if (e.code === '23505') return res.status(409).json({ error: 'Request already sent' }); return res.status(400).json({ error: e.message }); }
  res.status(201).json({ ok: true });
});

app.patch('/api/v1/neighbours/:id/accept', auth, async (req, res) => {
  const { rows: [n] } = await pool.query(`UPDATE neighbours SET status='accepted' WHERE id=$1 AND to_user=$2 RETURNING *`, [req.params.id, req.user.id]);
  if (!n) return res.status(404).json({ error: 'Request not found' });
  await pool.query(`INSERT INTO notifications(user_id,type,actor_id) VALUES($1,'neighbour_accept',$2)`, [n.from_user, req.user.id]);
  res.json(n);
});

// ── Notifications ──────────────────────────────────────────────
app.get('/api/v1/notifications', auth, async (req, res) => {
  const { rows } = await pool.query(
    `SELECT n.*,pr.handle AS actor_handle,pr.display_name AS actor_name,pr.avatar_url AS actor_avatar FROM notifications n LEFT JOIN profiles pr ON pr.id=n.actor_id WHERE n.user_id=$1 ORDER BY n.created_at DESC LIMIT 50`,
    [req.user.id]);
  const unread = rows.filter(r => !r.is_read).length;
  res.json({ notifications: rows, unread_count: unread });
});

app.patch('/api/v1/notifications/read-all', auth, async (req, res) => {
  await pool.query(`UPDATE notifications SET is_read=TRUE WHERE user_id=$1`, [req.user.id]);
  res.json({ ok: true });
});

// ── Waitlist ───────────────────────────────────────────────────
app.post('/api/v1/waitlist', async (req, res) => {
  const { email, name, message } = req.body ?? {};
  if (!email) return res.status(400).json({ error: 'email required' });
  try {
    await pool.query(`INSERT INTO waitlist(email,name,message) VALUES($1,$2,$3)`, [email.toLowerCase(), name, message]);
    res.status(201).json({ ok: true });
  } catch (e) {
    if (e.code === '23505') return res.status(409).json({ error: 'Email already registered' });
    res.status(500).json({ error: e.message });
  }
});

// ── Start ──────────────────────────────────────────────────────
app.listen(PORT, () => console.log(`KONGGER API running on :${PORT}`));
