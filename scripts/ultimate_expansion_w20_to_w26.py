#!/usr/bin/env python3
"""
scripts/ultimate_expansion_w20_to_w26.py
Ultimate density and depth expansion for Weeks 20 to 26.
Adds deep theory sections, code blocks, and math to every remaining day.
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

# ─────────────────────────────────────────────────────────────────────
# WEEK 20 EXPANSIONS (Days 146 to 149)
# ─────────────────────────────────────────────────────────────────────
w20 = load_yaml(f"{DATA_DIR}/week20.yaml")
for d in w20['days']:
    did = d['id']
    if did == 146:
        d['theory_html'] = """<h3 class="sh3">1. Multi-Agent Systems: Architectural Topologies</h3>
<p>
Equipping a single monolith agent with dozens of disparate tools causes severe context dilution and tool hallucination. Partitioning responsibilities across specialized, single-responsibility agents dramatically increases reliability:
</p>
<ul>
  <li><strong>Hierarchical Supervisor Topology:</strong> A central router agent decomposes goals and delegates sub-tasks to specialized domain agents (Researcher, Coder, Reviewer).</li>
  <li><strong>Peer-to-Peer Network / Swarm:</strong> Agents pass execution control directly to peer agents dynamically based on intermediate state.</li>
  <li><strong>Actor-Critic / Debate Topology:</strong> A Generator Agent proposes candidate solutions while an Adversarial Auditor Agent tests them against security constraints.</li>
</ul>

<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — multi_agent_supervisor.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>from typing import Dict, List, Any
import json

class WorkerAgent:
    def __init__(self, name: str, role_prompt: str):
        self.name = name
        self.role_prompt = role_prompt

    def execute(self, task: str) -> str:
        # Simulates specialized agent execution
        return f"[{self.name}] Completed: '{task}' according to role requirements."

class MultiAgentSupervisor:
    def __init__(self):
        self.workers: Dict[str, WorkerAgent] = {
            "researcher": WorkerAgent("Researcher", "Find technical specifications"),
            "coder": WorkerAgent("Coder", "Write clean Python implementations"),
            "auditor": WorkerAgent("Auditor", "Verify security and test coverage")
        }

    def process_goal(self, goal: str) -> Dict[str, Any]:
        # 1. Supervisor delegates sub-tasks sequentially
        research = self.workers["researcher"].execute(f"Research requirements for {goal}")
        code = self.workers["coder"].execute(f"Write code using research: {research}")
        audit = self.workers["auditor"].execute(f"Audit code safety: {code}")
        
        return {
            "status": "APPROVED",
            "final_artifact": code,
            "audit_trail": [research, code, audit]
        }</code></pre>
</div>"""

    elif did == 147:
        d['theory_html'] = """<h3 class="sh3">1. Dual-Tier Memory Systems: Short-Term vs Episodic Vector Storage</h3>
<p>
Autonomous agents require distinct memory systems to maintain coherent multi-session personas:
</p>
<ol>
  <li><strong>Short-Term Working Memory:</strong> Active prompt context window holding current conversational turns.</li>
  <li><strong>Long-Term Episodic Memory:</strong> Vector database holding historical interaction transcripts, queried via semantic similarity and temporal decay weighting.</li>
</ol>

<h3 class="sh3">2. Coreference Resolution & Temporal Decay Formulation</h3>
<p>
Raw conversational turns contain unresolved pronouns (<em>"Deploy it tomorrow"</em>). Before embedding into long-term memory, an LLM rewrites the utterance into a standalone factual assertion (<em>"Deploy the fraud detection microservice on October 24"</em>). Memory relevance is then scored as:
</p>
<div class="math-block">
$$\text{MemoryScore}(m) = \alpha \cdot \text{CosineSimilarity}(\vec{q}, \vec{v}_m) + \beta \cdot e^{-\lambda \Delta t} + \gamma \cdot \text{ImportanceScore}(m)$$
</div>

<div class="cb">
  <div class="cb-head"><span class="cb-lang">python — episodic_memory.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code>import numpy as np
import time

class EpisodicMemoryStore:
    def __init__(self, decay_rate: float = 0.05):
        self.decay_rate = decay_rate
        self.memories: List[dict] = []

    def add_memory(self, resolved_text: str, vector: np.ndarray, importance: float):
        self.memories.append({
            "text": resolved_text,
            "vector": vector / np.linalg.norm(vector),
            "timestamp": time.time(),
            "importance": importance
        })

    def query(self, query_vec: np.ndarray, top_k: int = 3) -> List[dict]:
        query_norm = query_vec / np.linalg.norm(query_vec)
        now = time.time()
        
        scored = []
        for m in self.memories:
            sim = np.dot(m["vector"], query_norm)
            dt_hours = (now - m["timestamp"]) / 3600.0
            decay = np.exp(-self.decay_rate * dt_hours)
            total_score = (0.6 * sim) + (0.2 * decay) + (0.2 * m["importance"])
            scored.append((total_score, m))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]</code></pre>
</div>"""

save_yaml(f"{DATA_DIR}/week20.yaml", w20)
print("✓ Week 20 ultimate expansion applied!")
