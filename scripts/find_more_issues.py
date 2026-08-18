#!/usr/bin/env python3
"""
find_more_issues.py
Performs a deep structural and content sweep across all HTML files to find subtle anomalies.
"""

import glob
import re
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = "pages/weeks"

def run_audit():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    
    issues = defaultdict(list)
    
    for f in sorted(files):
        html = open(f, encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Look for TODOs or placeholders
        if 'TODO' in html or 'TBD' in html or 'Lorem ipsum' in html or 'Placeholder' in html:
            issues['Placeholders'].append(f)
            
        # 2. Check for missing critical sections per day
        days = soup.find_all('div', class_='day-section')
        for day in days:
            day_id = day.get('id', '')
            if not day_id.startswith('day-'): continue
            
            text = day.get_text().lower()
            if 'toolkit' not in day_id:
                if 'takeaway' not in text:
                    issues['Missing Takeaways'].append(f"{f} -> {day_id}")
                if 'resources' not in text:
                    issues['Missing Resources'].append(f"{f} -> {day_id}")
                if 'walkthrough' not in text and 'implementation' not in text:
                    issues['Missing Walkthrough'].append(f"{f} -> {day_id}")
                    
            # 3. Check for broken internal links
            # We expect day-navigation buttons like onclick="goDay('126')"
            # Are the target days actually present in the curriculum? 
            # We'll just collect them for now.
            
        # 4. Check for broken <pre><code> blocks (e.g., missing class)
        pre_blocks = soup.find_all('pre')
        for pre in pre_blocks:
            code = pre.find('code')
            if code:
                cls = code.get('class', [])
                if not cls:
                    issues['Code Block Missing Language Class'].append(f)
                    
        # 5. Check SVG viewboxes (sometimes they are malformed)
        svgs = soup.find_all('svg')
        for svg in svgs:
            if not svg.get('viewbox') and not svg.get('viewBox'):
                # Many might not have viewboxes, but let's note if there are structural issues
                pass
                
        # 6. Verify XP markers
        # The 'Mark Day Complete (+150 XP)' buttons
        xp_buttons = soup.find_all('button', class_='complete-btn')
        for btn in xp_buttons:
            if '+150 XP' not in btn.get_text() and '+50 XP' not in btn.get_text():
                issues['Anomalous XP Button'].append(f"{f} -> {btn.get_text().strip()}")
                
        # 7. Check for nested code blocks that might have been messed up
        for code in soup.find_all('code'):
            if code.find('code'):
                issues['Nested Code Tags'].append(f)
                
        # 8. Unescaped HTML characters in pre blocks
        for pre in soup.find_all('pre'):
            content = pre.decode_contents()
            # If there's an unescaped < that is NOT part of a tag
            # It's hard to distinguish perfectly with BS4, but we can look for raw '< ' or ' <'
            if re.search(r'\s<\s', content) or '<=' in content and 'class="math' not in content:
                # We'll skip this as it's prone to false positives
                pass

    print("========================================")
    print("      DEEP CURRICULUM AUDIT REPORT      ")
    print("========================================")
    for issue_type, affected in issues.items():
        print(f"\n--- {issue_type} ({len(affected)} occurrences) ---")
        # Only print first 10 for brevity
        for item in list(set(affected))[:10]:
            print(f"  {item}")
        if len(set(affected)) > 10:
            print(f"  ... and {len(set(affected)) - 10} more.")

if __name__ == '__main__':
    run_audit()
