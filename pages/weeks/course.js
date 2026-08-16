window.mermaidConfig = { startOnLoad: false, suppressErrorRendering: false };
/**
 * ═══════════════════════════════════════════════════════════════════
 *  CANONICAL COURSE STATE & GAMIFICATION ENGINE (assets/js/course.js)
 *  Single Source of Truth, Resilient State, Multi-Tab Safe, Accessible
 * ═══════════════════════════════════════════════════════════════════
 */

// ── 1. GLOBAL CANONICAL STATE ──────────────────────────────────────
const STATE_SCHEMA_VERSION = 2;

let courseState = {
  version: STATE_SCHEMA_VERSION,
  xp: 0,
  streak: 0,
  lastDate: '',
  completedDays: {},    // Map of 'day-id': { xpAwarded: 150, timestamp: 123456789 }
  answeredQuizzes: {},  // Map of 'qid': { chosen: 'A', correct: true, timestamp: 123456789 }
  lastUpdated: Date.now()
};

// Legacy backward-compatibility proxy
let state = {
  xp: 0,
  streak: 0,
  done: [],
  lastDate: ''
};

// ── 2. STATE STORAGE & RESILIENCE ─────────────────────────────────
function getStorageKey() {
  return typeof WEEK !== 'undefined' ? `w${WEEK}-state` : 'global-course-state';
}

function loadState() {
  const key = getStorageKey();
  try {
    const raw = localStorage.getItem(key);
    if (!raw) {
      initFreshState();
      return;
    }
    const parsed = JSON.parse(raw);
    
    // Schema migration & validation
    if (parsed && typeof parsed === 'object') {
      courseState.xp = typeof parsed.xp === 'number' && !isNaN(parsed.xp) ? Math.max(0, parsed.xp) : 0;
      courseState.streak = typeof parsed.streak === 'number' && !isNaN(parsed.streak) ? Math.max(0, parsed.streak) : 0;
      courseState.lastDate = typeof parsed.lastDate === 'string' ? parsed.lastDate : '';
      
      // Migrate array 'done' -> object 'completedDays'
      if (Array.isArray(parsed.done)) {
        parsed.done.forEach(d => {
          const did = String(d);
          courseState.completedDays[did] = { xpAwarded: 150, timestamp: Date.now() };
        });
      } else if (parsed.completedDays && typeof parsed.completedDays === 'object') {
        courseState.completedDays = parsed.completedDays;
      }
      
      if (parsed.answeredQuizzes && typeof parsed.answeredQuizzes === 'object') {
        courseState.answeredQuizzes = parsed.answeredQuizzes;
      }
      courseState.lastUpdated = parsed.lastUpdated || Date.now();
    }
  } catch (err) {
    console.warn('⚠️ LocalStorage state corrupted or unavailable. Initializing safe fallback:', err);
    initFreshState();
  }
  syncLegacyStateProxy();
}

function initFreshState() {
  courseState.xp = 0;
  courseState.streak = 0;
  courseState.lastDate = '';
  courseState.completedDays = {};
  courseState.answeredQuizzes = {};
  courseState.lastUpdated = Date.now();
}

function syncLegacyStateProxy() {
  state.xp = courseState.xp;
  state.streak = courseState.streak;
  state.done = Object.keys(courseState.completedDays);
  state.lastDate = courseState.lastDate;
}

function saveState() {
  syncLegacyStateProxy();
  courseState.lastUpdated = Date.now();
  const key = getStorageKey();
  try {
    localStorage.setItem(key, JSON.stringify(courseState));
    return true;
  } catch (err) {
    console.error('❌ Failed to persist course state to LocalStorage:', err);
    showPersistenceErrorWarning();
    return false;
  }
}

function showPersistenceErrorWarning() {
  let toast = document.getElementById('persistence-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'persistence-toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.style.cssText = 'position:fixed; bottom:20px; right:20px; background:#e56b8c; color:#fff; padding:12px 18px; border-radius:8px; z-index:99999; font-weight:700; box-shadow:0 4px 12px rgba(0,0,0,0.4);';
    document.body.appendChild(toast);
  }
  toast.textContent = '⚠️ Storage quota exceeded. Progress kept in-memory for this session.';
  setTimeout(() => { if (toast) toast.remove(); }, 5000);
}

