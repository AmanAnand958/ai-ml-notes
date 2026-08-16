import glob, re
from bs4 import BeautifulSoup

print("=== SOLVING ALL DAY NESTING ISSUES ACROSS ALL 26 WEEKS ===")

for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # While any day is nested inside another day, insert a </div> before the nested day
    # Run iterations until all days are direct children of main
    changed = False
    for iteration in range(10):
        soup = BeautifulSoup(html, 'html.parser')
        nested_days = []
        for ds in soup.find_all('div', class_='day-section'):
            if ds.parent.name != 'main':
                nested_days.append(ds.get('id'))
        
        if not nested_days:
            break
            
        # For the first nested day found, insert a </div> right before its <div class="day-section" tag
        target_id = nested_days[0]
        # Find where target_id starts in html
        pattern = rf'(<div class="day-section"[^>]*id="{target_id}"[^>]*>)'
        m = re.search(pattern, html)
        if m:
            pos = m.start()
            html = html[:pos] + '</div>\n' + html[pos:]
            changed = True
        else:
            break

    # Also check if the last day or day-toolkit needs a closing </div> before </main>
    soup = BeautifulSoup(html, 'html.parser')
    # Count how many direct children of main are day-sections
    main = soup.find('main')
    if main:
        day_count = len(main.find_all('div', class_='day-section', recursive=False))
        total_day_count = len(soup.find_all('div', class_='day-section'))
        print(f"{fn}: {day_count}/{total_day_count} days are direct children of <main>")

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)

print("✓ Finished auto-balancing day sections across all weeks.")
