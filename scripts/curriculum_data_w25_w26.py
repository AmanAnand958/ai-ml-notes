# scripts/curriculum_data_w25_w26.py
# Exhaustive pedagogical theory & task prompts for Weeks 25 & 26 (Days 178 - 191)

CURRICULUM_W25_W26 = {
    # ── DAY 178: Kubernetes Core Concepts ──
    178: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> You are setting up an enterprise Kubernetes cluster (EKS/GKE) for distributed AI model serving and fine-tuning workloads.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Write Kubernetes manifests for: Namespace, ConfigMap, Deployment, and ClusterIP Service.</li>
  <li>Configure NVIDIA GPU Device Plugin resource allocations (<code>nvidia.com/gpu: 2</code>) with Guaranteed QoS tier.</li>
  <li>Mount an <code>emptyDir</code> with <code>medium: Memory</code> to <code>/dev/shm</code> to prevent PyTorch DataLoader SIGBUS crashes.</li>
</ul>"""
        ]
    },

    # ── DAY 179: Deploying vLLM on Kubernetes ──
    179: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Deploy a high-throughput vLLM serving StatefulSet hosting Llama-3-8B-Instruct on a multi-GPU Kubernetes cluster.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Configure container arguments: <code>--model</code>, <code>--gpu-memory-utilization 0.90</code>, and <code>--max-model-len 4096</code>.</li>
  <li>Implement HTTP Readiness and Liveness probes against the <code>/health</code> endpoint with <code>initialDelaySeconds: 45</code>.</li>
  <li>Verify that the service successfully streams tokens via Server-Sent Events (SSE).</li>
</ul>"""
        ]
    },

    # ── DAY 180: Horizontal Pod Autoscaling (HPA) ──
    180: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Configure Prometheus Custom Metric Horizontal Pod Autoscaling (HPA) for your GPU serving cluster.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Deploy Prometheus Adapter and expose custom vLLM metrics to the Kubernetes Custom Metrics API.</li>
  <li>Create an HPA manifest scaling pods from 2 to 10 replicas when <code>vllm:num_requests_waiting</code> exceeds 5.</li>
  <li>Simulate high-concurrency traffic with <code>locust</code> and verify automated pod scale-up within 30 seconds.</li>
</ul>"""
        ]
    },

    # ── DAY 181: Helm Charts for ML Stacks ──
    181: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Package a complex ML serving stack (FastAPI, Redis vector cache, Prometheus exporter) into a parameterized, reusable Helm chart.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Construct Helm chart directory structure: <code>Chart.yaml</code>, <code>values.yaml</code>, and <code>templates/</code>.</li>
  <li>Parameterize replica counts, GPU allocations, model repository paths, and ingress hostnames.</li>
  <li>Deploy and verify the release to staging and production namespaces using <code>helm upgrade --install</code>.</li>
</ul>"""
        ]
    },

    # ── DAY 182: GitHub Actions CI/CD for ML ──
    182: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a complete GitOps CI/CD workflow in GitHub Actions that automatically tests, builds, and deploys ML containers upon pull request merges.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Configure workflow jobs: 1. Lint & Format (flake8/black), 2. Unit Testing (pytest), 3. Model Accuracy Gate, 4. Multi-Stage Docker Build & Push.</li>
  <li>Use GitHub Secrets for secure AWS ECR / Docker Hub authentication.</li>
  <li>Trigger automated Helm deployment rollouts upon successful container publishing.</li>
</ul>"""
        ]
    },

    # ── DAY 183: Model Regression Testing ──
    183: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement an automated model behavioral regression testing suite evaluated against frozen golden test slices.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Define golden test suites across: Safety/Toxicity, Structured JSON Conformance, and Domain F1 Accuracy.</li>
  <li>Execute automated regression tests in CI/CD before any model is approved for staging promotion.</li>
  <li>Block deployment if candidate model accuracy regresses by $> 0.5\%$ on any critical data slice.</li>
</ul>"""
        ]
    },

    # ── DAY 184: Capstone: Kubernetes Production LLM Deployment ──
    184: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Deliver a production-grade, autoscaling LLM serving cluster on Kubernetes featuring Helm packaging, Prometheus custom metric HPA, and GitOps CI/CD automation.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Deploy vLLM StatefulSet with multi-GPU acceleration and shared memory volumes.</li>
  <li>Configure Ingress routing with TLS termination and streaming timeout annotations.</li>
  <li>Execute end-to-end load testing and verify automated horizontal pod autoscaling.</li>
