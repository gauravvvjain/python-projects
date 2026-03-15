"""
LRU Cache Implementation using Hash Map and Doubly Linked List

Complexity Analysis:
- get: O(1)
- put: O(1)
- Space: O(capacity)

Usage:
cache = LRUCache(2)
cache.put(1, "A")
cache.put(2, "B")
print(cache.get(1)) # "A"
cache.put(3, "C") # evicts 2
print(cache.get(2)) # -1
"""

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        
        # Dummy head and tail
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        """Add a node right after the head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Get the value of the key if it exists, otherwise return -1."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key, value):
        """Update the value of the key if it exists, otherwise add the key-value pair."""
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add_to_front(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            # Evict the least recently used item
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put("doc1", "content1")
    lru.put("doc2", "content2")
    print("get doc1:", lru.get("doc1"))
    lru.put("doc3", "content3")
    print("get doc2 (evicted):", lru.get("doc2")) # -1 due to eviction
