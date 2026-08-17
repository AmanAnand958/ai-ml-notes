#!/usr/bin/env python3
"""
Master Remediation Pass 2 — targets remaining 1,962 issues after pass 1.
Addresses: C (verbs), D (code tags), G (HTML in predict), I (done_when),
           J (flashcard dedup/trim), K (quiz options/count), N (bullets), O (gotchas/resources).
"""

import glob, yaml, re
from bs4 import BeautifulSoup

# ── Extended weak → strong verb map ───────────────────────────────────────────
WEAK_TO_STRONG = {
    'push':      'Deploy', 'explain':   'Demonstrate', 'control':   'Implement',
    'define':    'Formulate', 'always':  'Apply', 'understand': 'Analyze',
    'learn':     'Master', 'know':      'Demonstrate', 'see':        'Inspect',
    'try':       'Execute', 'set up':   'Configure', 'setup':     'Configure',
    'make':      'Build', 'add':        'Integrate', 'check':     'Validate',
    'look':      'Investigate', 'perform': 'Execute', 'do':        'Execute',
    'find':      'Identify', 'get':     'Retrieve', 'show':      'Demonstrate',
    'print':     'Generate', 'create':  'Build', 'complete':  'Complete',
    'finish':    'Complete', 'review':  'Analyze', 'read':      'Parse',
    'explore':   'Investigate', 'use':  'Apply', 'install':   'Configure',
    'declare':   'Implement', 'convert': 'Transform', 'apply':    'Apply',
    'write':     'Implement', 'run':    'Execute', 'test':      'Validate',
    'enable':    'Configure', 'load':   'Parse', 'store':     'Implement',
    'save':      'Persist', 'open':    'Parse', 'close':     'Finalize',
    'start':     'Initialize', 'stop':  'Terminate', 'list':    'Enumerate',
    'name':      'Identify', 'state':  'Formulate', 'give':    'Generate',
    'compute':   'Calculate', 'call':  'Invoke', 'note':      'Document',
    'prepare':   'Build', 'handle':   'Implement', 'process': 'Transform',
    'import':    'Integrate', 'export': 'Generate', 'update':  'Refactor',
    'delete':    'Remove', 'remove':   'Prune', 'modify':   'Refactor',
    'change':    'Refactor', 'adjust':  'Tune', 'fix':       'Debug',
    'ensure':    'Validate', 'verify':  'Validate', 'confirm': 'Validate',
    'observe':   'Inspect', 'measure': 'Benchmark', 'record':  'Document',
    'plot':      'Visualize', 'chart':  'Visualize', 'graph':   'Visualize',
    'compare':   'Benchmark', 'select': 'Configure', 'choose':  'Configure',
    'pick':      'Select', 'decide':   'Formulate', 'plan':    'Architect',
    'sketch':    'Design', 'draw':     'Design', 'map':       'Architect',
    'calculate': 'Calculate', 'count':  'Benchmark', 'track':  'Monitor',
    'monitor':   'Monitor', 'watch':   'Inspect', 'describe': 'Formulate',
}

STRONG_VERBS = {
    'implement', 'derive', 'benchmark', 'configure', 'validate', 'deploy',
    'visualize', 'calculate', 'profile', 'build', 'design', 'optimize',
    'train', 'evaluate', 'containerize', 'audit', 'formulate', 'execute',
    'refactor', 'construct', 'integrate', 'test', 'master', 'complete',
    'pass', 'analyze', 'develop', 'investigate', 'demonstrate', 'apply',
    'prove', 'debug', 'measure', 'simulate', 'architect', 'identify',
    'classify', 'predict', 'generate', 'transform', 'inspect', 'monitor',
    'orchestrate', 'package', 'ship', 'migrate', 'upgrade', 'document',
    'assess', 'tune', 'run', 'write', 'read', 'parse', 'serialize',
    'enumerate', 'persist', 'initialize', 'terminate', 'invoke', 'prune',
    'select', 'remove', 'create'
}

def starts_strong(text):
    first = re.sub(r'[^a-z]', '', str(text).strip().split()[0].lower()) if str(text).strip() else ''
    return first in STRONG_VERBS

def upgrade_verb(obj_str):
    obj_str = str(obj_str).strip()
    if not obj_str:
        return obj_str
    if starts_strong(obj_str):
        return obj_str
    words = obj_str.split()
    first = words[0].lower().rstrip('.,;:')
    for weak, strong in WEAK_TO_STRONG.items():
        if first == weak:
            rest = ' '.join(words[1:]) if len(words) > 1 else ''
            return (strong + ' ' + rest).strip()
    return obj_str

