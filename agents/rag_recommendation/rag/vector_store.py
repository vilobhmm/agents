"""
Vector Store

ChromaDB-backed vector store for trending AI content.
Supports add, search, similarity lookup, and auto-cleanup.
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents.rag_recommendation.rag.embedder import Embedder

logger = logging.getLogger(__name__)


class VectorStore:
    """
    ChromaDB-backed vector store for RAG retrieval.

    Collections:
      - trending_topics — indexed trending content from scrapers
      - user_preferences — topics a user has engaged with / bookmarked
      - topic_analysis — enriched analysis from the Analyst agent

    Usage:
        store = VectorStore()
        store.add_items("trending_topics", ids, texts, metadatas, embeddings)
        results = store.search("trending_topics", query_text, n=10)
    """

    DEFAULT_PERSIST_DIR = os.path.join(
        str(Path.home()), ".rag_recommendation", "chroma_db"
    )

    COLLECTIONS = ["trending_topics", "user_preferences", "topic_analysis"]

    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or self.DEFAULT_PERSIST_DIR
        self.embedder = Embedder()
        self._client = None
        self._collections: Dict[str, Any] = {}

    # -- lazy init ----------------------------------------------------------

    @property
    def client(self):
        if self._client is None:
            try:
                import chromadb
                from chromadb.config import Settings
                os.makedirs(self.persist_dir, exist_ok=True)
                self._client = chromadb.PersistentClient(
                    path=self.persist_dir,
                    settings=Settings(anonymized_telemetry=False),
                )
                logger.info(f"ChromaDB initialized at {self.persist_dir}")
            except ImportError:
                logger.error("chromadb not installed. Run: pip install chromadb")
                raise
        return self._client

    def _get_collection(self, name: str):
        if name not in self._collections:
            self._collections[name] = self.client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collections[name]

    # -- public API ---------------------------------------------------------

    def add_items(
        self,
        collection_name: str,
        ids: List[str],
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        embeddings: Optional[List[List[float]]] = None,
    ) -> int:
        """
        Add items to a collection.

        Args:
            collection_name: Target collection.
            ids: Unique IDs for each item.
            texts: Document texts.
            metadatas: Optional metadata dicts.
            embeddings: Pre-computed embeddings (auto-computed if None).

        Returns:
            Number of items added.
        """
        if not ids:
            return 0

        collection = self._get_collection(collection_name)

        if embeddings is None:
            embeddings = self.embedder.embed_texts(texts)

        # Ensure metadata values are ChromaDB-compatible (str, int, float, bool)
        safe_metadatas = None
        if metadatas:
            safe_metadatas = []
            for md in metadatas:
                safe = {}
                for k, v in md.items():
                    if isinstance(v, (str, int, float, bool)):
                        safe[k] = v
                    elif isinstance(v, list):
                        safe[k] = ", ".join(str(x) for x in v)
                    else:
                        safe[k] = str(v)
                safe_metadatas.append(safe)

        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=safe_metadatas,
        )

        logger.info(f"Upserted {len(ids)} items into '{collection_name}'")
        return len(ids)

    def search(
        self,
        collection_name: str,
        query: str,
        n_results: int = 10,
        where: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """
        Semantic search against a collection.

        Args:
            collection_name: Collection to search.
            query: Natural-language query.
            n_results: Max results.
            where: Optional ChromaDB where filter.

        Returns:
            List of result dicts with id, document, metadata, distance.
        """
        collection = self._get_collection(collection_name)
        query_embedding = self.embedder.embed_single(query)

        kwargs: Dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": min(n_results, collection.count() or 1),
        }
        if where:
            kwargs["where"] = where

        try:
            results = collection.query(**kwargs)
        except Exception as e:
            logger.error(f"Search error in '{collection_name}': {e}")
            return []

        # Flatten into list of dicts
        out: List[Dict[str, Any]] = []
        if results and results.get("ids"):
            for i, doc_id in enumerate(results["ids"][0]):
                out.append({
                    "id": doc_id,
                    "document": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    "distance": results["distances"][0][i] if results.get("distances") else 1.0,
                })

        return out

    def get_similar(
        self,
        collection_name: str,
        item_id: str,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find items similar to a given item by ID."""
        collection = self._get_collection(collection_name)

        try:
            item = collection.get(ids=[item_id], include=["embeddings"])
            if not item or not item["embeddings"]:
                return []
            embedding = item["embeddings"][0]
        except Exception:
            return []

        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results + 1,  # +1 because the item itself will match
        )

        out = []
        if results and results.get("ids"):
            for i, doc_id in enumerate(results["ids"][0]):
                if doc_id == item_id:
                    continue  # skip self
                out.append({
                    "id": doc_id,
                    "document": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    "distance": results["distances"][0][i] if results.get("distances") else 1.0,
                })

        return out[:n_results]

    def cleanup_old(self, collection_name: str, max_age_days: int = 30) -> int:
        """Remove items older than max_age_days."""
        collection = self._get_collection(collection_name)
        cutoff = (datetime.now() - timedelta(days=max_age_days)).isoformat()

        try:
            # Get all items with their metadata
            all_items = collection.get(include=["metadatas"])
            if not all_items or not all_items["ids"]:
                return 0

            old_ids = []
            for i, meta in enumerate(all_items.get("metadatas", [])):
                if meta and meta.get("published_at", "") < cutoff:
                    old_ids.append(all_items["ids"][i])

            if old_ids:
                collection.delete(ids=old_ids)
                logger.info(f"Cleaned up {len(old_ids)} old items from '{collection_name}'")

            return len(old_ids)
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")
            return 0

    def get_collection_stats(self) -> Dict[str, int]:
        """Get item counts for all collections."""
        stats = {}
        for name in self.COLLECTIONS:
            try:
                col = self._get_collection(name)
                stats[name] = col.count()
            except Exception:
                stats[name] = 0
        return stats
