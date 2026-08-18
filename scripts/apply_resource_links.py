#!/usr/bin/env python3
"""
apply_resource_links.py
Replaces boilerplate resource links with domain-specific curated resources.
"""

import re
from bs4 import BeautifulSoup

WEEKS_DIR = "pages/weeks"

# A collection of curated MLOps / ML Engineering resources
RESOURCES = {
    "RAG": [
        {"url": "https://python.langchain.com/docs/modules/data_connection/retrievers/", "type": "TUTORIAL", "title": "LangChain Retrieval Docs", "sub": "Comprehensive guide to building advanced RAG retrieval pipelines."},
        {"url": "https://www.pinecone.io/learn/series/rag/", "type": "GUIDE", "title": "Pinecone RAG Masterclass", "sub": "In-depth series on vector search, chunking strategies, and generation."},
        {"url": "https://arxiv.org/abs/2005.11401", "type": "PAPER", "title": "Retrieval-Augmented Generation (Original Paper)", "sub": "The seminal paper by Lewis et al. introducing RAG for knowledge-intensive tasks."}
    ],
    "Vector": [
        {"url": "https://faiss.ai/", "type": "REFERENCE", "title": "FAISS Official Documentation", "sub": "Library for efficient similarity search and clustering of dense vectors."},
        {"url": "https://arxiv.org/abs/1603.09320", "type": "PAPER", "title": "HNSW Algorithm Paper", "sub": "Malkov & Yashunin's foundational paper on Hierarchical Navigable Small World graphs."},
        {"url": "https://qdrant.tech/documentation/", "type": "REFERENCE", "title": "Qdrant Vector Database", "sub": "Documentation for the high-performance Rust-based vector search engine."}
    ],
    "LLM Serving": [
        {"url": "https://vllm.readthedocs.io/", "type": "REFERENCE", "title": "vLLM Documentation", "sub": "High-throughput and memory-efficient LLM serving engine with PagedAttention."},
        {"url": "https://github.com/NVIDIA/TensorRT-LLM", "type": "TOOL", "title": "NVIDIA TensorRT-LLM", "sub": "NVIDIA's framework for optimizing and deploying large language models."},
        {"url": "https://arxiv.org/abs/2309.06180", "type": "PAPER", "title": "PagedAttention Paper", "sub": "Research on memory management for LLM serving with continuous batching."}
    ],
    "Fine-Tuning": [
        {"url": "https://huggingface.co/docs/peft/", "type": "REFERENCE", "title": "Hugging Face PEFT", "sub": "Parameter-Efficient Fine-Tuning library documentation and examples."},
        {"url": "https://arxiv.org/abs/2106.09685", "type": "PAPER", "title": "LoRA: Low-Rank Adaptation", "sub": "Original paper demonstrating efficient fine-tuning by freezing pre-trained weights."},
        {"url": "https://arxiv.org/abs/2305.14314", "type": "PAPER", "title": "QLoRA: Efficient Finetuning", "sub": "Paper on quantised low-rank adaptation for massive LLMs on single GPUs."}
    ],
    "Orchestration": [
        {"url": "https://airflow.apache.org/", "type": "REFERENCE", "title": "Apache Airflow Docs", "sub": "Platform to programmatically author, schedule, and monitor workflows."},
        {"url": "https://docs.prefect.io/", "type": "REFERENCE", "title": "Prefect 2.0 Documentation", "sub": "Modern orchestration framework for dataflow automation in Python."},
        {"url": "https://mlflow.org/docs/latest/pipelines.html", "type": "GUIDE", "title": "MLflow Recipes (Pipelines)", "sub": "Opinionated templates for structuring and orchestrating ML projects."}
    ],
    "Deployment": [
        {"url": "https://kubernetes.io/docs/concepts/workloads/", "type": "REFERENCE", "title": "Kubernetes Workloads", "sub": "Core concepts for deploying applications (Deployments, StatefulSets)."},
        {"url": "https://keda.sh/", "type": "TOOL", "title": "KEDA: Event-driven Autoscaling", "sub": "Kubernetes-based Event Driven Autoscaling for dynamic ML workloads."},
        {"url": "https://helm.sh/docs/", "type": "REFERENCE", "title": "Helm Documentation", "sub": "The package manager for Kubernetes. Essential for reproducible ML deployments."}
    ],
    "Monitoring": [
        {"url": "https://docs.evidentlyai.com/", "type": "REFERENCE", "title": "Evidently AI Docs", "sub": "Open-source ML observability framework for detecting data and concept drift."},
        {"url": "https://prometheus.io/docs/introduction/overview/", "type": "REFERENCE", "title": "Prometheus Overview", "sub": "Standard open-source systems monitoring and alerting toolkit."},
        {"url": "https://grafana.com/docs/", "type": "REFERENCE", "title": "Grafana Documentation", "sub": "Platform for observability dashboards and metric visualization."}
    ],
    "Agents": [
        {"url": "https://python.langchain.com/docs/modules/agents/", "type": "REFERENCE", "title": "LangChain Agents", "sub": "Framework for LLMs to dynamically use tools to achieve goals."},
        {"url": "https://arxiv.org/abs/2210.03629", "type": "PAPER", "title": "ReAct: Synergizing Reasoning", "sub": "Foundational paper on combining reasoning traces with action generation."},
        {"url": "https://docs.crewai.com/", "type": "TOOL", "title": "CrewAI Documentation", "sub": "Framework for orchestrating role-playing, autonomous AI agents."}
    ],
    "Evaluation": [
        {"url": "https://docs.ragas.io/", "type": "TOOL", "title": "Ragas (RAG Assessment)", "sub": "Framework for evaluating Retrieval Augmented Generation pipelines."},
        {"url": "https://arxiv.org/abs/2306.05685", "type": "PAPER", "title": "LLM-as-a-Judge Paper", "sub": "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena."},
        {"url": "https://github.com/confident-ai/deepeval", "type": "TOOL", "title": "DeepEval", "sub": "Open-source evaluation framework for LLM applications."}
    ],
    "Data": [
        {"url": "https://dvc.org/doc", "type": "REFERENCE", "title": "Data Version Control (DVC)", "sub": "Git for data and models. Versioning for large files and datasets."},
        {"url": "https://neo4j.com/docs/", "type": "REFERENCE", "title": "Neo4j Graph Database", "sub": "Native graph database for advanced relationship extraction and GraphRAG."},
        {"url": "https://parquet.apache.org/", "type": "REFERENCE", "title": "Apache Parquet", "sub": "Columnar storage format for highly efficient data processing."}
    ],
    "Cloud": [
        {"url": "https://aws.amazon.com/sagemaker/", "type": "REFERENCE", "title": "Amazon SageMaker", "sub": "Build, train, and deploy machine learning models at scale."},
        {"url": "https://cloud.google.com/vertex-ai", "type": "REFERENCE", "title": "Google Vertex AI", "sub": "Fully managed ML platform for custom models and generative AI."},
        {"url": "https://learn.microsoft.com/en-us/azure/machine-learning/", "type": "REFERENCE", "title": "Azure Machine Learning", "sub": "Enterprise-grade service for end-to-end machine learning lifecycles."}
    ],
    "Default": [
        {"url": "https://huggingface.co/docs", "type": "REFERENCE", "title": "Hugging Face Ecosystem", "sub": "The central hub for ML models, datasets, and NLP libraries."},
        {"url": "https://github.com/features/actions", "type": "TOOL", "title": "GitHub Actions for CI/CD", "sub": "Automate your ML software workflows directly in GitHub."},
        {"url": "https://mlflow.org/docs/latest/index.html", "type": "REFERENCE", "title": "MLflow Documentation", "sub": "Open source platform for the machine learning lifecycle."}
    ]
}

