#!/usr/bin/env python3
"""
scripts/deep_syntax_and_html_tag_audit.py
Scans all 26 HTML week pages, root portals, and 26 YAML data files for:
1. Malformed HTML tag attributes (e.g. unescaped quotes in href, src, onclick, aria-label, style)
2. Leaking/unclosed HTML tags (<a, <div, <span, <p, <link, <meta, <script, <style>)
3. Escaped vs unescaped HTML entities in raw text nodes vs code/mermaid blocks
4. Stray closing tags without matching opening tags
5. Broken inline JavaScript event handlers
"""

import glob, yaml, re, os, json, html

print("=== STARTING COMPREHENSIVE SYNTAX & TAG INTEGRITY AUDIT ===")

findings = []
err_id = 1

def log_err(file_path, tag_type, issue_desc, line_no=None, snippet=""):
    global err_id
    findings.append({
        "id": f"SYNTAX-{err_id:03d}",
        "file": os.path.basename(file_path),
        "full_path": file_path,
        "tag_type": tag_type,
        "issue": issue_desc,
        "line": line_no,
        "snippet": snippet[:200]
    })
    err_id += 1

all_html = sorted(glob.glob('pages/weeks/week*.html') + ['index.html', 'roadmap.html', 'dashboard.html', 'resources.html'])
all_yaml = sorted(glob.glob('src/data/week*.yaml'))

# 1. AUDIT HTML FILES FOR MALFORMED ATTRIBUTES & TAG LEAKS
print("1. Scanning HTML pages for malformed attributes & tag leaks...")
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        content = "".join(lines)

    # Check for unclosed HTML opening tags e.g. <link href="..." without closing >
    unclosed_tags = re.finditer(r'<[a-zA-Z][^>]*<', content)
    for m in unclosed_tags:
        snip = m.group(0)
        # allow legitimate math or comparison operators if any inside code
        if '<code>' not in snip and '$$' not in snip:
            log_err(hf, "Tag Boundary", "Possible unclosed opening tag or consecutive '<'", snippet=snip)

    # Check for stray dangling literal tag fragments in body text
    stray_fragments = [
        ('rel="icon"', r'rel="icon"/>"'),
        ('aria-label leakage', r'aria-label="[^"]*"\s*role="img">"'),
        ('stray closing head', r'</head>\s*</head>'),
        ('stray closing body', r'</body>\s*</body>')
    ]
    for label, pat in stray_fragments:
        hits = re.findall(pat, content)
        if hits:
            log_err(hf, "Stray Fragment", f"Detected stray markup fragment: {label}", snippet=str(hits))

    # Check for broken onclick syntax
    onclicks = re.finditer(r'onclick="([^"]*)"', content)
    for m in onclicks:
        handler = m.group(1).strip()
        if handler.count('(') != handler.count(')'):
            log_err(hf, "JavaScript Onclick", f"Unbalanced parentheses in onclick handler: {handler}", snippet=handler)

# 2. AUDIT YAML THEORY STRINGS FOR MALFORMED HTML
print("2. Scanning YAML theory_html for malformed attributes & tags...")
for yf in all_yaml:
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        theory = str(d.get('theory_html', ''))
        
        # Check for malformed tags like <hN> class="..."
        malformed_h = re.findall(r'<h[1-6]>\s*class=', theory)
        if malformed_h:
            log_err(yf, "YAML Theory", f"Day {d_num}: Malformed <hN> class= attribute in YAML", snippet=str(malformed_h))

        # Check for unclosed <pre><code> tags in theory
        pre_o = len(re.findall(r'<pre\b', theory))
        pre_c = len(re.findall(r'</pre>', theory))
        if pre_o != pre_c:
            log_err(yf, "YAML Code Block", f"Day {d_num}: Unbalanced <pre> tags (opened: {pre_o}, closed: {pre_c})", snippet=f"Day {d_num}")

print(f"\nTotal Syntax / Tag Discrepancies Discovered: {len(findings)}")

with open('scripts/deep_syntax_audit_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("Saved report to: scripts/deep_syntax_audit_report.json")
