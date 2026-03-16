"""
VMware vSphere Metrics Q&A Agent.

Loads the entire book into context and answers user questions
using Claude with prompt caching for efficiency.
"""

import anthropic
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BOOK_PATH = "book.md"
BOOK_RAW_PATH = "book_raw.md"
MODEL = "claude-sonnet-4-6"


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

6. **Reference images** when relevant — the book includes many dashboard screenshots and diagrams that illustrate metric behaviors. Describe what they show when citing them.

7. **Handle ambiguity.** If a question could refer to metrics at different levels (VM, ESXi, Cluster), ask for clarification or explain the differences at each level.

8. **Be honest about gaps.** If the book doesn't cover something (e.g., it notes vSAN and NSX metrics are not yet added), say so clearly."""


def load_book() -> str:
    """Load book.md (with image descriptions) or fall back to book_raw.md."""
    if os.path.exists(BOOK_PATH):
        print(f"Loading {BOOK_PATH} (with image descriptions)")
        path = BOOK_PATH
    elif os.path.exists(BOOK_RAW_PATH):
        print(f"Loading {BOOK_RAW_PATH} (without image descriptions)")
        print("  Run 'python describe_images.py && python build_book.py' for full version")
        path = BOOK_RAW_PATH
    else:
        print("Error: No book file found. Run preprocess.py first.")
        sys.exit(1)

    with open(path, "r") as f:
        return f.read()


def create_cached_messages(book_content: str, conversation: list[dict]) -> tuple:
    """Build the message structure with the book cached in system prompt."""
    system = [
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
        },
        {
            "type": "text",
            "text": f"## Complete Book: VMware vSphere Metrics\n\n{book_content}",
            "cache_control": {"type": "ephemeral"},
        },
    ]
    return system, conversation


def main():
    client = anthropic.Anthropic()
    book_content = load_book()
    book_tokens = len(book_content) // 4
    print(f"Loaded book: ~{book_tokens:,} tokens")
    print(f"Model: {MODEL}")
    print(f"Using prompt caching (book cached after first request)")
    print(f"\nAsk me anything about VMware vSphere metrics!")
    print(f"Type 'quit' to exit.\n")

    conversation = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        system, messages = create_cached_messages(book_content, conversation)

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=system,
                messages=messages,
            )

            assistant_msg = response.content[0].text
            conversation.append({"role": "assistant", "content": assistant_msg})

            print(f"\nAssistant: {assistant_msg}\n")

            # Show cache stats
            usage = response.usage
            cache_read = getattr(usage, "cache_read_input_tokens", 0)
            cache_create = getattr(usage, "cache_creation_input_tokens", 0)
            print(
                f"  [tokens: in={usage.input_tokens} out={usage.output_tokens} "
                f"cache_read={cache_read} cache_create={cache_create}]\n"
            )

        except Exception as e:
            print(f"\nError: {e}\n")
            conversation.pop()  # Remove failed user message


if __name__ == "__main__":
    main()
