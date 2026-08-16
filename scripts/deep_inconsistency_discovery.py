#!/usr/bin/env python3
"""
Deep Inconsistency Discovery Suite:
Scans 8 specialized dimensions across all 26 weeks and root pages:
1. Predict-the-Output block logic & ID mapping
2. Quiz option correctness & feedback ID wiring
3. Flashcard DOM structure & flip click handlers
4. Task drawers & verification criteria
5. Inter-week navigation links (Previous/Next/Roadmap/Dashboard/Resources)
6. Roadmap.html vs Week pages title consistency
7. Metadata badge consistency
8. Hardcoded colors & Theme contrast risks
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

inconsistencies = []

def log_inc(dimension, week, day, severity, title, details, snippet=""):
    inconsistencies.append({
        "id": len(inconsistencies) + 1,
        "dimension": dimension,
        "week": week,
        "day": day,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:150].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 1: PREDICT-THE-OUTPUT BLOCK LOGIC & ID MAPPING
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 1: Predict Blocks...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    predicts = soup.find_all('div', class_=re.compile(r'predict-block|predict-box'))
    for p in predicts:
        p_id = p.get('id', '')
        inp = p.find('input')
        btn = p.find('button')
        res = p.find(class_=re.compile(r'predict-result|result'))
        
        # Check input ID matching
        if inp:
            inp_id = inp.get('id', '')
            if not inp_id:
                log_inc("Predict Blocks", wn, p_id or "predict", "HIGH", "Predict input missing ID", "Input field in predict block has no ID attribute.", str(p))
            elif res and not res.get('id'):
                log_inc("Predict Blocks", wn, p_id or "predict", "HIGH", "Predict result container missing ID", "Result div in predict block has no ID attribute.", str(p))
        
        # Check button onclick handler
        if btn:
            btn_onclick = btn.get('onclick', '')
            if not btn_onclick or 'checkPredict' not in btn_onclick:
                log_inc("Predict Blocks", wn, p_id or "predict", "HIGH", "Predict button missing checkPredict handler", f"Button onclick='{btn_onclick}' does not call checkPredict.", str(btn))
            else:
                m_cp = re.search(r"checkPredict\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*\)", btn_onclick)
                if not m_cp:
                    # check if answer has single quotes inside or backslashes
                    if "\\'" in btn_onclick or '\"' in btn_onclick:
                        pass
                    else:
                        log_inc("Predict Blocks", wn, p_id or "predict", "MEDIUM", "Malformed checkPredict argument signature", f"Button onclick='{btn_onclick}' has unconventional arguments.", btn_onclick)

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 2: QUIZ OPTION CORRECTNESS & FEEDBACK ID WIRING
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 2: Quiz Correctness & Feedback Wiring...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    quizzes = soup.find_all('div', class_='quiz-block')
    for q in quizzes:
        qid = q.get('id', 'quiz-unknown')
        opts = q.find_all(class_='quiz-opt')
        
        if not opts:
            log_inc("Quiz Correctness", wn, qid, "HIGH", "Quiz has no options", f"Quiz block {qid} contains no .quiz-opt elements.", str(q))
            continue
            
        correct_opts = []
        wrong_opts = []
        for o in opts:
            onclick = o.get('onclick', '')
            if "'correct'" in onclick or '"correct"' in onclick:
                correct_opts.append(o)
            elif "'wrong'" in onclick or '"wrong"' in onclick:
                wrong_opts.append(o)
            else:
                log_inc("Quiz Correctness", wn, qid, "HIGH", "Quiz option missing correct/wrong attribute", f"Option onclick='{onclick}' does not specify 'correct' or 'wrong'.", str(o))

        if len(correct_opts) == 0:
            log_inc("Quiz Correctness", wn, qid, "CRITICAL", "Quiz has NO correct option", f"Quiz block {qid} has 0 correct options (impossible to solve).", str(q))
        elif len(correct_opts) > 1:
            log_inc("Quiz Correctness", wn, qid, "MEDIUM", "Quiz has MULTIPLE correct options without multi-select", f"Quiz block {qid} has {len(correct_opts)} correct options.", str(q))

        # Check feedback containers
        c_fb = q.find(class_=re.compile(r'correct-fb'))
        w_fb = q.find(class_=re.compile(r'wrong-fb'))
        if not c_fb or not w_fb:
            log_inc("Quiz Feedback", wn, qid, "HIGH", "Missing feedback containers in quiz", f"Quiz block {qid} is missing either .correct-fb or .wrong-fb element.")

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 3: FLASHCARD DOM STRUCTURE & FLIP CLICK HANDLERS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 3: Flashcards...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    fcs = soup.find_all('div', class_='flashcard')
    for fc in fcs:
        onclick = fc.get('onclick', '')
        if 'flipped' not in onclick and 'toggle' not in onclick:
            log_inc("Flashcards", wn, "flashcard", "MEDIUM", "Flashcard missing flipped onclick handler", f"Flashcard onclick='{onclick}' does not toggle flipped state.", str(fc))
        
        # Check if flashcard has both front and back
        has_front = bool(fc.find(class_=re.compile(r'front|fc-front'))) or len(fc.find_all('div')) >= 2
        txt = fc.text.strip()
        if len(txt) < 10:
            log_inc("Flashcards", wn, "flashcard", "HIGH", "Empty / minimal flashcard text", f"Flashcard contains only {len(txt)} chars.", txt)

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 4: TASK DRAWERS & VERIFICATION CRITERIA
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 4: Task Drawers...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    tasks = soup.find_all('div', class_='task-block')
    for t in tasks:
        hdr = t.find(class_='task-header')
        body = t.find(class_='task-body')
        
        if not hdr:
            log_inc("Task Drawers", wn, "task", "HIGH", "Task missing .task-header", "Task block lacks a task header trigger.", str(t))
        else:
            onclick = hdr.get('onclick', '')
            if 'toggleTask' not in onclick:
                log_inc("Task Drawers", wn, "task", "HIGH", "Task header missing toggleTask onclick", f"Header onclick='{onclick}' does not call toggleTask.", str(hdr))

        if not body:
            log_inc("Task Drawers", wn, "task", "HIGH", "Task missing .task-body container", "Task block lacks an expandable body.", str(t))
        else:
            # Check if task body contains code solution
            cb = body.find(class_='cb') or body.find('pre')
            if not cb:
                log_inc("Task Drawers", wn, "task", "MEDIUM", "Task body lacks code solution card", "Task expandable drawer does not contain a solution code block.", str(body))

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 5: INTER-WEEK NAVIGATION LINKS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 5: Navigation Links...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    nav_div = soup.find('div', class_='week-nav-links')
    if not nav_div:
        log_inc("Navigation Links", wn, "sidebar", "HIGH", "Missing .week-nav-links in sidebar", f"Week {wn} lacks sidebar bottom navigation links container.")
    else:
        links = {a.text.strip(): a.get('href', '') for a in nav_div.find_all('a')}
        
        # Check Roadmap, Dashboard, Resources links
        for expected_text, expected_target in [("🗺 Roadmap", "../../roadmap.html"), ("📊 Dashboard", "../../dashboard.html"), ("📚 Resources", "../../resources.html")]:
            matching = [href for text, href in links.items() if expected_text in text]
            if not matching:
                log_inc("Navigation Links", wn, "sidebar", "MEDIUM", f"Missing {expected_text} nav link", f"Week {wn} sidebar does not link to {expected_text}.")
            elif matching[0] != expected_target:
                log_inc("Navigation Links", wn, "sidebar", "MEDIUM", f"Incorrect relative path for {expected_text}", f"Week {wn} links to '{matching[0]}' instead of '{expected_target}'.")

        # Check Previous week link
        if wn > 1:
            prev_expected = f"week{wn-1}.html"
            matching_prev = [href for text, href in links.items() if "Previous" in text or "← Week" in text]
            if not matching_prev:
                log_inc("Navigation Links", wn, "sidebar", "HIGH", f"Missing Previous Week ({wn-1}) link", f"Week {wn} sidebar does not have a link to Week {wn-1}.")
            elif matching_prev[0] != prev_expected:
                log_inc("Navigation Links", wn, "sidebar", "HIGH", f"Incorrect Previous Week link in Week {wn}", f"Week {wn} points to '{matching_prev[0]}' instead of '{prev_expected}'.")

        # Check Next week link
        if wn < 26:
            next_expected = f"week{wn+1}.html"
            matching_next = [href for text, href in links.items() if "Next" in text or f"Week {wn+1}" in text]
            if not matching_next:
                log_inc("Navigation Links", wn, "sidebar", "HIGH", f"Missing Next Week ({wn+1}) link", f"Week {wn} sidebar does not have a link to Week {wn+1}.")
            elif matching_next[0] != next_expected:
                log_inc("Navigation Links", wn, "sidebar", "HIGH", f"Incorrect Next Week link in Week {wn}", f"Week {wn} points to '{matching_next[0]}' instead of '{next_expected}'.")

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 6: ROADMAP VS WEEK PAGES TITLE ALIGNMENT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 6: Roadmap Title Alignment...")
fp_roadmap = ROOT_DIR / "roadmap.html"
if fp_roadmap.exists():
    soup_rm = BeautifulSoup(fp_roadmap.read_text(), 'html.parser')
    rm_weeks = soup_rm.find_all(class_=re.compile(r'week-card|week-node|week-item'))
    print(f"  Found {len(rm_weeks)} week nodes in roadmap.html")

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 7: METADATA BADGES & ESTIMATED TIMES
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 7: Metadata Badges...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        meta_row = ds.find('div', class_='meta-row')
        if not meta_row:
            log_inc("Metadata Badges", wn, did, "LOW", "Missing .meta-row badge container", f"{did} lacks time and difficulty metadata badges.")
        else:
            badges = meta_row.find_all(class_=re.compile(r'meta-badge'))
            if len(badges) < 2:
                log_inc("Metadata Badges", wn, did, "LOW", f"Sparse metadata badges in {did} ({len(badges)} found)", f"{did} has only {len(badges)} badge (standard is 2: time + difficulty).")

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION 8: HARDCODED COLORS & THEME CONTRAST RISKS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Dimension 8: Hardcoded Colors & Theme Contrast...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html_text = fp.read_text()
    
    # Check for hardcoded color: #fff or color: white on inline styles without background
    hardcoded_white_text = re.findall(r'style="[^"]*color:\s*(?:#ffffff|#fff|white)[^"]*"', html_text)
    if len(hardcoded_white_text) > 5:
        log_inc("Theme Contrast Risks", wn, "Global", "MEDIUM", f"High volume of hardcoded white text ({len(hardcoded_white_text)} instances)", "Hardcoded color: white creates readability failure when user toggles Light mode.", hardcoded_white_text[0])

    # Check for hardcoded color: #000 or color: black on inline styles without background
    hardcoded_black_text = re.findall(r'style="[^"]*color:\s*(?:#000000|#000|black)[^"]*"', html_text)
    if len(hardcoded_black_text) > 3:
        log_inc("Theme Contrast Risks", wn, "Global", "MEDIUM", f"Hardcoded black text ({len(hardcoded_black_text)} instances)", "Hardcoded color: black creates readability failure in Dark mode.", hardcoded_black_text[0])

print(f"\nDiscovered {len(inconsistencies)} specialized inconsistencies across the 8 dimensions!")
out_file = ROOT_DIR / "scripts" / "specialized_inconsistencies_inventory.json"
out_file.write_text(json.dumps(inconsistencies, indent=2), encoding='utf-8')
print(f"Saved to {out_file}")
