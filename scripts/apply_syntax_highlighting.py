#!/usr/bin/env python3
"""
apply_syntax_highlighting.py
Heuristically assigns missing language classes to code blocks across the curriculum.
"""

import re
import glob

WEEKS_DIR = "pages/weeks"

def determine_language(code_content: str) -> str:
    """Returns the most likely PrismJS language class based on content heuristics."""
    content = code_content.strip()
    
    # Empty or very short
    if not content:
        return "language-plaintext"
        
    # SQL
    if content.upper().startswith("SELECT ") or content.upper().startswith("WITH ") or "CREATE TABLE" in content.upper() or "CREATE VIEW" in content.upper() or "UPDATE " in content.upper() or "CREATE EXTENSION" in content.upper() or "EXPLAIN " in content.upper() or "BEGIN;" in content:
        return "language-sql"
        
    # Bash / Shell
    if "#!/usr/bin/env bash" in content or "docker run" in content or "docker build" in content or content.startswith("$") or content.startswith("pip install") or "apt-get" in content or "kubectl " in content or "dvc init" in content or content.startswith("# Initialize"):
        return "language-bash"
        
    # Dockerfile
    if "FROM " in content and ("WORKDIR " in content or "COPY " in content or "RUN " in content):
        return "language-docker"
        
    # YAML
    if ("version:" in content and "services:" in content) or ("apiVersion:" in content and "kind:" in content and "metadata:" in content) or "model:" in content and "name:" in content:
        return "language-yaml"
        
    # JSON
    if content.startswith("{") and content.endswith("}") and '"' in content:
        return "language-json"
        
    # HTML
    if content.startswith("<") and ">" in content and "</" in content:
        return "language-html"
        
    # Python (default for ML course)
    if "import " in content or "def " in content or "class " in content or "print(" in content or "from " in content or " = " in content or "df[" in content or "[]" in content or "if " in content or "for " in content:
        return "language-python"
        
    # Fallback to plain text if no clear markers
    return "language-plaintext"

def inject_classes(html: str) -> tuple[str, int]:
    count = 0
    
    # Match <pre><code>...</code></pre> where <code> has NO class
    # We use a regex that matches <code> without class="something"
    
    # We want to replace `<pre><code>` with `<pre><code class="...">`
    # and `<pre><code>\n` with `<pre><code class="...">\n`
    
    def replacer(match):
        nonlocal count
        pre_tag = match.group(1)
        code_tag = match.group(2)
        inner_content = match.group(3)
        
        # If it already has a class, skip, unless it's plaintext
        if 'class=' in code_tag and 'language-plaintext' not in code_tag:
            return match.group(0)
            
        lang = determine_language(inner_content)
        
        # Don't increment if we guessed plaintext and it was already plaintext
        if 'language-plaintext' in code_tag and lang == 'language-plaintext':
            return match.group(0)
            
        count += 1
        return f'{pre_tag}<code class="{lang}">{inner_content}</code></pre>'

    # Pattern captures: (1) <pre...> (2) <code...> (3) content
    pattern = r'(<pre[^>]*>)\s*(<code[^>]*>)(.*?)</code>\s*</pre>'
    new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)
    
    return new_html, count

def main():
    print("=" * 65)
    print("SYNTAX HIGHLIGHTING INJECTION")
    print("=" * 65)
    
    total = 0
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    for f in sorted(files):
        html = open(f, encoding='utf-8').read()
        new_html, cnt = inject_classes(html)
        if cnt > 0:
            with open(f, 'w', encoding='utf-8') as out:
                out.write(new_html)
            print(f"  {f}: {cnt} blocks formatted")
            total += cnt
            
    print(f"\nTotal: {total} blocks formatted.")

if __name__ == '__main__':
    main()
