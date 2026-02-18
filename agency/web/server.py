"""
Agency Web UI Server

FastAPI + WebSocket backend for the multi-agent control center.
Provides real-time visibility into agent conversations, queue state, and logs.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
AGENCY_DIR = Path.home() / ".agency"
QUEUE_DIR = AGENCY_DIR / "queue"
WORKSPACE_DIR = Path.home() / ".agency-workspace"
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"

# ─── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(title="Agency Control Center", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ─── WebSocket Manager ────────────────────────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self.active: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)
        logger.info(f"WebSocket connected. Total: {len(self.active)}")

    def disconnect(self, ws: WebSocket):
        self.active.discard(ws)
        logger.info(f"WebSocket disconnected. Total: {len(self.active)}")

    async def broadcast(self, data: dict):
        if not self.active:
            return
        dead = set()
        msg = json.dumps(data)
        for ws in self.active:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.active.discard(ws)


manager = ConnectionManager()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_agents_config() -> dict:
    """Load agents.json config."""
    config_path = TEMPLATES_DIR / "agents.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {"agents": {}, "teams": {}}


def get_queue_counts() -> dict:
    """Count messages in each queue stage."""
    counts = {"incoming": 0, "processing": 0, "outgoing": 0}
    for stage in counts:
        stage_dir = QUEUE_DIR / stage
        if stage_dir.exists():
            counts[stage] = len(list(stage_dir.glob("*.json")))
    return counts


def get_conversations() -> List[dict]:
    """Load all active conversations."""
    convs = []
    conv_dir = QUEUE_DIR / "conversations"
    if not conv_dir.exists():
        return convs

    for conv_file in sorted(conv_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:20]:
        try:
            with open(conv_file) as f:
                data = json.load(f)

            # Simplify responses for transport
            responses = []
            for r in data.get("responses", []):
                responses.append({
                    "agent_id": r.get("agent_id", ""),
                    "agent_name": r.get("agent_name", ""),
                    "response": r.get("response", ""),
                    "timestamp": r.get("timestamp", 0),
                })

            convs.append({
                "id": data.get("id", ""),
                "channel": data.get("channel", ""),
                "sender": data.get("sender", ""),
                "original_message": data.get("original_message", ""),
                "pending": data.get("pending", 0),
                "total_messages": data.get("total_messages", 0),
                "created_at": data.get("created_at", 0),
                "responses": responses,
            })
        except Exception as e:
            logger.warning(f"Could not parse {conv_file}: {e}")

    return convs


def get_recent_logs(n: int = 100) -> List[str]:
    """Get recent log lines."""
    log_file = LOGS_DIR / "agency.log"
    if not log_file.exists():
        # Try alternate locations
        for alt in [Path("logs/agency.log"), Path("/tmp/agency.log")]:
            if alt.exists():
                log_file = alt
                break
        else:
            return []

    try:
        with open(log_file) as f:
            lines = f.readlines()
        return [l.rstrip() for l in lines[-n:]]
    except Exception:
        return []


def get_agent_workspace_info() -> dict:
    """Get per-agent workspace info (last activity, history size)."""
    info = {}
    if not WORKSPACE_DIR.exists():
        return info

    for agent_dir in WORKSPACE_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        agent_id = agent_dir.name
        conv_file = agent_dir / "conversation.json"
        info[agent_id] = {
            "has_history": conv_file.exists(),
            "history_size": 0,
            "last_active": None,
        }
        if conv_file.exists():
            try:
                stat = conv_file.stat()
                info[agent_id]["last_active"] = stat.st_mtime
                with open(conv_file) as f:
                    hist = json.load(f)
                info[agent_id]["history_size"] = len(hist)
            except Exception:
                pass

    return info


# ─── Background Broadcaster ───────────────────────────────────────────────────

_last_state: dict = {}


async def state_broadcaster():
    """Poll for state changes and broadcast to WebSocket clients."""
    global _last_state

    # Track log position
    log_pos = 0
    log_file = LOGS_DIR / "agency.log"
    if log_file.exists():
        log_pos = log_file.stat().st_size

    while True:
        await asyncio.sleep(1.5)

        if not manager.active:
            continue

        try:
            # ── Queue state ──
            queue = get_queue_counts()
            if queue != _last_state.get("queue"):
                _last_state["queue"] = queue
                await manager.broadcast({"type": "queue_update", "data": queue})

            # ── Conversations ──
            convs = get_conversations()
            conv_ids = {c["id"]: c["pending"] for c in convs}
            if conv_ids != _last_state.get("conv_ids"):
                _last_state["conv_ids"] = conv_ids
                await manager.broadcast({"type": "conversations_update", "data": convs})

            # ── New log lines ──
            if log_file.exists():
                current_size = log_file.stat().st_size
                if current_size > log_pos:
                    try:
                        with open(log_file) as f:
                            f.seek(log_pos)
                            new_lines = f.read(current_size - log_pos)
                        log_pos = current_size
                        lines = [l for l in new_lines.split("\n") if l.strip()]
                        if lines:
                            await manager.broadcast({"type": "log_lines", "data": lines})
                    except Exception:
                        pass

            # ── Agent workspace info ──
            ws_info = get_agent_workspace_info()
            if ws_info != _last_state.get("ws_info"):
                _last_state["ws_info"] = ws_info
                await manager.broadcast({"type": "workspace_update", "data": ws_info})

        except Exception as e:
            logger.warning(f"Broadcaster error: {e}")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(state_broadcaster())
    logger.info("Agency Web UI started")


# ─── REST API ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return HTMLResponse("<h1>Agency Web UI</h1><p>Static files not found.</p>")


@app.get("/api/agents")
async def api_agents():
    config = load_agents_config()
    ws_info = get_agent_workspace_info()

    agents = []
    for agent_id, agent in config.get("agents", {}).items():
        info = ws_info.get(agent_id, {})
        agents.append({
            "agent_id": agent_id,
            "name": agent.get("name", agent_id),
            "provider": agent.get("provider", "anthropic"),
            "model": agent.get("model", "sonnet"),
            "personality": agent.get("personality", "")[:200],
            "skills": agent.get("skills", []),
            "has_history": info.get("has_history", False),
            "history_size": info.get("history_size", 0),
            "last_active": info.get("last_active"),
        })

    return {"agents": agents}


@app.get("/api/teams")
async def api_teams():
    config = load_agents_config()
    teams = []
    for team_id, team in config.get("teams", {}).items():
        teams.append({
            "team_id": team_id,
            "name": team.get("name", team_id),
            "description": team.get("description", ""),
            "agents": team.get("agents", []),
            "leader_agent": team.get("leader_agent", ""),
        })
    return {"teams": teams}


@app.get("/api/queue")
async def api_queue():
    return get_queue_counts()


@app.get("/api/conversations")
async def api_conversations():
    return {"conversations": get_conversations()}


@app.get("/api/logs")
async def api_logs(n: int = 200):
    return {"lines": get_recent_logs(n)}


@app.get("/api/workspace")
async def api_workspace():
    return {"agents": get_agent_workspace_info()}


class SendMessageRequest(BaseModel):
    message: str
    agent: Optional[str] = None
    team: Optional[str] = None
    sender: str = "web_ui"
    sender_id: str = "web"


@app.post("/api/messages")
async def api_send_message(req: SendMessageRequest):
    """Send a message to an agent or team by writing to the incoming queue."""
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    incoming_dir = QUEUE_DIR / "incoming"
    incoming_dir.mkdir(parents=True, exist_ok=True)

    msg_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().timestamp()

    # Format message with @agent prefix if not already there
    message_text = req.message
    if req.agent and not message_text.startswith(f"@{req.agent}"):
        message_text = f"@{req.agent} {message_text}"
    elif req.team and not message_text.startswith(f"@{req.team}"):
        message_text = f"@{req.team} {message_text}"

    payload = {
        "channel": "web",
        "sender": req.sender,
        "sender_id": req.sender_id,
        "message": message_text,
        "timestamp": timestamp,
        "message_id": msg_id,
        "agent": req.agent,
        "team": req.team,
        "conversation_id": None,
        "files": [],
        "metadata": {
            "source": "web_ui",
            "web_session": msg_id,
        }
    }

    fname = f"{timestamp}_{msg_id}.json"
    fpath = incoming_dir / fname
    with open(fpath, "w") as f:
        json.dump(payload, f, indent=2)

    logger.info(f"Web UI queued message to {req.agent or req.team}: {msg_id}")

    # Broadcast to all WS clients immediately
    await manager.broadcast({
        "type": "message_sent",
        "data": {
            "message_id": msg_id,
            "message": message_text,
            "agent": req.agent,
            "team": req.team,
            "timestamp": timestamp,
        }
    })

    return {"status": "queued", "message_id": msg_id}


@app.delete("/api/conversations/clear")
async def api_clear_conversations():
    """Clear all conversation history (workspace conversation.json files)."""
    cleared = 0
    if WORKSPACE_DIR.exists():
        for conv_file in WORKSPACE_DIR.glob("*/conversation.json"):
            conv_file.unlink()
            cleared += 1
    return {"cleared": cleared}


# ─── WebSocket ────────────────────────────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        # Send initial state on connect
        config = load_agents_config()
        await ws.send_text(json.dumps({
            "type": "init",
            "data": {
                "queue": get_queue_counts(),
                "conversations": get_conversations(),
                "logs": get_recent_logs(50),
                "workspace": get_agent_workspace_info(),
                "agents": list(config.get("agents", {}).keys()),
                "teams": list(config.get("teams", {}).keys()),
            }
        }))

        # Keep alive and handle any incoming messages
        while True:
            try:
                msg = await asyncio.wait_for(ws.receive_text(), timeout=30)
                data = json.loads(msg)
                if data.get("type") == "ping":
                    await ws.send_text(json.dumps({"type": "pong"}))
            except asyncio.TimeoutError:
                await ws.send_text(json.dumps({"type": "ping"}))

    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        manager.disconnect(ws)


# ─── Entry point ──────────────────────────────────────────────────────────────

def run_server(host: str = "0.0.0.0", port: int = 3000, open_browser: bool = True):
    """Run the web UI server."""
    import uvicorn

    if open_browser:
        import threading
        import time
        import webbrowser

        def _open():
            time.sleep(1.5)
            webbrowser.open(f"http://localhost:{port}")

        threading.Thread(target=_open, daemon=True).start()

    print(f"\n🌐  Agency Control Center → http://localhost:{port}\n")
    uvicorn.run(app, host=host, port=port, log_level="warning")
