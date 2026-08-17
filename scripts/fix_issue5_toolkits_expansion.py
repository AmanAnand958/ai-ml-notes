#!/usr/bin/env python3
"""
scripts/fix_issue5_toolkits_expansion.py
Fixes Issue 5: Expands toolkit.content_html for Weeks 20, 22, 23, 24, 25, 26
up to 2,800–3,600 characters each, matching the depth and structure of Week 18/Week 19.
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

EXPANDED_TOOLKITS = {}

# ─────────────────────────────────────────────────────────────────────
# WEEK 20 TOOLKIT (LLM Agents & Multi-Agent Systems)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[20] = {
    'title': 'Master Toolkit: Autonomous LLM Agents & Multi-Agent Orchestration',
    'subtitle': 'LangGraph cyclic state machines, dynamic multi-agent supervisors, and Pydantic tool schemas.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Autonomous LLM Agents & Multi-Agent Workflows</h2>
<p>
Essential production recipes, cyclic graph definitions, and tool schemas for orchestrating enterprise agentic workflows.
</p>

<h3 class="sh3">1. Production LangGraph State Machine with Checkpointer</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — agent_graph_state.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    messages: Annotated[List[Dict[str, str]], operator.add]
    next_step: str
    tool_outputs: Dict[str, Any]
    iteration_count: int

def route_next_node(state: AgentState) -> str:
    \"\"\"Dynamic conditional edge routing based on tool output validation.\"\"\"
    if state["iteration_count"] >= 5:
        return "human_fallback_gate"
    if "error" in state.get("tool_outputs", {}):
        return "reflection_node"
    if state["next_step"] == "FINISH":
        return "__end__"
    return "execute_tools"</code></pre>
</div>

<h3 class="sh3">2. Pydantic v2 Structured Tool Schema with Type Coercion</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — structured_tool_schema.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>from pydantic import BaseModel, Field
from typing import Literal, Optional

class SQLDatabaseQuerySchema(BaseModel):
    query: str = Field(description="Syntactically valid PostgreSQL SELECT query string")
    max_rows: int = Field(default=50, ge=1, le=1000, description="Row limit to prevent memory buffer overflows")
    timeout_seconds: float = Field(default=3.0, description="Execution timeout for long-running analytical queries")
    dialect: Literal["postgres", "snowflake", "bigquery"] = Field(default="postgres")

def execute_validated_sql(args: SQLDatabaseQuerySchema) -> dict:
    \"\"\"Executes database query protected by strict schema constraints.\"\"\"
    print(f"Executing query on {args.dialect} with limit={args.max_rows}...")
    return {"status": "SUCCESS", "rows": []}</code></pre>
</div>

<h3 class="sh3">3. Hierarchical Supervisor Dynamic Agent Router</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — supervisor_router.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>class MultiAgentSupervisor:
    \"\"\"Central planner delegating tasks across specialized domain worker agents.\"\"\"
    def __init__(self, workers: Dict[str, Any]):
        self.workers = workers

    def route_task(self, user_intent: str) -> str:
        if "sql" in user_intent.lower() or "database" in user_intent.lower():
            return "sql_analyst_agent"
        elif "search" in user_intent.lower() or "retrieval" in user_intent.lower():
            return "rag_retrieval_agent"
        elif "code" in user_intent.lower() or "script" in user_intent.lower():
            return "python_coder_agent"
        return "general_reasoner_agent"</code></pre>
</div>"""
}

# ─────────────────────────────────────────────────────────────────────
# WEEK 22 TOOLKIT (LLM Eval, Observability & Guardrails)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[22] = {
    'title': 'Master Toolkit: LLM Evaluation, Observability & Guardrails Suite',
    'subtitle': 'RAGAS metric runners, OpenTelemetry GenAI exporters, and Redis semantic caching engines.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Enterprise LLM Evaluation & Telemetry</h2>
<p>
Essential tools, metrics definitions, and telemetry exporters for maintaining production generative AI reliability.
</p>

<h3 class="sh3">1. Custom OpenTelemetry GenAI Span Exporter</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — otel_genai_tracer.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import time
from contextlib import contextmanager

class GenAITracer:
    \"\"\"Lightweight OpenTelemetry-compatible GenAI Span Context Manager.\"\"\"
    def __init__(self, trace_id: str):
        self.trace_id = trace_id

    @contextmanager
    def span(self, name: str, attributes: dict = None):
        start = time.perf_counter()
        span_data = {"name": name, "trace_id": self.trace_id, "start": start, "attributes": attributes or {}}
        try:
            yield span_data
        finally:
            end = time.perf_counter()
            span_data["duration_ms"] = round((end - start) * 1000, 2)
            print(f"[OTel Trace] {name} completed in {span_data['duration_ms']}ms | Attrs: {span_data['attributes']}")</code></pre>
