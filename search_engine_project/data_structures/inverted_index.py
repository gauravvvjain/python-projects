"""
Inverted Index Data Structure

Complexity Analysis:
- Add Document: O(W) where W is number of unique words in document
- Search: O(1) for retrieving doc list
- Serialize/Deserialize: O(V + D) where V is vocabulary size and D is total doc references

Usage:
idx = InvertedIndex()
idx.add_document("doc1", ["hello", "world"])
print(idx.search("hello"))
"""

import json

class InvertedIndex:
    def __init__(self):
        # Maps word -> set of document IDs
        self.index = {}

    def add_document(self, doc_id: str, words: list):
        """Add a document and its words to the index."""
        for word in words:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(doc_id)

    def search(self, word: str) -> set:
        """Returns a set of document IDs containing the word."""
        return self.index.get(word, set())

    def save_to_disk(self, filepath: str):
        """Persists the inverted index to disk using JSON."""
        # Sets are not JSON serializable, so convert to list
        serializable = {word: list(docs) for word, docs in self.index.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable, f)

    def load_from_disk(self, filepath: str):
        """Loads the inverted index from disk."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.index = {word: set(docs) for word, docs in data.items()}

if __name__ == "__main__":
    import os
    index = InvertedIndex()
    index.add_document("doc1", ["distributed", "search", "engine"])
    index.add_document("doc2", ["search", "results", "ranking"])
    
    print("Search 'search':", index.search("search"))
    
    test_filepath = "test_index_tmp.json"
    index.save_to_disk(test_filepath)
    
    loaded_index = InvertedIndex()
    loaded_index.load_from_disk(test_filepath)
    print("Loaded Search 'search':", loaded_index.search("search"))
    
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
