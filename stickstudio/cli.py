"""StickStudio Command-Line Interface.

Usage:
    python -m stickstudio init "Why Rome's Enemies Feared Roman Legions"
    python -m stickstudio lint output/why-romes-enemies-feared-roman-legions/script.md
    python -m stickstudio status output/why-romes-enemies-feared-roman-legions
    python -m stickstudio mcp
"""
import argparse
import json
from pathlib import Path
import sys

from stickstudio.core import get_project_status, init_project, slugify
from stickstudio.linter import lint_script_file


def main():
    parser = argparse.ArgumentParser(
        prog="stickstudio",
        description="StickStudio: Universal AI Stickman Video Director & Prompt Engineer"
    )
    subparsers = parser.add_subparsers(dest="command", help="StickStudio commands")

    # Command: init
    init_cmd = subparsers.add_parser("init", help="Initialize a topic output folder under output/<title-slug>/")
    init_cmd.add_argument("topic", help="Topic title or concept")
    init_cmd.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"], help="Video aspect ratio")
    init_cmd.add_argument("--style", default="Style 1 (Classic Minimalist)", help="Visual style")
    init_cmd.add_argument("--duration", type=int, default=60, help="Target duration in seconds (multiple of 10)")

    # Command: lint
    lint_cmd = subparsers.add_parser("lint", help="Validate a script against the prompt contract and output folder rules")
    lint_cmd.add_argument("path", help="Path to script.md or topic directory")

    # Command: status
    status_cmd = subparsers.add_parser("status", help="Inspect status of a topic prompt in output/<title-slug>/")
    status_cmd.add_argument("topic_or_path", help="Topic slug or directory path")

    # Command: mcp
    subparsers.add_parser("mcp", help="Launch the StickStudio MCP (Model Context Protocol) server over stdio")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        proj_dir = init_project(
            topic=args.topic,
            aspect_ratio=args.aspect_ratio,
            visual_style=args.style,
            duration=args.duration
        )
        print(f"StickStudio: Topic folder initialized successfully at:\n  {proj_dir}")
        print(f"Save your standalone prompt blocks in:\n  {proj_dir / 'script.md'}")

    elif args.command == "lint":
        target = Path(args.path)
        if target.is_dir():
            target = target / "script.md"
        errors = lint_script_file(target)
        if errors:
            print(f"StickStudio Lint: Found {len(errors)} error(s) in {target}:")
            for err in errors:
                print(f"  [ERROR] {err}")
            sys.exit(1)
        else:
            print(f"StickStudio Lint: [PASSED] {target} is 100% compliant with prompt contract and folder rules.")

    elif args.command == "status":
        stat = get_project_status(args.topic_or_path)
        print(json.dumps(stat, indent=2))

    elif args.command == "mcp":
        from stickstudio.mcp_server import run_mcp_server
        run_mcp_server()


if __name__ == "__main__":
    main()
