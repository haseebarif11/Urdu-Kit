"""Transliteration module for UrduKit.

Provides rule-based and lexicon-backed transliteration between
Roman Urdu and standard Urdu Script (Nastaliq/Naskh).
"""

import re
from typing import Dict, Set

from urdukit.detect import ENGLISH_MARKERS, ROMAN_URDU_MARKERS, ROMAN_URDU_PATTERN, URDU_CHAR_REGEX


# Common English loanwords conventionally written in Urdu script
ENGLISH_LOANWORDS: Dict[str, str] = {
    # Core English loanwords
    "order": "آرڈر",
    "orders": "آرڈرز",
    "invoice": "انوائس",
    "invoices": "انوائسز",
    "check": "چیک",
    "checks": "چیکس",
    "please": "پلیز",
    "plz": "پلیز",
    "cancel": "کینسل",
    "call": "کال",
    "calls": "کالز",
    "message": "میسج",
    "messages": "میسجز",
    "msg": "میسج",
    "msgs": "میسجز",
    "phone": "فون",
    "phones": "فونز",
    "email": "ای میل",
    "emails": "ای میلز",
    "account": "اکاؤنٹ",
    "accounts": "اکاؤنٹس",
    "password": "پاسورڈ",
    "internet": "انٹرنیٹ",
    "mobile": "موبائل",
    "office": "آفس",
    "meeting": "میٹنگ",
    "meetings": "میٹنگز",
    "project": "پراجیکٹ",
    "projects": "پراجیکٹس",
    "price": "پرائس",
    "delivery": "ڈیلیوری",
    "address": "ایڈریس",

    # Additional retail, e-commerce, banking & workplace loanwords
    "bill": "بل",
    "bills": "بلز",
    "receipt": "رسید",
    "payment": "پیمنٹ",
    "payments": "پیمنٹس",
    "cash": "کیش",
    "card": "کارڈ",
    "cards": "کارڈز",
    "bank": "بینک",
    "discount": "ڈسکاؤنٹ",
    "offer": "آفر",
    "offers": "آفرز",
    "store": "سٹور",
    "shop": "شاپ",
    "parcel": "پارسل",
    "courier": "کوریئر",
    "tracking": "ٹریکنگ",
    "customer": "کسٹمر",
    "service": "سروس",
    "support": "سپورٹ",
    "help": "ہیلپ",
    "ticket": "ٹکٹ",
    "tickets": "ٹکٹس",
    "booking": "بکنگ",
    "item": "آئٹم",
    "items": "آئٹمز",
    "product": "پروڈکٹ",
    "products": "پروڈکٹس",

    # Technology, telecom & devices
    "mail": "میل",
    "computer": "کمپیوٹر",
    "laptop": "لیپ ٹاپ",
    "online": "آن لائن",
    "system": "سسٹم",
    "data": "ڈیٹا",
    "code": "کوڈ",
    "link": "لنک",
    "app": "ایپ",
    "apps": "ایپس",
    "website": "ویب سائٹ",
    "site": "سائٹ",
    "screen": "سکرین",
    "server": "سرور",
    "network": "نیٹ ورک",
    "sim": "سم",
    "number": "نمبر",
    "numbers": "نمبرز",
    "group": "گروپ",
    "profile": "پروفائل",
    "post": "پوسٹ",
    "page": "پیج",
    "video": "ویڈیو",
    "videos": "ویڈیوز",
    "audio": "آڈیو",
    "photo": "فوٹو",
    "photos": "فوٹوز",
    "pic": "پک",
    "pics": "پکس",
    "file": "فائل",
    "files": "فائلز",

    # Everyday conversational loanwords
    "team": "ٹیم",
    "boss": "باس",
    "company": "کمپنی",
    "job": "جاب",
    "time": "ٹائم",
    "urgent": "ارجنٹ",
    "problem": "پرابلم",
    "problems": "پرابلمز",
    "issue": "ایشو",
    "issues": "ایشوز",
    "status": "سٹیٹس",
    "update": "اپ ڈیٹ",
    "result": "رزلٹ",
    "report": "رپورٹ",
    "test": "ٹیسٹ",
    "class": "کلاس",
    "school": "سکول",
    "college": "کالج",
    "university": "یونیورسٹی",
    "hospital": "ہسپتال",
    "doctor": "ڈاکٹر",
    "car": "کار",
    "bus": "بس",
    "train": "ٹرین",
    "hotel": "ہوٹل",
    "room": "روم",
    "ok": "اوکے",
    "okay": "اوکے",
    "yes": "یس",
    "no": "نو",
    "thanks": "تھینکس",
    "thank": "تھینک",
    "sorry": "سوری",
    "welcome": "ویلکم",
    "hello": "ہیلو",
    "hi": "ہائے",
    "bye": "بائے",
}

