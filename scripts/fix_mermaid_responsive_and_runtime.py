#!/usr/bin/env python3
"""
Step 2:
1. Ensure .mermaid CSS rules across all 26 weeks have full responsive overflow-x: auto.
2. Upgrade renderMermaid() in assets/js/course.js to automatically sanitize newlines in quoted labels at runtime.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

# 1. Update CSS across all weeks
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Check if .mermaid has overflow-x: auto
    if ".mermaid {" in raw and "overflow-x: auto" not in raw:
        raw = raw.replace(
            ".mermaid {",
            ".mermaid {\n  overflow-x: auto;\n  max-width: 100%;\n  -webkit-overflow-scrolling: touch;\n  margin: 1.2rem 0;\n  padding: 10px;\n  background: var(--bg2, #141720);\n  border-radius: 8px;\n  border: 1px solid var(--border, #2a3050);"
        )
        fp.write_text(raw, encoding='utf-8')
        print(f"  ✅ Added responsive overflow-x to .mermaid in Week {wn}")

# 2. Hardened renderMermaid in course.js
fp_js = ROOT_DIR / "assets" / "js" / "course.js"
js = fp_js.read_text(encoding='utf-8')

# Ensure renderMermaid cleans newlines inside quotes
if "raw.replace" in js:
    js = js.replace(
        "raw = raw.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '\"').replace(/&amp;/g, '&').trim();",
        """raw = raw.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '\"').replace(/&amp;/g, '&').trim();
      // Replace raw newlines inside quoted labels with <br/>
      raw = raw.replace(/\"[^\"]*\"/g, (q) => q.replace(/\\n/g, '<br/>'));"""
    )
    fp_js.write_text(js, encoding='utf-8')
    print("✅ Hardened runtime Mermaid quote sanitizer in assets/js/course.js!")

print("\n🎉 STEP 2 COMPLETE: RESPONSIVE MERMAID VIEWPORT & RUNTIME SANITIZER INSTALLED!")
