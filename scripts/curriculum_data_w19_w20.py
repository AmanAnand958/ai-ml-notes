# scripts/curriculum_data_w19_w20.py
# Exhaustive pedagogical theory & task prompts for Weeks 19 & 20 (Days 136 - 149)

CURRICULUM_W19_W20 = {
    # ── DAY 136: Hybrid Search & RRF ──
    136: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> You are architecting the retrieval engine for an enterprise cloud troubleshooting portal. The portal contains millions of server log snippets, diagnostic guides, and technical error documentation. Queries frequently contain exact hexadecimal error codes (e.g. <code>0x80070005</code>) alongside natural language symptom descriptions (e.g. <em>"Access denied when mounting volume"</em>).</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement an in-memory <strong>Okapi BM25 Lexical Index</strong> that tokenizes input documents, builds an inverted index, computes term frequencies, and evaluates document length normalization ($k_1 = 1.5, b = 0.75$).</li>
  <li>Implement a <strong>Dense Vector Cosine Scorer</strong> that computes bi-encoder vector dot products over normalized embeddings.</li>
  <li>Build a <strong>Reciprocal Rank Fusion (RRF) combiner</strong> with parameter $k = 60$ that merges parallel candidate lists into a single ranked pool.</li>
  <li>Ensure all doc scores include provenance metadata: <code>dense_rank</code>, <code>sparse_rank</code>, and final <code>rrf_score</code>.</li>
</ul>""",
            """<p><strong>Scenario:</strong> Benchmark the recall and latency of your hybrid search implementation against pure dense search and pure BM25 search over a 100-document technical diagnostic benchmark dataset.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Execute 10 test queries combining exact error tokens (<code>ERR_VNET_TIMEOUT</code>, <code>HTTP_504</code>) and semantic intent queries.</li>
  <li>Compute <strong>Mean Reciprocal Rank (MRR@10)</strong> and <strong>Hit Rate@5</strong> across all three retrieval modes.</li>
  <li>Assert that Hybrid Search achieves $\text{MRR@10} \ge 0.85$ and beats both standalone BM25 and standalone vector search by at least 10% relative margin.</li>
</ul>"""
        ]
    },

    # ── DAY 137: Cross-Encoders & Re-ranking ──
    137: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> In high-throughput customer support RAG, Bi-Encoder vector retrieval returns 50 candidate passages from technical manuals. However, subtle linguistic nuances (such as negative conditions: <em>"Do NOT restart server if error is 0x4B"</em>) are scored identically to positive conditions by vector dot products.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a <strong>Two-Stage Reranking Pipeline</strong> that takes a user query and 50 candidate passages from Stage-1 retrieval.</li>
  <li>Build a <strong>Cross-Encoder Joint Scorer</strong> evaluating cross-attention representations over $(q, p)$ pairs.</li>
  <li>Calibrate raw logits to sigmoid probabilities and sort candidates descending by rerank score.</li>
  <li>Measure and log Stage-1 vs Stage-2 p95 latency to verify compliance with a 50ms SLA budget.</li>
</ul>"""
        ]
    },

    # ── DAY 138: Advanced Chunking Strategies ──
    138: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> You are processing 500-page enterprise financial annual reports (10-K filings) containing dense text paragraphs, nested Markdown tables, and structured header hierarchies. Naive 500-character chunking breaks tables mid-row and severs footnote definitions.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a <strong>Parent-Child (Small-to-Big) Chunker</strong> that splits documents into 1024-token parent context blocks and subdivides each into 256-token searchable child chunks.</li>
  <li>Implement a <strong>Semantic Boundary Chunker</strong> that computes sentence-level embeddings and splits chunks dynamically when consecutive sentence cosine similarity drops below threshold $\tau = 0.75$.</li>
  <li>Verify that child chunks maintain immutable foreign key references to parent chunks.</li>
