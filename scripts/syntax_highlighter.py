"""
scripts/syntax_highlighter.py
Token-based Python syntax highlighter using standard library tokenize.
Preserves exact indentation and formatting while applying CSS classes:
<span class="kw">, <span class="fn">, <span class="cls">, <span class="str">, <span class="num">, <span class="cm">.
"""

import io, tokenize, html

KEYWORDS = {
    'import', 'from', 'as', 'def', 'class', 'return', 'if', 'else', 'elif',
    'for', 'while', 'in', 'is', 'not', 'and', 'or', 'with', 'try', 'except',
    'finally', 'raise', 'assert', 'yield', 'lambda', 'True', 'False', 'None',
    'async', 'await', 'pass', 'break', 'continue', 'self'
}

def highlight_python_code(code_str: str) -> str:
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code_str.strip()).readline))
        result = []
        last_row, last_col = 1, 0
        prev_tok = None
        
        for tok_type, tok_val, (srow, scol), (erow, ecol), _ in tokens:
            # Handle newlines and indentation
            if srow > last_row:
                result.append('\n' * (srow - last_row))
                last_col = 0
            if scol > last_col:
                result.append(' ' * (scol - last_col))
                
            if tok_type == tokenize.NAME:
                if tok_val in KEYWORDS:
                    result.append(f'<span class="kw">{tok_val}</span>')
                elif prev_tok and prev_tok[1] == 'def':
                    result.append(f'<span class="fn">{tok_val}</span>')
                elif prev_tok and prev_tok[1] == 'class':
                    result.append(f'<span class="cls">{tok_val}</span>')
                else:
                    result.append(html.escape(tok_val))
            elif tok_type == tokenize.STRING:
                result.append(f'<span class="str">{html.escape(tok_val)}</span>')
            elif tok_type == tokenize.NUMBER:
                result.append(f'<span class="num">{tok_val}</span>')
            elif tok_type == tokenize.COMMENT:
                result.append(f'<span class="cm">{html.escape(tok_val)}</span>')
            elif tok_type in (tokenize.NEWLINE, tokenize.NL):
                pass # Handled by srow tracking
            elif tok_type == tokenize.ENDMARKER:
                pass
            else:
                result.append(html.escape(tok_val))
                
            last_row, last_col = erow, ecol
            if tok_type not in (tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE, tokenize.NL):
                prev_tok = (tok_type, tok_val)
                
        return ''.join(result).strip()
    except Exception:
        # Fallback to escaped string if tokenization fails
        return html.escape(code_str.strip())

def make_cb(title_lang: str, code_str: str) -> str:
    hl_code = highlight_python_code(code_str)
    return f"""<div class="cb">
<div class="cb-head">
<span class="cb-lang">{title_lang.upper()}</span>
<div class="cb-btns">
<button class="copy-btn" onclick="copyCode(this)">copy</button>
<button class="run-btn" onclick="runCode(this)" style="margin-left: 4px;">Run</button>
</div>
</div>
<pre><code>{hl_code}</code></pre>
</div>"""
