# scripts/curriculum_data_w23_w24.py
# Exhaustive pedagogical theory & task prompts for Weeks 23 & 24 (Days 164 - 177)

CURRICULUM_W23_W24 = {
    # ── DAY 164: AWS SageMaker — Training & Endpoints ──
    164: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> You are setting up a cost-effective, automated deep learning training and real-time inference architecture on AWS SageMaker for an e-commerce recommendation model.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Configure a <strong>SageMaker PyTorch Estimator</strong> with Managed Spot Training (spot_instance=True) and automated S3 checkpoint saving.</li>
  <li>Deploy a <strong>Real-Time SageMaker Endpoint</strong> with multi-model hosting (MME) and target-tracking auto-scaling policies.</li>
  <li>Catch SIGTERM signals in training loops to guarantee zero loss of model weights upon spot instance reclamation.</li>
</ul>"""
        ]
    },

    # ── DAY 165: GCP Vertex AI ──
    165: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build and compile an end-to-end serverless ML pipeline on Google Cloud Vertex AI using the Kubeflow Pipelines (KFP) SDK.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Define containerized KFP components for: BigQuery data extraction, schema validation, distributed training, and Vertex Model Registry upload.</li>
  <li>Compile pipeline to JSON/YAML format and submit execution to Vertex AI Pipelines.</li>
  <li>Track artifact lineage and hyperparameter metrics automatically in Vertex ML Metadata.</li>
</ul>"""
        ]
    },

    # ── DAY 166: Serverless ML with Lambda + API Gateway ──
    166: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Deploy a lightweight text classification model to AWS Lambda behind Amazon API Gateway to achieve zero idle compute costs for an intermittent webhook service.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Convert a PyTorch transformer model to optimized <strong>ONNX Runtime</strong> format with INT8 dynamic quantization.</li>
  <li>Package inference logic into a containerized AWS Lambda function with <code>/tmp</code> model caching.</li>
  <li>Assert cold-start latency &lt; 150ms and warm inference latency &lt; 25ms.</li>
</ul>"""
        ]
    },

    # ── DAY 167: Azure OpenAI Service ──
    167: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Architect a secure, HIPAA-compliant enterprise AI deployment on Azure OpenAI Service for a healthcare network.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Configure <strong>Private Endpoints and Virtual Network (VNet) Peering</strong> to completely block public internet access.</li>
  <li>Implement Azure Active Directory / Entra ID <strong>Managed Identity RBAC authentication</strong> to eliminate static API keys.</li>
  <li>Configure Provisioned Throughput Units (PTU) with latency SLA monitoring.</li>
</ul>"""
        ]
    },

    # ── DAY 168: Cloud Cost Optimization for LLMs ──
    168: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement a FinOps Multi-Tier Model Cascading router that cuts monthly enterprise LLM API expenditure by 75%.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Train a lightweight query complexity classifier (FastText / DistilBERT).</li>
  <li>Route 80% of routine factual lookups to SLMs ($0.15/1M tokens) and 20% of complex reasoning tasks to frontier models ($5.00/1M tokens).</li>
  <li>Compute exact cost savings and benchmark accuracy equivalence against 100% frontier routing.</li>
</ul>"""
        ]
    },

    # ── DAY 169: Secrets Management ──
    169: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Secure an enterprise ML serving cluster by replacing all hardcoded credentials and static <code>.env</code> files with dynamic runtime secrets management.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Integrate <strong>AWS Secrets Manager / HashiCorp Vault</strong> SDK into your FastAPI application.</li>
  <li>Implement in-memory secrets caching with automated 30-day credential rotation handling.</li>
  <li>Add automated pre-commit scanning hooks (TruffleHog / GitGuardian) to block accidental credential commits.</li>
</ul>"""
        ]
    },

    # ── DAY 170: Capstone: Deploy RAG to AWS ──
    170: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Deploy an enterprise-grade production RAG application to AWS using ECS Fargate, Qdrant Vector DB, Amazon Bedrock, and CloudFront.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Write CloudFormation / Terraform infrastructure-as-code blueprints.</li>
  <li>Deploy containerized FastAPI service on Amazon ECS Fargate with Application Load Balancer.</li>
  <li>Verify end-to-end HTTPS request flow and secrets injection.</li>
