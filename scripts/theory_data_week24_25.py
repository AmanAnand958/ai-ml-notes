"""
Theoretical content definitions for:
- Week 24: Production MLOps Pipelines (Days 171 - 177)
- Week 25: Kubernetes & Infrastructure for AI (Days 178 - 184)
"""

THEORY_WEEKS_24_25 = {
    # ═════════════════════════════════════════════════════════════════════
    # WEEK 24: PRODUCTION MLOPS PIPELINES (Days 171 - 177)
    # ═════════════════════════════════════════════════════════════════════
    171: """<h3 class="sh3">1. Enterprise MLflow Experiment Tracking Architecture</h3>
<p>
In production MLOps environments, MLflow operates as a decoupled client-server architecture. The <strong>Tracking Server</strong> coordinates run metadata stored in a relational database (PostgreSQL) and persists heavy model artifacts (weights, conda environments, evaluation plots) to cloud object storage (AWS S3, Google Cloud Storage, or Azure Blob).
</p>
<div class="mermaid">
graph LR
  Client["Training Client / Worker"] -->|HTTP REST / Log Params & Metrics| Server["MLflow Tracking Server"]
  Server -->|SQL Backend Store| DB["PostgreSQL Database (Run Metadata)"]
  Client -->|Direct S3 Upload| S3["S3 Artifact Root (model.pkl, plots)"]
  UI["MLflow Web Dashboard"] --> Server
</div>
<div class="diagram-cap">Decoupled MLflow Tracking Architecture: Relational Backend Metadata and Object Storage Artifact Root.</div>

<h3 class="sh3">2. Structured Run Logging & Autologging</h3>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — mlflow_production_tracking.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier

mlflow.set_tracking_uri("http://mlflow.internal.company.com:5000")
mlflow.set_experiment("fraud-detection-production")

with mlflow.start_run(run_name="gbm-v2-l2-reg"):
    mlflow.log_params({"n_estimators": 200, "learning_rate": 0.05, "subsample": 0.8})
    
    model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05)
    model.fit(X_train, y_train)
    
    mlflow.log_metrics({"val_accuracy": 0.962, "val_f1": 0.941})
    mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name="FraudClassifier")</code></pre>
</div>""",

    172: """<h3 class="sh3">1. MLflow Model Registry & Alias-Based Promotion</h3>
<p>
Traditional stage-based transitions (<em>Staging</em>, <em>Production</em>, <em>Archived</em>) have been modernized in MLflow 2.8+ with <strong>Model Aliases</strong> and <strong>Model Tags</strong>. Aliases like <code>@champion</code>, <code>@challenger</code>, and <code>@shadow</code> provide deterministic pointers to specific model versions without altering code dependencies.
</p>
<div class="mermaid">
graph TD
  Train["Training Run v12"] --> Register["Register as 'FraudClassifier' v12"]
  Register --> Eval{"Automated Evaluation Gate\n(AUC > Champion + 0.01)"}
  Eval -->|Pass| SetAlias["Assign Alias: @champion -> v12"]
  Eval -->|Fail| Tag["Tag as: status=evaluation_failed"]
  SetAlias --> Serving["Inference Pods Load: 'models:/FraudClassifier@champion'"]
</div>
<div class="diagram-cap">Alias-Based Model Promotion Workflow with Automated Quality Gates.</div>""",

    173: """<h3 class="sh3">1. Data Version Control (DVC) & Dataset Lineage</h3>
<p>
Git is designed for small text files; tracking multi-gigabyte training datasets directly in Git leads to repository bloat and slow operations. <strong>DVC (Data Version Control)</strong> computes cryptographic content hashes (md5) of large datasets, stores small <code>.dvc</code> pointer files in Git, and synchronizes raw data with cloud object storage.
</p>
<div class="mermaid">
graph LR
  LocalData["data/raw_training.parquet (12 GB)"] --> DVC["dvc add data/raw_training.parquet"]
  DVC --> Pointer["data/raw_training.parquet.dvc (Git Tracked)"]
  DVC --> Remote["S3 Remote Storage (dvc push)"]
  Pointer --> Git["Git Repository (Commit & PR)"]
</div>
<div class="diagram-cap">DVC Workflow: Versioning Large Datasets with Git Pointers and Cloud Remote Storage.</div>""",

    174: """<h3 class="sh3">1. ML Workflow Orchestration with Apache Airflow</h3>
<p>
Complex ML pipelines require scheduled batch retraining, data ingestion, feature validation, and model evaluation orchestrated as Directed Acyclic Graphs (<strong>DAGs</strong>). Apache Airflow manages task dependencies, retries on failure, and passes lightweight task state via XComs.
</p>
<div class="mermaid">
graph LR
  Extract["1. Extract New Batch (SQL/S3)"] --> Validate["2. Validate Data (Great Expectations)"]
  Validate --> Preprocess["3. Feature Engineering"]
  Preprocess --> Train["4. Distributed Training"]
  Train --> Eval["5. Model Evaluation Gate"]
  Eval --> Deploy["6. Deploy to Staging & Notify Slack"]
</div>
<div class="diagram-cap">Apache Airflow ML Retraining DAG Pipeline Architecture.</div>""",

    175: """<h3 class="sh3">1. Model & Data Drift Monitoring with Evidently AI</h3>
<p>
Once deployed, model accuracy degrades over time due to <strong>Data Drift</strong> (covariate shift $P(X)$ changes) and <strong>Concept Drift</strong> (conditional distribution $P(Y|X)$ changes). Continuous monitoring detects distribution shifts before business metrics decline.
</p>
<div class="mermaid">
graph TD
  Ref["Reference Data (Training Baseline)"] & Prod["Production Inference Requests (Live Stream)"] --> Detector["Evidently AI Drift Engine"]
  Detector --> KS["Kolmogorov-Smirnov Test (Numerical Drift, p < 0.05)"]
  Detector --> PSI["Population Stability Index (PSI > 0.20)"]
  KS & PSI --> Alert{"Drift Detected?"}
  Alert -->|Yes| Retrain["Trigger Airflow Retraining DAG & Alert On-Call"]
  Alert -->|No| Dashboard["Update Grafana Telemetry Dashboard"]
</div>
<div class="diagram-cap">Continuous Data and Concept Drift Detection Architecture with Automated Retraining Triggers.</div>""",

    176: """<h3 class="sh3">1. Canary Deployments & Statistical A/B Testing</h3>
<p>
Replacing production models all-at-once carries catastrophic failure risk. <strong>Canary deployments</strong> route a small percentage of live traffic (e.g. 5–10%) to the candidate model (Canary) while the incumbent model (Baseline) handles the remaining traffic. Performance is compared using two-sided statistical tests (Mann-Whitney U, Student's t-test).
</p>
<div class="mermaid">
graph TD
  Traffic["Incoming Inference Traffic"] --> Ingress["Ingress Router / API Gateway"]
  Ingress -->|90% Traffic| Baseline["Baseline Model v1.0 (Production)"]
  Ingress -->|10% Traffic| Canary["Canary Model v1.1 (Candidate)"]
  Baseline & Canary --> Telemetry["Metrics Collection (Latency, Error Rate, Conversion)"]
  Telemetry --> Test{"Statistically Significant Improvement? (p < 0.05)"}
  Test -->|Yes| Promote["Progressive Traffic Shift (10% -> 50% -> 100%)"]
  Test -->|No / Regression| Rollback["Instant Automated Rollback to Baseline"]
</div>
<div class="diagram-cap">Canary Traffic Routing and Automated Statistical Promotion Architecture.</div>""",

    177: """<h3 class="sh3">1. Capstone: End-to-End Enterprise MLOps Pipeline</h3>
<p>
Consolidating the full MLOps lifecycle: DVC data versioning, MLflow experiment tracking and model registry, Airflow automated retraining DAGs, Evidently drift detection, and automated canary deployments.
</p>
<div class="mermaid">
graph LR
  DVC["1. DVC Versioning"] --> Airflow["2. Airflow DAG"]
  Airflow --> MLflow["3. MLflow Tracking & Registry"]
  MLflow --> Canary["4. Canary Deployment"]
  Canary --> Evidently["5. Drift Monitoring"]
  Evidently -->|Drift Trigger| Airflow
</div>
<div class="diagram-cap">End-to-End Enterprise MLOps Continuous Training & Deployment Feedback Loop.</div>""",

    # ═════════════════════════════════════════════════════════════════════
    # WEEK 25: KUBERNETES & INFRASTRUCTURE FOR AI (Days 178 - 184)
    # ═════════════════════════════════════════════════════════════════════
    178: """<h3 class="sh3">1. Kubernetes Architecture for AI Engineers</h3>
<p>
Kubernetes coordinates distributed GPU computing across worker nodes via the Control Plane:
</p>
<ul>
  <li><strong>kube-apiserver:</strong> The central REST API gateway handling declarative YAML state requests.</li>
  <li><strong>etcd:</strong> Highly available distributed key-value store holding the entire cluster state.</li>
  <li><strong>kube-scheduler:</strong> Assigns pending Pods to worker nodes based on resource requests, GPU availability, and node affinities.</li>
  <li><strong>kubelet:</strong> Agent running on each worker node that ensures containers described in PodSpecs are running and healthy.</li>
  <li><strong>NVIDIA Device Plugin:</strong> Exposes GPU hardware accelerators to the kubelet as allocatable node resources (<code>nvidia.com/gpu</code>).</li>
</ul>
<div class="mermaid">
graph TD
  subgraph Control Plane
    API["kube-apiserver"] <--> etcd["etcd (Cluster State)"]
    API <--> Sched["kube-scheduler"]
    API <--> CM["kube-controller-manager"]
  end
  subgraph GPU Worker Node
    Kubelet["kubelet"] <--> API
    Kubelet --> Containerd["containerd Runtime"]
    Containerd --> Pod1["Pod: vLLM (1x NVIDIA A100)"]
    Containerd --> Pod2["Pod: Triton (1x NVIDIA L4)"]
  end
</div>
<div class="diagram-cap">Kubernetes Control Plane and GPU Worker Node Interaction Architecture.</div>""",

    179: """<h3 class="sh3">1. Deploying vLLM on Kubernetes with GPU Allocations</h3>
<p>
Running high-throughput LLM inference in production Kubernetes clusters requires explicit GPU resource requests, shared memory volume mounts (<code>/dev/shm</code> for PyTorch distributed IPC), and robust readiness probes.
</p>
<div class="cb">
<div class="cb-head"><span class="cb-lang">yaml — vllm-gpu-deployment.yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama3-serving
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm-model
  template:
    metadata:
      labels:
        app: vllm-model
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args: ["--model", "meta-llama/Meta-Llama-3-8B-Instruct", "--gpu-memory-utilization", "0.90"]
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: "1"
            memory: "32Gi"
            cpu: "8"
        volumeMounts:
        - mountPath: /dev/shm
          name: dshm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory</code></pre>
</div>""",

    180: """<h3 class="sh3">1. Horizontal Pod Autoscaling (HPA) for LLM Serving</h3>
<p>
Standard CPU/Memory metrics are inadequate for autoscaling LLM deployments because GPU inference runs at 100% VRAM utilization even during low traffic. The <strong>Kubernetes HPA</strong> must scale on custom metrics scraped from Prometheus, such as <code>vllm:num_requests_waiting</code> or <code>vllm:gpu_cache_usage_factor</code>.
</p>
<div class="mermaid">
graph LR
  vLLM["vLLM Model Pods (/metrics)"] -->|Scrape every 15s| Prom["Prometheus Operator"]
  Prom --> Adapter["Prometheus Adapter (Custom Metrics API)"]
  Adapter --> HPA["Horizontal Pod Autoscaler"]
  HPA -->|Scale Replicas (2 -> 6)| Deployment["vLLM Deployment"]
</div>
<div class="diagram-cap">Custom-Metric Horizontal Pod Autoscaling Architecture for vLLM Clusters.</div>""",

    181: """<h3 class="sh3">1. Helm Charts for Standardized ML Deployments</h3>
<p>
Managing multiple raw YAML manifests across development, staging, and production environments is repetitive and error-prone. <strong>Helm</strong> acts as the package manager for Kubernetes, templating deployment manifests with environment-specific <code>values.yaml</code> configurations.
</p>
<div class="mermaid">
graph TD
  Chart["Helm Chart Templates\n(deployment.yaml, service.yaml, hpa.yaml)"] --> Engine["Helm Template Engine"]
  ValsDev["values-dev.yaml\n(CPU only, 1 replica)"] --> Engine
  ValsProd["values-prod.yaml\n(A100 GPU, 4 replicas, HPA)"] --> Engine
  Engine --> Manifests["Rendered Kubernetes Manifests"]
  Manifests --> K8s["Target Kubernetes Cluster"]
</div>
<div class="diagram-cap">Helm Templating Pipeline: Transforming Parameterized Values into Environment Manifests.</div>""",

    182: """<h3 class="sh3">1. GitHub Actions CI/CD for Machine Learning</h3>
<p>
Automated CI/CD for ML guarantees that every Git pull request undergoes static analysis (linting), unit testing, data schema validation, model regression checks, container image building, and canary staging rollout.
</p>
<div class="mermaid">
graph LR
  PR["Git Pull Request"] --> Lint["Job 1: Lint & Format (Ruff / Black)"]
  Lint --> Unit["Job 2: Unit Tests (pytest)"]
  Unit --> DataVal["Job 3: Schema Validation (Great Expectations)"]
  DataVal --> Regress["Job 4: Model Accuracy Regression Gate"]
  Regress --> Build["Job 5: Docker Build & Push to ECR"]
  Build --> Deploy["Job 6: Helm Upgrade Staging Cluster"]
</div>
<div class="diagram-cap">Comprehensive 6-Stage GitHub Actions CI/CD Pipeline for Enterprise ML Repositories.</div>""",

    183: """<h3 class="sh3">1. Automated Model Performance Regression Testing</h3>
<p>
In continuous deployment pipelines, new model candidates must prove they do not regress on critical edge cases or drop overall accuracy before merging into production. Automated regression test suites compare candidate model metrics against baseline production benchmarks with strict tolerance thresholds ($\Delta < 1.0\%$).
</p>
<div class="mermaid">
graph TD
  Candidate["Candidate Model (PR #142)"] --> Benchmark["Run Golden Evaluation Test Suite"]
  Baseline["Baseline Model (Production @champion)"] --> Benchmark
  Benchmark --> Compare{"Candidate Metric >= Baseline - 0.01?"}
  Compare -->|Yes| Pass["CI Check Passed (Green)"]
  Compare -->|No| Fail["CI Check Failed (Block Merge & Report Regressed Slices)"]
</div>
<div class="diagram-cap">Automated Model Regression Testing Gate in Continuous Integration.</div>""",

    184: """<h3 class="sh3">1. Capstone: Production Kubernetes LLM Infrastructure</h3>
<p>
Bringing together all elements of enterprise AI infrastructure: Helm chart packaging, vLLM serving on NVIDIA GPUs, Prometheus custom metrics, Horizontal Pod Autoscaler, and GitHub Actions CI/CD deployment automation.
</p>
<div class="mermaid">
graph TD
  Git["Git Push / Release Tag"] --> CI["GitHub Actions CI/CD"]
  CI --> Helm["Helm Upgrade"]
  Helm --> Cluster["Kubernetes Production Cluster"]
  Cluster --> HPA["HPA (Autoscaling on Waiting Queue)"]
  HPA --> Pods["vLLM GPU Pod Replicas"]
  Pods --> Monitor["Prometheus & Grafana Observability"]
</div>
<div class="diagram-cap">Production End-to-End Kubernetes LLM Deployment and Autoscaling Architecture.</div>"""
}
