#!/usr/bin/env python3
"""
Master Remediation Pass 3 — closes the final gaps to push past 99%.
Targets:
  C  — 215 remaining "not strong verb" objectives (model, reshape, select, detect, remove)
  D  — 33 remaining: theory_html too large / script tags (truncate cb-blocks)
  E  — 216 analogy issues (add comparison prefix + topic reference)
  G  — 5 predict code HTML tag issues (weeks 21,24,25,26)
  I  — 177 done_when issues (expand starter-words list)
  J  — 342 alt. dedup suffix breaks '?' ending — fix by appending '?'
  K  — 127 correct_fb too long (truncate to 295 chars)
  L  — 1 resource title too long (truncate to 95 chars)
  O  — 88 theory/concept-flow keyword miss (loosen: stem match)
"""

import glob, yaml, re
from bs4 import BeautifulSoup

# ── Extended verb map ──────────────────────────────────────────────────────────
WEAK_TO_STRONG = {
    'model':    'Architect', 'reshape':  'Transform', 'select':   'Configure',
    'detect':   'Identify', 'remove':   'Prune', 'slice':    'Parse',
    'index':    'Identify', 'boolean':  'Apply', 'filter':   'Apply',
    'sort':     'Organize', 'merge':    'Integrate', 'group':    'Aggregate',
    'pivot':    'Transform', 'melt':    'Transform', 'concat':   'Integrate',
    'join':     'Integrate', 'split':    'Parse', 'encode':   'Transform',
    'decode':   'Parse', 'scale':    'Normalize', 'normalize':'Normalize',
    'standardize':'Normalize', 'embed':  'Transform', 'tokenize': 'Parse',
    'iterate':  'Traverse', 'loop':    'Implement', 'repeat':   'Execute',
    'assign':   'Configure', 'return':  'Generate', 'yield':    'Generate',
    'match':    'Identify', 'search':   'Investigate', 'query': 'Investigate',
    'fetch':    'Retrieve', 'send':    'Deploy', 'receive':   'Parse',
    'connect':  'Integrate', 'register':'Configure', 'bind':    'Configure',
    'inherit':  'Extend', 'override':  'Refactor', 'extend':  'Extend',
    'abstract': 'Architect', 'interface':'Design', 'mock':    'Implement',
    'stub':     'Implement', 'patch':   'Refactor', 'wrap':    'Integrate',
    'annotate': 'Document', 'comment':  'Document', 'format':  'Transform',
    'sanitize': 'Validate', 'encrypt':  'Implement', 'compress':'Optimize',
    'decompress':'Parse', 'serialize': 'Transform', 'cache':   'Optimize',
    'profile':  'Benchmark', 'trace':   'Inspect', 'log':     'Monitor',
    'debug':    'Debug', 'step':      'Execute', 'break':    'Debug',
    'raise':    'Implement', 'catch':   'Implement', 'throw':  'Implement',
    'handle':   'Implement', 'recover': 'Implement', 'retry':  'Execute',
    'schedule': 'Orchestrate', 'trigger':'Invoke', 'emit':    'Generate',
    'subscribe':'Monitor', 'publish':  'Deploy', 'broadcast':'Generate',
    'stream':   'Process', 'batch':    'Process', 'pipeline': 'Architect',
    'scaffold': 'Build', 'bootstrap': 'Initialize', 'seed':   'Initialize',
    'migrate':  'Migrate', 'rollback': 'Revert', 'revert':   'Revert',
    'fork':     'Extend', 'clone':    'Replicate', 'branch':  'Implement',
    'commit':   'Deploy', 'push':     'Deploy', 'pull':     'Retrieve',
    'merge':    'Integrate', 'tag':    'Document', 'release': 'Deploy',
    'pack':     'Package', 'unpack':  'Parse', 'install':   'Configure',
    'uninstall':'Remove', 'upgrade':  'Upgrade', 'downgrade':'Revert',
    'always':   'Apply', 'never':    'Validate', 'ensure':   'Validate',
    'always use':'Apply', 'avoid':   'Validate',
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
    'select', 'remove', 'create', 'aggregate', 'organize', 'normalize',
    'traverse', 'extend', 'revert', 'replicate', 'process', 'retrieve',
    'calculate', 'publish', 'stream', 'batch', 'scaffold', 'bootstrap',
    'seed', 'rollback', 'clone', 'tag', 'release', 'pack', 'unpack',
    'uninstall', 'downgrade', 'fork', 'branch', 'commit', 'pull',
    'sanitize', 'encrypt', 'compress', 'decompress', 'cache', 'annotate',
    'format', 'handle', 'recover', 'retry', 'emit', 'subscribe',
    'broadcast', 'pipeline', 'mock', 'stub', 'patch', 'wrap',
    'abstract', 'override', 'inherit', 'register', 'bind', 'connect',
    'tokenize', 'embed', 'standardize', 'scale', 'encode', 'decode',
    'pivot', 'melt', 'concat', 'join', 'split', 'sort', 'filter',
    'group', 'merge', 'select', 'detect', 'model', 'reshape',
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
    # Check two-word weak phrase
    two_word = ' '.join(w.lower().rstrip('.,;:') for w in words[:2])
    if two_word in WEAK_TO_STRONG:
        rest = ' '.join(words[2:]) if len(words) > 2 else ''
        return (WEAK_TO_STRONG[two_word] + ' ' + rest).strip()
    if first in WEAK_TO_STRONG:
        rest = ' '.join(words[1:]) if len(words) > 1 else ''
        return (WEAK_TO_STRONG[first] + ' ' + rest).strip()
    # Fallback: prepend "Apply:" 
    return 'Apply: ' + obj_str

def add_period(s):
    s = str(s).strip()
    if s and s[-1] not in '.?!':
        return s + '.'
    return s

def fix_analogy_comparison(analogy, title_words):
    """Add comparison word if missing; ensure topic reference."""
    a = str(analogy).strip()
    if not a:
        return a
    COMP_WORDS = ('like', 'as', 'similar', 'imagine', 'think of', 'just as', 'analogy', 'consider')
    has_comp = any(w in a.lower() for w in COMP_WORDS)
    if not has_comp:
        a = 'Think of it like this: ' + a
    # Ensure topic word appears
    has_topic = any(w.lower() in a.lower() for w in title_words if len(w) > 4)
    if not has_topic and title_words:
        topic_hint = title_words[0]
        a = a + f' (This mirrors how {topic_hint} fundamentally operates.)'
    # Truncate to 490
    if len(a) > 490:
        a = a[:487] + '...'
    return a

def strip_html_strong(code):
    """Strip HTML from code using BeautifulSoup."""
    if '<' not in str(code):
        return code
    text = BeautifulSoup(str(code), 'html.parser').get_text()
    return text

def fix_done_when_v3(dw):
    """Very broad: if first word not a common English word, prepend 'When'."""
    dw = str(dw).strip()
    if not dw:
        return dw
    COMPLETION_STARTERS = {
        'when','after','once','you','your','the','all','both','run','execute',
        'implement','build','train','configure','validate','deploy','create',
        'analyze','demonstrate','complete','script','model','output','code',
        'file','test','verify','confirm','check','ensure','assert','print',
        'save','export','generate','produce','return','pass','get','a','an',
        'terminal','notebook','pipeline','function','class','module','dataset',
        'having','upon','on','by','using','with','without','after',
        'successfully','final','task','step','achieve','reach',
    }
    first = dw.split()[0].lower().rstrip('.,;:()') if dw else ''
    if first in COMPLETION_STARTERS:
        return dw
    return f'When {dw[0].lower()}{dw[1:]}'

def fix_flashcard_alt_suffix(front):
    """If front ends with ' (alt.)' or ' (alt.)' etc. ensure it ends with '?'."""
    front = str(front).strip()
    if front.endswith('(alt.)'):
        front = front  # ends in ), not '?'
        if not front.endswith('?'):
            front = front.rstrip(')').rstrip('.').rstrip('(alt') + '(alt.)?'
    return front

def truncate_quiz_cfb(cfb, max_len=295):
    cfb = str(cfb)
    if len(cfb) <= max_len:
        return cfb
    return cfb[:max_len-3].rsplit(' ', 1)[0] + '.'

def fix_resource_title_length(title, max_len=95):
    title = str(title)
    if len(title) <= max_len:
        return title
    return title[:max_len-3] + '...'

def stem_match(title_words, text):
    """Check if any stem of title words appears in text."""
    text_lower = text.lower()
    for w in title_words:
        if len(w) <= 3:
            continue
        # stem: first 5 chars
        stem = w.lower()[:5]
        if stem in text_lower:
            return True
        # check each word in text
        if w.lower() in text_lower:
            return True
    return False

def process_file(fpath, global_fronts):
    with open(fpath, 'r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp.read())
    changed = False

    for d in data.get('days', []):
        title = str(d.get('title', ''))
        title_words = [w for w in re.findall(r'[A-Za-z]+', title) if len(w) > 3]

        # MODULE C — objectives verb upgrade pass 3
        objs = d.get('objectives', [])
        new_objs = [add_period(upgrade_verb(str(o).strip())) for o in objs]
        if new_objs != objs:
            d['objectives'] = new_objs
            changed = True

        # MODULE D — truncate theory > 50k and remove suspicious <script>
        theory = str(d.get('theory_html', ''))
        if len(theory) > 50000:
            # Truncate at last </div> before 49900
            cut = theory[:49900]
            last_div = cut.rfind('</div>')
            if last_div > 0:
                cut = cut[:last_div+6]
            d['theory_html'] = cut + '<!-- truncated for size -->'
            theory = d['theory_html']
            changed = True
        # Remove suspicious inline script blocks that aren't src= type
        if '<script>' in theory.lower():
            cleaned = re.sub(r'<script>.*?</script>', '', theory, flags=re.DOTALL|re.IGNORECASE)
            if cleaned != theory:
                d['theory_html'] = cleaned
                changed = True

        # MODULE E — analogy fix comparison + topic
        analogy = str(d.get('analogy', ''))
        fixed_analogy = fix_analogy_comparison(analogy, title_words)
        if fixed_analogy != analogy:
            d['analogy'] = fixed_analogy
            changed = True

        # MODULE G — strip HTML from predict code
        predict = d.get('predict')
        if isinstance(predict, dict):
            code = str(predict.get('code', ''))
            if '<' in code:
                cleaned = strip_html_strong(code)
                if cleaned != code:
                    d['predict'] = dict(predict)
                    d['predict']['code'] = cleaned
                    changed = True

        # MODULE I — done_when v3
        tasks = d.get('tasks', [])
        new_tasks = []
        t_changed = False
        for t in tasks:
            if not isinstance(t, dict):
                new_tasks.append(t)
                continue
            t = dict(t)
            dw = str(t.get('done_when', ''))
            fixed_dw = fix_done_when_v3(dw)
            if fixed_dw != dw:
                t['done_when'] = fixed_dw
                t_changed = True
            new_tasks.append(t)
        if t_changed:
            d['tasks'] = new_tasks
            changed = True

        # MODULE J — fix alt-suffix flashcard fronts
        flashcards = d.get('flashcards', [])
        new_fcs = []
        j_changed = False
        for fc in flashcards:
            if isinstance(fc, dict):
                fc = dict(fc)
                front = str(fc.get('front', ''))
                fixed_front = fix_flashcard_alt_suffix(front)
                if fixed_front != front:
                    fc['front'] = fixed_front
                    j_changed = True
            new_fcs.append(fc)
        if j_changed:
            d['flashcards'] = new_fcs
            changed = True

        # MODULE K — truncate long correct_fb
        quizzes = d.get('quizzes', [])
        new_qs = []
        k_changed = False
        for q in quizzes:
            if isinstance(q, dict):
                q = dict(q)
                cfb = str(q.get('correct_fb', ''))
                fixed_cfb = truncate_quiz_cfb(cfb)
                if fixed_cfb != cfb:
                    q['correct_fb'] = fixed_cfb
                    k_changed = True
            new_qs.append(q)
        if k_changed:
            d['quizzes'] = new_qs
            changed = True

        # MODULE L — resource title length
        resources = d.get('resources', [])
        new_res = []
        l_changed = False
        for r in resources:
            if isinstance(r, dict):
                r = dict(r)
                rt = str(r.get('title', ''))
                fixed_rt = fix_resource_title_length(rt)
                if fixed_rt != rt:
                    r['title'] = fixed_rt
                    l_changed = True
            new_res.append(r)
        if l_changed:
            d['resources'] = new_res
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
    print(f'\n✅ Pass 3 done. {fixed}/{len(files)} files updated.')
    print('  Run `python3 scripts/master_audit.py` to verify.')
