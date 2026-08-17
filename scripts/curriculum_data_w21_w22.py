# scripts/curriculum_data_w21_w22.py
# Exhaustive pedagogical theory & task prompts for Weeks 21 & 22 (Days 150 - 163)

CURRICULUM_W21_W22 = {
    # ── DAY 150: vLLM & PagedAttention ──
    150: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> You are architecting the inference serving cluster for a high-concurrency LLM application processing 500 concurrent requests. Standard PyTorch serving exhausts GPU VRAM due to KV cache memory fragmentation.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a <strong>PagedAttention Block Memory Manager</strong> in Python that allocates fixed-size physical memory pages (block_size = 16 tokens) on demand.</li>
  <li>Implement a <strong>Logical-to-Physical Block Table Mapping</strong> enabling non-contiguous GPU memory assignment for incoming generation tokens.</li>
  <li>Build an <strong>Iteration-Level Continuous Batching Scheduler</strong> that dynamically evicts finished requests and admits queued requests at each token iteration step.</li>
  <li>Benchmark throughput (Tokens/Sec) against traditional static batching.</li>
</ul>"""
        ]
    },

    # ── DAY 151: FlashAttention & Speculative Decoding ──
    151: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Accelerate long-context (16K tokens) autoregressive transformer decoding on NVIDIA GPU hardware by eliminating High-Bandwidth Memory (HBM) read/write bottlenecks.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement an <strong>IO-Aware Tiled Attention Forward Pass</strong> simulating FlashAttention SRAM tiling and online softmax scaling ($m_i, l_i$).</li>
  <li>Implement a <strong>Speculative Decoding Engine</strong>: A small draft model generates $K=4$ speculative tokens, which are verified simultaneously in a single parallel forward pass by the large target model.</li>
  <li>Calculate speedup factor and assert mathematical output equivalence with standard autoregressive generation.</li>
</ul>"""
        ]
    },

    # ── DAY 152: Quantization (AWQ vs GPTQ vs GGUF) ──
    152: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Compress a 70-billion parameter FP16 language model (140GB VRAM) to run on two 24GB consumer GPUs (RTX 4090) or a single 48GB GPU with &lt;1% perplexity degradation.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement <strong>Symmetric Uniform INT8 and INT4 Quantization</strong> with dynamic scale $\text{Scale} = \frac{\max(|X|)}{2^{b-1}-1}$ and zero-point offset calculation.</li>
  <li>Implement an <strong>Activation-Aware Weight Protection (AWQ)</strong> heuristic: identify the top 1% salient weight channels based on average input activation magnitude and preserve them in FP16 while quantizing the remaining 99% to INT4.</li>
  <li>Compute and print Mean Squared Error (MSE) and memory compression ratio.</li>
</ul>"""
        ]
    },

    # ── DAY 153: QLoRA & PEFT ──
    153: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Fine-tune a frontier 70B parameter base model on a specialized domain dataset (legal contracts) using a single 48GB GPU workstation without out-of-memory crashes.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a custom <strong>LoRA (Low-Rank Adaptation) Linear Layer</strong> in PyTorch: $\mathbf{W} = \mathbf{W}_0 + \frac{\alpha}{r} (\mathbf{B} \cdot \mathbf{A})$ with rank $r=16$ and scaling $\alpha=32$.</li>
  <li>Implement <strong>NormalFloat4 (NF4) Quantile Quantization</strong> for the frozen base weights $\mathbf{W}_0$.</li>
  <li>Execute a forward and backward pass, verifying that only matrices $\mathbf{A}$ and $\mathbf{B}$ receive gradient updates while base weights remain strictly frozen.</li>
</ul>"""
        ]
    },

    # ── DAY 154: DPO, ORPO & GRPO ──
    154: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Align an instruction-tuned model with safety guidelines using Direct Preference Optimization (DPO) on pairwise comparison data without training an external reward model or running PPO.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement the <strong>DPO Loss Function</strong>: $\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$ with temperature $\beta = 0.1$.</li>
  <li>Compute log-probabilities of preferred responses $y_w$ and rejected responses $y_l$ under both active policy $\pi_\theta$ and frozen reference policy $\pi_{\text{ref}}$.</li>
  <li>Execute gradient descent step and assert that probability ratio for winning responses increases while losing response probability decreases.</li>
</ul>"""
        ]
    },

    # ── DAY 155: Synthetic Data & Deduplication ──
    155: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Generate 100,000 synthetic instruction-following reasoning examples using Evol-Instruct, then clean the dataset using MinHash LSH to remove near-duplicate examples before training.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement an <strong>Evol-Instruct Task Mutator</strong> applying constraint addition, deep reasoning steps, and concrete domain grounding.</li>
  <li>Implement <strong>MinHash Locality-Sensitive Hashing (LSH)</strong> using 128 hash functions and 5-word shingling to detect text pairs with Jaccard similarity $J(A, B) \ge 0.80$.</li>
  <li>Filter out duplicates and compute clean dataset yield percentage.</li>
</ul>"""
        ]
    },

    # ── DAY 156: Capstone: Deploying Custom Fine-Tuned Model ──
    156: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Package, quantize, and deploy your fine-tuned domain LLM as a production-grade FastAPI microservice under high-concurrency traffic.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Merge LoRA adapter weights $\Delta \mathbf{W}$ permanently into base model weights $\mathbf{W}_0$.</li>
  <li>Apply AWQ INT4 post-training quantization to compressed merged weights.</li>
  <li>Deploy inside a vLLM serving container with PagedAttention and continuous batching enabled.</li>
  <li>Execute a 50-client concurrent load test asserting p95 Time-To-First-Token (TTFT) &lt; 50ms.</li>
