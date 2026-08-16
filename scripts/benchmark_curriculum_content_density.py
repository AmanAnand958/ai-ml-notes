#!/usr/bin/env python3
"""
Curriculum Content Density & Laggard Identification Engine:
Calculates a multi-dimensional content depth score for each of the 26 weeks:
- Theory & Concepts Prose Word Count
- Code Block Density & Lines of Code
- Interactive Quizzes Count
- Revision Flashcards Count
- Interactive Predict Blocks Count
- Hands-on Practice Tasks Count
- Architectural Diagrams Count

Identifies which specific weeks and days lag in pedagogical volume or interactive components.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

curriculum_stats = []

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. Total Days
    day_sections = soup.find_all('div', class_=lambda c: c and 'day-section' in c)
    total_days = len(day_sections)
    
    # 2. Extract Theory Prose (excluding code, quizzes, flashcards)
    theory_words = 0
    day_word_counts = {}
    for ds in day_sections:
        did = ds.get('id', 'unknown')
        # Clone and strip non-prose elements
        ds_copy = BeautifulSoup(str(ds), 'html.parser')
        for el in ds_copy.find_all(['pre', 'code', 'div'], class_=['cb', 'quiz-block', 'flashcard', 'predict-box']):
            el.decompose()
        words = len(ds_copy.text.split())
        theory_words += words
        day_word_counts[did] = words

    # 3. Interactive Components Count
    code_blocks = len(soup.find_all('div', class_='cb'))
    quizzes = len(soup.find_all('div', class_='quiz-block'))
    flashcards = len(soup.find_all('div', class_='flashcard'))
    predict_blocks = len(soup.find_all('div', class_=re.compile(r'predict-box|pred-box')))
    mermaids = len(soup.find_all('div', class_='mermaid'))
    tasks = len(soup.find_all('div', class_=re.compile(r'task-block|practice-task|solution-drawer')))

    # 4. Compute Content Density Score (Weighted)
    # Target per week: ~4,000 words, ~30 code blocks, ~25 quizzes, ~15 flashcards, ~5 diagrams
    word_score = min(100, (theory_words / 4000) * 100)
    code_score = min(100, (code_blocks / 25) * 100)
    quiz_score = min(100, (quizzes / 20) * 100)
    fc_score = min(100, (flashcards / 12) * 100)
    diag_score = min(100, (mermaids / 5) * 100)
    
    composite_score = round(
        0.35 * word_score +
        0.25 * code_score +
        0.15 * quiz_score +
        0.10 * fc_score +
        0.15 * diag_score,
        1
    )
    
    # Determine lag level
    if composite_score >= 85:
        tier = "🏆 GOLD STANDARD (High Depth)"
    elif composite_score >= 70:
        tier = "✅ SOLID (Comprehensive)"
    elif composite_score >= 55:
        tier = "⚠️ MODERATE (Needs Expansion)"
    else:
        tier = "🚨 LAGGARD (Low Content Density)"

    # Identify lowest word count day in this week
    sorted_days = sorted(day_word_counts.items(), key=lambda x: x[1])
    lowest_day, lowest_words = sorted_days[0] if sorted_days else ("N/A", 0)

    curriculum_stats.append({
        "week": wn,
        "days": total_days,
        "theory_words": theory_words,
        "avg_words_per_day": round(theory_words / max(1, total_days)),
        "code_blocks": code_blocks,
        "quizzes": quizzes,
        "flashcards": flashcards,
        "predict_blocks": predict_blocks,
        "diagrams": mermaids,
        "tasks": tasks,
        "score": composite_score,
        "tier": tier,
        "lowest_day": lowest_day,
        "lowest_day_words": lowest_words
    })

# Save JSON
out_file = ROOT_DIR / "scripts" / "curriculum_content_benchmark.json"
out_file.write_text(json.dumps(curriculum_stats, indent=2), encoding='utf-8')

# Print summary table
print(f"{'Wk':<4} | {'Days':<5} | {'Theory Words':<13} | {'Avg/Day':<8} | {'Code':<5} | {'Quiz':<5} | {'Cards':<6} | {'Diag':<5} | {'Score':<6} | {'Status'}")
print("-" * 95)
for s in curriculum_stats:
    print(f"{s['week']:<4} | {s['days']:<5} | {s['theory_words']:<13} | {s['avg_words_per_day']:<8} | {s['code_blocks']:<5} | {s['quizzes']:<5} | {s['flashcards']:<6} | {s['diagrams']:<5} | {s['score']:<6}% | {s['tier']}")
