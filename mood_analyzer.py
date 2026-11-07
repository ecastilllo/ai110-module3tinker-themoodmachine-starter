"""Rule based mood analyzer with punctuation cleanup and simple negation."""

import re
from typing import List, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """Count known mood words, then convert their total into a label."""

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    def preprocess(self, text: str) -> List[str]:
        """Lowercase and separate words, contractions, emojis and punctuation.

        Keeping punctuation as separate tokens lets "happy!" match "happy"
        without letting negation cross a sentence boundary. Emojis are retained
        for inspection but do not receive scores in this version.
        """
        cleaned = text.strip().lower().replace("\u2019", "'")
        return re.findall(r"[\w]+(?:'[\w]+)*|[^\w\s]", cleaned)

    def _word_signals(self, text: str) -> List[Tuple[str, int]]:
        """Return each matched word and its signed contribution.

        Enhancement: not/no/never or an n't contraction reverses polarity
        directly or across one modifier (very/really/so/too). The short,
        explicit window cannot cross punctuation or conjunctions.
        Longer negation phrases and sarcasm remain limitations.
        """
        tokens = self.preprocess(text)
        signals = []
        for index, token in enumerate(tokens):
            value = int(token in self.positive_words) - int(token in self.negative_words)
            if value == 0:
                continue
            negation_index = index - 1
            # Part 3 fix: allow exactly one modifier between negation and mood.
            if negation_index >= 0 and tokens[negation_index] in {
                "very", "really", "so", "too"
            }:
                negation_index -= 1
            previous = tokens[negation_index] if negation_index >= 0 else ""
            negated = previous in {"not", "no", "never"} or previous.endswith("n't")
            if negated:
                value = -value
            phrase = " ".join(tokens[negation_index:index + 1]) if negated else token
            signals.append((phrase, value))
        return signals

    def score_text(self, text: str) -> int:
        """Add one for positive signals and subtract one for negative signals.

        Each occurrence counts. Negation is applied before summing.
        """
        return sum(value for _, value in self._word_signals(text))

    def predict_label(self, text: str) -> str:
        """Use the score's sign; balanced opposing signals mean mixed."""
        score = self.score_text(text)
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        signals = self._word_signals(text)
        if any(value > 0 for _, value in signals) and any(
            value < 0 for _, value in signals
        ):
            return "mixed"
        return "neutral"

    def explain(self, text: str) -> str:
        """Show tokens, adjusted matches, score and the resulting label."""
        signals = self._word_signals(text)
        positive_hits = [phrase for phrase, value in signals if value > 0]
        negative_hits = [phrase for phrase, value in signals if value < 0]
        return (
            f"Tokens = {self.preprocess(text)}; "
            f"positive = {positive_hits}; negative = {negative_hits}; "
            f"score = {self.score_text(text)}; label = {self.predict_label(text)}"
        )
