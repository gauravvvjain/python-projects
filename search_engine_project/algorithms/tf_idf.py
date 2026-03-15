"""
TF-IDF Algorithm Implementation

Complexity Analysis:
- Time: O(N * W) where N is number of documents and W is avg words per document
- Space: O(V) where V is vocabulary size (vocab dictionary)

Usage:
docs = {"doc1": ["hello", "world"], "doc2": ["hello", "search"]}
tfidf = TFIDF()
tfidf.fit(docs)
print(tfidf.get_score("hello", "doc1"))
"""

import math
from collections import Counter

class TFIDF:
    def __init__(self):
        self.doc_freqs = Counter() # word -> number of docs containing word
        self.doc_lengths = {}      # doc_id -> number of words in doc
        self.term_freqs = {}       # doc_id -> {word -> count}
        self.total_docs = 0

    def fit(self, documents: dict):
        """
        Fits the TF-IDF model to a corpus of documents.
        documents is a dict mapping doc_id -> list of tokens.
        """
        self.total_docs = len(documents)
        for doc_id, words in documents.items():
            self.doc_lengths[doc_id] = len(words)
            counts = Counter(words)
            self.term_freqs[doc_id] = counts
            for word in counts.keys():
                self.doc_freqs[word] += 1

    def compute_tf(self, word: str, doc_id: str) -> float:
        """Computes Term Frequency."""
        if doc_id not in self.term_freqs:
            return 0.0
        count = self.term_freqs[doc_id].get(word, 0)
        total_words = self.doc_lengths[doc_id]
        if total_words == 0:
            return 0.0
        return count / total_words

    def compute_idf(self, word: str) -> float:
        """Computes Inverse Document Frequency."""
        df = self.doc_freqs.get(word, 0)
        if df == 0:
            return 0.0
        # +1 smoothing to avoid division by zero
        return math.log((self.total_docs + 1) / (df + 1)) + 1.0

    def get_score(self, word: str, doc_id: str) -> float:
        """Computes TF-IDF score for a word in a specific document."""
        return self.compute_tf(word, doc_id) * self.compute_idf(word)

if __name__ == "__main__":
    docs = {
        "doc1": ["the", "quick", "brown", "fox"],
        "doc2": ["the", "lazy", "dog", "barks"],
        "doc3": ["the", "fox", "barks"]
    }
    model = TFIDF()
    model.fit(docs)
    print("TF-IDF for 'fox' in doc1:", model.get_score("fox", "doc1"))
    print("TF-IDF for 'fox' in doc2:", model.get_score("fox", "doc2"))
    print("TF-IDF for 'the' in doc1:", model.get_score("the", "doc1"))
