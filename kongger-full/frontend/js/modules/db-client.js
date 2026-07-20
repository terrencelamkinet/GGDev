const API_BASE=window.__KONGGER_CONFIG?.apiBase??'/api/v1';
const TTL={profile:60000,posts:30000,feed:20000,pages:120000,notif:10000};
const _cache=new Map();
function cacheGet(k){const e=_cache.get(k);if(!e)return null;if(Date.now()>e.x){_cache.delete(k);return null;}return e.v}
function cacheSet(k,v,t){_cache.set(k,{v,x:Date.now()+t})}
function cacheDel(p){for(const k of _cache.keys())if(k.startsWith(p))_cache.delete(k)}
const _wq=new Map();
function queueWrite(k,fn,ms=500){return new Promise(r=>{if(_wq.has(k))clearTimeout(_wq.get(k));const t=setTimeout(async()=>{_wq.delete(k);r(await fn());},ms);_wq.set(k,t)})}
async function api(method,path,body=null){
  const token=window.__KONGGER_CONFIG?.authToken;
  try{const res=await fetch(API_BASE+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})}, ...(body?{body:JSON.stringify(body)}:{})});
    const json=await res.json();if(!res.ok)return{data:null,error:json.error??'Request failed',status:res.status};return{data:json,error:null,status:res.status};}
  catch(e){return{data:null,error:e.message,status:0}}}

export const ProfileAPI={
  async getByHandle(h){const k=`profile:${h}`;const c=cacheGet(k);if(c)return{data:c,error:null};const r=await api('GET',`/profiles/${h}`);if(!r.error)cacheSet(k,r.data,TTL.profile);return r},
  async getMe(){const k='profile:me';const c=cacheGet(k);if(c)return{data:c,error:null};const r=await api('GET','/profiles/me');if(!r.error)cacheSet(k,r.data,TTL.profile);return r},
  async update(p){cacheDel('profile:me');return queueWrite('profile:update',()=>api('PATCH','/profiles/me',p),500)},
  logVisit(id){api('POST',`/profiles/${id}/visit`)},
  async getVisitors(id,period='today'){return api('GET',`/profiles/${id}/visitors?period=${period}`)},
};
export const AuthAPI={
  async register(email,password,display_name,handle){const r=await api('POST','/auth/register',{email,password,display_name,handle});if(!r.error&&r.data?.token){window.__KONGGER_CONFIG={...window.__KONGGER_CONFIG,authToken:r.data.token};}return r},
  async login(email,password){const r=await api('POST','/auth/login',{email,password});if(!r.error&&r.data?.token){window.__KONGGER_CONFIG={...window.__KONGGER_CONFIG,authToken:r.data.token};}return r},
  logout(){window.__KONGGER_CONFIG={...window.__KONGGER_CONFIG,authToken:null};cacheDel('')},
};
export const PostAPI={
  async getFeed(cursor=null,limit=20){const k=`feed:${cursor}`;const c=cacheGet(k);if(c)return{data:c,error:null};const p=new URLSearchParams({limit});if(cursor)p.set('cursor',cursor);const r=await api('GET',`/posts/feed?${p}`);if(!r.error)cacheSet(k,r.data,TTL.feed);return r},
  async listByAuthor(aid,cursor=null,limit=20){const k=`posts:${aid}:${cursor}`;const c=cacheGet(k);if(c)return{data:c,error:null};const p=new URLSearchParams({author:aid,limit});if(cursor)p.set('cursor',cursor);const r=await api('GET',`/posts?${p}`);if(!r.error)cacheSet(k,r.data,TTL.posts);return r},
  async create(payload){cacheDel('posts:');cacheDel('feed:');return api('POST','/posts',payload)},
  async update(id,payload){cacheDel(`post:${id}`);cacheDel('posts:');return api('PATCH',`/posts/${id}`,payload)},
  async delete(id){cacheDel(`post:${id}`);cacheDel('posts:');cacheDel('feed:');return api('DELETE',`/posts/${id}`)},
  async toggleLike(id,liked){cacheDel(`post:${id}`);return api(liked?'DELETE':'POST',`/posts/${id}/like`)},
};
export const PageAPI={
  async listByOwner(oid){const k=`pages:${oid}`;const c=cacheGet(k);if(c)return{data:c,error:null};const r=await api('GET',`/pages?owner=${oid}`);if(!r.error)cacheSet(k,r.data,TTL.pages);return r},
  async getBySlug(oid,slug){const k=`page:${oid}:${slug}`;const c=cacheGet(k);if(c)return{data:c,error:null};const r=await api('GET',`/pages/${oid}/${slug}`);if(!r.error)cacheSet(k,r.data,TTL.pages);return r},
  async create(p){cacheDel('pages:');return api('POST','/pages',p)},
  async updateLayout(id,layout){cacheDel('page:');return queueWrite(`page:layout:${id}`,()=>api('PATCH',`/pages/${id}/layout`,{layout_json:layout}),800)},
  async updateSections(id,sections){cacheDel('page:');return queueWrite(`page:sections:${id}`,()=>api('PATCH',`/pages/${id}/sections`,{sections}),800)},
  async delete(id){cacheDel('pages:');return api('DELETE',`/pages/${id}`)},
};
export const NeighbourAPI={
  async list(){const c=cacheGet('nb:list');if(c)return{data:c,error:null};const r=await api('GET','/neighbours');if(!r.error)cacheSet('nb:list',r.data,30000);return r},
  async send(uid){cacheDel('nb:');return api('POST',`/neighbours/${uid}`)},
  async accept(id){cacheDel('nb:');return api('PATCH',`/neighbours/${id}/accept`)},
  async remove(uid){cacheDel('nb:');return api('DELETE',`/neighbours/${uid}`)},
};
export const NotifAPI={
  async list(unread=false){const k=`notif:${unread}`;const c=cacheGet(k);if(c)return{data:c,error:null};const r=await api('GET',`/notifications?unread=${unread}`);if(!r.error)cacheSet(k,r.data,TTL.notif);return r},
  async markAllRead(){cacheDel('notif:');return api('PATCH','/notifications/read-all')},
};
export const WaitlistAPI={
  async join(email,name,message){return api('POST','/waitlist',{email,name,message})},
};
export default{Auth:AuthAPI,Profile:ProfileAPI,Post:PostAPI,Page:PageAPI,Neighbour:NeighbourAPI,Notif:NotifAPI,Waitlist:WaitlistAPI};