// Multi-Tab Synchronization
window.addEventListener('storage', (e) => {
  if (e.key === getStorageKey() && e.newValue) {
    try {
      const incoming = JSON.parse(e.newValue);
      if (incoming && incoming.lastUpdated > courseState.lastUpdated) {
        courseState = incoming;
        syncLegacyStateProxy();
        syncUI();
      }
    } catch (err) {}
  }
});

// ── 3. CANONICAL DAY COMPLETION (Single Source of Truth) ───────────
function completeDay(dayIdentifier, inlineXp) {
  const dayStr = String(dayIdentifier);
  
  if (courseState.completedDays[dayStr]) {
    console.log(`ℹ️ Day ${dayStr} already completed. No duplicate XP awarded.`);
    return;
  }
  
  let canonicalXp = 150;
  const dayElem = document.getElementById('day-' + dayStr) || document.getElementById(dayStr);
  if (dayElem && dayElem.getAttribute('data-xp')) {
    const parsedXp = parseInt(dayElem.getAttribute('data-xp'), 10);
    if (!isNaN(parsedXp) && parsedXp > 0) {
      canonicalXp = parsedXp;
    }
  } else if (typeof inlineXp === 'number' && !isNaN(inlineXp)) {
    canonicalXp = inlineXp;
  }
  
  courseState.completedDays[dayStr] = {
    xpAwarded: canonicalXp,
    timestamp: Date.now()
  };
  courseState.xp += canonicalXp;
  
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - 86400000).toDateString();
  if (courseState.lastDate !== today) {
    if (courseState.lastDate === yesterday) {
      courseState.streak++;
    } else {
      courseState.streak = 1;
    }
    courseState.lastDate = today;
  }
  
  saveState();
  syncUI();
  showXPToast(canonicalXp, dayStr);
  
  const btn = document.getElementById('btn-day-' + dayStr) || document.getElementById('btn-' + dayStr);
  if (btn) {
    btn.classList.add('done');
    btn.setAttribute('aria-pressed', 'true');
    btn.textContent = dayStr === 'toolkit' ? '✓ Toolkit Complete' : `✓ Day ${dayStr} Complete (+${canonicalXp} XP)`;
  }
  
  triggerConfetti();
}

// ── 4. QUIZ STATE MACHINE & IDEMPOTENT XP ─────────────────────────
function quiz(optEl, result, qid) {
  if (!optEl) return;
  const block = optEl.closest('.quiz-block') || optEl.closest('.quiz-card') || optEl.closest('[id^="quiz-"]');
  if (!block) return;
  
  const questionId = qid || block.id || optEl.getAttribute('data-qid') || 'q_' + Math.random().toString(36).substring(2, 8);
  
  if (courseState.answeredQuizzes[questionId]) {
    console.log(`ℹ️ Question ${questionId} already answered.`);
    return;
  }
  
  const isRight = (result === 'correct' || result === 'right');
  
  block.querySelectorAll('.quiz-opt, button.quiz-option').forEach(o => {
    o.setAttribute('disabled', 'true');
    o.style.pointerEvents = 'none';
    if (o !== optEl) o.classList.add('dimmed');
  });
  
  optEl.classList.add(isRight ? 'correct' : 'wrong');
  const letter = optEl.querySelector('.quiz-letter');
  if (letter) letter.textContent = isRight ? '✓' : '✗';
  
  courseState.answeredQuizzes[questionId] = {
    correct: isRight,
    timestamp: Date.now()
  };
  
  const fb = block.querySelector('.quiz-feedback') || block.querySelector('.correct-fb') || block.querySelector('.wrong-fb');
  if (fb) {
    fb.style.display = 'block';
    fb.setAttribute('aria-live', 'polite');
  }
  
  saveState();
}

// ── 5. ACCESSIBLE COMPILER MODAL & CODE CONTROLS ──────────────────
let lastFocusedElement = null;

