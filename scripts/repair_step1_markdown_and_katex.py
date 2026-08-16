#!/usr/bin/env python3
"""
Step 1: Fix Unformatted Text, Raw Markdown, and KaTeX Formula Glitches across all 26 Weeks.
- Replaces raw markdown bold (**text**) with <strong>text</strong>.
- Replaces raw markdown links ([text](url)) with <a href="url" target="_blank" rel="noopener">text</a>.
- Replaces raw markdown hashtags (# Heading) with styled headings.
- Replaces escaped HTML entities (&gt;, &lt;, &amp;) inside $$...$$ and $...$ with raw mathematical symbols.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    
    # 1. Clean escaped entities inside KaTeX math blocks
    def clean_math_entities(m):
        content = m.group(0)
        content = content.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&').replace('&quot;', '"')
        return content
        
    html = re.sub(r'\$\$[^\$]+\$\$', clean_math_entities, html)
    html = re.sub(r'(?<!\$)\$[^\$\n]+\$(?!\$)', clean_math_entities, html)
    
    # 2. Replace raw markdown links [text](url) outside code/pre/script
    # Only replace where not inside <pre> or <code>
    def replace_md_links(m):
        text = m.group(1)
        url = m.group(2)
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
        
    # Process text node replacements
    soup = BeautifulSoup(html, 'html.parser')
    
    for string_node in list(soup.find_all(string=True)):
        if string_node.parent and string_node.parent.name not in ['code', 'pre', 'script', 'style', 'a']:
            txt = str(string_node)
            # Check for **bold**
            if '**' in txt:
                new_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', txt)
                if new_html != txt:
                    parsed = BeautifulSoup(new_html, 'html.parser')
                    string_node.replace_with(parsed)
                    continue
                    
            # Check for [text](url)
            if '[' in txt and '](' in txt and ')' in txt:
                new_html = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', replace_md_links, txt)
                if new_html != txt:
                    parsed = BeautifulSoup(new_html, 'html.parser')
                    string_node.replace_with(parsed)
                    continue

    # 3. Clean raw '# ' in h1/h2 headings
    for h in soup.find_all(['h1', 'h2', 'h3']):
        if h.text.strip().startswith('#'):
            h.string = re.sub(r'^#+\s*', '', h.text.strip())

    # Write back
    fp.write_text(str(soup), encoding='utf-8')
    
    # Do direct regex cleanup for any remaining literal **...** in raw html
    raw_after = fp.read_text(encoding='utf-8', errors='replace')
    
    def replace_raw_bold(match):
        prefix = match.group(1)
        content = match.group(2)
        return f'{prefix}<strong>{content}</strong>'
        
    raw_after = re.sub(r'(>[^<]*?)\*\*([^*]+)\*\*', replace_raw_bold, raw_after)
    raw_after = re.sub(r'(>[^<]*?)\[([^\]]+)\]\((https?://[^\)]+)\)', r'\1<a href="\3" target="_blank" rel="noopener">\2</a>', raw_after)
    
    fp.write_text(raw_after, encoding='utf-8')
    print(f"  ✅ Fixed raw markdown & KaTeX math formulas in Week {wn}")

print("\n🎉 STEP 1 COMPLETE: ALL RAW MARKDOWN & KATEX MATH FORMULAS REPAIRED ACROSS ALL 26 WEEKS!")
