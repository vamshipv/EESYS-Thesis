"""Markdown report for one prompt-comparison results file (written next to it).

python -m experiments.prompt_comparison.analyze experiments/prompt_comparison/results/<name>.jsonl
"""
import json
import math
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from data.schema import EMOTIONS


def f1_per_class(gold: list[str], pred: list[str]) -> dict[str, float]:
    """F1 for each emotion (0 if it has no true positives)."""
    out = {}
    for e in EMOTIONS:
        tp = sum(g == e and p == e for g, p in zip(gold, pred))
        fp = sum(g != e and p == e for g, p in zip(gold, pred))
        fn = sum(g == e and p != e for g, p in zip(gold, pred))
        out[e] = 2 * tp / (2 * tp + fp + fn) if tp else 0.0
    return out


def macro_f1(gold: list[str], pred: list[str]) -> tuple[float, dict[str, float]]:
    """(macro-F1, per-class F1)."""
    per = f1_per_class(gold, pred)
    return sum(per.values()) / len(per), per


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar p-value: binomial test (p=0.5) on the b + c discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def table(header: list[str], rows: list[list]) -> list[str]:
    return (["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
            + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def mark(r: dict) -> str:
    return r["pred"] + (" ✓" if r["correct"] else "")


def headline(groups: dict[tuple, list[dict]]) -> list[str]:
    rows = []
    for (v, o), rs in groups.items():
        mf1, per = macro_f1([r["gold"] for r in rs], [r["pred"] for r in rs])
        worst = min(per, key=per.get)
        mass = [r["label_mass"] for r in rs]
        rows.append([v, o, len(rs), pct(sum(r["correct"] for r in rs) / len(rs)), f"{mf1:.3f}",
                     *(f"{per[e]:.2f}" for e in EMOTIONS), f"{worst} ({per[worst]:.2f})",
                     f"{sum(mass) / len(mass):.3f}", pct(sum(m < 0.9 for m in mass) / len(mass)),
                     pct(sum(m < 0.5 for m in mass) / len(mass)),
                     f"{sum(r['seconds'] for r in rs) / len(rs):.2f}"])
    return table(["version", "order", "n", "acc", "macro-F1", *(f"F1 {e[:4]}" for e in EMOTIONS),
                  "worst class", "mean mass", "mass<0.9", "mass<0.5", "mean s"], rows)


def confusion(rs: list[dict]) -> list[str]:
    counts = Counter((r["gold"], r["pred"]) for r in rs)
    head = ["gold \\ pred", *EMOTIONS]
    count_rows = [[g, *(counts[g, p] for p in EMOTIONS)] for g in EMOTIONS]
    count_rows.append(["**pred total**", *(sum(counts[g, p] for g in EMOTIONS) for p in EMOTIONS)])
    norm_rows = []
    for g in EMOTIONS:
        tot = sum(counts[g, p] for p in EMOTIONS) or 1
        norm_rows.append([g, *(pct(counts[g, p] / tot) for p in EMOTIONS)])
    return (["Counts:", ""] + table(head, count_rows)
            + ["", "Row-normalised:", ""] + table(head, norm_rows))


def flips(a: str, b: str, ra: list[dict], rb: list[dict]) -> list[str]:
    by_b = {r["id"]: r for r in rb}
    pairs = [(x, by_b[x["id"]]) for x in ra if x["id"] in by_b]
    both = sum(x["correct"] and y["correct"] for x, y in pairs)
    broke = sum(x["correct"] and not y["correct"] for x, y in pairs)
    fixed = sum(not x["correct"] and y["correct"] for x, y in pairs)
    wrong = [(x, y) for x, y in pairs if not x["correct"] and not y["correct"]]
    same_wrong = sum(x["pred"] == y["pred"] for x, y in wrong)
    agree = sum(x["pred"] == y["pred"] for x, y in pairs) / len(pairs)
    lines = table(["both right", f"broke ({a} right, {b} wrong)", f"fixed ({a} wrong, {b} right)",
                   "both wrong, same label", "both wrong, different", "pred agreement",
                   "McNemar p (exact)"],
                  [[both, broke, fixed, same_wrong, len(wrong) - same_wrong, pct(agree),
                    f"{mcnemar_exact(broke, fixed):.3f}"]])
    flipped = [(x, y) for x, y in pairs if x["pred"] != y["pred"]]
    if flipped:
        lines += ["", f"Texts where the prediction changed ({len(flipped)}):", ""] + table(
            ["id", "text", "gold", f"pred {a}", f"pred {b}"],
            [[x["id"], cell(x["text"]), x["gold"], mark(x), mark(y)] for x, y in flipped])
    return lines


def order_checks(by_order: dict[str, list[dict]]) -> list[str]:
    scores = {o: macro_f1([r["gold"] for r in rs], [r["pred"] for r in rs])
              for o, rs in by_order.items()}
    spread = max(s[0] for s in scores.values()) - min(s[0] for s in scores.values())
    lines = [f"Macro-F1 spread across orders (max - min): **{spread:.3f}**", ""]
    lines += table(["order", "labels order", "macro-F1", *(f"F1 {e[:4]}" for e in EMOTIONS)],
                   [[o, ", ".join(by_order[o][0]["labels_order"]), f"{s[0]:.3f}",
                     *(f"{s[1][e]:.2f}" for e in EMOTIONS)] for o, s in scores.items()])

    per_text = defaultdict(dict)
    for o, rs in by_order.items():
        for r in rs:
            per_text[r["id"]][o] = r
    full = {i: p for i, p in per_text.items() if len(p) == len(by_order)}
    bad = {i: p for i, p in full.items() if len({r["pred"] for r in p.values()}) > 1}
    n_ok = len(full) - len(bad)
    lines += ["", f"Per-text consistency (same pred under all {len(by_order)} orders): "
              f"**{pct(n_ok / len(full)) if full else 'n/a'}** ({n_ok}/{len(full)})", ""]

    pos = Counter(r["labels_order"].index(r["pred"]) for rs in by_order.values() for r in rs)
    total = sum(pos.values())
    lines += ["Prediction rate by list position (expected ~16.7% each):", ""] + table(
        [f"pos {k + 1}" for k in range(len(EMOTIONS))],
        [[pct(pos[k] / total) for k in range(len(EMOTIONS))]])
    if bad:
        lines += ["", f"Inconsistent texts ({len(bad)}):", ""] + table(
            ["id", "text", "gold", *by_order],
            [[i, cell(p[next(iter(p))]["text"]), p[next(iter(p))]["gold"],
              *(p[o]["pred"] for o in by_order)] for i, p in bad.items()])
    return lines


def report(path: Path) -> str:
    """Full markdown report for one results JSONL."""
    with open(path, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    meta_path = path.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["version"], r["order_id"]].append(r)
    groups = dict(sorted(groups.items()))
    versions = sorted({v for v, _ in groups})
    orders = sorted({o for _, o in groups})
    ollama = rows[0]["backend"] == "ollama"

    out = [f"# Prompt comparison report: {path.stem}", "",
           f"- Backend: {rows[0]['backend']}, model: {rows[0]['model']}",
           f"- Sample: {meta.get('sample', '?')}"
           + (f" (limit {meta['limit']})" if meta.get("limit") else ""),
           f"- Rows: {len(rows)}; versions: {', '.join(versions)}; orders: {', '.join(orders)}",
           f"- Prompt hashes: {meta.get('prompt_hashes', {})}; git: {meta.get('git_commit', '?')}",
           "- label_mass = probability on label tokens before renormalising"
           + (" (Ollama: top-20 logprobs only, so a lower bound)." if ollama else "."),
           "", "## Headline", ""] + headline(groups)

    out += ["", "## Confusion matrices"]
    for (v, o), rs in groups.items():
        out += ["", f"### {v} / {o}", ""] + confusion(rs)

    if len(versions) > 1:
        out += ["", "## Flip tables (same order)"]
        for o in orders:
            for a, b in combinations(versions, 2):
                if (a, o) in groups and (b, o) in groups:
                    out += ["", f"### {a} vs {b} ({o})", ""] + flips(a, b, groups[a, o], groups[b, o])

    if len(orders) > 1:
        out += ["", "## Label-order checks"]
        for v in versions:
            by_order = {o: groups[v, o] for o in orders if (v, o) in groups}
            if len(by_order) > 1:
                out += ["", f"### {v}", ""] + order_checks(by_order)
    return "\n".join(out) + "\n"


def main() -> None:
    path = Path(sys.argv[1])
    out = path.with_name(path.stem + ".report.md")
    out.write_text(report(path), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
