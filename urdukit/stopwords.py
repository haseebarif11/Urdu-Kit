"""Stopwords module for UrduKit.

Provides comprehensive stopword sets and filtering utilities for
Urdu Script and Roman Urdu text processing (IR, search indexing, TF-IDF, LLM prompt optimization).
"""

import re
from typing import Set

from urdukit.detect import Script, detect_script

# Core Urdu script stopwords (postpositions, auxiliaries, pronouns, conjunctions)
URDU_SCRIPT_STOPWORDS: Set[str] = {
    # Postpositions & particles
    "کا", "کے", "کی", "کو", "سے", "پر", "میں", "تک", "نے", "تلک",
    "بھی", "تو", "ہی", "نہ", "نہیں", "مت",
    
    # Conjunctions
    "اور", "یا", "مگر", "لیکن", "بلکہ", "کہ", "کیونکہ", "چونکہ", "اگر", "گر", "تاہم", "پھر", "پس",
    
    # Pronouns & demonstratives
    "یہ", "وہ", "اس", "ان", "انھوں", "انہوں", "انہیں", "انھیں", "اسے", "اسکو", "انکو",
    "ہم", "ہمارا", "ہماری", "ہمارے", "ہمیں",
    "تم", "تمہارا", "تمہاری", "تمہارے", "تمہیں",
    "آپ", "آپکا", "آپکی", "آپکے", "آپکو",
    "کون", "کوئی", "کچھ", "کیا", "کب", "کہاں", "کدھر", "کیوں", "کیسے", "کیسا", "کیسی",
    "سب", "تمام", "ہر", "کسی",
    
    # Auxiliaries & common verbs
    "ہے", "ہیں", "ہو", "ہوں", "ہوتا", "ہوتی", "ہوتے", "ہونا", "ہونی", "ہونے",
    "تھا", "تھی", "تھے", "تھیں",
    "ہوگا", "ہوگی", "ہوگے", "ہوںگے",
    "ہوا", "ہوئی", "ہوئے",
    "رہا", "رہی", "رہے", "رہنا", "رہتی", "رہتے",
    "گیا", "گئی", "گئے", "جاتا", "جاتی", "جاتے", "جانا",
    "کر", "کرنا", "کرتا", "کرتی", "کرتے", "کرو", "کریں", "کیا", "کیے",
    "دے", "دیا", "دی", "دیے", "دینا", "دیتے", "دیتی",
    "لے", "لیا", "لی", "لیے", "لینا",
    
    # Adverbs / qualifiers
    "والا", "والی", "والے", "والوں", "والا",
    "صرف", "شاید", "اب", "جب", "تب", "ساتھ", "پہلے", "بعد", "درمیان",
    "ایک", "دو", "تین", "چار", "پانچ"
}

# Core Roman Urdu stopwords
ROMAN_URDU_STOPWORDS: Set[str] = {
    # Postpositions & particles
    "ka", "ke", "ki", "kay", "ko", "se", "sy", "pe", "par", "mein", "main", "men", "tak", "ne", "nay",
    "bhi", "b", "to", "toh", "na", "nahi", "nahin", "nhi", "nahe", "mat", "mtt",
    
    # Conjunctions
    "aur", "or", "ya", "magar", "mgr", "lekin", "lekn", "lkn", "k", "ke", "kyun", "kyu", "agar", "agr", "phir",
    
    # Pronouns & demonstratives
    "ye", "yeh", "wo", "woh", "voh", "is", "us", "in", "un", "inhe", "unhe", "inhein", "unhein",
    "isko", "usko", "inko", "unko", "ise", "use",
    "hum", "humein", "humain", "hmain", "hamara", "hamari", "hamare",
    "tum", "tumhara", "tumhari", "tumhare", "tumhe", "tumhein",
    "aap", "ap", "apka", "apki", "apke", "aapka", "aapki", "aapke", "apko", "aapko",
    "kaun", "kon", "koi", "kuch", "kch", "kya", "kia", "kab", "kahan", "khan", "kidhar", "kidhr",
    "kaise", "kese", "kesy", "kaisay", "kaisa", "kaisi",
    "sab", "sb", "har", "kisi",
    
    # Auxiliaries & common verbs
    "hai", "hain", "hn", "ho", "hon", "hoon", "hota", "hoti", "hote", "hona",
    "tha", "thi", "the", "thay", "thaa", "thii",
    "hoga", "hogi", "hoge", "hga", "hgi", "hge",
    "hogaya", "hogayi", "hogaye", "hogya", "hogyi",
    "raha", "rha", "rahi", "rhi", "rahe", "rhe", "rahna",
    "gaya", "gayi", "gaye", "gae", "gya", "gyi", "jana", "jata", "jati", "jate",
    "kar", "kr", "karna", "krna", "karta", "krta", "karti", "krti", "karte", "krte", "karo", "kro", "karein", "krein",
    "diya", "de", "di", "diye", "dena",
    "liya", "le", "li", "liye", "lena",
    
    # Adverbs / qualifiers
    "wala", "wali", "wale", "walay", "walon",
    "sirf", "srf", "shayad", "shyd", "ab", "jab", "jb", "tab", "tb", "saath", "sath", "pehle", "phle", "baad", "bad",
    "ek", "aik", "do", "teen", "char", "panch"
}

