# scripts/theory_deep_w25_w26.py
# Deep theory for all 14 days in Weeks 25 and 26

W25_W26_THEORY = {
    # ── DAY 178: Kubernetes Core Concepts ──
    178: r"""<h3 class="sh3">1. Kubernetes Control Plane for Distributed AI</h3>
<p>
Running high-concurrency LLM inference and distributed training requires orchestrating containerized GPU workloads across physical compute nodes:
</p>
<div class="mermaid">
graph TD
    User["MLOps Engineer / CI/CD"] -->|kubectl / Helm| APIServer["kube-apiserver (Control Plane)"]
    APIServer --> etcd["etcd Key-Value Store"]
    APIServer --> Scheduler["kube-scheduler (GPU Resource Matching)"]
    Scheduler --> Worker1["Worker Node 1 (8x NVIDIA H100)"]
    Scheduler --> Worker2["Worker Node 2 (8x NVIDIA H100)"]
    Worker1 --> Pod1["vLLM Serving Pod (limits: nvidia.com/gpu: 4)"]
</div>
<div class="diagram-cap">Figure 178.1: Kubernetes GPU Workload Orchestration and Control Plane Architecture.</div>""",

    # ── DAY 179: Deploying vLLM on Kubernetes ──
    179: r"""<h3 class="sh3">1. Production vLLM StatefulSet & Shared Memory</h3>
<p>
Deploy vLLM on Kubernetes with:
</p>
<ul>
  <li><code>nvidia.com/gpu</code> resource requests matching limits for Guaranteed QoS.</li>
  <li><code>/dev/shm</code> mounted as an <code>emptyDir</code> with <code>medium: Memory</code> to prevent PyTorch distributed data loader deadlocks.</li>
  <li>Liveness and Readiness probes monitoring the <code>/health</code> HTTP endpoint.</li>
</ul>""",

    # ── DAY 180: Horizontal Pod Autoscaling (HPA) ──
    180: r"""<h3 class="sh3">1. Custom Metric Autoscaling with Prometheus</h3>
<p>
Generic CPU/Memory metrics fail for LLM autoscaling because GPUs sit at 100% compute even when requests are queuing.
</p>
<p>
<strong>Prometheus Adapter Custom Metric HPA:</strong> Autoscale GPU pods based on <code>vllm:num_requests_waiting</code> or <code>vllm:avg_prompt_throughput_tok_per_s</code>.
</p>""",

    # ── DAY 181: Helm Charts for ML Stacks ──
    181: r"""<h3 class="sh3">1. Parameterized Infrastructure with Helm</h3>
<p>
Helm charts parameterize Kubernetes deployments, services, ConfigMaps, and ingress rules across dev, staging, and production environments with simple <code>values.yaml</code> overrides.
</p>""",

    # ── DAY 182: GitHub Actions CI/CD for ML ──
    182: r"""<h3 class="sh3">1. GitOps Automated Quality Gates</h3>
<p>
Every pull request triggers:
</p>
<ol>
  <li>Linting (<code>flake8</code> / <code>black</code>).</li>
  <li>Unit testing (<code>pytest</code>).</li>
  <li>Model evaluation against golden regression datasets.</li>
  <li>Automated Docker image build and push to container registries.</li>
</ol>""",

    # ── DAY 183: Model Regression Testing ──
    183: r"""<h3 class="sh3">1. Golden Test Slices & Regression Gates</h3>
<p>
Evaluate candidate models against frozen golden test slices to guarantee zero regressions on critical safety, formatting, or domain-specific accuracy benchmarks.
</p>""",

    # ── DAY 184: Capstone: Production K8s LLM Deployment ──
    184: r"""<h3 class="sh3">1. Kubernetes Production AI Capstone</h3>
<p>
The Week 25 Capstone deploys a complete production LLM serving cluster on Kubernetes using Helm charts, Prometheus custom metric HPA, and automated GitOps CI/CD.
</p>""",

    # ── DAY 185: Vision-Language Models (VLMs) ──
    185: r"""<h3 class="sh3">1. Vision-Language Models (VLMs) & Cross-Modal Projectors</h3>
<p>
Vision-Language Models (e.g. <strong>LLaVA</strong>, <strong>Qwen-VL</strong>, <strong>CLIP</strong>) bridge computer vision and natural language processing. A visual encoder (Vision Transformer / ViT) divides an image into non-overlapping patches (e.g. $14 \times 14$), projects them into visual patch embeddings, and transforms them into the LLM's text embedding space using a multimodal projector (MLP or Cross-Attention Perceiver):
</p>
<div class="mermaid">
graph LR
  Img["Input Image (336x336)"] --> ViT["Vision Transformer (ViT-L/14)"]
  ViT --> Patches["576 Visual Patch Tokens (dim: 1024)"]
  Patches --> MLP["Multimodal Projection Layer (MLP / Cross-Attention)"]
  MLP --> VisTokens["Projected Visual Tokens (dim: 4096)"]
  Prompt["Text Prompt Tokens: 'Describe this image'"] --> Embed["Text Embedding"]
  VisTokens & Embed --> LLM["Autoregressive LLM (Llama-3 / Mistral)"]
  LLM --> Resp["Generated Textual Description"]
</div>
<div class="diagram-cap">Figure 185.1: Vision-Language Model (VLM) Architecture.</div>
<div class="math-block">
$$N_{\text{patches}} = \left( \frac{H}{P} \right) \times \left( \frac{W}{P} \right)$$
</div>""",

    # ── DAY 186: Multimodal RAG ──
    186: r"""<h3 class="sh3">1. Multimodal Document Intelligence & ColPali</h3>
<p>
Enterprise PDFs contain complex tables, charts, diagrams, and formatting that standard OCR text extractors fail to capture.
</p>
<p>
<strong>ColPali (Late-Interaction VLM):</strong> Indexes document page screenshots directly using Vision Transformers, preserving visual layout and enabling direct visual-semantic document retrieval.
</p>""",

    # ── DAY 187: Audio Processing with Whisper ──
    187: r"""<h3 class="sh3">1. OpenAI Whisper Architecture</h3>
<p>
Whisper processes 80-channel log-Mel spectrograms through an encoder-decoder Transformer to perform robust multilingual speech recognition with word-level timestamps.
</p>""",

    # ── DAY 188: ML System Design — Recommendation Systems ──
    188: r"""<h3 class="sh3">1. The Multi-Stage Recommendation Funnel</h3>
<p>
Industrial recommendation systems use a four-stage funnel:
</p>
<div class="mermaid">
graph TD
    Catalog["Total Catalog: 10M Items"] --> Retrieval["1. Candidate Retrieval (Two-Tower Model): 10M -> 1,000 | 5ms"]
    Retrieval --> Ranking["2. Heavy Neural Ranking (DLRM / Deep & Cross): 1,000 -> 100 | 25ms"]
    Ranking --> ReRanking["3. Re-Ranking & Diversity Filtering (MMR): 100 -> 20 | 5ms"]
    ReRanking --> Delivery["4. User Display Feed (Top 10 items)"]
</div>
<div class="diagram-cap">Figure 188.1: Multi-Stage Recommendation Funnel Architecture.</div>""",

    # ── DAY 189: DSPy — Programmatic Prompt Optimization ──
    189: r"""<h3 class="sh3">1. Prompt Programming with DSPy</h3>
<p>
DSPy replaces manual prompt engineering with algorithmic prompt optimization. Define declarative Signatures and Modules, and let the <strong>BootstrapFewShot / MIPRO Teleprompter</strong> compile optimal prompts and demonstrations against quantitative metric functions.
</p>""",

    # ── DAY 190: ML System Design — Semantic Search ──
    190: r"""<h3 class="sh3">1. Billion-Scale Semantic Search Architecture</h3>
<p>
Billion-scale semantic search partitions vectors across sharded clusters using HNSW + Product Quantization with GPU-accelerated cross-encoder rerankers.
</p>""",

    # ── DAY 191: Final Capstone & Portfolio Polish ──
    191: r"""<h3 class="sh3">1. Course Graduation & Portfolio Blueprint</h3>
<p>
Congratulations on completing the 191-Day AI/ML Self-Study Curriculum! You have mastered mathematical foundations, deep learning algorithms, production MLOps, and frontier GenAI systems.
</p>"""
}

print(f"Loaded {len(W25_W26_THEORY)} comprehensive theory modules for Weeks 25 & 26.")
