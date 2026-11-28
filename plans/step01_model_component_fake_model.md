# Step 1: Model Component contract + FakeModel

Status: done (built 2026-11-24 evening, 13 new tests, 40/40 pass; commit 4666526)
Build order: step 1 of 5 (component → Standardized Prediction → Model Interface → token deletion → runner + metrics)

## Read first
- `CLAUDE.md` (parent folder), `thesis vault/00_Dashboard/01_Status.md`, `02_Decisions.md`
- Design: `thesis vault/Claude outputs/Model Interface (wrapper).md`, §5f (common interface across components)
- Relevant decisions: 2026-11-23 "Common interface across model components" (#7), 2026-11-24 "Folder structure" and
  "Capability flags: who declares, who checks"

## Goal
Write the contract every Model Component follows, and the first component: a `FakeModel` that behaves like an LLM
from the outside (prompt in, raw token probabilities out) but uses hand-written word rules, so the correct explanation
is known exactly. Nothing in this step knows about emotions as classes: the FakeModel only emits token strings.

## Scope
Create:
- `models/__init__.py` (exports `Capabilities`, `RawOutput`, `ModelComponent`, `FakeModel`)
- `models/base.py`
- `models/fake_model.py`
- `tests/test_fake_model.py`

Do NOT touch / build in this step: `prediction/`, `model_interface/`, `xai/`, runner, `LlamaHFModel`, `OllamaModel`,
online component, generation (self-explanation) or gradients. Do not import `experiments/prompt_comparison/backends.py`
(it loads the HF tokenizer; the FakeModel and its tests must run without torch/transformers).

## Spec: `models/base.py`

### `Capabilities` (frozen dataclass)
Four bools: `scores`, `gradients`, `generation`, `repeated_calls`. This is the component's **"has"**: what the model
can do, written once per component class. (Access levels are NOT here; they come in step 3 with the Model Interface.)
- `enabled() -> frozenset[str]`: names of the flags that are True (the runner will later check `needs <= allowed`).

### `RawOutput` (frozen dataclass)
What a component returns for ONE text. Same shape for every component (Llama, API, FakeModel).
- `token_probs: tuple[tuple[str, float], ...]`: (token string, probability), sorted by probability, highest first
- `coverage: Literal["complete", "top-k"]`: `complete` = every relevant token present (Llama, FakeModel); `top-k` = API
- `seconds: float`: time spent on this text
- `n_input_tokens: int`
- `error: str | None = None`
- property `failed -> bool` (`error is not None`)
- `__post_init__` validation: if `error` is set, `token_probs` must be empty (a failed call has no probabilities,
  never zeros or uniform values; decision #7). Probabilities must be in [0, 1]. Raise `ValueError` otherwise.

### `ModelComponent` (abstract base class)
- `capabilities: Capabilities` (class attribute or set in `__init__`)
- `model_id: str` (used later for the setup fingerprint)
- abstract `score(messages_batch: list[list[dict]]) -> list[RawOutput]`
  - input: a list of already-built chat prompts (each = the `[system, user]` messages from `prompts.build_messages`);
    the component never builds prompts, never sees sample ids, gold labels, prompt version or label order
  - output: one `RawOutput` per prompt, **same order**
  - a failure for one text returns a failed `RawOutput` for that text; the others still come back. Only programmer
    errors (e.g. a prompt with no user message) raise.
- Docstrings say: components return raw tokens only; turning tokens into emotions is Standardized Prediction (step 2).

## Spec: `models/fake_model.py`

`FakeModel(ModelComponent)`, `model_id = "fake-lexicon-v1"`, `coverage = "complete"`.

> Test-only. The FakeModel replaces Llama's *neural network* with a word list, so tests know the right
> explanation in advance. It never produces thesis results; real runs use `LlamaHFModel` / the online component,
> which have no lexicon. Two different word lists exist: the **lexicon** = words in the INPUT sentence that drive the
> fake decision ("happy"); the **label tokens** = the OUTPUT answer tokens ("joy"/"Joy", like Llama's "anger"/"Ang"),
> which Standardized Prediction maps to emotions for every component alike.

**Reading the input**: the sentence = `content` of the last message with role `"user"` (with prompt v3 the user message
is exactly the text). No user message → `ValueError`. The system message is ignored.

**Words**: `re.findall(r"[a-z']+", text.lower())`. `n_input_tokens` = number of words.

**Lexicon** (module constant `DEFAULT_LEXICON: dict[str, str]`, word → emotion, 3–5 words per emotion), e.g.
- anger: angry, furious, hate, mad
- disgust: disgusting, gross, nasty, sick
- fear: scared, afraid, terrified, nervous
- joy: happy, love, great, glad
- sadness: sad, miss, cry, lonely
- surprise: wow, shocked, unexpected, surprised
Every lexicon value must be one of `data.EMOTIONS` (assert at import / in `__init__`).

**Scores** (additive, so the right explanation is known exactly):
- logit(emotion) = `WORD_WEIGHT` (3.0) × number of words in the text that map to that emotion
- logit of one off-label token `OFF_LABEL_TOKEN = "<off_label>"` = `OFF_LABEL_LOGIT` (2.0), fixed
- softmax over the 7 logits (6 emotions + the off-label token)
- Effect: an empty text → off-label ≈ 0.55, the six emotions equal (label mass ≈ 0.45, like a real model with no
  evidence); "I am so happy today" → joy ≈ 0.62, mass ≈ 0.77. More evidence → higher mass.

> **No "neutral".** The thesis uses only the six emotions; GoEmotions' neutral class is dropped from the data and
> never appears as a label or a token. The off-label token is NOT an emotion class: it stands for "everything the
> model says that is not one of our six labels" (with Llama e.g. "Rel", "frustration", "neutral"), i.e. the share
> that `label_mass` leaves out. Without it the FakeModel's label mass would always be 1, and the low-mass /
> `off_label` handling in Standardized Prediction could never be tested. Its name is deliberately not a word, so it
> can't be mistaken for a class.

**Tokens** (so Standardized Prediction has realistic work in step 2):
- each emotion's probability is split over two casings: `"joy"` gets `CASE_SPLIT` (0.8), `"Joy"` gets 0.2
- `"<off_label>"` is emitted as one token
- → 13 (token, prob) pairs per text, summing to 1, sorted highest first; ties broken by token string (deterministic)
- These tokens are matched by part (a) of the existing label-token rule (≥ 3 chars, label starts with it); `"<off_label>"`
  matches no label. The FakeModel never emits the "f" fear split (that belongs to Llama; tested in step 2).

**Constructor**: `FakeModel(lexicon=DEFAULT_LEXICON, capabilities=None, fail_on=frozenset())`
- default capabilities: `scores=True, gradients=False, generation=False, repeated_calls=True`; overridable
- `fail_on`: exact texts that return a failed `RawOutput` (`error="FakeModel: forced failure"`, no probabilities),
  to test failure handling later
- `n_calls: int`: number of texts actually scored (incremented per text, failed ones included); later used to check
  requested vs. executed calls with the cache
- `seconds` measured with `time.perf_counter()` per text

Constants (`WORD_WEIGHT`, `OFF_LABEL_TOKEN`, `OFF_LABEL_LOGIT`, `CASE_SPLIT`) at module top with a one-line comment each.

## Tests: `tests/test_fake_model.py`
Build real prompts with `prompts.build_messages(text, "v3")`, so the FakeModel is tested with the frozen prompt format.
1. Deterministic: same batch twice → identical outputs.
2. Order kept: batch of 3 texts with different evidence words → output i belongs to text i.
3. Evidence: "I am so happy today" → joy+Joy is the largest emotion share; "I am so today" → lower joy share.
4. Casings: for each emotion both casings are present, ratio 0.8 / 0.2.
5. All 13 probabilities sum to 1 (abs tol 1e-9); sorted descending.
6. Empty string: no error; the six emotion shares are equal; label mass (sum of the 12 emotion tokens) is lower than
   for "I am so happy today".
7. `fail_on`: that text → `failed`, empty `token_probs`, error message; the other texts in the same batch are normal.
8. `RawOutput` validation: error + probabilities → `ValueError`; probability > 1 → `ValueError`.
9. Capabilities: defaults as above; custom capabilities passed in are kept; `enabled()` returns the right names.
10. `n_calls` counts scored texts across calls (e.g. 3 + 2 → 5).
11. `coverage == "complete"`, `n_input_tokens` == word count.
12. Only the user message counts: same text with a different system message → same output; no user message →
    `ValueError`.
13. Lexicon values are all in `EMOTIONS`.

## Done when
- All tests pass, old and new: from `master code/`,
  `C:\Users\vamshi\.venvs\eesys-thesis\Scripts\python -m pytest`
- No torch/transformers import anywhere in `models/base.py`, `models/fake_model.py` or the new test.
- Type hints and docstrings on public classes/functions (CLAUDE.md coding conventions).

## Rules while building
- If something needs a choice this plan doesn't cover (e.g. a field name clash, a better shape for `RawOutput`),
  stop and ask; if decided, write it to `02_Decisions.md` right away.
- No model run in this step, so no `meta.json`. At the end, propose a commit (e.g. "step 1: model component contract
  + FakeModel") and wait for OK.
- At wrap-up: log entry (files touched, test count), update `01_Status.md`, mark this plan `Status: done`.
