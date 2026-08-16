#!/usr/bin/env python3
"""
Repair content-quality issues in markdown-notes/weeks/week19.md ... week26.md.

This script keeps the original pages/weeks HTML untouched. It treats
markdown-notes as the editable source for the separate generated markdown-site.
"""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "markdown-notes" / "weeks"
HTML_DIR = ROOT / "pages" / "weeks"


def clean(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def markdown_link_resources_from_html(week: int) -> list[list[str]]:
    """Return resource bullets per day section, using hrefs from original HTML."""
    html_path = HTML_DIR / f"week{week}.html"
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    sections = soup.select("main .day-section")
    output: list[list[str]] = []
    for section in sections:
        cards = section.select(".resource-card")
        bullets: list[str] = []
        for card in cards:
            if not isinstance(card, Tag):
                continue
            href = card.get("href", "").strip()
            nested = card.find("a", href=True)
            if not href and isinstance(nested, Tag):
                href = nested.get("href", "").strip()
            title_node = card.find(class_="res-title") or card.find("span") or card.find(["h3", "h4"])
            desc_node = card.find(class_="res-desc") or card.find("p")
            title = clean(title_node.get_text(" ", strip=True)) if isinstance(title_node, Tag) else clean(card.get_text(" ", strip=True))
            desc = clean(desc_node.get_text(" ", strip=True)) if isinstance(desc_node, Tag) else ""
            if href and title:
                suffix = f" — {desc}" if desc and desc != title else ""
                bullet = f"- [{title}]({href}){suffix}"
                if bullet not in bullets:
                    bullets.append(bullet)
        output.append(bullets)
    return output


def split_day_blocks(text: str) -> tuple[str, list[tuple[str, str]]]:
    pattern = re.compile(r"(?m)^##\s+(WEEK\s+\d+\s+·\s+(?:DAY\s+\d+|(?:MASTER\s+)?TOOLKIT)\b.*)$")
    matches = list(pattern.finditer(text))
    if not matches:
        return text, []
    intro = text[: matches[0].start()]
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.end() : end]))
    return intro, blocks


def restore_resource_links(text: str, week: int) -> str:
    intro, blocks = split_day_blocks(text)
    html_resources = markdown_link_resources_from_html(week)
    if not blocks:
        return text
    rebuilt = [intro.rstrip()]
    for index, (heading, body) in enumerate(blocks):
        resources = html_resources[index] if index < len(html_resources) else []
        if resources:
            resource_text = "\n".join(resources)
            body = re.sub(
                r"(## 📚 Recommended Resources\s*\n)(.*?)(?=\n### |\n## WEEK|\Z)",
                lambda match: f"{match.group(1)}\n{resource_text}\n",
                body,
                count=1,
                flags=re.S,
            )
        rebuilt.append(f"## {heading}{body.rstrip()}")
    return "\n\n".join(part for part in rebuilt if part).rstrip() + "\n"


