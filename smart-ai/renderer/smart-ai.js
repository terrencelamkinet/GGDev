// ── Tab Switching ────────────────────────
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(function(t){ t.classList.remove('active'); });
  document.querySelectorAll('.tab-panel').forEach(function(p){ p.classList.remove('active'); });
  var tab = document.querySelector('.tab[data-tab="' + name + '"]');
  var panel = document.getElementById('panel-' + name);
  if (tab) tab.classList.add('active');
  if (panel) panel.classList.add('active');
}
document.addEventListener('click', function(e) {
  var tab = e.target.closest('.tab');
  if (tab) switchTab(tab.dataset.tab);
});

// ── Clock ────────────────────────────────
function updateClock() {
  var n = new Date();
  var h = String(n.getHours()).padStart(2,'0');
  var m = String(n.getMinutes()).padStart(2,'0');
  var s = String(n.getSeconds()).padStart(2,'0');
  document.getElementById('clock-time').textContent = h + ':' + m + ':' + s;
  var days = ['SUN','MON','TUE','WED','THU','FRI','SAT'];
  document.getElementById('clock-date').textContent = days[n.getDay()] + ' ' + n.getDate() + '/' + (n.getMonth()+1);
}
setInterval(updateClock, 1000);
updateClock();

// ── System Info ──────────────────────────
function refreshSysInfo() {
  if (!window.smartAI) return;
  window.smartAI.getSysInfo().then(function(info) {
    document.getElementById('cpu-val').textContent = (info.cpu || '—') + '%';
    document.getElementById('ram-val').textContent = (info.ram || '—') + '%';
    document.getElementById('uptime-val').textContent = info.uptime || '—';
  }).catch(function(){});
}
refreshSysInfo();
setInterval(refreshSysInfo, 30000);

// ── Weather ──────────────────────────────
function refreshWeather() {
  if (!window.smartAI) return;
  window.smartAI.getWeather().then(function(w) {
    var el = document.getElementById('weather-display');
    if (w.error) {
      el.textContent = w.temp + '°C';
    } else {
      el.textContent = w.temp + '°C ' + w.condition;
      if (w.icon) {
        document.getElementById('weather-icon').textContent = w.condition === 'Clear' ? '☀️' : w.condition === 'Clouds' ? '☁️' : w.condition === 'Rain' ? '🌧️' : '🌤️';
      }
    }
  }).catch(function(){});
}
refreshWeather();
setInterval(refreshWeather, 600000);

// ── Chat ─────────────────────────────────
var chatHistory = [];
var chatInput = document.getElementById('chat-input');
var chatSend = document.getElementById('chat-send');
var chatBox = document.getElementById('chat-messages');

function addChatMsg(text, isUser) {
  var d = document.createElement('div');
  d.className = 'msg ' + (isUser ? 'msg-user' : 'msg-bot');
  d.textContent = text;
  chatBox.appendChild(d);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendChat() {
  var text = chatInput.value.trim();
  if (!text) return;
  addChatMsg(text, true);
  chatInput.value = '';
  chatInput.disabled = true;
  chatSend.disabled = true;
  chatSend.textContent = '...';
  
  window.smartAI.chat(text).then(function(resp) {
    addChatMsg(resp.reply || resp.error || 'No response', false);
  }).catch(function(e) {
    addChatMsg('Connection error: ' + e.message, false);
  }).finally(function() {
    chatInput.disabled = false;
    chatSend.disabled = false;
    chatSend.textContent = 'Send';
    chatInput.focus();
  });
}

if (chatSend) chatSend.addEventListener('click', sendChat);
if (chatInput) {
  chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
  });
}

// Quick text input
var quickInput = document.getElementById('quick-input');
var quickBtn = document.getElementById('quick-btn');
if (quickBtn) quickBtn.addEventListener('click', function() {
  var text = quickInput.value.trim();
  if (!text) return;
  switchTab('chat');
  setTimeout(function() {
    chatInput.value = text;
    sendChat();
  }, 200);
});
if (quickInput) {
  quickInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { e.preventDefault(); if (quickBtn) quickBtn.click(); }
  });
}

