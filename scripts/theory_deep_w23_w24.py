# scripts/theory_deep_w23_w24.py
# Deep theory for all 14 days in Weeks 23 and 24

W23_W24_THEORY = {
    # ── DAY 164: AWS SageMaker — Training & Endpoints ──
    164: r"""<h3 class="sh3">1. AWS SageMaker Architecture for Production ML</h3>
<p>
Amazon SageMaker decouples model development, distributed training, and real-time inference into managed serverless primitives:
</p>
<div class="mermaid">
graph TD
    Code["Training Script / Container"] --> Estimator["SageMaker PyTorch Estimator"]
    Estimator --> SpotInstances["Managed GPU Spot Instances (70% Cost Savings)"]
    SpotInstances --> S3Artifacts["Model Artifacts (.tar.gz -> S3)"]
    S3Artifacts --> ModelRegistry["SageMaker Model Registry"]
    ModelRegistry --> EndpointConfig["Endpoint Configuration (Production Variants)"]
    EndpointConfig --> RealTimeEndpoint["Real-Time Multi-Model Endpoint (Auto-scaling)"]
</div>
<div class="diagram-cap">Figure 164.1: AWS SageMaker Training & Deployment Lifecycle.</div>""",

    # ── DAY 165: GCP Vertex AI ──
    165: r"""<h3 class="sh3">1. Google Cloud Vertex AI Custom Pipelines</h3>
<p>
Vertex AI orchestrates ML pipelines using <strong>Kubeflow Pipelines (KFP)</strong> compiled into serverless execution graphs. Every component runs in an isolated container with automated lineage tracking in Vertex Metadata.
</p>""",

    # ── DAY 166: Serverless ML with Lambda + API Gateway ──
    166: r"""<h3 class="sh3">1. Serverless ONNX Runtime Inference</h3>
<p>
For intermittent or bursty ML workloads, provisioning 24/7 GPU instances wastes thousands of dollars in idle compute.
</p>
<p>
<strong>Serverless ML Architecture:</strong> Compiles models to <strong>ONNX Runtime</strong> and packages them into containerized AWS Lambda functions (up to 10GB RAM), fronted by API Gateway with sub-100ms cold starts and zero idle cost.
</p>""",

    # ── DAY 167: Azure OpenAI Service ──
    167: r"""<h3 class="sh3">1. Enterprise Azure OpenAI Architecture</h3>
<p>
Deploying enterprise GenAI on Azure ensures enterprise compliance through:
</p>
<ul>
  <li><strong>Private Endpoints & VNet Peering:</strong> Disables public internet ingress.</li>
  <li><strong>Managed Identity & Azure RBAC:</strong> Eliminates static API keys.</li>
  <li><strong>Provisioned Throughput Units (PTU):</strong> Guarantees dedicated model capacity and consistent sub-second latency SLAs.</li>
</ul>""",

    # ── DAY 168: Cloud Cost Optimization for LLMs ──
    168: r"""<h3 class="sh3">1. FinOps for GenAI: Model Cascading</h3>
<p>
Sending all queries to frontier models ($5.00/1M tokens) is economically unsustainable. <strong>Model Cascading</strong> uses an inexpensive small model or classifier to route 80% of routine categorization and factual lookups to SLMs ($0.15/1M tokens), reducing cloud API expenditure by over 70%.
</p>""",

    # ── DAY 169: Secrets Management ──
    169: r"""<h3 class="sh3">1. Secrets Governance & Zero Hardcoded Credentials</h3>
<p>
Never bake API keys or database passwords into Docker images or Git repositories. Production platforms dynamically inject credentials at runtime using <strong>AWS Secrets Manager</strong> or <strong>HashiCorp Vault</strong> with automatic rotation.
</p>""",

    # ── DAY 170: Capstone: Deploy RAG to AWS ──
    170: r"""<h3 class="sh3">1. Enterprise AWS RAG Architecture Capstone</h3>
<p>
The Week 23 Capstone provisions a production RAG stack on AWS using ECS Fargate, Qdrant vector database, Bedrock Claude-3.5-Sonnet models, and CloudFront CDN security.
</p>""",

    # ── DAY 171: MLflow Experiment Tracking ──
    171: r"""<h3 class="sh3">1. MLflow Experiment Tracking Architecture</h3>
<p>
MLflow decouples metadata tracking (PostgreSQL backend) from serialized model artifact storage (AWS S3 / GCS), providing full lineage tracking for every training run.
</p>
<div class="mermaid">
graph TD
    Client["Training Script"] --> MLflowServer["MLflow Tracking Server"]
    MLflowServer --> Postgres["PostgreSQL (Params, Metrics, Tags)"]
    MLflowServer --> S3["S3 (Model Artifacts, ONNX)"]
    MLflowServer --> Registry["Model Registry (@champion / @challenger)"]
</div>
<div class="diagram-cap">Figure 171.1: Production MLflow Tracking Architecture.</div>""",

    # ── DAY 172: MLflow Model Registry & Aliases ──
    172: r"""<h3 class="sh3">1. Modern MLflow Model Aliases</h3>
<p>
MLflow 2.8+ model aliases (<code>@champion</code>, <code>@challenger</code>) decouple inference microservices from version numbers, allowing instant point-and-click promotions via immutable URIs (<code>models:/FraudModel@champion</code>).
</p>""",

    # ── DAY 173: Data Version Control (DVC) ──
    173: r"""<h3 class="sh3">1. Git-Backed Dataset Versioning with DVC</h3>
<p>
Git cannot store gigabyte-scale datasets without bloating repository history. <strong>Data Version Control (DVC)</strong> generates lightweight <code>.dvc</code> pointer files tracked in Git, while syncing actual large datasets to remote object storage (S3 / GCS).
</p>""",

    # ── DAY 174: ML Workflow Orchestration with Airflow ──
    174: r"""<h3 class="sh3">1. Apache Airflow DAGs for Automated Retraining</h3>
<p>
Airflow orchestrates end-to-end ML pipelines: data extraction $\to$ schema validation $\to$ distributed training $\to$ model evaluation gate $\to$ registry promotion.
</p>""",

    # ── DAY 175: Model & Data Drift Monitoring ──
    175: r"""<h3 class="sh3">1. Statistical Drift Detection: KS-Test & PSI</h3>
<p>
Monitor live production features using Kolmogorov-Smirnov (KS) tests for continuous variables and Population Stability Index (PSI) for discrete distributions:
</p>
<div class="math-block">
$$\text{PSI} = \sum_{i=1}^B (\text{Act}_i - \text{Exp}_i) \times \ln\left( \frac{\text{Act}_i}{\text{Exp}_i} \right)$$
</div>
<p>
$\text{PSI} > 0.20$ triggers automated Airflow retraining DAGs.
</p>""",

    # ── DAY 176: Canary Deployments & Statistical A/B Testing ──
    176: r"""<h3 class="sh3">1. Zero-Downtime Canary Rollouts</h3>
<p>
Route 5-10% of live traffic to challenger models. Use statistical hypothesis testing (Welch's t-test / Chi-square) to detect conversion or latency regressions before 100% cutover.
</p>""",

    # ── DAY 177: Capstone: End-to-End Enterprise MLOps ──
    177: r"""<h3 class="sh3">1. Full-Loop Enterprise MLOps Pipeline</h3>
<p>
The Week 24 Capstone integrates DVC dataset tracking, MLflow experiment logging, Airflow DAG scheduling, Evidently AI drift monitoring, and automated canary deployments.
</p>"""
}

print(f"Loaded {len(W23_W24_THEORY)} comprehensive theory modules for Weeks 23 & 24.")
