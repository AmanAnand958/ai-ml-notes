#!/usr/bin/env python3
"""
scripts/expand_milestones_w22_to_w26.py
Further expands milestone and architectural days across Weeks 22-26 to achieve 550-650+ average word count and natural variance.
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

ADDITIONAL_MILESTONE_THEORY = {
    157: """
<h3 class="sh3">Deep Dive: RAG Triad Metric Calculations</h3>
<p>
The RAG Triad consists of three orthogonal evaluation vectors:
1. <strong>Context Precision:</strong> Measures whether retrieved chunks are relevant to the query without introducing noise. Calculated via Mean Reciprocal Rank (MRR) or NDCG@k against human relevance judgments.
2. <strong>Faithfulness:</strong> Measures whether the generated answer relies exclusively on retrieved facts rather than parametric hallucinations.
3. <strong>Answer Relevance:</strong> Evaluates whether the generated response directly answers the user prompt without tangent drift.
</p>
""",
    163: """
<h3 class="sh3">Production Generative AI Incident Response & Runbooks</h3>
<p>
Operating generative AI microservices requires pre-configured incident runbooks:
- <strong>Prompt Injection Storms:</strong> Automatically rate-limit tenant API keys and switch downstream LLM temperature to 0.0 with strict system prompts.
- <strong>Provider Outages (OpenAI / Anthropic 503):</strong> Gateway circuit breaker shifts traffic to self-hosted vLLM fallback pods.
- <strong>Semantic Cache Pollution:</strong> Purges Redis VSS embedding index when corrupt or malicious responses are detected in cache entries.
</p>
""",
    164: """
<h3 class="sh3">AWS SageMaker Control Plane vs Data Plane Architecture</h3>
<p>
SageMaker strictly separates management from computation:
- <strong>Control Plane:</strong> Manages endpoint configurations, auto-scaling policies, and IAM execution roles.
- <strong>Data Plane:</strong> High-performance NVMe-backed EC2 instances running Triton / TorchServe containers inside isolated VPC security groups.
</p>
""",
    170: """
<h3 class="sh3">Cloud Migration & Enterprise Disaster Recovery (DR) Strategy</h3>
<p>
Multi-region cloud ML deployments maintain active-passive or active-active configurations:
- <strong>Cross-Region S3 Bucket Replication:</strong> Replicates model artifacts and feature stores between <code>us-east-1</code> and <code>eu-central-1</code> in $<15$ minutes.
- <strong>Route 53 Latency Routing:</strong> Directs inference traffic to the geographically closest healthy SageMaker endpoint.
</p>
""",
    171: """
<h3 class="sh3">MLflow Model Registry Lifecycle & Approval Gates</h3>
<p>
The MLflow Model Registry governs model progression across environment tiers:
- <strong>Staging:</strong> Automated integration tests evaluate latency, throughput, and statistical data validation suites.
- <strong>Production:</strong> Requires signed peer approvals and compliance audits before tagging the model as <code>@champion</code>.
- <strong>Archived:</strong> Deprecated models retained for auditability and regulatory compliance.
</p>
""",
    177: """
<h3 class="sh3">Production Retraining DAGs & Automated Model Rollbacks</h3>
<p>
When Evidently AI detects statistical drift (PSI $> 0.2$), Apache Airflow triggers an automated retraining DAG:
1. Extracts fresh 30-day feature slices from Snowflake / BigQuery.
2. Executes distributed training with Optuna hyperparameter optimization.
3. Compares new candidate against production champion on a locked golden evaluation dataset.
4. Automatically promotes candidate if F1-score improves by $\ge 1.5\%$ without regression in p95 latency.
</p>
""",
    178: """
