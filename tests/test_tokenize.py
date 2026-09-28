"""Tests for urdukit.tokenize module."""

import pytest
from urdukit.tokenize import split_sentences, tokenize_words


def test_split_sentences_urdu_script():
    text = "یہ پہلا جملہ ہے۔ کیا آپ خیریت سے ہیں؟ جی ہاں، سب ٹھیک ہے۔"
    sentences = split_sentences(text)
    assert len(sentences) == 3
    assert sentences[0] == "یہ پہلا جملہ ہے۔"
    assert sentences[1] == "کیا آپ خیریت سے ہیں؟"
    assert sentences[2] == "جی ہاں، سب ٹھیک ہے۔"


def test_split_sentences_roman_urdu():
    text = "Mera naam Ali hai. Aap ka kya naam hai? Bohot shukriya!"
    sentences = split_sentences(text)
    assert len(sentences) == 3
    assert sentences[0] == "Mera naam Ali hai."
    assert sentences[1] == "Aap ka kya naam hai?"
    assert sentences[2] == "Bohot shukriya!"


def test_split_sentences_newlines():
    text = "Pehla paragraph\nDoosra sentence.\n\n\nTeesri line"
    sentences = split_sentences(text)
    assert len(sentences) == 3
    assert sentences[0] == "Pehla paragraph"
    assert sentences[1] == "Doosra sentence."
    assert sentences[2] == "Teesri line"


def test_split_sentences_empty_or_whitespace():
    assert split_sentences("") == []
    assert split_sentences("   \n\t  ") == []


def test_tokenize_words_with_punct():
    text = "کیا حال ہے؟ سب ٹھیک ہے، شکر ہے۔"
    tokens = tokenize_words(text, remove_punct=False)
    assert "کیا" in tokens
    assert "حال" in tokens
    assert "ہے" in tokens
    assert "؟" in tokens
    assert "،" in tokens
    assert "۔" in tokens


def test_tokenize_words_remove_punct():
    text = "کیا حال ہے؟ سب ٹھیک ہے، شکر ہے۔"
    tokens = tokenize_words(text, remove_punct=True)
    assert "؟" not in tokens
    assert "،" not in tokens
    assert "۔" not in tokens
    assert tokens == ["کیا", "حال", "ہے", "سب", "ٹھیک", "ہے", "شکر", "ہے"]


def test_tokenize_words_mixed_and_numbers():
    text = "Order 1250 روپے ka hai! Please check."
    tokens = tokenize_words(text, remove_punct=True)
    assert tokens == ["Order", "1250", "روپے", "ka", "hai", "Please", "check"]


def test_tokenize_words_empty():
    assert tokenize_words("") == []
    assert tokenize_words("   ") == []
