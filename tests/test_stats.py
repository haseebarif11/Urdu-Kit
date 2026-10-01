"""Tests for urdukit.stats module."""

import pytest
from urdukit.stats import text_stats, top_words


def test_text_stats_urdu_script():
    text = "یہ اردو کی پہلی لائن ہے۔ کیا سب ٹھیک ہے؟ قیمت ۱۲۵۰ روپے ہے۔"
    stats = text_stats(text)
    assert stats["word_count"] > 5
    assert stats["unique_word_count"] > 0
    assert 0.0 < stats["lexical_diversity"] <= 1.0
    assert stats["avg_word_length"] > 0
    assert stats["sentence_count"] == 3
    assert stats["urdu_char_count"] > 20
    assert stats["urdu_ratio"] > 0.9
    assert stats["digit_count"] == 4
    assert stats["script"] == "urdu_script"


def test_text_stats_roman_urdu():
    text = "Mera naam Ali hai. Order 1234 kab deliver hoga?"
    stats = text_stats(text)
    assert stats["sentence_count"] == 2
    assert stats["word_count"] >= 8
    assert stats["unique_word_count"] >= 7
    assert 0.0 < stats["lexical_diversity"] <= 1.0
    assert stats["avg_word_length"] > 0
    assert stats["latin_char_count"] > 20
    assert stats["latin_ratio"] > 0.9
    assert stats["digit_count"] == 4
    assert stats["script"] == "roman_urdu"


def test_text_stats_empty():
    stats = text_stats("")
    assert stats["character_count"] == 0
    assert stats["word_count"] == 0
    assert stats["unique_word_count"] == 0
    assert stats["lexical_diversity"] == 0.0
    assert stats["avg_word_length"] == 0.0
    assert stats["sentence_count"] == 0
    assert stats["urdu_char_count"] == 0
    assert stats["latin_char_count"] == 0
    assert stats["digit_count"] == 0
    assert stats["script"] == "unknown"


def test_top_words_roman_urdu():
    text = "bohat acha project hai bohat zabardast project shandar project"
    # With stopwords removed ('hai' is stopword, 'project' repeated 3 times, 'bohat' 2 times)
    top = top_words(text, n=3, remove_stop=True)
    assert len(top) > 0
    assert top[0][0] == "project"
    assert top[0][1] == 3

    # Without stopwords removal
    top_all = top_words(text, n=5, remove_stop=False)
    words_only = [w for w, _ in top_all]
    assert "project" in words_only


def test_top_words_urdu_script():
    text = "پاکستان کا مستقبل روشن ہے پاکستان زندہ باد پاکستان"
    top = top_words(text, n=2, remove_stop=True)
    assert len(top) >= 1
    assert top[0][0] == "پاکستان"
    assert top[0][1] == 3


def test_top_words_edge_cases():
    assert top_words("", n=5) == []
    assert top_words("   ", n=5) == []
    assert top_words("test word", n=0) == []
    assert top_words("test word", n=-1) == []

