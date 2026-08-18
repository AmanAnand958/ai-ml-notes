#!/usr/bin/env python3
"""
scripts/repair_all_diagrams_and_katex.py
Repairs:
1. All corrupted LaTeX control characters (\t, \f, \r, \b, \a, \v) in HTML and YAML.
2. All Mermaid diagram syntax errors across all weeks.
3. All SVG attribute spacing and unescaped ampersands in SVGs.
"""

import os
import re
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def fix_latex_corruptions(text):
    # Fix control characters that replaced backslashed latex commands
    # 1. Form feed (\x0c) -> \f
    text = re.sub(r'\x0crac', r'\\frac', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])\x0crac', r'\\frac', text)
    
    # 2. Bell (\x07) -> \a
    text = re.sub(r'\x07lpha', r'\\alpha', text)
    text = re.sub(r'\x07pprox', r'\\approx', text)
    text = re.sub(r'\x07st', r'\\ast', text)
    
    # 3. Vertical tab (\x0b) -> \v
    text = re.sub(r'\x0bec', r'\\vec', text)
    text = re.sub(r'\x0bspace', r'\\vspace', text)

    # 4. Backspace (\x08) -> \b
    text = re.sub(r'\x08egin', r'\\begin', text)
    text = re.sub(r'\x08eta', r'\\beta', text)
    text = re.sub(r'\x08ar', r'\\bar', text)
    text = re.sub(r'\x08ig', r'\\big', text)

    # 5. Carriage return (\x0d) -> \r or \r followed by ight
    text = re.sub(r'\x0dight', r'\\right', text)
    text = re.sub(r'\r(?=ight)', r'\\r', text)

    # 6. Tab (\x09) before common latex commands
    tab_cmds = [
        'text', 'times', 'theta', 'tau', 'to', 'textbf', 'textit', 'texttt', 'tanh', 'top', 
        'tilde', 'tan', 'triangle', 'tag', 'tfrac'
    ]
    for cmd in tab_cmds:
        text = re.sub(r'\t' + cmd, r'\\' + cmd, text)

    # 7. Unescaped word-level corruptions in math contexts
    # ' ight' -> '\right' inside math
    # Specific math fixes
    text = text.replace(r' ight)', r'\right)')
    text = text.replace(r' ight]', r'\right]')
    text = text.replace(r' ight\}', r'\right\}')
    text = text.replace(r' ight|', r'\right|')
    text = text.replace(r' ight.', r'\right.')
    text = text.replace(r' ight', r'\right')

    # Fix \left[ ... \right] or \left( ... \right) where \right was missing \
    # Fix instances of ' ext{' in math
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])ext\{', r'\\text{', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])imes(?=[\s\{])', r'\\times', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])heta(?=[\s\}_])', r'\\theta', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])lpha(?=[\s\}_])', r'\\alpha', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])eta(?=[\s\}_])', r'\\beta', text)
    text = re.sub(r'(?<=[\$\s\{=\+\-\*\(\[,;])ec\{', r'\\vec{', text)

    # Week 18 specific case equation
    text = text.replace(r'p(\theta \mid y) =  egin{cases}', r'p(\theta \mid y) = \begin{cases}')
    text = text.replace(r'\ell(\theta) & \text{if } y < y^* \ g(\theta)', r'\ell(\theta) & \text{if } y < y^* \\ g(\theta)')
    text = text.replace(r'C \times \text{Payload}_{\text{size}} ight)', r'C \times \text{Payload}_{\text{size}} \right)')

    # Week 20 specific:
    text = text.replace(r'\text{Score}(m) = \cos(\vec{q}, \vec{v}_m) \times e^{-\lambda \Delta t}', r'\text{Score}(m) = \cos(\vec{q}, \vec{v}_m) \times e^{-\lambda \Delta t}')
    text = text.replace(r'\alpha  0.7', r'\alpha \approx 0.7')
    text = text.replace(r'\alpha = 2r', r'\alpha = 2r')
    text = text.replace(r'\alpha=32', r'\alpha=32')

    # Week 22 cases:
    text = text.replace(r'\text{CacheHit}(\vec{q}, \vec{k}) =  egin{cases}', r'\text{CacheHit}(\vec{q}, \vec{k}) = \begin{cases}')
    text = text.replace(r'\ge \tau \ \text{Forward}', r'\ge \tau \\ \text{Forward}')

    # Week 9 inline math with &lt;
    text = text.replace(r'x_2^{int} &lt; x_1^{int}', r'x_2^{int} < x_1^{int}')
    text = text.replace(r'y_2^{int} &lt; y_1^{int}', r'y_2^{int} < y_1^{int}')

    return text

