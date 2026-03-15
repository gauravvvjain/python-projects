"""
Priority Queue Implementation using a Min-Heap

Complexity Analysis:
- push: O(log N)
- pop: O(log N)
- peek: O(1)
- Space: O(N) where N is number of elements

Usage:
pq = PriorityQueue()
pq.push("task", 1)
print(pq.pop())
"""

class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item, priority):
        """Insert item with priority into the heap."""
        self._heap.append({"item": item, "priority": priority})
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Remove and return the item with the lowest priority."""
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        if len(self._heap) == 1:
            return self._heap.pop()["item"]
        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return root["item"]

    def peek(self):
        """Return the lowest priority item without removing it."""
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0]["item"]
        
    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        while idx > 0 and self._heap[idx]["priority"] < self._heap[parent]["priority"]:
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        size = len(self._heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < size and self._heap[left]["priority"] < self._heap[smallest]["priority"]:
                smallest = left
            if right < size and self._heap[right]["priority"] < self._heap[smallest]["priority"]:
                smallest = right

            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break
                
    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

if __name__ == "__main__":
    pq = PriorityQueue()
    pq.push("task1", 3)
    pq.push("task2", 1)
    pq.push("task3", 2)
    print("Popped:", pq.pop()) # Prints task2
    print("Popped:", pq.pop()) # Prints task3
