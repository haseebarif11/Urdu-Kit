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


def test_rank_sorts_and_respects_top_k():
    embedder = UrduEmbedder(auto_normalize=False)
    fake_model = MagicMock()

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
                vecs.append([1.0, 0.0])
        return np.array(vecs)

    fake_model.encode.side_effect = fake_encode
    embedder._model = fake_model

    query = "urdu zaban seekhein"
    # Provide 4 candidate documents where original positions are:
    # index 0: unrelated (score 0.0)
    # index 1: exact match (score 1.0)
    # index 2: partial match (score 0.6)
    # index 3: another unrelated (score 0.0)
    documents = [
        "unrelated document about astronomy",
        "urdu zaban seekhein exact",
        "partial match urdu seekhein",
        "another unrelated document",
    ]

    top_k = 2
    results = embedder.rank(query, documents, top_k=top_k)

    # Exactly top_k results are returned
    assert len(results) == top_k

    # Results are sorted highest-similarity-first
    assert results[0][2] >= results[1][2]

    # Verify tuple structure (original_index, document_text, score) and index mapping
    orig_idx_0, doc_text_0, score_0 = results[0]
    assert orig_idx_0 == 1
    assert doc_text_0 == documents[1]
    assert pytest.approx(1.0, abs=0.01) == score_0

    orig_idx_1, doc_text_1, score_1 = results[1]
    assert orig_idx_1 == 2
    assert doc_text_1 == documents[2]
    assert pytest.approx(0.6, abs=0.01) == score_1


def test_similarity_empty_documents():
    embedder = UrduEmbedder()
    fake_model = MagicMock()
    embedder._model = fake_model

    scores = embedder.similarity("kuch bhi query", [])
    assert scores == []
    fake_model.encode.assert_not_called()


def test_rank_empty_documents():
    embedder = UrduEmbedder()
    fake_model = MagicMock()
    embedder._model = fake_model

    results = embedder.rank("kuch bhi query", [])
    assert results == []
    fake_model.encode.assert_not_called()


def test_rank_top_k_larger_than_documents():
    embedder = UrduEmbedder(auto_normalize=False)
    fake_model = MagicMock()

    def fake_encode(texts, **kwargs):
        vecs = []
        for t in texts:
            if "high" in t:
                vecs.append([1.0, 0.0])
            elif "low" in t:
                vecs.append([0.0, 1.0])
            else:
                vecs.append([1.0, 0.0])
        return np.array(vecs)

    fake_model.encode.side_effect = fake_encode
    embedder._model = fake_model

    documents = ["low relevance doc", "high relevance doc"]
    results = embedder.rank("query", documents, top_k=10)

    # Returns all available docs even if top_k is larger
    assert len(results) == 2
    assert results[0][0] == 1
    assert results[0][1] == "high relevance doc"
    assert results[1][0] == 0
    assert results[1][1] == "low relevance doc"
