#!/usr/bin/env python3
"""
scripts/inject_svg_diagrams_weeks18_to_26.py
Generates and injects hand-crafted, high-contrast, beautiful inline SVG diagrams
and rich architectural flowcharts into theory_html across Weeks 18 to 26.
"""

import os, yaml
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

# ═════════════════════════════════════════════════════════════════════
# SVG DIAGRAM DEFINITIONS
# ═════════════════════════════════════════════════════════════════════
SVG_DIAGRAMS = {}

# ── WEEK 18 DAY 125: Kubernetes Pod & GPU Resource Allocation ──
SVG_DIAGRAMS[125] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="Kubernetes GPU Workload Orchestration" height="260" viewBox="0 0 720 260" width="720" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <defs>
    <linearGradient id="k8s-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="gpu-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
    <linearGradient id="pod-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
  </defs>
  
  <!-- Outer Node Frame -->
  <rect x="10" y="10" width="700" height="240" rx="12" fill="url(#k8s-grad)" stroke="#334155" stroke-width="2"/>
  <text x="30" y="38" fill="#94a3b8" font-size="13" font-weight="bold">Kubernetes Worker Node (8x NVIDIA H100 SXM5 — 640GB VRAM)</text>
  
  <!-- Kubelet Box -->
  <rect x="30" y="55" width="130" height="70" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
  <text x="50" y="85" fill="#f8fafc" font-size="13" font-weight="bold">kubelet</text>
  <text x="42" y="105" fill="#94a3b8" font-size="10">Node Agent</text>
  
  <!-- NVIDIA GPU Plugin -->
  <rect x="30" y="145" width="130" height="85" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
  <text x="42" y="175" fill="#10b981" font-size="12" font-weight="bold">NVIDIA Plugin</text>
  <text x="40" y="195" fill="#cbd5e1" font-size="10">Device Discovery</text>
  <text x="40" y="210" fill="#94a3b8" font-size="9">nvidia.com/gpu: 8</text>

  <!-- Connection line to pods -->
  <path d="M 160 90 L 210 90" stroke="#64748b" stroke-width="2" stroke-dasharray="4"/>
  <path d="M 160 185 L 210 185" stroke="#10b981" stroke-width="2"/>

  <!-- Pod 1 -->
  <rect x="210" y="55" width="220" height="175" rx="8" fill="#0f172a" stroke="#3b82f6" stroke-width="2"/>
  <text x="225" y="80" fill="#60a5fa" font-size="12" font-weight="bold">Pod: vllm-serving-0</text>
  
  <rect x="225" y="95" width="190" height="50" rx="6" fill="#1e293b" stroke="#475569"/>
  <text x="235" y="115" fill="#f1f5f9" font-size="11">vLLM Inference Core</text>
  <text x="235" y="132" fill="#38bdf8" font-size="9.5">Limits: nvidia.com/gpu: 2</text>

  <rect x="225" y="155" width="190" height="60" rx="6" fill="#1e293b" stroke="#eab308"/>
  <text x="235" y="175" fill="#facc15" font-size="11">/dev/shm (emptyDir)</text>
  <text x="235" y="192" fill="#cbd5e1" font-size="9.5">Shared Memory: 16Gi</text>
  <text x="235" y="206" fill="#94a3b8" font-size="8.5">Prevents PyTorch SIGBUS</text>

  <!-- Pod 2 -->
  <rect x="460" y="55" width="230" height="175" rx="8" fill="#0f172a" stroke="#3b82f6" stroke-width="2"/>
  <text x="475" y="80" fill="#60a5fa" font-size="12" font-weight="bold">Pod: vllm-serving-1</text>
  
  <rect x="475" y="95" width="200" height="50" rx="6" fill="#1e293b" stroke="#475569"/>
  <text x="485" y="115" fill="#f1f5f9" font-size="11">vLLM Inference Core</text>
  <text x="485" y="132" fill="#38bdf8" font-size="9.5">Limits: nvidia.com/gpu: 2</text>

  <rect x="475" y="155" width="200" height="60" rx="6" fill="#1e293b" stroke="#eab308"/>
  <text x="485" y="175" fill="#facc15" font-size="11">/dev/shm (emptyDir)</text>
  <text x="485" y="192" fill="#cbd5e1" font-size="9.5">Shared Memory: 16Gi</text>
  <text x="485" y="206" fill="#94a3b8" font-size="8.5">Prevents PyTorch SIGBUS</text>
