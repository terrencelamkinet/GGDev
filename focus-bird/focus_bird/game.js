/* ================================================================
   FOCUS BIRD PRO v3 — game.js
   Canvas engine: bird, food, distractors, particles, backgrounds
   10 layers x 10 levels | age 1-40 | expert-designed distractors
   Research basis: UCSD ONTRAC (2016), Neuroelectrics NF Design (2014),
   PMC Executive Attention Training (2025), AAP Level 1 NF guidelines
   ================================================================ */
'use strict';

/* ── Global state ─────────────────────────────────────────── */
const G = {
  age:8, focus:50, threshold:40, space:false, extMode:false,
  running:false, stage:1, level:1, score:0, collected:0, goal:10,
  timer:0, combo:0, comboTimer:0, bestFocus:0,
};

/* ── Stage definitions ────────────────────────────────────── */
const STAGES = [
  {zh:'蘋果樂園',   sky1:'#4fc3f7', sky2:'#b3e5fc', gnd:'#388e3c', items:['apple']},
  {zh:'粟米田野',   sky1:'#ffd54f', sky2:'#fff9c4', gnd:'#689f38', items:['corn']},
  {zh:'薯條王國',   sky1:'#ff8a65', sky2:'#ffccbc', gnd:'#795548', items:['fries']},
  {zh:'可樂世界',   sky1:'#42a5f5', sky2:'#90caf9', gnd:'#1565c0', items:['cola']},
  {zh:'甜品花園',   sky1:'#f48fb1', sky2:'#fce4ec', gnd:'#ad1457', items:['cake']},
  {zh:'朱古力森林', sky1:'#8d6e63', sky2:'#d7ccc8', gnd:'#4e342e', items:['choco']},
  {zh:'雪糕山',     sky1:'#b3e5fc', sky2:'#e1f5fe', gnd:'#80deea', items:['icecream']},
  {zh:'蛋糕城堡',   sky1:'#ce93d8', sky2:'#f3e5f5', gnd:'#6a1b9a', items:['bigcake']},
  {zh:'雙重盛宴',   sky1:'#80cbc4', sky2:'#e0f2f1', gnd:'#00695c', items:['apple','fries']},
  {zh:'終極大混合', sky1:'#7e57c2', sky2:'#ede7f6', gnd:'#1a237e',
    items:['apple','corn','fries','cola','cake','choco','icecream','bigcake']},
];

/* ── Age profile ──────────────────────────────────────────── */
function ageProfile(age) {
  if (age<=2)  return {band:'嬰幼兒', session:5,  goalBase:5,  spd:.9,  grav:.016,grace:18,response:.08, threshold:22};
  if (age<=4)  return {band:'幼童',   session:8,  goalBase:7,  spd:1.0, grav:.019,grace:16,response:.10, threshold:26};
  if (age<=6)  return {band:'學前',   session:10, goalBase:9,  spd:1.15,grav:.022,grace:14,response:.12, threshold:30};
  if (age<=8)  return {band:'小學初', session:13, goalBase:11, spd:1.3, grav:.026,grace:12,response:.14, threshold:35};
  if (age<=10) return {band:'小學中', session:16, goalBase:13, spd:1.45,grav:.030,grace:10,response:.16, threshold:40};
  if (age<=13) return {band:'小學高', session:18, goalBase:15, spd:1.6, grav:.033,grace:9, response:.17, threshold:44};
  if (age<=17) return {band:'青少年', session:22, goalBase:17, spd:1.75,grav:.036,grace:8, response:.18, threshold:50};
  if (age<=25) return {band:'青年',   session:25, goalBase:18, spd:1.9, grav:.040,grace:7, response:.19, threshold:55};
  if (age<=35) return {band:'成人',   session:25, goalBase:16, spd:1.8, grav:.038,grace:8, response:.18, threshold:52};
  return              {band:'壯年',   session:22, goalBase:14, spd:1.6, grav:.034,grace:10,response:.16, threshold:48};
}

/* ── Canvas setup ─────────────────────────────────────────── */
const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
let W = canvas.width  = window.innerWidth;
let H = canvas.height = window.innerHeight;
window.addEventListener('resize', () => {
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;
});