</ul>"""
        ]
    },

    # ── DAY 157: LLM Evaluation Metrics (RAGAS) ──
    157: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build an automated CI/CD evaluation test suite for an enterprise customer service RAG system that runs before every code deployment.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement deterministic evaluation functions for <strong>Faithfulness (Groundedness)</strong> and <strong>Answer Relevance</strong>.</li>
  <li>Implement <strong>Context Precision@K</strong> and <strong>Context Recall</strong> scoring against golden reference datasets.</li>
  <li>Set automated deployment quality gates: fail CI build if Faithfulness &lt; 0.90 or Context Recall &lt; 0.85.</li>
</ul>"""
        ]
    },

    # ── DAY 158: Observability & Tracing ──
    158: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Instrument a multi-step RAG microservice with OpenTelemetry distributed tracing to identify latency bottlenecks and attribute API costs to individual tenants.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Create hierarchical OpenTelemetry Spans for: <code>cache_lookup</code>, <code>query_embedding</code>, <code>vector_search</code>, <code>cross_encoder_rerank</code>, and <code>llm_generate</code>.</li>
  <li>Record standardized GenAI semantic convention attributes: <code>gen_ai.prompt_tokens</code>, <code>gen_ai.completion_tokens</code>, and calculate financial cost per request.</li>
  <li>Export trace telemetry to Jaeger / Prometheus formats.</li>
</ul>"""
        ]
    },

    # ── DAY 159: Output Guardrails ──
    159: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a high-performance, multi-layer AI safety guardrail proxy that intercepts incoming prompts and outgoing LLM responses for a healthcare AI chatbot.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement <strong>Input Guardrails</strong>: Presidio regex/NER PII de-identification and vector embedding cosine jailbreak classifier.</li>
  <li>Implement <strong>Output Guardrails</strong>: Hallucinated medical advice detector and PII leak scrubber.</li>
  <li>Assert guardrail execution overhead is &lt; 15ms per request.</li>
</ul>"""
        ]
    },

    # ── DAY 160: Semantic Caching ──
    160: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement a Redis-backed Semantic Vector Cache for an enterprise FAQ bot that handles 1,000,000 queries per day, reducing LLM API costs by 75%.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Compute 1536-dimensional query embeddings and query the Redis vector index for nearest cached prompt vectors.</li>
  <li>If cosine similarity $\ge 0.94$, return cached response instantly (&lt; 5ms).</li>
  <li>If similarity &lt; 0.94, call the LLM, cache the (query_vector, response) pair with a 24-hour TTL, and return fresh output.</li>
</ul>"""
        ]
    },

    # ── DAY 161: API Gateways & Load Balancing ──
    161: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Architect an enterprise AI Gateway proxy (LiteLLM) that routes traffic across multiple LLM providers (OpenAI, Anthropic, Azure) and self-hosted vLLM GPU clusters.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement <strong>Token Bucket Rate Limiting</strong> enforcing RPM and TPM quotas per API key.</li>
  <li>Implement <strong>Automated Provider Failover</strong>: seamlessly route to secondary providers on HTTP 429/500 errors with exponential backoff and jitter.</li>
  <li>Load balance across self-hosted GPU nodes based on active KV cache queue depth.</li>
</ul>"""
        ]
    },

    # ── DAY 162: System Design Math ──
    162: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Perform hardware capacity planning and cost estimation for deploying a 70B parameter model serving 10,000 active concurrent users.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Calculate total VRAM requirements: Model Weights + KV Cache ($B=64, S=4096$) + Activation memory.</li>
  <li>Calculate memory bandwidth saturation and decode throughput (Tokens/Sec) on NVIDIA H100 (3.35 TB/s HBM3).</li>
  <li>Size the exact number of 8x H100 GPU nodes required to achieve a p95 latency &lt; 25ms/token.</li>
</ul>"""
        ]
    },

    # ── DAY 163: Advanced GenAI Milestone 🎉 ──
    163: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Execute a comprehensive architectural audit and integration smoke test across your entire GenAI technology stack.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Verify end-to-end integration: Semantic Cache $\to$ Hybrid RAG $\to$ Cross-Encoder $\to$ vLLM PagedAttention $\to$ Guardrails $\to$ OpenTelemetry.</li>
  <li>Benchmark total system response latency under load and verify zero unhandled exceptions.</li>
</ul>"""
        ]
    }
}
