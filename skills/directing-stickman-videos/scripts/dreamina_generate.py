#!/usr/bin/env python3
"""Generate the clips of a saved script with the Dreamina CLI (dreamina-canvas).

Folder layout (one folder per topic):
    output/<topic-slug>/script.md   prompt blocks only (### Clip i of N ... ```text ... ```)
    output/<topic-slug>/1.mp4 2.mp4 ... N.mp4   generated clips, in order
    output/<topic-slug>/dreamina.json           resume state (canvas and node ids)

Modes (never spends credits unless --mode run AND --yes):
    --mode dry-run  validate every prompt locally with `node create video --dry-run`
    --mode quote    create the canvas and draft nodes, then ask the service for a credit estimate
    --mode run      quote, run, wait and download each clip (needs --yes)

Examples:
    python dreamina_generate.py output/my-topic --mode dry-run
    python dreamina_generate.py output/my-topic --mode quote --clips 1-3
    python dreamina_generate.py output/my-topic --mode run --clips 1 --yes
    python dreamina_generate.py output/my-topic --mode run --yes
    python dreamina_generate.py output/my-topic --mode run --clips 3 --force --yes   # regenerate clip 3
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import uuid

PROMPT_LIMIT = 3600
REQUIRED_SECTIONS = ("Output specification:", "Timed visual beats:", "Spoken voiceover:",
                     "Voice continuity lock:", "Music and sound effects:", "Negative constraints:")
STYLE_RULES = {
    # style marker -> phrases every prompt of that style must contain (the style's enforced anchor and negatives)
    "Style 7": ("thin black stick body", "FULL-BODIED SHADED CHARACTERS", "NO VISIBLE TEXT"),
}
STYLE_BEATS = {"Style 7": 5}
# Wording that makes video models render shaded, realistic scenes. Style 7 must stay flat painted.
STYLE_FORBIDDEN_WORDS = {
    "Style 7": r"\b(dim|dimly|moonlit|candlelight|candlelit|volumetric|cinematic|photoreal\w*|realistic|spotlight|"
               r"lens flare|bokeh|depth of field|shadows?|glow\w*|sunbeams?|light rays?)\b",
}
BATCH_LIMIT_WITHOUT_STYLE_OK = 2  # more clips than this need an accepted test clip first


def find_cli():
    env = os.environ.get("DREAMINA_CLI")
    if env and os.path.exists(env):
        return env
    for name in ("dreamina-canvas", "dreamina-canvas.exe", "dreamina"):
        found = shutil.which(name)
        if found:
            return found
    home = os.path.expanduser("~")
    for p in (os.path.join(home, "bin", "dreamina-canvas.exe"),
              os.path.join(home, "bin", "dreamina-canvas"),
              os.path.join(home, ".local", "bin", "dreamina-canvas")):
        if os.path.exists(p):
            return p
    sys.exit("Dreamina CLI not found. Put dreamina-canvas on PATH or set DREAMINA_CLI to its full path.")


def run_cli(cli, args, timeout=900, check=True):
    cmd = [cli] + args + ["--format", "json", "--non-interactive"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    out = (proc.stdout or "").strip()
    try:
        data = json.loads(out) if out else {}
    except json.JSONDecodeError:
        data = {"ok": False, "raw": out, "stderr": (proc.stderr or "").strip()}
    if check and not data.get("ok", False):
        sys.exit("Dreamina CLI error for `%s`:\n%s" % (" ".join(args[:3]), json.dumps(data, indent=2)[:2000]))
    return data


def find_key(obj, key):
    """First value for `key` found anywhere in a nested dict/list."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = find_key(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, key)
            if r is not None:
                return r
    return None


def parse_script(path):
    text = open(path, encoding="utf-8").read()
    pat = re.compile(r"### Clip (\d+) of (\d+)[^\n]*\n+```text\n(.*?)\n```", re.S)
    clips = {}
    total = None
    for m in pat.finditer(text):
        clips[int(m.group(1))] = m.group(3).strip()
        total = int(m.group(2))
    if not clips:
        sys.exit("No clip blocks found in %s (expected '### Clip i of N' followed by a ```text block)." % path)
    if total != len(clips):
        sys.exit("Script says %s clips but %d blocks were found." % (total, len(clips)))
    return clips


