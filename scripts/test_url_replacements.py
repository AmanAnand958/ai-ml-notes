#!/usr/bin/env python3
import urllib.request, urllib.error

REPLACEMENTS = {
    'https://docs.gunicorn.org/en/stable/configure.html': 'https://docs.gunicorn.org/en/stable/settings.html',
    'https://render.com/docs/deploy-fastapi-docker': 'https://render.com/docs/deploy-fastapi',
    'https://huggingface.co/blog/cross-encoders': 'https://www.sbert.net/examples/applications/cross-encoder/README.html',
    'https://docs.vllm.ai/en/latest/models/engine_args.html': 'https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html',
    'https://docs.vllm.ai/en/latest/serving/deploying_with_k8s.html': 'https://docs.vllm.ai/en/latest/',
    'https://docs.vllm.ai/en/latest/serving/production.html': 'https://docs.vllm.ai/en/latest/',
    'https://docs.vllm.ai/en/latest/models/lora.html': 'https://docs.vllm.ai/en/latest/features/lora.html',
    'https://docs.vllm.ai/en/latest/serving/distributed_serving.html': 'https://docs.vllm.ai/en/latest/features/distributed_serving.html',
    'https://learn.microsoft.com/en-us/azure/api-management/gen-ai-gateway-capabilities': 'https://learn.microsoft.com/en-us/azure/ai-services/openai/',
    'https://www.trulens.org/trulens_eval/': 'https://www.trulens.org/',
    'https://huggingface.co/docs/hub/contributing': 'https://huggingface.co/docs/hub/index',
    'https://interviewing.io/guides/machine-learning-interview': 'https://www.youtube.com/watch?v=1r_B5t0e43U',
    'https://aws.amazon.com/solutions/guidance/generative-ai-application-builder-on-aws/': 'https://aws.amazon.com/bedrock/',
    'https://www.statmethods.net/stats/power.html': 'https://www.statsmodels.org/stable/stats.html',
    'https://cloud.google.com/architecture/framework/system-design/machine-learning': 'https://cloud.google.com/vertex-ai/docs',
    'https://docs.letta.com/concepts/memory': 'https://docs.letta.com/',
    'https://cloud.google.com/vertex-ai/docs/model-garden/explore-models': 'https://cloud.google.com/vertex-ai/docs/model-garden/overview',
    'https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/': 'https://langchain-ai.github.io/langgraph/',
    'https://gdmarmerola.github.io/ts-for-bayesian-optimisation/': 'https://scikit-optimize.github.io/stable/',
    'https://docs.evidentlyai.com/integrations/airflow': 'https://docs.evidentlyai.com/',
    'https://kipp.ly/transformer-inference-arithmetic/': 'https://kipply.dev/transformer-inference-arithmetic/',
    'https://www.uvicorn.org/deployment/': 'https://www.uvicorn.org/',
    'https://gatekeeper.dec.com/pub/DEC/SRC/publications/broder/positano-final-wp.pdf': 'https://ekzhu.com/datasketch/minhash.html',
    'https://chiphuyen.com/ml-system-design/': 'https://github.com/chiphuyen/machine-learning-systems-design'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

print("=== TESTING REPLACEMENT URLS ===")
for old_url, new_url in REPLACEMENTS.items():
    req = urllib.request.Request(new_url, headers=HEADERS, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            print(f"✅ {resp.status} : {new_url}")
    except Exception as e:
        print(f"❌ {new_url} : {e}")

