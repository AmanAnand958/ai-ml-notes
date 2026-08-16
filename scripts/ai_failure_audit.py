#!/usr/bin/env python3
"""
AI-Generated Content Failure Audit
Detects critical and high-severity failures across all week HTML files.
Focus: weeks 19-26 (weeks 1-18 mostly correct).
"""

import re
import os
import json
from collections import defaultdict
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")
OUTPUT_FILE = Path("/Users/amananand/Downloads/SDE/ai:ml-1/scripts/ai_audit_report.json")

# ─── DETECTION PATTERNS ───────────────────────────────────────────────────────

# 🔴 CRITICAL: Security anti-patterns in code blocks
SECURITY_PATTERNS = [
    (r'verify\s*=\s*False',               "SSL verification disabled (MITM risk)"),
    (r'password\s*=\s*["\'][^"\']{2,}["\']', "Hardcoded password in code"),
    (r'api_key\s*=\s*["\']sk-[a-zA-Z0-9]{10,}', "Hardcoded real API key"),
    (r'pickle\.loads\(.*user',            "pickle.loads on user input (RCE risk)"),
    (r'f["\'].*SELECT.*\{',               "SQL injection via f-string"),
    (r'f["\'].*DELETE.*\{',               "SQL injection via f-string"),
    (r'subprocess\..*shell\s*=\s*True',   "shell=True subprocess (command injection)"),
    (r'eval\s*\([^)]*input',              "eval() on user input"),
    (r'chmod\s+777',                      "chmod 777 (world-writable permissions)"),
    (r'os\.system\s*\([^)]*\+',          "os.system with string concatenation"),
]

