"""
VMware vSphere Metrics Q&A — CLI

Uses the same architecture as the web app:
- Haiku router selects relevant chapters per question
- Sonnet answers with selected chapters + skills
- Streamed output with prompt caching

Image input:
  Interactive:  prefix your message with one or more image paths, one per line:
                  image: /path/to/screenshot.png
                  What metrics are shown here?
  Non-interactive (single question):
                  python3 agent.py --question "..." --image a.png --image b.png
"""

import argparse
import base64
import json
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()

CHAPTERS_DIR = "chapters"
CHAPTERS_INDEX = os.path.join(CHAPTERS_DIR, "chapter_index.json")
CHAPTERS_INDEX_TXT = os.path.join(CHAPTERS_DIR, "chapter_index.txt")
SKILLS_DIR = "skills"
MODEL = "claude-sonnet-4-6"
ROUTER_MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You are an expert VMware vSphere metrics advisor. You have deep knowledge of VMware vSphere metrics from the authoritative book "VMware vSphere Metrics" which is provided in full below.

## How to answer questions

1. **Use the book as your primary source.** Always ground your answers in the book's content. If the book covers a topic, use its reasoning and explanations rather than general knowledge.

2. **Preserve reasoning chains.** The book explains WHY metrics behave certain ways — the architecture behind them. When answering, include this reasoning so users truly understand, not just memorize.

3. **Cite sections.** Reference the relevant chapter and section (e.g., "As explained in CPU > VM > Contention Metrics > Ready") so users can look up the full context.

4. **Be precise about metric distinctions.** The book emphasizes that:
   - Same-named metrics can have different formulas across different objects (VM vs ESXi vs Cluster)
   - Metrics that sound similar may measure fundamentally different things
   - Context (VM level vs vCPU level vs ESXi level) changes the meaning
   Always clarify these distinctions.

5. **Use the Triple See Method** when it helps structure an answer: Collection, Calculation (including thresholds), and Correlation.

6. **Handle ambiguity.** If a question could refer to metrics at different levels (VM, ESXi, Cluster), ask for clarification or explain the differences at each level.

7. **Be honest about gaps.** If the book doesn't cover something (e.g., it notes vSAN and NSX metrics are not yet added), say so clearly.
"""

ROUTER_PROMPT = """You are a router for a VMware vSphere metrics Q&A system. Given a user question, select which book chapters are needed to answer it.

Available chapters:
{chapter_index}

Rules:
- Always include "Introduction" — it has foundational concepts needed for all answers.
- Select 1-3 additional chapters that are most relevant to the question.
- If unsure, include more chapters rather than fewer.
- For troubleshooting questions, include the relevant resource chapter (CPU, Memory, Storage, Network) AND "Provider" (which covers cluster-level and ESXi-level views).
- For capacity planning, include "Consumer" and/or "Provider".
- For Windows guest OS questions, include "MS Windows".

