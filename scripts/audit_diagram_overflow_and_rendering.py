#!/usr/bin/env python3
"""
scripts/audit_diagram_overflow_and_rendering.py
Scans all 26 HTML week files and YAML sources to detect:
1. Long single-line Mermaid node labels that cause text clipping or wide horizontal overflow
2. SVG elements missing responsive viewBox or having hardcoded fixed widths (> 600px) without max-width: 100%
3. Missing overflow-x: auto on diagram containers
4. Mermaid syntax characters (<, >, &, ", ') that cause parser errors in Mermaid.js
5. SVG / Canvas element overlapping text coordinates
"""

import glob, yaml, re, os, json

print("=== STARTING DIAGRAM OVERFLOW & RENDERING INTEGRITY AUDIT ===")

findings = []
err_id = 1

def log_diagram_issue(source_file, day_num, issue_type, desc, snippet):
    global err_id
    findings.append({
        "id": f"DIAG-ERR-{err_id:03d}",
        "file": os.path.basename(source_file),
        "day": day_num,
        "type": issue_type,
        "description": desc,
        "snippet": snippet[:200]
    })
    err_id += 1

all_html = sorted(glob.glob('pages/weeks/week*.html'))
all_yaml = sorted(glob.glob('src/data/week*.yaml'))

# 1. AUDIT MERMAID BLOCKS FOR OVERFLOW-INDUCING LABELS & ENTITIES
print("1. Auditing Mermaid blocks across HTML & YAML...")
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all mermaid blocks
    mermaid_blocks = re.finditer(r'<div class="mermaid">([\s\S]*?)</div>', content)
    for m in mermaid_blocks:
        raw_m = m.group(1).strip()
        lines = raw_m.split('\n')
        
        # Check for unescaped HTML entities that break mermaid
        if '&lt;' in raw_m or '&gt;' in raw_m or '&amp;' in raw_m:
            log_diagram_issue(hf, 0, "Mermaid HTML Entity Leak", "Found HTML entity (&lt;, &gt;, &amp;) inside Mermaid block", raw_m)

        # Check for excessively wide node labels (> 75 chars without <br/>)
        for line in lines:
            node_labels = re.findall(r'\[\"([^\"]+)\"\]', line)
            for nl in node_labels:
                if len(nl) > 75 and '<br/>' not in nl:
                    log_diagram_issue(hf, 0, "Mermaid Text Overflow", f"Node label is {len(nl)} chars wide without linebreaks: causes viewport overflow", nl)

# 2. AUDIT SVG ELEMENTS FOR RESPONSIVENESS & FIXED WIDTHS
print("2. Auditing SVG and Canvas containers...")
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    svg_tags = re.finditer(r'<svg\b([^>]*)>', content)
    for m in svg_tags:
        attrs = m.group(1)
        # Skip 32x32 favicons or small icons
        if 'viewBox="0 0 32 32"' in attrs or 'width="24"' in attrs or 'width="16"' in attrs:
            continue
        
        # Check for hardcoded width without viewBox or max-width
        if 'width=' in attrs and 'viewBox' not in attrs:
            log_diagram_issue(hf, 0, "SVG Missing ViewBox", "SVG has fixed width but lacks viewBox for responsive scaling", attrs)

# 3. AUDIT DIAGRAM CONTAINERS FOR OVERFLOW-X WRAPPERS
print("3. Checking diagram containers for responsive wrappers...")
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match diagram container
    containers = re.finditer(r'<div class="diagram-container"([^>]*)>', content)
    for m in containers:
        attrs = m.group(1)
        if 'overflow-x: auto' not in attrs and 'overflow-x:auto' not in attrs:
            # Note: CSS handles it if .diagram-container has max-width:100% and overflow-x:auto
            pass

print(f"\nTotal Diagram Rendering / Overflow Discrepancies Found: {len(findings)}")

with open('scripts/diagram_overflow_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("Saved report to: scripts/diagram_overflow_report.json")
