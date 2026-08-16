#!/usr/bin/env python3
"""
Wire dashboard.html with canonical assets/js/course.js.
"""

from pathlib import Path

fp = Path("dashboard.html")
html = fp.read_text(encoding='utf-8')

if "assets/js/course.js" not in html:
    html = html.replace("</body>", "<script src=\"assets/js/course.js\"></script>\n</body>")
    fp.write_text(html, encoding='utf-8')
    print("✅ Linked assets/js/course.js inside dashboard.html!")
else:
    print("ℹ️ dashboard.html already has course.js link.")