def lint_prompt(n, text):
    """Return a list of problems that must be fixed before any credits are spent."""
    problems = []
    if len(text) >= PROMPT_LIMIT:
        problems.append("%d characters; the limit is %d" % (len(text), PROMPT_LIMIT))
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            problems.append("missing section '%s'" % sec)
    if re.search(r"#[0-9a-fA-F]{6}\b|rgb\(|hsl\(|pantone", text, re.I):
        problems.append("technical color notation (hex, rgb, hsl or Pantone) is not allowed")
    for style, phrases in STYLE_RULES.items():
        if style in text:
            for ph in phrases:
                if ph not in text:
                    problems.append("%s prompt is missing the required phrase '%s'" % (style, ph))
            setting = re.search(r"^Setting: (.*)$", text, re.M)
            if not setting or "flat" not in setting.group(1).lower():
                problems.append("%s Setting line must say the scenery is flat painted (or a flat void/plate)" % style)
            body = text.split("Negative constraints:")[0]
            bad = sorted({m.group(0).lower() for m in re.finditer(STYLE_FORBIDDEN_WORDS[style], body, re.I)})
            if bad:
                problems.append("%s prompt uses wording that triggers realistic shaded rendering: %s" % (style, ", ".join(bad)))
            beats = text.split("Timed visual beats:")[-1].split("Ending state")[0]
            count = len(re.findall(r"^- \[", beats, re.M))
            if count != STYLE_BEATS[style]:
                problems.append("%s prompts need %d timed beats, found %d" % (style, STYLE_BEATS[style], count))
    return problems


def download_clip(cli, pid, rid, out_path, attempts=5, per_try_timeout=180):
    """Download a generated clip with retries. Never regenerates; only re-reads the finished resource."""
    import time
    tmp_path = out_path + ".new"
    last = None
    for attempt in range(1, attempts + 1):
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        try:
            r = run_cli(cli, ["resource", "download", rid, "--project-id", pid, "-o", tmp_path],
                        timeout=per_try_timeout, check=False)
            last = r
            if r.get("ok") and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                os.replace(tmp_path, out_path)
                return True
        except subprocess.TimeoutExpired:
            last = {"error": "download timed out after %ss" % per_try_timeout}
        print("download attempt %d/%d failed: %s" % (attempt, attempts, json.dumps(last)[:300]))
        time.sleep(10)
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    return False


def contact_sheet(folder, n):
    """Write checks/N.jpg: five frames of N.mp4 in one picture, for the agent to look at."""
    src = os.path.join(folder, "%d.mp4" % n)
    if not os.path.exists(src):
        return None
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found; cannot make a contact sheet. Inspect %s by eye." % src)
        return None
    os.makedirs(os.path.join(folder, "checks"), exist_ok=True)
    dst = os.path.join(folder, "checks", "%d.jpg" % n)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-vf",
                    "fps=1/2,scale=480:-2,tile=3x2", "-frames:v", "1", "-q:v", "4", dst], check=False)
    return dst if os.path.exists(dst) else None


def needs_style_approval(todo_count, state, flag):
    """Batches larger than the limit need a user-accepted test clip first."""
    return todo_count > BATCH_LIMIT_WITHOUT_STYLE_OK and not (state.get("styleApproved") or flag)


def parse_selection(spec, total):
    if spec in (None, "", "all"):
        return list(range(1, total + 1))
    chosen = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            chosen.update(range(int(a), int(b) + 1))
        elif part:
            chosen.add(int(part))
    bad = [n for n in chosen if n < 1 or n > total]
    if bad:
        sys.exit("Clip numbers out of range: %s" % sorted(bad))
    return sorted(chosen)


def load_state(path):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"clips": {}}


TOUCHED = None  # clip keys this process owns; lets several helpers run in parallel on different clips


def save_state(path, state):
    """Write the state file. When several helpers run in parallel, merge only this process's own clips."""
    if TOUCHED is not None and os.path.exists(path):
        disk = load_state(path)
        for k, v in state.items():
            if k != "clips":
                disk[k] = v
        for key in TOUCHED:
            if key in state.get("clips", {}):
                disk.setdefault("clips", {})[key] = state["clips"][key]
        state = disk
    tmp = "%s.tmp%d" % (path, os.getpid())
    json.dump(state, open(tmp, "w", encoding="utf-8"), indent=2)
    os.replace(tmp, path)


