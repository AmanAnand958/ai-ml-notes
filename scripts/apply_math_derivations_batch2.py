#!/usr/bin/env python3
"""
apply_math_derivations_batch2.py
Replaces the remaining 36 EfficiencyScore boilerplate math blocks in Weeks 21-26
with authentic, domain-specific LaTeX derivations.
"""

import re
from bs4 import BeautifulSoup

WEEKS_DIR = "pages/weeks"

MATH_BATCH_2 = {

# ── WEEK 21 ──────────────────────────────────────────────────────────────────

(21, 'day-155'): r"""$$ \text{DataQuality} = w_1 \cdot \text{DeduplicationRatio} + w_2 \cdot \text{ToxicityScore}^{-1} + w_3 \cdot \text{TopicDiversity} $$
<p class="math-caption">Heuristic formula for LLM pre-training data quality weighting.</p>""",

(21, 'day-156'): r"""$$ W_{Q} = \text{dequantize}(W_{4bit}) + A B \quad \text{where } A \in \mathbb{R}^{d \times r}, B \in \mathbb{R}^{r \times k} $$
<p class="math-caption">QLoRA forward pass combining 4-bit base weights and low-rank adapters.</p>""",

# ── WEEK 22 ──────────────────────────────────────────────────────────────────

(22, 'day-157'): r"""$$ \text{RagasScore} = \frac{2 \cdot \text{Faithfulness} \cdot \text{AnswerRelevancy}}{\text{Faithfulness} + \text{AnswerRelevancy}} $$
<p class="math-caption">Harmonic mean of Ragas core metrics to evaluate RAG system quality.</p>""",

(22, 'day-158'): r"""$$ \text{TraceCost}_{USD} = \sum_{s \in \text{spans}} \left( \frac{\text{prompt\_tokens}_s}{10^6} \cdot C_{in} + \frac{\text{completion\_tokens}_s}{10^6} \cdot C_{out} \right) $$
<p class="math-caption">Calculating total request cost across all LLM spans within a single telemetry trace.</p>""",

(22, 'day-159'): r"""$$ P(\text{Safe} \mid X) = \prod_{k=1}^{K} \mathbb{I}(\text{Guardrail}_k(X) = \text{PASS}) $$
<p class="math-caption">Strict validation logic where a single guardrail failure rejects the generation.</p>""",

(22, 'day-160'): r"""$$ \text{Latency}_{TTFT} \approx \frac{\text{PromptTokens}}{\text{PrefillBandwidth}} + \text{NetworkLatency} $$
<p class="math-caption">Estimating Time To First Token (TTFT) as a function of prompt length and memory bandwidth.</p>""",

(22, 'day-161'): r"""$$ \text{LoadBalancing} \to \arg\min_m \left( \alpha \cdot \text{Latency}_m + \beta \cdot \text{Cost}_m + \gamma \cdot \text{QueueDepth}_m \right) $$
<p class="math-caption">Routing optimization function for LiteLLM load balancing across multiple API providers.</p>""",

(22, 'day-163'): r"""$$ \text{SystemScore} = \min(\text{Precision}_{target}, \text{Recall}_{target}) \cdot \mathbb{I}(\text{P99} < \text{SLA}) $$
<p class="math-caption">Production checkpoint acceptance criteria combining IR metrics with strict latency SLAs.</p>""",

# ── WEEK 23 ──────────────────────────────────────────────────────────────────

(23, 'day-164'): r"""$$ \text{TCO} = \text{ComputeHours} \times \text{InstanceRate} + \text{StorageGB} \times \text{StorageRate} + \text{DataEgress} $$
<p class="math-caption">Total Cost of Ownership (TCO) calculation for cloud-managed ML infrastructure.</p>""",

(23, 'day-165'): r"""$$ \text{AutoscalingPods} = \max\left(\text{MinReplicas}, \left\lceil \frac{\text{CurrentRPS}}{\text{TargetRPS\_per\_Pod}} \right\rceil \right) $$
<p class="math-caption">Target tracking autoscaling logic for Vertex AI model endpoints.</p>""",

(23, 'day-166'): r"""$$ \text{ColdStartPenalty} = \mathbb{I}(\text{ContainerInit}) \cdot \left( t_{\text{download}} + t_{\text{load\_weights}} \right) $$
<p class="math-caption">Latency penalty equation for serverless AWS Lambda inference cold starts.</p>""",

(23, 'day-167'): r"""$$ \text{RateLimitBuffer} = \max\left(0, \text{Tokens_{requested}} - \text{TPM_{limit}} \cdot \frac{\text{TimeWindow}}{60} \right) $$
<p class="math-caption">Token bucket algorithm estimation for Enterprise LLM rate limit planning.</p>""",

(23, 'day-168'): r"""$$ \text{GPUUtilization} = \frac{\int_{0}^{T} \text{ActiveSMs}(t) dt}{T \cdot \text{TotalSMs}} $$
<p class="math-caption">Streaming Multiprocessor (SM) utilization metric for FinOps cloud optimization.</p>""",

(23, 'day-169'): r"""$$ \text{CacheHitRatio} = \frac{\text{LocalReads}}{\text{LocalReads} + \text{APIRequests}} $$
<p class="math-caption">Efficiency metric for AWS Secrets Manager caching to minimize API latency and costs.</p>""",

(23, 'day-170'): r"""$$ \text{RAGLatency} = t_{embed} + t_{retrieve} + t_{rerank} + t_{LLM\_TTFT} + N \cdot t_{LLM\_decode} $$
<p class="math-caption">End-to-end latency breakdown for a Cloud RAG architecture returning N tokens.</p>""",

# ── WEEK 24 ──────────────────────────────────────────────────────────────────

(24, 'day-171'): r"""$$ \text{ReproducibilityScore} = \mathbb{I}(\text{Hash}_{train} == \text{Hash}_{orig}) \cdot \mathbb{I}(|M_{new} - M_{orig}| < \epsilon) $$
<p class="math-caption">Strict reproducibility definition requiring identical data hashes and model metrics within margin.</p>""",

(24, 'day-172'): r"""$$ \text{PromotionRisk} = \frac{\text{Errors}_{staging}}{\text{Requests}_{staging}} + \omega \cdot \max(0, \text{Latency}_{staging} - \text{SLA}) $$
<p class="math-caption">Risk assessment function before promoting models from Staging to Production in MLflow.</p>""",

(24, 'day-173'): r"""$$ \text{StorageSize} = \text{Size}_{base} + \sum_{v \in \text{versions}} \text{Size}_{\Delta v} $$
<p class="math-caption">DVC storage efficiency via content-addressable deduplication across dataset versions.</p>""",

(24, 'day-174'): r"""$$ P(\text{DAG\_Success}) = \prod_{i \in \text{CriticalPath}} P(\text{Task}_i = \text{Success}) $$
<p class="math-caption">Probability of successful ML pipeline execution based on independent Airflow task reliabilities.</p>""",

(24, 'day-175'): r"""$$ D_{KS} = \sup_x |F_{\text{reference}}(x) - F_{\text{current}}(x)| > \alpha $$
<p class="math-caption">Kolmogorov-Smirnov test statistic used by Evidently AI for numerical feature drift detection.</p>""",

(24, 'day-176'): r"""$$ \text{Traffic}_{green}(t) = \min\left(1.0, \frac{t - t_0}{\text{RolloutDuration}}\right) \cdot \mathbb{I}(\text{ErrorRate} < \tau) $$
<p class="math-caption">Progressive blue-green traffic shifting logic with automatic rollback on error threshold.</p>""",

(24, 'day-177'): r"""$$ \text{MLOpsMaturity} = \frac{\text{AutomatedSteps}}{\text{TotalPipelineSteps}} \times \mathbb{I}(\text{MonitoringEnabled}) $$
<p class="math-caption">Heuristic index for measuring Level 2 MLOps automation (DVC + Airflow + MLflow + Evidently).</p>""",

# ── WEEK 25 ──────────────────────────────────────────────────────────────────

(25, 'day-178'): r"""$$ \text{NodeCapacity} = \text{CPU}_{allocatable} - \sum \text{PodRequests}_{cpu} \ge \text{MinOverhead} $$
<p class="math-caption">Kubernetes node capacity constraint ensuring ML pods have sufficient guaranteed resources.</p>""",

(25, 'day-179'): r"""$$ \text{BatchEfficiency} = \frac{\text{TokensPerSecond}_{batched}}{\text{TokensPerSecond}_{sequential}} \propto \text{BatchSize} \cdot \left(1 - \text{MemoryOverhead}\right) $$
<p class="math-caption">Throughput improvement via continuous batching and PagedAttention in vLLM.</p>""",

(25, 'day-180'): r"""$$ \text{DesiredReplicas} = \left\lceil \text{CurrentReplicas} \cdot \frac{\text{CurrentMetricValue}}{\text{DesiredMetricValue}} \right\rceil $$
<p class="math-caption">Standard Kubernetes Horizontal Pod Autoscaler (HPA) algorithm for scaling ML services.</p>""",

(25, 'day-181'): r"""$$ \text{ReleaseStability} = 1 - \frac{\text{Rollbacks}}{\text{TotalHelmUpgrades}} $$
<p class="math-caption">Measurement of deployment stability using Helm atomic upgrades and rollbacks.</p>""",

(25, 'day-182'): r"""$$ t_{CICD} = t_{lint} + \max(t_{test}, t_{build}) + t_{deploy} $$
<p class="math-caption">Optimized CI/CD pipeline duration with parallelized testing and container building.</p>""",

(25, 'day-183'): r"""$$ \text{Degradation} = \max_{t} \left( M_{baseline} - M_{current}(t) \right) > \text{AlertThreshold} $$
<p class="math-caption">Silent quality degradation detection comparing trailing performance metrics against a golden baseline.</p>""",

(25, 'day-184'): r"""$$ \text{MTTR} = \frac{\sum \text{DowntimeDuration}}{\text{IncidentCount}} \downarrow \quad \text{via Automated Rollbacks} $$
<p class="math-caption">Mean Time To Recovery optimization through full CI/CD monitoring loops.</p>""",

# ── WEEK 26 ──────────────────────────────────────────────────────────────────

(26, 'day-185'): r"""$$ \text{MultimodalLoss} = \alpha \cdot \mathcal{L}_{text\_generation} + \beta \cdot \mathcal{L}_{image\_alignment} $$
<p class="math-caption">Objective function for aligning vision encoders with LLMs in LLaVA-style architectures.</p>""",

(26, 'day-186'): r"""$$ \text{Score}_{ColPali} = \sum_{i=1}^{|Q|} \max_{j \in |D|} \left( q_i \cdot d_j \right) $$
<p class="math-caption">MaxSim late-interaction scoring for multimodal document retrieval (ColPali).</p>""",

(26, 'day-187'): r"""$$ \text{WER} = \frac{\text{Substitutions} + \text{Deletions} + \text{Insertions}}{\text{TotalWordsInReference}} $$
<p class="math-caption">Word Error Rate calculation for evaluating Speech-to-Text pipeline accuracy.</p>""",

(26, 'day-188'): r"""$$ \mathcal{L}_{contrastive} = -\log \frac{\exp(\text{sim}(q, d^+)/\tau)}{\sum_{j=1}^{B} \exp(\text{sim}(q, d^-_j)/\tau)} $$
<p class="math-caption">InfoNCE loss function using in-batch negatives for training Two-Tower retrieval models.</p>""",

(26, 'day-189'): r"""$$ \text{DSPyOptimization} \to \arg\min_{\theta} \mathbb{E}_{(x,y) \sim D} \left[ \text{Metric}( \text{Program}_\theta(x), y ) \right] $$
<p class="math-caption">Objective for DSPy prompt/weight optimization replacing manual prompt engineering.</p>""",

(26, 'day-190'): r"""$$ \text{SearchComplexity}_{HNSW} \approx \mathcal{O}(\log(N) \cdot \text{efSearch} \cdot d) $$
<p class="math-caption">Time complexity estimation for approximate nearest neighbor search in HNSW vector databases.</p>""",

(26, 'day-191'): r"""$$ \text{CapstoneGrade} = \sum_{c \in \text{components}} w_c \cdot \text{QualityScore}(c) $$
<p class="math-caption">Final evaluation function aggregating evidence across all multimodal AI system components.</p>""",

}


