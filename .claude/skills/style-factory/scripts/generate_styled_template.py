#!/usr/bin/env python3
"""
Generate images in a learned visual style using reference images and a style profile.

This script is part of a style skill created by the style-factory.
It loads reference images and a style profile from its own folder,
then generates new images that match the learned style.

Usage:
    python generate_styled.py "description of what to generate" output.jpg
    python generate_styled.py "blog header about Q4 results" header.jpg --preset blog
    python generate_styled.py "product launch announcement" social.jpg --preset social
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types


MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]

PRESETS = {
    "blog": {"aspect_ratio": "16:9", "image_size": "2K"},
    "youtube": {"aspect_ratio": "16:9", "image_size": "2K"},
    "social": {"aspect_ratio": "1:1", "image_size": "1K"},
    "story": {"aspect_ratio": "9:16", "image_size": "2K"},
    "og": {"aspect_ratio": "16:9", "image_size": "2K"},
    "banner": {"aspect_ratio": "21:9", "image_size": "2K"},
}


def load_env():
    """Load .env from the skill folder (next to scripts/), then nanobanana-ultimate, then cwd."""
    skill_env = Path(__file__).resolve().parent.parent / ".env"
    nanobanana_env = Path(__file__).resolve().parent.parent.parent / "nanobanana-ultimate" / ".env"
    for env_path in [skill_env, nanobanana_env, Path.cwd() / ".env"]:
        try:
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = value
        except FileNotFoundError:
            pass


def get_api_key() -> str:
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not set. Either:\n"
            "  1. export GEMINI_API_KEY=your-key\n"
            "  2. Add GEMINI_API_KEY=your-key to .env file"
        )
    return api_key


def get_skill_dir() -> Path:
    """Get the skill's root directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def load_style_profile() -> dict:
    """Load the style profile JSON from the skill's references folder."""
    profile_path = get_skill_dir() / "references" / "style_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"Style profile not found: {profile_path}")
    with open(profile_path) as f:
        return json.load(f)


def load_reference_images() -> list[tuple[str, Image.Image]]:
    """Load all ref_*.jpg images from the skill's references folder."""
    refs_dir = get_skill_dir() / "references"
    ref_paths = sorted(refs_dir.glob("ref_*.jpg"))
    if not ref_paths:
        raise FileNotFoundError(f"No reference images (ref_*.jpg) found in {refs_dir}")
    return [(str(p), Image.open(p)) for p in ref_paths]


def build_style_prompt(user_prompt: str, profile: dict) -> str:
    """Construct a style-aware prompt combining the style profile with the user's request."""
    style_desc = profile.get("style_summary", "")
    mood = profile.get("mood", "")
    rendering = profile.get("rendering_style", "")
    lighting = profile.get("lighting", "")

    colors = profile.get("color_palette", {})
    dominant = ", ".join(colors.get("dominant_colors", []))
    accent = ", ".join(colors.get("accent_colors", []))

    composition = profile.get("composition", {})
    layout = composition.get("layout", "")
    whitespace = composition.get("whitespace", "")

    elements = ", ".join(profile.get("visual_elements", []))
    negatives = profile.get("negative_characteristics", [])
    neg_str = ". Avoid: " + ", ".join(negatives) if negatives else ""

    prompt = (
        f"Generate an image that exactly matches the visual style shown in the reference images. "
        f"Style: {style_desc} "
        f"Mood: {mood}. Rendering: {rendering}. Lighting: {lighting}. "
        f"Color palette: dominant colors {dominant}, accent colors {accent}. "
        f"Composition: {layout} layout, {whitespace} whitespace. "
        f"Visual elements: {elements}{neg_str}. "
        f"\n\nContent to depict: {user_prompt}"
    )
    return prompt


def get_output_dir() -> Path:
    """Get the nanobanana/ output folder at project root, creating if needed."""
    out = Path.cwd() / "nanobanana"
    out.mkdir(parents=True, exist_ok=True)
    return out


def auto_filename(style_name: str) -> str:
    """Generate a timestamped filename."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = style_name.replace(" ", "_").replace("-", "_")
    return f"{safe_name}_{ts}.jpg"


def resolve_model(model_arg: str) -> str:
    if model_arg in MODELS:
        return MODELS[model_arg]
    return model_arg


def generate_styled(
    user_prompt: str,
    output_path: str,
    model: str = "gemini-3-pro-image-preview",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
) -> str | None:
    """Generate an image in the learned style.

    Args:
        user_prompt: What content to depict.
        output_path: Where to save the generated image.
        model: Gemini model to use.
        aspect_ratio: Output aspect ratio.
        image_size: Output resolution.

    Returns:
        Text response from the model, if any.
    """
    profile = load_style_profile()
    ref_images = load_reference_images()

    styled_prompt = build_style_prompt(user_prompt, profile)

    client = genai.Client(api_key=get_api_key())

    # Build contents: instruction first, then all reference images
    contents: list = [styled_prompt] + [img for _, img in ref_images]

    config_kwargs: dict = {"response_modalities": ["IMAGE"]}
    image_config_kwargs: dict = {}
    if aspect_ratio:
        image_config_kwargs["aspectRatio"] = aspect_ratio
    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    config = types.GenerateContentConfig(**config_kwargs)

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    text_response = None
    image_saved = False

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_response = part.text
            elif part.inline_data is not None:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                image_saved = True

    if not image_saved:
        raise RuntimeError("No image was generated. Try simplifying the prompt.")

    return text_response


def main():
    profile = load_style_profile()
    style_name = profile.get("style_name", "styled")

    parser = argparse.ArgumentParser(
        description=f"Generate images in {style_name} style",
    )
    parser.add_argument("prompt", help="Content description for the image")
    parser.add_argument("output", nargs="?", default=None, help="Output path (default: nanobanana/{style}_TIMESTAMP.jpg)")
    parser.add_argument("--model", "-m", default="pro", help="Model: 'pro' (default), 'flash', or full ID")
    parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Output aspect ratio")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], help="Output resolution")
    parser.add_argument("--preset", "-p", choices=list(PRESETS.keys()), help="Content preset")

    args = parser.parse_args()

    model = resolve_model(args.model)
    aspect = args.aspect
    size = args.size

    if args.preset:
        preset = PRESETS[args.preset]
        aspect = aspect or preset.get("aspect_ratio")
        size = size or preset.get("image_size")

    output = args.output or str(get_output_dir() / auto_filename(style_name))

    try:
        ref_images = load_reference_images()
        text = generate_styled(
            user_prompt=args.prompt,
            output_path=output,
            model=model,
            aspect_ratio=aspect,
            image_size=size,
        )
        print(f"Styled image saved to: {output}")
        print(f"Style: {style_name}")
        print(f"Reference images: {len(ref_images)}")
        if text:
            print(f"Model response: {text}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
