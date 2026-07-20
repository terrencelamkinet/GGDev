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
  const EMA = 0.18;   /* smoothing factor for focus signal */
  const STALE_MS = 5000;  /* if no message for 5s, disable extMode */

  /* Run every frame: if data is stale, disable extMode so keyboard works */
  function checkStale() {
    if (G.extMode && Date.now() - lastMsgTime > STALE_MS) {
      G.extMode = false;
    }
  }

  function setDot(ok) {
    const d = document.getElementById('ws-dot');
    if (d) { d.classList.toggle('ok', ok); d.classList.toggle('connecting', !ok); }
    const lbl = document.getElementById('ws-label');
    if (lbl) { lbl.textContent = ok ? 'ON' : 'OFF'; lbl.style.color = ok ? '#74d680' : '#ff6b6b'; }
    if (typeof UI !== 'undefined') UI.updateWSLabel();
  }

  function connect() {
    try {
      if (socket) { socket.onclose = null; socket.close(); }
      socket = new WebSocket(URL);

      socket.onopen = () => {
        setDot(true);
        console.log('[WS] Connected to', URL);
      };

      socket.onclose = () => {
        setDot(false);
        if (retryTimer) clearTimeout(retryTimer);
        retryTimer = setTimeout(connect, 3000);
      };

      socket.onerror = () => setDot(false);

      socket.onmessage = (ev) => {
        try {
          const d = JSON.parse(ev.data);
          lastMsgTime = Date.now();

          /* Signal check: only enable extMode when BrainLink is actually connected.
             Relay server auto-sets signal=200 when data is >5s stale.
             Bridge now sets signal=0 when receiving real EEG data. */
          const hasSignal = typeof d.signal === 'number' && d.signal < 150;

          /* Primary: use attention value */
          if (typeof d.attention === 'number') {
            G.focus  = G.focus * (1 - EMA) + d.attention * EMA;
            if (hasSignal) G.extMode = true;
          }

          /* Extended EEG: TBR bonus if beta rising */
          if (typeof d.highBeta === 'number' && typeof d.theta === 'number') {
            const tbr = d.theta / (d.highBeta + 1);
            if (tbr < 2.5) {
              /* Good focus state — boost slightly */
              G.focus = Math.min(100, G.focus + 0.5);
            }
          }

          /* Accept threshold/age override from bridge */
          if (typeof d.threshold === 'number') G.threshold = d.threshold;
          if (typeof d.age       === 'number') G.age       = d.age;

        } catch (_) {}
      };

    } catch (_) { setDot(false); }

    /* Also clear extMode on disconnect so the game falls back to manual/keyboard
       control when WebSocket drops, rather than freezing at the last focus value. */
    function clearExtMode() { G.extMode = false; }
    if (!socket._eb_ext) {
      socket.addEventListener('close', clearExtMode);
      socket.addEventListener('error', clearExtMode);
      socket._eb_ext = true;
    }
  }

  function send(obj) {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(obj));
    }
  }

  return { connect, send, checkStale };
})();
