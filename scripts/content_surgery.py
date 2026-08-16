#!/usr/bin/env python3
"""
Content Surgery — Fix 4 confirmed real bugs:
1. Week 20: Replace identical RL Softmax formula on Days 144-149 with correct day-specific formulas
2. Week 20: The shared LangGraph code skeleton in Days 144-149 (documented, not auto-replaced — too risky)
3. Week 21 Day 156: Replace wrong plan_node/execute_node solution with vLLM deployment code
4. Week 23 Day 166: Replace off-topic Quiz Q3 (ALB) and Q4 (Rate Limiting) with Lambda-relevant questions
"""
import re
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# ─── FIX 1 & 2: Week 20 — Replace per-day formulas ───────────────────────────

# The formula that appears on ALL 7 days (only correct for Day 143 ReAct):
REACT_FORMULA = r'$$P(a_t \mid s_t) = \text{Softmax}(\text{LLM}(s_t, a_{1:t-1}, o_{1:t-1}))$$'

# Correct formula per day (only replacing days 144-149; 143 keeps the original):
CORRECT_FORMULAS = {
    '144': r'$$\hat{y} = \text{validate}(\text{LLM}(x), \text{schema}) \quad \text{where violations} \Rightarrow \text{retry}_{k}, k \leq K$$',
    '145': r'$$s_{t+1} = \delta(s_t, a_t) \quad \text{where } \delta: S \times A \rightarrow S \text{ (LangGraph transition function)}$$',
    '146': r'$$\text{Task}(i) = \text{Agent}_i(\text{context}_i, \text{tools}_i), \quad \text{Result} = \bigoplus_{i=1}^{N} \text{Task}(i)$$',
    '147': r'$$\text{resolve}(e_i, e_j) = \mathbb{1}\left[\text{sim}(\text{emb}(e_i), \text{emb}(e_j)) > \tau\right]$$',
    '148': r'$$\text{approve}(s_t) = \begin{cases} \text{continue} & \text{if human\_ok}(s_t) = 1 \\ \text{interrupt} & \text{otherwise} \end{cases}$$',
    '149': r'$$\text{System} = \text{Orchestrator}\left(\bigoplus_{k} \text{Agent}_k(\text{tools}_k, \text{memory}_k)\right)$$',
}

fp20 = WEEKS_DIR / "week20.html"
html20 = fp20.read_text(encoding='utf-8', errors='replace')
original20 = html20

day_boundaries = {}
for m in re.finditer(r'id="day-(\d+)"', html20):
    day_boundaries[m.group(1)] = m.start()

# Sort days by position
sorted_days = sorted(day_boundaries.items(), key=lambda x: x[1])

changes_made = 0
for i, (day, start_pos) in enumerate(sorted_days):
    if day not in CORRECT_FORMULAS:
        continue
    # Get end boundary (next day start or end of file)
    if i + 1 < len(sorted_days):
        end_pos = sorted_days[i + 1][1]
    else:
        end_pos = len(html20)
    
    day_segment = html20[start_pos:end_pos]
    
    # Find the Softmax formula in this segment
    if 'Softmax' in day_segment:
        new_formula = CORRECT_FORMULAS[day]
        new_segment = day_segment.replace(REACT_FORMULA, new_formula, 1)
        if new_segment != day_segment:
            html20 = html20[:start_pos] + new_segment + html20[end_pos:]
            # Recompute boundaries after replacement (length changed)
            delta = len(new_segment) - len(day_segment)
            for j in range(i + 1, len(sorted_days)):
                k, v = sorted_days[j]
                sorted_days[j] = (k, v + delta)
            changes_made += 1
            print(f"  ✅ Day {day}: Replaced formula with {new_formula[:60]}...")

if html20 != original20:
    fp20.write_text(html20, encoding='utf-8')
    print(f"\n✅ Week 20 saved — {changes_made} formula(s) replaced")
else:
    print("\n⚠️ Week 20 — No formula replacements made (check formula string encoding)")

# Verify
html20_check = fp20.read_text(encoding='utf-8', errors='replace')
remaining_softmax = len(re.findall('Softmax', html20_check))
print(f"Remaining Softmax instances in week20: {remaining_softmax} (expected: 1 — only Day 143)")

# ─── FIX 3: Week 21 Day 156 — Fix wrong solution code ────────────────────────
print(f"\n{'='*60}")
print("FIX 3: Week 21 Day 156 — Replace wrong solution block")
print(f"{'='*60}")

fp21 = WEEKS_DIR / "week21.html"
html21 = fp21.read_text(encoding='utf-8', errors='replace')
original21 = html21

# Find the plan_node/execute_node block in Day 156
# First confirm it's in Day 156
idx_156 = html21.rfind('id="day-156"')
if idx_156 < 0:
    print("❌ Day 156 not found")
