#!/usr/bin/env python3
"""
scripts/inject_bonus_content.py
Appends 5 Senior-Engineer Bonus Deep Dives to YAML and HTML files non-destructively:
1. Day 18 (Week 3): Polars & DuckDB Out-of-Core Processing
2. Day 54 (Week 8): PyTorch 2.x Compiler Internals (torch.compile & Triton Inductor)
3. Day 88 (Week 13): Tokenizer Production Traps (Token-Healing & Glitch Tokens)
4. Day 98 (Week 14): Contrastive Vision-Language Learning (CLIP & InfoNCE Loss)
5. Day 130 (Week 19): Production KV Cache Sizing & Capacity Planning Equation
"""

import glob, yaml, re, os, json, html

print("=== STARTING NON-DESTRUCTIVE BONUS CONTENT INJECTIONS ===")

BONUS_SECTIONS = {
    # 1. Day 18 (Week 3)
    (3, 18): '''\n<div class="bonus-deep-dive" style="background:var(--bg3); border-left:4px solid var(--accent); padding:1.2rem; border-radius:8px; margin:1.5rem 0;">
<h3 class="sh3" style="color:var(--accent); margin-top:0;">🎁 Senior Engineer Bonus: Out-of-Core Processing with Polars & DuckDB</h3>
<p>
While Pandas loads entire tables eagerly into RAM with high object-pointer overhead, production ML pipelines handle <strong>50GB–1TB datasets</strong> on single developer workstations using modern out-of-core columnar query engines:
</p>
<ul>
  <li><strong>Polars</strong>: Written in Rust on Apache Arrow memory layouts. Uses <em>LazyFrame</em> query graphs with automatic predicate pushdown and multi-threaded parallel execution.</li>
  <li><strong>DuckDB</strong>: In-process analytical SQL engine executing vectorized queries directly on partitioned disk Parquet files without loading full tables into RAM.</li>
</ul>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — polars_and_duckdb.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)">Run</button></div></div>
<pre><code><span class="kw">import</span> polars <span class="kw">as</span> pl
<span class="kw">import</span> duckdb

<span class="cm"># 1. Polars Lazy Execution Graph (zero memory allocated until collect)</span>
q = (
    pl.<span class="fn">scan_parquet</span>(<span class="str">"large_dataset.parquet"</span>)
    .<span class="fn">filter</span>(pl.<span class="fn">col</span>(<span class="str">"age"</span>) > <span class="num">25</span>)
    .<span class="fn">group_by</span>(<span class="str">"country"</span>)
    .<span class="fn">agg</span>(pl.<span class="fn">col</span>(<span class="str">"income"</span>).<span class="fn">mean</span>().<span class="fn">alias</span>(<span class="str">"avg_income"</span>))
)
<span class="cm"># Explain optimized query plan without execution:</span>
<span class="fn">print</span>(<span class="str">"Polars Query Plan:"</span>, q.<span class="fn">explain</span>())

<span class="cm"># 2. DuckDB Out-of-Core SQL directly on disk Parquet files</span>
con = duckdb.<span class="fn">connect</span>()
df_summary = con.<span class="fn">execute</span>(<span class="str">"""
    SELECT country, AVG(income) as avg_inc 
    FROM read_parquet('large_dataset.parquet') 
    GROUP BY country 
    HAVING count(*) > 1000
"""</span>).<span class="fn">df</span>()
<span class="fn">print</span>(<span class="str">"DuckDB Out-of-Core Execution Complete."</span>)</code></pre>
</div>
</div>\n''',

    # 2. Day 54 (Week 8)
    (8, 54): '''\n<div class="bonus-deep-dive" style="background:var(--bg3); border-left:4px solid var(--accent); padding:1.2rem; border-radius:8px; margin:1.5rem 0;">
<h3 class="sh3" style="color:var(--accent); margin-top:0;">🎁 Senior Engineer Bonus: PyTorch 2.x Compiler Stack (`torch.compile` & Inductor)</h3>
<p>
PyTorch 2.x eliminates Python interpreter dispatch latency and kernel memory bandwidth bottlenecks through its 3-tier compiler architecture:
</p>
<ol>
  <li><strong>TorchDynamo</strong>: Intercepts Python frame evaluation bytecode via CPython hooks and safely extracts computation graphs into FX graphs at runtime.</li>
  <li><strong>AOTAutograd</strong>: Traces forward and backward autograd graphs ahead-of-time before execution.</li>
  <li><strong>TorchInductor</strong>: The default compiler backend that generates optimized <em>OpenAI Triton</em> C++/CUDA kernels, automatically fusing point-wise activations (e.g. GeLU + LayerNorm + Residual Add) into single GPU SRAM passes.</li>
</ol>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — torch_compile_inductor.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)">Run</button></div></div>
<pre><code><span class="kw">import</span> torch
<span class="kw">import</span> torch.nn <span class="kw">as</span> nn

<span class="kw">class</span> <span class="cls">DeepTransformerBlock</span>(nn.Module):
    <span class="kw">def</span> <span class="fn">__init__</span>(self, dim: <span class="bi">int</span> = <span class="num">512</span>):
        <span class="bi">super</span>().<span class="fn">__init__</span>()
        self.norm = nn.<span class="fn">LayerNorm</span>(dim)
        self.linear = nn.<span class="fn">Linear</span>(dim, dim)
        self.act = nn.<span class="fn">GELU</span>()
        
    <span class="kw">def</span> <span class="fn">forward</span>(self, x: torch.Tensor) -> torch.Tensor:
        <span class="kw">return</span> x + self.<span class="fn">act</span>(self.<span class="fn">linear</span>(self.<span class="fn">norm</span>(x)))

model = <span class="cls">DeepTransformerBlock</span>().<span class="fn">to</span>(<span class="str">"cpu"</span>)

<span class="cm"># Compile model with Inductor kernel fusion and CUDA graph capture</span>
opt_model = torch.<span class="fn">compile</span>(model, mode=<span class="str">"reduce-overhead"</span>, backend=<span class="str">"inductor"</span>)
x = torch.<span class="fn">randn</span>(<span class="num">16</span>, <span class="num">128</span>, <span class="num">512</span>)
out = <span class="fn">opt_model</span>(x)
<span class="fn">print</span>(<span class="str">f"Compiled output shape: {list(out.shape)} with fused Triton kernel execution."</span>)</code></pre>
</div>
</div>\n''',

    # 3. Day 88 (Week 13)
    (13, 88): '''\n<div class="bonus-deep-dive" style="background:var(--bg3); border-left:4px solid var(--accent); padding:1.2rem; border-radius:8px; margin:1.5rem 0;">
<h3 class="sh3" style="color:var(--accent); margin-top:0;">🎁 Senior Engineer Bonus: Tokenizer Traps (Token-Healing & Glitch Tokens)</h3>
<p>
Production LLM serving faces subtle tokenization traps that degrade generation quality if unhandled:
</p>
<ul>
  <li><strong>Trailing Whitespace Mismatch</strong>: Prompting <code>"The price is: "</code> ends on token <code>' '</code>. The model may expect subsequent tokens to begin with space (e.g. <code>' $10'</code>), but since space was already consumed, it falls back to a sub-optimal non-space token (<code>'$'</code>), distorting output probability distributions.</li>
  <li><strong>Token-Healing</strong>: Advanced engines (e.g. Guidance, SGLang) automatically roll back the final prompt token before generation, re-evaluating the prefix match to guarantee seamless lexical boundary transitions.</li>
  <li><strong>Glitch Tokens</strong>: Vocabulary entries (e.g. <code>SolidGoldMagikarp</code>) created from raw internet scraping that never received gradient updates during pretraining; inputting them causes model hallucination or safety guardrail bypass.</li>
</ul>
</div>\n''',

    # 4. Day 98 (Week 14)
    (14, 98): '''\n<div class="bonus-deep-dive" style="background:var(--bg3); border-left:4px solid var(--accent); padding:1.2rem; border-radius:8px; margin:1.5rem 0;">
<h3 class="sh3" style="color:var(--accent); margin-top:0;">🎁 Senior Engineer Bonus: Contrastive Vision-Language Learning (CLIP & InfoNCE)</h3>
<p>
Modern multimodal foundation models (GPT-4o, Stable Diffusion, LLaVA) are powered by <strong>Contrastive Language-Image Pretraining (CLIP)</strong>. Given a batch of $N$ image-text pairs with normalized embeddings $I_i$ and $T_i$, CLIP optimizes a symmetric <strong>InfoNCE Dual-Encoder Loss</strong>:
</p>
$$\\mathcal{L}_{\\text{CLIP}} = \\frac{1}{2N} \\sum_{i=1}^{N} \\left( -\\log \\frac{\\exp(I_i \\cdot T_i / \\tau)}{\\sum_{j=1}^N \\exp(I_i \\cdot T_j / \\tau)} - \\log \\frac{\\exp(T_i \\cdot I_i / \\tau)}{\\sum_{j=1}^N \\exp(T_i \\cdot I_j / \\tau)} \\right)$$
<p>
Where $\\tau$ is a learnable temperature parameter scaling similarity logits. This creates a shared metric space where image features and text concepts align seamlessly for zero-shot classification and dense retrieval.
</p>
</div>\n''',

    # 5. Day 130 (Week 19)
    (19, 130): '''\n<div class="bonus-deep-dive" style="background:var(--bg3); border-left:4px solid var(--accent); padding:1.2rem; border-radius:8px; margin:1.5rem 0;">
<h3 class="sh3" style="color:var(--accent); margin-top:0;">🎁 Senior Engineer Bonus: Production KV Cache Sizing & Capacity Planning Equation</h3>
<p>
In high-throughput LLM serving clusters (vLLM, TensorRT-LLM), the exact GPU VRAM requirement for the KV Cache is governed by:
</p>
$$\\text{KV Cache Bytes Per Token} = 2 \\times n_{\\text{layers}} \\times n_{\\text{kv\\_heads}} \\times d_{\\text{head}} \\times \\text{dtype\\_bytes}$$
$$\\text{Total VRAM Budget} = \\text{KV Bytes Per Token} \\times \\text{Max Sequence Length} \\times \\text{Concurrent Batch Size}$$
<div class="table-wrap" style="overflow-x:auto; margin:1rem 0;">
<table class="concept-table">
<tr><th>Model Architecture</th><th>Attention Type</th><th>KV Heads</th><th>KV Cache / Token</th><th>100 Concurrency (4k Context)</th></tr>
<tr><td><strong>Llama-2-70B</strong></td><td>Multi-Head (MHA)</td><td>64</td><td>$2.56\\text{ MB}$</td><td>$\\mathbf{1048.5\\text{ GB}}$ (14x A100 80GB)</td></tr>
<tr><td><strong>Llama-3-70B</strong></td><td>Grouped-Query (GQA)</td><td>8 ($8\\times$ reduction)</td><td>$320\\text{ KB}$</td><td>$\\mathbf{131.0\\text{ GB}}$ (2x A100 80GB)</td></tr>
<tr><td><strong>Llama-3-70B (FP8 KV)</strong></td><td>GQA + FP8 Quantization</td><td>8 ($16\\times$ reduction)</td><td>$160\\text{ KB}$</td><td>$\\mathbf{65.5\\text{ GB}}$ (1x A100 80GB)</td></tr>
</table>
</div>
<p style="font-size:13px; color:var(--muted);">
This capacity equation explains why modern frontier LLMs universally adopt Grouped-Query Attention (GQA) and FP8/FP4 KV caching to enable high concurrency in production environments.
</p>
</div>\n'''
}

