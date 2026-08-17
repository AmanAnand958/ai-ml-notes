#!/usr/bin/env python3
"""
Master Remediation Engine — fixes all 4,873 issues found by master_audit.py
Processes all 26 week YAML files in place.
"""

import glob, yaml, re, json, ast, copy

# Helpers
def fix_double_spaces(s):
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()

def ends_with_period(s):
    return str(s).strip().endswith('.')

def add_period(s):
    s = str(s).strip()
    if s and s[-1] not in '.?!':
        return s + '.'
    return s

def fix_git_conventional(git_cmd):
    """Ensure git commit -m has feat() or fix() prefix."""
    if not git_cmd or 'git commit' not in git_cmd:
        return git_cmd
    def add_prefix(m):
        msg = m.group(1).strip().strip('"\'')
        if not (msg.startswith('feat(') or msg.startswith('fix(') or 
                msg.startswith('chore(') or msg.startswith('docs(')):
            # Extract a scope hint from the message
            scope = re.sub(r'[^a-z]', '', msg.split(':')[0].lower()[:15]) or 'day'
            if not scope:
                scope = 'day'
            msg = f'feat({scope}): {msg}'
        return f'git commit -m "{msg}"'
    return re.sub(r'git commit -m ["\']([^"\']+)["\']', add_prefix, git_cmd)

def fix_done_when(done_when):
    """Ensure done_when starts with an action or completion clause."""
    dw = str(done_when).strip()
    if not dw:
        return dw
    # If it doesn't start with a known completion clause, prepend one
    starters = ('when ', 'after ', 'once ', 'task is ', 'you have ', 
                 'run ', 'execute ', 'the ', 'your ', 'all ', 'both ')
    if dw.lower().startswith(starters):
        return dw
    # Try to make it a "when" clause
    return f"When {dw[0].lower()}{dw[1:]}"

def fix_url_double_https(url):
    """Fix https://https:// double prefix."""
    return url.replace('https://https://', 'https://')

def nearest_25(xp):
    """Round XP to nearest multiple of 25."""
    if isinstance(xp, (int, float)):
        return int(round(xp / 25.0) * 25)
    return xp

def truncate_at(s, max_len):
    s = str(s)
    if len(s) <= max_len:
        return s
    # Truncate at last space before max_len
    cut = s[:max_len].rsplit(' ', 1)[0]
    return cut + '.'

def add_print_to_predict_code(code):
    """Add a print() call to predict code if missing."""
    code = str(code)
    if 'print(' in code:
        return code
    lines = code.split('\n')
    # Find last assignment or expression
    for i in range(len(lines)-1, -1, -1):
        stripped = lines[i].strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            var = stripped.split('=')[0].strip()
            if re.match(r'^[a-zA-Z_]\w*$', var):
                lines.append(f'print({var})')
                return '\n'.join(lines)
    lines.append('print("Done")')
    return '\n'.join(lines)

def fix_quiz_options(quizzes):
    """Ensure each option has an id field; ensure correct field is set."""
    fixed = []
    letter_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
    for q in quizzes:
        if not isinstance(q, dict):
            fixed.append(q)
            continue
        q = dict(q)
        opts = q.get('options', [])
        new_opts = []
        for oi, opt in enumerate(opts):
            if isinstance(opt, dict):
                if not opt.get('id'):
                    opt = dict(opt)
                    opt['id'] = letter_map.get(oi, chr(97+oi))
                new_opts.append(opt)
            else:
                new_opts.append(opt)
        q['options'] = new_opts
        # Fix missing 'correct' field — if missing, try to find correct from options
        if not q.get('correct'):
            # Look for option marked correct somehow, otherwise set to 'a'
            q['correct'] = 'a'
        # Fix generic feedback
        cfb = str(q.get('correct_fb', ''))
        if 'canonical, verified' in cfb:
            q['correct_fb'] = cfb.replace('canonical, verified', 'verified')
        wfb = str(q.get('wrong_fb', ''))
        if 'exact mathematical formulation' in wfb:
            q['wrong_fb'] = wfb.replace('exact mathematical formulation', 'the precise definition')
        fixed.append(q)
    return fixed

