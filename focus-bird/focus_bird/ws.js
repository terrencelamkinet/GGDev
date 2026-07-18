/* ================================================================
   FOCUS BIRD PRO — ws.js
   WebSocket bridge to focus_bridge_windows.py
   ================================================================ */
'use strict';

const WS = (() => {
  let socket = null;
  let retryTimer = null;
  const URL = 'wss://brainlink.kinet-poc.com/game';
  const EMA = 0.18;   /* smoothing factor for focus signal */

  function setDot(ok) {
    const d = document.getElementById('ws-dot');
    if (d) d.classList.toggle('ok', ok);
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

          /* Signal check: only enable extMode when BrainLink is actually connected.
             relay.py sends signal=200 (no_signal) as initial state even without
             BrainLink — without this check the game sees attention=50 and thinks
             it's in extMode, causing the bird to descend on default values. */
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

  return { connect, send };
})();
