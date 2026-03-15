"""
Graph Implementation
"""
from collections import deque

class Graph:
    """
    An adjacency list based Graph implementation.
    Supports directed and undirected graphs.
    Useful for resolving dependencies or calculating paths.
    """
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.
        Time Complexity: O(1)
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, u, v, weight=1):
        """
        Adds an edge between vertex u and v.
        Time Complexity: O(1)
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Only add the edge if it doesn't already exist to avoid multi-graphs if unwanted
        # For simplicity, we just append here.
        self.adj_list[u].append((v, weight))
        
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def bfs(self, start_vertex):
        """
        Performs Breadth-First Search starting from a vertex.
        Time Complexity: O(V + E)
        Returns a list of visited vertices in BFS order.
        """
        if start_vertex not in self.adj_list:
            return []
            
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        visited.add(start_vertex)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.adj_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return result

    def dfs(self, start_vertex):
        """
        Performs Depth-First Search iteratively.
        Time Complexity: O(V + E)
        """
        if start_vertex not in self.adj_list:
            return []
            
        visited = set()
        stack = [start_vertex]
        result = []
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Push neighbors to stack (reverse order to visit in insertion order if desired, 
                # but standard ordering is fine)
                for neighbor, _ in reversed(self.adj_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        
        return result

    def has_cycle(self):
        """
        Detects if there is a cycle in the graph.
        Useful for dependency resolution.
        """
        visited = set()
        rec_stack = set()
        
        def dfs_cycle(v):
            visited.add(v)
            rec_stack.add(v)
            
            for neighbor, _ in self.adj_list.get(v, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # If undirected, need to ensure neighbor is not the parent.
                    # This simple impl is mostly for directed graphs.
                    return True
                    
            rec_stack.remove(v)
            return False

        if not self.directed:
            # Undirected cycle detection
            def dfs_cycle_undirected(v, parent):
                visited.add(v)
                for neighbor, _ in self.adj_list.get(v, []):
                    if neighbor not in visited:
                        if dfs_cycle_undirected(neighbor, v):
                            return True
                    elif neighbor != parent:
                        return True
                return False

            for vertex in self.adj_list:
                if vertex not in visited:
                    if dfs_cycle_undirected(vertex, None):
                        return True
            return False

        # Directed cycle detection
        for vertex in self.adj_list:
            if vertex not in visited:
                if dfs_cycle(vertex):
                    return True
        return False
