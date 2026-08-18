#!/usr/bin/env python3
"""
scripts/fix_remaining_katex_exact.py
Fixes remaining KaTeX errors:
- Double superscripts
- Line break before ight
- \t before \text / _heta
- $ > \ $ escaping
"""

import glob
import re

def fix_content(content):
    # Fix double superscript in week13:
    content = content.replace("v'_{w_O}^\\top", "{v'_{w_O}}^\\top")
    content = content.replace("v'_{w_i}^\\top", "{v'_{w_i}}^\\top")
    content = content.replace("v'_{w_O}^\top", "{v'_{w_O}}^\\top")
    content = content.replace("v'_{w_i}^\top", "{v'_{w_i}}^\\top")

    # Fix newline/carriage return before ight:
    content = re.sub(r'[\r\n\s]*\n\s*ight\)', r' \\right)', content)
    content = re.sub(r'[\r\n\s]*\n\s*ight\]', r' \\right]', content)
    content = re.sub(r'[\r\n\s]*\n\s*ight\}', r' \\right\\}', content)
    content = re.sub(r'[\r\n\s]*\n\s*ight\|', r' \\right|', content)
    content = re.sub(r'[\r\n\s]*\n\s*ight\b', r' \\right', content)
    content = re.sub(r'[\r\n\s]*\r\s*ight\)', r' \\right)', content)
    content = re.sub(r'[\r\n\s]*\r\s*ight\]', r' \\right]', content)
    content = re.sub(r'[\r\n\s]*\r\s*ight\}', r' \\right\\}', content)
    content = re.sub(r'[\r\n\s]*\r\s*ight\|', r' \\right|', content)
    content = re.sub(r'[\r\n\s]*\r\s*ight\b', r' \\right', content)

    # Any remaining 'ight)' or 'ight]' in math:
    content = re.sub(r'(?<=\s)ight\)', r'\\right)', content)
    content = re.sub(r'(?<=\s)ight\]', r'\\right]', content)
    content = re.sub(r'(?<=\s)ight\}', r'\\right\\}', content)
    content = re.sub(r'(?<=\s)ight\|', r'\\right|', content)
    content = re.sub(r'(?<=\s)ight\b', r'\\right', content)

    # Fix tab before \text or \times:
    content = re.sub(r'\t+\\text', r'\\text', content)
    content = re.sub(r'\t+\\times', r'\\times', content)
    content = re.sub(r'\t+\\IDF', r'\\text{IDF}', content)
    content = re.sub(r'\t+\\Softmax', r'\\text{Softmax}', content)
    content = re.sub(r'\t+\\accept', r'\\text{accept}', content)
    content = re.sub(r'\t+\\ref', r'\\text{ref}', content)
    content = re.sub(r'\t+\\pos', r'\\text{pos}', content)
    content = re.sub(r'\t+\\Required', r'\\text{Required}', content)
    content = re.sub(r'\t+\\weights', r'\\text{weights}', content)
    content = re.sub(r'\t+\\size', r'\\text{size}', content)
    content = re.sub(r'\t+\\Buffer', r'\\text{Buffer}', content)
    content = re.sub(r'\t+\\distill', r'\\text{distill}', content)
    content = re.sub(r'\t+\\DPO', r'\\text{DPO}', content)
    content = re.sub(r'\t+\\class', r'\\text{class}', content)
    content = re.sub(r'\t+\\patches', r'\\text{patches}', content)
    content = re.sub(r'\t_heta', r'\\theta', content)
    content = re.sub(r'\t+heta', r'\\theta', content)
    content = re.sub(r'\t+imes', r'\\times', content)
    content = re.sub(r'\t+ext', r'\\text', content)
    content = re.sub(r'\b_heta\b', r'\\theta', content)
    content = re.sub(r'(?<=\()\s*pi_\\theta', r'\\pi_\\theta', content)
    content = re.sub(r'(?<=\()\s*\\pi_\s*heta', r'\\pi_\\theta', content)
    content = re.sub(r'pi_\s*heta', r'\\pi_\\theta', content)

    # Fix broken inline $> \ $ in week20
    content = content.replace(r'$ > \ $', r'$ > $')
    content = content.replace(r'$> \$', r'$ > $')

    return content

for f in sorted(glob.glob('pages/weeks/week*.html') + glob.glob('src/data/week*.yaml')):
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    nc = fix_content(c)
    if nc != c:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(nc)
        print(f"Fixed {f}")
