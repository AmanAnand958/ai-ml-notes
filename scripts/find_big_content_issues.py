#!/usr/bin/env python3
"""
scripts/find_big_content_issues.py
Deep audit of 7 Major Content-Level & Conceptual Deficiencies:
1. Deprecated / Unethical Datasets (e.g., Boston Housing in ML examples)
2. Toy Dataset Dependency vs Out-of-Core Industrial Scale (Lack of Polars/DuckDB/Parquet streaming)
3. PyTorch 2.0+ Modern Compiler Architecture Gaps (torch.compile, Inductor, Triton Kernel fusion)
4. Vision-Language Multi-Modal Contrastive Learning Gaps (CLIP InfoNCE loss, temperature tuning)
5. Subword Tokenizer Failure Modes & Glitch Tokens (Byte-fallback, token-healing, prompt whitespace trapping)
6. Serving Capacity Planning: Exact KV Cache VRAM Sizing Equation (FP16/FP8 memory formulas)
7. LLM Benchmark Contamination & Overfitting Detection (N-gram overlap, decontamination protocols)
"""

import glob, yaml, re, os, json

print("=== STARTING BIG CONTENT-LEVEL ARCHITECTURAL AUDIT ===")

findings = []
f_id = 1

def record_issue(domain, severity, title, core_problem, pedagogical_impact, architectural_solution):
    global f_id
    findings.append({
        "id": f"CONTENT-{f_id:03d}",
        "domain": domain,
        "severity": severity,
        "title": title,
        "core_problem": core_problem,
        "pedagogical_impact": pedagogical_impact,
        "architectural_solution": architectural_solution
    })
    f_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
all_yaml_text = ""
for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        all_yaml_text += f.read()

# 1. Check for Boston Housing Dataset references
if 'boston' in all_yaml_text.lower():
    record_issue(
        "Ethical ML & Standards",
        "High",
        "Usage of Ethical / Deprecated Boston Housing Dataset",
        "The Boston Housing dataset was officially deprecated and removed from Scikit-Learn 1.2 due to ethical issues and racial bias in its B attribute.",
        "Students learn on deprecated datasets that fail modern ethical compliance and industry standards.",
        "Replace all occurrences with the California Housing dataset (`fetch_california_housing()`) or synthetic multi-variate housing data."
    )

# 2. PyTorch 2.0 Compilation & Kernel Fusion (torch.compile)
if 'torch.compile' not in all_yaml_text:
    record_issue(
        "Deep Learning Systems",
        "Critical",
        "Absence of PyTorch 2.0+ Compiler Stack (torch.compile, TorchDynamo & Inductor)",
        "PyTorch 2.x fundamentally changed deep learning performance from eager python dispatch to graph capture via TorchDynamo and OpenAI Triton kernel code generation via TorchInductor.",
        "Students are taught purely legacy PyTorch 1.x eager execution, leaving them unaware of 2x-3x speedups, memory fusion, and CUDA graph capture standard in 2024-2026 production.",
        "Add a dedicated module in Week 8/19: 'PyTorch 2.x Compiler Internals — TorchDynamo, AOTAutograd, Inductor & Triton Kernel Fusion'."
    )

# 3. Vision-Language & Contrastive Learning (CLIP & InfoNCE)
if 'infonce' not in all_yaml_text.lower() and 'clip' not in all_yaml_text.lower():
    record_issue(
        "Multimodal AI",
        "Critical",
        "Missing Contrastive Representation Learning & CLIP InfoNCE Loss",
        "Modern multimodal AI (vision-language models, diffusion text encoders, modern dense retrieval) is founded on Contrastive Language-Image Pretraining (CLIP) and InfoNCE dual-encoder loss.",
        "Students have a massive conceptual gap between unimodal text/image transformers and unified multimodal embeddings.",
        "Inject the InfoNCE symmetric cross-entropy derivation and dual-encoder projection architecture into Week 14/26."
    )

# 4. Exact KV Cache Production VRAM Sizing Equation
if '2 * n_layers' not in all_yaml_text and 'kv cache sizing' not in all_yaml_text.lower():
    record_issue(
        "LLM Serving Systems",
        "Critical",
        "Missing Production KV Cache Capacity Planning & VRAM Equation",
        "MLOps and LLM serving engineers must calculate exact GPU VRAM budgets for KV Cache: `Bytes = 2 × n_layers × n_kv_heads × d_head × precision_bytes × sequence_length × batch_size`.",
        "Students cannot perform capacity planning for vLLM / TensorRT-LLM clusters or determine maximum concurrent batch sizes before encountering OOMs.",
        "Add the formal KV cache VRAM sizing formula, GQA reduction derivation (8x memory savings vs MHA), and FP8 KV cache quantization in Week 19."
    )

# 5. Tokenization Edge Cases (Byte-Fallback, Glitch Tokens & Token-Healing)
if 'token-healing' not in all_yaml_text.lower() and 'glitch token' not in all_yaml_text.lower():
    record_issue(
        "LLM Engineering",
        "High",
        "Absence of Subword Tokenizer Production Traps (Token-Healing & Glitch Tokens)",
        "Standard BPE tokenizers produce severe generation artifacts when prompts end in whitespace (token boundary mismatch), and contain 'glitch tokens' (unseen embeddings causing prompt injection or model degeneration).",
        "Students build LLM prompts without understanding token boundary alignment, leading to degraded prompt-following and token-healing bugs in production APIs.",
        "Add a deep dive in Week 13 on Token-Healing algorithms, Byte-level BPE fallback, and Tokenizer vocab alignment."
    )

# 6. Benchmark Data Contamination & Decontamination Protocols
if 'decontamination' not in all_yaml_text.lower() and 'n-gram overlap' not in all_yaml_text.lower():
    record_issue(
        "LLM Evaluation",
        "High",
        "Missing LLM Benchmark Data Contamination & Decontamination Protocols",
        "Evaluating fine-tuned models on public benchmarks (GSM8K, MMLU, HumanEval) frequently yields artificially inflated scores due to test set leakage into pretraining/SFT corpora.",
        "Students cannot distinguish genuine model reasoning improvements from data contamination artifacts.",
        "Inject formal 8-gram and 13-gram decontamination filtering protocols, MinHash LSH deduplication, and perplexity outlier testing in Week 25."
    )

# 7. Industrial Scale Data Ingestion (DuckDB / Polars Out-of-Core Processing)
if 'duckdb' not in all_yaml_text.lower() and 'polars' not in all_yaml_text.lower():
    record_issue(
        "Data Engineering",
        "High",
        "Absence of Modern Out-of-Core Tabular Engines (Polars / DuckDB / Arrow)",
        "Pandas loads entire datasets into uncompressed in-memory RAM with high object-pointer overhead. Production ML pipelines process 50GB-1TB tabular features using Apache Arrow columnar formats, Polars lazy execution graphs, and DuckDB out-of-core SQL.",
        "Students are unprepared for real-world datasets exceeding laptop RAM (50GB+), assuming Pandas is the only tabular tool.",
        "Add a modern data engineering section in Week 2/3 comparing Pandas eager execution with Polars lazy query optimization and DuckDB parquet streaming."
    )

print(f"\nTotal Big Content-Level Issues Identified: {len(findings)}")

with open('scripts/big_content_issues_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("Saved report to: scripts/big_content_issues_report.json")
