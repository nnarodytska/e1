"""
Pre-process 'VMware vSphere Metrics.docx' into structured markdown.

Steps:
1. Extract all images to images/ folder
2. Convert paragraphs + tables to markdown preserving heading hierarchy
3. Inline image references where they appear in the document
4. Output: book_raw.md (text + tables + image placeholders)
"""

import os
import re
import zipfile
from docx import Document
from docx.oxml.ns import qn

DOCX_PATH = "book/VMware vSphere Metrics.docx"
IMAGES_DIR = "images"
OUTPUT_PATH = "book_raw.md"


def extract_images(docx_path: str, images_dir: str) -> dict[str, str]:
    """Extract all images from docx and return mapping of rId -> filename."""
    os.makedirs(images_dir, exist_ok=True)
    rid_to_file = {}

    with zipfile.ZipFile(docx_path) as z:
        media_files = [f for f in z.namelist() if f.startswith("word/media/")]
        for media_path in media_files:
            filename = os.path.basename(media_path)
            out_path = os.path.join(images_dir, filename)
            with z.open(media_path) as src, open(out_path, "wb") as dst:
                dst.write(src.read())
            rid_to_file[media_path] = filename

    return rid_to_file


def build_rel_to_media(docx_path: str) -> dict[str, str]:
    """Build mapping from relationship ID to media path."""
    import xml.etree.ElementTree as ET

    rel_map = {}
    with zipfile.ZipFile(docx_path) as z:
        rels_path = "word/_rels/document.xml.rels"
        if rels_path in z.namelist():
            with z.open(rels_path) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
                for rel in root.findall(f"{ns}Relationship"):
                    rid = rel.get("Id")
                    target = rel.get("Target")
                    if target and target.startswith("media/"):
                        rel_map[rid] = "word/" + target
    return rel_map


def get_images_in_paragraph(paragraph, rel_to_media: dict) -> list[str]:
    """Find all image references in a paragraph's XML."""
    images = []
    # Look for blip elements which reference images
    blips = paragraph._element.findall(
        ".//" + qn("a:blip")
    )
    for blip in blips:
        embed = blip.get(qn("r:embed"))
        if embed and embed in rel_to_media:
            media_path = rel_to_media[embed]
            filename = os.path.basename(media_path)
            images.append(filename)
    return images


def table_to_markdown(table) -> str:
    """Convert a docx table to markdown table."""
    rows = []
    for row in table.rows:
        cells = []
        for cell in row.cells:
            text = cell.text.strip().replace("\n", " ").replace("|", "\\|")
            cells.append(text)
        rows.append(cells)

    if not rows:
        return ""

    # Build markdown table
    lines = []
    # Header
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
    # Body
    for row in rows[1:]:
        # Pad row if needed
        while len(row) < len(rows[0]):
            row.append("")
        lines.append("| " + " | ".join(row[: len(rows[0])]) + " |")

    return "\n".join(lines)


def heading_level(style_name: str) -> int | None:
    """Extract heading level from style name like 'Heading 1'."""
    if not style_name:
        return None
    m = re.match(r"Heading (\d+)", style_name)
    return int(m.group(1)) if m else None


def convert_to_markdown(docx_path: str, images_dir: str) -> str:
    """Convert docx to markdown preserving structure."""
    doc = Document(docx_path)

    # Build image mappings
    rid_to_media = extract_images(docx_path, images_dir)
    rel_to_media = build_rel_to_media(docx_path)

    # We need to iterate through the document body in order,
    # handling both paragraphs and tables as they appear.
    md_parts = []
    body = doc.element.body

    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

        if tag == "p":
            # It's a paragraph
            from docx.text.paragraph import Paragraph

            para = Paragraph(child, doc)
            style_name = para.style.name if para.style else ""
            text = para.text.strip()

            # Check for images
            images = get_images_in_paragraph(para, rel_to_media)

            level = heading_level(style_name)
            if level:
                md_parts.append(f"\n{'#' * level} {text}\n")
            elif text:
                # Check for list styles
                if "List" in style_name or "Bullet" in style_name:
                    md_parts.append(f"- {text}")
                elif "Number" in style_name:
                    md_parts.append(f"1. {text}")
                else:
                    md_parts.append(text)

            for img in images:
                md_parts.append(f"\n![{img}](images/{img})\n")

        elif tag == "tbl":
            # It's a table
            from docx.table import Table

            table = Table(child, doc)
            md_table = table_to_markdown(table)
            if md_table:
                md_parts.append(f"\n{md_table}\n")

    return "\n".join(md_parts)


def main():
    print("Converting docx to markdown...")
    markdown = convert_to_markdown(DOCX_PATH, IMAGES_DIR)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(markdown)

    size = os.path.getsize(OUTPUT_PATH)
    lines = markdown.count("\n")
    print(f"Written {OUTPUT_PATH}: {size:,} bytes, {lines:,} lines")
    print(f"Images extracted to {IMAGES_DIR}/")

    # Count image references
    img_refs = markdown.count("![")
    print(f"Image references in markdown: {img_refs}")


if __name__ == "__main__":
    main()
