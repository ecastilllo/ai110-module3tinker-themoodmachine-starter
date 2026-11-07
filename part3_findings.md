# Part 3: Stress test and targeted fix

## Experiment
Ran the Part 2 model on nine breaker sentences and four pairs of equivalent
language styles. Printed tokens, matched signals, scores, labels, and tokens
with no direct vocabulary match using `stress_test.py`.
Negators and modifiers have a control role even though they do not directly
match the mood vocabulary. Intended labels below are interpretations for this
exercise; sarcasm, emojis, and softened statements can be ambiguous.

## Observed before/after results

| Breaker | Intended | Before | After |
| --- | --- | --- | --- |
| I love getting stuck in traffic | negative | positive | positive |
| That concert was sick | positive | neutral | neutral |
| I feel sick today | negative | neutral | neutral |
| That concert was fire | positive | neutral | neutral |
| I'm fine 🙃 | negative (frustrated reading) | neutral | neutral |
| I'm exhausted but proud of myself | mixed | neutral | neutral |
| I'm not very happy about this | negative | positive | negative |
| The exam was not really bad | positive | negative | positive |
| I'm happy but sad | mixed | mixed | mixed |

In the traffic example, "love" alone contributes +1. No other word contributes,
so that single keyword dominates the prediction. "Sick", "fire", "exhausted",
"proud", and the emoji receive no mood score. The model cannot infer their
meaning from context. Adding "sick" globally as positive would risk getting
"I feel sick today" wrong.

## Language style consistency

| Standard phrasing | Alternative style | Before predictions | After predictions |
| --- | --- | --- | --- |
| That concert was amazing | That concert was fire (slang) | positive / neutral | positive / neutral |
| I'm so happy | I'm soooo happyyy (informal spelling) | positive / neutral | positive / neutral |
| I'm excited about this | I'm well chuffed about this (regional expression) | positive / neutral | positive / neutral |
| I'm not happy | I'm not very happy (softened phrasing) | negative / positive | negative / negative |

The first three pairs show a systematic disadvantage for these tested language
styles because the vocabulary favors standard wording. This is evidence of
language style bias in these examples, not a measurement of demographic group
performance or proof about every dialect. These gaps remain documented.

## Targeted change and hypothesis

Chosen failure: negation separated from a mood word by one modifier.
Before the change, only the immediately preceding token was checked.
In "not very happy", "very" prevented the model from seeing "not", leaving
"happy" with a score of +1.

Hypothesis: allowing negation across exactly one of "very", "really", "so",
or "too" will fix this pattern without crossing punctuation or conjunctions.
Changed only the negation window and its explanatory phrase in
`mood_analyzer.py`; retained the vocabulary and label thresholds.

After the change, "not very happy" contributes -1 and "not really bad"
contributes +1. Both breakers are corrected. The explanation includes the
whole negated phrase.

## Verification and limitations

- Breaker matches improved from 1/9 to 3/9.
- All 16 original dataset predictions stayed the same: 11/16 correct (68.75%).
- Twelve targeted and regression checks passed, covering ordinary labels,
  direct and modified negation, contractions, punctuation boundaries,
  conjunction boundaries, repeated signals, and the one-modifier limit.
- `main.py` completed successfully, including exit from its interactive loop.
- No regressions appeared in these checks; broader reliability is unproven.
- "not very very happy" still becomes positive: the rule spans only one modifier.
- Sarcasm, ambiguous slang, emojis, and unfamiliar emotional words remain hard.
- "not really bad" may mean neutral or mildly positive depending on context;
  reversing polarity is an intentionally simplified rule.
- The breaker set guided the fix, so its improvement is not independent
  evidence of general accuracy.

## Reproduce

```bash
python -X utf8 main.py
python -X utf8 stress_test.py
```

The checked-in stress test runs the revised model. The Before column records
the actual run against the Part 2 version (commit 712331782e8860973fa04c7be7215f0d4e63af56).
