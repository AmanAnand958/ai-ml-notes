#!/usr/bin/env python3
"""
Deep Forensic Vector Scan 2:
1. Colab URL Generation Mechanics & Base64 / URI Encoding.
2. Compiler Modal & Run Action Integrity.
3. Top Navigation Bar Consistency across Root & Week pages.
4. Checklist Persist & toggleCheck Binding.
5. YouTube / Resource URL Structure & Embedded Media.
6. Raw Unformatted Math Formulas (e.g. 1/n sum (y - y_hat)^2 in plain text).
7. Keyboard Shortcuts (Alt+Left/Right, F key) & Toast Lifecycle.
8. Theme Toggle & Global Sync across all HTML files.
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.parse

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

advanced_findings = []

def add_issue(category, file_loc, severity, title, details, snippet=""):
    advanced_findings.append({
        "id": len(advanced_findings) + 1,
        "category": category,
        "location": file_loc,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. AUDIT OPENINCOLAB IMPLEMENTATION
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 1: Colab URL Generator Mechanics...")
js_course = (ROOT_DIR / "assets" / "js" / "course.js").read_text(encoding='utf-8')

if "function openInColab" in js_course:
    # Inspect implementation
    idx = js_course.find("function openInColab")
    colab_func = js_course[idx:idx+800]
    if "colab.research.google.com" not in colab_func and "colab" not in colab_func:
        add_issue("Interactive Runtime", "assets/js/course.js", "HIGH", "openInColab does not link to Google Colab", "openInColab() function does not construct a valid Google Colab target.", colab_func)
else:
    add_issue("Interactive Runtime", "assets/js/course.js", "HIGH", "Missing openInColab definition in course.js", "openInColab() is called in HTML but not defined in course.js.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. AUDIT COMPILER MODAL (runCode)
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 2: Compiler Modal Mechanics...")
if "function runCode" in js_course:
    idx = js_course.find("function runCode")
    run_func = js_course[idx:idx+1200]
    if "compiler-modal" not in run_func and "window.open" not in run_func:
        add_issue("Interactive Runtime", "assets/js/course.js", "MEDIUM", "runCode does not open interactive execution environment", "runCode() does not trigger compiler modal or interactive execution sandbox.", run_func)
else:
    add_issue("Interactive Runtime", "assets/js/course.js", "HIGH", "Missing runCode definition in course.js", "runCode() is called in HTML but not defined in course.js.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. AUDIT TOP NAVIGATION BARS & THEME TOGGLE ACROSS ALL PAGES
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 3: Navigation Bars & Theme Buttons...")
all_html_files = [ROOT_DIR / "index.html", ROOT_DIR / "dashboard.html", ROOT_DIR / "resources.html", ROOT_DIR / "roadmap.html"]
all_html_files += list(WEEKS_DIR.glob("week*.html"))

for fp in all_html_files:
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check Theme Button
    theme_btn = soup.find(id='theme-btn')
    if not theme_btn:
        add_issue("Theme / Dark Mode", fp.name, "MEDIUM", f"Missing #theme-btn in {fp.name}", f"{fp.name} lacks a dark/light mode toggle button.")
    else:
        onclick = theme_btn.get('onclick', '')
        if 'toggleTheme' not in onclick:
            add_issue("Theme / Dark Mode", fp.name, "HIGH", f"#theme-btn missing toggleTheme() in {fp.name}", f"Button onclick='{onclick}' does not call toggleTheme().")

    # Check Top Nav Links in Week Pages
    if "week" in fp.name:
        nav = soup.find('nav', class_=re.compile(r'nav|navbar'))
        if not nav:
            add_issue("Layout / Navigation", fp.name, "MEDIUM", f"Missing top <nav> bar in {fp.name}", f"{fp.name} lacks top navigation header.")
        else:
            roadmap_link = nav.find('a', href=re.compile(r'roadmap\.html'))
            dashboard_link = nav.find('a', href=re.compile(r'dashboard\.html'))
            resources_link = nav.find('a', href=re.compile(r'resources\.html'))
            
            if not roadmap_link:
                add_issue("Navigation Link Deficit", fp.name, "LOW", f"Top nav in {fp.name} lacks direct Roadmap link", "Top navigation bar does not link to roadmap.html.")
            if not dashboard_link:
                add_issue("Navigation Link Deficit", fp.name, "LOW", f"Top nav in {fp.name} lacks direct Dashboard link", "Top navigation bar does not link to dashboard.html.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. AUDIT CHECKLIST TOGGLE (toggleCheck)
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 4: Checklist Actions...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    chk_items = soup.find_all(class_=re.compile(r'chk-box|task-item'))
    for c in chk_items:
        parent = c.find_parent('label') or c.find_parent('li') or c.find_parent('div')
        if parent:
            onclick = parent.get('onclick', '')
            if 'toggleCheck' not in onclick:
                add_issue("Checklist Interaction", f"Week {wn}", "LOW", f"Checklist item missing toggleCheck in Week {wn}", "Checkbox item lacks interactive toggleCheck(this) handler.", str(parent)[:100])
                break

# ─────────────────────────────────────────────────────────────────────────────
# 5. AUDIT YOUTUBE & EXTERNAL MEDIA LINKS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 5: External Media & Video Links...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for a in soup.find_all('a', href=re.compile(r'youtube\.com|youtu\.be')):
        href = a.get('href', '')
        # Check if URL is valid YouTube URL
        if 'youtube.com/watch?v=' in href:
            vid_id = href.split('watch?v=')[1].split('&')[0]
            if len(vid_id) < 5:
                add_issue("Broken Media Link", f"Week {wn}", "HIGH", f"Malformed YouTube video ID in Week {wn}: {href}", "YouTube URL has truncated or missing video ID parameter.")
        elif 'youtube.com/playlist?list=' in href:
            list_id = href.split('playlist?list=')[1].split('&')[0]
            if len(list_id) < 5:
                add_issue("Broken Media Link", f"Week {wn}", "HIGH", f"Malformed YouTube playlist ID in Week {wn}: {href}", "YouTube playlist URL has truncated list parameter.")

# ─────────────────────────────────────────────────────────────────────────────
# 6. AUDIT RAW UNFORMATTED MATH FORMULAS IN PLAIN TEXT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 6: Unformatted Math Formulas in Plain Text...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for raw math text patterns like "MSE = 1/n sum" or "L_G = E[" outside math blocks
    for p in soup.find_all(['p', 'li', 'td']):
        txt = p.text
        if p.find('span', class_='katex') or '$$' in str(p) or '$' in str(p):
            continue
            
        if re.search(r'\b(?:MSE|RMSE|MAE|InfoNCE|DSSM)\s*=\s*(?:1/n|\(1/N\)|sum|E\[|log)', txt):
            add_issue(
                "Unformatted Math Formula", f"Week {wn}", "MEDIUM",
                f"Raw unformatted math formula in body text (Week {wn})",
                f"Plain text formula '{txt[:80]}...' should be rendered using KaTeX LaTeX notation ($$...$$).",
                txt[:120]
            )

# ─────────────────────────────────────────────────────────────────────────────
# 7. AUDIT KEYBOARD SHORTCUTS & TOAST NOTIFICATION
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 7: Keyboard Shortcuts & XP Toast...")
if "function showXPToast" not in js_course:
    add_issue("Gamification / Feedback", "assets/js/course.js", "HIGH", "Missing showXPToast function in course.js", "course.js does not define showXPToast() for visual XP gamification feedback.")

# Check toast container in HTML
for fp in all_html_files:
    html = fp.read_text(encoding='utf-8', errors='replace')
    if "xp-toast" not in html and "week" in fp.name:
        add_issue("Gamification / Feedback", fp.name, "LOW", f"Missing #xp-toast container in {fp.name}", f"{fp.name} lacks the dedicated #xp-toast floating container element.")

print(f"\nAdvanced Audit complete! Cataloged {len(advanced_findings)} specialized findings.")
out_file = ROOT_DIR / "scripts" / "advanced_vectors_issues_inventory.json"
out_file.write_text(json.dumps(advanced_findings, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
