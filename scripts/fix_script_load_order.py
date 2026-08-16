#!/usr/bin/env python3
"""
Fix the script loading order and goDay rendering across all 26 week HTML files.

Problems found:
1. mermaid.min.js and course.js are at bottom of <body>, AFTER the inline goDay script.
   DOMContentLoaded fires goDay() -> renderMermaid() before mermaid library is loaded.
2. window.mermaidConfig is set AFTER mermaid.min.js in some files.

Fix:
1. In ALL 26 weeks, move the mermaid config+script tags to <head> (before body content).
2. Update goDay() in the inline script to call renderMermaid with a delay after mermaid loads.
3. Update the body-bottom scripts to only include course.js (mermaid moved to head).
"""

from pathlib import Path
import re

WEEKS_DIR = Path("pages/weeks")

MERMAID_HEAD_BLOCK = """<script>window.mermaidConfig = { startOnLoad: false };</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>"""

def fix_week(wn):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        print(f"  ⚠️  Week {wn} not found, skipping")
        return
    
    raw = fp.read_text(encoding='utf-8')
    changed = False
    
    # 1. Remove window.mermaidConfig inline script blocks (anywhere in body)
    raw = re.sub(
        r'<script>\s*window\.mermaidConfig\s*=\s*\{[^}]*\}\s*;?\s*window\.mermaid\s*=\s*\{[^}]*\}\s*;?\s*</script>\s*\n?',
        '', raw
    )
    raw = re.sub(
        r'<script>\s*window\.mermaidConfig\s*=\s*\{[^}]*\}\s*;?\s*</script>\s*\n?',
        '', raw
    )
    
    # 2. Remove all mermaid CDN script tags from body
    raw = re.sub(
        r'<script[^>]*mermaid[^>]*></script>\s*\n?',
        '', raw
    )
    
    # 3. Inject mermaid config + script into <head> (right before </head>)
    if 'mermaid@10.9.0' not in raw:
        raw = raw.replace('</head>', MERMAID_HEAD_BLOCK + '\n</head>')
        changed = True
    else:
        # It was removed from body and needs to be in head
        if 'mermaid@10.9.0' not in raw:
            raw = raw.replace('</head>', MERMAID_HEAD_BLOCK + '\n</head>')
        changed = True
    
    # 4. Update the inline goDay script to use a mermaid-ready render call
    # Replace the renderMermaid call in goDay with a delayed call that waits for mermaid
    MERMAID_CALL_OLD = r'if \(typeof renderMermaid === \'function\'\) \{\s*renderMermaid\(\'day-\' \+ n\);\s*\}'
    MERMAID_CALL_NEW = """if (typeof renderMermaid === 'function') {
      // Small delay ensures section is visible before rendering
      setTimeout(() => renderMermaid('day-' + n), 50);
    }"""
    raw, count = re.subn(MERMAID_CALL_OLD, MERMAID_CALL_NEW, raw)
    if count > 0:
        changed = True
    
    fp.write_text(raw, encoding='utf-8')
    print(f"  ✅ Fixed script order in Week {wn}")

for wn in range(1, 27):
    fix_week(wn)

print("\n✅ Script loading order fixed across all 26 weeks!")
print("   Mermaid CDN is now in <head> so it's loaded before DOMContentLoaded fires.")
