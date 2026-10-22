---
name: directing-stickman-videos
description: "Use when turning copy, notes, articles, or topics into customizable-length English stick-figure videos (in 10-second multiples: 30s, 60s, 3min, 5min, default 60s), kinetic line-animation explainers, motivational shorts, or Gemini Omni Flash prompt packages."
---

# Directing Stickman Videos

## Core contract

Turn one source into a confirmed director's proposal and then N standalone prompts for approximately ten-second Gemini Omni Flash clips (where N = target duration in seconds / 10; default 6 clips for 60 seconds). Preserve the source's meaning while structuring it through a high-completion 5-stage emotional narrative arc.

## Setup gate

Require these before planning:

- source material
- aspect ratio: `16:9` or `9:16`
- target duration: in multiples of 10 seconds (e.g. `30s`, `60s`, `90s`, `3min`, `5min`; default: `60s` / 6 clips if unspecified)
- visual style and theme:
  - `Style 1 (Classic Minimalist)`: light (white background, black figure) or dark (black background, white figure)
  - `Style 2 (Modern Beanie Zeke)`:
    - `Style 2A (Modern Studio Tech)`: pure white high-key studio, subtle light-gray perspective grid, floating cyan/blue glass UI
    - `Style 2B (Cinematic Story)`: full-color narrative environments, cinematic lighting & depth
  - `Style 3 (Prehistoric Hand-Drawn / Dark Comedy)`: expressive white filled heads, black stick limbs, animal-hide costumes and earthy prehistoric settings; story-specific casting
  - `Style 4 (Cozy Storytelling / 治愈故事风)`: expressive minimalist white-filled characters with dark stick limbs in full-color 2D cartoon environments; varied story locations and cinematic shot changes
  - `Style 6 (History Stickman)`: cel-shaded cartoon with white filled heads, black stick limbs and historical costume; Rome is the first era pack, and the user names the era for other periods
  - `Style 7 (Caricature Chronicle)`: thin black stick bodies with large over-detailed caricature heads, flat painterly backgrounds, fast history countdowns, event breakdowns and real-battle narratives cut about every 2 seconds; tone is `wry` (dark-comedy, default) or `straight` (grave documentary; use it when the user asks for real narration, a serious battle or a documentary feel, and ask only if the tone is unclear)

If aspect ratio or visual style is missing, ask for all missing items in one concise message and stop. If duration is omitted, default to 60 seconds (6 clips). If a user provides a duration not divisible by 10, round to the nearest 10-second multiple. If a user specifies only light or dark theme, default to Style 1. Never select an aspect ratio or style silently. Do not re-ask choices already supplied.

Urgency, generation cost, client pressure, and requests to "pick normal settings" do not waive this gate.

## Workflow

1. Read `references/storyboard-template.md`, `references/style-catalog.md` and `references/voice-continuity.md`. Structure the narrative using the **5-Stage High-Completion Heartbeat Engine** (Golden Hook → Disrupting Assumptions → Unveiling Insider Secrets → Ultimate Truth Revelation → Elevation & Interactive Discussion), with timing dynamically scaled to the target duration. Produce Phase A in the user's language, with English VO and a reference translation.
2. Stop after the director's proposal and request explicit approval.
3. If the user changes ratio, duration, style, theme, narration, scene structure, or global direction, recompose Phase A and request approval again.
4. Only after approval of the current Phase A, read `references/omni-flash-prompt-contract.md`, produce Phase B, and save the prompts as `output/<title-slug>/script.md` as the Topic folder rule below requires (pure prompt output only; no video CLI execution).
5. Use `references/examples.md` only when a concrete end-to-end example would resolve ambiguity.

Topic approval, schedule pressure, or approval of an older draft is not approval of the current Phase A.

## Output rules

For Style 3, read `references/prehistoric-dark-comedy.md` before planning. Its casting, story rhythm, palette and continuity rules override the generic no-idle, device-count and five-stage discussion-ending rules below. Use setup → escalation → ironic payoff for narrative shorts; do not force a discussion question into a visual punchline. This is a visual storytelling style, not a claim about actual prehistory.

