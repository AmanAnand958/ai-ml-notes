"""
Theoretical content definitions for:
- Week 20: LLM Agents & Workflows (Days 143 - 149)
- Week 21: LLM Fine-Tuning & Inference (Days 150 - 156)
"""

THEORY_WEEKS_20_21 = {
    # ═════════════════════════════════════════════════════════════════════
    # WEEK 20: LLM AGENTS & WORKFLOWS (Days 143 - 149)
    # ═════════════════════════════════════════════════════════════════════
    143: """<h3 class="sh3">1. The ReAct (Reasoning + Acting) Paradigm</h3>
<p>
Standard Chain-of-Thought (CoT) prompting is purely internal and cannot interact with the external world. <strong>ReAct</strong> synergizes verbal reasoning with interactive tool execution in a structured loop:
</p>
<div class="mermaid">
graph TD
  Goal["User Goal / Task"] --> Thought["1. Thought:\nReason about current state"]
  Thought --> Action["2. Action:\nSelect Tool + Generate Arguments"]
  Action --> Exec["3. External Environment Execution\n(Python REPL / SQL / Web API)"]
  Exec --> Obs["4. Observation:\nCapture Raw Tool Output"]
  Eval{"Goal Achieved?"}
  Obs --> Eval
  Eval -->|No| Thought
  Eval -->|Yes| Finish["Final Answer to User"]
</div>
<div class="diagram-cap">The ReAct Loop: Cyclical execution between internal reasoning and external environment observations.</div>

<h3 class="sh3">2. Plan-and-Solve vs. Reactive Execution</h3>
<p>
While ReAct decides each step greedily one at a time, <strong>Plan-and-Solve</strong> prompting first creates a multi-step macro decomposition plan, then systematically executes each sub-task. This prevents reasoning drift on complex 10+ step workflows.
</p>""",

    144: """<h3 class="sh3">1. Structured Output Generation with Instructor & Pydantic</h3>
<p>
LLMs output unstructured text by default. In production workflows, downstream services require strictly typed JSON objects conforming to schemas. Libraries like <strong>Instructor</strong> and OpenAI/Anthropic Structured Outputs enforce schema compliance via constrained decoding and auto-retry validation loops.
</p>
<div class="mermaid">
graph LR
  Prompt["User Prompt + Pydantic Schema"] --> LLM["LLM (JSON Schema Constrained Mode)"]
  LLM --> Raw["Raw JSON Output"]
  Raw --> Validate{"Pydantic Validation"}
  Validate -->|Valid| App["Typed Python Object Instance"]
  Validate -->|ValidationError| Feedback["Auto-Retry with Error Feedback"]
  Feedback --> LLM
</div>
<div class="diagram-cap">Constrained JSON Decoding and Automatic Schema-Healing Validation Loop.</div>

<h3 class="sh3">2. Pydantic Schema Declaration for Tool Calling</h3>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — structured_schemas.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
<pre><code>from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedEntity(BaseModel):
    name: str = Field(description="Full name of person or company")
    category: str = Field(description="Entity category: ORG, PERSON, LOCATION")
    confidence: float = Field(ge=0.0, le=1.0, description="Extraction confidence")

class DocumentSummary(BaseModel):
    title: str
    key_points: List[str] = Field(min_items=3, max_items=5)
    entities: List[ExtractedEntity]
    sentiment: str = Field(regex="^(positive|neutral|negative)$")</code></pre>
</div>""",

    145: """<h3 class="sh3">1. LangGraph StateGraph Architecture</h3>
<p>
Unlike linear DAG runners, <strong>LangGraph</strong> supports cyclical graphs essential for iterative agent self-correction, reflection, and human-in-the-loop validation:
</p>
<div class="mermaid">
graph TD
  Start["START"] --> AgentNode["Agent Decision Node"]
  AgentNode --> ToolCondition{"Tools Needed?"}
  ToolCondition -->|Yes| ToolNode["Tool Execution Node"]
  ToolNode --> AgentNode
  ToolCondition -->|No| GradeNode["Quality Grader Node"]
  GradeNode -->|Satisfactory| EndNode["END"]
  GradeNode -->|Unsatisfactory| AgentNode
</div>
<div class="diagram-cap">LangGraph Cyclical State Execution Flow with Dual Feedback Decision Edges.</div>

<h3 class="sh3">2. TypedDict State Reducers</h3>
<p>
In LangGraph, all graph nodes receive and return partial updates to a shared state dictionary. State reducers merge updates cleanly without in-place mutation, enabling snapshot checkpointing and time-travel debugging.
</p>""",

    146: """<h3 class="sh3">1. Multi-Agent Systems & Swarm Topologies</h3>
<p>
When tasks require diverse domain expertise, a single monolithic agent degrades in reliability. <strong>Multi-agent systems</strong> distribute work across specialized personas with distinct toolsets and system prompts:
</p>
<div class="mermaid">
graph TD
  User["User Task"] --> Supervisor["Supervisor / Router Agent"]
  Supervisor --> Res["Researcher Agent\n(Web Search & Paper Tools)"]
  Supervisor --> Code["Coder Agent\n(Python Sandbox & Linter)"]
  Supervisor --> Critic["Critic / Quality Agent\n(Unit Tests & Fact Grader)"]
  Res & Code --> Critic
  Critic -->|Approved| Supervisor
  Supervisor --> Final["Final Synthesized Report"]
</div>
<div class="diagram-cap">Supervisor-Worker Multi-Agent Topology with Specialized Research, Coding, and Quality Verification.</div>""",

    147: """<h3 class="sh3">1. Vector Memory & Coreference Resolution</h3>
<p>
Agents interacting over long multi-turn sessions require both short-term working memory (conversation context) and long-term episodic memory (vectorized knowledge base). <strong>Coreference resolution</strong> replaces ambiguous pronouns (<em>"it"</em>, <em>"that server"</em>) with canonical entity names before embedding.
</p>
<div class="mermaid">
graph LR
  Input["'Restart it now'"] --> Coref["Coreference Resolver\n(Resolves 'it' -> 'Postgres Pod')"]
  Coref --> Mem["Canonical Query:\n'Restart Postgres Pod'"]
  Mem --> Retrieval["Vector Memory & Action Lookup"]
</div>
<div class="diagram-cap">Coreference resolution replaces pronouns with explicit entities before memory storage and retrieval.</div>""",

    148: """<h3 class="sh3">1. Human-in-the-Loop (HITL) Validation Patterns</h3>
<p>
Autonomous agents executing destructive or irreversible actions (e.g. running database migrations, issuing refunds, sending emails) require deterministic human approval gates.
</p>
<div class="mermaid">
graph TD
  Agent["Agent Proposes Action:\n'DROP TABLE staging_backup'"] --> Gate{"Safety Gate\n(Risk Score > 0.8)"}
  Gate -->|Safe| Auto["Execute Automatically"]
  Gate -->|High Risk| Pause["Pause Execution & Persist State Checkpoint"]
  Pause --> UI["Notify Human Reviewer (Slack / Web UI)"]
  UI --> Decision{"Human Approval?"}
  Decision -->|Approve| Resume["Resume Execution from Checkpoint"]
  Decision -->|Reject| Abort["Abort & Provide Rejection Feedback to Agent"]
</div>
<div class="diagram-cap">Human-in-the-Loop Approval Gate with State Checkpoint Persistence.</div>""",

    149: """<h3 class="sh3">1. Capstone: Production Multi-Agent System</h3>
<p>
Architecting an autonomous multi-agent software engineering team integrating Supervisor routing, stateful LangGraph execution, dynamic tool registration, episodic memory, and human review gates.
</p>
<div class="mermaid">
graph TD
  Task["Feature Request"] --> Lead["Tech Lead Agent"]
  Lead --> Plan["Architecture Spec"]
  Plan --> Dev["Developer Agent"]
  Dev --> Tests["QA / Test Runner Agent"]
  Tests --> Review{"Tests Pass?"}
  Review -->|No| Dev
  Review -->|Yes| HumanGate["Human Approval Gate"]
  HumanGate --> Deploy["Deployment Agent"]
</div>
<div class="diagram-cap">Production Multi-Agent Software Development Life Cycle Topology.</div>""",

    # ═════════════════════════════════════════════════════════════════════
    # WEEK 21: LLM FINE-TUNING & INFERENCE (Days 150 - 156)
    # ═════════════════════════════════════════════════════════════════════
    150: """<h3 class="sh3">1. High-Throughput LLM Serving with vLLM & PagedAttention</h3>
<p>
Standard autoregressive decoding suffers from severe GPU memory fragmentation because the Key-Value (KV) cache grows dynamically per token. Traditional serving allocates contiguous memory for the maximum possible sequence length, wasting up to 60–80% of VRAM.
</p>
<div class="mermaid">
graph TD
  subgraph Traditional Serving (Contiguous Pre-allocation)
    A1["Request 1 KV: [Tokens 1..50] (Allocated 2048 - 95% Wasted)"]
    A2["Severe Virtual Memory Fragmentation & OOM under batching"]
  end
  subgraph PagedAttention (Non-Contiguous Virtual Paging)
    B1["Physical KV Blocks in VRAM: [Block 0][Block 1][Block 2]..."]
    B2["Virtual Page Table maps Request Token Sequence to arbitrary physical blocks"]
    B3["Near Zero Memory Waste (>96% GPU Memory Utilization)"]
  end
</div>
<div class="diagram-cap">PagedAttention Virtual Memory Allocation vs Traditional Contiguous Pre-allocation.</div>

<h3 class="sh3">2. Continuous Batching & KV Cache Sizing</h3>
<p>
vLLM pairs PagedAttention with <strong>Continuous (Iteration-Level) Batching</strong>: rather than waiting for an entire batch to finish generation, completed sequences are evicted immediately and new requests are injected at the next token iteration.
</p>""",

    151: """<h3 class="sh3">1. FlashAttention: IO-Aware Exact Attention</h3>
<p>
Standard attention computes $QK^T$, writes the full $N \times N$ matrix to slow GPU High-Bandwidth Memory (HBM), computes Softmax, writes to HBM, and multiplies by $V$. <strong>FlashAttention</strong> tiles the computation into fast on-chip SRAM blocks, computing online softmax without ever materializing the $O(N^2)$ attention matrix in HBM.
</p>
<div class="mermaid">
graph LR
  subgraph Standard Attention (Memory Bottleneck)
    Q1["Q, K, V in HBM"] -->|Read| S1["Compute S = QK^T"]
    S1 -->|Write O(N^2) to HBM| HBM1["Slow HBM Matrix"]
    HBM1 -->|Read| S2["Softmax(S)"]
    S2 -->|Write O(N^2) to HBM| HBM2["Slow HBM Matrix"]
    HBM2 -->|Read| S3["P * V -> Out"]
  end
  subgraph FlashAttention (IO-Aware Tiling)
    Q2["Load Blocks Q_i, K_j into Fast SRAM"] --> Tile["Tile Computation + Online Softmax in SRAM"]
    Tile -->|Write Final O(N) only| Out["Output in HBM (2x-4x Speedup, O(N) Memory)"]
  end
</div>
<div class="diagram-cap">FlashAttention IO-aware SRAM block tiling vs Standard HBM read/write round-trips.</div>

<h3 class="sh3">2. Speculative Decoding</h3>
<p>
Speculative decoding uses a fast, lightweight draft model (e.g. 1B params) to guess $K$ candidate tokens in parallel, which are verified by the primary target model (e.g. 70B params) in a single parallel forward pass, achieving 2x–3x lower latency with identical output distribution.
</p>""",

    152: """<h3 class="sh3">1. Model Quantization: AWQ vs. GPTQ vs. GGUF</h3>
<p>
Large language models are memory-bandwidth bound during inference. Quantizing weights from 16-bit floats (FP16/BF16) to 4-bit integers (INT4) reduces VRAM requirements by up to 75% and doubles token generation speed.
</p>
<div class="mermaid">
graph TD
  Quant["Quantization Paradigms"] --> PTQ["1. Post-Training Quantization (PTQ)"]
  Quant --> QAT["2. Quantization-Aware Training (QAT)"]
  PTQ --> AWQ["AWQ (Activation-aware Weight Quantization)\n(Protects top 1% salient weights, best for serving)"]
  PTQ --> GPTQ["GPTQ (One-shot Layer-wise Inversion)\n(High compression, fast GPU kernels)"]
  PTQ --> GGUF["GGUF / llama.cpp\n(CPU + GPU offloading, k-quants)"]
</div>
<div class="diagram-cap">LLM Quantization Methods and Architectural Trade-offs.</div>""",

    153: """<h3 class="sh3">1. Parameter-Efficient Fine-Tuning (PEFT) & LoRA</h3>
<p>
Full parameter fine-tuning of a 70B model requires updating and storing 140GB+ of optimizer states and gradients across multiple GPUs. <strong>Low-Rank Adaptation (LoRA)</strong> freezes the pretrained weight matrix $W_0 \in \mathbb{R}^{d \times k}$ and decomposes the update into two low-rank matrices $A \in \mathbb{R}^{r \times k}$ and $B \in \mathbb{R}^{d \times r}$ with rank $r \ll \min(d, k)$:
</p>
<div class="math-block">
$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$
</div>
<p>
Where $A \sim \mathcal{N}(0, \sigma^2)$ and $B = 0$ at initialization, ensuring $\Delta W = 0$ before training begins.
</p>
<div class="mermaid">
graph LR
  x["Input Vector x"] --> W0["Frozen Pretrained Weights W_0\n(d x k)"]
  x --> A["LoRA Down-projection A\n(r x k)"]
  A --> B["LoRA Up-projection B\n(d x r)"]
  W0 --> Add["(+)"]
  B -->|Scaled by alpha/r| Add
  Add --> Out["Output Vector h"]
</div>
<div class="diagram-cap">LoRA Low-Rank Decomposition with Frozen Base Weights.</div>""",

    154: """<h3 class="sh3">1. Preference Alignment: DPO vs. ORPO vs. GRPO</h3>
<p>
Post-training alignment teaches models to follow human preferences (helpfulness and harmlessness). While traditional RLHF requires training a separate Reward Model and running complex PPO loops, modern alignment uses direct loss formulations:
</p>
<div class="mermaid">
graph TD
  Align["Alignment Methodologies"] --> RLHF["1. RLHF (PPO)\n(Requires Actor + Critic + Reward + Ref Model = 4 models in VRAM)"]
  Align --> DPO["2. DPO (Direct Preference Optimization)\n(Closed-form optimization over pairwise preferences [y_w > y_l])"]
  Align --> ORPO["3. ORPO (Odds Ratio Preference Optimization)\n(Monolithic SFT + Odds Ratio penalty, no ref model needed)"]
  Align --> GRPO["4. GRPO (Group Relative Policy Optimization)\n(Group-normalized reward sampling, DeepSeek-R1 reasoning alignment)"]
</div>
<div class="diagram-cap">Evolution of Preference Alignment from RLHF to Direct Closed-Form and Group-Relative Optimization.</div>

<h3 class="sh3">2. The DPO Objective</h3>
<div class="math-block">
$$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$
</div>""",

    155: """<h3 class="sh3">1. Synthetic Data Generation & MinHash Deduplication</h3>
<p>
High-quality fine-tuning data is the primary determinant of model performance. Synthetic data pipelines use frontier LLMs to generate reasoning traces, instruction-response pairs, and self-critiques, filtered by rigorous quality and deduplication gates.
</p>
<div class="mermaid">
graph LR
  Seed["Seed Prompts"] --> LLM["Frontier LLM (Evol-Instruct / Self-Instruct)"]
  LLM --> Raw["Raw Synthetic Corpus"]
  Raw --> MinHash["MinHash + LSH Near-Deduplication"]
  MinHash --> Filter["Reward / Quality LLM Filter"]
  Filter --> Dataset["Curated High-Quality SFT Dataset"]
</div>
<div class="diagram-cap">Synthetic Data Generation, Quality Filtering, and MinHash Deduplication Pipeline.</div>""",

    156: """<h3 class="sh3">1. Capstone: Deploying a Custom Fine-Tuned Model</h3>
<p>
Completing the end-to-end LLM lifecycle: SFT dataset curation with synthetic augmentation, QLoRA fine-tuning with Hugging Face TRL / Unsloth, DPO preference alignment, LoRA weight merging, AWQ quantization, and production deployment on vLLM.
</p>
<div class="mermaid">
graph LR
  Data["Curated SFT Dataset"] --> QLoRA["QLoRA Fine-Tuning"]
  QLoRA --> DPO["DPO Preference Tuning"]
  DPO --> Merge["Merge Adapters -> FP16"]
  Merge --> AWQ["AWQ 4-bit Quantization"]
  AWQ --> vLLM["vLLM High-Throughput Serving Cluster"]
  vLLM --> Client["Client Application"]
</div>
<div class="diagram-cap">End-to-End Fine-Tuning, Alignment, Quantization, and vLLM Serving Pipeline.</div>"""
}
