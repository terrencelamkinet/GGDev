/* ================================================================
   FOCUS BIRD PRO — profile.js
   PS5-style profile selection + save system (localStorage)
   ================================================================ */
'use strict';

const PROFILE = (() => {

  const STORAGE_KEY = 'focusbird_v02_profiles';

  const DEFAULTS = {
    version: 2,
    lastProfile: null,
    leaderboard: {},
    profiles: {
      guest: {
        name: 'Guest', age: 15, avatar: '👤',
        unlocked: {'1-1': true},
        completed: {},
        playTime: 0,
        lastPlayed: null
      },
      shema: {
        name: 'Shema', age: 4, avatar: '🌸',
        unlocked: {'1-1': true},
        completed: {},   // {'1-1': {score:5, time:45, stars:2}, '1-2':...}
        playTime: 0,     // total seconds
        lastPlayed: null // ISO timestamp
      },
      jeremy: {
        name: 'Jeremy', age: 7, avatar: '🚀',
        unlocked: {'1-1': true},
        completed: {},
        playTime: 0,
        lastPlayed: null
      }
    }
  };

  /* ── Data ── */
  let data = null;

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        data = JSON.parse(raw);
        // Merge defaults (in case new fields added)
        for (const k of Object.keys(DEFAULTS.profiles)) {
          if (!data.profiles[k]) data.profiles[k] = JSON.parse(JSON.stringify(DEFAULTS.profiles[k]));
          else {
            if (!data.profiles[k].unlocked) data.profiles[k].unlocked = {'1-1': true};
            if (!data.profiles[k].completed) data.profiles[k].completed = {};
            if (data.profiles[k].playTime === undefined) data.profiles[k].playTime = 0;
          }
        }
        if (!data.lastProfile) data.lastProfile = null;
      } else {
        data = JSON.parse(JSON.stringify(DEFAULTS));
      }
    } catch (_) {
      data = JSON.parse(JSON.stringify(DEFAULTS));
    }
    save();
  }

  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (_) {}
  }

  /* ── Profile API ── */

  function listProfiles() {
    return Object.entries(data.profiles).map(([id, p]) => ({id, ...p}));
  }

  function getProfile(id) {
    return data.profiles[id] || null;
  }

  function getActive() {
    if (!data.lastProfile) return null;
    return data.profiles[data.lastProfile] || null;
  }

  function getActiveId() {
    return data.lastProfile;
  }

  function select(id) {
    if (!data.profiles[id]) return false;
    data.lastProfile = id;
    data.profiles[id].lastPlayed = new Date().toISOString();
    save();
    return true;
  }

  function isUnlocked(profileId, stage, level) {
    const p = data.profiles[profileId];
    if (!p) return false;
    // Guest: all levels unlocked
    if (profileId === 'guest') return true;
    const key = `${stage}-${level}`;
    // Stage 1 Level 1 is always unlocked
    if (stage === 1 && level === 1) return true;
    return !!p.unlocked[key];
  }

  function markCompleted(profileId, stage, level, result) {
    const p = data.profiles[profileId];
    if (!p) return;
    const key = `${stage}-${level}`;
    const prev = p.completed[key];
    // Always update best records across attempts
    const bestTime = prev ? Math.max(prev.bestTime, result.time) : result.time;
    const bestFocus5s = prev ? Math.max(prev.bestFocus5s, result.bestFocus5s || 0) : (result.bestFocus5s || 0);
    // Don't overwrite stars if worse
    if (prev && prev.stars >= result.stars) {
      // Keep existing stars but update best records
      p.completed[key].bestTime = bestTime;
      p.completed[key].bestFocus5s = bestFocus5s;
      p.completed[key].date = new Date().toISOString();
    } else {
      p.completed[key] = {
        score: result.score || 0,
        time: result.time || 0,
        stars: result.stars || 1,
        bestTime: bestTime,
        bestFocus5s: bestFocus5s,
        date: new Date().toISOString()
      };
    }
    // Unlock next level
    const nextLevel = level < 10 ? `${stage}-${level + 1}` : `${stage + 1}-1`;
    // Only unlock if within bounds
    if (level < 10) {
      p.unlocked[`${stage}-${level + 1}`] = true;
    } else if (stage < 10) {
      p.unlocked[`${stage + 1}-1`] = true;
    }
    p.playTime = (p.playTime || 0) + (result.time || 0);
    save();
  }

  function getSettings(profileId) {
    const p = data.profiles[profileId];
    if (!p) return {age: 5, threshold: 40};
    // Age-based default settings
    const ageSettings = {
      4:  {age: 4, threshold: 30, grav: 1.0},
      7:  {age: 7, threshold: 40, grav: 0.9},
      15: {age: 15, threshold: 50, grav: 0.75},
    };
    return ageSettings[p.age] || {age: p.age, threshold: 40, grav: 0.9};
  }

  function resetProfile(profileId) {
    if (!data.profiles[profileId]) return;
    data.profiles[profileId] = JSON.parse(JSON.stringify(DEFAULTS.profiles[profileId]));
    save();
  }

  function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  function getBestRecord(profileId, stage, level) {
    const p = data.profiles[profileId];
    if (!p) return null;
    const key = `${stage}-${level}`;
    const c = p.completed[key];
    if (!c) return null;
    return { time: c.bestTime || c.time, focus: c.bestFocus5s || 0 };
  }

  /* ── Leaderboard (Guest) ── */

  function getLeaderboard(stage) {
    if (!data.leaderboard) data.leaderboard = {};
    if (!data.leaderboard[stage]) data.leaderboard[stage] = [];
    return data.leaderboard[stage];
  }

  function checkLeaderboardRank(stage, focus5s) {
    const lb = getLeaderboard(stage);
    if (lb.length < 3) return lb.length + 1;
    if (focus5s > lb[2].focus5s) {
      for (let i = 0; i < 3; i++) {
        if (focus5s > lb[i].focus5s) return i + 1;
      }
      return 3;
    }
    return 0;
  }

  function addLeaderboardEntry(stage, name, focus5s, time, level) {
    if (!name || !name.trim()) return false;
    const lb = getLeaderboard(stage);
    lb.push({ name: name.trim().slice(0,8), focus5s: Math.round(focus5s), time: Math.floor(time), level, date: new Date().toISOString() });
    lb.sort((a, b) => b.focus5s - a.focus5s || b.time - a.time);
    if (lb.length > 3) lb.length = 3;
    save();
    return true;
  }

  /* ── Render ── */

  let _onSelect = null;

  function onSelect(cb) {
    _onSelect = cb;
  }

  function renderProfileScreen(targetEl){
    const container = targetEl || document.getElementById('mc');
    if (!container) return;

    const profiles = listProfiles();

    let cardsHtml = profiles.map((p, i) => `
      <div class="p-card" data-id="${p.id}" style="animation-delay:${i * 0.12}s">
        <div class="p-avatar">${p.avatar}</div>
        <div class="p-name">${p.name}</div>
        <div class="p-age">${p.age} 歲</div>
        ${p.lastPlayed ? `<div class="p-last">上次: ${p.lastPlayed.slice(0,10)}</div>` : '<div class="p-last" style="opacity:.4">未玩過</div>'}
        ${p.completed ? `<div class="p-stats">🏆 ${Object.keys(p.completed).length} 關</div>` : ''}
      </div>
    `).join('');

    container.innerHTML = `
      <div class="p-screen">
        <div class="p-title">誰在玩？</div>
        <div class="p-cards">
          ${cardsHtml}
        </div>
        <div style="margin-top:30px;opacity:.35;font-size:clamp(12px,1.5vh,15px);color:#9bbfd4">
          專注飛鳥 Pro · v02 · 專注力訓練
        </div>
      </div>
    `;

    // Click handlers
    container.querySelectorAll('.p-card').forEach(el => {
      el.addEventListener('click', () => {
        const id = el.dataset.id;
        // Animate selection
        document.querySelectorAll('.p-card').forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        el.style.transform = 'scale(1.05)';
        setTimeout(() => {
          select(id);
          if (_onSelect) _onSelect(id);
        }, 400);
      });
    });
  }

  /* ── Level grid (with lock overlay) ── */

  function renderLevelGrid(profileId, container) {
    const p = data.profiles[profileId];
    if (!p) return;

    const stageIdx = 0; // Always show stage 1 first
    const stage = STAGES[stageIdx];
    const levels = Array.from({length: 10}, (_, i) => i + 1);

    let html = `<div class="sh" style="margin-top:4px">
      <span style="color:#ffd166">${p.avatar}</span> ${p.name} 的進度
      <span style="font-weight:400;font-size:clamp(11px,1.3vh,14px);color:#9bbfd4;margin-left:8px">
        ⏱ ${formatTime(p.playTime)}
      </span>
    </div>`;
    html += `<div class="lgrid">`;

    for (const level of levels) {
      const key = `${stageIdx + 1}-${level}`;
      const unlocked = isUnlocked(profileId, stageIdx + 1, level);
      const completed = p.completed[key];
      const stars = completed ? completed.stars : 0;
      const isCurrent = unlocked && !completed;

      html += `
        <div class="lcard ${unlocked ? 'l-unlocked' : 'l-locked'} ${isCurrent ? 'l-current' : ''}"
             data-stage="${stageIdx + 1}" data-level="${level}"
             ${unlocked ? '' : 'style="cursor:default"'}
             title="${unlocked ? (completed ? '✅ 已完成' : '▶ 可挑戰') : '🔒 未解鎖'}">
          ${unlocked
            ? `<div style="font-size:clamp(20px,3vw,36px);font-weight:900">${level}</div>`
            : `<div style="font-size:clamp(20px,3vw,36px)">🔒</div>`
          }
          <div style="font-size:clamp(10px,1.2vh,13px);color:#9bbfd4">第${level}關</div>
          ${stars > 0 ? `<div style="font-size:14px">${'⭐'.repeat(stars)}</div>` : ''}
          ${completed ? `<div style="font-size:10px;color:#9bbfd4">${formatTime(completed.time)}</div>` : ''}
          ${isCurrent ? '<div style="font-size:10px;color:#ffd166;margin-top:2px">▶ 進行中</div>' : ''}
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;

    // Click handlers for unlocked levels
    container.querySelectorAll('.l-unlocked').forEach(el => {
      el.addEventListener('click', () => {
        const stage = parseInt(el.dataset.stage);
        const level = parseInt(el.dataset.level);
        if (typeof UI !== 'undefined' && UI.confirmLevel) {
          UI.confirmLevel(stage, level);
        } else {
          startGame(stage, level);
        }
      });
    });
  }

  /* ── Init ── */
  load();

  return {
    load, save, listProfiles, getProfile, getActive, getActiveId,
    select, isUnlocked, markCompleted, getSettings, resetProfile,
    formatTime, getBestRecord, getLeaderboard, checkLeaderboardRank, addLeaderboardEntry,
    onSelect, renderProfileScreen, renderLevelGrid
  };
})();
