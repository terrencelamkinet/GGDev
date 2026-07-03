/* ================================================================
   FOCUS BIRD PRO v3 — audio.js
   Web Audio API engine
   - Distinct collection sound per food type
   - Combo escalation tones
   - Distractor burst sounds (surprise, low-frequency)
   - BGM per layer (10 profiles)
   ================================================================ */
'use strict';

const Audio = (() => {
  let AC = null, muted = false, bgmTimer = null, bgmStep = 0, bgmStage = 0;

  /* BGM profiles — one per layer */
  const BGM = [
    {scale:[523,659,784,1047],       bpm:108, wave:'sine',    vol:.016}, /* L1 apple */
    {scale:[440,554,659,880],        bpm:114, wave:'triangle',vol:.016}, /* L2 corn  */
    {scale:[349,440,523,698],        bpm:122, wave:'sine',    vol:.016}, /* L3 fries */
    {scale:[294,370,440,587,740],    bpm:118, wave:'sawtooth',vol:.014}, /* L4 cola  */
    {scale:[392,494,587,740,880],    bpm:106, wave:'sine',    vol:.016}, /* L5 cake  */
    {scale:[220,277,330,440],        bpm:100, wave:'triangle',vol:.014}, /* L6 choco */
    {scale:[262,330,392,523,659],    bpm:96,  wave:'sine',    vol:.016}, /* L7 ice   */
    {scale:[311,392,466,587,740],    bpm:110, wave:'sine',    vol:.016}, /* L8 bigcake */
    {scale:[440,554,659,784,1047],   bpm:120, wave:'triangle',vol:.016}, /* L9 duo   */
    {scale:[523,659,784,1047,1319],  bpm:130, wave:'sine',    vol:.016}, /* L10 all  */
  ];

  /* Food collection sound profiles
     Each food has a distinct timbre/pitch character so children
     learn to associate sound with visual — reinforces attention */
  const FOOD_SFX = {
    apple:    { freqs:[880,1100],     wave:'sine',    dur:.11, vol:.07 },
    corn:     { freqs:[660,880,1100], wave:'triangle',dur:.09, vol:.07 },
    fries:    { freqs:[440,660],      wave:'sawtooth',dur:.08, vol:.06 },
    cola:     { freqs:[294,440,587],  wave:'sine',    dur:.14, vol:.06 },
    cake:     { freqs:[1047,1319,1568],wave:'sine',   dur:.12, vol:.07 },
    choco:    { freqs:[220,330,440],  wave:'triangle',dur:.13, vol:.06 },
    icecream: { freqs:[1319,1568,2093],wave:'sine',   dur:.10, vol:.07 },
    bigcake:  { freqs:[523,784,1047,1319],wave:'sine',dur:.16, vol:.07 },
  };

  /* Distractor sound profiles — designed to be surprising but not alarming
     (Neuroelectrics 2014: distractor sounds should activate involuntary
     attention switch but must not cause fear/startle in young children) */
  const DISTRACT_SFX = [
    { freqs:[220,165],    wave:'sawtooth', dur:.18, vol:.045 }, /* low rumble */
    { freqs:[880,1320],   wave:'square',   dur:.09, vol:.04  }, /* chirp      */
    { freqs:[440,330,220],wave:'triangle', dur:.22, vol:.04  }, /* descend    */
    { freqs:[660,990],    wave:'sine',     dur:.12, vol:.05  }, /* ping       */
  ];

  function getAC(){
    if(!AC) AC=new(window.AudioContext||window.webkitAudioContext)();
    return AC;
  }
  function resume(){
    const a=getAC(); if(a.state==='suspended') a.resume();
  }
  function _tone(f,d=.1,wave='sine',vol=.05,delay=0){
    if(muted) return;
    resume();
    try {
      const a=getAC(), o=a.createOscillator(), g=a.createGain();
      const t0=a.currentTime+delay;
      o.type=wave; o.frequency.value=f;
      g.gain.setValueAtTime(vol,t0);
      g.gain.exponentialRampToValueAtTime(.0001,t0+d);
      o.connect(g); g.connect(a.destination);
      o.start(t0); o.stop(t0+d+.02);
    } catch(_) {}
  }

  /* ── Collection sound: distinct per food type ── */
  function collectSound(kind, combo=1) {
    const sfx = FOOD_SFX[kind] || FOOD_SFX.apple;
    const pitchShift = combo>=3 ? 1.25 : combo===2 ? 1.12 : 1;
    sfx.freqs.forEach((f,i)=>
      _tone(f*pitchShift, sfx.dur, sfx.wave, sfx.vol*(1+combo*.04), i*.038)
    );
  }

  /* ── Combo escalation ── */
  function combo(n){
    const base=440+Math.min(n-2,8)*65;
    [base,base*1.26,base*1.5].forEach((f,i)=>_tone(f,.1,'triangle',.055,i*.042));
  }

  /* ── Distractor burst sound ──
     Intensity 0-1; lower intensity = quieter, shorter, gentler pitch
     Stage 2-3 children get softer sounds; Stage 9-10 get sharper surprises */
  function distract(intensity=.5){
    if(muted) return;
    const sfx = DISTRACT_SFX[Math.floor(Math.random()*DISTRACT_SFX.length)];
    const vol = sfx.vol * (.4 + intensity*.6);
    const dur = sfx.dur * (.6 + intensity*.4);
    sfx.freqs.forEach((f,i)=>_tone(f,dur,sfx.wave,vol,i*.03));
  }

  /* ── Win / Lose ── */
  function win(){
    [523,659,784,1047,1319].forEach((f,i)=>_tone(f,.18,'sine',.06,i*.08));
  }
  function lose(){
    [370,294,220,165].forEach((f,i)=>_tone(f,.22,'sawtooth',.05,i*.11));
  }

  /* ── BGM ── */
  function startBGM(si){
    stopBGM(); bgmStep=0; bgmStage=Math.max(0,Math.min(9,si-1));
    _scheduleBGM();
  }
  function _scheduleBGM(){
    if(muted) return;
    const p=BGM[bgmStage], nd=60/p.bpm;
    /* Play two notes slightly apart for richer texture */
    _tone(p.scale[bgmStep%p.scale.length],nd*.75,p.wave,p.vol);
    if(bgmStep%4===0&&p.scale.length>3)
      _tone(p.scale[(bgmStep+2)%p.scale.length],nd*.65,p.wave,p.vol*.6,.06);
    bgmStep++;
    bgmTimer=setTimeout(_scheduleBGM,nd*1000);
  }
  function stopBGM(){ if(bgmTimer){clearTimeout(bgmTimer);bgmTimer=null;} }
  function setMuted(v){ muted=v; if(muted) stopBGM(); }
  function isMuted(){ return muted; }

  return { collectSound, combo, distract, win, lose, startBGM, stopBGM, setMuted, isMuted, resume };
})();
