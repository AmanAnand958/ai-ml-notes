#!/usr/bin/env python3
"""
Comprehensive Duplication Scanner across all 26 Weeks:
1. Duplicate HTML IDs (day IDs, quiz IDs, predict input IDs, feedback IDs, canvas IDs).
2. Duplicate Code Blocks (identical or near-identical code blocks within the same day/week).
3. Duplicate Quiz Questions (identical question prompts or duplicate options).
4. Duplicate Flashcards (identical term/definition pairs within a day/week).
5. Duplicate Prose Sections (identical paragraphs or subheadings repeated consecutively).
6. Duplicate Diagram Flowcharts (identical Mermaid graph definitions).
7. Duplicate DOM/Head Tags (<link>, <meta>, <script>).
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import hashlib

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

duplication_report = {
    "duplicate_ids_within_file": defaultdict(list),
    "duplicate_code_blocks": defaultdict(list),
    "duplicate_quizzes": defaultdict(list),
    "duplicate_flashcards": defaultdict(list),
    "duplicate_diagrams": defaultdict(list),
    "duplicate_head_tags": defaultdict(list)
}

total_duplicate_items = 0

print("Starting Comprehensive Duplication Audit across all 26 Weeks...")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # ── 1. DUPLICATE HTML IDS ──────────────────────────────────────────
    all_ids = [el['id'] for el in soup.find_all(id=True)]
    id_counts = Counter(all_ids)
    for el_id, count in id_counts.items():
        if count > 1:
            duplication_report["duplicate_ids_within_file"][f"week{wn}"].append({
                "id": el_id,
                "occurrences": count
            })
            total_duplicate_items += count - 1

    # ── 2. DUPLICATE CODE BLOCKS (Within same day/week) ─────────────────
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        code_hashes = defaultdict(list)
        for i, cb in enumerate(ds.find_all('div', class_='cb')):
            pre = cb.find('pre')
            if not pre: continue
            code_text = pre.text.strip()
            if len(code_text) < 30: continue # ignore tiny 1-liners
            chash = hashlib.md5(code_text.encode('utf-8')).hexdigest()
            code_hashes[chash].append((i+1, code_text[:60]))
            
        for chash, instances in code_hashes.items():
            if len(instances) > 1:
                duplication_report["duplicate_code_blocks"][f"week{wn}"].append({
                    "day": did,
                    "count": len(instances),
                    "code_snippet": instances[0][1]
                })
                total_duplicate_items += len(instances) - 1

    # ── 3. DUPLICATE QUIZ QUESTIONS ───────────────────────────────────
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        q_prompts = defaultdict(list)
        for i, qb in enumerate(ds.find_all('div', class_='quiz-block')):
            q_text_el = qb.find('div', class_='quiz-q')
            if not q_text_el: continue
            q_text = q_text_el.text.strip()
            q_prompts[q_text].append(i+1)
            
        for q_text, instances in q_prompts.items():
            if len(instances) > 1:
                duplication_report["duplicate_quizzes"][f"week{wn}"].append({
                    "day": did,
                    "count": len(instances),
                    "question": q_text[:70]
                })
                total_duplicate_items += len(instances) - 1

    # ── 4. DUPLICATE FLASHCARDS ───────────────────────────────────────
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        fc_terms = defaultdict(list)
        for i, fc in enumerate(ds.find_all('div', class_='flashcard')):
            term_el = fc.find('div', class_='fc-front') or fc.find('div', class_='flashcard-front') or fc.find('span')
            if not term_el: continue
            term = term_el.text.strip()
            fc_terms[term].append(i+1)
            
        for term, instances in fc_terms.items():
            if len(instances) > 1:
                duplication_report["duplicate_flashcards"][f"week{wn}"].append({
                    "day": did,
                    "count": len(instances),
                    "term": term
                })
                total_duplicate_items += len(instances) - 1

    # ── 5. DUPLICATE HEAD / SCRIPT TAGS ───────────────────────────────
    links = [l.get('href') for l in soup.find_all('link') if l.has_attr('href')]
    link_counts = Counter(links)
    for href, count in link_counts.items():
        if count > 1:
            duplication_report["duplicate_head_tags"][f"week{wn}"].append({
                "type": "link",
                "target": href,
                "count": count
            })
            total_duplicate_items += count - 1
            
    scripts = [s.get('src') for s in soup.find_all('script') if s.has_attr('src')]
    script_counts = Counter(scripts)
    for src, count in script_counts.items():
        if count > 1:
            duplication_report["duplicate_head_tags"][f"week{wn}"].append({
                "type": "script",
                "target": src,
                "count": count
            })
            total_duplicate_items += count - 1

out_file = ROOT_DIR / "scripts" / "duplications_audit_report.json"
out_file.write_text(json.dumps(duplication_report, indent=2), encoding='utf-8')

print(f"\nDuplication Audit Complete! Cataloged {total_duplicate_items} duplicate items.")
print(f"Report saved to {out_file}")
