/* ── kongger-web static server with API proxy ─────────────────── */
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const PORT = 3002;
const API_TARGET = 'http://localhost:3001';

const app = express();

// ── Proxy /api/v1/* → kongger-api (restore /api/v1 prefix) ────
app.use('/api/v1', createProxyMiddleware({
  target: API_TARGET,
  changeOrigin: true,
  pathRewrite: { '^/': '/api/v1/' },
  on: {
    proxyReq: (proxyReq) => {
      proxyReq.setHeader('X-Forwarded-Proto', 'https');
    },
  },
}));

// ── Proxy /api (non-v1 paths, e.g. /api/health → :3001/health) ─
app.use('/api', createProxyMiddleware({
  target: API_TARGET,
  changeOrigin: true,
}));

// ── Static files ──────────────────────────────────────────────
app.use(express.static(path.join(__dirname)));

// ── SPA fallback (non-API GET requests) ────────────────────────
app.get('/{*path}', (req, res) => {
  if (req.path.startsWith('/api/')) return res.status(404).json({ error: 'not found' });
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`kongger-web running on http://127.0.0.1:${PORT}`);
  console.log(`  → API proxy to ${API_TARGET}/api/v1`);
});
