"""
Bloom Filter Implementation

Complexity Analysis:
- Insert: O(k) where k is the number of hash functions
- Lookup: O(k)
- Space: O(m) where m is the size of the bit array

Usage:
bf = BloomFilter(size=1000, hash_count=3)
bf.add("google.com")
print("google.com" in bf) # True
"""

import hashlib
from typing import List

class BloomFilter:
    def __init__(self, size: int = 100000, hash_count: int = 5):
        self.size = size
        self.hash_count = hash_count
        # Simple boolean list for bit array
        self.bit_array: List[bool] = [False] * size

    def _hashes(self, item: str) -> List[int]:
        # Generate varied hashes using hashlib md5 and salting
        hashes = []
        for i in range(self.hash_count):
            h = int(hashlib.md5((str(i) + item).encode('utf-8')).hexdigest(), 16)
            hashes.append(h % self.size)
        return hashes

    def add(self, item: str):
        """Adds an item to the Bloom filter."""
        for h in self._hashes(item):
            self.bit_array[h] = True

    def __contains__(self, item: str) -> bool:
        """Checks if an item might be in the Bloom filter."""
        for h in self._hashes(item):
            if not self.bit_array[h]:
                return False
        return True

if __name__ == "__main__":
    bf = BloomFilter(size=100, hash_count=3)
    bf.add("https://example.com")
    print("Contains example.com:", "https://example.com" in bf) # True
    print("Contains google.com:", "https://google.com" in bf) # False (likely)
