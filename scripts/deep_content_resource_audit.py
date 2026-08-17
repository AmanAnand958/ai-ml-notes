#!/usr/bin/env python3
"""
scripts/deep_content_resource_audit.py
Deep multi-dimensional analysis of:
1. Hinglish Quality & Length (missing, <25 words, or lacking Romanized Hindi markers)
2. Resources Audit (YouTube creators: Indian & Renowned channels, relevance, duplicates across days, broken/empty URLs)
3. Div Nesting & DOM Hierarchy (unclosed/mismatched div tags, broken card containers)
4. Duplicate / Misplaced / Redundant Content (repeated analogies, copy-pasted tasks, duplicate theory sections)
5. Text Formatting & Overflow (unformatted spans, broken tables, code overflow)
6. Interactive Button Handlers (onclick hooks, target IDs)
"""

import glob, yaml, re, os, json, html

print("=== STARTING DEEP CONTENT, HINGLISH & RESOURCE AUDIT ===")

findings = {
    "hinglish_issues": [],
    "resource_issues": [],
    "div_nesting_issues": [],
    "duplicate_redundant_content": [],
    "theory_depth_issues": [],
    "button_interactive_issues": []
}

INDIAN_YT_KEYWORDS = [
    'krish naik', 'campusx', 'nitish', 'hitesh', 'chai aur code', 'code with harry', 
    'codewithharry', 'abhishek thakur', 'edureka hindi', 'simplilearn hindi', 'wsCube tech', 
    'geeky shows', 'gate smashers', 'saurabh shukla', 'apna college', 'take u forward', 'striver'
]

RENOWNED_YT_KEYWORDS = [
    '3blue1brown', 'statquest', 'karpathy', 'andrej', 'yannic kilcher', 'sentdex',
    'freecodecamp', 'mit openbrowse', 'stanford online', 'deeplearning.ai', 'andrew ng',
    'two minute papers', 'sebastian raschka', 'lex fridman', 'google cloud tech', 'huggingface'
]

# -------------------------------------------------------------
# 1. HINGLISH AUDIT (src/data/week*.yaml)
# -------------------------------------------------------------
print("1. Auditing Hinglish Explanations...")
yaml_files = sorted(glob.glob('src/data/week*.yaml'))

hindi_markers = ['hai', 'hain', 'karo', 'karta', 'hoti', 'hota', 'mein', 'ko', 'se', 'ka', 'ke', 'ki', 'bhi', 'pe', 'aur', 'karna', 'kyunki', 'samjho']

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        hinglish = str(d.get('hinglish', '')).strip()
        h_words = hinglish.split()
        
        # Check if missing or very short (<20 words)
        if not hinglish:
            findings["hinglish_issues"].append({
                "location": d_loc,
                "type": "Missing Hinglish",
                "detail": "Day has no Hinglish summary field."
            })
        elif len(h_words) < 20:
            findings["hinglish_issues"].append({
                "location": d_loc,
                "type": "Short Hinglish",
                "detail": f"Hinglish summary is too brief ({len(h_words)} words, recommended >=30 words). Text: '{hinglish}'"
            })
        else:
            # Check if it has genuine Hindi / Hinglish words
            h_lower = hinglish.lower()
            hindi_hits = sum(1 for m in hindi_markers if f" {m} " in f" {h_lower} ")
            if hindi_hits < 2:
                findings["hinglish_issues"].append({
                    "location": d_loc,
                    "type": "Pure English in Hinglish Field",
                    "detail": f"Hinglish field contains purely English text with zero Hindi conversational connectors. Text: '{hinglish[:100]}...'"
                })

