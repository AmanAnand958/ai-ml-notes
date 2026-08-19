#!/usr/bin/env python3
"""
scripts/replace_papers_with_tutorials_and_docs.py
Replaces all academic research paper / arXiv links across YAML and HTML files
with top Indian educators (Krish Naik, CampusX, Chai aur Code, CodeWithHarry)
and premier official documentation / recommended YouTube channels.
"""

import os, glob, re, yaml, html
from bs4 import BeautifulSoup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')
PAGES_DIR = os.path.join(ROOT_DIR, 'pages/weeks')

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)
yaml.SafeDumper.add_representer(LiteralStr, lit_repr)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

# Mapping of paper concepts to YouTube tutorial / Official Doc replacements
TOPIC_REPLACEMENTS = {
    # Week 9 (CNNs)
    'alexnet': {'title': 'Krish Naik — Deep Learning & CNN Architecture Masterclass', 'url': 'https://www.youtube.com/playlist?list=PLZoTAELRMXVPGU70ZGsckrMdr0FteeRUi'},
    'vgg': {'title': 'CampusX — Convolutional Neural Networks Deep Dive', 'url': 'https://www.youtube.com/@campusx-official'},
    'resnet': {'title': 'PyTorch Official — Torchvision Models & ResNet Documentation', 'url': 'https://pytorch.org/vision/stable/models.html'},
    'inception': {'title': 'StatQuest — Neural Networks and CNN Visual Intuition', 'url': 'https://www.youtube.com/@statquest'},
    'mobilenet': {'title': 'PyTorch Official — Transfer Learning for Computer Vision Tutorial', 'url': 'https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html'},
    'yolo': {'title': 'Krish Naik — Object Detection with YOLO & OpenCV in Python', 'url': 'https://www.youtube.com/@krishnaik06'},

    # Week 11 (GANs)
    'generative adversarial': {'title': 'Krish Naik — Generative Adversarial Networks (GANs) Explained', 'url': 'https://www.youtube.com/@krishnaik06'},
    'auto-encoding': {'title': 'PyTorch Official — DCGAN Training & Face Generation Tutorial', 'url': 'https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html'},

    # Week 12 (Attention & Seq2Seq)
    'neural machine translation': {'title': 'CampusX — Attention Mechanism & Seq2Seq Architecture', 'url': 'https://www.youtube.com/@campusx-official'},
    'bahdanau': {'title': 'PyTorch Official — NLP from Scratch: Translation with Sequence to Sequence Network', 'url': 'https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html'},

    # Week 14 (Transformers)
    'attention is all you need': {'title': 'Krish Naik — Complete Transformer Architecture from Scratch', 'url': 'https://www.youtube.com/@krishnaik06'},
    'transformer': {'title': 'Andrej Karpathy — Let\'s build GPT: from scratch, in code', 'url': 'https://www.youtube.com/watch?v=kCc8FmEb1nY'},

    # Week 19 (Advanced RAG)
    'hierarchical nsw': {'title': 'Chai aur Code (Hitesh Choudhary) — Vector Databases & HNSW Indexing Explained', 'url': 'https://www.youtube.com/@chaiaurcode'},
    'graph rag': {'title': 'Microsoft Official — GraphRAG Knowledge Engine Documentation', 'url': 'https://microsoft.github.io/graphrag/'},
    'hyde': {'title': 'Krish Naik — Advanced RAG with Query Transformation & HyDE', 'url': 'https://www.youtube.com/@krishnaik06'},
    'step back': {'title': 'LlamaIndex Official — Advanced Query Reformulation & Routing Guide', 'url': 'https://docs.llamaindex.ai/en/stable/optimizing/production_rag/'},

    # Week 20 (LLM Agents)
    'react': {'title': 'Krish Naik — LangGraph Full Course: Build Multi-Agent AI Systems', 'url': 'https://www.youtube.com/@krishnaik06'},
    'plan-and-solve': {'title': 'LangChain Official — Plan-and-Execute Agents Documentation', 'url': 'https://langchain-ai.github.io/langgraph/'},
    'autogen': {'title': 'Microsoft Official — AutoGen Multi-Agent Framework Documentation', 'url': 'https://microsoft.github.io/autogen/'},
    'metagpt': {'title': 'CampusX — AI Agents & Autonomous Execution Workflows', 'url': 'https://www.youtube.com/@campusx-official'},
    'memgpt': {'title': 'Instructor Official — Structured Outputs and Validation for LLMs', 'url': 'https://python.useinstructor.com/'},

    # Week 21 (vLLM, Quantization, Fine-Tuning)
    'pagedattention': {'title': 'vLLM Official — High-Throughput Serving Engine Documentation', 'url': 'https://docs.vllm.ai/en/latest/'},
    'flashattention': {'title': 'Andrej Karpathy — Fast LLM Inference & GPU Optimization Guide', 'url': 'https://www.youtube.com/@AndrejKarpathy'},
    'speculative decoding': {'title': 'vLLM Official — Speculative Decoding for Low-Latency Serving', 'url': 'https://docs.vllm.ai/en/latest/models/speculative_decoding.html'},
    'medusa': {'title': 'Hugging Face Official — Text Generation Inference (TGI) Guide', 'url': 'https://huggingface.co/docs/text-generation-inference/index'},
    'gptq': {'title': 'Hugging Face Official — Model Quantization with AutoGPTQ & AWQ', 'url': 'https://huggingface.co/docs/transformers/main/en/quantization'},
    'awq': {'title': 'Krish Naik — Quantizing LLMs with AWQ, GPTQ and GGUF for Fast Inference', 'url': 'https://www.youtube.com/@krishnaik06'},
    'lora': {'title': 'Hugging Face Official — PEFT (Parameter-Efficient Fine-Tuning) Guide', 'url': 'https://huggingface.co/docs/peft/index'},
    'qlora': {'title': 'Krish Naik — Fine-Tuning LLMs with QLoRA and Unsloth', 'url': 'https://www.youtube.com/@krishnaik06'},
    'direct preference optimization': {'title': 'Hugging Face Official — TRL (Transformer Reinforcement Learning: DPO, ORPO, GRPO)', 'url': 'https://huggingface.co/docs/trl/index'},
    'orpo': {'title': 'FreeCodeCamp — Fine-Tuning LLMs Masterclass Full Course', 'url': 'https://www.youtube.com/@freecodecamp'},
    'deepseekmath': {'title': 'Hugging Face Official — Preference Tuning & Alignment Documentation', 'url': 'https://huggingface.co/docs/trl/main/en/dpo_trainer'},
    'wizardlm': {'title': 'Chai aur Code — Synthetic Data Generation & Fine-Tuning Pipelines', 'url': 'https://www.youtube.com/@chaiaurcode'},
    'ultrafeedback': {'title': 'Argilla Official — Open Source Data Curation & Feedback Loops', 'url': 'https://docs.argilla.io/'},

    # Week 22 (Eval & Observability)
    'ragas': {'title': 'Ragas Official — RAG Assessment Framework Documentation', 'url': 'https://docs.ragas.io/en/stable/'},
    'mt-bench': {'title': 'Krish Naik — Evaluating LLM & RAG Pipelines using Ragas & LangSmith', 'url': 'https://www.youtube.com/@krishnaik06'},
    'gptcache': {'title': 'Arize Phoenix Official — LLM Tracing & Observability Guide', 'url': 'https://docs.arize.com/phoenix'},

    # Week 26 (Multimodal & System Design)
    'visual instruction tuning': {'title': 'Hugging Face Official — Vision-Language Models (LLaVA & SmolVLM) Guide', 'url': 'https://huggingface.co/docs/transformers/model_doc/llava'},
    'an image is worth': {'title': 'Krish Naik — Vision Transformers (ViT) Architecture & PyTorch Code', 'url': 'https://www.youtube.com/@krishnaik06'},
    'qwen2-vl': {'title': 'Hugging Face Official — Multimodal Generative AI Documentation', 'url': 'https://huggingface.co/docs/transformers/index'},
    'colpali': {'title': 'Qdrant Official — Multimodal Vector Search & Document Retrieval', 'url': 'https://qdrant.tech/documentation/'},
    'colbert': {'title': 'Krish Naik — Multimodal RAG with Vision-Language Models and Vector Stores', 'url': 'https://www.youtube.com/@krishnaik06'},
    'whisper': {'title': 'OpenAI Official — Whisper Speech Recognition Python Guide', 'url': 'https://github.com/openai/whisper'},
    'dspy': {'title': 'DSPy Official — Programmatic Prompt Optimization Documentation', 'url': 'https://dspy-docs.vercel.app/'}
}

