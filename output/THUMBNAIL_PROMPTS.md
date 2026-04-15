# Superpowers vs GSD — Thumbnail Generation Prompts

Ready-to-run commands for a fresh Claude Code session. All use the nanobanana-ultimate skill with Gemini Pro model.

## Reference Images Used

- `output/thumb_split_v2d.jpg` — tight crop explosive clash (composition ref)
- `output/thumb_compose_v1.jpg` — bold 3D text style reference
- `output/thumb_compose_v2a.jpg` — terminal layout composition ref
- `output/thumb_split_v2b.jpg` — side-by-side props composition ref
- `sample/characters/clawd/` — Clawd character references
- `thumbnail obs + cc/obsidian_cc_final_v3.jpg` — "Second Brain" style reference

---

## Prompt A: Explosive Clash

```bash
python3 .claude/skills/nanobanana-ultimate/scripts/compose_images.py \
  'YouTube thumbnail, 1280x720, 16:9 aspect ratio.

LAYOUT — divide the frame into two clear zones:
- TOP ZONE (top 30% of frame): MASSIVE white 3D block capital letters reading "SUPERPOWERS vs GSD" with heavy black drop shadow and slight depth extrude effect. Text spans the full width. Thick chunky Impact-style font. Nothing overlaps this text — it sits in clear space against the dark background.
- BOTTOM ZONE (lower 70% of frame): Two orange pixel-art box robot characters (Clawd) in extreme close-up, filling this zone edge-to-edge. Characters do NOT extend into the text zone.

LEFT CHARACTER: Orange pixel-art Clawd bathed in warm white-yellow energy glow, gripping a massive crackling white-yellow lightning bolt aimed toward center. Represents Superpowers.
RIGHT CHARACTER: Same orange pixel-art Clawd bathed in electric blue energy glow, gripping a large glowing blue mechanical gear/cog aimed toward center. Represents GSD.
CENTER: Where the lightning bolt and gear collide — explosive burst of white-yellow and blue sparks, energy particles, and light rays radiating outward.

BACKGROUND: Deep dark charcoal-to-black with subtle cosmic star field visible in gaps.
STYLE: Pixel-art characters rendered in modern 3D style with volumetric lighting. Dramatic cinematic energy effects. Gaming thumbnail aesthetic. No watermark, no extra text.' \
  output/thumb_clash_final.jpg \
  output/thumb_split_v2d.jpg \
  output/thumb_compose_v1.jpg \
  "sample/characters/clawd/clawd_sticker.png" \
  "sample/characters/clawd/clawd_logo.png" \
  "thumbnail obs + cc/obsidian_cc_final_v3.jpg" \
  --model pro --aspect 16:9 --size 2K
```

---

## Prompt B: Terminal Showdown

```bash
python3 .claude/skills/nanobanana-ultimate/scripts/compose_images.py \
  'YouTube thumbnail, 1280x720, 16:9 aspect ratio.

LAYOUT — divide the frame into two clear zones:
- TOP ZONE (top 30% of frame): MASSIVE white 3D block capital letters reading "SUPERPOWERS vs GSD" with heavy black drop shadow and depth extrude effect. Text spans full width. Thick chunky Impact-style font. Clear dark space behind text — nothing overlaps it.
- BOTTOM ZONE (lower 70% of frame): A large orange pixel-art box robot character (Clawd) standing center with arms raised in power pose, flanked by two dark glossy macOS-style terminal windows.

LEFT TERMINAL: Dark rounded-corner window with red/yellow/green traffic light dots, showing "/superpowers" in white-yellow glowing monospace text. Warm white-yellow energy sparks emanating from it.
RIGHT TERMINAL: Same style dark window showing "/gsd" in electric blue glowing monospace text. Blue energy sparks emanating from it.
CENTER CHARACTER: Large orange pixel-art Clawd (box body, black > < eyes, stubby legs, white outline stroke) standing between the terminals, arms raised, at about 50% of the lower zone height.

Energy sparks and lightning connecting the terminals through the character.

BACKGROUND: Dark charcoal gradient, subtle blue-purple atmospheric glow.
STYLE: Pixel-art character with 3D terminal windows. Developer/coding aesthetic meets dramatic gaming thumbnail. No watermark, no extra text beyond what is specified.' \
  output/thumb_terminal_final.jpg \
  output/thumb_compose_v2a.jpg \
  output/thumb_compose_v1.jpg \
  "sample/characters/clawd/clawd_sticker.png" \
  "sample/characters/clawd/clawd_logo.png" \
  "sample/characters/clawd/clawd_welcome.png" \
  --model pro --aspect 16:9 --size 2K
```

---

## Prompt C: Side by Side Props

```bash
python3 .claude/skills/nanobanana-ultimate/scripts/compose_images.py \
  'YouTube thumbnail, 1280x720, 16:9 aspect ratio.

LAYOUT — divide the frame into two clear zones:
- TOP ZONE (top 30% of frame): MASSIVE white 3D block capital letters reading "SUPERPOWERS vs GSD" with heavy black drop shadow and depth extrude effect. Text spans full width. Thick chunky Impact-style font. Clear dark space behind text — nothing overlaps it.
- BOTTOM ZONE (lower 70% of frame): Two large orange pixel-art box robot characters (Clawd) side by side, each taking up roughly half the width.

LEFT SIDE: Orange pixel-art Clawd facing right, holding a huge glowing white-yellow lightning bolt. Warm golden-white atmospheric glow behind. Small white text "/superpowers" below the character.
RIGHT SIDE: Same orange pixel-art Clawd facing left, holding a huge glowing electric blue mechanical gear/cog. Cool blue atmospheric glow behind. Small white text "/gsd" below the character (spelled G-S-D, not QSD).
CENTER DIVIDE: Crackling lightning energy where the two sides meet — white-yellow sparks from left colliding with blue sparks from right.

BACKGROUND: Dark cosmic black with subtle star field, split warm-left / cool-right atmosphere.
STYLE: Pixel-art characters in modern 3D render style. Dramatic neon glow effects. Gaming/tech YouTube thumbnail aesthetic. No watermark, no extra text beyond what is specified.' \
  output/thumb_props_final.jpg \
  output/thumb_split_v2b.jpg \
  output/thumb_compose_v1.jpg \
  "sample/characters/clawd/clawd_sticker.png" \
  "sample/characters/clawd/clawd_logo.png" \
  "thumbnail obs + cc/obsidian_cc_final_v3.jpg" \
  --model pro --aspect 16:9 --size 2K
```

---

## Tips for Iteration

- Change output filename to get a new variation (Gemini generates slightly different each time)
- Add more reference images for tighter style control (up to 14 refs supported)
- Use `edit_image.py` on any result to tweak specific elements
- Use `--size 4K` for maximum resolution
- To batch generate variations: run the same command multiple times with different output names
