"""
Describe images from the VMware metrics book using Claude's vision.

For each image referenced in book_raw.md:
1. Find the surrounding text context (before and after the image)
2. Send the image + context to Claude for a concise description
3. Save descriptions to image_descriptions.json

This can be resumed — it skips already-described images.
"""

import anthropic
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()
import re
import time

BOOK_PATH = "book_raw.md"
IMAGES_DIR = "images"
DESCRIPTIONS_PATH = "image_descriptions.json"
MODEL = "claude-sonnet-4-6"


def get_media_type(filename: str) -> str:
    ext = filename.lower().rsplit(".", 1)[-1]
    return {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
        "bmp": "image/bmp",
    }.get(ext, "image/png")


def extract_image_contexts(book_path: str) -> list[dict]:
    """Extract each image reference with surrounding text context."""
    with open(book_path, "r") as f:
        lines = f.readlines()

    image_contexts = []
    pattern = re.compile(r"!\[([^\]]*)\]\(images/([^)]+)\)")

    for i, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            filename = match.group(2)
            # Get surrounding context: 15 lines before and after
            start = max(0, i - 15)
            end = min(len(lines), i + 16)
            context_before = "".join(lines[start:i]).strip()
            context_after = "".join(lines[i + 1 : end]).strip()

            image_contexts.append(
                {
                    "filename": filename,
                    "line": i + 1,
                    "context_before": context_before[-500:],  # Last 500 chars
                    "context_after": context_after[:500],  # First 500 chars
                }
            )

    return image_contexts


def describe_image(
    client: anthropic.Anthropic, filename: str, context_before: str, context_after: str
) -> str:
    """Get a description of an image using Claude vision."""
    image_path = os.path.join(IMAGES_DIR, filename)

    if not os.path.exists(image_path):
        return f"[Image file not found: {filename}]"

    # Skip very small images (likely icons/bullets)
    size = os.path.getsize(image_path)
    if size < 1000:
        return "[Small decorative image/icon]"

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    media_type = get_media_type(filename)

    prompt = f"""This image is from a technical book about VMware vSphere Metrics.

Text BEFORE the image:
{context_before}

Text AFTER the image:
{context_after}

Describe what this image shows in 1-3 sentences. Focus on:
- What data/metrics are displayed (chart values, metric names, trends)
- What the image demonstrates in the context of the surrounding text
- Any specific numbers or labels visible

Be concise and technical. If it's a screenshot of a dashboard or chart, describe the key data points."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"[Error describing image: {e}]"


def main():
    # Load existing descriptions
    if os.path.exists(DESCRIPTIONS_PATH):
        with open(DESCRIPTIONS_PATH, "r") as f:
            descriptions = json.load(f)
    else:
        descriptions = {}

    # Extract image contexts
    contexts = extract_image_contexts(BOOK_PATH)
    print(f"Found {len(contexts)} image references")
    print(f"Already described: {len(descriptions)}")

    # Filter to undescribed images
    todo = [c for c in contexts if c["filename"] not in descriptions]
    print(f"To describe: {len(todo)}")

    if not todo:
        print("All images already described!")
        return

    client = anthropic.Anthropic()

    for i, ctx in enumerate(todo):
        filename = ctx["filename"]
        print(f"  [{i+1}/{len(todo)}] {filename}...", end=" ", flush=True)

        desc = describe_image(
            client, filename, ctx["context_before"], ctx["context_after"]
        )
        descriptions[filename] = desc
        print(f"OK ({len(desc)} chars)")

        # Save after each image (resume-friendly)
        with open(DESCRIPTIONS_PATH, "w") as f:
            json.dump(descriptions, f, indent=2)

        # Rate limiting
        time.sleep(0.3)

    print(f"\nDone! {len(descriptions)} total descriptions saved to {DESCRIPTIONS_PATH}")


if __name__ == "__main__":
    main()
