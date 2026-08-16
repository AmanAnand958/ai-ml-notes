#!/usr/bin/env python3
"""
Step 2: Inject clear introductory pedagogical prose before bare subheadings across all 26 weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

BARE_HEADINGS_MAP = {
    # Week 4 Day 24
    (4, "Central Limit Theorem"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">The <strong>Central Limit Theorem (CLT)</strong> states that the normalized sum or mean of a sufficiently large number of independent and identically distributed (i.i.d.) random variables approaches a Gaussian normal distribution ($\mathcal{N}(\mu, \sigma^2/n)$), regardless of the underlying population distribution shape.</p>""",
    
    # Week 4 Day 24
    (4, "Binomial and Poisson Distributions"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;"><strong>Binomial distributions</strong> model the discrete count of successes in $n$ independent Bernoulli trials with fixed probability $p$, while the <strong>Poisson distribution</strong> models the count of independent events occurring within a fixed interval of time or space at a constant average rate $\lambda$.</p>""",
    
    # Week 4 Day 26
    (4, "Matrix Operations"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">Matrix multiplication ($C = AB$) forms the computational foundation of modern neural network forward and backward passes, mapping input representations from dimension $d_{in}$ into transformed latent manifolds of dimension $d_{out}$.</p>""",
    
    # Week 4 Day 26
    (4, "Eigenvalues and Eigenvectors"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">An <strong>eigenvector</strong> $v$ of a square matrix $A$ represents a direction that is only scaled (not rotated) by linear transformation $A$, satisfying $Av = \lambda v$. In Principal Component Analysis (PCA), top eigenvectors of the covariance matrix point along directions of maximum data variance.</p>""",
    
    # Week 6 Day 42
    (6, "The Complete Regression Metric Toolkit"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">Evaluating continuous regression models requires quantifying both absolute prediction deviations (Mean Absolute Error, MAE) and quadratically penalized outlier errors (Root Mean Squared Error, RMSE), benchmarked against the variance explained ratio ($R^2$ score).</p>""",
    
    # Week 8 Day 57
    (8, "Learning Rate Schedules"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">Dynamically adjusting the learning rate $\eta_t$ throughout training prevents premature convergence in local minima and stabilizes late-stage parameter optimization. Standard strategies combine linear warmup with cosine annealing or ReduceLROnPlateau decay.</p>""",
    
    # Week 25 Day 179
    (25, "Persistent Volume for Model Cache"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">Inference pods require fast access to large model weight tarballs (14GB–70GB). Mounting a Kubernetes <strong>PersistentVolumeClaim (PVC)</strong> backed by high-throughput SSD (ReadWriteMany) caches weights locally, eliminating repeated network egress downloads during autoscaling events.</p>""",
    
    # Week 25 Day 182
    (25, "ML CI/CD Pipeline"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">An enterprise <strong>ML CI/CD pipeline</strong> automates linting, model regression testing, containerization, and GitOps deployments via ArgoCD or GitHub Actions upon every pull request.</p>""",
    
    # Week 25 Day 183
    (25, "pytest + DeepEval Regression Suite"): """<p style="margin: 0.8rem 0; font-size: 13.5px; line-height: 1.6;">Automated <strong>LLM regression suites (pytest + DeepEval)</strong> enforce deterministic quality gates on prompt templates, ensuring newly tuned models maintain hallucination, toxicity, and semantic similarity scores above production thresholds.</p>"""
}

for (wn, h_snippet), expl_html in BARE_HEADINGS_MAP.items():
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for h in soup.find_all(['h2', 'h3', 'h4']):
        if h_snippet.lower() in h.text.strip().lower():
            nxt = h.find_next_sibling()
            if nxt and nxt.name != 'p':
                p_tag = BeautifulSoup(expl_html, 'html.parser')
                h.insert_after(p_tag)
                print(f"  ✅ Injected pedagogical intro for '{h_snippet}' in Week {wn}")
                break
                
    fp.write_text(str(soup), encoding='utf-8')

print("\n🎉 STEP 2 COMPLETE: ALL CORE BARE HEADINGS ENRICHED WITH INTRODUCTORY PROSE!")
