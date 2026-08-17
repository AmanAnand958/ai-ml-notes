#!/usr/bin/env python3
"""
Forensic Legacy Data Extractor
Extracts structured content from monolithic v0 week HTML files into YAML data files.
"""

import os
import sys
import glob
import re
import yaml
from bs4 import BeautifulSoup

def clean_html(element):
    if not element:
        return ""
    # Return inner HTML stripped of outer tag
    return element.decode_contents().strip()

def extract_week(fpath):
    fname = os.path.basename(fpath)
    wnum = int(''.join(filter(str.isdigit, fname)))
    
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Week meta
    title_tag = soup.find('title')
    title_text = title_tag.get_text() if title_tag else f"Week {wnum}"
    # Clean title e.g. "Week 1 — Python Foundations | 191-Day AI/ML Roadmap"
    m = re.search(r'Week\s+\d+\s*[—–-]\s*([^|]+)', title_text)
    week_title = m.group(1).strip() if m else f"Week {wnum}"

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    week_desc = meta_desc.get('content', '') if meta_desc else ''

    week_data = {
        'week_number': wnum,
        'title': week_title,
        'description': week_desc,
        'days': []
    }

    day_sections = soup.find_all('div', class_='day-section')
    for ds in day_sections:
        did = ds.get('id', '')
        if not did:
            continue
        
        raw_id = did.replace('day-', '')
        
        if raw_id == 'toolkit':
            # Toolkit section
            t_header = ds.find('div', class_='day-header')
            t_title = t_header.find('h1').get_text(strip=True) if t_header and t_header.find('h1') else "Master Resource Kit"
            t_sub = t_header.find('p').get_text(strip=True) if t_header and t_header.find('p') else ""
            
            # Extract content html (everything inside theory or after header before complete-btn)
            t_theory = ds.find('div', class_='theory') or ds.find('div', id=re.compile(r'theory'))
            t_content = ""
            if t_theory:
                t_content = clean_html(t_theory)
            else:
                # Fallback: get everything between header and complete-btn
                children_html = []
                for child in ds.children:
                    if getattr(child, 'name', None) not in ['div'] or 'day-header' not in child.get('class', []):
                        if getattr(child, 'name', None) == 'button' and 'complete-btn' in child.get('class', []):
                            continue
                        children_html.append(str(child))
                t_content = ''.join(children_html).strip()

            week_data['toolkit'] = {
                'id': 'toolkit',
                'title': t_title,
                'subtitle': t_sub,
                'content_html': t_content,
                'xp': int(ds.get('data-xp', 500))
            }
            continue

        day_num = int(raw_id) if raw_id.isdigit() else raw_id

        # Objectives
        objectives = []
        obj_div = ds.find('div', class_='objectives')
        if obj_div:
            for li in obj_div.find_all('li'):
                objectives.append(clean_html(li))

        # Checklist
        checklist = []
        chk_div = ds.find('div', class_='checklist')
        if chk_div:
            for item in chk_div.find_all(class_='checklist-item'):
                text_el = item.find(class_='chk-text')
                if text_el:
                    checklist.append(clean_html(text_el))

        # Day Header
        d_header = ds.find('div', class_='day-header')
        d_title = d_header.find('h1').get_text(strip=True) if d_header and d_header.find('h1') else f"Day {day_num}"
        d_sub = d_header.find('p').get_text(strip=True) if d_header and d_header.find('p') else ""

        # Badges & Meta
        time_est = ""
        difficulty = ""
        extra_badges = []
        if d_header:
            meta_row = d_header.find('div', class_='meta-row')
            if meta_row:
                for badge in meta_row.find_all('span', class_='meta-badge'):
                    b_text = badge.get_text(strip=True)
                    classes = badge.get('class', [])
                    variant = [c for c in classes if c != 'meta-badge']
                    v = variant[0] if variant else 'b'
                    if '⏱' in b_text or 'mins' in b_text or 'hrs' in b_text or 'hr' in b_text:
                        time_est = b_text.replace('⏱', '').strip()
                    elif '⚡' in b_text or b_text in ['Beginner', 'Easy', 'Medium', 'Hard', 'Advanced', 'Specialized']:
                        difficulty = b_text.replace('⚡', '').strip()
                    else:
                        extra_badges.append({'label': b_text, 'variant': v})

        # Concept Map Flow
        concept_flow = []
        c_flow = ds.find('div', class_='concept-map-flow')
        if c_flow:
            for span in c_flow.find_all('span'):
                txt = span.get_text(strip=True)
                if txt and txt != '➔':
                    concept_flow.append(txt)

        # Hinglish & Analogy
        hinglish = ""
        hinglish_div = ds.find('div', class_='callout ci') or ds.find('div', class_='hinglish')
        if hinglish_div:
            p = hinglish_div.find('p')
            hinglish = clean_html(p) if p else clean_html(hinglish_div)

        analogy = ""
        analogy_div = ds.find('div', class_='analogy')
        if analogy_div:
            analogy = clean_html(analogy_div)

        # Theory HTML
        theory_html = ""
        theory_div = ds.find('div', id=f'day-{raw_id}-theory') or ds.find('div', class_='theory')
        if theory_div:
            # Remove redundant sh2 Theory & Concepts header if present inside
            for h in theory_div.find_all(['h2', 'h3'], class_='sh2'):
                if 'Theory' in h.get_text():
                    h.decompose()
            # Remove leading analogy or quick jumps if they were placed inside theory_div
            for dup in theory_div.find_all(['div'], class_=['analogy', 'quick-jumps']):
                dup.decompose()
            theory_html = clean_html(theory_div)
        
        # Fallback: if theory_html is empty, collect siblings between day-header and predict-block / tasks
        if not theory_html or len(theory_html.strip()) < 20:
            theory_parts = []
            collecting = False
            for child in ds.children:
                if getattr(child, 'name', None) == 'div' and 'day-header' in child.get('class', []):
                    collecting = True
                    continue
                if getattr(child, 'name', None) in ['div', 'h2'] and ('predict-block' in child.get('class', []) or 'tasks-section' in child.get('class', []) or 'Tasks' in child.get_text()):
                    collecting = False
                    break
                if collecting:
                    # Skip elements already extracted into their own dedicated fields
                    c_classes = child.get('class', []) if getattr(child, 'name', None) else []
                    if any(cls in c_classes for cls in ['objectives', 'checklist', 'concept-map-flow', 'callout', 'ci', 'analogy', 'quick-jumps', 'day-header']):
                        continue
                    if getattr(child, 'name', None) == 'h2' and ('Theory' in child.get_text() or 'objectives' in str(child)):
                        continue
                    theory_parts.append(str(child))
            theory_html = ''.join(theory_parts).strip()

        # Predict Block
        predict = None
        predict_div = ds.find('div', class_='predict-block')
        if predict_div:
            p_question = ""
            qp = predict_div.find('p')
            if qp:
                p_question = clean_html(qp)
            
            p_answer = ""
            pbtn = predict_div.find('button', class_='predict-btn')
            if pbtn:
                oc = pbtn.get('onclick', '')
                m = re.findall(r"['\"]([^'\"]*)['\"]", oc)
                if len(m) >= 2:
                    p_answer = m[1]

            p_sol = predict_div.find('div', class_='solution-box')
            p_exp = ""
            p_code = ""
            if p_sol:
                exp_p = p_sol.find('p')
                if exp_p:
                    p_exp = clean_html(exp_p).replace('Expected Output:', '').strip()
                pre = p_sol.find('pre')
                if pre:
                    p_code = clean_html(pre)

            predict = {
                'question': p_question,
                'answer': p_answer,
                'explanation': p_exp,
                'code': p_code
            }

        # Tasks
        tasks = []
        task_sec = ds.find('div', id=f'tasks-section-{raw_id}') or ds.find('div', class_='tasks-section')
        if task_sec:
            for tb in task_sec.find_all('div', class_='task-block'):
                t_badge = ""
                t_badge_class = "tb-med"
                badge_el = tb.find(class_='task-badge')
                if badge_el:
                    t_badge = badge_el.get_text(strip=True)
                    classes = badge_el.get('class', [])
                    for c in classes:
                        if c.startswith('tb-'):
                            t_badge_class = c

                t_title = ""
                title_el = tb.find(class_='task-title')
                if title_el:
                    t_title = title_el.get_text(strip=True)

                t_time = ""
                time_el = tb.find(class_='task-time')
                if time_el:
                    t_time = time_el.get_text(strip=True).replace('⏱', '').strip()

                body = tb.find(class_='task-body')
                prompt_html = ""
                done_when = ""
                git_cmd = ""
                sol_id = ""
                sol_title = ""
                sol_code = ""
                sol_lang = "python"

                if body:
                    # done when
                    dw_el = body.find(class_='done-when')
                    if dw_el:
                        done_when = clean_html(dw_el).replace('Done when:', '').replace('Done when', '').strip()
                        dw_el.decompose()

                    # git block
                    gb_el = body.find(class_='git-block')
                    if gb_el:
                        git_cmd = clean_html(gb_el)
                        gb_el.decompose()

                    # solution box
                    sol_box = body.find(class_='solution-box')
                    if sol_box:
                        sol_id = sol_box.get('id', '')
                        sol_head = sol_box.find(class_='sol-header')
                        if sol_head:
                            sol_title = clean_html(sol_head).replace('✅ VERIFIED SOLUTION —', '').strip()
                        lang_el = sol_box.find(class_='cb-lang')
                        if lang_el:
                            sol_lang = lang_el.get_text(strip=True)
                        pre = sol_box.find('pre')
                        if pre:
                            sol_code = clean_html(pre)
                        sol_box.decompose()

                    # Remove solution toggle button from prompt html
                    st_btn = body.find(class_='solution-toggle')
                    if st_btn:
                        st_btn.decompose()

                    prompt_html = clean_html(body)

                tasks.append({
                    'title': t_title or f"Task {len(tasks)+1}",
                    'badge': t_badge,
                    'badge_class': t_badge_class,
                    'time': t_time,
                    'prompt_html': prompt_html,
                    'done_when': done_when,
                    'git_cmd': git_cmd,
                    'sol_id': sol_id,
                    'solution_title': sol_title,
                    'solution_code': sol_code,
                    'solution_lang': sol_lang
                })

        # Quizzes
        quizzes = []
        for qb in ds.find_all('div', class_='quiz-block'):
            q_num = ""
            num_el = qb.find(class_='quiz-num')
            if num_el:
                q_num = num_el.get_text(strip=True)

            q_text = ""
            q_el = qb.find(class_='quiz-q')
            if q_el:
                q_text = clean_html(q_el)

            q_id = ""
            options = []
            for opt in qb.find_all(class_='quiz-opt'):
                oc = opt.get('onclick', '')
                is_correct = "'correct'" in oc or '"correct"' in oc
                m = re.findall(r"quiz\(this,\s*['\"](?:correct|wrong)['\"],\s*['\"]([^'\"]+)['\"]", oc)
                if m:
                    q_id = m[0]
                
                letter_el = opt.find(class_='quiz-letter')
                letter = letter_el.get_text(strip=True) if letter_el else ""
                if letter_el:
                    letter_el.decompose()
                opt_text = clean_html(opt)
                options.append({
                    'letter': letter,
                    'text': opt_text,
                    'is_correct': is_correct
                })

            correct_fb = ""
            cfb = qb.find(class_='correct-fb')
            if cfb:
                correct_fb = clean_html(cfb)

            wrong_fb = ""
            wfb = qb.find(class_='wrong-fb')
            if wfb:
                wrong_fb = clean_html(wfb)

            quizzes.append({
                'num_str': q_num,
                'question': q_text,
                'qid': q_id,
                'options': options,
                'correct_fb': correct_fb,
                'wrong_fb': wrong_fb
            })

        # Flashcards
        flashcards = []
        for fc in ds.find_all(class_='flashcard'):
            front_el = fc.find(class_='fc-front')
            back_el = fc.find(class_='fc-back')
            if front_el and back_el:
                flashcards.append({
                    'front': clean_html(front_el),
                    'back': clean_html(back_el)
                })

        # Gotchas
        gotcha = None
        gotcha_box = ds.find(class_='gotcha-box')
        if gotcha_box:
            g_title = ""
            strong = gotcha_box.find('strong')
            if strong:
                g_title = clean_html(strong)
                strong.decompose()
            g_desc = clean_html(gotcha_box)
            gotcha = {
                'title': g_title,
                'description': g_desc
            }

        # Takeaways
        takeaways = None
        takeaways_div = ds.find(class_='takeaways')
        if takeaways_div:
            h_line = ""
            h_el = takeaways_div.find(class_='hinglish')
            if h_el:
                h_line = clean_html(h_el).replace('📢', '').replace('<strong>Ek line mein:</strong>', '').strip()
                h_el.decompose()
            bullets = []
            for li in takeaways_div.find_all('li'):
                bullets.append(clean_html(li))
            takeaways = {
                'hinglish_line': h_line,
                'bullets': bullets
            }

        # Resources
        resources = []
        res_grid = ds.find(class_='res-grid')
        if res_grid:
            for card in res_grid.find_all(class_='resource-card'):
                r_type = ""
                type_el = card.find(class_='rc-type')
                if type_el:
                    r_type = type_el.get_text(strip=True)
                r_title = ""
                title_el = card.find(class_='rc-title') or card.find(class_='res-title')
                if title_el:
                    r_title = clean_html(title_el)
                r_sub = ""
                sub_el = card.find(class_='rc-sub') or card.find(class_='res-desc')
                if sub_el:
                    r_sub = clean_html(sub_el)
                r_url = card.get('href', '#')
                resources.append({
                    'type': r_type,
                    'title': r_title,
                    'desc': r_sub,
                    'url': r_url
                })

        day_obj = {
            'id': raw_id,
            'day_num': day_num,
            'title': d_title,
            'subtitle': d_sub,
            'time_estimate': time_est,
            'difficulty': difficulty,
            'badges': extra_badges,
            'xp': int(ds.get('data-xp', 150)),
            'objectives': objectives,
            'checklist': checklist,
            'concept_flow': concept_flow,
            'hinglish': hinglish,
            'analogy': analogy,
            'theory_html': theory_html,
            'predict': predict,
            'tasks': tasks,
            'quizzes': quizzes,
            'flashcards': flashcards,
            'gotcha': gotcha,
            'takeaways': takeaways,
            'resources': resources
        }
        week_data['days'].append(day_obj)

    return week_data

def main():
    src_dir = 'v0_snapshot/pages/weeks'
    out_dir = 'src/data'
    os.makedirs(out_dir, exist_ok=True)

    files = sorted(glob.glob(os.path.join(src_dir, 'week*.html')), key=lambda p: int(''.join(filter(str.isdigit, os.path.basename(p)))))
    print(f"📦 Extracting data from {len(files)} weeks in '{src_dir}' into '{out_dir}'...")

    for fpath in files:
        data = extract_week(fpath)
        wnum = data['week_number']
        out_path = os.path.join(out_dir, f"week{wnum:02d}.yaml")
        with open(out_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
        print(f"  ✓ week{wnum:02d}.yaml (extracted {len(data['days'])} days, toolkit={bool(data.get('toolkit'))})")

    print("\n✅ Legacy extraction complete across all 26 weeks!")

if __name__ == '__main__':
    main()
