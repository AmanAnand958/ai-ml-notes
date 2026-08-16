#!/usr/bin/env python3
"""
Fix all confirmed critical/high issues from full_checklist_audit.py for weeks 19-26.

Issues being fixed:
1. [CRITICAL 1.2] Only 6 day-sections detected — the regex parse misses the 7th because
   it's not closed before </main>. We need to verify actual count and fix unclosed divs.
2. [HIGH 2.10] Wrong day numbers in headers — the DAY numbers are CORRECT (136-191 is right!).
   The audit script had wrong expected ranges. This is a FALSE POSITIVE. No fix needed.
3. [HIGH 3.9] Week 21: missing device_map="auto" on large model loads.
4. [HIGH 4.3] Math ($...$) in quiz options but KaTeX not configured to render inside quiz-opt.
5. [MEDIUM 9.2] Missing <meta name="description"> on all weeks 19-26.
6. [MEDIUM 14.1] CDN scripts missing defer attribute.
7. [HIGH 7.2] Week 26 Day 191: completeDay uses 300 XP instead of 150.
8. Generic template flashcards in weeks 2-7 (not 19-26 — already clean).
"""

import re
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# Week metadata for meta descriptions
WEEK_META = {
    19: ("Advanced RAG System Design",
         "Master advanced RAG architectures: BM25, hybrid search, FAISS, Pinecone, reranking, and production retrieval pipelines in Python."),
    20: ("LLM Fine-Tuning & PEFT",
         "Deep dive into LoRA, QLoRA, and PEFT adapters. Fine-tune Llama 2 and Mistral 7B efficiently with quantization techniques."),
    21: ("LLM Agents & LangGraph",
         "Build autonomous AI agents with LangGraph, ReAct reasoning, multi-agent orchestration, and tool-calling patterns."),
    22: ("LLM Evaluation, Observability & Guardrails",
         "Evaluate LLMs with RAGAS and DeepEval, build monitoring dashboards, and implement content guardrails for production AI."),
    23: ("Cloud AI Services (GCP, AWS, Azure)",
         "Deploy ML models on Vertex AI, SageMaker, and Azure ML. Master serverless inference, AutoML, and cloud-native pipelines."),
    24: ("Production MLOps Pipelines",
         "Build end-to-end MLOps pipelines with MLflow, DVC, Airflow, Kubernetes, and CI/CD for machine learning systems."),
    25: ("Kubernetes & Infrastructure for AI",
         "Deploy AI workloads on Kubernetes with Helm, HPA autoscaling, GPU scheduling, Prometheus monitoring, and Grafana dashboards."),
    26: ("Multimodal AI & System Design Capstone",
         "Capstone week: multimodal AI (vision-language models), production system design interviews, and end-to-end portfolio projects."),
}

fixed_counts = {}

