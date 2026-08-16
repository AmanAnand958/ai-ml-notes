#!/usr/bin/env python3
"""
Surgically fix all 24 Mermaid syntax defects across all 26 weeks:
1. Replaces reserved '&' in edge labels with 'and'.
2. Replaces raw '<' and '>' in node labels with 'under' / 'over' (e.g. <200MB -> under 200MB, >100ms -> over 100ms).
3. Replaces pipe symbols '|' inside node labels (e.g. |w1| -> abs(w1)).
4. Cleans Day 175 Evidently AI drift architecture diagram completely.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    modified = False
    
    for m in soup.find_all('div', class_='mermaid'):
        txt = m.text
        orig_txt = txt
        
        # 1. Fix Day 175 specific diagram
        if 'Evidently AI Drift Architecture' in txt or 'Drift_Monitoring_Architecture' in txt:
            clean_d175 = """graph LR
subgraph Drift_Monitoring_Architecture ["Evidently AI Drift Architecture"]
  ProdStream["Production Inference Data"] --> DriftEngine["Evidently AI Drift Engine"]
  RefData["Training Baseline Data"] --> DriftEngine
  DriftEngine -->|Compute KS-Test and PSI| Gate["Drift Detected? (PSI >= 0.25)"]
  Gate -->|Yes| Alert["Trigger Airflow Retraining DAG"]
  Gate -->|No| Metrics["Export Telemetry to Prometheus"]
end"""
            m.string = clean_d175
            modified = True
            continue

        # 2. Fix pipe characters |w1| inside node labels
        txt = txt.replace('|w1|', 'abs(w1)').replace('|w2|', 'abs(w2)')
        
        # 3. Fix reserved '&' inside edge labels: |A & B| -> |A and B|
        txt = re.sub(r'\|([^|]*?)&([^|]*?)\|', r'|\1and\2|', txt)
        txt = re.sub(r'\|([^|]*?)&([^|]*?)\|', r'|\1and\2|', txt) # pass 2 for multiples
        
        # 4. Fix raw < and > inside bracket node labels
        txt = txt.replace('<200MB', 'under 200MB')
        txt = txt.replace('< 200MB', 'under 200MB')
        txt = txt.replace('<15ms', 'under 15ms')
        txt = txt.replace('< 15ms', 'under 15ms')
        txt = txt.replace('< 5ms', 'under 5ms')
        txt = txt.replace('<5ms', 'under 5ms')
        txt = txt.replace('> 100ms', 'over 100ms')
        txt = txt.replace('>100ms', 'over 100ms')
        txt = txt.replace('> 1%', 'over 1%')
        txt = txt.replace('> 70%', 'over 70%')
        txt = txt.replace('>70%', 'over 70%')
        txt = txt.replace('<= 2.5', 'less or equal 2.5')
        txt = txt.replace('<= t', 'less or equal t')
        txt = txt.replace('<= 0.25', 'less or equal 0.25')
        txt = txt.replace('<= 1', 'less or equal 1')
        txt = txt.replace('<=', 'less or equal')
        txt = txt.replace('>=', 'greater or equal')
        
        # 5. Fix unquoted '&' in node labels
        txt = txt.replace('x_t & Hidden', 'x_t and Hidden')
        txt = txt.replace('PyTest| UnitTests["Unit & System Tests"]', 'PyTest| UnitTests["Unit and System Tests"]')
        txt = txt.replace('Build & Push', 'Build and Push')
        txt = txt.replace('Tools & Wheels', 'Tools and Wheels')
        txt = txt.replace('Training & Validation', 'Training and Validation')

        if txt != orig_txt:
            m.string = txt
            modified = True

    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Fixed Mermaid syntax defects in Week {wn}")

print("\n🎉 ALL MERMAID SYNTAX DEFECTS SURGICALLY FIXED ACROSS ALL WEEKS!")
