#!/usr/bin/env python3
"""
Render markdown-notes/ into a separate static HTML site.

This does not touch the existing hand-authored/generated HTML under pages/.
Output goes to:
  markdown-site/index.html
  markdown-site/weeks/week01.html ... week26.html
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import markdown
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
MD_ROOT = ROOT / "markdown-notes"
MD_WEEKS = MD_ROOT / "weeks"
OUT_ROOT = ROOT / "markdown-site"
OUT_WEEKS = OUT_ROOT / "weeks"
MANIFEST = MD_ROOT / "manifest.json"

COLORS = ["green", "blue", "orange", "pink", "purple", "yellow", "teal"]


def load_manifest() -> list[dict[str, Any]]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def read_markdown(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if text.startswith("---\n"):
        _, raw_meta, body = text.split("---", 2)
        for line in raw_meta.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
        return meta, body.strip()
    return meta, text.strip()


def slug_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "section"


def split_days(markdown_text: str) -> tuple[str, list[tuple[str, str]]]:
    matches = [
        match
        for match in re.finditer(r"(?m)^##\s+(.+)$", markdown_text)
        if re.match(r"^WEEK\s+\d+\s+·\s+(DAY\s+\d+|(?:MASTER\s+)?TOOLKIT)\b", match.group(1).strip(), re.I)
    ]
    if not matches:
        return markdown_text, []

    intro = markdown_text[: matches[0].start()].strip()
    days: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        title = match.group(1).strip()
        body = markdown_text[match.end() : end].strip()
        days.append((title, body))
    return intro, days


def day_number_from_id(day_id: str) -> str:
    if day_id.startswith("day-"):
        return day_id.removeprefix("day-")
    return day_id


def clean_day_label(title: str, day_id: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    if " - " in title:
        return title.split(" - ", 1)[1].strip()
    if title:
        return title
    return f"Day {day_number_from_id(day_id)}"


def markdown_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=[
            "extra",
            "fenced_code",
            "tables",
            "sane_lists",
        ],
        output_format="html5",
    )


def enhance_content(rendered: str) -> str:
    soup = BeautifulSoup(rendered, "html.parser")

    for table in soup.find_all("table"):
        table["class"] = "concept-table"

    for blockquote in soup.find_all("blockquote"):
        classes = blockquote.get("class") or []
        blockquote["class"] = [*classes, "callout"]

    for pre in soup.find_all("pre"):
        classes = pre.get("class") or []
        pre["class"] = [*classes, "md-code"]
        code = pre.find("code")
        lang = "text"
        if code:
            for cls in code.get("class") or []:
                if cls.startswith("language-"):
                    lang = cls.removeprefix("language-")
                    break
        wrapper = soup.new_tag("div")
        wrapper["class"] = "cb"
        head = soup.new_tag("div")
        head["class"] = "cb-head"
        label = soup.new_tag("span")
        label["class"] = "cb-lang"
        label.string = lang
        btns = soup.new_tag("div")
        btns["class"] = "cb-btns"
        copy = soup.new_tag("button")
        copy["class"] = "copy-btn"
        copy["onclick"] = "copyCode(this)"
        copy.string = "copy"
        btns.append(copy)
        head.append(label)
        head.append(btns)
        pre.wrap(wrapper)
        wrapper.insert(0, head)

    for h2 in soup.find_all("h2"):
        h2.attrs.pop("id", None)
        h2["class"] = "sh2"
    for h3 in soup.find_all("h3"):
        h3.attrs.pop("id", None)
        h3["class"] = "sh3"
    for h4 in soup.find_all("h4"):
        h4.attrs.pop("id", None)
        h4["class"] = "sh4"

    return str(soup)


def render_day(title: str, body: str, day_id: str, active: bool, xp: int = 150) -> str:
    label = clean_day_label(title, day_id)
    day_num = day_number_from_id(day_id)
    rendered = enhance_content(markdown_to_html(body))
    active_class = " active" if active else ""
    escaped_label = html.escape(label)
    escaped_title = html.escape(title)
    return f"""
