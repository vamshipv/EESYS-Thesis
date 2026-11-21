> **INVALID (2026-11-21): scored with the old >=3-char token rule, which drops 'f', the tokenizer's first token of lowercase 'fear'; fear could not be scored under v2/v3. Kept for the record; see 02_Decisions.**

# Prompt comparison report: 2026-11-21_ollama_dryrun

- Backend: ollama, model: ollama:llama3.1:latest
- Sample: dev_large
- Rows: 450; versions: v1, v2, v3; orders: O1
- Prompt hashes: {'v1': 'd9250dd0ca98', 'v2': 'aa283b52fffd', 'v3': 'bcf65961ce96'}; git: 23d401c-dirty
- label_mass = probability on label tokens before renormalising (Ollama: top-20 logprobs only, so a lower bound).

## Headline

| version | order | n | acc | macro-F1 | F1 ange | F1 disg | F1 fear | F1 joy | F1 sadn | F1 surp | worst class | mean mass | mass<0.9 | mass<0.5 | mean s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | O1 | 150 | 66.7% | 0.663 | 0.68 | 0.61 | 0.57 | 0.78 | 0.72 | 0.62 | fear (0.57) | 0.892 | 21.3% | 8.7% | 0.36 |
| v2 | O1 | 150 | 58.0% | 0.536 | 0.61 | 0.65 | 0.00 | 0.79 | 0.59 | 0.57 | fear (0.00) | 0.813 | 30.7% | 16.7% | 0.36 |
| v3 | O1 | 150 | 64.7% | 0.632 | 0.59 | 0.67 | 0.39 | 0.80 | 0.72 | 0.63 | fear (0.39) | 0.881 | 16.0% | 10.0% | 0.39 |

## Confusion matrices

### v1 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 17 | 4 | 0 | 0 | 3 | 1 |
| disgust | 2 | 17 | 0 | 0 | 5 | 1 |
| fear | 4 | 5 | 10 | 0 | 2 | 4 |
| joy | 0 | 1 | 0 | 18 | 2 | 4 |
| sadness | 0 | 1 | 0 | 1 | 22 | 1 |
| surprise | 2 | 3 | 0 | 2 | 2 | 16 |
| **pred total** | 25 | 31 | 10 | 21 | 36 | 27 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 68.0% | 16.0% | 0.0% | 0.0% | 12.0% | 4.0% |
| disgust | 8.0% | 68.0% | 0.0% | 0.0% | 20.0% | 4.0% |
| fear | 16.0% | 20.0% | 40.0% | 0.0% | 8.0% | 16.0% |
| joy | 0.0% | 4.0% | 0.0% | 72.0% | 8.0% | 16.0% |
| sadness | 0.0% | 4.0% | 0.0% | 4.0% | 88.0% | 4.0% |
| surprise | 8.0% | 12.0% | 0.0% | 8.0% | 8.0% | 64.0% |

### v2 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 19 | 1 | 0 | 0 | 5 | 0 |
| disgust | 4 | 14 | 0 | 0 | 6 | 1 |
| fear | 8 | 2 | 0 | 0 | 9 | 6 |
| joy | 0 | 0 | 0 | 17 | 3 | 5 |
| sadness | 2 | 0 | 0 | 0 | 22 | 1 |
| surprise | 4 | 1 | 0 | 1 | 4 | 15 |
| **pred total** | 37 | 18 | 0 | 18 | 49 | 28 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 76.0% | 4.0% | 0.0% | 0.0% | 20.0% | 0.0% |
| disgust | 16.0% | 56.0% | 0.0% | 0.0% | 24.0% | 4.0% |
| fear | 32.0% | 8.0% | 0.0% | 0.0% | 36.0% | 24.0% |
| joy | 0.0% | 0.0% | 0.0% | 68.0% | 12.0% | 20.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 16.0% | 4.0% | 0.0% | 4.0% | 16.0% | 60.0% |

### v3 / O1

