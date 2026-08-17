#!/usr/bin/env python3
"""
scripts/center_all_diagrams_and_visuals.py
Applies centered layout styling across all diagrams, SVGs, Mermaid blocks, Canvases, Tables, and Math formulas
across all 26 HTML week files and YAML data sources.
"""

import glob, yaml, re, os

print("=== STARTING DIAGRAM & VISUAL CENTERING ENGINE ===")

# -------------------------------------------------------------
# 1. UPDATE CSS STYLES IN ALL 26 HTML FILES
# -------------------------------------------------------------
print("Injecting global centering CSS rules into HTML files...")

CENTER_CSS = """
/* Auto-Center All Diagrams, Mermaid, SVGs, Canvases, and Math Blocks */
.diagram-container, .math-block, .table-wrap {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  align-items: center !important;
  text-align: center !important;
  margin: 1.5rem auto !important;
  max-width: 100% !important;
}
.mermaid {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  margin: 1.2rem auto !important;
  text-align: center !important;
  width: 100% !important;
}
.mermaid svg {
  display: block !important;
  margin: 0 auto !important;
  max-width: 100% !important;
}
svg {
  display: block !important;
  margin: 1.2rem auto !important;
  max-width: 100% !important;
  height: auto !important;
}
canvas {
  display: block !important;
  margin: 1.2rem auto !important;
}
table.concept-table {
  margin: 1rem auto !important;
}
"""

html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS before </style> or inside <head>
    if 'Auto-Center All Diagrams' not in content:
        if '</style>' in content:
            content = content.replace('</style>', CENTER_CSS + '\n</style>', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'<style>{CENTER_CSS}</style>\n</head>', 1)

    # Ensure diagram containers have text-align:center and margin:auto
    content = re.sub(
        r'<div class="diagram-container"[^>]*>',
        r'<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">',
        content
    )

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(content)

print("✓ All 26 HTML week pages updated with responsive centering rules.")

# -------------------------------------------------------------
# 2. UPDATE YAML DATA SOURCES
# -------------------------------------------------------------
print("Standardizing diagram container attributes in YAML files...")
yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'<div class="diagram-container"[^>]*>',
        r'<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">',
        content
    )

    with open(yf, 'w', encoding='utf-8') as f:
        f.write(content)

print("✓ All YAML source files updated.")
print("\n=== DIAGRAM & VISUAL CENTERING COMPLETE ===")
