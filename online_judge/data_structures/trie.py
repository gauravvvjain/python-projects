"""
Trie (Prefix Tree) Implementation
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """
    A Trie (Prefix Tree) implementation.
    Useful for fast prefix matching, autocomplete, and string dictionaries.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        Time Complexity: O(M) where M is the length of the word.
        Space Complexity: O(M) in the worst case if word doesn't share prefixes.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Returns True if the word is in the trie.
        Time Complexity: O(M)
        Space Complexity: O(1)
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Returns True if there is a previously inserted word that has the prefix.
        Time Complexity: O(M)
        Space Complexity: O(1)
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
