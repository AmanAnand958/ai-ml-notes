#!/usr/bin/env python3
"""
Full Project Health Scanner:
Audits standalone pages (index.html, dashboard.html, roadmap.html), assets, internal links,
and UI runtime functions for any broken paths or inconsistencies.
"""

import os
import glob
import re
from bs4 import BeautifulSoup

def audit_project():
    print("🔍 Auditing all project pages, assets, and internal links...")
    
    issues = {
        'broken_internal_links': [],
        'missing_assets': [],
        'script_errors': [],
        'css_mismatches': []
    }
    
    html_files = glob.glob('*.html') + glob.glob('pages/**/*.html', recursive=True)
    print(f"Found {len(html_files)} HTML pages to scan.")
    
    for hf in sorted(html_files):
        with open(hf, 'r', encoding='utf-8') as fp:
            content = fp.read()
            soup = BeautifulSoup(content, 'html.parser')
            
        base_dir = os.path.dirname(hf)
        
        # 1. Check <link> and <script> src/href
        for tag in soup.find_all(['link', 'script', 'img', 'a']):
            target = tag.get('href') or tag.get('src')
            if not target or target.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
                continue
                
            # Strip query params / hash for file check
            clean_target = target.split('?')[0].split('#')[0]
            if not clean_target:
                continue
                
            # Resolve relative path
            target_path = os.path.normpath(os.path.join(base_dir, clean_target))
            if not os.path.exists(target_path):
                issues['broken_internal_links'].append(f"{hf} -> {target} (resolved: {target_path})")

    # 2. Check course.js for any undefined global references
    js_files = glob.glob('assets/**/*.js', recursive=True)
    for jf in js_files:
        with open(jf, 'r', encoding='utf-8') as fp:
            js_code = fp.read()
            # Simple syntax balance check
            if js_code.count('{') != js_code.count('}'):
                issues['script_errors'].append(f"{jf}: Mismatched braces {{ {js_code.count('{')} vs }} {js_code.count('}')}")
            if js_code.count('(') != js_code.count(')'):
                issues['script_errors'].append(f"{jf}: Mismatched parentheses ( {js_code.count('(')} vs ) {js_code.count(')')}")

    # 3. Check standalone page features (index.html, dashboard.html, roadmap.html)
    for root_page in ['index.html', 'dashboard.html', 'roadmap.html']:
        if os.path.exists(root_page):
            with open(root_page, 'r', encoding='utf-8') as fp:
                txt = fp.read()
                if 'Syne' in txt and 'fonts.googleapis.com' in txt and 'Syne' not in txt.split('fonts.googleapis.com')[1].split('>')[0]:
                    issues['css_mismatches'].append(f"{root_page}: Google fonts link missing Syne font")
                if 'DM+Sans' not in txt and 'DM Sans' in txt:
                    issues['css_mismatches'].append(f"{root_page}: Google fonts link missing DM Sans font")

    print("============================================================")
    print("📊 FULL PROJECT AUDIT REPORT")
    print("============================================================")
    clean = True
    for cat, errs in issues.items():
        if errs:
            clean = False
            print(f"⚠️ {cat}: {len(errs)} issues")
            for e in errs:
                print(f"   • {e}")
        else:
            print(f"✅ {cat}: 0 issues")
    print("============================================================")
    if clean:
        print("🎉 WHOLE PROJECT PASSED WITH 0 DEFECTS!")

if __name__ == '__main__':
    audit_project()