def fix_mermaid_diagrams(text):
    # Week 19 Day 136 Hybrid search
    old_w19 = """graph TD
    Query["User Query: 'Troubleshoot error 0x80070005 in Azure VM'"] --> Fork{"Query Dispatcher"}
    Fork -->|Dense Bi-Encoder| DenseSearch["Dense Vector Index (HNSW / Cosine Similarity)"]
    Fork -->|Sparse Tokenizer / BM25| SparseSearch["Sparse Lexical Index (Inverted Index / BM25)"]
    DenseSearch -->|Ranked List D (Top 50)| RRF["Reciprocal Rank Fusion (RRF) Engine
score = sum( 1 / (60 + rank_i) )"]
    SparseSearch -->|Ranked List S (Top 50)| RRF
    RRF --> TopK["Fused & Deduplicated Candidates (Top 20)"]
    TopK --> Reranker["Cross-Encoder Reranker (BGE-Reranker-Large)"]
    Reranker --> FinalContext["Final Top-5 Grounded Contexts -> LLM Context Window"]"""
    
    fixed_w19 = """graph TD
    Query["User Query: 'Troubleshoot error 0x80070005 in Azure VM'"] --> Fork{"Query Dispatcher"}
    Fork -->|Dense Bi-Encoder| DenseSearch["Dense Vector Index - HNSW / Cosine Similarity"]
    Fork -->|Sparse Tokenizer / BM25| SparseSearch["Sparse Lexical Index - Inverted Index / BM25"]
    DenseSearch -->|Ranked List D - Top 50| RRF["Reciprocal Rank Fusion Engine<br/>score = sum( 1 / (60 + rank_i) )"]
    SparseSearch -->|Ranked List S - Top 50| RRF
    RRF --> TopK["Fused and Deduplicated Candidates - Top 20"]
    TopK --> Reranker["Cross-Encoder Reranker - BGE-Reranker-Large"]
    Reranker --> FinalContext["Final Top-5 Grounded Contexts to LLM Context Window"]"""
    
    text = text.replace(old_w19, fixed_w19)

    # Week 10 Diagram #2:
    old_w10_2 = """graph LR
  CellPrev["Cell State C_{t-1}"] -->|x Forget Gate f_t| CellCurr["Cell State C_t"]
  Input["Input x_t and Hidden h_{t-1}"] --> ForgetGate["Forget Gate: sigma(W_f)"]
  Input --> InputGate["Input Gate: sigma(W_i) * tanh(W_c)"]
  InputGate -->|+ Add to Cell State| CellCurr
  CellCurr -->|tanh * Output Gate sigma(W_o)| HiddenCurr["Hidden State h_t"]"""

    fixed_w10_2 = """graph LR
  CellPrev["Cell State C_{t-1}"] -->|x Forget Gate f_t| CellCurr["Cell State C_t"]
  Input["Input x_t and Hidden h_{t-1}"] --> ForgetGate["Forget Gate: sigma(W_f)"]
  Input --> InputGate["Input Gate: sigma(W_i) * tanh(W_c)"]
  InputGate -->|+ Add to Cell State| CellCurr
  CellCurr -->|tanh * Output Gate sigma W_o| HiddenCurr["Hidden State h_t"]"""

    text = text.replace(old_w10_2, fixed_w10_2)

    # Week 20 Diagram #2:
    old_w20_2 = """graph LR
    Prompt["User Prompt + Pydantic Schema"] --> LLM["LLM Inference Core (OpenAI / vLLM)"]
    LLM --> RawText["Raw JSON String"]
    RawText --> Validator{"Pydantic Type Validation"}
    Validator -->|Valid Schema| Success["Typed Python Object Instance"]
    Validator -->|ValidationError (e.g. Invalid UUID)| SelfHeal["Instructor Self-Correction Loop
Feed Validation Error Diff back to LLM"]
    SelfHeal --> LLM"""

    fixed_w20_2 = """graph LR
    Prompt["User Prompt + Pydantic Schema"] --> LLM["LLM Inference Core - OpenAI / vLLM"]
    LLM --> RawText["Raw JSON String"]
    RawText --> Validator{"Pydantic Type Validation"}
    Validator -->|Valid Schema| Success["Typed Python Object Instance"]
    Validator -->|ValidationError - Invalid UUID| SelfHeal["Instructor Self-Correction Loop<br/>Feed Validation Error Diff back to LLM"]
    SelfHeal --> LLM"""

    text = text.replace(old_w20_2, fixed_w20_2)

    # Week 5 Diagram #5:
    old_w5_5 = """graph TD
  F1["Fold 1"] --> V1["Val"] and T1["Train"] and T2["Train"] and T3["Train"]
  F2["Fold 2"] --> T4["Train"] and V2["Val"] and T5["Train"] and T6["Train"]
  F3["Fold 3"] --> T7["Train"] and T8["Train"] and V3["Val"] and T9["Train"]
  F4["Fold 4"] --> T10["Train"] and T11["Train"] and T12["Train"] and V4["Val"]"""

    fixed_w5_5 = """graph TD
  F1["Fold 1"] --> V1["Validation Fold (20%)"]
  F1 --> T1["Training Folds (80%)"]
  F2["Fold 2"] --> V2["Validation Fold (20%)"]
  F2 --> T2["Training Folds (80%)"]
  F3["Fold 3"] --> V3["Validation Fold (20%)"]
  F3 --> T3["Training Folds (80%)"]
  F4["Fold 4"] --> V4["Validation Fold (20%)"]
  F4 --> T4["Training Folds (80%)"]"""

    text = text.replace(old_w5_5, fixed_w5_5)

    # Week 8 Diagram #3:
    old_w8_3 = """graph LR
  X["Input X"] -->|Forward Pass: z = w*x + b| Linear["Linear Neuron: z"]
  Linear -->|Forward Pass: a = sigma(z)| Activation["Activation: sigma(z)"]
  Activation -->|Forward Pass: L = Loss(a,y)| Loss["Loss Node: L"]
  Loss -->|Backward Pass: dL/da| Activation
  Activation -->|Backward Pass: dL/dz = dL/da * sigma_prime(z)| Linear
  Linear -->|Backward Pass: dL/dw = dL/dz * x| Weights["Gradient dL/dw"]"""

    fixed_w8_3 = """graph LR
  X["Input X"] -->|Forward Pass: z = w*x + b| Linear["Linear Neuron: z"]
  Linear -->|Forward Pass: a = sigma z| Activation["Activation: sigma(z)"]
  Activation -->|Forward Pass: L = Loss a,y| Loss["Loss Node: L"]
  Loss -->|Backward Pass: dL/da| Activation
  Activation -->|Backward Pass: dL/dz = dL/da * sigma_prime z| Linear
  Linear -->|Backward Pass: dL/dw = dL/dz * x| Weights["Gradient dL/dw"]"""

    text = text.replace(old_w8_3, fixed_w8_3)

    return text

def fix_svg_formatting(text):
    # Fix missing spaces between attributes in SVG tags
    # e.g. xmlns="http://www.w3.org/2000/svg"style= -> xmlns="http://www.w3.org/2000/svg" style=
    text = re.sub(r'\"(style|role|aria-label|height|width|viewBox|xmlns)=', r'" \1=', text)
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    new_content = fix_latex_corruptions(content)
    new_content = fix_mermaid_diagrams(new_content)
    new_content = fix_svg_formatting(new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
        return True
    return False

def main():
    html_files = sorted(glob.glob(os.path.join(ROOT_DIR, 'pages/weeks/week*.html')))
    yaml_files = sorted(glob.glob(os.path.join(ROOT_DIR, 'src/data/week*.yaml')))
    script_files = sorted(glob.glob(os.path.join(ROOT_DIR, 'scripts/*.py')))

    count = 0
    for f in html_files + yaml_files:
        if process_file(f):
            count += 1
    print(f"\nCompleted processing. {count} files updated.")

if __name__ == '__main__':
    main()
