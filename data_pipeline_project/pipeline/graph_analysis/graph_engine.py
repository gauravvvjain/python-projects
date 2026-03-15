import pandas as pd
import networkx as nx
import numpy as np
from pipeline.utils.file_utils import setup_logger

logger = setup_logger('graph_engine')

class GraphEngine:
    def __init__(self, correlation_matrix: pd.DataFrame, threshold: float = 0.5):
        self.correlation_matrix = correlation_matrix
        self.threshold = threshold
        self.graph = nx.Graph()

    def build_correlation_graph(self) -> nx.Graph:
        """
        Build a graph where nodes are dataset columns, and edges exist
        if the absolute correlation strength between them is above a threshold.
        """
        if self.correlation_matrix.empty:
            logger.warning("Empty correlation matrix provided. Cannot build graph.")
            return self.graph

        columns = self.correlation_matrix.columns
        self.graph.add_nodes_from(columns)

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                col1 = columns[i]
                col2 = columns[j]
                corr_val = self.correlation_matrix.loc[col1, col2]
                
                if pd.notna(corr_val) and abs(corr_val) >= self.threshold:
                    self.graph.add_edge(col1, col2, weight=abs(corr_val), correlation=corr_val)

        logger.info(f"Built correlation graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges using threshold {self.threshold}.")
        return self.graph

    def run_bfs(self, start_node: str) -> list:
        """Run Breadth First Search starting from a given node."""
        if start_node not in self.graph:
            logger.error(f"Node '{start_node}' not found in the graph.")
            return []
            
        bfs_edges = list(nx.bfs_edges(self.graph, source=start_node))
        bfs_nodes = [start_node] + [v for u, v in bfs_edges]
        logger.info(f"BFS traversal from '{start_node}': {bfs_nodes}")
        return bfs_nodes

    def run_dfs(self, start_node: str) -> list:
        """Run Depth First Search starting from a given node."""
        if start_node not in self.graph:
            logger.error(f"Node '{start_node}' not found in the graph.")
            return []
            
        dfs_edges = list(nx.dfs_edges(self.graph, source=start_node))
        dfs_nodes = [start_node] + [v for u, v in dfs_edges]
        logger.info(f"DFS traversal from '{start_node}': {dfs_nodes}")
        return dfs_nodes

    def run_graph_pipeline(self) -> dict:
        """
        Execute the graph building and traversals.
        Returns a summary of the graph properties and traversals.
        """
        self.build_correlation_graph()
        
        traversals = {}
        if self.graph.number_of_nodes() > 0:
            start_node = list(self.graph.nodes())[0]
            traversals['bfs'] = self.run_bfs(start_node)
            traversals['dfs'] = self.run_dfs(start_node)

        results = {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'traversals': traversals
        }
        
        return results