def determine_resources(day_title: str) -> list:
    t = day_title.lower()
    if any(k in t for k in ['rag', 'retriev']): return RESOURCES["RAG"]
    if any(k in t for k in ['vector', 'hnsw', 'faiss']): return RESOURCES["Vector"]
    if any(k in t for k in ['serve', 'vllm', 'inference', 'latency', 'api']): return RESOURCES["LLM Serving"]
    if any(k in t for k in ['fine-tun', 'lora', 'peft']): return RESOURCES["Fine-Tuning"]
    if any(k in t for k in ['airflow', 'pipeline', 'orchestrat', 'dag']): return RESOURCES["Orchestration"]
    if any(k in t for k in ['deploy', 'render', 'railway', 'lambda', 'container', 'k8s']): return RESOURCES["Deployment"]
    if any(k in t for k in ['monitor', 'evidently', 'drift', 'telemetry']): return RESOURCES["Monitoring"]
    if any(k in t for k in ['agent', 'crewai', 'langgraph', 'react']): return RESOURCES["Agents"]
    if any(k in t for k in ['eval', 'ragas', 'test', 'guardrail']): return RESOURCES["Evaluation"]
    if any(k in t for k in ['data', 'neo4j', 'dvc', 'dataset']): return RESOURCES["Data"]
    if any(k in t for k in ['cloud', 'aws', 'vertex', 'azure', 'sagemaker']): return RESOURCES["Cloud"]
    
    return RESOURCES["Default"]

def get_resources_html(resources: list) -> str:
    html = '<h2 class="sh2">📚 Resources</h2>\n<div class="res-grid">\n'
    for r in resources:
        html += f'<a class="resource-card" href="{r["url"]}" rel="noopener" target="_blank">\n'
        html += f'<div class="rc-type">{r["type"]}</div>\n'
        html += f'<div class="rc-title">{r["title"]}</div>\n'
        html += f'<div class="rc-sub">{r["sub"]}</div>\n'
        html += '</a>\n'
    html += '</div>\n'
    return html

def replace_resources_in_html(html: str, day_id: str, day_title: str) -> tuple:
    day_start = html.find(f'id="{day_id}"')
    if day_start == -1: return html, False
    next_day = html.find('class="day-section"', day_start + 20)
    section = html[day_start:next_day] if next_day != -1 else html[day_start:]
    
    target_pattern = r'<h2 class="sh2">\s*📚 Resources\s*</h2>\s*<div class="res-grid">.*?</a>\s*</div>'
    match = re.search(target_pattern, section, re.DOTALL)
    if not match:
        return html, False
        
    resources = determine_resources(day_title)
    new_block = get_resources_html(resources)
    
    new_section = section[:match.start()] + new_block + section[match.end():]
    new_html = html[:day_start] + new_section + (html[next_day:] if next_day != -1 else '')
    return new_html, True

def main():
    print("=" * 65)
    print("DAY-SPECIFIC RESOURCE LINKS REPLACEMENT")
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
            
            h2 = day.find('h2')
            title = h2.get_text() if h2 else ""
            
            html, changed = replace_resources_in_html(html, day_id, title)
            if changed:
                cnt += 1
                
        if html != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        total += cnt
        print(f"  Week {w}: {cnt} resource grids replaced")
        
    print(f"\nTotal: {total} replacements completed.")


if __name__ == '__main__':
    main()
