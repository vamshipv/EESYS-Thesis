"""Report for the batching check: every condition against the one-text-per-pass reference.

python -m experiments.batching_check.analyze [--stage short]
Pass rules (fixed 2026-11-23, PLAN.md): max |d prob| < 0.01, same predicted label on all texts,
max |d label_mass| < 0.01. --stage short also prints the step-3 gate (bs1 vs single_control < 1e-4).
"""
import argparse
import json
from pathlib import Path

from data.schema import EMOTIONS
from experiments.batching_check.run import CONDITIONS, OUT

REFERENCE = (Path(__file__).parents[1] / "prompt_comparison" / "results"
             / "2026-11-22_hf_bf16.jsonl")
REPORT = OUT.with_suffix(".report.md")
PROB_TOL = 0.01
MASS_TOL = 0.01
BS1_TOL = 1e-4


def read_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_reference() -> dict[str, dict]:
    """v3/O1 rows of the reference run, by id."""
    return {r["id"]: r for r in read_jsonl(REFERENCE)
            if r["version"] == "v3" and r["order_id"] == "O1"}


def compare(rows: list[dict], ref: dict[str, dict]) -> dict:
    """Differences of `rows` against `ref` (matched by id)."""
    dprob, dmass, changed, big = [], [], [], []
    worst = (0.0, None, None)
    for r in rows:
        b = ref[r["id"]]
        dm = abs(r["label_mass"] - b["label_mass"])
        dmass.append(dm)
        row_max = 0.0
        for l in EMOTIONS:
            d = abs(r["probs"][l] - b["probs"][l])
            dprob.append(d)
            row_max = max(row_max, d)
            if d > worst[0]:
                worst = (d, r["id"], l)
        if r["pred"] != b["pred"]:
            changed.append({"id": r["id"], "text": r["text"], "ref_pred": b["pred"],
                            "pred": r["pred"], "ref_probs": b["probs"], "probs": r["probs"]})
        if row_max >= PROB_TOL:
            big.append({"id": r["id"], "max_dprob": row_max,
                        "n_pad_tokens": r.get("n_pad_tokens", 0), "text": r["text"]})
    n = len(rows)
    return {"n": n, "max_dprob": max(dprob), "mean_dprob": sum(dprob) / len(dprob),
            "worst": worst, "max_dmass": max(dmass), "mean_dmass": sum(dmass) / n,
            "agree": n - len(changed), "changed": changed, "big": big,
            "sec_per_text": sum(r["seconds_per_text"] for r in rows) / n,
            "ref_sec": sum(ref[r["id"]]["seconds"] for r in rows) / n}


def verdict(c: dict, n_expected: int) -> str:
    if c["n"] < n_expected:
        return f"INCOMPLETE ({c['n']}/{n_expected})"
    ok = c["max_dprob"] < PROB_TOL and c["agree"] == c["n"] and c["max_dmass"] < MASS_TOL
    return "PASS" if ok else "FAIL"


def bs1_gate(by_cond: dict[str, list[dict]]) -> float | None:
    """Max |d prob| and |d mass| between bs1 and single_control on their shared texts."""
    if not {"bs1", "single_control"} <= by_cond.keys():
        return None
    a = {r["id"]: r for r in by_cond["single_control"]}
    diffs = [abs(r["probs"][l] - a[r["id"]]["probs"][l]) for r in by_cond["bs1"] if r["id"] in a
             for l in EMOTIONS]
    diffs += [abs(r["label_mass"] - a[r["id"]]["label_mass"]) for r in by_cond["bs1"]
              if r["id"] in a]
    return max(diffs)


def fmt_probs(p: dict) -> str:
    return ", ".join(f"{l[:3]} {p[l]:.3f}" for l in EMOTIONS)


