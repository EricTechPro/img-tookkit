---
name: sketch-explainer-style
description: Use when user asks to generate or create any image in sketch-explainer style, or references sketch-explainer in an image generation context
---

# Sketch Explainer Style

Generates images matching the sketch-explainer visual style using reference images and a style profile.

## Usage

Generate an image in this style:

```bash
python3 .claude/skills/sketch-explainer-style/scripts/generate_styled.py \
  "user's content description" \
  output.jpg \
  [--preset blog|youtube|social|story|og|banner] \
  [--aspect 16:9|1:1|9:16|...] \
  [--size 1K|2K|4K]
```

The script automatically loads all reference images and the style profile from its own folder.

## Style Profile

A hand-drawn, line-art illustration style with cross-hatching for shading, used for clear, diagrammatic explanations. The visual language is primarily monochromatic but can feature muted, watercolor-like color sections to organize information, with a focus on icons and flow.

## Character References

Include named characters (from `sample/characters/`) as visual reference:

```bash
python3 .claude/skills/sketch-explainer-style/scripts/generate_styled.py \
  "diagram showing Claw'd helping a developer" \
  output.jpg \
  --preset blog \
  --character clawd
```

Available characters are stored in `sample/characters/{name}/` with reference images.
When the user mentions "Claw'd", "Claude bot", or the Claude Code mascot, always use `--character clawd`.

## Examples

- "Generate a blog header about Q4 results in sketch-explainer style"
- "Create a social media post for our product launch in sketch-explainer style"
- "Make a YouTube thumbnail in sketch-explainer style"
- "Create a diagram with Claw'd explaining microservices" (auto-includes `--character clawd`)
