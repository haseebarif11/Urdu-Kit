"""Tests for urdukit.transliterate module."""

import pytest
from urdukit.transliterate import roman_to_urdu, urdu_to_roman


def test_roman_to_urdu_lexicon():
    assert roman_to_urdu("kya") == "کیا"
    assert roman_to_urdu("kaise") == "کیسے"
    assert roman_to_urdu("nahi") == "نہیں"
    assert roman_to_urdu("shukriya") == "شکریہ"
    assert roman_to_urdu("theek") == "ٹھیک"


def test_roman_to_urdu_phrases():
    res = roman_to_urdu("kya hal hai")
    assert "کیا" in res
    assert "ہے" in res


def test_urdu_to_roman_lexicon():
    assert urdu_to_roman("کیا") == "kya"
    assert urdu_to_roman("کیسے") == "kaise"
    assert urdu_to_roman("نہیں") == "nahi"
    assert urdu_to_roman("شکریہ") == "shukriya"
    assert urdu_to_roman("ٹھیک") == "theek"


def test_transliterate_empty():
    assert roman_to_urdu("") == ""
    assert urdu_to_roman("") == ""
