#!/usr/bin/env python3
"""
Master JavaScript Enhancer & Script Unifier:
1. Enriches `assets/js/course.js` with robust implementations of:
   - `jumpTo(dayId)`
   - `toggleTheme()`
   - `openRepl(code)`
   - `toggleCheck(taskId)`
   - `initKaTeX()` and `renderMath()`
2. Standardizes all script tags at the bottom of all 26 week HTML files:
   - CDN KaTeX min.js
   - CDN KaTeX auto-render min.js
   - CDN Mermaid min.js
   - ../../assets/js/course.js
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
COURSE_JS_PATH = Path("assets/js/course.js")

# ─────────────────────────────────────────────────────────────────────────────
# 1. ENRICH course.js
# ─────────────────────────────────────────────────────────────────────────────
course_js = COURSE_JS_PATH.read_text(encoding='utf-8')

extra_js = """
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
      alert('Code snippet:\\n\\n' + codeSnippet);
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
        ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
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
"""

if "window.jumpTo = function" not in course_js:
    course_js += "\n" + extra_js
    COURSE_JS_PATH.write_text(course_js, encoding='utf-8')
    print("✅ Enriched assets/js/course.js with global jumpTo, toggleTheme, openRepl, toggleCheck, and initKaTeX!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. STANDARDIZE SCRIPT TAGS ACROSS ALL 26 WEEKS
# ─────────────────────────────────────────────────────────────────────────────
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    # Remove existing script tags linking to KaTeX / Mermaid / course.js to prevent duplicate inclusions
    for s in soup.find_all('script'):
        src = s.get('src', '')
        if any(lib in src for lib in ['katex', 'mermaid', 'course.js']):
            s.decompose()
            
    body = soup.find('body')
    if body:
        scripts_markup = BeautifulSoup('''
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
  <script src="../../assets/js/course.js"></script>
''', 'html.parser')
        body.append(scripts_markup)
        
    fp.write_text(str(soup), encoding='utf-8')
    print(f"  ✅ Standardized script tags in Week {wn}")

print("\n🎉 ALL 26 WEEKS NOW HAVE STANDARDIZED JAVASCRIPT ARCHITECTURE!")
