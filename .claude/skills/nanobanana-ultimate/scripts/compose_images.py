#!/usr/bin/env python3
"""
Compose multiple images into a new image using Gemini API.

Supports up to 14 reference images for multi-image composition.

Usage:
    python compose_images.py "instruction" output.jpg image1.jpg [image2.jpg ...]

Examples:
    python compose_images.py "Create a group photo of these people" group.jpg person1.jpg person2.jpg
    python compose_images.py "Put the cat from image 1 on the couch from image 2" result.jpg cat.jpg couch.jpg
    python compose_images.py "Apply the art style from image 1 to image 2" styled.jpg style.jpg photo.jpg
    python compose_images.py "Combine these product photos into a collage" collage.jpg *.jpg

Environment:
    GEMINI_API_KEY - Required API key (also checks .env file)
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
import sys
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types


MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


def load_env():
    """Load .env from the skill folder (next to scripts/), then cwd as fallback."""
    skill_env = Path(__file__).resolve().parent.parent / ".env"
    for env_path in [skill_env, Path.cwd() / ".env"]:
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


def get_output_dir() -> Path:
    """Get the nanobanana/ output folder at project root, creating if needed."""
    out = Path.cwd() / "nanobanana"
    out.mkdir(parents=True, exist_ok=True)
    return out


def auto_filename(prefix: str = "img") -> str:
    """Generate a timestamped filename like img_20260303_094512.jpg."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.jpg"


def resolve_model(model_arg: str) -> str:
    if model_arg in MODELS:
        return MODELS[model_arg]
    return model_arg


def compose_images(
    instruction: str,
    output_path: str,
    image_paths: list[str],
    model: str = "gemini-3-pro-image-preview",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
) -> str | None:
    """Compose multiple images into a new image.

    Args:
        instruction: Text description of how to combine the images.
        output_path: Path to save the composed image.
        image_paths: List of input image paths (1-14 images).
        model: Gemini model ID (pro recommended for multi-image).
        aspect_ratio: Output aspect ratio.
        image_size: Output resolution.

    Returns:
        Text response from the model, if any.
    """
    if len(image_paths) > 14:
        raise ValueError("Maximum 14 reference images supported by Gemini")
    if len(image_paths) < 1:
        raise ValueError("At least one image is required")

    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

    client = genai.Client(api_key=get_api_key())
    images = [Image.open(path) for path in image_paths]
    contents: list = [instruction] + images

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
        raise RuntimeError("No image was generated. Try simplifying the instruction or using fewer reference images.")

    return text_response


def main():
    parser = argparse.ArgumentParser(
        description="Compose multiple images using Gemini API (supports up to 14 reference images)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("instruction", help="How to combine the images")
    parser.add_argument("output", nargs="?", default=None, help="Output path (default: nanobanana/compose_TIMESTAMP.jpg)")
    parser.add_argument("images", nargs="+", help="Input image paths (1-14 images)")
    parser.add_argument(
        "--model", "-m",
        default="pro",
        help="Model: 'pro' (quality, default for composition), 'flash' (fast), or full model ID",
    )
    parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Output aspect ratio")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], help="Output resolution")

    args = parser.parse_args()
    model = resolve_model(args.model)
    output = args.output or str(get_output_dir() / auto_filename("compose"))

    try:
        text = compose_images(
            instruction=args.instruction,
            output_path=output,
            image_paths=args.images,
            model=model,
            aspect_ratio=args.aspect,
            image_size=args.size,
        )
        print(f"Composed image saved to: {output}")
        print(f"Reference images used: {len(args.images)}")
        if text:
            print(f"Model response: {text}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
