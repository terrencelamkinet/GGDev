/* AI Central — Shared JS — v1.1.0 (icon system) */
(function(){
'use strict';

// ── Version ──────────────────────────────────────────────
window.AC_VER='v1.5.0';

// ── Theme ────────────────────────────────────────────────
const root=document.documentElement;
let theme=root.getAttribute('data-theme')||
  (matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
root.setAttribute('data-theme',theme);

function applyTheme(){
  root.setAttribute('data-theme',theme);
  document.querySelectorAll('[data-tt-ico]').forEach(ico=>{
    ico.closest('[data-tt]').innerHTML=theme==='dark'
      ?'<svg data-tt-ico width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      :'<svg data-tt-ico width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  });
}
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-tt]');
  if(b){theme=theme==='dark'?'light':'dark';applyTheme()}
});
applyTheme();

// ── Navigation helper ────────────────────────────────────
window.go=function(page){window.location.href=page};
window.closeOverlay=function(id){document.getElementById(id)?.classList.remove('open')};

// ── SVG icon helper ──────────────────────────────────────
window.IC=function(n){
  return '<img src="assets/icons/'+n+'.svg" class="ai-icon" alt="" width="20" height="20">';
};

// ── Toast ────────────────────────────────────────────────
let tc=document.getElementById('toast-container');
if(!tc){tc=document.createElement('div');tc.id='toast-container';document.body.appendChild(tc)}
window.AC={};
window.AC.toast=function(msg,type='',dur=2800){
  const t=document.createElement('div');
  t.className='toast'+(type?' '+type:'');t.textContent=msg;
  tc.appendChild(t);
  setTimeout(()=>{t.style.opacity='0';t.style.transform='translateX(20px)';
    t.style.transition='all .25s';setTimeout(()=>t.remove(),250)},dur);
};

// ── Sidebar HTML ─────────────────────────────────────────
const NAV=[
  {id:'dashboard', ico:'home',     lbl:'Dashboard',   href:'dashboard.html'},
  {id:'diagram',   ico:'brain',    lbl:'AI Diagram',  href:'diagram.html'},
  {id:'timeline',  ico:'calendar', lbl:'Timeline',    href:'timeline.html'},
  {id:'agents',    ico:'robot',    lbl:'AI Agents',   href:'agents.html'},
  {id:'cronjobs',  ico:'clock',    lbl:'Cron Jobs',   href:'cronjobs.html'},
  {id:'skills',    ico:'bolt',     lbl:'Skills',      href:'skills.html'},
  {id:'mcp',       ico:'plug',     lbl:'MCP Servers', href:'mcp.html', badge:'1'},
  {id:'apis',      ico:'link',     lbl:'APIs',        href:'apis.html'},
  {id:'upgrades',  ico:'arrow_up', lbl:'Upgrades',    href:'upgrades.html', badge:'8'},
  {id:'logs',      ico:'clipboard',lbl:'Logs',        href:'logs.html'},
  {id:'settings',  ico:'gear',     lbl:'Settings',    href:'settings.html'},
];

window.AC.sidebar=function(active){
  return`
<div class="sb-overlay" id="sb-ov" onclick="closeSidebar()"></div>
<nav class="sidebar" id="sb-nav" aria-label="Main navigation">
  <div class="sb-header">
    <div class="sb-logo-ico"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polygon points="12,2 22,8 22,16 12,22 2,16 2,8"/><circle cx="12" cy="12" r="3" fill="white" stroke="none"/></svg></div>
    <div><div class="sb-logo-txt">AI Central</div><div class="sb-logo-sub">System Monitor</div></div>
  </div>
  <div style="padding:6px 0">
    <div class="sb-section">Navigation</div>
    ${NAV.slice(0,3).map(n=>`
    <a href="${n.href}" class="sb-item${n.id===active?' on':''}" onclick="closeSidebar()">
      <span class="si-ico">${IC(n.ico)}</span>
      <span class="si-lbl">${n.lbl}</span>
      ${n.badge?`<span class="sb-badge">${n.badge}</span>`:''}
    </a>`).join('')}
    <div class="sb-section">AI Agents</div>
    ${NAV.slice(3,5).map(n=>`
    <a href="${n.href}" class="sb-item${n.id===active?' on':''}" onclick="closeSidebar()">
      <span class="si-ico">${IC(n.ico)}</span><span class="si-lbl">${n.lbl}</span>${n.badge?`<span class="sb-badge">${n.badge}</span>`:''}
    </a>`).join('')}
    <div class="sb-section">Configuration</div>
    ${NAV.slice(5,9).map(n=>`
    <a href="${n.href}" class="sb-item${n.id===active?' on':''}" onclick="closeSidebar()">
      <span class="si-ico">${IC(n.ico)}</span><span class="si-lbl">${n.lbl}</span>${n.badge?`<span class="sb-badge">${n.badge}</span>`:''}
    </a>`).join('')}
    <div class="sb-section">System</div>
    ${NAV.slice(9).map(n=>`
    <a href="${n.href}" class="sb-item${n.id===active?' on':''}" onclick="closeSidebar()">
      <span class="si-ico">${IC(n.ico)}</span><span class="si-lbl">${n.lbl}</span>${n.badge?`<span class="sb-badge">${n.badge}</span>`:''}
    </a>`).join('')}
  </div>
  <div class="sb-footer">
    <div class="sb-item" onclick="go('settings.html')"><span class="si-ico">${IC('user')}</span><span class="si-lbl">Terrence Lam</span></div>
    <div class="sb-ver">${window.AC_VER}</div>
  </div>
</nav>`;
};