For Style 4, read `references/cozy-storytelling.md` before planning and prompt assembly. Default each new ten-second segment to a different recognizable story setting, unless the user explicitly requests one location or approves a deliberate return. Preserve characters, drawing grammar, important props, movement direction and narrator—not an identical table or background across the whole video. Name the location cuts and any time jumps in Phase A. This is full-color cartoon storytelling, not a hand-drawn/sketchbook mode and not a claim of photorealistic 3D backgrounds.

For Style 6, read `references/history-stickman.md` before planning. If the era is missing, ask for it with the other setup items; Rome is available as a ready pack, and any other era gets a drafted era pack in Phase A for approval. Its cast, tone, era-pack, crowd and non-graphic-violence rules override the generic no-idle, device-count and mandatory discussion-ending rules below; use the five-stage flow for explainers and setup → escalation → turning point for narrative shorts. History is stylized, so do not present invented scenes or details as fact.

For Style 7, read `references/caricature-chronicle.md` before planning. Its caricature-head grammar, five-beat 10-second clips (about 30–34 spoken words, a visible change every ~2 seconds), countdown or setup → complication → reversal → kicker story engine, host-bumper, plate and inset rules, and tone guardrails override the generic no-idle, device-count, 20–25 words-per-clip and mandatory discussion-ending rules below. Every Style 7 prompt MUST repeat the verbatim anchor including its stick-body sentence (every character, even sleeping or distant ones, keeps a thin black stick body with thin black stick arms and legs; clothing is a flat shape on the torso only), the Style 7 negatives (including `NO FULL-BODIED SHADED CHARACTERS`), exactly five timed beats, and the voice, music and character locks; interiors and props are written as flat painted. `scripts/dreamina_generate.py` lints this and refuses to generate prompts that break it. Insets (name cards, map labels, bubbles) are post-production overlays, never generated text. Violence is cartoon-implied, victims are never mocked, and history is stylized, not invented fact.

- Structure every script using the 5-stage high-completion flow:
  1. **Golden Hook**: Instant curiosity trigger via a counter-intuitive question or visual paradox. Timing is flexible based on duration (e.g. within the first 2–5 seconds in short videos, up to 10–15s in long videos); never open with generic platitudes.
  2. **Disrupting Assumptions**: State what everyone thinks is true, then shatter it in one sentence to build cognitive conflict.
  3. **Unveiling Insider Secrets**: Pull back the curtain on hidden mechanics, counter-intuitive details, or the real obstacle.
  4. **Ultimate Truth Revelation**: Deliver the underlying business logic or human psychology truth with maximum cognitive payoff.
  5. **Elevation & High-Engagement Discussion**: Conclude with a memorable punchline and an irresistible discussion prompt that sparks debate in the comments.
- Scale English VO word count to approximately 20–25 words per 10-second clip across N clips (e.g. ~60–75 words for 30s / 3 clips, ~120–150 words for 60s / 6 clips, ~360–450 words for 3min / 18 clips, ~600–750 words for 5min / 30 clips).
- Give each clip three timed beats, at least four relevant visual devices, and a visual change every two to three seconds. Exception: Style 7 uses five 2-second beats per clip with a visible change about every 2 seconds (see `references/caricature-chronicle.md`).
- Keep character proportions, line weight, style, and narrator consistent across all clips.
- For Style 1, freeze the concise character anchor from `references/style-catalog.md` and repeat it verbatim in every clip. Keep two arms and two legs, one current pose per limb, stable proportions and uniform medium line weight; a moving arm replaces its previous pose rather than adding another arm. Keep the figure monochrome and saturated accents on props/graphics. Do not replace the anchor with "same character", ellipses, numeric anatomy recipes, skeleton/path instructions or clip-specific appearance descriptions. Occasional simple line expressions are allowed; the head remains hollow. Keep rich actions and effects separate from character design. Treat generated consistency as a visual acceptance check, not a guarantee from repeated text.
- For Style 1, limit the video to three saturated accent colors named with ordinary descriptive words (e.g. vivid red, electric blue, warm gold). For light theme, enforce a flat, digitally pure-white canvas with no textures, gradients, or 3D depth.
- For Style 2 (Modern Beanie Zeke), enforce character consistency:
  - Clip 1: `A minimalist 2D animated stick figure wearing a bright red beanie (smooth knit, no pom-pom) and a yellow t-shirt, with simple black stick limbs and shorts. Simple black lines, vibrant colors, smooth 2D animation style.`
  - Clips 2–N: `The same minimalist 2D animated stick figure in a bright red beanie and yellow shirt... Simple black lines, vibrant colors, smooth 2D animation style.`
  - No detailed eyes, pupils, or photorealistic features (avoids bug-eye deformation).