</svg>
<div class="diagram-cap">Figure 125.2: Production Kubernetes Pod Architecture with Dedicated GPU Allocation and /dev/shm Shared Memory Mounts.</div>
</div>
"""

# ── WEEK 19 DAY 137: Bi-Encoder vs Cross-Encoder Self-Attention ──
SVG_DIAGRAMS[137] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="Bi-Encoder vs Cross-Encoder Architecture Comparison" height="280" viewBox="0 0 740 280" width="740" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <defs>
    <linearGradient id="bi-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1e2e"/>
      <stop offset="100%" stop-color="#11111b"/>
    </linearGradient>
  </defs>

  <!-- Left: Bi-Encoder -->
  <rect x="10" y="10" width="345" height="260" rx="10" fill="url(#bi-grad)" stroke="#45475a" stroke-width="1.5"/>
  <text x="25" y="35" fill="#89b4fa" font-size="13" font-weight="bold">Stage 1: Bi-Encoder (Dense Vectors)</text>
  
  <rect x="30" y="55" width="135" height="40" rx="6" fill="#313244" stroke="#89b4fa"/>
  <text x="45" y="80" fill="#cdd6f4" font-size="11">Query q</text>
  <rect x="190" y="55" width="145" height="40" rx="6" fill="#313244" stroke="#a6e3a1"/>
  <text x="205" y="80" fill="#cdd6f4" font-size="11">Document d</text>

  <text x="80" y="120" fill="#f38ba8" font-size="18">↓</text>
  <text x="245" y="120" fill="#f38ba8" font-size="18">↓</text>

  <rect x="30" y="135" width="135" height="45" rx="6" fill="#181825" stroke="#cba6f7"/>
  <text x="45" y="155" fill="#cba6f7" font-size="10">BERT Encoder f_θ</text>
  <text x="55" y="170" fill="#9399b2" font-size="9">vec(u) in R^1024</text>

  <rect x="190" y="135" width="145" height="45" rx="6" fill="#181825" stroke="#cba6f7"/>
  <text x="205" y="155" fill="#cba6f7" font-size="10">BERT Encoder f_θ</text>
  <text x="215" y="170" fill="#9399b2" font-size="9">vec(v) in R^1024</text>

  <path d="M 97 180 L 172 215" stroke="#fab387" stroke-width="1.5"/>
  <path d="M 262 180 L 172 215" stroke="#fab387" stroke-width="1.5"/>

  <rect x="105" y="215" width="135" height="35" rx="6" fill="#fab387"/>
  <text x="115" y="237" fill="#11111b" font-size="11" font-weight="bold">Dot Product: u · v</text>
  <text x="30" y="258" fill="#a6adc8" font-size="9">Fast ANN (HNSW) | Zero cross-attention</text>

  <!-- Right: Cross-Encoder -->
  <rect x="375" y="10" width="355" height="260" rx="10" fill="url(#bi-grad)" stroke="#f38ba8" stroke-width="1.5"/>
  <text x="390" y="35" fill="#f38ba8" font-size="13" font-weight="bold">Stage 2: Cross-Encoder (Joint Attention)</text>

  <rect x="395" y="55" width="315" height="45" rx="6" fill="#313244" stroke="#f38ba8"/>
  <text x="410" y="82" fill="#cdd6f4" font-size="11">[CLS] + Query Tokens + [SEP] + Document Tokens</text>

  <text x="545" y="125" fill="#f38ba8" font-size="18">↓</text>

  <rect x="395" y="135" width="315" height="55" rx="6" fill="#181825" stroke="#f9e2af" stroke-width="1.5"/>
  <text x="430" y="158" fill="#f9e2af" font-size="11" font-weight="bold">Full Multi-Layer Cross Self-Attention</text>
  <text x="415" y="178" fill="#9399b2" font-size="9.5">Every query token attends to every doc token (O(L^2))</text>

  <text x="545" y="208" fill="#f38ba8" font-size="18">↓</text>

  <rect x="445" y="215" width="215" height="35" rx="6" fill="#a6e3a1"/>
  <text x="460" y="237" fill="#11111b" font-size="11" font-weight="bold">Calibrated Relevance Score σ(W h_CLS)</text>
</svg>
<div class="diagram-cap">Figure 137.2: Architectural Comparison: Bi-Encoder Independent Projection vs Cross-Encoder Full Cross-Attention.</div>
</div>
"""