// ── Bottom nav (mobile 5 key pages) ──────────────────────
const BNAV=[
  {id:'dashboard', ico:'home',     lbl:'Home',     href:'dashboard.html'},
  {id:'timeline',  ico:'calendar', lbl:'Timeline', href:'timeline.html'},
  {id:'agents',    ico:'robot',    lbl:'Agents',   href:'agents.html'},
  {id:'upgrades',  ico:'arrow_up', lbl:'Upgrades', href:'upgrades.html'},
  {id:'settings',  ico:'gear',     lbl:'Settings', href:'settings.html'},
];
window.AC.bnav=function(active){
  return`<nav class="bottom-nav" aria-label="Bottom navigation">
    ${BNAV.map(n=>`
    <a href="${n.href}" class="bn-item${n.id===active?' on':''}">
      <span class="bn-ico">${IC(n.ico)}</span>
      <span>${n.lbl}</span>
    </a>`).join('')}
  </nav>`;
};

// ── Hamburger markup (injected into topbar) ───────────────
window.AC.ham=`<button class="ham-btn" onclick="toggleSidebar()" aria-label="Toggle menu">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
    <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
</button>`;

// ── Sidebar toggle ────────────────────────────────────────
window.toggleSidebar=function(){
  const nav=document.getElementById('sb-nav');
  const ov=document.getElementById('sb-ov');
  if(!nav)return;
  const isOpen=nav.classList.contains('open');
  nav.classList.toggle('open',!isOpen);
  ov.classList.toggle('open',!isOpen);
  document.body.style.overflow=isOpen?'':'hidden';
};
window.closeSidebar=function(){
  document.getElementById('sb-nav')?.classList.remove('open');
  document.getElementById('sb-ov')?.classList.remove('open');
  document.body.style.overflow='';
};

// ── Swipe-to-close sidebar on mobile ─────────────────────
let sxStart=0;
document.addEventListener('touchstart',e=>{sxStart=e.touches[0].clientX},{passive:true});
document.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-sxStart;
  if(dx<-60&&document.getElementById('sb-nav')?.classList.contains('open'))closeSidebar();
},{passive:true});

// ── Swipe right from edge to open sidebar ─────────────────
document.addEventListener('touchstart',e=>{
  if(e.touches[0].clientX<20)sxStart=e.touches[0].clientX;
},{passive:true});
document.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-sxStart;
  if(sxStart<20&&dx>50)toggleSidebar();
},{passive:true});

// ── Close overlay on backdrop click ──────────────────────
document.addEventListener('click',e=>{
  if(e.target.classList.contains('overlay'))closeOverlay(e.target.id);
});

// ── Bottom modal sheet drag-to-close ─────────────────────
let mdStart=0,mdEl=null;
document.addEventListener('touchstart',e=>{
  const drag=e.target.closest('.modal-drag');
  if(drag){mdStart=e.touches[0].clientY;mdEl=drag.closest('.overlay')}
},{passive:true});
document.addEventListener('touchend',e=>{
  if(mdEl){
    const dy=e.changedTouches[0].clientY-mdStart;
    if(dy>80)mdEl.classList.remove('open');
    mdEl=null;
  }
},{passive:true});

})();
