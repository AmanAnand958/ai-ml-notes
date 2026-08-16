# 📋 Master Open Issues & Discrepancies Task List (191-Day AI/ML Roadmap)

> **Generated on:** 2026-08-15  
> **Status:** ✅ **ALL 29 AUDIT DIMENSIONS RESOLVED & VERIFIED (0 OPEN ISSUES)**  
> **Scope:** All 26 Weeks (`pages/weeks/week1.html` to `pages/weeks/week26.html`) + Root Portals & Shared Assets  

---

## 🎯 Summary of Completed Remediations

| Category | Priority | Status | Target Files / Scope |
| :--- | :---: | :---: | :--- |
| **Root Portal & Curriculum Desync** | 🔴 Critical | ✅ Resolved | `roadmap.html`, `index.html`, `resources.html`, `dashboard.html` (Weeks 19–26 + Theme Switcher) |
| **Broken Navigation Links** | 🔴 High | ✅ Resolved | Weeks 8, 14 (Verified and linked to clean targets) |
| **Code Syntax & Runtime Errors** | 🔴 High | ✅ Resolved | Weeks 1 (AST clean), 5, 12, `course.js` (XP exploit guarded + `toggleSolution` button state + `pre code` selector) |
| **Broken Task Collapsible Toggles** | 🔴 High | ✅ Resolved | Weeks 1–26 (All `.task-header` elements paired with immediate `.task-body` sibling containers) |
| **KaTeX Math & Delimiter Corruption** | 🔴 High | ✅ Resolved | All 26 files (0 `&#36;` corruptions, 0 unescaped entities, balanced math delimiters) |
| **HTML Markup & Tag Balance** | 🔴 High | ✅ Resolved | All 26 week HTML files balanced and valid |
| **Mermaid Syntax & Multiline Errors** | 🔴 High | ✅ Resolved | All 26 Weeks (`-->`, quoted labels, subgraphs, `<br/>` in pipe labels) |
| **Unrendered Text Placeholder Diagrams** | 🟡 Medium | ✅ Resolved | Week 21 (Day 150 converted to active Mermaid flowchart) |
| **XP Badge vs. Button Award Mismatches** | 🟡 Medium | ✅ Resolved | All 18 mismatches harmonized |
| **Duplicate Task Numbers in Same Day** | 🟡 Medium | ✅ Resolved | Week 3 (Day 21) and Week 4 (Day 30) re-indexed to sequential `TASK 2` |
| **Git Commit Block Day Offsets** | 🟡 Medium | ✅ Resolved | Week 6 (Days 38–44 commit numbers matched) |
| **Initial HTML Render Layout Flash (CLS)** | 🟡 Medium | ✅ Resolved | All 26 week HTML files (Days 2..N set to `style="display:none;"`) |
| **Progress Bar Element ID Synchronization** | 🟡 Medium | ✅ Resolved | All 26 files standardized with `#progress-fill` & `#progress-pct` |
| **Missing Tasks `done-when` Boxes** | 🟡 Medium | ✅ Resolved | Added across all tasks lacking completion criteria |
| **Google Fonts `<link>` in `<head>`** | 🟢 Low | ✅ Resolved | Injected into all 26 week files |

---

## 🔴 1. Critical Priority: Root Navigation & Broken Links

- [x] **[roadmap.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/roadmap.html) & [index.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/index.html)**:
  - Add navigation items and content sections for Weeks 19 through 26 (Days 136–191).
  - Update hero header: `<h1>Master AI/ML<br/>in 191 Days</h1>`.
  - Update hero stat: `<div class="stat-val">191</div>` TOTAL DAYS.
  - Update logo subtitle: `191 DAYS · COMPLETE GUIDE`.
- [x] **[roadmap.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/roadmap.html) & [index.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/index.html)**: Added `toggleTheme()` button, `data-theme="light"` styles, and `localStorage` sync.
- [x] **[resources.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/resources.html)**: Added topnav anchor navigation pills for Weeks 19–26.
- [x] **[dashboard.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/dashboard.html)**: Updated initial static placeholder from `0/135` $\rightarrow$ `0/191`.

---

## 🔴 2. High Priority: Syntax, Runtime, Task Toggles & Math Errors

- [x] **[assets/js/course.js](file:///Users/amananand/Downloads/SDE/ai:ml-1/assets/js/course.js)**: `checkPredict()` now guards against XP duplication (`result.dataset.solved = 'true'`, `input.disabled = true`).
- [x] **[assets/js/course.js](file:///Users/amananand/Downloads/SDE/ai:ml-1/assets/js/course.js)**: `toggleSolution(id, btn)` accepts `btn` and toggles between `"💡 Show Solution"` and `"🙈 Hide Solution"`.
- [x] **[assets/js/course.js](file:///Users/amananand/Downloads/SDE/ai:ml-1/assets/js/course.js)**: `highlightUncoloredCode()` targets `pre code` blocks.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Every task header now has an immediate sibling `.task-body` container.
- [x] **[week1.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Cleaned quote escaping in `clean_words` and restored exponent `**` in prime checker.
- [x] **[week12.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week12.html)**: Fixed double closing brace `}}` in `torch.save(...)`.
- [x] **[week5.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week5.html)**: Removed backslash escapes `\'` from `onclick="toggleSolution(...)"`.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Fixed all `&#36;` entity corruptions, balanced delimiters, and unescaped HTML entities inside math expressions.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Fixed all Mermaid diagrams (unescaped `--&gt;`, quoted node shapes, removed orphaned `end`, multiline `<br/>` pipe labels).

---

## 🟡 3. Medium Priority: Layout & Content Parity

- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Added initial `style="display:none;"` to Days 2..N and toolkit sections.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Standardized progress bar IDs (`#progress-fill` & `#progress-pct`).
- [x] **[week21.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week21.html)**: Converted Day 150 placeholder text diagram to an active Mermaid flowchart.
- [x] **[week3.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week3.html) & [week4.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week4.html)**: Re-indexed duplicate `TASK 1` headers to sequential `TASK 2`.
- [x] **[week6.html](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week6.html)**: Corrected git commit day offsets for Days 38–44.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Harmonized all 18 XP badge vs. complete button value mismatches.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Added missing `<div class="done-when">` verification criteria.

---

## 🟢 4. Low Priority: Typography & Quality Polish

- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Added Google Fonts stylesheet link (`IBM Plex Mono`, `Outfit`, `Syne`) to the `<head>` of all 26 week files.
- [x] **[All 26 Weeks](file:///Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week1.html)**: Re-anchored `.week-summary` containers directly under `<main>`.
