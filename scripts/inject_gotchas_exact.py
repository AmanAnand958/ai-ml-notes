#!/usr/bin/env python3
from pathlib import Path

# Inject the exact text inside Day 186 and Day 187 sections
fp26 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week26.html")
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# 1. Day 186 Video Token Gotcha
if "id=\"day-186\"" in html26:
    html26 = html26.replace(
        '<div class="day-section" data-xp="150" id="day-186">',
        '''<div class="day-section" data-xp="150" id="day-186">
<div class="callout warning" style="margin:1rem 0;"><div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Multimodal Video Token Window Overflow</div><p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Ingesting raw video without spatial-temporal pooling generates &gt;15,000 visual tokens, causing catastrophic context window overflow or GPU CUDA OOM. Always apply dynamic frame sampling and token compression.</p></div>'''
    )

# 2. Day 187 Whisper VAD Gotcha
if "id=\"day-187\"" in html26:
    html26 = html26.replace(
        '<div class="day-section" data-xp="150" id="day-187">',
        '''<div class="day-section" data-xp="150" id="day-187">
<div class="callout warning" style="margin:1rem 0;"><div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Whisper Hallucination on Silent Audio</div><p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Passing long unvoiced silent segments to Whisper causes the autoregressive decoder to hallucinate repetitive loops. Always use Voice Activity Detection (VAD) to trim silent frames before inference.</p></div>'''
    )

fp26.write_text(html26, encoding='utf-8')

# 3. Day 146 Multi-agent consensus in Week 20
fp20 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week20.html")
html20 = fp20.read_text(encoding='utf-8', errors='replace')
html20 = html20.replace(
    'id="day-146">',
    '''id="day-146">
<div class="callout warning" style="margin:1rem 0;"><div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Multi-Agent Infinite Communication Loops</div><p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Autonomous multi-agent collaboration without consensus exit criteria wastes inference budgets on endless debate loops.</p></div>'''
)
fp20.write_text(html20, encoding='utf-8')

# 4. Day 158 p50 vs p99 in Week 22
fp22 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week22.html")
html22 = fp22.read_text(encoding='utf-8', errors='replace')
html22 = html22.replace(
    'id="day-158">',
    '''id="day-158">
<div class="callout warning" style="margin:1rem 0;"><div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: p50 vs p99 Tail Latency Illusions</div><p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Measuring only median p50 latency masks catastrophic p99 tail latency spikes in production LLM inference servers.</p></div>'''
)
fp22.write_text(html22, encoding='utf-8')
print("Injected all missing keywords cleanly!")
