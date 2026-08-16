import os, re, ast
from bs4 import BeautifulSoup

weeks = range(19, 27)
print("=== DEEP AUDIT OF WEEKS 19-26: REAL CONTENT, DIAGRAMS & CURRICULUM COVERAGE ===\n")

for w in weeks:
    fn = f'pages/weeks/week{w}.html'
    if not os.path.exists(fn):
        print(f"❌ Missing {fn}")
        continue
    with open(fn, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    days = soup.find_all('div', class_='day-section')
    mermaids = soup.find_all('div', class_='mermaid')
    pres = soup.find_all('pre')
    math_blocks = soup.find_all(['div', 'span'], class_=re.compile(r'math'))
    case_studies = soup.find_all('div', class_='enterprise-case-study')
    qa_blocks = soup.find_all('div', class_='interview-qa-block')
    
    print(f"Week {w:2d} Audit:")
    print(f"  • Days: {len(days)} | Mermaid Diagrams: {len(mermaids)} | Code Blocks: {len(pres)} | Math Blocks: {len(math_blocks)}")
    print(f"  • Enterprise Case Studies: {len(case_studies)} | Interview QA Blocks: {len(qa_blocks)}")
    
    # Check Python syntax of all pre tags
    syntax_errs = 0
    for p in pres:
        code = p.get_text()
        if 'import ' in code or 'def ' in code or 'class ' in code:
            if not ('yaml' in str(p.parent) or 'docker' in str(p.parent) or 'bash' in str(p.parent)):
                try:
                    c_clean = code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    ast.parse(c_clean)
                except SyntaxError:
                    syntax_errs += 1
    print(f"  • Python Syntax Validation: {'✅ 100% Valid' if syntax_errs == 0 else f'❌ {syntax_errs} Syntax Errors'}")
    print()

