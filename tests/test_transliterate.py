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


def test_roman_to_urdu_loanwords():
    """Loanwords embedded in Roman Urdu should be rendered with standard Urdu script spellings."""
    res = roman_to_urdu("mera order cancel kr dein")
    assert res == "میرا آرڈر کینسل کر دیں"
    assert "آرڈر" in res
    assert "کینسل" in res


def test_roman_to_urdu_invoice():
    """Invoice and loanwords should be correctly handled and not mangled."""
    res = roman_to_urdu("invoice nahi mili")
    assert res == "انوائس نہیں ملی"
    assert "انوائس" in res
    assert "نہیں" in res
    assert "ملی" in res


def test_english_loanwords_mappings():
    """Verify that all core English loanwords map accurately to conventional Urdu spellings."""
    from urdukit.transliterate import ENGLISH_LOANWORDS

    expected = {
        "order": "آرڈر",
        "invoice": "انوائس",
        "check": "چیک",
        "please": "پلیز",
        "cancel": "کینسل",
        "call": "کال",
        "message": "میسج",
        "phone": "فون",
        "email": "ای میل",
        "account": "اکاؤنٹ",
        "password": "پاسورڈ",
        "internet": "انٹرنیٹ",
        "mobile": "موبائل",
        "office": "آفس",
        "meeting": "میٹنگ",
        "project": "پراجیکٹ",
        "price": "پرائس",
        "delivery": "ڈیلیوری",
        "address": "ایڈریس",
    }
    for word, expected_urdu in expected.items():
        assert ENGLISH_LOANWORDS[word] == expected_urdu
        assert roman_to_urdu(word) == expected_urdu
        assert roman_to_urdu(word.upper()) == expected_urdu


def test_roman_to_urdu_unrecognized_english_word():
    """Unrecognized English words not in loanwords and not Roman Urdu should remain untouched."""
    # Embedded unrecognized English word in Roman Urdu context
    res = roman_to_urdu("yeh algorithm bohot acha hai")
    assert "algorithm" in res
    assert res == "یہ algorithm بہت اچھا ہے"

    # Standalone unrecognized Latin words
    assert roman_to_urdu("blockchain") == "blockchain"
    assert roman_to_urdu("defective return policy") == "defective return policy"

