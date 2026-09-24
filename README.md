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
```

---

### 3. Transliteration (Roman Urdu ⇄ Urdu Script)

Fast bidirectional rule-based and lexicon-backed transliteration:

```python
from urdukit import roman_to_urdu, urdu_to_roman

# Roman Urdu to Urdu Script
urdu_text = roman_to_urdu("kya hal hai aapka? bohot shukriya")
print(urdu_text)
# Output: "کیا حال ہے آپ کا؟ بہت شکریہ"

# Urdu Script to Roman Urdu
roman_text = urdu_to_roman("آپ کیسے ہیں؟")
print(roman_text)
# Output: "aap kaise hain?"
```

---

### 4. Semantic Search & Embeddings

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
- [x] Bidirectional transliterator (`roman_to_urdu`, `urdu_to_roman`)
- [x] Multilingual semantic embeddings wrapper (`intfloat/multilingual-e5-small`)
- [ ] Hugging Face Spaces interactive demo
- [ ] Extended crowdsourced Roman Urdu dictionary from open Pakistani datasets
- [ ] Lightweight fastText / char-ngram language classifier for fine-grained sub-dialects

---

## 📄 License

MIT License. Free and open source for everyone. Contributions are warmly welcomed!
