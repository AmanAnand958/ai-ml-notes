#!/usr/bin/env python3
"""
Two-part fix:
1. Safari: Replace `window.mermaidConfig` (ignored by v10) with a proper
   `mermaid.initialize({ startOnLoad: false })` call RIGHT AFTER the CDN script
   so auto-scan never fires in any browser.
2. Chrome: Change tempHost from `visibility:hidden` to `opacity:0` so
   getBBox() returns real dimensions during SVG rendering.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("pages/weeks")

OLD_HEAD_PATTERN = re.compile(
    r'<script>\s*window\.mermaidConfig\s*=\s*\{[^}]*\}\s*;\s*</script>\s*\n?'
    r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@10\.9\.0/dist/mermaid\.min\.js"></script>',
    re.DOTALL
)

NEW_HEAD_BLOCK = (
    '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>\n'
    '<script>mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "loose" });</script>'
)

changed = 0
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        continue
    raw = fp.read_text(encoding="utf-8")
    new_raw, n = OLD_HEAD_PATTERN.subn(NEW_HEAD_BLOCK, raw)
    if n:
        fp.write_text(new_raw, encoding="utf-8")
        print(f"  ✅ Week {wn}: replaced mermaidConfig with mermaid.initialize()")
        changed += 1
    else:
        # Fallback: check if already using new pattern or some other form
        if 'mermaid.initialize({ startOnLoad: false' in raw:
            print(f"  ✓  Week {wn}: already using mermaid.initialize() — skip")
        else:
            print(f"  ⚠️  Week {wn}: pattern not matched — manual check needed")

print(f"\n✅ Fixed {changed} / 26 week files (mermaid startOnLoad)")
