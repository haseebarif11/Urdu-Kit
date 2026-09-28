"""Tests for urdukit.stats module."""

import pytest
from urdukit.stats import text_stats


def test_text_stats_urdu_script():
    text = "یہ اردو کی پہلی لائن ہے۔ کیا سب ٹھیک ہے؟ قیمت ۱۲۵۰ روپے ہے۔"
    stats = text_stats(text)
    assert stats["word_count"] > 5
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
    assert stats["latin_char_count"] > 20
    assert stats["latin_ratio"] > 0.9
    assert stats["digit_count"] == 4
    assert stats["script"] == "roman_urdu"


def test_text_stats_empty():
    stats = text_stats("")
    assert stats["character_count"] == 0
    assert stats["word_count"] == 0
    assert stats["sentence_count"] == 0
    assert stats["urdu_char_count"] == 0
    assert stats["latin_char_count"] == 0
    assert stats["digit_count"] == 0
    assert stats["script"] == "unknown"
