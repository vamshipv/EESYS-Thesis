# Plan: batching equivalence check (batched vs. one-text-per-pass scoring)

For Claude Code. Background and reasoning: vault note `Claude outputs/Model Interface (wrapper).md`
(§5c) and the 2026-11-23 batching entry in `02_Decisions.md`. Read both first.

## Goal
Find out whether scoring several texts in one forward pass (batching) gives the **same** results
as the existing one-text-per-pass scoring, and how much faster it is on this laptop.
This is a regression check, **not tuning**: the pass criterion is "same as before", never "better".
If batched results differ beyond the thresholds, batching is not used (batch size 1 stays).

**Reference** (already exists, don't rerun it): `experiments/prompt_comparison/results/2026-11-22_hf_bf16.jsonl`,
rows with `version == "v3"` and `order_id == "O1"` (150 texts of `dev_large`). Fields used: `id`,
`probs` (6 renormalised, dict by label), `label_mass`, `pred`, `seconds`.

## Fixed rules (set 2026-11-23, before any batched run; don't change them after seeing results)
- **Left padding** is a correctness rule, not a test condition. Right padding is never run.
- Batched scoring **passes** for a batch size only if, against the reference, on all 150 texts:
  1. max |Δ probability| over all 6 labels and all texts **< 0.01**
  2. predicted label identical on **150/150** texts
  3. max |Δ label_mass| **< 0.01**
- Report the single-vs-single control (step 3) next to it, so the size of normal run-to-run wobble is visible.

## Constraints
- Run from the master code root: `python -m experiments.batching_check.<script>`.
- **Don't change existing code** (`experiments/prompt_comparison/backends.py`, `score_hf`, `prompts/`, `data/`,
  `llama_hf_test.py`). Only add new files in `experiments/batching_check/` (+ a test file). Import and reuse:
  `load_model` (llama_hf_test), `hf_tokenizer`, `hf_label_ids`, `hf_input_ids`, `summarise`, `score_hf` (backends),
  `build_messages` (prompts), `load_samples` (data). Same label-token rule, same model id/revision, bf16,
  same `max_memory` as the reference run.
- Only packages already in requirements.txt. Plain Python for the comparison maths.
- Never touch the test split. Never overwrite existing result files.
- Check `git status` first: if the working tree is dirty, stop and tell me (the run meta must show a clean commit).
- Prompt v3, order O1 only (= `build_messages(text, "v3")`).

---

## Step 1: batched scorer (`experiments/batching_check/batch_scoring.py`)
`score_hf_batch(messages_list, batch_size) -> list[dict]` returning, per text and **in input order**, the same
dict shape as `score_hf` (probs, label_mass, pred, top_tokens, n_input_tokens), plus per-chunk timing.
- Split the input into chunks of `batch_size` (last chunk may be smaller).
- Render each prompt with the same chat template as `hf_input_ids` (`add_generation_prompt=True`).
- **Pad token:** Llama 3.1 has none set. Use `<|finetune_right_pad_id|>` if it exists in the vocab, else the eos
  token. Record which id was used in the meta.
- **Left padding** (`padding_side="left"`), pass the `attention_mask`, and pass explicit
  `position_ids = attention_mask.cumsum(-1) - 1` (clamped at 0), so real tokens get the same positions as in an
  unpadded single run.
- Read logits at position `-1` for every row (valid because of left padding), `.float()`, softmax over the full
  vocab, then the same label scoring as `score_hf` (reuse `hf_label_ids` + `summarise`).
- If a chunk raises CUDA/CPU out-of-memory: log it, mark that batch size as failed with reason "OOM",
  and continue with the next condition. Don't crash the whole run.

## Step 2: tests (`tests/test_batching_check.py`, tokenizer only, no model weights)
- With 3 prompts of different lengths, batched rendering is left-padded: every row ends with the same last token
  as its unpadded `hf_input_ids` version, the attention mask is 0 exactly on the pads, and the non-pad tokens equal
  the unpadded ids.
- position_ids of the real tokens are `0..n-1` for each row.
- Output order equals input order (e.g. with a fake scorer).
Run the full test suite; all existing tests must still pass.

## Step 3: short checks (~20 min); stop if either fails
a) **Single vs. single control:** first 20 texts of `dev_large` (same order as the reference), scored with the
   existing `score_hf` (unchanged). Compare with the reference → this is the normal run-to-run wobble.
b) **Batched scorer at batch size 1** on the same 20 texts → must match (a) to < 1e-4 (no padding happens, so the
   new code path must be equivalent to `score_hf`). If not, there is a bug in step 1: stop and tell me.

## Step 4: batched runs (long part, can run unattended)
- All 150 texts, batch size **4**, then batch size **8**. Same text order as the reference.
- Resumable like `experiments/prompt_comparison/run.py` (append one JSONL row per text, skip done keys on restart).
- Output: `experiments/batching_check/results/2026-11-23_hf_bf16_batch.jsonl` (+ `.meta.json`), one row per
  (condition, text): `condition` (`single_control` / `bs1` / `bs4` / `bs8`), `id`, `text`, `probs`, `label_mass`,
  `pred`, `n_input_tokens`, `n_pad_tokens`, `chunk_index`, `chunk_seconds`, `seconds_per_text`.
- Meta: git commit, model id + revision, dtype, max_memory, pad token id, padding side, batch sizes, prompt version
  + hash (`bcf65961ce96`), sample name, start/end time, peak GPU memory per condition.
- Expected time: worst case ~1 h per batch size if batching gives no speedup; probably much less.

## Step 5: report (`experiments/batching_check/analyze.py` → `results/2026-11-23_hf_bf16_batch.report.md`)
For each condition (`single_control`, `bs1`, `bs4`, `bs8`) against the reference:
- max and mean |Δ probability| (over all labels and texts) and which text/label has the max
- max and mean |Δ label_mass|
- predicted-label agreement (n/150 or n/20) and a list of any texts whose label changed (text, both labels, both probs)
- texts with |Δ probability| ≥ 0.01, with their `n_pad_tokens` (does the difference grow with padding?)
- seconds per text and speedup vs. the reference's mean `seconds`; peak GPU memory
- **verdict per batch size: PASS / FAIL** using the three fixed rules, plus "OOM" where it applies
- one-line recommendation: the largest batch size that passed (or "batch size 1" if none passed)

## When done
Show me the report summary. Then (as CLAUDE.md says) add the result to `02_Decisions.md` (date | decision | reason),
today's log entry, and `01_Status.md`. Don't change the thresholds or rerun with other settings without asking me.
