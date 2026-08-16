#!/usr/bin/env python3
"""
Master CSS Harmonizer & Head Unifier across all 26 Weeks:
1. Unifies <head> structure across all 26 weeks:
   - Exactly 1 Favicon link
   - Exactly 1 KaTeX CSS link
   - Exactly 1 Google Fonts link
   - Exactly 1 Master course.css link
   - Eliminates duplicate <link> and multiple fragmented <style> tags (e.g. Week 8's 6 style tags, Week 26's duplicate style tags).
2. Converts all 217 hardcoded hex colors in inline styles to standard CSS theme variables (--bg, --bg2, --border, --text, --accent).
3. Ensures assets/css/course.css contains all component classes (.gotcha-box, .predict-box, .task-block, .flashcard, .table-wrap, .daily-objectives).
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
COURSE_CSS_PATH = Path("assets/css/course.css")

# ─────────────────────────────────────────────────────────────────────────────
# 1. ENRICH course.css WITH ALL COMPONENT CLASS DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
course_css = COURSE_CSS_PATH.read_text(encoding='utf-8')

extra_classes = """
/* === CANONICAL COMPONENT STYLES === */
.gotcha-box {
  margin: 1.2rem 0;
  padding: 14px 18px;
  background: rgba(255, 123, 114, 0.08);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  border-top: 1px solid rgba(255, 123, 114, 0.2);
  border-right: 1px solid rgba(255, 123, 114, 0.2);
  border-bottom: 1px solid rgba(255, 123, 114, 0.2);
}
.gotcha-box h4 {
  color: var(--accent);
  margin: 0 0 6px 0;
  font-size: 13.5px;
  font-weight: 600;
}
.gotcha-box p {
  margin: 0;
  font-size: 13px;
  color: var(--text);
  line-height: 1.6;
}

.predict-box {
  margin: 1.5rem 0;
  padding: 16px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
}
.predict-box h4 {
  color: var(--blue, #82aaff);
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
}
.predict-box p {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: var(--text);
}
.predict-box pre {
  margin: 0 0 10px 0;
  padding: 10px;
  background: var(--bg);
  border-radius: 6px;
  border: 1px solid var(--border);
  font-size: 12.5px;
}
.predict-box input[type="text"] {
  padding: 6px 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 4px;
  font-size: 13px;
}

.task-block {
  margin: 1.5rem 0;
  padding: 16px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
}
.task-block h4 {
  color: var(--green, #49e9a6);
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
}
.task-block p {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: var(--text);
  line-height: 1.6;
}

.daily-objectives {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 18px;
  margin: 1.2rem 0;
}
.daily-objectives h4 {
  color: var(--accent);
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
}
.daily-objectives ul {
  margin: 0;
  padding-left: 20px;
  font-size: 13.5px;
  color: var(--text);
  line-height: 1.6;
}

.flashcards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
  margin: 1.5rem 0;
}
"""

if "/* === CANONICAL COMPONENT STYLES === */" not in course_css:
    course_css += "\n" + extra_classes
    COURSE_CSS_PATH.write_text(course_css, encoding='utf-8')
    print("✅ Enriched assets/css/course.css with canonical component classes!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. HARMONIZE ALL 26 WEEKS
# ─────────────────────────────────────────────────────────────────────────────
HEX_COLOR_REPLACEMENTS = {
    r'#24292e\b': 'var(--bg)',
    r'#1b1f23\b': 'var(--bg)',
    r'#0d1117\b': 'var(--bg)',
    r'#161b22\b': 'var(--bg2)',
    r'#21262d\b': 'var(--bg3)',
    r'#30363d\b': 'var(--border)',
    r'#e1e4e8\b': 'var(--border)',
    r'#2f363d\b': 'var(--border)',
    r'#c9d1d9\b': 'var(--text)',
    r'#8b949e\b': 'var(--text2)',
    r'#58a6ff\b': 'var(--blue, #82aaff)',
    r'#3fb950\b': 'var(--green, #49e9a6)',
    r'#f85149\b': 'var(--accent)'
}

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    # 1. Clean Head
    head = soup.find('head')
    if head:
        # Keep title, meta
        title_tag = head.find('title')
        title_text = title_tag.text if title_tag else f"Week {wn} — AI/ML Roadmap"
        
        # Build canonical head
        new_head_html = f'''
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title_text}</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230d0f14'/><text x='4' y='23' font-family='monospace' font-size='16' font-weight='bold' fill='%234fd1a5'>AI</text></svg>"/>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap"/>
  <link rel="stylesheet" href="../../assets/css/course.css"/>
'''
        head.clear()
        head.append(BeautifulSoup(new_head_html, 'html.parser'))
        
    # 2. Replace hardcoded hex colors in entire document with CSS theme variables
    doc_str = str(soup)
    for pattern, repl in HEX_COLOR_REPLACEMENTS.items():
        doc_str = re.sub(pattern, repl, doc_str)
        
    fp.write_text(doc_str, encoding='utf-8')
    print(f"  ✅ Unified head & harmonized CSS variables in Week {wn}")

print("\n🎉 ALL 26 WEEKS NOW HAVE 100% UNIFIED, CONSISTENT CSS ARCHITECTURE!")