</ul>"""
        ]
    },

    # ── DAY 171: MLflow Experiment Tracking ──
    171: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Set up a centralized, multi-tenant MLflow Tracking Server for an engineering team conducting parallel hyperparameter sweeps.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Configure MLflow tracking with PostgreSQL relational backend and AWS S3 artifact storage.</li>
  <li>Log hyperparameter dictionaries, learning rate step curves, confusion matrices, and serialized ONNX model binaries.</li>
  <li>Query the MLflow API programmatically to retrieve the best-performing run based on validation F1 score.</li>
</ul>"""
        ]
    },

    # ── DAY 172: MLflow Model Registry & Aliases ──
    172: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement a production model governance workflow using modern MLflow Model Aliases (<code>@champion</code>, <code>@challenger</code>).</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Register a newly trained model version in the MLflow Model Registry.</li>
  <li>Compare challenger accuracy against champion model on golden evaluation datasets.</li>
  <li>Promote the challenger model by reassigning the <code>@champion</code> alias via the MLflow Client API without downtime.</li>
</ul>"""
        ]
    },

    # ── DAY 173: Data Version Control (DVC) ──
    173: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Establish reproducible, Git-backed dataset versioning for a 50GB computer vision training dataset using Data Version Control (DVC).</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Initialize DVC in your repository and configure an S3 remote storage backend.</li>
  <li>Track large data directories with <code>dvc add</code>, generating <code>.dvc</code> pointer files committed to Git.</li>
  <li>Demonstrate seamless switching between dataset versions across Git branches using <code>dvc checkout</code>.</li>
</ul>"""
        ]
    },

    # ── DAY 174: Apache Airflow ML Orchestration ──
    174: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build an automated daily model retraining and evaluation DAG in Apache Airflow for a fraud detection system.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Construct an Airflow DAG with tasks: <code>extract_data</code> $\to$ <code>validate_schema</code> $\to$ <code>train_model</code> $\to$ <code>eval_gate</code> $\to$ <code>promote_registry</code>.</li>
  <li>Implement conditional branching: promote to <code>@champion</code> only if PR-AUC &gt; 0.92; trigger Slack alert if evaluation fails.</li>
  <li>Configure automated retries with exponential backoff on task failures.</li>
</ul>"""
        ]
    },

    # ── DAY 175: Model & Data Drift Monitoring ──
    175: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a production feature drift detection service using Evidently AI and Population Stability Index (PSI) monitoring.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Calculate Kolmogorov-Smirnov (KS) statistic for continuous numerical features.</li>
  <li>Compute <strong>Population Stability Index (PSI)</strong> across 10 quantile bins: $\text{PSI} = \sum (\text{Act}_i - \text{Exp}_i) \ln(\text{Act}_i / \text{Exp}_i)$.</li>
  <li>Trigger automated Airflow retraining webhooks when feature $\text{PSI} > 0.20$.</li>
</ul>"""
        ]
    },

    # ── DAY 176: Canary Deployments & A/B Testing ──
    176: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement a statistical Canary Deployment routing proxy that sends 10% of production traffic to a challenger recommendation model.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement deterministic user-hash traffic splitting (90% champion, 10% canary).</li>
  <li>Perform live hypothesis testing (Welch's t-test on latency, Chi-Square test on conversion rates).</li>
  <li>Assert automated rollback if error rate on canary exceeds 1.0% with $p < 0.01$.</li>
</ul>"""
        ]
    },

    # ── DAY 177: Capstone: Enterprise MLOps Pipeline ──
    177: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build and test a full-loop Enterprise MLOps Pipeline unifying DVC, MLflow, Airflow, Evidently AI, and Canary Deployments.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Execute end-to-end cycle: dataset update $\to$ DVC hash $\to$ Airflow retraining $\to$ MLflow logging $\to$ Drift evaluation $\to$ Canary rollout.</li>
  <li>Verify zero downtime and automated governance approval logs.</li>
</ul>"""
        ]
    }
}
