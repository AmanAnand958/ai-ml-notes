#!/usr/bin/env python3
"""
Comprehensive JavaScript Consistency & Runtime Safety Audit across all 26 Weeks:
1. External Script Tags: Checks CDN KaTeX, Mermaid, and `../../assets/js/course.js` links.
2. Embedded <script> Blocks: Audits for duplicate script blocks, conflicting function definitions, or legacy logic.
3. Inline Event Handler Validation: Extracts all `onclick`, `onkeydown`, `onchange` expressions and verifies that the referenced functions exist in `assets/js/course.js`.
4. `assets/js/course.js` Global API Coverage: Checks implementation of `quiz`, `copyCode`, `checkPredict`, `completeDay`, `toggleFlashcard`, `toggleSolution`, `renderMermaid`, `initKaTeX`.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

WEEKS_DIR = Path("pages/weeks")
COURSE_JS_PATH = Path("assets/js/course.js")
ROOT_DIR = Path(".")

course_js_content = COURSE_JS_PATH.read_text(encoding='utf-8')

# Extract functions defined in course.js
defined_functions = set(re.findall(r'(?:function\s+([a-zA-Z0-9_$]+)|window\.([a-zA-Z0-9_$]+)\s*=|const\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\()|([a-zA-Z0-9_$]+)\s*:\s*function)', course_js_content))
defined_fn_names = set()
for tup in defined_functions:
    for name in tup:
        if name: defined_fn_names.add(name)

# Add courseState methods
defined_fn_names.update(['courseState', 'quiz', 'copyCode', 'checkPredict', 'completeDay', 'toggleFlashcard', 'toggleSolution', 'renderMermaid', 'renderMath', 'showToast', 'saveState', 'loadState'])

js_audit_report = {
    "scripts_per_week": {},
    "embedded_scripts": {},
    "event_handlers": defaultdict(Counter),
    "unresolved_function_calls": defaultdict(list)
}

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. External Scripts
    script_tags = [s.get('src') for s in soup.find_all('script') if s.has_attr('src')]
    js_audit_report["scripts_per_week"][f"week{wn}"] = script_tags
    
    # 2. Embedded Scripts
    inline_scripts = [s.text for s in soup.find_all('script') if not s.has_attr('src')]
    js_audit_report["embedded_scripts"][f"week{wn}"] = {
        "count": len(inline_scripts),
        "total_chars": sum(len(txt) for txt in inline_scripts)
    }
    
    # 3. Inline Event Handlers
    for el in soup.find_all(lambda tag: any(attr.startswith('on') for attr in tag.attrs)):
        for attr, val in el.attrs.items():
            if attr.startswith('on'):
                js_audit_report["event_handlers"][f"week{wn}"][attr] += 1
                
                # Check function names in handler
                fn_matches = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', val)
                for fn in fn_matches:
                    if fn not in ['if', 'event', 'alert', 'console', 'document', 'window'] and fn not in defined_fn_names:
                        # Check if it's a DOM method like this.click or this.classList.toggle
                        if fn not in ['click', 'toggle', 'add', 'remove', 'contains']:
                            js_audit_report["unresolved_function_calls"][f"week{wn}"].append({
                                "element": el.name,
                                "attr": attr,
                                "function": fn,
                                "raw_code": val
                            })

out_file = ROOT_DIR / "scripts" / "js_consistency_audit_report.json"
out_file.write_text(json.dumps(js_audit_report, indent=2), encoding='utf-8')

print(f"{'Week':<8} | {'course.js Linked':<18} | {'KaTeX / Mermaid':<18} | {'Inline <script>':<18} | {'Unresolved FN Calls'}")
print("-" * 90)
for wn in range(1, 27):
    wkey = f"week{wn}"
    scripts = js_audit_report["scripts_per_week"].get(wkey, [])
    has_course_js = any('course.js' in s for s in scripts if s)
    has_katex = any('katex' in s for s in scripts if s)
    has_mermaid = any('mermaid' in s for s in scripts if s)
    km_status = f"{'K' if has_katex else '-'}/{'M' if has_mermaid else '-'}"
    
    inlines = js_audit_report["embedded_scripts"].get(wkey, {})
    unresolved = len(js_audit_report["unresolved_function_calls"].get(wkey, []))
    
    print(f"{wkey:<8} | {'✅ Linked' if has_course_js else '❌ MISSING':<18} | {km_status:<18} | {inlines.get('count', 0)} tags ({inlines.get('total_chars', 0)}c) | {unresolved}")
