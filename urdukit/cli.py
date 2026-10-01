"""Command-Line Interface (CLI) for UrduKit.

Provides terminal commands for script detection, normalization,
transliteration, tokenization, sentiment analysis, and text stats.
"""

import argparse
import json
import sys
from typing import List, Optional

from urdukit import __version__
from urdukit.detect import detect_script
from urdukit.normalize import normalize, normalize_digits
from urdukit.sentiment import analyze_sentiment
from urdukit.stats import text_stats, top_words
from urdukit.stopwords import remove_stopwords
from urdukit.tokenize import split_sentences, tokenize_words
from urdukit.transliterate import roman_to_urdu, to_urdu_script, urdu_to_roman


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="urdukit",
        description="UrduKit — CLI middleware toolkit for Urdu and Roman Urdu text processing.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"urdukit {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. detect
    detect_p = subparsers.add_parser("detect", help="Detect script of input text")
    detect_p.add_argument("text", type=str, help="Text to classify")

    # 2. normalize
    norm_p = subparsers.add_parser("normalize", help="Normalize spelling and orthography")
    norm_p.add_argument("text", type=str, help="Text to normalize")
    norm_p.add_argument(
        "--digits",
        choices=["latin", "urdu"],
        default=None,
        help="Normalize numerals to 'latin' (0-9) or 'urdu' (۰-۹)",
    )
    norm_p.add_argument(
        "--remove-diacritics",
        action="store_true",
        help="Strip Urdu diacritics / aerab",
    )

    # 3. transliterate
    trans_p = subparsers.add_parser("transliterate", help="Transliterate text between scripts")
    trans_p.add_argument("text", type=str, help="Text to transliterate")
    trans_p.add_argument(
        "--mode",
        choices=["to-urdu", "to-roman", "unified"],
        default="to-urdu",
        help="Transliteration direction (default: to-urdu)",
    )

    # 4. tokenize
    tok_p = subparsers.add_parser("tokenize", help="Tokenize into words or sentences")
    tok_p.add_argument("text", type=str, help="Text to tokenize")
    tok_p.add_argument(
        "--sentences",
        action="store_true",
        help="Split into sentences instead of words",
    )
    tok_p.add_argument(
        "--remove-punct",
        action="store_true",
        help="Remove standalone punctuation tokens",
    )

    # 5. sentiment
    sent_p = subparsers.add_parser("sentiment", help="Analyze sentiment polarity")
    sent_p.add_argument("text", type=str, help="Text to analyze")
    sent_p.add_argument(
        "--json", action="store_true", help="Output full analysis result as JSON"
    )

    # 6. stats
    stats_p = subparsers.add_parser("stats", help="Compute text statistics & metrics")
    stats_p.add_argument("text", type=str, help="Text to evaluate")
    stats_p.add_argument(
        "--top-words",
        type=int,
        default=0,
        metavar="N",
        help="Include top N frequent words in stats output",
    )

    # 7. stopwords
    sw_p = subparsers.add_parser("stopwords", help="Remove stopwords from text")
    sw_p.add_argument("text", type=str, help="Text to filter")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "detect":
        res = detect_script(args.text)
        print(res.value)

    elif args.command == "normalize":
        res = normalize(
            args.text,
            remove_diacritics=args.remove_diacritics,
            normalize_digits_to=args.digits,
        )
        print(res)

    elif args.command == "transliterate":
        if args.mode == "to-urdu":
            print(roman_to_urdu(args.text))
        elif args.mode == "to-roman":
            print(urdu_to_roman(args.text))
        elif args.mode == "unified":
            print(to_urdu_script(args.text))

    elif args.command == "tokenize":
        if args.sentences:
            sents = split_sentences(args.text)
            for s in sents:
                print(s)
        else:
            words = tokenize_words(args.text, remove_punct=args.remove_punct)
            print(" ".join(words))

    elif args.command == "sentiment":
        res = analyze_sentiment(args.text)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"{res['label']} (score: {res['score']})")

    elif args.command == "stats":
        stats = text_stats(args.text)
        if args.top_words > 0:
            stats["top_words"] = top_words(args.text, n=args.top_words)
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.command == "stopwords":
        filtered = remove_stopwords(args.text)
        print(filtered)

    return 0


if __name__ == "__main__":
    sys.exit(main())
