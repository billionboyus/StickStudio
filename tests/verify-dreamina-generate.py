#!/usr/bin/env python3
"""Offline checks for the Dreamina helper and the topic-folder rules (no CLI calls, no credits)."""
import importlib.util
import os
import subprocess
import sys
import tempfile

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
skill = os.path.join(root, "skills", "directing-stickman-videos")
helper = os.path.join(skill, "scripts", "dreamina_generate.py")

spec = importlib.util.spec_from_file_location("dreamina_generate", helper)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "script.md")
    body = "\n\n---\n\n".join(
        "### Clip %d of 3 (00:%02d–00:%02d)\n\n```text\nPrompt %d\n```" % (i, (i - 1) * 10, i * 10, i)
        for i in (1, 2, 3))
    open(path, "w", encoding="utf-8").write(body + "\n")
    clips = mod.parse_script(path)
    assert sorted(clips) == [1, 2, 3] and clips[2] == "Prompt 2", clips
    assert mod.parse_selection("all", 3) == [1, 2, 3]
    assert mod.parse_selection("1,3", 3) == [1, 3]
    assert mod.parse_selection("2-3", 3) == [2, 3]
    try:
        mod.parse_selection("4", 3)
    except SystemExit:
        pass
    else:
        raise AssertionError("out-of-range clip should exit")
    broken = os.path.join(tmp, "broken.md")
    open(broken, "w", encoding="utf-8").write(body.replace("of 3", "of 4") + "\n")
    try:
        mod.parse_script(broken)
    except SystemExit:
        pass
    else:
        raise AssertionError("clip-count mismatch should exit")

assert mod.find_key({"a": [{"b": {"nodeId": "n1"}}]}, "nodeId") == "n1"

# Prompt lint: Style 7 prompts must carry the enforced stick-body rule, negatives and five beats.
good = "\n".join(["Output specification: x", "Visual style: Style 7 Caricature Chronicle. thin black stick body", "Setting: A flat painted hall.", "Timed visual beats:",
                  "- [0-2s]: a", "- [2-4s]: b", "- [4-6s]: c", "- [6-8s]: d", "- [8-10s]: e", "Ending state [10s]: x",
                  "Spoken voiceover:", "Voice continuity lock:", "Music and sound effects:",
                  "Negative constraints: NO VISIBLE TEXT, NO FULL-BODIED SHADED CHARACTERS"])
assert mod.lint_prompt(1, good) == [], mod.lint_prompt(1, good)
assert mod.lint_prompt(1, good.replace("thin black stick body", "soft body"))
assert mod.lint_prompt(1, good.replace("NO FULL-BODIED SHADED CHARACTERS", "NO CGI"))
assert mod.lint_prompt(1, good.replace("- [8-10s]: e\n", ""))
assert mod.lint_prompt(1, good + " color #FF0000")
assert mod.lint_prompt(1, "x" * 3700)
# Style 7 must stay flat painted: lighting words and a missing flat Setting are rejected.
flat = good
assert mod.lint_prompt(1, flat) == [], mod.lint_prompt(1, flat)
assert any("flat" in x for x in mod.lint_prompt(1, good.replace("Setting: A flat painted hall.", "Setting: A hall.")))
for word in ("dim", "moonlit", "candlelight", "cinematic", "shadows", "volumetric"):
    assert any("realistic" in x for x in mod.lint_prompt(1, flat.replace("Setting: A flat painted hall.", "Setting: A flat painted " + word + " hall."))), word
# Negatives may mention the banned words: they are excluded from the wording check.
assert mod.lint_prompt(1, flat + " NO REALISTIC LIGHTING ON CHARACTERS") == []
# Batches of more than two clips need an accepted test clip.
assert mod.needs_style_approval(3, {}, False)
assert not mod.needs_style_approval(2, {}, False)
assert not mod.needs_style_approval(30, {"styleApproved": True}, False)
assert not mod.needs_style_approval(30, {}, True)
# The saved Shaolin script, if present, must pass the lint.
shaolin = os.path.join(root, "output", "what-did-shaolin-monks-actually-do-all-day", "script.md")
if os.path.exists(shaolin):
    for n, text in mod.parse_script(shaolin).items():
        assert mod.lint_prompt(n, text) == [], (n, mod.lint_prompt(n, text))

# Running without --yes must never spend credits: it exits before touching the CLI.
with tempfile.TemporaryDirectory() as tmp:
    open(os.path.join(tmp, "script.md"), "w", encoding="utf-8").write(body + "\n")
    env = dict(os.environ, DREAMINA_CLI=sys.executable)  # stand-in; auth call fails before any spend
    proc = subprocess.run([sys.executable, helper, tmp, "--mode", "run"], capture_output=True, text=True, env=env)
    assert proc.returncode != 0

# Skill rules every agent must see.
skill_md = open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read()
for needle in ("output/<title-slug>/script.md", "1.mp4", "Seedance 2.0 mini", "explicit yes", "FULL-BODIED SHADED CHARACTERS", "stick-body sentence",
               "references/dreamina-generation.md"):
    assert needle in skill_md, "SKILL.md missing: " + needle
doc = open(os.path.join(skill, "references", "dreamina-generation.md"), encoding="utf-8").read()
for needle in ("seedance_2.0_mini", "--duration 10", "N.mp4", "Ask first"):
    assert needle in doc, "dreamina-generation.md missing: " + needle
print("Dreamina helper and topic-folder rules passed; no credits used.")
