"""
Search Query Engine
Accepts queries, tokenizes, fetches candidate documents, ranks results.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from indexer.builder import IndexBuilder
from ranking.ranker import Ranker
from parser.html_parser import parse_document, simple_stem, STOP_WORDS, tokenize
from data_structures.lru_cache import LRUCache

class SearchEngine:
    def __init__(self, index_builder: IndexBuilder, ranker: Ranker, cache_size=100):
        self.index_builder = index_builder
        self.ranker = ranker
        self.cache = LRUCache(cache_size)

    def _parse_query(self, query: str) -> list:
        tokens = tokenize(query)
        processed = [simple_stem(t) for t in tokens if t not in STOP_WORDS]
        return processed

    def search(self, query: str, top_k: int = 10) -> list:
        # Check cache first
        cached_result = self.cache.get(query)
        if cached_result != -1:
            return cached_result

        query_tokens = self._parse_query(query)
        if not query_tokens:
            return []

        # Find candidate documents (using AND logic first)
        candidates = set()
        for i, token in enumerate(query_tokens):
            docs = self.index_builder.search(token)
            if i == 0:
                candidates = set(docs)
            else:
                candidates = candidates.intersection(docs)
                
        # Fallback to OR logic if AND results in no candidates
        if not candidates:
            for token in query_tokens:
                 candidates.update(self.index_builder.search(token))

        if not candidates:
            return []

        # Rank candidates
        ranked_results = self.ranker.rank_results(query_tokens, candidates)
        
        # Take top K doc IDs and their scores
        top_results = [{"url": doc_id, "score": score} for doc_id, score in ranked_results[:top_k]]
        
        # Save to cache
        self.cache.put(query, top_results)
        
        return top_results
