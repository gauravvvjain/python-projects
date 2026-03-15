"""
Union Find (Disjoint Set) Implementation
"""

class UnionFind:
    """
    Disjoint Set / Union Find data structure with path compression and union by rank.
    Useful for finding connected components, like tracking equivalence classes of test cases.
    """
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.count = size

    def find(self, p: int) -> int:
        """
        Finds the root of the set containing element p.
        Applies path compression for amortized O(alpha(N)) time.
        """
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p: int, q: int) -> bool:
        """
        Unions the sets containing p and q.
        Uses union by rank for balanced trees.
        Returns True if a merge happened, False if already in the same set.
        Time Complexity: Amortized O(alpha(N))
        """
        root_p = self.find(p)
        root_q = self.find(q)

        if root_p == root_q:
            return False  # Already connected

        # Union by rank
        if self.rank[root_p] > self.rank[root_q]:
            self.parent[root_q] = root_p
        elif self.rank[root_p] < self.rank[root_q]:
            self.parent[root_p] = root_q
        else:
            self.parent[root_q] = root_p
            self.rank[root_p] += 1
            
        self.count -= 1
        return True

    def connected(self, p: int, q: int) -> bool:
        """
        Checks if p and q are in the same set.
        """
        return self.find(p) == self.find(q)

    def get_count(self) -> int:
        """
        Returns the number of disjoint sets.
        """
        return self.count
