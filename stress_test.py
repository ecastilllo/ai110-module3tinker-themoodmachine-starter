"""Part 3: run breakers and compare language styles. Run: python -X utf8 stress_test.py"""
from dataset import SAMPLE_POSTS, TRUE_LABELS
from mood_analyzer import MoodAnalyzer

# Intended labels are interpretations for this exercise, not universal truths.
BREAKERS = [
    ("sarcasm", "I love getting stuck in traffic", "negative"),
    ("slang", "That concert was sick", "positive"),
    ("ambiguous slang", "I feel sick today", "negative"),
    ("slang", "That concert was fire", "positive"),
    ("emoji", "I'm fine 🙃", "negative"),
    ("mixed emotions", "I'm exhausted but proud of myself", "mixed"),
    ("negation with modifier", "I'm not very happy about this", "negative"),
    ("negation with modifier", "The exam was not really bad", "positive"),
    ("mixed signals", "I'm happy but sad", "mixed"),
]
STYLE_PAIRS = [
    ("standard / slang", "That concert was amazing", "That concert was fire", "positive"),
    ("standard / informal spelling", "I'm so happy", "I'm soooo happyyy", "positive"),
    ("standard / regional expression", "I'm excited about this", "I'm well chuffed about this", "positive"),
    ("direct / softened negation", "I'm not happy", "I'm not very happy", "negative"),
]

def main():
    model = MoodAnalyzer()
    correct = 0
    print("=== Breaker sentences ===")
    for category, text, intended in BREAKERS:
        predicted = model.predict_label(text)
        correct += predicted == intended
        ignored = [
            token for token in model.preprocess(text)
            if token not in model.positive_words and token not in model.negative_words
        ]
        print(f"{category}: {text!r}; intended={intended}; predicted={predicted}")
        print(model.explain(text))
        print(f"Tokens with no direct vocabulary match: {ignored}")
    print(f"Breaker accuracy: {correct}/{len(BREAKERS)}")
    print("\n=== Language style comparisons ===")
    for category, standard, alternative, intended in STYLE_PAIRS:
        print(f"{category}; intended={intended}")
        for text in (standard, alternative):
            print(f"{text!r}: {model.explain(text)}")
    print("\n=== Dataset regression check ===")
    correct = sum(model.predict_label(text) == label for text, label in zip(SAMPLE_POSTS, TRUE_LABELS))
    print(f"Dataset accuracy: {correct}/{len(SAMPLE_POSTS)}")
    print("Dataset predictions:", [model.predict_label(text) for text in SAMPLE_POSTS])

if __name__ == "__main__":
    main()