# Alias for backward compatibility
ENGLISH_LOANWORDS_TO_URDU = ENGLISH_LOANWORDS


# High-frequency Roman Urdu -> Urdu script dictionary (orthographically correct Urdu)
LEXICON_ROMAN_TO_URDU: Dict[str, str] = {
    # Pronouns & interrogatives
    "kya": "کیا",
    "kia": "کیا",
    "kyun": "کیوں",
    "kyu": "کیوں",
    "kaise": "کیسے",
    "kese": "کیسے",
    "kesy": "کیسے",
    "kaisay": "کیسے",
    "kaisa": "کیسا",
    "kaisi": "کیسی",
    "kab": "کب",
    "kahan": "کہاں",
    "khan": "کہاں",
    "kidhar": "کدھر",
    "kidhr": "کدھر",
    "kaun": "کون",
    "kon": "کون",
    "kitna": "کتنا",
    "kitne": "کتنے",
    "kitni": "کتنی",
    "kis": "کس",
    "kise": "کسے",
    "kisko": "کس کو",

    # Pronouns & possessives
    "aap": "آپ",
    "ap": "آپ",
    "aapka": "آپ کا",
    "aapki": "آپ کی",
    "aapke": "آپ کے",
    "aapko": "آپ کو",
    "apka": "آپ کا",
    "apki": "آپ کی",
    "apke": "آپ کے",
    "apko": "آپ کو",
    "tum": "تم",
    "tumhara": "تمہارا",
    "tumhari": "تمہاری",
    "tumhare": "تمہارے",
    "tumko": "تم کو",
    "hum": "ہم",
    "humein": "ہمیں",
    "humain": "ہمیں",
    "hmain": "ہمیں",
    "humara": "ہمارا",
    "humari": "ہماری",
    "humare": "ہمارے",
    "mera": "میرا",
    "meri": "میری",
    "mere": "میرے",
    "tera": "تیرا",
    "teri": "تیری",
    "tere": "تیرے",
    "mujhe": "مجھے",
    "mjhe": "مجھے",
    "mujhy": "مجھے",
    "tujhe": "تجھے",
    "tjhe": "تجھے",
    "yeh": "یہ",
    "ye": "یہ",
    "woh": "وہ",
    "wo": "وہ",
    "iska": "اس کا",
    "iski": "اس کی",
    "iske": "اس کے",
    "isko": "اس کو",
    "uska": "اس کا",
    "uski": "اس کی",
    "uske": "اس کے",
    "usko": "اس کو",
    "unka": "ان کا",
    "unki": "ان کی",
    "unke": "ان کے",
    "unhe": "انہیں",
    "unhein": "انہیں",
    "inhe": "انہیں",
    "inhein": "انہیں",

    # Auxiliaries and verbs
    "hai": "ہے",
    "hain": "ہیں",
    "hoon": "ہوں",
    "hon": "ہوں",
    "tha": "تھا",
    "thi": "تھی",
    "the": "تھے",
    "thay": "تھے",
    "hoga": "ہوگا",
    "hogi": "ہوگی",
    "hoge": "ہوگے",
    "hogaya": "ہو گیا",
    "hogayi": "ہو گئی",
    "kar": "کر",
    "kr": "کر",
    "karna": "کرنا",
    "krna": "کرنا",
    "karo": "کرو",
    "kro": "کرو",
    "karein": "کریں",
    "krein": "کریں",
    "karen": "کریں",
    "karta": "کرتا",
    "karti": "کرتی",
    "karte": "کرتے",
    "raha": "رہا",
    "rha": "رہا",
    "rahi": "رہی",
    "rhi": "رہی",
    "rahe": "رہے",
    "rhe": "رہے",
    "hota": "ہوتا",
    "hoti": "ہوتی",
    "hote": "ہوتے",
    "jana": "جانا",
    "jao": "جاؤ",
    "aao": "آؤ",
    "aana": "آنا",
    "gaya": "گیا",
    "gayi": "گئی",
    "gaye": "گئے",
    "batao": "بتاؤ",
    "btao": "بتاؤ",
    "dekho": "دیکھو",
    "dekh": "دیکھ",
    "suno": "سنو",
    "samajh": "سمجھ",

    # Particles & prepositions
    "nahi": "نہیں",
    "nahin": "نہیں",
    "nhi": "نہیں",
    "mat": "مت",
    "aur": "اور",
    "or": "اور",
    "lekin": "لیکن",
    "magar": "مگر",
    "bhi": "بھی",
    "to": "تو",
    "toh": "تو",
    "se": "سے",
    "sy": "سے",
    "par": "پر",
    "pe": "پر",
    "ko": "کو",
    "ka": "کا",
    "ki": "کی",
    "ke": "کے",
    "kay": "کے",
    "mein": "میں",
    "main": "میں",
    "men": "میں",
    "tak": "تک",
    "saath": "ساتھ",
    "sath": "ساتھ",
    "baad": "بعد",
    "pehle": "پہلے",
    "phir": "پھر",
    "ab": "اب",
    "jab": "جب",
    "tab": "تب",

    # Adjectives & conversational
    "acha": "اچھا",
    "achha": "اچھا",
    "achi": "اچھی",
    "ache": "اچھے",
    "theek": "ٹھیک",
    "thik": "ٹھیک",
    "bohot": "بہت",
    "boht": "بہت",
    "bht": "بہت",
    "bahut": "بہت",
    "zyada": "زیادہ",
    "thora": "تھوڑا",
    "sahi": "صحیح",
    "ghalat": "غلط",
    "galat": "غلط",
    "zaroor": "ضرور",
    "zaroori": "ضروری",
    "shukriya": "شکریہ",
    "shukria": "شکریہ",
    "yaar": "یار",
    "yar": "یار",
    "bhai": "بھائی",
    "janab": "جناب",
    "sahab": "صاحب",
    "khair": "خیر",
    "waqt": "وقت",
    "paise": "پیسے",
    "pese": "پیسے",
    "khushi": "خوشی",
    "nam": "نام",
    "naam": "نام",
    "salam": "سلام",
    "assalam": "السلام",
    "alaikum": "علیکم",
    "inshallah": "انشاءاللہ",
    "mashallah": "ماشاءاللہ",
    "alhamdulillah": "الحمدللہ",
    "jazakallah": "جزاک اللہ",

    # Additional high-frequency verbs, particles & modifiers
    "ho": "ہو",
    "hoo": "ہو",
    "kb": "کب",
    "tk": "تک",
    "de": "دے",
    "do": "دو",
    "den": "دیں",
    "dein": "دیں",
    "di": "دی",
    "diya": "دیا",
    "dya": "دیا",
    "le": "لے",
    "lo": "لو",
    "len": "لیں",
    "lein": "لیں",
    "li": "لی",
    "liya": "لیا",
    "lia": "لیا",
    "mili": "ملی",
    "mila": "ملا",
    "mile": "ملے",
    "mil": "مل",
    "abhi": "ابھی",
    "kabhi": "کبھی",
    "tabhi": "تبھی",
    "sab": "سب",
    "kuch": "کچھ",
    "koi": "کوئی",
    "kisi": "کسی",
    "dair": "دیر",
    "der": "دیر",
    "hal": "حال",
    "haal": "حال"
}