def video_args(args, prompt, title, project_id=None):
    a = ["node", "create", "video", "--mode", "t2v", "--model", args.model,
         "--ratio", args.ratio, "--resolution", args.resolution,
         "--duration", str(args.duration), "--prompt", prompt, "--title", title]
    if project_id:
        a += ["--project-id", project_id]
    return a


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="topic folder containing script.md, for example output/my-topic")
    ap.add_argument("--mode", choices=["dry-run", "quote", "run", "inspect", "download"], default="dry-run")
    ap.add_argument("--clips", default="all", help="all, 3, 1-5 or 1,4,7-9")
    ap.add_argument("--model", default="seedance_2.0_mini")
    ap.add_argument("--duration", type=float, default=10)
    ap.add_argument("--ratio", default="16:9")
    ap.add_argument("--resolution", default="720p")
    ap.add_argument("--credit-ceiling", type=int, default=60, help="max credits allowed per clip")
    ap.add_argument("--title", default=None, help="canvas name (defaults to the folder name)")
    ap.add_argument("--wait", default="20m", help="max wait per clip")
    ap.add_argument("--yes", action="store_true", help="required for --mode run: the user approved spending credits")
    ap.add_argument("--style-approved", action="store_true",
                    help="the user accepted the look of a test clip; unlocks batches of more than %d clips" % BATCH_LIMIT_WITHOUT_STYLE_OK)
    ap.add_argument("--force", action="store_true",
                    help="regenerate the selected clips even if N.mp4 exists (new node; the old file is replaced only after a successful download)")
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    script = os.path.join(folder, "script.md")
    if not os.path.exists(script):
        sys.exit("Missing %s. Save the prompts as <topic-folder>/script.md first." % script)
    clips = parse_script(script)
    total = len(clips)
    selected = parse_selection(args.clips, total)
    global TOUCHED
    TOUCHED = {str(n) for n in selected}
    failed = False
    for n in selected:
        for problem in lint_prompt(n, clips[n]):
            print("clip %d: %s" % (n, problem))
            failed = True
    if failed:
        sys.exit("Prompt lint failed. Fix script.md before generating; no credits were used.")
    cli = find_cli()
    print("CLI: %s | model %s | %ss | %s | %s | clips %s of %d" % (
        cli, args.model, int(args.duration), args.ratio, args.resolution, selected, total))

    status = run_cli(cli, ["auth", "status"])
    if not status["data"].get("loggedIn"):
        sys.exit("Not signed in. Run: %s auth login" % cli)

    if args.mode == "dry-run":
        for n in selected:
            r = run_cli(cli, video_args(args, clips[n], str(n)) + ["--dry-run"])
            print("clip %2d: valid (%d chars, side effects: %s)" % (
                n, len(clips[n]), r["data"].get("sideEffects")))
        print("Dry run passed. No canvas created and no credits used.")
        return

    if args.mode == "inspect":
        for n in selected:
            path = contact_sheet(folder, n)
            print("clip %2d: %s" % (n, path or "no clip file to inspect"))
        print("Open each sheet and check: thin black stick bodies and arms/legs, big caricature heads, flat painted "
              "scenery with no realistic lighting, no visible text. Report drift honestly.")
        return

    if args.mode == "download":
        state = load_state(os.path.join(folder, "dreamina.json"))
        pid = state.get("projectId")
        for n in selected:
            rid = state.get("clips", {}).get(str(n), {}).get("resourceId")
            out_path = os.path.join(folder, "%d.mp4" % n)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                print("clip %2d: %d.mp4 already exists" % (n, n))
            elif not rid:
                print("clip %2d: no generated resource recorded; nothing to download" % n)
            elif download_clip(cli, pid, rid, out_path):
                print("clip %2d: saved %s" % (n, out_path))
                sheet = contact_sheet(folder, n)
                if sheet:
                    print("clip %2d: LOOK AT THIS before going on: %s" % (n, sheet))
            else:
                print("clip %2d: download still failing; try again later (the clip is safe on the server)" % n)
        return

    if args.mode == "run" and not args.yes:
        sys.exit("--mode run spends credits. Ask the user first, then pass --yes.")

    state_path = os.path.join(folder, "dreamina.json")
    state = load_state(state_path)
    if not state.get("projectId"):
        name = args.title or os.path.basename(folder)
        r = run_cli(cli, ["canvas", "create", name])
        pid = find_key(r["data"], "projectId")
        if not pid:
            sys.exit("Could not read projectId from: %s" % json.dumps(r)[:800])
        state["projectId"] = pid
        state["canvas"] = name
        save_state(state_path, state)
        print("Canvas created: %s (%s)" % (name, pid))
    pid = state["projectId"]

    if args.mode == "run":
        todo = [n for n in selected if args.force or not os.path.exists(os.path.join(folder, "%d.mp4" % n))]
        if needs_style_approval(len(todo), state, args.style_approved):
            sys.exit("Generate and inspect one test clip first (--clips N, then --mode inspect). After the user accepts "
                     "the look, re-run with --style-approved to unlock batches of more than %d clips."
                     % BATCH_LIMIT_WITHOUT_STYLE_OK)
        if args.style_approved:
            state["styleApproved"] = True
            save_state(state_path, state)

    grand_total = 0
    for n in selected:
        key = str(n)
        info = state["clips"].setdefault(key, {})
        out_path = os.path.join(folder, "%d.mp4" % n)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0 and not args.force:
            print("clip %2d: %d.mp4 already exists, skipping (use --force to regenerate)" % (n, n))
            continue
        if args.force:
            info.clear()
        if info.get("resourceId") and args.mode == "run":
            print("clip %2d: already generated (resource %s); downloading only, no new credits" % (n, info["resourceId"]))
            if download_clip(cli, pid, info["resourceId"], out_path):
                print("clip %2d: saved %s" % (n, out_path))
                sheet = contact_sheet(folder, n)
                if sheet:
                    print("clip %2d: LOOK AT THIS before going on: %s" % (n, sheet))
                continue
            sys.exit("Clip %d is generated but its download keeps failing. Run --mode download later." % n)
        if not info.get("nodeId"):
            r = run_cli(cli, video_args(args, clips[n], str(n), pid))
            node_id = find_key(r["data"], "nodeId")
            if not node_id:
                sys.exit("Could not read nodeId from: %s" % json.dumps(r)[:800])
            info["nodeId"] = node_id
            save_state(state_path, state)
        q = run_cli(cli, ["node", "quote", "--node-id", info["nodeId"], "--project-id", pid])
        est = find_key(q["data"], "totalMaxCredits") or 0
        grand_total += est
        print("clip %2d: node %s, estimated max %s credits" % (n, info["nodeId"], est))
        if args.mode == "quote":
            continue
        if est > args.credit_ceiling:
            sys.exit("Clip %d estimate %s exceeds the ceiling %s. Stop." % (n, est, args.credit_ceiling))
        token = None
        if q["data"].get("confirmationRequired"):
            c = run_cli(cli, ["node", "confirm", "--node-id", info["nodeId"], "--project-id", pid,
                              "--credit-ceiling", str(args.credit_ceiling)])
            token = find_key(c["data"], "creditConfirmationToken") or find_key(c["data"], "token")
            if not token:
                sys.exit("Confirmation token missing: %s" % json.dumps(c)[:800])
        submit = info.get("submitId") or str(uuid.uuid4())
        info["submitId"] = submit
        save_state(state_path, state)
        run_args = ["node", "run", "--node-id", info["nodeId"], "--project-id", pid, "--submit-id", submit]
        if token:
            run_args += ["--credit-token", token]
        run_cli(cli, run_args)
        run_cli(cli, ["operation", "wait", submit, "--project-id", pid, "--timeout", args.wait],
                timeout=int(re.sub(r"\D", "", args.wait) or 20) * 60 + 120)
        shown = run_cli(cli, ["node", "show", "--node-id", info["nodeId"], "--project-id", pid])
        rid = None
        node = (shown["data"].get("nodes") or [{}])[0].get("node", {})
        for res in node.get("resources", []):
            if res.get("type") == "video" and res.get("status") == "success":
                rid = res.get("resourceId")
        if not rid:
            sys.exit("Clip %d finished without a successful video resource: %s" % (n, json.dumps(shown)[:800]))
        info["resourceId"] = rid
        save_state(state_path, state)
        if not download_clip(cli, pid, rid, out_path):
            sys.exit("Clip %d is generated (resource %s) but its download failed. Run --mode download later; "
                     "do not regenerate." % (n, rid))
        print("clip %2d: saved %s" % (n, out_path))
        sheet = contact_sheet(folder, n)
        if sheet:
            print("clip %2d: LOOK AT THIS before going on: %s" % (n, sheet))

    if args.mode == "quote":
        print("Estimated total for the selected clips: about %s credits (maximum). No credits used." % grand_total)


if __name__ == "__main__":
    main()
