"""
Graph Implementation (Adjacency List)

Complexity Analysis:
- Add Node: O(1)
- Add Edge: O(1)
- Neighbours: O(1)
- Space: O(V + E) where V is vertices, E is edges

Usage:
g = Graph()
g.add_edge("A", "B", 1.5)
print(g.get_neighbors("A"))
"""

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.nodes = set()

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.nodes.add(node)

    def add_edge(self, src, dest, weight=1.0):
        self.add_node(src)
        self.add_node(dest)
        self.adj_list[src].append((dest, weight))

    def get_neighbors(self, node):
        """Returns list of tuples: [(neighbor, weight), ...]"""
        return self.adj_list.get(node, [])
        
    def get_nodes(self):
        return list(self.nodes)

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B", 1.5)
    g.add_edge("A", "C", 2.0)
    print("Nodes:", g.get_nodes())
    print("Neighbors of A:", g.get_neighbors("A"))
