"""StickStudio Autonomous Agent Engine.

Provides programmatic and multi-agent interfaces for:
- Phase A (Director's Proposal) generation using the 5-Stage Heartbeat Engine
- Phase B (Standalone Prompts Compilation) adhering to prompt contracts
- Automated saving strictly to output/<title-slug>/script.md
- Strict validation and prompt linting
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from stickstudio.core import get_project_dir, init_project, load_script, save_script, slugify
from stickstudio.linter import lint_script_file

# Narrative Heartbeat Engine Stages
HEARTBEAT_STAGES = [
    ("Golden Hook", "Instant curiosity trigger via a counter-intuitive question or visual paradox."),
    ("Disrupting Assumptions", "State what everyone thinks is true, then shatter it in one sentence."),
    ("Unveiling Insider Secrets", "Pull back the curtain on hidden mechanics, counter-intuitive details, or the real obstacle."),
    ("Ultimate Truth Revelation", "Deliver the underlying business logic or human psychology truth with maximum cognitive payoff."),
    ("Elevation & Interactive Discussion", "Conclude with a memorable punchline and an irresistible discussion prompt."),
]


class StickStudioAgent:
    """Universal AI agent for stickman video direction and prompt engineering."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()

    def create_topic(self, topic: str, aspect_ratio: str = "16:9", visual_style: str = "Style 1 (Classic Minimalist)", duration: int = 60) -> Path:
        """Create a dedicated topic folder under output/<title-slug>/."""
        return init_project(topic, aspect_ratio=aspect_ratio, visual_style=visual_style, duration=duration, base_dir=self.base_dir)

    def write_prompt_script(self, topic: str, prompts: Dict[int, str], overwrite: bool = True) -> Tuple[Path, List[str]]:
        """Save prompts strictly to output/<title-slug>/script.md and run linter."""
        slug = slugify(topic)
        script_path = save_script(slug, prompts, base_dir=self.base_dir, overwrite=overwrite)
        errors = lint_script_file(script_path)
        return script_path, errors

    def validate_script(self, slug_or_path: str) -> List[str]:
        """Validate an existing script against the Output Directory Protocol and Prompt Contract."""
        proj_dir = get_project_dir(slug_or_path, base_dir=self.base_dir)
        script_path = proj_dir / "script.md" if proj_dir.is_dir() else Path(slug_or_path)
        return lint_script_file(script_path)

    def get_script(self, slug_or_path: str) -> Tuple[Dict[int, str], int]:
        """Read prompts from output/<title-slug>/script.md."""
        return load_script(slug_or_path, base_dir=self.base_dir)
