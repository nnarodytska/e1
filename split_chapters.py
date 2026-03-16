"""
Split book.md (or book_raw.md) into individual chapter files
and generate a chapter index with summaries.

Output:
  chapters/00_introduction.md
  chapters/01_cpu.md
  chapters/02_memory.md
  ...
  chapters/chapter_index.json
"""

import json
import os
import re

BOOK_PATH = "book.md" if os.path.exists("book.md") else "book_raw.md"
CHAPTERS_DIR = "chapters"
INDEX_PATH = os.path.join(CHAPTERS_DIR, "chapter_index.json")


def split_into_chapters(book_path: str) -> list[dict]:
    with open(book_path, "r") as f:
        content = f.read()

    # Split on Heading 1 (# Title)
    # Pattern: line starting with "# " (single #, not ##)
    parts = re.split(r"(?=\n# )", content)

    chapters = []
    preamble = parts[0].strip()

    # First part is everything before the first H1 (foreword, preface, etc.)
    if preamble:
        chapters.append({
            "id": "preamble",
            "title": "Preamble",
            "content": preamble,
        })

    for part in parts[1:]:
        part = part.strip()
        if not part:
            continue

        # Extract title from first line
        first_line = part.split("\n")[0]
        title = first_line.lstrip("# ").strip()

        if not title:
            continue

        # Known chapter titles from the book's TOC
        known_chapters = {"introduction", "cpu", "memory", "storage", "network",
                          "consumer", "provider", "ms windows", "epilogue"}
        # Skip false H1 splits (code blocks, inline text).
        # Merge them back into the previous chapter.
        if title.lower() not in known_chapters and title != "Preamble" and chapters:
            chapters[-1]["content"] += "\n" + part
            continue

        chapters.append({
            "id": re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_"),
            "title": title,
            "content": part,
        })

    return chapters


def extract_headings(content: str) -> list[str]:
    """Extract H2 and H3 headings as section summary."""
    headings = []
    for line in content.split("\n"):
        if line.startswith("## "):
            headings.append(line.lstrip("# ").strip())
        elif line.startswith("### "):
            headings.append("  - " + line.lstrip("# ").strip())
    return headings


def main():
    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    chapters = split_into_chapters(BOOK_PATH)
    print(f"Split {BOOK_PATH} into {len(chapters)} chapters:")

    index = []
    for i, ch in enumerate(chapters):
        # Write chapter file
        filename = f"{i:02d}_{ch['id']}.md"
        filepath = os.path.join(CHAPTERS_DIR, filename)
        with open(filepath, "w") as f:
            f.write(ch["content"])

        chars = len(ch["content"])
        tokens_est = chars // 4
        headings = extract_headings(ch["content"])

        index.append({
            "filename": filename,
            "title": ch["title"],
            "tokens": tokens_est,
            "sections": headings,
        })

        print(f"  {filename}: {ch['title']} (~{tokens_est:,} tokens, {len(headings)} sections)")

    # Write index
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

    print(f"\nIndex written to {INDEX_PATH}")

    # Also generate a compact text index for the router prompt
    text_index_path = os.path.join(CHAPTERS_DIR, "chapter_index.txt")
    with open(text_index_path, "w") as f:
        for ch in index:
            f.write(f"## {ch['title']} (~{ch['tokens']:,} tokens)\n")
            for section in ch["sections"]:
                f.write(f"  {section}\n")
            f.write("\n")

    print(f"Text index written to {text_index_path}")


if __name__ == "__main__":
    main()
