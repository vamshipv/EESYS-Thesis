# Prompt comparison report: 2026-11-22_ollama_orders

- Backend: ollama, model: ollama:llama3.1:latest
- Sample: dev_large
- Rows: 2700; versions: v1, v2, v3; orders: O1, O2, O3, O4, O5, O6
- Prompt hashes: {'v1': 'd9250dd0ca98', 'v2': 'aa283b52fffd', 'v3': 'bcf65961ce96'}; git: 23d401c-dirty
- label_mass = probability on label tokens before renormalising (Ollama: top-20 logprobs only, so a lower bound).

## Headline

| version | order | n | acc | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp | worst class | mean mass | mass<0.9 | mass<0.5 | mean s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | O1 | 150 | 66.7% | 0.663 | 0.72 | 0.60 | 0.57 | 0.78 | 0.72 | 0.59 | fear (0.57) | 0.896 | 19.3% | 8.0% | 0.36 |
| v1 | O2 | 150 | 65.3% | 0.649 | 0.64 | 0.62 | 0.53 | 0.77 | 0.80 | 0.54 | fear (0.53) | 0.888 | 24.0% | 8.0% | 0.38 |
| v1 | O3 | 150 | 70.7% | 0.710 | 0.71 | 0.59 | 0.65 | 0.81 | 0.83 | 0.67 | disgust (0.59) | 0.880 | 25.3% | 10.7% | 0.36 |
| v1 | O4 | 150 | 72.0% | 0.725 | 0.74 | 0.62 | 0.68 | 0.80 | 0.85 | 0.65 | disgust (0.62) | 0.868 | 29.3% | 10.0% | 0.37 |
| v1 | O5 | 150 | 70.7% | 0.716 | 0.71 | 0.58 | 0.68 | 0.82 | 0.84 | 0.67 | disgust (0.58) | 0.873 | 26.7% | 8.7% | 0.36 |
| v1 | O6 | 150 | 67.3% | 0.672 | 0.72 | 0.58 | 0.57 | 0.81 | 0.71 | 0.64 | fear (0.57) | 0.881 | 24.0% | 8.7% | 0.36 |
| v2 | O1 | 150 | 65.3% | 0.656 | 0.63 | 0.65 | 0.61 | 0.79 | 0.65 | 0.60 | surprise (0.60) | 0.887 | 19.3% | 9.3% | 0.36 |
| v2 | O2 | 150 | 64.7% | 0.654 | 0.56 | 0.59 | 0.61 | 0.76 | 0.81 | 0.59 | anger (0.56) | 0.880 | 23.3% | 9.3% | 0.41 |
| v2 | O3 | 150 | 69.3% | 0.697 | 0.62 | 0.67 | 0.65 | 0.79 | 0.83 | 0.62 | anger (0.62) | 0.877 | 21.3% | 10.0% | 0.37 |
| v2 | O4 | 150 | 70.7% | 0.716 | 0.61 | 0.68 | 0.72 | 0.76 | 0.84 | 0.68 | anger (0.61) | 0.872 | 22.0% | 10.0% | 0.35 |
| v2 | O5 | 150 | 68.7% | 0.691 | 0.61 | 0.68 | 0.68 | 0.80 | 0.76 | 0.61 | anger (0.61) | 0.875 | 22.7% | 10.0% | 0.35 |
| v2 | O6 | 150 | 68.7% | 0.690 | 0.64 | 0.70 | 0.65 | 0.82 | 0.70 | 0.64 | anger (0.64) | 0.881 | 22.0% | 10.0% | 0.35 |
| v3 | O1 | 150 | 70.0% | 0.704 | 0.60 | 0.65 | 0.75 | 0.80 | 0.76 | 0.67 | anger (0.60) | 0.979 | 4.7% | 0.7% | 0.34 |
| v3 | O2 | 150 | 71.3% | 0.719 | 0.60 | 0.69 | 0.78 | 0.79 | 0.81 | 0.64 | anger (0.60) | 0.974 | 6.7% | 1.3% | 0.33 |
| v3 | O3 | 150 | 72.0% | 0.726 | 0.61 | 0.65 | 0.78 | 0.79 | 0.81 | 0.71 | anger (0.61) | 0.972 | 8.0% | 1.3% | 0.35 |
| v3 | O4 | 150 | 72.7% | 0.733 | 0.60 | 0.68 | 0.78 | 0.79 | 0.83 | 0.72 | anger (0.60) | 0.975 | 6.7% | 0.7% | 0.34 |
| v3 | O5 | 150 | 72.7% | 0.727 | 0.60 | 0.67 | 0.68 | 0.86 | 0.80 | 0.76 | anger (0.60) | 0.975 | 6.0% | 0.0% | 0.33 |
| v3 | O6 | 150 | 70.7% | 0.712 | 0.60 | 0.65 | 0.75 | 0.82 | 0.73 | 0.72 | anger (0.60) | 0.977 | 4.7% | 0.0% | 0.34 |

## Confusion matrices

### v1 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 3 | 0 | 0 | 3 | 1 |
| disgust | 2 | 17 | 0 | 0 | 5 | 1 |
| fear | 3 | 6 | 10 | 0 | 2 | 4 |
| joy | 0 | 1 | 0 | 18 | 2 | 4 |
| sadness | 0 | 1 | 0 | 1 | 22 | 1 |
| surprise | 2 | 4 | 0 | 2 | 2 | 15 |
| **pred total** | 25 | 32 | 10 | 21 | 36 | 26 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 12.0% | 0.0% | 0.0% | 12.0% | 4.0% |
| disgust | 8.0% | 68.0% | 0.0% | 0.0% | 20.0% | 4.0% |
| fear | 12.0% | 24.0% | 40.0% | 0.0% | 8.0% | 16.0% |
| joy | 0.0% | 4.0% | 0.0% | 72.0% | 8.0% | 16.0% |
| sadness | 0.0% | 4.0% | 0.0% | 4.0% | 88.0% | 4.0% |
| surprise | 8.0% | 16.0% | 0.0% | 8.0% | 8.0% | 60.0% |

