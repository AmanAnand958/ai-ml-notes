#!/usr/bin/env python3
"""
fix_week20_safe.py — Week 20 targeted string-only fixes (no BeautifulSoup to protect math).

Fixes:
  8. Wrong day number: "Day 20 Task 2:" → "Day 147 Task 2:"
  7. Generic takeaway bullets replaced per day
  9. Unescaped < in math (none found in week20)
  1. KaTeX control chars (none found in week20)
"""

import re

html = open("pages/weeks/week20.html", encoding="utf-8").read()
original_dd = html.count("$$")
changes = []

# FIX 8: Wrong day number docstring
OLD8 = "# Day 20 Task 2: Vector Memory Engine with Temporal Recency Decay"
NEW8 = "# Day 147 Task 2: Vector Memory Engine with Temporal Recency Decay"
if OLD8 in html:
    html = html.replace(OLD8, NEW8, 1)
    changes.append("Fixed wrong day docstring: Day20→Day147")

# FIX 7: Replace generic takeaway bullets per day section
GENERIC = "Validate downstream integration tests and establish automated performance benchmark gates."

REPLACEMENTS = {
    "day-143": "ReAct agents must have a step limit (max_iterations) and a timeout — without them, a misconfigured tool or API failure causes an infinite reasoning loop.",
    "day-144": "Validate all LLM-generated JSON with Pydantic before passing to downstream services — structured output schemas reduce tool-call failure rate by 70-85%.",
    "day-145": "Use asyncio.gather() for parallel tool calls in multi-agent systems but set asyncio.timeout() on each — a slow tool blocks the entire supervisor otherwise.",
    "day-146": "Evaluate agent performance with task-completion rate, not just final answer quality — intermediate tool errors that recover silently indicate fragile reasoning chains.",
    "day-147": "When building vector memory for agents, expire embeddings older than N days — stale context degrades planning quality more than a smaller, fresh memory store.",
    "day-148": "Always trace LLM agent runs with LangSmith or OpenTelemetry — debugging non-deterministic multi-step failures is impossible without a full thought-action-observation trace.",
    "day-149": "Apply RAGAS evaluation metrics (faithfulness, answer relevancy, context precision) on a golden test set before every agent deployment — not just at launch.",
}

for day_id, replacement in REPLACEMENTS.items():
    # Find the section for this day and replace only the first occurrence of GENERIC within it
    day_start = html.find(f'id="{day_id}"')
    if day_start == -1:
        continue
    # Find next day section start or end of file
    next_day = html.find('class="day-section"', day_start + 10)
    section = html[day_start:next_day] if next_day != -1 else html[day_start:]
    
    if GENERIC in section:
        new_section = section.replace(GENERIC, replacement, 1)
        html = html[:day_start] + new_section + (html[next_day:] if next_day != -1 else "")
        changes.append(f"Fixed takeaway in {day_id}")

assert html.count("$$") == original_dd, f"Dollar-dollar count changed: {original_dd} → {html.count('$$')}"

with open("pages/weeks/week20.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"week20.html: {len(changes)} fixes applied, $$ count intact ({original_dd})")
for c in changes:
    print(f"  - {c}")
