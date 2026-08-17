#!/usr/bin/env python3
"""
scripts/inject_all_missing_diagrams.py
Injects rich, clean Mermaid.js and SVG diagrams across all identified high-priority days:
- Classical ML (KNN, Bias-Variance, XGBoost, SHAP)
- Computer Vision (Max-Pooling, ResNet, YOLO, U-Net)
- NLP & Transformers (RNN Unrolling, BPE, BERT DeBERTa)
- Serving & Distributed ML (Prometheus, vLLM PagedAttention, Triton, Ring-AllReduce, 1F1B, ZeRO-1/2/3)
- RLHF & Agents (PPO, RLHF Pipeline, ReAct Cycles, LangGraph State Machines)
"""

import glob, yaml, re, os, json, html

print("=== STARTING COMPREHENSIVE ARCHITECTURAL DIAGRAM INJECTIONS ===")

# Master Dictionary of Diagrams to Inject: Key is (week_num, day_num)
DIAGRAM_MAP = {
    # 1. Day 36 (Week 5): KNN & Naive Bayes
    (5, 36): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>KNN Voronoi Space vs Naive Bayes Decision Probability:</strong></p>
<div class="mermaid">
graph LR
    subgraph KNN_Spatial["KNN Spatial Metric"]
        Q["Query Point x"] --> D1["Euclidean Distance: d(x, x_i)"]
        D1 --> K_sort["Sort & Pick K-Nearest Neighbors"]
        K_sort --> Maj["Majority Vote / Weighted Average"]
    end
    subgraph NB_Prob["Naive Bayes Probability"]
        X_feat["Features: x1, x2, ..., xn"] --> Cond["Conditional Independence: P(x|C) = prod P(x_i|C)"]
        Cond --> Bayes["Bayes Theorem: P(C|x) propto P(C) * P(x|C)"]
        Bayes --> Argmax["arg max_C P(C|x)"]
    end
</div>
</div>\n''',

    # 2. Day 39 (Week 6): Bias-Variance Tradeoff
    (6, 39): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Bias–Variance Decomposition & Error Dynamics:</strong></p>
<div class="mermaid">
graph TD
    Complexity["Model Complexity / Polynomial Degree"] --> Under["Low Complexity: High Bias (Underfitting)"]
    Complexity --> Opt["Optimal Capacity: Minimal Generalization Error"]
    Complexity --> Over["High Complexity: High Variance (Overfitting)"]
    
    subgraph Total_Error["Total Expected Test Error"]
        Bias["Bias^2 (Systematic Assumptions)"] --> Sum["Total Error = Bias^2 + Variance + Irreducible Noise sigma^2"]
        Var["Variance (Sensitivity to Training Set)"] --> Sum
        Noise["Irreducible Noise sigma^2"] --> Sum
    end
</div>
</div>\n''',

    # 3. Day 48 (Week 7): Gradient Boosting & XGBoost
    (7, 48): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Gradient Boosting (GBDT / XGBoost) Sequential Residual Learning:</strong></p>
<div class="mermaid">
graph LR
    Data["Dataset (X, y)"] --> M0["F_0(x) = Base Mean"]
    M0 --> R1["Compute Pseudo-Residuals: r_1 = y - F_0(x)"]
    R1 --> T1["Fit Tree h_1(x) on Residuals r_1"]
    T1 --> M1["F_1(x) = F_0(x) + eta * h_1(x)"]
    M1 --> R2["Compute Residuals: r_2 = y - F_1(x)"]
    R2 --> T2["Fit Tree h_2(x) on r_2"]
    T2 --> Final["Final Ensemble: F_M(x) = F_0 + sum(eta * h_m(x))"]
</div>
</div>\n''',

    # 4. Day 50 (Week 7): SHAP Values
    (7, 50): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>SHAP (Shapley Additive Explanations) Feature Attribution:</strong></p>
<div class="mermaid">
graph LR
    Base["Base Value E[f(x)]"] --> F1["Feature 1: +0.42 (Push Up)"]
    F1 --> F2["Feature 2: -0.18 (Push Down)"]
    F2 --> F3["Feature 3: +0.31 (Push Up)"]
    F3 --> Pred["Final Model Prediction f(x) = E[f(x)] + sum(phi_i)"]
</div>
</div>\n''',

    # 5. Day 60 (Week 9): Max Pooling
    (9, 60): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Max-Pooling 2x2 Downsampling Operation (Stride = 2):</strong></p>
<div class="mermaid">
graph TD
    subgraph Input_4x4["Input Feature Map 4x4"]
        A["[12, 20, 30, 0]"]
        B["[8,  15, 1,  4]"]
        C["[10, 5,  18, 2]"]
        D["[3,  9,  4,  6]"]
    end
    subgraph Pool_Op["Max Pooling (2x2, s=2)"]
        TopL["max(12,20,8,15) = 20"]
        TopR["max(30,0,1,4) = 30"]
        BotL["max(10,5,3,9) = 10"]
        BotR["max(18,2,4,6) = 18"]
    end
    Input_4x4 --> Pool_Op --> Out_2x2["Output Feature Map 2x2: [[20, 30], [10, 18]]"]
</div>
</div>\n''',

    # 6. Day 62 (Week 9): ResNet Skip Connections
    (9, 62): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>ResNet Residual Block Identity Skip Connection:</strong></p>
<div class="mermaid">
graph TD
    X["Input x"] --> Weight1["Weight Layer (Conv 3x3 + BN)"]
    X --> Identity["Identity Shortcut: Identity(x)"]
    Weight1 --> ReLU1["ReLU Activation"]
    ReLU1 --> Weight2["Weight Layer (Conv 3x3 + BN)"]
    Weight2 --> Add["Element-wise Addition (+)"]
    Identity --> Add
    Add --> Out["Output: H(x) = F(x) + x -> ReLU(H(x))"]
</div>
</div>\n''',

    # 7. Day 63 (Week 9): YOLO Object Detection
    (9, 63): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>YOLO Single-Stage Grid Detection & NMS Pipeline:</strong></p>
<div class="mermaid">
graph LR
    Img["Input Image (416x416x3)"] --> CNN["Backbone (CSPDarkNet)"]
    CNN --> Grid["Grid Split (S x S)"]
    Grid --> BBox["B Bounding Boxes (x, y, w, h, conf) + C Class Probs per cell"]
    BBox --> IOU["IoU Filtering (Threshold > 0.5)"]
    IOU --> NMS["Non-Maximum Suppression (NMS)"]
    NMS --> Detections["Final Bounding Box Detections"]
</div>
</div>\n''',

    # 8. Day 64 (Week 9): U-Net Architecture
    (9, 64): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>U-Net Segmentation Encoder-Decoder Architecture with Skip Concatenations:</strong></p>
<div class="mermaid">
graph LR
    subgraph Encoder["Contracting Path (Encoder)"]
        E1["Input Image (572x572)"] --> E2["Conv 3x3 + MaxPool"]
        E2 --> E3["Conv 3x3 + MaxPool"]
        E3 --> E4["Bottleneck Latent Features"]
    end
    subgraph Decoder["Expanding Path (Decoder)"]
        E4 --> D1["Up-Conv 2x2"]
        D1 --> D2["Up-Conv 2x2"]
        D2 --> D3["Final Conv 1x1 -> Segmentation Mask"]
    end
    E1 -.->|High-Res Skip Connection| D3
    E2 -.->|Spatial Skip Connection| D2
    E3 -.->|Feature Skip Connection| D1
</div>
</div>\n''',

    # 9. Day 66 (Week 10): RNN Unrolling & BPTT
    (10, 66): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>RNN Temporal Unrolling & Backpropagation Through Time (BPTT):</strong></p>
<div class="mermaid">
graph LR
    subgraph Step_t0["t = 0"]
        x0["x_0"] --> h0["h_0 = tanh(W_hh * 0 + W_xh * x_0)"]
        h0 --> y0["y_0 = Softmax(W_hy * h_0)"]
    end
    subgraph Step_t1["t = 1"]
        x1["x_1"] --> h1["h_1 = tanh(W_hh * h_0 + W_xh * x_1)"]
        h1 --> y1["y_1 = Softmax(W_hy * h_1)"]
    end
    subgraph Step_t2["t = 2"]
        x2["x_2"] --> h2["h_2 = tanh(W_hh * h_1 + W_xh * x_2)"]
        h2 --> y2["y_2 = Softmax(W_hy * h_2)"]
    end
    h0 -->|W_hh recurrent weight| h1
    h1 -->|W_hh recurrent weight| h2
</div>
</div>\n''',

    # 10. Day 87 (Week 13): BPE Subword Merge Tree
    (13, 87): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Byte-Pair Encoding (BPE) Subword Merge Tree:</strong></p>
<div class="mermaid">
graph TD
    Raw["Raw Text: 'lower', 'lowest', 'newer', 'wider'"] --> Chars["Initial Character Vocab: {l, o, w, e, r, s, t, n, d}"]
    Chars --> M1["Merge 1: ('e', 'r') -> 'er'"]
    M1 --> M2["Merge 2: ('e', 's') -> 'es'"]
    M2 --> M3["Merge 3: ('es', 't') -> 'est'"]
    M3 --> M4["Merge 4: ('l', 'o') -> 'lo'"]
    M4 --> M5["Merge 5: ('lo', 'w') -> 'low'"]
    M5 --> Subwords["Final Subwords: {'low', 'er', 'est', 'new', 'wid'}"]
</div>
</div>\n''',

    # 11. Day 122 (Week 18): Prometheus Monitoring Pipeline
    (18, 122): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Prometheus & Grafana ML Inference Observability Pipeline:</strong></p>
<div class="mermaid">
graph LR
    ModelServer["FastAPI / Triton GPU Pods"] -->|Expose /metrics endpoint| Exporter["Prometheus Metrics Exporter"]
    Exporter -->|Pull scrape every 15s| Prom["Prometheus Server (TSDB)"]
    Prom --> Grafana["Grafana Dashboard (p99 Latency, GPU VRAM, Throughput)"]
    Prom --> Alertmanager["Alertmanager (Slack / PagerDuty on GPU OOM or SLA breach)"]
</div>
</div>\n''',

    # 12. Day 127 (Week 19): vLLM PagedAttention
    (19, 127): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>vLLM PagedAttention Virtual-to-Physical Block Table Translation:</strong></p>
<div class="mermaid">
graph LR
    subgraph Logical_Context["Logical Token Space"]
        L1["Seq A: Tokens 0-15 (Block 0)"]
        L2["Seq A: Tokens 16-31 (Block 1)"]
    end
    subgraph Block_Table["Virtual Block Table"]
        BT1["Block 0 -> Physical Page #7"]
        BT2["Block 1 -> Physical Page #2"]
    end
    subgraph GPU_RAM["Non-Contiguous GPU Memory Pool"]
        P2["Physical Page #2 (VRAM)"]
        P7["Physical Page #7 (VRAM)"]
    end
    L1 --> BT1 --> P7
    L2 --> BT2 --> P2
</div>
</div>\n''',

    # 13. Day 132 (Week 19): Triton Dynamic Batching
    (19, 132): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Triton Inference Server Dynamic Batching & Queue Scheduler:</strong></p>
<div class="mermaid">
graph TD
    R1["Request 1 (t=0ms)"] --> Queue["Dynamic Priority Queue"]
    R2["Request 2 (t=2ms)"] --> Queue
    R3["Request 3 (t=4ms)"] --> Queue
    Queue --> Timer{"max_queue_delay_us OR max_batch_size reached?"}
    Timer -->|Yes| FormBatch["Form Batched Tensor (B=3)"]
    FormBatch --> Engine["TensorRT / PyTorch Backend (Single Forward Pass)"]
    Engine --> Demux["Split Responses & Return to Clients"]
</div>
</div>\n''',

    # 14. Day 142 (Week 21): DDP Ring-AllReduce
    (21, 142): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>PyTorch DDP Ring-AllReduce Inter-GPU Communication Topology:</strong></p>
<div class="mermaid">
graph LR
    GPU0["GPU 0"] -->|Send chunk / Receive chunk| GPU1["GPU 1"]
    GPU1 -->|Send chunk / Receive chunk| GPU2["GPU 2"]
    GPU2 -->|Send chunk / Receive chunk| GPU3["GPU 3"]
    GPU3 -->|Send chunk / Receive chunk| GPU0
</div>
</div>\n''',

    # 15. Day 144 (Week 21): Pipeline Parallelism 1F1B
    (21, 144): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>Pipeline Parallelism 1F1B (One-Forward-One-Backward) Schedule:</strong></p>
<div class="mermaid">
graph LR
    subgraph Stage_0["GPU 0 (Layers 1-8)"]
        F0["F1 -> F2 -> F3 -> F4"] --> B0["B1 -> B2 -> B3 -> B4"]
    end
    subgraph Stage_1["GPU 1 (Layers 9-16)"]
        F1["F1 -> F2 -> F3 -> F4"] --> B1["B1 -> B2 -> B3 -> B4"]
    end
    subgraph Stage_2["GPU 2 (Layers 17-24)"]
        F2["F1 -> F2 -> F3 -> F4"] --> B2["B1 -> B2 -> B3 -> B4"]
    end
    F0 --> F1 --> F2 --> B2 --> B1 --> B0
</div>
</div>\n''',

    # 16. Day 146 (Week 21): DeepSpeed ZeRO-1/2/3
    (21, 146): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>DeepSpeed ZeRO-1, ZeRO-2, ZeRO-3 Memory Sharding Hierarchy:</strong></p>
<div class="mermaid">
graph TD
    ModelMemory["Total Model Memory (16x Model Size)"] --> ZeRO1["ZeRO-1: Shard Optimizer States P_os (4x Memory Reduction)"]
    ZeRO1 --> ZeRO2["ZeRO-2: Shard Optimizer States + Gradients P_os+g (8x Reduction)"]
    ZeRO2 --> ZeRO3["ZeRO-3: Shard Optimizer + Gradients + Model Parameters P_os+g+p (Linear Memory Scaling with GPUs)"]
</div>
</div>\n''',

    # 17. Day 151 (Week 22): PPO Actor-Critic
    (22, 151): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>PPO (Proximal Policy Optimization) Clipped Surrogate Loss Dynamics:</strong></p>
<div class="mermaid">
graph TD
    State["Prompt Context x"] --> Policy["Actor Policy pi_theta(y|x)"]
    Policy --> Action["Generated Output y"]
    Action --> Critic["Critic Value Model V_phi(x)"]
    Action --> Reward["Reward Model R(x, y)"]
    Reward --> GAE["Generalized Advantage Estimation A_t"]
    GAE --> Loss["Clipped Objective: min(r_t * A_t, clip(r_t, 1-eps, 1+eps) * A_t)"]
</div>
</div>\n''',

    # 18. Day 153 (Week 22): RLHF 3-Stage Pipeline
    (22, 153): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>RLHF 3-Stage End-to-End Alignment Pipeline:</strong></p>
<div class="mermaid">
graph LR
    Pretrain["Pretrained Base LLM"] --> SFT["Stage 1: Supervised Fine-Tuning (SFT)"]
    SFT --> Preference["Human Preference Pairs (Winner y_w, Loser y_l)"]
    Preference --> RM["Stage 2: Reward Model Training (Bradley-Terry Loss)"]
    RM --> PPO_RL["Stage 3: RL Policy Optimization (PPO / DPO)"]
    PPO_RL --> Aligned["Aligned Helpful & Harmless Production Model"]
</div>
</div>\n''',

    # 19. Day 161 (Week 23): ReAct Agent Cycle
    (23, 161): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>ReAct (Reason + Act) Autonomous Agent Cycle:</strong></p>
<div class="mermaid">
graph TD
    UserQuery["User Goal / Query"] --> Thought["Thought: Analyze state and reason next step"]
    Thought --> Action["Action: Select Tool & Format JSON parameters"]
    Action --> Tool["Execute Tool (Search / SQL / Shell / Python)"]
    Tool --> Observation["Observation: Tool Output / Return Value"]
    Observation --> Condition{"Task Complete?"}
    Condition -->|No| Thought
    Condition -->|Yes| FinalAnswer["Final Answer to User"]
</div>
</div>\n''',

    # 20. Day 163 (Week 23): LangGraph State Machine
    (23, 163): '''\n<div class="diagram-container" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; border:1px solid var(--border);">
<p><strong>LangGraph Stateful Multi-Agent Reducer & Conditional Graph:</strong></p>
<div class="mermaid">
graph LR
    Start["__start__"] --> Agent["Agent Node (LLM Decision)"]
    Agent --> Router{"Should Call Tools?"}
    Router -->|Yes| ToolNode["Tool Execution Node"]
    Router -->|No| EndNode["__end__"]
    ToolNode --> StateReducer["Update Shared State (AgentState Reducer)"]
    StateReducer --> Agent
</div>
</div>\n'''
}

# -------------------------------------------------------------
# 1. INJECT INTO YAML FILES
# -------------------------------------------------------------
print("Injecting diagrams into YAML files...")
for (w_num, d_num), diag_html in DIAGRAM_MAP.items():
    yf = f"src/data/week{w_num:02d}.yaml"
    if not os.path.exists(yf):
        continue
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        if d.get('day_num') == d_num:
            current_th = d.get('theory_html', '')
            if '<div class="mermaid">' not in current_th:
                d['theory_html'] = diag_html + current_th
    with open(yf, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

print("✓ Injected all diagrams into YAML sources.")

# -------------------------------------------------------------
# 2. SYNC INTO HTML FILES
# -------------------------------------------------------------
print("Injecting diagrams into HTML week portals...")
for (w_num, d_num), diag_html in DIAGRAM_MAP.items():
    hf = f"pages/weeks/week{w_num}.html"
    if not os.path.exists(hf):
        continue
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # If day does not already have this mermaid block
    if f'id="day-{d_num}"' in content and diag_html.strip()[:40] not in content:
        day_pattern = rf'(<div class="day-section[^"]*" id="day-{d_num}".*?<div class="theory-content">)'
        match = re.search(day_pattern, content, re.DOTALL)
        if match:
            content = content[:match.end()] + "\n" + diag_html + content[match.end():]
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(content)

print("✓ Injected all diagrams into HTML files.")
print("\n=== DIAGRAM INJECTIONS COMPLETE ===")
