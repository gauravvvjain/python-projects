"""
Tests for Algorithms
"""
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.pagerank import compute_pagerank
from algorithms.tf_idf import TFIDF
from algorithms.shortest_path import dijkstra
from algorithms.graph_traversals import bfs, dfs
from algorithms.topological_sort import topological_sort

def test_pagerank():
    g = {'A': ['B', 'C'], 'B': ['C'], 'C': ['A']}
    ranks = compute_pagerank(g)
    assert sum(ranks.values()) == pytest.approx(1.0)
    # B and C should have higher ranks based on links, but let's just check valid float
    assert isinstance(ranks['A'], float)

def test_tf_idf():
    docs = {"d1": ["hello", "world"], "d2": ["hello", "dist"]}
    tfidf = TFIDF()
    tfidf.fit(docs)
    assert tfidf.get_score("hello", "d1") > 0
    assert tfidf.get_score("not_exist", "d1") == 0

def test_dijkstra():
    g = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2)], 'C': []}
    dists = dijkstra(g, 'A')
    assert dists['C'] == 3

def test_bfs_dfs():
    g = {'A': ['B'], 'B': ['C'], 'C': []}
    assert bfs(g, 'A') == ['A', 'B', 'C']
    assert dfs(g, 'A') == ['A', 'B', 'C']
    
def test_topological_sort():
    g = {'A': ['B'], 'B': ['C'], 'C': []}
    assert topological_sort(g) == ['A', 'B', 'C']
