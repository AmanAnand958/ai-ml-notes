#!/usr/bin/env python3
"""
scripts/fix_favicon_tag_leaks.py
Fixes the malformed <link rel="icon"> tag across all HTML files.
Replaces broken/unescaped SVG favicon data URIs with standard clean URL-encoded data URIs.
"""

import glob, re, os

print("=== FIXING FAVICON TAG LEAKS ACROSS ALL HTML FILES ===")

CLEAN_FAVICON_LINK = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E%3Crect width=\'32\' height=\'32\' rx=\'6\' fill=\'%230d0f14\'/%3E%3Ctext x=\'4\' y=\'23\' font-family=\'monospace\' font-size=\'16\' font-weight=\'bold\' fill=\'%234fd1a5\'%3EAI%3C/text%3E%3C/svg%3E"/>'

all_html_files = sorted(glob.glob('pages/weeks/week*.html') + ['index.html', 'roadmap.html', 'dashboard.html', 'resources.html'])

fixed_count = 0
for hf in all_html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern matching any <link ... rel="icon" ...> or <link rel="icon" ...>
    # including those with unescaped SVG inner strings
    new_content = re.sub(r'<link\s+[^>]*rel=[\"\']icon[\"\'][^>]*>', CLEAN_FAVICON_LINK, content)
    new_content = re.sub(r'<link\s+href=[\"\']data:image/svg\+xml,[^>]*rel=[\"\']icon[\"\'][^>]*>', CLEAN_FAVICON_LINK, new_content)
    
    # Also clean any leftover stray leakage text like `AI</text></svg>" rel="icon"/>`
    new_content = re.sub(r'AI</text></svg>\"\s*rel=\"icon\"/>', '', new_content)

    if new_content != content:
        fixed_count += 1
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"✓ Fixed favicon tag in {fixed_count} HTML files.")
print("=== FAVICON TAG LEAK REPAIR COMPLETE ===")