### v1 / O2

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 21 | 2 | 0 | 0 | 1 | 1 |
| disgust | 6 | 17 | 0 | 0 | 1 | 1 |
| fear | 7 | 5 | 9 | 0 | 0 | 4 |
| joy | 1 | 2 | 0 | 18 | 1 | 3 |
| sadness | 1 | 2 | 0 | 1 | 20 | 1 |
| surprise | 5 | 2 | 0 | 3 | 2 | 13 |
| **pred total** | 41 | 30 | 9 | 22 | 25 | 23 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 84.0% | 8.0% | 0.0% | 0.0% | 4.0% | 4.0% |
| disgust | 24.0% | 68.0% | 0.0% | 0.0% | 4.0% | 4.0% |
| fear | 28.0% | 20.0% | 36.0% | 0.0% | 0.0% | 16.0% |
| joy | 4.0% | 8.0% | 0.0% | 72.0% | 4.0% | 12.0% |
| sadness | 4.0% | 8.0% | 0.0% | 4.0% | 80.0% | 4.0% |
| surprise | 20.0% | 8.0% | 0.0% | 12.0% | 8.0% | 52.0% |

### v1 / O3

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 21 | 3 | 0 | 0 | 1 | 0 |
| disgust | 4 | 19 | 0 | 0 | 1 | 1 |
| fear | 5 | 6 | 12 | 0 | 1 | 1 |
| joy | 1 | 3 | 0 | 19 | 0 | 2 |
| sadness | 1 | 2 | 0 | 1 | 20 | 1 |
| surprise | 2 | 6 | 0 | 2 | 0 | 15 |
| **pred total** | 34 | 39 | 12 | 22 | 23 | 20 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 84.0% | 12.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| disgust | 16.0% | 76.0% | 0.0% | 0.0% | 4.0% | 4.0% |
| fear | 20.0% | 24.0% | 48.0% | 0.0% | 4.0% | 4.0% |
| joy | 4.0% | 12.0% | 0.0% | 76.0% | 0.0% | 8.0% |
| sadness | 4.0% | 8.0% | 0.0% | 4.0% | 80.0% | 4.0% |
| surprise | 8.0% | 24.0% | 0.0% | 8.0% | 0.0% | 60.0% |

### v1 / O4

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 21 | 3 | 0 | 0 | 1 | 0 |
| disgust | 3 | 20 | 0 | 0 | 1 | 1 |
| fear | 4 | 6 | 13 | 0 | 0 | 2 |
| joy | 0 | 3 | 0 | 18 | 0 | 4 |
| sadness | 1 | 2 | 0 | 1 | 20 | 1 |
| surprise | 3 | 5 | 0 | 1 | 0 | 16 |
| **pred total** | 32 | 39 | 13 | 20 | 22 | 24 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 84.0% | 12.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| disgust | 12.0% | 80.0% | 0.0% | 0.0% | 4.0% | 4.0% |
| fear | 16.0% | 24.0% | 52.0% | 0.0% | 0.0% | 8.0% |
| joy | 0.0% | 12.0% | 0.0% | 72.0% | 0.0% | 16.0% |
| sadness | 4.0% | 8.0% | 0.0% | 4.0% | 80.0% | 4.0% |
| surprise | 12.0% | 20.0% | 0.0% | 4.0% | 0.0% | 64.0% |

### v1 / O5

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 5 | 0 | 0 | 1 | 1 |
| disgust | 3 | 20 | 0 | 1 | 0 | 1 |
| fear | 3 | 7 | 13 | 0 | 0 | 2 |
| joy | 0 | 3 | 0 | 20 | 0 | 2 |
| sadness | 0 | 4 | 0 | 1 | 19 | 1 |
| surprise | 2 | 5 | 0 | 2 | 0 | 16 |
| **pred total** | 26 | 44 | 13 | 24 | 20 | 23 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 20.0% | 0.0% | 0.0% | 4.0% | 4.0% |
| disgust | 12.0% | 80.0% | 0.0% | 4.0% | 0.0% | 4.0% |
| fear | 12.0% | 28.0% | 52.0% | 0.0% | 0.0% | 8.0% |
| joy | 0.0% | 12.0% | 0.0% | 80.0% | 0.0% | 8.0% |
| sadness | 0.0% | 16.0% | 0.0% | 4.0% | 76.0% | 4.0% |
| surprise | 8.0% | 20.0% | 0.0% | 8.0% | 0.0% | 64.0% |

### v1 / O6

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 4 | 0 | 0 | 3 | 0 |
| disgust | 2 | 19 | 0 | 0 | 3 | 1 |
| fear | 3 | 7 | 10 | 0 | 3 | 2 |
| joy | 0 | 3 | 0 | 19 | 2 | 1 |
| sadness | 0 | 2 | 0 | 1 | 21 | 1 |
| surprise | 2 | 5 | 0 | 2 | 2 | 14 |
| **pred total** | 25 | 40 | 10 | 22 | 34 | 19 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 16.0% | 0.0% | 0.0% | 12.0% | 0.0% |
| disgust | 8.0% | 76.0% | 0.0% | 0.0% | 12.0% | 4.0% |
| fear | 12.0% | 28.0% | 40.0% | 0.0% | 12.0% | 8.0% |
| joy | 0.0% | 12.0% | 0.0% | 76.0% | 8.0% | 4.0% |
| sadness | 0.0% | 8.0% | 0.0% | 4.0% | 84.0% | 4.0% |
| surprise | 8.0% | 20.0% | 0.0% | 8.0% | 8.0% | 56.0% |