// ── Notes ────────────────────────────────
function loadNotes() {
  window.smartAI.getNotes().then(function(data) {
    var list = document.getElementById('notes-list');
    list.innerHTML = '';
    if (!data.notes || data.notes.length === 0) {
      list.innerHTML = '<div class="note-empty">No notes yet</div>';
      return;
    }
    data.notes.forEach(function(n, i) {
      var d = document.createElement('div');
      d.className = 'note-item';
      d.innerHTML = '<div class="note-text">' + escapeHTML(n.text) + '</div><div class="note-ts">' + new Date(n.ts).toLocaleString() + '</div><button class="note-del" data-idx="' + i + '">✕</button>';
      d.querySelector('.note-del').addEventListener('click', function() {
        window.smartAI.deleteNote(i).then(loadNotes);
      });
      list.appendChild(d);
    });
  });
}

var noteSave = document.getElementById('note-save');
var noteInput = document.getElementById('note-input');
if (noteSave && noteInput) {
  noteSave.addEventListener('click', function() {
    var text = noteInput.value.trim();
    if (!text) return;
    window.smartAI.saveNote(text).then(function() {
      noteInput.value = '';
      loadNotes();
    });
  });
}
if (noteInput) {
  noteInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); noteSave.click(); }
  });
}
loadNotes();

function escapeHTML(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Recording ────────────────────────────
var mediaRec = null;
var recChunks = [];
var recTimer = null;
var recSeconds = 0;
var recBtn = document.getElementById('rec-btn');
var recStatus = document.getElementById('rec-status');

if (recBtn) {
  recBtn.addEventListener('click', function() {
    if (mediaRec && mediaRec.state === 'recording') {
      mediaRec.stop();
      clearInterval(recTimer);
      recBtn.textContent = '🎤';
      recBtn.classList.remove('recording');
      recStatus.textContent = '';
    } else {
      navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {
        recChunks = [];
        recSeconds = 0;
        mediaRec = new MediaRecorder(stream);
        mediaRec.ondataavailable = function(e) { if (e.data.size > 0) recChunks.push(e.data); };
        mediaRec.onstop = function() {
          var blob = new Blob(recChunks, { type: 'audio/webm' });
          var reader = new FileReader();
          reader.onload = function() {
            var b64 = reader.result.split(',')[1];
            window.smartAI.saveRecording(b64).then(function(r) {
              recStatus.textContent = 'Saved: ' + (r.file || 'OK');
            });
          };
          reader.readAsDataURL(blob);
          stream.getTracks().forEach(function(t) { t.stop(); });
        };
        mediaRec.start();
        recBtn.textContent = '⏹';
        recBtn.classList.add('recording');
        recTimer = setInterval(function() {
          recSeconds++;
          recStatus.textContent = Math.floor(recSeconds/60) + ':' + String(recSeconds%60).padStart(2,'0');
        }, 1000);
      }).catch(function(e) {
        recStatus.textContent = 'Mic error: ' + e.message;
      });
    }
  });
}

// ── 3D Diagram ───────────────────────────
var diagramLoaded = false;
var dScene, dCam, dRenderer, dCtrl;
var dSprGroup, dLinkGroup;

