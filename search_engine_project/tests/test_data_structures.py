"""
Tests for Data Structures
"""
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_structures.priority_queue import PriorityQueue
from data_structures.bloom_filter import BloomFilter
from data_structures.trie import Trie
from data_structures.lru_cache import LRUCache
from data_structures.inverted_index import InvertedIndex

def test_priority_queue():
    pq = PriorityQueue()
    pq.push("task1", 5)
    pq.push("task2", 1)
    pq.push("task3", 3)
    assert pq.pop() == "task2"
    assert pq.pop() == "task3"
    assert pq.pop() == "task1"
    assert pq.is_empty()

def test_bloom_filter():
    bf = BloomFilter(size=1000, hash_count=3)
    bf.add("test_url")
    assert "test_url" in bf

def test_trie():
    t = Trie()
    t.insert("indexing")
    assert t.search("indexing") is True
    assert t.search("index") is False
    assert t.starts_with("index") is True

def test_lru_cache():
    cache = LRUCache(2)
    cache.put(1, "A")
    cache.put(2, "B")
    assert cache.get(1) == "A"
    cache.put(3, "C") # evicts 2
    assert cache.get(2) == -1
    assert cache.get(3) == "C"

def test_inverted_index():
    idx = InvertedIndex()
    idx.add_document("doc1", ["query", "test"])
    assert "doc1" in idx.search("query")
    assert "doc1" not in idx.search("missing")
