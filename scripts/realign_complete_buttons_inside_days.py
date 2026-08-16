import glob, re
from bs4 import BeautifulSoup

print("=== REALIGNING ALL COMPLETE-BUTTONS INSIDE DAY SECTIONS ===")

for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    orig = html
    # Pattern: </div> (closing day or resources) followed by button followed by <div class="day-section"
    # We want: button followed by </div> followed by next day-section
    
    # 1. First, find any button that is followed directly by <div class="day-section" or </main> without a </div> between them
    # Example: </div>\s*<button class="complete-btn" id="btn-day-(\d+)"[^>]*>.*?</button>\s*(?:<!--\s*/day-\d+\s*-->\s*)?<div class="day-section"
    pattern = r'</div>\s*(?:<!--\s*/day-\d+-resources-section\s*-->\s*)?(?:<!--\s*/day-\d+\s*-->\s*)?<button class="complete-btn"\s*id="btn-day-(\d+)"([^>]*)>(.*?)</button>\s*(?:<!--\s*/day-\d+\s*-->\s*)?(<div class="day-section"|</main>|<div class="week-summary">)'
    
    def repl(m):
        d_num = m.group(1)
        attrs = m.group(2)
        btn_text = m.group(3)
        next_tag = m.group(4)
        return f'<button class="complete-btn" id="btn-day-{d_num}"{attrs}>{btn_text}</button>\n</div><!-- /day-{d_num} -->\n{next_tag}'

    html_fixed = re.sub(pattern, repl, html)

    if html_fixed != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html_fixed)
        print(f"✓ Realigned complete-buttons in {fn}")

# Check with BeautifulSoup
print("\n--- Validating Complete-Buttons in All Days ---")
all_ok = True
for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    days = soup.find_all('div', class_='day-section')
    for d in days:
        d_id = d.get('id', '')
        if d_id.startswith('day-') and d_id.replace('day-', '').isdigit():
            btn = d.find('button', class_='complete-btn')
            if not btn:
                all_ok = False
                print(f"  ❌ {fn} #{d_id} is STILL missing its complete-btn inside the day-section")

if all_ok:
    print("🌟 100% OF ALL DAY SECTIONS ACROSS ALL 26 WEEKS HAVE THEIR COMPLETE-BTN ENCLOSED INSIDE!")
