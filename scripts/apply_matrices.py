#!/usr/bin/env python3
"""
apply_matrices.py
Replaces boilerplate 'Engineering Decision Matrix' blocks with topic-specific ML matrices.
"""

import re
from bs4 import BeautifulSoup

WEEKS_DIR = "pages/weeks"

# A collection of authentic MLOps / ML Engineering decision matrices
MATRICES = {
    "RAG": {
        "headers": ["Retriever Type", "Recall@10", "Latency (p99)", "Hardware Cost", "Best For"],
        "rows": [
            ["Dense (HNSW)", "High", "< 50ms", "High (RAM/GPU)", "Semantic matching"],
            ["Sparse (BM25)", "Medium", "< 20ms", "Low (CPU)", "Exact keyword matching"],
            ["Hybrid + RRF", "Highest", "< 80ms", "Very High", "Production QA systems"]
        ]
    },
    "Vector": {
        "headers": ["Vector DB Index", "Build Time", "Query Speed", "Memory Footprint", "Recall"],
        "rows": [
            ["Flat (Exact)", "Instant", "O(N) - Slow", "Minimal", "100% (Baseline)"],
            ["IVF-PQ", "Slow (Training)", "Fast", "Very Low", "Medium"],
            ["HNSW", "Medium", "Ultra-Fast", "High (Graph)", "High (>95%)"]
        ]
    },
    "LLM Serving": {
        "headers": ["Inference Engine", "Batching", "GPU Memory", "Latency", "Best For"],
        "rows": [
            ["HuggingFace Pipeline", "Static", "High Overhead", "High", "Local dev / prototyping"],
            ["vLLM", "Continuous", "PagedAttention", "Low", "High-throughput production"],
            ["TensorRT-LLM", "Inflight", "Maximized", "Ultra-Low", "NVIDIA native scale"]
        ]
    },
    "Fine-Tuning": {
        "headers": ["Tuning Method", "VRAM Req (8B)", "Compute Time", "Performance", "Artifact Size"],
        "rows": [
            ["Full Fine-Tuning", "> 80GB (A100x2)", "Days", "Maximized", "16GB (Full Weights)"],
            ["LoRA (r=16)", "~24GB", "Hours", "98% of Full", "~50MB (Adapter)"],
            ["QLoRA (4-bit)", "~10GB", "Hours (Slower)", "95% of Full", "~50MB (Adapter)"]
        ]
    },
    "Orchestration": {
        "headers": ["Orchestrator", "Learning Curve", "Execution Environment", "State Management", "Primary Use Case"],
        "rows": [
            ["Cron / Bash", "Lowest", "Single VM", "Stateless", "Simple periodic scripts"],
            ["Airflow", "High", "Distributed (K8s/Celery)", "Database-backed", "Complex DAG dependencies"],
            ["Prefect", "Medium", "Hybrid", "Cloud-backed", "Dynamic Python workflows"]
        ]
    },
    "Deployment": {
        "headers": ["Deployment Env", "Cold Start", "Scaling Speed", "Cost Model", "Management Overhead"],
        "rows": [
            ["Serverless (Lambda)", "High (>5s)", "Instant", "Per-invocation", "Zero"],
            ["PaaS (Render/Railway)", "Medium", "Seconds", "Per-minute", "Low"],
            ["Kubernetes (GKE/EKS)", "Low", "Minutes (Nodes)", "Fixed + Auto", "High"]
        ]
    },
    "Monitoring": {
        "headers": ["Drift Type", "Detection Method", "Metric", "Alert Threshold", "Action"],
        "rows": [
            ["Data Drift", "KS-Test / PSI", "Feature Dist.", "p < 0.05", "Retrain Model"],
            ["Concept Drift", "Rolling Accuracy", "F1 / RMSE", "10% drop", "Update Labels & Retrain"],
            ["System Degradation", "Latency / 5xx", "P99 ms", "> SLA", "Scale / Rollback"]
        ]
    },
    "Agents": {
        "headers": ["Agent Architecture", "Reasoning Depth", "Latency", "Token Usage", "Use Case"],
        "rows": [
            ["Direct Prompting", "Zero", "Fastest", "Minimal", "Simple extraction"],
            ["ReAct Loop", "Medium", "Slow (Multi-turn)", "High", "Tool use & browsing"],
            ["Multi-Agent (CrewAI)", "Deep", "Very Slow", "Extreme", "Complex research tasks"]
        ]
    },
    "Evaluation": {
        "headers": ["Evaluation Method", "Scalability", "Correlation w/ Human", "Cost", "Best For"],
        "rows": [
            ["Exact Match / ROUGE", "Infinite", "Low", "Zero", "Fact checking / extractive"],
            ["LLM-as-a-Judge", "High", "High", "Moderate", "Tone, coherence, reasoning"],
            ["Human Evaluation", "None", "100% (Ground Truth)", "Very High", "Final production gate"]
        ]
    },
    "Data": {
        "headers": ["Storage Format", "Compression", "Read Speed (Analytical)", "Schema Evolution", "Ecosystem"],
        "rows": [
            ["CSV", "None", "Slow", "Manual", "Universal"],
            ["JSONL", "None", "Slow", "Flexible", "Web / API / LLM Data"],
            ["Parquet", "Snappy/GZIP", "Ultra-Fast (Columnar)", "Built-in", "Data Lakes / PyArrow"]
        ]
    },
    "Cloud": {
        "headers": ["Provider Strategy", "Lock-in", "Managed ML Tools", "Cost Efficiency", "Flexibility"],
        "rows": [
            ["AWS/GCP Native", "High", "SageMaker / Vertex", "Medium", "Low"],
            ["Cloud-Agnostic (K8s)", "Low", "Kubeflow / MLflow", "High (Spot Instances)", "Maximum"],
            ["Serverless API", "Medium", "Bedrock / OpenAI", "Variable", "Minimal"]
        ]
    },
    "Default": {
        "headers": ["Architecture Strategy", "Upfront Cost", "Maintenance", "Scalability", "Time-to-Market"],
        "rows": [
            ["Monolithic MVP", "Low", "Low (Initially)", "Poor", "Fast (< 1 week)"],
            ["Microservices", "High", "High", "Excellent", "Slow (Months)"],
            ["Serverless Functions", "Medium", "Low", "Infinite", "Medium"]
        ]
    }
}

