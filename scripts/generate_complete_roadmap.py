#!/usr/bin/env python3
"""
scripts/generate_complete_roadmap.py
Generates a comprehensive, modern, 100% synchronized roadmap.html for all 191 Days (Weeks 1–26).
"""

import os, yaml, re, html

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')
OUTPUT_FILE = os.path.join(ROOT_DIR, 'roadmap.html')

# Load all 26 YAML files
weeks_data = []
for w in range(1, 27):
    yf = os.path.join(DATA_DIR, f'week{w:02d}.yaml')
    if not os.path.exists(yf):
        yf = os.path.join(DATA_DIR, f'week{w}.yaml')
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        data['week_num'] = w
        weeks_data.append(data)

def get_phase_info(week_num):
    if 1 <= week_num <= 4:
        return {'id': 'phase1', 'name': 'Phase 1: Foundations', 'label': 'MONTH 1 · DAYS 1–30', 'color': 'var(--m1)', 'border_class': 'm1'}
    elif 5 <= week_num <= 8:
        return {'id': 'phase2', 'name': 'Phase 2: Classical ML', 'label': 'MONTH 2 · DAYS 31–58', 'color': 'var(--m2)', 'border_class': 'm2'}
    elif 9 <= week_num <= 12:
        return {'id': 'phase3', 'name': 'Phase 3: Deep Learning & CV', 'label': 'MONTH 3 · DAYS 59–86', 'color': 'var(--m3)', 'border_class': 'm3'}
    elif 13 <= week_num <= 16:
        return {'id': 'phase4', 'name': 'Phase 4: NLP & Transformers', 'label': 'MONTH 4 · DAYS 87–117', 'color': 'var(--m4)', 'border_class': 'm4'}
    elif 17 <= week_num <= 18:
        return {'id': 'phase5', 'name': 'Phase 5: MLOps & Deployment', 'label': 'PHASE 5 · DAYS 118–135', 'color': 'var(--mfin)', 'border_class': 'mfin'}
    else:
        return {'id': 'phase6', 'name': 'Phase 6: Advanced GenAI & Scale', 'label': 'PHASE 6 · DAYS 136–191', 'color': 'var(--m6)', 'border_class': 'm6'}

def get_section_id(week_num):
    if 1 <= week_num <= 4: return f'm1w{week_num}'
    elif 5 <= week_num <= 8: return f'm2w{week_num}'
    elif 9 <= week_num <= 12: return f'm3w{week_num}'
    elif 13 <= week_num <= 16: return f'm4w{week_num}'
    elif week_num == 17: return 'fin1'
    elif week_num == 18: return 'fin2'
    elif 19 <= week_num <= 20: return f'm5w{week_num}'
    else: return f'm6w{week_num}'

