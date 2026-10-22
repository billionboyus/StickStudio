"""StickStudio Script Linter & Validator.

Enforces:
1. Strict output directory protocol: output/<slug>/script.md
2. Prompt character limits (< 3600 characters)
3. Script structure: exactly N prompt blocks in ```text``` fences, no loose Phase A commentary
4. Required sections: Output specification, Timed visual beats, Spoken voiceover,
   Voice continuity lock, Music and sound effects, Negative constraints
5. Style-specific rules (e.g. Style 7 flat painted rules, no volumetric/realistic lighting words, 5 beats)
"""
from pathlib import Path
import re
from typing import Dict, List, Tuple

PROMPT_LIMIT = 3600
REQUIRED_SECTIONS = (
    "Output specification:",
    "Timed visual beats:",
    "Spoken voiceover:",
    "Voice continuity lock:",
    "Music and sound effects:",
    "Negative constraints:",
)

STYLE_RULES = {
    "Style 7": ("thin black stick body", "FULL-BODIED SHADED CHARACTERS", "NO VISIBLE TEXT"),
}

STYLE_BEATS = {"Style 7": 5}

STYLE_FORBIDDEN_WORDS = {
    "Style 7": r"\b(dim|dimly|moonlit|candlelight|candlelit|volumetric|cinematic|photoreal\w*|realistic|spotlight|"
               r"lens flare|bokeh|depth of field|shadows?|glow\w*|sunbeams?|light rays?)\b",
}


def parse_script_content(content: str) -> Tuple[Dict[int, str], int]:
    """Parse script content into clip index -> prompt mapping and total clips count."""
    pat = re.compile(r"### Clip (\d+) of (\d+)[^\n]*\n+```text\n(.*?)\n```", re.S)
    clips = {}
    total = None
    for m in pat.finditer(content):
        clip_num = int(m.group(1))
        total_clips = int(m.group(2))
        clips[clip_num] = m.group(3).strip()
        if total is None:
            total = total_clips
        elif total != total_clips:
            raise ValueError(f"Inconsistent clip total: saw {total} then {total_clips}")
    return clips, total or len(clips)


def lint_prompt(clip_idx: int, text: str) -> List[str]:
    """Lint an individual clip prompt against contract rules."""
    errs = []
    if len(text) > PROMPT_LIMIT:
        errs.append(f"Prompt is {len(text)} characters; limit is {PROMPT_LIMIT}.")

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            errs.append(f"Missing required section: {sec}")

    # Check for technical hex color notation
    if re.search(r"#[0-9a-fA-F]{6}\b", text):
        errs.append("Contains hex color code; use natural color descriptors instead.")

    # Style-specific checks
    for style, rules in STYLE_RULES.items():
        if style in text:
            for phrase in rules:
                if phrase not in text:
                    errs.append(f"{style} prompt missing required phrase: {phrase}")

    for style, beats in STYLE_BEATS.items():
        if style in text:
            found_beats = len(re.findall(r"- \[\d+[\-–—]\d+s\]:", text))
            if found_beats != beats:
                errs.append(f"{style} requires {beats} timed beats, found {found_beats}.")

    for style, pat in STYLE_FORBIDDEN_WORDS.items():
        if style in text:
            # Exclude negative constraints section from forbidden word match
            body = text.split("Negative constraints:")[0] if "Negative constraints:" in text else text
            m = re.search(pat, body, re.IGNORECASE)
            if m:
                errs.append(f"{style} prompt contains forbidden lighting/realism word '{m.group(0)}'. Must stay flat painted.")
            if "Setting:" in text and "flat" not in text.split("Setting:")[1].splitlines()[0].lower():
                errs.append(f"{style} Setting line must explicitly specify 'flat painted'.")

    return errs


def lint_script_file(script_path: Path) -> List[str]:
    """Validate a script file against the Output Directory Protocol and prompt contract."""
    errors = []
    path = Path(script_path).resolve()

    # Enforce Output Directory Protocol: output/<title-slug>/script.md
    parts = path.parts
    if "output" not in parts:
        errors.append(f"Output directory violation: script must reside inside 'output/<title-slug>/script.md', got: {path}")
    else:
        out_idx = parts.index("output")
        if len(parts) < out_idx + 2 or parts[-1] != "script.md":
            errors.append(f"Script naming violation: expected path ending in 'output/<title-slug>/script.md', got: {path}")

    if not path.exists():
        errors.append(f"Script file does not exist: {path}")
        return errors

    content = path.read_text(encoding="utf-8")

    # Check for forbidden commentary/tables in script.md
    if "| Narrative purpose |" in content or "Phase A" in content or "Storyboard" in content:
        errors.append("Script contains Phase A or storyboard commentary. script.md must contain ONLY standalone prompt blocks.")

    try:
        clips, total = parse_script_content(content)
    except Exception as e:
        errors.append(f"Failed to parse script blocks: {e}")
        return errors

    if not clips:
        errors.append("No valid clip prompt blocks found in script (format: ### Clip i of N ... ```text ... ```).")
        return errors

    if len(clips) != total:
        errors.append(f"Clip count mismatch: found {len(clips)} prompt blocks, but header specifies total of {total}.")

    expected_indices = list(range(1, total + 1))
    if sorted(clips.keys()) != expected_indices:
        errors.append(f"Missing or non-sequential clips: found {sorted(clips.keys())}, expected {expected_indices}.")

    for idx, prompt_text in clips.items():
        prompt_errors = lint_prompt(idx, prompt_text)
        for err in prompt_errors:
            errors.append(f"Clip {idx}: {err}")

    return errors
