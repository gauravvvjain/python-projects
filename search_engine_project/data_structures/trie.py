"""
Trie (Prefix Tree) Implementation

Complexity Analysis:
- Insert: O(L) where L is string length
- Search: O(L)
- Starts With: O(L)
- Space: O(N * L) where N is number of strings, L is avg length

Usage:
t = Trie()
t.insert("apple")
print(t.search("apple"))
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns True if word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the trie that starts with prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

if __name__ == "__main__":
    t = Trie()
    t.insert("indexing")
    t.insert("index")
    print("Search 'index':", t.search("index")) # True
    print("Search 'ind':", t.search("ind")) # False
    print("Starts with 'ind':", t.starts_with("ind")) # True
