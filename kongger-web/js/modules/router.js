export function initRouter(routes){
  function activate(hash){
    const id=(hash.replace('#','').replace('/',''))||'home';
    document.querySelectorAll('.page').forEach(p=>{
      if(p.id==='page-'+id){p.classList.add('active','page-enter');setTimeout(()=>p.classList.remove('page-enter'),220);}
      else p.classList.remove('active');
    });
    document.querySelectorAll('.nav__link,.bottom-nav__item').forEach(a=>{a.classList.toggle('active',a.dataset.page===id)});
    if(routes[id])routes[id]();
    window.scrollTo({top:0,behavior:'instant'});
  }
  window.addEventListener('hashchange',()=>activate(location.hash));
  activate(location.hash||'#home');
}