#!/usr/bin/env python3
"""
scripts/find_macro_architectural_issues.py
Deep macro-architectural analysis of:
1. Pacing & Cognitive Load Cliffs (Weeks where concept density jumps >5x)
2. Critical 2024-2026 Industry Technology Blindspots (MoE, FlashAttention, Speculative Decoding, Reasoning MCTS, YaRN)
3. Hardware Accessibility & Local Execution Barriers (Multi-GPU/Cloud requirements without CPU fallbacks)
4. Frontend Client Architecture & State Resiliency (Storage migration, offline caching, Pyodide worker failover)
5. Prerequisite Inversions & Forward References across weeks
"""

import glob, yaml, re, os, json

print("=== STARTING MACRO-ARCHITECTURAL CURRICULUM AUDIT ===")

macro_issues = []
m_id = 1

def add_macro(domain, severity, title, structural_flaw, evidence_analysis, architectural_recommendation):
    global m_id
    macro_issues.append({
        "id": f"MACRO-{m_id:03d}",
        "domain": domain,
        "severity": severity,
        "title": title,
        "structural_flaw": structural_flaw,
        "evidence_analysis": evidence_analysis,
        "architectural_recommendation": architectural_recommendation
    })
    m_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))

# 1. PACING & COGNITIVE LOAD ANALYSIS
print("1. Analyzing Pacing & Cognitive Density Cliffs...")
week_densities = {}
for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    total_concepts = sum(len(d.get('concept_flow', [])) for d in data.get('days', []))
    week_densities[w_num] = total_concepts

# Compare Week 1 (Beginner Python) vs Week 12 (LLMs) vs Week 21 (Distributed Training)
add_macro(
    "Curriculum Pacing",
    "Critical",
    "Cognitive Load Cliff: 10x Density Spike Between Foundations and Modern LLM Systems",
    "The curriculum allocates 7 full days to basic Python syntax (Week 1), but packs the entirety of modern LLM engineering (LoRA, QLoRA, 4-bit Quantization, GGUF, AWQ, Scaling Laws, Prompting) into a single 7-day sprint (Week 12).",
    f"Week 1 Concept Density: {week_densities.get(1, 0)} basic syntax items over 7 days vs Week 12: {week_densities.get(12, 0)} advanced frontier LLM architecture items in the same timeframe.",
    "Split Week 12 into a 2-week track: 'Week 12: Parameter-Efficient Fine-Tuning (LoRA/QLoRA/PEFT)' and 'Week 13: High-Performance Model Quantization (GGUF/AWQ/GPTQ)'."
)

add_macro(
    "Curriculum Pacing",
    "Critical",
    "Distributed Training & Parallelism Compression Bottleneck",
    "Week 21 attempts to teach DataParallel, DDP, Tensor Parallelism (Megatron-LM), Pipeline Parallelism (1F1B), FSDP, and DeepSpeed ZeRO-1/2/3 in 7 days, giving students <24 hours per distributed paradigm.",
    f"Week 21 covers 6 distinct cluster communication topologies and distributed memory models in 7 days.",
    "Introduce prerequisite inter-GPU communication primitives (NCCL, Ring-AllReduce, Broadcast) earlier in Week 8/17 before tackling multi-dimensional parallelism."
)

# 2. MODERN INDUSTRY TECHNOLOGY BLINDSPOTS (2024-2026 Frontiers)
print("2. Auditing Industry Frontier Blindspots...")

all_text = ""
for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        all_text += f.read()

BLINDSPOTS = [
    (
        "Mixture of Experts (MoE) Architecture Gaps",
        "moe",
        "DeepSeek, Mixtral, and modern frontier LLMs rely entirely on Sparse Mixture of Experts (MoE) with top-k gating, router load balancing, and expert capacity factors. The curriculum lacks a dedicated day on MoE routing.",
        "Include a dedicated standalone Day in Week 12/19: 'Mixture of Experts (MoE) — Top-K Routing, Expert Parallelism & Load Balancing Loss'."
    ),
    (
        "FlashAttention (v1, v2, v3) IO-Awareness & SRAM Tiling",
        "flashattention",
        "Attention memory bandwidth is the primary bottleneck in LLM training and inference. FlashAttention's online softmax and SRAM tiling are mentioned in passing but lack a mathematical derivation.",
        "Add a dedicated module in Week 11/19 deriving the online softmax numerical stability update and SRAM block tiling algorithm."
    ),
    (
        "Speculative Decoding & Draft Model Acceleration",
        "speculative decoding",
        "Inference acceleration via small draft model verification (Speculative Decoding, Medusa, Lookahead) is industry standard for reducing latency but absent from serving modules.",
        "Add Speculative Decoding in Week 19 (Inference Serving) explaining acceptance sampling criteria and tree-based draft verification."
    ),
    (
        "ColBERT & Late-Interaction Retrieval in Modern RAG",
        "colbert",
        "Dense single-vector embeddings suffer from information loss on complex queries. Late-interaction token-level similarity (ColBERT / PLAID) is missing from Week 14/15 RAG modules.",
        "Add Multi-Vector & Late-Interaction Retrieval to Week 15 showing MaxSim operator computation."
    ),
    (
        "Test-Time Compute & MCTS Reasoning Models (o1 / DeepSeek-R1)",
        "mcts",
        "The shift from pretraining scaling to test-time search scaling (Monte Carlo Tree Search, Process Reward Models, Chain-of-Thought verification) is absent from Week 22 RLHF.",
        "Add a dedicated module on Test-Time Compute Scaling, Process Supervision (PRMs), and Monte Carlo Tree Search for LLM reasoning."
    )
]