# Build HTML
out = []
out.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>Master AI/ML Roadmap 2026 — 191 Days (26 Weeks)</title>
  <meta content="Comprehensive 191-Day AI/ML, GenAI, MLOps and Distributed Systems Learning Roadmap" name="description"/>
  <meta content="Master AI/ML Roadmap 2026 — 191 Days" property="og:title"/>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Syne:wght@500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400&display=swap');

    :root {
      --bg: #0b0d13;
      --bg2: #12151f;
      --bg3: #1a1e2c;
      --card: #161a27;
      --border: #262c40;
      --text: #e8ecf5;
      --muted: #7e88a3;
      --accent1: #6c8cff;
      --accent2: #4fd1a5;
      --accent3: #f7a94b;
      --accent4: #e56b8c;
      --accent5: #b47cfc;
      --m1: #4fd1a5;
      --m2: #6c8cff;
      --m3: #f7a94b;
      --m4: #e56b8c;
      --mfin: #b47cfc;
      --m6: #38bdf8;
      --font-head: 'Syne', sans-serif;
      --font-body: 'DM Sans', sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
    }

    [data-theme="light"] {
      --bg: #f8fafc;
      --bg2: #ffffff;
      --bg3: #f1f5f9;
      --card: #ffffff;
      --border: #e2e8f0;
      --text: #0f172a;
      --muted: #64748b;
      --accent1: #3b82f6;
      --accent2: #10b981;
      --accent3: #f59e0b;
      --accent4: #ef4444;
      --accent5: #8b5cf6;
      --m1: #059669;
      --m2: #2563eb;
      --m3: #d97706;
      --m4: #db2777;
      --mfin: #7c3aed;
      --m6: #0284c7;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 15px;
      line-height: 1.65;
      display: flex;
      min-height: 100vh;
    }

    /* ── SIDEBAR ── */
    #sidebar {
      width: 280px;
      min-width: 280px;
      background: rgba(18, 21, 31, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-right: 1px solid var(--border);
      height: 100vh;
      position: sticky;
      top: 0;
      overflow-y: auto;
      padding: 0 0 2rem;
      z-index: 100;
      scrollbar-width: thin;
      scrollbar-color: var(--border) transparent;
      transition: all 0.3s ease;
    }

    .sidebar-logo {
      padding: 1.5rem 1.25rem 1rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 0.5rem;
    }
    .sidebar-logo .logo-text {
      font-family: var(--font-head);
      font-weight: 800;
      font-size: 16px;
      color: var(--text);
      letter-spacing: -0.5px;
      line-height: 1.3;
    }
    .sidebar-logo .logo-sub {
      font-size: 12px;
      color: var(--accent1);
      font-family: var(--font-mono);
      margin-top: 3px;
      letter-spacing: 0.5px;
    }

    .nav-section { padding: 0.3rem 0; }
    .nav-section-label {
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--muted);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 0.75rem 1.25rem 0.25rem;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0.4rem 1.25rem;
      font-size: 12.5px;
      color: var(--muted);
      cursor: pointer;
      border-left: 2px solid transparent;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      font-family: var(--font-body);
      text-decoration: none;
    }
    .nav-item:hover { color: var(--text); background: rgba(255, 255, 255, 0.03); transform: translateX(3px); }
    .nav-item.active { color: var(--text); border-left-color: var(--accent1); background: rgba(108,140,255,0.08); font-weight: 600; }
    .nav-item .dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
    .nav-item .day-range { font-size: 11px; color: var(--muted); font-family: var(--font-mono); margin-left: auto; }

    /* ── MAIN ── */
    #main {
      flex: 1;
      overflow-y: auto;
      padding: 0;
    }

    /* ── HERO ── */
    .hero {
      background: var(--bg2);
      border-bottom: 1px solid var(--border);
      padding: 3.5rem 3rem 3rem;
      position: relative;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      top: -100px; right: -100px;
      width: 500px; height: 500px;
      background: radial-gradient(circle, rgba(108,140,255,0.15) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-badge {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--accent1);
      border: 1px solid rgba(108,140,255,0.3);
      padding: 4px 12px;
      border-radius: 20px;
      display: inline-block;
      margin-bottom: 1.25rem;
      background: rgba(108,140,255,0.05);
      letter-spacing: 0.5px;
    }
    .hero h1 {
      font-family: var(--font-head);
      font-size: 2.8rem;
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -1.5px;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, var(--text) 0%, var(--accent1) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      color: var(--muted);
      max-width: 720px;
      font-size: 15.5px;
      line-height: 1.7;
      margin-bottom: 1.8rem;
    }
    .hero-stats {
      display: flex;
      gap: 1.25rem;
      flex-wrap: wrap;
    }
    .hero-stat {
      background: var(--bg3);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.9rem 1.4rem;
      text-align: center;
      min-width: 130px;
    }
    .hero-stat .val {
      font-family: var(--font-head);
      font-size: 1.8rem;
      font-weight: 800;
      color: var(--accent1);
      line-height: 1.1;
    }
    .hero-stat .lbl {
      font-size: 11.5px;
      color: var(--muted);
      font-family: var(--font-mono);
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* ── SECTIONS ── */
    .section {
      display: none;
      padding: 2.5rem 3rem;
      max-width: 1200px;
    }
    .section.active { display: block; }

    .section-header {
      margin-bottom: 2rem;
      padding-bottom: 1.25rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .section-tag {
      font-size: 12px;
      font-family: var(--font-mono);
      letter-spacing: 1px;
      color: var(--muted);
      margin-bottom: 0.4rem;
      text-transform: uppercase;
    }
    .section-header h2 {
      font-family: var(--font-head);
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -1px;
      line-height: 1.2;
      margin-bottom: 0.4rem;
    }
    .section-header p {
      color: var(--muted);
      max-width: 750px;
      font-size: 14.5px;
    }
    .open-week-btn {
      font-family: var(--font-mono);
      font-size: 13px;
      color: #fff;
      background: var(--accent1);
      border: 1px solid var(--accent1);
      padding: 8px 16px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .open-week-btn:hover { background: #5577ff; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(108,140,255,0.3); }

    /* ── WEEK BLOCKS ── */
    .week-block {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      margin-bottom: 2rem;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .week-header {
      padding: 1.1rem 1.5rem;
      background: var(--bg3);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 1rem;
      cursor: pointer;
      transition: background 0.2s;
    }
    .week-header:hover { background: rgba(255, 255, 255, 0.04); }
    .week-num {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text);
      background: var(--bg);
      border: 1px solid var(--border);
      padding: 3px 9px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      font-weight: 600;
    }
    .week-title {
      font-family: var(--font-head);
      font-size: 16px;
      font-weight: 700;
      flex: 1;
    }
    .week-meta {
      font-size: 12.5px;
      color: var(--muted);
      font-family: var(--font-mono);
    }
    .week-content { padding: 1.5rem; }

    /* ── DAY CARDS ── */
    .days-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.25rem;
    }
    .day-card {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem 1.25rem;
      border-left: 4px solid var(--accent1);
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      text-decoration: none;
      color: inherit;
    }
    .day-card:hover {
      border-color: var(--accent1);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    .day-label {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--muted);
      letter-spacing: 1px;
      margin-bottom: 0.4rem;
      font-weight: 600;
    }
    .day-title {
      font-family: var(--font-head);
      font-size: 14.5px;
      font-weight: 700;
      margin-bottom: 0.6rem;
      line-height: 1.35;
      color: var(--text);
    }
    .day-desc {
      font-size: 12.5px;
      color: var(--muted);
      line-height: 1.5;
      margin-bottom: 0.75rem;
      flex: 1;
    }
    .day-list {
      list-style: none;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.6;
      margin-bottom: 0.75rem;
    }
    .day-list li::before {
      content: '→ ';
      color: var(--accent2);
      font-family: var(--font-mono);
    }
    .day-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 0.6rem;
      border-top: 1px solid var(--border);
      font-family: var(--font-mono);
      font-size: 11.5px;
    }
    .day-hours { color: var(--accent3); }
    .day-link { color: var(--accent1); text-decoration: none; font-weight: 500; }

    /* ── TOC GRID ── */
    .toc-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0 2.5rem;
    }
    .toc-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.1rem 1.25rem;
      cursor: pointer;
      transition: all 0.2s;
      border-top: 3px solid var(--accent1);
    }
    .toc-card:hover {
      background: var(--bg3);
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .toc-card .tc-month { font-family: var(--font-mono); font-size: 11px; color: var(--muted); letter-spacing: 1px; margin-bottom: 0.3rem; }
    .toc-card .tc-title { font-family: var(--font-head); font-size: 14.5px; font-weight: 700; margin-bottom: 0.3rem; color: var(--text); }
    .toc-card .tc-days { font-size: 12px; color: var(--muted); font-family: var(--font-mono); }

    /* ── MILESTONES & CALLOUTS ── */
    .milestone {
      background: linear-gradient(135deg, rgba(108,140,255,0.08) 0%, rgba(180,124,252,0.08) 100%);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.5rem;
      margin: 2rem 0;
      display: flex;
      gap: 1.25rem;
      align-items: flex-start;
    }
    .milestone-icon { font-size: 2rem; flex-shrink: 0; line-height: 1; }
    .milestone-content h3 { font-family: var(--font-head); font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .milestone-content p { font-size: 13.5px; color: var(--muted); margin-bottom: 0.75rem; }
    .milestone-checks { display: flex; flex-wrap: wrap; gap: 8px 16px; font-size: 12.5px; font-family: var(--font-mono); color: var(--accent2); }

    .callout {
      border-radius: 10px;
      padding: 1.25rem;
      margin: 1.25rem 0;
      border-left: 4px solid;
      background: var(--bg2);
      font-size: 13.5px;
    }
    .callout-info { border-color: var(--accent1); }
    .callout-tip { border-color: var(--accent2); }
    .callout-proj { border-color: var(--accent5); }

    /* ── TABLES ── */
    .resource-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin: 1.25rem 0;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .resource-table th {
      background: var(--bg3);
      color: var(--muted);
      font-family: var(--font-mono);
      font-size: 12px;
      letter-spacing: 0.5px;
      text-align: left;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
    }
    .resource-table td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }
    .resource-table tr:hover { background: rgba(255,255,255,0.02); }
    .resource-table a { color: var(--accent1); text-decoration: none; font-weight: 500; }
    .resource-table a:hover { text-decoration: underline; }

    /* ── PROJECT GRIDS ── */
    .proj-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.25rem;
      margin: 1rem 0 2rem;
    }
    .proj-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
    }
    .proj-card h3 { font-family: var(--font-head); font-size: 15px; font-weight: 700; margin-bottom: 0.4rem; color: var(--text); }
    .proj-card p { font-size: 12.5px; color: var(--muted); line-height: 1.5; margin-bottom: 0.75rem; flex: 1; }
    .proj-tags { display: flex; flex-wrap: wrap; gap: 6px; }
    .proj-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      background: var(--bg3);
      border: 1px solid var(--border);
      padding: 2px 7px;
      border-radius: 4px;
      color: var(--accent2);
    }

    /* ── THEME BTN ── */
    #theme-btn {
      position: fixed;
      top: 16px;
      right: 20px;
      background: var(--card);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      z-index: 9999;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      font-family: var(--font-mono);
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    #theme-btn:hover { transform: scale(1.05); }

    /* ── RESPONSIVE ── */
    @media (max-width: 860px) {
      #sidebar { display: none; }
      .section { padding: 1.5rem; }
      .hero { padding: 2rem 1.5rem; }
      .hero h1 { font-size: 2rem; }
      .days-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <button id="theme-btn" onclick="toggleTheme()">🌓 Theme</button>

  <!-- SIDEBAR -->
  <aside id="sidebar">
    <div class="sidebar-logo">
      <div class="logo-text">AI/ML Roadmap 2026</div>
      <div class="logo-sub">191 DAYS · 26 WEEKS</div>
    </div>

    <div class="nav-section">
      <div class="nav-section-label">General</div>
      <div class="nav-item active" onclick="showSection('overview')">
        <span class="dot" style="background:var(--accent1)"></span>
        Master Overview
      </div>
      <div class="nav-item" onclick="showSection('techstack')">
        <span class="dot" style="background:var(--accent2)"></span>
        Tech Stack
      </div>
    </div>
''')

# Sidebar weeks navigation
current_phase_header = None
for w_data in weeks_data:
    w_num = w_data['week_num']
    phase = get_phase_info(w_num)
    sec_id = get_section_id(w_num)
    
    if phase['name'] != current_phase_header:
        current_phase_header = phase['name']
        out.append(f'''    <div class="nav-section">
      <div class="nav-section-label">{phase['name']}</div>''')
        
    days = w_data.get('days', [])
    start_d = days[0].get('day_num', 1) if days else 1
    end_d = days[-1].get('day_num', 1) if days else 1
    
    title = w_data.get('title', f'Week {w_num}')
    out.append(f'''      <div class="nav-item" onclick="showSection('{sec_id}')">
        <span class="dot" style="background:{phase['color']}"></span>
        <span>Week {w_num}</span>
        <span class="day-range">{start_d}–{end_d}</span>
      </div>''')

out.append('''    </div>

    <div class="nav-section">
      <div class="nav-section-label">Reference</div>
      <div class="nav-item" onclick="showSection('projects')">
        <span class="dot" style="background:var(--accent5)"></span>
        All Projects
      </div>
      <div class="nav-item" onclick="showSection('interview')">
        <span class="dot" style="background:var(--accent3)"></span>
        Interview Prep
      </div>
      <div class="nav-item" onclick="showSection('resources')">
        <span class="dot" style="background:var(--accent2)"></span>
        Resource Master List
      </div>
      <div class="nav-item" onclick="showSection('career')">
        <span class="dot" style="background:var(--accent1)"></span>
        Career Roadmap
      </div>
      <div class="nav-item" onclick="showSection('advice')">
        <span class="dot" style="background:var(--accent4)"></span>
        Final Advice
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main id="main">

    <!-- OVERVIEW SECTION -->
    <div class="section active" id="overview">
      <div class="hero">
        <div class="hero-badge">THE COMPLETE 2026 ARCHITECTURE ROADMAP</div>
        <h1>191-Day AI/ML, GenAI &amp; MLOps Mastery</h1>
        <p>From core Python &amp; Mathematics to Transformers, Hybrid RAG, Multi-Agent Systems, vLLM PagedAttention, and Distributed Kubernetes Infrastructure. Zero prerequisites to Enterprise AI Engineer.</p>
        <div class="hero-stats">
          <div class="hero-stat"><div class="val">191</div><div class="lbl">Days Total</div></div>
          <div class="hero-stat"><div class="val">26</div><div class="lbl">Weeks</div></div>
          <div class="hero-stat"><div class="val">6</div><div class="lbl">Mastery Phases</div></div>
          <div class="hero-stat"><div class="val">20+</div><div class="lbl">Capstone Projects</div></div>
        </div>
      </div>

      <h2 style="font-family:var(--font-head); font-size:1.6rem; font-weight:700; margin:2.5rem 0 1rem;">Curriculum Map &amp; Table of Contents</h2>
      <div class="toc-grid">''')

for w_data in weeks_data:
    w_num = w_data['week_num']
    phase = get_phase_info(w_num)
    sec_id = get_section_id(w_num)
    days = w_data.get('days', [])
    start_d = days[0].get('day_num', 1) if days else 1
    end_d = days[-1].get('day_num', 1) if days else 1
    title = w_data.get('title', f'Week {w_num}')
    
    out.append(f'''        <div class="toc-card" onclick="showSection('{sec_id}')" style="border-top-color:{phase['color']}">
          <div class="tc-month">WEEK {w_num:02d} · {phase['name'].split(':')[0]}</div>
          <div class="tc-title">{html.escape(title)}</div>
          <div class="tc-days">Days {start_d}–{end_d} · {len(days)} Lessons →</div>
        </div>''')

out.append('''      </div>

      <div class="milestone">
        <div class="milestone-icon">🗺️</div>
        <div class="milestone-content">
          <h3>The 6-Phase Progression Path</h3>
          <p>This curriculum is engineered to build compounding competence across mathematical theory, machine learning intuition, and production software engineering.</p>
          <div class="milestone-checks">
            <span>Phase 1 (W1-4): Python, Pandas &amp; Math</span>
            <span>Phase 2 (W5-8): Classical ML &amp; Deep Learning</span>
            <span>Phase 3 (W9-12): Computer Vision, GANs &amp; Sequences</span>
            <span>Phase 4 (W13-16): NLP, Transformers &amp; LLMs</span>
            <span>Phase 5 (W17-18): Docker, K8s &amp; MLOps Deployment</span>
            <span>Phase 6 (W19-26): Advanced RAG, Agents, vLLM &amp; Scale</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TECH STACK SECTION -->
    <div class="section" id="techstack">
      <div class="section-header">
        <div>
          <div class="section-tag">TOOLING &amp; FRAMEWORKS</div>
          <h2>Production AI Engineering Tech Stack</h2>
          <p>Industry-standard technologies used throughout all 191 days of the curriculum.</p>
        </div>
      </div>

      <div class="proj-grid">
        <div class="proj-card">
          <h3>Core Languages &amp; Compute</h3>
          <p>Python 3.11+, NumPy, SciPy, Pandas, Polars, SQL (PostgreSQL), Bash scripting.</p>
          <div class="proj-tags"><span class="proj-tag">Python</span><span class="proj-tag">SQL</span><span class="proj-tag">NumPy</span></div>
        </div>
        <div class="proj-card">
          <h3>Machine Learning &amp; Math</h3>
          <p>Scikit-learn, XGBoost, LightGBM, Optuna, SciPy, Statsmodels, Matplotlib, Seaborn.</p>
          <div class="proj-tags"><span class="proj-tag">scikit-learn</span><span class="proj-tag">XGBoost</span><span class="proj-tag">Optuna</span></div>
        </div>
        <div class="proj-card">
          <h3>Deep Learning &amp; CV</h3>
          <p>PyTorch 2.x, Torchvision, Torchaudio, Hugging Face Transformers, OpenCV.</p>
          <div class="proj-tags"><span class="proj-tag">PyTorch</span><span class="proj-tag">HuggingFace</span><span class="proj-tag">OpenCV</span></div>
        </div>
        <div class="proj-card">
          <h3>LLMs &amp; Agentic AI</h3>
          <p>vLLM, LangGraph, LlamaIndex, Instructor, Qdrant, ChromaDB, FAISS, DSPy.</p>
          <div class="proj-tags"><span class="proj-tag">vLLM</span><span class="proj-tag">LangGraph</span><span class="proj-tag">Qdrant</span></div>
        </div>
        <div class="proj-card">
          <h3>MLOps &amp; Infrastructure</h3>
          <p>Docker, Kubernetes, Helm, MLflow, DVC, Apache Airflow, GitHub Actions CI/CD.</p>
          <div class="proj-tags"><span class="proj-tag">Docker</span><span class="proj-tag">Kubernetes</span><span class="proj-tag">MLflow</span></div>
        </div>
        <div class="proj-card">
          <h3>Observability &amp; Guardrails</h3>
          <p>OpenTelemetry, Arize Phoenix, RAGAS, Evidently AI, Prometheus, Grafana.</p>
          <div class="proj-tags"><span class="proj-tag">OpenTelemetry</span><span class="proj-tag">RAGAS</span><span class="proj-tag">Prometheus</span></div>
        </div>
      </div>
    </div>
''')

# Build individual Week Sections (Week 1 to 26)
for w_data in weeks_data:
    w_num = w_data['week_num']
    phase = get_phase_info(w_num)
    sec_id = get_section_id(w_num)
    days = w_data.get('days', [])
    start_d = days[0].get('day_num', 1) if days else 1
    end_d = days[-1].get('day_num', 1) if days else 1
    title = w_data.get('title', f'Week {w_num}')
    subtitle = w_data.get('subtitle', '')
    
    out.append(f'''    <!-- WEEK {w_num} SECTION -->
    <div class="section" id="{sec_id}">
      <div class="section-header">
        <div>
          <div class="section-tag">{phase['label']}</div>
          <h2>Week {w_num} — {html.escape(title)}</h2>
          <p>{html.escape(subtitle) if subtitle else f"Comprehensive {len(days)}-day curriculum covering {html.escape(title)}."}</p>
        </div>
        <div>
          <a href="pages/weeks/week{w_num}.html" class="open-week-btn" target="_blank">
            Open Interactive Week Portal ↗
          </a>
        </div>
      </div>

      <div class="week-block" style="border-top:3px solid {phase['color']};">
        <div class="week-header" onclick="window.location.href='pages/weeks/week{w_num}.html'">
          <span class="week-num">WEEK {w_num}</span>
          <div class="week-title">{html.escape(title)}</div>
          <div class="week-meta">Days {start_d}–{end_d} · {len(days)} Days · ~5-6 hrs/day</div>
        </div>
        <div class="week-content">
          <div class="days-grid">''')
          
    for day in days:
        d_num = day.get('day_num') or day.get('id')
        d_title = day.get('title', f'Day {d_num}')
        d_time = day.get('time_estimate', '⏱ 5 hours')
        d_sub = day.get('subtitle', '')
        objectives = day.get('objectives', [])
        
        out.append(f'''            <a class="day-card" href="pages/weeks/week{w_num}.html#day-{d_num}" style="border-left-color:{phase['color']};">
              <div class="day-label">DAY {d_num}</div>
              <div class="day-title">{html.escape(d_title)}</div>''')
        
        if d_sub:
            out.append(f'''              <div class="day-desc">{html.escape(d_sub[:120])}{'...' if len(d_sub) > 120 else ''}</div>''')
            
        if objectives and isinstance(objectives, list):
            out.append('              <ul class="day-list">')
            for obj in objectives[:3]:
                clean_obj = html.escape(str(obj))
                out.append(f'                <li>{clean_obj[:90]}{"..." if len(clean_obj)>90 else ""}</li>')
            out.append('              </ul>')
            
        out.append(f'''              <div class="day-footer">
                <span class="day-hours">{html.escape(d_time)}</span>
                <span class="day-link">Open Lesson →</span>
              </div>
            </a>''')

    out.append(f'''          </div>
        </div>
      </div>
    </div>''')

# Reference Sections
out.append('''    <!-- ALL PROJECTS -->
    <div class="section" id="projects">
      <div class="section-header">
        <div>
          <div class="section-tag">PORTFOLIO PORTFOLIO</div>
          <h2>Complete Project Roadmap</h2>
          <p>All 20+ production-grade portfolio projects built across the 191 days.</p>
        </div>
      </div>

      <h3 style="font-family:var(--font-head); font-size:1.3rem; margin:1.5rem 0 1rem; color:var(--m1);">Phase 1 &amp; 2: Foundations &amp; Classical ML</h3>
      <div class="proj-grid">
        <div class="proj-card"><h3>1. CLI Contact Book &amp; Log Parser</h3><p>Command-line CRUD app with file persistence and OOP design.</p><div class="proj-tags"><span class="proj-tag">Python</span><span class="proj-tag">OOP</span></div></div>
        <div class="proj-card"><h3>2. Exploratory Data Analysis (EDA)</h3><p>Production data exploration with 10+ statistical insights and Seaborn heatmaps.</p><div class="proj-tags"><span class="proj-tag">Pandas</span><span class="proj-tag">Seaborn</span></div></div>
        <div class="proj-card"><h3>3. House Price Regression Pipeline</h3><p>End-to-end regression with Ridge, Lasso, and XGBoost tuning.</p><div class="proj-tags"><span class="proj-tag">XGBoost</span><span class="proj-tag">scikit-learn</span></div></div>
        <div class="proj-card"><h3>4. Customer Churn Predictor + SHAP</h3><p>Classification with feature importance, ROC-AUC, and SHAP explainability.</p><div class="proj-tags"><span class="proj-tag">SHAP</span><span class="proj-tag">RandomForest</span></div></div>
      </div>

      <h3 style="font-family:var(--font-head); font-size:1.3rem; margin:1.5rem 0 1rem; color:var(--m3);">Phase 3 &amp; 4: Deep Learning, Vision &amp; NLP</h3>
      <div class="proj-grid">
        <div class="proj-card"><h3>5. Plant Disease CNN Classifier</h3><p>MobileNetV2 transfer learning with data augmentation and Gradio demo.</p><div class="proj-tags"><span class="proj-tag">PyTorch</span><span class="proj-tag">CNN</span></div></div>
        <div class="proj-card"><h3>6. BiLSTM Sentiment Analyzer</h3><p>Bidirectional LSTM sequence model on IMDB reviews with word embeddings.</p><div class="proj-tags"><span class="proj-tag">LSTM</span><span class="proj-tag">PyTorch</span></div></div>
        <div class="proj-card"><h3>7. DCGAN Synthetic Generator</h3><p>Deep Convolutional GAN for generating realistic image distributions.</p><div class="proj-tags"><span class="proj-tag">GAN</span><span class="proj-tag">PyTorch</span></div></div>
        <div class="proj-card"><h3>8. Image Captioning with Attention</h3><p>CNN image encoder + Transformer decoder with cross-attention.</p><div class="proj-tags"><span class="proj-tag">Attention</span><span class="proj-tag">Transformers</span></div></div>
      </div>

      <h3 style="font-family:var(--font-head); font-size:1.3rem; margin:1.5rem 0 1rem; color:var(--m6);">Phase 5 &amp; 6: GenAI, RAG, Agents &amp; Scale</h3>
      <div class="proj-grid">
        <div class="proj-card"><h3>9. Enterprise Hybrid RAG System</h3><p>Dense + BM25 search with Reciprocal Rank Fusion, Cross-Encoder reranking, and RAGAS evaluation.</p><div class="proj-tags"><span class="proj-tag">RAG</span><span class="proj-tag">RRF</span><span class="proj-tag">Qdrant</span></div></div>
        <div class="proj-card"><h3>10. GraphRAG Knowledge Engine</h3><p>Neo4j entity-relation triples with Leiden community summarization.</p><div class="proj-tags"><span class="proj-tag">GraphRAG</span><span class="proj-tag">Neo4j</span></div></div>
        <div class="proj-card"><h3>11. Autonomous Multi-Agent Swarm</h3><p>LangGraph StateGraph supervisor with tool execution and Human-in-the-loop gating.</p><div class="proj-tags"><span class="proj-tag">LangGraph</span><span class="proj-tag">Agents</span></div></div>
        <div class="proj-card"><h3>12. Production vLLM K8s Serving</h3><p>Custom fine-tuned Llama-3 deployment on Kubernetes with HPA and OpenTelemetry tracing.</p><div class="proj-tags"><span class="proj-tag">vLLM</span><span class="proj-tag">Kubernetes</span><span class="proj-tag">OTel</span></div></div>
      </div>
    </div>

    <!-- INTERVIEW PREP -->
    <div class="section" id="interview">
      <div class="section-header">
        <div>
          <div class="section-tag">CAREER READINESS</div>
          <h2>Interview Preparation Roadmap</h2>
          <p>Core algorithmic, statistical, and system design defense questions for AI/ML roles.</p>
        </div>
      </div>

      <table class="resource-table">
        <tr><th>#</th><th>Interview Question</th><th>Core Technical Defense Points</th></tr>
        <tr><td>1</td><td>Bias-Variance Tradeoff</td><td>Bias = underfitting, Variance = overfitting. Model capacity increases variance. Regularization ($L_1/L_2$) and bagging reduce variance.</td></tr>
        <tr><td>2</td><td>Precision vs Recall</td><td>Precision prioritizes low false positives (spam, fraud alerts). Recall prioritizes low false negatives (disease detection). F1 / PR-AUC for imbalance.</td></tr>
        <tr><td>3</td><td>Self-Attention Complexity</td><td>$O(N^2 \cdot d)$ sequence length bottleneck. FlashAttention tiling and FlashDecoding optimize SRAM memory access.</td></tr>
        <tr><td>4</td><td>Dense vs Sparse Retrieval</td><td>Dense captures synonyms via continuous hyperspheres; Sparse (BM25) guarantees exact token precision. RRF fuses them ordinally.</td></tr>
        <tr><td>5</td><td>PagedAttention Mechanics</td><td>Eliminates KV cache fragmentation by allocating non-contiguous physical GPU VRAM blocks via virtual block tables.</td></tr>
        <tr><td>6</td><td>LoRA &amp; QLoRA</td><td>Decomposes weight updates $\Delta W = B \cdot A$ with low rank $r \ll d$. QLoRA quantizes base weights to 4-bit NormalFloat (NF4).</td></tr>
      </table>
    </div>

    <!-- RESOURCES -->
    <div class="section" id="resources">
      <div class="section-header">
        <div>
          <div class="section-tag">CURATED REFERENCES</div>
          <h2>Free Resource Master List</h2>
          <p>High-yield textbooks, research papers, and open-source GitHub repositories.</p>
        </div>
      </div>

      <table class="resource-table">
        <tr><th>Resource</th><th>Author / Institution</th><th>Link</th></tr>
        <tr><td><strong>Deep Learning Bible</strong></td><td>Ian Goodfellow, Yoshua Bengio, Aaron Courville</td><td><a href="https://www.deeplearningbook.org/" target="_blank">deeplearningbook.org →</a></td></tr>
        <tr><td><strong>Mathematics for Machine Learning</strong></td><td>Deisenroth, Faisal, Ong</td><td><a href="https://mml-book.github.io/" target="_blank">mml-book.github.io →</a></td></tr>
        <tr><td><strong>Attention Is All You Need (2017)</strong></td><td>Vaswani et al. (Google Brain)</td><td><a href="https://arxiv.org/abs/1706.03762" target="_blank">arXiv:1706.03762 →</a></td></tr>
        <tr><td><strong>vLLM &amp; PagedAttention (2023)</strong></td><td>Woosuk Kwon et al. (UC Berkeley)</td><td><a href="https://arxiv.org/abs/2309.06180" target="_blank">arXiv:2309.06180 →</a></td></tr>
      </table>
    </div>

    <!-- CAREER -->
    <div class="section" id="career">
      <div class="section-header">
        <div>
          <div class="section-tag">INDUSTRY NAVIGATION</div>
          <h2>AI Engineer Career Roadmap</h2>
          <p>Strategic career trajectory across ML Engineering, GenAI Applications, and Distributed AI Infrastructure.</p>
        </div>
      </div>

      <table class="resource-table">
        <tr><th>Role</th><th>Primary Competencies</th><th>Benchmark Target Stack</th></tr>
        <tr><td><strong>AI / GenAI Engineer</strong></td><td>RAG, Agents, LLM Evaluation, APIs</td><td>LangGraph, LlamaIndex, vLLM, Qdrant</td></tr>
        <tr><td><strong>MLOps / Platform Engineer</strong></td><td>Containerization, Kubernetes, CI/CD, Drift</td><td>Docker, K8s, Helm, MLflow, Prometheus</td></tr>
        <tr><td><strong>Machine Learning Engineer</strong></td><td>Feature Engineering, Training Loops, Optimization</td><td>PyTorch, XGBoost, ONNX, CUDA</td></tr>
      </table>
    </div>

    <!-- ADVICE -->
    <div class="section" id="advice">
      <div class="section-header">
        <div>
          <div class="section-tag">CLOSING THOUGHTS</div>
          <h2>Final Advice from Your Roadmap Architect</h2>
        </div>
      </div>

      <div class="callout callout-tip">
        <strong>🎯 The Compounding Principle:</strong><br/>
        191 days of consistent, deliberate execution builds an unshakeable engineering foundation. Consistency beats intensity. Commit code daily, document architecture decision records, profile latency, and build in public.
      </div>
    </div>
  </main>

  <script>
    function showSection(id) {
      document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      
      const target = document.getElementById(id);
      if (target) {
        target.classList.add('active');
        window.scrollTo({top: 0, behavior: 'smooth'});
      }
      
      // Highlight sidebar item
      const navItems = document.querySelectorAll('.nav-item');
      navItems.forEach(item => {
        if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(id)) {
          item.classList.add('active');
        }
      });
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    }

    // Initialize saved theme
    (function() {
      const saved = localStorage.getItem('theme');
      if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
      }
    })();
  </script>
</body>
</html>
''')

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"🎉 Successfully generated {OUTPUT_FILE} with all 191 days and 26 weeks!")
