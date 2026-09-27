"""Tests for to_urdu_script pipeline function."""

import pytest
from urdukit import to_urdu_script


def test_mixed_text_with_loanwords_converted():
    """Mixed text with loanwords: convert_loanwords=True should convert loanwords to Urdu script."""
    text = "میرا order cancel کر دیں please, bht dair ho gayi hai"

    # Default is convert_loanwords=True
    res_default = to_urdu_script(text)
    res_explicit = to_urdu_script(text, convert_loanwords=True)

    assert res_default == res_explicit
    # Urdu script content preserved
    assert "میرا" in res_default
    assert "کر" in res_default
    assert "دیں" in res_default
    # Loanwords converted
    assert "آرڈر" in res_default
    assert "کینسل" in res_default
    assert "پلیز" in res_default
    # Roman Urdu transliterated
    assert "بہت" in res_default
    assert "دیر" in res_default
    assert "ہو" in res_default
    assert "گئی" in res_default
    assert "ہے" in res_default

    # No leftover Latin words for recognized loanwords/Roman Urdu
    assert "order" not in res_default
    assert "cancel" not in res_default
    assert "please" not in res_default
    assert "bht" not in res_default


def test_mixed_text_with_loanwords_left_in_latin():
    """Mixed text with loanwords: convert_loanwords=False should leave loanwords in Latin script."""
    text = "میرا order cancel کر دیں please, bht dair ho gayi hai"

    res = to_urdu_script(text, convert_loanwords=False)

    # Urdu script content preserved
    assert "میرا" in res
    assert "کر" in res
    assert "دیں" in res
    # Loanwords kept in Latin script
    assert "order" in res
    assert "cancel" in res
    assert "please" in res
    assert "آرڈر" not in res
    assert "کینسل" not in res
    assert "پلیز" not in res
    # Roman Urdu still transliterated to Urdu script
    assert "بہت" in res
    assert "دیر" in res
    assert "ہو" in res
    assert "گئی" in res
    assert "ہے" in res


def test_unrecognized_english_word_untouched():
    """Unrecognized English words (not loanwords, not Roman Urdu) should remain untouched in both modes."""
    fake_brand = "ZulqarnainTech"
    fake_model = "QuantumWidget"
    text = f"Yeh {fake_brand} ka naya {fake_model} mobile hai"

    # Mode 1: convert_loanwords=True
    res_converted = to_urdu_script(text, convert_loanwords=True)
    assert fake_brand in res_converted
    assert fake_model in res_converted
    assert "یہ" in res_converted
    assert "کا" in res_converted
    assert "موبائل" in res_converted  # 'mobile' is a recognized loanword
    assert "ہے" in res_converted

    # Mode 2: convert_loanwords=False
    res_unconverted = to_urdu_script(text, convert_loanwords=False)
    assert fake_brand in res_unconverted
    assert fake_model in res_unconverted
    assert "یہ" in res_unconverted
    assert "کا" in res_unconverted
    assert "mobile" in res_unconverted  # 'mobile' kept in Latin
    assert "ہے" in res_unconverted


def test_urdu_script_content_never_altered():
    """Urdu script content in the input must never be altered or corrupted."""
    urdu_text = "شکریہ جناب، کیا حال ہے؟ آپ کا دن اچھا گزرے"

    res_true = to_urdu_script(urdu_text, convert_loanwords=True)
    res_false = to_urdu_script(urdu_text, convert_loanwords=False)

    assert res_true == urdu_text
    assert res_false == urdu_text


def test_to_urdu_script_empty_and_special():
    """Empty strings, whitespace, and numeric/punctuation strings should be handled gracefully."""
    assert to_urdu_script("") == ""
    assert to_urdu_script("   ") == "   "
    assert to_urdu_script("12345, 67890!") == "12345, 67890!"
