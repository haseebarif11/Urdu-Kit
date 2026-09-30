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
