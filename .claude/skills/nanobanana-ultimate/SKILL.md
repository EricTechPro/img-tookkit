# NanoBanana Ultimate — AI Image Generation

Combined skill for generating, editing, and composing images using Google's Gemini API.
Covers blog images, diagrams, illustrations, product shots, portraits, and creative experiments.

## Trigger Conditions

Activate when the user asks to:
- Generate, create, or make an image / illustration / diagram
- Create a blog header, thumbnail, social media image, or banner
- Edit, modify, or transform an existing image
- Compose multiple images together
- Create variations of an image
- Generate a flowchart, architecture diagram, or technical visualization
- Create product photography, portraits, or creative renders

## Setup

```bash
pip install google-genai Pillow
export GEMINI_API_KEY=your-key   # or add to .env file
```

Scripts location: `.claude/skills/nanobanana-ultimate/scripts/`

## Quick Reference

### Models

| Shorthand | Model ID | Best For |
|-----------|----------|----------|
| `flash` | `gemini-2.5-flash-image` | Fast generation, iterations, batch (default) |
| `pro` | `gemini-3-pro-image-preview` | High quality, complex compositions, multi-image |

### Resolutions
`1K` (default, fast), `2K` (recommended for blog/content), `4K` (maximum quality)

### Aspect Ratios
`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Content Presets

| Preset | Aspect | Size | Use Case |
|--------|--------|------|----------|
| `blog` | 16:9 | 2K | Blog featured image (1200x630) |
| `youtube` | 16:9 | 2K | YouTube thumbnail (1280x720) |
| `social` | 1:1 | 1K | Social media square (1080x1080) |
| `story` | 9:16 | 2K | Instagram/TikTok story (1080x1920) |
| `og` | 16:9 | 2K | Open Graph / link preview |
| `banner` | 21:9 | 2K | Wide banner / hero image |

---

## Commands

### Generate (Text to Image)
```bash
python .claude/skills/nanobanana-ultimate/scripts/generate_image.py \
  "A professional blog header about tax tips with calculator and documents" \
  output.jpg --preset blog
```

Options: `--model flash|pro`, `--aspect 16:9`, `--size 2K`, `--preset blog|youtube|social|story|og|banner`, `--character clawd`

### Edit (Modify Existing Image)
```bash
python .claude/skills/nanobanana-ultimate/scripts/edit_image.py \
  input.jpg "Add a subtle gradient overlay and company logo in the corner" \
  output.jpg
```

Options: `--model flash|pro`, `--aspect`, `--size`

### Compose (Combine Multiple Images)
```bash
python .claude/skills/nanobanana-ultimate/scripts/compose_images.py \
  "Create a collage with consistent style" output.jpg img1.jpg img2.jpg img3.jpg
```

Supports up to **14 reference images**. Options: `--model pro` (recommended), `--aspect`, `--size`

### Multi-Turn Chat (Iterative Refinement)
```bash
python .claude/skills/nanobanana-ultimate/scripts/multi_turn_chat.py --output-dir ./images/
```

Interactive session — generate an image, then refine it through conversation. Commands: `/save`, `/load`, `/clear`, `/quit`

### Batch Generate (Multiple Variations)
```bash
python .claude/skills/nanobanana-ultimate/scripts/batch_generate.py \
  "Modern flat illustration of bookkeeping" ./variations/ --count 5 --preset blog
