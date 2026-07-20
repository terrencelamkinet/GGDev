/**
 * KONGGER server.js — Express API Server
 * Node.js 20+ | pg (node-postgres) | JWT auth
 * Install: npm install express pg jsonwebtoken bcryptjs cors helmet express-rate-limit dotenv
 */
import 'dotenv/config';
import express     from 'express';
import { Pool }    from 'pg';
import jwt         from 'jsonwebtoken';
import bcrypt      from 'bcryptjs';
import cors        from 'cors';
import helmet      from 'helmet';
import rateLimit   from 'express-rate-limit';

const pool = new Pool({
  connectionString: process.env.PG_CONNECTION_STRING,
  max: 20, idleTimeoutMillis: 30000, connectionTimeoutMillis: 2000,
});

async function query(sql, params = [], userId = null) {
  const client = await pool.connect();
  try {
    if (userId) await client.query(`SET app.current_user_id = '${userId}'`);
    return await client.query(sql, params);
  } finally { client.release(); }
}

function auth(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try { req.user = jwt.verify(token, process.env.JWT_SECRET); next(); }
  catch { res.status(401).json({ error: 'Invalid token' }); }
}

const app = express();
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGIN ?? '*' }));
app.use(express.json({ limit: '2mb' }));

const limiter = rateLimit({ windowMs: 60000, max: 120, standardHeaders: true });
const writeLimiter = rateLimit({ windowMs: 60000, max: 30 });
const r = express.Router();
app.use('/api/v1', limiter, r);

// AUTH
r.post('/auth/register', writeLimiter, async (req, res) => {
  const { email, password, display_name, handle } = req.body;
  if (!email || !password || !display_name || !handle)
    return res.status(400).json({ error: 'Missing required fields' });
  try {
    const hashed = await bcrypt.hash(password, 12);
    const user = await query('INSERT INTO users (email,hashed_password) VALUES ($1,$2) RETURNING id,email',
      [email.toLowerCase(), hashed]);
    const uid = user.rows[0].id;
    await query('INSERT INTO profiles (id,display_name,handle) VALUES ($1,$2,$3)',
      [uid, display_name, handle.toLowerCase()], uid);
    const token = jwt.sign({ sub: uid, email }, process.env.JWT_SECRET, { expiresIn: '30d' });
    res.json({ token, user: user.rows[0] });
  } catch (e) {
    if (e.code === '23505') return res.status(409).json({ error: 'Email or handle already taken' });
    res.status(500).json({ error: 'Server error' });
  }
});

r.post('/auth/login', writeLimiter, async (req, res) => {
  const { email, password } = req.body;
  const u = await query('SELECT id,email,hashed_password FROM users WHERE email=$1', [email?.toLowerCase()]);
  if (!u.rows[0] || !await bcrypt.compare(password, u.rows[0].hashed_password))
    return res.status(401).json({ error: 'Invalid credentials' });
  const token = jwt.sign({ sub: u.rows[0].id, email }, process.env.JWT_SECRET, { expiresIn: '30d' });
  res.json({ token });
});

// PROFILES
r.get('/profiles/me', auth, async (req, res) => {
  const r2 = await query('SELECT * FROM profiles WHERE id=$1', [req.user.sub], req.user.sub);
  r2.rows[0] ? res.json(r2.rows[0]) : res.status(404).json({ error: 'Not found' });
});
r.get('/profiles/:handle', async (req, res) => {
  const r2 = await query('SELECT * FROM profiles WHERE handle=$1', [req.params.handle.toLowerCase()]);
  r2.rows[0] ? res.json(r2.rows[0]) : res.status(404).json({ error: 'Not found' });
});
r.patch('/profiles/me', auth, writeLimiter, async (req, res) => {
  const allowed = ['display_name','bio','avatar_url','cover_url','music_url','music_title',
    'music_artist','ad_title','ad_description','ad_link_url','theme_colour','is_private'];
  const upd = {};
  for (const k of allowed) if (req.body[k] !== undefined) upd[k] = req.body[k];
  if (!Object.keys(upd).length) return res.status(400).json({ error: 'Nothing to update' });
  const sets = Object.keys(upd).map((k, i) => `${k}=$${i+2}`).join(',');
  const vals = [req.user.sub, ...Object.values(upd)];
  const r2 = await query(`UPDATE profiles SET ${sets} WHERE id=$1 RETURNING *`, vals, req.user.sub);
  res.json(r2.rows[0]);
});
r.post('/profiles/:id/visit', async (req, res) => {
  await query('INSERT INTO visitor_logs (profile_id,visitor_id) VALUES ($1,$2)',
    [req.params.id, req.user?.sub ?? null]);
  res.json({ ok: true });
});
r.get('/profiles/:id/visitors', auth, async (req, res) => {
  const periods = { today: '1 day', week: '7 days', month: '30 days' };
  const intv = periods[req.query.period ?? 'today'] ?? '1 day';
  const r2 = await query(
    `SELECT COUNT(*) AS count FROM visitor_logs WHERE profile_id=$1 AND created_at>NOW()-INTERVAL '${intv}'`,
    [req.params.id], req.user.sub);
  res.json({ count: parseInt(r2.rows[0].count) });
});