def replace_math_in_section(html: str, day_id: str, new_math: str) -> tuple:
    day_start = html.find(f'id="{day_id}"')
    if day_start == -1:
        return html, False
    next_day = html.find('class="day-section"', day_start + 20)
    section = html[day_start:next_day] if next_day != -1 else html[day_start:]
    
    # Check if the EfficiencyScore block is present
    if 'EfficiencyScore' not in section and 'E = \sum' not in section:
        return html, False
        
    # The target block
    target_block_regex = r'<div class="math-block">\s*\$\$.*?\$\$\s*</div>'
    match = re.search(target_block_regex, section, re.DOTALL)
    if not match:
        return html, False
        
    new_block = f'<div class="math-block">\n{new_math}\n</div>'
    new_section = section[:match.start()] + new_block + section[match.end():]
    new_html = html[:day_start] + new_section + (html[next_day:] if next_day != -1 else '')
    return new_html, True


def main():
    print("=" * 65)
    print("MATH ENRICHMENT BATCH 2 — Weeks 21-26 (36 stubs)")
    print("=" * 65)
    
    total = 0
    for w in range(21, 27):
        path = f"{WEEKS_DIR}/week{w}.html"
        html = open(path, encoding='utf-8').read()
        original = html
        
        soup = BeautifulSoup(html, 'html.parser')
        days = [d.get('id', '') for d in soup.find_all('div', class_='day-section')]
        
        cnt = 0
        for day_id in days:
            key = (w, day_id)
            if key not in MATH_BATCH_2:
                continue
            html, changed = replace_math_in_section(html, day_id, MATH_BATCH_2[key])
            if changed:
                cnt += 1
                
        if html != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        total += cnt
        print(f"  Week {w}: {cnt} math blocks replaced")
        
    print(f"\nBatch 2 total: {total} replacements completed.")


if __name__ == '__main__':
    main()
