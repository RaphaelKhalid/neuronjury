"""Live viewport server.

/api/feed   -> aggregates feed/*.json (findings agents post on purpose)
/api/agents -> live per-agent activity parsed incrementally from workflow subagent transcripts
"""
import glob, json, os, re
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Lock
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FEED = os.path.join(ROOT, "feed")
PORT = int(os.environ.get("PORT", "8765"))
# Glob pattern for Claude Code workflow transcripts of this project; override with AGENTS_DIR.
AGENTS_DIR = os.environ.get("AGENTS_DIR", os.path.expanduser(
    "~/.claude/projects/*neuronjury*/*/subagents/workflows"))

RANGE_RE = re.compile(r"Your part: lines (\d+)\s*[–-]\s*(\d+)")


def short(s, n=90):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def humanize(name, inp, st):
    """Turn a tool call into a plain-English log line (emoji, text)."""
    inp = inp or {}
    if name == "Read":
        p = str(inp.get("file_path", ""))
        base = os.path.basename(p)
        off, lim = inp.get("offset"), inp.get("limit")
        if base == "already-clean.txt":
            a = int(off or 1)
            b = a + int(lim or 2000) - 1
            st["read_spans"].append((a, b))
            return "📖", f"Reading the essay, lines {a}–{b}"
        return "📖", f"Reading {base}"
    if name == "Grep":
        return "🔎", f"Searching the text for “{short(inp.get('pattern', ''), 50)}”"
    if name == "Glob":
        return "🗂️", f"Listing files {short(inp.get('pattern', ''), 50)}"
    if name == "WebSearch":
        st["searches"] += 1
        return "🌐", f"Searching the web: {short(inp.get('query', ''), 80)}"
    if name == "WebFetch":
        st["pages"] += 1
        u = urlparse(str(inp.get("url", "")))
        return "📄", f"Opening {u.netloc}{short(u.path, 50)}"
    if name == "Write":
        p = str(inp.get("file_path", "")).replace("\\", "/")
        base = os.path.basename(p)
        if "/feed/" in p:
            st["posts"] += 1
            try:
                h = json.loads(inp.get("content", "{}")).get("headline", "")
            except Exception:
                h = ""
            return "📣", f"Posted to the big screen: {short(h, 80)}" if h else "Posted to the big screen"
        if "/research/" in p:
            return "📝", f"Writing its full report ({base})"
        return "💾", f"Saving {base}"
    if name == "Edit":
        return "✏️", f"Editing {os.path.basename(str(inp.get('file_path', '')))}"
    if name in ("Bash", "PowerShell"):
        st["runs"] += 1
        return "⚙️", f"Running code: {short(inp.get('description') or inp.get('command', ''), 80)}"
    if name == "ToolSearch":
        return "🧰", "Loading its tools"
    if name == "StructuredOutput":
        st["done"] = True
        return "✅", "Handed in its results"
    if name.startswith("mcp__runpod"):
        return "☁️", f"Checking RunPod: {name.split('__')[-1]}"
    if name.startswith("mcp__"):
        return "🔌", f"Using {name.split('__')[-1]}"
    return "🔧", f"{name}"


