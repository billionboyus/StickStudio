# Style 7 — Caricature Chronicle (dark-comedy history countdown)

## What it is

A fast, wry history-explainer look: thin black stick bodies carrying large, over-detailed caricature heads, played as limited cut-out animation over flat painterly backgrounds, edited at roughly one shot every 2–3 seconds. It suits ranked lists ("seven insane weapons", "eight worst things"), historical event breakdowns, and biographies told with dark comedy.

It differs from Style 6 (polished cel-shaded cartoon, simple dot-and-brow faces, slower epic staging) and Style 3 (paper texture, prehistoric cast). Do not mix their drawing rules.

Derived from three reference videos and eight reference frames supplied by the owner. The audio was not analyzed (only captions); music, SFX and voice are proposals. Draw the grammar, never copy another channel's recurring mascot or logo.

## Fixed drawing grammar

- **Bodies:** thin black stick torso, arms and legs with a uniform line weight, exactly two arms and two legs, each shown only in its current pose. Hands and feet are simple rounded ends.
- **Heads are the actors:** large white (or story-appropriate skin tone) heads drawn with fine line shading: wrinkles, stubble, brow furrows, heavy lids, bloodshot or oversized eyes, crooked teeth, tired or smug mouths. Expressions are exaggerated and readable at a glance: double-takes, deadpan stares, screaming mouths, side-eye.
- **Hair, beards and headwear are painted onto the head:** helmets, hats, turbans, caps, feathers and wigs carry the era. Bodies may stay bare, or key characters may wear full period costume (robes, armor, cape, tunic); keep any costume identical across clips. Do not dress every extra in full costume.
- **Backgrounds, three plate types (use all three across a video):**
  1. flat painterly cartoon scenery with soft gradients (hills, desert, sunset sky, burning village, palace interior);
  2. softened or posterized photo-like plates (street, field, thatched huts, palace) kept behind the figures;
  3. plain flat grey or white void for host or aside shots.
- **Props and effects:** simple textured cartoon props (pots, spears, swarms, fireworks, fire, arrows) with the same thick outline as the figures.
- **Palette:** muted, earthy and warm by default (sand, olive, rust, slate), with one saturated accent such as fire orange or blood-red cloth per scene. Name colors in plain words.
- No paper texture, no glossy 3D, no photoreal faces, no cel-shaded metal sheen.
- Never use lighting words that invite realistic rendering (dim, moonlit, candlelight, volumetric, cinematic, realistic, shadows, glow, spotlight, bokeh, depth of field): use flat colors such as "pale", "warm orange lamp colors" or "flat blue night tones" instead. The Dreamina helper lints this.
- Video models drift toward soft, shaded, full-bodied characters, especially for sleeping, distant or robed figures and in dim interiors. Keep the stick-body sentence in the anchor, write interiors and props as "flat painted", and inspect a test clip before generating the rest.

### Anchor (repeat verbatim in every prompt)

```text
Limited cut-out 2D cartoon animation: thin black stick-figure bodies with large white caricature heads drawn with fine line shading, wrinkles, stubble, heavy-lidded or bloodshot eyes and exaggerated rubbery expressions; hair, beards and hats painted on the head. Uniform thick black outlines, flat painterly backgrounds with soft gradients. Every character, including sleeping or distant ones, keeps a thin black stick body with thin black stick arms and legs; clothing is a flat simple shape on the torso only, never a soft shaded full body. Exactly two arms and two legs, each shown only in its current pose. Dry dark-comedy tone.
```

Negatives (compact): `NO VISIBLE TEXT, LETTERS, NUMBERS, SUBTITLES, LOGOS OR WATERMARKS (blank signs and abstract markers only), NO SPEECH BUBBLES, NO GORE OR DISMEMBERMENT, NO PHOTOREALISTIC FACES, NO FULL-BODIED SHADED CHARACTERS, NO REALISTIC LIGHTING ON CHARACTERS, NO GLOSSY 3D CGI, NO PAPER TEXTURE, NO EXTRA LIMBS, NO DUPLICATE OR FUSED HEADS, NO COSTUME CHANGES, NO EXTRA CHARACTERS.`

