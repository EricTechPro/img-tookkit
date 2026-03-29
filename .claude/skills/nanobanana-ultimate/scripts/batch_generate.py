#!/usr/bin/env python3
"""
Generate multiple image variations from a single prompt using Gemini API.

Generates N variations with sequential naming for easy comparison.

Usage:
    python batch_generate.py "prompt" output_dir/ [options]

Examples:
    python batch_generate.py "A modern logo for a bookkeeping app" ./logos/ --count 5
    python batch_generate.py "Blog header about tax tips" ./headers/ --count 3 --preset blog
    python batch_generate.py "Product photo of a notebook" ./products/ --count 4 --model pro --aspect 4:3

Output files are named: {output_dir}/001.jpg, 002.jpg, 003.jpg, ...

Environment:
    GEMINI_API_KEY - Required API key (also checks .env file)
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types


MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

PRESETS = {
    "blog": {"aspect_ratio": "16:9", "image_size": "2K"},
    "youtube": {"aspect_ratio": "16:9", "image_size": "2K"},
    "social": {"aspect_ratio": "1:1", "image_size": "1K"},
    "story": {"aspect_ratio": "9:16", "image_size": "2K"},
    "og": {"aspect_ratio": "16:9", "image_size": "2K"},
    "banner": {"aspect_ratio": "21:9", "image_size": "2K"},
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


def resolve_model(model_arg: str) -> str:
    if model_arg in MODELS:
        return MODELS[model_arg]
    return model_arg


def generate_single(
    client: genai.Client,
    prompt: str,
    output_path: str,
    model: str,
    aspect_ratio: str | None = None,
    image_size: str | None = None,
) -> bool:
    """Generate a single image. Returns True if successful."""
    config_kwargs: dict = {"response_modalities": ["IMAGE"]}

    image_config_kwargs: dict = {}
    if aspect_ratio:
        image_config_kwargs["aspectRatio"] = aspect_ratio
    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    config = types.GenerateContentConfig(**config_kwargs)

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=config,
    )

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                return True

    return False


def batch_generate(
    prompt: str,
    output_dir: str,
    count: int = 3,
    model: str = "gemini-2.5-flash-image",
    aspect_ratio: str | None = None,
    image_size: str | None = None,
    prefix: str = "",
    delay: float = 1.0,
) -> list[str]:
    """Generate multiple image variations.

    Args:
        prompt: Text description of the image.
        output_dir: Directory to save generated images.
        count: Number of variations to generate.
        model: Gemini model ID.
        aspect_ratio: Aspect ratio for all images.
        image_size: Resolution for all images.
        prefix: Optional filename prefix (e.g., "blog_").
        delay: Seconds to wait between API calls (rate limiting).

    Returns:
        List of paths to successfully generated images.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=get_api_key())
    generated: list[str] = []

    for i in range(1, count + 1):
        filename = f"{prefix}{i:03d}.jpg"
        filepath = str(out_path / filename)

        print(f"  [{i}/{count}] Generating {filename}...", end=" ", flush=True)

        try:
            success = generate_single(
                client=client,
                prompt=prompt,
                output_path=filepath,
                model=model,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            )
            if success:
                generated.append(filepath)
                print("done")
            else:
                print("no image returned (safety filter?)")
        except Exception as e:
            print(f"error: {e}")

        # Rate limit delay between requests (skip after last)
        if i < count and delay > 0:
            time.sleep(delay)

    return generated


def main():
    parser = argparse.ArgumentParser(
        description="Generate multiple image variations from a prompt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", help="Text description of the image")
    parser.add_argument("output_dir", nargs="?", default="nanobanana", help="Output directory (default: nanobanana/)")
    parser.add_argument("--count", "-n", type=int, default=3, help="Number of variations (default: 3)")
    parser.add_argument(
        "--model", "-m",
        default="flash",
        help="Model: 'flash' (fast, default), 'pro' (quality), or full model ID",
    )
    parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Aspect ratio")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], help="Resolution")
    parser.add_argument(
        "--preset", "-p",
        choices=list(PRESETS.keys()),
        help="Content preset (sets aspect ratio and resolution)",
    )
    parser.add_argument("--prefix", default="", help="Filename prefix (e.g., 'blog_')")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between API calls (default: 1.0)")

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

    if args.count < 1 or args.count > 20:
        print("Error: count must be between 1 and 20", file=sys.stderr)
        sys.exit(1)

    print(f"Generating {args.count} variations...")
    print(f"  Model: {model}")
    print(f"  Aspect: {aspect or 'default (1:1)'}")
    print(f"  Size: {size or 'default (1K)'}")
    print(f"  Output: {args.output_dir}/")
    print()

    generated = batch_generate(
        prompt=args.prompt,
        output_dir=args.output_dir,
        count=args.count,
        model=model,
        aspect_ratio=aspect,
        image_size=size,
        prefix=args.prefix,
        delay=args.delay,
    )

    print(f"\nGenerated {len(generated)}/{args.count} images:")
    for path in generated:
        print(f"  {path}")


if __name__ == "__main__":
    main()
