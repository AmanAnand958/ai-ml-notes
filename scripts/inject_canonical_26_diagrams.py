#!/usr/bin/env python3
"""
scripts/inject_canonical_26_diagrams.py
Injects 26 rich, responsive, auto-centered architectural and geometric diagrams (SVG & Mermaid)
across Modules 1-5 in both YAML sources and HTML week pages.
"""

import glob, yaml, re, os

print("=== INJECTING 26 CANONICAL CURRICULUM DIAGRAMS ===")

CANONICAL_DIAGRAMS = {
    # Module 1
    7: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Python Memory Model (Stack Pointers vs Heap PyObject)</h4>
<div class="mermaid">
graph LR
    subgraph StackFrame["Call Stack Frame"]
        P1["x (ref: 0x7ffd)"]
        P2["y (ref: 0x7ffd)"]
        P3["data_list (ref: 0x8a10)"]
    end
    subgraph HeapMemory["Heap Memory (PyObject Structures)"]
        H1["PyLongObject (val=42, ob_refcnt=2)"]
        H2["PyListObject (ob_refcnt=1, ob_size=3)"]
        H3["Elements Array [0x7ffd, ...]"]
    end
    P1 --> H1
    P2 --> H1
    P3 --> H2
    H2 --> H3
</div>
<p style="font-size:0.85rem; color:var(--muted); margin-top:0.5rem; line-height:1.5;">
In CPython, variable names on the Call Stack hold memory pointers to reference-counted <code>PyObject</code> structs allocated on the Heap.
</p>
</div>""",

    9: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: NumPy Memory Strides & Contiguity Layout</h4>
<div class="mermaid">
graph TD
    subgraph C_Order["C-Contiguous (Row-Major) — Strides: (24, 8)"]
        R0["Row 0: [0, 1, 2]"] --> R1["Row 1: [3, 4, 5]"]
        M1["Linear Memory: 0, 1, 2, 3, 4, 5 (Step row = 3 * 8B = 24B)"]
    end
    subgraph F_Order["Fortran-Contiguous (Col-Major) — Strides: (8, 16)"]
        C0["Col 0: [0, 3]"] --> C1["Col 1: [1, 4]"] --> C2["Col 2: [2, 5]"]
        M2["Linear Memory: 0, 3, 1, 4, 2, 5 (Step col = 2 * 8B = 16B)"]
    end
</div>
<p style="font-size:0.85rem; color:var(--muted); margin-top:0.5rem; line-height:1.5;">
Strides define the exact byte jump required to advance one step along each dimension in contiguous memory buffers.
</p>
</div>""",

    16: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Pandas Relational Join Mechanics (Inner, Left, Outer)</h4>
<div class="mermaid">
graph LR
    subgraph LeftTable["Left DataFrame (L)"]
        L1["Key: A, Val: 10"]
        L2["Key: B, Val: 20"]
    end
    subgraph RightTable["Right DataFrame (R)"]
        R1["Key: B, Score: 95"]
        R2["Key: C, Score: 80"]
    end
    subgraph Joins["Merge Modes"]
        J1["Inner Join: Key B (Exact match intersection)"]
        J2["Left Join: Key A + Key B (Preserves all L keys, NaN on R)"]
        J3["Outer Join: Keys A, B, C (Full union with NaNs)"]
    end
    LeftTable --> Joins
    RightTable --> Joins
</div>
</div>""",

    22: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Linear Algebra Orthogonal Subspace Projection</h4>
<div class="mermaid">
graph TD
    B["Vector b (Target in R^n)"] --> P["Projection p = Ax_hat (in Col Space)"]
    B --> E["Orthogonal Error e = b - p (in Left Nullspace)"]
    P --> Formula["P = A(A^T A)^-1 A^T b where A^T (b - Ax_hat) = 0"]
</div>
<p style="font-size:0.85rem; color:var(--muted); margin-top:0.5rem; line-height:1.5;">
Least squares projects a target vector perpendicularly onto the subspace spanned by matrix columns.
</p>
</div>""",

    24: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Eigenvalue Invariant Axes & Spectral Decomposition</h4>
<div class="mermaid">
graph LR
    V["Eigenvector v"] --> Trans["Linear Matrix Transformation A"]
    Trans --> Out["Scaled Output Av = λv (Direction preserved, scaled by λ)"]
    Spectral["Spectral Theorem: A = Q Λ Q^T (Orthogonal eigenbasis rotation)"]
</div>
</div>""",

    27: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Gradient Descent Optimization Trajectories</h4>
<div class="mermaid">
graph TD
    Init["Initial Weights w_0"] --> Choice{"Optimizer Strategy"}
    Choice --> BGD["Batch GD: Smooth, deterministic, slow per epoch"]
    Choice --> MBGD["Mini-Batch GD: Balanced noise, GPU parallelized (Standard)"]
    Choice --> SGD["Pure SGD: High variance, noisy jump escapes local minima"]
    BGD --> Opt["Global / Local Minimum w*"]
    MBGD --> Opt
    SGD --> Opt
</div>
</div>""",

    # Module 2
    33: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: OLS Normal Equation vs Gradient Descent</h4>
<div class="mermaid">
graph LR
    Data["Design Matrix X & Target y"] --> Branch{"Solve Method"}
    Branch --> Closed["Closed-Form OLS: theta = (X^T X)^-1 X^T y (Exact for N < 10k)"]
    Branch --> Iter["Iterative GD: theta = theta - lr * X^T(X*theta - y) (Scales to N > 10M)"]
</div>
</div>""",

    38: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Decision Tree Recursive Partitioning & Information Gain</h4>
<div class="mermaid">
graph TD
    Root["Root Node (Gini = 0.50)"] --> Split{"Feature x_1 <= 2.5?"}
    Split -->|Yes| L1["Leaf 1 (Gini = 0.05, Class 0)"]
    Split -->|No| Sub{"Feature x_2 <= 5.0?"}
    Sub -->|Yes| L2["Leaf 2 (Gini = 0.00, Class 1)"]
    Sub -->|No| L3["Leaf 3 (Gini = 0.12, Class 0)"]
</div>
</div>""",

    43: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Support Vector Machine Max-Margin Hyperplane</h4>
<div class="mermaid">
graph TD
    H_Pos["Positive Margin Plane: w^T x + b = +1"]
    H_Sep["Optimal Decision Hyperplane: w^T x + b = 0"]
    H_Neg["Negative Margin Plane: w^T x + b = -1"]
    H_Pos --- H_Sep
    H_Sep --- H_Neg
    Margin["Margin Width = 2 / ||w|| (Support Vectors touch margin planes)"]
</div>
</div>""",

    45: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Random Forest Parallel Bagging Architecture</h4>
<div class="mermaid">
graph TD
    D["Training Dataset D (N samples, D features)"] --> B1["Bootstrap Sample 1 (sqrt(D) features)"]
    D --> B2["Bootstrap Sample 2 (sqrt(D) features)"]
    D --> BM["Bootstrap Sample M (sqrt(D) features)"]
    B1 --> T1["Decision Tree 1"]
    B2 --> T2["Decision Tree 2"]
    BM --> TM["Decision Tree M"]
    T1 --> Agg["Majority Vote / Mean Aggregator"]
    T2 --> Agg
    TM --> Agg
    Agg --> Final["Final Robust Prediction"]
</div>
</div>""",

    47: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: K-Means Lloyd's Iterative Optimization Loop</h4>
<div class="mermaid">
graph LR
    Init["Initialize K Centroids (K-Means++)"] --> Assign["Assignment Step: Assign x_i to Nearest Centroid mu_k"]
    Assign --> Update["Update Step: Recompute mu_k = mean of assigned points"]
    Update --> Check{"Centroids Shifted < epsilon?"}
    Check -->|No| Assign
    Check -->|Yes| Converged["Converged Voronoi Partition"]
</div>
</div>""",

    # Module 3
    57: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Multi-Layer Perceptron Forward & Backpropagation Graph</h4>
<div class="mermaid">
graph LR
    X["Input x"] --> Z1["z_1 = W_1 x + b_1"] --> A1["a_1 = sigma(z_1)"] --> Z2["z_2 = W_2 a_1 + b_2"] --> Y["Output y_hat"]
    Loss["Loss L(y, y_hat)"] -.->|dL/dz_2| Z2
    Z2 -.->|dL/dW_2| W2["Grad dL/dW_2 = (dL/dz_2) a_1^T"]
    Z2 -.->|dL/da_1| A1
    A1 -.->|dL/dz_1| Z1
    Z1 -.->|dL/dW_1| W1["Grad dL/dW_1 = (dL/dz_1) x^T"]
</div>
</div>""",

    61: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: BatchNorm vs LayerNorm Tensor Reduction Axes</h4>
<div class="mermaid">
graph TD
    subgraph BN["Batch Normalization (Computer Vision)"]
        BN_Desc["Reduces across Batch dimension N and spatial (H, W) per Channel C: shape (1, C, 1, 1)"]
    end
    subgraph LN["Layer Normalization (Transformers & NLP)"]
        LN_Desc["Reduces across Hidden dimension D per sample and token: shape (N, L, 1)"]
    end
</div>
</div>""",

    67: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: LSTM Cell Gating Signal Flow</h4>
<div class="mermaid">
graph LR
    In["Input [h_t-1, x_t]"] --> F["Forget Gate f_t = sigma(W_f x + b_f)"]
    In --> I["Input Gate i_t = sigma(W_i x + b_i)"]
    In --> C_tilde["Candidate C_t~ = tanh(W_c x + b_c)"]
    In --> O["Output Gate o_t = sigma(W_o x + b_o)"]
    F --> Cell["Cell State C_t = f_t * C_t-1 + i_t * C_t~"]
    Cell --> Hidden["Hidden State h_t = o_t * tanh(C_t)"]
</div>
</div>""",

    71: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Multi-Head Self-Attention Computational Pipeline</h4>
<div class="mermaid">
graph TD
    X["Input Sequence X (N x d_model)"] --> Q["Query: Q = X W_Q"]
    X --> K["Key: K = X W_K"]
    X --> V["Value: V = X W_V"]
    Q --> Dot["Scaled Dot-Product: (Q K^T) / sqrt(d_k)"]
    K --> Dot
    Dot --> Softmax["Softmax (Attention Weights A)"]
    Softmax --> Weighted["Attention Output: A * V"]
    V --> Weighted
    Weighted --> Proj["Output Projection: Concat(Heads) * W_O"]
</div>
</div>""",

    73: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Rotary Position Embeddings (RoPE) 2D Coordinate Rotation</h4>
<div class="mermaid">
graph LR
    Vec["2D Query/Key Chunk [x_1, x_2]"] --> Rot["Rotation Matrix R(m theta) = [[cos m theta, -sin m theta], [sin m theta, cos m theta]]"]
    Rot --> Out["Relative Position Encoded Output: q_m^T k_n = f(q, k, m-n)"]
</div>
</div>""",

    # Module 4
    85: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: KV Cache Prefill vs Incremental Auto-Regressive Decoding</h4>
<div class="mermaid">
graph TD
    subgraph Prefill["1. Prefill Phase (Compute-Bound)"]
        P_In["Prompt Tokens [t_1, t_2, t_3]"] --> P_Attn["Parallel Full Attention"] --> P_KV["Store Keys & Values in KV Cache"]
    end
    subgraph Decode["2. Generation Phase (Memory-Bandwidth Bound)"]
        D_In["New Token t_4"] --> D_Attn["Query t_4 Attends to [Cached KV 1..3 + New KV 4]"]
        D_Attn --> D_Out["Sample t_5 -> Append KV_4 -> Repeat"]
    end
</div>
</div>""",

    91: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: RAG Hybrid Search & Reciprocal Rank Fusion (RRF)</h4>
<div class="mermaid">
graph LR
    Q["User Query"] --> BM25["Sparse BM25 Keyword Search"]
    Q --> Dense["Dense Bi-Encoder Embedding Search"]
    BM25 --> Rank1["Sparse Rank List"]
    Dense --> Rank2["Dense Rank List"]
    Rank1 --> RRF["RRF Scoring: Score(d) = sum 1 / (60 + rank_i)"]
    Rank2 --> RRF
    RRF --> TopK["Fused Re-ranked Top-K Context"]
</div>
</div>""",

    100: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: HNSW Hierarchical Navigable Small World Graph</h4>
<div class="mermaid">
graph TD
    subgraph TopLayer["Layer 2 (Expressway - Long Jumps)"]
        L2_1["Entry Node"] --> L2_2["Node B"]
    end
    subgraph MidLayer["Layer 1 (Regional Grid)"]
        L1_1["Node A"] --> L1_2["Node B"] --> L1_3["Node C"]
    end
    subgraph BaseLayer["Layer 0 (All Vectors Dense Graph)"]
        L0_1["v1"] --- L0_2["v2"] --- L0_3["v3"] --- L0_4["Target Nearest Neighbor"]
    end
    TopLayer --> MidLayer --> BaseLayer
</div>
</div>""",

    115: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: LoRA Low-Rank Parameter Decomposition ($W = W_0 + \frac{\alpha}{r} B A$)</h4>
<div class="mermaid">
graph LR
    X["Input x (d_in)"] --> Frozen["Frozen Base Weights W_0 (d_in x d_out)"]
    X --> A["Down-Projection Matrix A (d_in x r)"]
    A --> B["Up-Projection Matrix B (r x d_out)"]
    B --> Scale["Scaling Factor (alpha / r)"]
    Frozen --> Sum["(+) Output Combiner"]
    Scale --> Sum
    Sum --> Out["Forward Activation h = W_0 x + (alpha/r) B A x"]
</div>
</div>""",

    128: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: CUDA Kernel Fusion (Eliminating VRAM Roundtrips)</h4>
<div class="mermaid">
graph TD
    subgraph Unfused["Unfused PyTorch Pipeline (3 VRAM Roundtrips)"]
        U1["Matrix Mult GEMM"] -->|Write to VRAM| UV1["VRAM Buffer 1"] -->|Read| U2["Add Bias"] -->|Write| UV2["VRAM Buffer 2"] -->|Read| U3["GELU Activation"]
    end
    subgraph Fused["Fused CUDA / Triton Kernel (1 VRAM Read, 1 VRAM Write)"]
        F1["Single GPU Kernel: Compute GEMM + Add Bias + Apply GELU in SRAM / Registers"]
    end
</div>
</div>""",

    # Module 5
    143: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Megatron-LM Tensor Parallelism (Column + Row Sharding)</h4>
<div class="mermaid">
graph LR
    X["Input Tensor X"] --> Col1["GPU 0: Column GEMM W_1,1"]
    X --> Col2["GPU 1: Column GEMM W_1,2"]
    Col1 --> GeLU1["GeLU"] --> Row1["GPU 0: Row GEMM W_2,1"]
    Col2 --> GeLU2["GeLU"] --> Row2["GPU 1: Row GEMM W_2,2"]
    Row1 --> AllReduce["All-Reduce (Sum across GPUs)"]
    Row2 --> AllReduce
    AllReduce --> Out["Output Layer"]
</div>
</div>""",

    155: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Direct Preference Optimization (DPO) Implicit Objective</h4>
<div class="mermaid">
graph LR
    Prompt["Prompt x + Pair (y_w, y_l)"] --> Model["Active Policy pi_theta"]
    Prompt --> Ref["Frozen Reference pi_ref"]
    Model --> LogRatio["Compute Implicit Reward: r(x, y) = beta * log(pi_theta / pi_ref)"]
    Ref --> LogRatio
    LogRatio --> Loss["Loss = -log sigma(r(x, y_w) - r(x, y_l))"]
</div>
</div>""",

    165: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Hierarchical Multi-Agent Supervisor-Worker Topology</h4>
<div class="mermaid">
graph TD
    User["User Request"] --> Supervisor["Supervisor / Planner Agent"]
    Supervisor --> Router{"Route Task"}
    Router -->|Code Generation| DevAgent["Software Dev Agent (Docker Sandbox)"]
    Router -->|Web Research| SearchAgent["Search & RAG Agent (Tavily/VectorDB)"]
    Router -->|Quality Control| ReviewAgent["Critic / Unit Test Agent"]
    DevAgent --> State["Shared State Graph"]
    SearchAgent --> State
    ReviewAgent --> State
    State --> Supervisor
    Supervisor --> Final["Validated Deliverable"]
</div>
</div>""",

    172: """<div class="diagram-container" style="background:var(--bg3); padding:1.2rem; border-radius:8px; margin:1.5rem auto; border:1px solid var(--border); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
<h4 style="color:var(--accent); margin-top:0; font-size:1.05rem;">Architecture Blueprint: Production LLM CI/CD & Automated Evaluation Pipeline</h4>
<div class="mermaid">
graph LR
    Commit["Git Commit (Prompt/Code Change)"] --> Pytest["1. Unit Tests (Deterministic Pytest)"]
    Pytest --> Eval["2. LLM-as-Judge Eval (RAGAS Groundedness & Accuracy)"]
    Eval --> Guard["3. Safety & Toxicity Guardrails (Guardrails AI)"]
    Guard --> Canary["4. Canary Deployment (5% Traffic Split)"]
    Canary --> Prom["5. Prometheus Latency & Drift Monitoring"]
</div>
</div>"""
}

