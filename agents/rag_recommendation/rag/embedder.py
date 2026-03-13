"""
Embedder

Embedding pipeline using sentence-transformers for vectorizing trending content.
Uses the all-MiniLM-L6-v2 model for fast, high-quality embeddings.
"""

import hashlib
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Lazy-load sentence-transformers to avoid slow import on startup
_model = None
_model_name = "all-MiniLM-L6-v2"


def _get_model():
    """Lazy-load the sentence-transformers model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {_model_name}")
            _model = SentenceTransformer(_model_name)
            logger.info("Embedding model loaded.")
        except ImportError:
            logger.error(
                "sentence-transformers not installed. "
                "Run: pip install sentence-transformers"
            )
            raise
    return _model


class Embedder:
    """
    Embedding pipeline for trending content.

    Features:
    - Lazy model loading
    - Batch embedding for efficiency
    - In-memory cache to avoid re-embedding identical text

    Usage:
        embedder = Embedder()
        vectors = embedder.embed_texts(["AI agents are ...", "RAG systems ..."])
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        global _model_name
        _model_name = model_name
        self._cache: Dict[str, List[float]] = {}

    @property
    def dimension(self) -> int:
        """Embedding dimension (384 for MiniLM-L6-v2)."""
        model = _get_model()
        return model.get_sentence_embedding_dimension()

    def embed_texts(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Embed a list of texts.

        Args:
            texts: Texts to embed.
            batch_size: Batch size for the model.

        Returns:
            List of embedding vectors (float lists).
        """
        if not texts:
            return []

        # Separate cached vs uncached
        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_indices: List[int] = []
        uncached_texts: List[str] = []

        for i, text in enumerate(texts):
            key = self._cache_key(text)
            if key in self._cache:
                results[i] = self._cache[key]
            else:
                uncached_indices.append(i)
                uncached_texts.append(text)

        # Embed uncached texts
        if uncached_texts:
            model = _get_model()
            embeddings = model.encode(
                uncached_texts,
                batch_size=batch_size,
                show_progress_bar=False,
                normalize_embeddings=True,
            )

            for idx, emb in zip(uncached_indices, embeddings):
                vec = emb.tolist()
                results[idx] = vec
                self._cache[self._cache_key(uncached_texts[uncached_indices.index(idx)])] = vec

        return [r for r in results if r is not None]

    def embed_single(self, text: str) -> List[float]:
        """Embed a single text string."""
        return self.embed_texts([text])[0]

    def clear_cache(self):
        """Clear the embedding cache."""
        self._cache.clear()

    def _cache_key(self, text: str) -> str:
        """Generate a cache key for a text."""
        return hashlib.md5(text.encode()).hexdigest()
