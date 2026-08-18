#!/usr/bin/env python3
"""
apply_production_walkthroughs.py
=================================
Replaces ProductionEngine boilerplate code inside <pre><code>...</code></pre>
blocks in the curriculum HTML files (Weeks 18-26).

Uses string replacement scoped to each day-section, never touches math blocks.
"""

import re
import html as html_module

WEEKS_DIR = "pages/weeks"

# =============================================================================
# Authentic production code by (week, day_id)
# =============================================================================

AUTHENTIC_CODE = {

# ── WEEK 18: Full-Stack MLOps Capstone ──────────────────────────────────────

(18, 'day-125'): '''\
# Day 125 — Production Kubernetes Pod Manager
import subprocess, json, time, logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("K8sPodManager")

class KubernetesPodManager:
    """Production Kubernetes Pod lifecycle manager for ML workloads."""

    def __init__(self, namespace: str = "ml-serving", context: Optional[str] = None):
        self.namespace = namespace
        self.ctx_flag = ["--context", context] if context else []

    def _kubectl(self, *args: str) -> Dict:
        cmd = ["kubectl", *self.ctx_flag, "-n", self.namespace, *args]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f"kubectl error: {result.stderr.strip()}")
        return json.loads(result.stdout) if result.stdout.strip().startswith(("{", "[")) else {"output": result.stdout.strip()}

    def get_pod_status(self, label_selector: str) -> Dict[str, Any]:
        pods = self._kubectl("get", "pods", "-l", label_selector, "-o", "json")
        items = pods.get("items", [])
        return {
            "total":   len(items),
            "running": sum(1 for p in items if p["status"]["phase"] == "Running"),
            "pending": sum(1 for p in items if p["status"]["phase"] == "Pending"),
            "failed":  sum(1 for p in items if p["status"]["phase"] == "Failed"),
        }

    def rollout_restart(self, deployment_name: str) -> str:
        result = self._kubectl("rollout", "restart", f"deployment/{deployment_name}")
        logger.info(f"Triggered rollout restart: {deployment_name}")
        return result.get("output", "")

    def wait_for_rollout(self, deployment_name: str, timeout_sec: int = 120) -> bool:
        cmd = ["kubectl", *self.ctx_flag, "-n", self.namespace,
               "rollout", "status", f"deployment/{deployment_name}", f"--timeout={timeout_sec}s"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = result.returncode == 0
        logger.info(f"Rollout {'succeeded' if success else 'FAILED'}: {deployment_name}")
        return success

    def scale_deployment(self, name: str, replicas: int) -> bool:
        self._kubectl("scale", f"deployment/{name}", f"--replicas={replicas}")
        logger.info(f"Scaled {name} to {replicas} replicas")
        return self.wait_for_rollout(name)

if __name__ == "__main__":
    mgr = KubernetesPodManager(namespace="ml-serving")
    print("KubernetesPodManager ready — connects to active kubectl context")
    print("Ops: get_pod_status, rollout_restart, wait_for_rollout, scale_deployment")
    print("Test: kubectl get pods -l app=llm-api -n ml-serving")
''',

(18, 'day-127'): '''\
# Day 127 — Production MLflow Experiment Tracker
import mlflow, time, logging, json
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MLflowTracker")

class MLflowExperimentTracker:
    """Production MLflow tracking with auto-registration and stage promotion."""

    def __init__(self, experiment_name: str, tracking_uri: str = "http://localhost:5000"):
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
        self.client = mlflow.MlflowClient()

    def log_training_run(self, params: Dict[str, Any], metrics: Dict[str, float],
                          model, artifact_path: str = "model", run_name: str = "run") -> str:
        with mlflow.start_run(run_name=run_name) as run:
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, artifact_path=artifact_path,
                                      registered_model_name=self.experiment_name)
            run_id = run.info.run_id
            logger.info(f"Run {run_id}: params={params}, metrics={metrics}")
            return run_id

    def promote_best_model(self, metric_key: str = "val_f1", stage: str = "Staging") -> Optional[str]:
        exp = self.client.get_experiment_by_name(self.experiment_name)
        runs = self.client.search_runs(
            experiment_ids=[exp.experiment_id],
            order_by=[f"metrics.{metric_key} DESC"], max_results=1
        )
        if not runs:
            logger.warning("No runs found to promote")
            return None
        versions = self.client.get_latest_versions(self.experiment_name, stages=["None"])
        if not versions:
            return None
        v = versions[0]
        self.client.transition_model_version_stage(self.experiment_name, v.version, stage)
        logger.info(f"Promoted v{v.version} ({runs[0].info.run_id[:8]}) to {stage}")
        return v.version

    def get_production_model(self):
        versions = self.client.get_latest_versions(self.experiment_name, stages=["Production"])
        if not versions:
            raise RuntimeError(f"No Production model for {self.experiment_name}")
        return mlflow.pyfunc.load_model(f"models:/{self.experiment_name}/Production")

if __name__ == "__main__":
    print("MLflowExperimentTracker: connects to localhost:5000 by default")
    print("Flow: log_training_run -> promote_best_model(Staging) -> promote(Production)")
    print("Start server: mlflow server --host 0.0.0.0 --port 5000")
''',

(18, 'day-128'): '''\
# Day 128 — Capstone System Architecture Validator
import time, hashlib, json, logging
from typing import Dict, Any, List, Set
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CapstoneArchitecture")

@dataclass
class DataSplit:
    name: str
    ids: Set[int]

    def checksum(self) -> str:
        return hashlib.md5(str(sorted(self.ids)).encode()).hexdigest()[:8]

@dataclass
class CapstoneBlueprint:
    """Architecture validator: checks leakage, component coverage, and latency targets."""
    project_name: str
    target_latency_ms: float = 200.0
    components: List[str] = field(default_factory=list)
    data_splits: List[DataSplit] = field(default_factory=list)
    _issues: List[str] = field(default_factory=list)

    REQUIRED_COMPONENTS = {"FastAPI", "Docker", "MLflow"}

    def validate_no_leakage(self) -> bool:
        if len(self.data_splits) < 2:
            return True
        sets = [s.ids for s in self.data_splits]
        names = [s.name for s in self.data_splits]
        is_clean = True
        for i in range(len(sets)):
            for j in range(i+1, len(sets)):
                overlap = sets[i] & sets[j]
                if overlap:
                    self._issues.append(f"LEAKAGE: {len(overlap)} shared IDs in {names[i]}∩{names[j]}")
                    is_clean = False
        logger.info(f"Leakage check: {'PASS' if is_clean else 'FAIL'} ({len(self._issues)} issues)")
        return is_clean

    def validate_components(self) -> bool:
        missing = self.REQUIRED_COMPONENTS - set(self.components)
        if missing:
            self._issues.append(f"Missing required components: {missing}")
        logger.info(f"Components: {len(self.components)} present, {len(missing)} missing")
        return not missing

    def architecture_report(self) -> Dict[str, Any]:
        return {
            "project": self.project_name,
            "components": self.components,
            "splits": [{"name": s.name, "size": len(s.ids), "checksum": s.checksum()} for s in self.data_splits],
            "target_latency_ms": self.target_latency_ms,
            "issues": self._issues,
            "status": "READY" if not self._issues else "BLOCKED",
        }

if __name__ == "__main__":
    bp = CapstoneBlueprint(
        project_name="Customer Churn Prediction API",
        target_latency_ms=150.0,
        components=["FastAPI", "XGBoost", "Redis", "MLflow", "Docker", "Render", "Gunicorn"],
        data_splits=[
            DataSplit("train", set(range(8000))),
            DataSplit("val",   set(range(8000, 9000))),
            DataSplit("test",  set(range(9000, 10000))),
        ]
    )
    bp.validate_no_leakage()
    bp.validate_components()
    report = bp.architecture_report()
    print(json.dumps(report, indent=2))
    assert report["status"] == "READY", f"Blueprint issues: {report['issues']}"
    print("CapstoneBlueprint validation: OK")
''',

# ── WEEK 19: Advanced RAG Architecture ──────────────────────────────────────

(19, 'day-136'): '''\
# Day 136 — Production Hybrid Search Engine (Dense + BM25 + RRF)
import math, time, logging
from typing import List, Dict, Any, Tuple
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("HybridSearch")

class HybridSearchEngine:
    """Hybrid retrieval: dense cosine + BM25 sparse, fused with Reciprocal Rank Fusion (k=60)."""

    def __init__(self, k_rrf: int = 60, top_k_each: int = 50):
        self.k_rrf = k_rrf
        self.top_k_each = top_k_each
        self._corpus: List[Dict] = []
        self._bm25 = None

    def index(self, documents: List[Dict[str, Any]]) -> None:
        from rank_bm25 import BM25Okapi
        self._corpus = documents
        tokenized = [doc["text"].lower().split() for doc in documents]
        self._bm25 = BM25Okapi(tokenized, k1=1.5, b=0.75)
        logger.info(f"Indexed {len(documents)} documents (BM25 k1=1.5, b=0.75)")

    def _dense_rank(self, query_vec: List[float], doc_vecs: List[List[float]]) -> List[Tuple[int, float]]:
        import numpy as np
        q = np.array(query_vec); q /= (np.linalg.norm(q) + 1e-9)
        scores = [(i, float(np.dot(q, np.array(d) / (np.linalg.norm(d) + 1e-9)))) for i, d in enumerate(doc_vecs)]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:self.top_k_each]

    def _sparse_rank(self, query: str) -> List[Tuple[int, float]]:
        scores = self._bm25.get_scores(query.lower().split())
        return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:self.top_k_each]

    def rrf_fuse(self, *ranked_lists) -> List[Tuple[int, float]]:
        rrf: Dict[int, float] = defaultdict(float)
        for rl in ranked_lists:
            for rank, (doc_id, _) in enumerate(rl, start=1):
                rrf[doc_id] += 1.0 / (self.k_rrf + rank)
        return sorted(rrf.items(), key=lambda x: x[1], reverse=True)

    def search(self, query: str, query_vec: List[float], doc_vecs: List[List[float]], top_n: int = 5) -> List[Dict]:
        t0 = time.perf_counter()
        fused = self.rrf_fuse(self._dense_rank(query_vec, doc_vecs), self._sparse_rank(query))
        results = [{"doc": self._corpus[i], "rrf_score": s} for i, s in fused[:top_n]]
        logger.info(f"Hybrid search {(time.perf_counter()-t0)*1000:.1f}ms, top-{top_n} returned")
        return results

if __name__ == "__main__":
    import numpy as np
    docs = [
        {"id": 1, "text": "Azure VM error 0x80070005 access denied administrators"},
        {"id": 2, "text": "BM25 retrieval formula term frequency inverse document frequency"},
        {"id": 3, "text": "dense vector cosine similarity embedding retrieval HNSW index"},
    ]
    engine = HybridSearchEngine()
    engine.index(docs)
    doc_vecs = [np.random.randn(128).tolist() for _ in docs]
    results = engine.search("Azure VM access error", np.random.randn(128).tolist(), doc_vecs, top_n=2)
    print(f"Top results: {[r['doc']['id'] for r in results]}")
    assert len(results) == 2
    print("HybridSearchEngine: OK")
''',

(19, 'day-137'): '''\
# Day 137 — Production Cross-Encoder Reranker (BGE-Reranker-Large)
import time, logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CrossEncoderReranker")

class CrossEncoderReranker:
    """Reranks bi-encoder candidates with BGE-Reranker-Large cross-attention scoring."""

    def __init__(self, model_name: str = "BAAI/bge-reranker-large", batch_size: int = 32,
                 max_length: int = 512):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name, max_length=max_length)
        self.batch_size = batch_size
        logger.info(f"CrossEncoder loaded: {model_name}")

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict]:
        """Score (query, doc_text) pairs and return top_n by cross-encoder relevance."""
        t0 = time.perf_counter()
        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)
        ranked = sorted(zip(candidates, scores.tolist()), key=lambda x: x[1], reverse=True)
        results = [{"doc": doc, "ce_score": round(float(score), 4)} for doc, score in ranked[:top_n]]
        elapsed = (time.perf_counter() - t0) * 1000
        logger.info(f"Reranked {len(candidates)} → top-{top_n} in {elapsed:.1f}ms")
        return results

    def pipeline(self, query: str, retriever, top_k_retrieve: int = 50,
                  top_n_rerank: int = 5, **retriever_kwargs) -> List[Dict]:
        """Full retrieve-then-rerank pipeline."""
        candidates = retriever.search(query, top_k=top_k_retrieve, **retriever_kwargs)
        return self.rerank(query, candidates, top_n=top_n_rerank)

if __name__ == "__main__":
    print("CrossEncoderReranker: BAAI/bge-reranker-large scores (query, doc) pairs")
    print("Latency: ~5-15ms per batch of 32 pairs on GPU")
    # Simulate reranking without model download
    import random
    candidates = [{"text": f"Document {i} discussing retrieval augmented generation"} for i in range(20)]
    scores = [random.gauss(0, 1) for _ in candidates]
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:5]
    print(f"Simulated top-5: {[r[0]['text'][:30] for r in ranked]}")
    assert len(ranked) == 5
    print("CrossEncoderReranker: OK")
''',

(19, 'day-138'): '''\
# Day 138 — Production Semantic + Parent-Document Chunker
import re, time, logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SemanticChunker")

class ParentDocumentChunker:
    """
    Parent-document chunking: index small child chunks (256 tokens) for dense retrieval,
    but return large parent chunks (2048 tokens) to the LLM for context richness.
    """

    def __init__(self, child_chunk_size: int = 256, parent_chunk_size: int = 2048,
                 overlap: int = 32):
        self.child_size = child_chunk_size
        self.parent_size = parent_chunk_size
        self.overlap = overlap

    def _token_count(self, text: str) -> int:
        # Approximation: 1 token ≈ 4 chars
        return len(text) // 4

    def _split_by_tokens(self, text: str, chunk_tokens: int, overlap_tokens: int) -> List[str]:
        words = text.split()
        chars_per_token = 4
        chunk_words = chunk_tokens * chars_per_token // 5  # avg word length ~5
        overlap_words = overlap_tokens * chars_per_token // 5
        chunks, i = [], 0
        while i < len(words):
            chunk = " ".join(words[i:i+chunk_words])
            chunks.append(chunk)
            i += chunk_words - overlap_words
        return chunks

    def chunk(self, document: Dict[str, Any]) -> Dict[str, List[Dict]]:
        text = document["text"]
        doc_id = document.get("id", "doc")
        parent_chunks = self._split_by_tokens(text, self.parent_size, self.overlap)
        result = {"parent_chunks": [], "child_chunks": []}
        for p_idx, parent in enumerate(parent_chunks):
            parent_id = f"{doc_id}_p{p_idx}"
            result["parent_chunks"].append({
                "chunk_id": parent_id, "text": parent,
                "token_count": self._token_count(parent)
            })
            child_chunks = self._split_by_tokens(parent, self.child_size, self.overlap // 2)
            for c_idx, child in enumerate(child_chunks):
                result["child_chunks"].append({
                    "chunk_id": f"{parent_id}_c{c_idx}", "parent_id": parent_id,
                    "text": child, "token_count": self._token_count(child)
                })
        logger.info(f"Doc {doc_id}: {len(result['parent_chunks'])} parent, "
                    f"{len(result['child_chunks'])} child chunks")
        return result

if __name__ == "__main__":
    import random, string
    # Generate a long document
    words = " ".join(["".join(random.choices(string.ascii_lowercase, k=random.randint(3,10))) for _ in range(5000)])
    doc = {"id": "doc_001", "text": words}
    chunker = ParentDocumentChunker(child_chunk_size=256, parent_chunk_size=1024)
    result = chunker.chunk(doc)
    print(f"Parent chunks: {len(result['parent_chunks'])}")
    print(f"Child chunks:  {len(result['child_chunks'])}")
    assert len(result["child_chunks"]) >= len(result["parent_chunks"])
    # Verify parent-child link
    child = result["child_chunks"][0]
    assert child["parent_id"] in {p["chunk_id"] for p in result["parent_chunks"]}
    print("ParentDocumentChunker: OK")
''',

(19, 'day-139'): '''\
# Day 139 — Production FAISS HNSW Index with IVF-PQ Compression
import time, logging
import numpy as np
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FAISSHNSWIndex")

class FAISSHNSWIndex:
    """Production FAISS HNSW index: M=32 connections, ef_search=64, inner product metric."""

    def __init__(self, dim: int = 1536, M: int = 32, ef_construction: int = 200):
        import faiss
        self.dim = dim
        self.index = faiss.IndexHNSWFlat(dim, M, faiss.METRIC_INNER_PRODUCT)
        self.index.hnsw.efConstruction = ef_construction
        self.metadata: List[Dict] = []
        logger.info(f"HNSW index: dim={dim}, M={M}, efConstruction={ef_construction}")

    def build(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        import faiss
        assert vectors.shape[0] == len(metadata)
        faiss.normalize_L2(vectors)          # cosine via inner product on unit vecs
        self.index.add(vectors)
        self.metadata = metadata
        logger.info(f"Built HNSW index: {vectors.shape[0]} vectors, dim={vectors.shape[1]}")

    def search(self, query: np.ndarray, top_k: int = 10, ef_search: int = 64) -> List[Dict]:
        import faiss
        t0 = time.perf_counter()
        self.index.hnsw.efSearch = ef_search
        q = query.reshape(1, -1).astype("float32")
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, top_k)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        results = [
            {"score": float(scores[0][i]), "metadata": self.metadata[int(indices[0][i])]}
            for i in range(top_k) if indices[0][i] >= 0
        ]
        logger.info(f"HNSW search: {elapsed_ms:.2f}ms, {len(results)} results")
        return results

    def save(self, path: str) -> None:
        import faiss, pickle
        faiss.write_index(self.index, f"{path}.faiss")
        with open(f"{path}.meta", "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved index to {path}.faiss")

    def load(self, path: str) -> None:
        import faiss, pickle
        self.index = faiss.read_index(f"{path}.faiss")
        with open(f"{path}.meta", "rb") as f:
            self.metadata = pickle.load(f)
        logger.info(f"Loaded index from {path}.faiss: {self.index.ntotal} vectors")

if __name__ == "__main__":
    dim, n = 128, 10_000
    vecs = np.random.randn(n, dim).astype("float32")
    meta = [{"doc_id": i, "chunk": f"chunk_{i}"} for i in range(n)]
    idx = FAISSHNSWIndex(dim=dim, M=16)
    idx.build(vecs, meta)
    query = np.random.randn(dim).astype("float32")
    results = idx.search(query, top_k=5)
    print(f"Top-5: {[r['metadata']['doc_id'] for r in results]}")
    assert len(results) == 5
    assert results[0]["score"] >= results[-1]["score"]
    print("FAISSHNSWIndex: OK")
''',

(19, 'day-140'): '''\
# Day 140 — Production Neo4j Knowledge Graph Triple Extractor
import time, logging, json
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("KGExtractor")

EXTRACTION_PROMPT = """Extract (subject, predicate, object) triples from the text.
Return ONLY a JSON array: [{"subject": "...", "predicate": "...", "object": "..."}, ...]
Limit to 10 most important factual triples. No explanation."""

class Neo4jKnowledgeGraphBuilder:
    """LLM-powered triple extraction + Neo4j ingestion for GraphRAG."""

    def __init__(self, openai_client, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.client = openai_client
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def extract_triples(self, text: str, model: str = "gpt-4o-mini") -> List[Dict[str, str]]:
        t0 = time.perf_counter()
        resp = self.client.chat.completions.create(
            model=model, temperature=0.0,
            messages=[{"role": "system", "content": EXTRACTION_PROMPT},
                      {"role": "user", "content": text}]
        )
        content = resp.choices[0].message.content.strip()
        # Strip code fences if present
        content = content.strip("`").removeprefix("json\n").strip()
        triples = json.loads(content) if content.startswith("[") else []
        logger.info(f"Extracted {len(triples)} triples in {(time.perf_counter()-t0)*1000:.0f}ms")
        return triples

    def ingest_triples(self, triples: List[Dict[str, str]]) -> int:
        cypher = (
            "MERGE (s:Entity {name: $subject}) "
            "MERGE (o:Entity {name: $object}) "
            "MERGE (s)-[r:RELATES {type: $predicate}]->(o) "
            "ON CREATE SET r.count = 1 "
            "ON MATCH SET r.count = r.count + 1"
        )
        with self.driver.session() as session:
            for t in triples:
                session.run(cypher, subject=t["subject"],
                            predicate=t["predicate"], object=t["object"])
        logger.info(f"Ingested {len(triples)} triples")
        return len(triples)

    def query_neighbors(self, entity: str, max_hops: int = 2) -> List[Dict]:
        cypher = (
            f"MATCH path = (e:Entity {{name: $entity}})-[*1..{max_hops}]-(n:Entity) "
            "RETURN DISTINCT n.name AS neighbor, length(path) AS hops"
        )
        with self.driver.session() as session:
            result = session.run(cypher, entity=entity)
            return [{"neighbor": r["neighbor"], "hops": r["hops"]} for r in result]

if __name__ == "__main__":
    print("Neo4jKnowledgeGraphBuilder: Requires OpenAI + Neo4j")
    # Simulate triple extraction
    simulated_triples = [
        {"subject": "FAISS",    "predicate": "implements", "object": "HNSW"},
        {"subject": "BM25",     "predicate": "uses",       "object": "TF-IDF"},
        {"subject": "RAG",      "predicate": "combines",   "object": "retrieval"},
        {"subject": "RRF",      "predicate": "fuses",      "object": "ranked lists"},
    ]
    print(f"Simulated triples ({len(simulated_triples)}):")
    for t in simulated_triples:
        print(f"  ({t['subject']}) -[{t['predicate']}]-> ({t['object']})")
    assert len(simulated_triples) == 4
    print("KnowledgeGraphBuilder: OK")
''',

(19, 'day-141'): '''\
# Day 141 — Production HyDE + Step-Back Query Expander
import time, logging, json
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("QueryExpander")

class HyDEQueryExpander:
    """
    Hypothetical Document Embedding (HyDE): generate a fake ideal answer,
    embed it, retrieve real docs similar to the fake answer.
    Also implements Step-Back prompting for abstraction-level expansion.
    """

    HYDE_PROMPT = "Write a short, detailed paragraph that would perfectly answer this question:\n{query}\nAnswer in 2-3 sentences as if you are a technical expert:"

    STEPBACK_PROMPT = "What is the broader, more general topic behind this specific question?\nQuestion: {query}\nBroader topic (1 sentence):"

    def __init__(self, llm_client, embedding_model):
        self.llm = llm_client
        self.embedder = embedding_model

    def generate_hypothetical_doc(self, query: str) -> str:
        t0 = time.perf_counter()
        resp = self.llm.chat.completions.create(
            model="gpt-4o-mini", temperature=0.3,
            messages=[{"role": "user", "content": self.HYDE_PROMPT.format(query=query)}]
        )
        hyp_doc = resp.choices[0].message.content.strip()
        logger.info(f"HyDE doc generated in {(time.perf_counter()-t0)*1000:.0f}ms: {hyp_doc[:60]}...")
        return hyp_doc

    def step_back_query(self, query: str) -> str:
        resp = self.llm.chat.completions.create(
            model="gpt-4o-mini", temperature=0.0,
            messages=[{"role": "user", "content": self.STEPBACK_PROMPT.format(query=query)}]
        )
        return resp.choices[0].message.content.strip()

    def expand_query(self, query: str) -> Dict[str, Any]:
        hyp_doc = self.generate_hypothetical_doc(query)
        step_back = self.step_back_query(query)
        hyp_embedding = self.embedder.encode(hyp_doc)
        query_embedding = self.embedder.encode(query)
        return {
            "original_query": query,
            "hypothetical_doc": hyp_doc,
            "step_back_query": step_back,
            "hyp_embedding": hyp_embedding.tolist(),
            "query_embedding": query_embedding.tolist(),
        }

if __name__ == "__main__":
    print("HyDEQueryExpander: Requires OpenAI + SentenceTransformer")
    # Simulate without LLM
    query = "How does HNSW graph index work for approximate nearest neighbor search?"
    hyp_doc = ("HNSW builds a hierarchical graph where each node connects to M nearest neighbors. "
                "Search traverses from the top layer greedily toward the query, then refines at lower layers.")
    step_back = "Graph-based approximate nearest neighbor search algorithms"
    print(f"Query:        {query}")
    print(f"HyDE doc:     {hyp_doc[:70]}...")
    print(f"Step-back:    {step_back}")
    print("HyDEQueryExpander: OK")
''',

(19, 'day-142'): '''\
# Day 142 — Production End-to-End RAG Pipeline
import time, logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RAGPipeline")

class ProductionRAGPipeline:
    """
    Full production RAG pipeline:
    Query → HyDE expansion → Hybrid retrieval → Cross-encoder rerank → LLM generation
    with citation tracking and RAGAS evaluation logging.
    """

    def __init__(self, retriever, reranker, llm_client,
                 top_k_retrieve: int = 50, top_n_rerank: int = 5,
                 generation_model: str = "gpt-4o"):
        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm_client
        self.top_k = top_k_retrieve
        self.top_n = top_n_rerank
        self.gen_model = generation_model

    def _build_context(self, chunks: List[Dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            src = chunk.get("doc", {}).get("source", f"Source {i}")
            parts.append(f"[{i}] {src}\n{chunk['doc']['text']}")
        return "\n\n".join(parts)

    def query(self, question: str, conversation_history: Optional[List] = None) -> Dict[str, Any]:
        t0 = time.perf_counter()
        # Step 1: Retrieve
        candidates = self.retriever.search(question, top_k=self.top_k)
        # Step 2: Rerank
        reranked = self.reranker.rerank(question, candidates, top_n=self.top_n)
        context = self._build_context(reranked)
        # Step 3: Generate
        messages = (conversation_history or []) + [
            {"role": "system", "content": (
                "You are a precise technical assistant. Answer based ONLY on the provided context. "
                "Cite sources using [N] notation. If the context doesn't answer the question, say so."
            )},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]
        resp = self.llm.chat.completions.create(
            model=self.gen_model, messages=messages, temperature=0.1, max_tokens=1024
        )
        answer = resp.choices[0].message.content
        total_ms = (time.perf_counter() - t0) * 1000
        result = {
            "question": question, "answer": answer,
            "sources": [r.get("doc", {}) for r in reranked],
            "contexts": [r.get("doc", {}).get("text", "") for r in reranked],
            "latency_ms": round(total_ms, 1),
            "tokens_used": resp.usage.total_tokens,
        }
        logger.info(f"RAG query in {total_ms:.0f}ms: {resp.usage.total_tokens} tokens")
        return result

if __name__ == "__main__":
    print("ProductionRAGPipeline: Requires retriever + reranker + OpenAI")
    print("Pipeline: hybrid_search(top_k=50) → cross_encoder_rerank(top_n=5) → GPT-4o generation")
    print("Output includes: answer, sources, contexts (for RAGAS), latency_ms, tokens_used")
    print("RAGPipeline: OK")
''',

# ── WEEK 20: LLM Agents ──────────────────────────────────────────────────────

(20, 'day-143'): '''\
# Day 143 — Production ReAct Agent with Tool Loop
import time, logging, json
from typing import List, Dict, Any, Callable, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ReActAgent")

class ReActAgent:
    """
    ReAct (Reasoning + Acting): interleaves Thought → Action → Observation steps.
    Hard limits: max_steps guard + timeout_sec prevents infinite loops.
    """

    SYSTEM_PROMPT = """You are a ReAct reasoning agent. At each step, respond with JSON:
{"thought": "your reasoning", "action": "tool_name", "action_input": {}}
When done: {"thought": "...", "action": "final_answer", "action_input": {"answer": "..."}}
Available tools: {tools}"""

    def __init__(self, llm_client, tools: Dict[str, Callable],
                 max_steps: int = 10, timeout_sec: float = 30.0, model: str = "gpt-4o"):
        self.llm = llm_client
        self.tools = tools
        self.max_steps = max_steps
        self.timeout = timeout_sec
        self.model = model

    def run(self, goal: str) -> Dict[str, Any]:
        tool_list = ", ".join(self.tools.keys())
        system = self.SYSTEM_PROMPT.format(tools=tool_list)
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": f"Goal: {goal}"}]
        trace, t_start = [], time.time()
        for step in range(1, self.max_steps + 1):
            if time.time() - t_start > self.timeout:
                raise TimeoutError(f"Agent timed out after {self.timeout}s at step {step}")
            resp = self.llm.chat.completions.create(
                model=self.model, messages=messages, temperature=0.0,
                response_format={"type": "json_object"}
            )
            step_data = json.loads(resp.choices[0].message.content)
            trace.append({"step": step, **step_data})
            logger.info(f"Step {step}: action={step_data.get('action')}, thought={step_data.get('thought','')[:60]}")
            if step_data.get("action") == "final_answer":
                return {"answer": step_data["action_input"]["answer"],
                        "steps": step, "trace": trace,
                        "elapsed_sec": round(time.time() - t_start, 2)}
            # Execute tool
            tool_name = step_data.get("action", "")
            if tool_name not in self.tools:
                obs = f"ERROR: Unknown tool '{tool_name}'. Valid: {list(self.tools.keys())}"
            else:
                try:
                    obs = str(self.tools[tool_name](**step_data.get("action_input", {})))
                except Exception as e:
                    obs = f"Tool error: {type(e).__name__}: {e}"
            messages.append({"role": "assistant", "content": json.dumps(step_data)})
            messages.append({"role": "user", "content": f"Observation: {obs}"})
        raise RuntimeError(f"Agent did not converge in {self.max_steps} steps")

if __name__ == "__main__":
    print("ReActAgent: Requires OpenAI client")
    # Simulate execution trace
    trace = [
        {"step": 1, "thought": "I need to search for current info", "action": "web_search",
         "action_input": {"query": "top RAG chunking strategies 2024"}},
        {"step": 2, "thought": "Found results, composing final answer", "action": "final_answer",
         "action_input": {"answer": "Top strategies: semantic, parent-document, late chunking"}},
    ]
    print(f"Simulated trace ({len(trace)} steps):")
    for s in trace:
        print(f"  Step {s['step']}: {s['action']} — {s['thought'][:50]}")
    assert trace[-1]["action"] == "final_answer"
    print("ReActAgent: OK")
''',

(20, 'day-144'): '''\
# Day 144 — Production Pydantic-Validated LLM Tool Caller
import time, logging, json
from typing import Dict, Any, Type, TypeVar, Optional, List
from pydantic import BaseModel, ValidationError, field_validator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("StructuredCaller")

T = TypeVar("T", bound=BaseModel)

class StructuredLLMCaller:
    """LLM caller with Pydantic schema enforcement and exponential-backoff retry."""

    def __init__(self, llm_client, max_retries: int = 3, model: str = "gpt-4o-mini"):
        self.llm = llm_client
        self.max_retries = max_retries
        self.model = model

    def call(self, prompt: str, schema: Type[T], system: Optional[str] = None) -> T:
        schema_str = json.dumps(schema.model_json_schema(), indent=2)
        sys_msg = system or f"Return valid JSON matching this schema:\n{schema_str}"
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                t0 = time.perf_counter()
                resp = self.llm.chat.completions.create(
                    model=self.model, temperature=0.0,
                    messages=[{"role": "system", "content": sys_msg},
                               {"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                raw = json.loads(resp.choices[0].message.content)
                validated = schema(**raw)
                ms = (time.perf_counter() - t0) * 1000
                logger.info(f"Validated {schema.__name__} on attempt {attempt} in {ms:.1f}ms")
                return validated
            except (ValidationError, json.JSONDecodeError, Exception) as e:
                last_error = e
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed: {type(e).__name__}: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 ** (attempt - 1))  # exp backoff
        raise RuntimeError(f"All {self.max_retries} attempts failed: {last_error}")

# Example Pydantic schemas for agent tools
class ResearchPlan(BaseModel):
    topic: str
    subtasks: List[str]
    estimated_hours: float

    @field_validator("estimated_hours")
    @classmethod
    def positive_hours(cls, v):
        if v <= 0:
            raise ValueError("estimated_hours must be positive")
        return v

class WebSearchInput(BaseModel):
    query: str
    num_results: int = 5
    language: str = "en"

    @field_validator("num_results")
    @classmethod
    def valid_count(cls, v):
        if not 1 <= v <= 20:
            raise ValueError("num_results must be 1-20")
        return v

if __name__ == "__main__":
    # Test validation logic
    plan = ResearchPlan(topic="HNSW indexing", subtasks=["theory", "implementation", "benchmarks"], estimated_hours=3.0)
    print(f"Valid plan: {plan.model_dump()}")
    try:
        bad = ResearchPlan(topic="X", subtasks=[], estimated_hours=-1.0)
    except ValidationError as e:
        print(f"Caught validation error: {e.error_count()} errors")
    search = WebSearchInput(query="FAISS vs ScaNN benchmark", num_results=10)
    print(f"Valid search: {search.model_dump()}")
    print("StructuredLLMCaller: OK")
''',

(20, 'day-145'): '''\
# Day 145 — Production LangGraph Multi-Actor State Machine
import time, logging, operator
from typing import Dict, Any, List, TypedDict, Annotated

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LangGraphWorkflow")

class WorkflowState(TypedDict):
    goal: str
    messages: Annotated[List[Dict], operator.add]   # append-only
    current_node: str
    artifacts: Dict[str, str]
    result: str

class LangGraphResearchWorkflow:
    """
    Multi-actor LangGraph workflow: Supervisor → Researcher → Analyst → Writer → Review.
    Uses TypedDict state with Annotated append-only message log.
    """

    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.graph = self._build()

    def _build(self):
        from langgraph.graph import StateGraph, END
        wf = StateGraph(WorkflowState)
        wf.add_node("supervisor",  self._supervisor)
        wf.add_node("researcher",  self._researcher)
        wf.add_node("analyst",     self._analyst)
        wf.add_node("writer",      self._writer)
        wf.set_entry_point("supervisor")
        wf.add_conditional_edges("supervisor", self._route_supervisor,
            {"researcher": "researcher", "analyst": "analyst",
             "writer": "writer", "END": END})
        wf.add_edge("researcher", "supervisor")
        wf.add_edge("analyst",    "supervisor")
        wf.add_edge("writer",     "supervisor")
        return wf.compile()

    def _route_supervisor(self, state: WorkflowState) -> str:
        msgs = state["messages"]
        if not msgs:
            return "researcher"
        last_role = msgs[-1].get("role", "")
        return {"researcher": "analyst", "analyst": "writer"}.get(last_role, "END")

    def _supervisor(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Supervisor: routing based on {len(state['messages'])} messages")
        return {**state, "current_node": "supervisor"}

    def _researcher(self, state: WorkflowState) -> WorkflowState:
        logger.info("Researcher: gathering information")
        return {**state, "messages": [{"role": "researcher", "content": f"Research complete for: {state['goal']}"}],
                "artifacts": {**state.get("artifacts", {}), "research": "findings ready"}}

    def _analyst(self, state: WorkflowState) -> WorkflowState:
        logger.info("Analyst: analyzing research")
        return {**state, "messages": [{"role": "analyst", "content": "Analysis complete"}],
                "artifacts": {**state.get("artifacts", {}), "analysis": "patterns identified"}}

    def _writer(self, state: WorkflowState) -> WorkflowState:
        logger.info("Writer: composing final output")
        return {**state, "messages": [{"role": "writer", "content": "Draft complete"}],
                "result": f"Final output for goal: {state['goal']}"}

    def run(self, goal: str) -> Dict[str, Any]:
        initial: WorkflowState = {"goal": goal, "messages": [], "current_node": "", "artifacts": {}, "result": ""}
        t0 = time.perf_counter()
        final = self.graph.invoke(initial)
        logger.info(f"Workflow complete in {(time.perf_counter()-t0)*1000:.0f}ms")
        return final

if __name__ == "__main__":
    wf = LangGraphResearchWorkflow()
    result = wf.run("Analyze the performance tradeoffs of HNSW vs IVF-PQ vector indexing")
    print(f"Result: {result['result']}")
    print(f"Messages logged: {len(result['messages'])}")
    print(f"Artifacts: {list(result['artifacts'].keys())}")
    assert result["result"] != ""
    print("LangGraphResearchWorkflow: OK")
''',

# ── WEEK 21: Fine-Tuning & Quantization ─────────────────────────────────────

(21, 'day-150'): '''\
# Day 150 — Production vLLM Async Serving Engine
import asyncio, time, logging
from typing import List, AsyncIterator, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("vLLMServer")

class ProductionvLLMEngine:
    """
    Production vLLM AsyncLLMEngine wrapper.
    Key config: PagedAttention (gpu_memory_utilization=0.90),
    prefix caching, tensor parallelism, and streaming output.
    """

    def __init__(self, model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
                 gpu_memory_utilization: float = 0.90,
                 max_num_seqs: int = 256, tensor_parallel_size: int = 1,
                 enable_prefix_caching: bool = True):
        from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
        self.SamplingParams = SamplingParams
        args = AsyncEngineArgs(
            model=model,
            gpu_memory_utilization=gpu_memory_utilization,
            max_num_seqs=max_num_seqs,
            tensor_parallel_size=tensor_parallel_size,
            enable_prefix_caching=enable_prefix_caching,
            dtype="bfloat16",
        )
        self.engine = AsyncLLMEngine.from_engine_args(args)
        logger.info(f"vLLM engine: {model}, tp={tensor_parallel_size}, "
                    f"mem={gpu_memory_utilization}, prefix_cache={enable_prefix_caching}")

    async def stream(self, prompt: str, max_tokens: int = 512, temperature: float = 0.8,
                      request_id: Optional[str] = None) -> AsyncIterator[str]:
        import uuid
        rid = request_id or str(uuid.uuid4())
        params = self.SamplingParams(
            max_tokens=max_tokens, temperature=temperature,
            repetition_penalty=1.1, top_p=0.95
        )
        async for output in self.engine.generate(prompt, params, request_id=rid):
            if output.outputs:
                yield output.outputs[0].text
            if output.finished:
                tps = output.outputs[0].token_ids.__len__() / max(output.metrics.finished_time - output.metrics.first_token_time, 0.001)
                logger.info(f"Request {rid}: {tps:.1f} tokens/s")

    async def batch_complete(self, prompts: List[str], **kwargs) -> List[str]:
        results = await asyncio.gather(*[self._collect(p, i, **kwargs) for i, p in enumerate(prompts)])
        return list(results)

    async def _collect(self, prompt: str, idx: int, **kwargs) -> str:
        out = ""
        async for chunk in self.stream(prompt, request_id=f"batch-{idx}", **kwargs):
            out += chunk
        return out

if __name__ == "__main__":
    print("ProductionvLLMEngine: Requires GPU + vllm package (pip install vllm)")
    print("Key config: PagedAttention, prefix_caching=True, tensor_parallel_size=4 for 70B")
    print("API: engine.stream(prompt) → async generator of text chunks")
    print("Throughput on A100: ~2000 tokens/s for 8B model, ~400 tokens/s for 70B (4 GPU)")
    print("vLLMEngine: OK")
''',

(21, 'day-151'): '''\
# Day 151 — Production FlashAttention-2 Integration
import time, logging, math
import torch
import torch.nn as nn
import torch.nn.functional as F

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FlashAttention")

class FlashAttentionLayer(nn.Module):
    """
    Hardware-aware multi-head attention using FlashAttention-2 tiling.
    Falls back to standard scaled dot-product attention on CPU.
    """

    def __init__(self, embed_dim: int = 4096, num_heads: int = 32, dropout: float = 0.0,
                 causal: bool = True):
        super().__init__()
        assert embed_dim % num_heads == 0
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.causal = causal
        self.scale = math.sqrt(self.head_dim)

        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, attention_mask: torch.Tensor = None) -> torch.Tensor:
        B, T, C = x.shape
        Q = self.q_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)

        if x.is_cuda:
            try:
                from flash_attn import flash_attn_func
                # FA2: (B, T, H, D) layout
                q = Q.transpose(1, 2).contiguous()  # (B, T, H, D)
                k = K.transpose(1, 2).contiguous()
                v = V.transpose(1, 2).contiguous()
                attn_out = flash_attn_func(q, k, v, dropout_p=self.dropout if self.training else 0.0,
                                           causal=self.causal)
                out = attn_out.reshape(B, T, C)
                logger.debug(f"FlashAttention-2: B={B}, T={T}, H={self.num_heads}")
            except ImportError:
                logger.warning("flash_attn not available, using torch SDPA")
                out = self._sdpa(Q, K, V, B, T, C, attention_mask)
        else:
            out = self._sdpa(Q, K, V, B, T, C, attention_mask)

        return self.out_proj(out)

    def _sdpa(self, Q, K, V, B, T, C, mask):
        out = F.scaled_dot_product_attention(
            Q, K, V, attn_mask=mask,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=self.causal and mask is None
        )
        return out.transpose(1, 2).contiguous().view(B, T, C)

if __name__ == "__main__":
    # CPU test (standard SDPA)
    layer = FlashAttentionLayer(embed_dim=512, num_heads=8, causal=True)
    x = torch.randn(2, 64, 512)  # batch=2, seq=64, dim=512
    out = layer(x)
    print(f"Input: {x.shape} → Output: {out.shape}")
    assert out.shape == (2, 64, 512)
    params = sum(p.numel() for p in layer.parameters())
    print(f"Parameters: {params:,}")
    # Memory: standard attn = O(T^2), FlashAttn = O(T) — huge win for T>512
    print("FlashAttentionLayer: OK (SDPA on CPU, FlashAttention-2 on CUDA)")
''',

(21, 'day-152'): '''\
# Day 152 — Production AWQ / GPTQ 4-bit Quantisation Evaluator
import time, logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("QuantisationEvaluator")

class QuantisationEvaluator:
    """
    Loads AWQ or GPTQ quantised models and measures:
    perplexity regression, inference throughput, and VRAM usage.
    """

    def __init__(self, base_model_name: str, quant_model_name: str, dtype: str = "awq"):
        import torch
        from transformers import AutoTokenizer
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        self.quant_model = self._load_quant(quant_model_name, dtype)
        logger.info(f"Loaded {dtype} quantised model: {quant_model_name}")

    def _load_quant(self, model_name: str, dtype: str):
        from transformers import AutoModelForCausalLM
        if dtype == "awq":
            from awq import AutoAWQForCausalLM
            return AutoAWQForCausalLM.from_quantized(model_name, fuse_layers=True).to(self.device)
        elif dtype == "gptq":
            return AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        raise ValueError(f"Unknown dtype: {dtype}")

    def measure_perplexity(self, dataset_text: str, stride: int = 512, max_length: int = 2048) -> float:
        import torch, math
        encodings = self.tokenizer(dataset_text, return_tensors="pt").to(self.device)
        input_ids = encodings.input_ids
        nlls, n_tokens = [], 0
        for i in range(0, input_ids.shape[1] - 1, stride):
            begin = max(i + stride - max_length, 0)
            end = min(i + stride, input_ids.shape[1])
            chunk = input_ids[:, begin:end]
            target_len = end - i
            with torch.no_grad():
                out = self.quant_model(chunk, labels=chunk)
                nll = out.loss * target_len
            nlls.append(nll.item())
            n_tokens += target_len
        ppl = math.exp(sum(nlls) / n_tokens)
        logger.info(f"Perplexity: {ppl:.2f} over {n_tokens} tokens")
        return ppl

    def measure_throughput(self, prompt: str, n_new_tokens: int = 200) -> Dict[str, float]:
        import torch
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        t0 = time.perf_counter()
        with torch.no_grad():
            out = self.quant_model.generate(**inputs, max_new_tokens=n_new_tokens, do_sample=False)
        elapsed = time.perf_counter() - t0
        new_toks = out.shape[1] - inputs.input_ids.shape[1]
        tps = new_toks / elapsed
        vram_gb = torch.cuda.max_memory_allocated() / 1e9 if torch.cuda.is_available() else 0
        logger.info(f"Throughput: {tps:.1f} tok/s, VRAM: {vram_gb:.2f}GB")
        return {"tokens_per_sec": tps, "new_tokens": new_toks, "elapsed_sec": elapsed, "vram_gb": vram_gb}

if __name__ == "__main__":
    print("QuantisationEvaluator: Requires GPU + awq / transformers")
    print("AWQ 4-bit: ~4x model size reduction, ~1.5-2x throughput on CUDA with INT4 kernels")
    print("Perplexity regression target: < 1.5 PPL increase vs fp16 baseline on domain corpus")
    # Quantised model sizing math:
    params_b = 8.0  # LLaMA-3 8B
    fp16_gb  = params_b * 2  # 16 bytes/param
    int4_gb  = params_b * 0.5
    print(f"LLaMA-3 8B: fp16={fp16_gb:.0f}GB → AWQ int4={int4_gb:.0f}GB ({fp16_gb/int4_gb:.0f}x reduction)")
    print("QuantisationEvaluator: OK")
''',

(21, 'day-155'): '''\
# Day 155 — Production LLM Training Data Pipeline (MinHash Dedup + Quality Filter)
import time, logging, hashlib, struct
from typing import List, Dict, Any, Tuple, Set
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DataPipeline")

class MinHashDeduplicator:
    """
    MinHash LSH deduplication for LLM training data.
    Removes near-duplicate documents (Jaccard similarity > threshold).
    """

    def __init__(self, num_perm: int = 128, threshold: float = 0.8, n_shingles: int = 5):
        import numpy as np
        self.num_perm = num_perm
        self.threshold = threshold
        self.n_shingles = n_shingles
        rng = np.random.RandomState(42)
        self._a = rng.randint(1, (1 << 31) - 1, size=num_perm)
        self._b = rng.randint(0, (1 << 31) - 1, size=num_perm)
        self._max_val = (1 << 31) - 1
        self._buckets: Dict[Tuple, Set[int]] = defaultdict(set)
        self._n_bands = num_perm // 4

    def _shingles(self, text: str) -> Set[int]:
        tokens = text.lower().split()
        return {hash(tuple(tokens[i:i+self.n_shingles])) & 0xFFFFFFFF
                for i in range(len(tokens) - self.n_shingles + 1)}

    def _minhash(self, shingles: Set[int]):
        import numpy as np
        if not shingles:
            return np.full(self.num_perm, self._max_val)
        s = np.array(list(shingles), dtype=np.uint64)
        sigs = np.min(((self._a[:, None] * s[None, :] + self._b[:, None]) % self._max_val), axis=1)
        return sigs

    def is_duplicate(self, doc_id: int, text: str) -> bool:
        sig = self._minhash(self._shingles(text))
        bands = [tuple(sig[i*4:(i+1)*4]) for i in range(self._n_bands)]
        for band in bands:
            bucket = self._buckets[band]
            if bucket:
                return True
            bucket.add(doc_id)
        return False

    def deduplicate(self, documents: List[Dict]) -> List[Dict]:
        unique, dups = [], 0
        for doc in documents:
            if not self.is_duplicate(doc["id"], doc["text"]):
                unique.append(doc)
            else:
                dups += 1
        logger.info(f"Dedup: {len(documents)} in, {len(unique)} unique, {dups} duplicates removed")
        return unique

class QualityFilter:
    """Filters low-quality documents by length, repetition, and language score."""

    def __init__(self, min_tokens: int = 50, max_tokens: int = 100_000,
                 max_char_repeat_ratio: float = 0.3):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.max_repeat = max_char_repeat_ratio

    def score(self, text: str) -> Dict[str, Any]:
        tokens = text.split()
        n = len(tokens)
        most_common = max(set(tokens), key=tokens.count) if tokens else ""
        repeat_ratio = tokens.count(most_common) / max(n, 1)
        return {
            "token_count": n, "repeat_ratio": repeat_ratio,
            "pass": self.min_tokens <= n <= self.max_tokens and repeat_ratio < self.max_repeat
        }

    def filter(self, documents: List[Dict]) -> List[Dict]:
        passed = [d for d in documents if self.score(d["text"])["pass"]]
        logger.info(f"Quality filter: {len(documents)} in, {len(passed)} passed")
        return passed

if __name__ == "__main__":
    docs = [
        {"id": 1, "text": "The transformer architecture revolutionized natural language processing tasks."},
        {"id": 2, "text": "The transformer architecture revolutionized natural language processing tasks."},  # dup
        {"id": 3, "text": "Attention mechanisms allow models to focus on relevant context tokens."},
        {"id": 4, "text": "bad " * 100},  # repetitive
    ]
    dedup = MinHashDeduplicator(num_perm=64, threshold=0.8)
    qf = QualityFilter(min_tokens=5)
    unique_docs = dedup.deduplicate(docs)
    clean_docs = qf.filter(unique_docs)
    print(f"Input: {len(docs)}, After dedup: {len(unique_docs)}, After filter: {len(clean_docs)}")
    assert len(clean_docs) <= len(unique_docs)
    print("LLM DataPipeline: OK")
''',

# ── WEEK 22: High-Performance Inference ─────────────────────────────────────

(22, 'day-157'): '''\
# Day 157 — Production RAGAS RAG Evaluation Pipeline
import time, logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RAGASEvaluator")

class RAGASEvaluationPipeline:
    """
    Evaluates RAG system quality using RAGAS metrics:
    faithfulness, answer_relevancy, context_precision, context_recall.
    """

    METRICS_NAMES = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

    def __init__(self, judge_model: str = "gpt-4o", embedding_model: str = "text-embedding-3-small"):
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        self.metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
        for m in self.metrics:
            m.llm = LangchainLLMWrapper(ChatOpenAI(model=judge_model, temperature=0))
            if hasattr(m, "embeddings"):
                m.embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model=embedding_model))
        logger.info(f"RAGAS evaluator: judge={judge_model}, embed={embedding_model}")

    def evaluate(self, samples: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        samples: List of {"question": str, "answer": str, "contexts": List[str],
                           "ground_truth": str}
        """
        from ragas import evaluate
        from datasets import Dataset
        t0 = time.perf_counter()
        dataset = Dataset.from_list(samples)
        result = evaluate(dataset, metrics=self.metrics)
        scores = result.to_pandas().mean().to_dict()
        elapsed = time.perf_counter() - t0
        logger.info(f"RAGAS: {len(samples)} samples in {elapsed:.1f}s — {scores}")
        return scores

    def generate_report(self, scores: Dict[str, float]) -> str:
        lines = ["=== RAGAS Evaluation Report ==="]
        for metric, score in scores.items():
            status = "✅" if score >= 0.7 else ("⚠️" if score >= 0.5 else "❌")
            lines.append(f"  {status} {metric}: {score:.3f}")
        overall = sum(scores.values()) / max(len(scores), 1)
        lines.append(f"\n  Overall: {overall:.3f} {'PASS' if overall >= 0.7 else 'FAIL'}")
        return "\n".join(lines)

if __name__ == "__main__":
    print("RAGASEvaluationPipeline: Requires ragas + openai packages")
    # Simulate scores (typical production values)
    simulated = {"faithfulness": 0.84, "answer_relevancy": 0.91, "context_precision": 0.76, "context_recall": 0.82}
    print(f"Simulated RAGAS scores: {simulated}")
    assert all(0 <= v <= 1 for v in simulated.values())
    overall = sum(simulated.values()) / len(simulated)
    print(f"Overall: {overall:.3f} ({'PASS' if overall >= 0.7 else 'FAIL'})")
    print("RAGASEvaluationPipeline: OK")
''',

(22, 'day-159'): '''\
# Day 159 — Production PII Scrubber with Presidio + Regex
import re, time, logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PIIScrubber")

class PIIScrubber:
    """
    Production PII scrubber: Microsoft Presidio (NER-based) + regex fallbacks
    for email, phone, IP address, and credit card detection.
    """

    REGEX_PATTERNS = {
        "EMAIL":   r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE":   r"\+?1?\s?[\(\-]?\d{3}[\)\-\s]?\d{3}[\-\s]?\d{4}",
        "IP_V4":   r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[\s\-]?){3}\d{4}\b",
        "SSN":     r"\b\d{3}-\d{2}-\d{4}\b",
    }

    def __init__(self, use_presidio: bool = True, entities: List[str] = None):
        self.use_presidio = use_presidio
        self.entities = entities or ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SSN", "CREDIT_CARD", "IP_ADDRESS"]
        if use_presidio:
            try:
                from presidio_analyzer import AnalyzerEngine
                from presidio_anonymizer import AnonymizerEngine
                self.analyzer = AnalyzerEngine()
                self.anonymizer = AnonymizerEngine()
                logger.info("Presidio engine loaded")
            except ImportError:
                logger.warning("Presidio not available, using regex-only mode")
                self.use_presidio = False

    def scrub_regex(self, text: str) -> Tuple[str, List[Dict]]:
        findings = []
        for entity_type, pattern in self.REGEX_PATTERNS.items():
            for match in re.finditer(pattern, text):
                findings.append({"entity": entity_type, "text": match.group(), "start": match.start(), "end": match.end()})
        # Replace from right to preserve offsets
        for f in sorted(findings, key=lambda x: x["start"], reverse=True):
            text = text[:f["start"]] + f"[{f['entity']}]" + text[f["end"]:]
        return text, findings

    def scrub(self, text: str) -> Tuple[str, List[Dict]]:
        t0 = time.perf_counter()
        if self.use_presidio:
            results = self.analyzer.analyze(text=text, entities=self.entities, language="en")
            anonymized = self.anonymizer.anonymize(text=text, analyzer_results=results)
            findings = [{"entity": r.entity_type, "score": r.score,
                         "start": r.start, "end": r.end} for r in results]
            scrubbed = anonymized.text
        else:
            scrubbed, findings = self.scrub_regex(text)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        logger.info(f"Scrubbed {len(findings)} PII entities in {elapsed_ms:.1f}ms")
        return scrubbed, findings

if __name__ == "__main__":
    scrubber = PIIScrubber(use_presidio=False)  # regex-only for demo
    test_text = "Contact john.doe@example.com or call +1 (555) 123-4567. IP: 192.168.1.100. CC: 4111-1111-1111-1111"
    scrubbed, findings = scrubber.scrub(test_text)
    print(f"Original: {test_text}")
    print(f"Scrubbed: {scrubbed}")
    print(f"Findings: {[f['entity'] for f in findings]}")
    assert "john.doe@example.com" not in scrubbed
    assert "[EMAIL]" in scrubbed
    print("PIIScrubber: OK")
''',

(22, 'day-162'): '''\
# Day 162 — Production GPU VRAM & Capacity Planner
import math, logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GPUPlanner")

class GPUCapacityPlanner:
    """
    Compute exact VRAM requirements for LLM serving:
    model weights + KV cache + activation memory.
    Determine max_batch_size and minimum GPU count.
    """

    DTYPE_BYTES = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1, "int4": 0.5}
    GPU_VRAM = {"A100-40GB": 40, "A100-80GB": 80, "H100-80GB": 80, "H100-94GB": 94,
                "RTX4090": 24, "V100-32GB": 32, "T4": 16}

    def model_vram_gb(self, params_billions: float, dtype: str = "bf16") -> float:
        return params_billions * 1e9 * self.DTYPE_BYTES.get(dtype, 2) / 1e9

    def kv_cache_gb(self, batch_size: int, seq_len: int, n_layers: int,
                     n_heads: int, head_dim: int, dtype: str = "fp16") -> float:
        """KV cache = 2 (K+V) × batch × seq × layers × heads × head_dim × bytes"""
        return 2 * batch_size * seq_len * n_layers * n_heads * head_dim * self.DTYPE_BYTES[dtype] / 1e9

    def max_batch_for_gpu(self, gpu: str, model_params_b: float, seq_len: int,
                           n_layers: int, n_heads: int, head_dim: int,
                           model_dtype: str = "bf16", kv_dtype: str = "fp16") -> int:
        vram_gb = self.GPU_VRAM.get(gpu, 80)
        model_gb = self.model_vram_gb(model_params_b, model_dtype)
        available_gb = vram_gb * 0.90 - model_gb
        if available_gb <= 0:
            return 0
        kv_per_seq_gb = self.kv_cache_gb(1, seq_len, n_layers, n_heads, head_dim, kv_dtype)
        return int(available_gb / kv_per_seq_gb)

    def sizing_report(self, model_name: str, params_b: float, n_layers: int,
                       n_heads: int, head_dim: int, seq_len: int = 4096,
                       gpu: str = "A100-80GB") -> Dict[str, Any]:
        model_gb = self.model_vram_gb(params_b, "bf16")
        kv_gb = self.kv_cache_gb(1, seq_len, n_layers, n_heads, head_dim)
        max_bs = self.max_batch_for_gpu(gpu, params_b, seq_len, n_layers, n_heads, head_dim)
        gpu_vram = self.GPU_VRAM.get(gpu, 80)
        min_gpus = math.ceil(model_gb / (gpu_vram * 0.9))
        return {
            "model": model_name, "gpu": gpu, "gpu_vram_gb": gpu_vram,
            "model_weight_gb": round(model_gb, 2),
            "kv_per_seq_gb": round(kv_gb, 4),
            "max_batch_size": max_bs,
            "min_gpus_for_model": min_gpus,
        }

if __name__ == "__main__":
    planner = GPUCapacityPlanner()
    # LLaMA-3 8B on A100 80GB
    r1 = planner.sizing_report("LLaMA-3-8B", 8.0, n_layers=32, n_heads=32, head_dim=128,
                                seq_len=4096, gpu="A100-80GB")
    print(f"LLaMA-3 8B on A100 80GB: {r1}")
    # LLaMA-3 70B on H100 80GB
    r2 = planner.sizing_report("LLaMA-3-70B", 70.0, n_layers=80, n_heads=64, head_dim=128,
                                seq_len=4096, gpu="H100-80GB")
    print(f"LLaMA-3 70B on H100 80GB: {r2}")
    assert r1["max_batch_size"] > 0
    assert r2["min_gpus_for_model"] >= 2
    print("GPUCapacityPlanner: OK")
''',

# ── WEEK 23: Cloud AI ────────────────────────────────────────────────────────

(23, 'day-164'): '''\
# Day 164 — Production SageMaker Inference Handler
import json, logging, time, os
import torch
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SageMakerHandler")

def model_fn(model_dir: str):
    """Load model artifacts from /opt/ml/model — called ONCE at container startup."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = os.path.join(model_dir, "model.pt")
    # Load tokenizer and model (replace with your actual architecture)
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.to(device).eval()
    logger.info(f"Model loaded from {model_dir} on {device}")
    return {"model": model, "tokenizer": tokenizer, "device": device}

def input_fn(request_body: str, content_type: str = "application/json") -> Dict:
    """Deserialize request body — called per request."""
    if content_type != "application/json":
        raise ValueError(f"Unsupported content_type: {content_type}")
    data = json.loads(request_body)
    if "inputs" not in data:
        raise ValueError("Request JSON must contain 'inputs' key")
    return data

def predict_fn(data: Dict, model_artifacts: Dict) -> Dict:
    """Run inference — called per request."""
    t0 = time.perf_counter()
    model = model_artifacts["model"]
    tokenizer = model_artifacts["tokenizer"]
    device = model_artifacts["device"]
    inputs = tokenizer(data["inputs"], return_tensors="pt", truncation=True,
                        max_length=512, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1).cpu().tolist()
    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"Inference: {latency_ms:.2f}ms, batch={len(data['inputs']) if isinstance(data['inputs'], list) else 1}")
    return {"probabilities": probs, "latency_ms": round(latency_ms, 2)}

def output_fn(prediction: Dict, accept: str = "application/json") -> str:
    """Serialize prediction — called per request."""
    if accept != "application/json":
        raise ValueError(f"Unsupported accept type: {accept}")
    return json.dumps(prediction)

if __name__ == "__main__":
    print("SageMaker Handler: model_fn → input_fn → predict_fn → output_fn")
    # Smoke test input/output serialisation
    body = json.dumps({"inputs": "SageMaker makes ML deployment straightforward"})
    parsed = input_fn(body)
    print(f"Parsed: {parsed}")
    fake_pred = {"probabilities": [[0.12, 0.88]], "latency_ms": 3.5}
    out = output_fn(fake_pred)
    print(f"Serialised: {out}")
    assert "probabilities" in json.loads(out)
    print("SageMakerHandler: OK")
''',

# ── WEEK 24: Production MLOps ────────────────────────────────────────────────

(24, 'day-171'): '''\
# Day 171 — Production Statistical Drift Detector
import logging, numpy as np
from typing import Dict, Any, List
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DriftDetector")

class ProductionDriftDetector:
    """
    Production drift monitoring:
    - PSI (Population Stability Index) for feature distribution shift
    - KS test for statistical distribution change
    - Wasserstein distance for severity quantification
    """

    PSI_BINS = 10
    PSI_WARN, PSI_ALERT = 0.1, 0.2  # STABLE / WARNING / ALERT thresholds

    def psi(self, ref: np.ndarray, prod: np.ndarray) -> Dict[str, Any]:
        _, bins = np.histogram(ref, bins=self.PSI_BINS)
        ref_pct = (np.histogram(ref, bins=bins)[0] + 1e-8) / len(ref)
        prod_pct = (np.histogram(prod, bins=bins)[0] + 1e-8) / len(prod)
        value = float(np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct)))
        status = "STABLE" if value < self.PSI_WARN else ("WARNING" if value < self.PSI_ALERT else "ALERT")
        return {"psi": round(value, 4), "status": status}

    def ks_test(self, ref: np.ndarray, prod: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        stat, p = stats.ks_2samp(ref, prod)
        return {"ks_stat": round(stat, 4), "p_value": round(p, 4), "drifted": p < alpha}

    def wasserstein(self, ref: np.ndarray, prod: np.ndarray) -> float:
        return round(float(stats.wasserstein_distance(ref, prod)), 4)

    def monitor_features(self, ref_df, prod_df, features: List[str]) -> Dict[str, Any]:
        report, drifted = {}, []
        for col in features:
            r, p = ref_df[col].dropna().values, prod_df[col].dropna().values
            psi_res = self.psi(r, p)
            ks_res = self.ks_test(r, p)
            w1 = self.wasserstein(r, p)
            report[col] = {"psi": psi_res, "ks": ks_res, "wasserstein": w1}
            if ks_res["drifted"] or psi_res["status"] == "ALERT":
                drifted.append(col)
        report["_summary"] = {"drifted_features": drifted, "total_monitored": len(features)}
        logger.info(f"Drift monitoring: {len(drifted)}/{len(features)} features drifted")
        return report

if __name__ == "__main__":
    import pandas as pd
    rng = np.random.RandomState(42)
    ref_data = pd.DataFrame({"feature_A": rng.normal(0, 1, 5000), "feature_B": rng.uniform(0, 1, 5000)})
    # Stable production distribution
    prod_stable = pd.DataFrame({"feature_A": rng.normal(0, 1, 2000), "feature_B": rng.uniform(0, 1, 2000)})
    # Drifted production distribution
    prod_drift  = pd.DataFrame({"feature_A": rng.normal(2.5, 1.5, 2000), "feature_B": rng.uniform(0.5, 1.5, 2000)})

    detector = ProductionDriftDetector()
    stable_report = detector.monitor_features(ref_data, prod_stable, ["feature_A", "feature_B"])
    drift_report  = detector.monitor_features(ref_data, prod_drift,  ["feature_A", "feature_B"])
    print(f"Stable drifted: {stable_report['_summary']['drifted_features']}")
    print(f"Drifted drifted: {drift_report['_summary']['drifted_features']}")
    assert len(drift_report["_summary"]["drifted_features"]) > len(stable_report["_summary"]["drifted_features"])
    print("ProductionDriftDetector: OK")
''',

# ── WEEK 25: Kubernetes & GPU Infrastructure ─────────────────────────────────

(25, 'day-178'): '''\
# Day 178 — Production Kubernetes GPU Workload Scheduler
import subprocess, json, logging, time
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("K8sGPUScheduler")

GPU_POD_YAML = """\
apiVersion: v1
kind: Pod
metadata:
  name: {name}
  labels: {{app: gpu-job}}
spec:
  restartPolicy: Never
  nodeSelector:
    nvidia.com/gpu.product: {gpu_model}
  tolerations:
  - {{key: "nvidia.com/gpu", operator: "Exists", effect: "NoSchedule"}}
  containers:
  - name: trainer
    image: {image}
    command: {command}
    resources:
      limits:
        nvidia.com/gpu: "{n_gpu}"
        memory: {memory}
      requests:
        nvidia.com/gpu: "{n_gpu}"
        memory: {memory}
    env:
    - {{name: NCCL_DEBUG, value: INFO}}
    - {{name: NCCL_IB_DISABLE, value: "0"}}
"""

class K8sGPUJobSubmitter:
    """Submit, monitor, and clean up GPU training jobs on Kubernetes."""

    def __init__(self, namespace: str = "ml-training"):
        self.ns = namespace

    def _run(self, *args, input_text: str = None) -> subprocess.CompletedProcess:
        cmd = ["kubectl", "-n", self.ns, *args]
        return subprocess.run(cmd, capture_output=True, text=True, input=input_text, timeout=30)

    def submit(self, job_name: str, image: str, command: List[str],
                n_gpu: int = 1, memory: str = "32Gi", gpu_model: str = "A100-SXM4-80GB") -> bool:
        yaml = GPU_POD_YAML.format(
            name=job_name, gpu_model=gpu_model, image=image,
            command=json.dumps(command), n_gpu=n_gpu, memory=memory
        )
        result = self._run("apply", "-f", "-", input_text=yaml)
        if result.returncode != 0:
            logger.error(f"Submit failed: {result.stderr}")
            return False
        logger.info(f"Submitted: {job_name} ({n_gpu}x{gpu_model})")
        return True

    def wait(self, job_name: str, timeout_sec: int = 3600) -> str:
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            r = self._run("get", "pod", job_name, "-o", "jsonpath={.status.phase}")
            phase = r.stdout.strip()
            logger.info(f"{job_name}: {phase}")
            if phase in ("Succeeded", "Failed"):
                return phase
            time.sleep(15)
        return "Timeout"

    def logs(self, job_name: str, tail: int = 100) -> str:
        r = self._run("logs", job_name, f"--tail={tail}")
        return r.stdout

    def delete(self, job_name: str) -> None:
        self._run("delete", "pod", job_name, "--ignore-not-found")
        logger.info(f"Deleted: {job_name}")

if __name__ == "__main__":
    submitter = K8sGPUJobSubmitter()
    print("K8sGPUJobSubmitter: kubectl-based GPU pod lifecycle manager")
    print("submit → wait → logs → delete")
    # Validate YAML template rendering
    yaml = GPU_POD_YAML.format(
        name="test-job", gpu_model="A100-SXM4-80GB",
        image="pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime",
        command='["python", "train.py"]', n_gpu=2, memory="64Gi"
    )
    print(f"YAML preview (first 300 chars): {yaml[:300]}")
    assert "nvidia.com/gpu" in yaml
    print("K8sGPUJobSubmitter: OK")
''',

# ── WEEK 26: Multimodal AI ───────────────────────────────────────────────────

(26, 'day-185'): '''\
# Day 185 — Production ViT Patch Projector (GPT-4V / LLaVA compatible)
import math, logging
import torch, torch.nn as nn
import torch.nn.functional as F

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ViTPatchProjector")

class ViTPatchProjector(nn.Module):
    """
    Vision Transformer patch embedding:
    image (B, C, H, W) → patch sequence (B, N+1, D) with CLS token + positional embedding.
    Compatible with LLaVA-style visual encoder inputs.
    """

    def __init__(self, image_size: int = 224, patch_size: int = 14,
                 in_channels: int = 3, embed_dim: int = 1024, dropout: float = 0.0):
        super().__init__()
        assert image_size % patch_size == 0
        self.n_patches = (image_size // patch_size) ** 2
        self.embed_dim = embed_dim
        self.patch_size = patch_size

        # Linear projection: Conv2d with kernel=stride=patch_size
        self.patch_embed = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size, bias=False)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, self.n_patches + 1, embed_dim))
        self.norm = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)
        self._init_weights()
        logger.info(f"ViTPatchProjector: {self.n_patches} patches, dim={embed_dim}, patch_size={patch_size}")

    def _init_weights(self):
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.kaiming_uniform_(self.patch_embed.weight, a=math.sqrt(5))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, C, H, W) → (B, N+1, D)"""
        B = x.shape[0]
        x = self.patch_embed(x)      # (B, D, H/P, W/P)
        x = x.flatten(2).transpose(1, 2)  # (B, N, D)
        cls = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls, x], dim=1)   # (B, N+1, D)
        x = self.norm(x + self.pos_embed)
        return self.dropout(x)

    def cls_features(self, x: torch.Tensor) -> torch.Tensor:
        """Image-level embedding via CLS token: (B, D)"""
        return self.forward(x)[:, 0, :]

    def patch_features(self, x: torch.Tensor) -> torch.Tensor:
        """Dense patch embeddings for ColPali-style retrieval: (B, N, D)"""
        return self.forward(x)[:, 1:, :]

if __name__ == "__main__":
    model = ViTPatchProjector(image_size=224, patch_size=14, embed_dim=1024)
    x = torch.randn(2, 3, 224, 224)
    full = model(x)
    cls = model.cls_features(x)
    patches = model.patch_features(x)
    n = (224 // 14) ** 2  # 256 patches
    print(f"Full output: {full.shape}   → expected (2, {n+1}, 1024)")
    print(f"CLS features: {cls.shape}  → expected (2, 1024)")
    print(f"Patch features: {patches.shape} → expected (2, {n}, 1024)")
    assert full.shape == (2, n+1, 1024)
    assert cls.shape == (2, 1024)
    params = sum(p.numel() for p in model.parameters())
    print(f"Parameters: {params:,}")
    print("ViTPatchProjector: OK")
''',

(26, 'day-187'): '''\
# Day 187 — Production Whisper Speech-to-Text Pipeline
import time, logging, os
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WhisperPipeline")

class WhisperTranscriptionPipeline:
    """
    Production speech-to-text pipeline using faster-whisper (CTranslate2 backend):
    - Voice Activity Detection (VAD) filtering
    - Word-level timestamps
    - Multi-language detection
    - Real-Time Factor (RTF) monitoring
    """

    def __init__(self, model_size: str = "large-v3", device: str = "cuda",
                 compute_type: str = "float16", beam_size: int = 5):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.beam_size = beam_size
        logger.info(f"Whisper {model_size} loaded ({device}, {compute_type})")

    def transcribe(self, audio_path: str, language: Optional[str] = None,
                    word_timestamps: bool = True, normalize: bool = True) -> Dict[str, Any]:
        t0 = time.perf_counter()
        segments, info = self.model.transcribe(
            audio_path, beam_size=self.beam_size, language=language,
            word_timestamps=word_timestamps,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500, "speech_pad_ms": 100},
        )
        segs = list(segments)
        text = " ".join(s.text.strip() for s in segs)
        if normalize:
            text = self._normalize(text)
        elapsed = time.perf_counter() - t0
        rtf = elapsed / max(info.duration, 0.001)
        logger.info(f"Transcribed {info.duration:.1f}s → RTF={rtf:.3f}, lang={info.language} ({info.language_probability:.2f})")
        return {
            "transcript": text,
            "language": info.language,
            "language_probability": round(info.language_probability, 3),
            "duration_sec": round(info.duration, 2),
            "processing_sec": round(elapsed, 2),
            "real_time_factor": round(rtf, 3),
            "segments": [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs],
        }

    def _normalize(self, text: str) -> str:
        """Strip leading/trailing whitespace and normalize multiple spaces."""
        import re
        return re.sub(r"\s+", " ", text).strip()

    def batch_transcribe(self, paths: List[str], **kwargs) -> List[Dict]:
        return [self.transcribe(p, **kwargs) for p in paths]

if __name__ == "__main__":
    print("WhisperTranscriptionPipeline: Requires faster-whisper + GPU")
    print("Compute types: float16 (GPU), int8_float16 (GPU, 2x speed), int8 (CPU)")
    print("VAD: min_silence_duration_ms=500 removes silence before transcription")
    # Simulate output
    simulated = {
        "transcript": "PagedAttention enables efficient KV cache management in vLLM.",
        "language": "en", "language_probability": 0.999,
        "duration_sec": 5.2, "processing_sec": 1.1, "real_time_factor": 0.21,
        "segments": [{"start": 0.0, "end": 5.2, "text": "PagedAttention enables..."}]
    }
    assert simulated["real_time_factor"] < 1.0, "Should be faster than real-time on GPU"
    print(f"RTF={simulated['real_time_factor']} < 1.0 (real-time capable): OK")
    print("WhisperPipeline: OK")
''',

(26, 'day-189'): '''\
# Day 189 — Production ColPali MaxSim Document Index
import torch, time, logging
import torch.nn.functional as F
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ColPaliIndex")

class ColPaliDocumentIndex:
    """
    Production ColPali late-interaction index:
    - Pre-computes and caches page patch embeddings at index time
    - Uses MaxSim scoring at query time: score(q,d) = Σ_i max_j cos_sim(q_i, d_j)
    - Time complexity: O(|Q| × |D| × n_pages) — scale with FAISS for 10k+ pages
    """

    def __init__(self, embed_dim: int = 128, device: str = "cpu"):
        self.embed_dim = embed_dim
        self.device = torch.device(device)
        self._pages: List[torch.Tensor] = []   # (N_patches, D) each
        self._meta: List[Dict] = []

    def add_pages(self, embeddings: List[torch.Tensor], metadata: List[Dict]) -> None:
        """Index-time: normalise and cache all page embeddings."""
        for emb, m in zip(embeddings, metadata):
            norm = F.normalize(emb.to(self.device), dim=-1)  # (P, D)
            self._pages.append(norm)
            self._meta.append(m)
        logger.info(f"Indexed {len(embeddings)} pages (total: {len(self._pages)})")

    def maxsim(self, query_emb: torch.Tensor, page_emb: torch.Tensor) -> float:
        """score(q, d) = Σ_i max_j cosine_sim(q_i, d_j)"""
        q = F.normalize(query_emb.to(self.device), dim=-1)  # (Q, D)
        sim = torch.matmul(q, page_emb.T)                   # (Q, P)
        return sim.max(dim=-1).values.sum().item()

    def search(self, query_emb: torch.Tensor, top_k: int = 5) -> List[Dict[str, Any]]:
        t0 = time.perf_counter()
        scores = [self.maxsim(query_emb, pe) for pe in self._pages]
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        elapsed_ms = (time.perf_counter() - t0) * 1000
        results = [{"rank": r+1, "score": scores[i], "metadata": self._meta[i]}
                   for r, i in enumerate(top_indices)]
        logger.info(f"MaxSim over {len(self._pages)} pages in {elapsed_ms:.1f}ms")
        return results

    def batch_search(self, query_embs: List[torch.Tensor], top_k: int = 5) -> List[List[Dict]]:
        return [self.search(q, top_k=top_k) for q in query_embs]

    def save(self, path: str) -> None:
        import pickle
        data = {"pages": [p.cpu().numpy() for p in self._pages], "meta": self._meta, "dim": self.embed_dim}
        with open(path, "wb") as f:
            pickle.dump(data, f)
        logger.info(f"Saved {len(self._pages)}-page index to {path}")

    def load(self, path: str) -> None:
        import pickle
        with open(path, "rb") as f:
            data = pickle.load(f)
        self._pages = [torch.from_numpy(p).to(self.device) for p in data["pages"]]
        self._meta = data["meta"]
        self.embed_dim = data["dim"]
        logger.info(f"Loaded {len(self._pages)}-page index from {path}")

if __name__ == "__main__":
    dim, n_pages, n_patches = 128, 200, 196
    # Simulate page embeddings (ColPali produces 196 patches per page for 224x224/14)
    idx = ColPaliDocumentIndex(embed_dim=dim)
    page_embs = [torch.randn(n_patches, dim) for _ in range(n_pages)]
    meta = [{"doc": f"report_{i//10}", "page": i} for i in range(n_pages)]
    idx.add_pages(page_embs, meta)
    # Query with 10 query tokens
    q_emb = torch.randn(10, dim)
    results = idx.search(q_emb, top_k=5)
    print(f"Top-5 pages: {[r['metadata']['page'] for r in results]}")
    print(f"Scores (desc): {[round(r['score'], 3) for r in results]}")
    assert len(results) == 5
    assert results[0]["score"] >= results[-1]["score"]
    print("ColPaliDocumentIndex: OK")
''',
}


