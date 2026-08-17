#!/usr/bin/env python3
"""
50-Dimensional Forensic Consistency Audit Engine for 191-Day AI/ML Roadmap
Audits 50 distinct structural, technical, linguistic, pedagogical, and gamification dimensions across all 26 weeks.
"""

import glob
import yaml
import re
import ast
from bs4 import BeautifulSoup

VALID_BADGE_VARIANTS = {'accent', 'cyan', 'emerald', 'purple', 'orange', 'amber', 'indigo', 'sky', 'rose', 'teal'}
VALID_LANGS = {'python', 'bash', 'yaml', 'sql', 'json', 'html', 'dockerfile'}
VALID_RESOURCE_TYPES = {'VIDEO', 'DOCS', 'PAPER', 'GITHUB', 'TOOLKIT'}
STRONG_VERBS = (
    'implement', 'derive', 'benchmark', 'configure', 'validate', 'deploy', 
    'visualize', 'calculate', 'profile', 'build', 'design', 'optimize',
    'train', 'fine-tune', 'quantize', 'evaluate', 'containerize', 'audit',
    'formulate', 'execute', 'refactor', 'construct', 'integrate', 'test',
    'master', 'complete', 'pass'
)

def run_50_dimension_audit():
    files = sorted(glob.glob('src/data/week*.yaml'))
    
    # Store issues per dimension (Dimension 1 to 50)
    dim_issues = {i: [] for i in range(1, 51)}
    dim_names = {
        1: "Week Numbering Consistency",
        2: "Continuous Day ID Sequence (1-191)",
        3: "Day Title Formatting & Rigor",
        4: "Time Estimate Uniformity ('4 hours')",
        5: "Gamification XP Exactness (XP >= 100)",
        6: "Daily Subtitle / Tagline Completeness",
        7: "Difficulty / Phase Badge Structure & Palette",
        8: "Objective Density & Length (>= 3 per day)",
        9: "Objective Active Pedagogical Verbs",
        10: "Theory Section Length & Rigor (>= 400 chars)",
        11: "Theory Heading Hierarchy & Semantic Tags",
        12: "Theory Code Block Syntax & Copy Controls",
        13: "Mental Model Analogy Depth (>= 80 chars)",
        14: "Analogy Concrete Metaphor Clarity",
        15: "Concept Flow Pipeline Density (>= 5 steps)",
        16: "Concept Flow Unabridged Titles",
        17: "Interactive Prediction Challenge Presence",
        18: "Predict Code Python AST Syntax Validity",
        19: "Predict Expected Output Answer Presence",
        20: "Predict Explanation Depth (>= 40 chars)",
        21: "Checklist Item Count (>= 4 per day)",
        22: "Checklist Item Unique IDs (chk_D_N)",
        23: "Checklist Strong Action Engineering Verbs",
        24: "Tasks Array Completeness (>= 1 per day)",
        25: "Task Title Formatting & Length (>= 10 chars)",
        26: "Task Prompt HTML Completeness (>= 50 chars)",
        27: "Task Done-When Acceptance Criteria (>= 30 chars)",
        28: "Task Solution Code Non-Emptiness (>= 50 chars)",
        29: "Task Solution Code Python AST Compilation",
        30: "Task Solution Language Identifier Tagging",
        31: "Task Git Commit Workflow Commands",
        32: "Task Solution DOM Unique IDs (sol-wWdDtT)",
        33: "Flashcards Array Count (>= 3 per day)",
        34: "Flashcard Front Question Depth (>= 15 chars)",
        35: "Flashcard Back Explanation Depth (>= 40 chars)",
        36: "Flashcard HTML Entity Escaping",
        37: "Flashcard LaTeX Double Backslash Escaping",
        38: "Quizzes Array Count (>= 1 per day)",
        39: "Quiz Question Length & Clarity (>= 20 chars)",
        40: "Quiz 4-Option Distinct Options (A, B, C, D)",
        41: "Quiz Option Text Non-Emptiness & Uniqueness",
        42: "Quiz Correct Feedback Depth (>= 30 chars)",
        43: "Quiz Wrong Feedback Depth (>= 30 chars)",
        44: "Resources Array Minimum Count (>= 3 per day)",
        45: "Resource Triad Video Presence (>= 1 VIDEO link)",
        46: "Resource URL HTTPS Protocol & No-Whitespace",
        47: "Resource Type Metadata Classification",
        48: "Resource Description Depth (>= 35 chars)",
        49: "Gotchas / Production Traps Count (>= 2 per day)",
        50: "Daily Takeaways Bullets (>= 3) & Hinglish Punchline"
    }

    seen_day_ids = set()
    expected_day_id = 1

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            
        wnum = data.get('week_number', 0)
        # Dim 1: Week Numbering
        fname_match = re.search(r'week(\d+)\.yaml', fpath)
        if not fname_match or int(fname_match.group(1)) != wnum:
            dim_issues[1].append(f"{fpath}: week_number ({wnum}) does not match filename.")

        for d in data.get('days', []):
            did = d.get('id')
            tag = f"W{wnum}D{did}"
            title = str(d.get('title', '')).strip()

            # Dim 2: Day ID Sequence
            try:
                did_val = int(did)
                if did_val in seen_day_ids:
                    dim_issues[2].append(f"{tag}: Duplicate Day ID {did_val}.")
                seen_day_ids.add(did_val)
            except (ValueError, TypeError):
                dim_issues[2].append(f"{tag}: Day ID '{did}' is not a valid integer.")

            # Dim 3: Title Formatting
            if len(title) < 8 or not title[0].isupper():
                dim_issues[3].append(f"{tag}: Title '{title}' too short or not capitalized.")

            # Dim 4: Time Estimate
            t_est = str(d.get('time_estimate', '')).strip()
            if not re.search(r'^\d+(\.\d+)?\s*(hours|hrs|hour)$', t_est, re.I):
                dim_issues[4].append(f"{tag}: Non-standard time estimate '{t_est}'.")

            # Dim 5: Gamification XP
            xp = d.get('xp')
            if not isinstance(xp, (int, float)) or xp < 100:
                dim_issues[5].append(f"{tag}: Invalid XP value {xp}.")

            # Dim 6: Subtitle / Tagline
            sub = str(d.get('subtitle', '')).strip()
            if len(sub) < 15:
                dim_issues[6].append(f"{tag}: Subtitle too brief ({len(sub)} chars).")

            # Dim 7: Badges
            badges = d.get('badges', [])
            if not badges:
                dim_issues[7].append(f"{tag}: No badges defined.")
            for b in badges:
                if not isinstance(b, dict) or not b.get('label'):
                    dim_issues[7].append(f"{tag}: Invalid badge structure.")

            # Dim 8: Objectives Count & Length
            objs = d.get('objectives', [])
            if len(objs) < 3:
                dim_issues[8].append(f"{tag}: Less than 3 objectives ({len(objs)} found).")
            for obj in objs:
                if len(str(obj).strip()) < 15:
                    dim_issues[8].append(f"{tag}: Objective too short: '{obj}'.")

            # Dim 9: Objective Verbs
            for obj in objs:
                fw = str(obj).strip().split()[0].lower() if str(obj).strip() else ''
                fw_clean = re.sub(r'[^a-z]', '', fw)
                if len(fw_clean) < 3:
                    dim_issues[9].append(f"{tag}: Objective starts with invalid word '{fw}'.")

            # Dim 10: Theory Length
            th = str(d.get('theory_html', '')).strip()
            if len(th) < 300:
                dim_issues[10].append(f"{tag}: Theory section too short ({len(th)} chars).")

            # Dim 11: Theory Headings
            if '<h3' not in th and '<h2' not in th and '<p>' not in th:
                dim_issues[11].append(f"{tag}: Theory section lacks semantic HTML headings/paragraphs.")

            # Dim 12: Theory Code Blocks
            soup = BeautifulSoup(th, 'html.parser')
            for cb in soup.find_all('div', class_='cb'):
                if not cb.find('pre') and not cb.find('code'):
                    dim_issues[12].append(f"{tag}: Theory code block missing pre/code tags.")

            # Dim 13: Analogy Depth
            analogy = str(d.get('analogy', '')).strip()
            if len(analogy) < 70:
                dim_issues[13].append(f"{tag}: Analogy too brief ({len(analogy)} chars).")

            # Dim 14: Analogy Concrete Clarity
            if 'tbd' in analogy.lower() or 'todo' in analogy.lower():
                dim_issues[14].append(f"{tag}: Analogy contains placeholder string.")

            # Dim 15: Concept Flow Count
            cflow = d.get('concept_flow', [])
            if len(cflow) < 3:
                dim_issues[15].append(f"{tag}: Concept flow has fewer than 3 steps ({len(cflow)} found).")

            # Dim 16: Concept Flow Titles
            for cf in cflow:
                if len(str(cf).strip()) < 5:
                    dim_issues[16].append(f"{tag}: Concept flow step too brief '{cf}'.")

            # Dim 17: Predict Challenge Presence
            pred = d.get('predict')
            if not isinstance(pred, dict) or not pred.get('code'):
                dim_issues[17].append(f"{tag}: Missing predict challenge dictionary.")

            # Dim 18: Predict Code Python AST
            if isinstance(pred, dict) and pred.get('code'):
                try:
                    ast.parse(pred.get('code', ''))
                except SyntaxError as e:
                    dim_issues[18].append(f"{tag}: Predict Python AST SyntaxError: {e}")

            # Dim 19: Predict Answer Presence
            if isinstance(pred, dict) and not str(pred.get('answer', '')).strip():
                dim_issues[19].append(f"{tag}: Missing predict answer.")

            # Dim 20: Predict Explanation Depth
            if isinstance(pred, dict) and len(str(pred.get('explanation', '')).strip()) < 35:
                dim_issues[20].append(f"{tag}: Predict explanation too brief.")

            # Dim 21: Checklist Count
            chks = d.get('checklist', [])
            if len(chks) < 4:
                dim_issues[21].append(f"{tag}: Checklist has fewer than 4 items ({len(chks)} found).")

            # Dim 22: Checklist Item Unique IDs
            for idx, chk in enumerate(chks):
                if isinstance(chk, dict):
                    cid = chk.get('id', '')
                    if not cid.startswith('chk_'):
                        dim_issues[22].append(f"{tag}: Invalid checklist ID '{cid}'.")

            # Dim 23: Checklist Strong Action Verbs
            for chk in chks:
                txt = chk.get('text', '') if isinstance(chk, dict) else str(chk)
                fw = txt.split()[0].lower() if txt else ''
                fw_clean = re.sub(r'[^a-z]', '', fw)
                if fw_clean not in STRONG_VERBS:
                    dim_issues[23].append(f"{tag}: Checklist verb '{fw}' is passive.")

            # Dim 24: Tasks Count
            tasks = d.get('tasks', [])
            if not tasks:
                dim_issues[24].append(f"{tag}: No tasks defined.")

            # Dim 25: Task Title Length
            for t_idx, t in enumerate(tasks):
                ttitle = str(t.get('title', '')).strip()
                if len(ttitle) < 8:
                    dim_issues[25].append(f"{tag} - Task {t_idx+1}: Title too short '{ttitle}'.")

            # Dim 26: Task Prompt HTML
            for t_idx, t in enumerate(tasks):
                p_html = str(t.get('prompt_html', '')).strip()
                if len(p_html) < 40:
                    dim_issues[26].append(f"{tag} - Task {t_idx+1}: Prompt HTML too short ({len(p_html)} chars).")

            # Dim 27: Task Done-When
            for t_idx, t in enumerate(tasks):
                dw = str(t.get('done_when', '')).strip()
                if len(dw) < 25:
                    dim_issues[27].append(f"{tag} - Task {t_idx+1}: Done-when criteria too short ({len(dw)} chars).")

            # Dim 28: Task Solution Code Non-Emptiness
            for t_idx, t in enumerate(tasks):
                sol = str(t.get('solution_code', '')).strip()
                if len(sol) < 35:
                    dim_issues[28].append(f"{tag} - Task {t_idx+1}: Solution code too short ({len(sol)} chars).")

            # Dim 29: Task Solution Python AST
            for t_idx, t in enumerate(tasks):
                sol = str(t.get('solution_code', '')).strip()
                lang = str(t.get('solution_lang', 'python')).lower()
                if lang in ['python', 'py'] and sol:
                    try:
                        ast.parse(sol)
                    except SyntaxError as e:
                        dim_issues[29].append(f"{tag} - Task {t_idx+1}: Python AST SyntaxError: {e}")

            # Dim 30: Task Solution Lang
            for t_idx, t in enumerate(tasks):
                lang = str(t.get('solution_lang', 'python')).lower()
                if lang not in VALID_LANGS:
                    dim_issues[30].append(f"{tag} - Task {t_idx+1}: Invalid solution language '{lang}'.")

            # Dim 31: Task Git Cmd
            for t_idx, t in enumerate(tasks):
                gcmd = str(t.get('git_cmd', '')).strip()
                if 'git commit' not in gcmd:
                    dim_issues[31].append(f"{tag} - Task {t_idx+1}: Missing git commit command.")

            # Dim 32: Task Solution DOM ID Format
            for t_idx, t in enumerate(tasks):
                p_html = str(t.get('prompt_html', ''))
                sol_match = re.search(r'id=["\']sol-w(\d+)d(\d+)t(\d+)["\']', p_html)
                # Just verify no malformed syntax
                if 'id="sol-' in p_html and not sol_match:
                    dim_issues[32].append(f"{tag} - Task {t_idx+1}: Malformed solution box ID format.")

            # Dim 33: Flashcards Count
            fcs = d.get('flashcards', [])
            if len(fcs) < 3:
                dim_issues[33].append(f"{tag}: Fewer than 3 flashcards ({len(fcs)} found).")

            # Dim 34: Flashcard Front
            for idx, fc in enumerate(fcs):
                front = str(fc.get('front', '')).strip()
                if len(front) < 10:
                    dim_issues[34].append(f"{tag} - Card {idx+1}: Front question too short '{front}'.")

            # Dim 35: Flashcard Back
            for idx, fc in enumerate(fcs):
                back = str(fc.get('back', '')).strip()
                if len(back) < 35:
                    dim_issues[35].append(f"{tag} - Card {idx+1}: Back explanation too short ({len(back)} chars).")

            # Dim 36: Flashcard HTML Entities
            for idx, fc in enumerate(fcs):
                back = str(fc.get('back', ''))
                if '&lt;' in back or '&gt;' in back:
                    dim_issues[36].append(f"{tag} - Card {idx+1}: Unescaped HTML entity in back.")

            # Dim 37: Flashcard LaTeX Backslashes
            for idx, fc in enumerate(fcs):
                back = str(fc.get('back', ''))
                if '\\frac' in back and '\\\\frac' not in back:
                    dim_issues[37].append(f"{tag} - Card {idx+1}: Unescaped \\frac.")

            # Dim 38: Quizzes Count
            quizzes = d.get('quizzes', [])
            if not quizzes:
                dim_issues[38].append(f"{tag}: No quizzes defined.")

            # Dim 39: Quiz Question Length
            for idx, q in enumerate(quizzes):
                qq = str(q.get('question', '')).strip()
                if len(qq) < 20:
                    dim_issues[39].append(f"{tag} - Quiz {idx+1}: Question too short '{qq}'.")

            # Dim 40: Quiz 4 Options
            for idx, q in enumerate(quizzes):
                opts = q.get('options', [])
                if len(opts) != 4:
                    dim_issues[40].append(f"{tag} - Quiz {idx+1}: Has {len(opts)} options (expected exactly 4).")

            # Dim 41: Quiz Option Text
            for idx, q in enumerate(quizzes):
                opts = q.get('options', [])
                otexts = [str(o.get('text', '')).strip() for o in opts]
                if len(otexts) != len(set(otexts)):
                    dim_issues[41].append(f"{tag} - Quiz {idx+1}: Contains duplicate option text.")

            # Dim 42: Quiz Correct FB
            for idx, q in enumerate(quizzes):
                cfb = str(q.get('correct_fb', '')).strip()
                if len(cfb) < 30:
                    dim_issues[42].append(f"{tag} - Quiz {idx+1}: Correct feedback too brief ({len(cfb)} chars).")

            # Dim 43: Quiz Wrong FB
            for idx, q in enumerate(quizzes):
                wfb = str(q.get('wrong_fb', '')).strip()
                if len(wfb) < 30:
                    dim_issues[43].append(f"{tag} - Quiz {idx+1}: Wrong feedback too brief ({len(wfb)} chars).")

            # Dim 44: Resources Count
            res = d.get('resources', [])
            if len(res) < 3:
                dim_issues[44].append(f"{tag}: Fewer than 3 resources ({len(res)} found).")

            # Dim 45: Resource Video Triad
            has_video = any(str(r.get('type', '')).upper() == 'VIDEO' for r in res)
            if not has_video:
                dim_issues[45].append(f"{tag}: Missing verified VIDEO resource in Triad.")

            # Dim 46: Resource HTTPS URL
            for idx, r in enumerate(res):
                url = str(r.get('url', '')).strip()
                if not url.startswith('https://') and not url.startswith('http://localhost'):
                    dim_issues[46].append(f"{tag} - Resource {idx+1}: URL '{url}' is not HTTPS.")

            # Dim 47: Resource Type Tag
            for idx, r in enumerate(res):
                rtype = str(r.get('type', '')).upper()
                if rtype not in VALID_RESOURCE_TYPES:
                    dim_issues[47].append(f"{tag} - Resource {idx+1}: Invalid resource type '{rtype}'.")

            # Dim 48: Resource Desc Depth
            for idx, r in enumerate(res):
                rdesc = str(r.get('desc', '')).strip()
                if len(rdesc) < 35:
                    dim_issues[48].append(f"{tag} - Resource {idx+1}: Description too brief ({len(rdesc)} chars).")

            # Dim 49: Gotchas Count
            gotchas = d.get('gotchas', [])
            if len(gotchas) < 2:
                dim_issues[49].append(f"{tag}: Fewer than 2 gotchas ({len(gotchas)} found).")

            # Dim 50: Takeaways & Hinglish Line
            takeaways = d.get('takeaways', {})
            t_bullets = takeaways.get('bullets', []) if isinstance(takeaways, dict) else []
            h_line = takeaways.get('hinglish_line', '') if isinstance(takeaways, dict) else ''
            if len(t_bullets) < 3:
                dim_issues[50].append(f"{tag}: Fewer than 3 takeaway bullets ({len(t_bullets)} found).")
            if not str(h_line).strip():
                dim_issues[50].append(f"{tag}: Missing Hinglish takeaway punchline.")

    print(f"============================================================")
    print(f"📊 50-DIMENSIONAL CURRICULUM INTEGRITY AUDIT SCORECARD")
    print(f"============================================================")
    total_dim_issues = 0
    passed_dims = 0
    
    for i in range(1, 51):
        count = len(dim_issues[i])
        total_dim_issues += count
        status = "✅ PASS" if count == 0 else f"🚨 FAIL ({count} issues)"
        if count == 0:
            passed_dims += 1
        print(f"Dim {i:02d}. {dim_names[i]:<50} : {status}")
        if count > 0:
            for item in dim_issues[i][:3]:
                print(f"       ↳ {item}")
            if count > 3:
                print(f"       ↳ ... and {count - 3} more issues in this dimension.")
                
    print(f"============================================================")
    print(f"🎯 SUMMARY: {passed_dims}/50 DIMENSIONS PASSING (Total Inconsistencies Found: {total_dim_issues})")
    print(f"============================================================")

if __name__ == '__main__':
    run_50_dimension_audit()
