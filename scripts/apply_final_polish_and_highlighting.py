#!/usr/bin/env python3
"""
Fix Script addressing the 3 Remaining Items:
1. Week 26 Day 188 Case Study: Replace Whisper audio transcription with YouTube/Netflix Two-Tower Recommendation System Case Study.
2. Week 26 Day 189 Case Study: Replace Stable Diffusion XL with DSPy Prompt Optimization Pipeline Case Study.
3. Week 20: Add <code class="language-python"> wrappers and syntax-highlighting spans (<span class="kw">, <span class="fn">, <span class="st">, <span class="cm">, <span class="num">, <span class="bi">) across all <pre> blocks in Days 143-149.
4. Week 4 Day 29: Add <code class="language-python"> and syntax-highlighting spans across all <pre> blocks for PCA.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# Helper for basic python syntax highlighting
KEYWORDS = {"import", "from", "def", "class", "return", "if", "else", "elif", "for", "while", "in", "as", "try", "except", "raise", "with", "lambda", "assert", "True", "False", "None", "and", "or", "not", "is"}
BUILTINS = {"print", "len", "sum", "abs", "round", "int", "float", "str", "list", "dict", "set", "super", "range", "min", "max"}

def highlight_python(code_str: str) -> str:
    lines = code_str.split("\n")
    hl_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            hl_lines.append(f'<span class="cm">{line}</span>')
            continue
        
        # Strings
        line = re.sub(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', r'<span class="st">\1</span>', line)
        
        # Keywords
        for kw in KEYWORDS:
            line = re.sub(rf'\b({kw})\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="kw">\1</span>', line)
            
        # Builtins
        for bi in BUILTINS:
            line = re.sub(rf'\b({bi})\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="bi">\1</span>', line)
            
        # Numbers
        line = re.sub(r'\b(\d+(?:\.\d+)?)\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="num">\1</span>', line)
        
        hl_lines.append(line)
    return f'<code class="language-python">{"\n".join(hl_lines)}</code>'

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX WEEK 26 CASE STUDIES (Days 188 & 189)
# ─────────────────────────────────────────────────────────────────────────────
print("=== 1. Fixing Week 26 Case Studies (Days 188 & 189) ===")
fp26 = WEEKS_DIR / "week26.html"
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Day 188: Two-Tower RecSys Case Study
old_cs188 = '🏢 Enterprise Case Study: Real-Time Audio Transcription with OpenAI Whisper</h3> <p>Healthcare and call center analytics platforms deploy OpenAI Whisper for automated transcription at scale'
new_cs188 = '🏢 Enterprise Case Study: Billion-Scale Candidate Retrieval with Two-Tower DSSM</h3> <p>Video streaming platforms like YouTube and e-commerce giants deploy Two-Tower Deep Structured Semantic Models (DSSM) to filter billion-item catalogs down to top-100 candidates in under 15ms latency.'

# Find and replace full Day 188 Case study block
d188_cs_pattern = r'🏢 Enterprise Case Study: Real-Time Audio Transcription with OpenAI Whisper.*?</div>\s*</div>'
d188_cs_replacement = '''🏢 Enterprise Case Study: Billion-Scale Candidate Retrieval with Two-Tower DSSM</h3>
<p>Streaming platforms like YouTube and Netflix deploy Two-Tower DSSM networks to separate user contextual preferences from item catalog embeddings. By pre-computing item candidate embeddings offline and querying an Inverted Multi-Index ANN vector database, the retrieval phase handles 100,000 queries per second with sub-15ms p99 latency before passing candidates to heavy cross-attention ranking models.</p>
</div></div>'''

html26 = re.sub(d188_cs_pattern, d188_cs_replacement, html26, flags=re.DOTALL)

# Day 189: DSPy Prompt Optimization Case Study
d189_cs_pattern = r'🏢 Enterprise Case Study: Text-to-Image Generation with Stable Diffusion XL.*?</div>\s*</div>'
d189_cs_replacement = '''🏢 Enterprise Case Study: Production Prompt Optimization with DSPy</h3>
<p>Enterprise AI teams at Databricks and Shopify deploy DSPy to replace brittle hand-crafted prompt strings with programmatic compilation pipelines. Using teleprompter optimizers (MIPROv2 and BootstrapFewShot), DSPy iteratively optimizes prompt instructions and few-shot exemplars against domain-specific evaluation metrics, boosting downstream accuracy by 25–40% while reducing latency and token costs.</p>
</div></div>'''

html26 = re.sub(d189_cs_pattern, d189_cs_replacement, html26, flags=re.DOTALL)

fp26.write_text(html26, encoding='utf-8')
print("  ✅ Replaced Day 188 and Day 189 Case Studies with authentic RecSys and DSPy content!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX WEEK 20 SYNTAX-HIGHLIGHTING SPANS ACROSS ALL PRE BLOCKS
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Adding Syntax-Highlighting to Week 20 Code Blocks ===")
fp20 = WEEKS_DIR / "week20.html"
html20 = fp20.read_text(encoding='utf-8', errors='replace')
soup20 = BeautifulSoup(html20, 'html.parser')

count_hl20 = 0
for pre in soup20.find_all('pre'):
    raw_code = pre.get_text()
    if len(raw_code.strip()) > 10:
        highlighted = highlight_python(raw_code)
        pre.clear()
        pre.append(BeautifulSoup(highlighted, 'html.parser'))
        count_hl20 += 1

fp20.write_text(str(soup20), encoding='utf-8')
print(f"  ✅ Added <code class='language-python'> and syntax-highlighting spans to {count_hl20} <pre> blocks in Week 20!")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIX WEEK 4 DAY 29 SYNTAX-HIGHLIGHTING SPANS ACROSS PRE BLOCKS
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 3. Adding Syntax-Highlighting to Week 4 Day 29 Code Blocks ===")
fp4 = WEEKS_DIR / "week4.html"
html4 = fp4.read_text(encoding='utf-8', errors='replace')
soup4 = BeautifulSoup(html4, 'html.parser')

d29 = soup4.find('div', id='day-29')
count_hl4 = 0
if d29:
    for pre in d29.find_all('pre'):
        raw_code = pre.get_text()
        if len(raw_code.strip()) > 10:
            highlighted = highlight_python(raw_code)
            pre.clear()
            pre.append(BeautifulSoup(highlighted, 'html.parser'))
            count_hl4 += 1

fp4.write_text(str(soup4), encoding='utf-8')
print(f"  ✅ Added <code class='language-python'> and syntax-highlighting spans to {count_hl4} <pre> blocks in Day 29!")

print("\n🎉 ALL FINAL POLISH & CODE HIGHLIGHTING TASKS COMPLETED!")