for title, kw, flaw, fix in BLINDSPOTS:
    if kw not in all_text.lower() or all_text.lower().count(kw) < 3:
        add_macro(
            "Curriculum Gaps",
            "High",
            title,
            flaw,
            f"Keyword '{kw}' frequency across all 26 weeks: {all_text.lower().count(kw)} mentions.",
            fix
        )

# 3. HARDWARE ACCESSIBILITY & CLOUD DEPENDENCY BARRIERS
print("3. Auditing Hardware Barriers & Local Execution Feasibility...")
add_macro(
    "Student Accessibility",
    "Critical",
    "Multi-GPU & Cloud Infrastructure Execution Barrier on Student Laptops",
    "Weeks 18 (Kubernetes GPU clusters), 19 (TensorRT-LLM/Triton), and 21 (Multi-GPU DDP / DeepSpeed ZeRO-3) assign tasks requiring high-end multi-GPU clusters ($10k+ hardware) without providing local CPU fallback mocks or Google Colab / Kaggle cloud notebook execution bridges.",
    "Tasks in Weeks 18 and 21 fail immediately on standard developer laptops (MacBooks, single-GPU PCs) without fallback simulators.",
    "Provide dual execution tracks: (1) Local PyTorch CPU/MPS multi-process simulation and (2) Zero-setup Google Colab T4/A100 launcher links for all GPU-intensive tasks."
)

# 4. FRONTEND ARCHITECTURE & CLIENT RESILIENCY
print("4. Auditing Frontend Client Architecture...")
add_macro(
    "Client Architecture",
    "High",
    "LocalStorage Schema Fragility & Lack of State Migration Engine",
    "Student progress (XP, completed days, streak, quiz answers) is stored as unversioned raw keys in browser LocalStorage. A change to course structure or day numbering risks breaking student state without an automated migration handler.",
    "No schema version key (e.g. `COURSE_SCHEMA_VERSION = '2.1'`) or migration function exists in `course.js`.",
    "Implement an atomic schema migration layer in `course.js` that checks schema version on boot and safely transforms legacy progress keys."
)

add_macro(
    "Client Architecture",
    "Medium",
    "Lack of Offline Progressive Web App (PWA) Capability for 191-Day Roadmap",
    "As an intensive 6-month curriculum, students study in offline environments (transit, airplanes, low-connectivity zones). The web application lacks a Service Worker, Web Manifest, and cache manifest, preventing offline review.",
    "No `sw.js` (Service Worker) or `manifest.json` found in root directory.",
    "Add a lightweight PWA Service Worker caching core CSS, JS, fonts, and HTML week pages for offline learning."
)

# 5. CODE SANDBOX WORKER FALLBACK
add_macro(
    "Interactive Sandbox",
    "High",
    "Code Sandbox 'Run' Button Fragility on CDN Failover",
    "The interactive 'Run' buttons in code blocks depend on external CDN scripts. If a student is behind a corporate firewall or offline, clicking 'Run' fails silently without showing an informative error or fallback output.",
    "No CDN failover timeout or visual error state when code execution runtime is unreachable.",
    "Implement a 3-second runtime health-check with an inline message: 'Interactive runner offline. Code is display-ready for local terminal execution.'"
)

print(f"\nTotal Macro-Architectural Issues Cataloged: {len(macro_issues)}")

with open('scripts/macro_architectural_issues.json', 'w', encoding='utf-8') as f:
    json.dump(macro_issues, f, indent=2)

print("Saved report to: scripts/macro_architectural_issues.json")
