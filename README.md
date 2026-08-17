# 🚀 26-Week AI/ML Interactive Course

A comprehensive, gamified 26-week curriculum (191 days) covering the complete path from Python foundations to Production Multimodal Deep Learning and LLM Systems.

---

## 🏛️ Architecture: Template + Data + Build + Validate

The course uses a **single-source compiler architecture**. Monolithic HTML files are never edited by hand.

```
/src
  /data
    week01.yaml ... week26.yaml    # Pure content: titles, objectives, theory, tasks, quizzes, flashcards
  /template
    week.template.html             # Single Jinja2 template for all 26 weeks
  /schema
    contract.json                  # Contract defining allowed JS functions & DOM IDs
    week.schema.json               # Content data schema
  /scripts
    extract_legacy_data.py         # Forensic parser to extract v0 HTML into structured YAML
    build.py                       # Jinja2 compiler: template + data -> pages/weeks/weekN.html
    validate.py                    # Multi-point mechanical validation suite
/v0_snapshot                       # Read-only freeze of legacy baseline files
pages/weeks/                       # Compiled build output (with auto-generated banner)
```

---

## 🛠️ Developer Workflow

### 1. Editing Content
All curriculum updates, quiz questions, tasks, code snippets, and explanations must be edited in the structured YAML files under `/src/data/`:
```bash
# Example: Edit Day 1 variables & tasks
src/data/week01.yaml
```

### 2. Building Week Pages
To compile the YAML data files and Jinja2 template into production HTML files:
```bash
# Build all 26 weeks
npm run build
# OR
python3 scripts/build.py

# Build a single week (e.g. Week 4)
python3 scripts/build.py 4
```

### 3. Validating Correctness
Run the mechanical validator to check function contracts, DOM IDs, KaTeX formulas, and HTML validity:
```bash
npm test
# OR
python3 scripts/validate.py pages/weeks
```

---

## 📜 Contract & Standards (`src/schema/contract.json`)

All pages adhere to the strict runtime contract:
- **Exposed JS functions**: `quiz()`, `completeDay()`, `checkPredict()`, `toggleTask()`, `toggleSolution()`, `toggleCheck()`, `copyCode()`, `runCode()`, `openRepl()`, `openInColab()`, `jumpTo()`, `toggleTheme()`.
- **LocalStorage Isolation**: Every week page automatically isolates its progress and state key (`w${WEEK}-state`).
- **Mechanical Validation**: 100% pass required on all pull requests and commits.
