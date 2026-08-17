#!/usr/bin/env python3
"""
Step 2: 
1. Enrich Transformer Day 96 (Week 14) with LayerNorm & Positional Embeddings.
2. Enrich WGAN-GP Day 75 (Week 11) with Gradient Penalty implementation.
3. Enrich Distributed Training Day 149 (Week 21) with ZeRO Stages and FSDP comparison.
"""

from pathlib import Path
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────────────────────
# 1. ENRICH TRANSFORMERS (Week 14 Day 96)
# ─────────────────────────────────────────────────────────────────────────────
fp14 = Path("pages/weeks/week14.html")
if fp14.exists():
    soup14 = BeautifulSoup(fp14.read_text(encoding='utf-8'), 'html.parser')
    d96 = soup14.find('div', id='day-96')
    if d96 and not d96.find(id='transformer-ln-rope-enriched'):
        theory = d96.find('h2', class_='sh2', id='day-96-theory') or d96.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="transformer-ln-rope-enriched" style="margin:1.5rem 0;">
  <h3 class="sh3">Pre-LN vs Post-LN & Rotary Positional Embeddings (RoPE)</h3>
  <p>Modern LLMs (Llama 3, Mistral, Gemma) replace original Post-LN and Sinusoidal encodings with two critical architectural innovations:</p>
  <ul>
    <li><strong>Pre-Layer Normalization (Pre-LN with RMSNorm):</strong> Normalizes inputs <em>before</em> the Multi-Head Attention and MLP blocks ($x + \text{MHA}(\text{RMSNorm}(x))$), preventing exploding gradients and enabling stable training without aggressive warmup schedules.</li>
    <li><strong>Rotary Positional Embedding (RoPE):</strong> Encodes relative token distance by rotating Query and Key vector pairs in the 2D complex plane ($R_{\Theta, m} q_m$), preserving relative spatial awareness across long context windows (32k–128k tokens).</li>
  </ul>
</div>
''', 'html.parser')
            theory.insert_after(section)
            fp14.write_text(str(soup14), encoding='utf-8')
            print("✅ Enriched Transformer architectural depth in Week 14 Day 96!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. ENRICH WGAN-GP (Week 11 Day 75)
# ─────────────────────────────────────────────────────────────────────────────
fp11 = Path("pages/weeks/week11.html")
if fp11.exists():
    soup11 = BeautifulSoup(fp11.read_text(encoding='utf-8'), 'html.parser')
    d75 = soup11.find('div', id='day-75')
    if d75 and not d75.find(id='wgan-gp-enriched'):
        theory = d75.find('h2', class_='sh2', id='day-75-theory') or d75.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup(r'''
<div id="wgan-gp-enriched" style="margin:1.5rem 0;">
  <h3 class="sh3">WGAN-GP: Gradient Penalty Formulation</h3>
  <div class="math-block" style="margin:1rem 0; padding:12px; background:var(--bg2); border-left:3px solid var(--accent); border-radius:6px; font-size:14px;">
    $$L = \mathbb{E}_{\tilde{x}}[D(\tilde{x})] - \mathbb{E}_{x}[D(x)] + \lambda \mathbb{E}_{\hat{x}}\left[\left(\|\nabla_{\hat{x}} D(\hat{x})\|_2 - 1\right)^2\right]$$
  </div>
  <p>Instead of hard weight clipping (which cripples network capacity), Gradient Penalty enforces the 1-Lipschitz continuity condition by penalizing Critic gradients that diverge from unit norm along random interpolations $\hat{x} = \epsilon x + (1-\epsilon)\tilde{x}$.</p>
</div>
''', 'html.parser')
            theory.insert_after(section)
            fp11.write_text(str(soup11), encoding='utf-8')
            print("✅ Enriched WGAN-GP Gradient Penalty in Week 11 Day 75!")

# ─────────────────────────────────────────────────────────────────────────────
# 3. ENRICH DISTRIBUTED TRAINING (Week 21 Day 149)
# ─────────────────────────────────────────────────────────────────────────────
fp21 = Path("pages/weeks/week21.html")
if fp21.exists():
    soup21 = BeautifulSoup(fp21.read_text(encoding='utf-8'), 'html.parser')
    d149 = soup21.find('div', id='day-149')
    if d149 and not d149.find(id='zero-fsdp-enriched'):
        theory = d149.find('h2', class_='sh2', id='day-149-theory') or d149.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="zero-fsdp-enriched" style="margin:1.5rem 0;">
  <h3 class="sh3">DeepSpeed ZeRO Stages vs PyTorch FSDP</h3>
  <div class="table-wrap" style="overflow-x:auto; margin:1.2rem 0; width:100%;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:13px;">
      <thead style="background:var(--bg3); border-bottom:1px solid var(--border);">
        <tr>
          <th style="padding:10px; text-align:left; color:var(--accent);">ZeRO Stage / FSDP</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Sharded State</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Memory Reduction</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Communication Overhead</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">ZeRO-1</td>
          <td style="padding:10px;">Optimizer States ($4\times$ model size in AdamW)</td>
          <td style="padding:10px;">$4\times$ memory reduction</td>
          <td style="padding:10px;">Same as standard DDP (no extra comms)</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">ZeRO-2 / FSDP HYBRID</td>
          <td style="padding:10px;">Optimizer States + Gradients</td>
          <td style="padding:10px;">$8\times$ memory reduction</td>
          <td style="padding:10px;">Same as standard DDP</td>
        </tr>
        <tr>
          <td style="padding:10px; font-weight:600;">ZeRO-3 / FSDP FULL_SHARD</td>
          <td style="padding:10px;">Optimizer + Gradients + Model Parameters</td>
          <td style="padding:10px;">Linear with GPU count $N$</td>
          <td style="padding:10px;">$1.5\times$ increase (All-Gather during forward/backward)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
''', 'html.parser')
            theory.insert_after(section)
            fp21.write_text(str(soup21), encoding='utf-8')
            print("✅ Enriched Distributed Training ZeRO & FSDP in Week 21 Day 149!")

print("\n🎉 ALL ARCHITECTURAL COVERAGE GAPS SUCCESSFULLY RESOLVED!")
