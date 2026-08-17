#!/usr/bin/env python3
"""
Course Site Compiler
Compiles structured YAML data files + Jinja2 template into production week HTML pages.
"""

import os
import sys
import glob
import json
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'src/template')
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'pages/weeks')

def build_all_weeks(target_week=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template('week.template.html')

    pattern = os.path.join(DATA_DIR, f"week{int(target_week):02d}.yaml") if target_week else os.path.join(DATA_DIR, "week*.yaml")
    data_files = sorted(glob.glob(pattern), key=lambda p: int(''.join(filter(str.isdigit, os.path.basename(p)))))

    if not data_files:
        print(f"❌ No data files found in {DATA_DIR} matching pattern.")
        sys.exit(1)

    print(f"🏗️  Compiling {len(data_files)} week(s) into '{OUTPUT_DIR}'...\n")

    compiled_files = []
    for df in data_files:
        with open(df, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        wnum = data['week_number']
        
        # Compute DAYS list for client-side routing & storage
        days_list = []
        for d in data.get('days', []):
            raw_id = d.get('id')
            if str(raw_id).isdigit():
                days_list.append(int(raw_id))
            else:
                days_list.append(str(raw_id))

        if data.get('toolkit'):
            days_list.append('toolkit')

        days_json = json.dumps(days_list)

        rendered_html = template.render(
            week=data,
            days_json=days_json
        )

        out_fname = f"week{wnum}.html"
        out_path = os.path.join(OUTPUT_DIR, out_fname)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        compiled_files.append(out_path)
        print(f"  ✓ Compiled week{wnum}.html ({len(data.get('days', []))} days, {len(rendered_html.splitlines())} lines)")

    print(f"\n🎉 Successfully compiled {len(compiled_files)} week pages.")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else None
    build_all_weeks(target)
