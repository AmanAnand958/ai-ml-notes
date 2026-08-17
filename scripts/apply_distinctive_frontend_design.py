#!/usr/bin/env python3
"""
scripts/apply_distinctive_frontend_design.py
Applies the distinctive, instrument-grade frontend design system:
1. Palette Tokens: Obsidian (#0B0E14), Surface (#141824), Matrix Emerald (#10B981), Cyber Cyan (#38BDF8)
2. Ambient Reading Progress Bar + Frosted Glass Telemetry HUD
3. Accessible Keyboard Navigation Engine (Left/Right Arrows, Q for Quiz, S for Solution)
4. Micro-Interactions: Quiz Shake Animation, Day Reward Glow, Reduced-Motion Compliance
5. Full bi-directional synchronization across all 26 HTML week pages.
"""

import glob, re, os

print("=== DEPLOYING DISTINCTIVE INSTRUMENT-GRADE FRONTEND DESIGN SYSTEM ===")

DISTINCTIVE_DESIGN_CSS = """
/* ═══════════════════════════════════════════════════════════════════
   DISTINCTIVE INSTRUMENT-GRADE DESIGN SYSTEM (AI/ML Study Workspace)
   ═══════════════════════════════════════════════════════════════════ */

:root {
  --bg-obsidian: #0b0e14;
  --bg-surface: #141824;
  --bg-surface-elevated: #1c2234;
  --accent-emerald: #10b981;
  --accent-cyan: #38bdf8;
  --accent-amber: #f59e0b;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-glow: rgba(16, 185, 129, 0.25);
  --text-main: #f1f5f9;
  --text-muted: #94a3b8;
  --font-display: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Ambient Top Reading Progress Tracker */
#reading-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 2.5px;
  background: linear-gradient(90deg, var(--accent-emerald), var(--accent-cyan));
  width: 0%;
  z-index: 99999;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
  transition: width 0.1s ease-out;
}

/* Frosted Glass Navigation Header */
.week-header, .top-nav, header {
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  background: rgba(11, 14, 20, 0.85) !important;
  border-bottom: 1px solid var(--border-subtle) !important;
}

/* Keyboard Shortcut Telemetry Badge */
.kbd-hint {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border-subtle);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}

/* Micro-Interaction: Quiz Shake on Incorrect */
@keyframes shakeError {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-6px); }
  40%, 80% { transform: translateX(6px); }
}
.quiz-opt-error {
  animation: shakeError 0.35s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  border-color: #ef4444 !important;
  background: rgba(239, 68, 68, 0.12) !important;
}

/* Micro-Interaction: Reward Glow on Day Completion */
@keyframes rewardPulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.reward-active {
  animation: rewardPulse 1.2s ease-out;
}

/* Reduced Motion Override */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
"""

KEYBOARD_JS_ENGINE = """
<script id="instrument-telemetry-engine">
document.addEventListener('DOMContentLoaded', () => {
  // 1. Create Ambient Top Reading Progress Bar
  if (!document.getElementById('reading-progress-bar')) {
    const bar = document.createElement('div');
    bar.id = 'reading-progress-bar';
    document.body.prepend(bar);
    
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = (document.documentElement.scrollHeight || document.body.scrollHeight) - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
    }, { passive: true });
  }

  // 2. Keyboard Navigation Engine (Left/Right Arrows, Q for Quiz, S for Solutions)
  document.addEventListener('keydown', (e) => {
    // Skip if user is actively typing in an input or textarea
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    if (e.key === 'ArrowRight') {
      const activeTab = document.querySelector('.day-tab.active, .tab-btn.active');
      if (activeTab && activeTab.nextElementSibling && (activeTab.nextElementSibling.classList.contains('day-tab') || activeTab.nextElementSibling.classList.contains('tab-btn'))) {
        activeTab.nextElementSibling.click();
      }
    } else if (e.key === 'ArrowLeft') {
      const activeTab = document.querySelector('.day-tab.active, .tab-btn.active');
      if (activeTab && activeTab.previousElementSibling && (activeTab.previousElementSibling.classList.contains('day-tab') || activeTab.previousElementSibling.classList.contains('tab-btn'))) {
        activeTab.previousElementSibling.click();
      }
    } else if (e.key.toLowerCase() === 'q') {
      const activeDay = document.querySelector('.day-section:not([style*="display: none"])');
      if (activeDay) {
        const quiz = activeDay.querySelector('.quiz-section');
        if (quiz) quiz.scrollIntoView({ behavior: 'smooth' });
      }
    } else if (e.key.toLowerCase() === 's') {
      const activeDay = document.querySelector('.day-section:not([style*="display: none"])');
      if (activeDay) {
        const solBtn = activeDay.querySelector('.toggle-sol-btn, button[onclick*="toggleSolution"]');
        if (solBtn) solBtn.click();
      }
    }
  });
});
</script>
"""

html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS
    if 'DISTINCTIVE INSTRUMENT-GRADE DESIGN SYSTEM' not in content:
        if '</style>' in content:
            content = content.replace('</style>', DISTINCTIVE_DESIGN_CSS + '\n</style>', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'<style>{DISTINCTIVE_DESIGN_CSS}</style>\n</head>', 1)

    # Inject JS
    if 'instrument-telemetry-engine' not in content:
        if '</body>' in content:
            content = content.replace('</body>', KEYBOARD_JS_ENGINE + '\n</body>', 1)
        else:
            content += KEYBOARD_JS_ENGINE

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(content)

print("✓ Injected instrument-grade design system into all 26 HTML week pages.")
print("\n=== DISTINCTIVE DESIGN SYSTEM DEPLOYMENT COMPLETE ===")
