"""
Dijkstra's Shortest Path Algorithm

Complexity Analysis:
- Time: O((V + E) * log V) where V is vertices, E is edges
- Space: O(V) for distances and Priority Queue

Usage:
graph = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2)], 'C': []}
print(dijkstra(graph, 'A'))
"""

import sys
import os

# Import Priority Queue from data_structures folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_structures.priority_queue import PriorityQueue

def dijkstra(graph: dict, start_node):
    """
    Computes shortest paths from start_node to all other reachable nodes.
    graph: dict mapping node -> list of (neighbor, weight) tuples
    Returns dict mapping node -> shortest distance
    """
    distances = {start_node: 0.0}
    pq = PriorityQueue()
    pq.push(start_node, 0.0)
    
    visited = set()

    while not pq.is_empty():
        current_node = pq.pop()
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        current_dist = distances[current_node]
        
        for neighbor, weight in graph.get(current_node, []):
            if neighbor in visited:
                continue
                
            new_dist = current_dist + weight
            
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                pq.push(neighbor, new_dist)
                
    return distances

if __name__ == "__main__":
    g = {
        'A': [('B', 1.0), ('C', 4.0)],
        'B': [('C', 2.0), ('D', 6.0)],
        'C': [('D', 3.0)],
        'D': []
    }
    print("Distances from A:", dijkstra(g, 'A'))
