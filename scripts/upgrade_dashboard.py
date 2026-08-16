#!/usr/bin/env python3
"""
Step 4: Upgrade dashboard.html for robust multi-tab and canonical courseState synchronization.
"""

from pathlib import Path
import re

fp = Path("dashboard.html")
html = fp.read_text(encoding='utf-8')

# Upgrade loadState function in dashboard.html
upgraded_load_state = '''  function loadState(weekNum) {
    let s = localStorage.getItem(`w${weekNum}-state`);
    if (s) {
      try {
        const parsed = JSON.parse(s);
        let doneCount = 0;
        let doneList = [];
        if (parsed.completedDays && typeof parsed.completedDays === 'object') {
          doneList = Object.keys(parsed.completedDays);
          doneCount = doneList.length;
        } else if (Array.isArray(parsed.done)) {
          doneList = parsed.done;
          doneCount = parsed.done.length;
        }
        return {
          xp: typeof parsed.xp === 'number' ? parsed.xp : 0,
          streak: typeof parsed.streak === 'number' ? parsed.streak : 0,
          done: doneList,
          doneCount: doneCount
        };
      } catch(e) {}
    }
    return { xp: 0, streak: 0, done: [], doneCount: 0 };
  }'''

html = re.sub(r'function loadState\(weekNum\)\s*\{[^}]*return\s*\{[^}]*\};\s*\}', upgraded_load_state, html, flags=re.DOTALL)

# Add window storage event listener to dashboard
if "window.addEventListener('storage'" not in html:
    html = html.replace(
      "window.addEventListener('DOMContentLoaded', () => {",
      "window.addEventListener('storage', () => { location.reload(); });\n\n  window.addEventListener('DOMContentLoaded', () => {"
    )

fp.write_text(html, encoding='utf-8')
print("✅ Successfully upgraded dashboard.html with canonical state and multi-tab sync!")
