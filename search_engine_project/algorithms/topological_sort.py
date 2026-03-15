"""
Topological Sort Algorithm

Complexity Analysis:
- Time: O(V + E) where V is vertices, E is edges
- Space: O(V) for visited set and recursion stack

Usage:
graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
print(topological_sort(graph))
"""

def topological_sort(graph: dict):
    """
    Sorts a Directed Acyclic Graph (DAG) using Post-Order DFS.
    Returns list of nodes in topological order.
    """
    visited = set()
    visiting = set() # To detect cycles
    order = []
    
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)

    def _dfs(node):
        if node in visiting:
            raise ValueError("Graph contains a cycle, cannot perform topological sort")
        if node in visited:
            return
            
        visiting.add(node)
        for neighbor in graph.get(node, []):
            _dfs(neighbor)
            
        visiting.remove(node)
        visited.add(node)
        order.append(node)

    for n in nodes:
        if n not in visited:
            _dfs(n)
            
    # The post-order DFS gives reversed topological order
    order.reverse()
    return order

if __name__ == "__main__":
    g = {
        'TaskA': ['TaskB', 'TaskC'],
        'TaskB': ['TaskD'],
        'TaskC': ['TaskD'],
        'TaskD': []
    }
    print("Topological order:", topological_sort(g))
