#!/usr/bin/env python3
"""Apply the same high-signal content cleanup to original Week 19-26 HTML pages."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages" / "weeks"


REPLACEMENTS = {
    "GPT-4V": "GPT-4o vision input",
    "GPT-4o vision input API": "OpenAI vision input API",
    "GPT-4o vision input &amp; LLaVA": "GPT-4o vision-capable models &amp; LLaVA",
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
    'api_key="API_KEY"': 'api_key="&lt;set API key via environment&gt;"',
    'password="password"': 'password: str | None = None',
    "vllm/vllm-openai:latest": "vllm/vllm-openai:v0.6.3",
    'tag: "latest"': 'tag: "v1.2.3"',
    "ghcr.io/my-org/mlops-serving:latest": "ghcr.io/my-org/mlops-serving:v1.0.0",
}


def fix_latex(text: str) -> str:
    text = text.replace("\x07lpha", r"\alpha")
    text = text.replace("\x08", "")
    text = text.replace("\x0c", "\\")
    text = text.replace("\t", " ")
    text = re.sub(r"(?<=\d)\s+imes\b", r" \\times", text)
    text = re.sub(r"\bN\s+imes\s+N\b", r"N \\times N", text)
    text = re.sub(r"\b2\s+imes\s+2\b", r"2 \\times 2", text)
    text = re.sub(r"(?<!\\)\bext\{", r"\\text{", text)
    text = re.sub(r"(?<!\\)\brac\{", r"\\frac{", text)
    text = text.replace(r"\pi_{\ref}", r"\pi_{\text{ref}}")
    return text


def fix_feedback(text: str) -> str:
    text = re.sub(
        r"✅ Correct! Excellent understanding of ([^<]+?)\.",
        r"✅ Correct: this answer keeps the required evidence, controls, and operating constraints explicit for \1.",
        text,
    )
    text = text.replace(
        "❌ Not quite. Review the theory section above for key details.",
        "❌ Distractor feedback: compare each wrong option against the production requirement; the distractors skip baselines, remove evaluation, bypass security, or ship without rollout telemetry.",
    )
    return text


def main() -> int:
    for week in range(19, 27):
        path = PAGES / f"week{week}.html"
        text = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)
        text = re.sub(r"(<span class=\"kw\">tag</span>: )latest", r"\1v1.2.3", text)
        text = fix_latex(text)
        text = fix_feedback(text)
        path.write_text(text, encoding="utf-8")
    print("EXTENSION HTML CONTENT REMEDIATION COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