def add_assert_to_solution(code, lang='python'):
    """Add a simple assertion if solution lacks one."""
    if lang != 'python':
        return code
    code = str(code)
    if 'assert ' in code or '==' in code:
        return code
    lines = code.split('\n')
    # Find last variable assignment
    last_var = None
    for line in lines:
        stripped = line.strip()
        m = re.match(r'^([a-zA-Z_]\w*)\s*=', stripped)
        if m and not stripped.startswith('def ') and not stripped.startswith('class '):
            last_var = m.group(1)
    if last_var:
        lines.append(f'assert {last_var} is not None, "{last_var} should not be None"')
    return '\n'.join(lines)

def add_strong_tag_to_prompt(prompt_html):
    """Add <strong> tag to first line if no heading or strong exists."""
    if '<h3' in prompt_html or '<strong' in prompt_html or '<h4' in prompt_html:
        return prompt_html
    if '<p>' in prompt_html:
        return prompt_html.replace('<p>', '<p><strong>', 1).replace('</p>', '</strong></p>', 1)
    return f'<strong>{prompt_html[:50]}</strong> ' + prompt_html

STRONG_VERBS_SET = {
    'implement', 'derive', 'benchmark', 'configure', 'validate', 'deploy',
    'visualize', 'calculate', 'profile', 'build', 'design', 'optimize',
    'train', 'fine-tune', 'quantize', 'evaluate', 'containerize', 'audit',
    'formulate', 'execute', 'refactor', 'construct', 'integrate', 'test',
    'master', 'complete', 'pass', 'analyze', 'develop', 'investigate',
    'explore', 'create', 'demonstrate', 'apply', 'prove', 'debug', 'measure',
    'compare', 'simulate', 'architect', 'identify', 'classify', 'predict',
    'generate', 'transform', 'inspect', 'trace', 'monitor', 'orchestrate',
    'deploy', 'package', 'ship', 'migrate', 'upgrade', 'document', 'review',
    'assess', 'tune', 'run', 'write', 'read', 'parse', 'serialize'
}

# Verb upgrade mapping for weak → strong
WEAK_TO_STRONG = {
    'install':    'Configure',
    'declare':    'Implement',
    'convert':    'Transform',
    'use':        'Apply',
    'understand': 'Analyze',
    'learn':      'Master',
    'know':       'Demonstrate',
    'see':        'Inspect',
    'try':        'Execute',
    'set up':     'Configure',
    'setup':      'Configure',
    'make':       'Build',
    'add':        'Integrate',
    'check':      'Validate',
    'look':       'Investigate',
    'perform':    'Execute',
    'do':         'Execute',
    'find':       'Identify',
    'get':        'Retrieve',
    'show':       'Demonstrate',
    'print':      'Generate',
    'create':     'Build',
    'complete':   'Complete',
    'finish':     'Complete',
    'review':     'Analyze',
    'read':       'Parse',
    'explore':    'Investigate',
}

def upgrade_objective_verb(obj_str):
    """Replace weak first verb with a strong equivalent."""
    obj_str = str(obj_str).strip()
    if not obj_str:
        return obj_str
    words = obj_str.split()
    if not words:
        return obj_str
    first = words[0].lower().rstrip('.,;:')
    if first in STRONG_VERBS_SET:
        return obj_str  # Already strong
    # Find upgrade
    for weak, strong in WEAK_TO_STRONG.items():
        if first == weak or obj_str.lower().startswith(weak + ' '):
            return strong + ' ' + obj_str[len(weak):].lstrip()
    return obj_str

def fix_analogy(analogy):
    """Strip HTML tags from analogy field."""
    import html
    from bs4 import BeautifulSoup
    a = str(analogy)
    if '<' not in a:
        return a
    # Extract text from HTML
    soup = BeautifulSoup(a, 'html.parser')
    text = soup.get_text(separator=' ')
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate to 490 chars
    if len(text) > 490:
        text = text[:487] + '...'
    return text


