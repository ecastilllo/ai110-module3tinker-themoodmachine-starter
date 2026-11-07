"""Reproduce Part 4 on the first 16 posts, then on all 20 posts.

Run: python -X utf8 part4_evaluation.py
Uses the starter ML training function without changing either model's logic.
"""
import json
import platform
from collections import Counter
from pathlib import Path

import sklearn
from dataset import SAMPLE_POSTS, TRUE_LABELS
from mood_analyzer import MoodAnalyzer
from ml_experiments import train_ml_model

# Fixed exploratory probes: never included in either training dataset.
# They are small, selected examples, not a representative test set.
PROBES = [
    ("That show was fire", "positive"),
    ("I feel sick today", "negative"),
    ("I love waiting in traffic", "negative"),
    ("I'm not very happy with the result", "negative"),
    ("I'm exhausted but proud of my progress", "mixed"),
    ("The meeting starts at noon", "neutral"),
    ("I am happy and excited", "positive"),
    ("This is awful and terrible", "negative"),
]

def evaluate_stage(texts, labels):
    assert len(texts) == len(labels)
    rule = MoodAnalyzer()
    vectorizer, model = train_ml_model(texts, labels)

    def rows(posts, expected):
        ml_predictions = model.predict(vectorizer.transform(posts))
        return [
            {"text": text, "true": true, "rule": rule.predict_label(text), "ml": str(ml)}
            for text, true, ml in zip(posts, expected, ml_predictions)
        ]

    training = rows(texts, labels)
    probes = rows([p[0] for p in PROBES], [p[1] for p in PROBES])
    original = rows(SAMPLE_POSTS[:16], TRUE_LABELS[:16])
    counts = {}
    for name, data in (("training", training), ("original16", original), ("probes", probes)):
        counts[name] = {
            model_name: sum(row[model_name] == row["true"] for row in data)
            for model_name in ("rule", "ml")
        }
        counts[name]["total"] = len(data)

    # Inspect the actual bag-of-words contributions for the chosen rule failure.
    example = "I absolutely love getting stuck in traffic 🙄"
    encoded = vectorizer.transform([example])
    winner = str(model.predict(encoded)[0])
    winning_index = list(model.classes_).index(winner)
    features = vectorizer.get_feature_names_out()
    contributions = [
        {"token": str(features[index]),
         "contribution": float(encoded[0, index] * model.coef_[winning_index, index])}
        for index in encoded.indices
    ]
    return {
        "training_rows": training, "probe_rows": probes, "original_rows": original,
        "correct_counts": counts, "label_counts": dict(Counter(labels)),
        "vocabulary_size": len(vectorizer.vocabulary_),
        "example_ml_prediction": winner,
        "example_ml_winning_class_contributions": contributions,
    }

def table(rows):
    result = ["| Post | Intended | Rule | ML |", "| --- | --- | --- | --- |"]
    result += ["| {text} | {true} | {rule} | {ml} |".format(**row) for row in rows]
    return "\n".join(result)

def main():
    assert len(SAMPLE_POSTS) == len(TRUE_LABELS) == 20
    assert set(TRUE_LABELS) <= {"positive", "negative", "neutral", "mixed"}
    assert not set(p[0] for p in PROBES) & set(SAMPLE_POSTS)
    before = evaluate_stage(SAMPLE_POSTS[:16], TRUE_LABELS[:16])
    after = evaluate_stage(SAMPLE_POSTS, TRUE_LABELS)
    results = {
        "python": platform.python_version(), "sklearn": sklearn.__version__,
        "before": before, "after": after,
        "chosen_failure_explanation": MoodAnalyzer().explain(
            "I absolutely love getting stuck in traffic 🙄"),
    }
    Path("part4_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Part 4 measured results", "",
             "ML dataset scores below are training accuracy, not unseen accuracy.",
             "Probe labels are intended interpretations for this exercise.", "",
             "| Evaluation set | Rule before | ML before | Rule after | ML after |",
             "| --- | --- | --- | --- | --- |"]
    for key, title in (("training", "Current dataset (16 before, 20 after)"),
                       ("original16", "Fixed original 16"), ("probes", "Fixed 8 unseen probes")):
        b, a = before["correct_counts"][key], after["correct_counts"][key]
        lines.append(f"| {title} | {b['rule']}/{b['total']} | {b['ml']}/{b['total']} | {a['rule']}/{a['total']} | {a['ml']}/{a['total']} |")
    for title, data in (("Original dataset before additions", before["training_rows"]),
                        ("Expanded dataset after additions", after["training_rows"]),
                        ("Unseen probes before additions", before["probe_rows"]),
                        ("Same unseen probes after additions", after["probe_rows"])):
        lines.extend(["", "## " + title, "", table(data)])
    lines.extend(["", "## Failure walkthrough", "", results["chosen_failure_explanation"],
                  "", "## Model and data inspection", "",
                  "CountVectorizer uses lowercase unigram word counts; the default token pattern excludes single-character tokens and emojis. LogisticRegression learns weights from the labeled examples. The script fits and evaluates on identical posts for its dataset score.",
                  "", "Before class counts: " + str(before["label_counts"]),
                  "After class counts: " + str(after["label_counts"]),
                  f"Vocabulary size: {before['vocabulary_size']} before; {after['vocabulary_size']} after.",
                  f"Python {results['python']}; scikit-learn {results['sklearn']}.",
                  "", "Raw results, including actual ML token contributions for the walkthrough sentence, are in part4_results.json."])
    Path("part4_measured_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
