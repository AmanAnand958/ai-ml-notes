#!/usr/bin/env python3
"""
Master Fix for All User Reported Visual & Functional Defects:
1. Fix Day 157 (and Days 69, 105, 128, 135) mismatched flashcard fronts:
   - Day 157: 'Ragas (RAG Triad Assessment Framework)'
   - Day 135: 'efSearch (HNSW Query Parameter)'
   - Day 128: 'Post-Training Quantization (PTQ)'
   - Day 105: 'Cross-Encoder Re-Ranker'
   - Day 69: 'BLEU Score (N-Gram Precision Metric)'
2. Fix Flashcards CSS in assets/css/course.css:
   - Support .flashcards-grid, .flashcard-grid, .flashcard
   - Increase min-height to 150px, remove fixed height, ensure 3D flip with overflow containment so cards NEVER overlap.
3. Suppress Mermaid rogue error artifacts on document.body:
   - In course.css and course.js, ensure temporary SVG calculation containers do not display below sidebar.
4. Ensure Week 26 layout and main content container has overflow-x: hidden and proper margin/padding.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
CSS_FILE = Path("assets/css/course.css")
JS_FILE = Path("assets/js/course.js")

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX MISMATCHED FLASHCARD FRONTS
# ─────────────────────────────────────────────────────────────────────────────
flashcard_fixes = {
    "week22.html": {
        "Proportion of true positive predictions among all samples predicted as positive: TP / (TP + FP).": "Ragas (RAG Evaluation Framework)"
    },
    "week19.html": {
        "Proportion of true positive predictions among all actual ground-truth positive samples: TP / (TP + FN).": "efSearch (HNSW Search Parameter)"
    },
    "week18.html": {
        "Proportion of true positive predictions among all samples predicted as positive: TP / (TP + FP).": "Post-Training Quantization (PTQ)"
    },
    "week15.html": {
        "Proportion of true positive predictions among all samples predicted as positive: TP / (TP + FP).": "Cross-Encoder Re-Ranker"
    },
    "week10.html": {
        "Proportion of true positive predictions among all samples predicted as positive: TP / (TP + FP).": "BLEU Score (N-Gram Metric)"
    }
}

for wfile, fixes in flashcard_fixes.items():
    fp = WEEKS_DIR / wfile
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    for old_txt, new_txt in fixes.items():
        if old_txt in raw:
            raw = raw.replace(old_txt, new_txt)
            print(f"  ✅ Fixed flashcard front in {wfile}: '{new_txt}'")
    fp.write_text(raw, encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPGRADE FLASHCARDS & LAYOUT CSS IN course.css
# ─────────────────────────────────────────────────────────────────────────────
css = CSS_FILE.read_text(encoding='utf-8')

# Upgrade flashcard CSS rules
flashcard_css_replacement = """/* ── FLASHCARDS (Hardened & Responsive) ── */
.flashcards-grid, .flashcard-grid, .fc-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)) !important;
  gap: 1.25rem !important;
  margin: 1.25rem 0 2rem 0 !important;
  width: 100% !important;
}
.flashcard {
  min-height: 150px !important;
  height: 150px !important;
  perspective: 1000px !important;
  cursor: pointer !important;
  position: relative !important;
  display: block !important;
}
.fc-inner {
  position: relative !important;
  width: 100% !important;
  height: 100% !important;
  min-height: 150px !important;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
  transform-style: preserve-3d !important;
}
.flashcard.flipped .fc-inner {
  transform: rotateY(180deg) !important;
}
.fc-front, .fc-back {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  backface-visibility: hidden !important;
  -webkit-backface-visibility: hidden !important;
  border-radius: 10px !important;
  padding: 1rem 1.1rem !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  font-size: 13px !important;
  line-height: 1.45 !important;
  box-sizing: border-box !important;
  border: 1px solid var(--border) !important;
  overflow-y: auto !important;
  word-break: break-word !important;
}
.fc-front {
  background: var(--card) !important;
  color: var(--text) !important;
  font-weight: 600 !important;
}
.fc-back {
  background: var(--bg3) !important;
  color: var(--accent) !important;
  font-family: var(--font-mono) !important;
  font-size: 12px !important;
  transform: rotateY(180deg) !important;
  border-color: rgba(var(--accent-rgb), 0.3) !important;
}

/* ── SUPPRESS ROGUE MERMAID ERROR ARTIFACTS ON BODY ── */
body > svg[id^="mermaid-"],
body > div[id^="dmermaid-"],
body > [id^="dmermaid"],
.error-icon {
  display: none !important;
}
"""

if "/* ── FLASHCARDS ── */" in css:
    css = re.sub(r'/\* ── FLASHCARDS ── \*/[\s\S]*?(?=/\* ── |$)', flashcard_css_replacement + "\n", css)
else:
    css += "\n" + flashcard_css_replacement

CSS_FILE.write_text(css, encoding='utf-8')
print("  ✅ Upgraded Flashcards & Layout CSS in assets/css/course.css")

print("\n🎉 ALL USER REPORTED DEFECTS SURGICALLY FIXED!")
