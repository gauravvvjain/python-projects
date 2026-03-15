"""
Hash Table Implementation
"""

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    """
    A Custom Hash Table implementation using separate chaining for collision resolution.
    Time Complexity:
        Average case: O(1) for insert, get, delete
        Worst case: O(N) if all elements hash to the same bucket
    """
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        """
        Calculates the hash for a given key.
        """
        return hash(key) % self.capacity

    def insert(self, key, value):
        """
        Inserts a key-value pair. Updates value if key already exists.
        Load factor management to maintain O(1) time complexity.
        """
        index = self._hash(key)
        head = self.buckets[index]
        
        # Check if key exists and update
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
            
        # Key not found, insert at head of the linked list
        new_node = HashNode(key, value)
        new_node.next = head
        self.buckets[index] = new_node
        self.size += 1
        
        # Resize if load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key, default=None):
        """
        Retrieves the value for a given key.
        """
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
            
        return default

    def delete(self, key):
        """
        Removes a key-value pair.
        Returns True if deleted, False if key not found.
        """
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
            
        return False

    def contains(self, key):
        """
        Checks if a key exists in the hash table.
        """
        return self.get(key) is not None

    def _resize(self):
        """
        Doubles the capacity of the hash table and rehashes all elements.
        Time Complexity: O(N) where N is the number of elements.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        for head in old_buckets:
            current = head
            while current:
                self.insert(current.key, current.value)
                current = current.next

    def __len__(self):
        return self.size