def get_matrix_html(matrix_data: dict, title: str) -> str:
    html = f'<h3 class="sh3">Engineering Decision Matrix: {title}</h3>\n'
    html += '<div style="overflow-x:auto;">\n'
    html += '<table style="width:100%; border-collapse:collapse; margin:1rem 0; font-size:13px; text-align:left;">\n'
    
    # Headers
    html += '<thead>\n<tr style="border-bottom:2px solid var(--border); background:var(--bg-secondary);">\n'
    for h in matrix_data["headers"]:
        html += f'<th style="padding:10px;">{h}</th>\n'
    html += '</tr>\n</thead>\n'
    
    # Rows
    html += '<tbody>\n'
    for row in matrix_data["rows"]:
        html += '<tr style="border-bottom:1px solid var(--border); transition: background 0.2s;" onmouseover="this.style.background=\'var(--bg-secondary)\'" onmouseout="this.style.background=\'transparent\'">\n'
        html += f'<td style="padding:10px;"><strong>{row[0]}</strong></td>\n'
        for cell in row[1:]:
            # Highlight specific keywords
            c_text = str(cell)
            if "High" in c_text and not "Highest" in c_text:
                c_text = c_text.replace("High", "<span style='color:var(--orange);'>High</span>")
            if "Low" in c_text and not "Lowest" in c_text:
                c_text = c_text.replace("Low", "<span style='color:var(--green);'>Low</span>")
            if "Fast" in c_text:
                c_text = c_text.replace("Fast", "<span style='color:var(--green);'>Fast</span>")
            if "Slow" in c_text:
                c_text = c_text.replace("Slow", "<span style='color:var(--red);'>Slow</span>")
                
            html += f'<td style="padding:10px;">{c_text}</td>\n'
        html += '</tr>\n'
    html += '</tbody>\n</table>\n</div>\n'
    return html

