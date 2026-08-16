#!/usr/bin/env python3
"""
Integrate Canonical renderMermaid into course.js & trigger on goDay and DOMContentLoaded.
"""

from pathlib import Path

fp = Path("/Users/amananand/Downloads/SDE/ai:ml-1/assets/js/course.js")
js = fp.read_text(encoding='utf-8')

# Check if renderMermaid is already present
if "function renderMermaid" not in js:
    render_func = '''
// ── 9. MERMAID RENDERING ENGINE ──────────────────────────────────
function renderMermaid(dayId) {
  let retries = 0;
  const run = () => {
    if (typeof mermaid === 'undefined') {
      retries++;
      if (retries < 20) {
        setTimeout(run, 100);
      } else {
        console.warn('Mermaid library not loaded (CDN offline or blocked).');
      }
      return;
    }
    if (!window.mermaidInitialized) {
      mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose' });
      window.mermaidInitialized = true;
    }
    const sec = document.getElementById(dayId) || document.getElementById('day-' + dayId) || document;
    const nodes = sec.querySelectorAll('.mermaid:not([data-rendered])');
    if (!nodes.length) return;
    if (mermaid.run) {
      mermaid.run({ nodes }).then(() => {
        nodes.forEach(n => n.setAttribute('data-rendered','1'));
      }).catch((err) => { console.error('Mermaid render error:', err); });
    } else if (mermaid.init) {
      mermaid.init(undefined, nodes);
      nodes.forEach(n => n.setAttribute('data-rendered','1'));
    }
  };
  run();
}
'''
    # Append to course.js
    js += render_func
    
    # Trigger renderMermaid inside goDay
    js = js.replace(
        "window.scrollTo({ top: 0, behavior: 'smooth' });",
        "window.scrollTo({ top: 0, behavior: 'smooth' });\n  renderMermaid(dayId);"
    )
    
    # Trigger renderMermaid on DOMContentLoaded
    js = js.replace(
        "syncUI();",
        "syncUI();\n  const firstSec = document.querySelector('.day-section.active');\n  if (firstSec) renderMermaid(firstSec.id);"
    )
    
    fp.write_text(js, encoding='utf-8')
    print("✅ Successfully integrated renderMermaid into assets/js/course.js!")

# Also update the inline goDay in week26.html
fp26 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week26.html")
w26 = fp26.read_text(encoding='utf-8')
if "renderMermaid" not in w26:
    w26 = w26.replace(
        "window.scrollTo({ top: 0, behavior: 'smooth' });",
        "window.scrollTo({ top: 0, behavior: 'smooth' });\n    if (typeof renderMermaid === 'function') renderMermaid('day-' + dayId);"
    )
    fp26.write_text(w26, encoding='utf-8')
    print("✅ Updated week26.html goDay with renderMermaid call!")
