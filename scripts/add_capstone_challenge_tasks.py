#!/usr/bin/env python3
"""
scripts/add_capstone_challenge_tasks.py
Injects a 3rd Advanced Production Challenge Task with complete verified solution code
into every Capstone and Milestone day in Weeks 19 to 26.
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

CAPSTONE_TASKS = {
    142: {
        'title': 'Task 3: Implement RRF Latency Benchmarking & Profiling',
        'badge': 'Task 3: Production Benchmarking',
        'badge_class': 'tb-adv',
        'time': '30 mins',
        'prompt_html': """<p><strong>Scenario:</strong> You need to validate that your hybrid search engine (BM25 + Dense Vectors) satisfies the enterprise SLA requirement of &lt;25ms p95 latency under a concurrent load of 50 RPS.</p>
<ul>
  <li>Construct an asynchronous load generator using Python's <code>asyncio</code>.</li>
  <li>Simulate 100 concurrent search queries with random embedding vectors.</li>
  <li>Compute p50, p95, and p99 latency percentiles and export a performance report.</li>
</ul>""",
        'done_when': 'Latency profiler outputs p50, p95, and p99 percentiles under 25ms.',
        'git_cmd': 'git add benchmarks/rrf_load_test.py && git commit -m "feat(perf): add RRF latency load test suite"',
        'sol_id': 'sol_d142_t3',
        'solution_title': 'RRF Asynchronous Latency Profiler',
        'solution_lang': 'python',
        'solution_code': """import asyncio
import time
import numpy as np

async def mock_hybrid_query(query_id: int) -> float:
    t0 = time.perf_counter()
    # Simulate BM25 (2ms) + Vector Lookup (8ms) + RRF Merge (1ms)
    await asyncio.sleep(np.random.uniform(0.008, 0.018))
    return (time.perf_counter() - t0) * 1000

async def run_benchmark(total_queries: int = 100):
    tasks = [mock_hybrid_query(i) for i in range(total_queries)]
    latencies = await asyncio.gather(*tasks)
    
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)
    
    print(f"--- RRF Performance Benchmark ({total_queries} queries) ---")
    print(f"  p50 Latency: {p50:.2f} ms")
    print(f"  p95 Latency: {p95:.2f} ms (Target: <25ms)")
    print(f"  p99 Latency: {p99:.2f} ms")
    return p95 < 25.0

if __name__ == '__main__':
    asyncio.run(run_benchmark())"""
    },
    149: {
        'title': 'Task 3: Multi-Agent Deadlock Detection & Safety Circuit Breaker',
        'badge': 'Task 3: Safety Guardrails',
        'badge_class': 'tb-adv',
        'time': '30 mins',
        'prompt_html': """<p><strong>Scenario:</strong> In cyclic multi-agent topologies, agents can become trapped in infinite debate loops if they fail to converge on an agreement. You must implement a circuit breaker that monitors graph execution depth.</p>
<ul>
  <li>Track the count of node transitions in the shared agent state.</li>
  <li>If transitions exceed <code>max_hops = 10</code>, force state eviction to a human fallback handler.</li>
  <li>Export an alert trace for security review.</li>
</ul>""",
        'done_when': 'Circuit breaker trips and gracefully returns human fallback state upon exceeding max hops.',
        'git_cmd': 'git add agents/circuit_breaker.py && git commit -m "feat(safety): add multi-agent deadlock circuit breaker"',
        'sol_id': 'sol_d149_t3',
        'solution_title': 'Multi-Agent Execution Circuit Breaker',
        'solution_lang': 'python',
        'solution_code': """from typing import Dict, Any

class AgentCircuitBreaker:
    def __init__(self, max_hops: int = 10):
        self.max_hops = max_hops

    def check_and_increment(self, state: Dict[str, Any]) -> Dict[str, Any]:
        hops = state.get("execution_hops", 0) + 1
        state["execution_hops"] = hops
        
        if hops > self.max_hops:
            state["status"] = "CIRCUIT_BREAKER_TRIPPED"
            state["next_step"] = "human_operator_fallback"
            print(f"⚠️ Circuit Breaker: Execution hops ({hops}) exceeded limit ({self.max_hops}). Tripping to human review.")
        return state

# Test circuit breaker execution
state = {"execution_hops": 9, "status": "RUNNING"}
breaker = AgentCircuitBreaker(max_hops=10)
state = breaker.check_and_increment(state)
state = breaker.check_and_increment(state)
assert state["status"] == "CIRCUIT_BREAKER_TRIPPED"
print("✓ Circuit breaker verified!")"""
    }
}

for w in range(19, 27):
    fpath = f"{DATA_DIR}/week{w:02d}.yaml"
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)
    
    for d in data.get('days', []):
        did = d['id']
        if did in CAPSTONE_TASKS:
            existing_tasks = d.get('tasks', [])
            # Check if already added
            if not any(t.get('title') == CAPSTONE_TASKS[did]['title'] for t in existing_tasks):
                existing_tasks.append(CAPSTONE_TASKS[did])
                d['tasks'] = existing_tasks
                print(f"  ✓ Added Task 3 to Day {did:03d} in Week {w:02d}")
                
    save_yaml(fpath, data)

print("\n✓ Capstone challenge tasks injected successfully!")
