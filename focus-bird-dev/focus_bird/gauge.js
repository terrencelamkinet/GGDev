/* ================================================================
   FOCUS BIRD PRO — gauge.js v3
   Real-time focus gauge (iOS stopwatch style) + sparkline + 85% tracker
   All motion uses time-based tween — never stops, never jumps
   ================================================================ */
'use strict';

const Gauge = (() => {
  let rafId = null, sparkData = [], lastLog = 0;
  let highStreak = 0, records = [], paused = false;
  let currentValue = 0, displayValue = 0, demo = false, demoFocus = 50;
  let twTo = 0;

  const COL = {
    track:   'rgba(255,255,255,.12)',
    red:     '#ff6b6b', amber: '#ffd166',
    green:   '#74d680', blue:  '#4f8cff',
    text:    '#f4faff', muted: '#9bbfd4',
    grid:    'rgba(255,255,255,.06)',
  };

  function focusColor(v) {
    if (v >= 85) return COL.blue;
    if (v >= 60) return COL.green;
    if (v >= 30) return COL.amber;
    return COL.red;
  }

  function arc(c, cx, cy, r, s, e, w, col) {
    c.beginPath(); c.arc(cx, cy, r, s, e);
    c.strokeStyle = col; c.lineWidth = w; c.lineCap = 'round'; c.stroke();
  }

  function isLive() {
    return G.running || (document.getElementById('ws-dot')?.classList.contains('ok'));
  }

  /* Every frame: advance displayValue toward target at constant speed (+1 per frame) */
  function tickTween() {
    if (currentValue !== twTo) {
      twTo = currentValue;
    }
    if (Math.round(displayValue) === twTo) { displayValue = twTo; return; }
    const diff = twTo - displayValue;
    /* Constant speed: ~72 units/sec = 1.2/frame. 40→70 = ~400ms, 20→80 = ~830ms */
    const step = Math.min(1.2, Math.abs(diff));
    if (Math.abs(diff) <= step) { displayValue = twTo; }
    else { displayValue += Math.sign(diff) * step; }
  }

  function drawGauge(c, W, H) {
    const cx = W/2, cy = H*0.42;
    const R = Math.min(W, H) * 0.35;
    const hasData = sparkData.length > 0;
    const val = Math.round(displayValue);
    const angle = (val/100)*Math.PI*1.5 + Math.PI*0.25;
    const sA = Math.PI*0.25, eA = Math.PI*1.75;

    /* Shadow */
    c.save(); c.shadowColor = focusColor(val); c.shadowBlur = 30;
    arc(c, cx, cy, R, sA, eA, 18, COL.track);
    const grad = c.createConicGradient(sA, cx, cy);
    grad.addColorStop(0, COL.red); grad.addColorStop(.3, COL.amber);
    grad.addColorStop(.6, COL.green); grad.addColorStop(.85, COL.blue); grad.addColorStop(1, COL.blue);
    c.strokeStyle = grad; c.lineWidth = 18;
    c.beginPath(); c.arc(cx, cy, R, sA, angle); c.stroke();
    c.restore();

    /* Ticks */
    for (let i=0;i<=10;i++) {
      const a=sA+(i/10)*Math.PI*1.5, inR=R-28, oR=R-10;
      c.beginPath(); c.moveTo(cx+Math.cos(a)*inR, cy+Math.sin(a)*inR);
      c.lineTo(cx+Math.cos(a)*oR, cy+Math.sin(a)*oR);
      c.strokeStyle=i%5===0?'rgba(255,255,255,.4)':'rgba(255,255,255,.18)';
      c.lineWidth=i%5===0?2.5:1.2; c.stroke();
    }
    ['0','25','50','75','100'].forEach((l,i)=>{
      const a=sA+(i*0.375)*Math.PI;
      c.font='bold 13px sans-serif'; c.textAlign='center'; c.textBaseline='middle';
      c.fillStyle=COL.muted;
      c.fillText(l, cx+Math.cos(a)*(R+26), cy+Math.sin(a)*(R+26));
    });

    /* Big number */
    c.font=`900 ${Math.round(R*.8)}px 'Baloo 2',sans-serif`;
    c.textAlign='center'; c.textBaseline='middle';
    c.fillStyle=focusColor(val); c.fillText(`${val}`, cx, cy-8);
    c.font='bold 14px sans-serif'; c.fillStyle=COL.muted;
    c.fillText(hasData ? (demo ? 'DEMO 專注度 %' : '專注度 %') : '等待腦電波數據...', cx, cy+R*.18);

    /* Needle */
    c.save(); c.translate(cx,cy); c.rotate(angle);
    c.beginPath(); c.moveTo(-6,12); c.lineTo(0,-R+24); c.lineTo(6,12); c.closePath();
    c.fillStyle=focusColor(val); c.shadowColor=focusColor(val); c.shadowBlur=12; c.fill();
    c.restore();

    /* Center cap */
    c.beginPath(); c.arc(cx,cy,12,0,Math.PI*2);
    c.fillStyle='#1a2332'; c.fill();
    c.strokeStyle='rgba(255,255,255,.25)'; c.lineWidth=2; c.stroke();
  }

  function drawSparkline(c, W, H) {
    const x0=W*.1, y0=H*.72, w=W*.8, h=H*.16, data=sparkData;
    if (data.length<1) {
      c.font='14px sans-serif'; c.textAlign='center'; c.fillStyle=COL.muted;
      c.fillText('等待數據中...', W/2, y0+h/2); return;
    }
    if (data.length<2) {
      c.font='14px sans-serif'; c.textAlign='center'; c.fillStyle=COL.muted;
      c.fillText('收集數據中...', W/2, y0+h/2); return;
    }
    c.fillStyle='rgba(0,0,0,.25)';
    c.beginPath(); c.roundRect(x0-8, y0-8, w+16, h+16, 12); c.fill();

    const yPos=p=>y0+h-(p/100)*h;
    [0,50,85,100].forEach(p=>{
      c.beginPath(); c.moveTo(x0, yPos(p)); c.lineTo(x0+w, yPos(p));
      c.strokeStyle=p===85?'rgba(79,140,255,.5)':COL.grid;
      c.lineWidth=p===85?1.5:1; c.setLineDash(p===85?[4,4]:[]); c.stroke(); c.setLineDash([]);
      if(p>0&&p<100){c.font='10px sans-serif';c.fillStyle=COL.muted;c.textAlign='right';c.fillText(`${p}%`, x0-6, yPos(p)+3);}
    });

    const stepX=w/Math.max(data.length-1,1), maxPts=Math.min(data.length,Math.floor(w/2));
    const slice=data.slice(-maxPts), offX=w-(slice.length-1)*stepX, li=slice.length-1;
    c.beginPath();
    slice.forEach((v,i)=>{
      const px=x0+offX+i*stepX;
      const py=i===li?yPos(Math.max(0,Math.min(100,displayValue))):yPos(v);
      i===0?c.moveTo(px,py):c.lineTo(px,py);
    });
    c.strokeStyle=COL.blue; c.lineWidth=2.5; c.stroke();
    c.lineTo(x0+offX+li*stepX, yPos(0)); c.lineTo(x0+offX, yPos(0)); c.closePath();
    c.fillStyle='rgba(79,140,255,.12)'; c.fill();
    c.font='11px sans-serif'; c.fillStyle=COL.muted; c.textAlign='left';
    c.fillText(demo ? 'DEMO 每秒專注度變化（撳 Space 或連接 BrainLink 即轉真實）' : '每秒專注度變化', x0, y0-12);
    c.textAlign='right'; c.fillText(`${Math.floor(sparkData.length*0.25)}秒`, x0+w, y0-12);
  }

  function drawStreak(c, W, H) {
    if (sparkData.length < 1) return;
    const x0=W*.1, y0=H*.91;
    c.font=`900 ${Math.round(H*.035)}px 'Baloo 2',sans-serif`; c.textAlign='center';
    const sc=highStreak>=5?COL.blue:COL.amber; c.fillStyle=sc;
    c.fillText(`🔥 連續高專注 ${highStreak}秒`, W/2, y0);
    c.font='12px sans-serif'; c.fillStyle=COL.muted; c.textAlign='center';
    c.fillText(highStreak>=5?'達成！記錄已保存 ✓':'專注度 ≥85% 持續5秒即記錄一次', W/2, y0+22);
    if(records.length>0){
      c.font='11px sans-serif'; c.textAlign='left'; c.fillStyle=COL.muted;
      records.slice(-5).reverse().forEach((r,i)=>{
        c.fillStyle=COL.blue; c.fillText(`★`, x0, y0+46+i*18);
        c.fillStyle=COL.text;
        c.fillText(`${r.t} — 專注 ${r.v}% (持續 ${r.d}秒)`, x0+18, y0+46+i*18);
      });
    }
  }

  let lastSparkPush = 0;
  function render() {
    const canvas=document.getElementById('gaugeCanvas');
    if(!canvas||paused){rafId=requestAnimationFrame(render);return;}
    const c=canvas.getContext('2d');
    const W=canvas.width=canvas.clientWidth*(window.devicePixelRatio||1);
    const H=canvas.height=canvas.clientHeight*(window.devicePixelRatio||1);
    c.scale(window.devicePixelRatio||1, window.devicePixelRatio||1);

    /* Tween animation — always running, full 1s per transition */
    tickTween();

    /* Push smooth displayValue to sparkData at 4Hz for smooth sparkline */
    const now = Date.now();
    if (now - lastSparkPush > 250) {
      sparkData.push(displayValue);
      if (sparkData.length > 120) sparkData.shift();
      lastSparkPush = now;
    }

    c.clearRect(0,0,canvas.clientWidth,canvas.clientHeight);
    drawGauge(c,canvas.clientWidth,canvas.clientHeight);
    drawSparkline(c,canvas.clientWidth,canvas.clientHeight);
    drawStreak(c,canvas.clientWidth,canvas.clientHeight);
    rafId=requestAnimationFrame(render);
  }

  let sampleTimer=null;
  function startSampling(){
    stopSampling(); lastLog=Date.now();
    sparkData.length = 0; lastSparkPush = 0;
    demoFocus = 50; demo = false;
    twTo = 0; displayValue = 0;
    sampleTimer=setInterval(()=>{
      const live = isLive();
      if (!live) {
        demo = true;
        demoFocus += (Math.random() - 0.5) * 20;
        if (demoFocus < 15) demoFocus += 8;
        else if (demoFocus > 90) demoFocus -= 8;
        demoFocus = Math.max(2, Math.min(98, demoFocus));
        if (Math.random() < 0.07) { demoFocus = Math.min(98, demoFocus + 30 + Math.random() * 15); }
        currentValue = Math.round(demoFocus);
      } else {
        demo = false;
        currentValue = G.focus;
      }
      /* Streak tracking uses raw currentValue */
      if(currentValue>=85){highStreak++;
        if(highStreak>=5&&(Date.now()-lastLog>3000)){
          const avg=sparkData.slice(-20).reduce((a,b)=>a+b,0)/20;
          records.push({t:new Date().toLocaleTimeString('zh-HK'),v:Math.round(avg),d:highStreak});
          if(records.length>50) records.shift(); lastLog=Date.now();
        }
      } else highStreak=0;
    },1000);
  }

  function stopSampling(){if(sampleTimer){clearInterval(sampleTimer);sampleTimer=null;}}

  function start(){paused=false;startSampling();if(!rafId) rafId=requestAnimationFrame(render);}
  function stop(){paused=true;stopSampling();if(rafId){cancelAnimationFrame(rafId);rafId=null;}}
  function reset(){sparkData=[];highStreak=0;records=[];lastLog=0;demoFocus=50;demo=false;
    twFrom=0;twTo=0;twStart=0;displayValue=0;currentValue=0;lastSparkPush=0;}
  function getRecords(){return[...records];}
  function getStreak(){return highStreak;}

  return{start,stop,reset,getRecords,getStreak};
})();
