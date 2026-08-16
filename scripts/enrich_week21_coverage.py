#!/usr/bin/env python3
"""
Inject Distributed ZeRO/FSDP into Week 21 Day 150 and QLoRA Rank Mathematics into Day 153.
"""

from pathlib import Path
from bs4 import BeautifulSoup

fp21 = Path("pages/weeks/week21.html")
soup21 = BeautifulSoup(fp21.read_text(encoding='utf-8'), 'html.parser')

# 1. Day 150: Distributed Inference & ZeRO / FSDP
d150 = soup21.find('div', id='day-150')
if d150 and not d150.find(id='zero-fsdp-enriched'):
    theory = d150.find('h2', class_='sh2', id='day-150-theory') or d150.find('h2', class_='sh2')
    if theory:
        section = BeautifulSoup('''
<div id="zero-fsdp-enriched" style="margin:1.5rem 0;">
  <h3 class="sh3">Distributed Serving: DeepSpeed ZeRO Stages vs Tensor Parallelism</h3>
  <div class="table-wrap" style="overflow-x:auto; margin:1.2rem 0; width:100%;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:13px;">
      <thead style="background:var(--bg3); border-bottom:1px solid var(--border);">
        <tr>
          <th style="padding:10px; text-align:left; color:var(--accent);">Parallelism Strategy</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Sharded Components</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Serving vs Training Use Case</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">Tensor Parallelism (TP)</td>
          <td style="padding:10px;">Splits linear layer weight matrices across GPUs (Column/Row Parallel)</td>
          <td style="padding:10px;">Ultra-low latency real-time inference (vLLM, TensorRT-LLM) within single node (NVLink)</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">Pipeline Parallelism (PP)</td>
          <td style="padding:10px;">Distributes different Transformer layers across sequential GPUs/nodes</td>
          <td style="padding:10px;">Massive 70B–405B models spanning multiple nodes where weights exceed single-node VRAM</td>
        </tr>
        <tr>
          <td style="padding:10px; font-weight:600;">DeepSpeed ZeRO-3 / FSDP</td>
          <td style="padding:10px;">Shards optimizer states, gradients, and model weights across cluster</td>
          <td style="padding:10px;">Distributed fine-tuning with zero parameter redundancy across dozens of GPUs</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
''', 'html.parser')
        theory.insert_after(section)
        print("✅ Enriched Distributed Serving & ZeRO Parallelism in Week 21 Day 150!")

# 2. Day 153: QLoRA & Low-Rank Adaptation Mathematics
d153 = soup21.find('div', id='day-153')
if d153 and not d153.find(id='qlora-math-enriched'):
    theory = d153.find('h2', class_='sh2', id='day-153-theory') or d153.find('h2', class_='sh2')
    if theory:
        section = BeautifulSoup('''
<div id="qlora-math-enriched" style="margin:1.5rem 0;">
  <h3 class="sh3">LoRA Matrix Factorization & 4-bit NormalFloat (NF4) Quantization</h3>
  <div class="math-block" style="margin:1rem 0; padding:12px; background:var(--bg2); border-left:3px solid var(--accent); border-radius:6px; font-size:14px;">
    $$W_{\text{adapted}} = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A) \quad \text{where } A \in \mathbb{R}^{r \times d_{in}}, \, B \in \mathbb{R}^{d_{out} \times r}, \, r \ll \min(d_{in}, d_{out})$$
  </div>
  <p>QLoRA freezes base weights $W_0$ in information-theoretically optimal <strong>NF4</strong> format and computes gradients solely for low-rank adapter matrices $A$ and $B$, cutting VRAM by 75% with zero quality loss.</p>
</div>
''', 'html.parser')
        theory.insert_after(section)
        print("✅ Enriched QLoRA Low-Rank Adaptation Mathematics in Week 21 Day 153!")

fp21.write_text(str(soup21), encoding='utf-8')
print("✅ Saved Week 21 with enriched distributed architecture & QLoRA depth!")
