# VMware vSphere Metrics Q&A Agent

A web-based Q&A agent that answers questions about VMware vSphere metrics using the full "VMware vSphere Metrics" book as its knowledge base. Built with Claude API + FastAPI.

## Architecture

```
User question
     |
     v
Router (Haiku) ──> selects relevant chapters (~2K tokens)
     |
     v
Answer (Sonnet) ──> responds using selected chapters + skills (~30-60K tokens)
     |
     v
Streamed response with feedback collection
```

- **Dynamic chapter routing** — only loads relevant chapters instead of the full book
- **Prompt caching** — system prompt and skills are cached across questions
- **Auto-triggered skills** — formatting, troubleshooting, metric comparison, metric explorer
- **Image upload** — users can paste/upload vSphere screenshots for analysis
- **Feedback collection** — thumbs up/down with optional comments stored in SQLite

## Prerequisites

- Python 3.12+
- Anthropic API key

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/nnarodytska/e1.git
cd e1
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Run

**Web app:**
```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```
Open http://localhost:8000

**CLI (terminal chat):**
```bash
python3 agent.py
```

## Project Structure

```
├── app.py                  # Web app (FastAPI + chat UI)
├── agent.py                # CLI agent (interactive terminal)
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed)
│
├── book.md                 # Full book markdown (with image descriptions)
│
├── chapters/               # Book split into individual chapters
│   ├── chapter_index.json  # Chapter metadata and sections
│   ├── chapter_index.txt   # Compact index for router prompt
│   ├── 00_preamble.md
│   ├── 01_introduction.md
│   ├── 02_cpu.md
│   └── ...
│
├── skills/                 # Auto-triggered agent skills
│   ├── formatting.md       # Answer structure (always active)
│   ├── troubleshoot.md     # Troubleshooting decision trees
│   ├── compare.md          # Side-by-side metric comparison
│   └── explore.md          # Level-by-level metric breakdown
│
└── feedback.db             # Conversations + feedback (SQLite, auto-created)
```

## Skills

Skills are markdown files in `skills/` that are loaded automatically at startup. They instruct the model how to respond in specific situations — no code changes needed.

| Skill | File | Trigger |
|-------|------|---------|
| **Formatting** | `formatting.md` | Always active. Structures every answer with TL;DR, Details, Action, Book ref. |
| **Troubleshoot** | `troubleshoot.md` | When user describes a performance problem. |
| **Troubleshoot CPU** | `troubleshoot_cpu.md` | When user reports VM CPU contention (high Ready, co-stop, slow VM). |
| **Troubleshoot Memory** | `troubleshoot_memory.md` | When user reports VM memory contention (balloon, swap, latency). |
| **CPU Frequency** | `cpu_frequency.md` | When user asks about actual CPU speed, Turbo Boost, or power policy effects. |
| **Compare** | `compare.md` | When user asks about differences between metrics ("X vs Y"). |
| **Explore** | `explore.md` | When user asks about a specific metric across levels (VM/ESXi/Cluster). |

To add a new skill, create a `.md` file in `skills/` and restart the server.

## Costs

The system+skills prompt (~5K tokens) is cached after the first question. Book chapters are selected dynamically per question and are not cached.

| Scenario | Tokens | Cost per question |
|----------|--------|-------------------|
| First question (cache write for skills) | ~5K skills + ~20–50K chapters | ~$0.08–$0.20 |
| Subsequent questions (skills cached) | ~5K cached + ~20–50K chapters | ~$0.06–$0.18 |
| Router call (Haiku) | ~2K | ~$0.001 |
| 10-question session | | ~$0.70–$1.80 |

## Viewing Feedback

```bash
# All feedback
sqlite3 feedback.db "SELECT created_at, rating, comment, substr(question,1,60) FROM feedback ORDER BY created_at DESC"

# Thumbs down with comments
sqlite3 feedback.db "SELECT created_at, comment, substr(question,1,60) FROM feedback WHERE rating='down' AND comment != '' ORDER BY created_at DESC"
```

Or visit `/conversations` in the web app for a full admin view with ratings.
