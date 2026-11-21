"""
Pull GoEmotions and write a small JSONL sample for the 6 Ekman basic emotions.

Rules:
  - only examples with exactly ONE label (single emotion, no multi-label rows)
  - that label must be one of: anger, disgust, fear, joy, sadness, surprise
  - text length between --min-len and --max-len (words by default, or characters)
  - at most --per-emotion examples per emotion

Usage:
  python extract_goemotions.py
  python extract_goemotions.py --unit chars --min-len 5 --max-len 15
"""

import argparse
import json
import random
from collections import defaultdict

from datasets import load_dataset

TARGET_EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]


def text_length(text: str, unit: str) -> int:
    return len(text.split()) if unit == "words" else len(text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--split", default="train", choices=["train", "validation", "test"])
    p.add_argument("--unit", default="words", choices=["words", "chars"])
    p.add_argument("--min-len", type=int, default=5)
    p.add_argument("--max-len", type=int, default=15)
    p.add_argument("--per-emotion", type=int, default=10)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", default="goemotions_basic6.jsonl")
    args = p.parse_args()

    ds = load_dataset("google-research-datasets/go_emotions", "simplified", split=args.split)
    label_names = ds.features["labels"].feature.names  # index -> emotion name

    # Shuffle so we don't just take the first N rows; seed keeps it reproducible.
    ds = ds.shuffle(seed=args.seed)

    picked = defaultdict(list)
    for row in ds:
        if len(row["labels"]) != 1:
            continue
        emotion = label_names[row["labels"][0]]
        if emotion not in TARGET_EMOTIONS or len(picked[emotion]) >= args.per_emotion:
            continue
        text = row["text"].strip()
        if not (args.min_len <= text_length(text, args.unit) <= args.max_len):
            continue
        picked[emotion].append({"id": row["id"], "text": text, "emotion": emotion})
        if all(len(picked[e]) >= args.per_emotion for e in TARGET_EMOTIONS):
            break

    with open(args.out, "w", encoding="utf-8") as f:
        for emotion in TARGET_EMOTIONS:
            for rec in picked[emotion]:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote {args.out}")
    for emotion in TARGET_EMOTIONS:
        n = len(picked[emotion])
        flag = "" if n == args.per_emotion else f"  (only found {n})"
        print(f"  {emotion:9s} {n}{flag}")


if __name__ == "__main__":
    main()
