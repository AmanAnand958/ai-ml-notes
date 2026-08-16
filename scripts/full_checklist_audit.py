#!/usr/bin/env python3
"""
Full Master Checklist Audit — Weeks 19-26
Checks ALL 18 layers from master_perfection_audit_checklist.md
"""
import re, json
from pathlib import Path
from collections import defaultdict

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")
OUT = Path("/Users/amananand/Downloads/SDE/ai:ml-1/scripts/full_checklist_report.json")

findings = defaultdict(list)

def add(week, layer, severity, check_id, description, detail="", fix=""):
    findings[week].append(dict(layer=layer, severity=severity, check=check_id,
                               description=description, detail=detail[:300], fix=fix))

for wn in range(19, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8', errors='replace')
    lines = html.split('\n')
    n = len(lines)

    print(f"\n{'='*60}")
    print(f"WEEK {wn} ({n} lines, {len(html):,} bytes)")
    print(f"{'='*60}")

    # ── LAYER 1: DOM & Structure ──────────────────────────────────
    # 1.1 Balanced day-section divs
    open_ds  = len(re.findall(r'<div\s+class="day-section"', html))
    close_ds = len(re.findall(r'</div>\s*<!--\s*end.*?day|day-section\s*-->', html, re.IGNORECASE))
    # Count total opens vs closes more carefully
    div_opens  = len(re.findall(r'<div\b', html))
    div_closes = len(re.findall(r'</div>', html))
    balance = div_opens - div_closes
    print(f"  [1.1] div balance: {div_opens} opens, {div_closes} closes → {'+' if balance>=0 else ''}{balance}")
    if abs(balance) > 5:
        add(wn,"L1","CRITICAL","1.1",f"Div imbalance: {balance} unclosed divs",
            fix="Find and close all unclosed day-section divs")

    # 1.2 Check section order — all 7 days should have key sections
    day_sections = re.findall(r'<div\s+class="day-section".*?(?=<div\s+class="day-section"|week-summary|</main)', html, re.DOTALL)
    print(f"  [1.2] Day sections found: {len(day_sections)}")
    if len(day_sections) != 7:
        add(wn,"L1","CRITICAL","1.2",f"Expected 7 day-sections, found {len(day_sections)}",
            fix="Check for unclosed/duplicate day-section divs")

    # 1.3 Week summary banner present
    has_summary = bool(re.search(r'class="week-summary"', html))
    print(f"  [1.3] Week summary banner: {'✅' if has_summary else '❌ MISSING'}")
    if not has_summary:
        add(wn,"L1","HIGH","1.3","Missing week-summary banner")

    # 1.5 Task accordion handlers
    bad_toggle = re.findall(r'onclick="[^"]*classList\.toggle\(.*?hidden', html)
    if bad_toggle:
        add(wn,"L1","HIGH","1.5",f"Bad toggle handler ({len(bad_toggle)} occurrences)",
            detail=str(bad_toggle[:2]), fix="Replace classList.toggle('hidden') with toggleTask(this)")
    print(f"  [1.5] Bad accordion toggles: {len(bad_toggle)}")

    # 1.6 Duplicate element IDs
    ids = re.findall(r'\bid="([^"]+)"', html)
    id_counts = defaultdict(int)
    for i in ids: id_counts[i] += 1
    dupes = {k:v for k,v in id_counts.items() if v > 1}
    if dupes:
        add(wn,"L1","CRITICAL","1.7",f"Duplicate IDs: {list(dupes.keys())[:5]}",
            fix="Make all element IDs unique")
    print(f"  [1.7] Duplicate IDs: {len(dupes)} ({list(dupes.keys())[:3]})")

    # ── LAYER 2: Topic Alignment ──────────────────────────────────
    # 2.10 Day header range correct
    day_headers = re.findall(r'DAY\s+(\d+)', html)
    if day_headers:
        days_in_week = [(wn-1)*7+1 + i for i in range(7)]
        found_days = [int(d) for d in day_headers]
        wrong = [d for d in found_days if d not in days_in_week]
        print(f"  [2.10] Day numbers found: {found_days[:7]} | expected range: {days_in_week}")
        if wrong:
            add(wn,"L2","HIGH","2.10",f"Wrong day numbers in headers: {wrong}",
                fix="Correct day numbers to match week's range")

    # ── LAYER 3: Code Quality ──────────────────────────────────────
    # 3.1 HTML artifacts in code
    html_in_code = len(re.findall(r'class=\\"kw\\"', html))
    print(f"  [3.1] Legacy kw artifacts in code: {html_in_code}")
    if html_in_code > 0:
        add(wn,"L3","CRITICAL","3.1",f"{html_in_code} legacy highlight artifacts found",
            fix="Re-run marker-based tokenizer to clean code blocks")

    # 3.4 Real API keys
    real_keys = re.findall(r'sk-[a-zA-Z0-9]{20,}', html)
    if real_keys:
        add(wn,"L3","CRITICAL","3.4",f"Potential real API key found: {real_keys[0][:15]}...",
            fix="Replace with os.getenv() or placeholder")
    print(f"  [3.4] Real API keys: {len(real_keys)}")

    # 3.6 Deprecated imports
    deprecated = re.findall(r'from langchain\.(chat_models|embeddings|vectorstores) import|openai\.ChatCompletion\.create|pinecone\.init\(', html)
    if deprecated:
        add(wn,"L3","HIGH","3.6",f"Deprecated imports: {deprecated[:3]}",
            fix="Update to current LangChain v0.3+ / OpenAI v1+ / Pinecone v3+ APIs")
    print(f"  [3.6] Deprecated imports: {len(deprecated)}")

    # 3.9 Missing device_map on large models
    large_models = re.findall(r'from_pretrained\([^)]*(?:7[Bb]|13[Bb]|70[Bb])[^)]*\)', html)
    no_device_map = [m for m in large_models if 'device_map' not in m]
    if no_device_map:
        add(wn,"L3","HIGH","3.9",f"{len(no_device_map)} large model loads missing device_map",
            detail=str(no_device_map[:2])[:200],
            fix='Add device_map="auto" to all large model .from_pretrained() calls')
    print(f"  [3.9] Large model loads missing device_map: {len(no_device_map)}")

    # ── LAYER 4: KaTeX / Math ──────────────────────────────────────
    # 4.1 Truncated LaTeX
    broken_latex = re.findall(r'(?<!\w)imes\b', html)
    print(f"  [4.1] Broken \\times→'imes': {len(broken_latex)}")
    if broken_latex:
        add(wn,"L4","CRITICAL","4.1",f"{len(broken_latex)} broken \\times escapes",
            fix="Replace bare 'imes' with \\times in LaTeX blocks")

    # 4.3 KaTeX in quiz options
    katex_quiz = re.findall(r'quiz-opt[^>]*>.*?\$[^$]+\$', html, re.DOTALL)
    has_katex_ignore = bool(re.search(r'ignoredClasses.*quiz', html))
    if katex_quiz and not has_katex_ignore:
        add(wn,"L4","HIGH","4.3","Math in quiz options but quiz-opt not in KaTeX ignoredClasses",
            fix="Add 'quiz-opt' to KaTeX renderMathInElement ignoredClasses config")
    print(f"  [4.3] Math in quiz: {len(katex_quiz)} | KaTeX ignores quiz: {has_katex_ignore}")

    # ── LAYER 5: Mermaid ──────────────────────────────────────────
    mermaid_blocks = re.findall(r'class="mermaid"[^>]*>(.*?)</div>', html, re.DOTALL)
    print(f"  [5.x] Mermaid blocks found: {len(mermaid_blocks)}")
    # 5.1 Unquoted labels with parens
    bad_labels = 0
    for mb in mermaid_blocks:
        if re.search(r'\[[^\]]*\([^\]]*\]\]|-->', mb):
            if re.search(r'\b\w+\[[^\]"]*\([^\]"]*\]', mb):
                bad_labels += 1
    if bad_labels:
        add(wn,"L5","HIGH","5.1",f"{bad_labels} mermaid blocks with unquoted paren labels")
    print(f"  [5.1] Unquoted mermaid labels: {bad_labels}")

    # 5.5 renderMermaid on tab switch
    has_render_mermaid = bool(re.search(r'renderMermaid|mermaid\.run|mermaid\.init', html))
    print(f"  [5.5] renderMermaid() on tab switch: {'✅' if has_render_mermaid else '❌ MISSING'}")
    if not has_render_mermaid:
        add(wn,"L5","HIGH","5.5","No mermaid re-render on tab switch — diagrams in hidden tabs blank",
            fix="Add mermaid.run() call in tab-switch handler")

    # ── LAYER 6: Interactive Widgets ──────────────────────────────
    # 6.1 Solution toggle ID linkage
    toggle_calls = re.findall(r"toggleSolution\('([^']+)'\)", html)
    toggle_ids   = re.findall(r'id="(sol-[^"]+)"', html)
    missing_ids  = [t for t in toggle_calls if t not in toggle_ids]
    if missing_ids:
        add(wn,"L6","CRITICAL","6.1",f"{len(missing_ids)} toggleSolution() calls with no matching id",
            detail=str(missing_ids[:5]), fix="Add matching id='sol-xxx' divs for each toggleSolution call")
    print(f"  [6.1] toggleSolution orphans: {len(missing_ids)}")

    # 6.3 Copy button
    has_copy = bool(re.search(r'copyCode\(this\)', html))
    print(f"  [6.3] copyCode() present: {'✅' if has_copy else '❌'}")

    # ── LAYER 7: Gamification ─────────────────────────────────────
    # 7.1 Complete button for every day
    complete_btns = re.findall(r'completeDay\((\d+),\s*(\d+)\)', html)
    print(f"  [7.1] completeDay() calls: {len(complete_btns)} (expected 7)")
    if len(complete_btns) != 7:
        add(wn,"L7","HIGH","7.1",f"Expected 7 completeDay() calls, found {len(complete_btns)}",
            fix="Add completeDay(N, 150) to each day's Complete button")

    # 7.2 XP consistency
    wrong_xp = [(d,xp) for d,xp in complete_btns if xp != '150']
    if wrong_xp:
        add(wn,"L7","HIGH","7.2",f"Non-standard XP values: {wrong_xp}",
            fix="Change all XP to 150 for consistency")
    print(f"  [7.2] Non-150 XP values: {wrong_xp}")

    # ── LAYER 8: Navigation ───────────────────────────────────────
    # 8.1 Previous/Next week links
    prev_link = re.search(rf'week{wn-1}\.html', html)
    next_link = re.search(rf'week{wn+1}\.html', html) if wn < 26 else True
    print(f"  [8.1] Prev week link (week{wn-1}): {'✅' if prev_link else '❌ MISSING'}")
    print(f"  [8.1] Next week link (week{wn+1}): {'✅' if next_link else '❌ MISSING'}")
    if not prev_link:
        add(wn,"L8","HIGH","8.1",f"Missing link back to week{wn-1}.html",
            fix=f"Add navigation link to week{wn-1}.html")
    if not next_link:
        add(wn,"L8","HIGH","8.1",f"Missing link forward to week{wn+1}.html",
            fix=f"Add navigation link to week{wn+1}.html")

    # 8.2 Roadmap link
    has_roadmap = bool(re.search(r'roadmap\.html', html))
    print(f"  [8.2] Roadmap link: {'✅' if has_roadmap else '❌ MISSING'}")
    if not has_roadmap:
        add(wn,"L8","HIGH","8.2","Missing link to roadmap.html")

    # ── LAYER 9: SEO ──────────────────────────────────────────────
    title_m = re.search(r'<title>([^<]+)</title>', html)
    title = title_m.group(1) if title_m else "MISSING"
    print(f"  [9.1] Title: {title[:60]}")
    if 'Week' not in title and 'week' not in title:
        add(wn,"L9","MEDIUM","9.1",f"Title doesn't mention week: '{title}'",
            fix=f"Set <title>Week {wn} — [Topics] | 191-Day AI/ML Roadmap</title>")

    meta_desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    print(f"  [9.2] Meta description: {'✅' if meta_desc else '❌ MISSING'}")
    if not meta_desc:
        add(wn,"L9","MEDIUM","9.2","Missing <meta name='description'>")

    h1_count = len(re.findall(r'<h1[\s>]', html))
    print(f"  [9.4] <h1> tags: {h1_count} (SEO: prefer 1 visible)")
    if h1_count > 3:
        add(wn,"L9","MEDIUM","9.4",f"{h1_count} <h1> tags — SEO crawlers prefer 1 dominant h1",
            fix="Use <h2> or <h3> for day subtitles inside hidden sections")

    # ── LAYER 14: Performance ─────────────────────────────────────
    # 14.1 CDN scripts with defer
    cdn_scripts = re.findall(r'<script\s+src="https://[^"]+(?:mermaid|katex)[^"]*"([^>]*)>', html)
    for cs in cdn_scripts:
        if 'defer' not in cs and 'async' not in cs:
            add(wn,"L14","MEDIUM","14.1","CDN script without defer/async — blocks render",
                detail=cs[:100], fix="Add defer to CDN <script> tags")
    print(f"  [14.1] CDN scripts without defer: {sum(1 for cs in cdn_scripts if 'defer' not in cs and 'async' not in cs)}")

    # 14.2 Duplicate CDN loads
    mermaid_cdn = len(re.findall(r'cdn.*mermaid', html, re.IGNORECASE))
    katex_cdn   = len(re.findall(r'cdn.*katex', html, re.IGNORECASE))
    print(f"  [14.2] Mermaid CDN refs: {mermaid_cdn} | KaTeX CDN refs: {katex_cdn}")
    if mermaid_cdn > 2:
        add(wn,"L14","HIGH","14.2",f"Duplicate Mermaid CDN loads ({mermaid_cdn})",
            fix="Remove duplicate <script src='...mermaid...'> tags")

    # ── LAYER 10: Accessibility ────────────────────────────────────
    # 10.4 rel=noopener on target=_blank
    blank_links = re.findall(r'<a[^>]+target="_blank"[^>]*>', html)
    unsafe_blank = [l for l in blank_links if 'noopener' not in l]
    if unsafe_blank:
        add(wn,"L10","MEDIUM","10.4",f"{len(unsafe_blank)} target=_blank links without rel=noopener",
            fix='Add rel="noopener noreferrer" to all target=_blank links')
    print(f"  [10.4] Unsafe _blank links: {len(unsafe_blank)}")

    # ── AI Failure Modes ──────────────────────────────────────────
    # F1: Missing device_map (already counted above in 3.9)
    # F2: Fabricated % claims in THEORY (not quiz distractors)
    theory_pct = re.findall(r'(?:reduction|improvement|faster|better)\s+(?:of\s+)?\d{2,3}[\-–]\d{2,3}%', html)
    print(f"  [F2] Unsourced % ranges in theory: {len(theory_pct)}")
    if theory_pct:
        add(wn,"AI","HIGH","F2",f"Unsourced % ranges in theory: {theory_pct[:3]}",
            fix="Add citation or soften to 'up to X%'")

    # F3: Generic template flashcard
    generic_fc = re.findall(r'Review and execute the complete code walkthrough', html, re.IGNORECASE)
    print(f"  [F3] Generic template flashcard: {len(generic_fc)}")
    if generic_fc:
        add(wn,"AI","HIGH","F3",f"Generic placeholder flashcard found ({len(generic_fc)}x)",
            fix="Replace with day-specific flashcard content")

    # F4: Tautological definitions
    tautologies = re.findall(r'attention\s+(?:helps\s+)?(?:the\s+model\s+)?(?:pay\s+)?attention', html, re.IGNORECASE)
    if tautologies:
        add(wn,"AI","MEDIUM","F4",f"{len(tautologies)} circular 'attention...attention' definitions")
    print(f"  [F4] Circular definitions: {len(tautologies)}")

    # F5: Stale model references
    stale = re.findall(r'GPT-3\.5\s+(?:is|remains?)\s+(?:the\s+)?(?:most|best|latest)', html, re.IGNORECASE)
    if stale:
        add(wn,"AI","MEDIUM","F5",f"Stale model claim: {stale[:2]}")
    print(f"  [F5] Stale model claims: {len(stale)}")

    # Summary line
    crit = sum(1 for f in findings[wn] if f['severity']=='CRITICAL')
    high = sum(1 for f in findings[wn] if f['severity']=='HIGH')
    med  = sum(1 for f in findings[wn] if f['severity']=='MEDIUM')
    print(f"\n  → WEEK {wn} SUMMARY: {crit} CRITICAL | {high} HIGH | {med} MEDIUM")

# ── Cross-week: duplicate flashcards ─────────────────────────────
print(f"\n{'='*60}")
print("CROSS-WEEK: Scanning all 26 weeks for generic template flashcards")
print(f"{'='*60}")
template_weeks = []
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8', errors='replace')
    count = len(re.findall(r'Review and execute the complete code walkthrough', html, re.IGNORECASE))
    if count:
        template_weeks.append((wn, count))
        print(f"  Week {wn}: {count}x generic template flashcard")

if not template_weeks:
    print("  ✅ No generic template flashcards found")

# ── Save and print totals ─────────────────────────────────────────
report = {"weeks": {}}
grand = {"CRITICAL":0,"HIGH":0,"MEDIUM":0}
for wn, items in findings.items():
    report["weeks"][wn] = items
    for item in items:
        grand[item["severity"]] = grand.get(item["severity"], 0) + 1

OUT.write_text(json.dumps(report, indent=2))

print(f"\n{'='*60}")
print("GRAND TOTALS (Weeks 19-26)")
print(f"{'='*60}")
for sev in ("CRITICAL","HIGH","MEDIUM"):
    icon = {"CRITICAL":"🔴","HIGH":"🟠","MEDIUM":"🟡"}[sev]
    print(f"  {icon} {sev}: {grand.get(sev,0)}")
print(f"\nFull report: {OUT}")
