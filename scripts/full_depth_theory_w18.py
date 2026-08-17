# scripts/full_depth_theory_w18.py
# Exhaustive, deep technical theory for Week 18 (Days 125 - 135)

W18_THEORY = {
    125: r"""<h3 class="sh3">1. Why Kubernetes for Machine Learning Deployments?</h3>
<p>
Modern machine learning models cannot run reliably on bare virtual machines in enterprise environments. Production AI systems require dynamic scaling, GPU resource sharing, automated health-checking, rolling zero-downtime updates, and fault tolerance. <strong>Kubernetes (K8s)</strong> serves as the industry standard container orchestrator that abstracts physical compute clusters into unified, declarative APIs.
</p>
<p>
In an ML deployment context, Kubernetes coordinates three core operations:
</p>
<ul>
  <li><strong>Inference Microservices:</strong> Packaging FastAPI/Triton/vLLM servers inside lightweight container Pods exposed behind ClusterIP and Ingress controllers.</li>
  <li><strong>GPU Scheduling & Isolation:</strong> Utilizing the NVIDIA GPU Device Plugin to allocate discrete GPU hardware slices (e.g. <code>nvidia.com/gpu: 1</code>) to specialized pods.</li>
  <li><strong>Horizontal Pod Autoscaling (HPA):</strong> Dynamically scaling pod replicas based on request concurrency, GPU memory saturation, and queue latency.</li>
</ul>
<div class="mermaid">
graph TD
    Client["Client / Application Gateway"] --> Ingress["K8s Ingress Controller (NGINX / Traefik)"]
    Ingress --> Service["K8s Service (ClusterIP: Load Balancer)"]
    Service --> Pod1["Pod 1: FastAPI + ONNX Runtime (GPU Node 1)"]
    Service --> Pod2["Pod 2: FastAPI + ONNX Runtime (GPU Node 1)"]
    Service --> Pod3["Pod 3: FastAPI + ONNX Runtime (GPU Node 2)"]
    Pod1 & Pod2 & Pod3 --> SharedVolume["Shared Persistent Volume (Model Weights Cache)"]
</div>
<div class="diagram-cap">Figure 125.1: Kubernetes ML Microservice Serving Architecture.</div>

<h3 class="sh3">2. Core Kubernetes Primitives for ML Engineers</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px;">Primitive</th>
      <th style="padding:8px;">Purpose</th>
      <th style="padding:8px;">ML Engineering Context</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Pod</strong></td>
      <td style="padding:8px;">Smallest deployable execution unit.</td>
      <td style="padding:8px;">Contains inference server container + optional sidecar (metrics exporter).</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Deployment</strong></td>
      <td style="padding:8px;">Declarative controller for stateless pod replicas.</td>
      <td style="padding:8px;">Manages rolling updates when model weights or API code change.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Service</strong></td>
      <td style="padding:8px;">Stable internal IP and DNS endpoint.</td>
      <td style="padding:8px;">Load balances requests across healthy model inference pods.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>ConfigMap / Secret</strong></td>
      <td style="padding:8px;">External configuration & encrypted credentials.</td>
      <td style="padding:8px;">Injects model paths, batch size settings, S3 keys, and Hugging Face tokens.</td>
    </tr>
  </tbody>
</table>

<h3 class="sh3">3. Production Kubernetes ML Deployment Manifest</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detection-api
  labels:
    app: fraud-detector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fraud-detector
  template:
    metadata:
      labels:
        app: fraud-detector
    spec:
      containers:
      - name: inference-engine
        image: enterprise-registry.io/ml/fraud-api:v2.1.0
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: "1"
          limits:
            memory: "8Gi"
            cpu: "4000m"
            nvidia.com/gpu: "1"
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory</code></pre>
</div>""",

    126: r"""<h3 class="sh3">1. PaaS vs Managed K8s: Selecting Deployment Targets</h3>
<p>
Deploying machine learning models to production requires choosing the right compute infrastructure tier. While large enterprises run dedicated Kubernetes clusters (EKS, GKE), early-stage products, internal tools, and agile prototypes benefit enormously from <strong>Platform-as-a-Service (PaaS)</strong> environments like <strong>Render</strong>, <strong>Railway</strong>, and <strong>Fly.io</strong>.
</p>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px;">Dimension</th>
      <th style="padding:8px;">PaaS (Render / Railway)</th>
      <th style="padding:8px;">Kubernetes (EKS / GKE)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Setup Overhead</strong></td>
      <td style="padding:8px;">Sub-10 minutes (Git push to deploy)</td>
      <td style="padding:8px;">Days to weeks (Cluster configuration, Helm, RBAC)</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Maintenance Cost</strong></td>
      <td style="padding:8px;">Zero infrastructure maintenance</td>
      <td style="padding:8px;">Requires dedicated Platform / DevOps engineers</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>GPU Sizing</strong></td>
      <td style="padding:8px;">Fixed tiers (e.g. A10G, T4)</td>
      <td style="padding:8px;">Full elasticity (Multi-node H100, spot instances)</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Best Fit</strong></td>
      <td style="padding:8px;">MVPs, internal APIs, standard Scikit/PyTorch models</td>
      <td style="padding:8px;">High-scale distributed LLM serving (10,000+ QPS)</td>
    </tr>
  </tbody>
</table>

<h3 class="sh3">2. Declarative Infrastructure as Code: <code>render.yaml</code></h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>services:
  - type: web
    name: ai-sentiment-service
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4
    plan: standard
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.8
      - key: MODEL_STAGE
        value: production
    healthCheckPath: /health</code></pre>
</div>""",

    127: r"""<h3 class="sh3">1. The MLOps Imperative: Solving Model Chaos</h3>
<p>
Without standardized MLOps practices, machine learning projects suffer from reproducibility crises: models trained in ephemeral Jupyter notebooks lack versioned dependencies, dataset hashes, and metric audit trails.
</p>
<p>
<strong>MLOps (Machine Learning Operations)</strong> bridges data science with software engineering by enforcing three core lifecycle pillars:
</p>
<div class="mermaid">
graph LR
    Pillar1["1. Experiment Tracking\n(Parameters, Loss Curves, Hardware Metrics)"] --> Pillar2["2. Model Registry\n(Versioned Artifacts, Lineage, Champion Aliases)"]
    Pillar2 --> Pillar3["3. Automated CI/CD & Deployment\n(Regression Tests, Containerization, Canary Rollouts)"]
</div>
<div class="diagram-cap">Figure 127.1: The Three Foundational Pillars of Enterprise MLOps.</div>

<h3 class="sh3">2. MLflow Tracking Architecture</h3>
<p>
<strong>MLflow</strong> standardizes experiment logging by separating metadata tracking from binary artifact storage:
</p>
<ul>
  <li><strong>Backend Store (SQL):</strong> Stores run IDs, timestamps, hyperparameter dictionaries, and scalar metric step histories in PostgreSQL or SQLite.</li>
  <li><strong>Artifact Store (Object Storage):</strong> Stores serialized model binaries (<code>.pt</code>, <code>.onnx</code>, <code>.joblib</code>), confusion matrices, and feature importance charts in AWS S3 or Google Cloud Storage.</li>
</ul>""",

    128: r"""<h3 class="sh3">1. Capstone Project Track Selection & Technical Architecture</h3>
<p>
A portfolio-grade AI/ML capstone project must demonstrate end-to-end engineering excellence across data modeling, algorithmic design, API serving, and infrastructure operations.
</p>
<div class="mermaid">
graph TD
    Client["Client Interface (Streamlit / Next.js)"] --> APIGateway["FastAPI Gateway (/predict, /health, /metrics)"]
    APIGateway --> Preprocessor["Feature Preprocessor (ColumnTransformer / Tokenizer)"]
    Preprocessor --> InferenceEngine["Model Inference Core (PyTorch / ONNX / vLLM)"]
    InferenceEngine --> Monitoring["Telemetry & Drift Monitoring (Evidently / OpenTelemetry)"]
    Monitoring --> Client
</div>
<div class="diagram-cap">Figure 128.1: Universal Capstone Microservice Architecture Blueprint.</div>

<h3 class="sh3">2. Recommended Industry Tracks</h3>
<ul>
  <li><strong>Track A (Enterprise RAG & Agents):</strong> Hybrid retrieval with Qdrant, Cross-Encoder reranking, and LangGraph cyclic workflows.</li>
  <li><strong>Track B (High-Throughput Serving & Fine-Tuning):</strong> QLoRA fine-tuning on custom corpora, merged weights, and vLLM continuous batching serving.</li>
  <li><strong>Track C (Production Predictive MLOps):</strong> Scikit-Learn / XGBoost fraud detection pipeline with DVC dataset versioning, MLflow registry promotion, and Airflow DAGs.</li>
</ul>""",

    129: r"""<h3 class="sh3">1. Production Preprocessing Pipelines</h3>
<p>
Data preprocessors must be versioned, fitted strictly on training data, and serialized alongside model weights to prevent <strong>training-serving skew</strong> and <strong>data leakage</strong>.
</p>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code><span class="kw">from</span> sklearn.compose <span class="kw">import</span> ColumnTransformer
<span class="kw">from</span> sklearn.pipeline <span class="kw">import</span> Pipeline
<span class="kw">from</span> sklearn.impute <span class="kw">import</span> SimpleImputer
<span class="kw">from</span> sklearn.preprocessing <span class="kw">import</span> StandardScaler, OneHotEncoder

num_pipe = Pipeline([
    (<span class="str">'imputer'</span>, SimpleImputer(strategy=<span class="str">'median'</span>)),
    (<span class="str">'scaler'</span>, StandardScaler())
])

cat_pipe = Pipeline([
    (<span class="str">'imputer'</span>, SimpleImputer(strategy=<span class="str">'most_frequent'</span>)),
    (<span class="str">'ohe'</span>, OneHotEncoder(handle_unknown=<span class="str">'ignore'</span>, sparse_output=<span class="kw">False</span>))
])

preprocessor = ColumnTransformer([
    (<span class="str">'num'</span>, num_pipe, [<span class="str">'age'</span>, <span class="str">'income'</span>, <span class="str">'tenure'</span>]),
    (<span class="str">'cat'</span>, cat_pipe, [<span class="str">'device_type'</span>, <span class="str">'region'</span>])
])</code></pre>
</div>""",

    130: r"""<h3 class="sh3">1. Packaging ML Models in FastAPI</h3>
<p>
FastAPI provides asynchronous request handling, automated OpenAPI documentation, and strict runtime type validation via Pydantic.
</p>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code><span class="kw">from</span> fastapi <span class="kw">import</span> FastAPI, HTTPException
<span class="kw">from</span> pydantic <span class="kw">import</span> BaseModel, Field
<span class="kw">import</span> joblib, numpy <span class="kw">as</span> np

app = FastAPI(title=<span class="str">"Production ML Inference Service"</span>)

<span class="kw">class</span> <span class="fn">PredictionRequest</span>(BaseModel):
    age: float = Field(..., ge=<span class="num">18</span>, le=<span class="num">100</span>)
    income: float = Field(..., ge=<span class="num">0</span>)
    tenure: int = Field(..., ge=<span class="num">0</span>)

@app.post(<span class="str">"/predict"</span>)
<span class="kw">def</span> <span class="fn">predict</span>(req: PredictionRequest):
    features = np.array([[req.age, req.income, req.tenure]])
    prob = float(<span class="num">1.0</span> / (<span class="num">1.0</span> + np.exp(-(<span class="num">0.05</span> * req.age - <span class="num">0.0001</span> * req.income))))
    <span class="kw">return</span> {<span class="str">"risk_probability"</span>: round(prob, <span class="num">4</span>), <span class="str">"decision"</span>: <span class="str">"HIGH_RISK"</span> <span class="kw">if</span> prob > <span class="num">0.5</span> <span class="kw">else</span> <span class="str">"NORMAL"</span>}</code></pre>
</div>""",

    131: r"""<h3 class="sh3">1. Full-Stack ML: Connecting UI with APIs</h3>
<p>
A complete ML system couples backend inference microservices with intuitive frontend interfaces (Streamlit, React/Next.js) capable of streaming token responses, visualizing confidence distributions, and rendering telemetry charts.
</p>""",

    132: r"""<h3 class="sh3">1. GitHub Repository Engineering Best Practices</h3>
<p>
Senior AI engineers structure repositories with clean separation of concerns:
</p>
<ul>
  <li><code>src/</code>: Application core logic, preprocessing pipelines, and model architecture definitions.</li>
  <li><code>configs/</code>: Declarative YAML configs decoupling hyperparameters from executable code.</li>
  <li><code>tests/</code>: Pytest unit tests, schema validation tests, and mock API tests.</li>
  <li><code>.github/workflows/</code>: Automated CI/CD pipelines enforcing linting, testing, and Docker builds.</li>
</ul>""",

    133: r"""<h3 class="sh3">1. Positioning AI/ML Engineering Competencies</h3>
<p>
Modern AI engineering roles demand both statistical/deep learning depth and production software engineering acumen. Highlighting observable infrastructure skills (Docker, Kubernetes, MLflow, vLLM, OpenTelemetry) demonstrates production readiness.
</p>""",

    134: r"""<h3 class="sh3">1. Technical Interview Review: Systems & Algorithms</h3>
<p>
Core interview review topics include bias-variance trade-offs, regularization mechanisms ($L_1$ sparsity vs $L_2$ shrinkage), self-attention computational complexity, and distributed training paradigms (Data Parallel, Tensor Parallel, Pipeline Parallel).
</p>""",

    135: r"""<h3 class="sh3">1. Mid-Course Milestone: MLOps Mastery</h3>
<p>
Congratulations on completing the first half of the curriculum! You have established complete mastery across mathematical foundations, classical algorithms, deep learning neural networks, and containerized MLOps deployments.
</p>"""
}