<section class="day-section{active_class}" data-xp="{xp}" id="{html.escape(day_id)}">
  <div class="day-header">
    <div class="day-tag">{html.escape(title.split(" - ", 1)[0])}</div>
    <h1>{escaped_label}</h1>
  </div>
  <div id="{html.escape(day_id)}-theory" class="md-content">
{rendered}
  </div>
  <button class="complete-btn" id="btn-day-{html.escape(day_num)}" onclick="completeDay('{html.escape(day_num)}', {xp})">Mark {escaped_label} Complete</button>
</section>
"""


def render_week_page(item: dict[str, Any]) -> str:
    week = int(item["week"])
    md_path = MD_WEEKS / f"week{week:02d}.md"
    meta, body = read_markdown(md_path)
    title = meta.get("title") or item.get("title") or f"Week {week}"
    intro, days = split_days(body)
    day_ids = item.get("days", [])
    if len(day_ids) < len(days):
        day_ids = [f"day-{week}-{index + 1}" for index in range(len(days))]

    rendered_days = []
    sidebar_items = []
    pills = []
    js_days = []
    for index, (day_title, day_body) in enumerate(days):
        day_id = day_ids[index]
        day_num = day_number_from_id(day_id)
        js_value = f"'{day_num}'" if not day_num.isdigit() else day_num
        js_days.append(js_value)
        rendered_days.append(render_day(day_title, day_body, day_id, index == 0))

        label = clean_day_label(day_title, day_id)
        color = COLORS[index % len(COLORS)]
        active = " active" if index == 0 else ""
        sidebar_items.append(
            f'<div class="sb-item{active}" id="sb-{html.escape(day_num)}" '
            f'onclick="goDay({js_value});closeSidebar()" '
            f'onkeydown="if(event.key===\'Enter\')goDay({js_value})" role="button" tabindex="0">'
            f'<span class="sb-dot" style="background:var(--{color})"></span>'
            f'Day {html.escape(day_num)} — {html.escape(label)}</div>'
        )
        pills.append(
            f'<div aria-selected="{str(index == 0).lower()}" class="day-pill{active}" '
            f'id="pill-{html.escape(day_num)}" onclick="goDay({js_value})" '
            f'onkeydown="if(event.key===\'Enter\'||event.key===\' \')goDay({js_value})" '
            f'role="tab" tabindex="0">{html.escape(day_num)}</div>'
        )

    prev_link = f'<a class="week-nav-btn" href="week{week - 1:02d}.html">← Week {week - 1}</a>' if week > 1 else ""
    next_link = f'<a class="week-nav-btn" href="week{week + 1:02d}.html">Week {week + 1} →</a>' if week < 26 else ""
    intro_html = enhance_content(markdown_to_html(intro)) if intro else ""
    day_count = len(days)
    title_escaped = html.escape(title)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_escaped}</title>
  <meta name="description" content="{title_escaped}">
  <link rel="stylesheet" href="../../assets/css/course.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}], ignoredClasses:['quiz-feedback','quiz-opt','cm','no-katex']}});"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.2.0/dist/mermaid.min.js"></script>
  <script>if (typeof mermaid !== 'undefined') {{ mermaid.initialize({{startOnLoad:false,theme:'dark',securityLevel:'loose'}}); }}</script>
</head>
<body>
<div class="xp-toast" id="xp-toast">+150 XP</div>
<nav aria-label="Week navigation" class="topnav" role="navigation">
  <div class="topnav-left">
    <button aria-expanded="false" aria-label="Toggle navigation menu" class="mob-menu-btn" id="sidebar-toggle" onclick="toggleSidebar()">Menu</button>
    <div class="brand">{title_escaped}</div>
    <div class="xp-display" id="xp-show">0 XP</div>
    <div class="streak-display" id="streak-show">0 day streak</div>
    <div class="level-badge" id="level-show">Beginner</div>
  </div>
  <div style="display:flex;align-items:center;gap:.8rem">
    <div class="prog-wrap">
      <div aria-label="Week progress" aria-valuemax="100" aria-valuemin="0" aria-valuenow="0" class="prog-outer" role="progressbar"><div class="prog-inner" id="prog-bar"></div></div>
      <span id="prog-text">0/{day_count} days</span>
    </div>
    <div aria-label="Day selector" class="day-pills" role="tablist">
      {"".join(pills)}
    </div>
  </div>
  <button aria-label="Toggle dark/light mode" class="theme-btn" id="theme-btn" onclick="toggleTheme()">Light</button>
</nav>
<div class="layout">
  <aside aria-label="Sidebar navigation" class="sidebar" id="sidebar" role="complementary">
    <div class="sb-label">Week {week} — Days</div>
    {"".join(sidebar_items)}
    <div class="sb-divider"></div>
    <div class="sb-label">Progress</div>
    <div class="sb-item" id="sb-xp-info"><span class="sb-dot" style="background:var(--orange)"></span><span id="sb-xp">0 XP earned</span></div>
    <div class="sb-item" id="sb-streak-info"><span class="sb-dot" style="background:var(--pink)"></span><span id="sb-streak">0 day streak</span></div>
    <div class="sb-divider"></div>
    <div class="sb-label">Navigate</div>
    <div class="week-nav-links">
      <a class="week-nav-btn" href="../index.html">Markdown Site</a>
      <a class="week-nav-btn" href="../../roadmap.html">Original Roadmap</a>
      {prev_link}
      {next_link}
    </div>
  </aside>
  <main class="main">
    {f'<section class="callout md-intro">{intro_html}</section>' if intro_html else ''}
    {"".join(rendered_days)}
  </main>
</div>
<script>
  const WEEK = {week};
  const DAYS = [{",".join(js_days)}];
</script>
<script src="../../assets/js/course.js"></script>
</body>
</html>
"""


