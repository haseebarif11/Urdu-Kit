"""Text normalization module for UrduKit.

Provides rule-based and dictionary-driven normalization for:
1. Roman Urdu spelling variants (e.g. "kesy", "kese", "kaisay" -> "kaise")
2. Character elongation ("bohooooot" -> "bohot", "yaaaar" -> "yaar")
3. Urdu script orthographic normalization (unifying Arabic/Urdu Unicode codepoints)
4. Whitespace, punctuation, and casing cleanup
"""

import re
from typing import Dict, Optional


# Canonical dictionary mapping Roman Urdu variants to standardized forms
ROMAN_URDU_CANONICAL_MAP: Dict[str, str] = {
    # Interrogatives (Questions)
    "kesy": "kaise",
    "kese": "kaise",
    "kaisay": "kaise",
    "kaisa": "kaise",
    "kaisi": "kaisi",
    "kia": "kya",
    "kyaa": "kya",
    "kyu": "kyun",
    "kyun": "kyun",
    "kiu": "kyun",
    "kyn": "kyun",
    "kew": "kyun",
    "kider": "kidhar",
    "kidhr": "kidhar",
    "kdr": "kidhar",
    "khan": "kahan",
    "kahan": "kahan",
    "kaha": "kahan",
    "kon": "kaun",
    "kone": "kaun",
    "koun": "kaun",
    "kab": "kab",
    "kbb": "kab",
    "ktna": "kitna",
    "kitny": "kitne",
    "kitnay": "kitne",

    # Negation
    "nhi": "nahi",
    "nahin": "nahi",
    "nahe": "nahi",
    "nahee": "nahi",
    "nhin": "nahi",
    "mtt": "mat",
    "naa": "na",

    # Pronouns & Possessives
    "ap": "aap",
    "aap": "aap",
    "apka": "aapka",
    "apki": "aapki",
    "apke": "aapke",
    "apko": "aapko",
    "apk": "aapka",
    "mujhe": "mujhe",
    "mjhe": "mujhe",
    "mujhy": "mujhe",
    "mjy": "mujhe",
    "mujy": "mujhe",
    "tujhe": "tujhe",
    "tjhe": "tujhe",
    "tujhy": "tujhe",
    "tjy": "tujhe",
    "humein": "humein",
    "humain": "humein",
    "hmain": "humein",
    "hamey": "humein",
    "hume": "humein",
    "unhe": "unhein",
    "unhain": "unhein",
    "unhein": "unhein",
    "unhy": "unhein",
    "inhe": "inhein",
    "inhain": "inhein",
    "inhein": "inhein",
    "inhy": "inhein",
    "wo": "woh",
    "voh": "woh",
    "ye": "yeh",
    "mera": "mera",
    "meraa": "mera",
    "mri": "meri",
    "mre": "mere",
    "tera": "tera",
    "teraa": "tera",
    "tri": "teri",
    "tre": "tere",
    "tmhara": "tumhara",
    "tumhra": "tumhara",
    "tmhra": "tumhara",
    "tmhari": "tumhari",
    "tumhri": "tumhari",
    "tmhare": "tumhare",
    "tumhre": "tumhare",
    "isko": "isko",
    "usko": "usko",

    # Verbs and Auxiliaries
    "krna": "karna",
    "kerna": "karna",
    "kr": "kar",
    "ker": "kar",
    "kro": "karo",
    "krein": "karein",
    "karen": "karein",
    "krta": "karta",
    "krti": "karti",
    "krte": "karte",
    "rha": "raha",
    "rhi": "rahi",
    "rhe": "rahe",
    "hga": "hoga",
    "hgi": "hogi",
    "hge": "hoge",
    "hogya": "hogaya",
    "hogyi": "hogayi",
    "thaa": "tha",
    "thii": "thi",
    "thay": "the",
    "the": "the",
    "hon": "hoon",
    "hn": "hain",
    "btao": "batao",
    "smjh": "samajh",
    "samjh": "samajh",
    "dkh": "dekh",
    "dkho": "dekho",
    "dakho": "dekho",
    "sunoo": "suno",
    "aaoo": "aao",
    "jao": "jao",

    # Adjectives & Adverbs
    "bht": "bohot",
    "boht": "bohot",
    "bohot": "bohot",
    "bohoot": "bohot",
    "bahut": "bohot",
    "bhat": "bohot",
    "thek": "theek",
    "thik": "theek",
    "achha": "acha",
    "achaa": "acha",
    "achhi": "achi",
    "achhe": "ache",
    "shi": "sahi",
    "shai": "sahi",
    "glt": "ghalat",
    "galat": "ghalat",
    "zyda": "zyada",
    "ziada": "zyada",
    "zayada": "zyada",
    "thoda": "thora",
    "thra": "thora",
    "zroor": "zaroor",
    "zarur": "zaroor",
    "zroori": "zaroori",
    "zaruri": "zaroori",
    "jldi": "jaldi",
    "phle": "pehle",
    "bad": "baad",
    "khubsurat": "khoobsurat",
    "pyari": "pyari",
    "pyara": "pyara",

    # Conjunctions, Prepositions & Fillers
    "lekn": "lekin",
    "lkn": "lekin",
    "mgr": "magar",
    "sy": "se",
    "kay": "ke",
    "men": "mein",
    "main": "mein",
    "pe": "par",
    "walay": "wale",
    "waley": "wale",
    "shukria": "shukriya",
    "sukriya": "shukriya",
    "shukrya": "shukriya",
    "yar": "yaar",
    "bhae": "bhai",
    "bhayi": "bhai",
    "bhy": "bhai",
    "wqt": "waqt",
    "waqat": "waqt",
    "pesay": "paise",
    "pese": "paise",
    "paysay": "paise",
    "plz": "please",
    "plzz": "please",
    "plsss": "please",
    "thx": "thanks",
    "tysm": "thank you so much",
    "wese": "waise"
}

