#!/usr/bin/env python3
"""
Comprehensive Content Enrichment & Gap Closure Script
1. Extracts & populates deep theory for Weeks 18-26 from markdown + v0 snapshot.
2. Replaces dead resource links in Weeks 19-26 with verified real URLs.
3. Replaces generic task titles with descriptive titles across all weeks.
4. Populates concept_flow for Week 5 & Week 9.
5. Fixes mistagged hinglish in Week 1 Day 1 and Week 5 Day 33.
6. Backfills gotcha callouts for Weeks 1-18.
"""

import os
import glob
import yaml
import re
import markdown
from bs4 import BeautifulSoup

def clean_html_str(elem):
    if not elem:
        return ""
    html = str(elem)
    html = re.sub(r'^\s*<div[^>]*>', '', html)
    html = re.sub(r'</div>\s*$', '', html)
    return html.strip()

def enrich_week18():
    with open('v0_snapshot/pages/weeks/week18.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    with open('src/data/week18.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for day in data.get('days', []):
        raw_id = day['id']
        ds = soup.find('div', id=f'day-{raw_id}')
        if not ds:
            continue

        # Extract theory
        theory_parts = []
        for c in ds.children:
            if getattr(c, 'name', None) == 'div' and 'callout' in c.get('class', []):
                if 'ci' not in c.get('class', []):
                    # Check if it has math-block or svg or mermaid
                    if c.find('div', class_=['math-block', 'mermaid', 'svg-diagram-container']) or len(c.get_text(strip=True)) > 200:
                        theory_parts.append(str(c))
        
        if theory_parts:
            day['theory_html'] = '\n'.join(theory_parts)

        # Extract misconception / gotcha
        misc = ds.find('div', class_='misconception') or ds.find('div', class_='cw')
        if misc and not day.get('gotcha'):
            p = misc.find('p')
            day['gotcha'] = {
                'title': '⚠️ Common Pitfall & Gotcha',
                'description': p.get_text(strip=True) if p else misc.get_text(strip=True)
            }

    with open('src/data/week18.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print("✓ Enriched Week 18 theory and gotchas")

def parse_markdown_weeks():
    """Extract theory, real resources, and descriptive tasks from content/md/week19.md - week26.md"""
    curated_resources = {
        19: [
            {"type": "PAPER", "title": "Reciprocal Rank Fusion in Information Retrieval (Cormack et al.)", "url": "https://dl.acm.org/doi/10.1145/1571941.1572114", "desc": "Foundational paper on rank fusion formulas"},
            {"type": "DOCS", "title": "Pinecone Hybrid Search & Sparse-Dense Vectors", "url": "https://docs.pinecone.io/guides/data/understanding-hybrid-search", "desc": "Implementing BM25 + dense retrieval in production"},
            {"type": "GUIDE", "title": "LlamaIndex Advanced Retrieval & Reranking", "url": "https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/", "desc": "Cross-encoders, Cohere rerankers, and sentence window chunking"},
            {"type": "ARTICLE", "title": "GraphRAG: Unlocking LLM Discovery on Structured Graphs", "url": "https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-complex-information/", "desc": "Microsoft Research GraphRAG architecture"}
        ],
        20: [
            {"type": "PAPER", "title": "ReAct: Synergizing Reasoning and Acting in Language Models", "url": "https://arxiv.org/abs/2210.03629", "desc": "The seminal ReAct framework paper by Yao et al."},
            {"type": "DOCS", "title": "LangGraph Multi-Agent Workflows & Cyclic State Machines", "url": "https://langchain-ai.github.io/langgraph/", "desc": "Building stateful, multi-actor LLM applications"},
            {"type": "FRAMEWORK", "title": "CrewAI: Framework for Orchestrating Role-Playing AI Agents", "url": "https://docs.crewai.com/", "desc": "Production multi-agent collaboration"},
            {"type": "GUIDE", "title": "Human-in-the-Loop Agent Interruption Patterns", "url": "https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/", "desc": "Safe tool execution with approval breakpoints"}
        ],
        21: [
            {"type": "PAPER", "title": "QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al.)", "url": "https://arxiv.org/abs/2305.14314", "desc": "NF4 quantization, Double Quantization, and Paged Optimizers"},
            {"type": "DOCS", "title": "Hugging Face PEFT: State-of-the-Art Parameter-Efficient Fine-Tuning", "url": "https://huggingface.co/docs/peft/index", "desc": "LoRA, AdaLoRA, and Prefix Tuning implementation"},
            {"type": "TUTORIAL", "title": "Direct Preference Optimization (DPO) Training Guide", "url": "https://huggingface.co/blog/dpo-trl", "desc": "TRL alignment without a separate reward model"},
            {"type": "BENCHMARK", "title": "EleutherAI LM Evaluation Harness", "url": "https://github.com/EleutherAI/lm-evaluation-harness", "desc": "Standardized evaluation suite for open LLMs"}
        ],
        22: [
            {"type": "PAPER", "title": "vLLM: Efficient Memory Management for LLM Serving with PagedAttention", "url": "https://arxiv.org/abs/2309.06180", "desc": "PagedAttention algorithms and continuous batching"},
            {"type": "DOCS", "title": "NVIDIA Triton Inference Server Documentation", "url": "https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html", "desc": "Multi-model GPU orchestration and dynamic batching"},
            {"type": "DOCS", "title": "TGI (Text Generation Inference) Production Guide", "url": "https://huggingface.co/docs/text-generation-inference/index", "desc": "Streaming, flash attention, and tensor parallelism"},
            {"type": "GUIDE", "title": "OpenAI Semantic Caching with Redis & Vector Similarity", "url": "https://redis.io/solutions/semantic-caching/", "desc": "Sub-millisecond prompt caching architecture"}
        ],
        23: [
            {"type": "PAPER", "title": "FlashAttention-2: Faster Attention with Better Parallelism", "url": "https://arxiv.org/abs/2307.08691", "desc": "Tri Dao's IO-aware exact attention acceleration"},
            {"type": "DOCS", "title": "OpenAI Triton: GPU Programming for Neural Networks", "url": "https://triton-lang.org/main/index.html", "desc": "Writing custom CUDA-grade kernels in Python"},
            {"type": "GUIDE", "title": "NVIDIA TensorRT-LLM High-Performance Inference", "url": "https://github.com/NVIDIA/TensorRT-LLM", "desc": "Kernel fusion, FP8 GEMM, and In-Flight Batching"},
            {"type": "TOOL", "title": "PyTorch 2.0 torch.compile & Inductor Compiler Deep Dive", "url": "https://pytorch.org/get-started/pytorch-2.0/", "desc": "Graph capture, FX graphs, and C++ codegen"}
        ],
        24: [
            {"type": "DOCS", "title": "MLflow 2.0: Unified LLMOps & Experiment Tracking", "url": "https://mlflow.org/docs/latest/index.html", "desc": "Prompt tracking, evaluation datasets, and model registry"},
            {"type": "DOCS", "title": "Evidently AI: Production Model Drift & Data Quality", "url": "https://docs.evidentlyai.com/", "desc": "Automated KS-tests, PSI calculations, and drift alerts"},
            {"type": "FRAMEWORK", "title": "Feast: Production Open Source Feature Store", "url": "https://docs.feast.dev/", "desc": "Point-in-time correct joins for training and online serving"},
            {"type": "TOOL", "title": "Great Expectations: Data Testing and Validation", "url": "https://greatexpectations.io/", "desc": "Data pipeline assertion suites"}
        ],
        25: [
            {"type": "DOCS", "title": "Kubernetes HPA (Horizontal Pod Autoscaler) with Custom Metrics", "url": "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/", "desc": "Prometheus-driven GPU autoscaling"},
            {"type": "DOCS", "title": "KServe: Cloud Native Model Serving on Kubernetes", "url": "https://kserve.github.io/website/", "desc": "Serverless ML inference with canary rollouts"},
            {"type": "GUIDE", "title": "Helm Charts for Machine Learning Deployments", "url": "https://helm.sh/docs/", "desc": "Templating multi-service AI architectures"},
            {"type": "TUTORIAL", "title": "Argo Workflows for Automated ML Pipelines", "url": "https://argoproj.github.io/argo-workflows/", "desc": "DAG-based continuous training loops"}
        ],
        26: [
            {"type": "PAPER", "title": "LLaVA: Large Language and Vision Assistant", "url": "https://arxiv.org/abs/2304.08485", "desc": "Visual instruction tuning with projection matrices"},
            {"type": "PAPER", "title": "CLIP: Learning Transferable Visual Models From Natural Language", "url": "https://arxiv.org/abs/2103.00020", "desc": "Contrastive multimodal pre-training by Radford et al."},
            {"type": "DOCS", "title": "OpenAI Whisper Speech Recognition Architecture", "url": "https://github.com/openai/whisper", "desc": "Robust speech transcription and translation"},
            {"type": "FRAMEWORK", "title": "DSPy: Programming—not prompting—Foundation Models", "url": "https://dspy-docs.vercel.app/", "desc": "Declarative self-optimizing LM pipelines"}
        ]
    }

    for wnum in range(19, 27):
        yaml_path = f"src/data/week{wnum:02d}.yaml"
        md_path = f"content/md/week{wnum}.md"

        if not os.path.exists(yaml_path) or not os.path.exists(md_path):
            continue

        with open(yaml_path, 'r', encoding='utf-8') as f:
            ydata = yaml.safe_load(f)

        with open(md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        # Split MD by day headers
        day_sections = re.split(r'(?m)^WEEK \d+ · DAY \d+', md_text)
        day_sections = [s for s in day_sections if s.strip()]

        for idx, day in enumerate(ydata.get('days', [])):
            if idx < len(day_sections):
                d_sec = day_sections[idx]
                
                # Extract Theory section from MD
                m_theory = re.search(r'## 🧠 Theory\n(.*?)(?=\n##|\Z)', d_sec, re.DOTALL)
                if m_theory:
                    raw_th = m_theory.group(1).strip()
                    # Convert markdown to HTML safely using markdown package
                    converted_html = markdown.markdown(raw_th, extensions=['fenced_code', 'tables'])
                    
                    # Wrap with BeautifulSoup to add class='cb' and copy/run buttons
                    soup_th = BeautifulSoup(converted_html, 'html.parser')
                    for h3 in soup_th.find_all('h3'):
                        h3['class'] = 'sh3'
                    for pre in soup_th.find_all('pre'):
                        code_tag = pre.find('code')
                        code_txt = code_tag.get_text() if code_tag else pre.get_text()
                        
                        cb_div = soup_th.new_tag('div', attrs={'class': 'cb'})
                        cb_head = soup_th.new_tag('div', attrs={'class': 'cb-head'})
                        
                        cb_lang = soup_th.new_tag('span', attrs={'class': 'cb-lang'})
                        cb_lang.string = 'python'
                        cb_head.append(cb_lang)
                        
                        cb_btns = soup_th.new_tag('div', attrs={'class': 'cb-btns'})
                        btn_copy = soup_th.new_tag('button', attrs={'class': 'copy-btn', 'onclick': 'copyCode(this)'})
                        btn_copy.string = 'copy'
                        btn_run = soup_th.new_tag('button', attrs={'class': 'run-btn', 'onclick': 'runCode(this)'})
                        btn_run.string = 'Run'
                        cb_btns.append(btn_copy)
                        cb_btns.append(btn_run)
                        cb_head.append(cb_btns)
                        
                        cb_div.append(cb_head)
                        new_pre = soup_th.new_tag('pre')
                        new_pre.string = code_txt
                        cb_div.append(new_pre)
                        
                        pre.replace_with(cb_div)
                    
                    day['theory_html'] = f'<div class="theory-prose" style="line-height:1.7; font-size:14.5px; color:var(--text);">\n{str(soup_th)}\n</div>'

            # Populate Curated Real Resources
            if wnum in curated_resources:
                res_list = curated_resources[wnum]
                day['resources'] = res_list

            # Fix Generic Task Titles
            for t_idx, task in enumerate(day.get('tasks', [])):
                t_title = task.get('title', '')
                if t_title in ['Task 1', 'Task 2', 'Task 3', 'Task']:
                    # Generate descriptive title from task prompt
                    prompt = task.get('prompt_html', '')
                    cleaned_p = re.sub(r'<[^>]+>', '', prompt).strip()
                    first_sentence = cleaned_p.split('.')[0].replace('Write a function to ', '').replace('Implement ', '').replace('Build ', '').strip()
                    if first_sentence and len(first_sentence) < 60:
                        task['title'] = f"Task {t_idx+1}: {first_sentence.title()}"
                    else:
                        task['title'] = f"Task {t_idx+1}: Implement {day.get('title', 'Pipeline Step')}"

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(ydata, f, allow_unicode=True, sort_keys=False)
        print(f"✓ Enriched Week {wnum} theory, real resources, and descriptive tasks")

def fix_special_gaps():
    # 1. Week 1 Day 1 hinglish fix
    with open('src/data/week01.yaml', 'r', encoding='utf-8') as f:
        w1 = yaml.safe_load(f)
    for d in w1['days']:
        if d['id'] == '1':
            d['hinglish'] = "Python bilkul human language jaisi simple aur readable hai. Isme curly braces `{}` ki jagah indentation `(tabs/spaces)` use hoti hai code blocks define karne ke liye."
    with open('src/data/week01.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(w1, f, allow_unicode=True, sort_keys=False)
    print("✓ Fixed Week 1 Day 1 hinglish")

    # 2. Week 5 Day 33 hinglish fix + concept_flow
    with open('src/data/week05.yaml', 'r', encoding='utf-8') as f:
        w5 = yaml.safe_load(f)
    w5_flow = ["Data Ingestion", "Train/Test Split", "Baseline Model", "Evaluation Metrics", "Error Analysis", "Iterative Tuning", "Production Thresholding"]
    for d in w5['days']:
        if d['id'] == '33':
            d['hinglish'] = "Classification models evaluate karte waqt sirf Accuracy kafi nahi hoti agar data imbalanced ho. Precision aur Recall ka harmonic mean (F1-score) real performance dikhata hai."
        if not d.get('concept_flow'):
            d['concept_flow'] = w5_flow
    with open('src/data/week05.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(w5, f, allow_unicode=True, sort_keys=False)
    print("✓ Fixed Week 5 Day 33 hinglish & concept_flow")

    # 3. Week 9 concept_flow fix
    with open('src/data/week09.yaml', 'r', encoding='utf-8') as f:
        w9 = yaml.safe_load(f)
    w9_flow = ["Pixel Grids & Convolutions", "Feature Maps & Pooling", "CNN Backbones (ResNet)", "Transfer Learning", "Object Detection (YOLO)", "Semantic Segmentation", "Vision Deployment"]
    for d in w9['days']:
        if not d.get('concept_flow'):
            d['concept_flow'] = w9_flow
    with open('src/data/week09.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(w9, f, allow_unicode=True, sort_keys=False)
    print("✓ Fixed Week 9 concept_flow")

    # 4. Backfill gotchas for Weeks 1-17
    gotcha_defaults = {
        1: ("Indentation & Variable References", "Python does not copy lists on assignment `b = a`; it references the same memory address. Use `b = a.copy()` to avoid accidental mutations."),
        2: ("Dictionary Keys & List Mutability", "Never use mutable data types (like lists) as dictionary keys or default function arguments (`def func(x=[])`)."),
        3: ("NumPy In-Place vs Copy Operations", "NumPy slicing returns a view, not a copy. Modifying a slice directly mutates the original array."),
        4: ("Matrix Multiplications & Transpose Alignment", "Always verify inner dimensions match before matrix multiplication: `(M, K) @ (K, N) -> (M, N)`."),
        5: ("Data Leakage in Preprocessing", "Never fit scalers or encoders on the entire dataset. Always fit strictly on the training set, then transform test/validation sets."),
        6: ("Gradient Descent Vanishing & Explosions", "Unnormalized input features lead to oscillating gradients and slow convergence. Always normalize features before gradient descent."),
        7: ("Learning Rate & Optimizer Overshooting", "Too high learning rate leads to exploding loss (`NaN`). If loss explodes, reduce LR by 10x immediately."),
        8: ("Cross-Entropy Loss Input Expectations", "PyTorch's `nn.CrossEntropyLoss` expects raw logits as input and automatically applies Softmax. Do NOT pass Softmax outputs into it!"),
        9: ("Tensor Shape Permutations in PyTorch vs OpenCV", "OpenCV uses `(H, W, C)` in BGR format, whereas PyTorch CNNs expect `(B, C, H, W)` in RGB normalized float."),
        10: ("RNN Hidden State Retention", "Always detach hidden states when backpropagating through time across batches to prevent memory explosions."),
        11: ("Multi-Head Attention Scale Factor", "Dividing by `sqrt(d_k)` prevents dot-product values from growing huge and pushing Softmax into near-zero gradient regions."),
        12: ("Positional Embeddings in Transformer Ingestion", "Self-attention has zero concept of word order without adding positional encodings (Sinusoidal or RoPE)."),
        13: ("Tokenizer Special Tokens Handling", "Missing `<|endoftext|>` or `[CLS]` tokens causes silent evaluation bugs and degraded generation coherence."),
        14: ("Quantization Scale Calibration", "Post-training quantization requires representative calibration datasets to calculate dynamic scales accurately."),
        15: ("CUDA Out-of-Memory (OOM) Overhead", "PyTorch allocates memory in cached chunks. Use `torch.cuda.empty_cache()` and gradient accumulation when batch sizes hit limits."),
        16: ("Distributed Data Parallel (DDP) Gradient Sync", "Ensure all processes initialize identical random seeds and model weights before starting DDP training loops."),
        17: ("Docker Container GPU Runtime Passthrough", "Always pass `--gpus all` and verify NVIDIA Container Toolkit is initialized in production Docker daemon.")
    }

    for wnum in range(1, 18):
        ypath = f"src/data/week{wnum:02d}.yaml"
        if not os.path.exists(ypath):
            continue
        with open(ypath, 'r', encoding='utf-8') as f:
            ydata = yaml.safe_load(f)
        
        title, desc = gotcha_defaults.get(wnum, ("Common Pitfall", "Always validate input tensor dimensions and data types before executing computation pipelines."))
        for d in ydata.get('days', []):
            if not d.get('gotcha'):
                d['gotcha'] = {
                    'title': f"⚠️ Gotcha: {title}",
                    'description': desc
                }
        with open(ypath, 'w', encoding='utf-8') as f:
            yaml.dump(ydata, f, allow_unicode=True, sort_keys=False)
    print("✓ Backfilled gotchas across Weeks 1-17")

if __name__ == '__main__':
    enrich_week18()
    parse_markdown_weeks()
    fix_special_gaps()
