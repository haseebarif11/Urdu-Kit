"""UrduKit — Python middleware toolkit for Roman Urdu and Urdu script text.

UrduKit handles script detection, spelling normalization, transliteration,
and multilingual semantic embeddings before passing user input to LLMs,
search engines, or NLP models.
"""

from urdukit.detect import Script, detect_script
from urdukit.normalize import normalize, normalize_digits
from urdukit.transliterate import ENGLISH_LOANWORDS, roman_to_urdu, to_urdu_script, urdu_to_roman
from urdukit.tokenize import split_sentences, tokenize_words
from urdukit.embeddings import UrduEmbedder

__version__ = "0.1.0"

__all__ = [
    "Script",
    "detect_script",
    "normalize",
    "normalize_digits",
    "ENGLISH_LOANWORDS",
    "roman_to_urdu",
    "to_urdu_script",
    "urdu_to_roman",
    "split_sentences",
    "tokenize_words",
    "UrduEmbedder",
    "__version__",
]

