#!/usr/bin/env python3
"""
Interactive multi-turn image generation and refinement using Gemini API.

Enables iterative image creation through a conversational interface.
Generate an image, then refine it through follow-up instructions.

Usage:
    python multi_turn_chat.py [--model MODEL] [--output-dir DIR]

Commands during chat:
    /save [filename]  - Save current image
    /load <path>      - Load an image into the conversation
    /clear            - Start fresh conversation
    /quit             - Exit

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


def load_env():
    """Load .env from the skill folder (next to scripts/), then cwd as fallback."""
    skill_env = Path(__file__).resolve().parent.parent / ".env"
    for env_path in [skill_env, Path.cwd() / ".env"]:
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


class ImageChat:
    """Multi-turn chat session for iterative image generation."""

    def __init__(self, model: str = "gemini-2.5-flash-image", output_dir: str = "."):
        self.client = genai.Client(api_key=get_api_key())
        self.model = model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chat = None
        self.current_image: Image.Image | None = None
        self.image_count = 0
        self._init_chat()

    def _init_chat(self):
        config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
        self.chat = self.client.chats.create(model=self.model, config=config)
        self.current_image = None

    def send_message(self, message: str, image: Image.Image | None = None) -> tuple[str | None, Image.Image | None]:
        """Send a message and optionally an image, get text and/or image back."""
        contents: list = []
        if message:
            contents.append(message)
        if image:
            contents.append(image)
        if not contents:
            return None, None

        response = self.chat.send_message(contents)

        text_response = None
        image_response = None
        for part in response.parts:
            if part.text is not None:
                text_response = part.text
            elif part.inline_data is not None:
                image_response = part.as_image()
                self.current_image = image_response

        return text_response, image_response

    def save_image(self, filename: str | None = None) -> str | None:
        """Save the current image to disk."""
        if self.current_image is None:
            return None
        if filename is None:
            self.image_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}_{self.image_count}.jpg"
        filepath = self.output_dir / filename
        self.current_image.save(filepath)
        return str(filepath)

    def load_image(self, path: str) -> Image.Image:
        """Load an image from disk into the conversation."""
        img = Image.open(path)
        self.current_image = img
        return img


def main():
    parser = argparse.ArgumentParser(
        description="Interactive multi-turn image generation with Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--model", "-m",
        default="flash",
        help="Model: 'flash' (fast, default), 'pro' (quality), or full model ID",
    )
    parser.add_argument("--output-dir", "-o", default="nanobanana", help="Directory to save images (default: nanobanana/)")

    args = parser.parse_args()
    model = resolve_model(args.model)

    try:
        chat = ImageChat(model=model, output_dir=args.output_dir)
    except Exception as e:
        print(f"Error initializing: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Gemini Image Chat ({model})")
    print("Commands: /save [name], /load <path>, /clear, /quit")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None

            if cmd == "/quit":
                print("Goodbye!")
                break
            elif cmd == "/clear":
                chat._init_chat()
                print("Conversation cleared.")
            elif cmd == "/save":
                path = chat.save_image(arg)
                print(f"Image saved to: {path}" if path else "No image to save.")
            elif cmd == "/load":
                if not arg:
                    print("Usage: /load <path>")
                else:
                    try:
                        chat.load_image(arg)
                        print(f"Loaded: {arg}")
                    except Exception as e:
                        print(f"Error loading image: {e}")
            else:
                print(f"Unknown command: {cmd}")
            continue

        try:
            # Include current image in first message if loaded
            image_to_send = None
            if chat.current_image and not chat.chat._curated_history:
                image_to_send = chat.current_image

            text, image = chat.send_message(user_input, image_to_send)
            if text:
                print(f"\nGemini: {text}")
            if image:
                path = chat.save_image()
                print(f"\n[Image generated: {path}]")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
