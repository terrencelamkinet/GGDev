/* ================================================================
   TOP FOCUS METER — topmeter.js
   置頂中央的專注力感應大儀錶（數字式）+ 即時報表 + 4組記錄面板
   - 高專注 (5秒均值 ≥85%)
   - 低專注 (5秒均值 ≤30%)
   - 急升 (單次升幅 >50)
   - 急跌 (單次跌幅 >50)
   ================================================================ */
'use strict';

const TopMeter = (() => {
  /* ---------- state ---------- */
  let rafId = null;
  let rawValue = 50;
  let dispValue = 50;
  let velocity = 0;
  let history = [];
  const HIST_MAX = 100;
  const WINDOW_MS = 5000;

  let highArmed = true, lowArmed = true;
  let highLogs = [], lowLogs = [];
  const LOG_MAX = 30;

  let demo = false, demoSeed = 50;
  let sampleTimer = null;
  let lastTick = 0;
  let prevValue = 50;
  let surgeLogs = [], plungeLogs = [];

  const els = {};

  function fmtTime(d) {
    const p = n => String(n).padStart(2, '0');
    return p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds()) + '.' + String(d.getMilliseconds()).padStart(3,'0').slice(0,2);
  }

  function focusColor(v) {
    if (v >= 85) return '#4f8cff';
    if (v >= 60) return '#74d680';
    if (v >= 30) return '#ffd166';
    return '#ff6b6b';
  }

  /* ---------- 建立 DOM ---------- */
  function mount() {
    if (document.getElementById('tfm-wrap')) return;

    const wrap = document.createElement('div');
    wrap.id = 'tfm-wrap';
    wrap.innerHTML =
      '<div id="tfm-gauge-box"><canvas id="tfm-gauge-canvas"></canvas></div>' +
      '<div id="tfm-report-box"><canvas id="tfm-report-canvas"></canvas></div>' +
      '<div id="tfm-log-row">' +
        '<div class="tfm-log-panel">' +
          '<div class="tfm-log-title high">&#x1f535; 高專注 (5秒均值 &#x2265;85%)</div>' +
          '<div id="tfm-high-list"><div class="tfm-log-empty">尚未記錄</div></div>' +
        '</div>' +
        '<div class="tfm-log-panel">' +
          '<div class="tfm-log-title low">&#x1f534; 低專注 (5秒均值 &#x2264;30%)</div>' +
          '<div id="tfm-low-list"><div class="tfm-log-empty">尚未記錄</div></div>' +
        '</div>' +
        '<div class="tfm-log-panel">' +
          '<div class="tfm-log-title surge">&#x1f4c8; 急升 (單次升 &gt;50)</div>' +
          '<div id="tfm-surge-list"><div class="tfm-log-empty">尚未記錄</div></div>' +
        '</div>' +
        '<div class="tfm-log-panel">' +
          '<div class="tfm-log-title plunge">&#x1f4c9; 急跌 (單次跌 &gt;50)</div>' +
          '<div id="tfm-plunge-list"><div class="tfm-log-empty">尚未記錄</div></div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(wrap);

    els.gaugeCanvas  = document.getElementById('tfm-gauge-canvas');
    els.reportCanvas = document.getElementById('tfm-report-canvas');
    els.highList = document.getElementById('tfm-high-list');
    els.lowList  = document.getElementById('tfm-low-list');
    els.surgeList = document.getElementById('tfm-surge-list');
    els.plungeList = document.getElementById('tfm-plunge-list');
  }

  /* ---------- 數據來源 ---------- */
  function readSource() {
    if (typeof window.G !== 'undefined' && typeof window.G.focus === 'number') {
      demo = false;
      return window.G.focus;
    }
    demo = true;
    demoSeed += (Math.random() - 0.5) * 26;
    if (Math.random() < 0.06) demoSeed += (Math.random() - 0.5) * 45;
    demoSeed = Math.max(1, Math.min(99, demoSeed));
    return demoSeed;
  }

  /* ---------- 每秒取樣 ---------- */
  function sampleTick() {
    const v = readSource();
    rawValue = v;

    /* Rapid change tracking */
    const delta = v - prevValue;
    if (delta > 50) {
      const entry = { time: fmtTime(new Date()), val: Math.round(v), delta: Math.round(delta) };
      surgeLogs.push(entry);
      if (surgeLogs.length > LOG_MAX) surgeLogs.shift();
      renderLog(surgeLogs, els.surgeList, 'surge');
    } else if (delta < -50) {
      const entry = { time: fmtTime(new Date()), val: Math.round(v), delta: Math.round(delta) };
      plungeLogs.push(entry);
      if (plungeLogs.length > LOG_MAX) plungeLogs.shift();
      renderLog(plungeLogs, els.plungeList, 'plunge');
    }
    prevValue = v;

    const now = Date.now();
    history.push({ t: now, v });
    if (history.length > HIST_MAX) history.shift();
    evaluateWindows(now);
  }

  function windowAvg(now) {
    const win = history.filter(p => now - p.t <= WINDOW_MS);
    if (win.length === 0) return null;
    return win.reduce((a, b) => a + b.v, 0) / win.length;
  }

  function evaluateWindows(now) {
    const spanOk = history.length > 0 && (now - history[0].t) >= WINDOW_MS - 200;
    if (!spanOk) return;
    const avg = windowAvg(now);
    if (avg === null) return;

    if (avg >= 85) {
      if (highArmed) {
        pushLog(highLogs, els.highList, now, avg, 'high');
        highArmed = false;
      }
    } else {
      highArmed = true;
    }

    if (avg <= 30) {
      if (lowArmed) {
        pushLog(lowLogs, els.lowList, now, avg, 'low');
        lowArmed = false;
      }
    } else {
      lowArmed = true;
    }
  }

  function pushLog(arr, listEl, now, avg, kind) {
    const entry = { time: fmtTime(new Date(now)), avg: Math.round(avg) };
    arr.push(entry);
    if (arr.length > LOG_MAX) arr.shift();
    renderLog(arr, listEl, kind);
  }

  function renderLog(arr, listEl, kind) {
    if (!listEl) return;
    if (arr.length === 0) { listEl.innerHTML = '<div class="tfm-log-empty">尚未記錄</div>'; return; }
    const color = kind === 'high' || kind === 'surge' ? '#4f8cff' : '#ff6b6b';
    let html = '';
    arr.slice().reverse().forEach(e => {
      if (kind === 'surge' || kind === 'plunge') {
        html += '<div class="tfm-log-item"><span>' + e.time + '</span><span style="color:' + color + ';font-weight:800">' + e.val + '% (' + (e.delta > 0 ? '+' : '') + e.delta + ')</span></div>';
      } else {
        html += '<div class="tfm-log-item"><span>' + e.time + '</span><span style="color:' + color + ';font-weight:800">' + e.avg + '%</span></div>';
      }
    });
    listEl.innerHTML = html;
  }

  /* ---------- 自適應緩動 ---------- */
  function tween(dt) {
    const diff = rawValue - dispValue;
    const absDiff = Math.abs(diff);
    if (absDiff < 0.05) { dispValue = rawValue; return; }
    const speedPerSec = 6 + absDiff * 4.2;
    let step = Math.sign(diff) * speedPerSec * dt;
    if (Math.abs(step) > absDiff) step = diff;
    dispValue += step;
  }

  /* ---------- 大儀錶 ---------- */
  function drawGauge() {
    const canvas = els.gaugeCanvas;
    const box = document.getElementById('tfm-gauge-box');
    if (!canvas || !box) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = box.clientWidth, h = box.clientHeight;
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
    }
    const c = canvas.getContext('2d');
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, w, h);

    const val = dispValue;
    const col = focusColor(val);

    const cx = w / 2, cy = h * 0.56, R = Math.min(w, h * 1.8) * 0.34;
    const sA = Math.PI * 0.78, eA = Math.PI * 2.22;
    c.beginPath(); c.arc(cx, cy, R, sA, eA);
    c.strokeStyle = 'rgba(255,255,255,.12)'; c.lineWidth = 10; c.lineCap = 'round'; c.stroke();

    const grad = c.createLinearGradient(cx - R, cy, cx + R, cy);
    grad.addColorStop(0, '#ff6b6b'); grad.addColorStop(.35, '#ffd166');
    grad.addColorStop(.65, '#74d680'); grad.addColorStop(1, '#4f8cff');
    const angle = sA + (val / 100) * (eA - sA);
    c.beginPath(); c.arc(cx, cy, R, sA, angle);
    c.strokeStyle = grad; c.lineWidth = 10; c.lineCap = 'round';
    c.save(); c.shadowColor = col; c.shadowBlur = 16; c.stroke(); c.restore();

    c.textAlign = 'center'; c.textBaseline = 'middle';
    c.font = '900 ' + Math.round(h * 0.34) + "px 'Baloo 2',monospace,sans-serif";
    c.fillStyle = col;
    c.save(); c.shadowColor = col; c.shadowBlur = 18;
    c.fillText(Math.round(val) + '', cx, cy - h * 0.02);
    c.restore();

    c.font = '800 ' + Math.round(h * 0.075) + 'px sans-serif';
    c.fillStyle = '#9bbfd4';
    c.fillText(demo ? 'DEMO 專注感應中...' : '即時專注感應', cx, cy + h * 0.30);

    const prev = history.length > 1 ? history[history.length - 2].v : rawValue;
    const delta = Math.round(rawValue - prev);
    if (delta !== 0 && history.length > 1) {
      c.font = '800 ' + Math.round(h * 0.08) + 'px sans-serif';
      c.fillStyle = delta > 0 ? '#74d680' : '#ff6b6b';
      c.fillText((delta > 0 ? '\u25b2+' : '\u25bc') + Math.abs(delta), cx, cy - h * 0.36);
    }
  }

  /* ---------- 即時報表 ---------- */
  function drawReport() {
    const canvas = els.reportCanvas;
    const box = document.getElementById('tfm-report-box');
    if (!canvas || !box) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = box.clientWidth, h = box.clientHeight;
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
    }
    const c = canvas.getContext('2d');
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, w, h);

    const pad = 6;
    const innerW = w - pad * 2, innerH = h - pad * 2;
    const yPos = p => pad + innerH - (p / 100) * innerH;

    [0, 30, 85, 100].forEach(p => {
      c.beginPath(); c.moveTo(pad, yPos(p)); c.lineTo(w - pad, yPos(p));
      c.strokeStyle = p === 85 ? 'rgba(79,140,255,.4)' : p === 30 ? 'rgba(255,107,107,.35)' : 'rgba(255,255,255,.06)';
      c.setLineDash(p === 0 || p === 100 ? [] : [3, 3]);
      c.lineWidth = 1; c.stroke(); c.setLineDash([]);
    });

    if (history.length < 2) {
      c.font = Math.round(h * 0.32) + 'px sans-serif'; c.fillStyle = '#6d8ba0';
      c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillText('收集數據中...', w / 2, h / 2);
      return;
    }

    const pts = history.slice(-60);
    const stepX = innerW / Math.max(pts.length - 1, 1);
    c.beginPath();
    pts.forEach((p, i) => {
      const px = pad + i * stepX;
      const val = i === pts.length - 1 ? dispValue : p.v;
      const py = yPos(Math.max(0, Math.min(100, val)));
      i === 0 ? c.moveTo(px, py) : c.lineTo(px, py);
    });
    c.strokeStyle = focusColor(dispValue); c.lineWidth = 2; c.stroke();
    c.lineTo(pad + (pts.length - 1) * stepX, yPos(0));
    c.lineTo(pad, yPos(0)); c.closePath();
    c.fillStyle = 'rgba(79,140,255,.10)'; c.fill();

    c.font = Math.round(h * 0.26) + 'px sans-serif'; c.fillStyle = '#9bbfd4';
    c.textAlign = 'left'; c.textBaseline = 'top';
    c.fillText('0-100% 即時報表', pad, pad);
    c.textAlign = 'right';
    c.fillText(Math.round(dispValue) + '%', w - pad, pad);
  }

  /* ---------- 主渲染循環 ---------- */
  let lastFrame = 0;
  function render(ts) {
    if (!lastFrame) lastFrame = ts;
    const dt = Math.min((ts - lastFrame) / 1000, 0.1);
    lastFrame = ts;
    tween(dt);
    drawGauge();
    drawReport();
    rafId = requestAnimationFrame(render);
  }

  function start() {
    mount();
    if (sampleTimer) clearInterval(sampleTimer);
    sampleTick();
    sampleTimer = setInterval(sampleTick, 1000);
    if (!rafId) rafId = requestAnimationFrame(render);
  }

  function stop() {
    if (sampleTimer) { clearInterval(sampleTimer); sampleTimer = null; }
    if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
    lastFrame = 0;
  }

  return { start, stop };
})();

document.addEventListener('DOMContentLoaded', () => TopMeter.start());
if (document.readyState === 'complete' || document.readyState === 'interactive') TopMeter.start();
