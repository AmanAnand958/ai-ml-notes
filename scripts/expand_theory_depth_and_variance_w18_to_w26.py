#!/usr/bin/env python3
"""
scripts/expand_theory_depth_and_variance_w18_to_w26.py
Fixes Issue 4: Expands theory_html across Weeks 18 to 26 with rich, authentic technical depth,
mathematical derivations, and production-engineering nuance matching the density and natural variance of Weeks 13-17.
"""

import os, yaml
from bs4 import BeautifulSoup
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

def get_word_count(html_content):
    soup = BeautifulSoup(html_content or '', 'html.parser')
    return len([w for w in soup.get_text().split() if w])

# Topic-specific deep substantive content additions for Weeks 18 to 26
DEEP_EXPANSIONS = {
    # ── WEEK 18 ──────────────────────────────────────────────────────
    125: """
<h3 class="sh3">Production Sizing & Compute Allocation for ML Microservices</h3>
<p>
When moving from local development to production container orchestration, sizing CPU and RAM allocations requires analyzing peak inference concurrency ($C$), average batch size ($B$), and resident memory for model weights ($M_{\text{weights}}$):
</p>
<div class="math-block">
$$\text{RAM}_{\text{Required}} = M_{\text{weights}} + \left( C \times \text{Payload}_{\text{size}} \right) + \text{Runtime}_{\text{Buffer}}$$
</div>
<p>
In containerized runtimes (Docker/Kubernetes), failing to account for payload serialization buffer overhead leads to immediate <code>OOMKilled</code> (Exit Code 137) container restarts under sudden traffic bursts.
</p>
""",
    127: """
<h3 class="sh3">Relational vs Non-Relational Storage Selection for MLOps</h3>
<p>
MLOps systems require a dual storage architecture: relational databases (PostgreSQL) manage user metadata, access tokens, and structured feature tables with strict ACID guarantees, while object stores (S3/GCS) store large immutable artifact blobs (serialized pickle models, ONNX graphs, and evaluation datasets). Storing model binaries directly inside relational rows introduces severe I/O bottlenecks during horizontal scaling.
</p>
""",
    131: """
<h3 class="sh3">Zero-Downtime Rolling Container Deployments</h3>
<p>
Deploying container updates without dropping in-flight inference requests requires configuring readiness probes with appropriate initial delays. During deployment, the ingress load balancer only directs traffic to new pods after model weights are fully deserialized into memory and warm-up inference queries return <code>200 OK</code>.
</p>
""",
    134: """
<h3 class="sh3">ML System Portfolio Presentation & Technical Storytelling</h3>
<p>
Senior and Staff ML interview loops evaluate portfolio projects across four engineering axes:
1. <strong>Problem Formulation:</strong> Business metric alignment and baseline benchmarking.
2. <strong>Data Lineage:</strong> Leakage prevention, out-of-fold validation, and feature drift detection.
3. <strong>Serving SLA:</strong> Latency distribution (p50, p95, p99), throughput (RPS), and compute efficiency.
4. <strong>Failure Modes:</strong> Graceful degradation, fallback models, and observability instrumentation.
</p>
""",

    # ── WEEK 20 ──────────────────────────────────────────────────────
    144: """
<h3 class="sh3">Function Calling & JSON Schema Validation Protocol</h3>
<p>
Modern LLM tool calling relies on constrained decoding and structured grammar generation. The LLM produces raw token logits constrained to match JSON schemas defined via Pydantic. When an agent attempts an invalid tool call (e.g. passing a string to an integer port parameter), the execution runtime intercepts the validation exception and reflects the schema error message back into the conversation context as a corrective observation.
</p>
""",
    148: """
<h3 class="sh3">Human-in-the-Loop (HITL) State Persistence & Checkpointing</h3>
<p>
Autonomous agent loops interacting with high-stakes external APIs (e.g. database deletions, financial transactions, production infrastructure deployments) require persistent interrupt gates. LangGraph achieves this by persisting graph state snapshots to Redis or PostgreSQL checkpointers, yielding control to human operators, and resuming graph traversal upon receiving cryptographic operator approval.
</p>
""",

    # ── WEEK 21 ──────────────────────────────────────────────────────
    151: """
<h3 class="sh3">Post-Training Quantization (PTQ): AWQ vs GPTQ Mechanics</h3>
<p>
Activation-aware Weight Quantization (AWQ) identifies the 1% most salient weight channels by observing activation magnitudes during calibration. By scaling salient channels prior to uniform INT4 quantization, AWQ protects outlier feature channels from truncation error:
</p>
<div class="math-block">
$$W' = W \cdot S^{-1}, \quad X' = S \cdot X, \quad \text{where } S_j = \max(|X_j|)^\alpha$$
</div>
<p>
This mathematical equivalence preserves perplexity on long-context reasoning tasks while cutting VRAM footprint from 16 GB to 4.5 GB for 7B models.
</p>
""",
    154: """
<h3 class="sh3">Direct Preference Optimization (DPO) Closed-Form Derivation</h3>
<p>
Unlike traditional RLHF with PPO (which requires training separate reward and value models), DPO leverages a closed-form substitution of the optimal policy $\pi^*$ into the Bradley-Terry preference model:
</p>
<div class="math-block">
$$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$
</div>
<p>
This eliminates the reward modeling phase, drastically reducing training instability and GPU memory requirements during alignment.
</p>
""",
    155: """
<h3 class="sh3">Speculative Decoding Verification & Rejection Sampling</h3>
<p>
Speculative decoding pairs a lightweight draft model ($M_q$) with a high-capacity target model ($M_p$). The draft model rapidly generates $K$ candidate tokens autoregressively. In a single forward pass, the target model verifies all $K$ tokens in parallel using modified rejection sampling:
</p>
<div class="math-block">
$$P(\text{accept } x_{t}) = \min\left(1, \frac{p(x_t|x_{<t})}{q(x_t|x_{<t})}\right)$$
</div>
<p>
Because memory bandwidth is the primary bottleneck during autoregressive generation, parallel verification increases generation speed by $2\times\text{--}3\times$ without altering target distribution outputs.
</p>
""",

    # ── WEEK 22 ──────────────────────────────────────────────────────
    159: """
<h3 class="sh3">Input Guardrails & Jailbreak Defense Architecture</h3>
<p>
Production GenAI gateways implement multi-stage defensive filtering:
1. <strong>Deterministic Regex & Presidio PII Masking:</strong> Redacts emails, credit cards, and social security numbers with zero latency overhead.
2. <strong>Vector Similarity Injection Classifier:</strong> Compares incoming prompt embeddings against known adversarial jailbreak embeddings (DAN, cipher attacks, roleplay exploits).
3. <strong>Small Language Model (SLM) Moderation Guard:</strong> Runs a fast, quantized 1B classifier (e.g. Llama-Guard-3-1B) to detect policy violations before invoking the primary LLM.
</p>
""",
    160: """
<h3 class="sh3">Semantic Caching Mathematical Similarity Bounds</h3>
<p>
Exact string caching fails on natural language queries due to paraphrasing. Semantic caching projects incoming queries into embedding space and checks vector distances against a Redis VSS index:
</p>
<div class="math-block">
$$\text{CacheHit}(\vec{q}, \vec{k}) = \begin{cases} \text{Return Cached Response} & \text{if } \cos(\vec{q}, \vec{k}) \ge \tau \\ \text{Forward to LLM} & \text{otherwise} \end{cases}$$
</div>
<p>
Tuning the similarity threshold $\tau \in [0.92, 0.96]$ balances cache hit rate ($30\%\text{--}45\%$ cost reduction) against false-positive semantic drift.
</p>
""",
    161: """
<h3 class="sh3">LLM Gateway Routing & Load Balancing Algorithms</h3>
<p>
Enterprise LLM gateways dynamically route requests across multiple upstream providers (OpenAI, Anthropic, self-hosted vLLM) based on real-time rate limit tracking (TPM/RPM token buckets), provider latency health checks, and fallback retry circuits.
</p>
""",
    162: """
<h3 class="sh3">Generative AI FinOps: Token Economics & Cost Attribution</h3>
<p>
Managing multi-tenant LLM infrastructure requires granular cost attribution:
- <strong>Prompt Caching Credits:</strong> Deducts $50\%\text{--}80\%$ from input token costs for static prefix embeddings.
- <strong>Tenant Quota Enforcement:</strong> Implements leaky-bucket rate limiters per API key to prevent runaway automated loops from exceeding department budgets.
</p>
""",

    # ── WEEK 23 ──────────────────────────────────────────────────────
    165: """
<h3 class="sh3">SageMaker Distributed Training & Spot Instance Checkpointing</h3>
<p>
Training large-scale deep learning models on AWS Spot GPU instances reduces compute costs by up to $70\%$. To survive sudden spot interruptions (2-minute warning notices), training loops must implement automated S3 state checkpointing: saving model weights, optimizer states, learning rate schedulers, and dataloader batch pointers to persistent S3 buckets.
</p>
""",
    166: """
<h3 class="sh3">SageMaker Multi-Model Endpoints (MME) Memory Management</h3>
<p>
Multi-Model Endpoints allow hosting hundreds of fine-tuned models on a single GPU cluster. SageMaker dynamically loads target model weights into GPU VRAM on first request and evicts least-recently-used (LRU) model weights when memory pressure approaches threshold limits.
</p>
""",
    167: """
<h3 class="sh3">Serverless AI Inference on AWS Lambda with ONNX Runtime</h3>
<p>
Deploying lightweight models (<100M parameters) on serverless AWS Lambda eliminates idle cluster costs. Compiling models to ONNX Runtime with quantization enables sub-50ms cold starts within Lambda's 10GB container image limit.
</p>
""",
    169: """
<h3 class="sh3">Cloud AI Infrastructure FinOps & Cost Optimization Matrix</h3>
<p>
Optimizing cloud ML infrastructure requires aligning workload types with pricing models:
- <strong>Reserved Instances / Savings Plans:</strong> 1-3 year commitments for steady-state baseline inference clusters (saving 40-60%).
- <strong>Spot Instances:</strong> Fault-tolerant hyperparameter searches and distributed pre-training jobs.
- <strong>On-Demand:</strong> Interactive exploratory research and unpredictable spike capacity.
</p>
""",

    # ── WEEK 24 ──────────────────────────────────────────────────────
    172: """
<h3 class="sh3">Data Version Control (DVC) Storage Pointers & Remote Caching</h3>
<p>
Git cannot efficiently version large binary datasets (Parquet, TFRecords). DVC calculates MD5 checksums of large files, writes lightweight <code>.dvc</code> pointer files to Git, and syncs raw binary chunks to content-addressable storage on AWS S3 or Google Cloud Storage.
</p>
""",
    174: """
<h3 class="sh3">Statistical Data Drift Detection: Population Stability Index (PSI)</h3>
<p>
Data drift occurs when production feature distributions $P(X)$ deviate from training distributions $Q(X)$. The Population Stability Index (PSI) quantifies this shift across $B$ binned feature intervals:
</p>
<div class="math-block">
$$\text{PSI} = \sum_{b=1}^B \left( P_b - Q_b \right) \times \ln\left( \frac{P_b}{Q_b} \right)$$
</div>
<p>
A PSI $> 0.2$ indicates significant distributional drift requiring automated retraining DAG triggering.
</p>
""",
    175: """
<h3 class="sh3">Canary & Shadow Traffic Routing for ML Models</h3>
<p>
Deploying a new model candidate directly to 100% traffic risks catastrophic downstream failures. Production MLOps employs:
- <strong>Shadow Deployments:</strong> Ingress router mirrors 100% of live traffic to the candidate model; candidate predictions are logged for telemetry but not returned to clients.
- <strong>Canary Rollouts:</strong> Routes 5% of live traffic to candidate model, monitoring error rates and latency percentiles before gradual promotion.
</p>
""",
    176: """
<h3 class="sh3">Model Governance & Production Model Cards</h3>
<p>
Regulatory compliance (EU AI Act, NIST AI RMF) mandates comprehensive model governance documentation: intended use cases, training dataset provenance, fairness and bias audits across demographic slices, performance decay bounds, and environmental compute footprints.
</p>
""",

    # ── WEEK 25 ──────────────────────────────────────────────────────
    179: """
<h3 class="sh3">Kubernetes NVIDIA GPU Scheduling & Topology Awareness</h3>
<p>
Kubernetes schedules GPU workloads via the NVIDIA GPU Operator and Device Plugin. For multi-GPU workloads (Tensor Parallelism), the scheduler must enforce NUMA node and NVLink topology affinity, ensuring communicating GPUs reside on the same PCIe switch to prevent inter-GPU communication bottlenecks.
</p>
""",
    182: """
<h3 class="sh3">Distributed Data Parallel (DDP) Ring-AllReduce Mechanics</h3>
<p>
In PyTorch Distributed Data Parallel (DDP), each GPU maintains an identical copy of model weights and processes a slice of the global batch. During the backward pass, gradients are synchronized across nodes using the Ring-AllReduce algorithm, transferring $2 \times \frac{N-1}{N} \times |W|$ bytes with bandwidth independent of node count $N$.
</p>
""",
    183: """
<h3 class="sh3">Distributed Ray Clustering on Kubernetes (KubeRay)</h3>
<p>
KubeRay orchestrates elastic compute clusters for distributed hyperparameter tuning (Ray Tune) and high-throughput model serving (Ray Serve), dynamically spawning worker pods on spot GPU instances and tearing them down upon job completion.
</p>
""",

    # ── WEEK 26 ──────────────────────────────────────────────────────
    187: """
<h3 class="sh3">Whisper Audio Transcription & Speculative Decoding for Speech</h3>
<p>
OpenAI's Whisper employs an encoder-decoder Transformer processing 80-channel log-Mel spectrograms. Chunking 30-second audio windows with voice activity detection (VAD) prevents hallucinations during silent intervals and reduces processing latency by $40\%$.
</p>
""",
    188: """
<h3 class="sh3">DSPy: Automated Prompt Compilation & Optimization</h3>
<p>
DSPy treats prompt engineering as an algorithmic optimization problem. Instead of hand-crafting prompts, DSPy parameterizes LLM pipeline signatures, evaluates outputs against a metric function, and uses Teleprompter optimizers (BootstrapFewShot, MIPRO) to automatically synthesize optimal few-shot demonstrations and prompt instructions.
</p>
""",
    189: """
<h3 class="sh3">Two-Tower Vector Retrieval System Design</h3>
<p>
Large-scale recommendation and retrieval systems process billions of candidates using a Two-Tower architecture:
- <strong>User / Query Tower:</strong> Computes embedding $\vec{u} = f_\theta(\text{UserFeatures})$ in real-time.
- <strong>Item / Document Tower:</strong> Computes embedding $\vec{v} = g_\phi(\text{ItemFeatures})$ offline and indexes millions of vectors in HNSW / SCaNN indices.
- <strong>Retrieval:</strong> Dot product $\vec{u} \cdot \vec{v}$ evaluates top-100 candidates in $<5\text{ms}$.
</p>
""",
    190: """
<h3 class="sh3">High-Concurrency Generative Search Architecture</h3>
<p>
Architecting an enterprise AI search engine capable of handling 10,000 QPS requires a 4-tier funnel:
1. <strong>Tier 1 (Filter & Lexical):</strong> BM25 / Sparse index narrows 100M documents $\to$ 10,000 candidates ($<2\text{ms}$).
2. <strong>Tier 2 (Vector Search):</strong> HNSW dense retrieval narrows 10,000 $\to$ 200 candidates ($<8\text{ms}$).
3. <strong>Tier 3 (Cross-Encoder Re-Ranker):</strong> MiniLM re-ranks 200 $\to$ 10 high-precision chunks ($<15\text{ms}$).
4. <strong>Tier 4 (LLM Generation):</strong> vLLM streaming synthesizer produces cited response ($<250\text{ms}$ TTFT).
</p>
"""
}

def expand_theories():
    counts_per_file = {}
    for w in range(18, 27):
        fpath = f"{DATA_DIR}/week{w:02d}.yaml"
        if not os.path.exists(fpath): continue
        data = load_yaml(fpath)
        
        file_count = 0
        for d in data.get('days', []):
            did = d['id']
            if did in DEEP_EXPANSIONS:
                current_th = d.get('theory_html', '')
                d['theory_html'] = current_th + "\n" + DEEP_EXPANSIONS[did].strip()
                file_count += 1
                
        save_yaml(fpath, data)
        counts_per_file[f"week{w:02d}.yaml"] = file_count
        
    return counts_per_file

if __name__ == '__main__':
    counts = expand_theories()
    print("=" * 60)
    print("Issue 4: Theory Content Depth & Variance Expansion Complete")
    print("=" * 60)
    for fname, cnt in counts.items():
        print(f"  • {fname}: {cnt} days expanded with deep technical sections")
    print(f"Total days deeply expanded: {sum(counts.values())}")
