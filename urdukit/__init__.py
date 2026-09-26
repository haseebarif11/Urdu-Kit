"""UrduKit — Python middleware toolkit for Roman Urdu and Urdu script text.

UrduKit handles script detection, spelling normalization, transliteration,
and multilingual semantic embeddings before passing user input to LLMs,
search engines, or NLP models.
"""

from urdukit.detect import Script, detect_script
from urdukit.normalize import normalize
from urdukit.transliterate import ENGLISH_LOANWORDS, roman_to_urdu, urdu_to_roman
from urdukit.embeddings import UrduEmbedder

__version__ = "0.1.0"

__all__ = [
    "Script",
    "detect_script",
    "normalize",
    "ENGLISH_LOANWORDS",
    "roman_to_urdu",
    "urdu_to_roman",
    "UrduEmbedder",
    "__version__",
]