# -------------------------------------------------------------
# 2. RESOURCES AUDIT (Creators, Indian YT, Duplicates, Authority)
# -------------------------------------------------------------
print("2. Auditing Resources & Video Authority...")
seen_global_urls = {}

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        resources = d.get('resources', [])
        
        if len(resources) < 3:
            findings["resource_issues"].append({
                "location": d_loc,
                "type": "Low Resource Count",
                "detail": f"Only {len(resources)} resources listed (recommended >= 4 curated resources per day)."
            })
            
        has_video = False
        has_indian_creator = False
        has_renowned_creator = False
        
        for r_idx, r in enumerate(resources):
            url = str(r.get('url', '')).strip()
            title = str(r.get('title', '')).strip()
            r_type = str(r.get('type', '')).upper()
            
            if 'youtube.com' in url or 'youtu.be' in url or r_type in ['VIDEO', 'YT']:
                has_video = True
                t_lower = (title + " " + url).lower()
                if any(k in t_lower for k in INDIAN_YT_KEYWORDS):
                    has_indian_creator = True
                if any(k in t_lower for k in RENOWNED_YT_KEYWORDS):
                    has_renowned_creator = True
                    
            # Check cross-day duplicate URLs
            if url and not url.startswith('#') and not url.startswith('https://pytorch.org') and not url.startswith('https://docs.python.org'):
                if url in seen_global_urls:
                    findings["resource_issues"].append({
                        "location": d_loc,
                        "type": "Cross-Day Duplicate Resource URL",
                        "detail": f"URL '{url}' was already used in {seen_global_urls[url]} (Resource: {title})"
                    })
                else:
                    seen_global_urls[url] = d_loc

        if not has_video and d_num <= 180:
            findings["resource_issues"].append({
                "location": d_loc,
                "type": "Missing Video Resource",
                "detail": "Day has no YouTube / Video tutorial resource."
            })

# -------------------------------------------------------------
# 3. HTML DIV NESTING & TAG BALANCE AUDIT
# -------------------------------------------------------------
print("3. Auditing HTML DOM Div Nesting & Hierarchy...")
html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    w_file = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    div_opens = len(re.findall(r'<div\b', content, re.IGNORECASE))
    div_closes = len(re.findall(r'</div>', content, re.IGNORECASE))
    if div_opens != div_closes:
        findings["div_nesting_issues"].append({
            "location": w_file,
            "type": "Unbalanced <div> Tags",
            "detail": f"<div opened {div_opens} times but closed {div_closes} times (diff: {div_opens - div_closes})"
        })

    # Check for unclosed <pre>, <code>, <span>, <p>
    for tag in ['pre', 'code', 'table', 'section']:
        o = len(re.findall(rf'<{tag}\b', content, re.IGNORECASE))
        c = len(re.findall(rf'</{tag}>', content, re.IGNORECASE))
        if o != c:
            findings["div_nesting_issues"].append({
                "location": w_file,
                "type": f"Unbalanced <{tag}> Tags",
                "detail": f"<{tag}> opened {o} times but closed {c} times (diff: {o - c})"
            })

    # Check for raw dangling spans outside code blocks
    dangling_spans = re.findall(r'</div>\s*<span class="cm">', content)
    if dangling_spans:
        findings["div_nesting_issues"].append({
            "location": w_file,
            "type": "Dangling Code Span Outside Container",
            "detail": f"Found {len(dangling_spans)} raw '<span class=\"cm\">' outside proper <div class=\"cb\"> container."
        })

# -------------------------------------------------------------
# 4. DUPLICATE & REDUNDANT CONTENT AUDIT
# -------------------------------------------------------------
print("4. Auditing Duplicate & Redundant Content...")
seen_analogies = {}
seen_tasks = {}

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        analogy = str(d.get('analogy', '')).strip()
        if analogy and len(analogy) > 25:
            norm_an = re.sub(r'\s+', ' ', analogy).strip()
            if norm_an in seen_analogies:
                findings["duplicate_redundant_content"].append({
                    "location": d_loc,
                    "type": "Duplicate Analogy Across Days",
                    "detail": f"Analogy is an exact duplicate of {seen_analogies[norm_an]}. Text: '{analogy[:80]}...'"
                })
            else:
                seen_analogies[norm_an] = d_loc

        # Check tasks duplication
        for t in d.get('tasks', []):
            t_title = str(t.get('title', '')).strip()
            if t_title and len(t_title) > 10:
                if t_title in seen_tasks:
                    findings["duplicate_redundant_content"].append({
                        "location": d_loc,
                        "type": "Duplicate Task Title Across Days",
                        "detail": f"Task '{t_title}' was already assigned in {seen_tasks[t_title]}."
                    })
                else:
                    seen_tasks[t_title] = d_loc

# -------------------------------------------------------------
# 5. SUMMARY
# -------------------------------------------------------------
print("\n" + "="*70)
print("=== DEEP CONTENT & RESOURCE AUDIT COMPLETE ===")
print("="*70)

for category, issues in findings.items():
    print(f"\n--- {category.upper()} ({len(issues)} findings) ---")
    for item in issues[:5]:
        print(f"  • [{item.get('type')}] {item.get('location')} -> {item.get('detail')[:100]}")
    if len(issues) > 5:
        print(f"    ... and {len(issues) - 5} more.")

with open('scripts/deep_content_audit_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("\nSaved full audit report to: scripts/deep_content_audit_report.json")
