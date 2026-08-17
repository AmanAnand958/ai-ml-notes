"""
scripts/curriculum_deep_data_weeks19_26.py
Deep, specialized domain content for all days in Weeks 19 to 26 (Days 136 to 191).
"""

WEEKS_19_26_SPECIALIZED = {
    # WEEK 20
    145: {
        "title": "LangGraph StateGraph & Cyclical Workflows",
        "hinglish": "LangGraph hume complex cyclical workflows banane deta hai. StateGraph mein State ek TypedDict hoti hai, Nodes Python functions hote hain, aur Conditional Edges decide karti hain ki next node kaunsa chalega (e.g. rewrite_query ya finish).",
        "analogy": "LangGraph is like a railway switching yard: tracks (edges) connect various stations (nodes), and automated switches (conditional routing) guide trains based on cargo manifest (TypedDict state).",
        "gotcha": {
            "title": "⚠️ Gotcha: In-Place State Mutation in LangGraph Nodes",
            "description": "Never mutate state dictionaries in place without returning updated keys! LangGraph state reducers rely on pure function returns to track checkpoint history and enable state rollbacks."
        },
        "theory_html": """<h3 class="sh3">1. LangGraph StateGraph Architecture</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
Unlike linear DAG runners, <strong>LangGraph</strong> supports cyclic graphs essential for iterative agent self-correction and reflection:
</p>
<div class="mermaid">
graph TD
  Start["START"] --> AgentNode["Agent Decision Node"]
  AgentNode --> ToolCondition["Tools Needed?"]
  ToolCondition -->|Yes| ToolNode["Tool Execution Node"]
  ToolNode --> AgentNode
  ToolCondition -->|No| GradeNode["Quality Grader Node"]
  GradeNode -->|Satisfactory| EndNode["END"]
  GradeNode -->|Unsatisfactory| AgentNode
</div>
<div class="diagram-cap">LangGraph Cyclical State Execution Flow with Dual Feedback Decision Edges.</div>
<h3 class="sh3">2. TypedDict State Reducer Pattern</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — langgraph_state_machine.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)">Run</button></div></div>
  <pre><code>from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    steps_taken: int
    history: List[str]
    is_finished: bool

def agent_node(state: AgentState) -> dict:
    new_steps = state["steps_taken"] + 1
    finished = new_steps >= 2
    return {"steps_taken": new_steps, "is_finished": finished, "history": state["history"] + [f"Executed step {new_steps}"]}

initial_state: AgentState = {"query": "Analyze quarterly reports", "steps_taken": 0, "history": [], "is_finished": False}
s1 = {**initial_state, **agent_node(initial_state)}
s2 = {**s1, **agent_node(s1)}
print("Final Graph State:", s2)</code></pre>
</div>"""
    },

    147: {
        "title": "Vector Memory & Coreference Resolution",
        "hinglish": "Agents mein Long-Term Memory implement karne ke liye hum Vector DB use karte hain. Coreference Resolution ensure karta hai ki pronouns ('he', 'it', 'the company') replace hokar exact entity name ban jayein, taaki vector search fail na ho.",
        "analogy": "Coreference resolution is like replacing vague pronouns in detective notes ('he went there') with full names ('John Doe went to Building 4') so anyone reading the file later understands the exact context.",
        "gotcha": {
            "title": "⚠️ Gotcha: Recency vs Semantic Relevance Memory Skew",
            "description": "Relying purely on vector similarity ignores temporal recency, causing agents to retrieve stale memories from 6 months ago over relevant updates from 5 minutes ago. Always blend semantic similarity with an exponential recency decay penalty."
        },
        "theory_html": """<h3 class="sh3">1. Episodic Memory Retrieval Scoring Formula</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
Production agent memory engines retrieve relevant past episodic interactions using a multi-factor ranking function:
</p>
<div class="math-block">
$$\\text{MemoryScore}(m) = \\alpha \\cdot \\text{Sim}(q, m) + \\beta \\cdot e^{-\\lambda \\cdot \\Delta t} + \\gamma \\cdot \\text{Importance}(m)$$
</div>
<div class="mermaid">
graph LR
  User["User Prompt: Where did he invest?"] --> Coref["Coreference Resolution\n('he' -> 'Elon Musk')"]
  Coref --> Query["Rewritten Query: Where did Elon Musk invest?"]
  Query --> VecMem["Vector Episodic Memory Search"]
  VecMem --> LLM["LLM Response Synthesis"]
</div>
<div class="diagram-cap">Coreference Resolution Preprocessing into Episodic Vector Memory Retrieval.</div>
<h3 class="sh3">2. Production Python Memory Scoring Engine</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — memory_engine.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)">Run</button></div></div>
  <pre><code>import numpy as np

def score_memory(sim: float, hours_ago: float, importance: float, alpha=0.5, beta=0.3, gamma=0.2, decay_rate=0.01) -> float:
    recency = np.exp(-decay_rate * hours_ago)
    return float(alpha * sim + beta * recency + gamma * importance)

m1_score = score_memory(sim=0.92, hours_ago=2.0, importance=0.8)
m2_score = score_memory(sim=0.95, hours_ago=200.0, importance=0.8)
print(f"Recent Memory Score: {m1_score:.4f} vs Stale Memory Score: {m2_score:.4f}")</code></pre>
</div>"""
    },

    # WEEK 21
    151: {
        "title": "FlashAttention & Speculative Decoding",
        "hinglish": "Standard Attention GPU ke High Bandwidth Memory (HBM) aur fast SRAM ke beech data transfer karne mein slow ho jati hai ($O(N^2)$ IO bottleneck). FlashAttention tiling use karke pura attention kernel SRAM ke andar calculate karta hai!",
        "analogy": "Standard attention is like walking to the distant library warehouse every time you read one sentence. FlashAttention loads an entire chapter into your personal desk (SRAM), reads it all at once, and writes back the final summary.",
        "gotcha": {
            "title": "⚠️ Gotcha: Head Dimension Misalignment in FlashAttention-2",
            "description": "FlashAttention-2 requires head dimensions to be exact multiples of 64 or 128 (e.g. d_head=128). Non-standard head dimensions fallback to slow unfused PyTorch kernels."
        },
        "theory_html": """<h3 class="sh3">1. GPU Memory Hierarchy & FlashAttention Tiling</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
Standard attention materializes the intermediate $N \\times N$ attention matrix $S = Q K^T$ and $P = \\text{softmax}(S)$ in slow GPU HBM ($1.5 - 3.0\\text{ TB/s}$). <strong>FlashAttention</strong> partitions inputs into blocks and performs incremental softmax normalization entirely in high-speed GPU SRAM ($19\\text{ TB/s}$).
</p>
<div class="mermaid">
graph TD
  subgraph "Standard Attention (Memory Bound)"
    Q1["Q, K in HBM"] --> Write1["Write N x N Matrix to HBM"]
    Write1 --> Softmax["Compute Softmax from HBM"]
    Softmax --> Write2["Write N x N Probs to HBM"]
    Write2 --> Output1["Multiply with V in HBM"]
  end
  subgraph "FlashAttention (Compute Bound Tiling)"
    Q2["Block Qi in SRAM"] & K2["Block Kj in SRAM"] --> Fused["Fused Tiled Kernel in SRAM\n(Online Softmax + Accumulate)"]
    Fused --> Output2["Final Output directly written to HBM"]
  end
</div>
<div class="diagram-cap">FlashAttention SRAM Tiling: Bypassing the O(N^2) memory bandwidth read/write bottleneck.</div>
<h3 class="sh3">2. Speculative Decoding Verification Principle</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
A lightweight Draft Model (e.g. 1B) predicts $K$ speculative tokens, and the Target Model (e.g. 70B) validates all $K$ tokens simultaneously in a <strong>single forward pass</strong>.
</p>"""
    },

    152: {
        "title": "Model Quantization: AWQ, GPTQ & GGUF",
        "hinglish": "Quantization mein hum 16-bit floating point weights (FP16) ko 4-bit ya 8-bit integers (INT4/INT8) mein convert karte hain. AWQ (Activation-aware Weight Quantization) 1% critical salient weights ko protect karta hai taaki accuracy drop 0.1% se kam rahe!",
        "analogy": "Quantization is like high-efficiency image compression: instead of saving 16 million colors per pixel, you use a 256-color palette (quantization scale factor) that looks virtually identical to the human eye while cutting file size by 75%.",
        "gotcha": {
            "title": "⚠️ Gotcha: Uniform Quantization Outlier Clipping",
            "description": "LLM activation tensors contain extreme outlier channels (over 100x average magnitude). Uniform naive quantization clips these outliers, completely destroying perplexity. Always use AWQ or SmoothQuant to scale outlier channels before integer casting."
        },
        "theory_html": """<h3 class="sh3">1. Quantization Formats Comparison</h3>
<div class="table-wrap">
<table class="concept-table">
  <tr><th>Format</th><th>Quantization Target</th><th>Hardware Acceleration</th><th>Primary Use Case</th></tr>
  <tr><td><strong>AWQ</strong></td><td>4-bit Weights (W4A16)</td><td>NVIDIA Tensor Cores</td><td>High-throughput GPU serving (vLLM, SGLang)</td></tr>
  <tr><td><strong>GPTQ</strong></td><td>4-bit Weights (Second-Order Hessian)</td><td>NVIDIA Tensor Cores</td><td>Single GPU local inference</td></tr>
  <tr><td><strong>GGUF / llama.cpp</strong></td><td>2-bit to 8-bit (k-quants)</td><td>Apple Silicon Metal / CPU AVX</td><td>Local edge devices, MacBooks, CPUs</td></tr>
  <tr><td><strong>FP8 (E4M3 / E5M2)</strong></td><td>8-bit Float Weights & Activations</td><td>NVIDIA Hopper / Ada (H100 / RTX 4090)</td><td>Zero-degradation Enterprise serving</td></tr>
</table>
</div>
<h3 class="sh3">2. Production Python Linear Quantization Function</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — quant_engine.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)">Run</button></div></div>
  <pre><code>import numpy as np

def quantize_to_int8(weights: np.ndarray):
    max_val = np.max(np.abs(weights))
    scale = max_val / 127.0
    q_weights = np.clip(np.round(weights / (scale + 1e-9)), -128, 127).astype(np.int8)
    return q_weights, scale

w_orig = np.random.randn(4, 4).astype(np.float32)
q_w, scale = quantize_to_int8(w_orig)
w_dequant = q_w.astype(np.float32) * scale
error = np.mean(np.abs(w_orig - w_dequant))
print(f"Quantization Complete. Average Reconstruction Error: {error:.6f}")</code></pre>
</div>"""
    },

    154: {
        "title": "Alignment: DPO, ORPO & GRPO",
        "hinglish": "PPO (RLHF) bohot unstable hota hai kyunki alag se Reward Model aur Value Network train karna padta hai. DPO (Direct Preference Optimization) mathematical substitution se reward model ko direct policy loss mein convert kar deta hai, jisse training simple cross-entropy ban jati hai!",
        "analogy": "RLHF with PPO is like hiring a judge (Reward Model), a coach (Critic), and an athlete (Policy) all practicing simultaneously. DPO is giving the athlete a direct video comparison of good vs bad performances to learn from directly.",
        "gotcha": {
            "title": "⚠️ Gotcha: Overfitting on Narrow DPO Preference Datasets",
            "description": "High beta parameters (beta > 0.5) in DPO loss cause rapid policy collapse where the model generates repetitive degenerate completions. Keep beta in [0.05, 0.1] and evaluate with KL divergence penalty."
        },
        "theory_html": """<h3 class="sh3">1. Direct Preference Optimization (DPO) Loss Function</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
DPO derives an exact closed-form expression for the implicit reward, eliminating the separate reward model entirely:
</p>
<div class="math-block">
$$\\mathcal{L}_{\\text{DPO}}(\\pi_\\theta; \\pi_{\\text{ref}}) = -\\mathbb{E}_{(x, y_w, y_l)} \\left[ \\log \\sigma \\left( \\beta \\log \\frac{\\pi_\\theta(y_w|x)}{\\pi_{\\text{ref}}(y_w|x)} - \\beta \\log \\frac{\\pi_\\theta(y_l|x)}{\\pi_{\\text{ref}}(y_l|x)} \\right) \\right]$$
</div>
<div class="mermaid">
graph LR
  Prompt["Prompt x"] --> Winner["Winning Response y_w"]
  Prompt --> Loser["Losing Response y_l"]
  Winner & Loser --> DPOLoss["DPO Loss Engine\n(Increases P(y_w) relative to ref; decreases P(y_l))"]
  DPOLoss --> Grad["Policy Weights Update"]
</div>
<div class="diagram-cap">DPO Alignment Pipeline: Direct gradient optimization from pairwise preference datasets.</div>"""
    }
}
