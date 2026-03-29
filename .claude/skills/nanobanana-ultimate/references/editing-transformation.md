# Editing & Transformation Reference

## Smart Outpainting (Composition Rescue)

### Expand to Different Aspect Ratio
```
Expand this [portrait/square] image to [landscape/16:9/wider] aspect ratio,
seamlessly extending the scene on [left/right/both sides], match existing
lighting, weather, and texture perfectly, logical continuation of the
environment, no visible seam lines, maintain original image quality
```

**Key rules for outpainting:**
- Match lighting direction and intensity
- Continue textures seamlessly (grass, sky, wall, etc.)
- Complete any objects that were cut off logically
- Maintain consistent color temperature
- No clone stamp artifacts

---

## Background Removal & Replacement

### Smart Crowd/Tourist Removal
```
Remove all people/tourists from this photo, fill the empty spaces with
intelligent continuation of the environment (cobblestone, grass, trees,
building facades), maintain consistent lighting and perspective,
no clone stamp artifacts, seamless result
```

### Background Replacement
```
Keep the subject exactly as they appear, replace the background with
[new background description], match lighting direction to original
(light coming from [left/right/above]), natural edge quality between
subject and new background, consistent depth of field, matching
color temperature
```

**Critical for background replacement:**
- Subject preservation is #1 priority
- Lighting consistency (direction, color temp, intensity)
- Edge quality (no halos, no hard cutoff)
- Depth & perspective match
- Shadow consistency

---

## Style Transfer (Identity Preserved)

### Transform to Different Art Style
```
Transform this photo into [art style] while keeping the person's face
100% recognizable. Preserve exact facial features, only change the
artistic rendering style.
```

**Supported styles:**
- 3D cartoon (Pixar/Disney style)
- Anime/manga
- Oil painting (classical)
- Watercolor
- Pixel art
- Comic book / pop art
- Pencil sketch
- Art nouveau

**Critical:** Always state identity preservation FIRST, then style transformation.

---

## Aspect Ratio & Format Changes

### Portrait to Landscape
```
Convert this portrait (vertical) image to landscape (horizontal) format,
keep the center subject preserved exactly, extend the scene on both sides
with logical continuation (if indoor: continue room/walls, if outdoor:
continue landscape/sky), seamless integration, no visible boundaries
```

---

## Torn Paper Art Effect (JSON)
```json
{
  "effect": "torn paper revealing art layers",
  "base_image": "[reference photo]",
  "tears": {
    "direction": "horizontal tears across image",
    "layers_revealed": [
      { "style": "line-art", "position": "top tear" },
      { "style": "sumi-e ink wash", "position": "upper-middle" },
      { "style": "watercolor", "position": "lower-middle" },
      { "style": "pencil-drawing", "position": "lower tear" },
      { "style": "colored-pencil", "position": "bottom" }
    ],
    "paper_edges": "realistic torn white paper edges with shadow"
  },
  "subject_preservation": "same subject visible in each layer, just different art style"
}
```

---

## Coordinate Visualization

### GPS to Scene
```
Photorealistic scene at GPS coordinates [lat, long] at [time of day],
accurate architectural and landscape features for that location,
[weather conditions], street-level perspective, golden hour lighting
(or as specified), 4K resolution
```

---

## Face Detection CCTV Simulation
```
CCTV security camera footage of [scene], high angle mounted camera
perspective, noisy/grainy distorted quality, white bounding boxes
around detected faces, corner zoom inset showing enlarged view of
most prominent face, no text overlays except bounding boxes,
timestamp overlay in corner, black and white or desaturated color
```

---

## Wide Angle Phone Screen Replacement (JSON)
```json
{
  "base_image": "[person holding phone photo]",
  "screen_content": "[second reference image]",
  "photography": {
    "lens": "ultra-wide angle 12-18mm",
    "perspective": "exaggerated wide-angle distortion"
  },
  "edit_rules": {
    "screen_fitting": "perspective-correct transform to match phone screen shape exactly",
    "reflection": "subtle screen glass reflection maintained",
    "brightness": "screen content brightness matches ambient lighting",
    "subject_preservation": "person and phone position unchanged"
  }
}
```

---

## Tips for Good Edits

1. **Be specific about what to change** — vague instructions get vague results
2. **State what to preserve** — explicitly mention what should NOT change
3. **Match the lighting** — describe the lighting direction in your instruction
4. **One edit at a time** — complex multi-edits often fail; chain simple edits instead
5. **Use the pro model** for complex edits requiring high fidelity