# Urdu Unicode normalization table
# Unifies Arabic presentation/codepoint variations into standardized Urdu characters
URDU_CHAR_NORMALIZATION_MAP: Dict[str, str] = {
    "\u0643": "\u06A9",  # Arabic Kaf -> Urdu Keheh (ک)
    "\u064A": "\u06CC",  # Arabic Yeh -> Urdu Yeh (ی)
    "\u0649": "\u06CC",  # Alef Maksura -> Urdu Yeh (ی)
    "\u0647": "\u06C1",  # Arabic Heh -> Urdu Heh Goal (ہ)
    "\u0629": "\u06C1",  # Teh Marbuta -> Urdu Heh Goal (ہ)
    "\u06C2": "\u06C1\u0654",  # Heh Goal with Hamza -> Heh + Hamza above
    "\u0648\u0670": "\u0624",  # Waw + Dagger Alef
    "\u0640": "",        # Arabic Tatweel (Kashida) -> Remove
    "\u060C": "،",       # Urdu comma
    "\u061B": "؛",       # Urdu semicolon
    "\u061F": "؟",       # Urdu question mark
}

# Urdu diacritics / aerab (Zabar, Zer, Pesh, Tashdeed, Tanween, Sukun, etc.)
URDU_DIACRITICS_REGEX = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")


def reduce_elongation(word: str) -> str:
    """Reduce repetitive character elongations common in informal Roman Urdu chat.

    Examples:
        - bohooooot -> bohot
        - yaaaar -> yaar
        - haaaan -> haan
        - theeeek -> theek
    """
    # Replace runs of 3 or more identical characters with 2 (e.g. aaa -> aa, ooo -> oo)
    reduced = re.sub(r"(.)\1{2,}", r"\1\1", word)

    # If the 2-char version is not canonical but single char is (e.g. bohoooot -> bohoot -> bohot),
    # check known dictionary matches
    if reduced in ROMAN_URDU_CANONICAL_MAP:
        return ROMAN_URDU_CANONICAL_MAP[reduced]

    single_collapsed = re.sub(r"(.)\1+", r"\1", word)
    if single_collapsed in ROMAN_URDU_CANONICAL_MAP:
        return ROMAN_URDU_CANONICAL_MAP[single_collapsed]

    return reduced