</div>

<h3 class="sh3">2. Redis Vector Similarity Semantic Cache Engine</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — redis_semantic_cache.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import numpy as np
from typing import Optional, Dict

class RedisSemanticCache:
    def __init__(self, threshold: float = 0.94):
        self.threshold = threshold
        self.cache: Dict[str, dict] = {}

    def get(self, query_emb: np.ndarray) -> Optional[str]:
        for key, entry in self.cache.items():
            stored_emb = entry["embedding"]
            sim = np.dot(query_emb, stored_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(stored_emb) + 1e-9)
            if sim >= self.threshold:
                print(f"⚡ Semantic Cache Hit (Score: {sim:.4f})")
                return entry["response"]
        return None

    def put(self, query_text: str, query_emb: np.ndarray, response: str):
        self.cache[query_text] = {"embedding": query_emb, "response": response}</code></pre>
</div>

<h3 class="sh3">3. Evaluation Metric Cheat Sheet</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px;">Metric</th>
      <th style="padding:8px;">Target Evaluation Dimension</th>
      <th style="padding:8px;">Evaluation Mechanism</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Faithfulness</strong></td>
      <td style="padding:8px;">Factual hallucinations</td>
      <td style="padding:8px;">LLM-as-a-judge claim extraction mapped to retrieved context.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Answer Relevance</strong></td>
      <td style="padding:8px;">Topic drift / Redundancy</td>
      <td style="padding:8px;">Cosine similarity of synthetic reverse-generated questions to original prompt.</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Context Precision</strong></td>
      <td style="padding:8px;">Rank quality in vector search</td>
      <td style="padding:8px;">Mean Average Precision (mAP) of relevant chunks in top-k retrieval.</td>
    </tr>
  </tbody>
</table>"""
}

# ─────────────────────────────────────────────────────────────────────
# WEEK 23 TOOLKIT (Cloud AI Services & SageMaker)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[23] = {
    'title': 'Master Toolkit: Cloud AI Services & FinOps Architecture Suite',
    'subtitle': 'SageMaker Boto3 deployment scripts, AWS Lambda ONNX templates, and FinOps budgeting alarms.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Cloud AI Infrastructure & FinOps</h2>
<p>
Automated cloud deployment blueprints for enterprise model serving, serverless inference, and cost governance.
</p>

<h3 class="sh3">1. AWS SageMaker Boto3 Endpoint Deployment Script</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — deploy_sagemaker_endpoint.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import boto3

def create_sagemaker_realtime_endpoint(
    model_name: str,
    s3_model_tar: str,
    role_arn: str,
    image_uri: str,
    instance_type: str = "ml.g5.xlarge"
):
    sm_client = boto3.client("sagemaker")
    
    # 1. Create Model
    sm_client.create_model(
        ModelName=model_name,
        PrimaryContainer={"Image": image_uri, "ModelDataUrl": s3_model_tar},
        ExecutionRoleArn=role_arn
    )
    
    # 2. Create Endpoint Config
    config_name = f"{model_name}-config"
    sm_client.create_endpoint_config(
        EndpointConfigName=config_name,
        ProductionVariants=[{
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": instance_type,
            "InitialVariantWeight": 1.0
        }]
    )
    
    # 3. Create Live Endpoint
    endpoint_name = f"{model_name}-endpoint"
    sm_client.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=config_name)
    print(f"✓ SageMaker endpoint '{endpoint_name}' creation initiated.")</code></pre>
</div>

<h3 class="sh3">2. Serverless AWS Lambda ONNX Inference Handler</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — lambda_onnx_handler.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import json
import numpy as np

def lambda_handler(event, context):
    \"\"\"Serverless inference handler executing ONNX Runtime model.\"\"\"
    try:
        body = json.loads(event.get("body", "{}"))
        input_data = np.array(body.get("inputs", []), dtype=np.float32)
        
        # Fast memory-mapped ONNX inference
        output = input_data * 1.5 + 0.2 # Placeholder execution graph
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"predictions": output.tolist(), "latency_ms": 14.2})
        }
    except Exception as err:
        return {"statusCode": 500, "body": json.dumps({"error": str(err)})}</code></pre>
</div>

<h3 class="sh3">3. Cloud FinOps Cost Optimization Decision Matrix</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px;">Inference Pattern</th>
      <th style="padding:8px;">Optimal AWS Resource</th>
      <th style="padding:8px;">Cost Savings vs On-Demand</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Unpredictable Bursts</strong></td>
      <td style="padding:8px;">AWS Lambda Serverless Inference</td>
      <td style="padding:8px;">Up to 70% (Zero idle cost)</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Steady 24/7 Traffic</strong></td>
      <td style="padding:8px;">SageMaker Savings Plans (3-Yr)</td>
      <td style="padding:8px;">50% — 64% Discount</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Batch Offline Scoring</strong></td>
      <td style="padding:8px;">SageMaker Transform on Spot GPU</td>
      <td style="padding:8px;">70% — 85% Discount</td>
    </tr>
  </tbody>
</table>"""
}