else:
    idx_end_156 = len(html21)  # last day
    day156_html = html21[idx_156:]
    
    # Find the bad solution block containing plan_node
    # The solution block is wrapped in a solution container
    bad_code_start = day156_html.find('plan_node')
    if bad_code_start < 0:
        print("❌ plan_node not found in Day 156")
    else:
        # Find the <code> block containing plan_node
        # Go back to find the opening <code> tag
        code_open = day156_html.rfind('<code', 0, bad_code_start)
        code_close_marker = day156_html.find('</code>', bad_code_start)
        
        if code_open >= 0 and code_close_marker >= 0:
            old_code = day156_html[code_open:code_close_marker + len('</code>')]
            print(f"Found bad code block ({len(old_code)} chars)")
            print(f"Preview: {re.sub(r'<[^>]+>','',old_code[:200]).strip()}")
            
            # Replace with correct vLLM deployment + QLoRA merge code
            NEW_VLLM_CODE = '''<code class="language-python"><span class="kw">import</span> subprocess
<span class="kw">import</span> json
<span class="kw">import</span> requests
<span class="kw">from</span> pathlib <span class="kw">import</span> Path

<span class="cm"># ── Step 1: Merge QLoRA adapter into base model ──────────────────</span>
<span class="kw">from</span> peft <span class="kw">import</span> AutoPeftModelForCausalLM
<span class="kw">from</span> transformers <span class="kw">import</span> AutoTokenizer
<span class="kw">import</span> torch

<span class="fn">def</span> <span class="fn">merge_qlora_adapter</span>(
    base_model_id: <span class="bi">str</span>,
    adapter_path: <span class="bi">str</span>,
    output_dir: <span class="bi">str</span>
) -&gt; <span class="bi">str</span>:
    <span class="st">"""Merge QLoRA adapter weights into base model and save."""</span>
    <span class="kw">print</span>(<span class="st">f"Loading adapter from <span class="bi">{adapter_path}</span>..."</span>)
    model = AutoPeftModelForCausalLM.from_pretrained(
        adapter_path,
        device_map=<span class="st">"auto"</span>,
        torch_dtype=torch.bfloat16,
    )
    merged = model.merge_and_unload()  <span class="cm"># fuse LoRA weights into base</span>
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    merged.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    <span class="kw">print</span>(<span class="st">f"✅ Merged model saved to <span class="bi">{output_dir}</span>"</span>)
    <span class="kw">return</span> output_dir

<span class="cm"># ── Step 2: Launch vLLM server ────────────────────────────────────</span>
<span class="fn">def</span> <span class="fn">launch_vllm_server</span>(model_path: <span class="bi">str</span>, port: <span class="bi">int</span> = <span class="num">8000</span>) -&gt; <span class="bi">None</span>:
    <span class="st">"""Start vLLM OpenAI-compatible server as subprocess."""</span>
    cmd = [
        <span class="st">"python"</span>, <span class="st">"-m"</span>, <span class="st">"vllm.entrypoints.openai.api_server"</span>,
        <span class="st">"--model"</span>, model_path,
        <span class="st">"--port"</span>, <span class="bi">str</span>(port),
        <span class="st">"--dtype"</span>, <span class="st">"bfloat16"</span>,
        <span class="st">"--max-model-len"</span>, <span class="st">"4096"</span>,
        <span class="st">"--gpu-memory-utilization"</span>, <span class="st">"0.90"</span>,
    ]
    <span class="kw">print</span>(<span class="st">f"Starting vLLM server on port <span class="bi">{port}</span>..."</span>)
    subprocess.Popen(cmd)  <span class="cm"># non-blocking; server runs in background</span>

<span class="cm"># ── Step 3: Query the deployed model ─────────────────────────────</span>
<span class="fn">def</span> <span class="fn">query_vllm</span>(prompt: <span class="bi">str</span>, port: <span class="bi">int</span> = <span class="num">8000</span>) -&gt; <span class="bi">str</span>:
    <span class="st">"""Send an inference request to vLLM OpenAI-compatible endpoint."""</span>
    response = requests.post(
        <span class="st">f"http://localhost:<span class="bi">{port}</span>/v1/chat/completions"</span>,
        json={
            <span class="st">"model"</span>: <span class="st">"merged-qlora-model"</span>,
            <span class="st">"messages"</span>: [{<span class="st">"role"</span>: <span class="st">"user"</span>, <span class="st">"content"</span>: prompt}],
            <span class="st">"max_tokens"</span>: <span class="num">512</span>,
            <span class="st">"temperature"</span>: <span class="num">0.1</span>,
        },
        timeout=<span class="num">60</span>
    )
    <span class="kw">return</span> response.json()[<span class="st">"choices"</span>][<span class="num">0</span>][<span class="st">"message"</span>][<span class="st">"content"</span>]

<span class="cm"># ── Main: Full pipeline ───────────────────────────────────────────</span>
<span class="kw">if</span> __name__ == <span class="st">"__main__"</span>:
    merged_path = merge_qlora_adapter(
        base_model_id=<span class="st">"mistralai/Mistral-7B-v0.1"</span>,
        adapter_path=<span class="st">"./qlora-adapter"</span>,
        output_dir=<span class="st">"./merged-mistral-7b"</span>,
    )
    launch_vllm_server(merged_path, port=<span class="num">8000</span>)
    
    <span class="kw">import</span> time; time.sleep(<span class="num">30</span>)  <span class="cm"># wait for server startup</span>
    answer = query_vllm(<span class="st">"Explain LoRA in one sentence."</span>)
    <span class="kw">print</span>(<span class="st">f"Model response: <span class="bi">{answer}</span>"</span>)</code>'''
            
            html21 = html21[:idx_156 + code_open] + NEW_VLLM_CODE + html21[idx_156 + code_close_marker + len('</code>'):]
            print(f"✅ Replaced bad plan_node code with vLLM deployment pipeline")

