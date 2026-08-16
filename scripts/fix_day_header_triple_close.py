import glob, re
from bs4 import BeautifulSoup

print("=== ERADICATING DAY-HEADER TRIPLE-CLOSE ACROSS ALL 26 WEEKS ===")

for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    orig = html
    # Replace <div class="meta-row">...</div></div></div> with <div class="meta-row">...</div></div>
    # Pattern: (<div class="meta-row">[\s\S]*?</div>\s*</div>)\s*</div>
    html_fixed = re.sub(r'(<div class="meta-row">[\s\S]*?</div>\s*</div>)\s*</div>', r'\1', html)

    if html_fixed != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html_fixed)
        print(f"✓ Fixed triple-close day-headers in {fn}")

print("✓ Finished fixing day-headers.")
