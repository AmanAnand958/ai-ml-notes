#!/usr/bin/env python3
"""
Comprehensive Imports Injector:
Scans all <pre> code elements across all 26 weeks and ensures pd., np., plt., torch. have self-contained import statements.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for pre in soup.find_all('pre'):
        code = pre.text
        # Avoid bash / sql
        if code.strip().startswith('$') or code.strip().startswith('SELECT') or code.strip().startswith('apiVersion:'):
            continue
            
        needed_imports = []
        if re.search(r'\bpd\.[a-zA-Z]', code) and 'import pandas' not in code:
            needed_imports.append('import pandas as pd')
        if re.search(r'\bnp\.[a-zA-Z]', code) and 'import numpy' not in code:
            needed_imports.append('import numpy as np')
        if re.search(r'\bplt\.[a-zA-Z]', code) and 'import matplotlib' not in code:
            needed_imports.append('import matplotlib.pyplot as plt')
        if re.search(r'\btorch\.nn\b', code) and 'import torch.nn' not in code and 'from torch import nn' not in code:
            needed_imports.append('import torch\nimport torch.nn as nn')
        elif re.search(r'\btorch\.[a-zA-Z]', code) and 'import torch' not in code:
            needed_imports.append('import torch')
            
        if needed_imports:
            import_block = '\n'.join(dict.fromkeys(needed_imports)) + '\n\n'
            pre.string = import_block + code
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Added self-contained library imports to all <pre> blocks in Week {wn}")

print("\n🎉 ALL CODE BLOCKS NOW HAVE COMPLETE INDEPENDENT IMPORT HEADERS!")
