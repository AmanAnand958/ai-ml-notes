"""
Theoretical content definitions for:
- Week 22: LLM Eval, Observability & Guardrails (Days 157 - 163)
- Week 23: Cloud AI Services (Days 164 - 170)
"""

THEORY_WEEKS_22_23 = {
    # ═════════════════════════════════════════════════════════════════════
    # WEEK 22: LLM EVAL, OBSERVABILITY & GUARDRAILS (Days 157 - 163)
    # ═════════════════════════════════════════════════════════════════════
    157: """<h3 class="sh3">1. The RAG & LLM Evaluation Triad</h3>
<p>
Evaluating generative AI systems cannot rely solely on standard precision/recall. Frameworks like <strong>RAGAS</strong> and <strong>TruLens</strong> decompose evaluation into four orthogonal, measurable dimensions:
</p>
<div class="mermaid">
graph TD
  Eval["RAG Evaluation Quadrant"] --> Faith["1. Faithfulness (Groundedness)\n(Are answer claims factually supported by retrieved context?)"]
  Eval --> Rel["2. Answer Relevance\n(Does the answer directly address the user's intent?)"]
  Eval --> CtxPrec["3. Context Precision\n(Are the relevant chunks ranked at the top of retrieval?)"]
  Eval --> CtxRec["4. Context Recall\n(Did retrieval capture all facts needed to answer?)"]
</div>
<div class="diagram-cap">The RAG Evaluation Quadrant: Faithfulness, Answer Relevance, Context Precision, and Context Recall.</div>

<h3 class="sh3">2. LLM-as-a-Judge vs. Deterministic Heuristics</h3>
<p>
While deterministic metrics (BLEU, ROUGE, Exact Match) evaluate surface-level token overlap, <strong>LLM-as-a-Judge</strong> uses strong reasoning models (e.g. GPT-4) prompted with structured rubrics to grade multi-step semantic quality and tone.
</p>""",

    158: """<h3 class="sh3">1. Distributed Tracing for LLM Applications</h3>
<p>
Modern compound AI systems involve multiple LLM calls, vector searches, tool executions, and state transitions. <strong>OpenTelemetry (OTel)</strong> and LLM observability platforms (<strong>Langfuse</strong>, <strong>LangSmith</strong>, <strong>Arize Phoenix</strong>) trace nested spans to pinpoint latency bottlenecks and token cost leaks.
</p>
<div class="mermaid">
graph TD
  Trace["Trace: User Request #8192 (Total: 420ms, Cost: $0.012)"] --> Span1["Span 1: Query Embedding (45ms)"]
  Trace --> Span2["Span 2: Qdrant Hybrid Search (28ms)"]
  Trace --> Span3["Span 3: Cross-Encoder Rerank (85ms)"]
  Trace --> Span4["Span 4: LLM Generation (250ms, 450 tokens)"]
  Trace --> Span5["Span 5: Guardrail Evaluation (12ms)"]
</div>
<div class="diagram-cap">Hierarchical Distributed Trace for a Multi-Stage RAG Pipeline.</div>""",

    159: """<h3 class="sh3">1. Safety Guardrails & Input/Output Filtering</h3>
<p>
Production AI systems must protect against adversarial prompt injections, jailbreaks, PII leakage, and toxic hallucinations before inputs reach the model and before responses reach users.
</p>
<div class="mermaid">
graph LR
  User["User Prompt"] --> InGuard["Input Guardrail\n(Injection Classifier / PII Anonymizer)"]
  InGuard -->|Clean| LLM["LLM Processing Engine"]
  InGuard -->|Blocked| BlockUser["400 Bad Request (Blocked by Safety Policy)"]
  LLM --> OutGuard["Output Guardrail\n(Hallucination Grader / Toxicity Check)"]
  OutGuard -->|Safe| Client["Safe Verified Response"]
  OutGuard -->|Unsafe| Fallback["Fallback Safe Response"]
</div>
<div class="diagram-cap">Bidirectional Guardrail Pipeline with Input Anonymization and Output Verification.</div>""",

    160: """<h3 class="sh3">1. Semantic Caching for Cost & Latency Reduction</h3>
<p>
Standard key-value caching fails on natural language because minor phrasing variations (<em>"What is capital of France?"</em> vs. <em>"France capital city?"</em>) produce different cache keys. <strong>Semantic Caching</strong> embeds incoming queries and matches against previously cached vectors within a cosine similarity threshold ($\tau \ge 0.95$).
</p>
<div class="mermaid">
graph TD
  Query["User Query"] --> Embed["Compute Query Embedding"]
  Embed --> VectorCache["Search Semantic Cache (Redis / Qdrant)"]
  VectorCache --> Match{"Cosine Sim >= 0.95?"}
  Match -->|Cache Hit| Hit["Return Cached Response\n(Latency: &lt; 5ms, Cost: $0.00)"]
  Match -->|Cache Miss| LLM["Call LLM API\n(Latency: 500ms, Cost: $0.005)"]
  LLM --> SaveCache["Store Embedding + Response in Cache"]
  SaveCache --> Resp["Return Fresh Response"]
</div>
<div class="diagram-cap">Semantic Caching Flowchart: Fast Vector Cache Lookup vs Full LLM Forward Pass.</div>""",

    161: """<h3 class="sh3">1. API Gateways & Load Balancing for LLM Clusters</h3>
<p>
Managing multiple model backends requires intelligent routing, rate limiting per API key, fallback redundancy across providers, and dynamic load balancing (Least Outstanding Requests, Weighted Round Robin).
</p>
<div class="mermaid">
graph TD
  Client["Client Traffic"] --> Gateway["AI Gateway (Kong / LiteLLM)"]
  Gateway --> RateLimit["Token Bucket Rate Limiter"]
  Gateway --> Cache["Shared Semantic Cache"]
  Gateway --> Router{"Router / Load Balancer"}
  Router --> Backend1["vLLM GPU Cluster 1 (Primary)"]
  Router --> Backend2["vLLM GPU Cluster 2 (Primary)"]
  Router --> Fallback["Azure OpenAI / AWS Bedrock (Fallback Provider)"]
</div>
<div class="diagram-cap">AI Gateway Architecture with Provider Fallbacks and Rate Limiting.</div>""",

    162: """<h3 class="sh3">1. GenAI System Design Math & Capacity Planning</h3>
<p>
Estimating GPU hardware, VRAM, and network requirements for enterprise generative AI deployments:
</p>
<div class="cb">
<div class="cb-head"><span class="cb-lang">text — System Design Formulas</span></div>
<pre><code>1. Model Memory (GB) = Parameters (Billions) × BytesPerParam (FP16=2, INT8=1, INT4=0.5)
   Example: 70B in INT4 = 70 × 0.5 = 35 GB VRAM

2. KV Cache per Request (Bytes) = 2 × Layers × Heads × HeadDim × SeqLen × BytesPerParam
   Example: Llama-3-70B (80 layers, 8 KV heads, dim 128, 4096 tokens, FP16):
   2 × 80 × 8 × 128 × 4096 × 2 ≈ 1.34 GB VRAM per concurrent stream

3. Serving Throughput (Tokens/sec) = (Concurrency × AvgTokensPerSec)
4. GPU Count = ceil(Total VRAM Needed / Single GPU VRAM Capacity)</code></pre>
</div>""",

    163: """<h3 class="sh3">1. Advanced GenAI Milestone & Portfolio Consolidation</h3>
<p>
Reviewing enterprise GenAI architectures: Advanced RAG, Autonomous LangGraph Multi-Agent Swarms, vLLM High-Throughput Serving, QLoRA Tuning, and Observability Telemetry.
</p>""",

    # ═════════════════════════════════════════════════════════════════════
    # WEEK 23: CLOUD AI SERVICES (Days 164 - 170)
    # ═════════════════════════════════════════════════════════════════════
    164: """<h3 class="sh3">1. AWS SageMaker: Training Jobs & Real-Time Endpoints</h3>
<p>
Amazon SageMaker manages the machine learning lifecycle on AWS. It isolates ephemeral distributed training instances (which terminate automatically upon completion) from persistent, auto-scaling real-time inference endpoints backed by Elastic Load Balancing.
</p>
<div class="mermaid">
graph LR
  subgraph Training Phase (Ephemeral)
    S3["S3 Training Data"] --> Spot["SageMaker Spot Instances\n(Distributed GPU Cluster)"]
    Spot --> Out["Model Artifact (model.tar.gz in S3)"]
  end
  subgraph Inference Phase (Persistent)
    Out --> ECR["ECR Inference Container (Triton / TorchServe)"]
    ECR --> Endpoint["SageMaker Real-Time Endpoint\n(Auto-Scales on TargetInvocations)"]
    Endpoint --> API["API Gateway / Lambda"]
  end
</div>
<div class="diagram-cap">AWS SageMaker Ephemeral Training Pipeline to Managed Real-Time Production Endpoint.</div>""",

    165: """<h3 class="sh3">1. Google Cloud Vertex AI Architecture</h3>
<p>
GCP Vertex AI unifies Google Cloud ML services under a single control plane. Vertex AI Pipelines compiles Kubeflow DAGs into serverless container steps, linking trained artifacts to the Vertex Model Registry and Model Garden.
</p>
<div class="mermaid">
graph LR
  BigQuery["BigQuery Data Warehouse"] --> Pipeline["Vertex AI Pipelines (Kubeflow DAG)"]
  Pipeline --> Train["Vertex Custom Training (TPU / A100)"]
  Train --> Registry["Vertex Model Registry"]
  Registry --> Endpoint["Vertex AI Online Prediction Endpoint"]
</div>
<div class="diagram-cap">Vertex AI End-to-End Enterprise Data-to-Serving Architecture.</div>""",

    166: """<h3 class="sh3">1. Serverless ML with AWS Lambda & API Gateway</h3>
<p>
For intermittent or bursty low-to-medium throughput workloads, serverless architectures scale to zero and eliminate idle GPU costs. Compiling models to <strong>ONNX</strong> or <strong>TFLite</strong> allows inference to execute inside lightweight AWS Lambda container runtimes (up to 10GB RAM).
</p>
<div class="mermaid">
graph LR
  Client["Client Request"] --> APIGW["Amazon API Gateway"]
  APIGW --> Lambda["AWS Lambda (ARM64 / Graviton)\n[In-Memory ONNX Runtime]"]
  Lambda --> S3["Model Cache in /tmp"]
  Lambda --> Resp["JSON Response (&lt; 25ms)"]
</div>
<div class="diagram-cap">Serverless ML Inference Topology using AWS Lambda, ONNX Runtime, and API Gateway.</div>""",

    167: """<h3 class="sh3">1. Enterprise Azure OpenAI Service Architecture</h3>
<p>
Azure OpenAI Service provides frontier OpenAI models (GPT-4o, text-embedding-3) backed by enterprise SLAs, private virtual networks (VNet Peering), role-based access control (RBAC via Microsoft Entra ID), and zero data-retention compliance policies.
</p>
<div class="mermaid">
graph LR
  Corp["Corporate VNet"] --> PrivateLink["Azure Private Endpoint (Private Link)"]
  PrivateLink --> AOAI["Azure OpenAI Service Resource"]
  Entra["Microsoft Entra ID (Managed Identity)"] -->|RBAC Auth| AOAI
  AOAI --> Model["Provisioned Throughput Units (PTU) Cluster"]
</div>
<div class="diagram-cap">Azure OpenAI Enterprise Secure Network Topology with Private Endpoints and Managed Identity.</div>""",

    168: """<h3 class="sh3">1. Cloud FinOps: Cost Optimization for LLM Systems</h3>
<p>
Unmanaged cloud AI costs can scale exponentially. FinOps strategies balance performance and budget across four key levers:
</p>
<ul>
  <li><strong>Model Cascading / Tiered Routing:</strong> Route 80% of simple classification queries to inexpensive SLMs ($0.15/1M tokens) and only call frontier LLMs ($5.00/1M tokens) when necessary.</li>
  <li><strong>Prompt Compression:</strong> Strip redundant filler tokens to minimize input context length.</li>
  <li><strong>Spot Training Instances:</strong> Save up to 70% on compute for distributed training with checkpoint recovery.</li>
  <li><strong>Provisioned Throughput (PTU) vs Pay-As-You-Go:</strong> Switch to PTUs when continuous utilization exceeds 65%.</li>
</ul>""",

    169: """<h3 class="sh3">1. Secrets Management for AI & MLOps Pipelines</h3>
<p>
Hardcoding API tokens, database credentials, or S3 access keys in code or Docker images introduces critical security vulnerabilities. Centralized secrets managers (<strong>AWS Secrets Manager</strong>, <strong>HashiCorp Vault</strong>) inject credentials securely at runtime with automated rotation.
</p>
<div class="mermaid">
graph LR
  App["ML Service Pod"] --> IAM["AWS IAM / Kubernetes ServiceAccount"]
  IAM --> Vault["AWS Secrets Manager / HashiCorp Vault"]
  Vault -->|Encrypted TLS Token| App
  App -->|Authenticated Call| OpenAI["External AI API (OpenAI / Cohere)"]
</div>
<div class="diagram-cap">Runtime Secrets Injection via Kubernetes Service Accounts and Cloud Secrets Manager.</div>""",

    170: """<h3 class="sh3">1. Capstone: Deploying an Enterprise RAG Pipeline to AWS</h3>
<p>
Deploying a full enterprise RAG application to AWS using AWS CDK / Terraform: VPC with private subnets, Qdrant on Amazon ECS Fargate, SageMaker / Bedrock inference, API Gateway, and CloudWatch alerting.
</p>
<div class="mermaid">
graph TD
  User["End User"] --> CF["CloudFront CDN + WAF"]
  CF --> ALB["Application Load Balancer"]
  ALB --> ECS["ECS Fargate: RAG FastAPI Backend"]
  ECS --> Qdrant["ECS Fargate: Qdrant Vector DB (EFS Storage)"]
  ECS --> Bedrock["Amazon Bedrock (Claude 3.5 Sonnet / Llama 3)"]
  ECS --> CW["Amazon CloudWatch Metrics & Logs"]
</div>
<div class="diagram-cap">Production AWS Cloud Architecture for Enterprise RAG System.</div>"""
}
