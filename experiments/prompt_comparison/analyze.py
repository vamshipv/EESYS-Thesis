"""Markdown report for one or more prompt-comparison results files.

python -m experiments.prompt_comparison.analyze <file1.jsonl> [<file2.jsonl> ...] [--out NAME]
One file: report next to it (<name>.report.md). Several files: rows are merged into one report,
results/<date>_combined_<backend>.report.md (or results/<NAME>.report.md with --out). Files are
only merged if backend, model, sample, label-token rule and decoding match.
"""
import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

from data.schema import EMOTIONS

LOW_MASS = 0.9  # label-mass selection criterion (02_Decisions 2026-11-21)
MERGE_KEYS = ("backend", "model", "sample", "label_token_rule", "decoding")


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


def pred_counts(rs: list[dict]) -> Counter:
    return Counter(r["pred"] for r in rs)


def paired(ra: list[dict], rb: list[dict]) -> list[tuple[dict, dict]]:
    by_b = {r["id"]: r for r in rb}
    return [(x, by_b[x["id"]]) for x in ra if x["id"] in by_b]


# --- stats used by the tables and the decision check -------------------------------------

def flip_stats(ra: list[dict], rb: list[dict]) -> dict:
    """Prediction flips A -> B: broke = A right & B wrong, fixed = A wrong & B right."""
    pairs = paired(ra, rb)
    wrong = [(x, y) for x, y in pairs if not x["correct"] and not y["correct"]]
    s = {"n": len(pairs),
         "both": sum(x["correct"] and y["correct"] for x, y in pairs),
         "broke": sum(x["correct"] and not y["correct"] for x, y in pairs),
         "fixed": sum(not x["correct"] and y["correct"] for x, y in pairs),
         "same_wrong": sum(x["pred"] == y["pred"] for x, y in wrong),
         "diff_wrong": sum(x["pred"] != y["pred"] for x, y in wrong),
         "agree": sum(x["pred"] == y["pred"] for x, y in pairs) / len(pairs)}
    s["p"] = mcnemar_exact(s["broke"], s["fixed"])
    return s


def mass_stats(ra: list[dict], rb: list[dict]) -> dict:
    """Paired label mass A vs B: texts below LOW_MASS for A only / B only / both / neither."""
    pairs = paired(ra, rb)
    lo = [(x["label_mass"] < LOW_MASS, y["label_mass"] < LOW_MASS) for x, y in pairs]
    s = {"n": len(pairs),
         "a_only": sum(a and not b for a, b in lo), "b_only": sum(b and not a for a, b in lo),
         "both": sum(a and b for a, b in lo), "neither": sum(not a and not b for a, b in lo),
         "b_higher": sum(y["label_mass"] > x["label_mass"] for x, y in pairs)}
    s["p"] = mcnemar_exact(s["a_only"], s["b_only"])
    return s


# --- report sections ----------------------------------------------------------------------

def headline(groups: dict[tuple, list[dict]]) -> list[str]:
    rows = []
    for (v, o), rs in groups.items():
        mf1, per = macro_f1([r["gold"] for r in rs], [r["pred"] for r in rs])
        worst = min(per, key=per.get)
        mass = [r["label_mass"] for r in rs]
        counts = pred_counts(rs)
        rows.append([v, o, len(rs), pct(sum(r["correct"] for r in rs) / len(rs)), f"{mf1:.3f}",
                     *(f"{per[e]:.2f}" for e in EMOTIONS), f"{worst} ({per[worst]:.2f})",
                     f"{sum(mass) / len(mass):.3f}", pct(sum(m < LOW_MASS for m in mass) / len(mass)),
                     pct(sum(m < 0.5 for m in mass) / len(mass)),
                     *(counts[e] for e in EMOTIONS),
                     f"{sum(r['seconds'] for r in rs) / len(rs):.2f}"])
    return table(["version", "order", "n", "acc", "macro-F1", *(f"F1 {e[:4]}" for e in EMOTIONS),
                  "worst class", "mean mass", "mass<0.9", "mass<0.5",
                  *(f"#pred {e[:4]}" for e in EMOTIONS), "mean s"], rows)


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
    s = flip_stats(ra, rb)
    lines = ["Predictions:", ""] + table(
        ["both right", f"broke ({a} right, {b} wrong)", f"fixed ({a} wrong, {b} right)",
         "both wrong, same label", "both wrong, different", "pred agreement", "McNemar p (exact)"],
        [[s["both"], s["broke"], s["fixed"], s["same_wrong"], s["diff_wrong"], pct(s["agree"]),
          f"{s['p']:.3f}"]])
    m = mass_stats(ra, rb)
    lines += ["", f"Label mass (< {LOW_MASS}):", ""] + table(
        [f"low {a} only", f"low {b} only", "low both", "low neither", "McNemar p (exact)",
         f"{b} mass > {a} mass"],
        [[m["a_only"], m["b_only"], m["both"], m["neither"], f"{m['p']:.3f}",
          f"{m['b_higher']}/{m['n']}"]])
    flipped = [(x, y) for x, y in paired(ra, rb) if x["pred"] != y["pred"]]
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


# Fixed before the v4 run (02_Decisions 2026-11-22, "Post-hoc check: prompt v4"). Don't change.
V4_MAX_LOW_MASS = 4
V4_MAX_ANGER = 37
V4_MAX_ANY_LABEL = 41
ALPHA = 0.05


