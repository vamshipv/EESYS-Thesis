import math
from dataclasses import asdict

import requests

from data import load_samples

LABELS = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]

def predict_proba(text, model="llama3.1"):  # use the exact name from `ollama list`
    prompt = (
        "Classify the emotion of the text. Answer with exactly one word from: "
        + ", ".join(LABELS) + ".\n\nText: " + text + "\nEmotion:"
    )
    r = requests.post("http://localhost:11434/api/chat", json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,            # no reasoning text before the label
        "logprobs": True,
        "top_logprobs": 20,
        "options": {"temperature": 0, "num_predict": 3},
    }).json()
    first = r["logprobs"][0]       # first generated token
    scores = {l: 0.0 for l in LABELS}
    for t in first["top_logprobs"]:
        tok = t["token"].strip().lower()
        for l in LABELS:
            if l.startswith(tok) and tok:   # also catches split tokens like "ang"
                scores[l] += math.exp(t["logprob"])
    total = sum(scores.values()) or 1.0
    return {l: s / total for l, s in scores.items()}, first["top_logprobs"][:5]

def show(i, row, probs, top):
    pred = max(probs, key=probs.get)
    ok = "CORRECT" if pred == row["label"] else "WRONG"
    print("=" * 70)
    print(f"Sentence {i}: {row['text']}")
    print(f"  True label : {row['label']}")
    print(f"  Predicted  : {pred}  ({probs[pred]:.0%} confident)  -> {ok}")
    print("  Probability per emotion:")
    for l in sorted(probs, key=probs.get, reverse=True):
        bar = "#" * round(probs[l] * 30)
        print(f"    {l:<9} {probs[l]:6.1%}  {bar}")
    print("  Model's top first-token guesses (logprob -> probability):")
    for t in top:
        print(f"    {t['token']!r:<12} logprob {t['logprob']:7.2f}  = {math.exp(t['logprob']):6.1%}")

if __name__ == "__main__":
    rows = [asdict(s) for s in load_samples("dev")][:5]  # shared dev set (validation split)
    for i, row in enumerate(rows, 1):
        probs, top = predict_proba(row["text"])
        show(i, row, probs, top)
    print("=" * 70)