function initDiagram() {
  if (diagramLoaded) return;
  diagramLoaded = true;
  var container = document.getElementById('diagram-container');
  if (!container || typeof THREE === 'undefined') return;
  
  dScene = new THREE.Scene();
  dScene.background = new THREE.Color('#0a0a14');
  dCam = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 1, 2000);
  dCam.position.set(0, 50, 250);
  dRenderer = new THREE.WebGLRenderer({ antialias: true });
  dRenderer.setSize(container.clientWidth, container.clientHeight);
  dRenderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
  container.appendChild(dRenderer.domElement);
  
  dCtrl = new THREE.OrbitControls(dCam, dRenderer.domElement);
  dCtrl.enableDamping = true;
  dCtrl.dampingFactor = 0.1;
  dCtrl.minDistance = 80;
  dCtrl.maxDistance = 500;
  dCtrl.target.set(0, 0, 0);
  
  dScene.add(new THREE.AmbientLight(0xcccccc, 1.2));
  
  // Simple nodes
  dSprGroup = new THREE.Group();
  dScene.add(dSprGroup);
  dLinkGroup = new THREE.Group();
  dScene.add(dLinkGroup);
  
  var nodes = [
    { id:'core', label:'AI Core', x:0, y:0, z:0, color:'#2563eb', size:1 },
    { id:'chat', label:'Chat', x:80, y:40, z:20, color:'#7c3aed', size:0.7 },
    { id:'voice', label:'Voice', x:-60, y:60, z:-30, color:'#0891b2', size:0.7 },
    { id:'notes', label:'Notes', x:-80, y:-30, z:40, color:'#047857', size:0.7 },
    { id:'tasks', label:'Tasks', x:60, y:-50, z:-20, color:'#ea580c', size:0.7 },
    { id:'diagram', label:'3D View', x:90, y:-20, z:-40, color:'#db2777', size:0.7 },
    { id:'system', label:'System', x:-50, y:-60, z:-10, color:'#64748b', size:0.7 },
  ];
  var edges = [
    ['core','chat'],['core','voice'],['core','notes'],['core','tasks'],['core','diagram'],['core','system'],
    ['chat','voice'],['notes','tasks'],['tasks','system']
  ];
  
  // Create sprites
  nodes.forEach(function(nd) {
    var cvs = document.createElement('canvas');
    cvs.width = 160; cvs.height = 80;
    var ctx = cvs.getContext('2d');
    ctx.fillStyle = '#12122a';
    ctx.beginPath(); ctx.roundRect(0,0,160,80,8); ctx.fill();
    ctx.strokeStyle = nd.color; ctx.lineWidth = 2; ctx.beginPath(); ctx.roundRect(0,0,160,80,8); ctx.stroke();
    ctx.font = '22px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle = '#e2e8f0'; ctx.fillText(nd.label, 80, 40);
    
    var tex = new THREE.CanvasTexture(cvs);
    tex.needsUpdate = true;
    var spr = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, sizeAttenuation: true }));
    spr.scale.set(nd.size * 30, nd.size * 15, 1);
    spr.position.set(nd.x, nd.y, nd.z);
    spr.userData = { id: nd.id };
    dSprGroup.add(spr);
  });
  
  // Create links
  edges.forEach(function(e) {
    var a = nodes.find(function(n){return n.id===e[0]});
    var b = nodes.find(function(n){return n.id===e[1]});
    if (!a || !b) return;
    var geom = new THREE.BufferGeometry();
    var verts = new Float32Array([a.x,a.y,a.z,b.x,b.y,b.z]);
    geom.setAttribute('position', new THREE.BufferAttribute(verts, 3));
    var line = new THREE.Line(geom, new THREE.LineBasicMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.3 }));
    dLinkGroup.add(line);
  });
  
  function diagramAnimate() {
    requestAnimationFrame(diagramAnimate);
    if (dCtrl) dCtrl.update();
    if (dRenderer && dScene && dCam) dRenderer.render(dScene, dCam);
  }
  diagramAnimate();
}

// Init diagram if tab shown
var diagramObserver = new MutationObserver(function() {
  var panel = document.getElementById('panel-diagram');
  if (panel && panel.classList.contains('active') && !diagramLoaded) {
    setTimeout(initDiagram, 100);
  }
});
diagramObserver.observe(document.getElementById('panel-diagram') || document.body, { attributes: true, attributeFilter: ['class'] });

// ── Auto-focus chat input ────────────────
switchTab('chat');
if (chatInput) setTimeout(function() { chatInput.focus(); }, 300);
