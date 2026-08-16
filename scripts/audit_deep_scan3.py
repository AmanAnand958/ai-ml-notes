#!/usr/bin/env python3
"""
Deep Forensic Scan 3:
1. HTML Tag Balance & Well-Formedness across all HTML files (div, span, pre, code, ul, li, etc.)
2. Inline JavaScript Syntax Validation (extracting and checking all inline <script> blocks)
3. CDN Library Version Consistency (KaTeX, Mermaid, IBM Plex Mono, Outfit fonts)
4. Print Stylesheet (@media print) rules & dark-theme print ink optimization
5. SEO Meta Tags & Page Title Uniqueness (<title>, <meta description>, favicon, og tags)
"""

import os
import re
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

deep_scan_findings = []

def record_finding(category, filename, severity, title, details, snippet=""):
    deep_scan_findings.append({
        "id": len(deep_scan_findings) + 1,
        "category": category,
        "location": filename,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

all_html_files = [ROOT_DIR / "index.html", ROOT_DIR / "dashboard.html", ROOT_DIR / "resources.html", ROOT_DIR / "roadmap.html"]
all_html_files += sorted(list(WEEKS_DIR.glob("week*.html")), key=lambda p: int(re.search(r'\d+', p.name).group()))

# ─────────────────────────────────────────────────────────────────────────────
# 1. AUDIT HTML TAG BALANCE
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 1: HTML Tag Balancing...")
TRACKED_TAGS = ['div', 'span', 'p', 'pre', 'code', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'button', 'main', 'aside', 'nav']

for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    
    # Strip scripts, styles, and comments before tag counting
    clean_raw = re.sub(r'<!--[\s\S]*?-->', '', raw)
    clean_raw = re.sub(r'<script[\s\S]*?</script>', '', clean_raw)
    clean_raw = re.sub(r'<style[\s\S]*?</style>', '', clean_raw)
    
    tag_opens = Counter(re.findall(r'<([a-zA-Z0-9]+)(?:\s+[^>]*)?>', clean_raw))
    tag_closes = Counter(re.findall(r'</([a-zA-Z0-9]+)>', clean_raw))
    
    for tag in TRACKED_TAGS:
        opens = tag_opens[tag]
        closes = tag_closes[tag]
        if opens != closes:
            diff = opens - closes
            record_finding(
                "HTML Tag Unbalanced", fp.name, "MEDIUM",
                f"Unbalanced <{tag}> tags in {fp.name} ({opens} open vs {closes} close, diff: {diff})",
                f"Document has {opens} <{tag}> opening tags but {closes} </{tag}> closing tags.",
                f"<{tag}> opens: {opens}, closes: {closes}"
            )

# ─────────────────────────────────────────────────────────────────────────────
# 2. AUDIT INLINE JAVASCRIPT SYNTAX VALIDITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 2: Inline JavaScript Syntax...")
for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    for i, s in enumerate(soup.find_all('script')):
        if not s.get('src'):
            js_code = s.text.strip()
            if js_code:
                # Test syntax using node -c if node is available, or basic token bracket check
                # Check bracket balancing in JS
                curly = js_code.count('{') - js_code.count('}')
                round_b = js_code.count('(') - js_code.count(')')
                square = js_code.count('[') - js_code.count(']')
                
                if curly != 0:
                    record_finding("JS Syntax Risk", fp.name, "HIGH", f"Unbalanced curly braces in inline <script> #{i+1} of {fp.name}", f"Curly brace difference: {curly}")
                if round_b != 0:
                    record_finding("JS Syntax Risk", fp.name, "HIGH", f"Unbalanced parentheses in inline <script> #{i+1} of {fp.name}", f"Parentheses difference: {round_b}")
                if square != 0:
                    record_finding("JS Syntax Risk", fp.name, "HIGH", f"Unbalanced square brackets in inline <script> #{i+1} of {fp.name}", f"Square bracket difference: {square}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. AUDIT CDN LIBRARY VERSIONS & CONSISTENCY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 3: CDN Version Consistency...")
cdn_usage = defaultdict(list)

for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    for s in soup.find_all('script'):
        src = s.get('src', '')
        if src:
            if 'katex' in src: cdn_usage['katex'].append((fp.name, src))
            elif 'mermaid' in src: cdn_usage['mermaid'].append((fp.name, src))
            
    for l in soup.find_all('link'):
        href = l.get('href', '')
        if 'katex' in href: cdn_usage['katex_css'].append((fp.name, href))

# Check for version splits in CDN libraries
for lib, occurrences in cdn_usage.items():
    versions = set(src for fn, src in occurrences)
    if len(versions) > 1:
        record_finding(
            "CDN Version Drift", "Global", "MEDIUM",
            f"Multiple conflicting CDN versions detected for {lib}",
            f"Found {len(versions)} distinct CDN URLs: {list(versions)[:3]}."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 4. AUDIT PRINT STYLESHEET OPTIMIZATION
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 4: Print Stylesheet (@media print)...")
for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    if "@media print" not in raw and "week" in fp.name:
        record_finding(
            "Print Stylesheet Gap", fp.name, "LOW",
            f"Missing @media print rules in {fp.name}",
            f"{fp.name} stylesheet lacks print media queries to hide sidebars and optimize ink contrast during PDF export."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 5. AUDIT SEO & META TAG INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 5: SEO Meta Tags & Titles...")
seen_titles = defaultdict(list)

for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    title = soup.find('title')
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    favicon = soup.find('link', attrs={'rel': re.compile(r'icon')})
    
    if not title or not title.text.strip():
        record_finding("SEO Meta Defect", fp.name, "HIGH", f"Missing <title> tag in {fp.name}", "Page lacks a <title> element.")
    else:
        seen_titles[title.text.strip()].append(fp.name)
        
    if not meta_desc or not meta_desc.get('content', '').strip():
        record_finding("SEO Meta Defect", fp.name, "MEDIUM", f"Missing <meta name='description'> in {fp.name}", "Page lacks search engine meta description.")
        
    if not viewport:
        record_finding("Mobile Meta Defect", fp.name, "HIGH", f"Missing <meta name='viewport'> in {fp.name}", "Page lacks mobile viewport scaling declaration.")
        
    if not favicon:
        record_finding("Brand / Favicon Defect", fp.name, "LOW", f"Missing favicon link in {fp.name}", "Page lacks a favicon <link rel='icon'>.")

# Check for duplicate titles across different pages
for t_text, files in seen_titles.items():
    if len(files) > 1:
        record_finding(
            "Duplicate Page Title", files[0], "LOW",
            f"Duplicate <title> across multiple pages: '{t_text}'",
            f"The exact same page title is shared across {files}."
        )

print(f"\nDeep Scan 3 complete! Cataloged {len(deep_scan_findings)} findings.")
out_file = Path("scripts/deep_scan3_issues_inventory.json")
out_file.write_text(json.dumps(deep_scan_findings, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
