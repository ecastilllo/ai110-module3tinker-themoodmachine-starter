# Model Card: Mood Machine

## 1. Model Overview

**Model type:** Rule-based classifier in `mood_analyzer.py`, compared with a
bag-of-words logistic regression classifier in `ml_experiments.py`.

**Intended purpose:** Classify the expressed tone of short English posts as
positive, negative, neutral, or mixed for a classroom experiment. A text label
is an interpretation of wording, not a measurement of the author's mental state.

**Intended users:** Students exploring how rules, data, labels, and evaluation
affect model behavior. These models have not been validated for consequential
decisions or mental-health assessment.

## 2. Data

**Dataset:** `SAMPLE_POSTS` contains 20 short, constructed English posts:
six starter examples, ten added in Part 1, and four added in Part 4.
Every post has a corresponding entry at the same index in `TRUE_LABELS`.
There are six positive, six negative, three neutral, and five mixed labels.

**Labeling:** Added examples and their labels were drafted with AI assistance.
Labels reflect the intended reading: praise as positive, frustration as negative,
routine statements as neutral, and opposing feelings as mixed. No independent
annotator agreement or group consensus was measured. These labels should not be
treated as unquestionable ground truth.

**Characteristics and gaps:** Posts include slang, emojis, sarcasm, negation,
and mixed feelings. For example, "Got the internship! Still stressed about moving
away 🥲" is mixed because achievement and anxiety coexist. "This is fine" is
labeled neutral, but context could make it sarcastic. The dataset is tiny,
uneven across classes, and does not represent the full range of English styles,
other languages, or real users. The mood word lists remain the starter lists
of ten positive and ten negative words; expanding the posts did not expand them.

## 3. How the Rule Based Model Works

**Preprocessing:** Lowercase text, normalize curly apostrophes, and separate
words, contractions, punctuation, and emojis into tokens. Punctuation no longer
prevents "happy!" from matching "happy". Emojis are visible in explanations but
receive no mood score.

**Scoring and labels:**

- Each positive-word occurrence adds 1; each negative-word occurrence subtracts 1.
- Negation with not/no/never or an n't contraction reverses a matched word's
  sign, directly or across one modifier: very, really, so, or too.
- A positive total returns positive; a negative total returns negative.
- A zero total with both positive and negative contributions returns mixed.
  A zero total without opposing signals returns neutral.
- `explain()` reports tokens, adjusted matches, total score, and label.

**Enhancement:** Part 3 extended adjacent negation to one modifier.
"I'm not very happy about this" changed from positive to negative, and
"The exam was not really bad" changed from negative to positive.
The nine-breaker result improved from 1/9 to 3/9 without changing any of the
original 16 dataset predictions.

**Strengths:** Transparent, repeatable behavior on known words, direct
negation, and balanced opposing signals.

**Weaknesses:** Unknown words contribute nothing. Mixed feelings with unequal
scores are classified by the stronger sign. Sarcasm and broader negation scope
are not understood.

## 4. How the ML Model Works

**Features and training:** CountVectorizer converts posts into lowercase
unigram word counts. Its default tokenization excludes emojis and
single-character tokens. LogisticRegression learns class weights from
`SAMPLE_POSTS` and `TRUE_LABELS`; it does not use the rule model's word lists.

**Data sensitivity:** Adding four labeled posts increased the learned vocabulary
from 79 to 94 features and changed weights. The ML model fit all added labels,
while the rule model missed all four. However, no predicted labels changed on
the fixed original 16 posts or the eight unseen probes. Unseen accuracy did not
improve in this experiment. Labels were not deliberately changed, so sensitivity
to relabeling was not measured.

**Strengths and weaknesses:** ML learns associations beyond the fixed word lists,
but can fit a tiny training set while making surprising errors on new text.
Correctly classifying a sarcastic training post does not demonstrate a general
ability to understand sarcasm.

## 5. Evaluation

Both entry points completed successfully. `part4_evaluation.py` compared models
before and after four additions, using the same eight probes excluded from
training.

| Evaluation set | Rule before | ML before | Rule after | ML after |
| --- | --- | --- | --- | --- |
| Current labeled dataset | 11/16 (68.75%) | 16/16 (100%) | 11/20 (55%) | 20/20 (100%) |
| Fixed original 16 posts | 11/16 | 16/16 | 11/16 | 16/16 |
| Fixed eight unseen probes | 4/8 (50%) | 6/8 (75%) | 4/8 (50%) | 6/8 (75%) |

