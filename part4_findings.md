# Part 4: Evaluate Your System

## Dataset and execution
Verified that every post has a label: 16 pairs before expansion and 20 afterward.
All labels are positive, negative, neutral, or mixed. Added four posts covering
mixed emotions, slang, and sarcasm. Ran both main.py and ml_experiments.py and
exited their interactive loops successfully. Used the existing Part 3 rules
and the starter CountVectorizer + LogisticRegression implementation.

## Measured comparison

| Evaluation | Rule before | ML before | Rule after | ML after |
| --- | --- | --- | --- | --- |
| Current dataset | 11/16 (68.75%) | 16/16 (100%) | 11/20 (55%) | 20/20 (100%) |
| Fixed original 16 posts | 11/16 | 16/16 | 11/16 | 16/16 |
| Fixed 8 unseen probes | 4/8 (50%) | 6/8 (75%) | 4/8 (50%) | 6/8 (75%) |

The ML dataset evaluation reuses its training examples. Its 100% score measures
fit to those examples, not generalization. The eight probes were excluded from
both training datasets, but they form a tiny, selected diagnostic set, not a
representative benchmark. Neither result establishes broad reliability.

## Mismatches and patterns
Before adding posts, the rule model missed five examples:

| Post | Human label | Rule prediction | Reason |
| --- | --- | --- | --- |
| Feeling tired but kind of hopeful | mixed | negative | tired contributes -1; hopeful is unknown |
| Got the internship! Still stressed about moving away 🥲 | mixed | negative | stressed contributes -1; achievement and emoji have no score |
| I absolutely love getting stuck in traffic 🙄 | negative | positive | love contributes +1; sarcasm is not modeled |
| Great, my laptop crashed right before I could save | negative | positive | great contributes +1; crashed is unknown |
| Pizza with my friends after a long day = best night 😊 | positive | neutral | none of the tokens match the mood vocabulary |

The expanded rule dataset has nine mismatches: the same five plus all four new
posts. Unfamiliar emotional words, slang, and sarcastic praise are recurring
failure patterns. The rule model gets direct examples such as "Today was a
terrible day", direct negation such as "I am not happy about this", and balanced
known signals such as "I'm happy for you, but sad that you're leaving" right.

Accuracy hides uneven performance. On the 20-post dataset, rule correctness is
4/6 positive, 3/6 negative, 3/3 neutral, and only 1/5 mixed.

## One incorrect prediction: walkthrough, not a fix
Chosen sentence: "I absolutely love getting stuck in traffic 🙄".

1. Preprocessing produces:
   ['i', 'absolutely', 'love', 'getting', 'stuck', 'in', 'traffic', '🙄'].
2. "love" matches POSITIVE_WORDS and contributes +1.
3. No token matches NEGATIVE_WORDS. The preceding token "absolutely" is not a
   negator or a supported modifier following a negator, so love is not reversed.
4. The other words and emoji contribute no mood points.
5. The total is +1, so predict_label returns positive; the intended reading
   expresses frustration and is labeled negative.

The explanation matches the printed tokens, signal list, score, and source
conditions. Decision: document sarcasm as a limitation now. A broad rule that
turns "love" negative could break sincere positive posts. Neither model's
classification logic was changed in Part 4.

## How ML behaves differently
ML correctly labels every training row, including the sarcastic traffic post.
Code inspection shows it learns unigram word-count weights from labels rather
than using the positive and negative word lists. CountVectorizer's default
tokenization omits emojis, so the rolling-eyes emoji cannot explain ML's result.

Measured weights support a learned word-association explanation: before the
additions, each of "absolutely", "getting", "stuck", and "traffic" contributes
about +0.234 to the negative-class logit in this training example. These are
class-specific contributions, not probabilities or a complete explanation
without the other classes and intercept. "love" itself also contributes
about +0.080 to that class. This is evidence of associations learned from
this tiny dataset, not evidence of understanding sarcasm.

Failures differ on unseen text. ML gets "I love waiting in traffic" right,
where the rule model still predicts positive. But ML calls "The meeting starts
at noon" positive and "I am happy and excited" negative; the rule model gets
both right. Correct training labels therefore do not eliminate surprising
errors on new combinations of familiar words.

## Effect of four added labeled posts
Added:
- "Feeling exhausted but proud after finishing my project" — mixed.
- "Lowkey hopeful about tomorrow even though I'm tired" — mixed.
- "That concert was fire, best night with my friends" — positive.
- "Oh great, another deadline moved to tonight" — negative.

ML retraining expands its vocabulary from 79 to 94 features and changes its
weights; for example, the traffic-token contribution above changes from
about +0.234 to +0.231. It fits all four new labels. The rule model does not learn
from SAMPLE_POSTS or TRUE_LABELS: its word lists and scoring rules are unchanged,
and it misses all four additions.

Thus ML is sensitive to added labeled training data at the vocabulary and
parameter level. In this experiment, that sensitivity produced no label
changes on the fixed original 16 or eight unseen probes, and no measured gain
in unseen accuracy. The rule score's drop from 68.75% to 55% reflects adding
harder evaluation examples, not a regression on the original posts.

## Reproduce and review
Run:

```bash
python -m pip install -r requirements.txt
python -X utf8 main.py
python -X utf8 ml_experiments.py
python -X utf8 part4_evaluation.py
```

part4_evaluation.py evaluates the first 16 posts, retrains on all 20, prints
individual predictions, and writes raw JSON and Markdown results.
part4_measured_results.md contains all observed predictions; part4_results.json
preserves measured counts, class counts, vocabulary sizes, and token contributions.

Verified run: Python 3.11.18, scikit-learn 1.5.2, NumPy 1.26.4, SciPy 1.13.1.
The GitHub Actions workflow pins these dependency versions and completed both
entry points and the comparison successfully:
https://github.com/ecastilllo/ai110-module3tinker-themoodmachine-starter/actions/runs/42407967523

The data and code snapshot tested was commit
49ca94faae44e180245f7061f29c74bede425389.