/* ── Drawing helpers ──────────────────────────────────────── */
function poly(c,fill,pts){
  c.fillStyle=fill; c.beginPath(); c.moveTo(pts[0][0],pts[0][1]);
  for(let i=1;i<pts.length;i++) c.lineTo(pts[i][0],pts[i][1]);
  c.closePath(); c.fill();
}
function circ(c,x,y,r,f){ c.fillStyle=f; c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.fill(); }
function rect(c,x,y,w,h,f,r=0){
  c.fillStyle=f;
  if(r>0){ c.beginPath(); c.roundRect(x,y,w,h,r); c.fill(); }
  else c.fillRect(x,y,w,h);
}

/* ── Bird ─────────────────────────────────────────────────── */
const Bird = {
  x:0, y:0, vy:0, wingPhase:0,
  init(){ this.x=W*.22; this.y=H*.42; this.vy=0; },
  update(focusLvl, prof){
    const thr=G.threshold;
    this.wingPhase += .1;
    if(G.extMode && focusLvl >= thr){
      const pull = G.extMode
        ? prof.grav * 0.9  /* fixed descent when focused — half speed */
        : prof.grav * 1.5;  /* space descent — half speed */
      this.vy += pull;
    } else {
      this.vy -= G.extMode ? prof.grav * 0.6 : prof.grav * 1.25;  /* fixed rise when not focused — half speed */
    }
    this.vy = Math.max(-2.25, Math.min(3, this.vy));
    // GROUND_Y same as food level: H-54-FOOD_SIZE
    const GROUND_Y = H-54-FOOD_SIZE;
    if(this.y > GROUND_Y){
      this.y = GROUND_Y;
      this.vy *= -.2; // bounce
    }
    this.y  = Math.max(32, this.y+this.vy);
  },
  draw(nearFoodY){
    const cx=this.x, cy=this.y;
    const wu=Math.sin(this.wingPhase)*18;
    const tilt=Math.max(-.28,Math.min(.28,this.vy*.055));
    ctx.save(); ctx.translate(cx,cy); ctx.rotate(tilt);
    if(G.focus>68){ ctx.shadowColor=STAGES[G.stage-1].sky1; ctx.shadowBlur=22; }
    else if(G.focus<22){ ctx.shadowColor='#ff4444'; ctx.shadowBlur=18; }
    poly(ctx,'#0d47a1',[[-62,0],[-86,-7],[-68,-22],[-48,-5]]);
    poly(ctx,'#1a4fa8',[[-12,2],[-58,-24+wu],[-48,-9+wu],[-6,14]]);
    poly(ctx,'#3a7bd5',[[0,-18],[48,-22],[56,2],[38,28],[0,26],[-20,6]]);
    poly(ctx,'#5b8de8',[[8,-6],[40,-8],[44,10],[30,22],[4,20]]);
    rect(ctx,14,22,24,8,'#ffe066',3);
    rect(ctx,12,29,28,3,'#ffb300',2);
    poly(ctx,'#4f8cff',[[38,-24],[76,-30],[80,-6],[58,2],[36,-2]]);
    poly(ctx,'rgba(255,255,255,.42)',[[46,-22],[64,-26],[66,-14],[50,-12]]);
    circ(ctx,58,-16,10,'#fff');
    const ey = nearFoodY ? Math.max(-8,Math.min(8,(nearFoodY-cy)*.06)) : 0;
    circ(ctx,60,-14+ey,5.5,'#1a237e');
    circ(ctx,61.5,-15+ey,1.8,'#fff');
    const brow = G.focus>62 ? -29 : G.focus<30 ? -22 : -25;
    ctx.strokeStyle='#1a237e'; ctx.lineWidth=2.2; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(50,brow); ctx.lineTo(67,brow-2); ctx.stroke();
    poly(ctx,'#fb8500',[[70,-14],[96,-8],[70,-2]]);
    poly(ctx,'#ffcc02',[[70,-14],[88,-9],[70,-8]]);
    ctx.shadowBlur=0; ctx.restore();
  }
};

/* ── Food drawing ─────────────────────────────────────────── */
const FOOD_COLS = {
  apple:'#c62828',corn:'#f9a825',fries:'#e65100',cola:'#1565c0',
  cake:'#ad1457',choco:'#4e342e',icecream:'#b2ebf2',bigcake:'#6a1b9a'
};
const FOOD_SIZE=26;

