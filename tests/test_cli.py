"""Tests for urdukit.cli module."""

import io
import json
import sys
import pytest
from urdukit.cli import main


def test_cli_detect(capsys):
    ret = main(["detect", "کیا حال ہے؟"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert captured == "urdu_script"


def test_cli_normalize(capsys):
    ret = main(["normalize", "kesy ho yaaaar?"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert captured == "kaise ho yaar?"


def test_cli_normalize_digits(capsys):
    ret = main(["normalize", "قیمت ۱۲۵۰ ہے", "--digits", "latin"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert captured == "قیمت 1250 ہے"


def test_cli_transliterate(capsys):
    ret = main(["transliterate", "kya hal hai", "--mode", "to-urdu"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "کیا" in captured


def test_cli_sentiment(capsys):
    ret = main(["sentiment", "bohot acha aur shandar kaam", "--json"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    data = json.loads(captured)
    assert data["label"] == "positive"


def test_cli_stats(capsys):
    ret = main(["stats", "Yeh ek test hai"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    data = json.loads(captured)
    assert data["word_count"] == 4


def test_cli_no_command(capsys):
    ret = main([])
    assert ret == 0


def test_cli_tokenize_words(capsys):
    ret = main(["tokenize", "urdu zaban seekho!", "--remove-punct"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert captured == "urdu zaban seekho"


def test_cli_tokenize_sentences(capsys):
    ret = main(["tokenize", "Yeh pehla jumla hai. Yeh doosra jumla hai.", "--sentences"])
    assert ret == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 2
    assert "pehla jumla" in lines[0]
    assert "doosra jumla" in lines[1]


def test_cli_stopwords(capsys):
    ret = main(["stopwords", "yeh ek achi kitab hai"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "kitab" in captured
    assert "yeh" not in captured.split()


def test_cli_sentiment_plain(capsys):
    ret = main(["sentiment", "bohot acha kaam hai"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "positive" in captured
    assert "(score:" in captured


def test_cli_transliterate_modes(capsys):
    # Test to-roman mode
    ret = main(["transliterate", "کیا حال ہے", "--mode", "to-roman"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "kya" in captured or "haal" in captured

    # Test unified mode
    ret = main(["transliterate", "main invoice send kar raha hoon", "--mode", "unified"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "انوائس" in captured


def test_cli_stats_default(capsys):
    ret = main(["stats", "yeh ek acha jumla hai"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "word_count" in captured
    assert "lexical_diversity" in captured
    assert "unique_word_count" in captured


def test_cli_stats_top_words(capsys):
    ret = main(["stats", "zabardast project zabardast idea", "--top-words", "2"])
    assert ret == 0
    captured = capsys.readouterr().out.strip()
    assert "top_words" in captured
    assert "zabardast" in captured
