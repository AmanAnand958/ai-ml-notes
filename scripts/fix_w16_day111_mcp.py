#!/usr/bin/env python3
"""
scripts/fix_w16_day111_mcp.py
Provides distinct, accurate MCP Server implementations for W16 D111 Tasks 2 & 3.
"""

import os, yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

def save_yaml(path, data):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

W16_FILE = os.path.join(DATA_DIR, "week16.yaml")
data = load_yaml(W16_FILE)
day111 = next(d for d in data.get('days', []) if d.get('id') == 111)

# Task 2: Study Notes MCP Server
day111['tasks'][1]['solution_code'] = """# Day 111 Task 2: Build a Study Notes MCP Server
from typing import Dict, List, Any

class StudyNotesMCPServer:
    \"\"\"Model Context Protocol (MCP) Server exposing tools for study notes.\"\"\"

    def __init__(self):
        self.notes: Dict[str, str] = {}

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {"name": "save_note", "description": "Save a study note by title", "parameters": {"title": "str", "content": "str"}},
            {"name": "get_note", "description": "Retrieve a study note by title", "parameters": {"title": "str"}},
            {"name": "search_notes", "description": "Search notes by keyword", "parameters": {"keyword": "str"}}
        ]

    def call_tool(self, name: str, arguments: dict) -> dict:
        if name == "save_note":
            title, content = arguments["title"], arguments["content"]
            self.notes[title] = content
            return {"content": [{"type": "text", "text": f"Note '{title}' saved successfully."}]}
        elif name == "get_note":
            title = arguments["title"]
            if title in self.notes:
                return {"content": [{"type": "text", "text": self.notes[title]}]}
            return {"isError": True, "content": [{"type": "text", "text": f"Note '{title}' not found."}]}
        elif name == "search_notes":
            kw = arguments["keyword"].lower()
            matches = [t for t, c in self.notes.items() if kw in t.lower() or kw in c.lower()]
            return {"content": [{"type": "text", "text": f"Matches: {', '.join(matches)}"}]}
        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

server = StudyNotesMCPServer()
tools = server.list_tools()
server.call_tool("save_note", {"title": "FlashAttention", "content": "IO-aware tiled attention kernel in SRAM."})
res = server.call_tool("get_note", {"title": "FlashAttention"})
print("MCP Server Response:", res["content"][0]["text"])
assert "IO-aware" in res["content"][0]["text"]
print("✓ Study Notes MCP Server verified.")"""

# Task 3: MCP Server with Prompt Templates + Auth
day111['tasks'][2]['solution_code'] = """# Day 111 Task 3: MCP Server with Prompt Templates + Token Auth
from typing import Dict, List, Any

class AuthenticatedMCPServer:
    \"\"\"MCP Server with bearer token validation and prompt templates.\"\"\"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.prompt_templates: Dict[str, str] = {
            "summarize_code": "Explain the algorithmic complexity and edge cases of this code:\\n{code}",
            "explain_architecture": "Describe the data flow and bottlenecks for system architecture: {system}"
        }

    def authenticate(self, token: str) -> bool:
        return token == self.api_token

    def list_prompts(self, token: str) -> List[Dict[str, str]]:
        if not self.authenticate(token):
            raise PermissionError("Invalid MCP Auth Token")
        return [{"name": k, "template": v} for k, v in self.prompt_templates.items()]

    def get_prompt(self, token: str, name: str, arguments: dict) -> str:
        if not self.authenticate(token):
            raise PermissionError("Invalid MCP Auth Token")
        if name not in self.prompt_templates:
            raise KeyError(f"Prompt template '{name}' not found")
        return self.prompt_templates[name].format(**arguments)

mcp = AuthenticatedMCPServer(api_token="mcp-secret-key-123")
rendered = mcp.get_prompt(token="mcp-secret-key-123", name="summarize_code", arguments={"code": "def solve(): pass"})
print("Rendered MCP Prompt Template:", rendered)
assert "algorithmic complexity" in rendered
print("✓ Authenticated MCP Server with Prompt Templates verified.")"""

save_yaml(W16_FILE, data)
print("✓ Patched W16 D111 Tasks 2 & 3 successfully!")
