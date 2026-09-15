const { app, BrowserWindow, globalShortcut, Tray, Menu, ipcMain, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');
const https = require('https');
const http = require('http');
const { spawn } = require('child_process');

// ── Config ────────────────────────────────
const CFG_DIR = path.join(os.homedir(), '.smart-ai');
const CFG_PATH = path.join(CFG_DIR, 'config.json');
const NOTES_PATH = path.join(CFG_DIR, 'notes.json');
const REC_DIR = path.join(CFG_DIR, 'recordings');

function ensureDir(p) { try { fs.mkdirSync(p, { recursive: true }); } catch(e) {} }
ensureDir(CFG_DIR); ensureDir(REC_DIR);

function loadJSON(p, def) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch(e) { return def; }
}
function saveJSON(p, data) {
  fs.writeFileSync(p, JSON.stringify(data, null, 2), 'utf8');
}

var config = loadJSON(CFG_PATH, {
  server_url: 'http://localhost:8000',
  weather_api_key: '',
  wake_word: '喂GG',
  hotkey: 'CommandOrControl+Alt+A',
  telegram_token: '',
  telegram_chat_id: ''
});

// ── Window ────────────────────────────────
var win = null;
var tray = null;
var isVisible = true;

function createWindow() {
  win = new BrowserWindow({
    width: 480, height: 620,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: false,
    resizable: true,
    minWidth: 360, minHeight: 480,
    backgroundColor: '#0a0a14',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    }
  });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  win.setAlwaysOnTop(true, 'screen-saver');
  win.setMenu(null);
  win.on('close', function(e) {
    if (!app.isQuitting) { e.preventDefault(); win.hide(); isVisible = false; }
  });
}

// ── Tray ─────────────────────────────────
function createTray() {
  var ico = nativeImage.createEmpty();
  tray = new Tray(ico);
  tray.setToolTip('Smart AI');
  var ctx = Menu.buildFromTemplate([
    { label: 'Show/Hide (Ctrl+Alt+A)', click: toggleView },
    { type: 'separator' },
    { label: 'Settings', click: function() { if(win) win.show(); } },
    { type: 'separator' },
    { label: 'Quit', click: function() { app.isQuitting = true; app.quit(); } }
  ]);
  tray.setContextMenu(ctx);
  tray.on('click', toggleView);
}
function toggleView() {
  if (!win) return;
  isVisible ? (win.hide(), isVisible=false) : (win.show(), win.focus(), isVisible=true);
}

// ── IPC Handlers ─────────────────────────
ipcMain.on('minimize', function() { if(win) win.minimize(); });
ipcMain.on('close', function() { if(win) { win.hide(); isVisible=false; } });
ipcMain.on('toggle', toggleView);

// System info
ipcMain.handle('getSysInfo', function() {
  var cpus = os.cpus();
  var totalMem = os.totalmem(), freeMem = os.freemem();
  // Simple CPU load
  var cpuLoad = 0;
  for (var i = 0; i < cpus.length; i++) {
    var cpu = cpus[i];
    var idle = cpu.times.idle;
    var total = cpu.times.user + cpu.times.nice + cpu.times.sys + cpu.times.idle + cpu.times.irq;
    cpuLoad += (1 - idle/total) * 100;
  }
  cpuLoad = Math.round(cpuLoad / cpus.length);
  
  return {
    cpu: cpuLoad,
    ram: Math.round((1 - freeMem/totalMem) * 100),
    disk: 0, // Would need disk usage module
    uptime: Math.floor(os.uptime() / 86400) + 'd'
  };
});

// Weather
ipcMain.handle('getWeather', function() {
  return new Promise(function(resolve) {
    if (!config.weather_api_key) {
      resolve({ error: 'No API key', temp: '—', condition: 'No key', icon: '' });
      return;
    }
    var url = 'https://api.openweathermap.org/data/2.5/weather?q=Hong+Kong&units=metric&appid=' + config.weather_api_key;
    https.get(url, function(resp) {
      var data = '';
      resp.on('data', function(c) { data += c; });
      resp.on('end', function() {
        try {
          var j = JSON.parse(data);
          resolve({ temp: Math.round(j.main.temp), condition: j.weather[0].main, icon: j.weather[0].icon });
        } catch(e) { resolve({ error: e.message, temp: '—', condition: 'Error', icon: '' }); }
      });
    }).on('error', function(e) { resolve({ error: e.message, temp: '—', condition: 'Error', icon: '' }); });
  });
});

// Chat with Hermes
ipcMain.handle('chat', function(evt, msg) {
  return new Promise(function(resolve) {
    var payload = JSON.stringify({ message: msg, session_id: 'desktop-' + os.hostname() });
    var url = new URL('/api/v1/chat', config.server_url);
    var req = http.request({
      hostname: url.hostname,
      port: url.port || 8000,
      path: url.pathname,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
    }, function(resp) {
      var data = '';
      resp.on('data', function(c) { data += c; });
      resp.on('end', function() {
        try {
          var j = JSON.parse(data);
          resolve({ ok: true, reply: j.reply || j.response || data });
        } catch(e) { resolve({ ok: true, reply: data }); }
      });
    });
    req.on('error', function(e) { resolve({ ok: false, error: e.message }); });
    req.write(payload);
    req.end();
  });
});

// Notes
ipcMain.handle('getNotes', function() { return loadJSON(NOTES_PATH, { notes: [] }); });
ipcMain.handle('saveNote', function(evt, note) {
  var data = loadJSON(NOTES_PATH, { notes: [] });
  data.notes.push({ text: note, ts: new Date().toISOString() });
  saveJSON(NOTES_PATH, data);
  return { ok: true };
});
ipcMain.handle('deleteNote', function(evt, idx) {
  var data = loadJSON(NOTES_PATH, { notes: [] });
  if (idx >= 0 && idx < data.notes.length) data.notes.splice(idx, 1);
  saveJSON(NOTES_PATH, data);
  return { ok: true };
});

// Recording
ipcMain.handle('saveRecording', function(evt, base64data) {
  var fn = 'recording-' + Date.now() + '.wav';
  var buf = Buffer.from(base64data, 'base64');
  fs.writeFileSync(path.join(REC_DIR, fn), buf);
  return { ok: true, file: fn };
});

// ── App ──────────────────────────────────
app.whenReady().then(function() {
  createWindow();
  createTray();
  globalShortcut.register('CommandOrControl+Alt+A', toggleView);
});

app.on('window-all-closed', function() {});
app.on('before-quit', function() { app.isQuitting = true; });
app.on('will-quit', function() { globalShortcut.unregisterAll(); });