class AgentState:
    def __init__(self, path):
        self.path = path
        self.offset = 0
        self.buf = b""
        self.st = {"read_spans": [], "searches": 0, "pages": 0, "posts": 0, "runs": 0, "done": False}
        self.events = []
        self.tools = 0
        self.out_tok = {}
        self.range = None
        self.first_ts = None
        self.last_ts = None
        self.thinking = False
        self.ended = False
        meta_p = path[: -len(".jsonl")] + ".meta.json"
        try:
            meta = json.load(open(meta_p, encoding="utf-8"))
        except Exception:
            meta = {}
        self.label = meta.get("description") or os.path.basename(path)[6:14]
        self.phase = meta.get("workflowPhase") or ""
        self.workflow = os.path.basename(os.path.dirname(path))

    def update(self):
        try:
            size = os.path.getsize(self.path)
        except OSError:
            return
        if size <= self.offset:
            return
        with open(self.path, "rb") as f:
            f.seek(self.offset)
            chunk = f.read(size - self.offset)
        self.offset = size
        data = self.buf + chunk
        lines = data.split(b"\n")
        self.buf = lines.pop()  # partial trailing line
        for raw in lines:
            if not raw.strip():
                continue
            try:
                d = json.loads(raw)
            except Exception:
                continue
            self.consume(d)

    def consume(self, d):
        ts = d.get("timestamp")
        if ts:
            self.first_ts = self.first_ts or ts
            self.last_ts = ts
        m = d.get("message") or {}
        if m.get("role") == "user" and self.range is None:
            c = m.get("content")
            text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))
            mm = RANGE_RE.search(text or "")
            if mm and "already-clean" in (text or ""):
                self.range = (int(mm.group(1)), int(mm.group(2)))
        if d.get("toolEndsTurn"):
            self.ended = True
        u = m.get("usage")
        if u and m.get("id"):
            self.out_tok[m["id"]] = max(self.out_tok.get(m["id"], 0), u.get("output_tokens") or 0)
        c = m.get("content")
        if m.get("role") == "assistant" and isinstance(c, list):
            for x in c:
                t = x.get("type")
                if t == "tool_use":
                    self.tools += 1
                    e, txt = humanize(x.get("name", ""), x.get("input"), self.st)
                    self.events.append({"ts": ts, "e": e, "t": txt})
                    self.thinking = False
                elif t == "thinking":
                    self.thinking = True
                elif t == "text" and x.get("text", "").strip():
                    self.events.append({"ts": ts, "e": "💬", "t": short(x["text"], 100)})
        if m.get("stop_reason") == "end_turn":
            self.ended = True
        self.events = self.events[-40:]

    def coverage(self):
        if not self.range:
            return None
        a, b = self.range
        covered = set()
        for x, y in self.st["read_spans"]:
            covered.update(range(max(a, x), min(b, y) + 1))
        return round(100 * len(covered) / max(1, b - a + 1))

    def to_json(self):
        return {
            "id": os.path.basename(self.path),
            "label": self.label,
            "phase": self.phase,
            "workflow": self.workflow,
            "done": self.st["done"] or self.ended,
            "thinking": self.thinking,
            "tools": self.tools,
            "searches": self.st["searches"],
            "pages": self.st["pages"],
            "posts": self.st["posts"],
            "runs": self.st["runs"],
            "out_tokens": sum(self.out_tok.values()),
            "coverage": self.coverage(),
            "first_ts": self.first_ts,
            "last_ts": self.last_ts,
            "events": self.events[-6:],
        }


AGENTS = {}
LOCK = Lock()


def agents_snapshot():
    with LOCK:
        for p in glob.glob(os.path.join(AGENTS_DIR, "wf_*", "agent-*.jsonl")):
            if p not in AGENTS:
                AGENTS[p] = AgentState(p)
            AGENTS[p].update()
        return [a.to_json() for a in AGENTS.values()]


def feed_snapshot():
    items = []
    os.makedirs(FEED, exist_ok=True)
    for name in os.listdir(FEED):
        if not name.endswith(".json"):
            continue
        p = os.path.join(FEED, name)
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue
        if isinstance(d, list):
            for i, x in enumerate(d):
                if isinstance(x, dict):
                    x.setdefault("id", f"{name}#{i}")
                    x["mtime"] = os.path.getmtime(p) + i * 0.001
                    items.append(x)
        elif isinstance(d, dict):
            d.setdefault("id", name)
            d["mtime"] = os.path.getmtime(p)
            items.append(d)
    items.sort(key=lambda x: x["mtime"])
    return items


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def log_message(self, *a):
        pass

    def send_json(self, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/feed"):
            return self.send_json(feed_snapshot())
        if self.path.startswith("/api/agents"):
            return self.send_json(agents_snapshot())
        return super().do_GET()


if __name__ == "__main__":
    print(f"viewport on http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
