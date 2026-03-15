"""
Index Builder
Populates the Inverted Index and handles disk persistence.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_structures.inverted_index import InvertedIndex

class IndexBuilder:
    def __init__(self, index_file="index.json"):
        self.index = InvertedIndex()
        self.index_file = index_file
        
    def load(self):
        """Loads index from disk if it exists."""
        if os.path.exists(self.index_file):
            self.index.load_from_disk(self.index_file)
            
    def save(self):
        """Saves current index state to disk."""
        self.index.save_to_disk(self.index_file)

    def add_document(self, doc_id: str, words: list):
        """Adds a document's token list to the index."""
        self.index.add_document(doc_id, words)

    def search(self, word: str) -> set:
        """Returns the set of document IDs containing the given word."""
        return self.index.search(word)

if __name__ == "__main__":
    builder = IndexBuilder("test_builder.json")
    builder.add_document("doc1", ["distribut", "search", "engin"])
    builder.save()
    print("Search 'search':", builder.search("search"))
    if os.path.exists("test_builder.json"):
        os.remove("test_builder.json")