function copyCode(btn) {
  const cb = btn.closest('.cb') || btn.closest('.solution-box') || btn.closest('.task-block');
  const codeElem = cb ? (cb.querySelector('code') || cb.querySelector('pre')) : null;
  if (!codeElem) return;
  
  const originalText = btn.textContent;
  const cleanCode = codeElem.innerText || codeElem.textContent;
  
  navigator.clipboard.writeText(cleanCode).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = originalText; }, 1500);
  }).catch(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = originalText; }, 1500);
  });
}

function openInColab(btn) {
  copyCode(btn);
  showToast('⚡ Code copied to clipboard! Opening Google Colab...');
  setTimeout(() => {
    window.open('https://colab.research.google.com/#create=true', '_blank', 'noopener,noreferrer');
  }, 400);
}

function runCode(btn) {
  copyCode(btn);
  showCompilerModal();
}

function showCompilerModal() {
  lastFocusedElement = document.activeElement;
  let modal = document.getElementById('compiler-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'compiler-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-labelledby', 'compiler-modal-title');
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(13, 15, 20, 0.88); backdrop-filter: blur(8px);
      z-index: 10000; display: flex; align-items: center; justify-content: center;
    `;
    modal.innerHTML = `
      <div style="background:#161922; border:1px solid rgba(255,255,255,0.15); border-radius:12px; padding:2rem; max-width:520px; width:90%; box-shadow:0 20px 40px rgba(0,0,0,0.6); position:relative;">
        <h3 id="compiler-modal-title" style="margin:0 0 1rem; color:#4fd1a5; font-size:1.3rem;">⚡ Online Python Environment</h3>
        <p style="color:#a0aec0; font-size:14px; line-height:1.6; margin-bottom:1.5rem;">Code copied to clipboard! Execute in your preferred interactive environment:</p>
        <div style="display:flex; flex-direction:column; gap:0.75rem;">
          <a href="https://colab.research.google.com/#create=true" target="_blank" rel="noopener" style="display:block; text-align:center; background:#f7a94b; color:#000; font-weight:700; padding:10px 16px; border-radius:8px; text-decoration:none;">🚀 Open Google Colab</a>
          <a href="https://replit.com/new/python3" target="_blank" rel="noopener" style="display:block; text-align:center; background:rgba(255,255,255,0.08); color:#e2e8f0; font-weight:600; padding:10px 16px; border-radius:8px; text-decoration:none;">🐍 Open Replit (Python 3.11)</a>
        </div>
        <button id="modal-close-btn" onclick="closeCompilerModal()" style="margin-top:1.5rem; width:100%; background:transparent; border:1px solid rgba(255,255,255,0.2); color:#fff; padding:8px; border-radius:6px; cursor:pointer;">Close</button>
      </div>
    `;
    document.body.appendChild(modal);
  }
  modal.style.display = 'flex';
  const closeBtn = document.getElementById('modal-close-btn');
  if (closeBtn) closeBtn.focus();
  
  modal.onkeydown = function(e) {
    if (e.key === 'Escape') closeCompilerModal();
  };
}

function closeCompilerModal() {
  const modal = document.getElementById('compiler-modal');
  if (modal) modal.style.display = 'none';
  if (lastFocusedElement) lastFocusedElement.focus();
}

// ── 6. UI SYNCHRONIZATION (DOM ID Harmonization) ──────────────────
function syncUI() {
  ['xp-show', 'sb-xp', 'nav-xp', 'stat-xp'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = `⚡ ${courseState.xp} XP`;
  });
  
  ['streak-show', 'sb-streak', 'nav-streak', 'stat-streak'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = `🔥 ${courseState.streak} day streak`;
  });
  
  const lvlEl = document.getElementById('level-show') || document.getElementById('user-level');
  if (lvlEl) lvlEl.textContent = getLevel(courseState.xp);
  
  const completedCount = Object.keys(courseState.completedDays).length;
  const totalDays = (typeof DAYS !== 'undefined' && Array.isArray(DAYS)) ? DAYS.length : 7;
  const pct = Math.min(100, Math.round((completedCount / totalDays) * 100));
  
  const progFill = document.getElementById('progress-fill') || document.getElementById('prog-bar') || document.querySelector('.prog-bar');
  if (progFill) {
    progFill.style.width = `${pct}%`;
    progFill.setAttribute('aria-valuenow', pct);
  }
  
  const progText = document.getElementById('progress-pct') || document.getElementById('prog-text') || document.querySelector('.prog-text');
  if (progText) {
    progText.textContent = `${pct}% (${completedCount}/${totalDays} days)`;
  }
  
  Object.keys(courseState.completedDays).forEach(dayId => {
    const btn = document.getElementById('btn-day-' + dayId) || document.getElementById('btn-' + dayId);
    if (btn) {
      btn.classList.add('done');
      btn.setAttribute('aria-pressed', 'true');
      btn.textContent = dayId === 'toolkit' ? '✓ Toolkit Complete' : `✓ Day ${dayId} Complete`;
    }
    const pill = document.querySelector(`.day-pill[data-day="${dayId}"]`);
    if (pill) pill.classList.add('done');
  });
}

function getLevel(xp) {
  if (xp >= 5000) return '🏆 ML Architect';
  if (xp >= 3000) return '🚀 Senior Engineer';
  if (xp >= 1500) return '⚡ Applied Practitioner';
  if (xp >= 500)  return '🌱 Junior ML Dev';
  return '🐣 Novice Explorer';
}

function showXPToast(amount, day) {
  let toast = document.getElementById('xp-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'xp-toast';
    toast.className = 'xp-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
  }
  toast.textContent = `+${amount} XP ⚡ (Day ${day} Completed!)`;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function showToast(msg) {
  let toast = document.getElementById('action-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'action-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.style.cssText = 'position:fixed; bottom:24px; left:50%; transform:translateX(-50%); background:#2d3748; color:#fff; padding:10px 20px; border-radius:8px; z-index:99999; font-size:14px; font-weight:600; box-shadow:0 10px 25px rgba(0,0,0,0.5);';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => { if (toast) toast.style.display = 'none'; }, 2500);
}

// ── 7. DAY NAVIGATION & ACCESSIBILITY ──────────────────────────────
function goDay(dayId) {
  document.querySelectorAll('.day-section').forEach(sec => {
    sec.classList.remove('active');
    sec.style.display = 'none';
  });
  document.querySelectorAll('.sb-item').forEach(item => item.classList.remove('active'));
  document.querySelectorAll('.day-pill').forEach(pill => pill.classList.remove('active'));
  
  const targetSec = document.getElementById('day-' + dayId) || document.getElementById(dayId);
  const targetPill = document.querySelector(`.day-pill[data-day="${dayId}"]`);
  
  if (targetSec) {
    targetSec.classList.add('active');
    targetSec.style.display = 'block';
  }
  if (targetPill) targetPill.classList.add('active');
  
  const sbBtn = Array.from(document.querySelectorAll('.sb-item')).find(el => el.getAttribute('onclick') && el.getAttribute('onclick').includes('goDay(' + dayId + ')'));
  if (sbBtn) sbBtn.classList.add('active');
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
  renderMermaid('day-' + dayId);
}

function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  if (sb) sb.classList.toggle('open');
}

function closeSidebar() {
  const sb = document.getElementById('sidebar');
  if (sb) sb.classList.remove('open');
}

function toggleTask(headerEl) {
  const body = headerEl.nextElementSibling;
  if (!body) return;
  const isHidden = body.style.display === 'none' || !body.style.display;
  body.style.display = isHidden ? 'block' : 'none';
  headerEl.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
}

function toggleSolution(arg1, arg2) {
  let sol = null;
  let btn = null;
  
  if (typeof arg1 === 'string') {
    sol = document.getElementById(arg1);
    btn = arg2 || (window.event ? window.event.target : null);
  } else if (arg1 && arg1.nodeType) {
    btn = arg1;
    sol = btn.nextElementSibling || (btn.parentElement ? btn.parentElement.querySelector('.solution-block, .solution, pre, .cb') : null);
  }
  
  if (!sol && btn && btn.nextElementSibling) {
    sol = btn.nextElementSibling;
  }
  
  if (!sol) return;
  const isHidden = (window.getComputedStyle(sol).display === 'none' || sol.style.display === 'none');
  sol.style.display = isHidden ? 'block' : 'none';
  if (btn) {
    btn.textContent = isHidden ? '🙈 Hide Solution' : '👁️ Show Solution';
    btn.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
  }
}

function checkPredict(arg1, arg2) {
  let input = null;
  let result = null;
  let answer = arg2;

  if (typeof arg1 === 'string') {
    input = document.getElementById(arg1 + '-input') || document.getElementById(arg1);
    result = document.getElementById(arg1 + '-result') || document.getElementById(arg1 + '-feedback') || document.getElementById(arg1);
  } else if (arg1 && arg1.nodeType) {
    const parent = arg1.closest('.predict-box') || arg1.closest('.predict-block') || arg1.closest('.task-block') || arg1.parentElement;
    input = parent ? parent.querySelector('input') : null;
    result = parent ? (parent.querySelector('.predict-result') || parent.querySelector('.predict-feedback') || parent.querySelector('.result')) : null;
  }

  if (!input || !result) return;
  if (result.dataset && result.dataset.solved === 'true') return;

  const normalize = (str) => {
    return String(str || '')
      .replace(/\r\n|\r|\n/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  };

  const userVal = normalize(input.value);
  const correctVal = normalize(answer);
  const rawUser = input.value.trim().toLowerCase();
  const rawExp = String(answer || '').trim().toLowerCase();

  const isCorrect = (userVal === correctVal) || (rawUser === rawExp) || (correctVal.length > 0 && userVal.includes(correctVal));

  result.style.display = 'block';
  if (isCorrect) {
    if (result.dataset) result.dataset.solved = 'true';
    input.disabled = true;
    result.style.background = 'rgba(79,209,165,.1)';
    result.style.border = '1px solid rgba(79,209,165,.3)';
    result.style.color = 'var(--green, #4fd1a5)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '✅ Correct! ' + String(answer).replace(/\n/g, ' ');

    if (typeof courseState !== 'undefined') {
      courseState.awardXP(10, 'prediction');
    } else if (typeof state !== 'undefined') {
      state.xp = (state.xp || 0) + 10;
      if (typeof saveState === 'function') saveState();
      if (typeof syncUI === 'function') syncUI();
      if (typeof showXPToast === 'function') showXPToast(10, 'prediction');
    }
  } else {
    result.style.background = 'rgba(229,107,140,.08)';
    result.style.border = '1px solid rgba(229,107,140,.3)';
    result.style.color = 'var(--pink, #e56b8c)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '❌ Expected: ' + String(answer).replace(/\n/g, ' ') + ' — try again';
  }
}

function triggerConfetti() {
  console.log('🎉 Milestone celebration triggered!');
}

// ── 8. MERMAID RENDERING ENGINE (Mermaid v10) ──

// Seed all .mermaid sources into data-diagram-src BEFORE any rendering touches the DOM.
// Must run once on page load while textContent is still the raw diagram code.
function seedMermaidSources() {
  document.querySelectorAll('.mermaid').forEach(node => {
    if (!node.getAttribute('data-diagram-src')) {
      const raw = (node.textContent || '').trim()
        .replace(/&gt;/g, '>').replace(/&lt;/g, '<')
        .replace(/&amp;/g, '&').replace(/&quot;/g, '"');
      if (raw) {
        node.setAttribute('data-diagram-src', raw);
      }
    }
  });
}

function renderMermaid(dayId) {
  let retries = 0;
  const attempt = () => {
    if (typeof mermaid === 'undefined' || typeof mermaid.render !== 'function') {
      retries++;
      if (retries < 50) setTimeout(attempt, 100);
      return;
    }

    let sec = null;
    if (dayId) {
      sec = document.getElementById(dayId) || document.getElementById('day-' + dayId);
    }
    if (!sec) {
      sec = document.querySelector('.day-section.active') || document.querySelector('.day-section');
    }
    if (!sec) return;

    const mermaidNodes = Array.from(sec.querySelectorAll('.mermaid'));
    if (!mermaidNodes.length) return;

    mermaidNodes.forEach((node, idx) => {
      // Skip already rendered
      if (node.querySelector('svg') && node.getAttribute('data-rendered') === '1') return;

      // ONLY read from the pre-seeded attribute — never from textContent after load
      const src = node.getAttribute('data-diagram-src');
      if (!src || !src.trim()) return;

      const uid = 'mdiag' + Date.now() + idx;
      try {
        mermaid.render(uid, src.trim()).then(({ svg, bindFunctions }) => {
          node.innerHTML = svg;
          if (typeof bindFunctions === 'function') bindFunctions(node);
          node.setAttribute('data-rendered', '1');
          const svgEl = node.querySelector('svg');
          if (svgEl) {
            svgEl.style.maxWidth = '100%';
            svgEl.style.height = 'auto';
          }
          document.querySelectorAll(
            'body > [id^="mermaid-"], body > [id^="dmermaid-"], body > div.error-icon'
          ).forEach(el => el.remove());
        }).catch(err => {
          console.warn('[Mermaid] render error diagram', idx, ':', err.message || err);
        });
      } catch(err) {
        console.error('[Mermaid] render threw:', err);
      }
    });
  };

  setTimeout(attempt, 80);
}

// ── 9. INITIALIZATION ON DOM READY ────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // FIRST: cache all diagram sources while textContent is still raw
  seedMermaidSources();

  loadState();
  syncUI();
  
  // Render first active day
  const activeSec = document.querySelector('.day-section.active') || document.querySelector('.day-section');
  if (activeSec) {
    renderMermaid(activeSec.id);
  } else {
    renderMermaid();
  }
  
  document.querySelectorAll('.day-pill').forEach(pill => {
    pill.addEventListener('click', (e) => {
      e.preventDefault();
      const did = pill.getAttribute('data-day');
      if (did) goDay(did);
    });
  });
});


// ── 10. GLOBAL INTERACTIVE UTILITIES & EVENT HANDLERS ──────────────

window.jumpTo = function(dayId) {
  if (!dayId) return;
  const targetId = dayId.startsWith('day-') ? dayId : 'day-' + dayId;
  const target = document.getElementById(targetId) || document.getElementById(dayId);
  if (target) {
    if (typeof window.goDay === 'function') {
      window.goDay(target.id.replace('day-', ''));
    }
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

window.toggleTheme = function() {
  const isLight = document.documentElement.classList.toggle('light-theme') || document.body.classList.toggle('light-theme');
  localStorage.setItem('course_theme_preference', isLight ? 'light' : 'dark');
  if (typeof showToast === 'function') {
    showToast(isLight ? '☀️ Light mode enabled' : '🌙 Dark mode enabled');
  }
};

window.openRepl = function(codeSnippet) {
  if (typeof copyCode === 'function') {
    navigator.clipboard.writeText(codeSnippet || '').then(() => {
      if (typeof showToast === 'function') {
        showToast('📋 Code copied to clipboard for REPL execution!');
      }
    }).catch(() => {
      alert('Code snippet:\n\n' + codeSnippet);
    });
  }
};

window.toggleCheck = function(taskId) {
  const el = document.getElementById(taskId);
  if (el) {
    el.classList.toggle('checked');
  }
};

window.initKaTeX = function() {
  if (typeof renderMathInElement === 'function') {
    try {
      renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false },
          { left: '\\[', right: '\\]', display: true }
        ],
        throwOnError: false,
        strict: false,
        ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
        ignoredClasses: ['mermaid', 'cb', 'code-block']
      });
    } catch(e) {
      console.warn('KaTeX auto-render error:', e);
    }
  }
};

// Auto-run KaTeX when script is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', window.initKaTeX);
} else {
  window.initKaTeX();
}


// Active cleanup of any rogue mermaid error nodes
setInterval(() => {
  document.querySelectorAll('body > [id^="mermaid-"], body > [id^="dmermaid-"], div.error-icon').forEach(el => el.remove());
}, 500);


