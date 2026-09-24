"""Tests for urdukit.detect module."""

import pytest
from urdukit.detect import Script, detect_script


def test_detect_urdu_script():
    examples = [
        "کیا حال ہے آپ کا؟",
        "پاکستان ایک خوبصورت ملک ہے۔",
        "شکریہ، مجھے سمجھ آ گیا ہے۔",
        "السلام علیکم، میں آپ کی کیا مدد کر سکتا ہوں؟",
    ]
    for text in examples:
        assert detect_script(text) == Script.URDU_SCRIPT, f"Failed on: {text}"


def test_detect_roman_urdu():
    examples = [
        "kya hal hai aapka?",
        "kesy ho bhai?",
        "mera order kab deliver hoga",
        "bht shukriya janab",
        "mujhe samajh nahi aa raha",
        "ap kaise hain",
        "woh kal wapas aayega",
    ]
    for text in examples:
        assert detect_script(text) == Script.ROMAN_URDU, f"Failed on: {text}"


def test_detect_english():
    examples = [
        "What is the status of my order?",
        "Can you please help me with my account?",
        "This product is really great and fast.",
        "Thank you so much for the update.",
    ]
    for text in examples:
        assert detect_script(text) == Script.ENGLISH, f"Failed on: {text}"


def test_detect_mixed_script():
    # Urdu script + English text
    assert detect_script("میرا order cancel کر دیں") == Script.MIXED
    assert detect_script("Ye product بالکل بیکار ہے, total waste of money") == Script.MIXED
    # Code-switching Roman Urdu + English
    assert detect_script("Please check my tracking ID, order kab tak deliver hoga?") == Script.MIXED


def test_detect_unknown():
    assert detect_script("") == Script.UNKNOWN
    assert detect_script("    ") == Script.UNKNOWN
    assert detect_script("1234567890") == Script.UNKNOWN
    assert detect_script("!@#$%^&*()_+{}[]:\"<>?,./") == Script.UNKNOWN
    assert detect_script("😀 🚀 💯") == Script.UNKNOWN
