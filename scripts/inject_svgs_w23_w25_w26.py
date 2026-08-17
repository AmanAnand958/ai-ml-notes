#!/usr/bin/env python3
"""
scripts/inject_svgs_w23_w25_w26.py
Injects custom high-contrast architectural SVGs into Weeks 23, 25, and 26.
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

# ─────────────────────────────────────────────────────────────────────
# SVG 1: Week 23 Day 164 (AWS SageMaker Architecture)
# ─────────────────────────────────────────────────────────────────────
SVG_W23_D164 = """<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="AWS SageMaker Training and Real-Time Inference Architecture" height="260" viewBox="0 0 700 260" width="700" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <rect x="10" y="10" width="680" height="240" rx="10" fill="#09090b" stroke="#f59e0b" stroke-width="2"/>
  <text x="25" y="35" fill="#fbbf24" font-size="13" font-weight="bold">AWS SageMaker End-to-End Enterprise Architecture</text>

  <!-- Training Tier -->
  <rect x="30" y="60" width="200" height="170" rx="8" fill="#18181b" stroke="#3f3f46"/>
  <text x="45" y="85" fill="#f59e0b" font-size="11" font-weight="bold">1. Ephemeral Training</text>
  <rect x="40" y="100" width="180" height="35" rx="4" fill="#27272a" stroke="#f59e0b"/>
  <text x="50" y="122" fill="#fbbf24" font-size="10">EC2 GPU (ml.g5.12xlarge)</text>
  <text x="50" y="155" fill="#94a3b8" font-size="9.5">• Pulls Dataset from S3</text>
  <text x="50" y="175" fill="#94a3b8" font-size="9.5">• Executes PyTorch / ECR</text>
  <text x="50" y="195" fill="#ef4444" font-size="9.5">• Auto-Terminates on Finish</text>

  <path d="M 230 145 L 270 145" stroke="#f59e0b" stroke-width="2"/>

  <!-- Model Registry Tier -->
  <rect x="270" y="60" width="180" height="170" rx="8" fill="#18181b" stroke="#38bdf8"/>
  <text x="285" y="85" fill="#38bdf8" font-size="11" font-weight="bold">2. Model Registry</text>
  <rect x="280" y="100" width="160" height="35" rx="4" fill="#0284c7"/>
  <text x="290" y="122" fill="#ffffff" font-size="10" font-weight="bold">Model Version Catalog</text>
  <text x="290" y="155" fill="#94a3b8" font-size="9.5">• S3 Artifact Lineage</text>
  <text x="290" y="175" fill="#94a3b8" font-size="9.5">• Approval Gate @champion</text>
  <text x="290" y="195" fill="#94a3b8" font-size="9.5">• Metadata / Metrics Log</text>

  <path d="M 450 145 L 490 145" stroke="#38bdf8" stroke-width="2"/>

  <!-- Serving Tier -->
  <rect x="490" y="60" width="180" height="170" rx="8" fill="#18181b" stroke="#10b981"/>
  <text x="505" y="85" fill="#10b981" font-size="11" font-weight="bold">3. Multi-Model Endpoint</text>
  <rect x="500" y="100" width="160" height="35" rx="4" fill="#065f46"/>
  <text x="510" y="122" fill="#ffffff" font-size="10" font-weight="bold">ALB + Auto-Scaling</text>
  <text x="510" y="155" fill="#94a3b8" font-size="9.5">• GPU Memory Pooling</text>
  <text x="510" y="175" fill="#94a3b8" font-size="9.5">• Dynamic Model Loading</text>
  <text x="510" y="195" fill="#10b981" font-size="9.5">• &lt;15ms p99 Latency</text>
</svg>
<div class="diagram-cap">Figure 164.1: AWS SageMaker Lifecycle: Ephemeral GPU Training $\to$ Model Registry Lineage $\to$ Multi-Model Endpoint Serving.</div>
</div>"""

# ─────────────────────────────────────────────────────────────────────
# SVG 2: Week 25 Day 180 (Prometheus HPA Autoscaling)
# ─────────────────────────────────────────────────────────────────────
SVG_W25_D180 = """<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="Kubernetes Horizontal Pod Autoscaling on GPU Metrics" height="260" viewBox="0 0 700 260" width="700" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <rect x="10" y="10" width="680" height="240" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="25" y="35" fill="#38bdf8" font-size="13" font-weight="bold">Kubernetes Custom GPU Metric Autoscaling (Prometheus HPA)</text>

  <rect x="30" y="70" width="180" height="70" rx="6" fill="#1e293b" stroke="#64748b"/>
  <text x="45" y="95" fill="#f8fafc" font-size="11" font-weight="bold">vLLM Inference Pods</text>
  <text x="45" y="115" fill="#94a3b8" font-size="9.5">Exposing :8000/metrics</text>
  <text x="45" y="130" fill="#38bdf8" font-size="9.5">Queue Depth + DCGM GPU%</text>

  <path d="M 210 105 L 260 105" stroke="#38bdf8" stroke-width="2"/>

  <rect x="260" y="70" width="170" height="70" rx="6" fill="#1e293b" stroke="#f59e0b"/>
  <text x="275" y="95" fill="#f59e0b" font-size="11" font-weight="bold">Prometheus Server</text>
  <text x="275" y="115" fill="#94a3b8" font-size="9.5">Scrapes every 5s</text>
  <text x="275" y="130" fill="#94a3b8" font-size="9.5">Calculates Avg Rate</text>

  <path d="M 430 105 L 480 105" stroke="#f59e0b" stroke-width="2"/>

  <rect x="480" y="70" width="190" height="70" rx="6" fill="#1e293b" stroke="#10b981"/>
  <text x="495" y="95" fill="#10b981" font-size="11" font-weight="bold">K8s HPA Controller</text>
  <text x="495" y="115" fill="#94a3b8" font-size="9.5">Target: Queue &gt; 5 / Pod</text>
  <text x="495" y="130" fill="#10b981" font-size="9.5">Scale: 2 → 8 GPU Replicas</text>

  <rect x="30" y="165" width="640" height="60" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="45" y="190" fill="#f8fafc" font-size="10.5" font-weight="bold">Formula: DesiredReplicas = ceil[ CurrentReplicas × ( CurrentMetricValue / TargetMetricValue ) ]</text>
  <text x="45" y="210" fill="#94a3b8" font-size="9.5">Prevents inference throttling during sudden LLM query traffic bursts.</text>
