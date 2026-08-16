#!/usr/bin/env python3
"""
Deep Forensic Scanner across 26 Weeks and Root Pages.
Catalogs all content quality issues, gaps, placeholders, pedagogical mismatches,
raw markdown in HTML, unformatted text, quiz flaws, mock data, and styling inconsistencies.
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import ast

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

findings = []

def add_finding(category, week, location, severity, title, details):
    findings.append({
        "id": len(findings) + 1,
        "category": category,
        "week": week,
        "location": location,
        "severity": severity,
        "title": title,
        "details": details
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. SCAN WEEKS 1 TO 26
# ─────────────────────────────────────────────────────────────────────────────
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        add_finding("Missing File", wn, f"pages/weeks/week{wn}.html", "CRITICAL", f"Week {wn} HTML file missing", f"Expected week{wn}.html does not exist.")
        continue

    raw_html = fp.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # ── A. Check Raw Markdown syntax inside HTML text nodes ──
    # 1. Stray markdown bold (**text**)
    # Search for text elements containing **
    for elem in soup.find_all(string=re.compile(r'\*\*[^*]+\*\*')):
        if elem.parent and elem.parent.name not in ['code', 'pre', 'script', 'style']:
            matches = re.findall(r'\*\*([^*]+)\*\*', elem)
            if matches:
                add_finding(
                    "Unformatted Text / Raw Markdown", wn, f"Week {wn} (<{elem.parent.name}>)", "MEDIUM",
                    f"Raw markdown bold syntax (**...**) in HTML",
                    f"Found raw markdown bold like '**{matches[0]}**' inside <{elem.parent.name}> tag instead of <strong>/<b>."
                )
                break
    
    # 2. Stray markdown links ([text](url))
    for elem in soup.find_all(string=re.compile(r'\[[^\]]+\]\(https?://[^\)]+\)')):
        if elem.parent and elem.parent.name not in ['code', 'pre', 'script', 'style']:
            matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', elem)
            if matches:
                add_finding(
                    "Unformatted Text / Raw Markdown", wn, f"Week {wn} (<{elem.parent.name}>)", "HIGH",
                    f"Raw markdown link syntax [text](url) in HTML",
                    f"Found unparsed markdown link [{matches[0][0]}]({matches[0][1]}) rendering as raw text instead of <a> tag."
                )
                break

    # 3. Stray markdown headers (# Header)
    for elem in soup.find_all(['p', 'div', 'span']):
        txt = elem.text.strip()
        if txt.startswith('# ') or txt.startswith('## ') or txt.startswith('### '):
            if elem.name not in ['code', 'pre'] and 'cb' not in elem.get('class', []):
                add_finding(
                    "Unformatted Text / Raw Markdown", wn, f"Week {wn} (<{elem.name}>)", "MEDIUM",
                    f"Raw markdown hashtag header in HTML container",
                    f"Found raw text '{txt[:50]}' inside <{elem.name}> instead of properly styled <h1/h2/h3> tag."
                )

    # 4. Stray backticks (`code`) in paragraphs
    for p_elem in soup.find_all(['p', 'li', 'td']):
        txt = p_elem.text
        bt_matches = re.findall(r'`([^`\n]{2,35})`', txt)
        if len(bt_matches) > 2:
            add_finding(
                "Unformatted Text / Raw Markdown", wn, f"Week {wn} (<{p_elem.name}>)", "LOW",
                f"Raw markdown backticks (`code`) in body text",
                f"Found {len(bt_matches)} backtick pairs like `{bt_matches[0]}` in body text instead of <code> tags."
            )
            break

    # ── B. Scan Day Sections & Pedagogical Structure ──
    day_sections = soup.find_all("div", class_=re.compile(r"\bday-section\b"))
    
    # Check DAYS script config
    m_days = re.search(r'const\s+DAYS\s*=\s*\[([^\]]+)\]', raw_html)
    declared_days = [d.strip().strip("'\"") for d in m_days.group(1).split(',')] if m_days else []
    found_day_ids = [d.get("id", "") for d in day_sections]
    
    # Check day count
    if len(day_sections) < 7:
        add_finding("Structural Gap", wn, f"Week {wn}", "HIGH", f"Fewer than 7 days in Week {wn}", f"Week {wn} contains only {len(day_sections)} day sections (expected at least 7).")

    for ds in day_sections:
        did = ds.get("id", "unknown")
        day_text = ds.text
        day_html = str(ds)
        
        # 1. Title and headers
        h1 = ds.find("h1")
        day_tag = ds.find("div", class_=re.compile(r"day-tag"))
        if not h1:
            add_finding("Structural Gap", wn, f"{did}", "HIGH", f"Missing <h1> title in {did}", f"Day section {did} does not contain a primary <h1> title heading.")
        if not day_tag:
            add_finding("Structural Gap", wn, f"{did}", "LOW", f"Missing .day-tag badge in {did}", f"Day section {did} lacks the standard 'WEEK X · DAY Y' metadata badge.")

        # 2. Objectives
        obj_div = ds.find("div", class_=re.compile(r"objectives"))
        if not obj_div and "By the end of Day" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "MEDIUM", f"Missing learning objectives in {did}", f"{did} does not define '🎯 By the end of Day...' learning objectives.")
        elif obj_div:
            items = obj_div.find_all("li")
            if len(items) < 2:
                add_finding("Content Quality / Depth", wn, f"{did}", "LOW", f"Sparse learning objectives in {did}", f"Only {len(items)} learning objective bullet points defined.")

        # 3. Theory & Concept depth
        theory_h2 = ds.find("h2", class_=re.compile(r"sh2"))
        if not theory_h2 and "Theory & Concepts" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "HIGH", f"Missing Theory & Concepts section in {did}", f"{did} lacks a dedicated 🧠 Theory & Concepts section.")
        
        # Hinglish explanation
        hinglish_div = ds.find("div", class_=re.compile(r"hinglish"))
        if not hinglish_div and "Hinglish Explanation" not in day_text and "Ek line mein" not in day_text:
            add_finding("Curriculum Style Inconsistency", wn, f"{did}", "LOW", f"Missing Hinglish conceptual analogy in {did}", f"{did} lacks the signature Hinglish intuitive analogy block.")

        # 4. Code Blocks & Completeness
        cbs = ds.find_all("div", class_=re.compile(r"\bcb\b"))
        if not cbs and not ds.find("pre"):
            add_finding("Missing Content", wn, f"{did}", "HIGH", f"No code examples in {did}", f"{did} does not contain any code cards (`.cb` or `<pre>`).")
        else:
            for cb_idx, cb in enumerate(cbs):
                code_elem = cb.find("code") or cb.find("pre")
                if not code_elem:
                    add_finding("Malformed Component", wn, f"{did}", "HIGH", f"Empty code card in {did}", f"Code card #{cb_idx+1} in {did} lacks code content.")
                else:
                    code_text = code_elem.text.strip()
                    # Check for placeholder implementations
                    if "pass  # TODO" in code_text or "pass # implement" in code_text or "# Add code here" in code_text or "TODO: Implement" in code_text:
                        add_finding("Incomplete / Placeholder Code", wn, f"{did}", "MEDIUM", f"Placeholder TODO in code card #{cb_idx+1} of {did}", f"Code contains unfinished placeholder stub: '{code_text[:60]}...'")
                    
                    # Check for generic dummy mocks
                    if "np.random.randn" in code_text and len(code_text) < 140 and ("Model" in day_text or "Pipeline" in day_text):
                        add_finding("Mock Data / Superficial Code", wn, f"{did}", "LOW", f"Superficial mock data snippet in {did}", f"Code block #{cb_idx+1} uses generic random mock tensors without illustrating algorithm mechanics.")

        # 5. Predict the Output Block
        predict = ds.find("div", class_=re.compile(r"predict-block|predict-box"))
        if not predict and "PREDICT THE OUTPUT" not in day_text:
            add_finding("Missing Interactive Component", wn, f"{did}", "MEDIUM", f"Missing 'Predict the Output' interactive challenge in {did}", f"{did} lacks the interactive prediction block.")
        elif predict:
            inp = predict.find("input")
            btn = predict.find("button")
            if not inp or not btn:
                add_finding("Broken Interactive Component", wn, f"{did}", "HIGH", f"Incomplete predict challenge in {did}", f"Predict block in {did} is missing either an <input> field or Check button.")

        # 6. Tasks & Solutions
        tasks = ds.find_all("div", class_=re.compile(r"task-block|task-card"))
        if not tasks and "Task 1" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "MEDIUM", f"Missing Hands-on Tasks in {did}", f"{did} does not contain hands-on task blocks with verification criteria.")
        else:
            for t_idx, t in enumerate(tasks):
                t_body = t.find("div", class_=re.compile(r"task-body"))
                if not t_body:
                    add_finding("Malformed Task", wn, f"{did}", "MEDIUM", f"Task #{t_idx+1} missing expandable body in {did}", f"Task block in {did} lacks a .task-body container.")

        # 7. Quizzes
        quizzes = ds.find_all("div", class_=re.compile(r"quiz-block|quiz-card"))
        if not quizzes and "Knowledge Check" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "HIGH", f"Missing Quiz Questions in {did}", f"{did} does not contain knowledge check quiz blocks.")
        elif len(quizzes) > 0 and len(quizzes) < 3:
            add_finding("Curriculum Depth Deficit", wn, f"{did}", "LOW", f"Fewer than standard 4 quiz questions in {did}", f"{did} has only {len(quizzes)} quiz questions (standard is 4).")
        
        # Check for repeated generic quiz options (hallucination signature)
        for q in quizzes:
            q_text = q.text
            if "Use a task-specific baseline and measure quality, latency" in q_text:
                add_finding(
                    "Generic / Hallucinated Quiz Option", wn, f"{did} ({q.get('id', 'quiz')})", "HIGH",
                    f"Generic boilerplate quiz option in {did}",
                    "Quiz options contain generic copy-pasted boilerplate ('Use a task-specific baseline... / Rely on uncalibrated heuristic...') unrelated to the specific question."
                )
                break

        # 8. Revision Flashcards
        fc_grid = ds.find("div", class_=re.compile(r"flashcard-grid"))
        fcs = ds.find_all("div", class_=re.compile(r"\bflashcard\b"))
        if not fc_grid or len(fcs) == 0:
            add_finding("Missing Interactive Component", wn, f"{did}", "MEDIUM", f"Missing Revision Flashcards in {did}", f"{did} lacks the 🃏 Revision Flashcards interactive grid.")
        elif len(fcs) < 3:
            add_finding("Curriculum Depth Deficit", wn, f"{did}", "LOW", f"Sparse flashcards in {did}", f"{did} contains only {len(fcs)} flashcards (standard is 3-4).")

        # 9. Key Takeaways
        takeaways = ds.find("div", class_=re.compile(r"takeaways"))
        if not takeaways and "Key Takeaways" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "MEDIUM", f"Missing Key Takeaways in {did}", f"{did} lacks the ✅ Key Takeaways summary card.")

        # 10. Recommended Resources
        resources = ds.find("div", class_=re.compile(r"res-grid|resources-grid"))
        if not resources and "Recommended Resources" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "MEDIUM", f"Missing Recommended Resources in {did}", f"{did} lacks curated external documentation and video links.")
        elif resources:
            r_links = resources.find_all("a")
            for rl in r_links:
                r_href = rl.get("href", "")
                if not r_href or r_href == "#":
                    add_finding("Dead / Placeholder Link", wn, f"{did}", "MEDIUM", f"Empty href in resource card of {did}", f"Resource '{rl.text.strip()[:30]}' has an empty or '#' href.")
                # Check for mismatched resource URLs
                if "spark.apache.org" in r_href and ("MLflow" in day_text or "DSPy" in day_text or "Whisper" in day_text):
                    add_finding("Pedagogical Resource Mismatch", wn, f"{did}", "HIGH", f"Mismatched Apache Spark resource link in {did}", f"Resource card links to '{r_href}' which is unrelated to {did}'s topic.")
                elif "github.com/trending" in r_href:
                    add_finding("Generic Resource Link", wn, f"{did}", "LOW", f"Generic GitHub trending link in {did}", f"Resource links to generic trending page rather than topic-specific repository.")

        # 11. Enterprise Case Study
        case_study = ds.find("div", class_=re.compile(r"enterprise-case-study|case-study"))
        if not case_study and "Case Study" not in day_text:
            add_finding("Missing Pedagogical Section", wn, f"{did}", "LOW", f"Missing Enterprise Case Study in {did}", f"{did} lacks an enterprise FAANG architecture breakdown.")

        # 12. Mathematical Deep-Dive
        math_card = ds.find("div", class_=re.compile(r"math-deepdive-card|math-block"))
        if not math_card and "$$" not in day_html:
            add_finding("Curriculum Depth Deficit", wn, f"{did}", "LOW", f"Missing Mathematical Deep-Dive in {did}", f"{did} does not contain a formalized mathematical LaTeX formulation card.")

        # 13. Day Complete Button
        complete_btn = ds.find("button", class_=re.compile(r"complete-btn"))
        if not complete_btn:
            add_finding("Missing Action Control", wn, f"{did}", "HIGH", f"Missing Day Complete button in {did}", f"{did} does not have a completion action button.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. SCAN ROOT PORTAL PAGES
# ─────────────────────────────────────────────────────────────────────────────
for root_page in ["index.html", "dashboard.html", "resources.html", "roadmap.html"]:
    rp = ROOT_DIR / root_page
    if not rp.exists():
        add_finding("Missing File", 0, root_page, "CRITICAL", f"Root file {root_page} missing", f"{root_page} not found in project root.")
        continue
    
    r_html = rp.read_text(encoding="utf-8", errors="replace")
    r_soup = BeautifulSoup(r_html, "html.parser")
    
    # Check dashboard state keys
    if root_page == "dashboard.html":
        if "courseState" not in r_html and "localStorage" not in r_html:
            add_finding("State Synchronization Gap", 0, "dashboard.html", "HIGH", f"Dashboard does not sync with course gamification state", "dashboard.html lacks state-listening or localStorage integration with courseState.")

    # Check resources catalog categorization
    if root_page == "resources.html":
        empty_sections = [s.get('id', 'section') for s in r_soup.find_all('section') if len(s.find_all('a')) == 0]
        if empty_sections:
            add_finding("Content Gap", 0, "resources.html", "MEDIUM", f"Empty resource categories in resources.html: {empty_sections}", f"Resource catalog contains sections with no links: {empty_sections}")

print(f"\nScan completed! Discovered {len(findings)} detailed issues across the project.")

# Save findings to json
report_path = ROOT_DIR / "scripts" / "master_issues_inventory.json"
report_path.write_text(json.dumps(findings, indent=2), encoding="utf-8")
print(f"Detailed issue inventory written to {report_path}")
