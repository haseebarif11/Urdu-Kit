"""Semantic embeddings module for UrduKit.

Provides a thin, optimized wrapper around multilingual embedding models
(such as 'intfloat/multilingual-e5-small') for semantic search, retrieval,
and clustering across Urdu script, Roman Urdu, and English.
"""

from typing import List, Optional, Tuple, Union


class UrduEmbedder:
    """Multilingual embedder optimized for Urdu and Roman Urdu.

    Lazily loads the underlying transformer model upon first call.
    Automatically normalizes Roman Urdu text variants prior to embedding
    to maximize semantic alignment.
    """

    def __init__(
        self,
        model_name: str = "intfloat/multilingual-e5-small",
        device: Optional[str] = None,
        auto_normalize: bool = True,
    ):
        """Initialize the UrduEmbedder.

        Args:
            model_name: Hugging Face model identifier.
                        Default: 'intfloat/multilingual-e5-small' (fast, lightweight, highly accurate for low-resource languages).
            device: 'cpu', 'cuda', 'mps', or None (auto-detect).
            auto_normalize: If True, passes texts through urdukit.normalize() before computing embeddings.
        """
        self.model_name = model_name
        self.device = device
        self.auto_normalize = auto_normalize
        self._model = None

    def _load_model(self):
        """Lazy load sentence_transformers."""
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required to use UrduEmbedder.\n"
                "Install it with: pip install urdukit[embeddings] or pip install sentence-transformers"
            ) from exc

        self._model = SentenceTransformer(self.model_name, device=self.device)
        return self._model

    def embed(
        self,
        texts: Union[str, List[str]],
        is_query: bool = False,
        batch_size: int = 32,
    ):
        """Compute dense vector embeddings for input text(s).

        Args:
            texts: Single string or list of text strings.
            is_query: If True and using an e5 model, prefixes with 'query: ' for asymmetric retrieval.
            batch_size: Batch size for model inference.

        Returns:
            numpy.ndarray of shape (N, embedding_dim) or (embedding_dim,).
        """
        model = self._load_model()

        single_input = isinstance(texts, str)
        text_list = [texts] if single_input else list(texts)

        # Preprocessing: normalize spelling variations if enabled
        if self.auto_normalize:
            from urdukit.normalize import normalize
            text_list = [normalize(t) for t in text_list]

        # e5 models recommend 'query: ' or 'passage: ' prefixes for asymmetric search
        is_e5 = "e5" in self.model_name.lower()
        if is_e5:
            prefix = "query: " if is_query else "passage: "
            text_list = [f"{prefix}{t}" for t in text_list]

        embeddings = model.encode(
            text_list,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        return embeddings[0] if single_input else embeddings

    def similarity(self, query: str, documents: List[str]) -> List[float]:
        """Compute cosine similarity between a query and a list of documents.

        Args:
            query: The search query (can be in Roman Urdu or Urdu script).
            documents: Candidate documents to compare against.

        Returns:
            List of float similarity scores between -1.0 and 1.0.
        """
        if not documents:
            return []

        import numpy as np

        query_vec = self.embed(query, is_query=True)
        doc_vecs = self.embed(documents, is_query=False)

        # Since embeddings are normalized to unit length, cosine similarity is the dot product
        scores = np.dot(doc_vecs, query_vec)
        return [float(s) for s in scores]

    def rank(
        self, query: str, documents: List[str], top_k: int = 5
    ) -> List[Tuple[int, str, float]]:
        """Rank candidate documents by relevance to a query.

        Args:
            query: Search query.
            documents: List of candidate texts.
            top_k: Maximum number of ranked results to return.

        Returns:
            List of tuples: (original_index, document_text, similarity_score)
            sorted from highest to lowest similarity.
        """
        scores = self.similarity(query, documents)
        scored_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )

        results = []
        for idx in scored_indices[:top_k]:
            results.append((idx, documents[idx], scores[idx]))

        return results