function drawFood(kind,x,y,r=FOOD_SIZE){
  ctx.save(); ctx.translate(x,y);
  const fns={apple:_apple,corn:_corn,fries:_fries,cola:_cola,
    cake:_cake,choco:_choco,icecream:_icecream,bigcake:_bigcake};
  (fns[kind]||_apple)(ctx,r);
  ctx.restore();
}
function _apple(c,r){
  circ(c,0,r*.2,r*.78,'#c62828');
  circ(c,-r*.18,r*.0,r*.28,'rgba(255,255,255,.2)');
  rect(c,-r*.06,-r*.85,r*.14,r*.58,'#2e7d32',2);
  c.strokeStyle='#a00000';c.lineWidth=1.5;
  c.beginPath();c.moveTo(-r*.12,r*.3);c.lineTo(r*.12,r*.1);c.stroke();
}
function _corn(c,r){
  poly(c,'#f9a825',[[-r*.4,-r*1.1],[r*.4,-r*1.1],[r*.5,r*.7],[-r*.5,r*.7]]);
  for(let col=0;col<3;col++)for(let row=0;row<5;row++)
    circ(c,-r*.22+col*r*.22,-r*.8+row*r*.35,r*.1,'#fdd835');
  poly(c,'#388e3c',[[-r*.5,r*.7],[-r*.1,r*.2],[-r*.5,r*.4]]);
  poly(c,'#388e3c',[[r*.5,r*.7],[r*.1,r*.2],[r*.5,r*.4]]);
}
function _fries(c,r){
  rect(c,-r*.45,r*.2,r*.9,r*.65,'#e65100',4);
  rect(c,-r*.4,r*.26,r*.8,r*.52,'#ff6f00',3);
  [-.28,-.12,.04,.2,.34].forEach(ox=>{
    rect(c,r*ox,-r*.5,r*.1,r*.75,'#ffd54f',2);
    rect(c,r*ox+r*.02,-r*.55,r*.06,r*.08,'#ff8f00',2);
  });
}
function _cola(c,r){
  rect(c,-r*.32,-r*.7,r*.64,r*1.55,'#1565c0',r*.22);
  rect(c,-r*.28,-r*.64,r*.56,r*1.42,'#1976d2',r*.18);
  rect(c,-r*.4,-r*.85,r*.8,r*.24,'#9e9e9e',r*.08);
  rect(c,-r*.24,-r*.5,r*.24,r*.24,'rgba(255,255,255,.3)',r*.05);
  circ(c,-r*.18,r*.1,r*.08,'rgba(255,255,255,.2)');
}
function _cake(c,r){
  rect(c,-r*.55,r*.05,r*1.1,r*.7,'#e91e63',r*.12);
  rect(c,-r*.45,r*.12,r*.9,r*.5,'#f48fb1',r*.09);
  rect(c,-r*.4,-r*.28,r*.8,r*.38,'#f06292',r*.1);
  rect(c,-r*.3,-r*.32,r*.6,r*.1,'rgba(255,255,255,.4)',r*.05);
  poly(c,'#ffd54f',[[-r*.08,-r*.62],[-r*.04,-r*.35],[r*.04,-r*.35],[r*.08,-r*.62]]);
  circ(c,0,-r*.65,r*.1,'#ff7043');
}
function _choco(c,r){
  rect(c,-r*.55,-r*.7,r*1.1,r*1.4,'#4e342e',r*.14);
  [[-.32,-.5],[0,-.5],[.32,-.5],[-.32,0],[0,0],[.32,0],[-.32,.5],[0,.5],[.32,.5]].forEach(([gx,gy])=>{
    c.fillStyle='#3e2723';c.beginPath();c.roundRect(r*gx-r*.1,r*gy-r*.16,r*.2,r*.3,2);c.fill();
  });
  circ(c,-r*.2,-r*.55,r*.12,'rgba(255,255,255,.2)');
}
function _icecream(c,r){
  poly(c,'#a1887f',[[-r*.35,r*.05],[r*.35,r*.05],[r*.15,r*.85],[-r*.15,r*.85]]);
  poly(c,'#bcaaa4',[[-r*.28,r*.12],[r*.28,r*.12],[r*.1,r*.72],[-r*.1,r*.72]]);
  circ(c,0,-r*.28,r*.52,'#e3f2fd');
  circ(c,-r*.14,-r*.42,r*.28,'#b3e5fc');
  circ(c,r*.14,-r*.38,r*.22,'#e3f2fd');
  circ(c,0,-r*.62,r*.2,'#b3e5fc');
  for(let i=0;i<6;i++) circ(c,Math.cos(i*Math.PI/3)*r*.25,Math.sin(i*Math.PI/3)*r*.25-r*.28,r*.06,'#ff8a65');
}
function _bigcake(c,r){
  [[r*.7,'#6a1b9a'],[r*.5,'#7b1fa2'],[r*.3,'#8e24aa']].forEach(([hr,col],i)=>{
    rect(c,-r*(1-.18*i),-r*.85+i*r*.5,r*(2-.36*i),hr,col,r*.1);
  });
  rect(c,-r*.12,-r*1.3,r*.1,r*.5,'#ff7043',2);
  circ(c,-r*.07,-r*1.35,r*.1,'#ffd54f');
  for(let i=0;i<8;i++) circ(c,Math.cos(i*Math.PI/4)*r*.55,-r*.2+Math.sin(i*Math.PI/4)*r*.2,r*.06,'#ffd54f');
}