### v2 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 19 | 1 | 0 | 0 | 5 | 0 |
| disgust | 3 | 14 | 0 | 0 | 7 | 1 |
| fear | 7 | 2 | 11 | 0 | 2 | 3 |
| joy | 0 | 0 | 0 | 17 | 3 | 5 |
| sadness | 2 | 0 | 0 | 0 | 22 | 1 |
| surprise | 4 | 1 | 0 | 1 | 4 | 15 |
| **pred total** | 35 | 18 | 11 | 18 | 43 | 25 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 76.0% | 4.0% | 0.0% | 0.0% | 20.0% | 0.0% |
| disgust | 12.0% | 56.0% | 0.0% | 0.0% | 28.0% | 4.0% |
| fear | 28.0% | 8.0% | 44.0% | 0.0% | 8.0% | 12.0% |
| joy | 0.0% | 0.0% | 0.0% | 68.0% | 12.0% | 20.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 16.0% | 4.0% | 0.0% | 4.0% | 16.0% | 60.0% |

### v2 / O2

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 23 | 1 | 0 | 0 | 1 | 0 |
| disgust | 11 | 13 | 0 | 0 | 1 | 0 |
| fear | 8 | 2 | 11 | 0 | 1 | 3 |
| joy | 4 | 2 | 0 | 16 | 1 | 2 |
| sadness | 2 | 1 | 0 | 0 | 21 | 1 |
| surprise | 9 | 0 | 0 | 1 | 2 | 13 |
| **pred total** | 57 | 19 | 11 | 17 | 27 | 19 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 92.0% | 4.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| disgust | 44.0% | 52.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| fear | 32.0% | 8.0% | 44.0% | 0.0% | 4.0% | 12.0% |
| joy | 16.0% | 8.0% | 0.0% | 64.0% | 4.0% | 8.0% |
| sadness | 8.0% | 4.0% | 0.0% | 0.0% | 84.0% | 4.0% |
| surprise | 36.0% | 0.0% | 0.0% | 4.0% | 8.0% | 52.0% |

### v2 / O3

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 23 | 1 | 0 | 0 | 1 | 0 |
| disgust | 7 | 15 | 0 | 0 | 2 | 1 |
| fear | 7 | 2 | 12 | 0 | 1 | 3 |
| joy | 3 | 1 | 0 | 17 | 1 | 3 |
| sadness | 2 | 0 | 0 | 0 | 22 | 1 |
| surprise | 7 | 1 | 0 | 1 | 1 | 15 |
| **pred total** | 49 | 20 | 12 | 18 | 28 | 23 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 92.0% | 4.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| disgust | 28.0% | 60.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 28.0% | 8.0% | 48.0% | 0.0% | 4.0% | 12.0% |
| joy | 12.0% | 4.0% | 0.0% | 68.0% | 4.0% | 12.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 28.0% | 4.0% | 0.0% | 4.0% | 4.0% | 60.0% |

### v2 / O4

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 23 | 1 | 0 | 0 | 1 | 0 |
| disgust | 7 | 15 | 0 | 0 | 2 | 1 |
| fear | 7 | 2 | 14 | 0 | 0 | 2 |
| joy | 4 | 0 | 0 | 16 | 1 | 4 |
| sadness | 2 | 1 | 0 | 0 | 21 | 1 |
| surprise | 7 | 0 | 0 | 1 | 0 | 17 |
| **pred total** | 50 | 19 | 14 | 17 | 25 | 25 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 92.0% | 4.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| disgust | 28.0% | 60.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 28.0% | 8.0% | 56.0% | 0.0% | 0.0% | 8.0% |
| joy | 16.0% | 0.0% | 0.0% | 64.0% | 4.0% | 16.0% |
| sadness | 8.0% | 4.0% | 0.0% | 0.0% | 84.0% | 4.0% |
| surprise | 28.0% | 0.0% | 0.0% | 4.0% | 0.0% | 68.0% |

### v2 / O5

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 21 | 1 | 0 | 0 | 3 | 0 |
| disgust | 6 | 16 | 0 | 0 | 2 | 1 |
| fear | 7 | 2 | 13 | 0 | 0 | 3 |
| joy | 2 | 1 | 0 | 18 | 2 | 2 |
| sadness | 2 | 1 | 0 | 0 | 21 | 1 |
| surprise | 6 | 1 | 0 | 2 | 2 | 14 |
| **pred total** | 44 | 22 | 13 | 20 | 30 | 21 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 84.0% | 4.0% | 0.0% | 0.0% | 12.0% | 0.0% |
| disgust | 24.0% | 64.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 28.0% | 8.0% | 52.0% | 0.0% | 0.0% | 12.0% |
| joy | 8.0% | 4.0% | 0.0% | 72.0% | 8.0% | 8.0% |
| sadness | 8.0% | 4.0% | 0.0% | 0.0% | 84.0% | 4.0% |
| surprise | 24.0% | 4.0% | 0.0% | 8.0% | 8.0% | 56.0% |

### v2 / O6

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 21 | 1 | 0 | 0 | 3 | 0 |
| disgust | 5 | 15 | 0 | 0 | 4 | 1 |
| fear | 7 | 2 | 12 | 0 | 2 | 2 |
| joy | 0 | 0 | 0 | 18 | 3 | 4 |
| sadness | 2 | 0 | 0 | 0 | 21 | 2 |
| surprise | 6 | 0 | 0 | 1 | 2 | 16 |
| **pred total** | 41 | 18 | 12 | 19 | 35 | 25 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 84.0% | 4.0% | 0.0% | 0.0% | 12.0% | 0.0% |
| disgust | 20.0% | 60.0% | 0.0% | 0.0% | 16.0% | 4.0% |
| fear | 28.0% | 8.0% | 48.0% | 0.0% | 8.0% | 8.0% |
| joy | 0.0% | 0.0% | 0.0% | 72.0% | 12.0% | 16.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 84.0% | 8.0% |
| surprise | 24.0% | 0.0% | 0.0% | 4.0% | 8.0% | 64.0% |

