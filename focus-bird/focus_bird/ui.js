/* ================================================================
   FOCUS BIRD PRO — ui.js
   All overlay screens, tab navigation, demo canvas, WS UI
   ================================================================ */
'use strict';

const UI = (() => {
  let demoRAF = null;

  function startDemo() {
    const dc = document.getElementById('demoC');
    if (!dc) return;
    const dc2 = dc.getContext('2d');
    let f = 0;
    cancelAnimationFrame(demoRAF);
    (function ad() {
      if (!document.getElementById('demoC')) return;
      f++;
      dc2.clearRect(0,0,420,280);
      const g2 = dc2.createLinearGradient(0,0,0,280);
      g2.addColorStop(0,'#4fc3f7'); g2.addColorStop(.6,'#b3e5fc'); g2.addColorStop(1,'#e8f5e9');
      dc2.fillStyle = g2; dc2.fillRect(0,0,420,280);
      dc2.fillStyle='#66bb6a'; dc2.fillRect(0,240,420,40);
      const by2 = 130+Math.sin(f*.04)*38;
      dc2.save(); dc2.translate(170,by2); dc2.scale(.62,.62);
      _demoBird(dc2,f*.15,Math.sin(f*.04)*.1);
      dc2.restore();
      dc2.save(); dc2.translate(310,237+Math.sin(f*.05+1)*5); dc2.scale(.52,.52);
      _demoApple(dc2); dc2.restore();
      dc2.save(); dc2.translate(370,237+Math.sin(f*.06+2)*5); dc2.scale(.42,.42);
      _demoCorn(dc2); dc2.restore();
      demoRAF = requestAnimationFrame(ad);
    })();
  }

  function _p(c2,fill,pts){c2.fillStyle=fill;c2.beginPath();c2.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)c2.lineTo(pts[i][0],pts[i][1]);c2.closePath();c2.fill();}

  function _demoBird(c2,wp,rot){
    const wu=Math.sin(wp)*20;
    c2.save(); c2.rotate(rot);
    _p(c2,'#0d47a1',[[-62,0],[-86,-7],[-68,-22],[-48,-5]]);
    _p(c2,'#1a4fa8',[[-12,2],[-58,-24+wu],[-48,-9+wu],[-6,14]]);
    _p(c2,'#3a7bd5',[[0,-18],[48,-22],[56,2],[38,28],[0,26],[-20,6]]);
    _p(c2,'#ffe066',[[18,8],[38,10],[34,28],[14,28]]);
    _p(c2,'#4f8cff',[[38,-24],[76,-30],[80,-6],[58,2],[36,-2]]);
    _p(c2,'#fff',[[55,-20],[65,-22],[67,-10],[57,-8]]);
    _p(c2,'#111',[[59,-18],[63,-19],[64,-11],[60,-10]]);
    _p(c2,'#fb8500',[[70,-14],[96,-8],[70,-2]]);
    c2.restore();
  }
  function _demoApple(c2){
    _p(c2,'#c62828',[[-16,2],[-8,-22],[12,-20],[20,4],[8,22],[-10,22]]);
    _p(c2,'#ef9a9a',[[-6,-10],[8,-8],[10,6],[0,14],[-8,12]]);
    _p(c2,'#2e7d32',[[-2,-22],[6,-36],[10,-20]]);
  }
  function _demoCorn(c2){
    _p(c2,'#f9a825',[[-12,-28],[12,-28],[18,28],[-18,28]]);
    _p(c2,'#fdd835',[[-8,-24],[8,-24],[12,24],[-12,24]]);
    _p(c2,'#388e3c',[[-14,24],[-4,0],[-14,14]]);
    _p(c2,'#388e3c',[[14,24],[4,0],[14,14]]);
  }

  function switchTab(screenId) {
    document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.screen===screenId));
    document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active',s.id===screenId));
  }

  function toast(msg){
    const el=document.createElement('div');el.className='toast';el.textContent=msg;
    document.body.appendChild(el);setTimeout(()=>el.remove&&el.remove(),1800);
  }

  function updateWSLabel(){
    ['wsStatusTxt','wsStatusTxt2'].forEach(id=>{
      const el=document.getElementById(id);
      if(!el)return;
      const d=document.getElementById('ws-dot');
      const ok=d&&d.classList.contains('ok');
      const stale=d&&d.classList.contains('stale');
      el.textContent=ok?'🧠 已連接':stale?'⏳ 連線無數據':'未連接';
      el.style.color=ok?'#74d680':stale?'#ffd166':'#ff6b6b';
    });
  }

  function showMain(profileId){
    G.running=false;
    const profile = profileId ? PROFILE.getProfile(profileId) : null;
    const p=ageProfile(G.age);
    document.getElementById('ov').classList.remove('gone');
    document.getElementById('btnMenu').style.display='none';
    Audio.stopBGM();

    /* stop previous device check timer */
    if (window._devCheckTimer) clearInterval(window._devCheckTimer);

    document.getElementById('mc').innerHTML=`
<div class="tabs">
  <button class="tab active" data-screen="sc-home">主頁</button>
  <button class="tab" data-screen="sc-tutorial">教學</button>
  <button class="tab" data-screen="sc-stages">選關</button>
  <button class="tab" data-screen="sc-settings">設定</button>
  <button class="tab" data-screen="sc-plan">訓練計劃</button>
  <button class="tab" data-screen="sc-profile">用戶</button>
</div>

<div class="screen active" id="sc-home">
  <div class="grid2">
    <div>
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">
        <div style="width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#2ec4b6,#4f8cff);display:grid;place-items:center;flex-shrink:0">
          <svg viewBox="0 0 64 64" width="36" height="36" fill="none">
            <path d="M16 38c0-13 10-24 22-24 8 0 14 4 18 9-6-1-11 0-15 4 4 0 9 3 12 6-5 3-10 3-14 3-2 10-10 17-19 17-7 0-13-4-15-9 4 2 8 2 11 2-2-3 0-5 0-8z" fill="white" fill-opacity=".22"/>
            <circle cx="42" cy="28" r="3" fill="white"/>
          </svg>
        </div>
        <div>
          <div style="font-family:'Baloo 2';font-size:19px;font-weight:900;line-height:1">專注飛鳥 Pro</div>
          <div class="note">${profile ? profile.avatar+' '+profile.name+' · ' : ''}腦電波控制 · 10層100關 · 1至40歲</div>
        </div>
      </div>
      <div class="ttl">集中精神<br>收集美食！</div>
      <p class="sub">戴上BrainLink腦電波頭盔，專注時令小鳥下沉收集美食。專注度越高，下沉越深，收集越多！</p>
      <div class="acts" style="margin-top:20px">
        <button class="btn p" style="font-size:clamp(14px,2vh,19px);padding:clamp(12px,1.8vh,17px) clamp(22px,3vw,40px)" id="btnStart">${profile ? '繼續訓練' : '開始遊戲'}</button>
        <button class="btn s" id="btnGoStages">選擇關卡</button>
        <button class="btn w" id="btnGoPlan">訓練計劃</button>
      </div>
      ${profile ? (()=>{
        /* find current level */
        let cs = 1, cl = 1;
        for (let s = 1; s <= 10; s++) {
          for (let l = 1; l <= 10; l++) {
            if (!profile.completed[`${s}-${l}`] && profile.unlocked[`${s}-${l}`]) { cs=s; cl=l; break; }
          }
          if (cs !== 1 || cl !== 1) break;
        }
        const st = STAGES[cs-1];
        /* compute goal */
        const pf = ageProfile(G.age);
        const goal = pf.goalBase + Math.floor((cs-1)*1.4+(cl-1)*0.9);
        const theme = cs >= 9 ? '混合' : st.zh;
        const totalStars = Object.values(profile.completed).reduce((a,c) => a + (c.stars||0), 0);
        const totalDone = Object.keys(profile.completed).length;
        return `
      <div class="panel" style="margin-top:16px;padding:14px 16px;border-left:4px solid #ffd166">
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
          <div style="font-size:28px">${profile.avatar}</div>
          <div style="flex:1;min-width:0">
            <div style="font-weight:900;font-size:clamp(13px,1.6vh,17px)">${profile.name}</div>
            <div class="note">⭐ ${totalStars}星 · ${totalDone}關完成 · ⏱ ${PROFILE.formatTime(profile.playTime)}</div>
          </div>
          <div style="text-align:right">
            <div style="font-weight:900;font-size:clamp(18px,2.2vh,24px);color:#ffd166">第${cs}層</div>
            <div class="note">第${cl}關</div>
          </div>
        </div>
        <div style="margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,.08)">
          <div class="grid2b" style="gap:8px;font-size:clamp(11px,1.3vh,14px)">
            <div>
              <span style="color:#9bbfd4">🎯 收集</span> <strong style="color:#ffd166">${goal}個 ${theme}</strong>
            </div>
            <div>
              <span style="color:#9bbfd4">🧠 專注</span> <strong id="homeFocusVal">${Math.round(G.focus)}%</strong>
              <span style="color:#9bbfd4"> · 門檻 ${G.threshold}</span>
            </div>
          </div>
        </div>
      </div>`; })() : ''}
    </div>
    <div>
      <canvas id="demoC" width="420" height="280"
        style="width:100%;border-radius:18px;border:1px solid rgba(255,255,255,.15);background:linear-gradient(180deg,#4fc3f7,#b3e5fc)"></canvas>
      <div class="grid2b" style="margin-top:12px;gap:8px">
        <div class="panel" style="padding:10px 12px">
          <div style="font-size:11px;font-weight:900;color:#9bbfd4;margin-bottom:4px">目前設定</div>
          <div style="font-size:clamp(12px,1.5vh,15px);font-weight:900" id="homeAgeDisplay">${p.band} · ${G.age}歲</div>
          <div class="note">門檻 ${G.threshold} · 每節${p.session}分</div>
        </div>
        <div class="panel" style="padding:10px 12px">
          <div style="font-size:11px;font-weight:900;color:#9bbfd4;margin-bottom:4px">連接狀態</div>
          <div style="font-size:clamp(12px,1.5vh,15px);font-weight:900" id="wsStatusTxt">偵測中...</div>
          <div class="note">裝置連線後方可遊玩</div>
        </div>
      </div>
    </div>
  </div>
  <div id="device-block" style="
    position:fixed;inset:0;z-index:40;
    display:flex;align-items:center;justify-content:center;
    background:rgba(4,14,22,.92);backdrop-filter:blur(18px)">
    <button id="btnDismissDevice" style="
      position:absolute;top:14px;right:14px;width:44px;height:44px;border-radius:50%;
      border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);
      color:#fff;font-size:22px;cursor:pointer;display:grid;place-items:center;
      transition:.15s;z-index:41" title="略過，稍後再連">✕</button>
    <div style="text-align:center;max-width:400px;padding:20px">
      <div style="font-size:52px;margin-bottom:14px;animation:pulse 1.5s ease-in-out infinite" id="dev-icon">🧠</div>
      <div style="font-family:'Baloo 2';font-size:clamp(24px,4vw,36px);font-weight:900;line-height:1.2;margin-bottom:8px">等待 BrainLink 連接</div>
      <div class="sub" style="margin-inline:auto">請確保頭盔已開機並連接<br>然後啟動 bridge：<br><code style="background:rgba(255,255,255,.1);padding:4px 10px;border-radius:6px;font-size:12px">brainlink_pro.py --port COM3 --relay</code></div>
      <div style="margin-top:14px;font-size:14px;color:#9bbfd4;margin-bottom:20px" id="dev-status-msg">
        等待連接中...
      </div>
      <div style="margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
        <button class="btn p" id="btnRetryDevice" style="font-size:15px">重新偵測</button>
      </div>
      <div style="margin-top:14px;font-size:12px;color:#9bbfd4">
        WS: <span id="dev-ws" style="color:#ff6b6b">❌</span>
        &nbsp;訊號: <span id="dev-sig">-</span>
        &nbsp;<span id="dev-device" style="display:none"></span>
      </div>
    </div>
  </div>
</div>

<div class="screen" id="sc-tutorial">
  <div class="sh" style="margin-bottom:14px">遊戲教學</div>
  <div class="tuts">
    ${[
      {bg:'#3a7bd5',t:'腦電波控制',d:'戴上BrainLink頭盔，保持專注，小鳥自動下沉收集食物。專注度越高，下沉越深。'},
      {bg:'#2ec4b6',t:'收集目標',d:'每關有指定收集數量，時間內收集足夠即可過關。食物沿地面從右方出現。'},
      {bg:'#ffd166',t:'連擊加分',d:'短時間內連續收集可觸發連擊加分！保持高專注令小鳥持續低飛。'},
      {bg:'#e63946',t:'年齡設定',d:'在設定頁調整1–40歲年齡滑桿，遊戲自動設定適合的速度、目標和難度。'},
      {bg:'#7b1fa2',t:'10層100關',d:'共10層，每層10關，食物和背景主題各不相同，難度循序漸進。'},
      {bg:'#ff7043',t:'Space備用',d:'沒有頭盔時按住Space鍵可控制小鳥，用於測試遊戲效果及展示。'},
    ].map(({bg,t,d})=>`
    <div class="tut">
      <div class="tut-ic" style="background:${bg}">
        <svg viewBox="0 0 40 40" width="28" height="28" fill="white"><circle cx="20" cy="20" r="14" fill-opacity=".35"/><circle cx="20" cy="20" r="6"/></svg>
      </div>
      <div style="font-weight:900;font-size:clamp(12px,1.5vh,15px);margin-bottom:5px">${t}</div>
      <p class="note">${d}</p>
    </div>`).join('')}
  </div>
  <div style="margin-top:20px">
    <div class="sh" style="margin-bottom:10px">10層食物主題</div>
    <table style="width:100%;border-collapse:collapse;font-size:clamp(10px,1.3vh,13px)">
      <tr style="background:rgba(46,196,182,.18)">
        ${['層','主題','食物','層','主題','食物'].map(h=>`<th style="padding:7px 10px;text-align:left;font-weight:900">${h}</th>`).join('')}
      </tr>
      ${[[1,'蘋果樂園','蘋果'],[2,'粟米田野','粟米'],[3,'薯條王國','薯條'],[4,'可樂世界','可樂'],[5,'甜品花園','甜品']]
        .map((r,i)=>{
          const r2=[[6,'朱古力森林','朱古力'],[7,'雪糕山','雪糕'],[8,'蛋糕城堡','蛋糕'],[9,'雙重盛宴','2種混合'],[10,'終極大混合','全部食物']][i];
          return `<tr style="border-bottom:1px solid rgba(255,255,255,.07)">
            <td style="padding:7px 10px;font-weight:800">${r[0]}</td><td style="padding:7px 10px">${r[1]}</td><td style="padding:7px 10px">${r[2]}</td>
            <td style="padding:7px 10px;font-weight:800">${r2[0]}</td><td style="padding:7px 10px">${r2[1]}</td><td style="padding:7px 10px">${r2[2]}</td>
          </tr>`;
        }).join('')}
    </table>
  </div>
</div>

<div class="screen" id="sc-stages">
  <div class="sh" style="margin-bottom:4px">選擇層次</div>
  <p class="note" style="margin-bottom:14px">共10層，每層10關，食物主題不同。</p>
  <div class="sgrid" id="stageGrid"></div>
  <div id="levelGrid" style="margin-top:18px"></div>
</div>

<div class="screen" id="sc-settings">
  <div class="sh" style="margin-bottom:14px">遊戲設定</div>
  <div class="grid2b" style="gap:16px">
    <div class="panel">
      <div class="sh">年齡設定 <span style="color:#9bbfd4;font-weight:600;font-size:11px">(1–40歲)</span></div>
      <div class="row">
        <input id="ageR" type="range" min="1" max="40" step="1" value="${G.age}">
        <div class="rval"><span id="ageV">${G.age}</span>歲</div>
      </div>
      <p class="note" id="ageNote" style="margin-top:8px">${p.band}：每節建議${p.session}分鐘，基礎目標${p.goalBase}個</p>
    </div>
    <div class="panel">
      <div class="sh">下沉門檻 <span style="color:#9bbfd4;font-weight:600;font-size:11px">(專注度值)</span></div>
      <div class="row">
        <input id="thrR" type="range" min="20" max="90" step="1" value="${G.threshold}">
        <div class="rval"><span id="thrV">${G.threshold}</span></div>
      </div>
      <p class="note" style="margin-top:8px">數值越低越易下沉。年幼建議20–40，成人建議50–70。</p>
    </div>
    <div class="panel">
      <div class="sh">腦電波連接</div>
      <p class="note" style="margin-top:4px">狀態：<span id="wsStatusTxt2">偵測中...</span></p>
      <p class="note">伺服器：ws://localhost:8765</p>
      <p class="note" style="margin-top:4px">請先啟動 focus_bridge_windows.py</p>
      <div class="acts" style="margin-top:10px">
        <button class="btn s" style="font-size:12px;padding:8px 12px" id="btnReconn">重新連接</button>
      </div>
    </div>
    <div class="panel">
      <div class="sh">音效設定</div>
      <p class="note" style="margin-top:4px">每層擁有獨立BGM音樂風格，收集音效根據連擊提升音調。</p>
      <div class="acts" style="margin-top:10px">
        <button class="btn s" style="font-size:12px;padding:8px 12px" id="btnToggleMute">${Audio.isMuted()?'開啟音效':'靜音'}</button>
      </div>
    </div>
  </div>
</div>

<div class="screen" id="sc-plan">
  <div class="sh" style="margin-bottom:6px">一個月專注力訓練計劃</div>
  <p class="note" style="margin-bottom:16px">參考AAP、PMC及NHA學術研究制定，多人認證有效。</p>
  <div class="grid2b" style="gap:12px">
    ${[
      {c:'#2ec4b6',w:'第一週：基礎適應',f:'每週3天（一三五）',t:'8–12分鐘/節',g:'成功率達60%+，熟悉遊戲操作',ref:'美國兒科學會（AAP）：神經反饋為注意力訓練Level 1最強支持介入。初期以低壓力、高成功率建立正強化。'},
      {c:'#4f8cff',w:'第二週：穩定提升',f:'每週4天（一二四五）',t:'12–16分鐘/節',g:'連擊出現≥3次/節',ref:'Frontiers in Human Neuroscience (2014)：每週3–5節×15分鐘，2週後可觀察工作記憶改善。'},
      {c:'#ffd166',w:'第三週：挑戰突破',f:'每週5天（週一至五）',t:'15–20分鐘/節',g:'完成第1層全10關，專注度≥55%',ref:'PMC (2025) RCT研究（n=104）：每週5節×20分鐘×4週，效果持續6–12個月。'},
      {c:'#ff8b6b',w:'第四週：鞏固成效',f:'每週5天',t:'18–25分鐘/節',g:'完成第1–2層，專注度≥65%',ref:'NHA指引（2025）：每週2–3節持續，10–20節後大多數人感受顯著改善。'},
    ].map(({c,w,f,t,g,ref})=>`
    <div class="wcard" style="--wc:${c}">
      <div class="wtitle">${w}</div>
      <div class="wbody">頻率：${f}<br>每節時長：${t}<br>本週目標：${g}</div>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,.1);margin:10px 0">
      <p class="note">${ref}</p>
    </div>`).join('')}
  </div>
  <div class="panel" style="margin-top:16px">
    <div class="sh" style="margin-bottom:10px;color:#a78bfa">專家指引摘要</div>
    <table class="ptable">
      <tr><th>指標</th><th>建議</th><th>依據</th></tr>
      <tr><td>每次時長</td><td>年齡 x 2–3分鐘</td><td>2歲約4–6分；10歲約20–30分</td></tr>
      <tr><td>每週頻率</td><td>3–5次</td><td>少於3次效果不顯著（PMC 2025）</td></tr>
      <tr><td>訓練總量</td><td>≥20節開始見效</td><td>≥30節效果穩固（NHA 2025）</td></tr>
      <tr><td>休息間隔</td><td>每節後5分鐘</td><td>恢復專注力（EdCity HK 2024）</td></tr>
      <tr><td>效果持續</td><td>6–12個月</td><td>多項RCT確認（PMC 2025）</td></tr>
    </table>
  </div>
</div>

<div class="screen" id="sc-profile">
  <div id="profile-screen-inner" style="min-height:200px"></div>
</div>
`;

    document.querySelectorAll('.tab').forEach(t=>
      t.addEventListener('click',()=>{
        switchTab(t.dataset.screen);
        if(t.dataset.screen==='sc-stages') buildStageGrid();
        if(t.dataset.screen==='sc-home') startDemo();
        if(t.dataset.screen==='sc-profile') {
          const inner = document.getElementById('profile-screen-inner');
          if (inner) PROFILE.renderProfileScreen(inner);
        }
      })
    );

    document.getElementById('btnStart').onclick  = ()=>{
      if (profileId) {
        // Find first unlocked level for this profile
        const p = PROFILE.getProfile(profileId);
        for (let s = 1; s <= 10; s++) {
          for (let l = 1; l <= 10; l++) {
            if (!p.completed[`${s}-${l}`] && p.unlocked[`${s}-${l}`]) {
              startGame(s, l);
              return;
            }
          }
        }
        startGame(1,1); // fallback
      } else {
        startGame(1,1);
      }
    };
    document.getElementById('btnGoStages').onclick = ()=>{
      document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.screen==='sc-stages'));
      document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active',s.id==='sc-stages'));
      buildStageGrid();
    };
    document.getElementById('btnGoPlan').onclick = ()=>{
      document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.screen==='sc-plan'));
      document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active',s.id==='sc-plan'));
    };

    document.getElementById('ageR').addEventListener('input',e=>{
      G.age=+e.target.value;
      document.getElementById('ageV').textContent=G.age;
      const pp=ageProfile(G.age);
      document.getElementById('ageNote').textContent=pp.band+'：每節建議'+pp.session+'分鐘，基礎目標'+pp.goalBase+'個';
      if(!document.getElementById('thrR').dataset.touched){
        G.threshold=pp.threshold;
        document.getElementById('thrR').value=pp.threshold;
        document.getElementById('thrV').textContent=pp.threshold;
      }
      document.getElementById('homeAgeDisplay').textContent=pp.band+' · '+G.age+'歲';
    });
    document.getElementById('thrR').addEventListener('input',e=>{
      document.getElementById('thrR').dataset.touched='1';
      G.threshold=+e.target.value;
      document.getElementById('thrV').textContent=G.threshold;
    });
    document.getElementById('btnReconn').onclick=()=>{ WS.connect(); toast('嘗試重新連接...'); };
    document.getElementById('btnToggleMute').onclick=()=>{
      const m=!Audio.isMuted(); Audio.setMuted(m);
      document.getElementById('btnToggleMute').textContent=m?'開啟音效':'靜音';
      document.getElementById('btnMute').textContent=m?'\u{1F507}':'♫';
      toast(m?'靜音':'音效開啟');
    };
    /* Device block — check every second */
    function checkDevice() {
      const s = WS.stats;
      const devBlock = document.getElementById('device-block');
      if (!devBlock) return;
      /* always update status elements */
      const el = (id) => document.getElementById(id);
      const wsEl = el('dev-ws');
      const sigEl = el('dev-sig');
      const devEl = el('dev-device');
      const msgEl = el('dev-status-msg');
      const iconEl = el('dev-icon');
      if (wsEl) {
        const dot = document.getElementById('ws-dot');
        if (dot && dot.classList.contains('ok')) {
          wsEl.textContent = '✅'; wsEl.style.color = '#74d680';
        } else if (dot && dot.classList.contains('stale')) {
          wsEl.textContent = '🟡'; wsEl.style.color = '#ffd166';
        } else {
          wsEl.textContent = '❌'; wsEl.style.color = '#ff6b6b';
        }
      }
      if (sigEl) sigEl.textContent = s.lastSig;

      /* CASE 1: WS not connected at all — show waiting, no bypass */
      if (!s.connected) {
        if (msgEl) msgEl.innerHTML = '🔄 連接伺服器中...<br><span style="font-size:12px;opacity:.7">請確保 bridge 正在執行</span>';
        if (iconEl) iconEl.textContent = '🔄';
        if (devEl) { devEl.style.display = 'none'; }
        return;  /* keep block */
      }

      /* CASE 2: WS connected + signal >= 150 (bridge up, no device) → block, show status */
      if (s.connected && typeof s.lastSig === 'number' && s.lastSig >= 150) {
        if (msgEl) msgEl.innerHTML = '⚠️ 伺服器已連接<br><span style="font-size:12px;opacity:.7">請開啟腦波儀電源並確保頭盔就位</span>';
        if (iconEl) iconEl.textContent = '🧢';
        if (devEl) {
          devEl.style.display = 'inline';
          devEl.textContent = '🔴 無裝置';
          devEl.style.color = '#ff6b6b';
        }
        return;  /* KEEP BLOCK — hard requirement */
      }

      /* CASE 3: WS connected + signal < 150 (= real brain data) → dismiss block */
      if (s.connected && typeof s.lastSig === 'number' && s.lastSig >= 0 && s.lastSig < 150) {
        devBlock.style.display = 'none';
        if (window._devCheckTimer) clearInterval(window._devCheckTimer);
        return;
      }

      /* CASE 4: fallback (e.g. lastSig is '-' or undefined) — keep block */
      if (msgEl) msgEl.textContent = '⏳ 等待裝置回應...';
    }
    checkDevice();
    window._devCheckTimer = setInterval(checkDevice, 1000);
    /* Live focus update for home screen */
    if (window._homeFocusTimer) clearInterval(window._homeFocusTimer);
    window._homeFocusTimer = setInterval(() => {
      const el = document.getElementById('homeFocusVal');
      if (el) el.textContent = Math.round(G.focus) + '%';
    }, 500);
    document.getElementById('btnRetryDevice').onclick = () => { checkDevice(); WS.connect(); };
    document.getElementById('btnDismissDevice').onclick = () => {
      const devBlock = document.getElementById('device-block');
      if (devBlock) {
        devBlock.style.display = 'none';
        if (window._devCheckTimer) clearInterval(window._devCheckTimer);
      }
    };
    updateWSLabel();
    startDemo();
  }

  function buildStageGrid(sel) {
    const grid = document.getElementById('stageGrid');
    if (!grid) return;
    grid.innerHTML = STAGES.map((st,i)=>`
      <button class="scard" data-si="${i+1}">
        <svg viewBox="0 0 32 32" width="26" height="26" fill="none">
          <circle cx="16" cy="16" r="14" fill="${st.sky1}" fill-opacity=".7"/>
          <circle cx="16" cy="16" r="7" fill="${st.gnd}" fill-opacity=".9"/>
        </svg>
        <div>第${i+1}層</div>
        <div style="font-size:10px;opacity:.7">${st.zh}</div>
      </button>`).join('');
    grid.querySelectorAll('.scard').forEach(btn=>{
      btn.addEventListener('click',()=>buildLevelGrid(+btn.dataset.si));
    });
    if (sel) buildLevelGrid(sel);
  }

  function buildLevelGrid(stage) {
    const st   = STAGES[stage-1];
    const cont = document.getElementById('levelGrid');
    if (!cont) return;
    const pid = PROFILE.getActiveId();
    const p = pid ? PROFILE.getProfile(pid) : null;
    cont.innerHTML=`
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <div class="sh" style="margin:0">第${stage}層：${st.zh}</div>
        <span class="note">${p ? '🔒 未解鎖 · ✅ 已完成' : '選擇關卡開始遊戲'}</span>
      </div>
      <div class="lgrid">
        ${[...Array(10)].map((_,i)=>{
          const lv = i+1;
          const key = `${stage}-${lv}`;
          const unlocked = p ? PROFILE.isUnlocked(pid, stage, lv) : true;
          const completed = p ? p.completed[key] : null;
          const stars = completed ? completed.stars : 0;
          const isCurrent = unlocked && !completed;
          return unlocked
            ? `<button class="lcard l-unlocked ${isCurrent ? 'l-current' : ''}" data-st="${stage}" data-lv="${lv}"
                title="${completed ? '✅ 已完成' : '▶ 可挑戰'}">
                <div style="font-size:clamp(20px,3vw,36px);font-weight:900">${lv}</div>
                <div>第${lv}關</div>
                ${stars > 0 ? `<div style="font-size:14px">${'⭐'.repeat(stars)}</div>` : ''}
                ${completed ? `<div style="font-size:10px;color:#9bbfd4">${PROFILE.formatTime(completed.time)}</div>` : ''}
              </button>`
            : `<div class="lcard l-locked" style="cursor:default">
                <div style="font-size:clamp(20px,3vw,36px)">🔒</div>
                <div>第${lv}關</div>
              </div>`;
        }).join('')}
      </div>`;
      cont.querySelectorAll('.lcard[data-st]').forEach(btn=>{
        btn.addEventListener('click',()=>startGame(+btn.dataset.st,+btn.dataset.lv));
      });
  }

  return { showMain, toast, updateWSLabel, startDemo };
})();