// POSTS
r.get('/posts/feed', auth, async (req, res) => {
  const { cursor, limit=20 } = req.query;
  const params = [req.user.sub, parseInt(limit)];
  const cc = cursor ? `AND p.created_at<$3` : '';
  if (cursor) params.push(new Date(cursor));
  const r2 = await query(
    `SELECT p.*,pr.display_name,pr.handle,pr.avatar_url FROM posts p
     JOIN profiles pr ON pr.id=p.author_id
     WHERE (p.author_id=$1 OR p.visibility='public'
       OR (p.visibility='neighbors' AND EXISTS (
         SELECT 1 FROM neighbours n WHERE n.status='accepted'
           AND ((n.requester_id=$1 AND n.addressee_id=p.author_id)
             OR (n.addressee_id=$1 AND n.requester_id=p.author_id)))))
     ${cc} ORDER BY p.created_at DESC LIMIT $2`,
    params, req.user.sub);
  const rows = r2.rows;
  res.json({ posts: rows, next_cursor: rows.length===parseInt(limit) ? rows.at(-1)?.created_at : null });
});
r.get('/posts', async (req, res) => {
  const { author, cursor, limit=20 } = req.query;
  const uid = req.headers.authorization ? jwt.decode(req.headers.authorization.split(' ')[1])?.sub : null;
  const params = [author, parseInt(limit)];
  if (cursor) params.push(new Date(cursor));
  const r2 = await query(
    `SELECT p.*,pr.display_name,pr.handle,pr.avatar_url FROM posts p
     JOIN profiles pr ON pr.id=p.author_id WHERE p.author_id=$1
     AND (p.visibility='public' ${cursor?'AND p.created_at<$3':''})
     ORDER BY p.created_at DESC LIMIT $2`, params, uid);
  res.json({ posts: r2.rows, next_cursor: r2.rows.length===parseInt(limit)?r2.rows.at(-1)?.created_at:null });
});
r.get('/posts/:id', async (req, res) => {
  const r2 = await query(
    `SELECT p.*,pr.display_name,pr.handle,pr.avatar_url FROM posts p JOIN profiles pr ON pr.id=p.author_id WHERE p.id=$1`,
    [req.params.id]);
  r2.rows[0] ? res.json(r2.rows[0]) : res.status(404).json({ error: 'Not found' });
});
r.post('/posts', auth, writeLimiter, async (req, res) => {
  const { title, content, mood, visibility, media_urls } = req.body;
  if (!content?.trim()) return res.status(400).json({ error: 'Content required' });
  const r2 = await query(
    `INSERT INTO posts (author_id,title,content,mood,visibility,media_urls) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *`,
    [req.user.sub, title, content.trim(), mood??'everyday', visibility??'neighbors', media_urls??[]],
    req.user.sub);
  res.status(201).json(r2.rows[0]);
});
r.patch('/posts/:id', auth, writeLimiter, async (req, res) => {
  const { title, content, mood, visibility } = req.body;
  const r2 = await query(
    `UPDATE posts SET title=$2,content=$3,mood=$4,visibility=$5 WHERE id=$1 AND author_id=$6 RETURNING *`,
    [req.params.id,title,content,mood,visibility,req.user.sub], req.user.sub);
  r2.rows[0] ? res.json(r2.rows[0]) : res.status(404).json({ error: 'Not found' });
});
r.delete('/posts/:id', auth, async (req, res) => {
  await query('DELETE FROM posts WHERE id=$1 AND author_id=$2', [req.params.id,req.user.sub], req.user.sub);
  res.json({ ok: true });
});
r.post('/posts/:id/like', auth, async (req, res) => {
  try {
    await query('INSERT INTO likes (user_id,post_id) VALUES ($1,$2)', [req.user.sub,req.params.id], req.user.sub);
    const cnt = await query('SELECT like_count FROM posts WHERE id=$1', [req.params.id]);
    res.json({ liked: true, like_count: cnt.rows[0]?.like_count });
  } catch(e) {
    if (e.code==='23505') return res.status(409).json({ error: 'Already liked' });
    res.status(500).json({ error: 'Server error' });
  }
});
r.delete('/posts/:id/like', auth, async (req, res) => {
  await query('DELETE FROM likes WHERE user_id=$1 AND post_id=$2', [req.user.sub,req.params.id], req.user.sub);
  const cnt = await query('SELECT like_count FROM posts WHERE id=$1', [req.params.id]);
  res.json({ liked: false, like_count: cnt.rows[0]?.like_count });
});

