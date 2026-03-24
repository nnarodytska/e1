"""
Quiz runner — runs all questions from quiz.json through the agent and prints a
summary table showing agent answer vs answer key.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
from dotenv import load_dotenv

import agent as ag

load_dotenv()

QUIZ_FILE = os.path.join(os.path.dirname(__file__), "quiz.json")

ANSWER_PROMPT = """You are a quiz grader. Given the agent's response to a multiple-choice question, extract which answer letter(s) the agent chose (A, B, C, D, E, F, G).

Return ONLY the letters, comma-separated if multiple (e.g. "A", "B, C", "A, D, F"). No explanation. No punctuation other than commas and spaces."""


def extract_answer(client: anthropic.Anthropic, response: str, options: list[str]) -> str:
    """Use Haiku to extract the answer letter(s) from the agent response."""
    options_text = "\n".join(options) if options else "(open-ended question)"
    prompt = f"""Question options:
{options_text}

Agent response:
{response}

Which answer letter(s) did the agent select?"""

    result = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        system=ANSWER_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return result.content[0].text.strip()


def build_question_text(q: dict) -> str:
    parts = []
    if q.get("context"):
        parts.append(q["context"])
    parts.append(q["question"])
    if q.get("options"):
        parts.append("\n".join(q["options"]))
    if q.get("hint"):
        parts.append(f"Hint: {q['hint']}")
    return "\n\n".join(parts)


def main():
    with open(QUIZ_FILE) as f:
        questions = json.load(f)

    client = anthropic.Anthropic()

    print("Loading chapters and skills...")
    chapters, index_txt, titles = ag.load_chapters()
    skills_content = ag.load_skills()
    print(f"Loaded {len(chapters)} chapters, {len([f for f in os.listdir(ag.SKILLS_DIR) if f.endswith('.md')])} skills\n")

    results = []

    for q in questions:
        qid = q["id"]
        answer_key = q.get("answer_key", "?")

        if answer_key.startswith("open-ended"):
            print(f"\n{'='*60}")
            print(f"[{qid}] {q['title']} — SKIPPED (open-ended)")
            results.append((qid, q["title"], "open-ended", answer_key, "—"))
            continue

        print(f"\n{'='*60}")
        print(f"[{qid}] {q['title']}")
        print(f"Answer key: {answer_key}")
        print("-" * 40)

        text = build_question_text(q)
        images = q.get("images", [])

        conversation = []
        response = ag.ask(
            client, text, images, conversation,
            chapters, index_txt, titles, skills_content,
        )

        if not response:
            results.append((qid, q["title"], "ERROR", answer_key, "✗"))
            continue

        agent_answer = extract_answer(client, response, q.get("options", []))
        print(f"  → Agent: {agent_answer}  |  Key: {answer_key}")

        match = agent_answer.upper().replace(" ", "") == answer_key.upper().replace(" ", "")
        results.append((qid, q["title"], agent_answer, answer_key, "✓" if match else "✗"))

    # Summary table
    print(f"\n\n{'='*70}")
    print("QUIZ RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"{'ID':<12} {'Title':<35} {'Agent':<12} {'Key':<12} {'Match'}")
    print(f"{'-'*70}")
    for qid, title, agent_ans, key, match in results:
        print(f"{qid:<12} {title[:34]:<35} {agent_ans:<12} {key:<12} {match}")

    correct = sum(1 for *_, m in results if m == "✓")
    total = sum(1 for *_, m in results if m != "—")
    print(f"\nScore: {correct}/{total}")


if __name__ == "__main__":
    main()
