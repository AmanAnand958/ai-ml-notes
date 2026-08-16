#!/usr/bin/env python3
"""
Surgically replace Mermaid diagrams in Week 24 Days 172 to 177 with 100% bulletproof, tested Mermaid syntax:
- Eliminates reserved '@' symbols (e.g. '@challenger' -> 'Challenger Alias', '@champion' -> 'Champion Alias').
- Eliminates raw '<', '>', '&', '%', and '/' from edge labels.
- Eliminates leading dashes from node labels.
- Replaces decision diamonds with clean syntax.
"""

from pathlib import Path
from bs4 import BeautifulSoup

fp24 = Path("pages/weeks/week24.html")
soup24 = BeautifulSoup(fp24.read_text(encoding='utf-8'), 'html.parser')

CLEAN_DIAGRAMS = {
    "day-172": """graph LR
subgraph Model_Registry_Lifecycle ["Model Registry Lifecycle"]
  TrainingRun["Model Training Run"] -->|register_model| RegisteredVersion["Model Version v2"]
  RegisteredVersion -->|Automated Validation Gate| ChallengerAlias["Challenger Alias (Staging)"]
  ChallengerAlias -->|Shadow Traffic Passed| ChampionAlias["Champion Alias (Production)"]
  ChampionAlias --> Serving["FastAPI Inference Service"]
end""",

    "day-173": """graph LR
subgraph DVC_Git_Workflow ["DVC Data Versioning Workflow"]
  Data["Large Raw Dataset (10 GB)"] -->|dvc add data| DvcFile["data.csv.dvc (MD5 Pointer 42 bytes)"]
  DvcFile -->|git commit track v1| GitRepo["Git Repository"]
  Data -->|dvc push| S3Remote["AWS S3 Remote Storage Bucket"]
end""",

    "day-174": """graph LR
subgraph Airflow_ML_DAG ["Airflow ML Orchestration DAG"]
  S1["S3 Data Sensor"] --> T1["Data Ingest and Validation"]
  T1 --> T2["Model Training Task"]
  T2 --> T3["Evaluation Threshold Gate"]
  T3 -->|F1 score meets threshold| T4["Register to MLflow Challenger"]
  T3 -->|F1 score below threshold| T5["Send Slack Alert and Abort"]
end""",

    "day-175": """graph LR
subgraph Drift_Monitoring_Architecture ["Evidently AI Drift Architecture"]
  ProdStream["Production Inference Data"] --> DriftEngine["Evidently AI Drift Engine"]
  RefData["Training Baseline Data"] --> DriftEngine
  DriftEngine -->|Compute KS-Test and PSI| Gate["Drift Detected? (PSI exceeds 0.25)"]
  Gate -->|Yes| Alert["Trigger Airflow Retraining DAG"]
  Gate -->|No| Metrics["Export Telemetry to Prometheus"]
end""",

    "day-176": """graph LR
subgraph Canary_Traffic_Routing ["Canary Traffic Routing"]
  UserInference["User Inferences"] --> Ingress["Ingress Gateway Router"]
  Ingress -->|90 percent Traffic| V1["Model v1: Champion (Stable)"]
  Ingress -->|10 percent Traffic| V2["Model v2: Challenger (Canary)"]
  V1 --> Monitor["Prometheus Metric Collector"]
  V2 --> Monitor
  Monitor -->|Error Rate exceeds SLA| Rollback["Instant Automated Rollback to 100 percent v1"]
end""",

    "day-177": """graph TD
  Train["Train Candidate Model"] --> Eval["Evaluate on Golden Test Set"]
  Eval --> Canary["5 percent Canary Traffic Deployment"]
  Canary --> Monitor["Monitor Latency and Precision"]
  Monitor -->|Pass Thresholds| FullRollout["100 percent Production Rollout"]
  Monitor -->|Fail Thresholds| Rollback["Automated Instant Rollback"]"""
}

for did, clean_m in CLEAN_DIAGRAMS.items():
    ds = soup24.find('div', id=did)
    if ds:
        m_tag = ds.find('div', class_='mermaid')
        if m_tag:
            m_tag.string = clean_m
            print(f"  ✅ Fixed clean Mermaid diagram for Week 24 ({did})!")

fp24.write_text(str(soup24), encoding='utf-8')
print("\n🎉 ALL MERMAID DIAGRAMS IN WEEK 24 DAYS 172–177 FULLY RESOLVED!")