def normalize_urdu_script(text: str, remove_diacritics: bool = False) -> str:
    """Normalize Urdu script characters to standard Pakistani Urdu Unicode forms.

    Args:
        text: Raw text containing Urdu characters.
        remove_diacritics: If True, strips diacritical marks (aerab: zer, zabar, pesh, etc.).

    Returns:
        Orthographically standardized Urdu script string.
    """
    for src, target in URDU_CHAR_NORMALIZATION_MAP.items():
        text = text.replace(src, target)

    if remove_diacritics:
        text = URDU_DIACRITICS_REGEX.sub("", text)

    return text


def normalize_roman_urdu(text: str, remove_elongation_flag: bool = True) -> str:
    """Normalize Roman Urdu tokens using spelling canonicalization and elongation reduction.

    Args:
        text: Input string with Roman Urdu text.
        remove_elongation_flag: Whether to collapse stretched characters.

    Returns:
        Normalized Roman Urdu text with standardized spellings.
    """
    # Tokenize while preserving punctuation and spacing
    tokens = re.split(r"(\s+|[^\w\s])", text)
    normalized_tokens = []

    for token in tokens:
        # If whitespace or punctuation, preserve as-is
        if not token or token.isspace() or re.match(r"^[^\w\s]+$", token):
            normalized_tokens.append(token)
            continue

        lower_token = token.lower()
        processed = lower_token

        # Step 1: Elongation reduction if requested
        if remove_elongation_flag and re.search(r"(.)\1{2,}", lower_token):
            processed = reduce_elongation(lower_token)

        # Step 2: Dictionary canonicalization
        canonical = ROMAN_URDU_CANONICAL_MAP.get(processed)
        if canonical:
            # Preserve original casing if whole token was UPPERCASE or Capitalized
            if token.isupper() and len(token) > 1:
                replacement = canonical.upper()
            elif token[0].isupper():
                replacement = canonical.capitalize()
            else:
                replacement = canonical
            normalized_tokens.append(replacement)
        else:
            normalized_tokens.append(processed if remove_elongation_flag else token)

    return "".join(normalized_tokens)


def normalize(
    text: str,
    remove_elongation: bool = True,
    normalize_script: bool = True,
    remove_diacritics: bool = False,
    strip_extra_whitespace: bool = True,
) -> str:
    """Main normalization middleware function.

    Standardizes Roman Urdu spellings, reduces character elongations,
    normalizes Urdu Unicode characters, and cleans whitespace.

    Args:
        text: Raw user input text (Roman Urdu, Urdu script, English, or Mixed).
        remove_elongation: Whether to collapse informal repeated letters (e.g. 'bohooot' -> 'bohot').
        normalize_script: Whether to convert non-standard Arabic ligatures to Urdu Unicode.
        remove_diacritics: Whether to remove Urdu aerab (diacritics like zer, zabar, pesh).
        strip_extra_whitespace: Whether to collapse multiple spaces into a single space.

    Returns:
        Clean, standardized text ready for LLM, search engine, or embedding models.
    """
    if not text:
        return ""

    result = text

    # 1. Normalize Urdu script codepoints if present
    if normalize_script:
        result = normalize_urdu_script(result, remove_diacritics=remove_diacritics)

    # 2. Normalize Roman Urdu spelling variants & elongations
    result = normalize_roman_urdu(result, remove_elongation_flag=remove_elongation)

    # 3. Clean redundant spaces while preserving line breaks if needed
    if strip_extra_whitespace:
        # Collapse multiple spaces or tabs into a single space per line
        result = re.sub(r"[ \t]+", " ", result)
        result = re.sub(r"\n\s*\n+", "\n", result)
        result = result.strip()

    return result
