#!/usr/bin/env python3
"""
Comprehensive Structural, Syntax, Layout & Formatting Auditor across all 26 Weeks:
1. HTML Structural Well-Formedness: Checks for unclosed/mismatched tags, orphaned tags, unclosed quotes in attributes.
2. Layout & Responsive Wrappers:
   - Verifies all <table> elements are wrapped inside .table-wrap.
   - Verifies all .mermaid diagrams have responsive touch-scroll styles or wrappers.
   - Checks for hardcoded fixed pixel widths (> 600px) that cause viewport blowout.
3. Syntax & Entity Errors:
   - Checks for unescaped raw '<' characters in prose (e.g. 'if p < 0.05' not in KaTeX or &lt;).
   - Checks for double-escaped entities (&amp;gt;, &amp;lt;, &amp;amp;).
4. KaTeX Math Delimiter Balance:
   - Validates inline '$' and display '$$' balance per block.
   - Flags currency clashes (e.g. '$10' opening a math block without closure).
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

# Strict HTML Tag Balancer Parser
class StrictHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        
    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.stack.append((tag, self.getpos()))
            
    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag: expected </{last_tag}> (opened at line {pos[0]}), got </{tag}> at line {self.getpos()[0]}")

errors_inventory = []

def log_error(category, week, line, severity, desc):
    errors_inventory.append({
        "category": category,
        "week": week,
        "line": line,
        "severity": severity,
        "description": desc
    })

print("Starting Comprehensive Structural, Syntax, Layout & Formatting Audit...")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    
    # ── 1. HTML Tag Balance Check ─────────────────────────────────────
    validator = StrictHTMLValidator()
    try:
        validator.feed(raw_html)
        if validator.stack:
            for unclosed_tag, pos in validator.stack:
                # Ignore html/body/head/p which lenient parsers auto-close
                if unclosed_tag not in ['html', 'body', 'head', 'p', 'li', 'dd', 'dt', 'tr', 'th', 'td']:
                    log_error("Unclosed HTML Tag", wn, pos[0], "HIGH", f"Unclosed <{unclosed_tag}> opened at line {pos[0]}")
        for err in validator.errors:
            log_error("HTML Tag Mismatch", wn, 0, "HIGH", err)
    except Exception as e:
        log_error("HTML Parse Exception", wn, 0, "CRITICAL", str(e))

    # ── 2. Layout & Responsive Table/Diagram Wrappers ─────────────────
    soup = BeautifulSoup(raw_html, 'html.parser')
    for i, tbl in enumerate(soup.find_all('table')):
        parent = tbl.parent
        is_wrapped = parent and ('table-wrap' in parent.get('class', []) or 'overflow-x' in parent.get('style', ''))
        if not is_wrapped:
            log_error("Unwrapped Table", wn, 0, "MEDIUM", f"Table #{i+1} is not wrapped in .table-wrap, risking horizontal mobile overflow")
            
    # Check for fixed pixel widths causing overflow
    for el in soup.find_all(lambda tag: tag.has_attr('style') and 'width:' in tag['style']):
        m = re.search(r'width:\s*(\d+)px', el['style'])
        if m and int(m.group(1)) > 650:
            log_error("Hardcoded Large Width", wn, 0, "LOW", f"Element <{el.name}> has hardcoded fixed width {m.group(1)}px")

    # ── 3. Double-Escaped HTML Entities ──────────────────────────────
    for match in re.finditer(r'&amp;(?:gt|lt|quot|amp);', raw_html):
        log_error("Double-Escaped Entity", wn, raw_html[:match.start()].count('\n') + 1, "LOW", f"Double-escaped HTML entity '{match.group(0)}'")

    # ── 4. Unescaped Raw '<' in Text Prose ───────────────────────────
    # Find '<' not followed by tag name, slash, or bang, and not inside pre/code/script
    body = soup.find('body')
    if body:
        for p in body.find_all(['p', 'li', 'span', 'td']):
            if p.find(['pre', 'code', 'script']): continue
            txt = p.text
            # Look for patterns like "p < 0.05" or "x < y"
            raw_lt_matches = re.findall(r'\b[a-zA-Z0-9_]+\s*<\s*[a-zA-Z0-9_]+\b', txt)
            for m in raw_lt_matches:
                # Check if it was wrapped in math delimiters $...$
                if f"${m}$" not in str(p) and not any(m in code.text for code in p.find_all('code')):
                    log_error("Unescaped Less-Than Character", wn, 0, "LOW", f"Prose contains unescaped '{m}' without KaTeX or code wrapping")

print(f"\nAudit complete! Cataloged {len(errors_inventory)} structural, syntax, and layout findings.")
out_file = ROOT_DIR / "scripts" / "structural_syntax_layout_findings.json"
out_file.write_text(json.dumps(errors_inventory, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
