"""
Distributed Worker Tasks
Defines tasks for RQ (Redis Queue) to process crawl and index jobs.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler.crawler import WebCrawler
from parser.html_parser import parse_document
from indexer.builder import IndexBuilder

def run_crawl_job(seed_url: str, max_pages: int = 10) -> dict:
    """Task to crawl starting from a seed URL."""
    crawler = WebCrawler(max_pages=max_pages)
    crawler.add_seed(seed_url)
    data = crawler.crawl()
    return data

def run_index_job(crawled_data: dict, index_file: str = "global_index.json"):
    """Task to parse and index crawled data."""
    builder = IndexBuilder(index_file)
    builder.load()
    
    parsed_docs = {}
    for url, html in crawled_data.items():
        tokens = parse_document(html)
        builder.add_document(url, tokens)
        parsed_docs[url] = tokens
        
    builder.save()
    return parsed_docs
