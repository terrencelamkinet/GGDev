export function initTheme(){
  const html=document.documentElement,btn=document.querySelector('[data-theme-toggle]');
  let dark=matchMedia('(prefers-color-scheme:dark)').matches;
  const stored=localStorage.getItem('kongger-theme');if(stored)dark=stored==='dark';
  function apply(){html.setAttribute('data-theme',dark?'dark':'light');if(btn)btn.innerHTML=dark?sun():moon();}
  apply();
  btn?.addEventListener('click',()=>{dark=!dark;localStorage.setItem('kongger-theme',dark?'dark':'light');apply();});
}
const moon=()=>`<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
const sun=()=>`<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`;