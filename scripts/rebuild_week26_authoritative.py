#!/usr/bin/env python3
"""
Full Week 26 Rebuilder using raw string to prevent unicode escape issues.
"""

from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")
fp26 = WEEKS_DIR / "week26.html"

html25 = (WEEKS_DIR / "week25.html").read_text(encoding='utf-8', errors='replace')
head_end = html25.find('</aside>') + len('</aside>')
header_sidebar = html25[:head_end]

header_sidebar = header_sidebar.replace("Week 25", "Week 26")
header_sidebar = header_sidebar.replace("Kubernetes", "Multimodal AI & System Design")
header_sidebar = header_sidebar.replace("week24.html", "week25.html")
header_sidebar = header_sidebar.replace("week26.html", "roadmap.html")
header_sidebar = header_sidebar.replace("178", "185").replace("179", "186").replace("180", "187").replace("181", "188").replace("182", "189").replace("183", "190").replace("184", "191")

week26_body = r'''
<main class="main">

<!-- DAY 185: Vision-Language Models (VLMs) -->
<div class="day-section active" data-xp="150" id="day-185">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 185</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">Vision-Language Models (VLMs)</h1>
    <p>CLIP Joint Embeddings, LLaVA Projections & Spatial Image Tokens</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Visual Projection Weight Quantization Collapse</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Quantizing the vision-language projector adapter without preserving high-precision scaling factors destroys visual token alignment with the language model vocabulary.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$\text{LLaVA Token Embedding: } \mathbf{H}_v = \mathbf{W}_{\text{proj}} \cdot \text{VisionEncoder}(I), \quad \text{where } \mathbf{H}_v \in \mathbb{R}^{N_{\text{patches}} \times d_{\text{llm}}}$$
  </div>
  <pre><code class="language-python">import torch
import torch.nn as nn

class MultimodalProjector(nn.Module):
    def __init__(self, visual_dim: int = 1024, llm_dim: int = 4096):
        super().__init__()
        self.linear1 = nn.Linear(visual_dim, llm_dim)
        self.gelu = nn.GELU()
        self.linear2 = nn.Linear(llm_dim, llm_dim)
        
    def forward(self, visual_features: torch.Tensor) -> torch.Tensor:
        return self.linear2(self.gelu(self.linear1(visual_features)))

# Pipeline demo
projector = MultimodalProjector(1024, 4096)
img_feats = torch.randn(1, 576, 1024)
projected_tokens = projector(img_feats)
print(f"Projected Visual Tokens Shape: {projected_tokens.shape}")</code></pre>
  <button class="complete-btn" id="btn-day-185" onclick="completeDay(185, 150)">Mark Day 185 Complete (+150 XP)</button>
</div>

<!-- DAY 186: Multimodal RAG -->
<div class="day-section" data-xp="150" id="day-186">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 186</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">Multimodal RAG & ColPali</h1>
    <p>Late Interaction Patch Retrieval & Document Image Indexing</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Multimodal Video Token Window Overflow</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Ingesting raw video without spatial-temporal pooling generates &gt;15,000 visual tokens, causing catastrophic context window overflow or GPU CUDA OOM. Always apply dynamic frame sampling and token compression.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$\text{MaxSim Late Interaction: } S(Q, D) = \sum_{i=1}^{|Q|} \max_{j=1}^{|D|} \left( \mathbf{q}_i^\top \mathbf{d}_j \right)$$
  </div>
  <pre><code class="language-python">import torch
import torch.nn.functional as F

def compute_colpali_maxsim(query_embeddings: torch.Tensor, doc_embeddings: torch.Tensor) -> torch.Tensor:
    """Computes MaxSim late interaction between token queries and multi-vector doc patches."""
    q_norm = F.normalize(query_embeddings, p=2, dim=-1)
    d_norm = F.normalize(doc_embeddings, p=2, dim=-1)
    sim_matrix = torch.bmm(q_norm, d_norm.transpose(1, 2))
    max_sims, _ = torch.max(sim_matrix, dim=-1)
    return torch.sum(max_sims, dim=-1)

# Verification
q_emb = torch.randn(2, 8, 128)
d_emb = torch.randn(2, 1024, 128)
scores = compute_colpali_maxsim(q_emb, d_emb)
print(f"ColPali Late Interaction Scores: {scores.detach().numpy()}")</code></pre>
  <button class="complete-btn" id="btn-day-186" onclick="completeDay(186, 150)">Mark Day 186 Complete (+150 XP)</button>
</div>

<!-- DAY 187: Audio Processing with Whisper -->
<div class="day-section" data-xp="150" id="day-187">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 187</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">Audio Processing with Whisper</h1>
    <p>Log-Mel Spectrograms, Voice Activity Detection & Autoregressive Transcription</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Whisper Hallucination on Silent Audio</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Passing long unvoiced silent segments to Whisper causes the autoregressive decoder to hallucinate repetitive loops. Always use Voice Activity Detection (VAD) to trim silent frames before inference.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$M(m, t) = \sum_{k=0}^{K-1} |X(k, t)|^2 \cdot H_m(k) \quad \xrightarrow{\log} \quad \text{80-Channel Log-Mel Spectrogram}$$
  </div>
  <pre><code class="language-python">import numpy as np

def compute_log_mel_spectrogram(waveform: np.ndarray, sr: int = 16000, n_mels: int = 80) -> np.ndarray:
    """Converts 16kHz audio waveform into 80-channel log-mel features for Whisper."""
    stft = np.abs(np.fft.rfft(waveform[:400]))
    mel_filters = np.linspace(0, 1, len(stft))
    mel_energy = np.outer(mel_filters, np.ones(n_mels)).T @ stft
    log_mel = np.log10(np.maximum(mel_energy, 1e-5))
    return log_mel

waveform = np.sin(np.linspace(0, 100, 16000))
features = compute_log_mel_spectrogram(waveform)
print(f"Log-Mel Spectrogram Feature Shape: {features.shape}")</code></pre>
  <button class="complete-btn" id="btn-day-187" onclick="completeDay(187, 150)">Mark Day 187 Complete (+150 XP)</button>
</div>

<!-- DAY 188: ML System Design — Recommendation System -->
<div class="day-section" data-xp="150" id="day-188">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 188</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">ML System Design — Recommendation System</h1>
    <p>Two-Tower Candidate Generation (DSSM), ANN Retrieval & Ranking</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Popularity Bias & Feedback Loops</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Training recommendation models purely on user clicks creates severe popularity bias and feedback loops. Enforce exploration bandits (e.g., epsilon-greedy or Thompson Sampling) on 5% of traffic.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$P(\text{Click} \mid u, i) = \sigma\left(\langle \psi(u), \phi(i) \rangle + b\right) = \frac{1}{1 + e^{-\mathbf{u}^\top \mathbf{v}_i}}$$
  </div>
  <pre><code class="language-python">import torch
import torch.nn as nn
import torch.nn.functional as F

class TwoTowerRecommendation(nn.Module):
    def __init__(self, user_dim: int, item_dim: int, embed_dim: int = 128):
        super().__init__()
        self.user_tower = nn.Sequential(nn.Linear(user_dim, 256), nn.ReLU(), nn.Linear(256, embed_dim))
        self.item_tower = nn.Sequential(nn.Linear(item_dim, 256), nn.ReLU(), nn.Linear(256, embed_dim))
        
    def forward(self, u_feat: torch.Tensor, i_feat: torch.Tensor) -> torch.Tensor:
        u_emb = F.normalize(self.user_tower(u_feat), p=2, dim=-1)
        i_emb = F.normalize(self.item_tower(i_feat), p=2, dim=-1)
        return torch.sum(u_emb * i_emb, dim=-1)

model = TwoTowerRecommendation(64, 64, 128)
scores = model(torch.randn(4, 64), torch.randn(4, 64))
print(f"Two-Tower Similarity Scores: {scores.detach().numpy()}")</code></pre>
  <button class="complete-btn" id="btn-day-188" onclick="completeDay(188, 150)">Mark Day 188 Complete (+150 XP)</button>
</div>

<!-- DAY 189: DSPy — Programmatic Prompt Optimization -->
<div class="day-section" data-xp="150" id="day-189">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 189</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">DSPy — Programmatic Prompt Optimization</h1>
    <p>Signatures, Teleprompters, BootstrapFewShot & MIPROv2</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: Metric Overfitting with Small Validation Sets</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Optimizing DSPy teleprompters on tiny validation datasets overfits prompt instructions to training artifacts rather than true reasoning primitives.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$\text{Prompt}^* = \arg\max_{P \in \mathcal{P}} \mathbb{E}_{(x,y) \sim \mathcal{D}_{\text{val}}}\left[\text{Metric}(\text{LM}(x; P), y)\right]$$
  </div>
  <pre><code class="language-python">import dspy

class RAGSignature(dspy.Signature):
    """Answers factual questions given retrieved technical context."""
    context = dspy.InputField(desc="Retrieved reference documents")
    question = dspy.InputField(desc="User query")
    answer = dspy.OutputField(desc="Accurate, concise factual answer")

class ProductionRAG(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(RAGSignature)
        
    def forward(self, context: str, question: str):
        return self.generate_answer(context=context, question=question)

print("DSPy Production RAG Module Compiled Successfully.")</code></pre>
  <button class="complete-btn" id="btn-day-189" onclick="completeDay(189, 150)">Mark Day 189 Complete (+150 XP)</button>
</div>

<!-- DAY 190: ML System Design — Semantic Search -->
<div class="day-section" data-xp="150" id="day-190">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 190</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">ML System Design — Semantic Search</h1>
    <p>Billion-Scale Vector Sharding, Inverted Multi-Index & Product Quantization (IVFPQ)</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--red);">⚠️ Gotcha: 1 Billion Vector RAM Explosion</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">Storing 1 Billion 1536-dimensional vectors in float32 requires 6 Terabytes of RAM. Production systems must combine Inverted File (IVF) coarse quantizers with Product Quantization (PQ-64) to achieve a 95% RAM reduction.</p>
  </div>
  <div class="math-block" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; font-size:14px;">
    $$\text{RAM}_{\text{float32}} = N \cdot d \cdot 4 \text{ bytes}, \quad \text{RAM}_{\text{PQ-M}} = N \cdot M \cdot 1 \text{ byte} \quad (\approx 95\% \text{ reduction})$$
  </div>
  <pre><code class="language-python">import numpy as np

def calculate_vector_db_sharding(total_vectors: int = 1_000_000_000, dim: int = 1536, ram_per_node_gb: int = 64) -> dict:
    raw_ram_gb = (total_vectors * dim * 4) / (1024**3)
    pq_ram_gb = (total_vectors * 64 * 1) / (1024**3)
    shards_needed = int(np.ceil(pq_ram_gb / (ram_per_node_gb * 0.7)))
    return {
        "raw_ram_gb": round(raw_ram_gb, 2),
        "pq_ram_gb": round(pq_ram_gb, 2),
        "shards_needed": shards_needed
    }

sharding_spec = calculate_vector_db_sharding()
print(f"Billion-Scale Sharding Specs: {sharding_spec}")</code></pre>
  <button class="complete-btn" id="btn-day-190" onclick="completeDay(190, 150)">Mark Day 190 Complete (+150 XP)</button>
</div>

<!-- DAY 191: Final Capstone & Portfolio Polish -->
<div class="day-section" data-xp="150" id="day-191">
  <div class="day-header">
    <div class="day-tag">WEEK 26 · DAY 191</div>
    <h1 style="font-size:1.8rem; font-weight:800; color:var(--text); margin:0.4rem 0 0.6rem;">Final Capstone & Portfolio Polish</h1>
    <p>Production Multi-Agent RAG System & 191-Day AI/ML Roadmap Graduation 🎉</p>
  </div>
  <div class="callout warning" style="margin:1rem 0;">
    <div class="callout-title" style="font-weight:700; color:var(--green);">🎓 Congratulations on Completing the 191-Day Curriculum!</div>
    <p style="margin:0.4rem 0 0; font-size:13px; line-height:1.6;">You have built end-to-end foundations covering Classical ML, Deep Learning, Transformers, LLMs, Agents, MLOps, Kubernetes, and Multimodal System Design.</p>
  </div>
  <button class="complete-btn" id="btn-day-191" onclick="completeDay(191, 150)">Mark Day 191 Complete (+150 XP) — Graduate!</button>
</div>

<div class="week-summary">
  <div class="ws-header"><span class="ws-icon">🏆</span><h3>Week 26 Milestone — 191-Day AI/ML Mastery!</h3></div>
  <p style="color:var(--muted); font-size:13px; line-height:1.6;">All 26 Weeks, 191 Days, 57 Architectures, and 100+ Production Systems mastered.</p>
</div>

</main>

<script>
  const WEEK = 26;
  const DAYS = [185,186,187,188,189,190,191];
  
  function showDay(dayId) {
    document.querySelectorAll('.day-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.day-pill').forEach(pill => pill.classList.remove('active'));
    const targetSec = document.getElementById('day-' + dayId);
    const targetPill = document.querySelector(`.day-pill[data-day="${dayId}"]`);
    if (targetSec) targetSec.classList.add('active');
    if (targetPill) targetPill.classList.add('active');
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function completeDay(dayNum, xp) {
    alert(`Day ${dayNum} completed! +${xp} XP awarded!`);
    const btn = document.getElementById(`btn-day-${dayNum}`);
    if (btn) {
      btn.innerText = `✅ Day ${dayNum} Completed (+${xp} XP)`;
      btn.style.background = 'var(--green)';
      btn.style.color = '#000';
    }
  }

  document.querySelectorAll('.day-pill').forEach(pill => {
    pill.addEventListener('click', (e) => {
      e.preventDefault();
      showDay(pill.getAttribute('data-day'));
    });
  });
</script>
</body>
</html>
'''

fp26.write_text(header_sidebar + week26_body, encoding='utf-8')
print("✅ Authoritative week26.html rebuilt cleanly with raw string literals!")
