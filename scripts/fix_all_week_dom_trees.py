import glob, re
from bs4 import BeautifulSoup

print("=== FIXING ALL WEEK DOM TREES AND SIBLING CLOSURES ===")

# 1. Remove duplicate empty day-section blocks in week2, week3, week7
for fn, d_num in [('pages/weeks/week2.html', 14), ('pages/weeks/week3.html', 21), ('pages/weeks/week7.html', 51)]:
    with open(fn, 'r', encoding='utf-8') as f:
        t = f.read()
    pattern = rf'<div class="day-section"[^>]*id="day-{d_num}"[^>]*>\s*(?:<!--[^>]*-->\s*)*</div>'
    t_fixed = re.sub(pattern, '', t)
    if t_fixed != t:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(t_fixed)
        print(f"✓ Removed stray empty duplicate day-{d_num} in {fn}")

# 2. Fix the double </div> at the end of day sections in weeks 7, 8, 12, 13, 15, 16, 17, 20
for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Clean up double closing comments/divs that close main prematurely
    orig = html
    html = re.sub(r'</div>\s*</div>\s*(<!--\s*/day-\d+\s*-->)\s*<div class="day-section"', r'</div>\n\1\n<div class="day-section"', html)
    html = re.sub(r'</div>\s*</div>\s*<div class="day-section"', r'</div>\n<div class="day-section"', html)
    
    if html != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Rebalanced day section closing divs in {fn}")

# 3. Verify all day-sections in all 26 weeks
print("\n--- Verifying All Day Sections Parentage ---")
all_clean = True
for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    for ds in soup.find_all('div', class_='day-section'):
        d_id = ds.get('id', 'unknown')
        parent = ds.parent.name
        if parent != 'main':
            all_clean = False
            print(f"  ❌ {fn} #{d_id} has parent <{parent}> (expected <main>)")

if all_clean:
    print("🌟 100% OF ALL DAY SECTIONS ACROSS ALL 26 WEEKS ARE DIRECT SIBLINGS UNDER <main>!")