# ─────────────────────────────────────────────────────────────────────
# WEEK 24 TOOLKIT (Production MLOps & CI/CD Pipelines)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[24] = {
    'title': 'Master Toolkit: Production MLOps & CI/CD Pipeline Suite',
    'subtitle': 'MLflow tracking servers, DVC AWS S3 remote storage configurations, and Airflow retraining DAGs.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Production MLOps & CI/CD Pipelines</h2>
<p>
Reproducible data version control, experiment tracking, automated drift monitors, and continuous deployment workflows.
</p>

<h3 class="sh3">1. DVC AWS S3 Remote Storage Commands</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">bash — dvc_commands.sh</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code># Initialize DVC in git repository
dvc init

# Configure S3 Content-Addressable Storage
dvc remote add -d s3remote s3://my-enterprise-mlops-bucket/dvcstore
dvc remote modify s3remote region us-east-1

# Track 10GB dataset with pointer file
dvc add data/raw_features.parquet
git add data/raw_features.parquet.dvc .gitignore
git commit -m "chore(data): version raw features v1.4"

# Push heavy data to S3
dvc push</code></pre>
</div>

<h3 class="sh3">2. Apache Airflow Automated Retraining DAG with Drift Sensor</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — airflow_retrain_dag.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>from datetime import datetime, timedelta

def check_feature_drift(**kwargs):
    psi_score = 0.24 # Calculated from production telemetry
    if psi_score > 0.20:
        print(f"⚠️ Feature drift detected (PSI={psi_score:.2f} > 0.20). Triggering retrain.")
        return "trigger_distributed_training"
    return "skip_retraining"

def execute_model_training():
    print("Executing distributed PyTorch model training with Optuna HPO...")
    return "s3://models/candidate_v2.tar.gz"</code></pre>
</div>

<h3 class="sh3">3. MLflow Automated Champion-Candidate Gate</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — mlflow_promotion_gate.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>def evaluate_and_promote_model(candidate_f1: float, champion_f1: float, p95_latency_ms: float):
    \"\"\"Enforces strict promotion gate before model tagging in registry.\"\"\"
    if candidate_f1 >= (champion_f1 + 0.015) and p95_latency_ms <= 25.0:
        print(f"✅ Candidate Model Approved! F1: {candidate_f1:.4f} (+{candidate_f1 - champion_f1:.4f}) | Latency: {p95_latency_ms}ms")
        return "PROMOTE_TO_CHAMPION"
    print(f"❌ Candidate Model Rejected. Insufficient metric gain or SLA regression.")
    return "REJECT_CANDIDATE"</code></pre>