```

Options: `--count N` (1-20), `--prefix blog_`, `--delay 1.0`, `--preset`, `--model`, `--aspect`, `--size`

---

## Prompt Engineering

### Core Principles

1. **Specificity over brevity** — detailed prompts produce better results
2. **Technical language** — camera models, lens specs, lighting terms improve realism
3. **Progressive layering** — start simple, add detail iteratively
4. **JSON for complexity** — use structured JSON for multi-element scenes
5. **Negative prompts** — state what to avoid ("no text", "no watermark")

### Prompt Pattern Selection

| Complexity | Approach | When to Use |
|------------|----------|-------------|
| Simple | Text prompt | Single subject, straightforward style |
| Moderate | Hybrid (text + specs) | Some technical precision needed |
| Complex | JSON structure | Multiple elements, era aesthetics, precise specs |

### Simple Prompt Pattern
```
[Style/mood] + [Subject description] + [Environment] + [Technical specs] + [Quality markers]
```

Example:
```
Professional corporate photography of a modern office desk with laptop and coffee,
warm morning light from left window, shot on Sony A7III with 35mm f/2.8,
shallow depth of field, 4K resolution, clean minimal aesthetic
```

### JSON Prompt Pattern

For complex scenes — see `references/json-structure-guide.md` for full templates.

```json
{
  "subject": { "description": "..." },
  "photography": { "camera": "Sony A7III", "lens": "85mm f/1.4", "lighting": "..." },
  "background": { "setting": "...", "color": "#hex" },
  "negative_prompt": "text, watermark, blurry"
}
```

### Camera & Lighting Quick Reference

| Camera | Best For |
|--------|----------|
| Sony A7III | Portraits, general professional |
| Canon EOS R5 | Product, editorial |
| Hasselblad H6D | Macro, ultra-detail |
| Canon IXUS | Retro/2000s aesthetic |
| iPhone 16 | Casual, modern snapshot |

| Lens | Best For |
|------|----------|
| 85mm f/1.4 | Portraits (shallow DOF) |
| 35mm f/2.8 | Environmental, street |
| 50mm f/1.8 | General purpose |
| 12-18mm | Fisheye, ultra-wide |
| Macro | Extreme close-up, detail |

| Lighting | Mood |
|----------|------|
| Three-point studio | Professional, corporate |
| Golden hour | Warm, lifestyle |
| Harsh direct flash | Retro, Y2K, party |
| Dramatic side-light | Editorial, moody |
| Soft diffused | Product, e-commerce |

| Film Stock | Look |
|------------|------|
| Kodak Portra 400 | Warm, nostalgic, skin tones |
| Kodak Ektar 100 | Vibrant, saturated colors |
| Digital but mimicking film | Retro with digital sharpness |

---

## Identity Preservation

When editing photos of people, **state face preservation in the FIRST sentence**.

### Critical Phrases
- "Keep the facial features of the person in the uploaded image exactly consistent"
- "Preserve original face 100% accurate from reference image"

### JSON Pattern
```json
{ "face": { "preserve_original": true, "reference_match": true, "accuracy": "100%" } }
```

See `references/photorealism-portraits.md` for full identity preservation templates.

---

## Pattern Categories

Each category has a dedicated reference file with ready-to-use templates:

| Category | Reference File | Examples |
|----------|---------------|----------|
| Photorealism & Portraits | `references/photorealism-portraits.md` | Headshots, era aesthetics, identity preservation |
| Creative Experiments | `references/creative-experiments.md` | 3D renders, dioramas, surreal, split-view |
| Product & Commercial | `references/product-commercial.md` | E-commerce, luxury, editorial, data viz |
| Editing & Transformation | `references/editing-transformation.md` | Outpainting, bg removal, style transfer |
| JSON Structure Guide | `references/json-structure-guide.md` | JSON templates for complex prompts |

---

## Diagram Generation

For flowcharts, architecture diagrams, and technical visualizations:

### Flowchart
```
Clean technical flowchart diagram showing [process], white background,
rounded rectangle nodes with [color] fill, directional arrows between steps,
clear readable labels, professional infographic style, minimal design,
no decorative elements, 2K resolution
```

### Architecture Diagram
```
System architecture diagram of [system], boxes representing services/components,
arrows showing data flow, color-coded by layer (blue=frontend, green=api, orange=database),
clean sans-serif labels, white background, technical documentation style
```

### Comparison / Feature Grid
```
Clean comparison infographic of [items], table-style grid layout,
checkmarks and X marks, consistent icon style, brand colors [colors],
professional presentation quality, ready for blog or slides
```

**Tip:** For diagrams with text, keep labels SHORT (1-3 words per node). Gemini handles short text better than long labels.

---

## Blog Image Best Practices

1. **Use the `blog` preset** — 16:9 at 2K gives optimal blog header dimensions
2. **Avoid text in images** — Gemini struggles with text rendering; add text via HTML/CSS overlay instead
3. **Consistent branding** — include brand colors in prompts for visual consistency across posts
4. **Illustrative > literal** — abstract/illustrative images often look more professional than photorealistic for blog headers
5. **Batch generate** — create 3-5 variations and pick the best one
6. **Negative prompts** — always add `"no text, no watermark, no logo"` for clean blog images

### Blog Header Prompt Template
```
Professional blog header illustration about [topic], modern flat design style,
[brand color palette], clean composition with negative space for text overlay,
abstract geometric elements, subtle gradients, no text or words in the image,
16:9 aspect ratio, 2K resolution
```

---

## Advanced Features

### Search Grounding
The pro model can use Google Search to inform image generation for current events or real-world accuracy. This is handled automatically when the model detects it's needed.

### Multi-Turn Refinement
Use `multi_turn_chat.py` for iterative creation:
1. Generate initial image
2. "Make the sky more dramatic"
3. "Add warm lighting from the left"
4. "Zoom out to show more of the scene"
5. `/save final_version.jpg`

### Up to 14 Reference Images
`compose_images.py` supports combining up to 14 reference images — useful for:
- Style transfer from one image to another's content
- Combining elements from multiple sources
- Creating group compositions from individual portraits

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GEMINI_API_KEY not set" | `export GEMINI_API_KEY=your-key` or add to `.env` file |
| Safety filter blocks | Rephrase prompt — remove potentially sensitive terms |
| No image returned | Simplify the prompt; complex prompts sometimes fail silently |
| Rate limit (429) | Wait 60 seconds, or increase `--delay` for batch generation |
| Wrong colors/style | Be more specific — use hex codes, camera models, film stocks |
| Text in image looks bad | Avoid text in generated images; overlay text via HTML/CSS instead |
| JPEG format mismatch | Always use `.jpg` extension — Gemini returns JPEG by default |
| Inconsistent faces | Add identity preservation phrases at the START of the prompt |
| Batch failures | Some variations may fail safety filters — this is normal, re-run failed ones |

## File Format Note

**Always use `.jpg` extension for output files.** Gemini returns JPEG format by default. Using `.png` extension on JPEG data causes media type mismatch errors.