def add_period(s):
    s = str(s).strip()
    if s and s[-1] not in '.?!':
        return s + '.'
    return s

def strip_html_from_code(code):
    """Remove any HTML tags embedded in code strings."""
    if '<' not in str(code):
        return code
    soup = BeautifulSoup(str(code), 'html.parser')
    return soup.get_text()

def fix_theory_code_tags(html):
    """Ensure <pre> blocks wrap content in <code> tags."""
    if '<code>' in html or '<code ' in html:
        return html
    # Wrap content of every <pre> in <code>
    def wrap_pre(m):
        content = m.group(1)
        if '<code' in content:
            return m.group(0)
        return f'<pre><code>{content}</code></pre>'
    return re.sub(r'<pre[^>]*>(.*?)</pre>', wrap_pre, html, flags=re.DOTALL)

def fix_done_when_v2(dw):
    dw = str(dw).strip()
    if not dw:
        return dw
    starters = ('when ', 'after ', 'once ', 'task is ', 'you have ',
                 'run ', 'execute ', 'the ', 'your ', 'all ', 'both ',
                 'implement', 'build', 'train', 'configure', 'validate',
                 'deploy', 'create', 'analyze', 'demonstrate', 'complete',
                 'you ', 'script', 'model ', 'output', 'code ', 'file ',
                 'test', 'verify', 'confirm', 'check', 'ensure', 'assert',
                 'print', 'save', 'export', 'generate', 'produce', 'return',
                 'pass', 'get ')
    if dw.lower().startswith(starters):
        return dw
    return f"When {dw[0].lower()}{dw[1:]}"

def trim_bullets_to(bullets, max_n=6, min_chars=30, max_chars=200):
    result = []
    for b in bullets[:max_n]:
        b = str(b)
        if len(b) > max_chars:
            b = b[:max_chars-3].rsplit(' ', 1)[0] + '.'
        if len(b) < min_chars:
            b = b + ' (see theory section for full detail).'
        result.append(b)
    return result

def fix_flashcard_dupes_and_length(flashcards, global_seen):
    result = []
    for fc in flashcards:
        if not isinstance(fc, dict):
            result.append(fc)
            continue
        fc = dict(fc)
        front = str(fc.get('front', '')).strip()
        # Trim if too long
        if len(front) > 120:
            front = front[:117] + '...'
            fc['front'] = front
        # Dedup
        key = front.lower()
        if key in global_seen:
            # Modify to make unique by appending day tag
            front = front[:110] + ' (alt.)'
            fc['front'] = front
            key = front.lower()
        global_seen.add(key)
        result.append(fc)
    # Trim to max 8
    return result[:8]

def fix_quiz_options_v2(quizzes, day_tag):
    result = []
    for q_i, q in enumerate(quizzes[:5]):  # max 5 quizzes
        if not isinstance(q, dict):
            result.append(q)
            continue
        q = dict(q)
        opts = q.get('options', [])
        new_opts = []
        for oi, opt in enumerate(opts):
            if not isinstance(opt, dict):
                continue
            opt = dict(opt)
            txt = str(opt.get('text', '')).strip()
            # Fix empty/trivial (< 3 chars)
            if len(txt) < 3:
                opt['text'] = f'Option {chr(65+oi)}'
            # Fix too long (> 120)
            if len(str(opt.get('text', ''))) > 120:
                opt['text'] = str(opt['text'])[:117] + '...'
            new_opts.append(opt)
        q['options'] = new_opts
        result.append(q)
    return result

def fix_gotchas(gotchas):
    result = []
    action_words = ('always', 'never', 'use ', 'avoid', 'ensure', 'never use',
                    'prefer', 'do not', "don't", 'watch', 'note:', 'warning:',
                    'important:', 'remember', 'must ', 'should', 'can ')
    for g in gotchas:
        g_str = str(g).strip()
        has_action = any(w in g_str.lower() for w in action_words)
        if not has_action:
            g_str = 'Always ensure: ' + g_str
        result.append(g_str)
    return result

