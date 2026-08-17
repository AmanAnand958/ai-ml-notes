#!/usr/bin/env python3
"""
scripts/curriculum_utils.py
Common utilities for robust YAML loading, saving, and AST validation.
"""

import os, yaml

class LiteralStr(str): pass

def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(LiteralStr, lit_repr)

def load_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict):
        return {k: deep_literal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj:
        return LiteralStr(obj)
    return obj

def save_yaml(path: str, data: dict):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
