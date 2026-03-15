"""
End to end pipeline tests
"""
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler.crawler import WebCrawler
from parser.html_parser import parse_document
from indexer.builder import IndexBuilder
from ranking.ranker import Ranker
from search.engine import SearchEngine

def test_full_pipeline(tmp_path):
    index_file = tmp_path / "test_index.json"
    
    # 1. Mock Crawled Data
    crawled_data = {
        "http://example.com/page1": "<html><body><h1>Search Engine</h1><p>Distributed search engine</p></body></html>",
        "http://example.com/page2": "<html><body><h1>Indexing</h1><p>Engine builds inverted index</p><a href='http://example.com/page1'>link</a></body></html>"
    }
    
    # 2. Parse Documents and Build Index
    builder = IndexBuilder(str(index_file))
    parsed_docs = {}
    for url, html in crawled_data.items():
        tokens = parse_document(html)
        builder.add_document(url, tokens)
        parsed_docs[url] = tokens
    builder.save()
    
    # 3. Build Ranker
    crawler = WebCrawler()
    ranker = Ranker()
    ranker.build_graph(crawled_data, crawler.extract_links)
    ranker.fit_tfidf(parsed_docs)
    
    # 4. Search
    engine = SearchEngine(builder, ranker)
    results = engine.search("engine")
    
    # Assertions
    assert len(results) > 0
    # Both pages have "engine" (actually "engin" due to stemming), let's check parsing output
    # Stemmer converts "engine" to "engin" but the query is also stemmed to "engin"
    urls = [res["url"] for res in results]
    assert "http://example.com/page1" in urls
    assert "http://example.com/page2" in urls
