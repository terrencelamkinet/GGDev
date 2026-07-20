import { initRouter } from './modules/router.js';
import { initTheme }  from './modules/theme.js';
import { initModals } from './modules/modal.js';
import { initParticles } from './modules/particles.js';
import { showToast }  from './modules/toast.js';
import { PostAPI, ProfileAPI, PageAPI, WaitlistAPI, AuthAPI } from './modules/db-client.js';

const routes = { home:loadHome, profile:loadProfile, proposal:()=>{}, ai:loadAI };

// Expose toast globally for onclick attributes
window.showToastGlobal = showToast;

// ── Demo posts when no API ─────────────────────────────────────
const DEMO_POSTS = [
  {id:'1',display_name:'Kat Cheung',handle:'kat_c',avatar_url:'https://picsum.photos/seed/kat/88/88',title:'又到周五的心情',content:'今天天氣不錯，去了維多利亞公園逛了一下。看到有人在放風箏，突然想起小時候爸爸也帶我去放過。時間過得真的很快... 💭',mood:'nostalgic',like_count:24,comment_count:6,created_at:new Date(Date.now()-3600000).toISOString()},
  {id:'2',display_name:'Marcus Lam',handle:'marcus_l',avatar_url:'https://picsum.photos/seed/marcus/88/88',title:'剛看完新電影',content:'終於看了那部大家都在說的電影，果然不負眾望！特效太好看了，劇情也比我想像中複雜。強烈推薦給大家 🎬',mood:'excited',like_count:18,comment_count:12,created_at:new Date(Date.now()-7200000).toISOString()},
  {id:'3',display_name:'Sophie Wu',handle:'sophie_w',avatar_url:'https://picsum.photos/seed/sophie/88/88',title:null,content:'今天煮了第一次湯圓，雖然形狀不太圓... 但味道還可以！下次再改良一下配方 😅🍡',mood:'happy',like_count:42,comment_count:9,created_at:new Date(Date.now()-14400000).toISOString()},
];

function timeAgo(ts){if(!ts)return'';const d=(Date.now()-new Date(ts))/1000;if(d<60)return'just now';if(d<3600)return Math.floor(d/60)+'m ago';if(d<86400)return Math.floor(d/3600)+'h ago';return Math.floor(d/86400)+'d ago';}
function animateNumber(el,from,to,dur){const s=performance.now();requestAnimationFrame(function t(n){const p=Math.min((n-s)/dur,1);el.textContent=Math.round(from+(to-from)*p);if(p<1)requestAnimationFrame(t);});}

function renderPostCard(p){
  const moods={happy:'😊',calm:'😌',moved:'🥺',thinking:'🤔',nostalgic:'💭',everyday:'📖',excited:'🤩',sad:'😢',grateful:'🙏',anxious:'😰'};
  const mood=moods[p.mood]??'📖';
  return `<div class="post-card card-stagger reveal" data-post-id="${p.id}">
    <div class="post-card__header">
      <img class="post-card__avatar" src="${p.avatar_url??'https://picsum.photos/seed/'+p.handle+'/88/88'}" alt="${p.display_name}" width="44" height="44" loading="lazy">
      <div class="post-card__meta">
        <div class="post-card__name">${p.display_name}</div>
        <div class="post-card__handle">@${p.handle} · ${timeAgo(p.created_at)}</div>
      </div>
      <span class="post-card__mood" title="${p.mood||''}">${mood}</span>
    </div>
    ${p.title?`<div class="post-card__title">${p.title}</div>`:''}
    <div class="post-card__content">${p.content}</div>
    <div class="post-card__actions">
      <button class="like-btn" data-post="${p.id}" data-liked="false" aria-label="Like post">
        <span class="heart-icon">♡</span> <span class="like-count">${p.like_count??0}</span>
      </button>
      <button class="btn btn-ghost btn-sm">💬 ${p.comment_count??0}</button>
    </div>
  </div>`;
}

