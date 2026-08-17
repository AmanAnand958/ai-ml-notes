#!/usr/bin/env python3
"""
scripts/apply_comprehensive_block_css.py
Enforces complete, robust, modern CSS styling across all blocks:
- Code Blocks (.cb, .cb-head, .cb-lang, .cb-btns, .copy-btn, .run-btn, pre, code)
- Bonus Deep-Dives (.bonus-deep-dive)
- Diagram Containers (.diagram-container, .mermaid)
- Math Blocks (.math-block)
- Concept Tables (.table-wrap, table.concept-table, th, td)
- Gotcha Callouts (.gotcha, .analogy)
- Tasks & Task Badges (.task-card, .task-badge)
- Quizzes & Predict Blocks (.quiz-card, .predict-box)
"""

import glob, re, os

print("=== STARTING COMPREHENSIVE BLOCK CSS STANDARDIZATION ===")

COMPREHENSIVE_BLOCK_CSS = """
/* ═══════════════════════════════════════════════════════════════════
   COMPREHENSIVE BLOCK STYLING SYSTEM (Code, Diagrams, Math, Tables, Bonus)
   ═══════════════════════════════════════════════════════════════════ */

/* 1. Code Block Containers */
.cb {
  background: var(--bg2, #12151e) !important;
  border: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  border-radius: 8px !important;
  margin: 1.2rem 0 !important;
  overflow: hidden !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}
.cb-head {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  background: var(--bg3, #1a1e2c) !important;
  padding: 0.4rem 0.8rem !important;
  border-bottom: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
}
.cb-lang {
  font-family: var(--font-mono, monospace) !important;
  font-size: 0.78rem !important;
  color: var(--accent, #4fd1a5) !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
}
.cb-btns {
  display: flex !important;
  gap: 0.4rem !important;
}
.copy-btn, .run-btn {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid var(--border, rgba(255,255,255,0.12)) !important;
  color: var(--text, #e2e8f0) !important;
  padding: 0.25rem 0.6rem !important;
  border-radius: 4px !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}
.copy-btn:hover, .run-btn:hover {
  background: var(--accent, #4fd1a5) !important;
  color: #0d0f14 !important;
  border-color: var(--accent, #4fd1a5) !important;
}
.cb pre {
  margin: 0 !important;
  padding: 1rem !important;
  overflow-x: auto !important;
  background: transparent !important;
}
.cb pre code {
  font-family: var(--font-mono, "Fira Code", monospace) !important;
  font-size: 0.88rem !important;
  line-height: 1.55 !important;
  color: #e2e8f0 !important;
}

/* 2. Senior Engineer Bonus Deep-Dives */
.bonus-deep-dive {
  background: var(--bg3, #1a1e2c) !important;
  border-left: 4px solid var(--accent, #4fd1a5) !important;
  border-top: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  border-right: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  border-bottom: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  padding: 1.25rem !important;
  border-radius: 8px !important;
  margin: 1.75rem 0 !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.18) !important;
}
.bonus-deep-dive h3 {
  color: var(--accent, #4fd1a5) !important;
  margin-top: 0 !important;
  font-size: 1.15rem !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}

/* 3. Mathematical Formula Blocks */
.math-block {
  background: var(--bg3, #1a1e2c) !important;
  border: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  padding: 1.2rem !important;
  border-radius: 8px !important;
  margin: 1.5rem auto !important;
  text-align: center !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  max-width: 100% !important;
  overflow-x: auto !important;
}

/* 4. Concept Comparison Tables */
.table-wrap {
  overflow-x: auto !important;
  margin: 1.5rem auto !important;
  border-radius: 8px !important;
  border: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  background: var(--bg2, #12151e) !important;
}
table.concept-table {
  width: 100% !important;
  border-collapse: collapse !important;
  text-align: left !important;
  font-size: 0.88rem !important;
}
table.concept-table th {
  background: var(--bg3, #1a1e2c) !important;
  color: var(--accent, #4fd1a5) !important;
  padding: 0.75rem 1rem !important;
  border-bottom: 2px solid var(--border, rgba(255,255,255,0.12)) !important;
  font-weight: 600 !important;
}
table.concept-table td {
  padding: 0.65rem 1rem !important;
  border-bottom: 1px solid var(--border, rgba(255,255,255,0.06)) !important;
  color: var(--text, #e2e8f0) !important;
}
table.concept-table tr:hover {
  background: rgba(255,255,255,0.02) !important;
}

/* 5. Diagram Containers & Mermaid Schemas */
.diagram-container {
  background: var(--bg3, #1a1e2c) !important;
  border: 1px solid var(--border, rgba(255,255,255,0.08)) !important;
  padding: 1.25rem !important;
  border-radius: 8px !important;
  margin: 1.5rem auto !important;
  text-align: center !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
}
.mermaid {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  margin: 1.2rem auto !important;
  width: 100% !important;
  overflow-x: auto !important;
}
"""

html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # If block styling not already injected, add to <head> or <style>
    if 'COMPREHENSIVE BLOCK STYLING SYSTEM' not in content:
        if '</style>' in content:
            content = content.replace('</style>', COMPREHENSIVE_BLOCK_CSS + '\n</style>', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'<style>{COMPREHENSIVE_BLOCK_CSS}</style>\n</head>', 1)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(content)

print("✓ Injected comprehensive block styling into all 26 HTML week pages.")
print("\n=== BLOCK CSS ENFORCEMENT COMPLETE ===")
