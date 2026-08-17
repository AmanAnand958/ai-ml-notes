#!/usr/bin/env python3
"""
scripts/audit_topic_coverage_completeness.py
Audits topic completeness and coverage gaps across all 191 days:
Evaluates whether each day's topic contains all required production concepts or has gaps:
1. NumPy (Broadcasting, strides, views vs copies, memory layout C/F, einsum, vectorized ops)
2. Pandas (Indexing loc/iloc, groupby optimizations, memory types, categorical memory, merges)
3. Linear Algebra (SVD, Eigenvalues, QR, Condition Numbers, Norms, Projections)
4. Calculus & Optimization (Hessians, Jacobians, Taylor Expansion, Convexity, Momentum, Adam, L-BFGS)
5. Classical ML (Bias-Variance, Regularization L1/L2, Trees, Ensembles, SVM Kernels, Naive Bayes)
6. Deep Learning & CNNs (Receptive field, Backprop derivations, Dilated conv, Depthwise separable)
7. RNNs & Transformers (BPTT, Exploding gradients, RoPE, ALiBi, Multi-Head, KV caching)
8. LLM Fine-Tuning & Quantization (LoRA, QLoRA, AWQ, GPTQ, GGUF, Unsloth, DPO, PPO)
9. RAG & Vector DBs (HNSW, IVF-PQ, BM25+Dense Hybrid, Cross-encoders, RAGAS, Context precision)
10. MLOps & Serving (vLLM, Triton, Continuous batching, PagedAttention, Prometheus, CI/CD, Docker)
"""

import glob, yaml, re, os, json

print("=== STARTING TOPIC COVERAGE COMPLETENESS AUDIT ===")