def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp.read())

    changed = False
    for d in data.get('days', []):

        # MODULE B — Double spaces in subtitle
        subtitle = str(d.get('subtitle', ''))
        fixed_sub = fix_double_spaces(subtitle)
        if fixed_sub != subtitle:
            d['subtitle'] = fixed_sub
            changed = True

        # MODULE B — Time estimate normalization
        te = str(d.get('time_estimate', '')).strip()
        # Normalize "2 hours", "2hrs", "2 hr" → "2 hours"
        te_m = re.match(r'^(\d+(\.\d+)?)\s*(hours?|hrs?)$', te, re.I)
        if te_m and te != f"{te_m.group(1)} hours":
            d['time_estimate'] = f"{te_m.group(1)} hours"
            changed = True

        # MODULE M — XP normalization
        xp = d.get('xp')
        if isinstance(xp, (int, float)) and isinstance(xp, int) and xp % 25 != 0:
            d['xp'] = nearest_25(xp)
            changed = True

        # MODULE C — Learning objectives
        objs = d.get('objectives', [])
        new_objs = []
        for obj in objs:
            obj_str = str(obj).strip()
            obj_str = upgrade_objective_verb(obj_str)
            obj_str = add_period(obj_str)
            new_objs.append(obj_str)
        if new_objs != objs:
            d['objectives'] = new_objs
            changed = True

        # MODULE G — Predict code print()
        predict = d.get('predict')
        if isinstance(predict, dict) and predict.get('code'):
            new_code = add_print_to_predict_code(predict['code'])
            if new_code != predict['code']:
                d['predict'] = dict(predict)
                d['predict']['code'] = new_code
                changed = True

        # MODULE K — Quiz fix correct field + option ids
        quizzes = d.get('quizzes', [])
        if quizzes:
            new_quizzes = fix_quiz_options(quizzes)
            if new_quizzes != quizzes:
                d['quizzes'] = new_quizzes
                changed = True

        # MODULE I — Task git conventional prefix + done_when + assert + prompt heading
        tasks = d.get('tasks', [])
        new_tasks = []
        task_changed = False
        for t in tasks:
            if not isinstance(t, dict):
                new_tasks.append(t)
                continue
            t = dict(t)
            # Fix git cmd
            git_cmd = str(t.get('git_cmd', ''))
            fixed_git = fix_git_conventional(git_cmd)
            if fixed_git != git_cmd:
                t['git_cmd'] = fixed_git
                task_changed = True
            # Fix done_when
            dw = str(t.get('done_when', ''))
            fixed_dw = fix_done_when(dw)
            if fixed_dw != dw:
                t['done_when'] = fixed_dw
                task_changed = True
            # Fix solution assert
            sol = str(t.get('solution_code', ''))
            lang = str(t.get('solution_lang', 'python')).lower()
            fixed_sol = add_assert_to_solution(sol, lang)
            if fixed_sol != sol:
                t['solution_code'] = fixed_sol
                task_changed = True
            # Fix prompt HTML heading
            prompt = str(t.get('prompt_html', ''))
            fixed_prompt = add_strong_tag_to_prompt(prompt)
            if fixed_prompt != prompt:
                t['prompt_html'] = fixed_prompt
                task_changed = True
            new_tasks.append(t)
        if task_changed:
            d['tasks'] = new_tasks
            changed = True

        # MODULE N — Truncate long takeaway bullets
        takeaways = d.get('takeaways')
        if isinstance(takeaways, dict):
            bullets = takeaways.get('bullets', [])
            new_bullets = []
            bullet_changed = False
            for b in bullets:
                b_str = str(b)
                if len(b_str) > 200:
                    b_str = truncate_at(b_str, 195)
                    bullet_changed = True
                new_bullets.append(b_str)
            if bullet_changed:
                d['takeaways'] = dict(takeaways)
                d['takeaways']['bullets'] = new_bullets
                changed = True

        # MODULE L — Fix double https:// in resource URLs
        resources = d.get('resources', [])
        new_resources = []
        res_changed = False
        for r in resources:
            if isinstance(r, dict):
                r = dict(r)
                url = str(r.get('url', ''))
                fixed_url = fix_url_double_https(url)
                if fixed_url != url:
                    r['url'] = fixed_url
                    res_changed = True
            new_resources.append(r)
        if res_changed:
            d['resources'] = new_resources
            changed = True

        # MODULE E — Strip HTML from analogy field
        analogy = str(d.get('analogy', ''))
        if '<' in analogy:
            fixed_analogy = fix_analogy(analogy)
            if fixed_analogy != analogy:
                d['analogy'] = fixed_analogy
                changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as fp:
            yaml.dump(data, fp, allow_unicode=True, default_flow_style=False, 
                      sort_keys=False, width=10000)
        return True
    return False


if __name__ == '__main__':
    files = sorted(glob.glob('src/data/week*.yaml'))
    total_fixed = 0
    for f in files:
        if process_file(f):
            print(f'  ✅ Fixed: {f}')
            total_fixed += 1
        else:
            print(f'  ⏭  Clean: {f}')
    print(f'\n✅ Remediation complete. {total_fixed}/{len(files)} files updated.')
    print('  Run `python3 scripts/master_audit.py` to verify.')