def determine_matrix(day_title: str) -> tuple:
    t = day_title.lower()
    if any(k in t for k in ['rag', 'retriev']): return MATRICES["RAG"], "Retrieval Architectures"
    if any(k in t for k in ['vector', 'hnsw', 'faiss']): return MATRICES["Vector"], "Vector DB Indexing"
    if any(k in t for k in ['serve', 'vllm', 'inference', 'latency']): return MATRICES["LLM Serving"], "LLM Inference Engines"
    if any(k in t for k in ['fine-tun', 'lora', 'peft']): return MATRICES["Fine-Tuning"], "Fine-Tuning Strategies"
    if any(k in t for k in ['airflow', 'pipeline', 'orchestrat']): return MATRICES["Orchestration"], "Workflow Orchestration"
    if any(k in t for k in ['deploy', 'render', 'railway', 'lambda']): return MATRICES["Deployment"], "Deployment Environments"
    if any(k in t for k in ['monitor', 'evidently', 'drift']): return MATRICES["Monitoring"], "Drift Detection & Monitoring"
    if any(k in t for k in ['agent', 'crewai', 'langgraph', 'react']): return MATRICES["Agents"], "Agent Architectures"
    if any(k in t for k in ['eval', 'ragas', 'test']): return MATRICES["Evaluation"], "LLM Evaluation Methods"
    if any(k in t for k in ['data', 'neo4j', 'dvc']): return MATRICES["Data"], "Data Storage & Versioning"
    if any(k in t for k in ['cloud', 'aws', 'vertex']): return MATRICES["Cloud"], "Cloud ML Strategy"
    
    return MATRICES["Default"], "General Production Trade-offs"

def replace_matrix_in_html(html: str, day_id: str, day_title: str) -> tuple:
    day_start = html.find(f'id="{day_id}"')
    if day_start == -1: return html, False
    next_day = html.find('class="day-section"', day_start + 20)
    section = html[day_start:next_day] if next_day != -1 else html[day_start:]
    
    if 'Engineering Decision Matrix' not in section:
        return html, False
        
    # The target block pattern: <h3 ...>Engineering Decision Matrix...</h3>\n<table...>...</table>
    target_pattern = r'<h3 class="sh3">Engineering Decision Matrix.*?</table>'
    match = re.search(target_pattern, section, re.DOTALL)
    if not match:
        return html, False
        
    matrix_data, m_title = determine_matrix(day_title)
    new_block = get_matrix_html(matrix_data, m_title)
    
    new_section = section[:match.start()] + new_block + section[match.end():]
    new_html = html[:day_start] + new_section + (html[next_day:] if next_day != -1 else '')
    return new_html, True


def main():
    print("=" * 65)
    print("ENGINEERING DECISION MATRIX REPLACEMENT")
    print("=" * 65)
    
    total = 0
    for w in range(18, 27):
        path = f"{WEEKS_DIR}/week{w}.html"
        html = open(path, encoding='utf-8').read()
        original = html
        
        soup = BeautifulSoup(html, 'html.parser')
        days = soup.find_all('div', class_='day-section')
        
        cnt = 0
        for day in days:
            day_id = day.get('id', '')
            if 'toolkit' in day_id: continue
            
            # Extract day title from the first h2 or h3
            h2 = day.find('h2')
            title = h2.get_text() if h2 else ""
            
            html, changed = replace_matrix_in_html(html, day_id, title)
            if changed:
                cnt += 1
                
        if html != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        total += cnt
        print(f"  Week {w}: {cnt} matrices replaced")
        
    print(f"\nTotal: {total} replacements completed.")


if __name__ == '__main__':
    main()