### v3 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 17 | 2 | 0 | 0 | 4 | 2 |
| disgust | 4 | 16 | 0 | 0 | 4 | 1 |
| fear | 5 | 3 | 15 | 0 | 0 | 2 |
| joy | 1 | 1 | 0 | 18 | 2 | 3 |
| sadness | 2 | 0 | 0 | 0 | 22 | 1 |
| surprise | 3 | 2 | 0 | 2 | 1 | 17 |
| **pred total** | 32 | 24 | 15 | 20 | 33 | 26 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 68.0% | 8.0% | 0.0% | 0.0% | 16.0% | 8.0% |
| disgust | 16.0% | 64.0% | 0.0% | 0.0% | 16.0% | 4.0% |
| fear | 20.0% | 12.0% | 60.0% | 0.0% | 0.0% | 8.0% |
| joy | 4.0% | 4.0% | 0.0% | 72.0% | 8.0% | 12.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 12.0% | 8.0% | 0.0% | 8.0% | 4.0% | 68.0% |

### v3 / O2

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 3 | 0 | 0 | 3 | 1 |
| disgust | 4 | 20 | 0 | 0 | 1 | 0 |
| fear | 5 | 3 | 16 | 0 | 0 | 1 |
| joy | 2 | 2 | 0 | 17 | 2 | 2 |
| sadness | 1 | 1 | 0 | 0 | 22 | 1 |
| surprise | 5 | 4 | 0 | 1 | 1 | 14 |
| **pred total** | 35 | 33 | 16 | 18 | 29 | 19 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 12.0% | 0.0% | 0.0% | 12.0% | 4.0% |
| disgust | 16.0% | 80.0% | 0.0% | 0.0% | 4.0% | 0.0% |
| fear | 20.0% | 12.0% | 64.0% | 0.0% | 0.0% | 4.0% |
| joy | 8.0% | 8.0% | 0.0% | 68.0% | 8.0% | 8.0% |
| sadness | 4.0% | 4.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 20.0% | 16.0% | 0.0% | 4.0% | 4.0% | 56.0% |

### v3 / O3

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 3 | 0 | 0 | 2 | 2 |
| disgust | 5 | 17 | 0 | 0 | 2 | 1 |
| fear | 5 | 3 | 16 | 0 | 0 | 1 |
| joy | 2 | 1 | 0 | 17 | 2 | 3 |
| sadness | 1 | 1 | 0 | 0 | 22 | 1 |
| surprise | 3 | 2 | 0 | 1 | 1 | 18 |
| **pred total** | 34 | 27 | 16 | 18 | 29 | 26 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 12.0% | 0.0% | 0.0% | 8.0% | 8.0% |
| disgust | 20.0% | 68.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 20.0% | 12.0% | 64.0% | 0.0% | 0.0% | 4.0% |
| joy | 8.0% | 4.0% | 0.0% | 68.0% | 8.0% | 12.0% |
| sadness | 4.0% | 4.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 12.0% | 8.0% | 0.0% | 4.0% | 4.0% | 72.0% |

### v3 / O4

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 18 | 3 | 0 | 0 | 2 | 2 |
| disgust | 5 | 17 | 0 | 0 | 2 | 1 |
| fear | 5 | 3 | 16 | 0 | 0 | 1 |
| joy | 2 | 1 | 0 | 17 | 1 | 4 |
| sadness | 1 | 1 | 0 | 0 | 22 | 1 |
| surprise | 4 | 0 | 0 | 1 | 1 | 19 |
| **pred total** | 35 | 25 | 16 | 18 | 28 | 28 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 72.0% | 12.0% | 0.0% | 0.0% | 8.0% | 8.0% |
| disgust | 20.0% | 68.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 20.0% | 12.0% | 64.0% | 0.0% | 0.0% | 4.0% |
| joy | 8.0% | 4.0% | 0.0% | 68.0% | 4.0% | 16.0% |
| sadness | 4.0% | 4.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 16.0% | 0.0% | 0.0% | 4.0% | 4.0% | 76.0% |

### v3 / O5

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 17 | 3 | 0 | 0 | 3 | 2 |
| disgust | 5 | 17 | 0 | 0 | 2 | 1 |
| fear | 5 | 4 | 13 | 1 | 1 | 1 |
| joy | 1 | 1 | 0 | 21 | 1 | 1 |
| sadness | 1 | 1 | 0 | 0 | 22 | 1 |
| surprise | 3 | 0 | 0 | 2 | 1 | 19 |
| **pred total** | 32 | 26 | 13 | 24 | 30 | 25 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 68.0% | 12.0% | 0.0% | 0.0% | 12.0% | 8.0% |
| disgust | 20.0% | 68.0% | 0.0% | 0.0% | 8.0% | 4.0% |
| fear | 20.0% | 16.0% | 52.0% | 4.0% | 4.0% | 4.0% |
| joy | 4.0% | 4.0% | 0.0% | 84.0% | 4.0% | 4.0% |
| sadness | 4.0% | 4.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 12.0% | 0.0% | 0.0% | 8.0% | 4.0% | 76.0% |

### v3 / O6

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 17 | 2 | 0 | 0 | 4 | 2 |
| disgust | 4 | 16 | 0 | 0 | 4 | 1 |
| fear | 5 | 4 | 15 | 0 | 0 | 1 |
| joy | 1 | 1 | 0 | 18 | 3 | 2 |
| sadness | 1 | 1 | 0 | 0 | 22 | 1 |
| surprise | 4 | 0 | 0 | 1 | 2 | 18 |
| **pred total** | 32 | 24 | 15 | 19 | 35 | 25 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 68.0% | 8.0% | 0.0% | 0.0% | 16.0% | 8.0% |
| disgust | 16.0% | 64.0% | 0.0% | 0.0% | 16.0% | 4.0% |
| fear | 20.0% | 16.0% | 60.0% | 0.0% | 0.0% | 4.0% |
| joy | 4.0% | 4.0% | 0.0% | 72.0% | 12.0% | 8.0% |
| sadness | 4.0% | 4.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 16.0% | 0.0% | 0.0% | 4.0% | 8.0% | 72.0% |

## Flip tables (same order)

### v1 vs v2 (O1)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 93 | 7 | 5 | 35 | 10 | 85.3% | 0.774 |

