---
name: style-factory
description: Use when user wants to learn a visual style from reference images, create a reusable style skill, or says "learn this style", "create a style from these images", "build a style profile"
---

# Style Factory

Creates reusable style skills from reference images. Given a folder of images (or URLs to fetch), analyzes the visual style and scaffolds a complete skill that generates new images locked to that style.

## Workflow

### Phase 1: Gather Assets

1. **Local images** - If user provides a path, use those directly
2. **Online assets** - If user mentions a URL, brand website, or Google Drive link:
   - Use `WebFetch` to scrape the page, find image URLs (`<img>`, `og:image`, favicon, logo elements)
   - Download relevant images with `curl` to a temporary `references/` folder
   - For Google Drive: convert share URL to `https://drive.google.com/uc?export=download&id={FILE_ID}`
3. **Organize** - Rename to `ref_001.jpg`, `ref_002.jpg`, etc. Keep up to 8 reference images (most representative)

### Phase 2: Analyze Style

Run the analysis script to extract a structured style profile:

```bash
python .claude/skills/style-factory/scripts/analyze_style.py \
  --name "style-name" \
  --output .claude/skills/{style-name}-style/references/style_profile.json \
  ref_001.jpg ref_002.jpg ...
```

This sends reference images to Gemini with `response_modalities=["TEXT"]` and returns a JSON profile:

```json
{
  "style_name": "...",
  "style_summary": "2-3 sentence description",
  "color_palette": {
    "dominant_colors": ["#hex1", "#hex2", "#hex3"],
    "accent_colors": ["#hex1"],
    "saturation": "low | medium | high | vibrant",
    "warmth": "cool | neutral | warm"
  },
  "composition": {
    "layout": "centered | rule-of-thirds | asymmetric | grid | freeform",
    "whitespace": "minimal | moderate | generous",
    "density": "sparse | balanced | dense"
  },
  "mood": "...",
  "rendering_style": "...",
  "visual_elements": ["..."],
  "lighting": "...",
  "typography_hints": "...",
  "negative_characteristics": ["..."]
}
```

**Present the profile to the user for review before proceeding.**

### Phase 3: Build the Skill

Create this folder structure:

```
.claude/skills/{style-name}-style/
  SKILL.md                    # Triggers on "{style-name} style" mentions
  references/
    style_profile.json        # Analyzed style profile
    ref_001.jpg               # Reference images (self-contained)
    ref_002.jpg
    ...
  scripts/
    generate_styled.py        # Main generation script (copied from template)
```

**SKILL.md template** for the generated skill:

```markdown
---
name: {style-name}-style
description: Use when user asks to generate or create any image in {style-name} style, or references {style-name} in an image generation context
---

# {Style Name} Style

Generates images matching the {style-name} visual style using reference images and a style profile.

## Usage

Generate an image in this style:

\```bash
python .claude/skills/{style-name}-style/scripts/generate_styled.py \
  "user's content description" \
  output.jpg \
  [--preset blog|youtube|social|story|og|banner] \
  [--aspect 16:9|1:1|9:16|...] \
  [--size 1K|2K|4K]
\```

The script automatically loads all reference images and the style profile from its own folder.

## Style Profile

{Insert style_summary from profile here}

## Examples

- "Generate a blog header about Q4 results in {style-name} style"
- "Create a social media post for our product launch in {style-name} style"
- "Make a YouTube thumbnail in {style-name} style"
```

**generate_styled.py** - Copy the template from `.claude/skills/style-factory/scripts/generate_styled_template.py` into the new skill's `scripts/generate_styled.py`.

**Symlink the .env** so the generated skill can find the API key:

```bash
ln -sf ../../nanobanana-ultimate/.env .claude/skills/{style-name}-style/.env
```

### Phase 4: Confirm

Tell the user:
- Style skill created at `.claude/skills/{style-name}-style/`
- How to use it: "Generate a [content] in {style-name} style"
- Number of reference images included
- Style profile summary