/* ── Particles ────────────────────────────────────────────── */
const particles=[];
function spawnParticles(x,y,color){
  for(let i=0;i<14;i++){
    const a=Math.random()*Math.PI*2, s=1.5+Math.random()*4;
    particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-2,life:1,color,r:3+Math.random()*4,g:.15});
  }
}
function updateParticles(){
  for(let i=particles.length-1;i>=0;i--){
    const p=particles[i];
    p.x+=p.vx; p.y+=p.vy; p.vy+=p.g; p.life-=.028;
    ctx.globalAlpha=Math.max(0,p.life);
    circ(ctx,p.x,p.y,p.r,p.color);
    ctx.globalAlpha=1;
    if(p.life<=0) particles.splice(i,1);
  }
}

/* ── Floating labels ──────────────────────────────────────── */
const floats=[];
function spawnFloat(x,y,txt,col='#ffd166'){
  floats.push({x,y:y-10,vy:-1.6,life:1.2,txt,col,sz:20+Math.random()*8});
}
function updateFloats(){
  for(let i=floats.length-1;i>=0;i--){
    const f=floats[i]; f.y+=f.vy; f.life-=.022;
    if(f.life<=0){floats.splice(i,1);continue;}
    ctx.save(); ctx.globalAlpha=f.life;
    ctx.font=`900 ${f.sz}px 'Baloo 2',sans-serif`;
    ctx.fillStyle=f.col; ctx.textAlign='center';
    ctx.fillText(f.txt,f.x,f.y);
    ctx.restore();
  }
}

/* ================================================================
   DISTRACTOR SYSTEM
   Research basis:
   - UCSD ONTRAC (2016): adaptive distractor suppression training —
     distractor similarity & frequency adapted after each trial
   - Neuroelectrics NF Design (2014): game distractors must not
     exceed 30% of stimulus area; increase only after 3+ success runs
   - PMC Executive Attention (2025): "inhibitory control" trained via
     sudden irrelevant stimuli requiring active suppression
   - AAP ADHD NF guidelines: distractors activate top-down attention
     control, reinforced when child maintains focus despite distraction
   Progressive stages:
     Stage 1:    NO distractors (pure focus building)
     Stage 2-3:  Visual only — slow moving shapes crossing sky
     Stage 4-5:  Visual + occasional sound burst (low freq)
     Stage 6-7:  Visual + sound + brief screen flash
     Stage 8-9:  All above + fake food (decoy items that vanish)
     Stage 10:   Maximum distraction — all types at higher frequency
   Within each stage, level 1-10 scales frequency and intensity.
   ================================================================ */

const distractors = [];
let distractorTimer = 0;
let flashAlpha = 0;  /* screen flash overlay */

/* Distractor config per stage (expert-calibrated) */
function distractorConfig(stage, level) {
  if (stage < 2) return null;  /* Layer 1: NO distractors */
  const base = stage - 2;      /* 0-8 */
  const lvlScale = (level - 1) / 9;   /* 0-1 */
  return {
    /* interval in frames: starts slow, gets faster */
    interval: Math.max(80, 340 - base*28 - lvlScale*60),
    hasSound: stage >= 4,
    hasFlash: stage >= 6,
    hasDecoy: stage >= 8,
    intensity: Math.min(1, base/8 + lvlScale*.3),
    types: stage<=3 ? ['shape'] :
           stage<=5 ? ['shape','burst'] :
           stage<=7 ? ['shape','burst','flash'] :
                      ['shape','burst','flash','decoy'],
  };
}