# ── WEEK 20 DAY 145: LangGraph Cyclic StateGraph ──
SVG_DIAGRAMS[145] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="LangGraph Cyclic StateGraph Architecture" height="240" viewBox="0 0 700 240" width="700" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <defs>
    <linearGradient id="lg-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
  </defs>

  <rect x="10" y="10" width="680" height="220" rx="12" fill="url(#lg-bg)" stroke="#6366f1" stroke-width="2"/>
  <text x="30" y="35" fill="#a5b4fc" font-size="13" font-weight="bold">LangGraph Stateful Cyclic Execution State Machine</text>

  <!-- Start Node -->
  <circle cx="50" cy="110" r="18" fill="#10b981"/>
  <text x="35" y="115" fill="#ffffff" font-size="10" font-weight="bold">START</text>

  <!-- Arrow to Planner -->
  <path d="M 68 110 L 110 110" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Planner Node -->
  <rect x="110" y="80" width="130" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="135" y="105" fill="#38bdf8" font-size="11" font-weight="bold">Planner Node</text>
  <text x="125" y="125" fill="#94a3b8" font-size="9.5">Generate Sub-goals</text>

  <!-- Arrow to Tool Node -->
  <path d="M 240 110 L 290 110" stroke="#94a3b8" stroke-width="2"/>

  <!-- Tool Node -->
  <rect x="290" y="80" width="130" height="60" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="315" y="105" fill="#f59e0b" font-size="11" font-weight="bold">Tool Node</text>
  <text x="305" y="125" fill="#94a3b8" font-size="9.5">Execute APIs/Sandbox</text>

  <!-- Arrow to Evaluator -->
  <path d="M 420 110 L 470 110" stroke="#94a3b8" stroke-width="2"/>

  <!-- Evaluator Node -->
  <rect x="470" y="80" width="130" height="60" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
  <text x="488" y="105" fill="#ec4899" font-size="11" font-weight="bold">Evaluator Node</text>
  <text x="482" y="125" fill="#94a3b8" font-size="9.5">Validate Criteria</text>

  <!-- Loop back edge (Cyclic Error Recovery) -->
  <path d="M 535 80 C 535 30, 175 30, 175 80" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="5"/>
  <text x="310" y="45" fill="#f87171" font-size="10" font-weight="bold">Retry Loop / Error Correction</text>

  <!-- Arrow to End -->
  <path d="M 600 110 L 640 110" stroke="#10b981" stroke-width="2"/>
  <circle cx="658" cy="110" r="18" fill="#10b981"/>
  <text x="648" y="115" fill="#ffffff" font-size="10" font-weight="bold">END</text>

  <!-- PostgreSQL Checkpointer Banner -->
  <rect x="180" y="175" width="340" height="35" rx="6" fill="#0284c7"/>
  <text x="200" y="197" fill="#ffffff" font-size="11" font-weight="bold">PostgreSQL Checkpointer (State Snapshot on Each Hop)</text>
