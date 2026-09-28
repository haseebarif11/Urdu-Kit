"""Lightweight sentiment analysis module for UrduKit.

Provides rule-based and lexicon-driven polarity classification for
Urdu Script and Roman Urdu without requiring heavy machine learning dependencies.
"""

import re
from typing import Dict, List, Set, Union

from urdukit.tokenize import tokenize_words

# Urdu Script Positive Lexicon
POSITIVE_WORDS_URDU: Set[str] = {
    "اچھا", "اچھی", "اچھے", "بہترین", "عمدہ", "شاندار", "خوبصورت", "پیارا", "پیاری",
    "کامیاب", "خوشی", "خوش", "محبت", "پسند", "مبارک", "شکریہ", "شکر", "آسان",
    "راحت", "اطمینان", "مفید", "فائدہ", "سلامتی", "تحفہ", "شریف", "ایماندار",
    "لذیذ", "مزےدار", "کمال", "زبردست", "فٹ", "جیت", "مقبول"
}

# Urdu Script Negative Lexicon
NEGATIVE_WORDS_URDU: Set[str] = {
    "برا", "بری", "برے", "خراب", "بدترین", "بکواس", "فضول", "غلط", "نقصان",
    "مصیبت", "پریشانی", "دھوکہ", "جھوٹ", "دکھ", "غم", "مایوس", "نفرت", "ناکام",
    "بیمار", "مشکل", "خطرناک", "درد", "چوری", "ظلم", "افسوس", "خسارہ", "بدبودار"
}

# Roman Urdu Positive Lexicon
POSITIVE_WORDS_ROMAN: Set[str] = {
    "acha", "achi", "ache", "achha", "achhi", "achhe", "behtareen", "behtreen",
    "zabardast", "zbrdst", "shandar", "khoobsurat", "khubsurat", "pyara", "pyari",
    "kamal", "fit", "shukriya", "shukria", "sukriya", "khush", "khushi", "pasand",
    "lajawab", "mubarak", "faida", "aasan", "itminan", "sukoon", "mohabat", "pyar",
    "best", "good", "great", "excellent", "love", "amazing", "super"
}

# Roman Urdu Negative Lexicon
NEGATIVE_WORDS_ROMAN: Set[str] = {
    "bura", "buri", "bure", "kharab", "khrab", "bakwas", "bkwas", "fazool", "fzul",
    "ghalat", "galat", "glt", "badtameez", "dhoka", "jhoot", "nafrat", "nakaam",
    "nuksan", "nuqsan", "pareshan", "pareshani", "afsos", "mushkil", "dard", "gham",
    "khatarnak", "zaleel", "bekar", "ghatia", "bad", "worst", "terrible", "poor", "hate"
}

# Negation indicators
NEGATION_WORDS: Set[str] = {
    "nahi", "nahin", "nhi", "nahe", "na", "mat", "mtt",
    "نہیں", "نہ", "مت", "نا"
}

# Intensifier markers (boost score)
INTENSIFIER_WORDS: Set[str] = {
    "bohot", "boht", "bht", "bahut", "zyada", "ziada", "zyda", "intehai",
    "بہت", "زیادہ", "انتہائی"
}


def analyze_sentiment(text: str) -> Dict[str, Union[str, float, List[str]]]:
    """Analyze sentiment polarity of Urdu script or Roman Urdu text.

    Args:
        text: Input text string in Urdu script, Roman Urdu, or mixed English.

    Returns:
        Dictionary containing:
        - 'label': 'positive', 'negative', or 'neutral'
        - 'score': Polarity score normalized between -1.0 and 1.0
        - 'positive_words': List of matched positive tokens
        - 'negative_words': List of matched negative tokens
    """
    if not text or not text.strip():
        return {
            "label": "neutral",
            "score": 0.0,
            "positive_words": [],
            "negative_words": [],
        }

    tokens = tokenize_words(text, remove_punct=True)
    lower_tokens = [t.lower() for t in tokens]

    positive_matches: List[str] = []
    negative_matches: List[str] = []

    pos_score = 0.0
    neg_score = 0.0

    num_tokens = len(lower_tokens)

    for i, token in enumerate(lower_tokens):
        # Look behind up to 2 tokens and look ahead up to 2 tokens for negation or intensifier
        # In Urdu, negation can precede ('nahi acha') or follow ('acha nahi hai')
        is_negated = False
        multiplier = 1.0

        # Check lookbehind
        for lookback in (1, 2):
            if i - lookback >= 0:
                prev_token = lower_tokens[i - lookback]
                if prev_token in NEGATION_WORDS:
                    is_negated = True
                elif prev_token in INTENSIFIER_WORDS:
                    multiplier = 1.5

        # Check lookahead for negation
        for lookahead in (1, 2):
            if i + lookahead < num_tokens:
                next_token = lower_tokens[i + lookahead]
                if next_token in NEGATION_WORDS:
                    is_negated = True


        is_pos = token in POSITIVE_WORDS_URDU or token in POSITIVE_WORDS_ROMAN
        is_neg = token in NEGATIVE_WORDS_URDU or token in NEGATIVE_WORDS_ROMAN

        if is_pos:
            if is_negated:
                # Inverted by negation (e.g. "acha nahi hai" -> negative)
                neg_score += 1.0 * multiplier
                negative_matches.append(f"not_{token}")
            else:
                pos_score += 1.0 * multiplier
                positive_matches.append(token)

        elif is_neg:
            if is_negated:
                # Inverted by negation (e.g. "bura nahi hai" -> positive)
                pos_score += 0.8 * multiplier
                positive_matches.append(f"not_{token}")
            else:
                neg_score += 1.0 * multiplier
                negative_matches.append(token)

    total_hits = pos_score + neg_score
    if total_hits == 0:
        return {
            "label": "neutral",
            "score": 0.0,
            "positive_words": [],
            "negative_words": [],
        }

    # Normalized score between -1.0 and 1.0
    net_score = (pos_score - neg_score) / total_hits
    rounded_score = round(net_score, 3)

    if rounded_score > 0.15:
        label = "positive"
    elif rounded_score < -0.15:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": rounded_score,
        "positive_words": positive_matches,
        "negative_words": negative_matches,
    }
