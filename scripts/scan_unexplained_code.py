#!/usr/bin/env python3
"""
Scan for code blocks with zero comments or bare execution calls like `mlflow.autolog()` with no inline explanations,
and catalog all code blocks that lack step-by-step explanatory comments across all 26 weeks.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
unexplained_code_blocks = []

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        for i, cb in enumerate(ds.find_all('div', class_='cb')):
            pre = cb.find('pre')
            if not pre: continue
            code = pre.text.strip()
            
            # Check comment ratio
            lines = [l.strip() for l in code.split('\n') if l.strip()]
            comment_lines = [l for l in lines if l.startswith('#') or l.startswith('//')]
            
            # Specifically check for MLflow, DVC, TorchServe, vLLM, ONNX, TensorRT, Triton calls
            has_enterprise_tool = any(tool in code.lower() for tool in ['mlflow', 'dvc', 'torchserve', 'vllm', 'onnx', 'tensorrt', 'triton', 'wandb', 'optuna', 'fastapi'])
            
            if len(comment_lines) == 0 and len(lines) > 3:
                unexplained_code_blocks.append({
                    "week": wn,
                    "day": did,
                    "index": i + 1,
                    "reason": "Zero comments in code block",
                    "code_snippet": code[:140]
                })
            elif has_enterprise_tool and len(comment_lines) <= 1:
                unexplained_code_blocks.append({
                    "week": wn,
                    "day": did,
                    "index": i + 1,
                    "reason": f"Enterprise tool without step-by-step commentary",
                    "code_snippet": code[:140]
                })

print(f"Found {len(unexplained_code_blocks)} code blocks lacking line-by-line pedagogical commentary.")
out_file = Path("scripts/unexplained_code_blocks.json")
out_file.write_text(json.dumps(unexplained_code_blocks, indent=2), encoding='utf-8')
print(f"Saved catalog to {out_file}")
