export function showToast(msg,type='info',duration=3000){
  const c=document.getElementById('toast-container');if(!c)return;
  const t=document.createElement('div');const icons={success:'✓',error:'✕',info:'ℹ'};
  t.className=`toast toast--${type} toast-enter`;
  t.innerHTML=`<span>${icons[type]||'ℹ'}</span><span>${msg}</span>`;
  c.appendChild(t);
  if(type!=='error'&&duration>0){setTimeout(()=>{t.classList.replace('toast-enter','toast-exit');setTimeout(()=>t.remove(),210);},duration);}
  else{const x=document.createElement('button');x.textContent='×';x.style.cssText='margin-left:auto;font-size:1.2em;opacity:.7;cursor:pointer;border:none;background:none';x.onclick=()=>{t.classList.add('toast-exit');setTimeout(()=>t.remove(),210)};t.appendChild(x);}
}