
// Theme toggle
(function(){
  const toggle = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  let dark = true;
  root.setAttribute('data-theme', 'dark');
  if (toggle) {
    toggle.addEventListener('click', () => {
      dark = !dark;
      root.setAttribute('data-theme', dark ? 'dark' : 'light');
      toggle.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      toggle.innerHTML = dark
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
    });
  }
})();

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Mobile menu
let menuOpen = false;
function toggleMobileMenu() {
  menuOpen = !menuOpen;
  const menu = document.getElementById('mobile-menu');
  const btn = document.querySelector('.nav-mobile-toggle');
  menu.classList.toggle('open', menuOpen);
  btn.setAttribute('aria-expanded', menuOpen.toString());
  btn.innerHTML = menuOpen
    ? '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'
    : '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="8" x2="21" y2="8"/><line x1="3" y1="16" x2="21" y2="16"/></svg>';
}
function closeMobileMenu() { if(menuOpen) toggleMobileMenu(); }
document.addEventListener('keydown', e => { if(e.key === 'Escape') { closeModal(); closeMobileMenu(); } });

// Modal
function openModal(tab) {
  document.getElementById('auth-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
  switchTab(tab || 'signup');
  setTimeout(() => {
    const first = document.querySelector('#auth-modal input');
    if (first) first.focus();
  }, 100);
}
function closeModal() {
  document.getElementById('auth-modal').classList.remove('open');
  document.body.style.overflow = '';
}
function handleOverlayClick(e) { if(e.target === document.getElementById('auth-modal')) closeModal(); }
function switchTab(tab) {
  document.querySelectorAll('.modal-tab').forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected','false'); });
  document.querySelectorAll('.form-panel').forEach(p => p.classList.remove('active'));
  const activeTab = document.getElementById('tab-' + tab);
  const activePanel = document.getElementById('panel-' + tab);
  if(activeTab) { activeTab.classList.add('active'); activeTab.setAttribute('aria-selected','true'); }
  if(activePanel) activePanel.classList.add('active');
}

// Toast
let toastTimer;
function showToast(msg) {
  const toast = document.getElementById('toast');
  const msgEl = document.getElementById('toast-msg');
  msgEl.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

// Auth handlers
function handleSignup() {
  const name = document.getElementById('signup-name').value.trim();
  const email = document.getElementById('signup-email').value.trim();
  if(!name) { document.getElementById('signup-name').focus(); showToast('Please enter your name'); return; }
  if(!email || !email.includes('@')) { document.getElementById('signup-email').focus(); showToast('Please enter a valid email'); return; }
  closeModal();
  showToast('🎉 Welcome to NEXUS! Setting up your workspace...');
}
function handleLogin() {
  const email = document.getElementById('login-email').value.trim();
  if(!email || !email.includes('@')) { document.getElementById('login-email').focus(); showToast('Please enter your email'); return; }
  closeModal();
  showToast('✓ Logging you in... redirecting to dashboard');
}
function handleOAuth(provider) {
  closeModal();
  showToast(`Connecting with ${provider}...`);
}

// Nav scroll effect
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if(window.scrollY > 20) { nav.style.borderBottomColor = 'var(--border-mid)'; }
  else { nav.style.borderBottomColor = 'var(--border)'; }
}, { passive: true });
