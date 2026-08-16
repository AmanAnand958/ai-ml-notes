#!/usr/bin/env python3
"""
Deep Pedagogical Coverage & Technical Accuracy Audit across all 26 Weeks:
1. Deprecated Python/ML API usage (pd.DataFrame.append, old sklearn/torch functions).
2. Title & Objectives vs Actual Body Coverage Gap (announced concepts missing in body).
3. Mathematical precision & common technical misconceptions (L1 vs L2, Softmax simplex, Attention scale 1/sqrt(d_k)).
4. Tensor shape annotations completeness in Deep Learning weeks (Weeks 8-16, 19-26).
5. Failure modes & production Gotchas completeness.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
pedagogical_issues = []

def log_coverage_issue(category, week, day, severity, title, details, snippet=""):
    pedagogical_issues.append({
        "id": len(pedagogical_issues) + 1,
        "category": category,
        "week": week,
        "day": day,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. DEPRECATED ML / PYTHON API DETECTOR
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 1: Deprecated ML API Usage...")
DEPRECATED_APIS = {
    r'\.append\s*\(': "DataFrame.append() is deprecated and removed in Pandas 2.0; use pd.concat() instead.",
    r'plot_confusion_matrix\s*\(': "sklearn.metrics.plot_confusion_matrix is deprecated in scikit-learn 1.2+; use ConfusionMatrixDisplay.from_estimator() instead.",
    r'plot_roc_curve\s*\(': "sklearn.metrics.plot_roc_curve is deprecated; use RocCurveDisplay.from_estimator() instead.",
    r'np\.matrix\s*\(': "np.matrix is officially discouraged by NumPy; use standard 2D np.ndarray with @ operator instead.",
    r'torch\.Tensor\s*\(': "Calling torch.Tensor() creates uninitialized memory; prefer torch.tensor() or torch.zeros()/torch.randn() for explicit data.",
    r'from\s+sklearn\.grid_search\b': "sklearn.grid_search was removed; use sklearn.model_selection instead.",
    r'from\s+sklearn\.cross_validation\b': "sklearn.cross_validation was removed; use sklearn.model_selection instead.",
    r'dflt_dtype': "Old NumPy alias."
}

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    html = fp.read_text(encoding='utf-8')
    
    for pattern, desc in DEPRECATED_APIS.items():
        matches = re.finditer(pattern, html)
        for m in matches:
            idx = m.start()
            snippet = html[max(0, idx-40):idx+60]
            log_coverage_issue(
                "Deprecated API Usage", wn, f"Week {wn}", "HIGH",
                f"Deprecated library function found: {m.group(0)}",
                desc,
                snippet
            )

# ─────────────────────────────────────────────────────────────────────────────
# 2. TOPIC COVERAGE GAPS: OBJECTIVES VS ACTUAL BODY TEXT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 2: Objectives vs Body Text Coverage Gaps...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        h1 = ds.find('h1')
        title_text = h1.text.strip() if h1 else ""
        day_text = ds.text
        
        # Check specific key topics announced in titles that might be under-explained in body
        # e.g., Kubernetes Ingress / ConfigMaps / Secrets
        if "Kubernetes" in title_text and "Core Concepts" in title_text:
            missing_k8s = []
            for concept in ["ConfigMap", "Secret", "Ingress", "Namespace"]:
                if concept not in day_text:
                    missing_k8s.append(concept)
            if missing_k8s:
                log_coverage_issue(
                    "Incomplete Coverage", wn, did, "MEDIUM",
                    f"K8s Core Concepts skips announced topics: {missing_k8s}",
                    f"Lesson covers Pods and Services but omits standard foundational primitives: {missing_k8s}."
                )

        # Attention Mechanism: Check if Positional Encoding and LayerNorm are explained
        if "Attention" in title_text or "Transformer" in title_text:
            missing_tf = []
            for concept in ["Positional", "LayerNorm", "Q, K, V", "Softmax"]:
                if concept.lower() not in day_text.lower():
                    missing_tf.append(concept)
            if missing_tf:
                log_coverage_issue(
                    "Incomplete Coverage", wn, did, "MEDIUM",
                    f"Transformer lesson lacks coverage for: {missing_tf}",
                    f"{did} announces Attention/Transformers but omits detailed breakdown of {missing_tf}."
                )

        # GANs: Check if Wasserstein loss / Gradient Penalty / Mode Collapse are explained
        if "GAN" in title_text or "Generative" in title_text:
            missing_gan = []
            for concept in ["Mode Collapse", "Discriminator", "Generator", "Wasserstein"]:
                if concept.lower() not in day_text.lower():
                    missing_gan.append(concept)
            if missing_gan:
                log_coverage_issue(
                    "Incomplete Coverage", wn, did, "MEDIUM",
                    f"GAN lesson lacks coverage for: {missing_gan}",
                    f"{did} announces Generative Adversarial Networks but omits {missing_gan}."
                )

        # LoRA / Parameter-Efficient Fine-Tuning
        if "LoRA" in title_text or "PEFT" in title_text or "Fine-Tuning" in title_text:
            missing_peft = []
            for concept in ["Rank", "Adapter", "Quantization", "QLoRA"]:
                if concept.lower() not in day_text.lower():
                    missing_peft.append(concept)
            if missing_peft:
                log_coverage_issue(
                    "Incomplete Coverage", wn, did, "LOW",
                    f"PEFT/LoRA lesson lacks coverage for: {missing_peft}",
                    f"{did} discusses fine-tuning but omits key concepts: {missing_peft}."
                )

# ─────────────────────────────────────────────────────────────────────────────
# 3. MATHEMATICAL PRECISION & TECHNICAL ACCURACY AUDIT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 3: Technical Inaccuracies & Conceptual Misconceptions...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # 1. Softmax independent probabilities claim
    if "softmax outputs independent" in raw.lower():
        log_coverage_issue("Technical Inaccuracy", wn, "Global", "HIGH", "Misleading claim about Softmax independence", "Softmax outputs a normalized probability simplex where sum=1 (mutually exclusive events), unlike sigmoid which outputs independent Bernoulli probabilities.")

    # 2. Check if attention formula contains 1/sqrt(d_k) scaling factor
    if "Attention(Q, K, V)" in raw:
        if "sqrt" not in raw and r"\sqrt" not in raw and "d_k" not in raw:
            log_coverage_issue("Mathematical Imprecision", wn, "Global", "MEDIUM", "Scaled Dot-Product Attention formula missing 1/sqrt(d_k)", "Attention formula omits the variance scaling factor 1/sqrt(d_k) required to prevent vanishing softmax gradients on large hidden dimensions.")

    # 3. Check L1 vs L2 regularization descriptions
    if "l1 produces smooth" in raw.lower() or "l2 produces sparse" in raw.lower():
        log_coverage_issue("Technical Inaccuracy", wn, "Global", "CRITICAL", "Reversed L1/L2 Regularization properties", "L1 Lasso produces sparse feature selection (zeros), whereas L2 Ridge produces non-zero weight decay shrinkage.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. TENSOR SHAPE ANNOTATION AUDIT (Deep Learning Weeks 8-16, 19-26)
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 4: Tensor Shape Tracking Completeness...")
for wn in [8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 26]:
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        cbs = ds.find_all('div', class_='cb')
        
        has_shape_comments = False
        for cb in cbs:
            code = cb.text
            if re.search(r'#.*shape|#.*\(batch|\.shape', code, re.IGNORECASE):
                has_shape_comments = True
                break
                
        if not has_shape_comments and len(cbs) > 0:
            log_coverage_issue(
                "Pedagogical Clarity", wn, did, "LOW",
                f"Missing tensor shape tracking annotations in {did}",
                f"Deep learning code in {did} lacks explicit input/output tensor shape comments (e.g. `(batch_size, seq_len, d_model)`), which are critical for student comprehension."
            )

# ─────────────────────────────────────────────────────────────────────────────
# 5. PRODUCTION GOTCHAS & FAILURE MODES AUDIT
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 5: Production Gotchas & Failure Modes...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        gotcha = ds.find('div', class_=re.compile(r'gotcha|gotcha-box|callout-warning'))
        if not gotcha and 'Gotcha' not in ds.text and 'Common Pitfall' not in ds.text and 'toolkit' not in did:
            log_coverage_issue(
                "Missing Failure Mode Guidance", wn, did, "LOW",
                f"Missing '⚠️ Gotcha & Production Pitfall' box in {did}",
                f"{did} does not highlight common debugging traps or silent production failure modes for this topic."
            )

print(f"\nPedagogical Coverage Audit complete! Cataloged {len(pedagogical_issues)} coverage & technical findings.")
out_file = Path("scripts/pedagogical_coverage_issues_inventory.json")
out_file.write_text(json.dumps(pedagogical_issues, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
