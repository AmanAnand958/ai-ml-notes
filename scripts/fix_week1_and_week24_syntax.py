#!/usr/bin/env python3
"""
Fix remaining specific syntax items in Week 1 and Week 24:
1. Week 1: Fix missing quote in `print(f"Type of name : {type(name)}")`.
2. Week 24: Fix **kwargs (replaces <strong>kwargs), fix >> in Airflow DAG, and set language='yaml' on dvc.yaml and github actions workflows.
"""

from pathlib import Path
from bs4 import BeautifulSoup

# 1. Week 1
fp1 = Path("pages/weeks/week1.html")
soup1 = BeautifulSoup(fp1.read_text(encoding='utf-8'), 'html.parser')
for pre in soup1.find_all('pre'):
    txt = pre.text
    txt = txt.replace('print(f"Type of name : {type(name)})', 'print(f"Type of name : {type(name)}")')
    txt = txt.replace('print(f"Type of age  : {type(age)})', 'print(f"Type of age  : {type(age)}")')
    txt = txt.replace('print(f"Type of age: {type(age)})', 'print(f"Type of age: {type(age)}")')
    pre.string = txt
fp1.write_text(str(soup1), encoding='utf-8')
print("✅ Fixed Week 1 quotes!")

# 2. Week 24
fp24 = Path("pages/weeks/week24.html")
soup24 = BeautifulSoup(fp24.read_text(encoding='utf-8'), 'html.parser')
for cb in soup24.find_all('div', class_='cb'):
    lang = cb.find('span', class_='cb-lang')
    pre = cb.find('pre')
    if not pre: continue
    txt = pre.text
    
    # Check YAML blocks
    if 'stages:' in txt and 'cmd: python' in txt:
        if lang: lang.string = 'yaml'
    elif 'name: Production MLOps' in txt or 'jobs:\n  test_and_evaluate:' in txt:
        if lang: lang.string = 'yaml'
    elif 'class ProductionModelGate:' in txt:
        clean_gate = '''import mlflow
from mlflow.models.signature import infer_signature
import numpy as np

class ProductionModelGate:
    """
    Automated Governance Gate evaluating candidate models against production champion baselines.
    """
    def __init__(self, min_f1_threshold: float = 0.90, max_latency_ms: float = 45.0):
        self.min_f1_threshold = min_f1_threshold
        self.max_latency_ms = max_latency_ms

    def evaluate_and_promote(self, model_name: str, candidate_metrics: dict) -> bool:
        f1 = candidate_metrics.get("f1_score", 0.0)
        latency = candidate_metrics.get("p99_latency_ms", 100.0)
        
        print(f"Evaluating {model_name} - F1: {f1:.4f} (Req >= {self.min_f1_threshold}) | Latency: {latency}ms (Req <= {self.max_latency_ms}ms)")
        
        if f1 >= self.min_f1_threshold and latency <= self.max_latency_ms:
            print(f"✅ APPROVED: Promoting {model_name} to @champion alias in MLflow Registry.")
            return True
        else:
            print(f"❌ REJECTED: Candidate {model_name} does not meet enterprise quality/latency SLAs.")
            return False

gate = ProductionModelGate(min_f1_threshold=0.92, max_latency_ms=30.0)
gate.evaluate_and_promote("FraudDetectorV2", {"f1_score": 0.942, "p99_latency_ms": 22.4})'''
        pre.string = clean_gate
    elif 'train_model_task' in txt:
        clean_airflow = '''from datetime import datetime, timedelta

# Apache Airflow ML Pipeline DAG Definition
def train_model_task(**kwargs):
    print("Training PyTorch model and logging metrics to MLflow...")
    return "training_success"

def evaluate_model_task(**kwargs):
    ti = kwargs['ti']
    status = ti.xcom_pull(task_ids='train_model')
    print(f"Evaluating model output from step: {status}. F1 score = 0.94 - PASS")
    return True

print("Airflow ML DAG loaded: Daily Model Retraining & Evaluation Pipeline.")'''
        pre.string = clean_airflow
    elif 'pull_data  train' in txt or 'with DAG("full_mlops_pipeline"' in txt:
        clean_dag = '''# Airflow DAG wiring everything together
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator

with DAG("full_mlops_pipeline", schedule="@weekly", start_date=datetime(2026, 1, 1), catchup=False) as dag:
    
    pull_data     = PythonOperator(task_id="pull_dvc_data", python_callable=lambda: print("Pulling DVC data"))
    train         = PythonOperator(task_id="train_mlflow",  python_callable=lambda: print("Training MLflow"))
    evaluate      = BranchPythonOperator(task_id="champion_challenger", python_callable=lambda: "promote_to_prod")
    promote       = PythonOperator(task_id="promote_to_prod", python_callable=lambda: print("Promoting model"))
    drift_check   = PythonOperator(task_id="evidently_drift", python_callable=lambda: print("Checking drift"))
    alert_slack   = PythonOperator(task_id="alert_on_drift",  python_callable=lambda: print("Alerting slack"))
    
    pull_data >> train >> evaluate >> promote >> drift_check
    drift_check >> alert_slack'''
        pre.string = clean_dag

fp24.write_text(str(soup24), encoding='utf-8')
print("✅ Fixed Week 24 Airflow & YAML blocks!")