## Cast cards

Per named role give: role and age range, head shape and size, skin tone, hair/beard, brow and eye character, one signature expression, headwear, optional clothing piece, one accessory. Recurring characters need two visible non-color differences. Freeze each card and repeat its FULL text in every prompt where the character appears; never "the same general". Keep named characters to three or fewer per clip and describe extras once ("a line of identical soldiers with the same helmet and sour expression").

**Optional host avatar:** a plain-void presenter who gestures, holds a prop that illustrates the next point, or reacts to the story. Invent a new avatar for each channel or project; do not copy an existing channel's mascot. Host shots are 10–25% of runtime and never carry plot action.

## Pacing (measured on the reference videos)

| Measure | Reference value | Rule for this style |
|---|---|---|
| Shot cuts | about 19–25 per minute across three videos (median gap 2.1–2.5s; in the fastest video a quarter of gaps were 1.2s or shorter, and the first minute had a cut about every 1.7s; longest holds 8–19s) | a new shot about every 2s; five timed beats per 10s clip, with 1–1.5s bursts at action peaks |
| Narration speed | about 200 words per minute in all three videos (about 33 words per 10s) | 30–34 words per 10s clip (about 180–200 wpm); shorten VO before slowing the pace |
| Hook | premise and promise in the first 6–20s | state the premise or ranking rule within 10s |
| List segments | 8 ranked items of about 85–110s, or 7 weapons of about 90–100s | one item per 80–110s in long videos; one item per 10–20s in 30–60s videos |
| Host bumpers | about 10–25% of sampled frames | one bumper per 40–90s as a breather or a topic switch |
| Ending | dark quip, no long outro | land the final item, then one dry button line |

Because a generated clip is 10s, build each clip from five 2s beats: 1) establish, 2) action, 3) second action or cut-away, 4) reaction close-up, 5) kicker or transition. Action peaks may split a beat into two 1s cuts. Hold a single deadpan reaction for 1–2s as a payoff; use quick push-ins, whip pans, speed-line bursts and zoom punches on static plates, and puppet-style motion (head tilt, arm swing, a hop) on figures. Change something on screen at every beat: a new angle, plate, prop or character. Avoid abstract morphing.

## Story engine: the countdown

1. **Hook (0–10s):** premise plus the ranking rule ("seven insane ancient weapons", "ranked from bad to horrific").
2. **Item loop, repeat per item:** title beat (number plus the thing), context in one sentence, the surprising mechanism or deed, a comic reenactment, a fact inset (painting, diagram or map), then a dark-funny kicker line.
3. **Escalation:** order items from mild to extreme, or primitive to advanced, and say so in the hook.
4. **Ending:** the last item hits hardest, followed by one deadpan closing line. A discussion question is optional, not required.

For non-list stories (events, biographies) use setup → complication → reversal → kicker, with the same pacing.

**Second-person biography option:** tell a life or a battle as "you" in present tense ("It's medieval Japan and you're born in a small village..."), moving fast through key episodes with a one-line joke or gut-punch per episode (a real-life tragedy stays straight). Works in both tone modes.

## Insets and text

Generated clips contain no visible words. Plan these as post-production inserts, listed by clip and time in the proposal:
- ranked-number or name cards (portrait on a parchment plate plus a name);
- map plates with place labels (generate the map with icon markers only; add labels in post);
- diagram or artwork plates (historic paintings and technical drawings, licensed or public-domain);
- thought or speech bubbles with 2–5 words.

## Tone modes

