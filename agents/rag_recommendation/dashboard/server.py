"""
Dashboard API Server

Lightweight HTTP server that:
1. Runs the multi-agent recommendation pipeline
2. Serves the dashboard static files
3. Exposes /api/data endpoint for the frontend
"""

import asyncio
import json
import logging
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from typing import Optional

logger = logging.getLogger(__name__)

# ── Module-level state ────────────────────────────────────────────
_cached_json: Optional[str] = None
_dashboard_dir = Path(__file__).parent


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves static files + /api/data endpoint."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(_dashboard_dir), **kwargs)

    def do_GET(self):
        # API endpoint
        if self.path == "/api/data":
            self._serve_api()
            return

        # API refresh endpoint
        if self.path == "/api/refresh":
            self._serve_refresh()
            return

        # Static files (default handler)
        super().do_GET()

    def _serve_api(self):
        global _cached_json
        if _cached_json:
            self._json_response(200, _cached_json)
        else:
            self._json_response(503, json.dumps({
                "error": "Pipeline has not run yet. Please wait..."
            }))

    def _serve_refresh(self):
        """Trigger a pipeline refresh in the background."""
        Thread(target=_run_pipeline_sync, daemon=True).start()
        self._json_response(200, json.dumps({"status": "refresh_started"}))

    def _json_response(self, code: int, body: str):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, fmt, *args):
        # Suppress noisy request logs
        if "/api/" not in (args[0] if args else ""):
            return
        logger.debug(fmt % args)


def _run_pipeline_sync():
    """Run the async pipeline in a new event loop (for background thread)."""
    global _cached_json
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_run_pipeline())
        _cached_json = result
        loop.close()
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        _cached_json = json.dumps({"error": str(e)})


async def _run_pipeline() -> str:
    """Execute the recommendation pipeline and return JSON."""
    from agents.rag_recommendation.orchestrator import RecommendationOrchestrator

    orchestrator = RecommendationOrchestrator()
    await orchestrator.run()
    return orchestrator.to_json()


def start_server(
    port: int = 8080,
    run_pipeline: bool = True,
    open_browser: bool = True,
):
    """
    Start the dashboard server.

    Args:
        port: HTTP port.
        run_pipeline: If True, run the recommendation pipeline on startup.
        open_browser: If True, open the dashboard in the default browser.
    """
    global _cached_json

    print(f"\n{'═' * 60}")
    print(f"  🎯 AI Agents Trend Radar — Dashboard Server")
    print(f"  📡 http://localhost:{port}")
    print(f"{'═' * 60}\n")

    if run_pipeline:
        print("🔄 Running multi-agent pipeline (Curator → Analyst → Recommender)...")
        Thread(target=_run_pipeline_sync, daemon=True).start()

    if open_browser:
        import webbrowser
        # Slight delay to let server start
        def _open():
            import time
            time.sleep(1.5)
            webbrowser.open(f"http://localhost:{port}")
        Thread(target=_open, daemon=True).start()

    server = HTTPServer(("0.0.0.0", port), DashboardHandler)
    try:
        print(f"✅ Server running on http://localhost:{port}")
        print("   Press Ctrl+C to stop.\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        server.server_close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Agents Trend Radar Dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--no-pipeline", action="store_true", help="Skip initial pipeline run")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")

    args = parser.parse_args()
    start_server(
        port=args.port,
        run_pipeline=not args.no_pipeline,
        open_browser=not args.no_browser,
    )
