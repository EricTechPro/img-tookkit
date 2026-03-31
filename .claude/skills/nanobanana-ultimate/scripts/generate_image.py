#!/usr/bin/env python3
"""
Generate images from text prompts using Gemini API.

Usage:
    python generate_image.py "prompt" output.jpg [options]

Examples:
    python generate_image.py "A cat in space" cat.jpg
    python generate_image.py "Epic landscape" landscape.jpg --aspect 16:9 --size 2K
    python generate_image.py "Blog header about taxes" header.jpg --preset blog
    python generate_image.py "Product shot" product.jpg --model pro --aspect 4:3

Presets:
    blog      - Blog featured image (1200x630, 16:9)
    youtube   - YouTube thumbnail (1280x720, 16:9)
    social    - Social media square (1080x1080, 1:1)
    story     - Story/Reel format (1080x1920, 9:16)
    og        - Open Graph image (1200x630, 16:9)
    banner    - Wide banner (21:9)

Environment:
    GEMINI_API_KEY - Required API key (also checks .env file)
"""

from __future__ import annotations

import argparse
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

PRESETS = {
    "blog": {"aspect_ratio": "16:9", "image_size": "2K", "description": "Blog featured image (1200x630)"},
    "youtube": {"aspect_ratio": "16:9", "image_size": "2K", "description": "YouTube thumbnail (1280x720)"},
    "social": {"aspect_ratio": "1:1", "image_size": "1K", "description": "Social media square (1080x1080)"},
    "story": {"aspect_ratio": "9:16", "image_size": "2K", "description": "Story/Reel vertical (1080x1920)"},
    "og": {"aspect_ratio": "16:9", "image_size": "2K", "description": "Open Graph image (1200x630)"},
    "banner": {"aspect_ratio": "21:9", "image_size": "2K", "description": "Wide banner"},
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


def load_env():
    """Load .env from the skill folder (next to scripts/), then cwd as fallback."""
    skill_env = Path(__file__).resolve().parent.parent / ".env"
    for env_path in [skill_env, Path.cwd() / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = value


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


def get_characters_dir() -> Path:
    """Get the characters directory at project root."""
    return Path.cwd() / "sample" / "characters"


def load_character_images(character_name: str) -> list[Image.Image]:
    """Load all images for a named character from sample/characters/{name}/."""
    char_dir = get_characters_dir() / character_name
    if not char_dir.exists():
        available = [d.name for d in get_characters_dir().iterdir() if d.is_dir()] if get_characters_dir().exists() else []
        raise FileNotFoundError(
            f"Character '{character_name}' not found in {get_characters_dir()}. "
            f"Available characters: {', '.join(available) or 'none'}"
        )
    img_paths = sorted(
        p for p in char_dir.iterdir()
        if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
    )
    if not img_paths:
        raise FileNotFoundError(f"No images found in {char_dir}")
    return [Image.open(p) for p in img_paths]


def generate_image(
    prompt: str,
    output_path: str,
    model: str = "gemini-2.5-flash-image",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
    characters: list[str] | None = None,
) -> str | None:
    """Generate an image from a text prompt.

    Args:
        prompt: Text description of the image to generate.
        output_path: Path to save the generated image.
        model: Gemini model ID.
        aspect_ratio: Aspect ratio (e.g., "16:9", "1:1").
        image_size: Resolution ("1K", "2K", or "4K").
        characters: List of character names to include as reference images.

    Returns:
        Text response from the model, if any.
    """
    client = genai.Client(api_key=get_api_key())

    # Load character reference images
    char_images: list[Image.Image] = []
    if characters:
        for char_name in characters:
            char_images.extend(load_character_images(char_name))
        char_names = ", ".join(characters)
        prompt += (
            f"\n\nIMPORTANT: The following reference images show the character(s) '{char_names}'. "
            f"Use these as exact visual reference for how the character should look in the generated image. "
            f"Preserve the character's visual identity (colors, shape, proportions) accurately."
        )

    config_kwargs: dict = {"response_modalities": ["IMAGE"]}

    image_config_kwargs: dict = {}
    if aspect_ratio:
        image_config_kwargs["aspectRatio"] = aspect_ratio
    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    config = types.GenerateContentConfig(**config_kwargs)

    contents: list = [prompt] + char_images

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
                image = part.inline_data
                # Save image data
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image.data)
                image_saved = True

    if not image_saved:
        raise RuntimeError(
            "No image was generated. The prompt may have been blocked by safety filters. "
            "Try rephrasing or simplifying the prompt."
        )

    return text_response


def get_output_dir() -> Path:
    """Get the nanobanana/ output folder at project root, creating if needed."""
    out = Path.cwd() / "nanobanana"
    out.mkdir(parents=True, exist_ok=True)
    return out


def auto_filename(prefix: str = "gen") -> str:
    """Generate a timestamped filename like gen_20260303_094512.jpg."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.jpg"


def resolve_model(model_arg: str) -> str:
    """Resolve model shorthand to full model ID."""
    if model_arg in MODELS:
        return MODELS[model_arg]
    return model_arg


def main():
    parser = argparse.ArgumentParser(
        description="Generate images from text prompts using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Presets:\n" + "\n".join(f"  {k:10s} - {v['description']}" for k, v in PRESETS.items()),
    )
    parser.add_argument("prompt", help="Text description of the image")
    parser.add_argument("output", nargs="?", default=None, help="Output file path (default: nanobanana/gen_TIMESTAMP.jpg)")
    parser.add_argument(
        "--model", "-m",
        default="flash",
        help="Model: 'flash' (fast, default), 'pro' (quality), or full model ID",
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=ASPECT_RATIOS,
        help="Aspect ratio (overrides preset)",
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1K", "2K", "4K"],
        help="Resolution (overrides preset)",
    )
    parser.add_argument(
        "--preset", "-p",
        choices=list(PRESETS.keys()),
        help="Content preset (sets aspect ratio and resolution)",
    )
    parser.add_argument(
        "--character", "-c",
        action="append",
        help="Character name(s) to include as visual reference (from sample/characters/). Can be repeated.",
    )

    args = parser.parse_args()

    # Apply preset defaults, then allow overrides
    aspect = args.aspect
    size = args.size
    if args.preset:
        preset = PRESETS[args.preset]
        if not aspect:
            aspect = preset["aspect_ratio"]
        if not size:
            size = preset["image_size"]

    model = resolve_model(args.model)
    output = args.output or str(get_output_dir() / auto_filename("gen"))

    try:
        text = generate_image(
            prompt=args.prompt,
            output_path=output,
            model=model,
            aspect_ratio=aspect,
            image_size=size,
            characters=args.character,
        )
        print(f"Image saved to: {output}")
        if args.character:
            print(f"Character references: {', '.join(args.character)}")
        if text:
            print(f"Model response: {text}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
