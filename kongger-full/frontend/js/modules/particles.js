export function initParticles(){
  const canvas=document.getElementById('particles-canvas');if(!canvas)return;
  const ctx=canvas.getContext('2d');let W,H,pts=[];
  function resize(){W=canvas.width=innerWidth;H=canvas.height=innerHeight}
  resize();window.addEventListener('resize',resize);
  function mkPt(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*2+.5,vx:(Math.random()-.5)*.3,vy:(Math.random()-.5)*.3,a:Math.random()}}
  for(let i=0;i<60;i++)pts.push(mkPt());
  const isDark=()=>document.documentElement.getAttribute('data-theme')==='dark';
  function draw(){ctx.clearRect(0,0,W,H);const col=isDark()?'255,200,200':'180,80,120';
    for(const p of pts){ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=`rgba(${col},${p.a*.4})`;ctx.fill();p.x+=p.vx;p.y+=p.vy;p.a+=.004;if(p.a>1||p.x<0||p.x>W||p.y<0||p.y>H)Object.assign(p,mkPt());}
    requestAnimationFrame(draw);}
  draw();
}