#!/usr/bin/env python3
"""
scripts/fix_week2_pre_tag.py
"""

with open('pages/weeks/week2.html', 'r', encoding='utf-8') as f:
    t = f.read()

t = t.replace(
'''<pre>def validate_checkpoint_day14():
    """Day 14 SQL Window Functions Checkpoint."""
    sample_df = {"employee": "Alice", "department": "Engineering", "salary": 120000}
    print(f"Checkpoint Day 14 Verified: {sample_df['employee']} | Salary: ${sample_df['salary']:,}")

validate_checkpoint_day14()
                </div>''',
'''<pre>def validate_checkpoint_day14():
    """Day 14 SQL Window Functions Checkpoint."""
    sample_df = {"employee": "Alice", "department": "Engineering", "salary": 120000}
    print(f"Checkpoint Day 14 Verified: {sample_df['employee']} | Salary: ${sample_df['salary']:,}")

validate_checkpoint_day14()</pre>
                </div>'''
)

with open('pages/weeks/week2.html', 'w', encoding='utf-8') as f:
    f.write(t)

print("Fixed unclosed <pre> in week2.html")
