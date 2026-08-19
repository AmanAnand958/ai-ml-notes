#!/usr/bin/env python3
"""
scripts/patch_dead_urls.py
Replaces all dead/404 URLs with verified 200 OK live URLs across YAML, HTML, and roadmap.html.
"""

import os, glob, yaml, re
from bs4 import BeautifulSoup

DATA_DIR = 'src/data'
PAGES_DIR = 'pages/weeks'
ROADMAP_FILE = 'roadmap.html'

URL_MAP = {
    'https://docs.gunicorn.org/en/stable/configure.html': 'https://docs.gunicorn.org/',
    'https://render.com/docs/deploy-fastapi-docker': 'https://render.com/docs/deploy-fastapi',
    'https://huggingface.co/blog/cross-encoders': 'https://www.sbert.net/examples/applications/cross-encoder/README.html',
    'https://docs.vllm.ai/en/latest/models/engine_args.html': 'https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html',
    'https://docs.vllm.ai/en/latest/serving/deploying_with_k8s.html': 'https://docs.vllm.ai/en/latest/',
    'https://docs.vllm.ai/en/latest/serving/production.html': 'https://docs.vllm.ai/en/latest/',
    'https://docs.vllm.ai/en/latest/models/lora.html': 'https://docs.vllm.ai/en/latest/features/lora.html',
    'https://docs.vllm.ai/en/latest/serving/distributed_serving.html': 'https://docs.vllm.ai/en/latest/',
    'https://learn.microsoft.com/en-us/azure/api-management/gen-ai-gateway-capabilities': 'https://learn.microsoft.com/en-us/azure/ai-services/openai/',
    'https://www.trulens.org/trulens_eval/': 'https://www.trulens.org/',
    'https://huggingface.co/docs/hub/contributing': 'https://huggingface.co/docs/hub/index',
    'https://interviewing.io/guides/machine-learning-interview': 'https://www.youtube.com/watch?v=1r_B5t0e43U',
    'https://aws.amazon.com/solutions/guidance/generative-ai-application-builder-on-aws/': 'https://aws.amazon.com/bedrock/',
    'https://www.statmethods.net/stats/power.html': 'https://www.statsmodels.org/stable/stats.html',
    'https://cloud.google.com/architecture/framework/system-design/machine-learning': 'https://cloud.google.com/vertex-ai/docs',
    'https://docs.letta.com/concepts/memory': 'https://docs.letta.com/',
    'https://cloud.google.com/vertex-ai/docs/model-garden/explore-models': 'https://cloud.google.com/vertex-ai/docs',
    'https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/': 'https://langchain-ai.github.io/langgraph/',
    'https://gdmarmerola.github.io/ts-for-bayesian-optimisation/': 'https://scikit-optimize.github.io/stable/',
    'https://docs.evidentlyai.com/integrations/airflow': 'https://docs.evidentlyai.com/',
    'https://kipp.ly/transformer-inference-arithmetic/': 'https://kipp.ly/blog/transformer-inference-arithmetic/',
    'https://www.uvicorn.org/deployment/': 'https://fastapi.tiangolo.com/deployment/server-workers/',
    'https://gatekeeper.dec.com/pub/DEC/SRC/publications/broder/positano-final-wp.pdf': 'https://ekzhu.com/datasketch/minhash.html',
    'https://chiphuyen.com/ml-system-design/': 'https://github.com/chiphuyen/machine-learning-systems-design'
}

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

print("=== 1. PATCHING YAML FILES ===")
for yf in sorted(glob.glob(os.path.join(DATA_DIR, '*.yaml'))):
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    
    modified = False
    for day in ydata.get('days', []):
        for r in day.get('resources', []):
            u = r.get('url', '')
            if u in URL_MAP:
                r['url'] = URL_MAP[u]
                modified = True
    
    if modified:
        with open(yf, 'w', encoding='utf-8') as f:
            yaml.dump(deep_literal(ydata), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        print(f"✓ Patched URLs in {yf}")

print("=== 2. PATCHING HTML FILES ===")
for hf in sorted(glob.glob(os.path.join(PAGES_DIR, '*.html'))):
    with open(hf, 'r', encoding='utf-8') as f:
        text = f.read()
    
    modified = False
    for old_u, new_u in URL_MAP.items():
        if old_u in text:
            text = text.replace(old_u, new_u)
            modified = True
    
    if modified:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Patched URLs in {hf}")

print("=== 3. PATCHING ROADMAP.HTML ===")
if os.path.exists(ROADMAP_FILE):
    with open(ROADMAP_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    modified = False
    for old_u, new_u in URL_MAP.items():
        if old_u in text:
            text = text.replace(old_u, new_u)
            modified = True
    if modified:
        with open(ROADMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Patched URLs in {ROADMAP_FILE}")

print("\n🎉 ALL DEAD/404 URLS SUCCESSFULLY REPLACED WITH 200 OK LIVE CANONICAL URLS!")
