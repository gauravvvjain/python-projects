"""
Unit Tests for Data Structures
"""
import pytest
import sys
import os

# Add the project root to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.heap import MinHeap, MaxHeap
from data_structures.trie import Trie
from data_structures.segment_tree import SegmentTree
from data_structures.union_find import UnionFind
from data_structures.graph import Graph
from data_structures.hash_table import HashTable

class TestHeap:
    def test_min_heap(self):
        heap = MinHeap()
        heap.push(5)
        heap.push(2)
        heap.push(8)
        heap.push(1)
        
        assert len(heap) == 4
        assert heap.peek() == 1
        assert heap.pop() == 1
        assert heap.pop() == 2
        assert heap.pop() == 5
        assert heap.pop() == 8
        assert len(heap) == 0

    def test_max_heap(self):
        heap = MaxHeap()
        heap.push(5)
        heap.push(2)
        heap.push(8)
        heap.push(1)
        
        assert len(heap) == 4
        assert heap.peek() == 8
        assert heap.pop() == 8
        assert heap.pop() == 5
        assert heap.pop() == 2
        assert heap.pop() == 1

class TestTrie:
    def test_trie_insert_search(self):
        trie = Trie()
        trie.insert("apple")
        assert trie.search("apple") is True
        assert trie.search("app") is False
        assert trie.starts_with("app") is True
        
        trie.insert("app")
        assert trie.search("app") is True

class TestSegmentTree:
    def test_segment_tree(self):
        arr = [1, 3, 5, 7, 9, 11]
        st = SegmentTree(arr)
        
        # Query sum(arr[1:4]) -> 3+5+7 = 15
        assert st.query(1, 3) == 15
        
        # Query sum(arr[0:5]) -> 1+3+5+7+9+11 = 36
        assert st.query(0, 5) == 36
        
        # Update arr[2] to 4
        st.update(2, 4)
        
        # Request sum(arr[1:4]) -> 3+4+7 = 14
        assert st.query(1, 3) == 14

class TestUnionFind:
    def test_union_find(self):
        uf = UnionFind(10)
        assert uf.get_count() == 10
        
        uf.union(1, 2)
        uf.union(2, 3)
        assert uf.connected(1, 3) is True
        assert uf.connected(1, 4) is False
        assert uf.get_count() == 8

class TestGraph:
    def test_graph_bfs_dfs(self):
        g = Graph(directed=True)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        g.add_edge(2, 3)
        g.add_edge(3, 3)
        
        assert g.bfs(2) == [2, 0, 3, 1]
        
    def test_cycle_detection(self):
        g1 = Graph(directed=True)
        g1.add_edge(0, 1)
        g1.add_edge(1, 2)
        g1.add_edge(2, 0)
        assert g1.has_cycle() is True
        
        g2 = Graph(directed=False)
        g2.add_edge(0, 1)
        g2.add_edge(1, 2)
        assert g2.has_cycle() is False
        g2.add_edge(2, 0)
        assert g2.has_cycle() is True

class TestHashTable:
    def test_hash_table(self):
        ht = HashTable()
        ht.insert("key1", "value1")
        ht.insert("key2", "value2")
        
        assert ht.get("key1") == "value1"
        assert ht.get("key2") == "value2"
        assert ht.contains("key1") is True
        assert ht.get("key3") is None
        
        # Update existing
        ht.insert("key1", "new_value")
        assert ht.get("key1") == "new_value"
        
        # Delete
        assert ht.delete("key2") is True
        assert ht.contains("key2") is False
        assert ht.delete("key2") is False
        
        # Test resize
        for i in range(20):
            ht.insert(f"k{i}", f"v{i}")
            
        assert len(ht) == 21  # 20 + 1 remaining ("key1")
        assert ht.capacity > 16
        assert ht.get("k19") == "v19"
