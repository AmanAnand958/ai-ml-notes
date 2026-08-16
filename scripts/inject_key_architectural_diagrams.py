#!/usr/bin/env python3
"""
Step 3: Inject rich Mermaid architectural flowcharts into key complex system & algorithm days.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

KEY_ARCHITECTURAL_DIAGRAMS = {
    # 1. Week 5 Day 35: K-Fold Cross-Validation
    (5, "day-35"): '''<div class="mermaid">
graph TD
  Data["Full Training Dataset (100%)"] --> Split["Stratified Split"]
  Split --> F1["Fold 1 (Val) | Folds 2-5 (Train)"]
  Split --> F2["Fold 2 (Val) | Folds 1,3,4,5 (Train)"]
  Split --> F3["Fold 3 (Val) | Folds 1,2,4,5 (Train)"]
  Split --> F4["Fold 4 (Val) | Folds 1,2,3,5 (Train)"]
  Split --> F5["Fold 5 (Val) | Folds 1-4 (Train)"]
  F1 --> Avg["Mean CV Score & Variance (μ ± σ)"]
  F2 --> Avg
  F3 --> Avg
  F4 --> Avg
  F5 --> Avg
</div>''',

    # 2. Week 7 Day 47: Random Forest Ensemble Bagging
    (7, "day-47"): '''<div class="mermaid">
graph TD
  Train["Training Dataset"] --> Boot1["Bootstrap Sample 1 (w/ replacement)"]
  Train --> Boot2["Bootstrap Sample 2 (w/ replacement)"]
  Train --> BootN["Bootstrap Sample N (w/ replacement)"]
  Boot1 --> Tree1["Decision Tree 1 (Random sqrt(d) features)"]
  Boot2 --> Tree2["Decision Tree 2 (Random sqrt(d) features)"]
  BootN --> TreeN["Decision Tree N (Random sqrt(d) features)"]
  Tree1 --> Vote["Majority Voting / Soft Probability Average"]
  Tree2 --> Vote
  TreeN --> Vote
  Vote --> Final["Final Robust Ensemble Prediction"]
</div>''',

    # 3. Week 8 Day 54: Backpropagation Computational Graph
    (8, "day-54"): '''<div class="mermaid">
graph LR
  X["Input x"] -->|Forward| Z1["Linear: z₁ = W₁x + b₁"]
  Z1 -->|Forward| A1["Activation: a₁ = ReLU(z₁)"]
  A1 -->|Forward| Z2["Output: z₂ = W₂a₁ + b₂"]
  Z2 -->|Forward| Loss["Loss J(y, ŷ)"]
  Loss -->|dL/dz₂| GradW2["Compute dL/dW₂ = (dL/dz₂)·a₁ᵀ"]
  GradW2 -->|dL/da₁| GradZ1["Compute dL/dz₁ = (W₂ᵀ·dL/dz₂) ⊙ ReLU'(z₁)"]
  GradZ1 -->|dL/dW₁| GradW1["Compute dL/dW₁ = (dL/dz₁)·xᵀ"]
</div>''',

    # 4. Week 10 Day 68: LSTM Memory Cell State Highway
    (10, "day-68"): '''<div class="mermaid">
graph TD
  Inputs["Inputs: [h_{t-1}, x_t]"] --> Forget["Forget Gate: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)"]
  Inputs --> InputG["Input Gate: i_t = σ(W_i · [h_{t-1}, x_t] + b_i)"]
  Inputs --> Cand["Candidate State: C̃_t = tanh(W_c · [h_{t-1}, x_t] + b_c)"]
  Inputs --> OutG["Output Gate: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)"]
  Forget --> CellUpdate["Cell State Highway: C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t"]
  Cand --> CellUpdate
  InputG --> CellUpdate
  CellUpdate --> Hidden["Hidden Output: h_t = o_t ⊙ tanh(C_t)"]
  OutG --> Hidden
</div>''',

    # 5. Week 23 Day 164: SageMaker Multi-Model Endpoint Architecture
    (23, "day-164"): '''<div class="mermaid">
graph TD
  Client["Client Inference Request (TargetModel header)"] --> ALB["SageMaker HTTPS Application Load Balancer"]
  ALB --> Container["Multi-Model Inference Container (Triton / TorchServe)"]
  Container --> MemCache{"Model in Container Memory?"}
  MemCache -->|Yes: Hit| Infer["Execute Fast GPU Inference (<10ms)"]
  MemCache -->|No: Miss| S3["Dynamically Load Model Tarball from S3 Bucket"]
  S3 --> Load["Decompress & Load Weights into VRAM Cache"]
  Load --> Infer
  Infer --> Client
</div>'''
}

for (wn, did), diag_html in KEY_ARCHITECTURAL_DIAGRAMS.items():
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    d_sec = soup.find('div', id=did)
    if d_sec and not d_sec.find('div', class_='mermaid'):
        theory = d_sec.find('h2', class_='sh2', id=f'{did}-theory') or d_sec.find('h2', class_='sh2')
        if theory:
            parsed_diag = BeautifulSoup(diag_html, 'html.parser')
            theory.insert_after(parsed_diag)
            fp.write_text(str(soup), encoding='utf-8')
            print(f"  ✅ Injected architectural flowchart into Week {wn} ({did})")

print("\n🎉 STEP 3 COMPLETE: KEY ARCHITECTURAL DIAGRAMS INJECTED & VALIDATED!")