for wn in range(19, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    original = html
    fixes = []

    # ── FIX 1: Add meta description if missing ────────────────────
    if f'name="description"' not in html and wn in WEEK_META:
        topic, desc = WEEK_META[wn]
        meta_tag = f'  <meta name="description" content="{desc}"/>\n'
        # Insert after charset meta
        html = html.replace(
            '<meta charset="utf-8"/>',
            f'<meta charset="utf-8"/>\n{meta_tag.rstrip()}',
            1
        )
        fixes.append("Added meta description")

    # ── FIX 2: Add defer to CDN script tags ───────────────────────
    # Target mermaid and katex CDN scripts without defer
    def add_defer(m):
        tag = m.group(0)
        if 'defer' not in tag and 'async' not in tag:
            return tag.replace('<script ', '<script defer ')
        return tag
    
    new_html = re.sub(
        r'<script\s+src="https://cdn\.jsdelivr\.net/[^"]*(?:mermaid|katex)[^"]*"[^>]*>',
        add_defer, html
    )
    if new_html != html:
        html = new_html
        fixes.append("Added defer to CDN script tags")

    # ── FIX 3: Week 26 Day 191 — wrong XP (300 → 150) ────────────
    if wn == 26:
        new_html = re.sub(r'completeDay\(191,\s*300\)', 'completeDay(191, 150)', html)
        if new_html != html:
            html = new_html
            fixes.append("Fixed Day 191 XP: 300 → 150")

    # ── FIX 4: Week 21 — add device_map="auto" to 7B model loads ─
    if wn == 21:
        # Pattern: from_pretrained("...7B..." or "...7b...") without device_map
        def fix_device_map(m):
            call = m.group(0)
            if 'device_map' not in call:
                # Add device_map before closing paren
                call = call.rstrip(')')
                call += ',\n    device_map="auto")'
            return call
        
        # Match from_pretrained calls containing large model names
        new_html = re.sub(
            r'from_pretrained\(["\'](?:mistralai/Mistral-7B[^"\']*|meta-llama/Llama-2-7b[^"\']*)["\'][^)]*\)',
            fix_device_map, html, flags=re.DOTALL
        )
        if new_html != html:
            html = new_html
            fixes.append("Added device_map='auto' to large model loads")

    # ── FIX 5: KaTeX — ensure quiz-opt is in ignoredClasses ───────
    # Find the renderMathInElement config and add quiz-opt if missing
    katex_pattern = r'(renderMathInElement\s*\([^,]+,\s*\{[^}]*ignoredClasses\s*:\s*\[)([^\]]*?)(\])'
    
    def add_quiz_to_ignored(m):
        existing = m.group(2)
        if 'quiz-opt' not in existing:
            if existing.strip():
                return m.group(1) + existing + ', "quiz-opt", "quiz-feedback"' + m.group(3)
            else:
                return m.group(1) + '"quiz-opt", "quiz-feedback"' + m.group(3)
        return m.group(0)
    
    new_html = re.sub(katex_pattern, add_quiz_to_ignored, html, flags=re.DOTALL)
    if new_html != html:
        html = new_html
        fixes.append("Added quiz-opt to KaTeX ignoredClasses")
    else:
        # If no ignoredClasses exists, add it to the renderMathInElement call
        alt_pattern = r'(renderMathInElement\s*\([^,]+,\s*\{)'
        def add_ignored_block(m):
            return m.group(1) + '\n        ignoredClasses: ["quiz-opt", "quiz-feedback"],'
        
        # Only apply if ignoredClasses truly not present
        if 'ignoredClasses' not in html and 'renderMathInElement' in html:
            new_html = re.sub(alt_pattern, add_ignored_block, html, count=1)
            if new_html != html:
                html = new_html
                fixes.append("Injected ignoredClasses into KaTeX config")

    # ── Save if changed ───────────────────────────────────────────
    if html != original:
        fp.write_text(html, encoding='utf-8')
        fixed_counts[wn] = fixes
        print(f"✅ Week {wn}: {len(fixes)} fix(es) applied")
        for f in fixes:
            print(f"   • {f}")
    else:
        print(f"⚪ Week {wn}: No changes needed")

print(f"\n{'='*50}")
print(f"Fixed {len(fixed_counts)} week files")
print(f"Weeks modified: {list(fixed_counts.keys())}")

# ── Also check the 1.2 issue (day-section count = 6 not 7) ───────
print(f"\n{'='*50}")
print("INVESTIGATING [1.2] — Why only 6 day-sections detected?")
print("(Checking if this is a real bug or regex limitation)")
print(f"{'='*50}")

for wn in range(19, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8', errors='replace')
    
    # Count actual day-section opens
    opens = len(re.findall(r'<div\s+class="day-section"', html))
    
    # Try different regex to get last section
    sections_greedy = re.findall(r'<div\s+class="day-section".*?(?=<div\s+class="day-section"|</main|$)', html, re.DOTALL)
    sections_until_end = re.findall(r'<div\s+class="day-section"', html)
    
    print(f"  Week {wn}: {opens} day-section OPENS → {'✅ 7 correct' if opens == 7 else f'❌ {opens} WRONG'}")

print("\nNote: If all show 7 day-section opens, then [1.2] was a regex false positive")
print("(the script's regex couldn't capture the last section which runs to </main>)")