Texts where the prediction changed (22):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | sadness |
| eeerg5v | Look at that shit-eating grin | anger | disgust | anger ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | sadness |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | disgust ✓ | sadness |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | anger |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | fear ✓ |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | disgust | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | surprise |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness ✓ | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | sadness |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | surprise ✓ | anger |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | surprise ✓ |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v1 vs v3 (O1)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 95 | 5 | 10 | 34 | 6 | 86.0% | 0.302 |

Texts where the prediction changed (21):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | fear ✓ |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | fear ✓ |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | fear ✓ |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness ✓ | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O1)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 95 | 3 | 10 | 33 | 9 | 85.3% | 0.092 |

Texts where the prediction changed (22):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | sadness | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | sadness | anger |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | sadness | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | fear ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | sadness | disgust |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | surprise | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | joy ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | sadness | disgust |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | surprise ✓ |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | surprise ✓ | joy |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | anger | disgust |

### v1 vs v2 (O2)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 90 | 8 | 7 | 36 | 9 | 84.0% | 1.000 |

Texts where the prediction changed (24):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | anger ✓ |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | anger ✓ |
| ed85eg7 | That explains an awful lot about ICP. | disgust | surprise | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | anger |
| efapqfy | that's like a kel'thuzad/kael'thas wet dream right there. Line them up for disgusting aoe XD | disgust | disgust ✓ | anger |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | disgust ✓ | anger |
| edcxlpz | There was a horrible accident | fear | fear ✓ | sadness |
| ee1u7av | It’s gonna be a large group interview in a shady office. Ghost em. | fear | disgust | fear ✓ |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | anger | fear ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | fear ✓ |
| edx3px0 | I get scared just reading your flair | fear | disgust | anger |
| ef3nupt | AMD this is why we rejoice in his banning.... :) | joy | joy ✓ | anger |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | anger |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | anger |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | anger |
| eecahse | Oh wow I genuinely thought this was funny can’t believe you copped it so hard | surprise | joy | surprise ✓ |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | anger |

### v1 vs v3 (O2)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 89 | 9 | 18 | 28 | 6 | 78.0% | 0.122 |

Texts where the prediction changed (33):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | disgust |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| ed85eg7 | That explains an awful lot about ICP. | disgust | surprise | disgust ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | anger | disgust ✓ |
| effw6qi | Disgusting. Need to get the tooth hole fixed😂 | disgust | anger | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| ee1u7av | It’s gonna be a large group interview in a shady office. Ghost em. | fear | disgust | fear ✓ |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | anger | fear ✓ |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | fear ✓ |
| edx3px0 | I get scared just reading your flair | fear | disgust | fear ✓ |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | surprise ✓ |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | surprise ✓ | disgust |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | anger |
| eewbfj5 | Oh my gosh she opens her gullet like a freaking pelican!!! | surprise | surprise ✓ | disgust |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eecahse | Oh wow I genuinely thought this was funny can’t believe you copped it so hard | surprise | joy | surprise ✓ |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | anger | disgust |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O2)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 89 | 8 | 18 | 31 | 4 | 80.0% | 0.076 |

Texts where the prediction changed (30):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | anger ✓ | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | anger ✓ | disgust |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| ed85eg7 | That explains an awful lot about ICP. | disgust | anger | disgust ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | anger | disgust ✓ |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | anger | disgust ✓ |
| effw6qi | Disgusting. Need to get the tooth hole fixed😂 | disgust | anger | disgust ✓ |
| efapqfy | that's like a kel'thuzad/kael'thas wet dream right there. Line them up for disgusting aoe XD | disgust | anger | disgust ✓ |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | anger | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| edx3px0 | I get scared just reading your flair | fear | anger | fear ✓ |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| ef3nupt | AMD this is why we rejoice in his banning.... :) | joy | anger | joy ✓ |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | anger | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | anger | disgust |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | anger | surprise ✓ |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | surprise ✓ | disgust |
| eewbfj5 | Oh my gosh she opens her gullet like a freaking pelican!!! | surprise | surprise ✓ | disgust |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | anger | disgust |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | anger | surprise ✓ |

### v1 vs v2 (O3)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 99 | 7 | 5 | 27 | 12 | 84.0% | 0.774 |

Texts where the prediction changed (24):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | anger ✓ |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | anger ✓ |
| eetucfv | The humidity in Sydney is worse. | disgust | disgust ✓ | anger |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | disgust | surprise |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | surprise |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | disgust | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | anger |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | anger |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | disgust | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | anger |

### v1 vs v3 (O3)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 97 | 9 | 11 | 26 | 7 | 82.0% | 0.824 |

Texts where the prediction changed (27):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | disgust | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | surprise |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | joy ✓ | sadness |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | disgust | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | disgust | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O3)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 98 | 6 | 10 | 33 | 3 | 87.3% | 0.454 |

Texts where the prediction changed (19):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | anger ✓ | disgust |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | anger ✓ | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| eetucfv | The humidity in Sydney is worse. | disgust | anger | disgust ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | anger | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | anger | surprise ✓ |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | anger | disgust |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | anger | surprise ✓ |

### v1 vs v2 (O4)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 100 | 8 | 6 | 23 | 13 | 82.0% | 0.791 |

Texts where the prediction changed (27):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | anger ✓ |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | anger ✓ |
| eetucfv | The humidity in Sydney is worse. | disgust | disgust ✓ | anger |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | surprise |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | surprise | sadness |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | disgust | anger |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | disgust | anger |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| eepdkxb | Cheers, I live minutes away from you, will check it out some time soon. | joy | joy ✓ | surprise |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | surprise ✓ | anger |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | disgust | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | anger |

### v1 vs v3 (O4)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 99 | 9 | 10 | 24 | 8 | 82.0% | 1.000 |

Texts where the prediction changed (27):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | fear ✓ |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | fear ✓ |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | joy ✓ |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | disgust | anger |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | surprise ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | disgust | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O4)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 99 | 7 | 10 | 29 | 5 | 85.3% | 0.629 |