</svg>
<div class="diagram-cap">Figure 145.2: LangGraph State Machine with Cyclic Error Recovery and State Snapshot Persistence.</div>
</div>
"""

# ── WEEK 21 DAY 150: PagedAttention Virtual Memory Block Mapping ──
SVG_DIAGRAMS[150] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="PagedAttention Virtual Block Table Mapping" height="260" viewBox="0 0 720 260" width="720" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <defs>
    <linearGradient id="paged-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09090b"/>
      <stop offset="100%" stop-color="#18181b"/>
    </linearGradient>
  </defs>

  <rect x="10" y="10" width="700" height="240" rx="10" fill="url(#paged-bg)" stroke="#27272a" stroke-width="2"/>
  <text x="25" y="35" fill="#22c55e" font-size="13" font-weight="bold">PagedAttention: Virtual Memory Block Mapping (Zero Fragmentation)</text>

  <!-- Logical Sequence Blocks -->
  <rect x="30" y="60" width="180" height="170" rx="8" fill="#18181b" stroke="#3f3f46"/>
  <text x="45" y="85" fill="#a1a1aa" font-size="11" font-weight="bold">Logical Sequence</text>
  
  <rect x="40" y="95" width="160" height="35" rx="4" fill="#27272a" stroke="#60a5fa"/>
  <text x="50" y="117" fill="#60a5fa" font-size="10.5">Block 0 (Tokens 0-15)</text>

  <rect x="40" y="135" width="160" height="35" rx="4" fill="#27272a" stroke="#f472b6"/>
  <text x="50" y="157" fill="#f472b6" font-size="10.5">Block 1 (Tokens 16-31)</text>

  <rect x="40" y="175" width="160" height="35" rx="4" fill="#27272a" stroke="#facc15"/>
  <text x="50" y="197" fill="#facc15" font-size="10.5">Block 2 (Tokens 32-47)</text>

  <!-- Page Table (Mapping Directory) -->
  <rect x="250" y="60" width="180" height="170" rx="8" fill="#18181b" stroke="#22c55e" stroke-width="1.5"/>
  <text x="270" y="85" fill="#4ade80" font-size="11" font-weight="bold">Block Table (Directory)</text>
  <text x="265" y="115" fill="#f8fafc" font-size="10.5">Logical 0 → Physical 7</text>
  <text x="265" y="155" fill="#f8fafc" font-size="10.5">Logical 1 → Physical 23</text>
  <text x="265" y="195" fill="#f8fafc" font-size="10.5">Logical 2 → Physical 12</text>

  <!-- Arrows from logical to table -->
  <path d="M 200 112 L 250 112" stroke="#60a5fa" stroke-width="2"/>
  <path d="M 200 152 L 250 152" stroke="#f472b6" stroke-width="2"/>
  <path d="M 200 192 L 250 192" stroke="#facc15" stroke-width="2"/>

  <!-- Physical Non-Contiguous GPU Memory -->
  <rect x="470" y="60" width="220" height="170" rx="8" fill="#18181b" stroke="#3f3f46"/>
  <text x="490" y="85" fill="#a1a1aa" font-size="11" font-weight="bold">Physical GPU VRAM Pages</text>

  <rect x="480" y="95" width="200" height="30" rx="4" fill="#1e293b" stroke="#60a5fa"/>
  <text x="490" y="115" fill="#60a5fa" font-size="10">Phys Block 7: Tokens 0-15</text>

  <rect x="480" y="130" width="200" height="30" rx="4" fill="#1e293b" stroke="#3f3f46"/>
  <text x="490" y="150" fill="#71717a" font-size="9.5">Phys Block 8..22: Other Requests</text>

  <rect x="480" y="165" width="200" height="30" rx="4" fill="#1e293b" stroke="#f472b6"/>
  <text x="490" y="185" fill="#f472b6" font-size="10">Phys Block 23: Tokens 16-31</text>
</svg>
<div class="diagram-cap">Figure 150.2: PagedAttention Virtual Memory Block Mapping: Physical non-contiguous memory allocation eliminating GPU KV cache fragmentation.</div>
</div>
"""

# ── WEEK 21 DAY 153: LoRA & QLoRA Low-Rank Decomposition ──
SVG_DIAGRAMS[153] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="LoRA Low-Rank Decomposition Architecture" height="250" viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <rect x="10" y="10" width="660" height="230" rx="10" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <text x="25" y="35" fill="#38bdf8" font-size="13" font-weight="bold">LoRA: Low-Rank Adapter Decomposition (W = W_0 + (α/r)·B·A)</text>

  <!-- Input Vector x -->
  <rect x="30" y="90" width="70" height="55" rx="6" fill="#1e293b" stroke="#94a3b8"/>
  <text x="45" y="122" fill="#f8fafc" font-size="12" font-weight="bold">x ∈ R^d</text>

  <!-- Branch to Frozen Base Weights W_0 -->
  <path d="M 100 117 L 160 80" stroke="#94a3b8" stroke-width="2"/>
  <rect x="160" y="50" width="220" height="60" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
  <text x="175" y="75" fill="#94a3b8" font-size="11" font-weight="bold">Frozen Base Weights W_0</text>
  <text x="195" y="95" fill="#ef4444" font-size="10">d × k (Zero Gradient Updates)</text>

  <!-- Branch to LoRA Adapter A -->
  <path d="M 100 117 L 160 160" stroke="#38bdf8" stroke-width="2"/>
  <rect x="160" y="140" width="130" height="45" rx="6" fill="#0284c7" stroke="#38bdf8"/>
  <text x="175" y="162" fill="#ffffff" font-size="10.5" font-weight="bold">LoRA Matrix A</text>
  <text x="185" y="177" fill="#e0f2fe" font-size="9">r × k (Gaussian Init)</text>

  <!-- Intermediate Bottleneck -->
  <path d="M 290 162 L 320 162" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="330" cy="162" r="8" fill="#38bdf8"/>
  <text x="323" y="190" fill="#7dd3fc" font-size="9">rank r=16</text>

  <!-- LoRA Adapter B -->
  <path d="M 340 162 L 370 162" stroke="#38bdf8" stroke-width="2"/>
  <rect x="370" y="140" width="130" height="45" rx="6" fill="#0284c7" stroke="#38bdf8"/>
  <text x="175+210" y="162" fill="#ffffff" font-size="10.5" font-weight="bold">LoRA Matrix B</text>
  <text x="185+210" y="177" fill="#e0f2fe" font-size="9">d × r (Zero Init)</text>

  <!-- Summation Point (+) -->
  <path d="M 380 80 L 540 110" stroke="#64748b" stroke-width="2"/>
  <path d="M 500 162 L 540 125" stroke="#38bdf8" stroke-width="2"/>
  
  <circle cx="550" cy="117" r="14" fill="#22c55e"/>
  <text x="544" y="122" fill="#ffffff" font-size="16" font-weight="bold">+</text>

  <!-- Output Vector h -->
  <path d="M 564 117 L 610 117" stroke="#22c55e" stroke-width="2"/>
  <rect x="610" y="90" width="50" height="55" rx="6" fill="#1e293b" stroke="#22c55e"/>
  <text x="625" y="122" fill="#22c55e" font-size="13" font-weight="bold">h</text>
