#!/usr/bin/env python3
"""
Step 1: Enrich Kubernetes Core Concepts (Week 25 Day 178) with ConfigMaps, Secrets, Ingress, and Namespaces.
"""

from pathlib import Path
from bs4 import BeautifulSoup

fp25 = Path("pages/weeks/week25.html")
soup = BeautifulSoup(fp25.read_text(encoding='utf-8'), 'html.parser')

d178 = soup.find('div', id='day-178')
if d178:
    theory = d178.find('h2', class_='sh2', id='day-178-theory') or d178.find('h2', class_='sh2')
    if theory:
        # Check if already enriched
        if not d178.find(id='k8s-primitives-enriched'):
            enriched_section = BeautifulSoup('''
<div id="k8s-primitives-enriched" style="margin: 1.5rem 0;">
  <h3 class="sh3">Core Kubernetes Primitives for Machine Learning Workloads</h3>
  <div class="table-wrap" style="overflow-x:auto; margin:1.2rem 0; width:100%;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:13px;">
      <thead style="background:var(--bg3); border-bottom:1px solid var(--border);">
        <tr>
          <th style="padding:10px; text-align:left; color:var(--accent);">Primitive</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">ML Purpose</th>
          <th style="padding:10px; text-align:left; color:var(--accent);">Key Best Practice</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">ConfigMap</td>
          <td style="padding:10px;">Stores non-confidential configs (model paths, batch size, vLLM max context length)</td>
          <td style="padding:10px;">Mount as volume or environment variables; decoupling parameters from Docker images</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">Secret</td>
          <td style="padding:10px;">Stores sensitive credentials (Hugging Face tokens, AWS S3 access keys, API keys)</td>
          <td style="padding:10px;">Use HashiCorp Vault or AWS Secrets Manager synced via External Secrets Operator</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border);">
          <td style="padding:10px; font-weight:600;">Ingress & IngressRoute</td>
          <td style="padding:10px;">Routes external HTTP/gRPC traffic with TLS termination to internal inference services</td>
          <td style="padding:10px;">Use Traefik or Envoy Ingress with HTTP/2 and streaming support for LLM token streaming</td>
        </tr>
        <tr>
          <td style="padding:10px; font-weight:600;">Namespace & ResourceQuota</td>
          <td style="padding:10px;">Partitions cluster resources and enforces maximum GPU quotas across engineering teams</td>
          <td style="padding:10px;">Define hard limits on <code>requests.nvidia.com/gpu</code> per namespace to avoid starvation</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
''', 'html.parser')
            theory.insert_after(enriched_section)
            fp25.write_text(str(soup), encoding='utf-8')
            print("✅ 1. Enriched Kubernetes Core Primitives in Week 25 Day 178!")