/* Distractor shape types */
const DISTRACTOR_SHAPES = ['star','circle','zigzag','arrow','spiral'];

function spawnDistractor(stage, level) {
  const cfg = distractorConfig(stage, level);
  if (!cfg) return;
  const t = cfg.types[Math.floor(Math.random()*cfg.types.length)];
  const fromRight = Math.random() > .3;
  const spd = (2 + cfg.intensity*3.5) * (fromRight ? -1 : 1);
  const sx   = fromRight ? W+60 : -60;
  const sy   = 40 + Math.random()*(H*.55);
  /* Color — bright but not food-colored, to avoid confusion */
  const distCols=['#ff6b35','#f7c59f','#efefd0','#004e89','#1a936f','#c77dff'];
  const col = distCols[Math.floor(Math.random()*distCols.length)];
  distractors.push({
    x:sx, y:sy, vx:spd, vy:(Math.random()-.5)*1.4,
    shape:DISTRACTOR_SHAPES[Math.floor(Math.random()*DISTRACTOR_SHAPES.length)],
    r:18+Math.random()*18*cfg.intensity,
    life:1, col, type:t, ang:0, angv:(Math.random()-.5)*.08,
    isDecoy: t==='decoy',
  });
  /* Trigger side effects */
  if (t==='burst' || t==='flash' || t==='decoy') {
    Audio.distract(cfg.intensity);
  }
  if (t==='flash') {
    flashAlpha = 0.28 + cfg.intensity*.22;
  }
}

function updateDistractors(stage, level) {
  const cfg = distractorConfig(stage, level);
  if (!cfg) return;
  distractorTimer++;
  if (distractorTimer >= cfg.interval) {
    distractorTimer = 0;
    spawnDistractor(stage, level);
  }
  /* Flash fade */
  if (flashAlpha > 0) {
    ctx.fillStyle = `rgba(255,255,255,${flashAlpha})`;
    ctx.fillRect(0,0,W,H);
    flashAlpha = Math.max(0, flashAlpha - .025);
  }
  for (let i=distractors.length-1; i>=0; i--) {
    const d = distractors[i];
    d.x += d.vx; d.y += d.vy; d.ang += d.angv;
    /* Decoys vanish quickly to avoid rewarding collision */
    if (d.isDecoy) d.life -= .018;
    /* Remove when off screen */
    if (d.x<-80||d.x>W+80||d.y<-80||d.y>H+80||d.life<=0) {
      distractors.splice(i,1); continue;
    }
    ctx.save(); ctx.translate(d.x,d.y); ctx.rotate(d.ang);
    ctx.globalAlpha = d.isDecoy ? d.life*0.7 : 0.82;
    drawDistractorShape(ctx, d.shape, d.r, d.col);
    ctx.globalAlpha = 1; ctx.restore();
  }
}

function drawDistractorShape(c, shape, r, col) {
  c.fillStyle = col;
  c.strokeStyle = 'rgba(255,255,255,.5)';
  c.lineWidth = 1.5;
  switch(shape) {
    case 'star': {
      c.beginPath();
      for(let i=0;i<10;i++){
        const a=i*Math.PI/5-Math.PI/2, rad=i%2===0?r:r*.42;
        i===0 ? c.moveTo(Math.cos(a)*rad,Math.sin(a)*rad)
              : c.lineTo(Math.cos(a)*rad,Math.sin(a)*rad);
      }
      c.closePath(); c.fill(); c.stroke(); break;
    }
    case 'circle': {
      c.beginPath(); c.arc(0,0,r,0,Math.PI*2); c.fill(); c.stroke(); break;
    }
    case 'zigzag': {
      c.beginPath(); c.moveTo(-r,0);
      for(let i=1;i<=5;i++) c.lineTo(-r+i*(r*.4),(i%2===0?-1:1)*r*.5);
      c.stroke(); break;
    }
    case 'arrow': {
      poly(c,col,[[-r*.1,-r*.5],[r*.5,0],[-r*.1,r*.5],[-r*.1,r*.18],[-r*.8,r*.18],[-r*.8,-r*.18],[-r*.1,-r*.18]]);
      break;
    }
    case 'spiral': {
      c.beginPath();
      for(let a=0;a<Math.PI*3;a+=.18){
        const sr=(a/(Math.PI*3))*r;
        const sx=Math.cos(a)*sr, sy=Math.sin(a)*sr;
        a===0 ? c.moveTo(sx,sy) : c.lineTo(sx,sy);
      }
      c.strokeStyle=col; c.lineWidth=2.5; c.stroke(); break;
    }
  }
}