def render_index(manifest: list[dict[str, Any]]) -> str:
    cards = []
    for item in manifest:
        week = int(item["week"])
        title = html.escape(str(item["title"]))
        cards.append(
            f'<a class="resource-card" href="weeks/week{week:02d}.html">'
            f'<h3>Week {week:02d}</h3><p>{title}</p><span>{len(item.get("days", []))} day sections</span></a>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Markdown Course Site</title>
  <link rel="stylesheet" href="../assets/css/course.css">
</head>
<body>
  <main class="main" style="max-width:1100px;margin:0 auto;padding:2rem;">
    <div class="day-header">
      <div class="day-tag">Markdown Generated Site</div>
      <h1>191-Day AI/ML Roadmap</h1>
      <p>This site is generated from markdown-notes/ and is separate from the original HTML pages.</p>
    </div>
    <div class="res-grid">
      {"".join(cards)}
    </div>
  </main>
</body>
</html>
"""


def validate_html(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    soup = BeautifulSoup(text, "html.parser")
    if not soup.find("main"):
        errors.append("missing main")
    ids: dict[str, int] = {}
    for element in soup.find_all(attrs={"id": True}):
        ids[element["id"]] = ids.get(element["id"], 0) + 1
    duplicates = sorted(key for key, count in ids.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate ids: {', '.join(duplicates[:8])}")
    if text.count("<section") != text.count("</section>"):
        errors.append("section tag count mismatch")
    return errors


def main() -> int:
    manifest = load_manifest()
    OUT_WEEKS.mkdir(parents=True, exist_ok=True)

    for item in manifest:
        week = int(item["week"])
        out_path = OUT_WEEKS / f"week{week:02d}.html"
        out_path.write_text(render_week_page(item), encoding="utf-8")

    OUT_ROOT.joinpath("index.html").write_text(render_index(manifest), encoding="utf-8")

    errors: list[str] = []
    for html_file in sorted(OUT_WEEKS.glob("week*.html")) + [OUT_ROOT / "index.html"]:
        for error in validate_html(html_file):
            errors.append(f"{html_file.relative_to(ROOT)}: {error}")

    if errors:
        print("MARKDOWN SITE RENDERED WITH ISSUES")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"MARKDOWN SITE RENDER PASSED: wrote {len(manifest)} weeks to {OUT_ROOT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