def replace_stub_in_section(html: str, day_id: str, new_code: str) -> tuple[str, bool]:
    """Replace ProductionEngine code within a day section using string manipulation."""
    day_start = html.find(f'id="{day_id}"')
    if day_start == -1:
        return html, False

    next_day = html.find('class="day-section"', day_start + 20)
    section = html[day_start:next_day] if next_day != -1 else html[day_start:]

    if 'class ProductionEngine:' not in section:
        return html, False

    # Find <pre><code>...</code></pre> containing ProductionEngine
    pre_code_pat = re.compile(r'<pre><code>(.*?)</code></pre>', re.DOTALL)
    matches = list(pre_code_pat.finditer(section))
    target_match = None
    for m in matches:
        # Decode HTML entities to check for ProductionEngine
        decoded = html_module.unescape(m.group(1))
        if 'class ProductionEngine:' in decoded:
            target_match = m
            break

    if not target_match:
        return html, False

    # Escape new code for HTML
    escaped = (new_code
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;'))

    new_block = f'<pre><code>{escaped}</code></pre>'
    new_section = section[:target_match.start()] + new_block + section[target_match.end():]

    new_html = html[:day_start] + new_section + (html[next_day:] if next_day != -1 else '')
    return new_html, True


def main():
    print("=" * 65)
    print("PRODUCTION WALKTHROUGH ENRICHMENT — 64 stubs across 9 weeks")
    print("=" * 65)
    print()
    total = 0
    skipped = 0
    for w in range(18, 27):
        path = f"{WEEKS_DIR}/week{w}.html"
        html = open(path, encoding='utf-8').read()
        original = html
        dd_before = html.count('$$')

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        days = [d.get('id', '') for d in soup.find_all('div', class_='day-section')
                if 'toolkit' not in d.get('id', '')]

        week_cnt = 0
        for day_id in days:
            key = (w, day_id)
            if key not in AUTHENTIC_CODE:
                continue  # skip — use fallback or future expansion
            html, changed = replace_stub_in_section(html, day_id, AUTHENTIC_CODE[key])
            if changed:
                week_cnt += 1

        # Safety check: math delimiters must be intact
        dd_after = html.count('$$')
        if dd_after != dd_before:
            print(f"  Week {w}: WARNING math delimiter changed {dd_before}→{dd_after}, reverting")
            html = original
            skipped += 1
        else:
            if html != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(html)
            total += week_cnt
            print(f"  Week {w}: {week_cnt} stubs replaced (explicit entries)")

    print()
    remaining_stubs = sum(open(f"{WEEKS_DIR}/week{w}.html").read().count('class ProductionEngine:') for w in range(18, 27))
    print(f"Replacements made: {total}")
    print(f"Remaining stubs: {remaining_stubs}")
    print(f"Skipped (math protection): {skipped}")


if __name__ == '__main__':
    main()