/* ── Background ───────────────────────────────────────────── */
function drawBG(stage) {
  const st = STAGES[stage-1];
  const grd = ctx.createLinearGradient(0,0,0,H);
  grd.addColorStop(0,st.sky1); grd.addColorStop(.65,st.sky2); grd.addColorStop(1,st.gnd);
  ctx.fillStyle=grd; ctx.fillRect(0,0,W,H);
  /* Clouds */
  const t=Date.now()*.00018;
  ctx.fillStyle='rgba(255,255,255,.17)';
  [[.15,.11,120,42],[.3,.07,190,34],[.55,.14,160,40],[.73,.09,145,36],[.88,.12,175,42]].forEach(([xr,yr,cw,ch],ci)=>{
    const cx=(((xr-t*.3*(ci%2===0?1:.6))%1+1)%1)*W;
    const cy=yr*H;
    ctx.beginPath();ctx.ellipse(cx,cy,cw,ch,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx-cw*.4,cy+ch*.2,cw*.7,ch*.65,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx+cw*.4,cy+ch*.15,cw*.6,ch*.55,0,0,Math.PI*2);ctx.fill();
  });
  /* Rolling hills */
  ctx.fillStyle=st.gnd;
  ctx.beginPath(); ctx.moveTo(0,H*.76);
  for(let x=0;x<=W;x+=4){
    const hy=H*.76+Math.sin(x*.008+Date.now()*.0004)*26+Math.sin(x*.02)*10;
    ctx.lineTo(x,hy);
  }
  ctx.lineTo(W,H); ctx.lineTo(0,H); ctx.closePath(); ctx.fill();
  /* Ground */
  ctx.fillStyle=st.gnd+'bb'; ctx.fillRect(0,H-54,W,54);
  ctx.fillStyle='rgba(255,255,255,.11)'; ctx.fillRect(0,H-54,W,3);
  /* Stage 10 star nebula */
  if(stage===10){
    for(let s=0;s<4;s++){
      const sx=Math.random()*W, sy=Math.random()*H*.65;
      circ(ctx,sx,sy,Math.random()*1.5+.5,`rgba(255,255,255,${.3+Math.random()*.6})`);
    }
    ctx.fillStyle='rgba(100,80,200,.08)';
    ctx.beginPath();ctx.arc(W*.7,H*.3,180,0,Math.PI*2);ctx.fill();
  }
}

/* ── HUD ──────────────────────────────────────────────────── */
function updateHUD(){
  const mm=String(Math.floor(G.timer/60)).padStart(2,'0');
  const ss=String(G.timer%60).padStart(2,'0');
  const fp=Math.round(G.focus);
  document.getElementById('b-stage').textContent=`第${G.stage}層`;
  document.getElementById('b-level').textContent=`第${G.level}關`;
  document.getElementById('b-score').textContent=`${G.score}分`;
  document.getElementById('b-goal').textContent=`${G.collected}/${G.goal}`;
  document.getElementById('b-time').textContent=`${mm}:${ss}`;
  const fill=document.getElementById('fbar-fill');
  fill.style.width=`${fp}%`;
  fill.style.background=fp<30?'#ff6b6b':fp<60?'linear-gradient(90deg,#ffd166,#ff8b6b)':'linear-gradient(90deg,#74d680,#4f8cff)';
  document.getElementById('fpct').textContent=`${fp}%`;
  const cb=document.getElementById('b-combo');
  if(G.combo>=2){cb.style.display='';cb.textContent=`連擊x${G.combo}`;}
  else cb.style.display='none';
}

