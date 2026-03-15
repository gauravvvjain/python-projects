"""
PageRank Algorithm Implementation

Complexity Analysis:
- Time: O(I * (V + E)) where I is number of iterations, V is vertices, E is edges
- Space: O(V) for storing the scores

Usage:
graph = {'A': ['B', 'C'], 'B': ['C'], 'C': ['A']}
scores = compute_pagerank(graph)
"""

def compute_pagerank(graph, damping_factor=0.85, max_iterations=100, tolerance=1.0e-6):
    """
    Computes the PageRank of nodes in a directed graph.
    graph: dict mapping node -> list of outgoing nodes
    """
    nodes = set(graph.keys())
    for deps in graph.values():
        nodes.update(deps)

    if not nodes:
        return {}

    N = len(nodes)
    # Initialize all nodes with 1/N
    pagerank = {node: 1.0 / N for node in nodes}
    
    # Pre-calculate out-degrees. Dangling nodes act as if they point to all nodes
    out_degree = {node: len(graph.get(node, [])) for node in nodes}

    for i in range(max_iterations):
        new_pagerank = {node: 0.0 for node in nodes}
        dangling_sum = sum(pagerank[node] for node in nodes if out_degree[node] == 0)

        for node in nodes:
            # Base rank from damping
            new_pagerank[node] = (1.0 - damping_factor) / N
            # Add rank from dangling nodes distributed evenly
            new_pagerank[node] += damping_factor * (dangling_sum / N)
            
        # Add incoming rank values
        for src, dests in graph.items():
            if out_degree[src] > 0:
                rank_to_share = pagerank[src] / out_degree[src]
                for dest in dests:
                    new_pagerank[dest] += damping_factor * rank_to_share

        # Check convergence
        diff = sum(abs(new_pagerank[node] - pagerank[node]) for node in nodes)
        pagerank = new_pagerank

        if diff < tolerance:
            break

    return pagerank

if __name__ == "__main__":
    g = {
        'PageA': ['PageB', 'PageC'],
        'PageB': ['PageC'],
        'PageC': ['PageA'],
        'PageD': ['PageC']
    }
    ranks = compute_pagerank(g)
    for k, v in sorted(ranks.items(), key=lambda x: x[1], reverse=True):
        print(f"{k}: {v:.4f}")