# 🔴 CRITICAL: Deprecated/wrong API patterns
DEPRECATED_PATTERNS = [
    (r'pinecone\.init\s*\(',              "Deprecated pinecone.init() - use Pinecone(api_key=...)"),
    (r'from langchain\.chat_models import', "Deprecated langchain import path (pre-0.2)"),
    (r'from langchain\.embeddings import', "Deprecated langchain embeddings import"),
    (r'from langchain\.vectorstores import', "Deprecated langchain vectorstores import"),
    (r'from langchain import\s+(?!hub)',  "Old-style langchain monolith import"),
    (r'ChatOpenAI\([^)]*openai_api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded key in ChatOpenAI constructor"),
    (r'openai\.ChatCompletion\.create',   "Deprecated openai v0.x API (use client.chat.completions.create)"),
    (r'openai\.Completion\.create',       "Deprecated openai v0.x completion API"),
    (r'\.predict\s*\(',                   "Potentially deprecated .predict() LangChain method"),
    (r'index\.query\s*\([^)]*queries\s*=', "Old Pinecone .query(queries=) signature"),
    (r'weaviate\.Client\(',               "Old Weaviate v3 client (use weaviate.connect_to_*)"),
    (r'chromadb\.Client\(',               "Old ChromaDB Client() - use chromadb.PersistentClient()"),
]

# 🟠 HIGH: Hallucinated/suspicious paper citations
HALLUCINATED_CITATIONS = [
    (r'Chen et al\.\s+202[0-9]',         "Unverified 'Chen et al.' citation - verify DOI"),
    (r'arXiv:\d{4}\.\d{4,5}',            "arXiv citation - verify paper actually exists"),
    (r'Brown et al\.\s+2020',            "GPT-3 paper (verify claim matches actual paper)"),
    (r'according to.*paper',             "Cited claim - verify against source"),
    (r'\d{1,2}[xX×]\s+(?:faster|better|more efficient)', "Performance multiplier claim - needs citation"),
    (r'\d{2,3}\.?\d?%\s+(?:accuracy|improvement|reduction)', "Specific % claim - verify source"),
]

# 🟠 HIGH: Wrong/conflated technical vocabulary
VOCABULARY_ERRORS = [
    (r'fine.?tun\w+ (?:is same as|equals|=) (?:RLHF|instruction)', "Fine-tuning conflated with RLHF/instruction tuning"),
    (r'embedding[s]? (?:is|are) (?:same as|identical to) encoding', "Embedding conflated with encoding"),
    (r'parameter[s]?\s+(?:like|such as)\s+learning.rate', "Hyperparameter called 'parameter'"),
    (r'inference\s+(?:during\s+)?training',                "Inference/training vocabulary mix"),
    (r'overfitting\s+(?:is|means)\s+(?:low|poor)\s+accuracy', "Overfitting mis-defined"),
    (r'transformer\s+(?:was\s+)?invented\s+(?:by\s+)?(?:Google|OpenAI)\s+in\s+201[89]', "Wrong transformer attribution year"),
    (r'BERT\s+(?:introduced|invented)\s+(?:attention|transformer)', "BERT didn't introduce attention (Vaswani 2017)"),
    (r'GPT.4\s+has\s+\d+\s*(?:trillion|billion)\s+parameters', "Hallucinated GPT-4 parameter count"),
]

# 🟠 HIGH: Sycophantic/filler content
FILLER_PATTERNS = [
    (r'[Gg]reat\s+question',             "Sycophantic filler: Great question"),
    (r'[Tt]ruly\s+(?:revolutionary|fascinating|groundbreaking|remarkable)', "Hyperbolic filler"),
    (r'[Aa]s\s+we\s+can\s+see\s+from\s+the\s+(?:above|diagram|table)', "Redundant filler phrase"),
    (r'[Bb]eautifully\s+illustrates',    "Sycophantic filler"),
    (r'[Tt]his\s+is\s+(?:a\s+)?(?:truly|really)\s+(?:exciting|amazing|fascinating)', "Filler enthusiasm"),
    (r'[Ll]et.s\s+dive\s+(?:deep\s+)?into',  "Generic lets-dive-into opener"),
    (r'[Ii]n\s+(?:today.s|this)\s+(?:lesson|session|tutorial),\s+we\s+will', "Template opener filler"),
]

# 🟠 HIGH: Missing production caveats (code blocks with sharp edges)
MISSING_CAVEAT_PATTERNS = [
    (r'torch\.load\([^)]+\)',             "torch.load without weights_only=True (arbitrary code exec risk)"),
    (r'\.from_pretrained\([^)]+\)',       "Model loaded without device_map - may OOM on small GPUs"),
    (r'upsert\([^)]+\)',                  "Vector DB upsert without idempotency note"),
    (r'delete_collection\(',             "Destructive operation - no warning comment present"),
    (r'truncation\s*=\s*False',          "tokenizer without truncation - silent failure on long inputs"),
    (r'max_length\s*=\s*(?:None|none)',  "max_length=None can cause OOM on long sequences"),
]

# 🟡 MEDIUM: Circular/tautological definitions
TAUTOLOGICAL_PATTERNS = [
    (r'attention\s+(?:helps\s+)?(?:the\s+model\s+)?(?:pay\s+)?attention', "Circular attention definition"),
    (r'embedding\s+(?:that\s+)?embeds\s+',  "Circular embedding definition"),
    (r'(?:represents?|captures?)\s+(?:the\s+)?(?:semantic\s+)?meaning\s+(?:of\s+)?(?:the\s+)?(?:word|token)',
     "Vague semantic meaning definition - explain HOW"),
    (r'HNSW\s+(?:is\s+)?(?:fast\s+)?because\s+(?:it\s+)?(?:uses?\s+)?hierarchical',
     "Circular HNSW explanation"),
]

# 🟡 MEDIUM: Stale model/tool references
STALE_REFERENCES = [
    (r'GPT-3\.5\s+(?:is\s+)?(?:the\s+)?(?:most|best|latest|state.of.the.art)',
     "GPT-3.5 described as current best - outdated"),
    (r'Llama\s+2\s+(?:is\s+)?(?:the\s+)?(?:best|most capable|leading)\s+open.source',
     "Llama 2 as best open-source - Llama 3 exists"),
    (r'\$0\.00[12]\s+per\s+1[Kk]\s+token',  "Outdated OpenAI pricing"),
    (r'mistral.7b\s+(?:is\s+)?(?:the\s+)?best\s+open',  "Mistral 7B as best open-source - outdated"),
    (r'GPT-4\s+(?:is\s+)?(?:the\s+)?(?:most|best|latest)',  "GPT-4 as current best - o1/o3/Gemini exist"),
]

# ─── DUPLICATE DETECTION ──────────────────────────────────────────────────────

def extract_quiz_questions(html):
    """Extract quiz question text for cross-week duplicate detection."""
    questions = re.findall(r'class="quiz-q"[^>]*>\s*([^<]{20,})', html)
    return [q.strip() for q in questions]

def extract_flashcard_fronts(html):
    """Extract flashcard front text."""
    fronts = re.findall(r'class="fc-front"[^>]*>.*?<p>([^<]{15,})</p>', html, re.DOTALL)
    return [f.strip() for f in fronts]

def extract_code_blocks(html):
    """Extract code block content (first 200 chars) for near-duplicate detection."""
    blocks = re.findall(r'<code[^>]*>(.*?)</code>', html, re.DOTALL)
    return [re.sub(r'<[^>]+>', '', b)[:200].strip() for b in blocks if len(b) > 100]

def extract_case_studies(html):
    """Extract enterprise case study opening sentences."""
    cases = re.findall(r'(?:enterprise|real.world|case.study)[^.]{0,50}\.', html, re.IGNORECASE)
    return [c.strip() for c in cases]

# ─── CONTEXT CONTAMINATION ────────────────────────────────────────────────────

# Topic keyword sets per week (what SHOULD appear vs what SHOULDN'T)
WEEK_TOPICS = {
    19: {"expected": ["RAG", "BM25", "Okapi", "hybrid search", "sparse", "dense", "reranker", "FAISS", "Pinecone"],
         "week_name": "Advanced RAG"},
    20: {"expected": ["LoRA", "QLoRA", "PEFT", "adapter", "fine-tun", "quantiz", "rank", "low-rank"],
         "week_name": "Fine-Tuning & PEFT"},
    21: {"expected": ["LangGraph", "agent", "tool call", "ReAct", "chain-of-thought", "multi-agent", "orchestrat"],
         "week_name": "LLM Agents & LangGraph"},
    22: {"expected": ["MLflow", "DVC", "experiment track", "model registry", "artifact", "version"],
         "week_name": "MLOps & Experiment Tracking"},
    23: {"expected": ["GCP", "Vertex AI", "Cloud Run", "BigQuery", "Beam", "serverless", "GKE"],
         "week_name": "Cloud ML (GCP)"},
    24: {"expected": ["Kubernetes", "Helm", "pod", "deployment", "HPA", "kubectl", "container", "Docker"],
         "week_name": "Kubernetes & Infrastructure"},
    25: {"expected": ["monitoring", "drift", "Prometheus", "Grafana", "alerting", "observ", "SLO", "latency"],
         "week_name": "ML Monitoring & Observability"},
    26: {"expected": ["capstone", "system design", "production", "end-to-end", "pipeline", "architecture"],
         "week_name": "Capstone & System Design"},
}

def check_context_contamination(week_num, html):
    """Check if a week's opening blocks contain content from wrong topics."""
    issues = []
    if week_num not in WEEK_TOPICS:
        return issues
    
    config = WEEK_TOPICS[week_num]
    expected_kw = config["expected"]
    
    # Check other week keywords appearing in day 1 opening block
    for other_week, other_config in WEEK_TOPICS.items():
        if other_week == week_num:
            continue
        for kw in other_config["expected"]:
            if kw in expected_kw:
                continue
            # Look for foreign keyword in the first 10,000 chars (opening blocks)
            head_html = html[:10000]
            if re.search(rf'\b{re.escape(kw)}\b', head_html, re.IGNORECASE):
                issues.append({
                    "type": "context_contamination",
                    "severity": "HIGH",
                    "detail": f"Week {other_week} keyword '{kw}' found in Week {week_num} opening section",
                    "foreign_week": other_week,
                    "foreign_topic": other_config["week_name"]
                })
    return issues[:5]  # cap to prevent noise

# ─── MAIN AUDIT ENGINE ───────────────────────────────────────────────────────

def run_pattern_scan(html, patterns, severity, category):
    """Generic pattern scanner returning structured findings."""
    findings = []
    for pattern, description in patterns:
        matches = list(re.finditer(pattern, html, re.IGNORECASE))
        if matches:
            findings.append({
                "category": category,
                "severity": severity,
                "description": description,
                "count": len(matches),
                "snippets": [html[max(0,m.start()-40):m.end()+40].replace('\n', ' ') for m in matches[:3]]
            })
    return findings

def audit_week(week_num):
    """Full audit of a single week file."""
    filepath = WEEKS_DIR / f"week{week_num}.html"
    if not filepath.exists():
        return None
    
    html = filepath.read_text(encoding='utf-8', errors='replace')
    results = {
        "week": week_num,
        "file": str(filepath),
        "total_chars": len(html),
        "findings": []
    }
    
    # Critical scans
    results["findings"] += run_pattern_scan(html, SECURITY_PATTERNS, "CRITICAL", "Security Anti-Pattern")
    results["findings"] += run_pattern_scan(html, DEPRECATED_PATTERNS, "CRITICAL", "Deprecated API")
    
    # High scans
    results["findings"] += run_pattern_scan(html, HALLUCINATED_CITATIONS, "HIGH", "Unverified Citation/Claim")
    results["findings"] += run_pattern_scan(html, VOCABULARY_ERRORS, "HIGH", "Technical Vocabulary Error")
    results["findings"] += run_pattern_scan(html, FILLER_PATTERNS, "HIGH", "Sycophantic Filler")
    results["findings"] += run_pattern_scan(html, MISSING_CAVEAT_PATTERNS, "HIGH", "Missing Production Caveat")
    
    # Medium scans
    results["findings"] += run_pattern_scan(html, TAUTOLOGICAL_PATTERNS, "MEDIUM", "Circular Definition")
    results["findings"] += run_pattern_scan(html, STALE_REFERENCES, "MEDIUM", "Stale Reference")
    
    # Context contamination (only weeks with defined topics)
    results["findings"] += check_context_contamination(week_num, html)
    
    # Store raw data for cross-week duplicate detection
    results["_quiz_questions"] = extract_quiz_questions(html)
    results["_flashcard_fronts"] = extract_flashcard_fronts(html)
    results["_code_block_samples"] = extract_code_blocks(html)
    results["_case_studies"] = extract_case_studies(html)
    
    # Count by severity
    results["critical_count"] = sum(1 for f in results["findings"] if f.get("severity") == "CRITICAL")
    results["high_count"] = sum(1 for f in results["findings"] if f.get("severity") == "HIGH")
    results["medium_count"] = sum(1 for f in results["findings"] if f.get("severity") == "MEDIUM")
    
    return results

def find_cross_week_duplicates(all_results):
    """Find quiz questions, flashcards, and code blocks duplicated across weeks."""
    duplicates = []
    
    # Quiz duplicate detection
    quiz_index = defaultdict(list)  # normalized_question -> [week_nums]
    for r in all_results:
        for q in r.get("_quiz_questions", []):
            key = re.sub(r'\s+', ' ', q.lower().strip())[:80]
            quiz_index[key].append(r["week"])
    
    for q, weeks in quiz_index.items():
        if len(weeks) > 1:
            duplicates.append({
                "type": "duplicate_quiz_question",
                "severity": "HIGH",
                "detail": f"Same quiz question in weeks {weeks}: '{q[:60]}...'",
                "weeks": weeks
            })
    
    # Flashcard duplicate detection
    fc_index = defaultdict(list)
    for r in all_results:
        for fc in r.get("_flashcard_fronts", []):
            key = re.sub(r'\s+', ' ', fc.lower().strip())[:60]
            fc_index[key].append(r["week"])
    
    for fc, weeks in fc_index.items():
        if len(weeks) > 1:
            duplicates.append({
                "type": "duplicate_flashcard",
                "severity": "MEDIUM",
                "detail": f"Same flashcard in weeks {weeks}: '{fc[:50]}...'",
                "weeks": weeks
            })
    
    # Code block near-duplicate
    code_index = defaultdict(list)
    for r in all_results:
        for cb in r.get("_code_block_samples", []):
            key = re.sub(r'\s+', ' ', cb.lower())[:100]
            if key:
                code_index[key].append(r["week"])
    
    for cb, weeks in code_index.items():
        if len(weeks) > 1:
            duplicates.append({
                "type": "duplicate_code_block",
                "severity": "MEDIUM",
                "detail": f"Identical code block in weeks {weeks}: '{cb[:60]}...'",
                "weeks": weeks
            })
    
    return duplicates

# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

def main():
    print("🔍 AI Failure Audit — Starting scan of all 26 weeks...\n")
    
    all_results = []
    
    # Audit all weeks (1-18 lighter scan, 19-26 full focus)
    for week_num in range(1, 27):
        result = audit_week(week_num)
        if result:
            all_results.append(result)
            c = result["critical_count"]
            h = result["high_count"]
            m = result["medium_count"]
            flag = "🔴" if c > 0 else ("🟠" if h > 0 else ("🟡" if m > 0 else "✅"))
            print(f"  {flag} Week {week_num:2d}: {c} CRITICAL | {h} HIGH | {m} MEDIUM")
    
    # Cross-week duplicate analysis
    print("\n🔁 Running cross-week duplicate detection...")
    duplicates = find_cross_week_duplicates(all_results)
    dup_critical = [d for d in duplicates if d["severity"] == "HIGH"]
    print(f"   Found {len(duplicates)} total duplicates ({len(dup_critical)} HIGH severity)\n")
    
    # Build final report
    report = {
        "summary": {
            "total_weeks_scanned": len(all_results),
            "weeks_with_critical": [r["week"] for r in all_results if r["critical_count"] > 0],
            "weeks_with_high": [r["week"] for r in all_results if r["high_count"] > 0],
            "total_critical": sum(r["critical_count"] for r in all_results),
            "total_high": sum(r["high_count"] for r in all_results),
            "total_medium": sum(r["medium_count"] for r in all_results),
            "cross_week_duplicates": len(duplicates),
        },
        "cross_week_duplicates": duplicates,
        "week_results": []
    }
    
    for r in all_results:
        # Strip raw data from final report (too large)
        clean = {k: v for k, v in r.items() if not k.startswith("_")}
        report["week_results"].append(clean)
    
    # Save full JSON report
    OUTPUT_FILE.write_text(json.dumps(report, indent=2), encoding='utf-8')
    
    # Print critical and high findings for weeks 19-26
    print("=" * 70)
    print("DETAILED FINDINGS — WEEKS 19-26 (CRITICAL + HIGH ONLY)")
    print("=" * 70)
    
    for r in all_results:
        if r["week"] < 19:
            continue
        critical_high = [f for f in r["findings"] if f.get("severity") in ("CRITICAL", "HIGH")]
        if not critical_high:
            print(f"\n✅ Week {r['week']}: No critical/high issues found")
            continue
        
        print(f"\n{'─'*60}")
        print(f"📋 WEEK {r['week']} — {r['critical_count']} CRITICAL | {r['high_count']} HIGH")
        print(f"{'─'*60}")
        
        for f in critical_high:
            sev = f.get("severity", "?")
            icon = "🔴" if sev == "CRITICAL" else "🟠"
            print(f"\n  {icon} [{sev}] {f.get('category', '')}")
            print(f"     {f.get('description', f.get('detail', ''))}")
            if "count" in f:
                print(f"     Occurrences: {f['count']}")
            if "snippets" in f:
                for s in f["snippets"][:2]:
                    snippet = s.strip()[:100]
                    print(f"     ▸ ...{snippet}...")
    
    # Weeks 1-18 summary
    print("\n" + "=" * 70)
    print("WEEKS 1-18 SUMMARY")
    print("=" * 70)
    for r in all_results:
        if r["week"] >= 19:
            continue
        if r["critical_count"] > 0 or r["high_count"] > 0:
            print(f"  🔴 Week {r['week']:2d}: {r['critical_count']} critical, {r['high_count']} high — NEEDS REVIEW")
    
    # Cross-week duplicate summary
    if duplicates:
        print("\n" + "=" * 70)
        print("CROSS-WEEK DUPLICATES")
        print("=" * 70)
        for d in duplicates[:20]:
            icon = "🟠" if d["severity"] == "HIGH" else "🟡"
            print(f"  {icon} [{d['type']}] Weeks {d['weeks']}: {d['detail'][:80]}")
    
    print(f"\n✅ Full report saved to: {OUTPUT_FILE}")
    
    # Final totals
    s = report["summary"]
    print(f"\n📊 TOTALS: {s['total_critical']} CRITICAL | {s['total_high']} HIGH | {s['total_medium']} MEDIUM")
    print(f"   Weeks needing immediate attention: {s['weeks_with_critical']}")

if __name__ == "__main__":
    main()
