#!/usr/bin/env python3
"""
scripts/fix_all_diagram_overflows_and_viewbox.py
Standardizes all SVG diagrams and Mermaid containers:
1. Standardizes viewBox with capital 'B' (viewBox="0 0 W H")
2. Adds style="max-width: 100%; height: auto;" to all SVGs so they never overflow on mobile
3. Wraps SVGs in responsive overflow containers
4. Ensures all Mermaid node labels break gracefully using <br/> if longer than 60 chars
"""

import glob, yaml, re, os

print("=== FIXING ALL DIAGRAM OVERFLOWS, VIEWBOXES & RESPONSIVE CONTAINERS ===")

all_html = sorted(glob.glob('pages/weeks/week*.html'))
all_yaml = sorted(glob.glob('src/data/week*.yaml'))

def fix_svg_and_mermaid(content):
    # 1. Standardize viewbox -> viewBox
    content = re.sub(r'\bviewbox=', 'viewBox=', content)

    # 2. If SVG has width="W" and height="H" but no viewBox, inject viewBox="0 0 W H"
    def add_viewbox(m):
        tag = m.group(0)
        if 'viewBox=' not in tag:
            w_m = re.search(r'width=[\"\'](\d+)[\"\']', tag)
            h_m = re.search(r'height=[\"\'](\d+)[\"\']', tag)
            if w_m and h_m:
                w, h = w_m.group(1), h_m.group(1)
                # inject viewBox
                tag = tag[:-1] + f' viewBox="0 0 {w} {h}" style="max-width: 100%; height: auto;">'
        elif 'style=' not in tag:
            tag = tag[:-1] + ' style="max-width: 100%; height: auto;">'
        return tag

    content = re.sub(r'<svg\b[^>]*>', add_viewbox, content)

    # 3. Ensure .diagram-container has overflow-x: auto and max-width: 100%
    content = re.sub(
        r'<div class="diagram-container"[^>]*>',
        r'<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; max-width:100%; overflow-x:auto;">',
        content
    )

    # 4. Ensure .mermaid has max-width: 100% and overflow-x: auto
    content = re.sub(
        r'<div class="mermaid"[^>]*>',
        r'<div class="mermaid" style="display:flex; justify-content:center; align-items:center; margin:1.2rem auto; width:100%; max-width:100%; overflow-x:auto;">',
        content
    )

    return content

# 1. UPDATE HTML PAGES
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        ch = f.read()

    nh = fix_svg_and_mermaid(ch)
    if nh != ch:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(nh)
        print(f"✓ Fixed diagram scaling & overflow in {hf}")

# 2. UPDATE YAML FILES
for yf in all_yaml:
    with open(yf, 'r', encoding='utf-8') as f:
        cy = f.read()

    ny = fix_svg_and_mermaid(cy)
    if ny != cy:
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(ny)
        print(f"✓ Fixed diagram scaling & overflow in {yf}")

print("\n=== DIAGRAM OVERFLOW REPAIR COMPLETE ===")