// COMMENTS
r.get('/posts/:postId/comments', async (req, res) => {
  const { cursor, limit=20 } = req.query;
  const uid = req.headers.authorization ? jwt.decode(req.headers.authorization.split(' ')[1])?.sub : null;
  const params = [req.params.postId, parseInt(limit)];
  const cc = cursor ? 'AND c.created_at<$3' : '';
  if (cursor) params.push(new Date(cursor));
  const r2 = await query(
    `SELECT c.*,pr.display_name,pr.handle,pr.avatar_url FROM comments c
     JOIN profiles pr ON pr.id=c.author_id
     WHERE c.post_id=$1 AND c.is_deleted=FALSE ${cc}
     ORDER BY c.created_at ASC LIMIT $2`,
    params, uid);
  res.json({ comments: r2.rows, next_cursor: r2.rows.length===parseInt(limit) ? r2.rows.at(-1)?.created_at : null });
});
r.post('/posts/:postId/comments', auth, writeLimiter, async (req, res) => {
  const { content, parent_id } = req.body;
  if (!content?.trim()) return res.status(400).json({ error: 'Content required' });
  const r2 = await query(
    `INSERT INTO comments (post_id,author_id,parent_id,content) VALUES ($1,$2,$3,$4) RETURNING *`,
    [req.params.postId, req.user.sub, parent_id??null, content.trim()], req.user.sub);
  res.status(201).json(r2.rows[0]);
});
r.delete('/comments/:id', auth, async (req, res) => {
  await query("UPDATE comments SET is_deleted=TRUE,content='[deleted]' WHERE id=$1 AND author_id=$2",
    [req.params.id, req.user.sub], req.user.sub);
  res.json({ ok: true });
});

// PAGES
r.get('/pages', async (req, res) => {
  const r2 = await query(`SELECT * FROM pages WHERE owner_id=$1 AND is_published=TRUE ORDER BY sort_order`, [req.query.owner]);
  res.json(r2.rows);
});
r.get('/pages/:ownerId/:slug', async (req, res) => {
  const r2 = await query(
    `SELECT p.*,json_agg(ps ORDER BY ps.z_index) AS sections FROM pages p
     LEFT JOIN page_sections ps ON ps.page_id=p.id
     WHERE p.owner_id=$1 AND p.slug=$2 AND p.is_published=TRUE GROUP BY p.id`,
    [req.params.ownerId, req.params.slug]);
  r2.rows[0] ? res.json(r2.rows[0]) : res.status(404).json({ error: 'Page not found' });
});
r.post('/pages', auth, writeLimiter, async (req, res) => {
  const { slug, title, description } = req.body;
  const r2 = await query(
    `INSERT INTO pages (owner_id,slug,title,description) VALUES ($1,$2,$3,$4) RETURNING *`,
    [req.user.sub,slug,title,description], req.user.sub);
  res.status(201).json(r2.rows[0]);
});
r.patch('/pages/:id/layout', auth, async (req, res) => {
  const r2 = await query(
    `UPDATE pages SET layout_json=$2 WHERE id=$1 AND owner_id=$3 RETURNING id,layout_json`,
    [req.params.id, req.body.layout_json, req.user.sub], req.user.sub);
  res.json(r2.rows[0] ?? { error: 'Not found' });
});
r.patch('/pages/:id/sections', auth, writeLimiter, async (req, res) => {
  const { sections } = req.body;
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    await client.query(`SET app.current_user_id='${req.user.sub}'`);
    await client.query('DELETE FROM page_sections WHERE page_id=$1', [req.params.id]);
    for (const s of sections) {
      await client.query(
        `INSERT INTO page_sections (page_id,section_type,title,content_json,position_x,position_y,width,height,z_index)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)`,
        [req.params.id,s.section_type,s.title,s.content_json,s.position_x,s.position_y,s.width,s.height,s.z_index]);
    }
    await client.query('COMMIT');
    res.json({ ok: true });
  } catch(e) { await client.query('ROLLBACK'); res.status(500).json({ error: e.message }); }
  finally { client.release(); }
});
r.delete('/pages/:id', auth, async (req, res) => {
  await query('DELETE FROM pages WHERE id=$1 AND owner_id=$2', [req.params.id,req.user.sub], req.user.sub);
  res.json({ ok: true });
});

