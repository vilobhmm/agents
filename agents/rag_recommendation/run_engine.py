"""
CLI entry point for the Multi-Agent RAG Recommendation Engine.

Usage:
    # Full pipeline + dashboard
    python -m agents.rag_recommendation.run_engine

    # Scrape & analyze only (no dashboard)
    python -m agents.rag_recommendation.run_engine --scrape-only

    # Dashboard only (serve cached data)
    python -m agents.rag_recommendation.run_engine --dashboard-only

    # Custom port
    python -m agents.rag_recommendation.run_engine --port 9000
"""

import argparse
import asyncio
import json
import logging
import sys


def main():
    parser = argparse.ArgumentParser(
        description="🎯 AI Agents Trend Radar — Multi-Agent RAG Recommendation Engine"
    )
    parser.add_argument(
        "--scrape-only",
        action="store_true",
        help="Run pipeline and print results (no dashboard)",
    )
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Start dashboard without running the pipeline",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Dashboard server port (default: 8080)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't auto-open browser",
    )
    parser.add_argument(
        "--interests",
        nargs="+",
        default=None,
        help='User interests for personalization (e.g. --interests "RAG" "multi-agent")',
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.scrape_only:
        _run_scrape_only(interests=args.interests)
    elif args.dashboard_only:
        _run_dashboard(port=args.port, run_pipeline=False, open_browser=not args.no_browser)
    else:
        _run_dashboard(port=args.port, run_pipeline=True, open_browser=not args.no_browser)


def _run_scrape_only(interests=None):
    """Run the pipeline and print results to stdout."""
    from agents.rag_recommendation.orchestrator import RecommendationOrchestrator

    print("\n🎯 Running multi-agent recommendation pipeline...\n")

    orchestrator = RecommendationOrchestrator(user_interests=interests)
    result = asyncio.run(orchestrator.run())

    # Print summary
    feed = result["curated_feed"]
    recs = result["recommendations"]
    meta = result["metadata"]

    print(f"\n{'═' * 60}")
    print(f"  Pipeline completed in {meta['pipeline_duration_seconds']}s")
    print(f"{'═' * 60}")
    print(f"\n{feed.summary_text()}")
    print(f"\n{recs.summary_text()}")
    print(f"\n{'═' * 60}")
    print(f"  Vector Store: {meta['vector_store_stats']}")
    print(f"{'═' * 60}\n")


def _run_dashboard(port, run_pipeline, open_browser):
    """Start the dashboard server."""
    from agents.rag_recommendation.dashboard.server import start_server
    start_server(port=port, run_pipeline=run_pipeline, open_browser=open_browser)


if __name__ == "__main__":
    main()