# Invert for Urdu Script -> Roman Urdu lookups
LEXICON_URDU_TO_ROMAN: Dict[str, str] = {v: k for k, v in reversed(list(LEXICON_ROMAN_TO_URDU.items()))}
# Manually fix specific canonical inverses where needed
LEXICON_URDU_TO_ROMAN["کیا"] = "kya"
LEXICON_URDU_TO_ROMAN["کیسے"] = "kaise"
LEXICON_URDU_TO_ROMAN["نہیں"] = "nahi"
LEXICON_URDU_TO_ROMAN["بہت"] = "bohot"
LEXICON_URDU_TO_ROMAN["آپ"] = "aap"
LEXICON_URDU_TO_ROMAN["ہم"] = "hum"
LEXICON_URDU_TO_ROMAN["ہمیں"] = "humein"
LEXICON_URDU_TO_ROMAN["مجھے"] = "mujhe"
LEXICON_URDU_TO_ROMAN["ٹھیک"] = "theek"
LEXICON_URDU_TO_ROMAN["شکریہ"] = "shukriya"
LEXICON_URDU_TO_ROMAN["اچھا"] = "acha"
LEXICON_URDU_TO_ROMAN["میں"] = "mein"
LEXICON_URDU_TO_ROMAN["سے"] = "se"
LEXICON_URDU_TO_ROMAN["کے"] = "ke"
LEXICON_URDU_TO_ROMAN["کرو"] = "karo"
LEXICON_URDU_TO_ROMAN["کرنا"] = "karna"
LEXICON_URDU_TO_ROMAN["کر"] = "kar"
LEXICON_URDU_TO_ROMAN["رہا"] = "raha"
LEXICON_URDU_TO_ROMAN["رہی"] = "rahi"
LEXICON_URDU_TO_ROMAN["رہے"] = "rahe"
LEXICON_URDU_TO_ROMAN["دیں"] = "dein"
LEXICON_URDU_TO_ROMAN["ملی"] = "mili"
LEXICON_URDU_TO_ROMAN["ابھی"] = "abhi"
LEXICON_URDU_TO_ROMAN["ہو"] = "ho"
LEXICON_URDU_TO_ROMAN["کب"] = "kab"
LEXICON_URDU_TO_ROMAN["تک"] = "tak"


