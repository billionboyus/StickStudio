"""StickStudio Model Context Protocol (MCP) Server.

Enables any AI Agent (Claude Desktop, Claude Code, Gemini Antigravity, Hermes, Cursor)
to call StickStudio tools over JSON-RPC stdio.
"""
import json
from pathlib import Path
import sys
from typing import Any, Dict

from stickstudio.core import get_project_status, init_project, save_script, slugify
from stickstudio.linter import lint_script_file

MCP_TOOLS = [
    {
        "name": "stickstudio_init_topic",
        "description": "Initialize a dedicated topic folder under output/<title-slug>/ for stickman video prompts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The video topic or title."},
                "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16"], "default": "16:9"},
                "visual_style": {"type": "string", "default": "Style 1 (Classic Minimalist)"},
                "duration": {"type": "integer", "default": 60, "description": "Duration in seconds (multiple of 10)."}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "stickstudio_save_prompt_script",
        "description": "Save generated video prompt blocks strictly to output/<title-slug>/script.md.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic title or slug."},
                "prompts": {
                    "type": "object",
                    "description": "Dictionary mapping clip number (1 to N) to prompt text.",
                    "additionalProperties": {"type": "string"}
                }
            },
            "required": ["topic", "prompts"]
        }
    },
    {
        "name": "stickstudio_lint_script",
        "description": "Lint and validate a script against the prompt contract and output folder protocol.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to script.md or topic directory under output/."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "stickstudio_status",
        "description": "Check the status and validation of a topic's script in output/<title-slug>/.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic_or_path": {"type": "string", "description": "Topic title, slug, or path."}
            },
            "required": ["topic_or_path"]
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a StickStudio MCP tool call."""
    if name == "stickstudio_init_topic":
        proj_dir = init_project(
            topic=arguments["topic"],
            aspect_ratio=arguments.get("aspect_ratio", "16:9"),
            visual_style=arguments.get("visual_style", "Style 1 (Classic Minimalist)"),
            duration=arguments.get("duration", 60)
        )
        return {"content": [{"type": "text", "text": f"Topic folder initialized at: {proj_dir}"}]}

    elif name == "stickstudio_save_prompt_script":
        prompts_raw = arguments["prompts"]
        prompts = {int(k): str(v) for k, v in prompts_raw.items()}
        path = save_script(arguments["topic"], prompts)
        errs = lint_script_file(path)
        status_msg = f"Saved script to {path}."
        if errs:
            status_msg += f"\nValidation warnings/errors:\n" + "\n".join(f"- {e}" for e in errs)
        else:
            status_msg += "\nValidation passed: 100% compliant."
        return {"content": [{"type": "text", "text": status_msg}]}

    elif name == "stickstudio_lint_script":
        target = Path(arguments["path"])
        if target.is_dir():
            target = target / "script.md"
        errs = lint_script_file(target)
        if errs:
            return {"isError": True, "content": [{"type": "text", "text": f"Lint errors ({len(errs)}):\n" + "\n".join(f"- {e}" for e in errs)}]}
        return {"content": [{"type": "text", "text": f"Lint passed: {target} satisfies all prompt and folder rules."}]}

    elif name == "stickstudio_status":
        stat = get_project_status(arguments["topic_or_path"])
        return {"content": [{"type": "text", "text": json.dumps(stat, indent=2)}]}

    else:
        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}


def run_mcp_server():
    """Run MCP JSON-RPC server listening on stdin / responding on stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "stickstudio", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": MCP_TOOLS}
            }
        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})
            result = handle_tool_call(tool_name, args)
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            }
        else:
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {}
            }

        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()