Texts where the prediction changed (22):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | anger ✓ | disgust |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | anger ✓ | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| eetucfv | The humidity in Sydney is worse. | disgust | anger | disgust ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | fear ✓ |
| edrc8re | Scary. I bet youre fun at parties. | fear | surprise | fear ✓ |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | sadness | surprise |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | joy ✓ |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | anger | disgust |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| eepdkxb | Cheers, I live minutes away from you, will check it out some time soon. | joy | surprise | joy ✓ |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | anger | surprise |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | anger | surprise ✓ |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | anger | surprise ✓ |

### v1 vs v2 (O5)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 97 | 9 | 6 | 23 | 15 | 80.0% | 0.607 |

Texts where the prediction changed (30):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | anger ✓ |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | sadness |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | surprise | anger ✓ |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | disgust | anger ✓ |
| eeerg5v | Look at that shit-eating grin | anger | disgust | anger ✓ |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| eetoykw | It feels oddly comforting and familiar that we suck at hockey again. | disgust | joy | sadness |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | anger |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | surprise |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | joy ✓ | sadness |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | disgust | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | sadness |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | joy ✓ | anger |
| edhj78h | Had such a hard time cutting up the steak | sadness | disgust | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| ed7yj4s | It must be really sad and lonely under your bridge troll. | sadness | disgust | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | anger |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | surprise ✓ | sadness |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | anger |

### v1 vs v3 (O5)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 98 | 8 | 11 | 24 | 9 | 81.3% | 0.648 |

Texts where the prediction changed (28):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | surprise |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | disgust | sadness |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | anger ✓ | sadness |
| eetoykw | It feels oddly comforting and familiar that we suck at hockey again. | disgust | joy | sadness |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | fear ✓ | sadness |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | fear ✓ | joy |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | surprise |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | joy ✓ |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | disgust | joy ✓ |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | sadness |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| ed7yj4s | It must be really sad and lonely under your bridge troll. | sadness | disgust | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | surprise ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | surprise ✓ |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O5)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 96 | 7 | 13 | 30 | 4 | 84.0% | 0.263 |

Texts where the prediction changed (24):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | anger ✓ | disgust |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | sadness | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | anger ✓ | sadness |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | fear ✓ | sadness |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | fear ✓ | joy |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | disgust |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear ✓ |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | sadness | joy ✓ |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | joy ✓ |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | anger | joy ✓ |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | anger | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | surprise ✓ |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | anger | surprise ✓ |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | anger | surprise ✓ |

### v1 vs v2 (O6)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 95 | 6 | 8 | 26 | 15 | 80.7% | 0.791 |

Texts where the prediction changed (29):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | anger ✓ |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | anger ✓ |
| eeerg5v | Look at that shit-eating grin | anger | disgust | anger ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | anger |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | sadness | fear ✓ |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | sadness |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | disgust | surprise |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | disgust | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | surprise |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness ✓ | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | surprise |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | anger |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | sadness | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | anger |

### v1 vs v3 (O6)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 93 | 8 | 13 | 27 | 9 | 80.0% | 0.383 |

Texts where the prediction changed (30):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | disgust | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | disgust ✓ | anger |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| edcxlpz | There was a horrible accident | fear | sadness | fear ✓ |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | fear ✓ |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | sadness | fear ✓ |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| edrc8re | Scary. I bet youre fun at parties. | fear | disgust | fear ✓ |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | disgust | joy ✓ |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | disgust | surprise |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness ✓ | disgust |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | disgust | sadness ✓ |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | sadness |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | disgust | surprise ✓ |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | sadness | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | disgust | surprise ✓ |

### v2 vs v3 (O6)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 97 | 6 | 9 | 33 | 5 | 86.7% | 0.607 |

Texts where the prediction changed (20):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | anger ✓ | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | anger ✓ | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | fear ✓ |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | fear ✓ |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | disgust |
| edrc8re | Scary. I bet youre fun at parties. | fear | sadness | fear ✓ |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | joy ✓ |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | sadness | disgust |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | surprise | anger |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | surprise | sadness ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | anger | surprise ✓ |

## Label-order checks

### v1

Macro-F1 spread across orders (max - min): **0.076**

| order | labels order | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp |
|---|---|---|---|---|---|---|---|---|
| O1 | anger, disgust, fear, joy, sadness, surprise | 0.663 | 0.72 | 0.60 | 0.57 | 0.78 | 0.72 | 0.59 |
| O2 | disgust, fear, joy, sadness, surprise, anger | 0.649 | 0.64 | 0.62 | 0.53 | 0.77 | 0.80 | 0.54 |
| O3 | fear, joy, sadness, surprise, anger, disgust | 0.710 | 0.71 | 0.59 | 0.65 | 0.81 | 0.83 | 0.67 |
| O4 | joy, sadness, surprise, anger, disgust, fear | 0.725 | 0.74 | 0.62 | 0.68 | 0.80 | 0.85 | 0.65 |
| O5 | sadness, surprise, anger, disgust, fear, joy | 0.716 | 0.71 | 0.58 | 0.68 | 0.82 | 0.84 | 0.67 |
| O6 | surprise, anger, disgust, fear, joy, sadness | 0.672 | 0.72 | 0.58 | 0.57 | 0.81 | 0.71 | 0.64 |

Per-text consistency (same pred under all 6 orders): **74.7%** (112/150)

Prediction rate by list position (expected ~16.7% each):

| pos 1 | pos 2 | pos 3 | pos 4 | pos 5 | pos 6 |
|---|---|---|---|---|---|
| 14.0% | 14.8% | 16.1% | 16.9% | 18.6% | 19.7% |

Inconsistent texts (38):