</svg>
<div class="diagram-cap">Figure 153.2: LoRA Parameter Decomposition: Freezing massive base weights and training low-rank bottleneck projections.</div>
</div>
"""

# ── WEEK 26 DAY 188: Industrial 4-Stage Recommendation System Funnel ──
SVG_DIAGRAMS[188] = """
<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="Industrial Recommendation System Multi-Stage Funnel" height="280" viewBox="0 0 700 280" width="700" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <defs>
    <linearGradient id="funnel-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect x="10" y="10" width="680" height="260" rx="12" fill="url(#funnel-bg)" stroke="#334155" stroke-width="2"/>
  <text x="30" y="35" fill="#f59e0b" font-size="13" font-weight="bold">Industrial Recommendation Multi-Stage Funnel Architecture</text>

  <!-- Stage 1: Candidate Generation -->
  <polygon points="50,55 650,55 580,105 120,105" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="210" y="78" fill="#93c5fd" font-size="12" font-weight="bold">1. Candidate Retrieval (Two-Tower / FAISS ANN)</text>
  <text x="225" y="95" fill="#bfdbfe" font-size="10">10,000,000 Items → 1,000 Candidates | Latency: 5ms</text>

  <!-- Stage 2: Heavy Neural Ranking -->
  <polygon points="125,110 575,110 515,160 185,160" fill="#431407" stroke="#ea580c" stroke-width="1.5"/>
  <text x="220" y="133" fill="#fdba74" font-size="12" font-weight="bold">2. Heavy Neural Ranking (DLRM / Deep & Cross)</text>
  <text x="235" y="150" fill="#fed7aa" font-size="10">1,000 Candidates → 100 Items | Latency: 25ms</text>

  <!-- Stage 3: Re-ranking & Diversity -->
  <polygon points="190,165 510,165 460,215 240,215" fill="#14532d" stroke="#16a34a" stroke-width="1.5"/>
  <text x="220" y="188" fill="#86efac" font-size="12" font-weight="bold">3. Re-Ranking & Diversity (MMR + Rules)</text>
  <text x="255" y="205" fill="#bbf7d0" font-size="10">100 Items → 20 Items | Latency: 5ms</text>

  <!-- Stage 4: User Delivery Feed -->
  <rect x="250" y="222" width="200" height="35" rx="6" fill="#9333ea"/>
  <text x="270" y="244" fill="#ffffff" font-size="11" font-weight="bold">4. Final User Feed (Top 10)</text>
</svg>
<div class="diagram-cap">Figure 188.2: The Four-Stage Industrial Recommendation Funnel Architecture.</div>
</div>
"""

# ═════════════════════════════════════════════════════════════════════
# INJECT SVG DIAGRAMS INTO WEEKS 18 - 26
# ═════════════════════════════════════════════════════════════════════
print("=== INJECTING HAND-CRAFTED SVG DIAGRAMS INTO WEEKS 18-26 ===")

for w in range(18, 27):
    fpath = f"{DATA_DIR}/week{w:02d}.yaml"
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)

    for day in data.get('days', []):
        did = day.get('id')
        try:
            day_num = int(did)
        except (ValueError, TypeError):
            continue

        if day_num in SVG_DIAGRAMS:
            svg_content = SVG_DIAGRAMS[day_num]
            th = day.get('theory_html', '') or ''
            if '<svg' not in th:
                day['theory_html'] = svg_content + "\n" + th
                print(f"  ✓ Injected Custom SVG Diagram into Day {day_num:03d} ('{day.get('title')[:30]}')")

    save_yaml(fpath, data)
    print(f"  ✓ Saved week{w:02d}.yaml")

print("\n🎉 SVG diagrams successfully injected into Weeks 18-26!")