def v4_decision_check(v3: list[dict], v4: list[dict]) -> list[str]:
    """PASS/FAIL per condition of the fixed v4 rule; v4 replaces v3 only if all pass."""
    m, f, counts = mass_stats(v3, v4), flip_stats(v3, v4), pred_counts(v4)
    n_low = sum(r["label_mass"] < LOW_MASS for r in v4)
    top_label, top_n = counts.most_common(1)[0]
    c1 = n_low <= V4_MAX_LOW_MASS and not (m["p"] < ALPHA and m["b_only"] > m["a_only"])
    c2 = counts["anger"] <= V4_MAX_ANGER and top_n <= V4_MAX_ANY_LABEL
    c3 = not (f["p"] < ALPHA and f["broke"] > f["fixed"])
    res = lambda ok: "**PASS**" if ok else "**FAIL**"
    return ["## v4 decision check (rule fixed in 02_Decisions, 2026-11-22)", "",
            f"1. Label mass not worse: {res(c1)}. v4 texts with mass < {LOW_MASS}: {n_low} "
            f"(limit {V4_MAX_LOW_MASS}); paired low v3 only / v4 only: {m['a_only']} / {m['b_only']}, "
            f"McNemar p = {m['p']:.3f}.",
            f"2. Anger sink reduced: {res(c2)}. v4 anger predicted {counts['anger']} "
            f"(limit {V4_MAX_ANGER}); most-predicted label {top_label} {top_n} (limit {V4_MAX_ANY_LABEL}).",
            f"3. Macro-F1 not significantly worse: {res(c3)}. v4 broke / fixed vs v3: "
            f"{f['broke']} / {f['fixed']}, McNemar p = {f['p']:.3f}.",
            "", f"**Result: {'v4 replaces v3' if c1 and c2 and c3 else 'v3 stays'}.**", ""]


# --- loading and merging ------------------------------------------------------------------

def load(path: Path) -> tuple[list[dict], dict]:
    """Rows and meta (empty dict if there is no meta file) of one results JSONL."""
    with open(path, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    meta_path = path.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    return rows, meta


def merge(sources: list[tuple[Path, list[dict], dict]]) -> list[dict]:
    """Concatenate rows of several files; raise ValueError if their setups differ or a
    (id, version, order) appears twice."""
    first_path, _, first_meta = sources[0]
    for path, _, meta in sources[1:]:
        for k in MERGE_KEYS:
            if meta.get(k) != first_meta.get(k):
                raise ValueError(f"Can't merge: '{k}' differs between {first_path.name} "
                                 f"({first_meta.get(k)}) and {path.name} ({meta.get(k)}).")
    seen: dict[tuple, str] = {}
    rows = []
    for path, rs, _ in sources:
        for r in rs:
            key = (r["id"], r["version"], r["order_id"])
            if key in seen:
                raise ValueError(f"Can't merge: {key} is in both {seen[key]} and {path.name}.")
            seen[key] = path.name
            rows.append(r)
    return rows


def report(sources: list[tuple[Path, list[dict], dict]], title: str,
           extra: list[str] | None = None) -> str:
    """Full markdown report for the merged rows of one or more results files."""
    rows = merge(sources)
    meta = sources[0][2]
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["version"], r["order_id"]].append(r)
    groups = dict(sorted(groups.items()))
    versions = sorted({v for v, _ in groups})
    orders = sorted({o for _, o in groups})
    ollama = rows[0]["backend"] == "ollama"

    out = [f"# Prompt comparison report: {title}", "",
           f"- Backend: {rows[0]['backend']}, model: {rows[0]['model']}",
           f"- Sample: {meta.get('sample', '?')}"
           + (f" (limit {meta['limit']})" if meta.get("limit") else ""),
           f"- Rows: {len(rows)}; versions: {', '.join(versions)}; orders: {', '.join(orders)}",
           "- Sources:"]
    for path, rs, m in sources:
        out.append(f"  - `{path.name}` ({len(rs)} rows): git {m.get('git_commit', '?')}, "
                   f"prompt hashes {m.get('prompt_hashes', {})}")
    out += ["- label_mass = probability on label tokens before renormalising"
            + (" (Ollama: top-20 logprobs only, so a lower bound)." if ollama else ".")]
    out += [""] + (extra or [])
    if ("v3", "O1") in groups and ("v4", "O1") in groups:
        out += v4_decision_check(groups["v3", "O1"], groups["v4", "O1"])
    out += ["## Headline", ""] + headline(groups)

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
    ap = argparse.ArgumentParser(description="Prompt comparison report")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--out", default=None, help="report name (without .report.md)")
    args = ap.parse_args()
    sources = [(p, *load(p)) for p in args.files]
    if len(sources) == 1 and not args.out:
        out, title = args.files[0].with_name(args.files[0].stem + ".report.md"), args.files[0].stem
    else:
        name = args.out or f"{date.today().isoformat()}_combined_{sources[0][2].get('backend', 'x')}"
        out, title = args.files[0].parent / f"{name}.report.md", name
    if out.exists() and len(sources) > 1:
        raise FileExistsError(f"{out} exists; pick another --out.")
    try:
        text = report(sources, title)
    except ValueError as e:
        raise SystemExit(str(e))
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
