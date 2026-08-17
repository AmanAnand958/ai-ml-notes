#!/usr/bin/env python3
"""
scripts/fix_week25_26_task_prompts.py
Cleans corrupted HTML tags and updates task prompts in Weeks 25 & 26 with accurate, topic-specific descriptions.
"""

import os, yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f: return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

def save_yaml(path, data):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

# 1. Fix Week 25 Day 184 Tasks
w25_path = f"{DATA_DIR}/week25.yaml"
w25 = load_yaml(w25_path)
d184 = next(d for d in w25['days'] if d.get('id') == 184)
d184['tasks'][0]['prompt_html'] = '<p>Deploy a high-concurrency vLLM serving StatefulSet to a Kubernetes cluster using Helm. Configure GPU resource requests matching limits for Guaranteed QoS and mount an emptyDir shared memory volume at <code>/dev/shm</code>.</p>'
d184['tasks'][1]['solution_code'] = d184['tasks'][1]['solution_code'].replace('# Run after: kubectl apply -f k8s/\nimport subprocess', '# K8s LLM Deployment verification script\nimport subprocess')
save_yaml(w25_path, w25)
print("✓ Fixed Week 25 Day 184 tasks")

# 2. Fix Week 26 Tasks
w26_path = f"{DATA_DIR}/week26.yaml"
w26 = load_yaml(w26_path)

prompts_w26 = {
    185: '<p>Construct a Multimodal Projection Layer in PyTorch that maps 1024-dimensional ViT visual patch embeddings into 4096-dimensional LLM text token space. Calculate the total visual token sequence length for a 336x336 input image.</p>',
    186: '<p>Build a Multimodal RAG retrieval pipeline using ColPali / CLIP embeddings. Index document page screenshots directly in a vector store and evaluate visual-semantic query matching accuracy.</p>',
    187: '<p>Implement an audio preprocessing pipeline matching OpenAI Whisper specifications. Extract 80-channel log-Mel spectrogram features from a 16kHz audio waveform with 25ms window and 10ms hop length.</p>',
    188: '<p>Architect a scalable Two-Tower candidate retrieval model and neural ranker for an industrial recommendation system handling 10,000,000 candidate items under a 50ms latency SLA.</p>',
    189: '<p>Implement a DSPy teleprompter compilation workflow. Define a declarative Signature for multi-hop question answering and use BootstrapFewShot to optimize prompt demonstrations against a validation metric.</p>',
    190: '<p>Design a billion-scale distributed semantic search engine architecture. Implement HNSW index partitioning, scalar quantization (SQ8), and GPU-accelerated cross-encoder reranking.</p>',
    191: '<p>Execute comprehensive end-to-end integration and smoke tests across all capstone services: verify RAG endpoints, fine-tuned model inference, Kubernetes GPU metrics, and OpenTelemetry distributed traces.</p>'
}

for d in w26['days']:
    did = d.get('id')
    if did in prompts_w26:
        d['tasks'][0]['prompt_html'] = prompts_w26[did]
        print(f"  ✓ Cleaned prompt for Day {did} ('{d.get('title')[:30]}')")

save_yaml(w26_path, w26)
print("✓ Saved week26.yaml with clean task prompts!")
