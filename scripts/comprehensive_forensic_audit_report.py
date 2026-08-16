#!/usr/bin/env python3
"""
Comprehensive Forensic Discovery & Cataloging Suite across all 26 Weeks.
Strictly categorizes >100 distinct content, pedagogical, formatting, and structural issues.
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import ast
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

audit_findings = []

def record_finding(category, week_num, day_id, severity, issue_title, description, code_snippet=""):
    audit_findings.append({
        "id": len(audit_findings) + 1,
        "category": category,
        "week": week_num,
        "day": day_id,
        "severity": severity,
        "title": issue_title,
        "description": description,
        "snippet": code_snippet[:160].replace('\n', ' ') if code_snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. SCAN ALL 26 WEEKS
# ─────────────────────────────────────────────────────────────────────────────
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue

    raw_html = fp.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # ── A. FORMATTING & UNPARSED MARKDOWN DEFECTS ──
    # Check for raw markdown links [text](url)
    for string_node in soup.find_all(string=re.compile(r'\[[^\]]{2,50}\]\(https?://[^\)]+\)')):
        parent = string_node.parent
        if parent and parent.name not in ['code', 'pre', 'script', 'style']:
            matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', string_node)
            for text, url in matches:
                record_finding(
                    "Unformatted Text / Raw Markdown", wn, "Global", "HIGH",
                    f"Unrendered Markdown Link: [{text}]({url})",
                    f"Raw markdown link syntax is rendered as plain text in the UI instead of a clickable <a> anchor tag.",
                    f"[{text}]({url})"
                )

    # Check for raw markdown bold **text**
    for string_node in soup.find_all(string=re.compile(r'\*\*[^*]{2,60}\*\*')):
        parent = string_node.parent
        if parent and parent.name not in ['code', 'pre', 'script', 'style']:
            matches = re.findall(r'\*\*([^*]+)\*\*', string_node)
            for m in matches:
                record_finding(
                    "Unformatted Text / Raw Markdown", wn, "Global", "MEDIUM",
                    f"Unrendered Markdown Bold: **{m}**",
                    f"Raw markdown bold asterisks (**...**) display literally in body text instead of <strong> or <b> tags.",
                    f"**{m}**"
                )

    # Check for unformatted raw LaTeX / broken math tokens
    math_entities = re.findall(r'\$\$[^\$]*&(?:gt|lt|amp|quot);[^\$]*\$\$', raw_html)
    if math_entities:
        record_finding(
            "Unformatted Text / KaTeX Glitch", wn, "Global", "HIGH",
            f"Escaped HTML entities inside KaTeX formula delimiters ($$...$$)",
            f"Found {len(math_entities)} mathematical formula blocks containing escaped entities like &gt; or &lt; that prevent KaTeX from parsing the equation.",
            math_entities[0]
        )

    # ── B. DAY-BY-DAY CURRICULUM & CONTENT GAPS ──
    day_sections = soup.find_all("div", class_=lambda c: c and ("day-section" in c.split() or c == "day-section"))
    
    for ds in day_sections:
        did = ds.get("id", f"week-{wn}-unknown")
        d_text = ds.text
        d_html = str(ds)
        
        # 1. Check Primary Heading
        h1 = ds.find("h1")
        if not h1:
            record_finding("Structural Defect", wn, did, "HIGH", f"Missing <h1> title heading", f"{did} has no main <h1> heading.")
        elif h1.text.strip().startswith('#'):
            record_finding("Unformatted Text", wn, did, "MEDIUM", f"Raw markdown '#' in <h1> title", f"<h1> heading contains raw markdown '#' character: '{h1.text.strip()}'")

        # 2. Check Objectives Section
        obj = ds.find("div", class_="objectives")
        if not obj and "By the end of Day" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "MEDIUM", f"Missing Learning Objectives", f"{did} is missing the standard '🎯 By the end of Day...' learning objectives card.")
        elif obj and len(obj.find_all("li")) < 2:
            record_finding("Content Quality / Depth", wn, did, "LOW", f"Sparse learning objectives", f"{did} has only {len(obj.find_all('li'))} objective bullet points.")

        # 3. Check Theory & Conceptual Analogy
        theory = ds.find(class_=re.compile(r'theory|sh2'))
        if not theory and "Theory & Concepts" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "HIGH", f"Missing Theory & Concepts section", f"{did} lacks a core conceptual theory foundation section.")
        
        hinglish = ds.find("div", class_="hinglish")
        if not hinglish and "Ek line mein" not in d_text and "Hinglish Explanation" not in d_text:
            record_finding("Pedagogical Inconsistency", wn, did, "LOW", f"Missing Hinglish intuitive summary ('Ek line mein...')", f"{did} lacks the signature Hinglish intuitive concept summary block.")

        # 4. Check Code Blocks Quality
        cbs = [cb for cb in ds.find_all("div") if cb.get("class") == ["cb"]]
        if not cbs:
            record_finding("Missing Curriculum Content", wn, did, "HIGH", f"Missing code block examples", f"{did} contains no practical code cards.")
        else:
            for i, cb in enumerate(cbs):
                code_tag = cb.find("pre") or cb.find("code")
                if not code_tag or not code_tag.text.strip():
                    record_finding("Malformed Component", wn, did, "HIGH", f"Empty code card #{i+1}", f"Code block #{i+1} in {did} has no code text.")
                else:
                    raw_c = code_tag.text
                    if "pass  # TODO" in raw_c or "pass # implement" in raw_c or "TODO: Implement" in raw_c:
                        record_finding("Placeholder / Stub Code", wn, did, "MEDIUM", f"Unfinished placeholder TODO in code #{i+1}", f"Code card #{i+1} contains unfinished stub implementation.", raw_c[:80])
                    elif len(raw_c.strip()) < 35 and "print(" not in raw_c:
                        record_finding("Content Quality / Depth", wn, did, "LOW", f"Extremely short code snippet in #{i+1}", f"Code snippet #{i+1} is only {len(raw_c.strip())} chars.", raw_c)

        # 5. Check Predict the Output Block
        predict = ds.find(class_=re.compile(r'predict-block|predict-box'))
        if not predict and "PREDICT THE OUTPUT" not in d_text:
            record_finding("Missing Interactive Component", wn, did, "MEDIUM", f"Missing 'Predict the Output' interactive challenge", f"{did} does not have an active prediction challenge.")
        elif predict:
            inp = predict.find("input")
            btn = predict.find("button")
            if not inp or not btn:
                record_finding("Broken Component", wn, did, "HIGH", f"Incomplete predict challenge elements", f"Predict block in {did} lacks either an input element or submit check button.")

        # 6. Check Hands-on Tasks & Solutions
        tasks = ds.find_all("div", class_="task-block")
        if not tasks and "Task 1" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "MEDIUM", f"Missing Hands-on Tasks", f"{did} has no practical coding task blocks.")
        else:
            for t_idx, t in enumerate(tasks):
                header = t.find("div", class_="task-header")
                body = t.find("div", class_="task-body")
                if not header or not body:
                    record_finding("Malformed Component", wn, did, "MEDIUM", f"Malformed Task #{t_idx+1}", f"Task #{t_idx+1} in {did} lacks a proper header or expandable body.")

        # 7. Check Quizzes & Question Quality
        quizzes = ds.find_all("div", class_="quiz-block")
        if not quizzes and "Knowledge Check" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "HIGH", f"Missing Quiz Questions", f"{did} lacks knowledge check quizzes.")
        elif len(quizzes) > 0 and len(quizzes) < 4:
            record_finding("Curriculum Depth Deficit", wn, did, "LOW", f"Fewer than 4 quiz questions ({len(quizzes)} found)", f"{did} contains only {len(quizzes)} quiz questions (course standard is 4).")
        
        # Detect repeated/hallucinated generic quiz choices
        for q in quizzes:
            q_txt = q.text
            if "Use a task-specific baseline and measure quality, latency" in q_txt:
                record_finding(
                    "Generic / Hallucinated Quiz Option", wn, did, "HIGH",
                    f"Generic copy-pasted quiz options in {q.get('id', 'quiz')}",
                    "Multiple-choice options contain generic fallback text ('Use a task-specific baseline... / Rely on uncalibrated heuristic guesses...') instead of topic-specific distractors.",
                    q_txt[:120]
                )
                break

        # 8. Check Revision Flashcards
        fc_grid = ds.find("div", class_="flashcard-grid")
        fcs = ds.find_all("div", class_="flashcard")
        if not fc_grid or len(fcs) == 0:
            record_finding("Missing Interactive Component", wn, did, "MEDIUM", f"Missing Revision Flashcards", f"{did} has no interactive flashcard flip cards.")
        elif len(fcs) < 3:
            record_finding("Curriculum Depth Deficit", wn, did, "LOW", f"Sparse flashcards ({len(fcs)} found)", f"{did} has only {len(fcs)} flashcards (standard is 3-4).")

        # 9. Check Key Takeaways
        takeaways = ds.find("div", class_="takeaways")
        if not takeaways and "Key Takeaways" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "MEDIUM", f"Missing Key Takeaways Summary", f"{did} lacks the executive summary takeaway box.")

        # 10. Check Recommended Resources
        res = ds.find("div", class_="res-grid")
        if not res and "Recommended Resources" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "MEDIUM", f"Missing Recommended Resources", f"{did} lacks external documentation, paper, or tutorial resource cards.")
        elif res:
            for a in res.find_all("a"):
                href = a.get("href", "")
                # Detect mismatched resource links
                if "spark.apache.org" in href and any(topic in d_text for topic in ["MLflow", "DSPy", "Whisper", "Kubernetes", "VLM"]):
                    record_finding(
                        "Pedagogical Resource Mismatch", wn, did, "HIGH",
                        f"Mismatched Apache Spark documentation link in {did}",
                        f"Resource card points to Apache Spark documentation '{href}' on a lesson topic unrelated to Spark.",
                        href
                    )
                elif "github.com/trending" in href:
                    record_finding(
                        "Generic Resource Link", wn, did, "LOW",
                        f"Generic GitHub trending link in {did}",
                        "Resource links to generic github.com/trending rather than a dedicated repository for this day's subject.",
                        href
                    )

        # 11. Check Enterprise Case Study
        case_study = ds.find("div", class_="enterprise-case-study")
        if not case_study and "Enterprise Case Study" not in d_text:
            record_finding("Missing Curriculum Content", wn, did, "LOW", f"Missing Enterprise Case Study", f"{did} lacks a FAANG/enterprise production architecture case study.")

        # 12. Check Mathematical Deep-Dive
        math_card = ds.find("div", class_="math-deepdive-card")
        if not math_card and "$$" not in d_html:
            record_finding("Curriculum Depth Deficit", wn, did, "LOW", f"Missing Mathematical Deep-Dive formulation", f"{did} lacks a formalized LaTeX equation card.")

        # 13. Check Day Complete Button
        btn = ds.find("button", class_="complete-btn")
        if not btn:
            record_finding("Missing Action Control", wn, did, "HIGH", f"Missing Day Complete action button", f"{did} has no button to mark the day complete and claim XP.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. SCAN ROOT PAGES FOR GAPS
# ─────────────────────────────────────────────────────────────────────────────
for root_page in ["index.html", "dashboard.html", "resources.html", "roadmap.html"]:
    rp = ROOT_DIR / root_page
    if not rp.exists():
        record_finding("Missing Core Page", 0, root_page, "CRITICAL", f"Missing root page {root_page}", f"Root file {root_page} is missing.")
        continue

    r_soup = BeautifulSoup(rp.read_text(encoding="utf-8", errors="replace"), "html.parser")
    
    # Check dashboard state sync
    if root_page == "dashboard.html":
        # Check if dashboard has course.js link or state listeners
        r_text = rp.read_text()
        if "course.js" not in r_text:
            record_finding(
                "Architectural Disconnect", 0, "dashboard.html", "HIGH",
                "dashboard.html does not load assets/js/course.js",
                "The dashboard does not import the canonical course.js state engine, leading to potential out-of-sync stats display."
            )
            
    # Check resources catalog for empty sections
    if root_page == "resources.html":
        sections = r_soup.find_all("section")
        for s in sections:
            if len(s.find_all("a")) == 0:
                record_finding(
                    "Content Gap", 0, f"resources.html (#{s.get('id', 'section')})", "MEDIUM",
                    f"Empty resource category section in resources.html",
                    f"Section '{s.get('id')}' contains no resource links."
                )

print(f"\nAudit complete. Found {len(audit_findings)} concrete issues across all 26 weeks and root pages.")

out_fp = ROOT_DIR / "scripts" / "verified_forensic_issues_catalog.json"
out_fp.write_text(json.dumps(audit_findings, indent=2), encoding="utf-8")
print(f"Catalog saved to {out_fp}")
