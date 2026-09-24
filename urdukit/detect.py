"""Script detection module for UrduKit.

Classifies text as:
- URDU_SCRIPT: Text written in Urdu / Arabic-derived script (Nastaliq/Naskh)
- ROMAN_URDU: Urdu written in the Latin alphabet
- ENGLISH: English text
- MIXED: Text containing a blend of scripts or languages (e.g. Urdu script + English, or Roman Urdu + English)
- UNKNOWN: Empty, numeric, or unclassifiable text
"""

from enum import Enum
import re
from typing import Set


class Script(str, Enum):
    """Supported script and language categories."""
    URDU_SCRIPT = "urdu_script"
    ROMAN_URDU = "roman_urdu"
    ENGLISH = "english"
    MIXED = "mixed"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value


# Unicode ranges for Urdu and Arabic script characters
# \u0600-\u06FF: Arabic
# \u0750-\u077F: Arabic Supplement (includes extended Urdu characters like ے, ڈ, ڑ, ں)
# \uFB50-\uFDFF: Arabic Presentation Forms-A
# \uFE70-\uFEFF: Arabic Presentation Forms-B
URDU_CHAR_REGEX = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN_CHAR_REGEX = re.compile(r"[A-Za-z]")

# High-confidence Roman Urdu marker words (distinctive Pakistani Roman Urdu vocabulary)
ROMAN_URDU_MARKERS: Set[str] = {
    # Pronouns & demonstratives
    "kya", "kia", "kyun", "kyu", "kese", "kesy", "kaise", "kaisay", "kaisa", "kaisi",
    "mera", "meri", "mere", "tera", "teri", "tere", "apka", "aapka", "apki", "aapki",
    "apke", "aapke", "aap", "hum", "humein", "humain", "hmain", "tum", "tumhara",
    "tumhari", "tumhare", "woh", "wo", "yeh", "ye", "unka", "unki", "unke", "inka",
    "inki", "inke", "inhe", "unhe", "inhain", "unhain", "mujhe", "mjhe", "mujhy",
    "tujhe", "tjhe", "tujhy", "isko", "usko", "inhe", "unhe", "kis", "kise", "kisko",
    
    # Auxiliary verbs & verbs
    "hai", "hain", "hon", "hoon", "tha", "thi", "the", "thay", "hoga", "hogi", "hoge",
    "hogaya", "hogayi", "karna", "krna", "kar", "kr", "karo", "kro", "karen", "krein",
    "raha", "rha", "rahi", "rhi", "rahe", "rhe", "hota", "hoti", "hote", "gaya",
    "gayi", "gae", "gaye", "jana", "jao", "jaein", "aao", "aana", "bolo", "bol",
    "sun", "suno", "dekh", "dekho", "dekha", "samajh", "samjha", "batao", "btao",
    
    # Particles, prepositions, conjunctions
    "nahi", "nahin", "nhi", "nahe", "mat", "bhi", "b", "toh", "to", "aur", "or",
    "lekin", "lekn", "lkn", "magar", "par", "pe", "se", "sy", "ko", "ka", "ki", "ke",
    "kay", "mein", "main", "men", "tak", "saath", "sath", "baad", "pehle", "phir",
    
    # Common adjectives & adverbs
    "acha", "achha", "achhi", "achi", "ache", "achhe", "theek", "thik", "thek",
    "bohot", "boht", "bht", "bahut", "zyada", "ziada", "zyda", "thora", "thoda",
    "kam", "sahi", "galat", "glt", "khubsurat", "khoobsurat", "pyara", "pyari",
    
    # Salutations, discourse markers, conversational
    "shukriya", "shukria", "sukriya", "meherbani", "yaar", "yar", "bhai", "bhae",
    "janab", "sahab", "sahib", "baji", "apa", "chalo", "chal", "sunain", "khair",
    "mashallah", "inshallah", "alhamdulillah", "subhanallah", "jazakallah",
    "zaroor", "zarur", "zroor", "waise", "wese", "halka", "tez", "jaldi"
}

