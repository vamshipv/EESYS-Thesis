# Plan: prompt comparison (v1/v2/v3) + label-order test

For Claude Code. Background and reasoning: vault note "Prompt comparison and label-order protocol".
Work in small steps and stop after each numbered step so I can check it. Don't change existing
behaviour of the main code: only add to it.

## Goal
Choose one prompt version and one label order for Llama 3.1 8B Instruct on a fixed validation
sample, comparing them with macro-F1, confusion matrices, flip tables + McNemar, and a
label-order rotation check. Run on Ollama (4-bit) first as a dry run, then on HF bf16.

## Constraints
- Run everything from the master code root: `python -m experiments.prompt_comparison.<script>`.
- Use only packages already in requirements.txt. No pandas/sklearn/scipy: metrics and
  McNemar in plain Python (exact McNemar via a binomial test with `math.comb`). If plots
  need matplotlib, ask me before adding it.
- Never touch the test split. Never overwrite existing sample files, prompt files or result logs.
- Deterministic: temperature 0, same settings for every version.

---

## Step 1: build the larger dev set
- Run `data.build_sample.build_sample(split="validation", n_per_label=25, seed=42,
  min_words=5, max_words=15, out_name="dev_large")`. Same seed and filter as `dev`, so
  `dev` is nested inside it. Disgust has only 28 texts with this filter, so 25 is the max round number.
- Don't change the `__main__` block of build_sample.py; run it from a one-off command
  and add the call to the module docstring under "Sets used in the thesis".
- Add a test in tests/test_data.py: `dev_large` loads (150 texts, 25 per emotion) and
  every `dev` id is in `dev_large`.

## Step 2: prompt v3 (system message version) + messages builder
- v3 = the same wording as v2, but split into a system message (instruction + label list)
  and a user message (only the text):
  - system: `You classify the emotion of a text. Answer in lowercase with exactly one word from: {labels}.`
  - user: `{text}`
- Template format: in `prompts/v3.txt`, a line `<<<USER>>>` separates the system part (above)
  from the user part (below). v1/v2 have no separator, so they're user-only (as now).
- In `prompts/__init__.py` add `build_messages(text, version, labels=None) -> list[dict]`
  returning chat messages (`[{"role": "system", ...}, {"role": "user", ...}]` or user-only).
  `labels` defaults to `EMOTIONS`; passing another order is how the rotation test works.
  Keep `build_prompt` working exactly as now. Update the module docstring with the v3 entry
  (date 2026-11-21).
- Tests: v1/v2 give one user message identical to `build_prompt`; v3 gives system + user;
  a custom `labels` order appears in the text.

## Step 3: backends.py (one scoring rule for both backends)
- `experiments/prompt_comparison/backends.py` with two functions taking a messages list:
  - `score_ollama(messages, model="llama3.1")`: based on ollama_calls_test.py (top-20 logprobs)
  - `score_hf(messages)`: based on llama_hf_test.py (reuse its `load_model()`; full distribution)
- Both return the same dict: `probs` (6 labels, renormalised), `label_mass` (share of
  probability on label tokens before renormalising; for Ollama, from the top 20 only),
  `top_tokens` (top 5), `pred` (argmax label), `seconds`.
- One shared rule for matching tokens to labels (currently different between the two
  scripts): a first token counts for a label if, after strip+lower, the label starts with it
  and it has at least 3 characters (the HF rule). Put the rule in one helper used by both.
- Don't edit ollama_calls_test.py or llama_hf_test.py.
- Before writing run.py, print the fully rendered HF chat prompt for one v2 and one v3
  example so I can check the system message (Llama 3.1's template adds its own date lines).

## Step 4: orders.py
- `ORDERS`: 6 cyclic rotations of `EMOTIONS`, ids `O1`..`O6`, where `O1` = `EMOTIONS`
  (canonical). Each emotion appears in each position exactly once.

## Step 5: run.py
- CLI: `--backend {ollama,hf}`, `--sample` (default `dev_large`), `--versions` (e.g. v1 v2 v3),
  `--orders` (default `O1`), `--limit N` (first N texts, for quick tests), `--tag` (optional).
- One run = all texts × versions × orders. Writes
  `experiments/prompt_comparison/results/<date>_<backend>_<tag>.jsonl`, one row per call:
  `id, text, gold, version, order_id, labels_order, pred, correct, probs, label_mass,
  top_tokens, seconds, backend, model`. Plus a `<same name>.meta.json` with: sample name,
  prompt file hashes (short sha256), backend, model id/revision, decoding settings, git commit,
  start/end time.
- **Resumable**: append each row as soon as it's done and skip (id, version, order_id) rows
  already in the file, so the long bf16 run can be stopped and continued.
- Print progress with an estimated time left.
- Commit result logs to git (they're small and they're thesis evidence). Make sure
  .gitignore doesn't hide `experiments/prompt_comparison/results/`.

## Step 6: analyze.py
- Input: one results jsonl. Output: a markdown report next to it (`<name>.report.md`) that
  I can read in VS Code and paste into the vault.
- **Headline table** per version (and per order if more than one): accuracy, macro-F1,
  per-class F1, worst-class F1 (which), mean label_mass, % rows with label_mass < 0.5
  (our "invalid" rate), mean seconds.
- **Confusion matrices** per version: rows = gold, columns = pred, as counts and as
  row-normalised %.
- **Flip tables** for every pair of versions (same order): both right / A right B wrong
  ("broke") / A wrong B right ("fixed") / both wrong (same wrong label vs different),
  agreement %, exact McNemar p-value, and the list of flipped texts (id, text, gold, pred A, pred B).
- **Order checks** (when more than one order): macro-F1 per order and spread (max - min);
  per-text consistency (% of texts with the same pred under all orders); prediction rate by
  list position (expected ~16.7% each); per-emotion F1 per order; list of inconsistent texts.

## Step 7: README.md
Short: what this experiment is, the exact commands below, where results go, link to the
vault note.

---

## Runs (after the code works)
1. Quick test: `--backend ollama --versions v1 v2 v3 --limit 5`
2. Ollama dry run: `--backend ollama --versions v1 v2 v3 --tag dryrun` → analyze. A dry run
   only (4-bit model); the decision comes from bf16.
3. Timing check: `python llama_hf_test.py 5`; note seconds/text and peak RAM; × 450 calls.
4. bf16 run: `--backend hf --versions v1 v2 v3 --tag bf16` in the background (resumable).
5. Later: label-order run on the chosen version: `--backend hf --versions <winner> --orders O1 O2 O3 O4 O5 O6`.
