# Prompt comparison (v1/v2/v3) + label-order test

Picks one prompt version and label order for Llama 3.1 8B Instruct on the validation set
`dev_large` (150 texts, 25 per emotion, contains `dev`). Compares versions with macro-F1,
label mass, confusion matrices, flip tables with exact McNemar, and a label-order rotation check
(O1–O6, see `orders.py`). Method and selection criteria: vault note "Prompt comparison and
label-order protocol" and `02_Decisions.md` (2026-11-21). Plan: `PLAN.md`.

Run from the `master code` root:

```
# quick test
python -m experiments.prompt_comparison.run --backend ollama --versions v1 v2 v3 --limit 5 --tag quicktest
# Ollama dry run (4-bit, learning only)
python -m experiments.prompt_comparison.run --backend ollama --versions v1 v2 v3 --tag dryrun
# bf16 run (slow, resumable: stop with Ctrl+C, rerun the same command to continue)
python -m experiments.prompt_comparison.run --backend hf --versions v1 v2 v3 --tag bf16
# label-order run on the chosen version
python -m experiments.prompt_comparison.run --backend hf --versions <winner> --orders O1 O2 O3 O4 O5 O6 --tag orders
# report
python -m experiments.prompt_comparison.analyze experiments/prompt_comparison/results/<name>.jsonl
```

Results go to `results/<date>_<backend>_<tag>.jsonl` (one row per call), `.meta.json` (sample,
prompt hashes, model, decoding, git commit, sessions) and `.report.md` (from `analyze`).
A rerun with the same backend and tag continues the newest matching file.