Counts:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 17 | 2 | 0 | 0 | 4 | 2 |
| disgust | 4 | 16 | 0 | 0 | 4 | 1 |
| fear | 6 | 3 | 6 | 0 | 3 | 7 |
| joy | 1 | 1 | 0 | 18 | 2 | 3 |
| sadness | 2 | 0 | 0 | 0 | 22 | 1 |
| surprise | 3 | 1 | 0 | 2 | 1 | 18 |
| **pred total** | 33 | 23 | 6 | 20 | 36 | 32 |

Row-normalised:

| gold \ pred | anger | disgust | fear | joy | sadness | surprise |
|---|---|---|---|---|---|---|
| anger | 68.0% | 8.0% | 0.0% | 0.0% | 16.0% | 8.0% |
| disgust | 16.0% | 64.0% | 0.0% | 0.0% | 16.0% | 4.0% |
| fear | 24.0% | 12.0% | 24.0% | 0.0% | 12.0% | 28.0% |
| joy | 4.0% | 4.0% | 0.0% | 72.0% | 8.0% | 12.0% |
| sadness | 8.0% | 0.0% | 0.0% | 0.0% | 88.0% | 4.0% |
| surprise | 12.0% | 4.0% | 0.0% | 8.0% | 4.0% | 72.0% |

## Flip tables (same order)

### v1 vs v2 (O1)

