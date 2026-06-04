#!/usr/bin/env python3
"""
Agent Dashboard — local HTTP server.
Run:  python dashboard/server.py
Open: http://localhost:8765
"""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
AGENTS_DIR = ROOT / "agents"
SCRIPTS_DIR = ROOT / "scripts"
RESEARCH_DIR = ROOT / "research" / "sources"
DASHBOARD_DIR = Path(__file__).parent

PORT = 8765


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except Exception:
        return {}


def read_file(path: Path, max_chars: int = 0) -> str:
    if not path.exists():
        return ""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
            return content[:max_chars] if max_chars else content
    except Exception:
        return ""


def count_files(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(1 for f in directory.iterdir() if f.is_file() and f.name != ".gitkeep")


def get_agents():
    agents = []
    if not AGENTS_DIR.exists():
        return agents

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
            continue

        config = load_json(agent_dir / "agent.yaml")

        memory_dir = agent_dir / "memory"
        memory = {
            "raw_history": (memory_dir / "raw_history.jsonl").exists(),
            "long_term": (memory_dir / "long_term_memory.json").exists(),
            "session_notes": (memory_dir / "session_notes.md").exists(),
            "compacted": (memory_dir / "compacted_context.md").exists(),
        }

        knowledge_dir = agent_dir / "knowledge"
        knowledge_count = 0
        if knowledge_dir.exists():
            for f in knowledge_dir.iterdir():
                if f.is_file() and f.name not in ("README.md", ".gitkeep"):
                    knowledge_count += 1

        evals_dir = agent_dir / "evals"
        has_evals = (evals_dir / "eval_cases.yaml").exists()

        outputs_dir = agent_dir / "outputs"
        outputs_count = count_files(outputs_dir)

        agents.append({
            "name": agent_dir.name,
            "display_name": agent_dir.name.replace("_", " ").title(),
            "description": config.get("description", ""),
            "version": config.get("version", "1.0.0"),
            "role": config.get("role", ""),
            "model_provider": (config.get("model") or {}).get("provider", "mock"),
            "memory": memory,
            "memory_coverage": sum(memory.values()),
            "knowledge_count": knowledge_count,
            "has_evals": has_evals,
            "has_checklist": (agent_dir / "checklist.yaml").exists(),
            "outputs_count": outputs_count,
        })

    return agents


def get_agent_detail(name: str) -> dict:
    agent_dir = AGENTS_DIR / name
    if not agent_dir.exists():
        return {}

    config = load_json(agent_dir / "agent.yaml")
    system_prompt = read_file(agent_dir / "system_prompt.md", max_chars=6000)

    knowledge_dir = agent_dir / "knowledge"
    knowledge_files = []
    if knowledge_dir.exists():
        for f in sorted(knowledge_dir.iterdir()):
            if f.is_file() and f.name not in ("README.md", ".gitkeep"):
                knowledge_files.append({"name": f.name, "size": f.stat().st_size})

    memory_dir = agent_dir / "memory"
    session_notes = read_file(memory_dir / "session_notes.md", max_chars=2000)

    return {
        "name": name,
        "config": config,
        "system_prompt": system_prompt,
        "knowledge_files": knowledge_files,
        "session_notes": session_notes,
    }


def get_stats():
    agents = get_agents()
    total = len(agents)
    full_memory = sum(1 for a in agents if a["memory_coverage"] == 4)
    has_evals = sum(1 for a in agents if a["has_evals"])
    has_knowledge = sum(1 for a in agents if a["knowledge_count"] > 0)
    research_sources = get_research_sources()
    scripts = get_scripts()
    return {
        "total_agents": total,
        "full_memory": full_memory,
        "has_evals": has_evals,
        "has_knowledge": has_knowledge,
        "research_sources": len(research_sources),
        "scripts": len(scripts),
    }


def get_research_sources():
    sources = []
    if not RESEARCH_DIR.exists():
        return sources
    for src_dir in sorted(RESEARCH_DIR.iterdir()):
        if not src_dir.is_dir() or src_dir.name == "custom":
            continue
        config = load_json(src_dir / "source_config.yaml")
        raw_count = count_files(src_dir / "raw")
        processed_count = count_files(src_dir / "processed")
        sources.append({
            "name": src_dir.name,
            "display_name": config.get("name", src_dir.name.replace("_", " ").title()),
            "description": config.get("description", ""),
            "enabled": config.get("enabled", False),
            "mode": config.get("mode", "mock"),
            "raw_count": raw_count,
            "processed_count": processed_count,
        })
    return sources


def get_scripts():
    scripts = []
    if not SCRIPTS_DIR.exists():
        return scripts
    for script in sorted(SCRIPTS_DIR.glob("*.py")):
        if script.name.startswith("_"):
            continue
        scripts.append({
            "name": script.name,
            "display_name": script.stem.replace("_", " ").title(),
        })
    return scripts


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress access logs

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path: Path):
        if not path.exists():
            self.send_error(404, "Not found")
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/") or "/"

        routes = {
            "/api/stats":     lambda: self.send_json(get_stats()),
            "/api/agents":    lambda: self.send_json(get_agents()),
            "/api/research":  lambda: self.send_json(get_research_sources()),
            "/api/scripts":   lambda: self.send_json(get_scripts()),
        }

        if path in ("/", "/index.html"):
            self.send_html(DASHBOARD_DIR / "index.html")
        elif path in routes:
            routes[path]()
        elif path.startswith("/api/agent/"):
            name = path[len("/api/agent/"):]
            detail = get_agent_detail(name)
            self.send_json(detail if detail else {"error": "not found"}, 200 if detail else 404)
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"  Agent Dashboard  ->  http://localhost:{port}")
    print("  Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
