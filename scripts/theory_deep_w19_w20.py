# scripts/theory_deep_w19_w20.py
# Deep theory for all 14 days in Weeks 19 and 20

W19_W20_THEORY = {
    # ── DAY 136: Hybrid Search & RRF ──
    136: r"""<h3 class="sh3">1. Dense vs Sparse Search: Complementary Strengths</h3>
<p>
Dense vector search encodes queries and documents into continuous vector spaces using neural bi-encoders (e.g. <code>text-embedding-3-large</code>, <code>bge-large-en-v1.5</code>). It excels at matching high-level semantic intent, conceptual synonyms, and fuzzy paraphrases. However, dense search routinely fails on <strong>exact keyword matching</strong>, serial numbers, SKU codes, technical identifiers (e.g. <code>ERR_0x80070005</code>), and rare named entities.
</p>
<p>
Conversely, sparse lexical algorithms like <strong>BM25</strong> (Best Matching 25) compute relevance strictly based on term frequency and inverse document frequency ($TF \times IDF$). BM25 guarantees precision on exact tokens but cannot recognize semantic relatedness when query and document use different vocabulary.
</p>
<div class="mermaid">
graph TD
    Query["User Query: 'Troubleshoot error 0x80070005 in Azure VM'"] --> Dispatcher{"Query Dispatcher"}
    Dispatcher -->|Dense Embedder| DenseIndex["Dense Vector Index (HNSW / Cosine)"]
    Dispatcher -->|BM25 Tokenizer| SparseIndex["Sparse Lexical Index (Inverted Index)"]
    DenseIndex -->|Top 50 Candidates| RRF["Reciprocal Rank Fusion (RRF) Engine\nRRF(d) = sum( 1 / (60 + rank_i) )"]
    SparseIndex -->|Top 50 Candidates| RRF
    RRF --> TopFused["Fused & Deduplicated Candidates (Top 20)"]
    TopFused --> Reranker["Cross-Encoder Reranker"]
    Reranker --> LLMContext["Final Top-5 Grounded Context -> LLM"]
</div>
<div class="diagram-cap">Figure 136.1: Enterprise Hybrid Search Architecture with Parallel Dense/Sparse Ingestion and Reciprocal Rank Fusion.</div>

<h3 class="sh3">2. Reciprocal Rank Fusion (RRF) Mathematical Formulation</h3>
<p>
Because raw BM25 scores (unbounded reals $[0, \infty)$) and dense similarity scores (bounded $[-1, 1]$ or $[0, 1]$) have incompatible distributions, naive linear score combination requires fragile tuning. RRF resolves this by fusing documents based purely on their <em>ordinal rank position</em>:
</p>
<div class="math-block">
$$\text{RRF}(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
</div>
<p>
Where $M = \{\text{Dense}, \text{BM25}\}$, $r_m(d) \in \{1, 2, \dots, K\}$ is the 1-based rank of document $d$ in system $m$, and $k = 60$ is the established smoothing constant that prevents high-ranking outliers from overpowering consistent multi-system consensus.
</p>

<h3 class="sh3">3. Production Python RRF Engine Implementation</h3>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code><span class="kw">from</span> typing <span class="kw">import</span> List, Dict
<span class="kw">from</span> collections <span class="kw">import</span> defaultdict

<span class="kw">def</span> <span class="fn">reciprocal_rank_fusion</span>(
    dense_results: List[Dict],
    sparse_results: List[Dict],
    k: int = <span class="num">60</span>,
    top_n: int = <span class="num">5</span>
) -> List[Dict]:
    rrf_scores: Dict[str, float] = defaultdict(float)
    doc_map: Dict[str, Dict] = {}

    <span class="kw">for</span> rank, doc <span class="kw">in</span> enumerate(dense_results, start=<span class="num">1</span>):
        d_id = doc[<span class="str">'id'</span>]
        rrf_scores[d_id] += <span class="num">1.0</span> / (k + rank)
        doc_map[d_id] = doc

    <span class="kw">for</span> rank, doc <span class="kw">in</span> enumerate(sparse_results, start=<span class="num">1</span>):
        d_id = doc[<span class="str">'id'</span>]
        rrf_scores[d_id] += <span class="num">1.0</span> / (k + rank)
        doc_map[d_id] = doc

    ranked_ids = sorted(rrf_scores.keys(), key=<span class="kw">lambda</span> x: rrf_scores[x], reverse=<span class="kw">True</span>)
    fused = []
    <span class="kw">for</span> d_id <span class="kw">in</span> ranked_ids[:top_n]:
        res = dict(doc_map[d_id])
        res[<span class="str">'rrf_score'</span>] = round(rrf_scores[d_id], <span class="num">5</span>)
        fused.append(res)
    <span class="kw">return</span> fused</code></pre>
</div>""",

    # ── DAY 137: Cross-Encoders & Re-ranking ──
    137: r"""<h3 class="sh3">1. The Two-Stage Information Retrieval Architecture</h3>
<p>
In enterprise search over millions of chunks, running deep cross-attention on every document at query time is computationally prohibitive ($O(N \cdot L^2)$ transformer latency). High-throughput search systems split retrieval into two distinct stages:
</p>
<ul>
  <li><strong>Stage 1 (Bi-Encoder Candidate Generation):</strong> Offline-computed vector embeddings allow vector ANN indexes (HNSW, ScaNN) to retrieve the top 50–100 candidate chunks in under 10ms.</li>
  <li><strong>Stage 2 (Cross-Encoder Re-Ranking):</strong> A heavy transformer model evaluates full self-attention across the combined sequence $[\text{CLS}] \circ \text{Query} \circ [\text{SEP}] \circ \text{Passage} \circ [\text{SEP}]$, scoring semantic relevance with 10x higher precision.</li>
</ul>
<div class="mermaid">
graph LR
    UserQuery["Query"] --> BiEncoder["Stage 1: Bi-Encoder (HNSW Index)\nRetrieve Top-100 in 10ms"]
    BiEncoder --> CrossEncoder["Stage 2: Cross-Encoder (BGE-Reranker)\nFull Self-Attention over (Q, P) in 30ms"]
    CrossEncoder --> LLMContext["Top 3-5 Filtered Chunks -> LLM Context"]
</div>
<div class="diagram-cap">Figure 137.1: Two-stage retrieval pipeline combining Bi-Encoder scale with Cross-Encoder precision.</div>

<h3 class="sh3">2. Cross-Encoder Mathematical Formulation</h3>
<p>
Unlike bi-encoders which project query and document into separate vector spaces ($\text{score} = \vec{q} \cdot \vec{d}$), cross-encoders concatenate them into a single token sequence:
</p>
<div class="math-block">
$$\mathbf{X} = [\text{CLS}], q_1, \dots, q_m, [\text{SEP}], p_1, \dots, p_n, [\text{SEP}]$$
</div>
<p>
The final hidden state of the classification token $\mathbf{h}_{[\text{CLS}]}$ captures full query-document token interactions and is projected through a linear classification head:
</p>
<div class="math-block">
$$s(q, p) = \sigma(\mathbf{W}^T \mathbf{h}_{[\text{CLS}]} + b)$$
</div>""",

    # ── DAY 138: Advanced Chunking Strategies ──
    138: r"""<h3 class="sh3">1. The Granularity Dilemma in Document Chunking</h3>
<p>
Document chunking directly dictates retrieval precision and generation quality. If chunks are too small (e.g. 100 tokens), they lack surrounding context for complex synthesis. If chunks are too large (e.g. 1500 tokens), embeddings average too many unrelated concepts together, causing the target answer to be lost during vector matching.
</p>
<div class="mermaid">
graph TD
    Document["Raw Document (Markdown / PDF)"] --> Chunker{"Chunking Architecture"}
    Chunker --> ParentChild["Parent-Child Indexing\nSearch on 128-token child chunks;\nPass 1024-token parent chunk to LLM"]
    Chunker --> SemanticBoundaries["Semantic Chunking\nSplit text dynamically when sentence-to-sentence\ncosine similarity drops below threshold theta"]
    Chunker --> StructureAware["Document Structure-Aware\nSplit on Markdown H1/H2/H3 headers and tables"]
</div>
<div class="diagram-cap">Figure 138.1: Advanced chunking strategies resolving the granularity dilemma.</div>

<h3 class="sh3">2. Parent-Child / Small-to-Big Retrieval Implementation</h3>
<p>
Small-to-Big chunking indexes small, specific child chunks for high vector search recall, but maps matches back to parent document chunks for generation:
</p>
<div class="cb">
  <div class="cb-head"><span class="cb-lang">python</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button></div></div>
  <pre><code><span class="kw">from</span> typing <span class="kw">import</span> List, Dict
<span class="kw">import</span> uuid

<span class="kw">class</span> <span class="fn">ParentChildChunker</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self, parent_size: int = <span class="num">1024</span>, child_size: int = <span class="num">256</span>, overlap: int = <span class="num">32</span>):
        self.parent_size = parent_size
        self.child_size = child_size
        self.overlap = overlap

    <span class="kw">def</span> <span class="fn">chunk_text</span>(self, text: str) -> Dict[str, list]:
        words = text.split()
        parents, children = [], []
        
        <span class="kw">for</span> p_start <span class="kw">in</span> range(<span class="num">0</span>, len(words), self.parent_size - self.overlap):
            p_words = words[p_start : p_start + self.parent_size]
            p_id = str(uuid.uuid4())
            parents.append({<span class="str">'id'</span>: p_id, <span class="str">'text'</span>: <span class="str">' '</span>.join(p_words)})

            <span class="kw">for</span> c_start <span class="kw">in</span> range(<span class="num">0</span>, len(p_words), self.child_size - self.overlap):
                c_words = p_words[c_start : c_start + self.child_size]
                children.append({
                    <span class="str">'child_id'</span>: str(uuid.uuid4()),
                    <span class="str">'parent_id'</span>: p_id,
                    <span class="str">'text'</span>: <span class="str">' '</span>.join(c_words)
                })
        <span class="kw">return</span> {<span class="str">'parents'</span>: parents, <span class="str">'children'</span>: children}</code></pre>
</div>""",

    # ── DAY 139: Vector Indexing Deep Dive ──
    139: r"""<h3 class="sh3">1. Exact vs Approximate Nearest Neighbors (ANN)</h3>
<p>
Exact search (<strong>Flat Index / FlatL2</strong>) performs exhaustive $O(N \cdot d)$ pairwise distance calculations. While recall is 100%, query latency scales linearly with dataset size ($N$), becoming unusable for datasets exceeding 1,000,000 vectors.
</p>
<p>
Production vector databases (Qdrant, Pinecone, Milvus) employ <strong>Approximate Nearest Neighbors (ANN)</strong> algorithms to trade off fractional recall (&gt;98%) for logarithmic or constant lookup speeds:
</p>
<ul>
  <li><strong>Inverted File Index (IVF):</strong> Partitions vector space into $C$ Voronoi cells using k-means. Searches only the centroids closest to the query vector (controlled by parameter <code>nprobe</code>).</li>
  <li><strong>Hierarchical Navigable Small World (HNSW):</strong> Builds a multi-layer proximity graph where upper layers provide fast long-distance traversal and lower layers provide fine-grained local convergence. $O(\log N)$ search complexity.</li>
  <li><strong>Product Quantization (PQ):</strong> Subdivides high-dimensional vectors into sub-vectors, quantizing each into centroid codebooks to compress VRAM by 85–95%.</li>
</ul>

<h3 class="sh3">2. Vector Index Performance Comparison Matrix</h3>
<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px;">
  <thead>
    <tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:8px;">Index Type</th>
      <th style="padding:8px;">Search Complexity</th>
      <th style="padding:8px;">Recall @ 10</th>
      <th style="padding:8px;">Memory Footprint</th>
      <th style="padding:8px;">Build Time</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>Flat (Exact)</strong></td>
      <td style="padding:8px;">$O(N \cdot d)$</td>
      <td style="padding:8px;">100%</td>
      <td style="padding:8px;">1x (Raw Vectors)</td>
      <td style="padding:8px;">Zero</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>IVF-Flat</strong></td>
      <td style="padding:8px;">$O(\text{nprobe} \cdot \frac{N}{C} \cdot d)$</td>
      <td style="padding:8px;">92 - 97%</td>
      <td style="padding:8px;">1.1x</td>
      <td style="padding:8px;">Fast (K-means clustering)</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>HNSW</strong></td>
      <td style="padding:8px;">$O(\log N)$</td>
      <td style="padding:8px;"><strong>98 - 99.5%</strong></td>
      <td style="padding:8px;">1.5x - 2.0x (Graph edges)</td>
      <td style="padding:8px;">Moderate</td>
    </tr>
    <tr style="border-bottom:1px solid var(--border);">
      <td style="padding:8px;"><strong>HNSW + Scalar Quantization (SQ8)</strong></td>
      <td style="padding:8px;">$O(\log N)$</td>
      <td style="padding:8px;">97 - 99%</td>
      <td style="padding:8px;"><strong>0.35x (65% RAM reduction)</strong></td>
      <td style="padding:8px;">Moderate</td>
    </tr>
  </tbody>
</table>""",

    # ── DAY 140: GraphRAG & Knowledge Graphs ──
    140: r"""<h3 class="sh3">1. The Point-Lookup Failure of Standard Vector RAG</h3>
<p>
Standard vector similarity retrieval is designed for <strong>local point lookups</strong>: queries that ask for specific, localized facts (e.g. <em>"What is the interest rate on loan #8812?"</em>). However, vector RAG fails completely on <strong>global aggregation and relational reasoning queries</strong>, such as:
</p>
<ul>
  <li><em>"What are the main systemic supply chain failure modes across all European vendor audits in 2024?"</em></li>
  <li><em>"How do the security vulnerabilities in the authentication service relate to the incidents reported by the payment gateway?"</em></li>
</ul>
<p>
Because vector embeddings match against isolated chunks, no single chunk contains the macro-level answer. <strong>GraphRAG</strong> (developed by Microsoft Research) bridges this gap by extracting a knowledge graph of entities and relationships from the text, running community detection, and pre-generating hierarchical community summaries.
</p>
<div class="mermaid">
graph TD
    RawDocs["Corpus Documents"] --> LLMExtract["LLM Extraction Pipeline\nExtract: Entities (Nodes), Claims, & Relations (Edges)"]
    LLMExtract --> KnowledgeGraph["Knowledge Graph G = (V, E)"]
    KnowledgeGraph --> Leiden["Leiden Community Detection Algorithm\nHierarchical Graph Partitioning (Levels C0, C1, C2)"]
    Leiden --> CommSummaries["Community Summary Generation\nPre-summarize each cluster with an LLM"]
    CommSummaries --> GlobalSearch["Global Search Engine\nQuery mapped to community summaries -> Map-Reduce Synthesis"]
</div>
<div class="diagram-cap">Figure 140.1: GraphRAG Extraction, Leiden Clustering, and Hierarchical Community Summarization.</div>

<h3 class="sh3">2. Leiden Community Detection & Modularity Math</h3>
<p>
The Leiden algorithm partitions the entity graph into densely connected clusters by maximizing network <strong>modularity</strong> $\mathcal{H}$:
</p>
<div class="math-block">
$$\mathcal{H} = \frac{1}{2m} \sum_{i,j} \left( A_{ij} - \gamma \frac{k_i k_j}{2m} \right) \delta(\sigma_i, \sigma_j)$$
</div>
<p>
Where $A_{ij}$ is the adjacency weight between entity $i$ and $j$, $k_i = \sum_j A_{ij}$ is the degree of node $i$, $m = \frac{1}{2}\sum_{ij} A_{ij}$ is the total network edge weight, $\gamma$ is the resolution parameter, and $\delta(\sigma_i, \sigma_j) = 1$ if nodes $i, j$ belong to the same community $\sigma$.
</p>""",

    # ── DAY 141: Advanced Query Transformations ──
    141: r"""<h3 class="sh3">1. Query Reformulation Strategies in Enterprise RAG</h3>
<p>
User queries are frequently poorly formulated, ambiguous, or conceptually distant from the target document phrasing. <strong>Advanced Query Transformations</strong> rewrite, expand, or decompose the raw user prompt prior to vector index querying:
</p>
<div class="mermaid">
graph TD
    RawPrompt["User Query"] --> Transform{"Transformation Engine"}
    Transform --> HyDE["1. HyDE (Hypothetical Document Embeddings)\nGenerate a hypothetical answer with LLM;\nEmbed the hallucinated answer instead of query"]
    Transform --> MultiQuery["2. Multi-Query Expansion\nGenerate 3-5 diverse linguistic variants of query;\nExecute parallel searches and fuse results"]
    Transform --> StepBack["3. Step-Back Prompting\nAbstract query into high-level fundamental principle;\nRetrieve foundational background context"]
    Transform --> SubQuery["4. Sub-Query Decomposition\nDecompose complex multi-hop question into sub-queries;\nExecute in parallel and synthesize"]
</div>
<div class="diagram-cap">Figure 141.1: The Four Core Query Transformation Pipelines.</div>

<h3 class="sh3">2. Hypothetical Document Embeddings (HyDE) Formulation</h3>
<p>
HyDE (Gao et al., 2022) leverages an instruction-tuned LLM $M$ to synthesize a hypothetical document:
</p>
<div class="math-block">
\hat{d} = M(q), \quad \vec{v}_{\text{query}} = \text{Embed}(\hat{d})
</div>
<p>
Because $\hat{d}$ resides directly in the <em>document embedding manifold</em> (sharing document vocabulary, grammar, and structural tone), $\vec{v}_{\text{query}}$ achieves significantly higher cosine similarity with actual relevant documents than the short query vector $\text{Embed}(q)$.
</p>""",

    # ── DAY 142: Capstone: Production RAG ──
    142: r"""<h3 class="sh3">1. Production RAG Architecture: End-to-End Blueprint</h3>
<p>
Building an enterprise-grade RAG system requires integrating ingestion, retrieval, reranking, and continuous evaluation into a unified, resilient microservice:
</p>
<div class="mermaid">
graph TD
    User["Client App"] --> APIGateway["FastAPI Gateway + Rate Limiter"]
    APIGateway --> Cache["Semantic Vector Cache (Redis)"]
    Cache -->|Cache Miss| Transform["Query Transformation (HyDE + Multi-Query)"]
    Transform --> HybridSearch["Qdrant Hybrid Index (HNSW + BM25)"]
    HybridSearch --> RRF["RRF Fusion (Top 50 Candidates)"]
    RRF --> CrossEncoder["Cross-Encoder Reranker (BGE-Reranker-Large)"]
    CrossEncoder --> GuardrailIn["Input Safety Guardrail (Presidio PII Scrubbing)"]
    GuardrailIn --> LLM["vLLM Serving Cluster (Llama-3-70B)"]
    LLM --> GuardrailOut["Output Grounding Guardrail (Hallucination Check)"]
    GuardrailOut --> Telemetry["OpenTelemetry Tracing + RAGAS Monitoring"]
    GuardrailOut --> User
</div>
<div class="diagram-cap">Figure 142.1: End-to-End Enterprise Production RAG Blueprint.</div>

<h3 class="sh3">2. Production Operational Checklist</h3>
<ul>
  <li><strong>Sub-50ms Retrieval SLA:</strong> Use HNSW + SQ8 vector indexes paired with batch cross-encoder reranking ($K=50$).</li>
  <li><strong>Continuous Evaluation Gates:</strong> Automated CI/CD assertion testing Faithfulness $\ge 0.90$ and Answer Relevance $\ge 0.85$ on golden test sets before promoting code.</li>
</ul>""",

    # ── DAY 143: ReAct & Plan-and-Solve ──
    143: r"""<h3 class="sh3">1. The ReAct Paradigm: Synergizing Reasoning & Action</h3>
<p>
Standard prompting techniques either focus purely on internal reasoning (e.g. <strong>Chain-of-Thought / CoT</strong>) or purely on action execution (e.g. single-step tool calling). Chain-of-Thought suffers from hallucination and state drift on multi-step interactive tasks because it lacks grounded observations from external environments.
</p>
<p>
The <strong>ReAct (Reason + Act)</strong> framework (Yao et al., 2022) introduces an iterative, cyclic feedback loop:
</p>
<div class="math-block">
$$\text{Thought}_t \longrightarrow \text{Action}_t(a_t) \longrightarrow \text{Observation}_t(o_t) \longrightarrow \text{Thought}_{t+1} \dots$$
</div>
<div class="mermaid">
graph LR
    User["User Task Goal"] --> Thought["1. Thought: Reason about sub-goal"]
    Thought --> Action["2. Action: Call API / Database / Code Tool"]
    Action --> Env["Environment Execution (OS, SQL, Web)"]
    Env --> Obs["3. Observation: Parse tool execution output"]
    Obs --> Check{"Goal Satisfied?"}
    Check -->|No / Need Info| Thought
    Check -->|Yes| Finish["Final Synthesized Answer"]
</div>
<div class="diagram-cap">Figure 143.1: The Cyclic ReAct Execution State Machine.</div>

<h3 class="sh3">2. ReAct vs Plan-and-Solve Architecture</h3>
<ul>
  <li><strong>ReAct:</strong> Greedy, reactive next-step selection. Ideal for exploratory queries and unstructured debug workflows.</li>
  <li><strong>Plan-and-Solve:</strong> Generates a full decomposition DAG upfront before executing sub-tasks. Minimizes token consumption on structured multi-step tasks.</li>
</ul>""",

    # ── DAY 144: Structured Output via Instructor ──
    144: r"""<h3 class="sh3">1. The Need for Guaranteed Structured Outputs</h3>
<p>
When LLMs power downstream microservices, robotic control loops, or database operations, raw unstructured natural language is unacceptable. Responses must conform strictly to typed schemas (Pydantic / JSON Schema) without hallucinated keys, invalid enums, or parsing failures.
</p>
<div class="mermaid">
graph LR
    Prompt["Prompt + Pydantic Schema"] --> LLM["LLM Inference Engine"]
    LLM --> JSONParse{"JSON Validation"}
    JSONParse -->|Valid Schema| Success["Typed Pydantic Object Output"]
    JSONParse -->|ValidationError| RetryLoop["Instructor Self-Correction Loop\nFeed Error Diff back to LLM for instant heal"]
    RetryLoop --> LLM
</div>
<div class="diagram-cap">Figure 144.1: Instructor Schema Validation & Automated Self-Correction Loop.</div>

<h3 class="sh3">2. Constrained Grammar Masking (CFG)</h3>
<p>
Modern inference engines (e.g. vLLM, outlines) enforce JSON compliance at the token logit level:
</p>
<div class="math-block">
\text{LogitMask}(t_i) = \begin{cases} 0 & \text{if token } t_i \text{ is syntactically valid in CFG state } S \\ -\infty & \text{if token } t_i \text{ violates JSON schema} \end{cases}
</div>
<p>
This mathematically guarantees 100% syntactically valid JSON in a single forward pass without retry overhead.
</p>""",

    # ── DAY 145: LangGraph StateGraph ──
    145: r"""<h3 class="sh3">1. Why StateGraphs? Moving Beyond Linear Chains</h3>
<p>
Real-world agentic workflows are inherently <strong>cyclical and stateful</strong>. An agent must evaluate code output, catch exceptions, loop back to rewrite the code, ask for human clarification, or branch dynamically based on run-time tool responses. <strong>LangGraph</strong> models these compound systems as a <strong>Cyclic StateGraph</strong>:
</p>
<div class="mermaid">
stateDiagram-v2
    [*] --> PlannerNode: User Goal
    PlannerNode --> ToolExecutionNode: Action Required
    ToolExecutionNode --> EvaluatorNode: Tool Observation
    EvaluatorNode --> PlannerNode: Error / Retry Loop
    EvaluatorNode --> [*]: Goal Satisfied & Verified
</div>
<div class="diagram-cap">Figure 145.1: LangGraph Cyclic StateGraph with Self-Correction Loops.</div>

<h3 class="sh3">2. Core StateGraph Architecture Primitives</h3>
<ul>
  <li><strong>State Schema (TypedDict / Pydantic):</strong> Immutable state passed between nodes. Nodes return functional state diffs.</li>
  <li><strong>Nodes (Pure Functions):</strong> Callable Python units ($f(\text{State}) \to \Delta \text{State}$) that perform discrete tasks.</li>
  <li><strong>Conditional Edges:</strong> Routing functions that inspect state and determine the next execution node dynamically.</li>
  <li><strong>Checkpointers:</strong> Snapshot state history across every step, enabling deterministic time-travel rollbacks and human-in-the-loop approvals.</li>
</ul>""",

    # ── DAY 146: Multi-Agent Systems ──
    146: r"""<h3 class="sh3">1. Multi-Agent Topologies & Worker Swarms</h3>
<p>
Monolithic agents burdened with dozens of tools suffer from context dilution, instruction confusion, and high error rates. <strong>Multi-Agent Systems</strong> decompose complex workflows into specialized, single-responsibility agents coordinated through structured topologies:
</p>
<div class="mermaid">
graph TD
    User["User Mission"] --> Supervisor["Supervisor / Router Agent\nDecomposes mission & assigns sub-tasks"]
    Supervisor --> AgentA["Research Agent\n(Tools: ArXiv, Google, Vector DB)"]
    Supervisor --> AgentB["Coder Agent\n(Tools: Python Sandbox, AST Validator)"]
    Supervisor --> AgentC["Security Auditor Agent\n(Tools: Semgrep, Bandit, Dependency Scan)"]
    AgentA & AgentB & AgentC --> Critic["Critic & Synthesis Agent\nEvaluates output quality gates"]
    Critic -->|Pass| FinalDelivery["Final Verified Result"]
    Critic -->|Reject| Supervisor
</div>
<div class="diagram-cap">Figure 146.1: Hierarchical Multi-Agent Architecture with Supervisor and Quality Critic Gates.</div>

<h3 class="sh3">2. Core Multi-Agent Interaction Patterns</h3>
<ul>
  <li><strong>Hierarchical Supervisor:</strong> A central manager agent delegates tasks to domain specialists and aggregates outputs.</li>
  <li><strong>Sequential Assembly Line:</strong> Agents execute in fixed order, passing progressive artifacts downstream.</li>
  <li><strong>Evaluator-Optimizer:</strong> Generator agent generates candidates; Critic agent evaluates against rubric and requests revisions until convergence.</li>
</ul>""",

    # ── DAY 147: Vector Memory & Coreference ──
    147: r"""<h3 class="sh3">1. Episodic vs Semantic Agent Memory</h3>
<p>
Autonomous agents operating over extended sessions require persistent memory systems:
</p>
<ul>
  <li><strong>Short-Term Working Memory:</strong> In-context message history ($N$ recent turns). Constrained by token context limits.</li>
  <li><strong>Long-Term Episodic Memory:</strong> Vector-indexed conversational snapshots retrieved dynamically based on query semantic similarity.</li>
</ul>

<h3 class="sh3">2. Coreference Resolution & Temporal Decay</h3>
<p>
Raw conversational turns contain ambiguous pronouns (e.g. <em>"Deploy it to staging"</em>). Prior to vector indexing, <strong>Coreference Resolution</strong> rewrites pronouns into explicit canonical entity names (<em>"Deploy the payment microservice to staging"</em>).
</p>
<p>
To prevent stale historical memories from overpowering fresh user instructions, retrieval combines cosine similarity with <strong>exponential temporal decay</strong>:
</p>
<div class="math-block">
$$\text{Score}(m) = \cos(\vec{q}, \vec{v}_m) \times \exp(-\lambda \cdot \Delta t)$$
</div>
<p>
Where $\Delta t$ is the memory age in hours and $\lambda$ is the recency decay coefficient.
</p>""",

    # ── DAY 148: Human-in-the-loop (HITL) ──
    148: r"""<h3 class="sh3">1. Human-in-the-Loop (HITL) Safety Gates</h3>
<p>
Autonomous AI agents executing in enterprise production environments must have hard safety boundaries. While read-only operations (e.g. data search, summarization) can run autonomously, <strong>state-mutating, financial, or irreversible actions</strong> (e.g. database schema migrations, funds transfer, sending external emails) require explicit human authorization.
</p>
<div class="mermaid">
stateDiagram-v2
    [*] --> AgentAutonomous: Task Ingestion
    AgentAutonomous --> ActionProposal: Plan Action
    ActionProposal --> SafetyGateCheck: Risk Evaluation
    SafetyGateCheck --> AutoExecute: Low Risk (Read-only)
    SafetyGateCheck --> PauseState: High Risk (State-mutating)
    PauseState --> PersistCheckpoint: Save State to DB
    PersistCheckpoint --> HumanReviewer: Alert Slack/Dashboard
    HumanReviewer --> ResumeExecution: Human Approved
    HumanReviewer --> AbortRollback: Human Rejected
    AutoExecute --> [*]
    ResumeExecution --> [*]
    AbortRollback --> [*]
</div>
<div class="diagram-cap">Figure 148.1: LangGraph Human-in-the-Loop (HITL) Interrupt and Approval State Machine.</div>""",

    # ── DAY 149: Capstone: Multi-Agent System ──
    149: r"""<h3 class="sh3">1. Production Multi-Agent System Architecture</h3>
<p>
The Multi-Agent Capstone integrates all Week 20 competencies into a production-grade autonomous research and software engineering assistant:
</p>
<ul>
  <li><strong>LangGraph State Machine:</strong> Dynamic routing across Supervisor, Research, Coding, and Critic nodes.</li>
  <li><strong>Strict Schema Validation:</strong> Instructor / Pydantic schemas enforce type safety across all inter-agent messages.</li>
  <li><strong>Persistent Checkpointing:</strong> PostgreSQL state checkpointer enables pauses for human review and error rollback.</li>
  <li><strong>Distributed OpenTelemetry Spans:</strong> Every tool execution and agent hop records token consumption, latency, and tool status.</li>
</ul>"""
}

print(f"Loaded {len(W19_W20_THEORY)} comprehensive theory modules for Weeks 19 & 20.")