# English marker words (common stopwords & grammar indicators)
ENGLISH_MARKERS: Set[str] = {
    "the", "is", "are", "am", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "doing",
    "a", "an", "this", "that", "these", "those", "there", "their",
    "what", "where", "when", "why", "how", "who", "which", "whose",
    "with", "for", "from", "about", "into", "through", "after", "before",
    "can", "could", "would", "should", "will", "shall", "might", "must",
    "i", "me", "my", "mine", "myself",
    "you", "your", "yours", "yourself", "they", "them", "their", "theirs", "themselves",
    "we", "us", "our", "ours", "ourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "and", "but", "because", "or", "so", "if", "then", "just", "very",
    "please", "thank", "thanks", "hello", "hi", "good", "well", "great",
    "check", "order", "help", "need", "want", "like", "know", "see", "get"
}


def _tokenize_latin(text: str) -> list[str]:
    """Extract lowercased Latin alphanumeric word tokens."""
    return [w.lower() for w in re.findall(r"\b[A-Za-z]+['’]?[A-Za-z]*\b", text)]


def detect_script(text: str) -> Script:
    """Classify input text into Script category.

    Args:
        text: The raw text string to evaluate.

    Returns:
        Script enum: URDU_SCRIPT, ROMAN_URDU, ENGLISH, MIXED, or UNKNOWN.
    """
    if not text or not text.strip():
        return Script.UNKNOWN

    urdu_chars = URDU_CHAR_REGEX.findall(text)
    latin_chars = LATIN_CHAR_REGEX.findall(text)

    urdu_count = len(urdu_chars)
    latin_count = len(latin_chars)

    total_alpha = urdu_count + latin_count

    # If no recognized script alphabetic characters exist (e.g. only numbers/emojis/punctuation)
    if total_alpha == 0:
        return Script.UNKNOWN

    urdu_ratio = urdu_count / total_alpha
    latin_ratio = latin_count / total_alpha

    # 1. Check for mixed Urdu script + Latin script
    # If both Urdu script and Latin script are meaningfully present (each > 15%)
    if urdu_count >= 2 and latin_count >= 2 and urdu_ratio > 0.15 and latin_ratio > 0.15:
        return Script.MIXED

    # 2. Pure or heavily dominant Urdu script
    if urdu_ratio >= 0.85:
        return Script.URDU_SCRIPT

    # 3. If Latin characters dominate, differentiate between ROMAN_URDU, ENGLISH, or MIXED
    words = _tokenize_latin(text)
    if not words:
        if urdu_count > 0:
            return Script.URDU_SCRIPT
        return Script.UNKNOWN

    roman_urdu_hits = 0
    english_hits = 0

    for word in words:
        is_ru = word in ROMAN_URDU_MARKERS
        is_en = word in ENGLISH_MARKERS
        if is_ru and not is_en:
            roman_urdu_hits += 1
        elif is_en and not is_ru:
            english_hits += 1
        elif is_ru and is_en:
            # Ambiguous single tokens like 'or', 'to', 'main'
            # Count towards both or context
            roman_urdu_hits += 0.5
            english_hits += 0.5

    # Check for code-switching / mixed Latin (Roman Urdu + English)
    # E.g. "Order kab deliver hoga? Please check my tracking ID."
    if roman_urdu_hits >= 2 and english_hits >= 2:
        return Script.MIXED

    # If significant Roman Urdu indicators are found
    if roman_urdu_hits > 0 and roman_urdu_hits >= english_hits:
        return Script.ROMAN_URDU

    if english_hits > 0 and english_hits > roman_urdu_hits:
        return Script.ENGLISH

    # If no marker hits, use heuristic pattern check for common Roman Urdu endings/n-grams
    # Pakistani Roman Urdu common phonetics: 'kh', 'gh', 'ch', 'th', 'dh', 'bh', 'jh', 'ain', 'ein', 'oun', 'nay', 'kay'
    ru_pattern = re.compile(r"(kh|gh|ch|th|dh|bh|jh|ain|ein|oun|iya|iye|nay|kay|hon|hoon|rha|rhi|rhe|bht|nhi)\b", re.I)
    ru_matches = len(ru_pattern.findall(text))

    if ru_matches >= 2:
        return Script.ROMAN_URDU

    # Default to ENGLISH if mostly Latin without Urdu cues, or UNKNOWN if very short ambiguous single word
    if len(words) == 1 and roman_urdu_hits == 0 and english_hits == 0:
        return Script.UNKNOWN

    return Script.ENGLISH