function attachLikeHandlers(container){
  container.querySelectorAll('.like-btn').forEach(btn=>{
    btn.addEventListener('click',async()=>{
      const liked=btn.dataset.liked==='true';
      const countEl=btn.querySelector('.like-count');
      const heartEl=btn.querySelector('.heart-icon');
      const newLiked=!liked;
      btn.dataset.liked=String(newLiked);
      btn.classList.toggle('liked',newLiked);
      heartEl.textContent=newLiked?'♥':'♡';
      if(newLiked){heartEl.classList.add('heart-liked');setTimeout(()=>heartEl.classList.remove('heart-liked'),420);}
      countEl.textContent=parseInt(countEl.textContent)+(newLiked?1:-1);
      const{error}=await PostAPI.toggleLike(btn.dataset.post,liked);
      if(error){
        btn.dataset.liked=String(liked);btn.classList.toggle('liked',liked);
        heartEl.textContent=liked?'♥':'♡';
        countEl.textContent=parseInt(countEl.textContent)+(liked?1:-1);
      }
    });
  });
}

function revealCards(container){
  const obs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target);}});},{threshold:0.1});
  container.querySelectorAll('.reveal').forEach(el=>obs.observe(el));
}

async function loadHome(){
  const feed=document.getElementById('feed-list');if(!feed)return;
  feed.innerHTML=Array(3).fill(0).map(()=>`<div class="post-card"><div class="post-card__header"><div class="skeleton skeleton-avatar"></div><div style="flex:1"><div class="skeleton skeleton-text" style="width:40%"></div><div class="skeleton skeleton-text" style="width:25%"></div></div></div><div class="skeleton skeleton-heading"></div><div class="skeleton skeleton-text"></div><div class="skeleton skeleton-text" style="width:60%"></div></div>`).join('');
  const{data,error}=await PostAPI.getFeed();
  const posts=(!error&&data?.posts?.length)?data.posts:DEMO_POSTS;
  feed.innerHTML=posts.map(p=>renderPostCard(p)).join('');
  attachLikeHandlers(feed);revealCards(feed);
}

async function loadProfile(){
  const container=document.getElementById('profile-container');if(!container)return;
  const handle=window.__KONGGER_CONFIG?.currentHandle??'kongger_demo';
  const{data:profile,error}=await ProfileAPI.getByHandle(handle);
  if(error||!profile){
    container.innerHTML=`<div class="card" style="text-align:center;padding:var(--space-16)">
      <div class="profile-cover" style="margin-bottom:var(--space-6)"><img src="https://picsum.photos/seed/kongger-cover/1200/300" alt="Cover" width="1200" height="300" loading="lazy"></div>
      <img class="profile-avatar" style="margin:0 auto var(--space-4)" src="https://picsum.photos/seed/kongger_demo/176/176" alt="Demo" width="88" height="88">
      <div class="profile-name">KONGGER Demo</div>
      <div class="profile-handle">@kongger_demo</div>
      <div class="profile-bio" style="margin-top:var(--space-3)">歡迎來到 KONGGER！連接你的 PostgreSQL 後端後，這裡會顯示真實的個人檔案。</div>
      <div class="profile-stats" style="justify-content:center">
        <div class="profile-stat"><div class="profile-stat__num" id="visitor-count">128</div><div class="profile-stat__label">今日訪客</div></div>
        <div class="profile-stat"><div class="profile-stat__num">30</div><div class="profile-stat__label">鄰居上限</div></div>
      </div>
      <div style="margin-top:var(--space-6)"><button class="btn btn-primary" onclick="openModal('modal-neighbour')">+ 加鄰居</button></div>
    </div>`;
    const vcEl=document.getElementById('visitor-count');if(vcEl)animateNumber(vcEl,0,128,1000);
    return;
  }
  ProfileAPI.logVisit(profile.id);
  container.innerHTML=`<div class="profile-header">
    <div class="profile-cover"><img src="${profile.cover_url??'https://picsum.photos/seed/kongger-cover/1200/300'}" alt="Cover" width="1200" height="300" loading="lazy"></div>
    <div class="profile-info">
      <img class="profile-avatar" src="${profile.avatar_url??'https://picsum.photos/seed/'+handle+'/176/176'}" alt="${profile.display_name}" width="88" height="88" loading="lazy">
      <div><div class="profile-name">${profile.display_name}</div><div class="profile-handle">@${profile.handle}</div>
        <div class="profile-bio">${profile.bio??''}</div>
        <div class="profile-stats"><div class="profile-stat"><div class="profile-stat__num" id="visitor-count">—</div><div class="profile-stat__label">今日訪客</div></div></div>
      </div>
      <div style="margin-left:auto"><button class="btn btn-primary btn-sm" onclick="openModal('modal-neighbour')">+ 加鄰居</button></div>
    </div>
  </div>
  ${profile.music_url?`<div class="music-widget reveal" style="margin-bottom:var(--space-6)"><div class="music-album playing">🎵</div><div class="music-info"><div class="music-title">${profile.music_title??'Now Playing'}</div><div class="music-artist">${profile.music_artist??''}</div></div><div class="music-eq playing"><span></span><span></span><span></span></div></div>`:''}
  <div id="profile-posts"></div>`;
  const{data:vd}=await ProfileAPI.getVisitors(profile.id,'today');
  const vcEl=document.getElementById('visitor-count');if(vcEl&&vd?.count!=null)animateNumber(vcEl,0,vd.count,800);
  const{data:pd}=await PostAPI.listByAuthor(profile.id);
  const postsEl=document.getElementById('profile-posts');
  if(postsEl){const posts=pd?.posts??[];postsEl.innerHTML=posts.length?posts.map(p=>renderPostCard(p)).join(''):`<div style="text-align:center;padding:var(--space-12);color:var(--color-text-muted)"><div style="font-size:2.5em">📖</div><p>No posts yet</p></div>`;attachLikeHandlers(postsEl);}
  revealCards(container);
}

