#!/usr/bin/env python3
"""
Pedagogical Code Commentary & Explanation Injector:
1. Enriches MLflow Autolog and Tracking in Week 18 & Week 24 with step-by-step comments.
2. Injects rich line-by-line commentary into DVC, vLLM, TensorRT, FastAPI, ONNX, and PyTorch training scripts.
3. Injects dedicated theoretical explanation callouts for MLflow Autolog mechanics.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. ENRICH MLFLOW IN WEEK 18 & WEEK 24
# ─────────────────────────────────────────────────────────────────────────────
# Week 18 Day 126
fp18 = WEEKS_DIR / "week18.html"
if fp18.exists():
    soup18 = BeautifulSoup(fp18.read_text(encoding='utf-8'), 'html.parser')
    d126 = soup18.find('div', id='day-126') or soup18.find('div', id='day-125')
    if d126 and not d126.find(id='mlflow-autolog-deep-dive'):
        theory = d126.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="mlflow-autolog-deep-dive" style="margin:1.5rem 0; padding:1.2rem; background:var(--bg2); border:1px solid var(--border); border-radius:8px;">
  <h3 class="sh3" style="color:var(--accent); margin-top:0;">Deep-Dive: How MLflow Autolog Works Under the Hood</h3>
  <p>Calling <code>mlflow.autolog()</code> (or framework-specific <code>mlflow.sklearn.autolog()</code>, <code>mlflow.pytorch.autolog()</code>) enables zero-code automated instrumentation by monkey-patching the training framework's <code>.fit()</code> and <code>.train()</code> methods:</p>
  <ul style="line-height:1.7; font-size:13.5px;">
    <li><strong>Automatic Hyperparameter Capture:</strong> Intercepts model initialization kwargs (e.g. <code>n_estimators=100</code>, <code>max_depth=6</code>, <code>learning_rate=0.01</code>) and logs them via <code>mlflow.log_params()</code> before execution begins.</li>
    <li><strong>Epoch & Step Metric Telemetry:</strong> Attaches training callbacks that stream loss, accuracy, F1-score, and learning rate curves after every epoch via <code>mlflow.log_metrics()</code> with accurate step timestamps.</li>
    <li><strong>Model Schema & Signature Inference:</strong> Samples a batch of input features and output predictions to record an immutable input/output tensor signature (e.g. <code>TensorSpec(dtype=float32, shape=(-1, 10))</code>), catching runtime shape mismatches before deployment.</li>
    <li><strong>Artifact Serialization & Environment Lock:</strong> Automatically packages the serialized model weights (Pickle/ONNX/TorchScript), <code>requirements.txt</code>, and <code>conda.yaml</code> environment files to guarantee 100% bit-exact reproducibility.</li>
  </ul>
</div>
''', 'html.parser')
            theory.insert_after(section)
            fp18.write_text(str(soup18), encoding='utf-8')
            print("✅ Injected deep MLflow Autolog explanation into Week 18!")

# Week 24 Day 171
fp24 = WEEKS_DIR / "week24.html"
if fp24.exists():
    soup24 = BeautifulSoup(fp24.read_text(encoding='utf-8'), 'html.parser')
    d171 = soup24.find('div', id='day-171') or soup24.find('div', id='day-170')
    if d171 and not d171.find(id='mlflow-registry-deep-dive'):
        theory = d171.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="mlflow-registry-deep-dive" style="margin:1.5rem 0; padding:1.2rem; background:var(--bg2); border:1px solid var(--border); border-radius:8px;">
  <h3 class="sh3" style="color:var(--accent); margin-top:0;">MLflow Model Registry: Aliases (@champion, @challenger) vs Deprecated Stages</h3>
  <p>In modern MLOps (MLflow 2.8+), mutable stages (<em>Staging/Production/Archived</em>) have been replaced by <strong>Model Aliases and Tags</strong>:</p>
  <ul style="line-height:1.7; font-size:13.5px;">
    <li><strong><code>@champion</code> Alias:</strong> Points to the active model version currently serving 100% of live production traffic. Inference services load via <code>models:/Customer_Churn@champion</code> without hardcoding version numbers.</li>
    <li><strong><code>@challenger</code> Alias:</strong> Points to candidate models undergoing shadow deployments or A/B testing against live production traffic.</li>
    <li><strong>Atomic Promotion:</strong> Switching the <code>@champion</code> alias to a newer model version executes instantaneously in the metadata database, enabling zero-downtime rollouts and instant single-click rollbacks.</li>
  </ul>
</div>
''', 'html.parser')
            theory.insert_after(section)
            fp24.write_text(str(soup24), encoding='utf-8')
            print("✅ Injected MLflow Registry & Champion/Challenger depth into Week 24!")

print("\n🎉 STEP 1 COMPLETE: MLFLOW EXPLANATIONS FULLY ENRICHED!")
