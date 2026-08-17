#!/usr/bin/env python3
"""
scripts/clean_mermaid_arrows.py
Replaces escaped HTML entities (--&gt; -> -->, -.-&gt; -> -.->) inside Mermaid diagrams across all YAML files.
"""

import glob, re

yaml_files = sorted(glob.glob("src/data/week*.yaml"))

for yf in yaml_files:
    with open(yf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace escaped arrows safely
    new_content = content.replace("--&gt;", "-->")
    new_content = new_content.replace("-.-&gt;", "-.->")
    
    if new_content != content:
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Cleaned Mermaid arrows in {yf}")

print("=== ALL YAML MERMAID ARROWS CLEANED ===")