- For Style 2A (Modern Studio Tech), enforce: `in a modern bright white studio space with subtle light-gray perspective grid lines on the floor plane. High-key studio lighting, clean white negative space, sleek glowing cyan and electric blue glass holographic UI elements.` Always include negative constraint: `STRICTLY MINIMALIST, NO CIRCUIT BOARD TEXTURES, NO SCI-FI WALL PANELS, NO CRACKED CONCRETE.`
- For Style 2B (Cinematic Story), specify full-color narrative setting and cinematic lighting while preserving the 2D animated stick-figure character design.
- For Style 4, freeze each approved character's complete anchor and repeat it in every clip where that role appears. Separate static design from first-frame positions, timed prop transfers and final states; changing scene does not reset prop ownership or the narrator. Read its reference for shot variety and visual acceptance checks.
- For all styles, avoid abstract liquid/shape morphing. Drive motion with concrete character actions (leaping, touching glass, drawing luminous lines, opening doors) with timed beats across `[0–3s]`, `[3–7s]`, and `[7–10s]`. Never leave the character idle.
- For **all styles**, apply `references/voice-continuity.md`: choose a complete video-level voice profile in Phase A, then repeat its full frozen English block verbatim in every clip. Different videos may choose different voices; a scene/style/character change must not recast the narrator. Lock timbre, register, accent, texture, delivery, pace and recording treatment, not just "same narrator". Keep emotional progression in visuals/music. Style-specific music rules never override this shared voice contract. Mandate BGM continuity from clip 1.
- Treat narration as audio-only (`Audio voiceover only, strictly no speech bubbles, no dialogue boxes`). Quote exact dialogue and forbid alteration, repetition, captions, subtitles, or visual transcription.
- Never place technical color notation (hex, RGB, Pantone) inside generation prompts.
- Default generated clips to no visible words, letters, numbers, or interface copy. Put optional two-to-five-word overlays in a separate post-production note.
- Match every clip ending to the next clip opening through action, an important prop, screen direction or a planned cut. Style 4 uses deliberate scene changes or approved time jumps; it does not require the same background in adjacent clips.
- Do not invent unsupported facts, statistics, quotations, or product claims.

## Topic folder, script and video (required for every Phase B)

Every topic gets its own folder under the project's `output/` (current working directory; create it if missing). Everything for that topic lives in it, and nothing is saved loose in `output/`.

- **Folder:** `output/<title-slug>/`, where the slug is the lowercase English title with hyphens (for example `output/what-did-samurai-actually-do-in-peacetime/`). If the folder already exists and holds a script, do not overwrite it silently: add a numeric suffix (`-2`) unless the user asked to replace it.
- **Script:** `output/<title-slug>/script.md` with ONLY the standalone prompt blocks. For each clip write `### Clip <i> of <N> (mm:ss–mm:ss)` followed by one fenced ```text block with the complete prompt, and separate clips with a line containing `---`. Do not put Phase A, storyboard tables, the global continuity block, the stitching guide, the voice/music note, the post-production overlay list or any commentary in the file. Those belong in the chat reply.
- **Check before saving:** every prompt is under the character limit in the prompt contract, and the file contains exactly N clip blocks.
- **Output:** The deliverable is prompt-only in `output/<title-slug>/script.md`. Do not invoke external video CLI tools or Dreamina CLI (no Seedance 2.0 mini calls, no requesting explicit yes for credits, no `1.mp4` generation; see `references/dreamina-generation.md` for legacy reference). Leave the output with the prompt only.

## Revision rules

Recompose rather than rename:

- `16:9`: stage action across left, center, and right; use lateral tracking and negative space.
- `9:16`: use depth, stacked motion, vertical reveals, and interface-safe placement.

Theme, ratio, duration, or style changes require a fresh visual balance check. A global change invalidates prior approval.

## Final check

Apply the checklist in the loaded reference. Repair any failed condition before responding.
