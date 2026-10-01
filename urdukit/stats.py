"""Text statistics and analytics module for UrduKit.

Computes character, word, sentence, and script distribution metrics
for Urdu script, Roman Urdu, and multilingual text.
"""

from collections import Counter
import re
from typing import Any, Dict, List, Tuple

from urdukit.detect import LATIN_CHAR_REGEX, URDU_CHAR_REGEX, detect_script
from urdukit.stopwords import is_stopword
from urdukit.tokenize import split_sentences, tokenize_words

DIGIT_REGEX = re.compile(r"[\d۰-۹٠-٩]")


def text_stats(text: str) -> Dict[str, Any]:
    """Calculate linguistic and structural statistics for input text.

    Args:
        text: Input text string to evaluate.

    Returns:
        Dictionary containing:
        - 'character_count': Total characters including whitespace
        - 'word_count': Total word tokens
        - 'unique_word_count': Number of unique words (case-insensitive)
        - 'lexical_diversity': Type-Token Ratio (TTR: unique_words / total_words)
        - 'avg_word_length': Average characters per word token
        - 'sentence_count': Total recognized sentences
        - 'urdu_char_count': Count of Urdu script characters
        - 'latin_char_count': Count of Latin characters
        - 'digit_count': Count of numeric digits (Urdu + Latin)
        - 'urdu_ratio': Ratio of Urdu characters among alphabetic characters (0.0 - 1.0)
        - 'latin_ratio': Ratio of Latin characters among alphabetic characters (0.0 - 1.0)
        - 'script': Detected primary script category ('urdu_script', 'roman_urdu', etc.)
        - 'reading_time_sec': Estimated reading time in seconds (~180 WPM)
    """
    if not text or not text.strip():
        return {
            "character_count": 0,
            "word_count": 0,
            "unique_word_count": 0,
            "lexical_diversity": 0.0,
            "avg_word_length": 0.0,
            "sentence_count": 0,
            "urdu_char_count": 0,
            "latin_char_count": 0,
            "digit_count": 0,
            "urdu_ratio": 0.0,
            "latin_ratio": 0.0,
            "script": "unknown",
            "reading_time_sec": 0,
        }

    char_count = len(text)
    words = tokenize_words(text, remove_punct=True)
    word_count = len(words)
    sentences = split_sentences(text)
    sentence_count = len(sentences)

    normalized_words = [w.lower() for w in words]
    unique_words = set(normalized_words)
    unique_word_count = len(unique_words)
    lexical_diversity = round(unique_word_count / word_count, 3) if word_count > 0 else 0.0
    avg_word_length = round(sum(len(w) for w in words) / word_count, 2) if word_count > 0 else 0.0

    urdu_chars = len(URDU_CHAR_REGEX.findall(text))
    latin_chars = len(LATIN_CHAR_REGEX.findall(text))
    digits = len(DIGIT_REGEX.findall(text))

    total_alpha = urdu_chars + latin_chars
    urdu_ratio = round(urdu_chars / total_alpha, 3) if total_alpha > 0 else 0.0
    latin_ratio = round(latin_chars / total_alpha, 3) if total_alpha > 0 else 0.0

    detected = detect_script(text)

    # Average adult reading speed ~180 words per minute -> 3 words per second
    reading_time_sec = max(1, round(word_count / 3)) if word_count > 0 else 0

    return {
        "character_count": char_count,
        "word_count": word_count,
        "unique_word_count": unique_word_count,
        "lexical_diversity": lexical_diversity,
        "avg_word_length": avg_word_length,
        "sentence_count": sentence_count,
        "urdu_char_count": urdu_chars,
        "latin_char_count": latin_chars,
        "digit_count": digits,
        "urdu_ratio": urdu_ratio,
        "latin_ratio": latin_ratio,
        "script": str(detected),
        "reading_time_sec": reading_time_sec,
    }


def top_words(text: str, n: int = 10, remove_stop: bool = True) -> List[Tuple[str, int]]:
    """Return the most frequent word tokens in text with their occurrences.

    Args:
        text: Input string in Urdu script or Roman Urdu.
        n: Number of top words to return (default: 10).
        remove_stop: If True, filters out Urdu and Roman Urdu stopwords.

    Returns:
        List of (word, count) tuples sorted in descending order of frequency.
    """
    if not text or not text.strip() or n <= 0:
        return []

    words = tokenize_words(text, remove_punct=True)
    if not words:
        return []

    processed = []
    for w in words:
        wl = w.lower()
        if remove_stop and is_stopword(wl):
            continue
        processed.append(wl)

    counter = Counter(processed)
    return counter.most_common(n)
