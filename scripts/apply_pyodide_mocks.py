#!/usr/bin/env python3
"""
apply_pyodide_mocks.py
Injects sys.modules mocks for Pyodide-incompatible libraries (torch, mlflow, faiss, boto3)
at the top of affected <pre> code blocks so the browser runner doesn't crash.
"""

import re
import glob

def inject_mocks(html: str) -> tuple[str, int]:
    count = 0
    
    # We look for <pre> or <pre><code> that contains any of the bad imports.
    # We will use re.finditer to replace them.
    
    pattern = r'(<pre(?:[^>]*)>)(?:<code(?:[^>]*)>)?(.*?)(?:</code>)?</pre>'
    
    def replacer(match):
        nonlocal count
        pre_tag = match.group(1)
        code_content = match.group(2)
        
        # Check if it has any bad imports
        bad_imports = []
        if re.search(r'^\s*(import|from)\s+torch\b', code_content, re.MULTILINE): bad_imports.append('torch')
        if re.search(r'^\s*(import|from)\s+mlflow\b', code_content, re.MULTILINE): bad_imports.append('mlflow')
        if re.search(r'^\s*(import|from)\s+faiss\b', code_content, re.MULTILINE): bad_imports.append('faiss')
        if re.search(r'^\s*(import|from)\s+boto3\b', code_content, re.MULTILINE): bad_imports.append('boto3')
        
        if not bad_imports:
            return match.group(0) # No change
            
        # It has bad imports, check if we already mocked it
        if 'sys.modules[' in code_content and 'MagicMock' in code_content:
            return match.group(0) # Already mocked
            
        count += 1
        
        # Generate the mock injection
        mock_code = 'import sys\nfrom unittest.mock import MagicMock\n'
        for lib in bad_imports:
            if lib == 'torch':
                mock_code += 'sys.modules["torch"] = MagicMock()\n'
                mock_code += 'sys.modules["torch.nn"] = MagicMock()\n'
                mock_code += 'sys.modules["torch.nn.functional"] = MagicMock()\n'
                mock_code += 'sys.modules["torch.utils"] = MagicMock()\n'
                mock_code += 'sys.modules["torch.utils.data"] = MagicMock()\n'
            else:
                mock_code += f'sys.modules["{lib}"] = MagicMock()\n'
        
        mock_code += '\n'
        
        # We need to preserve the original tag structure. 
        # If the original was <pre><code>...</code></pre>, we should keep it.
        # But my regex captures the inner content and we can just reconstruct a <pre> block.
        # Since I replaced some with just <pre> earlier, let's just output <pre>
        return f'{pre_tag}\n{mock_code}{code_content.lstrip()}</pre>'
        
    new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)
    return new_html, count

def main():
    print("=" * 65)
    print("PYODIDE MOCK INJECTION")
    print("=" * 65)
    
    total = 0
    files = glob.glob("pages/weeks/*.html")
    for f in files:
        html = open(f, encoding='utf-8').read()
        new_html, cnt = inject_mocks(html)
        if cnt > 0:
            with open(f, 'w', encoding='utf-8') as out:
                out.write(new_html)
            print(f"  {f}: {cnt} blocks mocked")
            total += cnt
            
    print(f"\nTotal: {total} blocks mocked.")

if __name__ == '__main__':
    main()