</ul>"""
        ]
    },

    # ── DAY 139: Vector Indexing Deep Dive ──
    139: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Your vector database cluster is consuming 128GB of RAM hosting 10,000,000 1536-dimensional embeddings. Cloud infrastructure costs must be reduced by 70% while maintaining search latency under 15ms.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement an <strong>Inverted File Index (IVF) with K-Means Centroid Clustering</strong> partitioning the vector space into $C = 16$ Voronoi cells.</li>
  <li>Implement <strong>Scalar Quantization (SQ8)</strong> compressing 32-bit floating-point coordinates into 8-bit unsigned integers with dynamic min/max scale reconstruction.</li>
  <li>Benchmark FlatL2 vs IVF-Flat vs IVF-SQ8 across recall@10 and memory consumption.</li>
</ul>"""
        ]
    },

    # ── DAY 140: GraphRAG & Knowledge Graphs ──
    140: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a GraphRAG knowledge extraction pipeline for an internal corporate wiki. The system must answer macro-level questions such as: <em>"What were the cross-departmental security vulnerabilities identified across all Q2 microservice audits?"</em></p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement an <strong>Entity and Relationship Extractor</strong> extracting structured triples <code>(subject, predicate, object)</code> from unstructured text.</li>
  <li>Implement the <strong>Leiden Community Detection Algorithm</strong> to partition the knowledge graph into densely connected thematic clusters.</li>
  <li>Pre-generate hierarchical community summaries at root and sub-domain levels for Map-Reduce global search synthesis.</li>
</ul>"""
        ]
    },

    # ── DAY 141: Advanced Query Transformations ──
    141: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Users frequently submit vague, brief questions to your corporate helpdesk (e.g. <em>"vpn broke"</em>). Standard vector search fails because the query embedding is distant from the official documentation title (<em>"Troubleshooting GlobalProtect IPSec Tunnel Handshake Timeouts"</em>).</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement <strong>Hypothetical Document Embeddings (HyDE)</strong>: Generate a hypothetical answer with an LLM and embed the generated document to search the vector index.</li>
  <li>Implement <strong>Multi-Query Expansion</strong>: Generate 3 diverse paraphrases and execute parallel searches fused via RRF.</li>
  <li>Implement <strong>Step-Back Prompting</strong>: Extract the foundational underlying computer networking principle for background context retrieval.</li>
</ul>"""
        ]
    },

    # ── DAY 142: Capstone: Production RAG ──
    142: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Deploy an end-to-end production RAG microservice on FastAPI combining all Week 19 technologies under strict performance and reliability SLAs.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Integrate Redis semantic vector caching (&lt;5ms cache hit latency).</li>
  <li>Implement Qdrant hybrid search (HNSW dense + BM25 sparse) with Reciprocal Rank Fusion ($k=60$).</li>
  <li>Add Cross-Encoder candidate reranking and Presidio PII data masking.</li>
  <li>Instrument full OpenTelemetry distributed tracing recording prompt/completion token consumption and p95 latency.</li>
</ul>"""
        ]
    },

    # ── DAY 143: ReAct & Plan-and-Solve ──
    143: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement an autonomous diagnostic IT support agent that troubleshoots production server incidents by querying Prometheus metrics, inspecting Linux system logs, and querying SQL incident databases.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement the full cyclic <strong>ReAct State Machine</strong>: $\text{Thought}_t \to \text{Action}_t \to \text{Observation}_t \to \text{Thought}_{t+1}$.</li>
  <li>Register three deterministic tools: <code>query_prometheus_cpu(node_id)</code>, <code>tail_system_log(service)</code>, and <code>restart_service(service)</code>.</li>
  <li>Enforce strict maximum execution limits (<code>max_steps = 8</code>) and error handling reflection loops.</li>
</ul>"""
        ]
    },

    # ── DAY 144: Structured Output via Instructor ──
    144: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build an automated medical invoice information extraction service that parses unstructured clinical discharge summaries into strictly validated Pydantic models.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Define nested Pydantic models for <code>PatientRecord</code>, <code>DiagnosisCode</code> (ICD-10 enum), and <code>BillingItem</code>.</li>
  <li>Implement Instructor automated self-healing retry loops that catch validation errors and feed error diffs back to the LLM for instant correction.</li>
  <li>Assert 100% type conformance with zero JSON parsing exceptions on edge-case noisy input strings.</li>
