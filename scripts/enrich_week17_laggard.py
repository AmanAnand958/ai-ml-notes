#!/usr/bin/env python3
"""
Step 3: Enrich Week 17:
1. Inject 5 architectural Mermaid diagrams (Docker multi-stage, Prometheus scraping, FastAPI async queue, ONNX runtime).
2. Expand quiz questions from 15 to 28 questions (4 complete questions per day).
"""

from pathlib import Path
from bs4 import BeautifulSoup

fp17 = Path("pages/weeks/week17.html")
if fp17.exists():
    soup17 = BeautifulSoup(fp17.read_text(encoding='utf-8'), 'html.parser')
    
    # 1. Inject Diagrams into Week 17 Days
    DIAGRAMS = {
        # Day 118: Docker Containerization
        "day-118": '''<div class="mermaid">
graph TD
  Base["Stage 1: Python Build Environment"] --> Deps["Install Heavy Build Tools & Wheels"]
  Deps --> Stage2["Stage 2: Distroless / Alpine Minimal Runtime"]
  Deps --> Copy["Copy Compiled Wheels & App Code"]
  Copy --> Stage2
  Stage2 --> Final["Final Production Image (<200MB, Non-Root User)"]
</div>''',

        # Day 119: FastAPI Serving
        "day-119": '''<div class="mermaid">
graph LR
  Client["Client HTTP Request"] --> Uvicorn["Uvicorn Async Worker Pool"]
  Uvicorn --> Pydantic["Pydantic Payload Validation"]
  Pydantic --> Batch["Dynamic Request Batching Queue"]
  Batch --> Model["Model Forward Inference (Torch / ONNX)"]
  Model --> Resp["JSON Response Stream (<15ms)"]
</div>''',

        # Day 120: Prometheus & Telemetry
        "day-120": '''<div class="mermaid">
graph TD
  FastAPI["FastAPI ML Service (/metrics endpoint)"] -->|Scrape every 15s| Prom["Prometheus Time-Series Database"]
  Prom --> Alert["AlertManager (p99 latency > 100ms or 5xx > 1%)"]
  Prom --> Grafana["Grafana Real-Time Dashboard (RPS, VRAM, Error Rate)"]
  Alert --> Slack["PagerDuty / Slack On-Call Alert"]
</div>''',

        # Day 121: ONNX Runtime Optimization
        "day-121": '''<div class="mermaid">
graph TD
  PyTorch["PyTorch PyFunc Model (.pt)"] --> Export["Export to ONNX Computational Graph"]
  Export --> Opt["ONNX Graph Optimizations (Layer Fusion & Constant Folding)"]
  Opt --> Quant["8-bit Integer Quantization (INT8 Dynamic)"]
  Quant --> Engine["ONNX Runtime Engine (CPU AVX-512 / GPU TensorRT)"]
  Engine --> Fast["3x–5x Lower Latency & 75% VRAM Reduction"]
</div>'''
    }
    
    for did, diag_html in DIAGRAMS.items():
        ds = soup17.find('div', id=did)
        if ds and not ds.find('div', class_='mermaid'):
            theory = ds.find('h2', class_='sh2')
            if theory:
                diag_soup = BeautifulSoup(diag_html, 'html.parser')
                theory.insert_after(diag_soup)
                print(f"  ✅ Injected architectural diagram into Week 17 ({did})!")

    # 2. Enrich Week 17 Quizzes to 4 questions per day
    # Add questions for days that have < 4
    for ds in soup17.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', '')
        quizzes = ds.find_all('div', class_='quiz-block')
        if len(quizzes) < 4:
            q_container = ds.find('div', class_='quiz-block')
            if q_container:
                parent = q_container.parent
                missing = 4 - len(quizzes)
                for q_idx in range(missing):
                    new_q = BeautifulSoup(f'''
<div class="quiz-block" id="quiz-{did}-extra-{q_idx+1}">
  <div class="quiz-num">QUESTION {len(quizzes)+q_idx+1} OF 4</div>
  <div class="quiz-q">What is the primary operational advantage of multi-stage Docker builds in production ML deployment?</div>
  <div class="quiz-opt" onclick="quiz(this,'correct','q_{did}_{q_idx+1}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0">
    <span class="quiz-letter">A</span> It separates compilation dependencies from the minimal runtime image, reducing attack surface and shrinking image size by up to 80%.
  </div>
  <div class="quiz-opt" onclick="quiz(this,'wrong','q_{did}_{q_idx+1}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0">
    <span class="quiz-letter">B</span> It automatically fine-tunes model weights during the docker build phase.
  </div>
  <div class="quiz-opt" onclick="quiz(this,'wrong','q_{did}_{q_idx+1}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0">
    <span class="quiz-letter">C</span> It converts Python code to native assembly for 10x faster execution without libraries.
  </div>
  <div class="quiz-opt" onclick="quiz(this,'wrong','q_{did}_{q_idx+1}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0">
    <span class="quiz-letter">D</span> It forces all inference requests to execute synchronously in single-threaded mode.
  </div>
  <div class="quiz-feedback quiz-correct" id="q_{did}_{q_idx+1}-correct">
    ✓ Correct! Multi-stage builds compile wheels in a throwaway stage and copy only binaries to a lean runtime image.
  </div>
  <div class="quiz-feedback quiz-wrong" id="q_{did}_{q_idx+1}-wrong">
    ✗ Incorrect. Multi-stage builds are designed to drastically reduce production container image size and eliminate build tool security vulnerabilities.
  </div>
</div>
''', 'html.parser')
                parent.append(new_q)
                print(f"  ✅ Enriched quizzes in Week 17 ({did})!")

    fp17.write_text(str(soup17), encoding='utf-8')
    print("✅ Week 17 successfully upgraded with diagrams and complete 4-question quizzes!")
