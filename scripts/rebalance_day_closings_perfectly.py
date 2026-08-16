import glob, re
from bs4 import BeautifulSoup

print("=== ENSURING EXACTLY ONE CLOSING </div> PER DAY SECTION ===")

for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find day-section markers
    # We want: before every `<div class="day-section"` (except the first one)
    # there must be `</div>` that closes the previous day section.
    # And after the last day-section (or day-toolkit), there must be `</div>` that closes it.
    
    # 1. Clean up duplicate </div> or missing </div> before <div class="day-section"
    # Ensure pattern: <button class="complete-btn"...>...</button>\n</div>\n<div class="day-section"
    orig = html
    
    # Replace button followed by arbitrary whitespace/comments and <div class="day-section"
    # with button\n</div>\n<div class="day-section"
    html = re.sub(
        r'(<button class="complete-btn"[^>]*>.*?</button>)\s*(?:</div>\s*)*(?:<!--[\s\S]*?-->\s*)*(<div class="day-section")',
        r'\1\n</div>\n\2',
        html
    )
    
    # Also handle the last day-section before </main> or <div class="week-summary">
    html = re.sub(
        r'(<button class="complete-btn"[^>]*>.*?</button>)\s*(?:</div>\s*)*(?:<!--[\s\S]*?-->\s*)*(</main>|<div class="week-summary">)',
        r'\1\n</div>\n\2',
        html
    )

    if html != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Formatted day closing tags in {fn}")

# Check with BeautifulSoup
print("\n--- Validating Day Sections Parentage in All 26 Weeks ---")
all_good = True
for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    days = soup.find_all('div', class_='day-section')
    for d in days:
        d_id = d.get('id', '')
        parent = d.parent.name
        btn = d.find('button', class_='complete-btn')
        if parent != 'main':
            all_good = False
            print(f"  ❌ {fn} #{d_id} has parent <{parent}> (expected <main>)")
        elif d_id.startswith('day-') and d_id.replace('day-', '').isdigit() and not btn:
            all_good = False
            print(f"  ❌ {fn} #{d_id} is missing its complete-btn")

if all_good:
    print("🌟 100% OF ALL DAY SECTIONS IN ALL 26 WEEKS ARE DIRECT SIBLINGS UNDER <main> AND CONTAIN THEIR COMPLETE-BUTTON!")
