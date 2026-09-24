"""Tests for urdukit.embeddings module."""

import pytest
from urdukit.embeddings import UrduEmbedder


def test_embedder_initialization():
    embedder = UrduEmbedder(model_name="intfloat/multilingual-e5-small")
    assert embedder.model_name == "intfloat/multilingual-e5-small"
    assert embedder.auto_normalize is True
    assert embedder._model is None  # Lazy loading check


def test_missing_dependency_informative_error(monkeypatch):
    embedder = UrduEmbedder()
    # Simulate missing sentence-transformers package
    import sys

    # Save original modules if present
    orig_st = sys.modules.get("sentence_transformers")
    try:
        sys.modules["sentence_transformers"] = None  # Force ImportError on import
        with pytest.raises(ImportError) as exc_info:
            embedder._load_model()
        assert "sentence-transformers is required" in str(exc_info.value)
        assert "pip install urdukit[embeddings]" in str(exc_info.value)
    finally:
        if orig_st is not None:
            sys.modules["sentence_transformers"] = orig_st
        else:
            sys.modules.pop("sentence_transformers", None)