/* ── Main game ────────────────────────────────────────────── */
let foods=[], foodTimer=0, gameTick=0, timerTick=0;

function startGame(stage,level){
  G.stage=stage; G.level=level;
  G.score=0; G.collected=0; G.combo=0; G.comboTimer=0; G.bestFocus=0;
  const prof=ageProfile(G.age);
  G.goal = prof.goalBase + Math.floor((stage-1)*1.4+(level-1)*.9);
  if(!G.threshold||G.threshold===40) G.threshold=prof.threshold;
  G.running=true;
  foods=[]; distractors.splice(0); distractorTimer=0; flashAlpha=0;
  foodTimer=0; gameTick=0; timerTick=0;
  G.timer = Math.max(30, G.goal*(stage+level)*3);
  Bird.init();
  document.getElementById('ov').classList.add('gone');
  document.getElementById('btnMenu').style.display='';
  Audio.startBGM(stage);
  requestAnimationFrame(loop);
}

function loop(){
  if(!G.running) return;
  gameTick++;
  if (typeof WS !== 'undefined') WS.checkStale();
  const prof=ageProfile(G.age);
  /* Focus update — only from WS data (extMode), never self-decay */
  if(!G.extMode){
    /* Hold steady — no keyboard fallback focus change */
  }
  G.bestFocus=Math.max(G.bestFocus,G.focus);
  /* Timer */
  timerTick++;
  if(timerTick>=60){timerTick=0; G.timer=Math.max(0,G.timer-1);}
  /* Draw */
  ctx.clearRect(0,0,W,H);
  drawBG(G.stage);
  /* Distractors (before food/bird so they appear behind) */
  updateDistractors(G.stage, G.level);
  /* Food — random spacing, further apart */
  const st=STAGES[G.stage-1];
  const baseInt=Math.max(100,220-G.stage*10-(G.level-1)*5);
  const spawnInt=(baseInt+Math.floor(Math.random()*baseInt*1.2))*60/prof.spd/60;  /* 0-120% random */
  foodTimer++;
  if(foodTimer>spawnInt){
    foodTimer=0;
    const kind=st.items[Math.floor(Math.random()*st.items.length)];
    foods.push({
      x:W+FOOD_SIZE, y:H-54-FOOD_SIZE, kind,
      vx:-(1.0+prof.spd*.5+(G.level-1)*.03+G.stage*.03+Math.random()*0.8)
    });
  }
  const nearFoodY=foods.length?foods.reduce((a,b)=>Math.abs(b.x-Bird.x)<Math.abs(a.x-Bird.x)?b:a).y:null;
  for(let i=foods.length-1;i>=0;i--){
    const fd=foods[i];
    fd.x+=fd.vx; 
    if(fd.x<-60){foods.splice(i,1);continue;}
    const dx=fd.x-Bird.x, dy=fd.y-Bird.y;
    if(Math.sqrt(dx*dx+dy*dy)<FOOD_SIZE+30){
      G.collected++;
      G.score+=10+G.combo*5;
      G.comboTimer=62; G.combo++;
      Audio.collectSound(fd.kind, G.combo);
      if(G.combo>=3){
        spawnFloat(fd.x,fd.y,`COMBO x${G.combo}!`,'#ff9800');
      } else {
        spawnFloat(fd.x,fd.y,`+${10+G.combo*5}`,'#ffd166');
      }
      spawnParticles(fd.x,fd.y,FOOD_COLS[fd.kind]||'#ffd166');
      foods.splice(i,1); continue;
    }
    drawFood(fd.kind,fd.x,fd.y,FOOD_SIZE);
  }
  if(G.comboTimer>0)G.comboTimer--; else G.combo=0;
  Bird.update(G.focus,prof);
  Bird.draw(nearFoodY);
  updateParticles();
  updateFloats();
  updateHUD();
  /* update debug panel */
  const dbg = document.getElementById('dbg');
  if (dbg && dbg.style.display !== 'none') {
    const s = WS.stats;
    document.getElementById('dbg-ws').textContent = s.connected ? '✅ connected' : '❌ disconnected';
    document.getElementById('dbg-ws').style.color = s.connected ? '#74d680' : '#ff6b6b';
    document.getElementById('dbg-att').textContent = s.lastAtt;
    document.getElementById('dbg-sig').textContent = s.lastSig;
    document.getElementById('dbg-ext').textContent = G.extMode;
    document.getElementById('dbg-dev').textContent = s.deviceConnected ? '✅' : '❌';
    document.getElementById('dbg-eeg').textContent = s.hasEEG ? '✅' : '❌';
    document.getElementById('dbg-msgs').textContent = s.msgs;
    document.getElementById('dbg-errs').textContent = s.errs;
    /* seconds since last data */
    var since = s.lastMsgAt ? Math.round((Date.now() - s.lastMsgAt)/1000) : '-';
    document.getElementById('dbg-last').textContent = since;
    document.getElementById('dbg-sigv').textContent = s.lastSig;
    /* auto-update ws-status every frame: 🟢=live data 🟡=2-5s stale 🔴=5s+ */
    var wsStatus = document.getElementById('ws-status');
    if (wsStatus) {
      if (s.lastMsgAt && Date.now() - s.lastMsgAt < 2000) wsStatus.textContent = '🟢';
      else if (s.lastMsgAt && Date.now() - s.lastMsgAt < 5000) wsStatus.textContent = '🟡';
      else wsStatus.textContent = '🔴';
    }
    /* device status label — always visible */
    var devLabel = document.getElementById('device-status');
    if (devLabel) {
      if (!s.connected) devLabel.textContent = '离线';
      else if (!s.deviceConnected) devLabel.textContent = 'bridge已連 裝置離線';
      else if (!s.hasEEG) devLabel.textContent = '等待EEG...';
      else devLabel.textContent = '🧠 BrainLink';
      devLabel.style.color = (s.deviceConnected && s.hasEEG) ? '#74d680' : '#ff6b6b';
    }
    /* show last 5 values as log */
    const logEl = document.getElementById('dbg-log');
    if (logEl) {
      logEl.innerHTML = s.log.slice(-5).map(function(entry) {
        var t = new Date(entry.t);
        var time = t.getHours().toString().padStart(2,'0') + ':' + t.getMinutes().toString().padStart(2,'0') + ':' + t.getSeconds().toString().padStart(2,'0');
        return '<div>' + time + ' att=' + entry.att + ' sig=' + entry.sig + ' ' + (entry.hasSig ? '✅' : '❌') + '</div>';
      }).join('');
    }
  }
  if(G.collected>=G.goal){endLevel(true);return;}
  if(G.timer<=0){endLevel(false);return;}
  requestAnimationFrame(loop);
}