Respond with ONLY a JSON array of chapter titles. Example: ["Introduction", "CPU", "Provider"]"""


def load_chapters() -> tuple[dict[str, str], str, list[str]]:
    """Load chapter index and all chapter content."""
    if not os.path.exists(CHAPTERS_INDEX):
        print(f"Error: {CHAPTERS_INDEX} not found. Run preprocess.py first.")
        sys.exit(1)

    with open(CHAPTERS_INDEX) as f:
        index = json.load(f)
    with open(CHAPTERS_INDEX_TXT) as f:
        index_txt = f.read()

    chapters: dict[str, str] = {}
    titles: list[str] = []
    for entry in index:
        filepath = os.path.join(CHAPTERS_DIR, entry["filename"])
        with open(filepath) as f:
            chapters[entry["title"]] = f.read()
        titles.append(entry["title"])

    return chapters, index_txt, titles


def load_skills() -> str:
    """Load all skills from skills/ directory."""
    if not os.path.isdir(SKILLS_DIR):
        return ""
    skills_text = "\n## Skills\n\nYou have specialized skills that can be activated. When activated, follow the skill instructions precisely.\n\n"
    for filename in sorted(os.listdir(SKILLS_DIR)):
        if filename.endswith(".md"):
            with open(os.path.join(SKILLS_DIR, filename)) as f:
                skills_text += f.read() + "\n\n"
    return skills_text


def load_image(path: str) -> dict:
    """Load an image file and return an Anthropic image content block."""
    ext = os.path.splitext(path)[1].lower()
    media_type_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                      ".gif": "image/gif", ".webp": "image/webp"}
    media_type = media_type_map.get(ext, "image/png")
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


def route_question(
    client: anthropic.Anthropic,
    message: str,
    index_txt: str,
    chapters: dict[str, str],
    titles: list[str],
) -> list[str]:
    """Use Haiku to select relevant chapters for the question."""
    prompt = ROUTER_PROMPT.format(chapter_index=index_txt)
    response = client.messages.create(
        model=ROUTER_MODEL,
        max_tokens=200,
        system=prompt,
        messages=[{"role": "user", "content": message}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        selected = json.loads(text)
        if isinstance(selected, list):
            valid = [t for t in selected if t in chapters]
            if "Introduction" not in valid and "Introduction" in chapters:
                valid.insert(0, "Introduction")
            return valid if valid else titles
    except Exception:
        pass
    return titles


def parse_input(raw: str) -> tuple[list[str], str]:
    """Parse raw multi-line input into (image_paths, text).

    Lines starting with 'image:' (case-insensitive) are treated as image paths.
    All other lines form the text message.
    """
    image_paths = []
    text_lines = []
    for line in raw.split("\n"):
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith("image:"):
            path = stripped[6:].strip()
            if path:
                image_paths.append(path)
        else:
            text_lines.append(stripped)
    return image_paths, "\n".join(l for l in text_lines if l).strip()


def build_user_content(text: str, image_paths: list[str]) -> list[dict] | str:
    """Build the content block(s) for a user message."""
    if not image_paths:
        return text
    content = []
    for path in image_paths:
        if not os.path.exists(path):
            print(f"  Warning: image not found: {path}")
            continue
        content.append(load_image(path))
        print(f"  [image loaded: {path}]")
    if text:
        content.append({"type": "text", "text": text})
    return content if content else text


def ask(
    client: anthropic.Anthropic,
    text: str,
    image_paths: list[str],
    conversation: list[dict],
    chapters: dict[str, str],
    index_txt: str,
    titles: list[str],
    skills_content: str,
) -> str:
    """Send a question (with optional images) and stream the response."""
    router_text = text or "analyze this screenshot"
    selected = route_question(client, router_text, index_txt, chapters, titles)
    book_excerpt = "\n\n".join(chapters[t] for t in selected if t in chapters)
    excerpt_tokens = len(book_excerpt) // 4
    print(f"  [router: {selected} — ~{excerpt_tokens:,} tokens]")

    system = [
        {
            "type": "text",
            "text": SYSTEM_PROMPT + skills_content,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": f"## Book Chapters: {', '.join(selected)}\n\n{book_excerpt}",
        },
    ]

    user_content = build_user_content(text, image_paths)
    conversation.append({"role": "user", "content": user_content})

    print("\nAssistant: ", end="", flush=True)
    full_response = []
    try:
        with client.messages.stream(
            model=MODEL,
            max_tokens=4096,
            system=system,
            messages=conversation,
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
                full_response.append(chunk)

        assistant_msg = "".join(full_response)
        conversation.append({"role": "assistant", "content": assistant_msg})

        msg = stream.get_final_message()
        usage = msg.usage
        cache_read = getattr(usage, "cache_read_input_tokens", 0)
        cache_create = getattr(usage, "cache_creation_input_tokens", 0)
        print(
            f"\n  [tokens: in={usage.input_tokens} out={usage.output_tokens} "
            f"cache_read={cache_read} cache_create={cache_create}]\n"
        )
        return assistant_msg

    except Exception as e:
        print(f"\nError: {e}\n")
        conversation.pop()
        return ""


def interactive(client, chapters, index_txt, titles, skills_content):
    print("\nAsk me anything about VMware vSphere metrics!")
    print("Prefix image paths with 'image:' on a separate line before your question.")
    print("Type 'reset' to start a new conversation, 'quit' to exit.\n")

    conversation: list[dict] = []

    while True:
        try:
            lines = []
            first = input("You: ").strip()
            if not first:
                continue
            if first.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break
            if first.lower() == "reset":
                conversation.clear()
                print("Conversation reset.\n")
                continue
            lines.append(first)
            # If the first line is an image: prefix, keep reading until a blank line or non-image line
            while first.lower().startswith("image:"):
                try:
                    nxt = input("     ").strip()
                except EOFError:
                    break
                if not nxt:
                    break
                lines.append(nxt)
                first = nxt
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        raw = "\n".join(lines)
        image_paths, text = parse_input(raw)
        if not text and not image_paths:
            continue

        ask(client, text, image_paths, conversation, chapters, index_txt, titles, skills_content)


def main():
    parser = argparse.ArgumentParser(description="VMware vSphere Metrics Q&A CLI")
    parser.add_argument("--question", "-q", help="Question to ask (non-interactive)")
    parser.add_argument("--image", "-i", action="append", default=[], metavar="PATH",
                        help="Image file(s) to include with the question (repeatable)")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    print("Loading chapters...")
    chapters, index_txt, titles = load_chapters()
    total_tokens = sum(len(c) // 4 for c in chapters.values())
    print(f"Loaded {len(chapters)} chapters (~{total_tokens:,} total tokens)")

    skills_content = load_skills()
    skill_files = [f for f in os.listdir(SKILLS_DIR) if f.endswith(".md")] if os.path.isdir(SKILLS_DIR) else []
    print(f"Loaded {len(skill_files)} skills: {', '.join(skill_files)}")
    print(f"Model: {MODEL}  |  Router: {ROUTER_MODEL}")

    if args.question or args.image:
        # Non-interactive single-question mode
        conversation: list[dict] = []
        ask(client, args.question or "", args.image, conversation,
            chapters, index_txt, titles, skills_content)
    else:
        interactive(client, chapters, index_txt, titles, skills_content)


if __name__ == "__main__":
    main()
