# Plan: post-hoc prompt v4 + combined v1–v4 report

For Claude Code. Stop after each step so I can check it. Background: vault `02_Decisions`
(2026-11-22, "Post-hoc check: prompt v4") and protocol note §5.1. The decision rule is already
fixed there, before the run; don't change it.

## Why
v1 = capitalised / user message, v2 = lowercase / user, v3 = lowercase / system message.
v4 = **capitalised / system message** completes the 2×2 design. bf16 suggests the system message
improves label mass and lowercase causes the anger sink; v4 tests whether we can have the first
without the second.

## Constraints
- Don't modify or overwrite `results/2026-11-22_hf_bf16.*` (the evidence for choosing v3).
  v4 goes into its own result file.
- Same settings as the 22 Nov bf16 run: `--backend hf`, `dev_large`, order `O1`, same model id
  and revision, same label-token rule. Only the prompt changes.
- No new packages. Commit before the run so the meta file has a clean git hash.

## Step 1: prompt v4
- `prompts/v4.txt` = `prompts/v3.txt` with only the words "in lowercase " removed:
  ```
  You classify the emotion of a text. Answer with exactly one word from: {labels}.
  <<<USER>>>
  {text}
  ```
- Add the v4 line to the `prompts/__init__.py` docstring (2026-11-22, post-hoc 2×2 check).
- Test: `build_messages(text, "v4")` returns system + user, and the system text equals v3's
  with "in lowercase " removed (so the two can only differ in that).
- Print the rendered HF chat prompt for one example (v3 and v4 side by side) for me to check.

## Step 2: analyze.py accepts several result files
- `python -m experiments.prompt_comparison.analyze <file1.jsonl> [<file2.jsonl> ...] [--out NAME]`
  - One file: works exactly as now (same report name).
  - Several files: merge the rows into one report. Default output name
    `results/<date>_combined_<backend>.report.md`, or `--out`.
- Before merging, check that all files share: backend, model id + revision, sample, label-token
  rule and decoding settings. Abort with a clear message if not (e.g. never mix Ollama and HF).
  Also abort if the same (id, version, order) appears in two files.
- The report header lists every source file with its git hash and prompt hashes.
- Version order in all tables: sorted (v1, v2, v3, v4).

## Step 3: label-mass comparison in the report (it's rule 1, currently computed by hand)
For every version pair (same order), add a **label-mass flip table** next to the prediction
flip table:
- texts with label_mass < 0.9 for A only / for B only / both / neither, exact McNemar p
  (only on the "A only" vs "B only" cells),
- number of texts where B's label_mass > A's (out of n).
Check: for v1 vs v3 on the existing bf16 file it must give 7 / 0, p = 0.016, and v3 higher
on 138 of 150 texts (computed by hand on 22 Nov).

Also add to the headline table: **predicted count per label** (how often each label was
predicted), so the anger-sink rule can be read directly.

## Step 4: run v4 on bf16 (~1 h)
```
python -m experiments.prompt_comparison.run --backend hf --versions v4 --tag bf16_v4
```
Quick test first with `--limit 3`, then the full run (resumable).

## Step 5: combined report
```
python -m experiments.prompt_comparison.analyze results/2026-11-22_hf_bf16.jsonl results/<date>_hf_bf16_v4.jsonl --out <date>_hf_bf16_v1-v4
```
Then add a short **"v4 decision check"** section at the top of the combined report that
evaluates the fixed rule mechanically against v3 and prints PASS/FAIL per condition:
1. v4 texts with label_mass < 0.9 ≤ 4, and the paired label-mass McNemar is not significant
   in v3's favour (fail only if p < 0.05 with more "v4 only" low texts than "v3 only");
2. v4 anger predicted ≤ 37 and no label predicted more than 41 times;
3. v4 vs v3 macro-F1: fail only if the prediction flip table is significantly in v3's favour
   (McNemar p < 0.05 with more "v4 broke" than "v4 fixed").
Final line: "v4 replaces v3" only if all three PASS, otherwise "v3 stays".
Don't change the thresholds; they come from 02_Decisions.

## After this (not part of this plan)
I record the outcome in 02_Decisions; then the bf16 label-order test runs on whichever version
won.
