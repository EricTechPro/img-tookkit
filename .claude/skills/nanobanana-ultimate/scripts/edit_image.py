#!/usr/bin/env python3
"""
Edit existing images using Gemini API.

Usage:
    python edit_image.py input.jpg "edit instruction" output.jpg [options]

Examples:
    python edit_image.py photo.jpg "Add a rainbow in the sky" edited.jpg
    python edit_image.py room.jpg "Change the sofa to red leather" room_edited.jpg
    python edit_image.py portrait.jpg "Make it look like a Van Gogh painting" artistic.jpg --model pro

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


def edit_image(
    input_path: str,
    instruction: str,
    output_path: str,
    model: str = "gemini-2.5-flash-image",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
) -> str | None:
    """Edit an existing image using a text instruction.

    Args:
        input_path: Path to the source image.
        instruction: Text description of the edit to apply.
        output_path: Path to save the edited image.
        model: Gemini model ID.
        aspect_ratio: Output aspect ratio.
        image_size: Output resolution.

    Returns:
        Text response from the model, if any.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    client = genai.Client(api_key=get_api_key())
    input_image = Image.open(input_path)

    config_kwargs: dict = {"response_modalities": ["IMAGE"]}
    image_config_kwargs: dict = {}
    if aspect_ratio:
        image_config_kwargs["aspectRatio"] = aspect_ratio
    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    config = types.GenerateContentConfig(**config_kwargs)

    response = client.models.generate_content(
        model=model,
        contents=[instruction, input_image],
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
        raise RuntimeError(
            "No image was generated. The edit instruction may have been blocked by safety filters. "
            "Try rephrasing the instruction."
        )

    return text_response


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input image path")
    parser.add_argument("instruction", help="Edit instruction")
    parser.add_argument("output", nargs="?", default=None, help="Output path (default: nanobanana/edit_TIMESTAMP.jpg)")
    parser.add_argument(
        "--model", "-m",
        default="flash",
        help="Model: 'flash' (fast, default), 'pro' (quality), or full model ID",
    )
    parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Output aspect ratio")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], help="Output resolution")

    args = parser.parse_args()
    model = resolve_model(args.model)
    output = args.output or str(get_output_dir() / auto_filename("edit"))

    try:
        text = edit_image(
            input_path=args.input,
            instruction=args.instruction,
            output_path=output,
            model=model,
            aspect_ratio=args.aspect,
            image_size=args.size,
        )
        print(f"Edited image saved to: {output}")
        if text:
            print(f"Model response: {text}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
