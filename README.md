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

- **Dynamic chapter routing** — only loads relevant chapters (3-4x cheaper than full book)
- **Prompt caching** — subsequent questions reuse cached chapters
- **4 auto-triggered skills** — formatting, troubleshooting, metric comparison, metric explorer
- **Image upload** — users can paste/upload vSphere screenshots for analysis
- **Feedback collection** — thumbs up/down with optional comments stored in SQLite

## Prerequisites

- Python 3.12+
- Anthropic API key
- ngrok account (optional, for public access)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Pre-process the book (first time only)

The book must be placed at `book/VMware vSphere Metrics.docx`.

```bash
# Convert docx to structured markdown
python3 preprocess.py

# Describe images using Claude vision (optional, ~10-15 min)
python3 describe_images.py

# Build final book with image descriptions
python3 build_book.py

# Split into chapters for dynamic routing
python3 split_chapters.py
```

If you skip image descriptions, the agent still works — it just won't have textual descriptions of charts and diagrams.

### 4. Run the web app

```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000

### 5. Expose publicly (optional)

```bash
# With ngrok (replace with your domain)
ngrok http 8000 --domain your-domain.ngrok.dev
```

Or with Docker:

```bash
docker build -t vmware-metrics-qa .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=sk-ant-... vmware-metrics-qa
```

## Project Structure

```
├── app.py                  # Web app (FastAPI + chat UI)
├── agent.py                # CLI agent (interactive terminal)
├── preprocess.py           # Converts docx -> book_raw.md
├── describe_images.py      # Describes images with Claude vision
├── build_book.py           # Merges image descriptions -> book.md
├── split_chapters.py       # Splits book into chapters for routing
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build
├── .env                    # API key (not committed)
│
├── book/                   # Source book (.docx)
├── book_raw.md             # Converted markdown (no image descriptions)
├── book.md                 # Full markdown (with image descriptions)
├── images/                 # Extracted images from book
├── image_descriptions.json # Vision-generated image descriptions
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
│   ├── troubleshoot.md     # Decision trees from drawio diagrams
│   ├── compare.md          # Side-by-side metric comparison
│   └── explore.md          # Level-by-level metric breakdown
│
├── diagrams/               # Source troubleshooting flowcharts
│   └── vSphere CPU Performance Troubleshooting.drawio
│
└── feedback.db             # User feedback (SQLite, auto-created)
```

## Skills

Skills are markdown files in `skills/` that are loaded automatically at startup. They instruct the model how to respond in specific situations.

| Skill | File | Trigger |
|-------|------|---------|
| **Formatting** | `formatting.md` | Always active. Structures every answer with TL;DR, Details, Action, Book ref. |
| **Troubleshoot** | `troubleshoot.md` | When user describes a performance problem. Uses decision trees from the drawio diagrams. |
| **Compare** | `compare.md` | When user asks about differences between metrics ("X vs Y"). |
| **Explore** | `explore.md` | When user asks about a specific metric across levels (VM/ESXi/Cluster). |

To add a new skill, create a `.md` file in `skills/` and restart the server.

## Costs

| Scenario | Tokens | Cost per question |
|----------|--------|-------------------|
| First question (cache write) | ~60K | ~$0.20 |
| Subsequent questions (cache read) | ~60K | ~$0.02 |
| Router call (Haiku) | ~2K | ~$0.001 |
| 10-question session | | ~$0.40 |

## Viewing Feedback

```bash
# All feedback
sqlite3 feedback.db "SELECT created_at, rating, comment, substr(question,1,60) FROM feedback ORDER BY created_at DESC"

# Just thumbs down with comments
sqlite3 feedback.db "SELECT created_at, comment, substr(question,1,60) FROM feedback WHERE rating='down' AND comment != '' ORDER BY created_at DESC"
```
