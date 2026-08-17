#!/usr/bin/env python3
"""
scripts/fix_all_syntax_and_tag_anomalies.py
Remediates all discovered syntax errors:
1. Malformed div tag in pages/weeks/week17.html
2. Malformed LaTeX/HTML formula in pages/weeks/week12.html
3. Extra </pre> tags in src/data/week02.yaml (Day 13)
4. Leftover <hN> class= in src/data/week02.yaml (Day 10) and week04.yaml (Day 23)
"""

import yaml, re, os, glob

print("=== FIXING ALL SYNTAX AND HTML TAG ANOMALIES ===")

# 1. FIX week17.html
w17_path = 'pages/weeks/week17.html'
if os.path.exists(w17_path):
    with open(w17_path, 'r', encoding='utf-8') as f:
        c17 = f.read()
    c17 = re.sub(r'<div --="" <!--="" day-124="">', '<!-- /day-124 -->', c17)
    with open(w17_path, 'w', encoding='utf-8') as f:
        f.write(c17)
    print("✓ Fixed malformed div comment in pages/weeks/week17.html")

# 2. FIX week12.html
w12_path = 'pages/weeks/week12.html'
if os.path.exists(w12_path):
    with open(w12_path, 'r', encoding='utf-8') as f:
        c12 = f.read()
    c12 = re.sub(
        r'\$\$w_t = \\arg\\max_\{w \\in \\mathcal\{V\}\} P\(w \\mid w_\{[\s\S]*?</t\},>\s*</span>',
        r'$$w_t = \\arg\\max_{w \\in \\mathcal{V}} P(w \\mid w_{<t}, \\mathbf{x})$$\n        </span>\n        <span class="desc">\n         Where the model grabs the single best token immediately.\n        </span>',
        c12
    )
    with open(w12_path, 'w', encoding='utf-8') as f:
        f.write(c12)
    print("✓ Fixed LaTeX/HTML formula tag in pages/weeks/week12.html")

# 3. FIX week02.yaml (Day 13 & Day 10)
w02_path = 'src/data/week02.yaml'
if os.path.exists(w02_path):
    with open(w02_path, 'r', encoding='utf-8') as f:
        c02 = f.read()
    # Fix Day 10 <h3 class=
    c02 = re.sub(r'<h3\s*>\s*class=', '<h3 class=', c02)
    c02 = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', c02)
    # Fix Day 13 extra </pre>
    c02 = c02.replace('</pre>\n</pre>', '</pre>')
    with open(w02_path, 'w', encoding='utf-8') as f:
        f.write(c02)
    print("✓ Fixed syntax issues in src/data/week02.yaml")

# 4. FIX week04.yaml (Day 23)
w04_path = 'src/data/week04.yaml'
if os.path.exists(w04_path):
    with open(w04_path, 'r', encoding='utf-8') as f:
        c04 = f.read()
    c04 = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', c04)
    with open(w04_path, 'w', encoding='utf-8') as f:
        f.write(c04)
    print("✓ Fixed syntax issues in src/data/week04.yaml")

# 5. SCAN ALL YAML AND HTML FOR ANY REMAINING <h[1-6]> class=
for yf in glob.glob('src/data/week*.yaml'):
    with open(yf, 'r', encoding='utf-8') as f:
        cy = f.read()
    ny = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', cy)
    if ny != cy:
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(ny)

for hf in glob.glob('pages/weeks/week*.html'):
    with open(hf, 'r', encoding='utf-8') as f:
        ch = f.read()
    nh = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', ch)
    if nh != ch:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(nh)

print("\n=== ALL SYNTAX AND TAG ANOMALIES REMEDIATED ===")
