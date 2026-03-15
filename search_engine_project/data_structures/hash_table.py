"""
Hash Table Implementation (with Chaining for collision resolution)

Complexity Analysis:
- Put, Get, Remove: Average O(1), Worst Case O(N)
- Space: O(N)

Usage:
ht = HashTable()
ht.put("key1", "value1")
print(ht.get("key1"))
"""

class HashTable:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        # Array of lists to handle collisions via chaining
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        bucket_idx = self._hash(key)
        bucket = self.table[bucket_idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Update existing key
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        bucket_idx = self._hash(key)
        bucket = self.table[bucket_idx]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def remove(self, key):
        bucket_idx = self._hash(key)
        bucket = self.table[bucket_idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key):
        bucket_idx = self._hash(key)
        bucket = self.table[bucket_idx]
        for k, v in bucket:
            if k == key:
                return True
        return False

if __name__ == "__main__":
    ht = HashTable()
    ht.put("user1", "alice")
    ht.put("user2", "bob")
    print("User1:", ht.get("user1"))
    print("Has user2:", "user2" in ht)
    ht.remove("user1")
    print("Has user1 after removal:", "user1" in ht)
