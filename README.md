# 🇵🇰 UrduKit

> **The missing NLP middleware toolkit for Roman Urdu, Urdu Script, and Code-Switched text.**

[![PyPI Version](https://img.shields.io/pypi/v/urdukit.svg)](https://pypi.org/project/urdukit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/urdukit.svg)](https://pypi.org/project/urdukit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

---

## 📌 Why UrduKit?

Pakistani text input in the real world is chaotic:
- **Phonetic variations:** `"kesy"`, `"kese"`, `"kaisay"`, and `"kisa"` all mean the exact same thing (*"how"*).
- **Elongation & slang:** Informal chat is packed with repeated characters: `"bohooooot"`, `"yaaaar"`, `"theeeek"`.
- **Script mixing & code-switching:** Sentences fluidly weave between Roman Urdu, Urdu script (*کیا حال ہے*), and English (*"Mera order kab deliver hoga? Please check tracking ID"*).
- **Orthographic inconsistencies:** Urdu script from keyboards often mixes Arabic Unicode characters (`ك`, `ي`, `ة`, kashida `ـ`) with proper Pakistani Urdu characters (`ک`, `ی`, `ہ`).

LLMs, search engines, and vector databases stumble on these variations, resulting in poor retrieval, hallucinatory responses, or language drift.

**UrduKit sits directly between raw user input and your AI system** (LLM, vector DB, search engine, sentiment model), preprocessing input into clean, standardized representations and formatting responses back into the user's preferred script.

---

## 🔄 Architecture & Flow

```text
  Raw User Input
  ("Kesy ho yaaaar? Order kab deliver hoga?")
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────┐
  │                        UrduKit                           │
  │                                                          │
  │  1. detect_script()      ──► Classify: Roman Urdu /      │
  │                              Urdu Script / English / Mix │
  │  2. normalize()          ──► "Kaise ho yaar? Order kab   │
  │                              deliver hoga?"              │
  │  3. roman_to_urdu()      ──► (Optional) Transliterate to │
  │                              Urdu script                 │
  │  4. UrduEmbedder()       ──► Semantic search / RAG       │
  └──────────────────────────┬───────────────────────────────┘
                             │
                             ▼
         Clean Text to LLM / Search / Model
             (Groq / Ollama / OpenAI / RAG)
                             │
                             ▼
         Response Formatted to User's Script
```

---

## ⚡ Quick Install

Install core package (zero heavy dependencies, installs in seconds):
```bash
pip install urdukit
```

Install with semantic embeddings support (multilingual sentence-transformers):
```bash
pip install "urdukit[embeddings]"
```

For development:
```bash
git clone https://github.com/haseebarif11/Urdu-Kit.git
cd Urdu-Kit
pip install -e ".[dev]"
```

---

## 🚀 Usage Examples

### 1. Script & Language Detection

Accurately classifies inputs into `URDU_SCRIPT`, `ROMAN_URDU`, `ENGLISH`, `MIXED`, or `UNKNOWN`.

```python
from urdukit import detect_script, Script

# Urdu Script
print(detect_script("کیا حال ہے آپ کا؟"))
# Output: Script.URDU_SCRIPT

# Roman Urdu
print(detect_script("mera order kab tak deliver hoga bhai?"))
# Output: Script.ROMAN_URDU

# English
print(detect_script("What is the status of my refund?"))
# Output: Script.ENGLISH

# Code-switching / Mixed script
print(detect_script("Mera parcel cancel kar dein please, it is too late."))
# Output: Script.MIXED
```

---

### 2. Spelling Normalization & Elongation Reduction

Canonicalizes non-standard Roman Urdu spellings, reduces chat elongation, and standardizes Urdu script Unicode codepoints.

```python
from urdukit import normalize

# Roman Urdu variations canonicalization
raw_input = "Kesy ho yaaaar? bohooooot dino baad baat hui, bht maza aya!"
clean = normalize(raw_input)
print(clean)
# Output: "Kaise ho yaar? bohot dino baad baat hui, bohot maza aya!"

# Urdu script Unicode unification (converts Arabic Kaf/Yeh to Urdu forms & strips tatweel)
raw_urdu = "شـــکـــریہ، كیا آپ علی ہیں؟"
print(normalize(raw_urdu))
# Output: "شکریہ، کیا آپ علی ہیں؟"

# Eastern Arabic-Indic / Arabic numeral normalization
from urdukit import normalize_digits

print(normalize_digits("قیمت ۱۲۵۰ روپے ہے", target="latin"))
# Output: "قیمت 1250 روپے ہے"

# Combined normalization with numerals in one pipeline call
print(normalize("kesy ho yaaaar? OTP ۴۵۶۷۸ ہے", normalize_digits_to="latin"))
# Output: "kaise ho yaar? OTP 45678 ہے"
```

---

### 3. Transliteration & Script Unification

Fast bidirectional rule-based and lexicon-backed transliteration, plus unified script conversion:

```python
from urdukit import roman_to_urdu, urdu_to_roman, to_urdu_script

# Roman Urdu to Urdu Script
urdu_text = roman_to_urdu("kya hal hai aapka? bohot shukriya")
print(urdu_text)
# Output: "کیا حال ہے آپ کا؟ بہت شکریہ"

# Urdu Script to Roman Urdu
roman_text = urdu_to_roman("آپ کیسے ہیں؟")
print(roman_text)
# Output: "aap kaise hain?"

# Unified Urdu Script for Mixed / Code-switched text (opt-in for LLMs/embeddings)
mixed_input = "میرا order cancel کر دیں please, bht dair ho gayi hai"
unified = to_urdu_script(mixed_input, convert_loanwords=True)
print(unified)
# Output: "میرا آرڈر کینسل کر دیں پلیز, بہت دیر ہو گئی ہے"

# Retain loanwords in Latin while converting Roman Urdu:
unified_latin_loanwords = to_urdu_script(mixed_input, convert_loanwords=False)
print(unified_latin_loanwords)
# Output: "میرا order cancel کر دیں please, بہت دیر ہو گئی ہے"
```

---

### 4. Sentence Segmentation & Word Tokenization

Lightweight tokenizers designed specifically to respect Urdu punctuation (`۔` full stop, `؟` question mark, `،` comma, `؛` semicolon) as well as Latin boundaries:

```python
from urdukit import split_sentences, tokenize_words

# Sentence splitting (recognizes Urdu Khatma '۔' and Question mark '؟')
urdu_doc = "یہ پہلا جملہ ہے۔ کیا آپ خیریت سے ہیں؟ جی ہاں، سب ٹھیک ہے۔"
sentences = split_sentences(urdu_doc)
print(sentences)
# Output: ['یہ پہلا جملہ ہے۔', 'کیا آپ خیریت سے ہیں؟', 'جی ہاں، سب ٹھیک ہے۔']

# Word tokenization with optional punctuation removal
tokens = tokenize_words("کیا حال ہے؟ سب ٹھیک ہے، شکر ہے۔", remove_punct=True)
print(tokens)
# Output: ['کیا', 'حال', 'ہے', 'سب', 'ٹھیک', 'ہے', 'شکر', 'ہے']
```

---

### 5. Stopword Detection & Filtering

High-speed stopword identification and removal for search indexes, TF-IDF / BM25, and prompt compression:

```python
from urdukit import remove_stopwords, is_stopword, get_stopwords

# Check individual stopwords
print(is_stopword("اور"))   # True (Urdu script)
print(is_stopword("aur"))   # True (Roman Urdu)
print(is_stopword("laptop")) # False

# Filter stopwords automatically (detects script on the fly)
urdu_text = "پاکستان کا دارالحکومت اسلام آباد ہے"
print(remove_stopwords(urdu_text))
# Output: "پاکستان دارالحکومت اسلام آباد"

roman_text = "order cancel karne ka tareeqa kya hai"
print(remove_stopwords(roman_text))
# Output: "order cancel karne tareeqa"
```

---

### 6. Semantic Search & Embeddings

Semantic search across Roman Urdu, Urdu script, and English with auto-normalization:

```python
from urdukit import UrduEmbedder

# Automatically loads lightweight multilingual model ('intfloat/multilingual-e5-small')
embedder = UrduEmbedder()

documents = [
    "Order cancel karne ka tareeqa kya hai?",
    "Return policy aur refund kitne dino mein milta hai?",
    "Delivery charges kitnay hain?",
    "Customer support ka helpline number"
]

query = "kesy order cancel karu?"

# Get relevance ranking
ranked = embedder.rank(query, documents, top_k=2)

for rank, doc, score in ranked:
    print(f"[{score:.4f}] {doc}")

# Output:
# [0.8924] Order cancel karne ka tareeqa kya hai?
# [0.7241] Return policy aur refund kitne dino mein milta hai?
```

---

### 7. Sentiment Polarity Analysis

Fast, lightweight sentiment scoring for Pakistani Roman Urdu and Urdu script without requiring 500MB+ models:

```python
from urdukit import analyze_sentiment

# Roman Urdu sentiment (with negation awareness)
print(analyze_sentiment("yeh bohot achi aur shandar product hai"))
# Output: {'label': 'positive', 'score': 1.0, 'positive_words': ['achi', 'shandar'], 'negative_words': []}

print(analyze_sentiment("yeh mobile acha nahi hai"))
# Output: {'label': 'negative', 'score': -1.0, 'positive_words': [], 'negative_words': ['not_acha']}

# Urdu script sentiment
print(analyze_sentiment("بہت برا اور ناقص کام ہے، سخت نقصان ہوا"))
# Output: {'label': 'negative', 'score': -1.0, 'positive_words': [], 'negative_words': ['برا', 'نقصان']}
```

---

### 8. Text Analytics & Script Statistics

Inspect document lengths, word counts, lexical diversity, and language/script distribution:

```python
from urdukit import text_stats, top_words

text = "یہ پہلا جملہ ہے۔ قیمت ۱۲۵۰ روپے ہے۔ یہ دوسرا شاندار جملہ ہے۔"

# Structural & linguistic metrics
stats = text_stats(text)
print(stats)
# Output:
# {
#   'character_count': 59,
#   'word_count': 11,
#   'unique_word_count': 9,
#   'lexical_diversity': 0.818,
#   'avg_word_length': 3.64,
#   'sentence_count': 3,
#   'urdu_char_count': 36,
#   'latin_char_count': 0,
#   'digit_count': 4,
#   'urdu_ratio': 1.0,
#   'latin_ratio': 0.0,
#   'script': 'urdu_script',
#   'reading_time_sec': 4
# }

# Extract top frequent keywords (excluding stopwords)
top = top_words("bohat acha project hai bohat zabardast project shandar project", n=3)
print(top)
# [('project', 3), ('bohat', 2), ('shandar', 1)]
```

---

### 9. Command-Line Interface (CLI)

Use `urdukit` directly from your terminal or shell scripts:

```bash
# Detect script
urdukit detect "kya haal hai bhai?"

# Normalize text & numerals
urdukit normalize "kesy ho yaaaar? OTP ۴۵۶ ہے" --digits latin

# Transliterate
urdukit transliterate "kya hal hai" --mode to-urdu

# Tokenize words or sentences
urdukit tokenize "urdu zaban seekho!" --remove-punct
urdukit tokenize "یہ پہلا جملہ ہے۔ یہ دوسرا جملہ ہے۔" --sentences

# Remove stopwords
urdukit stopwords "yeh ek achi kitab hai"

# Analyze sentiment
urdukit sentiment "bohot achi service hai" --json

# Text statistics & top frequent words
urdukit stats "یہ اردو ٹیکسٹ ہے جس میں الفاظ کی تعداد ناپی جاتی ہے" --top-words 3
```

---

## 🤖 End-to-End LLM Middleware Pipeline

Here is how you can use `urdukit` to guard your LLM pipeline (e.g. using free-tier Groq, Ollama, or OpenAI):

```python
from urdukit import detect_script, normalize, roman_to_urdu, Script

def process_user_query(raw_user_input: str) -> str:
    # 1. Detect user's input language and script
    script_type = detect_script(raw_user_input)
    
    # 2. Normalize spelling and reduce elongations
    clean_text = normalize(raw_user_input)
    
    # 3. Create context-aware prompt for the LLM
    system_prompt = (
        "You are an AI assistant for Pakistani users. "
        f"The user wrote in {script_type.value}. "
        "Respond clearly and match their script style."
    )
    
    # Send clean_text to your LLM (Groq / Ollama / OpenAI)...
    # llm_response = call_llm(system_prompt, clean_text)
    
    return f"Processed: '{clean_text}' (Script: {script_type.value})"

# Example:
print(process_user_query("kesyyy hooo bhai?? mera package kidhr h??"))
# Output: Processed: 'kaise ho bhai?? mera package kidhar h??' (Script: roman_urdu)
```

---

## 🧪 Running Tests

UrduKit comes with a comprehensive test suite covering realistic Pakistani slang, typos, and Unicode edge cases:

```bash
pytest
```

---

## 🗺️ Roadmap

- [x] Script detection (`urdu_script`, `roman_urdu`, `english`, `mixed`, `unknown`)
- [x] Roman Urdu dictionary-based spelling normalizer & elongation reduction
- [x] Urdu script Unicode normalizer (Arabic ligature normalization, Kashida removal)
- [x] Numerals normalization (Eastern Arabic-Indic ۰-۹, Arabic-Indic ٠-٩, and Latin 0-9)
- [x] Bidirectional transliterator (`roman_to_urdu`, `urdu_to_roman`) and unified script conversion (`to_urdu_script`)
- [x] Sentence segmentation (`split_sentences`) and word tokenization (`tokenize_words`)
- [x] Stopword detection and filtering for Urdu script and Roman Urdu (`remove_stopwords`, `is_stopword`)
- [x] Lightweight sentiment polarity analyzer (`analyze_sentiment`)
- [x] Text analytics and script distribution metrics (`text_stats`)
- [x] Command-Line Interface (`urdukit` CLI)
- [x] Multilingual semantic embeddings wrapper (`intfloat/multilingual-e5-small`)
- [ ] Hugging Face Spaces interactive demo
- [ ] Extended crowdsourced Roman Urdu dictionary from open Pakistani datasets
- [ ] Lightweight fastText / char-ngram language classifier for fine-grained sub-dialects

---

## 📄 License

MIT License. Free and open source for everyone. Contributions are warmly welcomed!
