"""
Breadth First Search (BFS) and Depth First Search (DFS)

Complexity Analysis (for both):
- Time: O(V + E) where V is vertices, E is edges
- Space: O(V) for visited set and queue/stack

Usage:
graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
print(bfs(graph, 'A'))
"""

from collections import deque

def bfs(graph: dict, start_node):
    """Performs Breadth First Search and returns visited nodes in order."""
    visited = []
    queue = deque([start_node])
    visited_set = {start_node}
    
    while queue:
        node = queue.popleft()
        visited.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)
                
    return visited

def dfs(graph: dict, start_node):
    """Performs Depth First Search and returns visited nodes in order."""
    visited = []
    visited_set = set()
    
    def _dfs_recursive(node):
        visited_set.add(node)
        visited.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited_set:
                _dfs_recursive(neighbor)
                
    _dfs_recursive(start_node)
    return visited

if __name__ == "__main__":
    g = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    print("BFS:", bfs(g, 'A'))
    print("DFS:", dfs(g, 'A'))
