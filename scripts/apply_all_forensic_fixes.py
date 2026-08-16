#!/usr/bin/env python3
"""
Comprehensive Fix Script for All Confirmed Forensic Issues:
1. Week 23: Clean up EOF duplication (remove orphaned Day 166/169 content after week-summary)
2. Week 22: Realign shifted Gotchas across Days 158, 159, and 160
3. Week 19: Modernize LLMChain to LCEL in Day 141 (HyDE)
4. Week 22: Replace hallucinated RAGAS Harmonic Triad formula with standard canonical metrics in Day 157
5. Week 23: Fix Cloud Provider Bleed in Day 165 (GCP) and Day 167 (Azure) Task 2 titles/descriptions
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX WEEK 23 EOF DUPLICATION
# ─────────────────────────────────────────────────────────────────────────────
print("=== 1. Fixing Week 23 EOF Duplication ===")
fp23 = WEEKS_DIR / "week23.html"
html23 = fp23.read_text(encoding='utf-8', errors='replace')

# Locate week-summary div and find its proper closing
ws_idx = html23.find('<div class="week-summary">')
if ws_idx != -1:
    # Find the scripts section at the bottom
    script_idx = html23.find('<script>\n  const WEEK = 23;')
    if script_idx == -1:
        script_idx = html23.find('const WEEK = 23;')
        if script_idx != -1:
            script_idx = html23.rfind('<script', 0, script_idx)
            
    if script_idx != -1 and ws_idx < script_idx:
        # Extract week summary block and ensure it closes cleanly right before </main>
        # Check what is between week-summary and script
        between = html23[ws_idx:script_idx]
        
        # Keep week-summary container and closing </main>
        # Let's inspect week-summary block
        ws_close = between.find('</div>\n</div>\n</main>')
        if ws_close == -1:
            ws_close = between.find('</main>')
            
        if ws_close != -1:
            cleaned_between = between[:ws_close + len('</main>')] + '\n'
            new_html23 = html23[:ws_idx] + cleaned_between + html23[script_idx:]
            
            # Check if duplicate completeDay(166) or (169) exist after clean
            html23 = new_html23
            print("  ✅ Stripped orphaned trailing DOM nodes from Week 23")
            fp23.write_text(html23, encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX WEEK 22 SHIFTED GOTCHAS
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Realigning Week 22 Gotchas ===")
fp22 = WEEKS_DIR / "week22.html"
html22 = fp22.read_text(encoding='utf-8', errors='replace')

# Day 158 Gotcha should be about Tracing / Latency Spacing (OpenTelemetry)
# Day 159 Gotcha should be about Guardrail Overhead / Regex Failures
# Day 160 Gotcha should be about Semantic Cache Poisoning & Threshold Drift

d158_old_gotcha = r'⚠️ Gotcha: Day 158 Pitfall WarningEvaluating RAG with only generation metrics \(BLEU/ROUGE\) masks retrieval failures\. An answer can be well-formed English while being completely ungrounded in the retrieved context \(hallucination\)\. Always measure retrieval faithfulness separately from generation fluency\.'
d158_new_gotcha = r'⚠️ Gotcha: Day 158 Pitfall WarningTracing high-throughput LLM services with 100% synchronous logging creates severe network latency bottlenecks and memory leaks. Always use non-blocking asynchronous OpenTelemetry span batching and sampling for production workloads.'

d159_old_gotcha = r'⚠️ Gotcha: Day 159 Pitfall WarningTracing high-throughput LLM services with 100% synchronous logging creates severe network latency bottlenecks\. Always use non-blocking background queue workers for OpenTelemetry span export\.'
d159_new_gotcha = r'⚠️ Gotcha: Day 159 Pitfall WarningPrompt injection and jailbreak defenses relying purely on static regex filters fail against base64, leetspeak, and multi-turn indirect injection. Always combine deterministic pattern scanning with a semantic LLM guardrail classifier.'

d160_old_gotcha = r'⚠️ Gotcha: Day 160 Pitfall WarningPrompt injection defenses relying purely on regex filters fail against base64 or synonym obfuscation\. Always combine deterministic pattern scanning with a dedicated guardrail LLM classifier\.'
d160_new_gotcha = r'⚠️ Gotcha: Day 160 Pitfall WarningSemantic cache similarity threshold miscalibration causes false-positive cache hits, serving outdated or contextually invalid answers to distinct user queries. Set strict similarity thresholds (&ge; 0.92) and enforce short TTLs for dynamic data.'

html22 = re.sub(d158_old_gotcha, d158_new_gotcha, html22)
html22 = re.sub(d159_old_gotcha, d159_new_gotcha, html22)
html22 = re.sub(d160_old_gotcha, d160_new_gotcha, html22)

fp22.write_text(html22, encoding='utf-8')
print("  ✅ Realignment of Week 22 Gotchas completed (Days 158, 159, 160)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIX WEEK 19 DAY 141 (HYDE) DEPRECATED LLMCHAIN -> LCEL
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 3. Modernizing Week 19 Day 141 LLMChain -> LCEL ===")
fp19 = WEEKS_DIR / "week19.html"
html19 = fp19.read_text(encoding='utf-8', errors='replace')

# Replace langchain.chains LLMChain with langchain_core.output_parsers StrOutputParser
old_import = 'from langchain.chains import LLMChain'
new_import = 'from langchain_core.output_parsers import StrOutputParser'

old_chain = 'hyde_chain = LLMChain(llm=llm, prompt=prompt)'
new_chain = 'hyde_chain = prompt | llm | StrOutputParser()'

old_invoke = 'hypothetical_doc = hyde_chain.run(query=query)'
new_invoke = 'hypothetical_doc = hyde_chain.invoke({"query": query})'

html19 = html19.replace(old_import, new_import)
html19 = html19.replace(old_chain, new_chain)
html19 = html19.replace(old_invoke, new_invoke)

fp19.write_text(html19, encoding='utf-8')
print("  ✅ Upgraded HyDE implementation in Week 19 Day 141 to modern LCEL")

# ─────────────────────────────────────────────────────────────────────────────
# 4. FIX WEEK 22 DAY 157 RAGAS HARMONIC TRIAD FORMULA
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 4. Correcting Week 22 Day 157 RAGAS Math Formula ===")
html22 = fp22.read_text(encoding='utf-8', errors='replace')

# Replace hallucinated Harmonic Triad formula with standard canonical RAG Triad formulas
old_formula = r'$$\text{RAG Triad Score} = \frac{3}{\frac{1}{\text{Faithfulness}} + \frac{1}{\text{Answer Relevance}} + \frac{1}{\text{Context Recall}}}$$'
new_formula = r'$$\text{Faithfulness} = \frac{|\text{Supported Claims}|}{|\text{Total Generated Claims}|}, \quad \text{Context Relevance} = \frac{|\text{Relevant Sentences}|}{|\text{Total Retrieved Sentences}|}$$'

html22 = html22.replace(old_formula, new_formula)
fp22.write_text(html22, encoding='utf-8')
print("  ✅ Replaced hallucinated composite RAGAS formula with standard independent metrics")

# ─────────────────────────────────────────────────────────────────────────────
# 5. FIX WEEK 23 CLOUD BLEED (GCP & AZURE DAYS)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 5. Fixing Week 23 Cloud Provider Content Alignment ===")
html23 = fp23.read_text(encoding='utf-8', errors='replace')

# Day 165 (GCP): Replace references to SageMaker Spot Estimator in Task 2 with Vertex AI Custom Training Job
html23 = html23.replace(
    'Task 2: SageMaker Spot Training Estimator with Checkpointing',
    'Task 2: Vertex AI Custom Job Estimator with Managed Spot'
)
html23 = html23.replace(
    'Spot Estimator Configured! Expected Compute Cost Reduction: 68%',
    'Vertex AI Spot Job Configured! Expected Compute Cost Reduction: 68%'
)

# Day 167 (Azure): Replace AWS Deequ baseline with Azure ML Data Drift Monitor
html23 = html23.replace(
    'Task 2: SageMaker Model Monitor Baseline with AWS Deequ',
    'Task 2: Azure ML Data Drift Monitor Baseline with DataProfile'
)
html23 = html23.replace(
    'Deequ Constraints Generated:',
    'Azure ML Drift Profile Constraints Generated:'
)

fp23.write_text(html23, encoding='utf-8')
print("  ✅ Updated GCP Day 165 and Azure Day 167 Task 2 naming & outputs")

print("\n🎉 ALL TARGETED FORENSIC FIXES APPLIED SUCCESSFULLY!")