TOPIC_CHECKLISTS = {
    "NumPy": {
        "days": [7],
        "must_have": [
            ("Broadcasting Rules", ["broadcast", "stride", "dimension"]),
            ("Views vs Copies", ["view", "copy", "base", "memory"]),
            ("Memory Strides & Contiguity", ["stride", "contiguous", "c_contiguous", "order"]),
            ("Einstein Summation (einsum)", ["einsum", "einops", "contraction"]),
            ("Vectorized Matrix Operations", ["matmul", "dot", "axis", "vectorize"]),
            ("Random Sampling & Seeds", ["random", "seed", "generator", "choice"])
        ]
    },
    "Pandas": {
        "days": [8, 9, 10],
        "must_have": [
            ("Explicit Indexing (loc vs iloc)", ["loc", "iloc", "indexing"]),
            ("Memory Optimization & Categoricals", ["category", "memory_usage", "dtype", "downcast"]),
            ("GroupBy & Split-Apply-Combine", ["groupby", "agg", "transform", "apply"]),
            ("Time-Series & Resampling", ["resample", "datetime", "rolling"]),
            ("Merge & Join Strategies", ["merge", "join", "how='inner'", "indicator"])
        ]
    },
    "Linear Algebra": {
        "days": [22, 23, 24],
        "must_have": [
            ("Vector Spaces & Linear Independence", ["span", "basis", "dimension", "rank"]),
            ("Matrix Decompositions (LU / QR / SVD)", ["svd", "singular value", "decomposition", "qr"]),
            ("Eigenvalues & Eigenvectors", ["eigenvalue", "eigenvector", "characteristic", "spectral"]),
            ("Matrix Inversion & Condition Number", ["determinant", "condition number", "pseudo-inverse", "pinv"]),
            ("Geometric Projections & Orthogonality", ["orthogonal", "projection", "gram-schmidt", "dot product"])
        ]
    },
    "Calculus & Optimization": {
        "days": [25, 26, 27, 28],
        "must_have": [
            ("Multivariate Gradients & Jacobians", ["gradient", "jacobian", "partial derivative"]),
            ("Hessian Matrix & Curvature", ["hessian", "curvature", "second derivative", "saddle point"]),
            ("Stochastic Gradient Descent & Momentum", ["sgd", "momentum", "velocity", "learning rate"]),
            ("Adaptive Optimizers (Adam, RMSprop)", ["adam", "rmsprop", "second moment", "bias correction"]),
            ("Convexity & Taylor Expansion", ["convex", "taylor", "local minimum", "loss landscape"])
        ]
    },
    "Classical ML": {
        "days": [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
        "must_have": [
            ("Bias-Variance Decomposition", ["bias", "variance", "overfitting", "underfitting"]),
            ("Regularization (Lasso L1 / Ridge L2 / ElasticNet)", ["l1", "l2", "lasso", "ridge", "sparsity"]),
            ("Decision Trees & Impurity (Gini / Entropy)", ["gini", "entropy", "information gain", "split"]),
            ("Ensembles (Random Forest & Gradient Boosting / XGBoost)", ["bagging", "boosting", "random forest", "xgboost", "residual"]),
            ("Support Vector Machines & Kernel Trick", ["margin", "support vector", "rbf", "kernel", "slack"]),
            ("Evaluation Metrics (ROC-AUC, Precision-Recall, F1)", ["roc", "auc", "precision", "recall", "confusion matrix"])
        ]
    },
    "Deep Learning & PyTorch": {
        "days": [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
        "must_have": [
            ("Autograd Computational Graph & Backward Pass", ["autograd", "backward", "grad", "computation graph"]),
            ("Activation Functions (ReLU, GELU, SiLU, LeakyReLU)", ["relu", "gelu", "silu", "vanishing gradient"]),
            ("Normalization Layers (BatchNorm vs LayerNorm vs RMSNorm)", ["batchnorm", "layernorm", "rmsnorm", "running mean"]),
            ("Initialization Schemes (Xavier / He Kaiming)", ["xavier", "kaiming", "initialization", "variance"]),
            ("Custom Loss Functions & Datasets/DataLoaders", ["dataset", "dataloader", "custom loss", "batch_size", "collate_fn"])
        ]
    },
    "CNNs & Computer Vision": {
        "days": [57, 58, 59, 60, 61, 62, 63],
        "must_have": [
            ("Convolution Arithmetic (Padding, Stride, Dilation)", ["stride", "padding", "dilation", "feature map", "kernel"]),
            ("Receptive Field Calculation", ["receptive field", "effective receptive field", "pooling"]),
            ("Modern Architectures (ResNet Residual Connections)", ["resnet", "residual", "skip connection", "bottleneck"]),
            ("Transfer Learning & Pretrained Backbones", ["pretrained", "freeze", "fine-tuning", "imagenet"])
        ]
    },
    "Transformers & LLMs": {
        "days": [71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84],
        "must_have": [
            ("Multi-Head Attention & Scaled Dot-Product", ["multi-head", "scaled dot-product", "qkv", "d_k"]),
            ("Positional Encodings (Sinusoidal, RoPE, ALiBi)", ["positional", "rope", "rotary", "sinusoidal"]),
            ("Causal Masking & KV Caching", ["causal", "mask", "kv cache", "autoregressive"]),
            ("Transformer Encoder vs Decoder Architecture", ["encoder", "decoder", "cross-attention", "bert", "gpt"]),
            ("Fine-Tuning (LoRA, QLoRA, PEFT)", ["lora", "qlora", "adapter", "rank", "alpha"]),
            ("Model Quantization (INT8 / INT4 / GGUF / AWQ)", ["quantization", "int4", "int8", "gguf", "awq", "smoothquant"])
        ]
    },
    "RAG & Vector Search": {
        "days": [99, 100, 101, 102, 103, 104, 105],
        "must_have": [
            ("Vector Indexing Algorithms (HNSW, IVF-PQ)", ["hnsw", "ivf", "pq", "quantization", "graph"]),
            ("Hybrid Search (Dense + Sparse BM25 / RRF)", ["bm25", "hybrid", "reciprocal rank fusion", "rrf"]),
            ("Chunking Strategies & Context Stuffing", ["chunking", "semantic chunking", "sliding window"]),
            ("Reranking (Cross-Encoders)", ["rerank", "cross-encoder", "relevance"]),
            ("Evaluation Frameworks (RAGAS / TruLens)", ["ragas", "faithfulness", "groundedness", "answer relevance"])
        ]
    },
    "High-Throughput Serving & MLOps": {
        "days": [127, 128, 129, 130, 131, 132, 133],
        "must_have": [
            ("Continuous Batching & PagedAttention (vLLM)", ["continuous batching", "pagedattention", "vllm", "block table"]),
            ("Triton Inference Server Dynamic Batching", ["triton", "model repository", "dynamic batching", "sla"]),
            ("Distributed Training (DDP / FSDP / ZeRO-1/2/3)", ["ddp", "fsdp", "zero", "allreduce", "pipeline"]),
            ("Monitoring & Metrics (Prometheus / Grafana / Drift)", ["prometheus", "grafana", "drift", "psi", "latency"])
        ]
    }
}

coverage_findings = []
cov_id = 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
all_day_data = {}

for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        d_yaml = yaml.safe_load(f)
    for d in d_yaml.get('days', []):
        all_day_data[d.get('day_num')] = d

for topic_name, spec in TOPIC_CHECKLISTS.items():
    combined_topic_text = ""
    for d_num in spec["days"]:
        if d_num in all_day_data:
            day_obj = all_day_data[d_num]
            combined_topic_text += " " + str(day_obj.get('title', ''))
            combined_topic_text += " " + str(day_obj.get('theory_html', ''))
            for t in day_obj.get('tasks', []):
                combined_topic_text += " " + str(t.get('title', '')) + " " + str(t.get('solution_code', ''))

    combined_topic_text = combined_topic_text.lower()
    
    for concept_title, keywords in spec["must_have"]:
        found = any(k.lower() in combined_topic_text for k in keywords)
        if not found:
            coverage_findings.append({
                "id": f"COV-{cov_id:03d}",
                "topic": topic_name,
                "target_days": spec["days"],
                "missing_concept": concept_title,
                "required_keywords": keywords,
                "status": "GAP_DETECTED"
            })
            cov_id += 1
        else:
            coverage_findings.append({
                "id": f"COV-{cov_id:03d}",
                "topic": topic_name,
                "target_days": spec["days"],
                "missing_concept": concept_title,
                "required_keywords": keywords,
                "status": "VERIFIED_PRESENT"
            })
            cov_id += 1

print(f"\nTotal Concept Checkpoints Evaluated: {len(coverage_findings)}")
gaps = [c for c in coverage_findings if c["status"] == "GAP_DETECTED"]
verified = [c for c in coverage_findings if c["status"] == "VERIFIED_PRESENT"]

print(f"  • Verified Complete: {len(verified)}")
print(f"  • Coverage Gaps:     {len(gaps)}")

with open('scripts/topic_coverage_report.json', 'w', encoding='utf-8') as f:
    json.dump(coverage_findings, f, indent=2)

print("Saved report to: scripts/topic_coverage_report.json")