**Interpretation:** ML's dataset score is training accuracy. The eight probes
are selected diagnostics, not a representative benchmark. The rule score fell
because the evaluation set gained harder posts, not because original predictions
regressed. Accuracy also hides class differences: on the expanded dataset,
the rule model gets only 1/5 mixed posts right, compared with 3/3 neutral posts.

**Correct rule predictions:**

| Example | Prediction | Explanation |
| --- | --- | --- |
| Today was a terrible day | negative | terrible contributes -1 |
| I am not happy about this | negative | not reverses happy to -1 |
| I'm happy for you, but sad that you're leaving | mixed | happy +1 and sad -1 balance |

**Incorrect predictions and contrasting failures:**

| Example | Intended | Rule | ML | What the result shows |
| --- | --- | --- | --- | --- |
| I absolutely love getting stuck in traffic 🙄 | negative | positive | negative | Rule counts love +1; ML has trained on this labeled post |
| I'm exhausted but proud of myself | mixed | neutral | Not evaluated on this exact sentence | Rule knows neither emotional word |
| I am happy and excited | positive | positive | negative | ML fails on this unseen combination of familiar words |
| The meeting starts at noon | neutral | neutral | positive | ML assigns an emotional label to an unseen routine statement |

The traffic error is documented as a limitation rather than patched with a
broad rule that could damage sincere uses of "love".
Full observations are in [Part 3 findings](part3_findings.md),
[Part 4 findings](part4_findings.md), and
[measured predictions](part4_measured_results.md).

## 6. Limitations

- Sarcasm remains unreliable: "I love getting stuck in traffic" is positive
  under the rules because only love contributes.
- Unfamiliar slang, emojis, and emotional vocabulary are missed. "That concert
  was fire" and "I'm fine 🙃" both receive neutral rule labels under the intended
  positive and frustrated readings, respectively.
- "not very very happy" still becomes positive because negation spans only
  one supported modifier. Negated negative words may be neutral in context
  rather than positive as the simplified rule assumes.
- Neither model has been validated on long posts, other languages, or a broad
  population. Ambiguous labels and small sample sizes limit conclusions.
- A neutral prediction can mean no recognized signal, not an absence of emotion.

## 7. Ethical Considerations

**Overt bias / language-style coverage:** Part 3 found inconsistent treatment of
equivalent styles. "That concert was amazing" is positive, but "That concert
was fire" is neutral. "I'm so happy" is positive, but "I'm soooo happyyy" is
neutral. "I'm excited about this" is positive, but "I'm well chuffed about this"
is neutral. The rule model may underserve writers using slang, expressive
spelling, or regional expressions because its vocabulary favors standard
wording. These examples demonstrate a style-coverage gap; demographic group
performance was not measured.

**Covert compliance / AI-assistant reflection:** There was no separate formal
word-list audit. During stress testing, the assistant raised style-coverage
problems and warned that making "sick" universally positive could misclassify
"I feel sick today". During evaluation, it also flagged that ML training
accuracy does not establish unseen performance. It therefore did not simply
confirm every modeling choice. However, the initial dataset expansion did not
include a systematic coverage or label-agreement audit. The assistant should
have highlighted those gaps earlier and made the need to review AI-drafted
labels more explicit. Its suggestions required checks against actual outputs.

**Potential impact and privacy:** Misreading frustration as positive could
dismiss distress; style-dependent errors could disadvantage some writers.
The model should not guide employment, disciplinary, or clinical decisions.
If real messages are introduced, obtain appropriate consent, minimize retained
text, and protect personal information. The current examples are constructed
for this exercise.

## 8. Ideas for Improvement

- Review AI-assisted labels with multiple people and record disagreements.
- Collect more varied, balanced examples and preserve a separate test set.
- Measure per-class performance and matched language-style pairs.
- Test contextual handling of slang, emojis, negation, and unequal mixed signals.
- Compare word bigrams or character features against the unigram ML baseline,
  checking new examples for regressions rather than assuming improvement.

Evaluation environment: Python 3.11.18 and scikit-learn 1.5.2. The measured
Part 4 run is linked in `part4_findings.md`.