function endLevel(win){
  G.running=false; Audio.stopBGM();
  win ? Audio.win() : Audio.lose();
  setTimeout(()=>{
    document.getElementById('ov').classList.remove('gone');
    document.getElementById('btnMenu').style.display='none';
    const ns=win&&G.level===10?Math.min(10,G.stage+1):G.stage;
    const nl=win?(G.level===10?1:G.level+1):G.level;
    const hasDist=G.stage>=2;
    document.getElementById('mc').innerHTML=`
      <div style="text-align:center;padding:clamp(20px,3vh,44px) 22px">
        <div style="font-family:'Baloo 2';font-size:clamp(32px,6vw,72px);font-weight:900;line-height:.95;
          background:linear-gradient(135deg,${win?'#2ec4b6,#ffd166':'#ff6b6b,#ff8b6b'});
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
          ${win?'過關！':'再試！'}
        </div>
        <div style="font-size:clamp(12px,1.7vh,17px);color:#9bbfd4;margin:10px 0 8px">
          第${G.stage}層 第${G.level}關 · 得分 ${G.score} · 收集 ${G.collected}/${G.goal}<br>
          最高專注 ${Math.round(G.bestFocus)}%${hasDist?' · 含干擾訓練':''}
        </div>
        ${hasDist?`<div style="font-size:11px;color:#a78bfa;margin-bottom:14px;max-width:44ch;margin-inline:auto">
          干擾抑制訓練已啟動（第${G.stage}層）— 保持專注無視干擾是本層訓練重點
        </div>`:''}
        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap">
          ${win&&ns<=10?`<button class="btn p" onclick="startGame(${ns},${nl})">下一關</button>`:''}
          <button class="btn s" onclick="startGame(${G.stage},${G.level})">重新挑戰</button>
          <button class="btn w" onclick="UI.showMain()">主選單</button>
        </div>
      </div>`;
  }, 380);
}
