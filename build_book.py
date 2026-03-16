"""
Build the final book markdown by replacing image references
with their descriptions from image_descriptions.json.

Input:  book_raw.md + image_descriptions.json
Output: book.md (ready to be loaded into the agent's context)
"""

import json
import re

BOOK_RAW_PATH = "book_raw.md"
DESCRIPTIONS_PATH = "image_descriptions.json"
OUTPUT_PATH = "book.md"


def main():
    with open(BOOK_RAW_PATH, "r") as f:
        content = f.read()

    with open(DESCRIPTIONS_PATH, "r") as f:
        descriptions = json.load(f)

    pattern = re.compile(r"!\[([^\]]*)\]\(images/([^)]+)\)")

    def replace_image(match):
        filename = match.group(2)
        desc = descriptions.get(filename)
        if desc and not desc.startswith("["):
            return f"[Image: {desc}]"
        return f"[Image: {filename}]"

    result = pattern.sub(replace_image, content)

    with open(OUTPUT_PATH, "w") as f:
        f.write(result)

    size = len(result)
    print(f"Written {OUTPUT_PATH}: {size:,} chars (~{size // 4:,} tokens)")


if __name__ == "__main__":
    main()
