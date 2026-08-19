#!/usr/bin/env python3
import os, glob, yaml, html
from bs4 import BeautifulSoup

DATA_DIR = 'src/data'
PAGES_DIR = 'pages/weeks'

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)
yaml.SafeDumper.add_representer(LiteralStr, lit_repr)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

print("=== REGENERATING CHECKLISTS FOR ALL 191 DAYS (DAYS 1-191) ===")

for yf in sorted(glob.glob('src/data/*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    
    for day in ydata.get('days', []):
        did = int(day.get('day_num') or day.get('id'))
        title = day.get('title', f'Day {did}')
        tasks = day.get('tasks', [])
        t1_title = tasks[0].get('title', 'Production Implementation') if tasks else 'Production Implementation'

        day['checklist'] = [
            {'id': f'chk_{did}_1', 'text': f'Master the core concepts, mathematical principles, and architecture of {title}'},
            {'id': f'chk_{did}_2', 'text': f'Complete hands-on implementation and test assertions for {t1_title}'},
            {'id': f'chk_{did}_3', 'text': f'Validate practical edge cases, performance trade-offs, and failure modes for Day {did}'},
            {'id': f'chk_{did}_4', 'text': 'Evaluate conceptual mastery via interactive flashcards and quiz challenges'}
        ]

    with open(yf, 'w', encoding='utf-8') as f:
        yaml.dump(deep_literal(ydata), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

# Sync to all HTML pages
for w in range(1, 27):
    hf = f'pages/weeks/week{w}.html'
    yf = f'src/data/week{w:02d}.yaml' if w < 10 else f'src/data/week{w}.yaml'
    if not os.path.exists(hf) or not os.path.exists(yf): continue

    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    for day in ydata.get('days', []):
        did = int(day.get('day_num') or day.get('id'))
        day_sec = soup.find('div', id=f'day-{did}')
        if not day_sec: continue

        chk_sec = day_sec.find('div', class_='checklist-section') or day_sec.find('div', id=f'checklist-section-{did}')
        if chk_sec:
            chk_items = day.get('checklist', [])
            chk_html = [f'<div class="checklist-section" id="checklist-section-{did}">', '<h2 class="sh2">✅ Daily Mastery Checklist</h2>', '<div class="chk-list">']
            for item in chk_items:
                cid = item.get('id', f'chk_{did}_1')
                ctext = html.escape(item.get('text', ''))
                chk_html.append(f'''<div class="chk-item" id="{cid}" onclick="toggleCheck('{cid}')" onkeydown="if(event.key==='Enter'||event.key===' ')toggleCheck('{cid}')" role="checkbox" tabindex="0" aria-checked="false">
<div class="chk-box"></div>
<div class="chk-label">{ctext}</div>
</div>''')
            chk_html.append('</div></div>')
            new_chk_soup = BeautifulSoup('\n'.join(chk_html), 'html.parser')
            chk_sec.replace_with(new_chk_soup.div)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("✓ Cleanly regenerated checklists for all 191 days across YAML and HTML!")