</ul>"""
        ]
    },

    # ── DAY 185: Vision-Language Models (VLMs) ──
    185: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Construct a Vision-Language Model (VLM) multimodal projector in PyTorch that bridges Vision Transformer (ViT) image patch embeddings into LLM token space.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a 2-layer MLP Multimodal Projector mapping 1024-dimensional visual tokens to 4096-dimensional LLM text embeddings.</li>
  <li>Calculate visual patch token counts ($N_{\text{patches}} = \frac{H}{P} \times \frac{W}{P}$) for a 336x336 image with patch size $P=14$.</li>
  <li>Execute a forward pass concatenating projected visual tokens with text prompt embeddings.</li>
</ul>"""
        ]
    },

    # ── DAY 186: Multimodal RAG & ColPali ──
    186: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a Multimodal Document Retrieval engine using ColPali / CLIP to search complex enterprise PDF documents containing charts, tables, and blueprints.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Convert PDF document pages to screenshots and generate multi-vector visual patch embeddings.</li>
  <li>Implement Late-Interaction MaxSim scoring: $\text{Score}(Q, D) = \sum_{i=1}^{|Q|} \max_{j=1}^{|D|} (\mathbf{q}_i \cdot \mathbf{d}_j)$.</li>
  <li>Benchmark retrieval accuracy against traditional OCR + text vector search on a visual document benchmark.</li>
</ul>"""
        ]
    },

    # ── DAY 187: Audio Processing with Whisper ──
    187: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement an audio preprocessing and feature extraction pipeline matching OpenAI Whisper specifications for multilingual speech recognition.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Resample raw audio to 16kHz mono and pad/trim waveforms to exact 30-second audio frames.</li>
  <li>Compute 80-channel log-Mel spectrogram features using Short-Time Fourier Transform (STFT) with 25ms window and 10ms hop length.</li>
  <li>Implement Voice Activity Detection (VAD) to filter silent chunks and prevent autoregressive hallucination loops.</li>
</ul>"""
        ]
    },

    # ── DAY 188: ML System Design — Recommendation Systems ──
    188: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Architect an industrial-scale recommendation engine serving 50,000,000 users over a catalog of 10,000,000 items under a strict 40ms p95 latency SLA.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Design the complete four-stage funnel: Two-Tower Candidate Generation (10M $\to$ 1,000) $\to$ Heavy Neural Ranking (1,000 $\to$ 100) $\to$ MMR Diversity Re-ranking (100 $\to$ 20) $\to$ Display Feed.</li>
  <li>Specify offline vector indexing pipelines (FAISS/HNSW) and online real-time feature store lookups (Redis/Feast).</li>
  <li>Calculate total system throughput, memory requirements, and GPU cluster sizing.</li>
</ul>"""
        ]
    },

    # ── DAY 189: DSPy — Programmatic Prompt Optimization ──
    189: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Replace brittle, manual prompt engineering with algorithmic prompt optimization using DSPy for a complex multi-hop financial QA pipeline.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Define declarative DSPy Signatures and composable ChainOfThought modules.</li>
  <li>Compile and optimize the pipeline using the <code>BootstrapFewShot</code> teleprompter against a custom quantitative validation metric.</li>
  <li>Benchmark accuracy improvements before and after DSPy teleprompter compilation.</li>
</ul>"""
        ]
    },

    # ── DAY 190: ML System Design — Semantic Search ──
    190: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Design a billion-scale distributed semantic search architecture handling 1,000,000,000 documents with sub-50ms query latency.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Design distributed vector sharding using consistent hashing and spherical k-means clustering.</li>
  <li>Implement Scalar Quantization (SQ8) to compress vector RAM footprint by 75%.</li>
  <li>Architect the two-stage retrieval pipeline: Distributed HNSW ANN lookup $\to$ GPU-accelerated Cross-Encoder reranking.</li>
</ul>"""
        ]
    },

    # ── DAY 191: Final Capstone & Portfolio Polish ──
    191: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Execute the final end-to-end certification, automated integration testing, and portfolio deployment across your entire 191-Day AI/ML engineering body of work.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Verify end-to-end integration across: Classical ML Pipelines, Deep Learning Vision/NLP models, Production MLOps (DVC/MLflow/Airflow), Kubernetes Clusters, and Frontier GenAI RAG/Agent microservices.</li>
  <li>Structure production-ready GitHub repositories with one-line Docker Compose startup commands, live API documentation, and architecture diagrams.</li>
</ul>"""
        ]
    }
}
