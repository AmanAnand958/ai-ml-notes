#!/usr/bin/env python3
import yaml

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

# Fix Day 162 predict block in week22.yaml
with open('src/data/week22.yaml', 'r') as f:
    y22 = yaml.safe_load(f)

for d in y22['days']:
    if int(d.get('day_num') or d.get('id')) == 162:
        d['predict'] = {
            'question': 'If a 7B parameter model (with GQA, 8 KV heads) is quantized to 4-bit with 2048-token context and batch size 4, how much total VRAM is required?',
            'answer': 'Total 7B 4-bit VRAM: 4.98 GB (Fits comfortably in an 8GB/16GB GPU)',
            'explanation': '4-bit weights take ~3.26 GB (7B * 0.5 bytes). With Grouped Query Attention (GQA, 8 KV heads), the KV cache takes ~1.07 GB for batch 4 at 2k context. Adding ~0.65 GB for CUDA overhead yields ~4.98 GB total VRAM.',
            'code': '''# Sizing Calculator for 7B 4-bit Quantized Model (with GQA)
def calculate_7b_quantized_vram(params_billion: float = 7.0, bit_precision: int = 4, context_len: int = 2048, batch_size: int = 4, num_kv_heads: int = 8) -> float:
    # 1. Weights in GB
    weights_gb = (params_billion * 10**9 * (bit_precision / 8.0)) / (1024**3)
    # 2. KV Cache (32 layers, 8 kv_heads, 128 head_dim, 2 bytes/element)
    kv_cache_bytes = 2 * 32 * num_kv_heads * 128 * 2.0 * context_len * batch_size
    kv_cache_gb = kv_cache_bytes / (1024**3)
    # 3. CUDA & Runtime Overhead (~15%)
    overhead_gb = (weights_gb + kv_cache_gb) * 0.15
    total_vram = weights_gb + kv_cache_gb + overhead_gb
    print(f"Total 7B 4-bit VRAM: {total_vram:.2f} GB (Weights: {weights_gb:.2f} GB, KV Cache: {kv_cache_gb:.2f} GB)")
    return total_vram

if __name__ == "__main__":
    vram = calculate_7b_quantized_vram()
    assert 4.0 <= vram <= 5.5
'''
        }

with open('src/data/week22.yaml', 'w') as f:
    yaml.dump(deep_literal(y22), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

# Fix Day 175 predict block in week24.yaml
with open('src/data/week24.yaml', 'r') as f:
    y24 = yaml.safe_load(f)

for d in y24['days']:
    if int(d.get('day_num') or d.get('id')) == 175:
        pcode = d['predict']['code']
        if 'import numpy as np' not in pcode:
            d['predict']['code'] = 'import numpy as np\n' + pcode

with open('src/data/week24.yaml', 'w') as f:
    yaml.dump(deep_literal(y24), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

print("✓ Successfully patched predict blocks for Days 162 and 175")
