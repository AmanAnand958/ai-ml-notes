"""
Theoretical content definitions for:
- Week 18: Capstone & Portfolio Polish (Days 125 - 135)
- Week 19: Advanced RAG System Design (Days 136 - 142)
"""

THEORY_WEEKS_18_19 = {
    # ═════════════════════════════════════════════════════════════════════
    # WEEK 18: CAPSTONE & PORTFOLIO POLISH (Days 125 - 135)
    # ═════════════════════════════════════════════════════════════════════
    125: """<h3 class="sh3">1. Kubernetes Core Primitives for ML Engineers</h3>
<p>
Deploying machine learning models in production requires high availability, rolling zero-downtime updates, and automated self-healing. <strong>Kubernetes (K8s)</strong> manages containerized ML workloads across compute clusters using key declarative primitives:
</p>
<div class="mermaid">
graph TD
  Client["Client / External Web Traffic"] --> Ingress["Ingress Controller (NGINX / ALB)"]
  Ingress --> Svc["ClusterIP Service (Load Balancer)"]
  Svc --> Pod1["Pod 1: FastAPI Model Worker\n(RAM: 2Gi, CPU: 1.0)"]
  Svc --> Pod2["Pod 2: FastAPI Model Worker\n(RAM: 2Gi, CPU: 1.0)"]
  Svc --> Pod3["Pod 3: FastAPI Model Worker\n(RAM: 2Gi, CPU: 1.0)"]
  RS["ReplicaSet (Replicas: 3)"] -.->|Maintains Desired State| Pod1 & Pod2 & Pod3
</div>
<div class="diagram-cap">Kubernetes Ingress, Service, and ReplicaSet Architecture for High-Availability Model Serving.</div>

<h3 class="sh3">2. Production Pod Manifest & Resource Constraints</h3>
<p>
A production ML deployment requires explicit resource boundaries and readiness probes to ensure traffic is only routed after model weights are fully loaded into memory:
</p>
<div class="cb">
<div class="cb-head"><span class="cb-lang">yaml — model-deployment.yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-inference-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-serving
  template:
    metadata:
      labels:
        app: ml-serving
    spec:
      containers:
      - name: fastapi-model
        image: my-registry.io/ml-service:v1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10</code></pre>
</div>""",

    126: """<h3 class="sh3">1. PaaS Deployment Patterns for ML Applications</h3>
<p>
Platform-as-a-Service (PaaS) providers like <strong>Render</strong> and <strong>Railway</strong> streamline continuous deployment by connecting directly to Git repositories. When changes merge into <code>main</code>, the platform builds the Docker container, attaches managed environment variables, issues SSL certificates, and exposes a public HTTPS endpoint.
</p>
<div class="mermaid">
graph LR
  Git["Git Push to main"] --> Webhook["PaaS Webhook Trigger"]
  Webhook --> Build["Docker Build & Dependency Cache"]
  Build --> Health["Healthcheck Probe (/health)"]
  Health --> Traffic["Traffic Cutover (Zero-Downtime)"]
  Traffic --> CDN["Edge CDN / HTTPS Endpoint"]
</div>
<div class="diagram-cap">Automated Git-driven PaaS deployment workflow with health-check validation.</div>

<h3 class="sh3">2. Multi-Stage Dockerfile for Minimal Image Size</h3>
<p>
Large images increase cold-start latency and bandwidth costs. Using a multi-stage build isolates build dependencies (compilers, wheel caches) from the final lightweight runtime image:
</p>
<div class="cb">
<div class="cb-head"><span class="cb-lang">dockerfile — Dockerfile</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]</code></pre>
</div>""",

    127: """<h3 class="sh3">1. The MLOps Lifecycle & Experiment Tracking</h3>
<p>
Traditional software versioning tracks source code via Git, but machine learning requires versioning three distinct dimensions: <strong>Code</strong>, <strong>Data</strong>, and <strong>Model Hyperparameters / Metrics</strong>. Without structured experiment tracking, comparing candidate models across training iterations is error-prone.
</p>
<div class="mermaid">
graph TD
  Code["1. Code (Git Commit)"] & Data["2. Data (DVC / S3 URI)"] & Params["3. Parameters (LR, Batch Size)"] --> Train["Model Training Run"]
  Train --> Metrics["Validation Metrics (Accuracy, AUC, F1)"]
  Train --> Artifacts["Model Artifacts (.onnx / .pkl)"]
  Metrics & Artifacts --> MLflow["MLflow Tracking Server & Model Registry"]
  MLflow --> Stage["Model Staging & Promotion Gate"]
</div>
<div class="diagram-cap">Tri-factor tracking: Associating code, data, and parameters with logged artifacts in MLflow.</div>

<h3 class="sh3">2. Programmatic Experiment Logging with MLflow</h3>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — train_and_log.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

mlflow.set_experiment("churn-prediction-v2")

with mlflow.start_run(run_name="gbm-depth-4"):
    params = {"n_estimators": 100, "learning_rate": 0.05, "max_depth": 4}
    mlflow.log_params(params)
    
    clf = GradientBoostingClassifier(**params)
    clf.fit(X_train, y_train)
    
    auc = roc_auc_score(y_val, clf.predict_proba(X_val)[:, 1])
    mlflow.log_metric("val_roc_auc", auc)
    mlflow.sklearn.log_model(clf, artifact_path="model")</code></pre>
</div>""",

    128: """<h3 class="sh3">1. Capstone System Architecture & Specification</h3>
<p>
An enterprise machine learning capstone project must demonstrate end-to-end engineering rigor: from data ingestion and validation to model serving, monitoring, and interactive user interfaces.
</p>
<div class="mermaid">
graph LR
  subgraph Data Pipeline
    Raw["Raw Parquet Data"] --> Val["Great Expectations Validation"]
    Val --> Pre["Feature Transformer"]
  end
  subgraph Inference Engine
    Pre --> Model["Trained Model (ONNX Runtime)"]
    Model --> API["FastAPI REST Endpoints"]
  end
  subgraph Client & Monitoring
    API --> UI["Streamlit / React Dashboard"]
    API --> Prom["Prometheus Metrics & Drift Alerts"]
  end
</div>
<div class="diagram-cap">Capstone End-to-End System Architecture: Pipeline, Inference Engine, and Observability Layers.</div>

<h3 class="sh3">2. System Contract & API Interface Design</h3>
<p>
Defining explicit Pydantic schemas prevents downstream inference failures due to missing or ill-typed input fields.
</p>""",

    129: """<h3 class="sh3">1. Modular Model Training Pipeline</h3>
<p>
Clean ML engineering separates preprocessing logic, training execution, and evaluation gates into reusable, testable Python modules.
</p>
<div class="mermaid">
graph TD
  Raw["Raw Dataset"] --> Split["Stratified Train/Val/Test Split"]
  Split --> Fit["Fit Preprocessor on Train Only"]
  Fit --> Transform["Transform Train, Val, Test"]
  Transform --> Train["Train Estimator"]
  Train --> Eval["Evaluate on Test Set"]
  Eval --> Gate{"Passes Quality Gate?\n(AUC > 0.85 & Latency < 20ms)"}
  Gate -->|Yes| Save["Export Artifacts"]
  Gate -->|No| Abort["Abort & Alert"]
</div>
<div class="diagram-cap">Reproducible Training Pipeline with Automated Quality Gate Validation.</div>""",

    130: """<h3 class="sh3">1. Containerizing Inference Services with FastAPI & Uvicorn</h3>
<p>
FastAPI provides asynchronous request handling, automated OpenAPI documentation, and strict Pydantic payload validation. Paired with Gunicorn/Uvicorn process workers, it handles concurrent prediction requests efficiently.
</p>
<div class="mermaid">
graph LR
  Client["Client POST /predict"] --> Gunicorn["Gunicorn Master Process"]
  Gunicorn --> W1["Worker 1 (Uvicorn)"]
  Gunicorn --> W2["Worker 2 (Uvicorn)"]
  W1 & W2 --> Cache["In-Memory Model Session"]
  Cache --> Resp["JSON Prediction Response"]
</div>
<div class="diagram-cap">Gunicorn Worker Process Management for High-Throughput FastAPI Serving.</div>""",

    131: """<h3 class="sh3">1. Frontend Integration & Cloud Production Deployment</h3>
<p>
Connecting a modern frontend (Streamlit, Gradio, or Next.js) to your containerized ML service completes the user-facing deployment. Securing the API with CORS policies and API tokens ensures safe multi-tenant access.
</p>
<div class="mermaid">
graph LR
  User["End User"] --> Frontend["Streamlit / Web UI"]
  Frontend -->|JSON / HTTPS| API["FastAPI Backend (Render / AWS)"]
  API --> Engine["ONNX / PyTorch Inference"]
  API --> Logs["CloudWatch / Datadog Logs"]
</div>
<div class="diagram-cap">Frontend to Backend API Integration Architecture with Centralized Logging.</div>""",

    132: """<h3 class="sh3">1. Architecting a Senior-Level GitHub Repository</h3>
<p>
Hiring managers and technical leads look for professional repository hygiene. A top-tier portfolio repository includes:
</p>
<ul>
  <li><strong>System Architecture Diagram:</strong> Visual representation of components, data flow, and APIs.</li>
  <li><strong>Quickstart Guide:</strong> One-line <code>docker compose up</code> setup command.</li>
  <li><strong>Reproducibility:</strong> Pinned dependencies, seeds, and DVC data pipelines.</li>
  <li><strong>CI/CD Badges:</strong> Automated unit testing and linting status.</li>
  <li><strong>Benchmarking Table:</strong> Latency (p50/p95), throughput (QPS), and validation metrics.</li>
</ul>""",

    133: """<h3 class="sh3">1. Resume & LinkedIn Positioning for ML & AI Engineers</h3>
<p>
Translate technical tasks into high-impact engineering accomplishments using the <strong>Action + Context + Metric</strong> formula:
</p>
<div class="cb">
<div class="cb-head"><span class="cb-lang">text — Bullet Point Comparison</span></div>
<pre><code>❌ WEAK: "Trained a machine learning model to predict customer churn in Python."
✅ STRONG: "Architected an end-to-end churn prediction pipeline using XGBoost and FastAPI; reduced inference latency from 140ms to 22ms (p95) and delivered $180k projected annual retention savings."</code></pre>
</div>""",

    134: """<h3 class="sh3">1. Machine Learning Interview Framework</h3>
<p>
Technical ML interviews evaluate candidates across three core pillars:
</p>
<div class="mermaid">
graph TD
  Pillars["ML Engineering Interview"] --> Math["1. Theory & Math\n(Gradients, Loss Functions, Trade-offs)"]
  Pillars --> Coding["2. Applied Coding\n(Vectorization, Data Structures, PyTorch)"]
  Pillars --> Design["3. System Design\n(Scale, Latency SLAs, Drift, Caching)"]
</div>
<div class="diagram-cap">The Three Pillars of Senior Machine Learning Technical Interviews.</div>""",

    135: """<h3 class="sh3">1. Mid-Course Milestone: Applied System Architecture</h3>
<p>
Consolidating Months 1–4: Foundations (Linear Algebra, Calculus, Statistics), Core Machine Learning (Scikit-Learn, Ensembles), Deep Learning & NLP (CNNs, RNNs, Attention, Transformers), and MLOps Deployment (FastAPI, Docker, Kubernetes).
</p>""",

    # ═════════════════════════════════════════════════════════════════════
    # WEEK 19: ADVANCED RAG SYSTEM DESIGN (Days 136 - 142)
    # ═════════════════════════════════════════════════════════════════════
    136: """<h3 class="sh3">1. The Dual-Tower Problem: Sparse vs. Dense Retrieval</h3>
<p>
In enterprise RAG systems, vanilla vector search frequently misses domain-specific queries containing exact alphanumeric identifiers (e.g., error codes, product SKUs, or legal clause numbers). Sparse retrieval (<strong>BM25</strong>) excels at exact keyword precision, while dense embedding models (e.g., <code>text-embedding-3-large</code>) capture semantic intent and conceptual similarity.
</p>
<div class="mermaid">
graph TD
  Query["User Query"] --> Sparse["Sparse Retriever\n(BM25 Inverted Index)"]
  Query --> Dense["Dense Retriever\n(HNSW Vector Index)"]
  Sparse --> RankA["Sparse Ranked List\n[Doc A, Doc B, Doc C]"]
  Dense --> RankB["Dense Ranked List\n[Doc B, Doc D, Doc A]"]
  RankA & RankB --> Fusion["Reciprocal Rank Fusion\n(RRF Engine, k=60)"]
  Fusion --> FinalRank["Fused Top-K Context\n1. Doc B (Score: 0.032)\n2. Doc A (Score: 0.031)"]
</div>
<div class="diagram-cap">Hybrid Retrieval Architecture: Combining Sparse Inverted Index and Dense Vector ANN with RRF Fusion.</div>

<h3 class="sh3">2. Mathematical Formulation of Reciprocal Rank Fusion (RRF)</h3>
<p>
RRF resolves the score-calibration problem by ignoring raw similarity scores and operating strictly on ordinal rank positions:
</p>
<div class="math-block">
$$RRFScore(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
</div>
<p>
Where $r_m(d)$ is the 1-based rank of document $d$ in retriever $m$, and $k$ is a smoothing constant (standard: $k = 60$) that prevents top ranks from dominating disproportionately.
</p>""",

    137: """<h3 class="sh3">1. Bi-Encoder Dual Tower vs. Cross-Encoder Architecture</h3>
<p>
Modern RAG search pipelines use a two-stage <strong>Retrieve-and-Rerank</strong> architecture to balance millisecond latency with deep cross-attention semantic precision.
</p>
<div class="mermaid">
graph LR
  subgraph Stage 1: Candidate Retrieval (Top 100)
    Q1["Query"] --> E1["Query Encoder"]
    D1["Corpus (1M+ Docs)"] --> E2["Precomputed Index"]
    E1 & E2 --> ANN["Fast Cosine ANN\n(&lt; 15ms)"]
  end
  ANN --> Candidates["Top 100 Candidates"]
  subgraph Stage 2: Cross-Encoder Re-Ranking (Top 5)
    Candidates & Q1 --> CE["Cross-Encoder\n(Full Self-Attention over [Q, Doc])"]
    CE --> Scored["High-Precision Top 5\n(&lt; 35ms)"]
  end
</div>
<div class="diagram-cap">Two-Stage Retrieve-and-Rerank: Fast ANN candidate generation followed by deep cross-attention reranking.</div>

<h3 class="sh3">2. Cross-Attention Mechanism</h3>
<p>
Unlike Bi-encoders which embed query $q$ and document $d$ independently ($u = f(q), v = g(d)$), a <strong>Cross-Encoder</strong> concatenates query and document tokens into a single sequence, computing full token-to-token attention:
</p>
<div class="math-block">
$$\text{Input} = \text{[CLS]} \circ q_1 \dots q_n \circ \text{[SEP]} \circ d_1 \dots d_m \circ \text{[SEP]}$$
$$\text{Score} = \sigma\left(W \cdot \text{Transformer}(\text{Input})_{[\text{CLS}]}\right)$$
</div>""",

    138: """<h3 class="sh3">1. Advanced Document Chunking Strategies</h3>
<p>
Naively splitting text by arbitrary character or token counts breaks syntactic boundaries and separates context from relevant entities. Production RAG utilizes semantic-aware chunking strategies:
</p>
<div class="mermaid">
graph TD
  Doc["Raw Long-Form Document"] --> Strategy{"Chunking Strategy"}
  Strategy --> Fixed["1. Fixed-Size with Overlap\n(512 tokens, 10% overlap)"]
  Strategy --> Sem["2. Semantic Splitting\n(Embed sentence diffs, split on cosine drops)"]
  Strategy --> Hier["3. Parent-Child / Hierarchical\n(Child 128 tokens -> Parent 1024 tokens)"]
  Strategy --> DocTree["4. Document Hierarchy\n(H1 -> H2 -> Section-aware parsing)"]
</div>
<div class="diagram-cap">Document Chunking Strategies for Optimal Context Retrieval.</div>

<h3 class="sh3">2. Parent-Child (Small-to-Big) Retrieval Pattern</h3>
<p>
Small chunks (100–200 tokens) produce the most accurate embedding matches, but large chunks (1000+ tokens) provide the LLM with sufficient context for synthesis. The <strong>Parent-Child pattern</strong> indexes small child chunks for vector search, but returns the parent container chunk to the LLM context window.
</p>""",

    139: """<h3 class="sh3">1. Vector Index Algorithms: HNSW vs. IVF vs. PQ</h3>
<p>
Vector databases balance three competing trade-offs: <strong>Query Latency</strong>, <strong>Recall Accuracy</strong>, and <strong>Memory (RAM) Footprint</strong>.
</p>
<div class="mermaid">
graph TD
  Index["Vector Index Families"] --> Flat["1. Flat / Exact Search\n(O(N) brute force, 100% recall, high latency)"]
  Index --> IVF["2. Inverted File (IVFFlat)\n(K-means Voronoi partitioning, medium RAM)"]
  Index --> HNSW["3. HNSW (Hierarchical Navigable Small World)\n(Multi-layer skip graph, >98% recall, high RAM)"]
  Index --> PQ["4. Product Quantization (PQ)\n(Vector compression, 4x-16x RAM savings, 85-92% recall)"]
</div>
<div class="diagram-cap">Taxonomy of Approximate Nearest Neighbor (ANN) Indexing Strategies.</div>

<h3 class="sh3">2. Hierarchical Navigable Small World (HNSW) Graphs</h3>
<p>
HNSW constructs a multi-layer graph where top layers have sparse, long-range connections for rapid routing, and bottom layers have dense, local connections for precise neighbor discovery (analogous to Skip Lists applied to multi-dimensional geometry).
</p>""",

    140: """<h3 class="sh3">1. GraphRAG: Knowledge Graphs for Complex Multi-Hop Reasoning</h3>
<p>
Standard vector RAG fails on global corpus questions like <em>"What are the main themes across all quarterly reports?"</em> or multi-hop relationship queries. <strong>GraphRAG</strong> extracts entity-relation-entity triples using LLMs, clusters them into communities via the Leiden algorithm, and generates hierarchical community summaries.
</p>
<div class="mermaid">
graph LR
  Docs["Document Chunks"] --> Extract["LLM Entity & Relationship Extraction"]
  Extract --> Graph["Knowledge Graph (Nodes & Edges)"]
  Graph --> Leiden["Leiden Community Detection"]
  Leiden --> Summaries["Hierarchical Community Summaries"]
  Summaries --> GlobalSearch["Global Multi-Hop Query Answering"]
</div>
<div class="diagram-cap">GraphRAG Architecture: Entity extraction, community detection, and hierarchical summary generation.</div>""",

    141: """<h3 class="sh3">1. Query Transformation & Expansion Techniques</h3>
<p>
User queries are often ambiguous, underspecified, or phrased differently than the source documents. Query transformation rewrites or decomposes the input before retrieval:
</p>
<div class="mermaid">
graph TD
  UserQ["Raw User Query"] --> Transform{"Transformation Strategy"}
  Transform --> Rewrite["Query Rewriting / Rephrasing"]
  Transform --> SubQ["Sub-Query Decomposition\n(Break complex query into 3 parallel searches)"]
  Transform --> HyDE["HyDE (Hypothetical Document Embeddings)\n(Generate hallucinated answer, embed that)"]
  Transform --> StepBack["Step-Back Prompting\n(Retrieve higher-level foundational concept)"]
</div>
<div class="diagram-cap">Advanced Query Transformation Strategies: HyDE, Sub-Query Decomposition, and Step-Back Prompting.</div>

<h3 class="sh3">2. Hypothetical Document Embeddings (HyDE)</h3>
<p>
HyDE prompts an instruction-tuned LLM to generate a hypothetical answer to the query. Even if factually imperfect, the hypothetical document shares the lexical and embedding structure of target documents far more closely than a terse question.
</p>""",

    142: """<h3 class="sh3">1. Production RAG Architecture: End-to-End Capstone</h3>
<p>
A complete, enterprise-ready RAG pipeline combines query transformation, hybrid retrieval, cross-encoder reranking, context compression, grounded answer generation, and real-time hallucination evaluation.
</p>
<div class="mermaid">
graph TD
  UserQ["User Query"] --> Transform["Query Rewriter & HyDE"]
  Transform --> Hybrid["Hybrid Search (BM25 + Dense Qdrant)"]
  Hybrid --> RRF["Reciprocal Rank Fusion (k=60)"]
  RRF --> Top100["Top 100 Candidates"]
  Top100 --> Rerank["Cross-Encoder Reranker"]
  Rerank --> Top5["Top 5 High-Precision Chunks"]
  Top5 --> Synth["LLM Generator (with Strict Grounding System Prompt)"]
  Synth --> Eval["RAGAS Evaluator (Faithfulness > 0.90)"]
  Eval --> Output["Verified Grounded Answer"]
</div>
<div class="diagram-cap">End-to-End Enterprise Production RAG System Topology with Automated Quality Gates.</div>"""
}