</div>"""
}

# ─────────────────────────────────────────────────────────────────────
# WEEK 25 TOOLKIT (Kubernetes & GPU Infrastructure)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[25] = {
    'title': 'Master Toolkit: Kubernetes & GPU Infrastructure Suite',
    'subtitle': 'NVIDIA GPU DaemonSet manifests, Prometheus service monitors, and Helm chart values.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Kubernetes & GPU Infrastructure</h2>
<p>
Kubernetes manifests, Helm chart configurations, and autoscaling definitions for enterprise multi-node GPU clusters.
</p>

<h3 class="sh3">1. Kubernetes NVIDIA GPU Pod Resource Specification</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">yaml — vllm-gpu-pod.yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>apiVersion: v1
kind: Pod
metadata:
  name: vllm-inference-worker
spec:
  restartPolicy: OnFailure
  containers:
  - name: inference-engine
    image: vllm/vllm-openai:latest
    resources:
      limits:
        nvidia.com/gpu: 2
        memory: 64Gi
        cpu: "16"
      requests:
        nvidia.com/gpu: 2
        memory: 64Gi
        cpu: "16"
    volumeMounts:
    - mountPath: /dev/shm
      name: dshm
  volumes:
  - name: dshm
    emptyDir:
      medium: Memory
      sizeLimit: 32Gi</code></pre>
</div>

<h3 class="sh3">2. Prometheus Custom Metric Horizontal Pod Autoscaler (HPA)</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">yaml — vllm-hpa.yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-queue-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-inference-deployment
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: External
    external:
      metric:
        name: vllm:avg_waiting_requests_per_pod
      target:
        type: Value
        averageValue: "5"</code></pre>
</div>

<h3 class="sh3">3. Helm Chart Values for Tensor Parallel Serving</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">yaml — values-tensor-parallel.yaml</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code># Helm values configuration for distributed 70B LLM serving
model:
  name: "meta-llama/Meta-Llama-3-70B-Instruct"
  tensorParallelSize: 4
  maxModelLen: 8192
  gpuMemoryUtilization: 0.94

resources:
  requests:
    nvidia.com/gpu: 4
    memory: "128Gi"
  limits:
    nvidia.com/gpu: 4
    memory: "128Gi"</code></pre>
</div>"""
}

# ─────────────────────────────────────────────────────────────────────
# WEEK 26 TOOLKIT (Multimodal AI & System Design)
# ─────────────────────────────────────────────────────────────────────
EXPANDED_TOOLKITS[26] = {
    'title': 'Master Toolkit: Multimodal AI & Principal System Design Suite',
    'subtitle': 'ColPali late-interaction engines, Whisper audio transcription pipelines, and DSPy optimization suites.',
    'xp': 500,
    'content_html': """<h2 class="sh2">🛠️ Master Toolkit: Multimodal AI & Principal System Design</h2>
<p>
Advanced multimodal inference, late-interaction vector retrieval, and prompt optimization architectures.
</p>

<h3 class="sh3">1. End-to-End ColPali Multimodal Retrieval Pipeline</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — colpali_retrieval.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import torch

def late_interaction_maxsim(query_tokens: torch.Tensor, doc_token_matrix: torch.Tensor) -> float:
    \"\"\"
    Computes MaxSim score across visual patch tokens and query text embeddings.
    Score(Q, D) = sum_i max_j (q_i . d_j)
    \"\"\"
    # query_tokens: (Q, d), doc_token_matrix: (P, d)
    sims = torch.matmul(query_tokens, doc_token_matrix.T)
    max_sims, _ = torch.max(sims, dim=1)
    return float(torch.sum(max_sims))</code></pre>
</div>

<h3 class="sh3">2. Whisper Audio Streaming Transcription with VAD</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — whisper_vad_pipeline.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import numpy as np

def chunk_audio_stream(audio_pcm: np.ndarray, sample_rate: int = 16000, chunk_seconds: int = 30):
    \"\"\"Chunks audio stream into 30s spectrogram windows for Whisper ASR.\"\"\"
    chunk_samples = sample_rate * chunk_seconds
    total_chunks = int(np.ceil(len(audio_pcm) / chunk_samples))
    
    for i in range(total_chunks):
        start = i * chunk_samples
        end = min(len(audio_pcm), (i + 1) * chunk_samples)
        yield audio_pcm[start:end]</code></pre>
</div>

<h3 class="sh3">3. DSPy Multi-Hop Teleprompter Optimization Setup</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — dspy_optimization.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>class MultiHopRAGSignature:
    \"\"\"DSPy Signature defining input-output contract for complex multi-hop retrieval.\"\"\"
    context: str = "Retrieved document paragraphs"
    question: str = "User query requiring relational deduction"
    reasoning: str = "Step-by-step intermediate deduction"
    answer: str = "Factual answer citing specific context passages"

def evaluate_teleprompter_metric(gold, pred, trace=None) -> bool:
    return gold.answer.lower() in pred.answer.lower()</code></pre>
</div>"""
}

# Apply to YAML files
counts_per_file = {}
for w, tk in EXPANDED_TOOLKITS.items():
    fpath = f"{DATA_DIR}/week{w:02d}.yaml"
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)
    data['toolkit'] = tk
    save_yaml(fpath, data)
    counts_per_file[f"week{w:02d}.yaml"] = len(tk['content_html'])

if __name__ == '__main__':
    print("=" * 60)
    print("Issue 5: Toolkits Expanded Across Weeks 20, 22-26")
    print("=" * 60)
    for fname, cnt in counts_per_file.items():
        print(f"  • {fname}: expanded to {cnt} characters")
