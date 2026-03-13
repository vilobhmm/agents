# 🎯 AI Agents Trend Radar

**Multi-Agent RAG Recommendation Engine** — Discovers, analyzes, and recommends trending AI agents & agentic AI topics using 3 specialized AI agents and Retrieval-Augmented Generation.

---

## 🚀 Quick Start

```bash
# Full pipeline + web dashboard
python -m agents.rag_recommendation.run_engine

# Scrape & analyze (console output)
python -m agents.rag_recommendation.run_engine --scrape-only

# Custom interests
python -m agents.rag_recommendation.run_engine --interests "RAG" "multi-agent" "code agents"

# Dashboard only (serve cached data)
python -m agents.rag_recommendation.run_engine --dashboard-only --port 9000
```

Open **http://localhost:8080** to explore the dashboard.

---

## 🏗️ Architecture

```
Sources (6) → Curator Agent → Analyst Agent → Recommender Agent → Dashboard
                   ↓                                    ↑
              ChromaDB Vector Store ──── RAG Retrieval ──┘
```

### 🤖 Three Specialized Agents

| Agent | Role | What It Does |
|-------|------|-------------|
| **🔍 Curator** | Scout | Scrapes 6 sources, deduplicates, ranks by trending score, clusters into topics |
| **📊 Analyst** | Researcher | Deep-dives with Claude: summaries, "why it matters", key developments, reading levels |
| **💡 Recommender** | Advisor | RAG-powered personalization: semantic matching, combined scoring, "why read" explanations |

### 🌐 Data Sources

| Source | Method |
|--------|--------|
| arXiv | Atom API (cs.AI, cs.MA, cs.CL) |
| HackerNews | Algolia Search API |
| Reddit | Public JSON API |
| GitHub | Trending page scrape |
| AI Lab Blogs | RSS feeds (OpenAI, Google, Meta, HuggingFace, LangChain) |
| HuggingFace | Daily Papers page |

### 📚 RAG Engine

- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector Store**: ChromaDB with cosine similarity
- **Collections**: `trending_topics`, `user_preferences`, `topic_analysis`

---

## 📁 File Structure

```
agents/rag_recommendation/
├── run_engine.py           # CLI entry point
├── orchestrator.py         # 3-agent pipeline coordinator
├── scrapers/
│   ├── trending_scraper.py # Multi-source scraper
│   └── source_aggregator.py# Dedup, score & cluster
├── rag/
│   ├── embedder.py         # Sentence-transformers
│   └── vector_store.py     # ChromaDB wrapper
├── agents/
│   ├── curator_agent.py    # Scout/filter agent
│   ├── analyst_agent.py    # Deep-dive agent
│   └── recommender_agent.py# Personalization agent
└── dashboard/
    ├── server.py           # API server
    ├── index.html          # Dashboard UI
    ├── styles.css          # Dark glassmorphism theme
    └── app.js              # Client logic
```

---

## ⚙️ Configuration

### API Keys

```bash
export ANTHROPIC_API_KEY=sk-ant-...  # For Analyst & Recommender LLM analysis
```

> The engine works without an API key — agents fall back to rule-based analysis.

### Custom Interests

```python
from agents.rag_recommendation.orchestrator import RecommendationOrchestrator

engine = RecommendationOrchestrator(
    user_interests=["RAG", "code agents", "agent memory"]
)
result = await engine.run()
```

---

## 🧪 Testing

```bash
python -m pytest tests/test_rag_recommendation.py -v
```