| both right | broke (v1 right, v2 wrong) | fixed (v1 wrong, v2 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 83 | 17 | 4 | 35 | 11 | 78.7% | 0.007 |

Texts where the prediction changed (32):

| id | text | gold | pred v1 | pred v2 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | surprise | sadness |
| eeerg5v | Look at that shit-eating grin | anger | disgust | anger ✓ |
| edtrli2 | I've seen AOCs ridiculous proposals | anger | disgust | anger ✓ |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | disgust ✓ | anger |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | sadness |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | disgust ✓ | sadness |
| ed0s890 | I’m afraid too. It’s the not knowing what will happen that scares me. | fear | fear ✓ | sadness |
| ee2lna8 | It happens so much that it really scares me tbh. | fear | fear ✓ | surprise |
| ee1u7av | It’s gonna be a large group interview in a shady office. Ghost em. | fear | fear ✓ | anger |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| edew673 | I would be afraid he would come back and somehow blame me for his failure. | fear | fear ✓ | sadness |
| efg7lsu | i have bought this but not played. i'm scared. hold me. | fear | fear ✓ | sadness |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | disgust | anger |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | surprise | sadness |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| edx3px0 | I get scared just reading your flair | fear | fear ✓ | sadness |
| ee913vk | I was scared for that white building. | fear | fear ✓ | surprise |
| eebatsv | That’s what I’m terrified of. | fear | fear ✓ | surprise |
| ef75xhl | We all are afraid of losing our jobs here or being blackballed all the same. | fear | fear ✓ | sadness |
| ee2kw21 | Please elaborate on that story! Ive always been afraid of exactly this happening to me. | fear | fear ✓ | sadness |
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

### v1 vs v3 (O1)

| both right | broke (v1 right, v3 wrong) | fixed (v1 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 91 | 9 | 6 | 36 | 8 | 84.7% | 0.607 |

Texts where the prediction changed (23):

| id | text | gold | pred v1 | pred v3 |
|---|---|---|---|---|
| efh5nbl | I would absolutely hate it if they used it in the games tbh | anger | disgust | sadness |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| edtrli2 | I've seen AOCs ridiculous proposals | anger | disgust | anger ✓ |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | disgust ✓ | anger |
| ed5nhb9 | The very worst possible route they could have gone. | disgust | sadness | anger |
| ee2lna8 | It happens so much that it really scares me tbh. | fear | fear ✓ | surprise |
| ee1u7av | It’s gonna be a large group interview in a shady office. Ghost em. | fear | fear ✓ | anger |
| eegpyf2 | If an AI projectile is your biggest problem you've got bigger issues, next. | fear | disgust | anger |
| efg7lsu | i have bought this but not played. i'm scared. hold me. | fear | fear ✓ | sadness |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | surprise |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | surprise |
| eddiml0 | That’s a terrible amount of bp for 11 kills | fear | disgust | anger |
| ee2kw21 | Please elaborate on that story! Ive always been afraid of exactly this happening to me. | fear | fear ✓ | sadness |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | joy ✓ | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | joy ✓ |
| edhj78h | Had such a hard time cutting up the steak | sadness | sadness ✓ | anger |
| eeaal96 | Yikes. I feel sorry for the team that gives him anything above 5.5 | sadness | disgust | anger |
| eeldnnq | Here's a purple heart for you recapping that! OMG matching romantic scoots I'm cryin' | sadness | joy | sadness ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | disgust | surprise ✓ |
| eeb188m | Wow [NAME] has a lot more insecurities than I thought | surprise | surprise ✓ | sadness |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | surprise ✓ |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |

### v2 vs v3 (O1)

| both right | broke (v2 right, v3 wrong) | fixed (v2 wrong, v3 right) | both wrong, same label | both wrong, different | pred agreement | McNemar p (exact) |
|---|---|---|---|---|---|---|
| 84 | 3 | 13 | 40 | 10 | 82.7% | 0.021 |

Texts where the prediction changed (26):

| id | text | gold | pred v2 | pred v3 |
|---|---|---|---|---|
| ef1i4tx | Me but with boobs. When will be able to trade body parts [NAME] | anger | sadness | surprise |
| eeydnih | Whaaaat no way, you can’t play it with other people? | anger | anger ✓ | surprise |
| eeerg5v | Look at that shit-eating grin | anger | anger ✓ | disgust |
| ed1fvvy | Not any weirder than male doctors handling women junk for centuries. | disgust | anger | disgust ✓ |
| edqg9pm | Unhhh has not been funny for a while now. This is definitely a terrible idea. | disgust | sadness | anger |
| edribac | [NAME] but probably secondly, [NAME] because I find both so boring. | disgust | sadness | disgust ✓ |
| ed0s890 | I’m afraid too. It’s the not knowing what will happen that scares me. | fear | sadness | fear ✓ |
| edew673 | I would be afraid he would come back and somehow blame me for his failure. | fear | sadness | fear ✓ |
| eejxmnj | Matinee games always scare me, but I have confidence in this team. LGI! | fear | sadness | surprise |
| eeuhyfj | Venezuela has uniquely terrible oil. | fear | anger | disgust |
| ef70jgb | oh man clicking 2 buttons before you read an article, the absolute horror | fear | anger | surprise |
| edy460m | Stoop Kid’s afraid to leave his stoop! | fear | sadness | surprise |
| edx3px0 | I get scared just reading your flair | fear | sadness | fear ✓ |
| ee913vk | I was scared for that white building. | fear | surprise | fear ✓ |
| eebatsv | That’s what I’m terrified of. | fear | surprise | fear ✓ |
| ef75xhl | We all are afraid of losing our jobs here or being blackballed all the same. | fear | sadness | fear ✓ |
| efc05gk | I hope you enjoy endless mosquitoes as the climate warms. | joy | sadness | disgust |
| editvs0 | [NAME] always makes my day when he's yelling at the refs | joy | surprise | anger |
| efh46zt | This is actually funny OP, stop trying to be so negative | joy | surprise | joy ✓ |
| edj4q2f | Oh god the “glow”! I get comments about it at work almost weekly. | surprise | sadness | surprise ✓ |
| ee74jew | 730,000 readers and only 6 posts in a week? Wow... | surprise | sadness | surprise ✓ |
| eevq4j1 | ? ur slide is right stick | surprise | anger | surprise ✓ |
| edv7c5c | Omg l live for [NAME] stirring the pot!! | surprise | surprise ✓ | joy |
| edet9yg | I still can't believe I used to watch [NAME] videos | surprise | sadness | surprise ✓ |
| eewrafg | Wow, not exactly a complimentary typo. | surprise | disgust | anger |
| eegp95p | Shocking that a fat DnD kid is this self-important. Remarkable. | surprise | anger | disgust |
