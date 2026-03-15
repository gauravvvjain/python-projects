"""
Heap / Priority Queue Implementation
"""

class MinHeap:
    """
    A binary Min-Heap implementation from scratch.
    Useful for job scheduling and finding the k-th smallest element.
    """
    def __init__(self):
        self.heap = []

    def push(self, val):
        """
        Inserts a new element into the heap.
        Time Complexity: O(log N)
        Space Complexity: O(1)
        """
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """
        Removes and returns the smallest element.
        Time Complexity: O(log N)
        Space Complexity: O(1)
        """
        if not self.heap:
            raise IndexError("pop from empty heap")
        
        # Swap root with last element
        self._swap(0, len(self.heap) - 1)
        min_val = self.heap.pop()
        
        # Sift down the new root
        if self.heap:
            self._sift_down(0)
            
        return min_val

    def peek(self):
        """
        Returns the smallest element without removing it.
        Time Complexity: O(1)
        """
        if not self.heap:
            return None
        return self.heap[0]

    def _sift_up(self, idx):
        parent_idx = (idx - 1) // 2
        if parent_idx >= 0 and self.heap[idx] < self.heap[parent_idx]:
            self._swap(idx, parent_idx)
            self._sift_up(parent_idx)

    def _sift_down(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
            
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
            
        if smallest != idx:
            self._swap(idx, smallest)
            self._sift_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __len__(self):
        return len(self.heap)

class MaxHeap(MinHeap):
    """
    A binary Max-Heap implementation from scratch.
    Useful for leaderboards or finding the k-th largest element.
    It builds on MinHeap by negating values, or overriding comparisons.
    For simplicity, we override the comparison in sift operations.
    """
    def _sift_up(self, idx):
        parent_idx = (idx - 1) // 2
        if parent_idx >= 0 and self.heap[idx] > self.heap[parent_idx]:
            self._swap(idx, parent_idx)
            self._sift_up(parent_idx)

    def _sift_down(self, idx):
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
            
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right
            
        if largest != idx:
            self._swap(idx, largest)
            self._sift_down(largest)