def build_report(stage: str | None) -> str:
    ref = load_reference()
    rows = read_jsonl(OUT)
    meta_path = OUT.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    cmeta = meta.get("conditions", {})
    by_cond: dict[str, list[dict]] = {}
    for r in rows:
        by_cond.setdefault(r["condition"], []).append(r)

    lines = ["# Batching equivalence check (bf16 Llama, v3/O1, dev_large)", "",
             f"Reference: `{REFERENCE.name}` (v3/O1, one text per forward pass, {len(ref)} texts).",
             f"Results: `{OUT.name}`; git commit {meta.get('git_commit', '?')}; pad token "
             f"{meta.get('pad_token')} (id {meta.get('pad_token_id')}), padding "
             f"{meta.get('padding_side')}.",
             f"Pass rules (fixed before the runs): max |Δp| < {PROB_TOL}, predicted label identical "
             f"on all texts, max |Δ label_mass| < {MASS_TOL}.", "",
             "| condition | n | max abs Δp (text, label) | mean abs Δp | max abs Δmass | mean abs Δmass "
             "| same pred | s/text | ref s/text | speedup | peak GPU GiB | verdict |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    results = {}
    for cond in CONDITIONS:
        cm = cmeta.get(cond, {})
        if cond not in by_cond:
            if cm.get("status") == "OOM":
                lines.append(f"| {cond} | 0 | | | | | | | | | | OOM |")
                results[cond] = "OOM"
            continue
        c = compare(by_cond[cond], ref)
        v = "OOM" if cm.get("status") == "OOM" else verdict(c, cm.get("n_texts", c["n"]))
        results[cond] = v
        c["verdict"] = v
        by_cond[cond + "_cmp"] = c  # type: ignore[assignment]
        peak = cm.get("peak_gpu_gib")
        lines.append(
            f"| {cond} | {c['n']} | {c['max_dprob']:.2e} ({c['worst'][1]}, {c['worst'][2]}) "
            f"| {c['mean_dprob']:.2e} | {c['max_dmass']:.2e} | {c['mean_dmass']:.2e} "
            f"| {c['agree']}/{c['n']} | {c['sec_per_text']:.1f} | {c['ref_sec']:.1f} "
            f"| {c['ref_sec'] / c['sec_per_text']:.2f}x | "
            f"{f'{peak:.2f}' if peak is not None else '-'} | {v} |")

    gate = bs1_gate(by_cond)
    if gate is not None:
        lines += ["", f"**Step-3 gate** (bs1 vs. single_control, same texts): max abs difference "
                      f"{gate:.2e} -> {'OK' if gate < BS1_TOL else 'FAIL'} (needs < {BS1_TOL:g})."]

    for cond in CONDITIONS:
        c = by_cond.get(cond + "_cmp")
        if not c:
            continue
        lines += ["", f"## {cond}"]
        if c["changed"]:
            lines.append("Predicted label changed:")
            for x in c["changed"]:
                lines.append(f"- `{x['id']}` {x['ref_pred']} -> {x['pred']}: {x['text']!r}  \n"
                             f"  ref [{fmt_probs(x['ref_probs'])}]  \n  new [{fmt_probs(x['probs'])}]")
        else:
            lines.append("Predicted label changed: none.")
        if c["big"]:
            lines.append(f"Texts with max abs Δp ≥ {PROB_TOL} (with pad tokens):")
            for x in sorted(c["big"], key=lambda x: -x["max_dprob"]):
                lines.append(f"- `{x['id']}` Δp {x['max_dprob']:.3f}, {x['n_pad_tokens']} pads: "
                             f"{x['text']!r}")
        else:
            lines.append(f"Texts with max abs Δp ≥ {PROB_TOL}: none.")
        if cond in ("bs4", "bs8"):
            rs = by_cond[cond]
            pads = sorted({r["n_pad_tokens"] for r in rs})
            groups = {"0 pads": [r for r in rs if r["n_pad_tokens"] == 0],
                      "1-5 pads": [r for r in rs if 1 <= r["n_pad_tokens"] <= 5],
                      ">5 pads": [r for r in rs if r["n_pad_tokens"] > 5]}
            parts = []
            for name, g in groups.items():
                if g:
                    d = compare(g, ref)
                    parts.append(f"{name}: n={d['n']}, max abs Δp {d['max_dprob']:.2e}, "
                                 f"mean {d['mean_dprob']:.2e}")
            lines.append(f"Padding range {pads[0]}-{pads[-1]}. By padding: " + "; ".join(parts) + ".")

    passed = [c for c in ("bs8", "bs4") if results.get(c) == "PASS"]
    if stage != "short":
        rec = (f"batch size {passed[0][2:]}" if passed else "batch size 1")
        lines += ["", f"**Recommendation:** {rec} (largest batch size that passed)."]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["short", "full"], default="full")
    args = ap.parse_args()
    report = build_report(args.stage)
    print(report)
    if args.stage == "full":
        REPORT.write_text(report, encoding="utf-8")
        print(f"-> {REPORT}")


if __name__ == "__main__":
    main()
