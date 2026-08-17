#!/usr/bin/env python3
import yaml

SPECIFIC_FCS = {
    '47': {'front': 'Random Forest Feature Subsampling (m = sqrt(p))?', 'back': 'Decorrelates individual trees by forcing each split to choose from a random subset of sqrt(p) features, reducing ensemble variance.'},
    '111': {'front': 'MCP (Model Context Protocol) Architecture?', 'back': 'Standardized JSON-RPC protocol allowing LLM clients to securely discover tools, read context resources, and invoke prompts from isolated servers.'},
    '147': {'front': 'Agent Memory: Coreference Resolution?', 'back': 'Resolves pronouns ("he", "it", "that document") to concrete entities before generating embedding vectors for memory storage.'},
    '150': {'front': 'PagedAttention Virtual Memory Mapping?', 'back': 'Allocates KV cache memory dynamically in fixed-size contiguous blocks, slashing GPU memory fragmentation from 70% to <4%.'},
    '152': {'front': 'AWQ vs GPTQ Quantization?', 'back': 'AWQ protects salient 1% activation weights while quantizing the rest; GPTQ uses second-order Hessian information to optimize weight rounding.'},
    '153': {'front': 'QLoRA NormalFloat4 (NF4) Quantization?', 'back': 'Information-theoretically optimal quantile quantization for normally distributed weights, with double quantization to reduce memory footprint.'},
    '154': {'front': 'DPO (Direct Preference Optimization) Formulation?', 'back': 'Directly optimizes policy LLM on preference pairs without training a separate reward model.'},
    '184': {'front': 'Kubernetes LLM Horizontal Pod Autoscaling with KEDA?', 'back': 'Scales inference pod replicas based on real-time metrics (vLLM pending request queue length and GPU duty cycle) rather than raw CPU usage.'},
    '185': {'front': 'Vision-Language Model Cross-Attention Projector?', 'back': 'Projects visual tokens from a Vision Transformer (ViT) into the text LLM input embedding space via a 2-layer MLP or Q-Former.'},
    '186': {'front': 'ColPali Multimodal Document Retrieval?', 'back': 'Embeds whole PDF pages as patch tokens using PaliGemma and computes late-interaction MaxSim scores directly without relying on error-prone OCR pipelines.'}
}

files = ['src/data/week07.yaml', 'src/data/week16.yaml', 'src/data/week20.yaml', 'src/data/week21.yaml', 'src/data/week25.yaml', 'src/data/week26.yaml']

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)
    for d in data.get('days', []):
        did = str(d.get('id', ''))
        if did in SPECIFIC_FCS:
            clean_fcs = []
            for fc in d.get('flashcards', []):
                front = str(fc.get('front', ''))
                if any(k in front for k in ['Core Objective of', 'Key principle of', 'Common failure mode in']):
                    clean_fcs.append(SPECIFIC_FCS[did])
                else:
                    clean_fcs.append(fc)
            if not clean_fcs:
                clean_fcs.append(SPECIFIC_FCS[did])
            d['flashcards'] = clean_fcs
    with open(fpath, 'w', encoding='utf-8') as fp:
        yaml.dump(data, fp, allow_unicode=True, sort_keys=False)

print('✅ Upgraded all target flashcards with deep technical concepts!')
