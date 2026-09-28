"""Tests for urdukit.stopwords module."""

import pytest
from urdukit.stopwords import (
    get_stopwords,
    is_stopword,
    remove_stopwords,
    URDU_SCRIPT_STOPWORDS,
    ROMAN_URDU_STOPWORDS,
)


def test_get_stopwords_categories():
    urdu_sw = get_stopwords("urdu_script")
    assert "کا" in urdu_sw
    assert "ہے" in urdu_sw
    assert "ka" not in urdu_sw

    roman_sw = get_stopwords("roman_urdu")
    assert "ka" in roman_sw
    assert "hai" in roman_sw
    assert "کا" not in roman_sw

    all_sw = get_stopwords("all")
    assert "کا" in all_sw
    assert "ka" in all_sw

    with pytest.raises(ValueError):
        get_stopwords("invalid_category")


def test_is_stopword():
    assert is_stopword("اور") is True
    assert is_stopword("پاکستان") is False
    assert is_stopword("aur") is True
    assert is_stopword("laptop") is False
    assert is_stopword("") is False


def test_remove_stopwords_urdu_script():
    text = "یہ ایک خوبصورت کتاب ہے"
    # "یہ", "ایک", "ہے" are stopwords; "خوبصورت", "کتاب" are content words
    filtered = remove_stopwords(text, lang="urdu_script")
    assert "خوبصورت" in filtered
    assert "کتاب" in filtered
    assert "یہ" not in filtered
    assert "ہے" not in filtered


def test_remove_stopwords_roman_urdu():
    text = "yeh ek bohot achi kitab hai"
    # "yeh", "ek", "hai" are stopwords
    filtered = remove_stopwords(text, lang="roman_urdu")
    assert "achi" in filtered
    assert "kitab" in filtered
    assert "yeh" not in filtered
    assert "hai" not in filtered


def test_remove_stopwords_auto():
    # Urdu script auto detection
    urdu_text = "پاکستان کا دارالحکومت اسلام آباد ہے"
    res_urdu = remove_stopwords(urdu_text)
    assert "پاکستان" in res_urdu
    assert "دارالحکومت" in res_urdu
    assert "اسلام" in res_urdu
    assert "آباد" in res_urdu
    assert "کا" not in res_urdu
    assert "ہے" not in res_urdu

    # Roman Urdu auto detection
    roman_text = "order cancel karne ka tareeqa kya hai"
    res_roman = remove_stopwords(roman_text)
    assert "order" in res_roman
    assert "cancel" in res_roman
    assert "tareeqa" in res_roman
    tokens_res = res_roman.split()
    assert "ka" not in tokens_res
    assert "kya" not in tokens_res
    assert "hai" not in tokens_res


def test_remove_stopwords_empty():
    assert remove_stopwords("") == ""
    assert remove_stopwords("   ") == ""
