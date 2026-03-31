#!/usr/bin/env python3
"""
Analyze reference images to extract a structured style profile using Gemini API.

Sends images with TEXT response mode to get a JSON style profile describing
the visual language: colors, composition, mood, rendering style, etc.

Usage:
    python analyze_style.py --name "acme-brand" --output profile.json ref1.jpg ref2.jpg ...
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types


def load_env():
    """Load .env from the skill folder (next to scripts/), then cwd as fallback."""
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


ANALYSIS_PROMPT = """Analyze these reference images and extract a structured style profile as JSON.

Examine the visual language across all images: colors, composition patterns, mood, rendering technique, recurring visual elements, lighting, and any typography characteristics.

Return ONLY valid JSON in this exact structure (no markdown code fences, just raw JSON):

{
  "style_name": "%STYLE_NAME%",
  "style_summary": "2-3 sentence description of the overall visual language that could be used as a generation prompt prefix",
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
  "mood": "professional | playful | moody | energetic | minimal | luxurious | etc",
  "rendering_style": "photorealistic | flat illustration | 3D render | watercolor | vector | mixed media | etc",
  "visual_elements": ["list of recurring motifs, shapes, patterns, textures found across images"],
  "lighting": "soft diffused | dramatic | studio | natural | neon | etc",
  "typography_hints": "serif | sans-serif | handwritten | monospace | none (if no text in refs)",
  "negative_characteristics": ["things explicitly absent across all images - e.g., no gradients, no drop shadows, no borders"]
}

Be specific and precise. Use actual hex color codes from the images. The style_summary should be detailed enough to guide image generation."""


def analyze_style(
    style_name: str,
    image_paths: list[str],
    output_path: str,
    model: str = "gemini-3-pro-image-preview",
) -> dict:
    """Analyze reference images and return a style profile.

    Args:
        style_name: Name for this style.
        image_paths: Paths to reference images (1-8 recommended).
        output_path: Where to save the JSON profile.
        model: Gemini model to use for analysis.

    Returns:
        The parsed style profile dict.
    """
    if len(image_paths) > 14:
        raise ValueError("Maximum 14 reference images supported")
    if len(image_paths) < 1:
        raise ValueError("At least one reference image is required")

    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

    client = genai.Client(api_key=get_api_key())
    images = [Image.open(path) for path in image_paths]

    prompt = ANALYSIS_PROMPT.replace("%STYLE_NAME%", style_name)
    contents: list = [prompt] + images

    config = types.GenerateContentConfig(
        response_modalities=["TEXT"],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    text = None
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text = part.text
                break

    if not text:
        raise RuntimeError("No text response from model. Try with fewer images.")

    # Clean up response - strip markdown fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # Remove opening fence (```json or ```)
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    profile = json.loads(cleaned)

    # Save to file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(profile, f, indent=2)

    print(f"Style profile saved to: {output_path}")
    print(f"Reference images analyzed: {len(image_paths)}")
    print(f"\nStyle Summary: {profile.get('style_summary', 'N/A')}")
    print(f"Mood: {profile.get('mood', 'N/A')}")
    print(f"Rendering: {profile.get('rendering_style', 'N/A')}")

    return profile


def main():
    parser = argparse.ArgumentParser(
        description="Analyze reference images to extract a style profile",
    )
    parser.add_argument("images", nargs="+", help="Reference image paths")
    parser.add_argument("--name", "-n", required=True, help="Style name")
    parser.add_argument(
        "--output", "-o",
        default="style_profile.json",
        help="Output JSON path (default: style_profile.json)",
    )
    parser.add_argument(
        "--model", "-m",
        default="gemini-3-pro-image-preview",
        help="Gemini model (default: pro)",
    )

    args = parser.parse_args()

    try:
        profile = analyze_style(
            style_name=args.name,
            image_paths=args.images,
            output_path=args.output,
            model=args.model,
        )
        print("\n--- Full Profile ---")
        print(json.dumps(profile, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing model response as JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
