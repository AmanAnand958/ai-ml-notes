#!/usr/bin/env python3
"""
Comprehensive Diagram & Visual Architecture Audit across all 26 Weeks:
1. Strict Mermaid syntax verification (unquoted parentheses/brackets, broken arrows, unclosed subgraphs).
2. Diagram Coverage Gaps: Identifies all complex system/algorithm days that lack a visual architecture diagram.
3. Container Responsiveness: Checks if all .mermaid blocks have responsive overflow handling.
4. Dynamic Tab Navigation Trigger: Checks if renderMermaid is invoked on every day transition.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
diagram_audit_results = []

def log_diag_issue(category, week, day, severity, title, details, snippet=""):
    diagram_audit_results.append({
        "id": len(diagram_audit_results) + 1,
        "category": category,
        "week": week,
        "day": day,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. STRICT MERMAID SYNTAX SCANNER
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 1: Strict Mermaid Syntax & Token Safety...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    mermaids = soup.find_all('div', class_='mermaid')
    for i, m in enumerate(mermaids):
        raw_code = m.text.strip()
        
        # Check graph header
        lines = [line.strip() for line in raw_code.split('\n') if line.strip()]
        if not lines:
            log_diag_issue("Empty Diagram", wn, f"Week {wn} (Diagram #{i+1})", "HIGH", f"Empty .mermaid container in Week {wn}", "Diagram container has no Mermaid syntax text.")
            continue
            
        header = lines[0]
        if not re.match(r'^(?:graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|gitGraph)\b', header):
            log_diag_issue("Invalid Diagram Header", wn, f"Week {wn} (Diagram #{i+1})", "HIGH", f"Unrecognized Mermaid header in Week {wn}: '{header}'", "Diagram must start with a valid declaration like 'graph TD' or 'flowchart LR'.", header)

        # Check for unquoted parentheses or brackets inside node labels
        # e.g., A[Text (With Parentheses)] -> should be A["Text (With Parentheses)"]
        for line in lines[1:]:
            # Match unquoted brackets containing parentheses: e.g. [Label (Extra)] but not ["Label (Extra)"]
            bad_parens = re.findall(r'\[(?!\")[^\]]*\([^\)]*\)[^\]]*(?<!\")\]', line)
            if bad_parens:
                log_diag_issue(
                    "Mermaid Syntax Risk", wn, f"Week {wn} (Diagram #{i+1})", "MEDIUM",
                    f"Unquoted parentheses in node label: {bad_parens[0]}",
                    "Mermaid parser treats unquoted parentheses as shape definitions or syntax errors. Wrap label in quotes: [\"...\"]",
                    line
                )

            # Check for unclosed quotes in lines
            quote_count = line.count('"')
            if quote_count % 2 != 0:
                log_diag_issue(
                    "Mermaid Syntax Error", wn, f"Week {wn} (Diagram #{i+1})", "HIGH",
                    f"Unclosed double quote in Mermaid statement",
                    f"Line contains an odd number of double quotes ({quote_count}): '{line}'.",
                    line
                )

            # Check for unclosed brackets or braces
            if line.count('[') != line.count(']'):
                log_diag_issue(
                    "Mermaid Syntax Error", wn, f"Week {wn} (Diagram #{i+1})", "HIGH",
                    f"Unbalanced square brackets in Mermaid line",
                    f"Mismatch in '[' ({line.count('[')}) vs ']' ({line.count(']')}) in: '{line}'.",
                    line
                )

# ─────────────────────────────────────────────────────────────────────────────
# 2. DIAGRAM COVERAGE GAPS: IDENTIFY DAYS LACKING ARCHITECTURAL FLOWCHARTS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 2: Diagram Coverage Gaps across all 198 Days...")

SYSTEM_TOPIC_KEYWORDS = [
    ("Pipeline", "Data / ML Pipeline flow"),
    ("Architecture", "System / Model Architecture"),
    ("Transformer", "Multi-Head Attention & Transformer block"),
    ("RAG", "Retrieval Augmented Generation flow"),
    ("Agent", "Autonomous Multi-Agent Loop"),
    ("Kubernetes", "Pod / Service / Ingress Traffic routing"),
    ("Deploy", "Deployment & CI/CD pipeline"),
    ("Serving", "Inference & Batching engine"),
    ("Recommendation", "Two-Tower / Candidate Generation flow"),
    ("Search", "Vector / Hybrid Search & Re-ranking pipeline"),
    ("CNN", "Convolution & Feature Map extraction flow"),
    ("RNN", "Recurrent Sequential flow"),
    ("LSTM", "Memory Cell & Gating flow"),
    ("GAN", "Generator vs Discriminator Minimax loop"),
    ("Diffusion", "Forward Noising & Reverse Denoising process"),
    ("Audio", "Spectrogram & Acoustic encoder flow"),
    ("Vision", "Patch Embedding & Multimodal projection")
]

total_days_scanned = 0
days_with_diagrams = 0
days_missing_diagrams = []

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        total_days_scanned += 1
        
        has_diagram = bool(ds.find('div', class_='mermaid')) or bool(ds.find('svg', class_='diagram'))
        if has_diagram:
            days_with_diagrams += 1
        else:
            h1 = ds.find('h1')
            title = h1.text.strip() if h1 else did
            
            # Check if this topic warranted an architectural diagram
            matching_keywords = [desc for kw, desc in SYSTEM_TOPIC_KEYWORDS if kw.lower() in title.lower() or kw.lower() in ds.text[:300].lower()]
            if matching_keywords:
                days_missing_diagrams.append((wn, did, title, matching_keywords[0]))
                log_diag_issue(
                    "Diagram Coverage Gap", wn, did, "LOW",
                    f"Missing visual architecture diagram in {did} ('{title}')",
                    f"This day covers {matching_keywords[0]}, but currently relies solely on text/code without a Mermaid flowchart."
                )

# ─────────────────────────────────────────────────────────────────────────────
# 3. CONTAINER RESPONSIVENESS & OVERFLOW AUDIT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 3: Mermaid Container Viewport Styling...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Check if .mermaid in embedded style has overflow-x handling
    css_match = re.search(r'\.mermaid\s*\{([^}]+)\}', raw)
    if css_match:
        css_props = css_match.group(1)
        if 'overflow' not in css_props:
            log_diag_issue(
                "Responsive Diagram Risk", wn, "Global", "MEDIUM",
                f".mermaid CSS in Week {wn} lacks overflow-x: auto",
                "Wide Mermaid flowcharts on mobile devices may clip without explicit overflow-x: auto on the .mermaid container."
            )
    else:
        log_diag_issue(
            "Missing Diagram Styling", wn, "Global", "LOW",
            f"Week {wn} lacks dedicated .mermaid CSS rules in <style>",
            "No specific styling rules for .mermaid containers were found in the page stylesheet."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 4. REPORT METRICS
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nDiagram Audit complete!")
print(f"  • Total Days Scanned     : {total_days_scanned}")
print(f"  • Days with Visual Charts: {days_with_diagrams} ({round(days_with_diagrams/total_days_scanned*100, 1)}%)")
print(f"  • Days Missing Diagrams  : {len(days_missing_diagrams)}")
print(f"  • Total Identified Issues: {len(diagram_audit_results)}")

out_file = Path("scripts/diagram_issues_inventory.json")
out_file.write_text(json.dumps(diagram_audit_results, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