function loadAI(){
  revealCards(document.getElementById('page-ai'));
}

document.addEventListener('DOMContentLoaded',()=>{
  initTheme();initModals();initParticles();initRouter(routes);

  // Waitlist form
  document.getElementById('waitlist-form')?.addEventListener('submit',async e=>{
    e.preventDefault();const btn=e.target.querySelector('button[type="submit"]');
    const email=e.target.querySelector('[name="email"]')?.value;
    const name=e.target.querySelector('[name="name"]')?.value;
    btn.classList.add('loading');
    const{error}=await WaitlistAPI.join(email,name,'');
    btn.classList.remove('loading');
    if(error){showToast(error==='Email already registered'?'已登記過了！🎉':error,'error');}
    else{showToast('成功登記！等待邀請 🎊','success');e.target.reset();}
  });

  // Post form
  const postForm=document.getElementById('post-form');
  if(postForm){
    const textarea=postForm.querySelector('textarea');
    const charCount=postForm.querySelector('.char-count');
    textarea?.addEventListener('input',()=>{const l=textarea.value.length;if(charCount){charCount.textContent=`${l}/500`;charCount.className='char-count'+(l>450?' danger':l>350?' warn':'');}});
    postForm.addEventListener('submit',async e=>{
      e.preventDefault();const btn=e.target.querySelector('button[type="submit"]');
      const content=textarea?.value.trim();
      const mood=postForm.querySelector('.mood-btn.selected')?.dataset.mood??'everyday';
      if(!content){showToast('請寫一些內容！','info');return;}
      btn.classList.add('loading');
      const{error}=await PostAPI.create({content,mood,visibility:'neighbors'});
      btn.classList.remove('loading');
      if(error){showToast(error,'error');}
      else{showToast('日記已發佈！✨','success');postForm.reset();loadHome();document.getElementById('modal-compose')?.classList.remove('open');document.body.style.overflow='';}
    });
  }

  // Mood buttons
  document.querySelectorAll('.mood-btn').forEach(b=>{b.addEventListener('click',()=>{document.querySelectorAll('.mood-btn').forEach(x=>x.classList.remove('selected'));b.classList.add('selected');});});

  // Auth form
  document.getElementById('auth-form')?.addEventListener('submit',async e=>{
    e.preventDefault();const btn=e.target.querySelector('button[type="submit"]');
    const email=e.target.querySelector('[name="email"]')?.value||e.target.querySelector('#auth-email')?.value;
    const pw=e.target.querySelector('#auth-password')?.value;
    btn.classList.add('loading');
    const{error}=await AuthAPI.login(email,pw);
    btn.classList.remove('loading');
    if(error){showToast(error,'error');}
    else{showToast('登入成功！👋','success');document.getElementById('modal-auth')?.classList.remove('open');document.body.style.overflow='';}
  });

  // Input validation debounce 500ms
  document.querySelectorAll('.input[required]').forEach(inp=>{
    let t;inp.addEventListener('input',()=>{clearTimeout(t);t=setTimeout(()=>{const err=inp.parentElement?.querySelector('.input-error');if(!inp.value.trim()){inp.classList.add('error');if(err)err.textContent='此欄位為必填';}else{inp.classList.remove('error');if(err)err.textContent='';}},500);});
  });
});