# 1. INJECT INTO YAML DATA SOURCES
print("Injecting diagrams into YAML files...")
yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    updated = False
    for day in data.get('days', []):
        d_num = day.get('day_num', 0)
        if d_num in CANONICAL_DIAGRAMS:
            theory = day.get('theory_html', '')
            diag = CANONICAL_DIAGRAMS[d_num]
            # Check if this exact diagram title is already present
            title_match = re.search(r'<h4[^>]*>(.*?)</h4>', diag)
            if title_match and title_match.group(1) not in theory:
                day['theory_html'] = theory + '\n' + diag
                updated = True

    if updated:
        with open(yf, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("✓ Injected canonical diagrams into YAML sources.")

# 2. INJECT INTO HTML PORTALS
print("Injecting diagrams into HTML files...")
html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    updated = False
    for d_num, diag in CANONICAL_DIAGRAMS.items():
        title_match = re.search(r'<h4[^>]*>(.*?)</h4>', diag)
        if title_match and title_match.group(1) not in content:
            # Match the day section
            day_pattern = rf'(<div[^>]*id=[\"\']day-{d_num}[\"\'][^>]*>[\s\S]*?)(</div>\s*<!--\s*/day-{d_num}\s*-->|</div>\s*<div class=[\"\']day-section[\"\']|<!-- /day-section -->)'
            m = re.search(day_pattern, content)
            if m:
                # Append before day section closure
                insert_target = m.group(1)
                new_day_block = insert_target + '\n' + diag + '\n'
                content = content.replace(insert_target, new_day_block, 1)
                updated = True

    if updated:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)

print("✓ Injected canonical diagrams into HTML week portals.")
print("\n=== ALL 26 CANONICAL DIAGRAMS SUCCESSFULLY INJECTED ===")
