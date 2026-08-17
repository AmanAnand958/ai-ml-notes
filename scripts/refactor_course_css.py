#!/usr/bin/env python3
"""
Refactors and cleans course.css:
1. Consolidates light theme into a single source of truth at the top.
2. Fixes .main, .main-content spacing and padding.
3. Fixes invalid CSS (1px stroke -> 1px solid).
4. Unifies color tokens (replaces rogue Catppuccin hex codes with design variables).
5. Adds robust mobile responsive rules for breadcrumbs, day-pills, and badges.
"""

import re

with open('assets/css/course.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Fix invalid CSS: "1px stroke" -> "1px solid"
css = css.replace('1px stroke', '1px solid')

# 2. Fix rogue hex codes in utility/callouts
css = css.replace('#89b4fa', 'var(--blue)')
css = css.replace('#cba6f7', 'var(--purple)')
css = css.replace('#a6e3a1', 'var(--green)')
css = css.replace('#f9e2af', 'var(--orange)')
css = css.replace('rgba(137, 180, 250, 0.05)', 'rgba(var(--blue-rgb), 0.05)')
css = css.replace('rgba(203, 166, 247, 0.08)', 'rgba(var(--purple-rgb), 0.08)')
css = css.replace('rgba(203, 166, 247, 0.05)', 'rgba(var(--purple-rgb), 0.05)')
css = css.replace('rgba(166, 227, 161, 0.05)', 'rgba(var(--green-rgb), 0.05)')
css = css.replace('rgba(249, 226, 175, 0.04)', 'rgba(var(--orange-rgb), 0.04)')

# 3. Replace duplicate light theme override block around line 1805
duplicate_light_block = """/* ── LIGHT THEME OVERRIDES ── */
[data-theme="light"] {
  --bg: #f8fafc;
  --bg2: #f1f5f9;
  --bg3: #e2e8f0;
  --card: #ffffff;
  --border: #cbd5e1;
  --text: #0f172a;
  --muted: #475569;
}
[data-theme="light"] .topnav {
  background: rgba(248, 250, 252, 0.85);
  border-bottom-color: #cbd5e1;
}
[data-theme="light"] .card,
[data-theme="light"] .day-card,
[data-theme="light"] .res-card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}"""

css = css.replace(duplicate_light_block, "/* Light theme consolidated at top of stylesheet */")

# 4. Ensure .main and .main-content have proper padding and max-width
css = re.sub(
    r'/\* ── MAIN ── \*/\s*\.main\s*\{[^}]*\}',
    """/* ── MAIN ── */
.main,
.main-content {
  flex: 1;
  min-width: 0;
  max-width: 880px;
  margin: 0 auto;
  padding: 2.5rem 2rem 5rem;
  box-sizing: border-box;
  width: 100%;
}""",
    css
)

# 5. Insert comprehensive Light Mode design tokens after :root
light_theme_definition = """
/* ── CONSOLIDATED LIGHT THEME PALETTE & COMPONENT STYLES ── */
[data-theme="light"],
.light-theme {
  --bg: #f8fafc;
  --bg2: #ffffff;
  --bg3: #f1f5f9;
  --card: #ffffff;
  --border: #e2e8f0;
  --border2: rgba(0, 0, 0, 0.08);
  --text: #0f172a;
  --muted: #64748b;

  --accent: #4f46e5;
  --accent-rgb: 79, 70, 229;
  --accent-secondary: #7c3aed;
  --accent-sec-rgb: 124, 58, 237;

  --blue: #2563eb;
  --blue-rgb: 37, 99, 235;
  --purple: #7c3aed;
  --purple-rgb: 124, 58, 237;
  --green: #059669;
  --green-rgb: 5, 150, 105;
  --orange: #d97706;
  --orange-rgb: 217, 119, 6;
  --pink: #db2777;
  --pink-rgb: 219, 39, 119;
}

[data-theme="light"] .topnav,
.light-theme .topnav {
  background: rgba(255, 255, 255, 0.88);
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
[data-theme="light"] .sidebar,
.light-theme .sidebar {
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
}
[data-theme="light"] .day-header,
.light-theme .day-header {
  border-bottom: 1px solid #e2e8f0;
}
[data-theme="light"] .task-block,
.light-theme .task-block {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
[data-theme="light"] .task-header,
.light-theme .task-header {
  background: #ffffff;
}
[data-theme="light"] .task-body,
.light-theme .task-body {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}
[data-theme="light"] .cb,
.light-theme .cb {
  background: #0f172a;
  border-color: #1e293b;
}
[data-theme="light"] .cb-head,
.light-theme .cb-head {
  background: #1e293b;
  border-bottom-color: #334155;
  color: #94a3b8;
}
[data-theme="light"] .quiz-block,
.light-theme .quiz-block {
  background: #ffffff;
  border: 1px solid #e2e8f0;
}
[data-theme="light"] .quiz-opt,
.light-theme .quiz-opt {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #1e293b;
}
[data-theme="light"] .quiz-opt:hover,
.light-theme .quiz-opt:hover {
  background: #f1f5f9;
  border-color: var(--accent);
}
[data-theme="light"] .flashcard,
.light-theme .flashcard {
  background: #ffffff;
  border-color: #e2e8f0;
}
[data-theme="light"] .fc-front,
.light-theme .fc-front {
  background: #ffffff;
  color: #0f172a;
}
[data-theme="light"] .fc-back,
.light-theme .fc-back {
  background: #f8fafc;
  color: #0f172a;
}
[data-theme="light"] .gotcha-box,
.light-theme .gotcha-box {
  background: rgba(217, 119, 6, 0.06);
  border-color: rgba(217, 119, 6, 0.3);
}
[data-theme="light"] .takeaways,
.light-theme .takeaways {
  background: rgba(5, 150, 105, 0.06);
  border-color: rgba(5, 150, 105, 0.3);
}
[data-theme="light"] .resource-card,
.light-theme .resource-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
}
"""

if '[data-theme="light"]' not in css[:500]:
    # Insert after :root block
    m_root = re.search(r'\}\n', css)
    if m_root:
        pos = m_root.end()
        css = css[:pos] + light_theme_definition + css[pos:]

# 6. Enhance Mobile responsive rules
mobile_rules = """
/* ── COMPREHENSIVE MOBILE VIEWPORT RULES (320px - 768px) ── */
@media (max-width: 768px) {
  .topnav {
    padding: 0.5rem 0.8rem;
    gap: 0.5rem;
  }
  .nav-breadcrumbs {
    max-width: 140px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 11.5px;
  }
  .brand {
    font-size: 11.5px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .xp-display,
  .streak-display {
    font-size: 11px;
    padding: 2px 6px;
  }
  .level-badge {
    display: none;
  }
  .prog-wrap {
    display: none;
  }
  .day-pills {
    overflow-x: auto;
    flex-wrap: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    max-width: 100%;
    padding: 2px 0;
  }
  .main,
  .main-content {
    padding: 1.5rem 1rem 4rem;
  }
  .day-header h1 {
    font-size: 1.5rem;
  }
  .concept-map-flow {
    overflow-x: auto;
    flex-wrap: wrap;
    white-space: normal;
  }
  .quick-jumps {
    border-radius: 16px;
    padding: 6px 8px;
  }
  .jump-btn {
    padding: 4px 10px;
    font-size: 11px;
  }
}
"""
css += "\n" + mobile_rules

with open('assets/css/course.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('pages/weeks/course.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("✅ Successfully refactored course.css & pages/weeks/course.css")
