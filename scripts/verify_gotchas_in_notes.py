#!/usr/bin/env python3
"""
Cross-check each production gotcha from the Master Gotcha Checklist against
the actual HTML files to verify they are correctly represented.

Gotchas to verify (mapped to week/day):
- Week 20, Day 150: vLLM GPU utilization cap 0.90 
- Week 20, Day 150: vLLM PagedAttention block size >= 16
- Week 25, Day 183: KServe /dev/shm mount
- Week 20, Day 151: Speculative Decoding vocabulary mismatch
- Week 20, Day 152: INT4 quantization without AWQ/GPTQ perplexity spike
- Week 19, Day 136: BM25 + Dense normalization / RRF
- Week 19, Day 137: Cross-Encoder candidate limit 50-100
- Week 26, Day 186: Multimodal video token overflow 15k tokens
- Vector DB RAM 1B vectors / Product Quantization
- Week 19, Day 140: GraphRAG token drain
- Week 20, Day 143: ReAct max_iterations limit
- Week 20, Day 146: Multi-agent consensus exit criteria
- Week 20, Day 147: Vector memory recency decay
- Week 20, Day 147: Coreference resolution / History-Aware Retriever
- Week 20, Day 148: HITL interrupt_before for destructive tools
- Week 25, Day 178: K8s resource requests+limits
- Week 25, Day 179: GPU node affinity and tolerations
- Week 23, Day 166: API Gateway 29-second timeout
- Week 24, Day 171: MLflow SQLite lock contention -> PostgreSQL
- Week 23, Day 169: Docker secret leakage ENV variable
- Week 22, Day 157: LLM-as-a-Judge position bias
- Week 22, Day 158: p50 vs p99 latency
- Week 26, Day 187: Whisper VAD before transcription
- Week 23, Day 168: Runaway agent token drain / circuit breaker
- Week 23, Day 165: Vertex AI min_replica_count >= 1
- Week 22, Day 162: Flaky CI/CD eval against live LLM APIs
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

def get_day_text(week_num, day_num):
    fp = WEEKS_DIR / f"week{week_num}.html"
    if not fp.exists():
        return ""
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    day = soup.find('div', id=f'day-{day_num}')
    return day.get_text() if day else ""

CHECKS = [
    ("W21/D150 vLLM GPU util cap 0.90",     21, 150, ["0.90", "gpu-memory-utilization", "OOM"]),
    ("W21/D150 vLLM block size >= 16",       21, 150, ["block", "PagedAttention", "16"]),
    ("W25/D183 KServe /dev/shm mount",       25, 183, ["/dev/shm", "KServe", "shared memory"]),
    ("W21/D151 Spec Decode vocab mismatch",  21, 151, ["Speculative", "vocabulary", "tokenizer"]),
    ("W21/D152 INT4 AWQ/GPTQ outlier",       21, 152, ["AWQ", "GPTQ", "outlier", "perplexity"]),
    ("W19/D136 BM25 norm + RRF",             19, 136, ["RRF", "normalize", "BM25"]),
    ("W19/D137 Cross-Encoder 50-100 cap",    19, 137, ["50", "100", "Cross-Encoder", "latency"]),
    ("W26/D186 Multimodal video token OOM",  26, 186, ["15,000", "video", "token", "OOM"]),
    ("W19/D140 GraphRAG token drain",        19, 140, ["GraphRAG", "token", "noisy"]),
    ("W20/D143 ReAct max_iterations",        20, 143, ["max_iterations", "infinite", "loop"]),
    ("W20/D146 Multi-agent consensus exit",  20, 146, ["consensus", "exit", "80%"]),
    ("W20/D147 Vector memory recency decay", 20, 147, ["recency", "decay", "stale"]),
    ("W20/D147 Coreference resolution",      20, 147, ["coreference", "History-Aware", "rewrite"]),
    ("W20/D148 HITL interrupt_before",       20, 148, ["interrupt_before", "HITL", "destructive"]),
    ("W25/D178 K8s requests + limits",       25, 178, ["requests", "limits", "OOMKilled"]),
    ("W25/D179 GPU node affinity/tolerations",25,179, ["affinity", "toleration", "GPU"]),
    ("W23/D166 API GW 29-second timeout",    23, 166, ["29", "timeout", "WebSocket"]),
    ("W24/D171 MLflow SQLite -> PostgreSQL", 24, 171, ["SQLite", "PostgreSQL", "lock"]),
    ("W23/D169 Docker ENV secret leakage",   23, 169, ["ENV", "secret", "layer"]),
    ("W22/D157 LLM-Judge position bias",     22, 157, ["position", "bias", "swap"]),
    ("W22/D158 p50 vs p99 latency",          22, 158, ["p99", "p50", "tail"]),
    ("W26/D187 Whisper VAD",                 26, 187, ["VAD", "Voice Activity", "silent"]),
    ("W23/D168 Runaway agent circuit breaker",23,168, ["circuit", "budget", "runaway"]),
    ("W23/D165 Vertex AI min_replica >= 1",  23, 165, ["min_replica", "cold start", "scale"]),
    ("W22/D162 Flaky CI/CD live LLM eval",   22, 162, ["flaky", "snapshot", "live"]),
]

print(f"{'Gotcha Check':<45} {'Status':<12} {'Missing Keywords'}")
print("-" * 90)

confirmed = 0
missing = 0
partial = 0

for check_name, wn, dn, keywords in CHECKS:
    text = get_day_text(wn, dn).lower()
    found = [kw for kw in keywords if kw.lower() in text]
    not_found = [kw for kw in keywords if kw.lower() not in text]
    
    if len(found) == len(keywords):
        status = "✅ PASS"
        confirmed += 1
    elif len(found) >= len(keywords) // 2:
        status = "⚠️  PARTIAL"
        partial += 1
    else:
        status = "❌ FAIL"
        missing += 1
    
    missing_str = ", ".join(not_found) if not_found else ""
    print(f"{check_name:<45} {status:<12} {missing_str}")

print("-" * 90)
print(f"\nSummary: ✅ {confirmed} PASS | ⚠️  {partial} PARTIAL | ❌ {missing} FAIL out of {len(CHECKS)} checks")
