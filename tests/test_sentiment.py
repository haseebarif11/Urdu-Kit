"""Tests for urdukit.sentiment module."""

import pytest
from urdukit.sentiment import analyze_sentiment


def test_sentiment_positive_roman_urdu():
    res = analyze_sentiment("yeh bohot achi aur shandar product hai")
    assert res["label"] == "positive"
    assert res["score"] > 0
    assert len(res["positive_words"]) >= 1


def test_sentiment_negative_roman_urdu():
    res = analyze_sentiment("bilkul bakwas aur fazool service hai, bohot kharab experience")
    assert res["label"] == "negative"
    assert res["score"] < 0
    assert "bakwas" in res["negative_words"] or "fazool" in res["negative_words"]


def test_sentiment_positive_urdu_script():
    res = analyze_sentiment("یہ بہت خوبصورت اور عمدہ کتاب ہے، شکریہ")
    assert res["label"] == "positive"
    assert res["score"] > 0
    assert "خوبصورت" in res["positive_words"] or "عمدہ" in res["positive_words"]


def test_sentiment_negative_urdu_script():
    res = analyze_sentiment("بہت برا اور ناقص کام ہے، سخت نقصان ہوا")
    assert res["label"] == "negative"
    assert res["score"] < 0
    assert "برا" in res["negative_words"] or "نقصان" in res["negative_words"]


def test_sentiment_negation_handling():
    # "acha nahi hai" should be classified as negative due to negation inversion
    res = analyze_sentiment("yeh mobile acha nahi hai")
    assert res["label"] == "negative"
    assert res["score"] < 0


def test_sentiment_neutral():
    res = analyze_sentiment("Mera order number 1234 hai")
    assert res["label"] == "neutral"
    assert res["score"] == 0.0
    assert res["positive_words"] == []
    assert res["negative_words"] == []


def test_sentiment_empty():
    res = analyze_sentiment("")
    assert res["label"] == "neutral"
    assert res["score"] == 0.0
