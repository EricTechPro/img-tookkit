# JSON Prompt Structure Guide

## When to Use JSON Prompts

Use JSON-structured prompts when:
1. Multiple elements need detailed specification
2. Era-specific aesthetics (Y2K, 2000s, 1990s)
3. Complex scenes with multiple subjects
4. Precise technical camera/lens requirements
5. Multi-layered compositions (torn paper, split view, etc.)

**Simple prompts** work for: single subject, straightforward composition, basic style.

---

## Core JSON Structure

```json
{
  "subject": {
    "description": "Main subject details",
    "face": { "preserve_original": true }
  },
  "accessories": ["item 1", "item 2"],
  "photography": {
    "camera": "Camera model",
    "lens": "Lens spec",
    "lighting": "Lighting description",
    "iso": 400,
    "quality": "8K"
  },
  "background": {
    "setting": "Environment description",
    "color": "#hex or description"
  },
  "negative_prompt": "Things to avoid"
}
```

---

## Era-Specific Templates

### 2000s Mirror Selfie
```json
{
  "subject": {
    "description": "[person] taking mirror selfie",
    "face": { "preserve_original": true, "reference_match": true }
  },
  "photography": {
    "camera": "Canon IXUS / early digital compact",
    "flash": "harsh direct built-in flash",
    "quality": "2-3 megapixel aesthetic",
    "artifacts": ["slight overexposure from flash", "warm color cast", "digital noise"]
  },
  "scene": {
    "location": "bedroom mirror",
    "era_details": ["2000s room decor", "visible in mirror reflection"]
  },
  "negative_prompt": "modern phone, professional quality, studio lighting"
}
```

### Y2K Scrapbook Collage
```json
{
  "layout": "scrapbook collage of 6 photos",
  "subject": {
    "facelock_identity": true,
    "accuracy": "100%"
  },
  "multiple_poses": [
    "peace sign selfie",
    "full body casual",
    "laughing candid",
    "profile looking away",
    "mirror selfie",
    "hand on hip pose"
  ],
  "aesthetic": "Y2K scrapbook with stickers and decorative tape",
  "negative_prompt": "inconsistent face between photos, different person"
}
```

### 1990s Film Camera Aesthetic
```json
{
  "photography": {
    "camera": "Canon IXUS",
    "lens": "35mm equivalent f/2.8",
    "flash": "harsh direct flash",
    "iso": 400,
    "film": "digital but mimicking film color science"
  },
  "style": "late 90s / early 2000s snapshot",
  "quality_markers": ["slight noise", "flash falloff in background", "sharp center soft edges"]
}
```

---

## Complex Scene Templates

### Multi-Realm Surreal Composition
```json
{
  "scene": {
    "realm_physical": "Real-world element description",
    "realm_digital": "Digital/virtual element description",
    "surreal_bridge_event": "How the two realms connect (liquid flowing between, light merging, etc.)"
  },
  "photography": {
    "lighting": "dramatic side-lighting emphasizing transition",
    "focus": "sharp on the bridge point between realms",
    "quality": "8K ultra HD"
  }
}
```

### Fisheye / Wide Angle Portrait
```json
{
  "subject": "[subject description]",
  "lens": {
    "type": "12mm fisheye",
    "barrel_distortion": "heavy",
    "distortion_effects": [
      "face slightly stretched in center",
      "background curves dramatically at edges",
      "foreground objects appear oversized"
    ]
  },
  "composition": "subject in center, environment wrapping around frame edges",
  "effects": ["barrel distortion", "no phone visible in hands"]
}
```

---

## Advanced Editing Operations

### Torn Paper Effect
```json
{
  "effect": "torn paper art layers",
  "base_image": "[reference]",
  "tears": {
    "direction": "horizontal",
    "layers_revealed": [
      { "style": "line-art", "position": "top" },
      { "style": "watercolor", "position": "middle" },
      { "style": "pencil-drawing", "position": "bottom" }
    ],
    "paper_edges": "realistic torn white paper with cast shadow"
  },
  "subject_preservation": "same subject across all layers"
}
```

### Phone Screen Replacement
```json
{
  "base_image": "[person holding phone]",
  "screen_content": "[image to show on screen]",
  "edit_rules": {
    "screen_fitting": "perspective-correct to match screen angle",
    "reflection": "subtle glass reflection maintained",
    "brightness_match": true,
    "subject_unchanged": true
  }
}
```

---

## Technical Specification Templates

### Professional Portrait with Full Specs
```json
{
  "subject": {
    "description": "[person description]",
    "face": { "preserve_original": true }
  },
  "photography": {
    "camera": "Sony A7III",
    "lens": "85mm f/1.4",
    "lighting": "three-point studio setup (key, fill, rim)",
    "quality": "8K"
  },
  "background": {
    "color": "#562226",
    "style": "clean gradient"
  },
  "quality_markers": [
    "natural skin texture with visible pores",
    "crisp focus on eyes",
    "shallow depth of field",
    "clean cinematic color grading"
  ]
}
```

---

## Best Practices

1. **Validate JSON syntax** — use consistent indentation, proper commas
2. **Group related properties** — keep camera specs together, style specs together
3. **Use exact values** — hex color codes (#562226), specific camera models (Sony A7III)
4. **Include negative prompts** — explicitly state what to avoid
5. **Identity preservation first** — put face preservation rules at the top of the JSON
6. **Start simple, test** — begin with basic JSON, add complexity incrementally
7. **Hierarchical structure** — nest logically (photography > camera, lens, lighting)
