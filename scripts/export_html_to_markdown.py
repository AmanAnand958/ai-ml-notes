#!/usr/bin/env python3
"""
Export the generated week HTML pages into editable Markdown notes.

The output is intentionally separate from the existing site:
  markdown-notes/
    README.md
    manifest.json
    weeks/week01.md ... week26.md

This is a source-authoring escape hatch for the course content. It strips
navigation/runtime chrome and keeps the actual notes, tasks, quizzes, code,
tables, diagrams, and resources in a safer Markdown representation.
"""

from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, Comment, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / "pages" / "weeks"
OUT_DIR = ROOT / "markdown-notes"
WEEKS_DIR = OUT_DIR / "weeks"

SKIP_CLASSES = {
    "topnav",
    "sidebar",
    "xp-toast",
    "prog-wrap",
    "day-pills",
    "mob-menu-btn",
    "theme-btn",
    "cb-head",
    "day-tag",
}

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "canvas",
    "dd",
    "details",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "ul",
}


def clean_text(value: str) -> str:
    value = unescape(value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def collapse_blank_lines(value: str) -> str:
    lines = [line.rstrip() for line in value.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def fence_lang_from_block(block: Tag) -> str:
    labels: list[str] = []
    previous = block.find_previous("span", class_="cb-lang")
    if previous:
        labels.append(previous.get_text(" ", strip=True))
    classes = block.get("class") or []
    labels.extend(classes)
    code = block.find("code") if block.name == "pre" else block
    if isinstance(code, Tag):
        labels.extend(code.get("class") or [])

    label = " ".join(labels).lower()
    if "python" in label:
        return "python"
    if "yaml" in label or "yml" in label:
        return "yaml"
    if "json" in label:
        return "json"
    if "dockerfile" in label or "docker" in label:
        return "dockerfile"
    if "shell" in label or "bash" in label or "terminal" in label:
        return "bash"
    if "markdown" in label or "readme" in label:
        return "markdown"
    if "mermaid" in label:
        return "mermaid"
    if "sql" in label:
        return "sql"
    if "javascript" in label or "js" in label:
        return "javascript"
    if "expected output" in label or "output" in label:
        return "text"
    return ""


def code_text(block: Tag) -> str:
    code = block.find("code") if block.name == "pre" else block
    if isinstance(code, Tag):
        text = code.get_text("", strip=False)
    else:
        text = block.get_text("", strip=False)
    return text.strip("\n")


def table_to_markdown(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False)
        if not cells:
            continue
        rows.append([clean_text(cell.get_text(" ", strip=True)).replace("|", "\\|") for cell in cells])
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header = rows[0]
    body = rows[1:]
    out = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    out.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(out)


def inline_markdown(node: Tag | NavigableString) -> str:
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""

    name = node.name.lower()
    text = "".join(inline_markdown(child) for child in node.children)
    text = clean_text(text)

    if name in {"strong", "b"} and text:
        return f"**{text}**"
    if name in {"em", "i"} and text:
        return f"*{text}*"
    if name == "code" and text:
        return f"`{text}`"
    if name == "br":
        return "\n"
    if name == "a":
        href = node.get("href", "").strip()
        if href and text:
            return f"[{text}]({href})"
        return text
    return text


def should_skip(tag: Tag) -> bool:
    classes = set(tag.get("class") or [])
    if classes & SKIP_CLASSES:
        return True
    if tag.name in {"script", "style", "link", "meta", "nav", "aside"}:
        return True
    if tag.name == "button":
        return True
    return False


def children_blocks(tag: Tag) -> Iterable[Tag | NavigableString]:
    for child in tag.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            if child.strip():
                yield child
            continue
        if isinstance(child, Tag) and not should_skip(child):
            yield child


def block_markdown(node: Tag | NavigableString, depth: int = 0) -> str:
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        return clean_text(str(node))
    if not isinstance(node, Tag) or should_skip(node):
        return ""

    name = node.name.lower()
    classes = set(node.get("class") or [])

    if "resource-card" in classes:
        href = node.get("href", "").strip()
        nested_link = node.find("a", href=True)
        if not href and isinstance(nested_link, Tag):
            href = nested_link.get("href", "").strip()
        title_node = node.find(class_="res-title") or node.find("span") or node.find(["h3", "h4"])
        desc_node = node.find(class_="res-desc") or node.find("p")
        title = clean_text(title_node.get_text(" ", strip=True)) if isinstance(title_node, Tag) else clean_text(node.get_text(" ", strip=True))
        desc = clean_text(desc_node.get_text(" ", strip=True)) if isinstance(desc_node, Tag) else ""
        if href and title:
            suffix = f" — {desc}" if desc and desc != title else ""
            return f"- [{title}]({href}){suffix}"
        if title:
            suffix = f" — {desc}" if desc and desc != title else ""
            return f"- {title}{suffix}"

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = min(int(name[1]), 6)
        text = clean_text(node.get_text(" ", strip=True))
        return f"{'#' * level} {text}" if text else ""

    if name == "p":
        text = inline_markdown(node)
        return text

    if name == "pre" or name == "code" and "language-mermaid" in classes:
        lang = fence_lang_from_block(node)
        text = code_text(node)
        if not text:
            return ""
        fence = "````" if "```" in text else "```"
        return f"{fence}{lang}\n{text}\n{fence}"

    if "mermaid" in classes:
        text = node.get_text("\n", strip=True)
        if text:
            return f"```mermaid\n{text}\n```"

    if name == "table":
        return table_to_markdown(node)

    if name in {"ul", "ol"}:
        ordered = name == "ol"
        items = []
        for index, li in enumerate(node.find_all("li", recursive=False), 1):
            marker = f"{index}." if ordered else "-"
            text = clean_text(" ".join(block_markdown(child, depth + 1) for child in children_blocks(li)))
            if text:
                items.append(f"{marker} {text}")
        return "\n".join(items)

    if name == "li":
        text = clean_text(" ".join(block_markdown(child, depth + 1) for child in children_blocks(node)))
        return f"- {text}" if text else ""

    if name == "blockquote":
        text = "\n".join(block_markdown(child, depth + 1) for child in children_blocks(node))
        text = collapse_blank_lines(text).strip()
        return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())

    if name == "hr":
        return "---"

    if name == "svg":
        label = node.get("aria-label") or node.find("text")
        label_text = clean_text(label.get_text(" ", strip=True)) if isinstance(label, Tag) else clean_text(str(label or "SVG diagram"))
        return f"> Diagram omitted from Markdown export: {label_text}"

    if name == "canvas":
        label = node.get("aria-label") or node.get("id") or "interactive canvas"
        return f"> Canvas omitted from Markdown export: {clean_text(str(label))}"

    child_output = []
    for child in children_blocks(node):
        item = block_markdown(child, depth + 1)
        if item:
            child_output.append(item)
    return "\n\n".join(child_output)


def day_title(day: Tag) -> str:
    tag = day.find(class_="day-tag")
    h1 = day.find("h1")
    bits = []
    if tag:
        bits.append(clean_text(tag.get_text(" ", strip=True)))
    if h1:
        bits.append(clean_text(h1.get_text(" ", strip=True)))
    if bits:
        return " - ".join(bits)
    return day.get("id", "Day")


def extract_week(path: Path) -> tuple[str, dict]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else path.stem
    week_number = int(re.search(r"\d+", path.stem).group())
    day_sections = soup.select("main .day-section")

    meta = {
        "week": week_number,
        "title": title,
        "source_html": str(path.relative_to(ROOT)),
        "days": [section.get("id", "") for section in day_sections],
    }

    out = [
        "---",
        f"week: {week_number}",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f"source_html: {path.relative_to(ROOT)}",
        "---",
        "",
        f"# {title}",
        "",
        "> Generated from HTML. Edit this Markdown copy first, then use it as the source for a future HTML renderer.",
    ]

    if not day_sections:
        main = soup.find("main") or soup.body or soup
        content = block_markdown(main)
        if content:
            out.append(content)
    else:
        for section in day_sections:
            out.extend(["", f"## {day_title(section)}", ""])
            content_parts = []
            for child in children_blocks(section):
                if isinstance(child, Tag) and "day-header" in (child.get("class") or []):
                    for header_child in children_blocks(child):
                        if isinstance(header_child, Tag) and header_child.name == "h1":
                            continue
                        if isinstance(header_child, Tag) and header_child.name in {"p", "div"}:
                            item = block_markdown(header_child)
                            if item:
                                content_parts.append(item)
                    continue
                item = block_markdown(child)
                if item:
                    content_parts.append(item)
            out.append("\n\n".join(content_parts))

    return collapse_blank_lines("\n".join(out)), meta


def validate_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if text.count("```") % 2:
        errors.append("unbalanced triple-backtick fences")
    if text.count("````") % 2:
        errors.append("unbalanced quadruple-backtick fences")
    if "<div" in text or "</div>" in text:
        errors.append("raw div tag leaked into markdown")
    if "<script" in text or "</script>" in text:
        errors.append("raw script tag leaked into markdown")
    return errors


def write_readme(manifest: list[dict]) -> None:
    readme = [
        "# Markdown Notes Export",
        "",
        "This folder is a separate Markdown copy of the course notes generated from `pages/weeks/*.html`.",
        "",
        "The existing HTML site was not changed. Use these files as the safer authoring format while a Markdown-to-HTML renderer is built.",
        "",
        "## Files",
        "",
        "- `weeks/week01.md` through `weeks/week26.md`: editable week notes",
        "- `manifest.json`: source mapping and exported day ids",
        "",
        "## Conversion Notes",
        "",
        "- Navigation, sidebar, completion buttons, and runtime JavaScript are stripped.",
        "- Code blocks, tables, links, quizzes, tasks, resources, and text content are preserved as Markdown where possible.",
        "- SVG and canvas visuals are represented by short placeholder notes so the Markdown stays readable.",
        "- Some malformed HTML may still produce awkward text. Fix the Markdown source directly, then generate future HTML from Markdown.",
    ]
    readme.append("")
    readme.append("## Exported Weeks")
    readme.append("")
    for item in manifest:
        readme.append(f"- Week {item['week']:02d}: `weeks/week{item['week']:02d}.md` ({len(item['days'])} day sections)")
    OUT_DIR.joinpath("README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")


def main() -> int:
    WEEKS_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    errors: list[str] = []

    html_files = sorted(HTML_DIR.glob("week*.html"), key=lambda p: int(re.search(r"\d+", p.stem).group()))
    for html_file in html_files:
        markdown, meta = extract_week(html_file)
        out_path = WEEKS_DIR / f"week{meta['week']:02d}.md"
        out_path.write_text(markdown, encoding="utf-8")
        manifest.append(meta)

    OUT_DIR.joinpath("manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_readme(manifest)

    for md_file in sorted(WEEKS_DIR.glob("week*.md")):
        for error in validate_markdown(md_file):
            errors.append(f"{md_file.relative_to(ROOT)}: {error}")

    if len(manifest) != 26:
        errors.append(f"expected 26 week files, exported {len(manifest)}")

    if errors:
        print("MARKDOWN EXPORT COMPLETED WITH ISSUES")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"MARKDOWN EXPORT PASSED: wrote {len(manifest)} weeks to {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