ALL_STOPWORDS: Set[str] = URDU_SCRIPT_STOPWORDS | ROMAN_URDU_STOPWORDS


def get_stopwords(lang: str = "all") -> Set[str]:
    """Retrieve stopword set for the specified script/language.

    Args:
        lang: Target stopword category:
            - 'urdu_script' (or 'urdu', 'ur'): Urdu script stopwords.
            - 'roman_urdu' (or 'roman', 'ru'): Roman Urdu stopwords.
            - 'all': Combined Urdu script and Roman Urdu stopwords.

    Returns:
        Set of lowercase stopword strings.
    """
    lang_clean = lang.lower().strip()
    if lang_clean in ("urdu_script", "urdu", "ur"):
        return set(URDU_SCRIPT_STOPWORDS)
    elif lang_clean in ("roman_urdu", "roman", "ru"):
        return set(ROMAN_URDU_STOPWORDS)
    elif lang_clean == "all":
        return set(ALL_STOPWORDS)
    else:
        raise ValueError(
            f"Unknown lang: '{lang}'. Expected 'urdu_script', 'roman_urdu', or 'all'."
        )


def is_stopword(word: str, lang: str = "all") -> bool:
    """Check whether a single word is a recognized stopword.

    Args:
        word: Token string to evaluate.
        lang: Stopword category ('urdu_script', 'roman_urdu', or 'all').

    Returns:
        True if the word is in the requested stopword set, False otherwise.
    """
    if not word or not word.strip():
        return False
    sw = get_stopwords(lang=lang)
    return word.strip().lower() in sw


def remove_stopwords(text: str, lang: str = "auto") -> str:
    """Filter out stopwords from input text while preserving punctuation and spacing.

    Args:
        text: Input string (Urdu script, Roman Urdu, or Mixed).
        lang: 'auto' (detect script automatically), 'urdu_script', 'roman_urdu', or 'all'.

    Returns:
        String with stopwords removed and cleaned spacing.
    """
    if not text or not text.strip():
        return ""

    if lang == "auto":
        detected = detect_script(text)
        if detected == Script.URDU_SCRIPT:
            active_stopwords = URDU_SCRIPT_STOPWORDS
        elif detected == Script.ROMAN_URDU:
            active_stopwords = ROMAN_URDU_STOPWORDS
        else:
            active_stopwords = ALL_STOPWORDS
    else:
        active_stopwords = get_stopwords(lang=lang)

    # Tokenize while capturing delimiters and whitespace
    tokens = re.split(r"(\s+|[^\w\s])", text)
    filtered = []

    for token in tokens:
        if not token or token.isspace() or re.match(r"^[^\w\s]+$", token):
            filtered.append(token)
            continue

        if token.lower() not in active_stopwords:
            filtered.append(token)

    # Clean up redundant spaces caused by removed tokens
    result = "".join(filtered)
    result = re.sub(r"[ \t]+", " ", result)
    result = re.sub(r"\n\s*\n+", "\n", result)
    return result.strip()
