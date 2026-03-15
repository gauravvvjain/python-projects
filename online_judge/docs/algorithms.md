# Algorithms & Data Structures

We implemented several data structures from scratch in the `data_structures` module.

### 1. MinHeap / MaxHeap
**Usage:** Used internally by the Ranking Engine to compute the real-time leaderboard.
**Complexity:** `O(N log K)` for maintaining Top-K scores. `O(log N)` for insert/pop.
**Implementation details:** Uses a flat list. Calculates parents via `(idx - 1) // 2`. Includes `sift_up` and `sift_down`.

### 2. Trie (Prefix Tree)
**Usage:** Fast multi-string pattern matching, could be used for advanced AST code analysis or autocomplete on the frontend.
**Complexity:** `O(M)` insert and search, where M is string length.

### 3. Segment Tree
**Usage:** Could be used for analyzing performance timelines over ranges (e.g. tracking min/max memory usage over N intervals).
**Complexity:** `O(log N)` for queries and updates.

### 4. Union Find
**Usage:** Finds equivalence classes. Can be used for problem clustering or identifying plagiarism.
**Complexity:** Amortized `O(alpha(N))` via path compression and union by rank.

### 5. Graph (BFS / DFS)
**Usage:** Validating dependencies or problem prerequisite trees (e.g., LeetCode course schedules).
**Complexity:** `O(V + E)` for traversals. Cycle detection is critical for dependency resolution.

### 6. Hash Table
**Usage:** Key-Value storage with linear chaining for resolving collisions. Automatically resizes when load factor > 0.75.
**Complexity:** `O(1)` average time for insert/delete/get.
