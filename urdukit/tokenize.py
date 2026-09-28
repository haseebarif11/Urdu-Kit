"""Tokenization module for UrduKit.

Provides sentence segmentation and word tokenization tailored for
Urdu script, Roman Urdu, and mixed code-switched text.
"""

import re
from typing import List

# Sentence end delimiters in Urdu and Latin scripts:
# \u06D4: Urdu full stop / Khatma (۔)
# \u061F: Urdu question mark (؟)
# !: Exclamation mark
# ?: Standard question mark
# .: Standard full stop
# Regex to match words (Urdu, Latin, and digits) or punctuation marks
WORD_TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]")

# Standalone punctuation detector
PUNCT_PATTERN = re.compile(r"^[^\w\s]+$")


def split_sentences(text: str) -> List[str]:
    """Split input text into sentences respecting Urdu and Latin punctuation.

    Recognizes Urdu full stops (۔), Urdu question marks (؟), standard
    Latin punctuation (!, ?, .), and newlines.

    Args:
        text: Input text string in Urdu script, Roman Urdu, or mixed.

    Returns:
        List of non-empty, stripped sentence strings.
    """
    if not text or not text.strip():
        return []

    # Split on sentence boundary punctuation followed by space or newline,
    # or periods following a word
    raw_sentences = re.split(
        r"(?<=[۔؟!?])\s+|\n+|(?<=[a-zA-Z\u0600-\u06FF]\.)\s+",
        text,
    )

    sentences: List[str] = []
    for s in raw_sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        # Also handle sentences attached without spaces e.g. "بات ہے۔دوسری بات"
        sub_sentences = re.split(r"(?<=[۔؟!?])(?=[a-zA-Z\u0600-\u06FF])", s_clean)
        for sub in sub_sentences:
            sub_clean = sub.strip()
            if sub_clean:
                sentences.append(sub_clean)

    return sentences


def tokenize_words(text: str, remove_punct: bool = False) -> List[str]:
    """Tokenize text into words and punctuation tokens.

    Supports Urdu script words, Roman Urdu/English words, numbers, and
    Urdu/Latin punctuation marks.

    Args:
        text: Input text string to tokenize.
        remove_punct: If True, strips out standalone punctuation tokens
            (such as ،, ؛, ۔, ؟, !, ., etc.). Defaults to False.

    Returns:
        List of token strings.
    """
    if not text or not text.strip():
        return []

    tokens = WORD_TOKEN_PATTERN.findall(text)

    if remove_punct:
        tokens = [t for t in tokens if not PUNCT_PATTERN.match(t)]

    return tokens
