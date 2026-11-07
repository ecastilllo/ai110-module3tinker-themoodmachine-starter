"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey excited that I finally got this code working 😂",
    "No cap, this week has been awful",
    "Got the internship! Still stressed about moving away 🥲",
    "I absolutely love getting stuck in traffic 🙄",
    "Submitted the assignment and closed my laptop",
    "That exam was not bad at all",
    "Great, my laptop crashed right before I could save",
    "I'm happy for you, but sad that you're leaving",
    "Just sitting here waiting for the next class",
    "Pizza with my friends after a long day = best night 😊",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # Lowkey excited that I finally got this code working 😂
    "negative",  # No cap, this week has been awful
    "mixed",  # Got the internship! Still stressed about moving away 🥲
    "negative",  # I absolutely love getting stuck in traffic 🙄
    "neutral",  # Submitted the assignment and closed my laptop
    "positive",  # That exam was not bad at all
    "negative",  # Great, my laptop crashed right before I could save
    "mixed",  # I'm happy for you, but sad that you're leaving
    "neutral",  # Just sitting here waiting for the next class
    "positive",  # Pizza with my friends after a long day = best night 😊
]

# Each post has exactly one label at the same index in TRUE_LABELS.
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), "Each post needs a matching label."
