#!/usr/bin/env python3
"""Content audit for markdown-notes Weeks 19-26 and generated markdown-site."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "markdown-notes" / "weeks"
SITE_DIR = ROOT / "markdown-site" / "weeks"

BLOCKED_PATTERNS = [
    "GPT-4V",
    "Senior AI Engineer",
    "Senior Full-Stack AI Engineer",
    "production-ready",
    "zero-downtime deployments trivial",
    "vllm/vllm-openai:latest",
    "tag: latest",
    'tag: "latest"',
    'password="password"',
    'api_key="API_KEY"',
    "Completed all 191 days",
    "guaranteed regional SLA availability",
    "data residency guarantees",
    "SLA uptime quotas guarantee",
    "Review the theory section above",
    "Excellent understanding of",
]


def split_day_blocks(text: str) -> list[str]:
    pattern = re.compile(r"(?m)^##\s+WEEK\s+\d+\s+·\s+(?:DAY\s+\d+|(?:MASTER\s+)?TOOLKIT)\b.*$")
    matches = list(pattern.finditer(text))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append(text[match.start() : end])
    return blocks


def audit_markdown() -> list[str]:
    errors: list[str] = []
    for week in range(19, 27):
        path = MD_DIR / f"week{week:02d}.md"
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        for pattern in BLOCKED_PATTERNS:
            if pattern in text:
                errors.append(f"{rel}: blocked phrase remains: {pattern}")

        for char_code in [7, 8, 12]:
            if chr(char_code) in text:
                errors.append(f"{rel}: control character U+{char_code:04X} remains")

        if re.search(r"\b(?:imes|ext\{|rac\{)\b", text):
            errors.append(f"{rel}: likely broken LaTeX token remains")

        if text.count("```") % 2:
            errors.append(f"{rel}: unbalanced fenced code blocks")

        if "Resource maintenance note:" not in text:
            errors.append(f"{rel}: missing resource maintenance note")

        blocks = split_day_blocks(text)
        if len(blocks) != 7:
            errors.append(f"{rel}: expected 7 day/toolkit blocks, found {len(blocks)}")

        for block_index, block in enumerate(blocks, 1):
            resource_match = re.search(r"(?s)^## 📚 Recommended Resources\s*\n(.*?)(?=\n### |\n## WEEK|\Z)", block, re.M)
            if not resource_match:
                errors.append(f"{rel}: day block {block_index} missing resources section")
                continue
            links = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", resource_match.group(1))
            if len(links) < 2:
                errors.append(f"{rel}: day block {block_index} has fewer than 2 restored resource links")

        for match in re.finditer(r"```python\n(.*?)\n```", text, re.S):
            try:
                ast.parse(match.group(1))
            except SyntaxError as exc:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: python code block syntax error: {exc.msg}")

    return errors


def audit_generated_site() -> list[str]:
    errors: list[str] = []
    for week in range(19, 27):
        path = SITE_DIR / f"week{week:02d}.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        rel = path.relative_to(ROOT)
        sections = soup.select(".day-section")
        pills = soup.select(".day-pill")
        if len(sections) != 7:
            errors.append(f"{rel}: expected 7 day sections, found {len(sections)}")
        if len(pills) != 7:
            errors.append(f"{rel}: expected 7 day pills, found {len(pills)}")
        ids: dict[str, int] = {}
        for element in soup.find_all(attrs={"id": True}):
            ids[element["id"]] = ids.get(element["id"], 0) + 1
        duplicates = [key for key, count in ids.items() if count > 1]
        if duplicates:
            errors.append(f"{rel}: duplicate ids remain: {duplicates[:8]}")
    return errors


def main() -> int:
    errors = audit_markdown() + audit_generated_site()
    if errors:
        print("EXTENSION MARKDOWN CONTENT AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EXTENSION MARKDOWN CONTENT AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
