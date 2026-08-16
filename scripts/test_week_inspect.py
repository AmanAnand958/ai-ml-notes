import re
from bs4 import BeautifulSoup

def audit_and_fix_week(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find day-section starts
    day_starts = list(re.finditer(r'<div class="day-section"[^>]*id="(day-[^"]+)"[^>]*>', html))
    if not day_starts:
        return
        
    print(f"\n--- Checking {fn} ({len(day_starts)} days) ---")
    soup = BeautifulSoup(html, 'html.parser')
    
    for d in soup.find_all('div', class_='day-section'):
        d_id = d.get('id', '')
        btn = d.find('button', class_='complete-btn')
        print(f"  {d_id}: parent={d.parent.name}, has_btn={btn is not None}, num_children={len(list(d.children))}")

audit_and_fix_week('pages/weeks/week8.html')
audit_and_fix_week('pages/weeks/week12.html')
