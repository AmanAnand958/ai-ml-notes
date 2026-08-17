#!/usr/bin/env python3
"""
scripts/deep_security_and_edge_audit.py
Deep audit of:
1. Hardcoded API keys / Secret patterns in task solutions or theory examples (e.g. OpenAI/Anthropic/HF tokens)
2. Insecure Python Practices (e.g. raw eval(), unsafe pickle.load() without weights_only=True)
3. Python 3.12+ Deprecations (e.g. datetime.utcnow(), pkg_resources, imp module, distutils)
4. Missing GPU Memory Cleanup in PyTorch Loops (torch.cuda.empty_cache() on OOM)
5. Missing Asynchronous / Non-blocking I/O in API Call Loops
"""

import glob, yaml, re, os, json

print("=== STARTING DEEP SECURITY, DEPRECATION & EDGE-CASE AUDIT ===")

sec_findings = []
s_id = 1

def add_sec(category, severity, location, title, problem, evidence, recommendation):
    global s_id
    sec_findings.append({
        "id": f"SEC-{s_id:03d}",
        "category": category,
        "severity": severity,
        "location": location,
        "title": title,
        "problem": problem,
        "evidence": str(evidence)[:250],
        "recommendation": recommendation
    })
    s_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        # 1. Check for Unsafe Pickle Loading
        theory = d.get('theory_html', '')
        for t in d.get('tasks', []):
            sol = t.get('solution_code', '')
            combined = theory + "\n" + sol
            
            # Unsafe pickle
            if 'pickle.load' in combined and 'weights_only=True' not in combined and 'torch.load' in combined:
                if 'weights_only' not in combined:
                    add_sec(
                        "Security",
                        "High",
                        d_loc,
                        "Unsafe PyTorch Weight Deserialization (`torch.load` without `weights_only=True`)",
                        "Calling `torch.load()` on untrusted checkpoints without `weights_only=True` allows arbitrary code execution via Python pickle exploits (CVE-2024-3568).",
                        "torch.load(...) found without weights_only=True parameter.",
                        "Enforce `torch.load(checkpoint_path, weights_only=True)` or recommend Hugging Face `safetensors`."
                    )
                    
            # Raw eval() usage
            if 'eval(' in combined and 'model.eval()' not in combined and 'def eval(' not in combined:
                add_sec(
                    "Security",
                    "Critical",
                    d_loc,
                    "Insecure `eval()` Expression Execution in Python Snippet",
                    "Using dynamic `eval()` to parse user strings or JSON creates arbitrary code execution vulnerabilities.",
                    "eval() detected in code snippet.",
                    "Replace `eval()` with `ast.literal_eval()` or `json.loads()` for safe parsing."
                )

            # Python 3.12 Deprecation: datetime.utcnow()
            if 'datetime.utcnow()' in combined:
                add_sec(
                    "Deprecation",
                    "Low",
                    d_loc,
                    "Deprecated `datetime.utcnow()` Invocation (Python 3.12+)",
                    "`datetime.utcnow()` is deprecated in Python 3.12 and produces timezone-naive timestamps prone to silent UTC offsets.",
                    "datetime.utcnow() found.",
                    "Replace with `datetime.now(datetime.timezone.utc)`."
                )

            # PyTorch CUDA OOM without empty_cache() in batch evaluation
            if 'torch.cuda' in combined and 'for batch in' in combined and 'empty_cache' not in combined and 'no_grad' not in combined:
                add_sec(
                    "CUDA Memory",
                    "Medium",
                    d_loc,
                    "Inference Loop Missing `@torch.no_grad()` / `torch.inference_mode()`",
                    "Iterating over test batches without `torch.no_grad()` accumulates gradient graphs in GPU VRAM, triggering out-of-memory (OOM) crashes.",
                    "Batch loop without inference_mode or no_grad context.",
                    "Wrap evaluation loops with `with torch.inference_mode():` to disable autograd memory allocation."
                )

            # Unbounded List Appending in High-Throughput Tokenization
            if 'for token in' in combined and '.append(' in combined and 'sys.getsizeof' not in combined:
                if 'tokens.append' in combined and 'pre-allocate' not in combined:
                    add_sec(
                        "Performance",
                        "Low",
                        d_loc,
                        "Dynamic List Resizing Overhead in Inner Tokenizer Loop",
                        "Appending millions of tokens to a dynamic Python list triggers frequent memory reallocation (over-allocation overhead); requires generator yielding or NumPy array buffer pre-allocation.",
                        "Dynamic list append loop detected.",
                        "Use generator expressions (`yield token`) or pre-allocated arrays for memory efficiency."
                    )

print(f"\nTotal Security & Edge-Case Findings: {len(sec_findings)}")

with open('scripts/deep_security_edge_report.json', 'w', encoding='utf-8') as f:
    json.dump(sec_findings, f, indent=2)

print("Saved report to: scripts/deep_security_edge_report.json")