- **Wry (default):** dark-comedy history with deadpan reactions, host bumpers, rubbery expressions and comedic stings, as described above.
- **Straight (real battle or documentary):** use when the user asks for real narration, a serious battle, or a documentary feel. Keep the stick bodies and caricature heads, but ground the acting: tense, tired, determined, shocked expressions, with no rubbery gags, no toy props, no host bumper and no jokes. Cuts about every 2s with five beats per clip; 30–34 spoken words per 10-second clip (about 180–200 wpm, grave but brisk, the measured speed of the reference videos); a grave documentary narrator profile with a brisk steady pace (resolve every field, repeat it verbatim, untested with the provider); music of low strings, military snare, muted brass and sustained drones, with no piano and no comedic stings; realistic but bloodless SFX. Use a map plate and time cards as post-production inserts, show both sides as people, state losses plainly in the closing line, and never mock the dead.
- **Straight-mode anchor:** repeat the anchor above but replace its last sentence with `Grave documentary tone with grounded expressions.`

## Era notes (modern conflicts, including WW2)

- Identify sides by helmet shape, cap, color and silhouette only. Never draw swastikas, SS runes or other hate symbols, and avoid real insignia and flags; use plain, unmarked uniforms. Add `NO SWASTIKAS OR HATE SYMBOLS, NO REAL INSIGNIA` to the negatives.
- Prefer stories about plans, inventions, deception, logistics and blunders. Do not joke about the Holocaust, genocide, civilian bombing casualties or war crimes; if a topic touches them, play it straight and briefly, or choose another topic.
- Real named people are allowed as caricature cast cards but keep them dignified or gently comic, with facts hedged ("reportedly") where sources disagree.
- Animal and wartime harm stays implied: no animals hurt on screen, no casualties, smoke and flame as cartoon effects.

## Tone guardrails

- Violence is cartoon-implied: X eyes, a small red dot, a toppled figure, fire, smoke. No blood pools, severed body parts or torture close-ups.
- Joke at perpetrators' hubris, logistics, bad plans and bad manners, and at the absurd mechanics of history. Do not mock victims of massacres, slavery, genocide or famine; play those beats straight, with a held, quiet shot, then continue.
- Fiction is stylized dramatization: do not invent quotations, numbers or causes. Mark disputed claims as "historians disagree" in VO.

## Audio

Voice: apply `voice-continuity.md`. A suitable video-level profile is an adult male, General American, brisk deadpan storyteller with light sarcasm and dry studio sound; resolve every field and repeat it verbatim. This profile is untested with the provider. Music: sparse comedic underscore (plucked strings, a muted brass sting, light percussion), with short SFX on impacts and reactions; no mandatory piano. SFX and music were not analyzed in the references.

## Continuity and generation

Phase A includes: the ranked or story outline with item order and timings; cast cards; the plate plan (which plate type per item); host-avatar card if used; the insert list; music/SFX; opening and ending states per clip. Phase B repeats the verbatim anchor, the full visible cast cards, the setting and the negatives. Track prop ownership and keep the same clothing piece per character. Reference frames or the previous ending frame may be used as references when the interface supports it. Treat generated consistency as an acceptance check, not a guarantee. This style has not been provider-tested yet: start with one clip, inspect heads, hands, props and crowd drift, and stop to report material failures.

## Prompt assembly

Output spec → anchor → plate and setting → full cast cards for visible roles → opening state → five timed beats labeled `[0–2s]`, `[2–4s]`, `[4–6s]`, `[6–8s]`, `[8–10s]` with props and reactions → exact quoted VO (audio-only) → verbatim voice block → music and SFX → ending state → negatives. Keep each prompt under 3,600 characters.

## Review checklist

- Heads carry the acting; bodies stay thin black stick limbs with two arms and two legs.
- Anchor, cast cards and clothing pieces match across clips; extras are described once.
- All three plate types appear across the video; no paper texture or glossy 3D.
- Each 10s clip has five beats (a visible change every ~2s) and about 30–34 words of VO.
- Hook states the premise or ranking rule within 10s; items escalate; the ending is a dry button.
- Insets are listed for post-production; clips contain no words.
- Violence is implied; victims are not mocked; facts are not invented.
- Voice block is identical in every prompt; limits of the untested profile are disclosed.
