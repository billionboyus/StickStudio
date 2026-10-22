"""StickStudio Core Engine.

Manages:
- Topic slugification
- Output directory isolation (output/<title-slug>/)
- Script file saving & loading (output/<title-slug>/script.md)
- Prompt validation and status inspection
"""
import json
import os
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

from stickstudio.linter import lint_script_file, parse_script_content


def slugify(title: str) -> str:
    """Convert an arbitrary title into a clean, lowercase hyphenated slug."""
    text = title.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "stickman-video"


def get_project_dir(slug_or_path: str, base_dir: Optional[Path] = None) -> Path:
    """Resolve the topic project directory strictly under output/<slug>."""
    if base_dir is None:
        base_dir = Path.cwd()

    candidate = Path(slug_or_path)
    if candidate.is_dir() and "output" in candidate.parts:
        return candidate.resolve()

    slug = slugify(str(slug_or_path))
    target = base_dir / "output" / slug
    return target.resolve()


def init_project(
    topic: str,
    aspect_ratio: str = "16:9",
    visual_style: str = "Style 1 (Classic Minimalist)",
    duration: int = 60,
    base_dir: Optional[Path] = None,
) -> Path:
    """Initialize a dedicated topic folder under output/<slug>/ for the prompt."""
    slug = slugify(topic)
    proj_dir = get_project_dir(slug, base_dir=base_dir)
    proj_dir.mkdir(parents=True, exist_ok=True)
    return proj_dir


def save_script(
    slug_or_dir: str,
    prompts: Dict[int, str],
    base_dir: Optional[Path] = None,
    overwrite: bool = True,
) -> Path:
    """Save clip prompts strictly to output/<title-slug>/script.md.

    The file contains ONLY standalone prompt blocks separated by '---'.
    No Phase A tables, stitching guides, or commentary are included.
    """
    proj_dir = get_project_dir(slug_or_dir, base_dir=base_dir)
    proj_dir.mkdir(parents=True, exist_ok=True)

    script_path = proj_dir / "script.md"
    if script_path.exists() and not overwrite:
        raise FileExistsError(f"Script already exists at {script_path}. Use overwrite=True to replace.")

    total_clips = len(prompts)
    blocks = []
    for idx in sorted(prompts.keys()):
        start_sec = (idx - 1) * 10
        end_sec = idx * 10
        start_min, start_s = divmod(start_sec, 60)
        end_min, end_s = divmod(end_sec, 60)
        timecode = f"{start_min:02d}:{start_s:02d}–{end_min:02d}:{end_s:02d}"

        prompt_body = prompts[idx].strip()
        block = f"### Clip {idx} of {total_clips} ({timecode})\n\n```text\n{prompt_body}\n```"
        blocks.append(block)

    full_script = "\n\n---\n\n".join(blocks) + "\n"
    script_path.write_text(full_script, encoding="utf-8")
    return script_path


def load_script(slug_or_path: str, base_dir: Optional[Path] = None) -> Tuple[Dict[int, str], int]:
    """Load and parse prompts from output/<title-slug>/script.md."""
    path = Path(slug_or_path)
    if not path.is_file():
        proj_dir = get_project_dir(slug_or_path, base_dir=base_dir)
        path = proj_dir / "script.md"

    if not path.exists():
        raise FileNotFoundError(f"Script file not found: {path}")

    content = path.read_text(encoding="utf-8")
    return parse_script_content(content)


def get_project_status(slug_or_dir: str, base_dir: Optional[Path] = None) -> Dict:
    """Inspect and report prompt status of a topic in output/<title-slug>/."""
    proj_dir = get_project_dir(slug_or_dir, base_dir=base_dir)
    if not proj_dir.exists():
        return {"exists": False, "dir": str(proj_dir)}

    script_path = proj_dir / "script.md"
    script_exists = script_path.exists()
    total_clips = 0
    lint_errors = []
    clips = {}

    if script_exists:
        lint_errors = lint_script_file(script_path)
        try:
            clips, total_clips = parse_script_content(script_path.read_text(encoding="utf-8"))
        except Exception as e:
            lint_errors.append(f"Parse error: {e}")

    return {
        "exists": True,
        "dir": str(proj_dir),
        "script_exists": script_exists,
        "script_path": str(script_path) if script_exists else None,
        "total_clips": total_clips,
        "parsed_clips": len(clips),
        "lint_errors": lint_errors,
        "valid": len(lint_errors) == 0 if script_exists else False,
    }
