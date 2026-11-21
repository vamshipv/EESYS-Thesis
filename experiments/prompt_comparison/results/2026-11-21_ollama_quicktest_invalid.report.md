> **INVALID (2026-11-21): scored with the old >=3-char token rule, which drops 'f', the tokenizer's first token of lowercase 'fear'; fear could not be scored under v2/v3. Kept for the record; see 02_Decisions.**

# Prompt comparison report: 2026-11-21_ollama_quicktest

- Backend: ollama, model: ollama:llama3.1:latest
- Sample: dev_large (limit 5)
- Rows: 15; versions: v1, v2, v3; orders: O1
- Prompt hashes: {'v1': 'd9250dd0ca98', 'v2': 'aa283b52fffd', 'v3': 'bcf65961ce96'}; git: 23d401c-dirty
- label_mass = probability on label tokens before renormalising (Ollama: top-20 logprobs only, so a lower bound).

## Headline

| version | order | n | acc | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp | worst class | mean mass | mass<0.9 | mass<0.5 | mean s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | O1 | 5 | 40.0% | 0.095 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | disgust (0.00) | 0.653 | 40.0% | 40.0% | 2.34 |
| v2 | O1 | 5 | 40.0% | 0.095 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | disgust (0.00) | 0.634 | 40.0% | 40.0% | 0.34 |
| v3 | O1 | 5 | 40.0% | 0.095 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | disgust (0.00) | 0.949 | 20.0% | 0.0% | 0.31 |

## Confusion matrices

### v1 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 2 | 2 | 0 | 0 | 0 | 1 |
| disgust | 0 | 0 | 0 | 0 | 0 | 0 |
| fear | 0 | 0 | 0 | 0 | 0 | 0 |
| joy | 0 | 0 | 0 | 0 | 0 | 0 |
| sadness | 0 | 0 | 0 | 0 | 0 | 0 |
| surprise | 0 | 0 | 0 | 0 | 0 | 0 |
| **pred total** | 2 | 2 | 0 | 0 | 0 | 1 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 40.0% | 40.0% | 0.0% | 0.0% | 0.0% | 20.0% |
| disgust | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| fear | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| joy | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| sadness | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| surprise | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### v2 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 2 | 1 | 0 | 0 | 2 | 0 |
| disgust | 0 | 0 | 0 | 0 | 0 | 0 |
| fear | 0 | 0 | 0 | 0 | 0 | 0 |
| joy | 0 | 0 | 0 | 0 | 0 | 0 |
| sadness | 0 | 0 | 0 | 0 | 0 | 0 |
| surprise | 0 | 0 | 0 | 0 | 0 | 0 |
| **pred total** | 2 | 1 | 0 | 0 | 2 | 0 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 40.0% | 20.0% | 0.0% | 0.0% | 40.0% | 0.0% |
| disgust | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| fear | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| joy | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| sadness | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| surprise | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### v3 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 2 | 1 | 0 | 0 | 1 | 1 |
| disgust | 0 | 0 | 0 | 0 | 0 | 0 |
| fear | 0 | 0 | 0 | 0 | 0 | 0 |
| joy | 0 | 0 | 0 | 0 | 0 | 0 |
| sadness | 0 | 0 | 0 | 0 | 0 | 0 |
| surprise | 0 | 0 | 0 | 0 | 0 | 0 |
| **pred total** | 2 | 1 | 0 | 0 | 1 | 1 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 40.0% | 20.0% | 0.0% | 0.0% | 20.0% | 20.0% |
| disgust | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| fear | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| joy | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| sadness | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| surprise | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Flip tables (same order)

### v1 vs v2 (O1)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 1 | 2 | 60.0% | 1.000 |

Texts where the prediction changed (2):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | sadness |

### v1 vs v3 (O1)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 2 | 1 | 80.0% | 1.000 |

Texts where the prediction changed (1):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |

### v2 vs v3 (O1)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 2 | 1 | 80.0% | 1.000 |

Texts where the prediction changed (1):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | sadness | surprise |
