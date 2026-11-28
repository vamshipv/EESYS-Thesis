# Step 2: Standardized Prediction

Status: ready to build (planned 2026-11-28)
Build order: step 2 of 5 (component ✓ → **Standardized Prediction** → Model Interface → token deletion + metrics → runner), then the Llama component

## Read first
- `CLAUDE.md`, `thesis vault/00_Dashboard/01_Status.md`, `02_Decisions.md`
- Design: `thesis vault/Claude outputs/Model Interface (wrapper).md` §4 (three kinds of numbers), §5 (contract), §5e
  (provenance), §5f (raw shape, failures); sequence diagram §2b = arrows 4–5
- Decisions: 2026-11-21 label-token rule (the "f" fix), 2026-11-23 core contract (#1), provenance (#6), common
  interface (#7)
- Existing reference code: `experiments/prompt_comparison/backends.py` (`match_label`, `label_first_tokens`,
  `summarise`). Its rule produced the frozen v3/O1 results.
- Step 1 code: `models/base.py` (`RawOutput`), `models/fake_model.py`

## Goal
Turn one component's raw output (`RawOutput`: token/probability pairs) into one standard `Prediction`:
label-token rule → raw label probabilities → label mass → renormalised six probabilities in `EMOTIONS` order →
predicted label. One implementation for every component (Llama, API, FakeModel), so outputs stay comparable (T1).

## Scope
Create:
- `prediction/__init__.py` (exports `Prediction`, `LabelTokenRule`, `standardize`, `LLAMA31_FIRST_TOKENS`)
- `prediction/schema.py` (`Prediction`)
- `prediction/label_tokens.py` (`LabelTokenRule`, `LLAMA31_FIRST_TOKENS`)
- `prediction/standardize.py` (`standardize`, `standardize_batch`)
- `tests/test_prediction.py`

Do NOT build: Model Interface (where the prompt, fingerprint and access level live: step 3), XAI, runner, Llama
component. Do NOT change `experiments/prompt_comparison/` (it is the frozen reference; only import it in tests).

## Spec: the label-token rule (`prediction/label_tokens.py`)

**Must behave exactly like `backends.match_label`.** That rule is frozen with prompt v3; a different rule would make new
results incomparable with the prompt experiments. Moving it here is a copy, not a redesign.

A first answer token counts for a label if
(a) after `strip()` + `lower()` it has ≥ 3 characters (`MIN_TOKEN_CHARS`) and a label starts with it
    ("anger", " Ang", "sad", "SURPRISE"), or
(b) it is exactly one of the model tokenizer's own first tokens of a label, lowercase or capitalised (adds "f" for
    lowercase "fear", which Llama splits into "f" + "ear").
Otherwise `None` (e.g. "neutral", "Rel", "frustration", "<off_label>", "f" without a table). Assert that a token never
matches two labels (as the reference does).

`LabelTokenRule` (frozen dataclass; a class because it holds state and has per-model versions):
- `first_tokens: Mapping[str, str]` (token → label; part (b)); default empty
- `rule_id: str = "label-token-v2"` (the 21 Nov rule; goes into the setup fingerprint in step 3)
- `match(token: str) -> str | None`

`LLAMA31_FIRST_TOKENS: dict[str, str]`: the Llama 3.1 table as a constant, so Standardized Prediction never loads a
tokenizer. **Derive it once** by running `backends.label_first_tokens()` with the local tokenizer
(`unsloth/Llama-3.1-8B-Instruct`, revision from `llama_hf_test.py`) and copy the dict into the code with a comment
(model id + revision + date). Expected to include at least `"f": "fear"`; capitalised forms may also be split
(the results show "Ang" for "Anger"). Do not guess entries.

Which table a component uses: proposed `ModelComponent.label_first_tokens` attribute (FakeModel: empty, Llama:
`LLAMA31_FIRST_TOKENS`, API: its own table later), read by the Model Interface in step 3. **Not built in this step;
just keep `standardize` taking the rule as a parameter.**

## Spec: `Prediction` (`prediction/schema.py`, frozen dataclass)
One per text; what the runner, XAI methods and metrics see.

| Field | Type | Meaning |
|---|---|---|
| `status` | `Literal["ok", "off_label", "failed"]` | `ok`: mass > 0 · `off_label`: no label token at all (mass 0) · `failed`: the component call failed |
| `probs` | `tuple[float, ...] \| None` | six renormalised probabilities, **always `EMOTIONS` order**, sum 1; `None` unless `ok` |
| `label_mass` | `float \| None` | sum of raw label probabilities (0–1); `0.0` for `off_label`, `None` for `failed` |
| `label` | `str \| None` | argmax of `probs`; ties → first in `EMOTIONS` order (as the reference); `None` unless `ok` |
| `mass_partial` | `bool` | `True` if `coverage == "top-k"` (API): mass is a lower bound |
| `error` | `str \| None` | copied from `RawOutput` when `failed` |
| `seconds` | `float` | copied from `RawOutput` |
| `n_input_tokens` | `int` | copied from `RawOutput` |
| `cache_hit` | `bool = False` | set by the experiment cache later |
| `fingerprint` | `str \| None = None` | setup fingerprint, filled by the Model Interface in step 3 |

- `prob(emotion: str) -> float`: one column by name (what an XAI method reads for its target); raises if not `ok`.
- `__post_init__` validation: `ok` ⇒ 6 probs summing to 1 (tol 1e-9), label set; `off_label`/`failed` ⇒ `probs` and
  `label` are `None`; `failed` ⇒ `error` set.
- Raw label probabilities are NOT stored (= `probs × label_mass`, decision #1). API tokens/cost fields come with the
  online component.

## Spec: `standardize` (`prediction/standardize.py`, plain functions)
`standardize(raw: RawOutput, rule: LabelTokenRule) -> Prediction`
1. `raw.failed` → `Prediction(status="failed", error=raw.error, ...)`; no probabilities (never zeros or 1/6).
2. Sum probabilities per label over all tokens that `rule.match` assigns to it (same label from several tokens adds up:
   "anger" + "Ang" + "ANGER" → anger). Tokens matching no label are ignored (they are the off-label share).
3. `label_mass` = sum of the six raw label probabilities.
4. mass == 0 → `status="off_label"`, `label_mass=0.0`, no probs. (**Changed from the reference**, which returned
   uniform 1/6: a made-up score would flow into LIME looking real; decision #7.)
5. Otherwise renormalise (÷ mass), order as `EMOTIONS`, label = argmax (ties → first in `EMOTIONS`).
6. `mass_partial = raw.coverage == "top-k"`. Copy `seconds`, `n_input_tokens`.
- No judging: low mass (e.g. 0.3) is still `ok`; flagging is the analysis' job.
- `standardize_batch(raws, rule) -> list[Prediction]`: same order.
- Does not know about prompts, models, targets or callers.

## Tests (`tests/test_prediction.py`)
Hand-made `RawOutput`s unless stated.
1. Rule equals the reference: for a token list (`"anger"`, `" Ang"`, `"ANGER"`, `"ang"`, `"an"`, `"f"`, `"F"`, `"ear"`,
   `"Fear"`, `"sad"`, `"Sadness"`, `"dis"`, `"surpr"`, `"joy"`, `"Joy"`, `"neutral"`, `"Neutral"`, `"Rel"`,
   `"frustration"`, `"<off_label>"`, `""`, `"  "`), `LabelTokenRule(LLAMA31_FIRST_TOKENS).match(t)` ==
   `backends.match_label(t, first_tokens=LLAMA31_FIRST_TOKENS)` (passing the table means no tokenizer is loaded).
2. "f" counts for fear only with the Llama table; with an empty table it matches nothing.
3. Casings add up: `anger 0.6, Ang 0.3, ANGER 0.05` → raw anger 0.95.
4. **Neutral is never an emotion**: adding `neutral 0.2` / `Neutral 0.1` changes no emotion's raw probability and
   lowers `label_mass` accordingly; same for `"<off_label>"`.
5. Worked example from the design note §4: raw joy 0.60, sadness 0.20, anger 0.05, fear 0.03, surprise 0.01,
   disgust 0.01, other 0.10 → mass 0.90, joy 0.667, sum 1, label joy.
6. `probs` always in `EMOTIONS` order whatever order the tokens arrive in.
7. Tie → first in `EMOTIONS` order (e.g. anger 0.4, sadness 0.4 → anger).
8. Off-label: only non-label tokens → `status="off_label"`, mass 0.0, probs/label `None`, `prob()` raises.
9. Failed `RawOutput` → `status="failed"`, error copied, no probs, mass `None`.
10. `coverage="top-k"` → `mass_partial` True; `"complete"` → False.
11. Low mass stays `ok` (mass 0.05 → ok, renormalised).
12. `Prediction` validation rejects inconsistent records (ok without probs, failed without error, probs not summing to 1).
13. FakeModel end to end: `standardize_batch(FakeModel().score(prompts), LabelTokenRule())` →
    "I am so happy today": ok, label joy, mass ≈ 0.772, joy ≈ 0.80 renormalised (0.618 / 0.772); empty text: ok, six
    equal probs (1/6), mass ≈ 0.448; `fail_on` text → failed; order kept.
14. Optional, skipped if the tokenizer isn't available offline: `LLAMA31_FIRST_TOKENS == backends.label_first_tokens()`
    (`pytest.importorskip("transformers")`; load with `local_files_only=True`, skip on error).

## Done when
- All tests pass, old and new: from `master code/`, `C:\Users\vamshi\.venvs\eesys-thesis\Scripts\python -m pytest`
  (previously 40/40), including test 14 on the laptop where the tokenizer is cached.
- No torch/transformers import in `prediction/` (only in the optional test 14).
- Type hints + docstrings on public classes/functions.

## Rules while building
- If the derived first-token table differs from what the reference produces, or anything this plan doesn't cover comes
  up, stop and ask. Record decisions in `02_Decisions.md` right away.
- No model run, so no `meta.json`. At the end, propose a commit ("step 2: standardized prediction") and wait for OK.
- At wrap-up: log entry, update `01_Status.md`, mark this plan `Status: done`.
