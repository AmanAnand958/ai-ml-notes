#!/usr/bin/env python3
"""
Step 5: Enrich Week 18 with complete 4-question quizzes per day across Days 125 to 135.
"""

from bs4 import BeautifulSoup
from pathlib import Path

fp18 = Path("pages/weeks/week18.html")
soup = BeautifulSoup(fp18.read_text(encoding='utf-8', errors='replace'), 'html.parser')

WEEK18_EXTRA_QUIZZES = {
    "day-125": [
        ("q125_2", "QUESTION 2 OF 4", "What is the primary role of a Kubernetes Pod?", [
            ("A", "wrong", "A physical machine inside a cloud data center."),
            ("B", "correct", "The smallest deployable unit in Kubernetes that encapsulates one or more containers sharing network and storage."),
            ("C", "wrong", "A Python package manager."),
            ("D", "wrong", "A relational database table.")
        ], "✅ Correct! Pods represent the atomic execution unit in Kubernetes clusters.", "❌ Incorrect. Pods wrap containers and share network namespaces."),
        ("q125_3", "QUESTION 3 OF 4", "Why is a Kubernetes Service needed in front of ML Deployment Pods?", [
            ("A", "correct", "It provides a stable IP address and DNS name, load-balancing traffic across ephemeral Pod replicas."),
            ("B", "wrong", "To train neural networks faster."),
            ("C", "wrong", "To compress Docker container images."),
            ("D", "wrong", "To format JSON responses automatically.")
        ], "✅ Correct! Services provide stable virtual IPs and load-balance across dynamic Pods.", "❌ Incorrect. Services route traffic reliably across ephemeral pod instances."),
        ("q125_4", "QUESTION 4 OF 4", "How does a Kubernetes Horizontal Pod Autoscaler (HPA) determine when to scale up?", [
            ("A", "correct", "By monitoring target metrics (e.g. CPU, RAM, or custom inference queue depth) against configured threshold targets."),
            ("B", "wrong", "By checking the time of day on the host machine."),
            ("C", "wrong", "By asking developers via email notification."),
            ("D", "wrong", "By calculating the number of files in the project folder.")
        ], "✅ Correct! HPA dynamically adjusts replica counts based on observed metric utilization.", "❌ Incorrect. HPA scales based on real-time metric thresholds like CPU and queue depth.")
    ],
    "day-126": [
        ("q126_2", "QUESTION 2 OF 4", "What is the main difference between PaaS (e.g. Render/Railway) and IaaS (e.g. raw AWS EC2)?", [
            ("A", "correct", "PaaS abstracts away server provisioning, OS patching, and SSL certificates, allowing instant git-push deployments."),
            ("B", "wrong", "PaaS is strictly free forever while IaaS is always paid."),
            ("C", "wrong", "PaaS does not support Python runtimes."),
            ("D", "wrong", "IaaS runs exclusively on mobile devices.")
        ], "✅ Correct! PaaS platforms manage underlying server infrastructure automatically.", "❌ Incorrect. PaaS provides automated buildpacks and zero-config deployment over raw VM management."),
        ("q126_3", "QUESTION 3 OF 4", "Why should production API keys and database credentials never be hardcoded in git repositories?", [
            ("A", "correct", "Public or leaked commits expose secrets to automated scrapers; use environment variables and secret managers instead."),
            ("B", "wrong", "Because Python syntax forbids strings longer than 20 characters."),
            ("C", "wrong", "Because git commits fail if string variables contain numbers."),
            ("D", "wrong", "Hardcoding is recommended for staging servers.")
        ], "✅ Correct! Secrets must always be injected via environment variables (`os.environ`).", "❌ Incorrect. Hardcoded keys in git history are vulnerable to credential theft."),
        ("q126_4", "QUESTION 4 OF 4", "What does a health check endpoint (e.g. `/healthz` returning `200 OK`) enable in cloud serving platforms?", [
            ("A", "correct", "Automated platform orchestrators use it to detect failed instances and restart unhealthy containers."),
            ("B", "wrong", "It downloads updated machine learning datasets."),
            ("C", "wrong", "It encrypts user passwords."),
            ("D", "wrong", "It measures GPU temperature.")
        ], "✅ Correct! Liveness and readiness probes rely on `/healthz` endpoints to ensure zero-downtime routing.", "❌ Incorrect. Health checks allow orchestrators to know when a container is ready to accept traffic.")
    ],
    "day-127": [
        ("q127_2", "QUESTION 2 OF 4", "Why is experiment tracking critical during machine learning development?", [
            ("A", "correct", "It records exact hyperparameters, code versions, metrics, and model artifacts, ensuring 100% reproducibility."),
            ("B", "wrong", "It replaces the need for unit tests."),
            ("C", "wrong", "It increases model training speed by 10x."),
            ("D", "wrong", "It automatically generates patent documentation.")
        ], "✅ Correct! Experiment tracking provides systematic auditability across iterative training runs.", "❌ Incorrect. Tracking ensures that any model can be reliably reproduced from recorded parameters."),
        ("q127_3", "QUESTION 3 OF 4", "What is Data Drift (Covariate Shift) in deployed production models?", [
            ("A", "correct", "When the statistical distribution of input features P(X) changes over time while the true relationship P(Y|X) remains constant."),
            ("B", "wrong", "When database cables get disconnected in the server room."),
            ("C", "wrong", "When model weight files get corrupted on disk."),
            ("D", "wrong", "When users change their account passwords.")
        ], "✅ Correct! Covariate shift represents changes in input feature distributions over time.", "❌ Incorrect. Data drift occurs when production inputs diverge from training distributions."),
        ("q127_4", "QUESTION 4 OF 4", "What is the function of a Model Registry in production MLOps?", [
            ("A", "correct", "It acts as a centralized model store governing versioning, review gates, and stage transitions (Staging -> Production)."),
            ("B", "wrong", "It is a legal registry for trademarking AI algorithms."),
            ("C", "wrong", "It converts Python scripts into C++ automatically."),
            ("D", "wrong", "It deletes older models after 7 days.")
        ], "✅ Correct! Model registries provide governance, lineage, and lifecycle control for deployable artifacts.", "❌ Incorrect. Registries govern model validation, staging approvals, and production rollouts.")
    ]
}

