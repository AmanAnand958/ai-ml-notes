#!/usr/bin/env python3
"""
Step 1: Enrich Week 23 (Days 166, 168, 169) with deep enterprise theory and architecture.
- Day 166: Serverless ML with Lambda (Provisioned Concurrency, 10GB container image support, cold-start mitigation).
- Day 168: The 5 Cost Drivers (FinOps cost optimization formulas, Spot vs On-Demand GPU arbitrage, Egress traffic caching).
- Day 169: Secrets Management (AWS Secrets Manager, KMS envelope encryption, IAM least-privilege role assumption).
"""

from pathlib import Path
from bs4 import BeautifulSoup

fp23 = Path("pages/weeks/week23.html")
if fp23.exists():
    soup23 = BeautifulSoup(fp23.read_text(encoding='utf-8'), 'html.parser')
    
    # 1. Day 166: Serverless ML
    d166 = soup23.find('div', id='day-166')
    if d166 and not d166.find(id='lambda-deep-dive'):
        theory = d166.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="lambda-deep-dive" style="margin: 1.2rem 0; line-height: 1.7; font-size: 14px;">
  <p>Deploying machine learning models to <strong>AWS Lambda</strong> offers massive cost efficiency for intermittent traffic (zero idle costs), but introduces two architectural hurdles:</p>
  
  <div style="background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 14px; margin: 1rem 0;">
    <h4 style="color: var(--accent); margin-top: 0; margin-bottom: 8px; font-size: 14px;">⚡ Serverless ML Architecture & Mitigation Patterns:</h4>
    <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: var(--text);">
      <li><strong>10GB Container Image Support:</strong> Standard zip deployments cap at 250MB (too small for PyTorch/TensorFlow). Packaging model weights into a multi-stage Docker container image uploaded to Amazon ECR supports up to 10GB images.</li>
      <li><strong>Cold Start Elimination (Provisioned Concurrency):</strong> Standard serverless invocations incur a 2–6 second cold start initializing Python runtimes and loading weights. Configuring <em>Provisioned Concurrency</em> keeps a pool of warm execution environments ready for sub-20ms P99 responses.</li>
      <li><strong>Model Weight Caching in <code>/tmp</code> (Ephemeral Storage):</strong> Mounting up to 10GB of fast ephemeral storage in <code>/tmp</code> allows the Lambda handler to download model weights once on container init and reuse the in-memory graph across thousands of warm warm invocations.</li>
    </ul>
  </div>
</div>
''', 'html.parser')
            theory.insert_after(section)
            print("  ✅ Enriched Day 166 (Serverless Lambda) in Week 23!")

    # 2. Day 168: Cost Optimization & FinOps
    d168 = soup23.find('div', id='day-168')
    if d168 and not d168.find(id='cost-deep-dive'):
        theory = d168.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="cost-deep-dive" style="margin: 1.2rem 0; line-height: 1.7; font-size: 14px;">
  <p><strong>Cloud AI/ML Cost Engineering (FinOps):</strong> Untracked GPU training and endpoint hosting can bankrupt startups. Production ML infrastructure budgets are dominated by five drivers:</p>
  
  <div class="table-wrap" style="overflow-x:auto; margin:1.2rem 0; width:100%;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:13px;">
      <thead style="background:var(--bg3); border-bottom:1px solid var(--border);">
        <tr>
          <th style="padding:10px; text-align:left; color:var(--accent);">Cost Vector</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Typical Waste Mechanism</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Production Mitigation Strategy</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">GPU Compute (65%)</td>
          <td style="padding:10px;">Over-provisioning On-Demand A100s for offline batch workloads</td>
          <td style="padding:10px;">Use <strong>Spot Instances (60–80% savings)</strong> with checkpoint fault-tolerance and Savings Plans for baseline inference</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">Data Egress (15%)</td>
          <td style="padding:10px;">Transferring multi-TB embedding sets across different AWS regions</td>
          <td style="padding:10px;">Co-locate inference clusters in the same VPC/Region as S3 buckets and use VPC Endpoints (S3 Gateway)</td>
        </tr>
        <tr>
          <td style="padding:10px; font-weight:600;">Idle Endpoint VRAM (12%)</td>
          <td style="padding:10px;">Dedicated GPU instances running 24/7 during zero-traffic night hours</td>
          <td style="padding:10px;">Implement <strong>Serverless Inference or Scale-to-Zero</strong> Horizontal Pod Autoscaling (HPA) via KEDA</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
''', 'html.parser')
            theory.insert_after(section)
            print("  ✅ Enriched Day 168 (Cost Optimization) in Week 23!")

    # 3. Day 169: Secrets Management
    d169 = soup23.find('div', id='day-169')
    if d169 and not d169.find(id='secrets-deep-dive'):
        theory = d169.find('h2', class_='sh2')
        if theory:
            section = BeautifulSoup('''
<div id="secrets-deep-dive" style="margin: 1.2rem 0; line-height: 1.7; font-size: 14px;">
  <p><strong>Zero-Trust Secrets Management in ML Systems:</strong> Machine learning pipelines interact with dozens of privileged credentials (Hugging Face tokens, OpenAI API keys, database connection strings, S3 service accounts). Hardcoding keys in Git or baking them into Docker layers violates compliance and exposes enterprise infrastructure.</p>
  
  <div style="background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 14px; margin: 1rem 0;">
    <h4 style="color: var(--accent); margin-top: 0; margin-bottom: 8px; font-size: 14px;">🔐 Enterprise Secrets Architecture:</h4>
    <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: var(--text);">
      <li><strong>KMS Envelope Encryption:</strong> AWS Secrets Manager encrypts data using a Customer Master Key (CMK). The plaintext secret exists only in volatile memory inside the inference container and is never written to disk.</li>
      <li><strong>IAM Role-Based Identity (No Long-Lived Access Keys):</strong> EC2, EKS, and Lambda services assume temporary STS IAM credentials through instance profiles and service accounts (IRSA), eliminating static <code>AWS_ACCESS_KEY_ID</code> tokens.</li>
      <li><strong>Automated Rotation:</strong> Secrets Manager invokes a rotation Lambda function on a 30-day schedule to regenerate database passwords and update client caches without service interruption.</li>
    </ul>
  </div>
</div>
''', 'html.parser')
            theory.insert_after(section)
            print("  ✅ Enriched Day 169 (Secrets Management) in Week 23!")

    fp23.write_text(str(soup23), encoding='utf-8')
    print("✅ Week 23 successfully upgraded!")
