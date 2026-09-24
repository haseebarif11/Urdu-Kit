"""Tests for urdukit.normalize module."""

import pytest
from urdukit.normalize import normalize, reduce_elongation, normalize_urdu_script


def test_normalize_roman_urdu_variants():
    # Test canonicalization of common variants
    assert normalize("kesy ho aap") == "kaise ho aap"
    assert normalize("kese ho aap") == "kaise ho aap"
    assert normalize("kaisay ho aap") == "kaise ho aap"

    assert normalize("kia hal hai") == "kya hal hai"
    assert normalize("nhi yaar") == "nahi yaar"
    assert normalize("bht shukria") == "bohot shukriya"
    assert normalize("mjhe btao") == "mujhe batao"
    assert normalize("hmain help chahiye") == "humein help chahiye"


def test_normalize_elongation():
    # Test collapse of repeated characters
    assert normalize("bohooooot shukriya") == "bohot shukriya"
    assert normalize("yaaaaar suno") == "yaar suno"
    assert normalize("theeeek hai") == "theek hai"
    assert normalize("plzzzzz reply") == "please reply"


def test_normalize_casing_preservation():
    # Test uppercase and capitalization retention
    assert normalize("Kesy ho") == "Kaise ho"
    assert normalize("NHI") == "NAHI"


def test_normalize_urdu_script():
    # Test Arabic Kaf -> Urdu Keheh (\u0643 -> \u06A9)
    arabic_kaf_text = "كتاب"
    expected_urdu = "کتاب"
    assert normalize(arabic_kaf_text) == expected_urdu

    # Test Arabic Yeh -> Urdu Yeh (\u064A -> \u06CC)
    arabic_yeh_text = "علي"
    expected_urdu_yeh = "علی"
    assert normalize(arabic_yeh_text) == expected_urdu_yeh

    # Test Arabic Tatweel (Kashida) removal (\u0640)
    kashida_text = "شـــکـــریہ"
    assert normalize(kashida_text) == "شکریہ"

    # Test diacritics removal if flag is set
    text_with_aerab = "کِتَابٌ"
    assert normalize(text_with_aerab, remove_diacritics=True) == "کتاب"


def test_normalize_whitespace():
    assert normalize("  kya   hal   hai   ") == "kya hal hai"
    assert normalize("") == ""
    assert normalize("   ") == ""
