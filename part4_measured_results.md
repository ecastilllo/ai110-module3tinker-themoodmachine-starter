# Part 4 measured results

ML dataset scores below are training accuracy, not unseen accuracy.
Probe labels are intended interpretations for this exercise.

| Evaluation set | Rule before | ML before | Rule after | ML after |
| --- | --- | --- | --- | --- |
| Current dataset (16 before, 20 after) | 11/16 | 16/16 | 11/20 | 20/20 |
| Fixed original 16 | 11/16 | 16/16 | 11/16 | 16/16 |
| Fixed 8 unseen probes | 4/8 | 6/8 | 4/8 | 6/8 |

## Original dataset before additions

| Post | Intended | Rule | ML |
| --- | --- | --- | --- |
| I love this class so much | positive | positive | positive |
| Today was a terrible day | negative | negative | negative |
| Feeling tired but kind of hopeful | mixed | negative | mixed |
| This is fine | neutral | neutral | neutral |
| So excited for the weekend | positive | positive | positive |
| I am not happy about this | negative | negative | negative |
| Lowkey excited that I finally got this code working 😂 | positive | positive | positive |
| No cap, this week has been awful | negative | negative | negative |
| Got the internship! Still stressed about moving away 🥲 | mixed | negative | mixed |
| I absolutely love getting stuck in traffic 🙄 | negative | positive | negative |
| Submitted the assignment and closed my laptop | neutral | neutral | neutral |
| That exam was not bad at all | positive | positive | positive |
| Great, my laptop crashed right before I could save | negative | positive | negative |
| I'm happy for you, but sad that you're leaving | mixed | mixed | mixed |
| Just sitting here waiting for the next class | neutral | neutral | neutral |
| Pizza with my friends after a long day = best night 😊 | positive | neutral | positive |

## Expanded dataset after additions

| Post | Intended | Rule | ML |
| --- | --- | --- | --- |
| I love this class so much | positive | positive | positive |
| Today was a terrible day | negative | negative | negative |
| Feeling tired but kind of hopeful | mixed | negative | mixed |
| This is fine | neutral | neutral | neutral |
| So excited for the weekend | positive | positive | positive |
| I am not happy about this | negative | negative | negative |
| Lowkey excited that I finally got this code working 😂 | positive | positive | positive |
| No cap, this week has been awful | negative | negative | negative |
| Got the internship! Still stressed about moving away 🥲 | mixed | negative | mixed |
| I absolutely love getting stuck in traffic 🙄 | negative | positive | negative |
| Submitted the assignment and closed my laptop | neutral | neutral | neutral |
| That exam was not bad at all | positive | positive | positive |
| Great, my laptop crashed right before I could save | negative | positive | negative |
| I'm happy for you, but sad that you're leaving | mixed | mixed | mixed |
| Just sitting here waiting for the next class | neutral | neutral | neutral |
| Pizza with my friends after a long day = best night 😊 | positive | neutral | positive |
| Feeling exhausted but proud after finishing my project | mixed | neutral | mixed |
| Lowkey hopeful about tomorrow even though I'm tired | mixed | negative | mixed |
| That concert was fire, best night with my friends | positive | neutral | positive |
| Oh great, another deadline moved to tonight | negative | positive | negative |

## Unseen probes before additions

| Post | Intended | Rule | ML |
| --- | --- | --- | --- |
| That show was fire | positive | neutral | positive |
| I feel sick today | negative | neutral | negative |
| I love waiting in traffic | negative | positive | negative |
| I'm not very happy with the result | negative | negative | negative |
| I'm exhausted but proud of my progress | mixed | neutral | mixed |
| The meeting starts at noon | neutral | neutral | positive |
| I am happy and excited | positive | positive | negative |
| This is awful and terrible | negative | negative | negative |

## Same unseen probes after additions

| Post | Intended | Rule | ML |
| --- | --- | --- | --- |
| That show was fire | positive | neutral | positive |
| I feel sick today | negative | neutral | negative |
| I love waiting in traffic | negative | positive | negative |
| I'm not very happy with the result | negative | negative | negative |
| I'm exhausted but proud of my progress | mixed | neutral | mixed |
| The meeting starts at noon | neutral | neutral | positive |
| I am happy and excited | positive | positive | negative |
| This is awful and terrible | negative | negative | negative |

## Failure walkthrough

Tokens = ['i', 'absolutely', 'love', 'getting', 'stuck', 'in', 'traffic', '🙄']; positive = ['love']; negative = []; score = 1; label = positive

## Model and data inspection

CountVectorizer uses lowercase unigram word counts; the default token pattern excludes single-character tokens and emojis. LogisticRegression learns weights from the labeled examples. The script fits and evaluates on identical posts for its dataset score.

Before class counts: {'positive': 5, 'negative': 5, 'mixed': 3, 'neutral': 3}
After class counts: {'positive': 6, 'negative': 6, 'mixed': 5, 'neutral': 3}
Vocabulary size: 79 before; 94 after.
Python 3.11.18; scikit-learn 1.5.2.

Raw results, including actual ML token contributions for the walkthrough sentence, are in part4_results.json.
