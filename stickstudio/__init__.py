"""StickStudio: Universal AI Stickman Video Director & Prompt Engineer."""

from stickstudio.agent import StickStudioAgent
from stickstudio.core import get_project_dir, init_project, load_script, save_script, slugify
from stickstudio.linter import lint_prompt, lint_script_file

__version__ = "1.0.0"
__all__ = [
    "StickStudioAgent",
    "init_project",
    "save_script",
    "load_script",
    "slugify",
    "get_project_dir",
    "lint_script_file",
    "lint_prompt",
]