# Phonetic multigraph / character rules for fallback roman_to_urdu
ROMAN_DIGRAPHS_TO_URDU = [
    ("kh", "خ"),
    ("gh", "غ"),
    ("sh", "ش"),
    ("ch", "چ"),
    ("th", "تھ"),
    ("ph", "پھ"),
    ("bh", "بھ"),
    ("dh", "دھ"),
    ("jh", "جھ"),
    ("rh", "ڑھ"),
    ("zh", "ژ"),
    ("aa", "ا"),
    ("ee", "ی"),
    ("oo", "و"),
    ("ou", "و"),
    ("ai", "ے"),
    ("ei", "ی"),
]

ROMAN_CHAR_TO_URDU = {
    "a": "ا",
    "b": "ب",
    "p": "پ",
    "t": "ت",
    "T": "ٹ",
    "s": "س",
    "j": "ج",
    "c": "ک",
    "h": "ہ",
    "d": "د",
    "D": "ڈ",
    "r": "ر",
    "R": "ڑ",
    "z": "ز",
    "f": "ف",
    "q": "ق",
    "k": "ک",
    "g": "گ",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "w": "و",
    "v": "و",
    "y": "ی",
    "i": "ی",
    "e": "ے",
    "o": "و",
    "u": "و",
    "x": "کس",
}


# Distinctive Roman Urdu morphological & inflectional patterns
ROMAN_URDU_INFLECTION_PATTERN = re.compile(
    r"([aeiou]y?e?ga|[aeiou]y?e?gi|[aeiou]y?e?ge|[aeiou]y?e?nge|[aeiou]unga|[aeiou]oonga|waala|waali|waale|wala|wali|wale)\b",
    re.I,
)
DISTINCT_URDU_DIGRAPHS = ("kh", "gh", "jh", "dh", "bh", "rh")
DISTINCT_URDU_ENDINGS = re.compile(
    r"(ein|oun|iya|iye|nay|kay|hon|hoon|rha|rhi|rhe|bht|nhi)\b",
    re.I,
)


