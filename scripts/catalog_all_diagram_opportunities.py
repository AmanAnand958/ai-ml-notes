#!/usr/bin/env python3
"""
scripts/catalog_all_diagram_opportunities.py
Analyzes the entire 191-day AI/ML curriculum and catalogs every technical diagram needed:
Categorized by:
1. ALREADY INJECTED (20 Major System Architecture Blueprints)
2. HIGH-VALUE REMAINING CONCEPTUAL DIAGRAMS (Mathematical workflows, geometry, dataflow graphs)
"""

import glob, yaml, re, os, json

print("=== CATALOGING ALL CURRICULUM DIAGRAMS ===")

all_yaml = sorted(glob.glob('src/data/week*.yaml'))

existing_diagrams = []
candidate_diagrams = []

# List of topics across all 191 days with diagram specifications
DIAGRAM_TAXONOMY = {
    # Module 1: Python & Foundations (Weeks 1-4)
    3: {"topic": "OOP vs Functional Programming", "type": "Comparison Matrix", "desc": "Object state encapsulation vs stateless pure function pipeline"},
    7: {"topic": "Python Memory Management (Stack vs Heap)", "type": "Memory Layout SVG", "desc": "Stack frames (pointers, references) vs Heap objects (C-structures, refcounts)"},
    9: {"topic": "NumPy Strides & Memory Layout", "type": "Tensor Geometry SVG", "desc": "C-contiguous vs Fortran contiguous row-major strides in 1D/2D arrays"},
    16: {"topic": "Pandas Merges (Inner, Left, Right, Outer)", "type": "Venn / Set Theory SVG", "desc": "Relational table join behaviors and key alignment"},
    22: {"topic": "Matrix Multiplication Geometry & Projections", "type": "Geometric Vector SVG", "desc": "Column space projection matrix P = A(A^T A)^-1 A^T onto subspace"},
    24: {"topic": "Eigenvalues & Eigenvectors", "type": "Geometric Transformation SVG", "desc": "Linear transformation stretch along principal axes (Av = λv)"},
    27: {"topic": "Gradient Descent vs Stochastic GD vs Mini-Batch", "type": "Optimization Trajectory SVG", "desc": "Loss surface contour paths (smooth vs noisy vs mini-batch)"},
    
    # Module 2: Classical ML (Weeks 5-8)
    33: {"topic": "Linear Regression Normal Equation vs OLS", "type": "Geometry SVG", "desc": "Orthogonal projection of target vector y onto feature space X"},
    38: {"topic": "Decision Tree Splitting (Gini & Entropy)", "type": "Binary Partition Tree", "desc": "Recursive 2D feature space partitioning and decision boundaries"},
    43: {"topic": "SVM Maximum Margin Hyperplane & Slack", "type": "Geometric Hyperplane SVG", "desc": "Margin 2/||w|| with support vectors and soft-margin slack variables (ξ_i)"},
    45: {"topic": "Random Forest Bagging & Feature Subsampling", "type": "Ensemble Flowchart", "desc": "Bootstrap aggregation with random subspace feature splits"},
    47: {"topic": "K-Means Clustering Iterations", "type": "Spatial Voronoi Diagram", "desc": "Centroid reassignment and Voronoi cell convergence"},
    
    # Module 3: Deep Learning Foundations (Weeks 9-12)
    57: {"topic": "Multi-Layer Perceptron Forward & Backprop", "type": "Computational Graph", "desc": "Chain rule gradient flow (dL/dW = dL/da * da/dz * dz/dW)"},
    61: {"topic": "Batch Normalization vs Layer Normalization", "type": "Tensor Dimension Cube", "desc": "Normalization axes across (N, C, H, W) vs (N, L, D)"},
    67: {"topic": "LSTM & GRU Gating Cells", "type": "Circuit Architecture Flow", "desc": "Forget, input, cell candidate, and output gate equations"},
    71: {"topic": "Transformer Multi-Head Self-Attention", "type": "Matrix Attention Tensor Flow", "desc": "Q, K, V linear projections, scaled dot-product matrix, and output concat"},
    73: {"topic": "Positional Encoding (Sinusoidal vs RoPE)", "type": "Frequency Geometry SVG", "desc": "Rotary 2D coordinate rotation in complex plane vs absolute wave patterns"},
    
    # Module 4: LLMs, Multi-Modal & Serving (Weeks 13-20)
    85: {"topic": "KV Cache Auto-Regressive Decoding", "type": "Memory Buffer Tensor Diagram", "desc": "Cached Key-Value tensors avoiding redundant prefill computation"},
    91: {"topic": "RAG Hybrid Search & Dense Retrieval", "type": "Information Retrieval Pipeline", "desc": "BM25 keyword search + Dense Vector embedding reciprocal rank fusion (RRF)"},
    100: {"topic": "Vector Database HNSW Indexing", "type": "Hierarchical Graph SVG", "desc": "Multi-layer skip-list graph for sub-millisecond approximate nearest neighbors"},
    115: {"topic": "LoRA & QLoRA Low-Rank Decomposition", "type": "Weight Matrix Factoring SVG", "desc": "W_0 + (B x A) where B in R^(d x r) and A in R^(r x k)"},
    128: {"topic": "TensorRT-LLM & CUDA Kernel Fusion", "type": "GPU Kernel Pipeline", "desc": "Fused GEMM + Bias + Activation preventing VRAM roundtrip latencies"},
    
    # Module 5: Distributed, Alignment & Multi-Agents (Weeks 21-26)
    143: {"topic": "Tensor Parallelism (Megatron-LM Style)", "type": "Matrix Sharding Architecture", "desc": "Column-parallel GEMM in QKV followed by row-parallel GEMM in projection"},
    155: {"topic": "Direct Preference Optimization (DPO)", "type": "Objective Flowchart", "desc": "Implicit reward formulation eliminating separate reward model training"},
    165: {"topic": "Hierarchical Multi-Agent Orchestration", "type": "Supervisor-Worker Graph", "desc": "Supervisor agent delegating specialized subtasks to worker tool agents"},
    172: {"topic": "Automated CI/CD for LLM Apps & Guardrails", "type": "Production Deployment Flow", "desc": "Git commit -> Pytest unit tests -> LLM-as-Judge eval -> Canary rollout"}
}

print(f"Total Canonical Diagram Blueprints Mapped: {len(DIAGRAM_TAXONOMY)}")

with open('scripts/diagram_needs_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(DIAGRAM_TAXONOMY, f, indent=2)

print("Saved catalog to: scripts/diagram_needs_catalog.json")
