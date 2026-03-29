# Photorealism & Portraits Reference

## Identity Preservation

**Critical:** When editing photos of people, state face preservation in the FIRST sentence.

### Essential Phrases
- "Keep the facial features of the person in the uploaded image exactly consistent"
- "Preserve original face 100% accurate from reference image"
- "Maintain exact facial identity throughout the transformation"

### JSON Pattern
```json
{
  "face": {
    "preserve_original": true,
    "reference_match": true,
    "accuracy": "100%"
  }
}
```

### What Can Change
- Background, lighting, clothing, pose, style
- Hair color/style (with explicit instruction)
- Age appearance (with explicit instruction)

### What Must NOT Change
- Facial bone structure, eye shape/color, nose shape
- Unique identifying features (moles, dimples, scars)

---

## Templates

### Professional Headshot
```
Professional corporate headshot of [subject], shot on Sony A7III with 85mm f/1.4 lens,
three-point studio lighting setup, shallow depth of field, clean [#color] background,
natural skin texture with visible pores, crisp focus on eyes, 8K ultra HD,
clean cinematic color grading
```

### 2000s Mirror Selfie (JSON)
```json
{
  "subject": {
    "description": "[subject description]",
    "face": { "preserve_original": true, "reference_match": true }
  },
  "photography": {
    "style": "early 2000s digital camera",
    "camera": "Canon IXUS",
    "flash": "harsh direct built-in flash",
    "quality": "2-3 megapixel look",
    "artifacts": ["slight overexposure from flash", "warm color cast"]
  },
  "scene": {
    "location": "bedroom mirror selfie",
    "era_details": ["visible in mirror reflection", "2000s room decor"]
  },
  "negative_prompt": "modern phone, high quality, professional lighting"
}
```

### 1990s Camera Flash Portrait
```
[Subject] photographed with 35mm film camera, direct flash creating harsh
front-lighting, slight red-eye effect, warm nostalgic color temperature,
visible film grain (ISO 400), slightly soft focus, amateur composition,
Kodak Gold 200 color palette
```

### Kodak Portra 400 Style
```
[Subject] shot on Kodak Portra 400 film, warm nostalgic tones, golden hour
side-lighting, 35mm film camera, natural film grain, slightly lifted blacks,
warm skin tones, soft bokeh background, analog photography aesthetic
```

### Harsh Flash Photography (JSON)
```json
{
  "subject": { "description": "[subject]" },
  "photography": {
    "camera": "Canon IXUS 400",
    "lens": "built-in 35mm equivalent f/2.8",
    "flash": "harsh direct pop-up flash",
    "iso": 400,
    "quality_markers": ["slight noise", "flash falloff in background", "sharp in center"]
  },
  "style": "early digital compact camera aesthetic"
}
```

### Multiple Pose Y2K Scrapbook (JSON)
```json
{
  "layout": "scrapbook collage of 6 photos",
  "subject": {
    "facelock_identity": true,
    "accuracy": "100%"
  },
  "multiple_poses": [
    "peace sign close-up selfie",
    "full body casual lean",
    "laughing candid",
    "looking away profile",
    "mirror selfie",
    "group pose with hand on hip"
  ],
  "aesthetic": "Y2K scrapbook with stickers and decorative elements",
  "negative_prompt": "inconsistent face, different person in each photo"
}
```

### Fisheye / Wide Angle Selfie
```
[Subject] extreme close-up selfie with 12mm fisheye lens, exaggerated barrel
distortion, nose appears larger, background curves at edges, fun playful
perspective, sharp focus on face, environmental distortion visible,
no phone visible in hands
```

### Character Consistency Selfie
```
[Subject] taking a selfie with [celebrity/character], same lighting on both
subjects, consistent perspective, matching skin tone warmth, unified
composition, both in sharp focus, casual arm-around-shoulder pose
```

---

## Quality Markers

Use these to boost photorealism:
- `8K ultra HD` / `4K resolution`
- `natural skin texture with visible pores`
- `crisp focus on eyes`
- `shallow depth of field`
- `clean cinematic color grading`
- `natural rim lighting`
- `film grain` (for analog looks)
- `sharp detail in fabric texture`
