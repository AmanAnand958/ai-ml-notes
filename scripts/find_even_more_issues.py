#!/usr/bin/env python3
"""
find_even_more_issues.py
Performs another pass of auditing for broken links, sequence errors, and malformed HTML.
"""

import glob
import re
import os
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = "pages/weeks"

def run_audit():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    
    issues = defaultdict(list)
    all_files = [os.path.basename(f) for f in files]
    
    all_days_found = []
    
    for f in sorted(files):
        html = open(f, encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        
        filename = os.path.basename(f)
        try:
            week_num = int(re.search(r'week(\d+)\.html', filename).group(1))
        except:
            week_num = None
            
        # 1. Mismatched Week Title
        h1 = soup.find('h1')
        if h1 and week_num:
            title_text = h1.get_text()
            if f'Week {week_num}:' not in title_text and f'Week {week_num} ' not in title_text:
                issues['Mismatched Week Title'].append(f"{filename}: expected Week {week_num}, found '{title_text}'")
                
        # 2. Duplicate IDs
        ids = [tag.get('id') for tag in soup.find_all(id=True)]
        if len(ids) != len(set(ids)):
            import collections
            duplicates = [item for item, count in collections.Counter(ids).items() if count > 1]
            issues['Duplicate HTML IDs'].append(f"{filename}: {duplicates}")
            
        # 3. Broken Anchor Links
        # Links like href="#day-45"
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('#'):
                if href[1:] not in ids:
                    issues['Broken Anchor Links'].append(f"{filename}: {href}")
            elif href.endswith('.html'):
                if href not in all_files and 'http' not in href:
                    issues['Broken Internal File Links'].append(f"{filename}: {href}")
                    
        # 4. Check Day Sequencing
        day_sections = soup.find_all('div', class_='day-section')
        for day in day_sections:
            day_id = day.get('id')
            if day_id and day_id.startswith('day-'):
                try:
                    all_days_found.append(int(day_id.replace('day-', '')))
                except:
                    pass
                    
        # 5. Empty Sections (tags with no meaningful text or children)
        # Check standard sections like objectives, takeaways
        for section_class in ['objectives', 'takeaways', 'toolkit']:
            sections = soup.find_all('div', class_=section_class)
            for sec in sections:
                if len(sec.get_text(strip=True)) < 10:  # Very short or empty
                    issues['Empty Sections'].append(f"{filename}: empty {section_class}")

    # Process overall day sequence
    all_days_found.sort()
    missing_days = []
    if all_days_found:
        for d in range(1, max(all_days_found) + 1):
            if d not in all_days_found:
                missing_days.append(d)
                
    if missing_days:
        issues['Missing Days in Sequence'] = missing_days

    print("========================================")
    print("      DEEP AUDIT V2 REPORT      ")
    print("========================================")
    for issue_type, affected in issues.items():
        print(f"\n--- {issue_type} ({len(affected)} occurrences) ---")
        for item in list(set(affected))[:10]:
            print(f"  {item}")
        if len(set(affected)) > 10:
            print(f"  ... and {len(set(affected)) - 10} more.")

if __name__ == '__main__':
    run_audit()