</ul>"""
        ]
    },

    # ── DAY 145: LangGraph StateGraph ──
    145: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build an autonomous Python code generator and test-runner agent using LangGraph. The agent must write code, execute tests in a sandbox, and automatically loop back to fix syntax/assertion bugs until all tests pass.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Define a typed <code>AgentState</code> schema with message history, code draft, test output, and iteration counter.</li>
  <li>Construct a <strong>Cyclic StateGraph</strong> with <code>code_generator_node</code>, <code>test_runner_node</code>, and <code>debugger_node</code>.</li>
  <li>Implement conditional edge routing: route to <code>END</code> if tests pass; loop back to <code>debugger_node</code> if tests fail (max 3 retries).</li>
  <li>Configure SQLite state checkpointer for time-travel state rollback.</li>
</ul>"""
        ]
    },

    # ── DAY 146: Multi-Agent Systems ──
    146: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a collaborative Multi-Agent Software Review Team consisting of a Supervisor Agent, a Security Auditor Agent (checking for SQL injection & CVEs), a Performance Optimization Agent (checking Big-O complexity), and a Final Synthesizer Agent.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement a <strong>Hierarchical Supervisor Topology</strong> coordinating domain specialist agents.</li>
  <li>Implement structured inter-agent state message passing with typed Pydantic payloads.</li>
  <li>Execute parallel evaluations and aggregate findings into an executive security and performance audit report.</li>
</ul>"""
        ]
    },

    # ── DAY 147: Vector Memory & Coreference ──
    147: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build a persistent long-term episodic memory system for a personal AI executive assistant that maintains context across multi-week conversational sessions.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Implement <strong>Coreference Resolution</strong>: rewrite ambiguous conversational turns (<em>"Send it to him tomorrow"</em> $\to$ <em>"Send the quarterly audit report to John tomorrow"</em>) prior to vector storage.</li>
  <li>Implement <strong>Exponential Temporal Decay Scoring</strong>: $\text{Score}(m) = \cos(\vec{q}, \vec{v}_m) \times e^{-\lambda \Delta t}$.</li>
  <li>Benchmark retrieval accuracy against raw un-decayed vector search on a 30-day conversational timeline.</li>
</ul>"""
        ]
    },

    # ── DAY 148: Human-in-the-loop (HITL) ──
    148: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Implement a Human-in-the-Loop approval gate inside an automated financial payment agent in LangGraph. Read-only balance checks execute autonomously, but any payment $> \$10,000$ pauses execution and awaits human authorization.</p>
<p>
<strong>Requirements:</strong></p>
<ul>
  <li>Configure LangGraph interrupt breakpoints on high-risk action nodes (<code>execute_wire_transfer</code>).</li>
  <li>Persist state snapshot to a persistent checkpointer and dispatch an approval alert payload.</li>
  <li>Implement the resume endpoint accepting human decisions: <code>APPROVED</code> (resumes execution) or <code>REJECTED</code> (rolls back state cleanly).</li>
</ul>"""
        ]
    },

    # ── DAY 149: Capstone: Multi-Agent System ──
    149: {
        'tasks_prompts': [
            """<p><strong>Scenario:</strong> Build and deploy a production-grade Autonomous Research & Software Engineering Multi-Agent System integrating LangGraph StateGraphs, Pydantic schemas, persistent PostgreSQL checkpointers, and OpenTelemetry distributed tracing.</p>
<p><strong>Requirements:</strong></p>
<ul>
  <li>Construct full multi-agent workflow: Supervisor $\to$ Web Researcher $\to$ Coder $\to$ Critic $\to$ Human Approval $\to$ Deployment.</li>
  <li>Implement tool execution sandboxing in isolated container environments.</li>
  <li>Record distributed traces capturing latency and token costs for every agent hop and tool execution.</li>
</ul>"""
        ]
    }
}
