/**
 * KONGGER db-client.js — Frontend PostgreSQL API Client
 * All DB access goes through this module.
 *
 * Timing targets (matching Instagram/Facebook):
 *   Button tap -> optimistic UI:     0ms   (immediate visual feedback)
 *   Local cache read:                <5ms
 *   API response (cached CDN):       <80ms
 *   API response (first load):       <300ms
 *   Page navigation (SPA hash):      <150ms
 */

const API_BASE = window.__KONGGER_CONFIG?.apiBase ?? '/api/v1';
const CACHE_TTL = { profile: 60000, posts: 30000, feed: 20000, pages: 120000, notifications: 10000 };

// ── Memory Cache ─────────────────────────────────────────────────
const _cache = new Map();
function cacheGet(key) {
  const e = _cache.get(key);
  if (!e) return null;
  if (Date.now() > e.expires) { _cache.delete(key); return null; }
  return e.value;
}
function cacheSet(key, val, ttl) { _cache.set(key, { value: val, expires: Date.now() + ttl }); }
function cacheInvalidate(pat) { for (const k of _cache.keys()) if (k.startsWith(pat)) _cache.delete(k); }

// ── Write Queue (debounced) ───────────────────────────────────────
const _wq = new Map();
function queueWrite(key, fn, ms = 500) {
  return new Promise((res) => {
    if (_wq.has(key)) clearTimeout(_wq.get(key).t);
    const t = setTimeout(async () => { _wq.delete(key); res(await fn()); }, ms);
    _wq.set(key, { t });
  });
}

// ── Core Fetch ───────────────────────────────────────────────────
async function apiFetch(method, path, body = null) {
  const token = window.__KONGGER_CONFIG?.authToken;
  try {
    const res = await fetch(API_BASE + path, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: 'Bearer ' + token } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
    const json = await res.json();
    if (!res.ok) return { data: null, error: json.error ?? 'Request failed', status: res.status };
    return { data: json, error: null, status: res.status };
  } catch (err) {
    return { data: null, error: err.message, status: 0 };
  }
}

// ── Profile API ───────────────────────────────────────────────────
export const ProfileAPI = {
  async getByHandle(handle) {
    const k = `profile:${handle}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', `/profiles/${handle}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.profile);
    return r;
  },
  async getMe(userId) {
    const k = `profile:me:${userId}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', '/profiles/me');
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.profile);
    return r;
  },
  async update(payload) {
    cacheInvalidate('profile:me');
    return queueWrite('profile:update', () => apiFetch('PATCH', '/profiles/me', payload), 500);
  },
  logVisit(profileId) { apiFetch('POST', `/profiles/${profileId}/visit`); },
  async getVisitors(id, period = 'today') { return apiFetch('GET', `/profiles/${id}/visitors?period=${period}`); },
};

// ── Post API ──────────────────────────────────────────────────────
export const PostAPI = {
  async getFeed(cursor = null, limit = 20) {
    const k = `feed:${cursor}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const p = new URLSearchParams({ limit });
    if (cursor) p.set('cursor', cursor);
    const r = await apiFetch('GET', `/posts/feed?${p}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.feed);
    return r;
  },
  async listByAuthor(authorId, cursor = null, limit = 20) {
    const k = `posts:author:${authorId}:${cursor}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const p = new URLSearchParams({ author: authorId, limit });
    if (cursor) p.set('cursor', cursor);
    const r = await apiFetch('GET', `/posts?${p}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.posts);
    return r;
  },
  async getById(id) {
    const k = `post:${id}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', `/posts/${id}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.posts);
    return r;
  },
  async create(payload) {
    cacheInvalidate('posts:author:'); cacheInvalidate('feed:');
    return apiFetch('POST', '/posts', payload);
  },
  async update(id, payload) {
    cacheInvalidate(`post:${id}`); cacheInvalidate('posts:author:');
    return apiFetch('PATCH', `/posts/${id}`, payload);
  },
  async delete(id) {
    cacheInvalidate(`post:${id}`); cacheInvalidate('posts:author:'); cacheInvalidate('feed:');
    return apiFetch('DELETE', `/posts/${id}`);
  },
  /** Optimistic: update UI immediately, then call this */
  async toggleLike(postId, currentlyLiked) {
    cacheInvalidate(`post:${postId}`);
    return apiFetch(currentlyLiked ? 'DELETE' : 'POST', `/posts/${postId}/like`);
  },
};

// ── Page API ──────────────────────────────────────────────────────
export const PageAPI = {
  async listByOwner(ownerId) {
    const k = `pages:owner:${ownerId}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', `/pages?owner=${ownerId}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.pages);
    return r;
  },
  async getBySlug(ownerId, slug) {
    const k = `page:${ownerId}:${slug}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', `/pages/${ownerId}/${slug}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.pages);
    return r;
  },
  async create(payload) {
    cacheInvalidate('pages:owner:');
    return apiFetch('POST', '/pages', payload);
  },
  /** Debounced 800ms — drag-drop auto-save */
  async updateLayout(pageId, layoutJson) {
    cacheInvalidate('page:');
    return queueWrite(`page:layout:${pageId}`, () => apiFetch('PATCH', `/pages/${pageId}/layout`, { layout_json: layoutJson }), 800);
  },
  async updateSections(pageId, sections) {
    cacheInvalidate('page:');
    return queueWrite(`page:sections:${pageId}`, () => apiFetch('PATCH', `/pages/${pageId}/sections`, { sections }), 800);
  },
  async delete(pageId) {
    cacheInvalidate('pages:');
    return apiFetch('DELETE', `/pages/${pageId}`);
  },
};

// ── Neighbour API ─────────────────────────────────────────────────
export const NeighbourAPI = {
  async list() {
    const c = cacheGet('neighbours:list');
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', '/neighbours');
    if (!r.error) cacheSet('neighbours:list', r.data, 30000);
    return r;
  },
  async sendRequest(userId) { cacheInvalidate('neighbours:'); return apiFetch('POST', `/neighbours/${userId}`); },
  async accept(reqId) { cacheInvalidate('neighbours:'); return apiFetch('PATCH', `/neighbours/${reqId}/accept`); },
  async remove(userId) { cacheInvalidate('neighbours:'); return apiFetch('DELETE', `/neighbours/${userId}`); },
};

// ── Notification API ──────────────────────────────────────────────
export const NotificationAPI = {
  async list(unreadOnly = false) {
    const k = `notif:${unreadOnly}`;
    const c = cacheGet(k);
    if (c) return { data: c, error: null };
    const r = await apiFetch('GET', `/notifications?unread=${unreadOnly}`);
    if (!r.error) cacheSet(k, r.data, CACHE_TTL.notifications);
    return r;
  },
  async markAllRead() { cacheInvalidate('notif:'); return apiFetch('PATCH', '/notifications/read-all'); },
  async markRead(id) { cacheInvalidate('notif:'); return apiFetch('PATCH', `/notifications/${id}/read`); },
};

// ── Waitlist API ──────────────────────────────────────────────────
export const WaitlistAPI = {
  async join(email, name, message) { return apiFetch('POST', '/waitlist', { email, name, message }); },
};

export default { Profile: ProfileAPI, Post: PostAPI, Page: PageAPI, Neighbour: NeighbourAPI, Notification: NotificationAPI, Waitlist: WaitlistAPI };