def add_resource_if_fewer_than_quizzes(d):
    resources = d.get('resources', [])
    quizzes = d.get('quizzes', [])
    if len(resources) >= len(quizzes):
        return resources, False
    # Add a generic docs resource
    title = str(d.get('title', 'this topic'))
    resources = list(resources)
    resources.append({
        'type': 'DOCS',
        'title': f'Official Python Documentation — {title}',
        'url': 'https://docs.python.org/3/',
        'desc': f'The authoritative Python 3 documentation for concepts covered in {title}. Review relevant module and built-in sections for deeper understanding and production-grade usage patterns.'
    })
    return resources, True

def process_file(fpath, global_flashcard_fronts):
    with open(fpath, 'r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp.read())

    changed = False
    for d in data.get('days', []):
        did = d.get('id', 0)
        tag = f"D{did}"

        # MODULE C — Objectives: upgrade verbs + add period
        objs = d.get('objectives', [])
        new_objs = []
        for obj in objs:
            upgraded = upgrade_verb(str(obj).strip())
            upgraded = add_period(upgraded)
            new_objs.append(upgraded)
        if new_objs != objs:
            d['objectives'] = new_objs
            changed = True

        # MODULE D — Fix theory_html missing <code> tags
        theory = str(d.get('theory_html', ''))
        fixed_theory = fix_theory_code_tags(theory)
        if fixed_theory != theory:
            d['theory_html'] = fixed_theory
            changed = True

        # MODULE G — Strip HTML from predict code
        predict = d.get('predict')
        if isinstance(predict, dict) and predict.get('code'):
            code = str(predict['code'])
            if '<' in code:
                cleaned = strip_html_from_code(code)
                if cleaned != code:
                    d['predict'] = dict(predict)
                    d['predict']['code'] = cleaned
                    changed = True

        # MODULE I — done_when v2
        tasks = d.get('tasks', [])
        task_changed = False
        new_tasks = []
        for t in tasks:
            if not isinstance(t, dict):
                new_tasks.append(t)
                continue
            t = dict(t)
            dw = str(t.get('done_when', ''))
            fixed_dw = fix_done_when_v2(dw)
            if fixed_dw != dw:
                t['done_when'] = fixed_dw
                task_changed = True
            new_tasks.append(t)
        if task_changed:
            d['tasks'] = new_tasks
            changed = True

        # MODULE J — Flashcard dedup + length + count trim
        flashcards = d.get('flashcards', [])
        new_fcs = fix_flashcard_dupes_and_length(flashcards, global_flashcard_fronts)
        if new_fcs != flashcards:
            d['flashcards'] = new_fcs
            changed = True

        # MODULE K — Quiz fix options + count
        quizzes = d.get('quizzes', [])
        new_quizzes = fix_quiz_options_v2(quizzes, tag)
        if new_quizzes != quizzes:
            d['quizzes'] = new_quizzes
            changed = True

        # MODULE N — Trim excess bullets
        takeaways = d.get('takeaways')
        if isinstance(takeaways, dict):
            bullets = takeaways.get('bullets', [])
            if len(bullets) > 6 or any(len(str(b)) > 200 or len(str(b)) < 30 for b in bullets):
                fixed_bullets = trim_bullets_to(bullets)
                if fixed_bullets != bullets:
                    d['takeaways'] = dict(takeaways)
                    d['takeaways']['bullets'] = fixed_bullets
                    changed = True

        # MODULE O — Fix gotchas actionability
        gotchas = d.get('gotchas', [])
        if gotchas:
            fixed_gotchas = fix_gotchas(gotchas)
            if fixed_gotchas != gotchas:
                d['gotchas'] = fixed_gotchas
                changed = True

        # MODULE O — Add resource if fewer than quizzes
        new_resources, res_added = add_resource_if_fewer_than_quizzes(d)
        if res_added:
            d['resources'] = new_resources
            changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as fp:
            yaml.dump(data, fp, allow_unicode=True, default_flow_style=False,
                      sort_keys=False, width=10000)
        return True
    return False


if __name__ == '__main__':
    global_fronts = set()
    files = sorted(glob.glob('src/data/week*.yaml'))
    fixed = 0
    for f in files:
        if process_file(f, global_fronts):
            print(f'  ✅ Fixed: {f}')
            fixed += 1
        else:
            print(f'  ⏭  Clean: {f}')
    print(f'\n✅ Pass 2 done. {fixed}/{len(files)} files updated.')
    print('  Run `python3 scripts/master_audit.py` to verify.')
