import re
from collections import Counter

# List of religious terms to search for
religious_terms = [
    "god", "allah", "buddha", "jesus", "christ", "mosque", "church", "temple",
    "bible", "quran", "torah", "prayer", "faith", "religion", "spiritual"
]

# Sample texts (you can replace these with any text data you have)
texts = [
    "The Bible is a holy book for Christians. It contains stories of Jesus and his teachings.",
    "The Quran is the sacred text of Islam, believed to be the word of Allah.",
    "Buddhism teaches the path to enlightenment through the teachings of Buddha.",
    "Many people find solace in prayer and attend church services regularly.",
    "Religion plays a significant role in the lives of billions of people worldwide.",
    "Spiritual practices vary widely across different cultures and faiths."
]

# Function to count religious terms in a single text
def count_religious_terms(text, terms):
    text_lower = text.lower()
    term_counts = Counter()
    for term in terms:
        term_counts[term] = len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
    return term_counts

# Aggregate counts across all texts
total_counts = Counter()
for text in texts:
    total_counts += count_religious_terms(text, religious_terms)

# Print the results
print("Frequency of Religious Terms:")
for term, count in total_counts.items():
    print(f"{term}: {count}")