def _is_roman_urdu_word(word: str) -> bool:
    """Check if a Latin word is recognized Roman Urdu vocabulary or follows Roman Urdu patterns."""
    lower_w = word.lower()

    # 1. Known Roman Urdu dictionaries and markers
    if lower_w in LEXICON_ROMAN_TO_URDU:
        return True
    if lower_w in ROMAN_URDU_MARKERS:
        return True

    # 2. English markers that are not in Roman Urdu lexicon are English, not Roman Urdu
    if lower_w in ENGLISH_MARKERS:
        return False

    # 3. Check for distinct Urdu digraphs (e.g. 'bhai', 'ghar', 'khabar', 'dhan', 'jheel')
    if any(dg in lower_w for dg in DISTINCT_URDU_DIGRAPHS):
        # Exclude English words containing 'gh' like 'night', 'light', 'high', 'laugh', 'rough', 'tough', 'cough', 'ghost'
        if "gh" in lower_w and not any(dg in lower_w for dg in ("kh", "jh", "dh", "bh", "rh")):
            if re.search(r"(ight|ough|augh|igh\b|^ghost)", lower_w):
                return False
        return True

    # 4. Check for distinct Urdu grammatical endings
    if DISTINCT_URDU_ENDINGS.search(lower_w):
        return True

    # 5. Check for Roman Urdu verb inflection patterns (e.g. 'aayega', 'jayegi', 'karenge', 'karunga')
    if ROMAN_URDU_INFLECTION_PATTERN.search(lower_w):
        return True

    return False


def _transliterate_phonetic_roman_to_urdu(word: str) -> str:
    """Phonetic rule-based transducer for Roman Urdu words."""
    lower_w = word.lower()
    res = []
    i = 0
    w_len = len(lower_w)

    # Initial 'a' or 'aa' at beginning of word becomes Alif Madda 'آ' or Alif 'ا'
    if lower_w.startswith("aa"):
        res.append("آ")
        i += 2
    elif lower_w.startswith("a"):
        res.append("ا")
        i += 1

    while i < w_len:
        matched = False
        # Try 2-letter digraphs
        if i + 1 < w_len:
            two_chars = lower_w[i : i + 2]
            for digraph, urdu_char in ROMAN_DIGRAPHS_TO_URDU:
                if two_chars == digraph:
                    res.append(urdu_char)
                    i += 2
                    matched = True
                    break
        if matched:
            continue

        char = lower_w[i]
        # Preserve uppercase distinction if retroflex consonant (e.g. T -> ٹ, D -> ڈ, R -> ڑ)
        raw_char = word[i] if i < len(word) else char
        if raw_char in ("T", "D", "R"):
            res.append(ROMAN_CHAR_TO_URDU.get(raw_char, char))
        elif char in ROMAN_CHAR_TO_URDU:
            res.append(ROMAN_CHAR_TO_URDU[char])
        else:
            res.append(char)
        i += 1

    return "".join(res)


def _transliterate_word_roman_to_urdu(word: str) -> str:
    """Transliterate a single Roman Urdu word to Urdu script.

    1. Checks common English loanword dictionary for conventional Urdu script spelling.
    2. Checks high-frequency Roman Urdu lexicon.
    3. If the word matches recognized Roman Urdu vocabulary/patterns, phonetically transliterates.
    4. Otherwise, preserves the original word untouched in Latin script.
    """
    if not word or not any(c.isalpha() for c in word):
        return word

    # If the word already contains Urdu script characters, preserve as-is
    if URDU_CHAR_REGEX.search(word):
        return word

    lower_w = word.lower()

    # 1. Preferred: English loanwords conventionally written in Urdu script
    if lower_w in ENGLISH_LOANWORDS:
        return ENGLISH_LOANWORDS[lower_w]

    # 2. High-frequency Roman Urdu lexicon
    if lower_w in LEXICON_ROMAN_TO_URDU:
        return LEXICON_ROMAN_TO_URDU[lower_w]

    # 3. Check if this is a Roman Urdu word matching patterns/vocabulary
    if not _is_roman_urdu_word(lower_w):
        # Fallback: leave unrecognized English / Latin words untouched
        return word

    # 4. Phonetic rule-based transducer fallback for recognized Roman Urdu patterns
    return _transliterate_phonetic_roman_to_urdu(word)


