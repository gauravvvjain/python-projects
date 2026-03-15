"""
Ranking Engine
Calculates PageRank and combines it with TF-IDF for search results.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.pagerank import compute_pagerank
from algorithms.tf_idf import TFIDF

class Ranker:
    def __init__(self):
        self.tfidf = TFIDF()
        self.pagerank_scores = {}
        self.page_graph = {}

    def build_graph(self, crawled_data: dict, crawler_extract_links_func):
        """
        Builds a directed graph from the crawled data.
        crawled_data: dict of URL -> HTML content
        """
        for url, html in crawled_data.items():
            links = crawler_extract_links_func(html, url)
            # Only keep links that are within our crawled data to form a closed graph
            valid_links = [l for l in links if l in crawled_data]
            self.page_graph[url] = valid_links

        self.pagerank_scores = compute_pagerank(self.page_graph)

    def fit_tfidf(self, parsed_documents: dict):
        """
        Fits the TF-IDF model.
        parsed_documents: dict of URL -> list of tokens
        """
        self.tfidf.fit(parsed_documents)

    def rank_results(self, query_tokens: list, candidate_docs: set, alpha: float = 0.5) -> list:
        """
        Ranks candidate documents based on combined TF-IDF and PageRank scores.
        alpha: weight for TF-IDF (1 - alpha for PageRank)
        Returns list of (doc_id, score) sorted descending.
        """
        results = []
        for doc in candidate_docs:
            tfidf_score = sum(self.tfidf.get_score(token, doc) for token in query_tokens)
            pr_score = self.pagerank_scores.get(doc, 0.0)
            
            # Combine scores
            combined_score = (alpha * tfidf_score) + ((1 - alpha) * pr_score)
            results.append((doc, combined_score))

        # Sort by highest score first
        results.sort(key=lambda x: x[1], reverse=True)
        return results