| id | text | gold | O1 | O2 | O3 | O4 | O5 | O6 |
|---|---|---|---|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | surprise | disgust | disgust | disgust | disgust |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger | anger | anger | anger | surprise | anger |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | sadness | anger | anger | anger | disgust | sadness |
| eeerg5v | Look at that shit-eating grin | anger | disgust | anger | anger | anger | disgust | disgust |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | sadness | anger | anger | anger | anger | sadness |
| eetoykw | It feels oddly comforting and familiar that we suck at hockey again. | disgust | sadness | sadness | sadness | sadness | joy | sadness |
| eetucfv | The humidity in Sydney is worse. | disgust | sadness | disgust | disgust | disgust | disgust | sadness |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust | anger | disgust | disgust | disgust | disgust |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | sadness | disgust | disgust | disgust | disgust | disgust |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger | anger | disgust | disgust | disgust |
| eet78m8 | If he hits you and constantly degrades you, it's abuse | disgust | sadness | anger | anger | anger | anger | sadness |
| effw6qi | Disgusting. Need to get the tooth hole fixed😂 | disgust | disgust | anger | disgust | disgust | disgust | disgust |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | surprise | disgust | surprise | surprise | surprise |
| edcxlpz | There was a horrible accident | fear | sadness | fear | sadness | fear | fear | sadness |
| ee1u7av | It’s gonna be a large group interview in a shady office. Ghost em. | fear | fear | disgust | fear | fear | fear | fear |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger | disgust | disgust | disgust | disgust |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | anger | fear | fear | fear | sadness |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | disgust | anger | anger | disgust | disgust | disgust |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | surprise | fear | fear | fear | sadness |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger | anger | anger | disgust | disgust |
| edrc8re | Scary. I bet youre fun at parties. | fear | surprise | surprise | disgust | disgust | disgust | disgust |
| edx3px0 | I get scared just reading your flair | fear | fear | disgust | fear | fear | fear | fear |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | sadness | sadness | joy | surprise | joy | sadness |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | surprise | surprise | surprise | surprise | disgust |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | sadness | anger | anger | disgust | disgust | sadness |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | surprise | disgust | disgust | disgust | disgust | disgust |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | surprise | disgust | surprise | joy | joy |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness | anger | anger | anger | disgust | sadness |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | sadness | disgust | disgust | disgust | disgust | disgust |
| ed7yj4s | It must be really sad and lonely under your bridge troll. | sadness | sadness | sadness | sadness | sadness | disgust | sadness |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | sadness | surprise | surprise | surprise | surprise |
| eevq4j1 | ? ur slide is right stick | surprise | surprise | anger | disgust | anger | disgust | disgust |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | surprise | surprise | surprise | surprise | surprise | sadness |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | joy | joy | surprise | joy | joy |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | sadness | disgust | disgust | surprise | sadness |
| eecahse | Oh wow I genuinely thought this was funny can’t believe you copped it so hard | surprise | surprise | joy | surprise | surprise | surprise | surprise |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger | disgust | disgust | disgust | disgust |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | anger | disgust | disgust | disgust | disgust |

### v2

Macro-F1 spread across orders (max - min): **0.062**

| order | labels order | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp |
|---|---|---|---|---|---|---|---|---|
| O1 | anger, disgust, fear, joy, sadness, surprise | 0.656 | 0.63 | 0.65 | 0.61 | 0.79 | 0.65 | 0.60 |
| O2 | disgust, fear, joy, sadness, surprise, anger | 0.654 | 0.56 | 0.59 | 0.61 | 0.76 | 0.81 | 0.59 |
| O3 | fear, joy, sadness, surprise, anger, disgust | 0.697 | 0.62 | 0.67 | 0.65 | 0.79 | 0.83 | 0.62 |
| O4 | joy, sadness, surprise, anger, disgust, fear | 0.716 | 0.61 | 0.68 | 0.72 | 0.76 | 0.84 | 0.68 |
| O5 | sadness, surprise, anger, disgust, fear, joy | 0.691 | 0.61 | 0.68 | 0.68 | 0.80 | 0.76 | 0.61 |
| O6 | surprise, anger, disgust, fear, joy, sadness | 0.690 | 0.64 | 0.70 | 0.65 | 0.82 | 0.70 | 0.64 |

Per-text consistency (same pred under all 6 orders): **77.3%** (116/150)

Prediction rate by list position (expected ~16.7% each):

| pos 1 | pos 2 | pos 3 | pos 4 | pos 5 | pos 6 |
|---|---|---|---|---|---|
| 15.3% | 14.9% | 15.9% | 16.9% | 18.0% | 19.0% |

Inconsistent texts (34):

| id | text | gold | O1 | O2 | O3 | O4 | O5 | O6 |
|---|---|---|---|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | sadness | anger | anger | anger | anger | anger |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | sadness | anger | anger | anger | sadness | anger |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | sadness | anger | anger | anger | anger | sadness |
| edahxv0 | Must be so frustrating having the wrong old man facing their own shutdowns. | anger | sadness | anger | anger | anger | sadness | sadness |
| ed85eg7 | That explains an awful lot about ICP. | disgust | surprise | anger | surprise | surprise | surprise | surprise |
| eetucfv | The humidity in Sydney is worse. | disgust | sadness | disgust | anger | anger | disgust | sadness |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | sadness | anger | anger | anger | anger | anger |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | sadness | anger | sadness | sadness | sadness | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger | anger | anger | anger | anger |
| eet78m8 | If he hits you and constantly degrades you, it's abuse | disgust | sadness | anger | anger | anger | anger | sadness |
| effw6qi | Disgusting. Need to get the tooth hole fixed😂 | disgust | disgust | anger | disgust | disgust | disgust | disgust |
| efapqfy | that's like a kel'thuzad/kael'thas wet dream right there. Line them up for disgusting aoe XD | disgust | disgust | anger | disgust | disgust | disgust | disgust |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | sadness | anger | disgust | disgust | disgust | disgust |
| edt81gk | Top 10 nibbas satan's too afraid to torture. | fear | surprise | surprise | surprise | fear | surprise | surprise |
| edcxlpz | There was a horrible accident | fear | sadness | sadness | sadness | fear | fear | fear |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | fear | fear | fear | fear | sadness |
| edrc8re | Scary. I bet youre fun at parties. | fear | surprise | surprise | surprise | surprise | surprise | sadness |
| edx3px0 | I get scared just reading your flair | fear | fear | anger | fear | fear | fear | fear |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | sadness | disgust | disgust | anger | disgust | sadness |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | sadness | anger | anger | anger | anger | sadness |
| ef3nupt | AMD this is why we rejoice in his banning.... :) | joy | joy | anger | joy | joy | joy | joy |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | surprise | anger | anger | anger | joy | surprise |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | surprise | disgust | surprise | surprise | sadness | surprise |
| eepdkxb | Cheers, I live minutes away from you, will check it out some time soon. | joy | joy | joy | joy | surprise | joy | joy |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | anger | anger | anger | anger | joy |
| ef8ijup | that is the saddest damn yogurt ive ever seen | sadness | sadness | disgust | sadness | disgust | disgust | sadness |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | sadness | sadness | sadness | sadness | sadness | surprise |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | sadness | anger | disgust | surprise | disgust | sadness |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | sadness | sadness | sadness | surprise | sadness | surprise |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | anger | surprise | surprise | surprise | surprise |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | surprise | anger | anger | anger | joy | surprise |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | sadness | surprise | surprise | sadness | sadness |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger | anger | anger | anger | anger |
| eeqzmin | It’s bad law. I wouldn’t be surprised either. | surprise | surprise | anger | anger | anger | anger | anger |