</svg>
<div class="diagram-cap">Figure 180.1: Kubernetes HPA Autoscaling Pipeline: Scraping vLLM Queue Metrics to dynamically scale GPU pods.</div>
</div>"""

# ─────────────────────────────────────────────────────────────────────
# SVG 3: Week 26 Day 185 (Vision Transformer Multimodal Pipeline)
# ─────────────────────────────────────────────────────────────────────
SVG_W26_D185 = """<div style="margin: 1.5rem 0; text-align: center;">
<svg aria-label="Vision Language Model ViT Patch Token Projection Architecture" height="260" viewBox="0 0 700 260" width="700" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: var(--font-mono, monospace);">
  <rect x="10" y="10" width="680" height="240" rx="10" fill="#09090b" stroke="#a855f7" stroke-width="2"/>
  <text x="25" y="35" fill="#c084fc" font-size="13" font-weight="bold">Vision-Language Model (VLM): ViT Patch Projection Pipeline</text>

  <rect x="30" y="70" width="130" height="80" rx="6" fill="#18181b" stroke="#38bdf8"/>
  <text x="40" y="95" fill="#38bdf8" font-size="11" font-weight="bold">Input Image</text>
  <text x="40" y="115" fill="#94a3b8" font-size="9.5">336 × 336 RGB</text>
  <text x="40" y="135" fill="#94a3b8" font-size="9.5">576 Patches (14×14)</text>

  <path d="M 160 110 L 200 110" stroke="#38bdf8" stroke-width="2"/>

  <rect x="200" y="70" width="140" height="80" rx="6" fill="#18181b" stroke="#f59e0b"/>
  <text x="210" y="95" fill="#f59e0b" font-size="11" font-weight="bold">Vision Encoder</text>
  <text x="210" y="115" fill="#94a3b8" font-size="9.5">CLIP / SigLIP ViT</text>
  <text x="210" y="135" fill="#94a3b8" font-size="9.5">R^(576 × 1024)</text>

  <path d="M 340 110 L 380 110" stroke="#f59e0b" stroke-width="2"/>

  <rect x="380" y="70" width="140" height="80" rx="6" fill="#18181b" stroke="#ec4899"/>
  <text x="390" y="95" fill="#ec4899" font-size="11" font-weight="bold">MLP Projector</text>
  <text x="390" y="115" fill="#94a3b8" font-size="9.5">Linear → GELU → Linear</text>
  <text x="390" y="135" fill="#94a3b8" font-size="9.5">Maps 1024d → 4096d</text>

  <path d="M 520 110 L 560 110" stroke="#ec4899" stroke-width="2"/>

  <rect x="560" y="70" width="110" height="80" rx="6" fill="#18181b" stroke="#10b981"/>
  <text x="570" y="95" fill="#10b981" font-size="11" font-weight="bold">Text LLM</text>
  <text x="570" y="115" fill="#94a3b8" font-size="9.5">Llama-3 Core</text>
  <text x="570" y="135" fill="#10b981" font-size="9.5">Unified Tokens</text>

  <rect x="30" y="170" width="640" height="55" rx="6" fill="#18181b" stroke="#3f3f46"/>
  <text x="45" y="195" fill="#a855f7" font-size="10.5" font-weight="bold">Visual Tokens are treated as continuous prefix embeddings in the LLM's autoregressive context.</text>
  <text x="45" y="212" fill="#94a3b8" font-size="9.5">Enables joint visual-spatial reasoning and document question answering in a single forward pass.</text>
</svg>
<div class="diagram-cap">Figure 185.1: Vision-Language Model Architecture: Patching $\to$ ViT Encoding $\to$ MLP Projection $\to$ Unified LLM Attention.</div>
</div>"""

# Apply SVGs to YAMLs
# 1. Week 23 Day 164
w23 = load_yaml(f"{DATA_DIR}/week23.yaml")
for d in w23['days']:
    if d['id'] == 164:
        d['theory_html'] = SVG_W23_D164 + "\n" + d['theory_html']
save_yaml(f"{DATA_DIR}/week23.yaml", w23)
print("✓ Injected SVG into Week 23 Day 164")

# 2. Week 25 Day 180
w25 = load_yaml(f"{DATA_DIR}/week25.yaml")
for d in w25['days']:
    if d['id'] == 180:
        d['theory_html'] = SVG_W25_D180 + "\n" + d['theory_html']
save_yaml(f"{DATA_DIR}/week25.yaml", w25)
print("✓ Injected SVG into Week 25 Day 180")

# 3. Week 26 Day 185
w26 = load_yaml(f"{DATA_DIR}/week26.yaml")
for d in w26['days']:
    if d['id'] == 185:
        d['theory_html'] = SVG_W26_D185 + "\n" + d['theory_html']
save_yaml(f"{DATA_DIR}/week26.yaml", w26)
print("✓ Injected SVG into Week 26 Day 185")