# -------------------------------------------------------------
# 1. APPLY TO YAML DATA FILES
# -------------------------------------------------------------
print("Injecting bonus modules into YAML sources non-destructively...")
for (w_num, d_num), bonus_html in BONUS_SECTIONS.items():
    yf = f"src/data/week{w_num:02d}.yaml"
    if not os.path.exists(yf):
        continue
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        if d.get('day_num') == d_num:
            current_th = d.get('theory_html', '')
            if 'Senior Engineer Bonus:' not in current_th:
                d['theory_html'] = current_th + bonus_html
    with open(yf, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

print("✓ Injected bonus sections into YAML data sources.")

# -------------------------------------------------------------
# 2. SYNC TO HTML FILES
# -------------------------------------------------------------
print("Injecting bonus modules into HTML week portals non-destructively...")
for (w_num, d_num), bonus_html in BONUS_SECTIONS.items():
    hf = f"pages/weeks/week{w_num}.html"
    if not os.path.exists(hf):
        continue
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Senior Engineer Bonus:' not in content:
        # Find the day container and append before day tasks
        day_pattern = rf'(<div class="day-section[^"]*" id="day-{d_num}".*?)(<div class="tasks-section"|<div class="predict-section"|<div class="quiz-section")'
        match = re.search(day_pattern, content, re.DOTALL)
        if match:
            new_section = match.group(1) + bonus_html + match.group(2)
            content = content[:match.start()] + new_section + content[match.end():]
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(content)

print("✓ All HTML week files updated with bonus deep dive modules.")
print("\n=== BONUS CONTENT INJECTION COMPLETE ===")