def replace_claims(text: str) -> str:
    replacements = {
        "GPT-4V": "GPT-4o vision input",
        "GPT-4o vision input API": "OpenAI vision input API",
        "GPT-4o vision input & LLaVA": "GPT-4o vision-capable models & LLaVA",
        "API documentation for GPT-4o vision input": "OpenAI vision input documentation",
        "Gemini 1.5 Pro": "Vertex AI Gemini multimodal models (verify current model ID in official docs)",
        "guaranteeing 100% precision": "improving precision on identifier queries",
        "guarantees 100% precision": "improves precision on identifier queries",
        "SLA uptime quotas guarantee karta hai": "SLA aur quota behavior official docs mein verify karna padta hai",
        "data residency guarantees": "configurable regional data-residency controls subject to the selected service and region",
        "guaranteed regional SLA availability": "documented regional SLA terms that must be verified before deployment",
        "Embedding the same document repeatedly wastes API calls — caching returns the stored vector instantly for free": "Embedding the same document repeatedly wastes API calls; caching can reuse the stored vector, but storage and cache infrastructure still have cost.",
        "Event-driven ingestion keeps the vector DB always up-to-date.": "Event-driven ingestion reduces staleness, but retries, dead-letter queues, and monitoring are still required.",
        "Senior AI Engineer hona matlab hai": "observable production AI engineering competency ka evidence hai",
        "Senior Full-Stack AI Engineer": "Portfolio-ready full-stack AI engineer candidate",
        "K8s rolling updates + Helm make zero-downtime deployments trivial.": "K8s rolling updates and Helm support controlled rollouts, but zero-downtime requires readiness probes, capacity headroom, rollback tests, and traffic monitoring.",
        "is production-ready!": "has been practiced through implementation and review artifacts.",
        "production_readiness\": \"100% OPERATIONAL\"": "production_readiness\": \"READY_FOR_REVIEW\"",
        "Completed all 191 days": "Completed the 191-day portfolio path with reviewable evidence artifacts",
        "\"The journey never ends, but you now have the tools to build anything you can imagine. Go build the future!\"": "\"The journey continues; you now have a portfolio of systems, trade-off notes, and operating checklists to keep improving.\"",
        "You can run it locally for free": "You can run it locally without API charges, subject to hardware and electricity costs",
        "Use local Whisper models (base/small) for free, private transcription on CPU.": "Use local Whisper models (base/small) to avoid API charges and keep audio local, subject to CPU runtime and hardware limits.",
        "Azure account (free trial works)": "Azure account with budget alerts configured; verify current trial terms before running paid resources",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fix_latex_corruption(text: str) -> str:
    text = text.replace("\x07lpha", r"\alpha")
    text = text.replace("\x08", "")
    text = text.replace("\x0c", "\\")
    text = text.replace("\tines", r"\times")
    text = text.replace("\times", r"\times")
    text = text.replace("\text{", r"\text{")
    text = text.replace("\t", " ")
    text = re.sub(r"(?<=\d)\s+imes\b", r" \\times", text)
    text = re.sub(r"\bN\s+imes\s+N\b", r"N \\times N", text)
    text = re.sub(r"\b2\s+imes\s+2\b", r"2 \\times 2", text)
    text = re.sub(r"\b0\.5\s*imes\b", r"0.5\\times", text)
    text = re.sub(r"(?<!\\)\bext\{", r"\\text{", text)
    text = re.sub(r"(?<!\\)\brac\{", r"\\frac{", text)
    text = text.replace(r"\pi_{\ref}", r"\pi_{\text{ref}}")
    return text


def fix_infra_examples(text: str) -> str:
    text = text.replace('api_key="API_KEY"', 'api_key="<set PINECONE_API_KEY in environment>"')
    text = text.replace('api_key="API_KEY"', 'api_key="<set API key via environment>"')
    text = text.replace('password="password"', 'password: str | None = None')
    text = text.replace("vllm/vllm-openai:latest", "vllm/vllm-openai:v0.6.3")
    text = text.replace('tag: "latest"', 'tag: "v1.2.3"')
    text = re.sub(r"(?m)^  tag: latest$", "  tag: v1.2.3", text)
    text = text.replace("ghcr.io/my-org/mlops-serving:latest", "ghcr.io/my-org/mlops-serving:v1.0.0")
    text = text.replace("# In production: docker push ghcr.io/my-org/mlops-serving:latest", "# In production: docker push ghcr.io/my-org/mlops-serving:v1.0.0")
    return text


def feedback_reason(option: str) -> str:
    lower = option.lower()
    if "without a baseline" in lower or "larger system" in lower:
        return "skips baseline evidence, so quality and cost cannot be compared."
    if "remove evaluation" in lower:
        return "removes the signal needed to catch regressions."
    if "hard-code credentials" in lower or "bypass security" in lower:
        return "creates a security and portability failure."
    if "skip reproduction" in lower or "increase model size" in lower:
        return "changes the system before reproducing the failure."
    if "ship globally" in lower or "successful demo" in lower:
        return "has no staged rollout, telemetry, or rollback path."
    if "uncalibrated" in lower or "heuristic guesses" in lower:
        return "uses guesswork instead of measured acceptance criteria."
    if "no monitoring" in lower:
        return "confuses a demo with an operated system."
    if "memorized" in lower or "skipped" in lower:
        return "does not produce reviewable implementation evidence."
    return "does not satisfy the production requirement stated in the question."


def rewrite_quiz_feedback(text: str) -> str:
    pattern = re.compile(
        r"(QUESTION\s+\d+\s+OF\s+\d+\s*\n\n(?P<question>.*?)\n\nA\n\n(?P<a>.*?)\n\nB\n\n(?P<b>.*?)\n\nC\n\n(?P<c>.*?)(?:\n\nD\n\n(?P<d>.*?))?\n\n)"
        r"✅ Correct! Excellent understanding of (?P<topic>.*?)\.\s*\n\n"
        r"❌ Not quite\. Review the theory section above for key details\.",
        re.S,
    )

    def repl(match: re.Match[str]) -> str:
        topic = clean(match.group("topic"))
        a = clean(match.group("a"))
        b = clean(match.group("b"))
        c = clean(match.group("c"))
        d = clean(match.group("d") or "")
        distractors = [f"B: {feedback_reason(b)}", f"C: {feedback_reason(c)}"]
        if d:
            distractors.append(f"D: {feedback_reason(d)}")
        correct = f"✅ Correct: option A is the defensible {topic} choice because it keeps evidence, controls, and operating constraints explicit."
        wrong = "❌ Distractor feedback: " + " ".join(distractors)
        return f"{match.group(1)}{correct}\n\n{wrong}"

    return pattern.sub(repl, text)


def add_resource_maintenance_note(text: str) -> str:
    note = "> Resource maintenance note: verify model names, SDK methods, pricing, quotas, and service limits against official vendor documentation before running production or paid cloud exercises."
    if note in text:
        return text
    return text.replace("> Generated from HTML. Edit this Markdown copy first, then use it as the source for a future HTML renderer.", "> Generated from HTML. Edit this Markdown copy first, then use it as the source for a future HTML renderer.\n\n" + note)


def remediate_file(path: Path, week: int) -> None:
    text = path.read_text(encoding="utf-8")
    text = restore_resource_links(text, week)
    text = replace_claims(text)
    text = fix_latex_corruption(text)
    text = fix_infra_examples(text)
    text = rewrite_quiz_feedback(text)
    text = add_resource_maintenance_note(text)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for week in range(19, 27):
        remediate_file(MD_DIR / f"week{week:02d}.md", week)
    print("EXTENSION MARKDOWN CONTENT REMEDIATION COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
