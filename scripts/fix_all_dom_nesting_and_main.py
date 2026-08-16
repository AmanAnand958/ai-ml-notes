import glob, re
from bs4 import BeautifulSoup

print("=== FIXING ALL DOM NESTING & MAIN ENCAPSULATION ISSUES ===")

# Helper: ensure <main class="main"> wraps all day-sections and closes right before footer/scripts
def fix_file_main_wrapper(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # If there are unclosed callout divs, let's fix them before each <div class="day-section"
    # An unclosed callout usually looks like <div class="callout... without matching </div> before day-section
    lines = html.split('\n')
    new_lines = []
    
    # 1. First remove any premature </main> tags before the last day section
    last_day_pos = html.rfind('class="day-section"')
    if last_day_pos != -1:
        before_last = html[:last_day_pos]
        after_last = html[last_day_pos:]
        before_last_fixed = before_last.replace('</main>', '')
        html = before_last_fixed + after_last

    # 2. Fix unclosed callout blocks before day-sections
    # Replace `<div class="day-section"` when preceded by unclosed callouts
    html = re.sub(r'(<div class="callout[^>]*>[\s\S]*?)(<button class="complete-btn"|<div class="day-section")', lambda m: m.group(1) + '</div>\n' + m.group(2) if m.group(1).count('<div') > m.group(1).count('</div>') else m.group(0), html)

    # 3. Ensure day-toolkit is inside main before </main>
    if '<div class="day-section" id="day-toolkit"' in html:
        # If day-toolkit is after </main>, move </main> after day-toolkit
        if html.find('</main>') < html.find('id="day-toolkit"'):
            html = html.replace('</main>', '')
            html = html.replace('</div>\n<!-- /day-toolkit -->', '</div>\n<!-- /day-toolkit -->\n</main>')
            if '</main>' not in html:
                html = re.sub(r'(<button class="complete-btn"[^>]*onclick="completeDay\([^)]+\)"[^>]*>.*?</button>\s*</div>)', r'\1\n</main>', html)

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)

for fn in sorted(glob.glob('pages/weeks/week*.html'), key=lambda x: int(re.search(r'\d+', x).group(0))):
    fix_file_main_wrapper(fn)

print("✓ Ran initial pass on main encapsulation and callout balancing.")