if html21 != original21:
    fp21.write_text(html21, encoding='utf-8')
    print("✅ Week 21 saved")
else:
    print("⚠️ Week 21 — no changes saved")

# ─── FIX 4: Week 23 Day 166 — Fix off-topic quiz Q3 & Q4 ─────────────────────
print(f"\n{'='*60}")
print("FIX 4: Week 23 Day 166 — Fix off-topic quiz questions Q3 & Q4")
print(f"{'='*60}")

fp23 = WEEKS_DIR / "week23.html"
html23 = fp23.read_text(encoding='utf-8', errors='replace')
original23 = html23

# Find day 166 boundaries
idx_166 = html23.rfind('id="day-166"')
# Find next day
idx_167 = html23.find('id="day-167"')
if idx_167 < 0: idx_167 = len(html23)

day166_html = html23[idx_166:idx_167]

# Find Q3: Application Load Balancer question
alb_q_match = re.search(
    r'(<div\s+class="quiz-q"[^>]*>)[^<]*[Aa]pplication\s+Load\s+Balancer[^<]*</div>',
    day166_html
)
rate_q_match = re.search(
    r'(<div\s+class="quiz-q"[^>]*>)[^<]*[Rr]ate\s+[Ll]imiting[^<]*</div>',
    day166_html
)

print(f"Q3 (ALB) found: {alb_q_match is not None}")
print(f"Q4 (Rate Limiting) found: {rate_q_match is not None}")

# Because rewriting full quiz blocks with options/answers is very complex 
# (need to rewrite answers too), we'll find and replace the question TEXT only
# and mark the surrounding quiz block for what it tests

# Replace Q3 (ALB) with Lambda container image size question
if alb_q_match:
    old_q3_text = alb_q_match.group(0)
    new_q3_text = old_q3_text.replace(
        alb_q_match.group(0),
        alb_q_match.group(1) + "What is the maximum container image size supported by AWS Lambda, and why does this constrain ML model deployments?</div>"
    )
    # Note: This replaces just the question text; the answer options also need updating
    # but we can't safely infer them without seeing the full quiz block structure
    print(f"Q3 replacement ready: Lambda container image size limit question")

# Replace Q4 (Rate Limiting) with Lambda cold start question  
if rate_q_match:
    old_q4_text = rate_q_match.group(0)
    new_q4_text = old_q4_text.replace(
        rate_q_match.group(0),
        rate_q_match.group(1) + "Which technique most effectively reduces Lambda cold-start latency for large ML models deployed as container images?</div>"
    )
    print(f"Q4 replacement ready: Lambda cold-start mitigation question")

# To do a safe replacement, we need to see the full quiz block structure
# Let's extract and print the Q3 and Q4 blocks to verify before replacing
q3_block_start = day166_html.find("Application Load Balancer")
if q3_block_start >= 0:
    # Go back to find quiz item container
    quiz_item_start = day166_html.rfind('class="quiz-item"', 0, q3_block_start)
    quiz_item_end = day166_html.find('</div>', q3_block_start + 200)
    quiz_item_end = day166_html.find('class="quiz-item"', quiz_item_end)
    
    q3_block = day166_html[quiz_item_start:quiz_item_end] if quiz_item_start >= 0 else ""
    print(f"\nQ3 block (first 500 chars):")
    print(re.sub(r'<[^>]+>', '', q3_block[:500]).strip())

print("\n⚠️ Q3/Q4 replacement skipped — need to see full quiz block structure with answer options")
print("Run: python3 -c \"see_quiz_block.py\" to extract full Q3/Q4 blocks for safe replacement")
print("Manual fix recommended for quiz content to preserve correct answer marking")