// NEIGHBOURS
r.get('/neighbours', auth, async (req, res) => {
  const r2 = await query(
    `SELECT n.*,pr.display_name,pr.handle,pr.avatar_url FROM neighbours n
     JOIN profiles pr ON pr.id=CASE WHEN n.requester_id=$1 THEN n.addressee_id ELSE n.requester_id END
     WHERE (n.requester_id=$1 OR n.addressee_id=$1) AND n.status='accepted'`,
    [req.user.sub], req.user.sub);
  res.json(r2.rows);
});
r.post('/neighbours/:userId', auth, writeLimiter, async (req, res) => {
  try {
    const r2 = await query(`INSERT INTO neighbours (requester_id,addressee_id) VALUES ($1,$2) RETURNING *`,
      [req.user.sub, req.params.userId], req.user.sub);
    res.status(201).json(r2.rows[0]);
  } catch(e) { res.status(409).json({ error: e.message }); }
});
r.patch('/neighbours/:id/accept', auth, async (req, res) => {
  const r2 = await query(
    `UPDATE neighbours SET status='accepted' WHERE id=$1 AND addressee_id=$2 RETURNING *`,
    [req.params.id, req.user.sub], req.user.sub);
  res.json(r2.rows[0]);
});

// NOTIFICATIONS
r.get('/notifications', auth, async (req, res) => {
  const extra = req.query.unread==='true' ? ' AND is_read=FALSE' : '';
  const r2 = await query(
    `SELECT n.*,pr.display_name,pr.handle,pr.avatar_url FROM notifications n
     LEFT JOIN profiles pr ON pr.id=n.actor_id
     WHERE n.user_id=$1 ${extra} ORDER BY n.created_at DESC LIMIT 50`,
    [req.user.sub], req.user.sub);
  res.json(r2.rows);
});
r.patch('/notifications/read-all', auth, async (req, res) => {
  await query('UPDATE notifications SET is_read=TRUE WHERE user_id=$1', [req.user.sub], req.user.sub);
  res.json({ ok: true });
});

// WAITLIST
r.post('/waitlist', writeLimiter, async (req, res) => {
  const { email, name, message } = req.body;
  if (!email?.includes('@')) return res.status(400).json({ error: 'Valid email required' });
  try {
    const r2 = await query(
      `INSERT INTO waitlist (email,name,message) VALUES ($1,$2,$3) RETURNING id,invite_code`,
      [email.toLowerCase(), name, message]);
    res.status(201).json(r2.rows[0]);
  } catch(e) {
    if (e.code==='23505') return res.status(409).json({ error: 'Email already registered' });
    res.status(500).json({ error: 'Server error' });
  }
});

// HEALTH
app.get('/health', async (_, res) => {
  try { await pool.query('SELECT 1'); res.json({ status: 'ok', pg: 'connected' }); }
  catch { res.status(503).json({ status: 'error', pg: 'disconnected' }); }
});

const PORT = process.env.PORT ?? 3001;
app.listen(PORT, () => console.log(`KONGGER API :${PORT}`));
export default app;