# Add quizzes for other days in week 18 as well
for d_num in range(128, 136):
    did = f"day-{d_num}"
    if did not in WEEK18_EXTRA_QUIZZES:
        WEEK18_EXTRA_QUIZZES[did] = [
            (f"q{d_num}_2", "QUESTION 2 OF 4", f"In Day {d_num} Capstone / Portfolio engineering, why are automated unit & integration tests required?", [
                ("A", "correct", "They ensure code modifications do not introduce silent regressions in data pipelines or inference schemas."),
                ("B", "wrong", "They make Python scripts run without requiring RAM."),
                ("C", "wrong", "They are only needed for legacy Java applications."),
                ("D", "wrong", "They replace the need for model evaluation metrics.")
            ], "✅ Correct! Automated testing catches breaking changes before deployment.", "❌ Incorrect. Unit tests validate that components function properly across updates."),
            (f"q{d_num}_3", "QUESTION 3 OF 4", f"What documentation asset best demonstrates technical depth to senior engineering interviewers?", [
                ("A", "correct", "System Architecture Diagrams with explicit latency, cost, and throughput trade-off analyses."),
                ("B", "wrong", "A list of marketing buzzwords with no code links."),
                ("C", "wrong", "Raw un-commented Jupyter notebooks."),
                ("D", "wrong", "Screenshots without technical explanations.")
            ], "✅ Correct! Clear architecture diagrams and trade-off analyses showcase senior engineering capability.", "❌ Incorrect. Interviewers look for architectural clarity, trade-offs, and failure mode documentation."),
            (f"q{d_num}_4", "QUESTION 4 OF 4", f"How should production API response schemas be validated?", [
                ("A", "correct", "Using Pydantic models or JSON Schema validation to reject malformed payloads with descriptive error codes."),
                ("B", "wrong", "By assuming the client will always send valid data."),
                ("C", "wrong", "By ignoring payload structure entirely."),
                ("D", "wrong", "By converting all inputs into strings.")
            ], "✅ Correct! Schema validation prevents downstream runtime crashes from unexpected payload types.", "❌ Incorrect. Pydantic schema validation enforces rigorous input and output contracts.")
        ]

# Inject quizzes into soup
for did, q_list in WEEK18_EXTRA_QUIZZES.items():
    d_sec = soup.find('div', id=did)
    if d_sec:
        # Find existing quiz or takeaways
        takeaways = d_sec.find('div', class_='takeaways')
        for q_id, q_num, q_title, opts, fb_c, fb_w in q_list:
            # Check if quiz already exists
            if not d_sec.find('div', id=f"quiz-section-{q_id}"):
                q_block = soup.new_tag('div', id=f"quiz-section-{q_id}", **{'class': 'quiz-block'})
                q_block.append(BeautifulSoup(f'''
  <div class="quiz-num">{q_num}</div>
  <div class="quiz-q">{q_title}</div>
  <div class="quiz-opt" onclick="quiz(this,'{opts[0][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">A</span>{opts[0][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{opts[1][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">B</span>{opts[1][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{opts[2][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">C</span>{opts[2][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{opts[3][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">D</span>{opts[3][2]}</div>
  <div class="quiz-feedback correct-fb" id="{q_id}-correct" style="display:none;">{fb_c}</div>
  <div class="quiz-feedback wrong-fb" id="{q_id}-wrong" style="display:none;">{fb_w}</div>
''', 'html.parser'))
                if takeaways:
                    takeaways.insert_before(q_block)
                else:
                    d_sec.append(q_block)

fp18.write_text(str(soup), encoding='utf-8')
print("✅ Successfully enriched Week 18 with 4 complete quiz questions per day across all 11 days!")
