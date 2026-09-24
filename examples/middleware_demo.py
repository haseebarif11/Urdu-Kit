"""UrduKit Middleware Demo.

Demonstrates how UrduKit sits between raw user input and downstream AI applications.
"""

import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from urdukit import Script, detect_script, normalize, roman_to_urdu, urdu_to_roman


def main():
    print("=" * 60)
    print("Welcome to UrduKit — NLP Middleware for Roman & Script Urdu")
    print("=" * 60)

    test_inputs = [
        "kesyyy hooo yaaaar? mera order kb tk aayega?",
        "میرا order cancel کر دیں please, bht dair ho gayi hai",
        "What is the return policy for defective items?",
        "شـــکـــریہ جناب، كیا حال ہے؟",
        "hmain invoice nahi mili abhi tak, plz check krein",
    ]

    for idx, text in enumerate(test_inputs, 1):
        print(f"\n--- [Example {idx}] ---")
        print(f"Raw Input    : {text}")

        # Step 1: Detect script/language
        detected = detect_script(text)
        print(f"Script Type  : {detected.value.upper()}")

        # Step 2: Normalize (canonicalize Roman Urdu spelling variants & Urdu Unicode)
        clean_text = normalize(text)
        print(f"Normalized   : {clean_text}")

        # Step 3: Transliterate (if Roman Urdu, show Urdu script equivalent)
        if detected == Script.ROMAN_URDU:
            urdu_script = roman_to_urdu(clean_text)
            print(f"Urdu Script  : {urdu_script}")
        elif detected == Script.URDU_SCRIPT:
            roman_text = urdu_to_roman(clean_text)
            print(f"Roman Urdu   : {roman_text}")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")


if __name__ == "__main__":
    main()
