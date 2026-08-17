# scripts/theory_deep_w21_w22.py
# Deep theory for all 14 days in Weeks 21 and 22

W21_W22_THEORY = {
    # ── DAY 150: vLLM & PagedAttention ──
    150: r"""<h3 class="sh3">1. GPU VRAM Memory Bottlenecks in LLM Serving</h3>
<p>
Serving large language models in production requires managing three distinct memory components:
</p>
<ol>
  <li><strong>Model Weights ($M_{\text{weights}}$):</strong> Fixed footprint ($P \times \text{bytes\_per\_param}$). A 70B parameter model in FP16 requires $70 \times 2\text{GB} = 140\text{GB}$ VRAM.</li>
  <li><strong>Activation Memory:</strong> Intermediate tensor activations during forward passes.</li>
  <li><strong>Key-Value (KV) Cache ($M_{\text{KV}}$):</strong> Dynamically grows with batch size and context length. For multi-head attention:
    <div class="math-block">
    $$M_{\text{KV}} = 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{bytes} \times B \times S$$
    </div>
  </li>
</ol>
<p>
In legacy serving engines, KV cache tensors were pre-allocated contiguously for the maximum sequence length (e.g. $S = 4096$). This led to massive <strong>internal memory fragmentation</strong> ($60\text{--}80\%$ of GPU VRAM wasted on unused reserved slots) and limited concurrency.
</p>

<h3 class="sh3">2. PagedAttention Architecture: Virtual Memory for KV Cache</h3>
<p>
Developed by Kwon et al. (UC Berkeley / vLLM), <strong>PagedAttention</strong> draws inspiration from operating system virtual memory paging:
</p>
<div class="mermaid">
graph TD
    LogicalTokens["Logical Sequence Tokens (0 to 63)"] --> PageTable["Block Table / Page Directory\nMaps Logical Blocks -> Physical Blocks"]
    PageTable --> Block0["Physical Block 7 (SRAM/HBM: Tokens 0-15)"]
    PageTable --> Block1["Physical Block 23 (Non-contiguous: Tokens 16-31)"]
    PageTable --> Block2["Physical Block 12 (Non-contiguous: Tokens 32-47)"]
    PageTable --> Block3["Physical Block 89 (Non-contiguous: Tokens 48-63)"]
</div>
<div class="diagram-cap">Figure 150.1: PagedAttention virtual block tables allocating non-contiguous physical GPU VRAM pages.</div>
<p>
By partitioning the KV cache into fixed-size physical blocks (e.g. 16 or 32 tokens per block), vLLM achieves:
</p>
<ul>
  <li><strong>Near-Zero Memory Waste:</strong> Reduces VRAM fragmentation to &lt;4%, allowing <strong>2x - 4x larger concurrent batch sizes</strong>.</li>
  <li><strong>Copy-on-Write Memory Sharing:</strong> Enables parallel speculative decoding and tree search without duplicating prompt KV cache in memory.</li>
</ul>""",

    # ── DAY 151: FlashAttention & Speculative Decoding ──
    151: r"""<h3 class="sh3">1. The Memory Bandwidth Bottleneck: Standard Attention</h3>
<p>
Standard Multi-Head Attention computes the attention matrix:
</p>
<div class="math-block">
$$\mathbf{A} = \text{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}$$
</div>
<p>
On modern GPUs (e.g. NVIDIA A100 / H100), compute throughput (Tensor Cores: 312 TFLOPS) is orders of magnitude faster than High-Bandwidth Memory (HBM) read/write bandwidth (2.0 TB/s). In standard PyTorch attention, the intermediate $N \times N$ attention matrix must be materialized in HBM, read into on-chip SRAM for softmax, written back to HBM, and read again for multiplication with $\mathbf{V}$. This causes an <strong>$O(N^2)$ IO memory bandwidth bottleneck</strong>.
</p>

<h3 class="sh3">2. FlashAttention: Exact Attention with IO-Aware SRAM Tiling</h3>
<p>
<strong>FlashAttention</strong> (Tri Dao et al.) computes exact attention with zero memory footprint for the $N \times N$ matrix by tiling query, key, and value blocks directly inside ultra-fast on-chip <strong>SRAM (19 TB/s)</strong>:
</p>
<div class="mermaid">
graph LR
    HBM["GPU High-Bandwidth Memory (HBM: 2 TB/s)"] -->|Load Block Q_i, K_j (SRAM Tiling)| SRAM["Fast On-Chip SRAM (19 TB/s)"]
    SRAM -->|Online Softmax Scaling| Compute["Tensor Core Matmul: S_ij = Q_i K_j^T"]
    Compute -->|Accumulate Output Block O_i| SRAM
    SRAM -->|Write Final Output (O(N) IO)| HBM
</div>
<div class="diagram-cap">Figure 151.1: FlashAttention SRAM tiling and online softmax scaling eliminating HBM IO passes.</div>""",

    # ── DAY 152: Quantization ──
    152: r"""<h3 class="sh3">1. Post-Training Quantization (PTQ): AWQ vs GPTQ vs GGUF</h3>
<p>
Quantization compresses 16-bit floating-point weights (FP16/BF16) to lower bitwidths (INT8, INT4, INT2), slashing memory requirements and memory bandwidth bottlenecks during autoregressive decoding.
</p>
<ul>
  <li><strong>AWQ (Activation-aware Weight Quantization):</strong> Observes that not all weights are equally important; protecting the top 1% salient weight channels (based on activation magnitudes) allows 4-bit quantization with near-zero perplexity degradation.</li>
  <li><strong>GPTQ:</strong> Layer-by-layer second-order Taylor expansion (Optimal Brain Surgeon) minimizing mean squared error: $\arg\min_{\hat{\mathbf{W}}} \|\mathbf{W}\mathbf{X} - \hat{\mathbf{W}}\mathbf{X}\|_2^2$.</li>
  <li><strong>GGUF / llama.cpp:</strong> Binary format optimized for CPU and mixed CPU/GPU offloaded inference with non-uniform k-quants.</li>
</ul>

<h3 class="sh3">2. Quantization Mathematical Formulation</h3>
<div class="math-block">
$$X_{\text{quant}} = \text{clip}\left( \left\lfloor \frac{X}{\text{Scale}} \right\rceil + Z, -2^{b-1}, 2^{b-1}-1 \right)$$
</div>""",

    # ── DAY 153: QLoRA & PEFT ──
    153: r"""<h3 class="sh3">1. Low-Rank Adaptation (LoRA)</h3>
<p>
LoRA freezes the pre-trained weight matrix $\mathbf{W}_0 \in \mathbb{R}^{d \times k}$ and injects trainable low-rank decomposition matrices:
</p>
<div class="math-block">
$$\mathbf{W} = \mathbf{W}_0 + \frac{\alpha}{r} (\mathbf{B} \cdot \mathbf{A})$$
</div>
<p>
Where $\mathbf{A} \in \mathbb{R}^{r \times k} \sim \mathcal{N}(0, \sigma^2)$, $\mathbf{B} \in \mathbb{R}^{d \times r} = 0$, and rank $r \in \{8, 16, 32\}$.
</p>

<h3 class="sh3">2. QLoRA: 4-Bit NormalFloat (NF4)</h3>
<p>
QLoRA fine-tunes 70B parameter models on a single 48GB GPU by combining:
</p>
<ul>
  <li><strong>NF4 Quantization:</strong> Information-theoretically optimal for normal distributions.</li>
  <li><strong>Double Quantization (DQ):</strong> Quantizes scale constants, saving 0.37 bits/param.</li>
  <li><strong>Paged Optimizers:</strong> Pages memory to CPU RAM during activation spikes.</li>
</ul>""",

    # ── DAY 154: DPO, ORPO & GRPO ──
    154: r"""<h3 class="sh3">1. Direct Preference Optimization (DPO)</h3>
<p>
DPO aligns language models directly on pairwise human preferences without training a separate reward model or tuning unstable PPO actor-critic loops:
</p>
<div class="math-block">
$$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \beta \log \frac{\pi_\theta(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right) \right]$$
</div>""",

    # ── DAY 155: Synthetic Data & Deduplication ──
    155: r"""<h3 class="sh3">1. Synthetic Data Generation & MinHash Deduplication</h3>
<p>
Frontier fine-tuning datasets are increasingly synthesized using frontier LLMs (Self-Instruct, Evol-Instruct). However, un-deduplicated synthetic data causes severe model overfitting and loss of reasoning diversity.
</p>
<p>
<strong>MinHash with Locality-Sensitive Hashing (LSH)</strong> approximates Jaccard similarity across millions of text strings in near-linear time:
</p>
<div class="math-block">
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|} \approx \Pr(\min(h(A)) = \min(h(B)))$$
</div>""",

    # ── DAY 156: Capstone: Deploying Fine-Tuned Model ──
    156: r"""<h3 class="sh3">1. End-to-End Fine-Tuning & Serving Lifecycle</h3>
<p>
Deploying a fine-tuned LLM to production requires:
</p>
<ol>
  <li><strong>LoRA Adapter Merge:</strong> Merge $\Delta \mathbf{W}$ into $\mathbf{W}_0$ for zero inference forward-pass latency overhead.</li>
  <li><strong>AWQ INT4 Quantization:</strong> Quantize merged weights to achieve 70% VRAM reduction.</li>
  <li><strong>vLLM Serving Container:</strong> Deploy with PagedAttention and continuous batching under FastAPI.</li>
</ol>""",

    # ── DAY 157: LLM Evaluation Metrics ──
    157: r"""<h3 class="sh3">1. The RAGAS Evaluation Quadrant</h3>
<p>
Enterprise RAG systems are evaluated across four complementary dimensions:
</p>
<ul>
  <li><strong>Faithfulness (Groundedness):</strong> Are all claims in the generated answer supported by the retrieved context?</li>
  <li><strong>Answer Relevance:</strong> Does the response directly address the user's query intent?</li>
  <li><strong>Context Precision:</strong> Are the most relevant retrieved chunks positioned at top ranks?</li>
  <li><strong>Context Recall:</strong> Does the retrieved context contain all necessary information to answer the question?</li>
</ul>""",

    # ── DAY 158: Observability & Tracing ──
    158: r"""<h3 class="sh3">1. OpenTelemetry Distributed Tracing for GenAI</h3>
<p>
Compound AI systems (RAG, multi-agent swarms) require distributed tracing to pinpoint latency bottlenecks and attribute token costs.
</p>
<p>
An <strong>OpenTelemetry Trace</strong> forms a Directed Acyclic Graph of <strong>Spans</strong> capturing embedding generation, vector DB lookups, reranking, and LLM token generation times.
</p>""",

    # ── DAY 159: Output Guardrails ──
    159: r"""<h3 class="sh3">1. Multi-Layer AI Safety Guardrails</h3>
<p>
Deploy dual-layer protection:
</p>
<ul>
  <li><strong>Input Classifiers:</strong> Scrub PII (Microsoft Presidio) and detect prompt injection jailbreaks using cosine similarity against adversarial vector clusters.</li>
  <li><strong>Output Verifiers:</strong> Prevent hallucinated toxic content and enforce structured JSON compliance before responses reach clients.</li>
</ul>""",

    # ── DAY 160: Semantic Caching ──
    160: r"""<h3 class="sh3">1. Exact vs Semantic Vector Caching</h3>
<p>
Exact caching fails when users phrase the same query with slight variations (<em>"How to reset router?"</em> vs <em>"Router reboot steps?"</em>).
</p>
<p>
<strong>Semantic Caching (e.g. Redis + Vector Index)</strong> computes the query embedding and checks if cosine similarity with a cached query exceeds threshold $\tau \ge 0.95$, returning cached responses in &lt;5ms and saving up to 80% on LLM API costs.
</p>""",

    # ── DAY 161: API Gateways & Load Balancing ──
    161: r"""<h3 class="sh3">1. Enterprise AI Gateways</h3>
<p>
AI Gateways (LiteLLM, Kong AI) provide unified ingress for LLM workloads:
</p>
<ul>
  <li><strong>Token Bucket Rate Limiting:</strong> Enforce rate limits per user/organization.</li>
  <li><strong>Automated Provider Failover:</strong> Fallback to secondary providers when primary models return 429/500 errors.</li>
  <li><strong>Dynamic Cluster Load Balancing:</strong> Distribute requests across GPU serving nodes based on active KV cache queue depth.</li>
</ul>""",

    # ── DAY 162: System Design Math ──
    162: r"""<h3 class="sh3">1. GPU VRAM & Throughput Capacity Planning</h3>
<p>
Formulas for sizing LLM serving infrastructure:
</p>
<div class="math-block">
$$\text{VRAM}_{\text{total}} = M_{\text{weights}} + M_{\text{KV}} + M_{\text{activations}}$$
</div>
<div class="math-block">
$$M_{\text{KV}} = 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times 2\text{ bytes} \times B \times S$$
</div>
<p>
For a 70B model with batch size $B=32$ and context $S=4096$, KV cache requires $\approx 52\text{GB}$ VRAM.
</p>""",

    # ── DAY 163: Advanced GenAI Milestone 🎉 ──
    163: r"""<h3 class="sh3">1. Advanced GenAI System Design Milestone</h3>
<p>
Congratulations on mastering advanced GenAI systems! You have built competency in:
</p>
<ul>
  <li>Hybrid Search, RRF Fusion, Cross-Encoder Rerankers, and GraphRAG.</li>
  <li>Cyclic StateGraphs, ReAct loops, Multi-Agent Swarms, and HITL safety gates.</li>
  <li>PagedAttention, FlashAttention, QLoRA, DPO, and distributed OpenTelemetry observability.</li>
</ul>"""
}

print(f"Loaded {len(W21_W22_THEORY)} comprehensive theory modules for Weeks 21 & 22.")