def find_replacement(title, url):
    title_lower = title.lower()
    url_lower = url.lower()
    for key, repl in TOPIC_REPLACEMENTS.items():
        if key in title_lower or key in url_lower:
            return repl
    # Generic fallback based on channel or doc
    if 'arxiv' in url_lower or 'paper' in title_lower:
        return {'title': 'Krish Naik — AI/ML & Deep Learning Engineering Masterclass', 'url': 'https://www.youtube.com/@krishnaik06'}
    return None

print("=== 1. REPLACING PAPERS / ARXIV IN YAML DATA FILES ===")
total_yaml_replacements = 0

for yf in sorted(glob.glob('src/data/*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    
    file_modified = False
    for day in ydata.get('days', []):
        resources = day.get('resources', [])
        new_resources = []
        for r in resources:
            title = str(r.get('title', ''))
            url = str(r.get('url', ''))
            if 'arxiv' in url.lower() or 'arxiv' in title.lower() or 'paper' in title.lower():
                repl = find_replacement(title, url)
                if repl:
                    r['title'] = repl['title']
                    r['url'] = repl['url']
                    r['type'] = 'video' if 'youtube' in repl['url'] else 'docs'
                    total_yaml_replacements += 1
                    file_modified = True
            new_resources.append(r)
        day['resources'] = new_resources

    if file_modified:
        ydata = deep_literal(ydata)
        with open(yf, 'w', encoding='utf-8') as f:
            yaml.dump(ydata, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        print(f"✓ Updated YAML: {yf}")

print(f"Total YAML resource replacements: {total_yaml_replacements}")

print("\n=== 2. SYNCHRONIZING RESOURCE SECTIONS TO HTML PAGES ===")
for w in range(1, 27):
    hf = os.path.join(PAGES_DIR, f'week{w}.html')
    yf = os.path.join(DATA_DIR, f'week{w:02d}.yaml')
    if not os.path.exists(yf):
        yf = os.path.join(DATA_DIR, f'week{w}.yaml')
    if not os.path.exists(hf) or not os.path.exists(yf):
        continue

    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    for day in ydata.get('days', []):
        did = str(day.get('day_num') or day.get('id'))
        day_sec = soup.find('div', id=f'day-{did}')
        if not day_sec: continue

        res_sec = day_sec.find('div', class_='resources-section') or day_sec.find('div', id=f'resources-section-{did}')
        if res_sec:
            resources = day.get('resources', [])
            res_html = [f'<div class="resources-section" id="resources-section-{did}">', '<h2 class="sh2">📚 Resources &amp; Video Tutorials</h2>', '<div class="res-list">']
            for r in resources:
                r_title = html.escape(str(r.get('title', '')))
                r_url = html.escape(str(r.get('url', '')))
                r_type = r.get('type', 'docs')
                badge_lbl = '🎥 Video' if 'youtube' in r_url.lower() or r_type == 'video' else '📖 Docs'
                badge_cls = 'r-video' if 'youtube' in r_url.lower() or r_type == 'video' else 'r-docs'
                
                res_html.append(f'''<a class="res-item" href="{r_url}" rel="noopener" target="_blank">
<div class="r-icon">{badge_lbl}</div>
<div class="r-text">
<div class="r-title">{r_title}</div>
<div class="r-desc">{r_url}</div>
</div>
</a>''')
            res_html.append('</div></div>')
            new_res_soup = BeautifulSoup('\n'.join(res_html), 'html.parser')
            res_sec.replace_with(new_res_soup.div)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"✓ Updated HTML: {hf}")

print("\n🎉 ALL RESEARCH PAPER / ARXIV REFERENCES SUCCESSFULLY REPLACED WITH YOUTUBE TUTORIALS & OFFICIAL DOCS!")
