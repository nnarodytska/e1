"""
VMware vSphere Metrics Q&A — Web App

FastAPI backend with streaming responses and a chat UI.
"""

import os
import sqlite3
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

load_dotenv()

BOOK_PATH = "book.md"
BOOK_RAW_PATH = "book_raw.md"
SKILLS_DIR = "skills"
CHAPTERS_DIR = "chapters"
CHAPTERS_INDEX = os.path.join(CHAPTERS_DIR, "chapter_index.json")
CHAPTERS_INDEX_TXT = os.path.join(CHAPTERS_DIR, "chapter_index.txt")
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

8. **Format your answers in Markdown** for readability. Use tables, headers, and bullet points where appropriate.

9. **When the user uploads an image** (screenshot of a dashboard, metrics chart, esxtop output, etc.):
   - Identify all visible metrics, their values, and trends
   - Interpret them using the book's methodology and thresholds
   - Flag any values that indicate performance issues or capacity concerns
   - Explain what the metrics mean in relation to each other (e.g., high CPU Ready with low Usage)
   - Recommend next steps for troubleshooting if issues are found

"""

def load_skills(skills_dir: str) -> str:
    """Load all .md files from skills/ directory and concatenate them."""
    if not os.path.isdir(skills_dir):
        return ""
    skills_text = "\n## Skills\n\nYou have specialized skills that can be activated. When activated, follow the skill instructions precisely.\n\n"
    for filename in sorted(os.listdir(skills_dir)):
        if filename.endswith(".md"):
            with open(os.path.join(skills_dir, filename), "r") as f:
                skills_text += f.read() + "\n\n"
    return skills_text


# In-memory session store: session_id -> list of messages
sessions: dict[str, list[dict]] = {}
chapters: dict[str, str] = {}  # title -> content
chapter_index_txt: str = ""
chapter_titles: list[str] = []
skills_content: str = ""


DB_PATH = os.path.join(os.environ.get("DATA_DIR", "."), "feedback.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating TEXT NOT NULL CHECK(rating IN ('up', 'down')),
            comment TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chapters, chapter_index_txt, chapter_titles, skills_content
    init_db()

    # Load chapter index
    import json as _json
    with open(CHAPTERS_INDEX, "r") as f:
        index = _json.load(f)
    with open(CHAPTERS_INDEX_TXT, "r") as f:
        chapter_index_txt = f.read()

    # Load all chapters into memory
    for entry in index:
        filepath = os.path.join(CHAPTERS_DIR, entry["filename"])
        with open(filepath, "r") as f:
            chapters[entry["title"]] = f.read()
        chapter_titles.append(entry["title"])

    total_tokens = sum(len(c) // 4 for c in chapters.values())
    print(f"Loaded {len(chapters)} chapters (~{total_tokens:,} total tokens)")
    for title, content in chapters.items():
        print(f"  {title}: ~{len(content)//4:,} tokens")

    skills_content = load_skills(SKILLS_DIR)
    skill_files = [f for f in os.listdir(SKILLS_DIR) if f.endswith(".md")] if os.path.isdir(SKILLS_DIR) else []
    print(f"Loaded {len(skill_files)} skills: {', '.join(skill_files)}")
    yield


app = FastAPI(title="VMware Metrics Q&A", lifespan=lifespan)
client = anthropic.Anthropic()


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_PAGE


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


def route_question(message: str) -> list[str]:
    """Use a fast model to select relevant chapters."""
    prompt = ROUTER_PROMPT.format(chapter_index=chapter_index_txt)

    response = client.messages.create(
        model=ROUTER_MODEL,
        max_tokens=200,
        system=prompt,
        messages=[{"role": "user", "content": message}],
    )

    # Parse the response — extract JSON array (may be wrapped in ```json fences)
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        import json as _json
        selected = _json.loads(text)
        if isinstance(selected, list):
            # Validate titles exist
            valid = [t for t in selected if t in chapters]
            # Always ensure Introduction is included
            if "Introduction" not in valid and "Introduction" in chapters:
                valid.insert(0, "Introduction")
            return valid if valid else chapter_titles  # fallback to all
    except Exception:
        pass

    # Fallback: return all chapters
    return chapter_titles


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "").strip()
    session_id = body.get("session_id", str(uuid.uuid4()))
    images = body.get("images", [])  # list of {data: base64, media_type: "image/png"}

    if not message and not images:
        return {"error": "Empty message"}

    if session_id not in sessions:
        sessions[session_id] = []

    # Build user content with optional images
    user_content = []
    for img in images:
        user_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": img.get("media_type", "image/png"),
                "data": img["data"],
            },
        })
    if message:
        user_content.append({"type": "text", "text": message})

    sessions[session_id].append({"role": "user", "content": user_content})

    # Stage 1: Route to relevant chapters
    selected = route_question(message or "analyze this screenshot")
    book_excerpt = "\n\n".join(
        chapters[title] for title in selected if title in chapters
    )
    excerpt_tokens = len(book_excerpt) // 4
    print(f"  Router selected: {selected} (~{excerpt_tokens:,} tokens)")

    system = [
        {"type": "text", "text": SYSTEM_PROMPT + skills_content},
        {
            "type": "text",
            "text": f"## Book Chapters: {', '.join(selected)}\n\n{book_excerpt}",
            "cache_control": {"type": "ephemeral"},
        },
    ]

    # Stage 2: Answer with selected chapters
    def generate():
        full_response = []
        with client.messages.stream(
            model=MODEL,
            max_tokens=4096,
            system=system,
            messages=sessions[session_id],
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield text

        sessions[session_id].append(
            {"role": "assistant", "content": "".join(full_response)}
        )

    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/api/feedback")
async def feedback(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "")
    message_id = body.get("message_id", "")
    question = body.get("question", "")
    answer = body.get("answer", "")
    rating = body.get("rating", "")
    comment = body.get("comment", "")

    if rating not in ("up", "down"):
        return JSONResponse({"error": "Invalid rating"}, status_code=400)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO feedback (session_id, message_id, question, answer, rating, comment, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (session_id, message_id, question[:2000], answer[:5000], rating, comment[:1000], datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.post("/api/reset")
async def reset(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "")
    if session_id in sessions:
        del sessions[session_id]
    return {"ok": True}


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VMware Metrics Q&A</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    background: #1e293b;
    border-bottom: 1px solid #334155;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  header h1 {
    font-size: 18px;
    font-weight: 600;
    color: #f1f5f9;
  }

  header h1 span { color: #60a5fa; }

  #reset-btn {
    background: #334155;
    color: #94a3b8;
    border: 1px solid #475569;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
  }

  #reset-btn:hover { background: #475569; color: #e2e8f0; }

  #chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .message {
    max-width: 85%;
    line-height: 1.6;
  }

  .message.user {
    align-self: flex-end;
    background: #1d4ed8;
    color: #fff;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    font-size: 15px;
  }

  .message.assistant {
    align-self: flex-start;
    background: #1e293b;
    border: 1px solid #334155;
    padding: 18px 22px;
    border-radius: 4px 18px 18px 18px;
    font-size: 14px;
  }

  .message.assistant h1, .message.assistant h2, .message.assistant h3 {
    margin-top: 16px;
    margin-bottom: 8px;
    color: #93c5fd;
  }

  .message.assistant h1 { font-size: 18px; }
  .message.assistant h2 { font-size: 16px; }
  .message.assistant h3 { font-size: 15px; }

  .message.assistant p { margin: 8px 0; }

  .message.assistant table {
    border-collapse: collapse;
    margin: 12px 0;
    width: 100%;
    font-size: 13px;
  }

  .message.assistant th, .message.assistant td {
    border: 1px solid #475569;
    padding: 8px 12px;
    text-align: left;
  }

  .message.assistant th { background: #334155; color: #93c5fd; }

  .message.assistant code {
    background: #334155;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
  }

  .message.assistant blockquote {
    border-left: 3px solid #60a5fa;
    padding-left: 14px;
    margin: 10px 0;
    color: #94a3b8;
    font-style: italic;
  }

  .message.assistant ul, .message.assistant ol {
    margin: 8px 0 8px 20px;
  }

  .message.assistant li { margin: 4px 0; }

  .message.assistant strong { color: #f1f5f9; }

  #input-area {
    background: #1e293b;
    border-top: 1px solid #334155;
    padding: 16px 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  #image-preview-bar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .image-preview {
    position: relative;
    width: 64px;
    height: 64px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #475569;
  }

  .image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .image-preview .remove-img {
    position: absolute;
    top: 2px;
    right: 2px;
    background: rgba(0,0,0,0.7);
    color: #fff;
    border: none;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    font-size: 11px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
  }

  #input-row {
    display: flex;
    gap: 12px;
  }

  #upload-btn {
    background: #334155;
    color: #94a3b8;
    border: 1px solid #475569;
    padding: 12px 14px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
  }

  #upload-btn:hover { background: #475569; color: #e2e8f0; }

  #input {
    flex: 1;
    background: #0f172a;
    border: 1px solid #334155;
    color: #e2e8f0;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 15px;
    outline: none;
    font-family: inherit;
  }

  #input:focus { border-color: #60a5fa; }

  #send-btn {
    background: #2563eb;
    color: #fff;
    border: none;
    padding: 12px 24px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 500;
  }

  #send-btn:hover { background: #1d4ed8; }
  #send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .message.user .user-images {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    flex-wrap: wrap;
  }

  .message.user .user-images img {
    max-width: 200px;
    max-height: 150px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2);
  }

  .typing-indicator {
    display: inline-block;
    color: #64748b;
    font-style: italic;
    font-size: 13px;
  }

  #welcome {
    text-align: center;
    margin: auto;
    max-width: 600px;
    color: #64748b;
  }

  #welcome h2 { color: #93c5fd; margin-bottom: 12px; font-size: 20px; }
  #welcome p { margin: 8px 0; font-size: 14px; line-height: 1.6; }

  .example-questions {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }

  .example-q {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    text-align: left;
    font-size: 13px;
    color: #94a3b8;
    position: relative;
    z-index: 10;
    user-select: none;
  }

  .example-q:hover { border-color: #60a5fa; color: #e2e8f0; }

  .feedback-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid #334155;
  }

  .feedback-bar button {
    background: none;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 4px 10px;
    cursor: pointer;
    font-size: 16px;
    color: #94a3b8;
    transition: all 0.15s;
  }

  .feedback-bar button:hover { border-color: #60a5fa; color: #e2e8f0; }
  .feedback-bar button.selected-up { border-color: #22c55e; color: #22c55e; background: rgba(34,197,94,0.1); }
  .feedback-bar button.selected-down { border-color: #ef4444; color: #ef4444; background: rgba(239,68,68,0.1); }

  .feedback-bar .feedback-label {
    font-size: 12px;
    color: #64748b;
  }

  .feedback-bar .feedback-thanks {
    font-size: 12px;
    color: #22c55e;
  }

  .feedback-comment-box {
    margin-top: 8px;
    display: flex;
    gap: 8px;
  }

  .feedback-comment-box input {
    flex: 1;
    background: #0f172a;
    border: 1px solid #475569;
    color: #e2e8f0;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    outline: none;
    font-family: inherit;
  }

  .feedback-comment-box input:focus { border-color: #ef4444; }

  .feedback-comment-box button {
    background: #334155;
    color: #94a3b8;
    border: 1px solid #475569;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
  }

  .feedback-comment-box button:hover { background: #475569; color: #e2e8f0; }
</style>
</head>
<body>

<header>
  <h1><span>VMware Metrics</span> Q&A</h1>
  <button id="reset-btn" onclick="resetChat()">New Chat</button>
</header>

<div id="chat-container">
  <div id="welcome">
    <h2>VMware vSphere Metrics Expert</h2>
    <p>Ask any question about VMware vSphere metrics. Answers are grounded in the authoritative book with full reasoning chains preserved.</p>
    <div class="example-questions" style="margin-top: 16px;">
      <div class="example-q" onclick="askExample(this)">My VM is slow and I see high CPU Ready. Help me troubleshoot.</div>
      <div class="example-q" onclick="askExample(this)">What is the difference between CPU Ready and CPU Contention?</div>
      <div class="example-q" onclick="askExample(this)">What is the difference between Usage and Utilization?</div>
      <div class="example-q" onclick="askExample(this)">Why is VM CPU Demand lower than VM CPU Usage?</div>
      <div class="example-q" onclick="askExample(this)">Explain CPU Usage across VM, ESXi, and Cluster levels</div>
      <div class="example-q" onclick="askExample(this)">What is the impact of Hyper-Threading on CPU metrics?</div>
    </div>
  </div>
</div>

<div id="input-area">
  <div id="image-preview-bar"></div>
  <div id="input-row">
    <button id="upload-btn" onclick="document.getElementById('file-input').click()" title="Upload screenshot">&#128247;</button>
    <input type="file" id="file-input" accept="image/*" multiple style="display:none" onchange="handleFiles(this.files)">
    <input type="text" id="input" placeholder="Ask about VMware metrics... (paste or upload screenshots)" onkeydown="if(event.key==='Enter')sendMessage()" onpaste="handlePaste(event)">
    <button id="send-btn" onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
const sessionId = crypto.randomUUID();
let isStreaming = false;
let pendingImages = []; // [{data: base64, media_type: "image/png", dataUrl: "data:..."}]

function askExample(el) {
  document.getElementById('input').value = el.textContent;
  sendMessage();
}

function handleFiles(files) {
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue;
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      const base64 = dataUrl.split(',')[1];
      pendingImages.push({ data: base64, media_type: file.type, dataUrl });
      renderImagePreviews();
    };
    reader.readAsDataURL(file);
  }
}

function handlePaste(event) {
  const items = event.clipboardData?.items;
  if (!items) return;
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      event.preventDefault();
      const file = item.getAsFile();
      handleFiles([file]);
    }
  }
}

function renderImagePreviews() {
  const bar = document.getElementById('image-preview-bar');
  bar.innerHTML = '';
  pendingImages.forEach((img, idx) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'image-preview';
    wrapper.innerHTML = '<img src="' + img.dataUrl + '"><button class="remove-img" onclick="removeImage(' + idx + ')">x</button>';
    bar.appendChild(wrapper);
  });
}

function removeImage(idx) {
  pendingImages.splice(idx, 1);
  renderImagePreviews();
}

async function sendMessage() {
  if (isStreaming) return;
  const input = document.getElementById('input');
  const message = input.value.trim();
  if (!message && pendingImages.length === 0) return;

  const imagesToSend = [...pendingImages];
  pendingImages = [];
  renderImagePreviews();
  input.value = '';
  isStreaming = true;
  document.getElementById('send-btn').disabled = true;

  // Remove welcome
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();

  const chat = document.getElementById('chat-container');

  // Add user message with images
  const userDiv = document.createElement('div');
  userDiv.className = 'message user';
  if (imagesToSend.length > 0) {
    const imgContainer = document.createElement('div');
    imgContainer.className = 'user-images';
    imagesToSend.forEach(img => {
      const imgEl = document.createElement('img');
      imgEl.src = img.dataUrl;
      imgContainer.appendChild(imgEl);
    });
    userDiv.appendChild(imgContainer);
  }
  if (message) {
    const textEl = document.createElement('div');
    textEl.textContent = message;
    userDiv.appendChild(textEl);
  }
  chat.appendChild(userDiv);

  // Add assistant message placeholder
  const assistantDiv = document.createElement('div');
  assistantDiv.className = 'message assistant';
  assistantDiv.innerHTML = '<span class="typing-indicator">Analyzing...</span>';
  chat.appendChild(assistantDiv);
  chat.scrollTop = chat.scrollHeight;

  const payload = {
    message: message || 'Please analyze this screenshot and explain what the metrics show.',
    session_id: sessionId,
    images: imagesToSend.map(i => ({ data: i.data, media_type: i.media_type })),
  };

  let fullText = '';
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      fullText += decoder.decode(value, { stream: true });
      assistantDiv.innerHTML = marked.parse(fullText);
      chat.scrollTop = chat.scrollHeight;
    }
  } catch (e) {
    assistantDiv.innerHTML = '<p style="color:#ef4444">Error: Could not get response. Please try again.</p>';
  }

  // Add feedback bar
  const msgId = crypto.randomUUID();
  const feedbackBar = document.createElement('div');
  feedbackBar.className = 'feedback-bar';
  feedbackBar.setAttribute('data-msg-id', msgId);
  feedbackBar._question = message || '(image upload)';
  feedbackBar._answer = fullText;
  const fbLabel = document.createElement('span');
  fbLabel.className = 'feedback-label';
  fbLabel.textContent = 'Was this helpful?';
  const fbUp = document.createElement('button');
  fbUp.title = 'Helpful';
  fbUp.innerHTML = '&#128077;';
  fbUp.addEventListener('click', function() { submitFeedback(this, 'up'); });
  const fbDown = document.createElement('button');
  fbDown.title = 'Not helpful';
  fbDown.innerHTML = '&#128078;';
  fbDown.addEventListener('click', function() { submitFeedback(this, 'down'); });
  feedbackBar.appendChild(fbLabel);
  feedbackBar.appendChild(fbUp);
  feedbackBar.appendChild(fbDown);
  assistantDiv.appendChild(feedbackBar);

  isStreaming = false;
  document.getElementById('send-btn').disabled = false;
  input.focus();
}

function submitFeedback(btn, rating) {
  const bar = btn.closest('.feedback-bar');
  if (bar.dataset.submitted === 'true') return;

  const msgId = bar.getAttribute('data-msg-id');
  const question = bar._question;
  const answer = bar._answer;

  // Highlight selected button
  const buttons = bar.querySelectorAll('button');
  buttons.forEach(b => b.classList.remove('selected-up', 'selected-down'));
  btn.classList.add(rating === 'up' ? 'selected-up' : 'selected-down');

  if (rating === 'up') {
    // Submit immediately
    bar.dataset.submitted = 'true';
    fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message_id: msgId, question, answer, rating }),
    });
    const label = bar.querySelector('.feedback-label');
    label.className = 'feedback-thanks';
    label.textContent = 'Thanks for the feedback!';
  } else {
    // Show comment box
    let commentBox = bar.parentElement.querySelector('.feedback-comment-box');
    if (!commentBox) {
      commentBox = document.createElement('div');
      commentBox.className = 'feedback-comment-box';
      const cbInput = document.createElement('input');
      cbInput.type = 'text';
      cbInput.placeholder = 'What was wrong? (optional)';
      cbInput.addEventListener('keydown', function(e) { if (e.key === 'Enter') submitDownFeedback(cbInput.nextElementSibling); });
      const cbBtn = document.createElement('button');
      cbBtn.textContent = 'Send';
      cbBtn.addEventListener('click', function() { submitDownFeedback(this); });
      commentBox.appendChild(cbInput);
      commentBox.appendChild(cbBtn);
      commentBox._msgId = msgId;
      commentBox._question = question;
      commentBox._answer = answer;
      bar.parentElement.appendChild(commentBox);
      commentBox.querySelector('input').focus();
    }
  }
}

function submitDownFeedback(btn) {
  const box = btn.closest('.feedback-comment-box');
  const comment = box.querySelector('input').value.trim();
  const bar = box.parentElement.querySelector('.feedback-bar');

  bar.dataset.submitted = 'true';
  fetch('/api/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      message_id: box._msgId,
      question: box._question,
      answer: box._answer,
      rating: 'down',
      comment,
    }),
  });

  const label = bar.querySelector('.feedback-label');
  label.className = 'feedback-thanks';
  label.textContent = 'Thanks for the feedback!';
  box.remove();
}

function resetChat() {
  fetch('/api/reset', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });
  const chat = document.getElementById('chat-container');
  chat.innerHTML = `
    <div id="welcome">
      <h2>VMware vSphere Metrics Expert</h2>
      <p>Ask any question about VMware vSphere metrics. Answers are grounded in the authoritative book with full reasoning chains preserved.</p>
      <div class="example-questions" style="margin-top: 16px;">
        <div class="example-q" onclick="askExample(this)">My VM is slow and I see high CPU Ready. Help me troubleshoot.</div>
        <div class="example-q" onclick="askExample(this)">What is the difference between CPU Ready and CPU Contention?</div>
        <div class="example-q" onclick="askExample(this)">What is the difference between Usage and Utilization?</div>
        <div class="example-q" onclick="askExample(this)">Why is VM CPU Demand lower than VM CPU Usage?</div>
        <div class="example-q" onclick="askExample(this)">Explain CPU Usage across VM, ESXi, and Cluster levels</div>
        <div class="example-q" onclick="askExample(this)">What is the impact of Hyper-Threading on CPU metrics?</div>
      </div>
    </div>`;
}
</script>

</body>
</html>"""
