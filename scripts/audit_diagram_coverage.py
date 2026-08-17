#!/usr/bin/env python3
"""
scripts/audit_diagram_coverage.py
Audits all 191 days across all 26 weeks for diagram coverage:
- Detects whether each day contains:
  1. SVG Diagrams (<svg ...>)
  2. Mermaid Architecture Diagrams (<div class="mermaid">...</div> or ```mermaid)
  3. Interactive HTML Canvas (<canvas ...>)
- Categorizes days with zero visual diagrams into:
  - Complex multi-component / mathematical days that urgently require diagrams
  - Straightforward syntax / setup days
"""

import glob, yaml, re, os, json

print("=== STARTING DIAGRAM & VISUALIZATION AUDIT ACROSS ALL 191 DAYS ===")

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
html_files = sorted(glob.glob('pages/weeks/week*.html'))

diagram_report = {
    "summary": {},
    "days_with_visuals": [],
    "days_missing_all_visuals": [],
    "high_priority_missing_diagrams": []
}

# Complex topics that should always have a visual diagram
COMPLEX_KEYWORDS = [
    'architecture', 'pipeline', 'neural network', 'cnn', 'rnn', 'transformer', 
    'attention', 'backprop', 'autograd', 'diffusion', 'quantization', 'distributed', 
    'ddp', 'fsdp', 'rag', 'vector', 'hnsw', 'vllm', 'batching', 'tree', 'reinforcement',
    'gradient', 'matrix', 'svd', 'eigen', 'kmeans', 'decision tree', 'resnet', 'bert', 'gpt'
]

total_days = 0

for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    hf = f"pages/weeks/week{w_num}.html"
    
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    
    html_content = ""
    if os.path.exists(hf):
        with open(hf, 'r', encoding='utf-8') as f:
            html_content = f.read()

    for d in ydata.get('days', []):
        total_days += 1
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        # Combine day text
        d_theory = str(d.get('theory_html', ''))
        
        # Check day slice in HTML
        day_html = ""
        day_match = re.search(rf'(<div class="day-section[^"]*" id="day-{d_num}".*?)(?=<div class="day-section|\Z)', html_content, re.DOTALL)
        if day_match:
            day_html = day_match.group(1)
            
        combined_markup = d_theory + "\n" + day_html
        
        has_svg = '<svg' in combined_markup.lower()
        has_mermaid = 'class="mermaid"' in combined_markup or 'class=\'mermaid\'' in combined_markup or '```mermaid' in combined_markup
        has_canvas = '<canvas' in combined_markup.lower()
        
        counts = {
            "svg_count": len(re.findall(r'<svg\b', combined_markup, re.IGNORECASE)),
            "mermaid_count": len(re.findall(r'class=[\"\']mermaid[\"\']', combined_markup, re.IGNORECASE)),
            "canvas_count": len(re.findall(r'<canvas\b', combined_markup, re.IGNORECASE))
        }
        
        is_visual = has_svg or has_mermaid or has_canvas
        
        entry = {
            "day_num": d_num,
            "week_num": w_num,
            "title": d_title,
            "location": d_loc,
            "has_svg": has_svg,
            "has_mermaid": has_mermaid,
            "has_canvas": has_canvas,
            "counts": counts
        }
        
        if is_visual:
            diagram_report["days_with_visuals"].append(entry)
        else:
            diagram_report["days_missing_all_visuals"].append(entry)
            
            # Check if this topic is complex and urgently needs a diagram
            t_lower = (d_title + " " + d_theory).lower()
            if any(k in t_lower for k in COMPLEX_KEYWORDS):
                diagram_report["high_priority_missing_diagrams"].append(entry)

diagram_report["summary"] = {
    "total_days": total_days,
    "days_with_visuals": len(diagram_report["days_with_visuals"]),
    "days_missing_all_visuals": len(diagram_report["days_missing_all_visuals"]),
    "high_priority_missing_diagrams_count": len(diagram_report["high_priority_missing_diagrams"]),
    "visual_coverage_percentage": f"{(len(diagram_report['days_with_visuals']) / total_days) * 100:.1f}%"
}

print(f"\nTotal Days Analyzed: {total_days}")
print(f"  • Days with Visuals (SVG/Mermaid/Canvas): {len(diagram_report['days_with_visuals'])} ({diagram_report['summary']['visual_coverage_percentage']})")
print(f"  • Days Missing All Visuals:              {len(diagram_report['days_missing_all_visuals'])}")
print(f"  • High-Priority Complex Days Needing Diagrams: {len(diagram_report['high_priority_missing_diagrams'])}")

with open('scripts/diagram_coverage_report.json', 'w', encoding='utf-8') as f:
    json.dump(diagram_report, f, indent=2)

print("\nSaved full diagram report to: scripts/diagram_coverage_report.json")
