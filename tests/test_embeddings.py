from unittest.mock import MagicMock
import numpy as np
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


def test_auto_normalize_applied_before_embedding():
    embedder = UrduEmbedder(auto_normalize=True)
    fake_model = MagicMock()
    fake_model.encode.side_effect = lambda texts, **kwargs: np.zeros((len(texts), 4))
    embedder._model = fake_model

    unnormalized_text = "kesyyy hooo yaaaar"
    embedder.embed(unnormalized_text)

    assert fake_model.encode.called
    call_args, _ = fake_model.encode.call_args
    passed_texts = call_args[0]
    assert len(passed_texts) == 1
    assert "kaise" in passed_texts[0]
    assert "kesyyy" not in passed_texts[0]


def test_e5_query_passage_prefixing():
    embedder = UrduEmbedder(
        model_name="intfloat/multilingual-e5-small", auto_normalize=False
    )
    fake_model = MagicMock()
    fake_model.encode.side_effect = lambda texts, **kwargs: np.zeros((len(texts), 4))
    embedder._model = fake_model

    sample_text = "urdu zaban ki tareekh"

    embedder.embed(sample_text, is_query=True)
    assert fake_model.encode.call_args[0][0][0].startswith("query: ")
    assert fake_model.encode.call_args[0][0][0] == "query: urdu zaban ki tareekh"

    embedder.embed(sample_text, is_query=False)
    assert fake_model.encode.call_args[0][0][0].startswith("passage: ")
    assert fake_model.encode.call_args[0][0][0] == "passage: urdu zaban ki tareekh"


def test_similarity_scores_correct():
    embedder = UrduEmbedder(auto_normalize=False)
    fake_model = MagicMock()

    # Predefined normalized unit vectors (dim=2):
    # Query: [1.0, 0.0]
    # Exact match: [1.0, 0.0] -> cosine similarity = 1.0
    # Unrelated (orthogonal): [0.0, 1.0] -> cosine similarity = 0.0
    # Partial match: [0.6, 0.8] -> cosine similarity = 0.6
    def fake_encode(texts, **kwargs):
        vecs = []
        for t in texts:
            if "exact" in t:
                vecs.append([1.0, 0.0])
            elif "unrelated" in t:
                vecs.append([0.0, 1.0])
            elif "partial" in t:
                vecs.append([0.6, 0.8])
            else:
                # Query text
                vecs.append([1.0, 0.0])
        return np.array(vecs)

    fake_model.encode.side_effect = fake_encode
    embedder._model = fake_model

    query = "urdu zaban seekhein"
    documents = [
        "urdu zaban seekhein exact",
        "unrelated document about astronomy",
        "partial match urdu seekhein",
    ]

    scores = embedder.similarity(query, documents)

    assert len(scores) == 3
    assert pytest.approx(1.0, abs=0.01) == scores[0]
    assert pytest.approx(0.0, abs=0.01) == scores[1]
    assert pytest.approx(0.6, abs=0.01) == scores[2]