### v3

Macro-F1 spread across orders (max - min): **0.029**

| order | labels order | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp |
|---|---|---|---|---|---|---|---|---|
| O1 | anger, disgust, fear, joy, sadness, surprise | 0.704 | 0.60 | 0.65 | 0.75 | 0.80 | 0.76 | 0.67 |
| O2 | disgust, fear, joy, sadness, surprise, anger | 0.719 | 0.60 | 0.69 | 0.78 | 0.79 | 0.81 | 0.64 |
| O3 | fear, joy, sadness, surprise, anger, disgust | 0.726 | 0.61 | 0.65 | 0.78 | 0.79 | 0.81 | 0.71 |
| O4 | joy, sadness, surprise, anger, disgust, fear | 0.733 | 0.60 | 0.68 | 0.78 | 0.79 | 0.83 | 0.72 |
| O5 | sadness, surprise, anger, disgust, fear, joy | 0.727 | 0.60 | 0.67 | 0.68 | 0.86 | 0.80 | 0.76 |
| O6 | surprise, anger, disgust, fear, joy, sadness | 0.712 | 0.60 | 0.65 | 0.75 | 0.82 | 0.73 | 0.72 |

Per-text consistency (same pred under all 6 orders): **82.0%** (123/150)

Prediction rate by list position (expected ~16.7% each):

| pos 1 | pos 2 | pos 3 | pos 4 | pos 5 | pos 6 |
|---|---|---|---|---|---|
| 17.1% | 15.9% | 16.2% | 16.8% | 15.9% | 18.1% |

Inconsistent texts (27):

| id | text | gold | O1 | O2 | O3 | O4 | O5 | O6 |
|---|---|---|---|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | sadness | sadness | disgust | disgust | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | disgust | surprise | surprise | surprise | surprise |
| eeomndj | I apologise for coming off as rude, the end comment was unnecessary and needlessly rude | anger | sadness | anger | anger | anger | sadness | sadness |
| ed85eg7 | That explains an awful lot about ICP. | disgust | surprise | disgust | surprise | surprise | surprise | surprise |
| eetucfv | The humidity in Sydney is worse. | disgust | sadness | disgust | disgust | disgust | disgust | sadness |
| ee1t9sw | no idea how [NAME] was a [NAME] or [NAME]. just awful | disgust | sadness | disgust | sadness | sadness | sadness | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | anger | disgust | anger | anger | anger | anger |
| eet78m8 | If he hits you and constantly degrades you, it's abuse | disgust | sadness | anger | anger | anger | anger | sadness |
| edcxlpz | There was a horrible accident | fear | fear | fear | fear | fear | sadness | fear |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | fear | fear | fear | fear | joy | fear |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | fear | fear | fear | fear | disgust | disgust |
| edrc8re | Scary. I bet youre fun at parties. | fear | surprise | surprise | surprise | fear | surprise | fear |
| eduhdh0 | In Canada you should probably be more worried about moose than bears | fear | surprise | fear | fear | surprise | fear | surprise |
| edsvx30 | Different personalities, I've always been like that with friends and family. | joy | sadness | sadness | sadness | surprise | joy | sadness |
| efefln5 | It's special if you're into it. Some women genuinely enjoy it. | joy | surprise | surprise | surprise | joy | joy | joy |
| edv2gbm | If you don't like it, you didn't have to comment. Just let people be happy. | joy | sadness | anger | anger | anger | joy | sadness |
| edlhhfm | My Ping Pong Queen looks so happy! I cried lol | joy | joy | sadness | sadness | sadness | joy | sadness |
| ed91gzi | ~~macri gato~~ Also, nice to see Buthan there | joy | surprise | disgust | surprise | surprise | sadness | surprise |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | joy | joy | joy | surprise | joy | joy |
| edhj78h | Had such a hard time cutting up the steak | sadness | anger | disgust | disgust | disgust | disgust | disgust |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | disgust | disgust | surprise | surprise | sadness |
| eevq4j1 | ? ur slide is right stick | surprise | surprise | anger | surprise | surprise | surprise | surprise |
| edzh5rz | I've been into cuckolding for many years, and I'm wondering the same thing! | surprise | surprise | disgust | surprise | surprise | surprise | surprise |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | joy | anger | surprise | surprise | joy | surprise |
| eewbfj5 | Oh my gosh she opens her gullet like a freaking pelican!!! | surprise | surprise | disgust | surprise | surprise | surprise | surprise |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | anger | anger | anger | anger | surprise | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | disgust | disgust | disgust | anger | anger | anger |
