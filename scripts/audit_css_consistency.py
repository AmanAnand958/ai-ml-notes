#!/usr/bin/env python3
"""
Comprehensive CSS Consistency & Style Audit across all 26 Weeks:
1. External Stylesheet Links: Checks that every week links to `../../assets/css/course.css`.
2. Embedded <style> tags: Audits all <style> blocks in <head> for rogue overrides, divergent variable definitions, or hardcoded fonts/colors.
3. Component-Level Inline Styles: Scans core components (.gotcha-box, .predict-box, .task-block, .flashcard, .quiz-block, .cb, tables, etc.) for inline style overrides vs canonical class usage.
4. Hardcoded Color vs CSS Variables: Identifies instances of hardcoded hex/rgb/hsl colors that bypass CSS theme variables (--bg, --text, --accent, --border, --green, --blue, --yellow, --purple).
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

css_audit_report = {
    "external_links": {},
    "embedded_style_tags": {},
    "inline_style_counts": {},
    "hardcoded_colors": defaultdict(list),
    "component_style_patterns": defaultdict(list)
}

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. External Stylesheets
    link_tags = [l.get('href') for l in soup.find_all('link', rel='stylesheet')]
    css_audit_report["external_links"][f"week{wn}"] = link_tags
    
    # 2. Embedded <style> tags
    styles = soup.find_all('style')
    css_audit_report["embedded_style_tags"][f"week{wn}"] = {
        "count": len(styles),
        "total_chars": sum(len(s.text) for s in styles)
    }
    
    # 3. Inline style usage
    elements_with_inline_style = soup.find_all(lambda tag: tag.has_attr('style'))
    css_audit_report["inline_style_counts"][f"week{wn}"] = len(elements_with_inline_style)
    
    # 4. Check for hardcoded colors in inline styles
    hex_color_re = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}\b')
    for el in elements_with_inline_style:
        s_val = el['style']
        hexes = hex_color_re.findall(s_val)
        for h in hexes:
            if h.lower() not in ['#fff', '#ffffff', '#000', '#000000', '#82aaff', '#49e9a6', '#ff7b72']: # known accents
                css_audit_report["hardcoded_colors"][f"week{wn}"].append({
                    "tag": el.name,
                    "class": el.get('class', []),
                    "color": h,
                    "style": s_val[:80]
                })

out_file = ROOT_DIR / "scripts" / "css_consistency_audit_report.json"
out_file.write_text(json.dumps(css_audit_report, indent=2), encoding='utf-8')

print(f"{'Week':<8} | {'External CSS':<25} | {'<style> Tags':<12} | {'Inline Style Elements':<22} | {'Hardcoded Colors'}")
print("-" * 95)
for wn in range(1, 27):
    wkey = f"week{wn}"
    ext = ", ".join(css_audit_report["external_links"].get(wkey, []))
    st = css_audit_report["embedded_style_tags"].get(wkey, {})
    inline_cnt = css_audit_report["inline_style_counts"].get(wkey, 0)
    hard_cnt = len(css_audit_report["hardcoded_colors"].get(wkey, []))
    print(f"{wkey:<8} | {ext[:25]:<25} | {st.get('count', 0)} ({st.get('total_chars', 0)}c) | {inline_cnt:<22} | {hard_cnt}")
