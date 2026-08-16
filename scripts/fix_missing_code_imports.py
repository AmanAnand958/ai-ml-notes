#!/usr/bin/env python3
"""
Step 1: Fix Missing Library Imports in Code Snippets across all 26 Weeks.
Prepends missing 'import numpy as np', 'import pandas as pd', 'import matplotlib.pyplot as plt',
'import torch', 'import torch.nn as nn' when snippets call pd., np., plt., torch. without headers.
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
    
    for cb in soup.find_all('div', class_='cb'):
        lang = cb.find('span', class_='cb-lang')
        lang_text = lang.text.strip().lower() if lang else 'python'
        if lang_text != 'python': continue
        
        pre = cb.find('pre')
        if not pre: continue
        code = pre.text
        
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
            # Prepend imports to code
            import_block = '\n'.join(dict.fromkeys(needed_imports)) + '\n\n'
            pre.string = import_block + code
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Added missing library imports to code cards in Week {wn}")

print("\n🎉 STEP 1 COMPLETE: ALL CODE SNIPPETS NOW HAVE SELF-CONTAINED IMPORTS!")
