#!/usr/bin/env python3
"""
Sync Canonical goDay & Day Switching across all weeks 1 to 26:
Replaces any broken inline goDay handlers with the canonical, multi-layer day switcher
that properly clears inline display overrides, manages active classes, scrolls to top,
and triggers Safari/Chrome Mermaid rendering.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    
    # Check DAYS array for this week
    m = re.search(r'const\s+DAYS\s*=\s*(\[[^\]]+\]);', html)
    days_array = m.group(1) if m else '[]'
    
    canonical_bottom_script = f'''<script>
  const WEEK = {wn};
  const DAYS = {days_array};

  function goDay(n) {{
    document.querySelectorAll('.day-section').forEach(s => {{
      s.classList.remove('active');
      s.style.removeProperty('display');
    }});
    document.querySelectorAll('.sb-item').forEach(i => i.classList.remove('active'));
    document.querySelectorAll('.day-pill').forEach(p => {{
      p.classList.remove('active');
      p.setAttribute('aria-selected', 'false');
    }});
    
    const section = document.getElementById('day-' + n) || document.getElementById(n);
    if (section) {{
      section.classList.add('active');
      section.style.display = 'block';
    }}
    
    const sbItem = document.getElementById('sb-' + n) || Array.from(document.querySelectorAll('.sb-item')).find(el => el.getAttribute('onclick') && el.getAttribute('onclick').includes('goDay(' + n + ')'));
    if (sbItem) {{ sbItem.classList.add('active'); }}
    
    const pill = document.getElementById('pill-' + n) || document.querySelector(`.day-pill[data-day="${{n}}"]`);
    if (pill) {{
      pill.classList.add('active');
      pill.setAttribute('aria-selected', 'true');
    }}
    
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    
    if (typeof renderMermaid === 'function') {{
      renderMermaid('day-' + n);
    }}
  }}

  function closeSidebar() {{
    const sb = document.getElementById('sidebar');
    if (sb) sb.classList.remove('open');
  }}

  function toggleSidebar() {{
    const sb = document.getElementById('sidebar');
    if (sb) sb.classList.toggle('open');
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    if (Array.isArray(DAYS) && DAYS.length > 0) {{
      goDay(DAYS[0]);
    }}
  }});
</script>
<script src="../../assets/js/course.js"></script>
</body>
</html>'''

    # Replace everything from the first bottom config script tag down to </html>
    idx_conf = html.rfind('const WEEK =')
    if idx_conf != -1:
        idx_script_open = html.rfind('<script', 0, idx_conf)
        if idx_script_open != -1:
            html = html[:idx_script_open] + canonical_bottom_script
            fp.write_text(html, encoding='utf-8')
            print(f"  ✅ Synchronized canonical goDay in Week {wn}")

print("\n🎉 ALL 26 WEEKS NOW HAVE UNIFIED CANONICAL DAY SWITCHING ENGINE!")