def roman_to_urdu(text: str) -> str:
    """Convert Roman Urdu text to Urdu script.

    Uses an English loanwords dictionary for common loanwords, a high-frequency
    lexicon for Roman Urdu words and phrases, phonetic fallback rules for
    unmatched Roman Urdu patterns, and leaves unrecognized Latin words untouched.

    Args:
        text: Input string in Roman Urdu.

    Returns:
        Transliterated Urdu script text.
    """
    if not text:
        return ""

    tokens = re.split(r"(\s+|[^\w\s])", text)
    result = []

    for token in tokens:
        if not token or token.isspace() or re.match(r"^[^\w\s]+$", token):
            result.append(token)
            continue

        # Check ENGLISH_LOANWORDS dictionary FIRST (case-insensitive)
        token_lower = token.lower()
        if token_lower in ENGLISH_LOANWORDS:
            result.append(ENGLISH_LOANWORDS[token_lower])
            continue

        # Check Roman Urdu vocabulary, lexicon & phonetic transliteration
        result.append(_transliterate_word_roman_to_urdu(token))

    return "".join(result)


# Basic Urdu script to Roman character mapping
URDU_CHAR_TO_ROMAN = {
    "ا": "a",
    "آ": "aa",
    "ب": "b",
    "پ": "p",
    "ت": "t",
    "ٹ": "t",
    "ث": "s",
    "ج": "j",
    "چ": "ch",
    "ح": "h",
    "خ": "kh",
    "د": "d",
    "ڈ": "d",
    "ذ": "z",
    "ر": "r",
    "ڑ": "r",
    "ز": "z",
    "ژ": "zh",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "z",
    "ط": "t",
    "ظ": "z",
    "ع": "a",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ک": "k",
    "گ": "g",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ں": "n",
    "و": "o",
    "ہ": "h",
    "ۂ": "h",
    "ۃ": "t",
    "ء": "",
    "ی": "i",
    "ئ": "i",
    "ے": "e",
    "،": ",",
    "؛": ";",
    "؟": "?",
}

URDU_ASPIRATED_TO_ROMAN = {
    "بھ": "bh",
    "پھ": "ph",
    "تھ": "th",
    "ٹھ": "th",
    "جھ": "jh",
    "چھ": "ch",
    "دھ": "dh",
    "ڈھ": "dh",
    "رھ": "rh",
    "ڑھ": "rh",
    "کھ": "kh",
    "گھ": "gh",
}


def _transliterate_word_urdu_to_roman(word: str) -> str:
    """Transliterate a single Urdu script word to Roman Urdu."""
    if word in LEXICON_URDU_TO_ROMAN:
        return LEXICON_URDU_TO_ROMAN[word]

    res = []
    i = 0
    w_len = len(word)

    while i < w_len:
        # Check two-character aspirated consonants (e.g. ب + ھ)
        if i + 1 < w_len:
            two_chars = word[i : i + 2]
            if two_chars in URDU_ASPIRATED_TO_ROMAN:
                res.append(URDU_ASPIRATED_TO_ROMAN[two_chars])
                i += 2
                continue

        char = word[i]
        if char in URDU_CHAR_TO_ROMAN:
            res.append(URDU_CHAR_TO_ROMAN[char])
        else:
            res.append(char)
        i += 1

    return "".join(res)


def urdu_to_roman(text: str) -> str:
    """Convert Urdu script text into readable Roman Urdu.

    Args:
        text: Input string in Urdu script.

    Returns:
        Transliterated Roman Urdu text.
    """
    if not text:
        return ""

    tokens = re.split(r"(\s+|[^\w\s])", text)
    result = []

    for token in tokens:
        if not token or token.isspace() or re.match(r"^[^\w\s]+$", token):
            result.append(token)
            continue
        result.append(_transliterate_word_urdu_to_roman(token))

    return "".join(result)