<h3 class="sh3">Kubernetes Cluster Architecture for Machine Learning</h3>
<p>
A production ML Kubernetes cluster isolates workloads into distinct node pools:
- <strong>CPU System Node Pool:</strong> Runs Ingress controllers, Prometheus, and Grafana (c6i.2xlarge).
- <strong>GPU Inference Node Pool:</strong> Runs vLLM and TensorRT-LLM pods on spot/on-demand instances (g5.2xlarge).
- <strong>GPU Training Node Pool:</strong> Runs multi-node DDP jobs on InfiniBand-connected clusters (p4d.24xlarge).
</p>
""",
    184: """
<h3 class="sh3">Enterprise Kubernetes ML Platform Engineering Review</h3>
<p>
Production Kubernetes AI platforms must enforce strict resource quotas:
- <strong>ResourceQuotas & LimitRanges:</strong> Prevents a single tenant from starving cluster GPU allocations.
- <strong>PodDisruptionBudgets (PDB):</strong> Guarantees minimum available inference replicas during cluster node upgrades.
- <strong>NetworkPolicies:</strong> Restricts inter-pod traffic to authorized microservice namespaces.
</p>
""",
    185: """
<h3 class="sh3">Vision Transformer (ViT) Patch Tokenization Mathematical Formulation</h3>
<p>
ViT decomposes a 2D image $\mathbf{X} \in \mathbb{R}^{H \times W \times C}$ into a sequence of non-overlapping patches $\mathbf{x}_p \in \mathbb{R}^{N \times (P^2 C)}$, where $P$ is patch resolution (e.g. $14 \times 14$) and $N = \frac{HW}{P^2}$ is token count:
</p>
<div class="math-block">
$$\mathbf{z}_0 = \left[ \mathbf{x}_{\text{class}}; \, \mathbf{x}_p^1 \mathbf{E}; \, \mathbf{x}_p^2 \mathbf{E}; \, \dots; \, \mathbf{x}_p^N \mathbf{E} \right] + \mathbf{E}_{\text{pos}}$$
</div>
<p>
Linear projection matrix $\mathbf{E}$ maps each flattened patch into the Transformer hidden dimension $D$.
</p>
""",
    186: """
<h3 class="sh3">ColPali Late Interaction vs Single-Vector Dense Retrieval</h3>
<p>
Single-vector multimodal models compress an entire image into a single 1024D vector, losing fine-grained document details (tables, chart axes, captions). ColPali retains all 576 visual patch token embeddings and computes late interaction via MaxSim:
</p>
<div class="math-block">
$$\text{Score}(Q, D) = \sum_{i=1}^{|Q|} \max_{j=1}^{|D|} \left( \vec{q}_i \cdot \vec{d}_j \right)$$
</div>
<p>
This preserves spatial grounding and enables indexing complex PDF documents without OCR preprocessing pipelines.
</p>
""",
    191: """
<h3 class="sh3">Final Master Capstone: Principal AI Engineering System Design Checklist</h3>
<p>
Assembling the master portfolio capstone requires demonstrating end-to-end mastery:
1. <strong>Data & Ingestion:</strong> Multimodal ColPali vector indexing and hybrid BM25 + Dense RRF fusion.
2. <strong>Serving & Optimization:</strong> vLLM engine with PagedAttention and FP8 / INT4 AWQ quantization.
3. <strong>Agentic Routing:</strong> LangGraph multi-agent supervisors with cyclic state validation and human approval gates.
4. <strong>Infrastructure & Telemetry:</strong> Kubernetes GPU autoscaling, OpenTelemetry GenAI spans, and automated drift alerting.
</p>
"""
}

for w in range(22, 27):
    fpath = f"{DATA_DIR}/week{w:02d}.yaml"
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)
    
    for d in data.get('days', []):
        did = d['id']
        if did in ADDITIONAL_MILESTONE_THEORY:
            d['theory_html'] += "\n" + ADDITIONAL_MILESTONE_THEORY[did].strip()
            print(f"  ✓ Deeply expanded Day {did:03d} in Week {w:02d}")
            
    save_yaml(fpath, data)

print("\n✓ Milestone theory expansion complete!")
