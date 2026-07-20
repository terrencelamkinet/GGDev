export function initModals(){
  document.querySelectorAll('.modal-overlay').forEach(ov=>{
    ov.addEventListener('click',e=>{if(e.target===ov){ov.classList.remove('open');document.body.style.overflow='';}});
  });
  document.querySelectorAll('[data-modal-close]').forEach(btn=>{
    btn.addEventListener('click',()=>{const ov=document.getElementById(btn.dataset.modalClose);if(ov){ov.classList.remove('open');document.body.style.overflow='';}});
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.modal-overlay.open').forEach(m=>{m.classList.remove('open');document.body.style.overflow='';});});
}