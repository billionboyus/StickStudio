# Dreamina generation (Seedance 2.0 mini)

Use this after the script is saved and the user says yes to generating. Every agent follows the same steps with the same helper, so results land in the same place.

## Folder layout (one folder per topic)

```
output/<title-slug>/script.md     prompt blocks only (### Clip i of N + one ```text block each)
output/<title-slug>/1.mp4 ... N.mp4   generated clips, numbered in order
output/<title-slug>/dreamina.json     resume state (canvas and node ids), written by the helper
```

Create the folder when you first save the script. Everything for the topic stays in it: script, clips, state. Never write loose files into `output/`.

## Ask first, then generate

After saving `script.md`, ask once, in plain words: "Generate the video with Dreamina using Seedance 2.0 mini, N clips of 10 seconds, about X credits?" Get X from the quote step below. Never spend credits without an explicit yes. Offer to test clip 1 first. Do not repeat the question once answered, and do not generate if the user declines.

## Helper

`scripts/dreamina_generate.py` (in this skill folder) drives the Dreamina CLI. It finds `dreamina-canvas` on PATH, in `~/bin`, or from the `DREAMINA_CLI` environment variable. On Windows use `python -X utf8`.

| Mode | What it does | Spends credits |
|---|---|---|
| `--mode dry-run` | validates every prompt locally with `node create video --dry-run` | no |
| `--mode quote` | creates the canvas and draft nodes, asks the service for a credit estimate | no |
| `--mode run --yes` | quote, run, wait, then download each clip to `N.mp4` | yes |

```bash
python scripts/dreamina_generate.py output/<slug> --mode dry-run
python scripts/dreamina_generate.py output/<slug> --mode quote --title "<Topic title>"
python scripts/dreamina_generate.py output/<slug> --mode run --clips 1 --yes      # test clip first
python scripts/dreamina_generate.py output/<slug> --mode run --yes                # everything
```

Lint: before any mode runs, every selected prompt is checked for length, required sections, no technical color notation, and the style's enforced phrases (Style 7 needs the stick-body sentence, `FULL-BODIED SHADED CHARACTERS` in the negatives and exactly five beats). A failing prompt stops the run with no credits used. `--force` regenerates a clip into a new node and replaces `N.mp4` only after the download succeeds.

Enforced by the helper: Style 7 prompts must not use wording that makes the model render shaded realistic scenes (dim, moonlit, candlelight, volumetric, cinematic, realistic, shadows, glow, spotlight, bokeh, depth of field) and the Setting line must say the scenery is flat painted. Batches of more than two clips are refused until a test clip has been generated, inspected with `--mode inspect` (writes `checks/N.jpg`, a five-frame contact sheet) and accepted by the user, after which the agent passes `--style-approved`. `run` also writes the contact sheet after each download and prints its path: open it before continuing.

If drift persists after the prompt rules, the next control is reference images (the model's `m2v` mode accepts up to 9 images): upload approved style frames or character sheets and use them as references. This changes the cost and the result, so ask the user first.

Defaults: model `seedance_2.0_mini` (alias `seedance2.0mini`), text-to-video (`t2v`), `--duration 10`, `--ratio 16:9`, `--resolution 720p`, a per-clip credit ceiling of 60. Match `--ratio` to the approved proposal (`9:16` for portrait). Finished clips are skipped on re-run, so an interrupted job resumes. Clips run one at a time; a 30-clip video takes a long time, so run it in the background and report progress.

## Facts checked on 2026-10-18 (CLI 1.0.2, signed in)

- `seedance_2.0_mini` supports `t2v`, `first_last_frame` and `m2v`, 720p only, durations 4 to 15 seconds, ratios 21:9, 16:9, 4:3, 1:1, 3:4 and 9:16.
- A 10-second 720p mini quote came back at a maximum of 50 credits per clip, so a 6-clip video is about 300 credits and a 30-clip video about 1,500. Tell the user the estimate before asking.
- `node create video --dry-run` validates locally with no side effects. `node quote` and `canvas create` use no credits.
- `resource download <resource-id> -o <file.mp4>` downloads a generated video (about 10 MB in 7 seconds in the test). Use an explicit file path.

## Verified end to end (2026-10-18)

The helper ran `canvas create`, `node create video`, `node quote`, `node run`, `operation wait`, `node show` and `resource download` for one real clip (Shaolin clip 3, `seedance_2.0_mini`, 10 s, 16:9, 720p). It cost 50 credits and saved `3.mp4` (9.5 MB, H.264 1280x720 plus AAC audio, 10.0 s). The confirmation step was not required for that quote (`confirmationRequired: false`); the helper handles it if it appears. Narration audio was not listened to by the agent: check by ear.

Style lesson from that clip: the model followed the beats and the host caricature, but drew a sleeping monk with a soft full body and the bell in a shaded painterly style, losing the thin black stick-body look. For Style 7, when generating, strengthen the anchor with `Every character, including sleeping or distant ones, keeps a thin black stick body with simple stick limbs` and add `NO FULL-BODIED SHADED CHARACTERS` to the negatives. Always inspect a test clip before generating the rest.

## Failure handling

- Not signed in: `dreamina-canvas auth login` (the user completes the sign-in).
- Estimate above the ceiling: stop and ask the user; do not raise the ceiling silently.
- Download fails: retry the download alone with `resource download`, never regenerate.
- Never delete the user's canvases or nodes.
