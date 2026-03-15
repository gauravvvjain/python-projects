"""
Segment Tree Implementation
"""

class SegmentTree:
    """
    Segment Tree for range queries and range updates.
    Useful for querying execution timelines, memory spikes over intervals, etc.
    This implementation answers Range Sum Queries, but can be adapted for Min/Max.
    """
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, index, value):
        """
        Updates the value at the given index.
        Time Complexity: O(log N)
        """
        if self.n > 0:
            self._update(0, 0, self.n - 1, index, value)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            if start <= idx <= mid:
                self._update(left_child, start, mid, idx, val)
            else:
                self._update(right_child, mid + 1, end, idx, val)
                
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query(self, l, r):
        """
        Queries the sum in the range [l, r] inclusive.
        Time Complexity: O(log N)
        """
        if self.n == 0:
            return 0
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        # Range represented by node is completely outside the queried range
        if r < start or end < l:
            return 0
            
        # Range represented by node is completely inside the queried range
        if l <= start and end <= r:
            return self.tree[node]
            
        # Range represented by node is partially inside the queried range
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        p1 = self._query(left_child, start, mid, l, r)
        p2 = self._query(right_child, mid + 1, end, l, r)
        
        return p1 + p2
