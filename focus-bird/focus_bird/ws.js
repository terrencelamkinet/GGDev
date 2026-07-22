/* ================================================================
   FOCUS BIRD PRO — ws.js
   WebSocket bridge to focus_bridge_windows.py
   ================================================================ */
'use strict';

const WS = (() => {
  let socket = null;
  let retryTimer = null;
  let lastMsgTime = 0;
  const URL = 'wss://brainlink.kinet-poc.com/game';
  const ATT_BUF_SIZE = 5;  /* rolling average window */

  /* — Exposed for debug panel — */
  const stats = { connected: false, lastAtt: '-', lastSig: '-', msgs: 0, errs: 0, log: [], lastMsgAt: 0, deviceConnected: false, hasEEG: false, dataLive: false };
  let attBuf = [];  /* rolling buffer for smoothing */

  function setDot(ok, isLive) {
    const d = document.getElementById('ws-dot');
    if (!d) return;
    d.classList.toggle('ok', ok && isLive);
    d.classList.toggle('stale', ok && !isLive);
    stats.connected = ok;
    stats.dataLive = !!isLive;
    if (typeof UI !== 'undefined') UI.updateWSLabel();
  }

  function connect() {
    try {
      if (socket) { socket.onclose = null; socket.close(); }
      socket = new WebSocket(URL);

      socket.onopen = () => {
        setDot(true, false);
        console.log('[WS] Connected to', URL);
      };

      socket.onclose = () => {
        setDot(false);
        G.extMode = false;
        /* show offline in HUD */
        const dsEl = document.getElementById('device-status');
        if (dsEl) { dsEl.innerHTML = '🔴 離線'; dsEl.style.color = '#ff6b6b'; }
        if (retryTimer) clearTimeout(retryTimer);
        retryTimer = setTimeout(connect, 3000);
        stats.msgs = 0;
      };

      socket.onerror = () => {
        setDot(false);
        G.extMode = false;
        stats.errs++;
      };

      socket.onmessage = (ev) => {
        try {
          const d = JSON.parse(ev.data);
          lastMsgTime = Date.now();
          stats.msgs++;
          stats.lastAtt = d.attention;
          stats.lastSig = d.signal;
          stats.deviceConnected = d.deviceConnected === true;
          stats.hasEEG = d.hasEEG === true;
          /* Update HUD device-status in real time */
          const dsEl = document.getElementById('device-status');
          if (dsEl) {
            const sigOk = typeof d.signal === 'number' && d.signal >= 0 && d.signal < 150;
            const attOk = typeof d.attention === 'number';
            if (sigOk && attOk) {
              dsEl.innerHTML = '🧠 已連接';
              dsEl.style.color = '#74d680';
            } else if (typeof d.signal === 'number' && d.signal >= 150) {
              dsEl.innerHTML = '🔴 無裝置';
              dsEl.style.color = '#ff6b6b';
            } else {
              dsEl.innerHTML = '⏳';
              dsEl.style.color = '#9bbfd4';
            }
          }

          console.log('[WS]', JSON.stringify(d));
          // status indicator element
          if (!stats._statusEl) stats._statusEl = document.getElementById('ws-status');

          /* Signal check — only use BrainLink data when signal < 150 */
          const hasSignal = typeof d.signal === 'number' && d.signal < 150;

          /* Keep rolling log of last 10 messages */
          stats.log.push({ t: Date.now(), att: d.attention, sig: d.signal, hasSig: hasSignal });
          if (stats.log.length > 10) stats.log.shift();

          /* Primary: use rolling average of last N attention values */
          if (typeof d.attention === 'number' && hasSignal) {
            attBuf.push(d.attention);
            if (attBuf.length > ATT_BUF_SIZE) attBuf.shift();
            var sum = 0;
            for (var i = 0; i < attBuf.length; i++) sum += attBuf[i];
            G.focus = Math.round(sum / attBuf.length);
            G.extMode = true;
            stats.lastMsgAt = Date.now();  /* only mark as fresh when real data */
            setDot(true, true);  /* live device data detected */
          } else if (typeof d.attention === 'number') {
            /* signal bad — log but hold G.focus */
            G.extMode = false;
          } else {
            G.extMode = false;
          }

          /* Extended EEG: TBR bonus if beta rising (tiny boost) */
          if (typeof d.highBeta === 'number' && typeof d.theta === 'number') {
            const tbr = d.theta / (d.highBeta + 1);
            if (tbr < 2.5 && hasSignal) {
              G.focus = Math.min(100, G.focus + 1);
            }
          }

          if (typeof d.threshold === 'number') G.threshold = d.threshold;
          if (typeof d.age       === 'number') G.age       = d.age;

        } catch (_) { stats.errs++; }
      };

    } catch (_) { setDot(false); }
  }

  function checkStale() {
    if (!G.extMode) return;
    if (Date.now() - lastMsgTime > 5000) {
      G.extMode = false;
      setDot(true, false);  /* connected but data stale */
      console.log('[WS] Stale timeout — keyboard fallback');
    }
  }

  function send(obj) {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(obj));
    }
  }

  return { connect, send, checkStale, stats };
})();
