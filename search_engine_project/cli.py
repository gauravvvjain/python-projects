"""
CLI Interface for the Search Engine Core Components
"""

import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler.crawler import WebCrawler
from parser.html_parser import parse_document
from indexer.builder import IndexBuilder
from ranking.ranker import Ranker
from search.engine import SearchEngine

def main():
    parser = argparse.ArgumentParser(description="Distributed Search Engine CLI")
    parser.add_argument("--crawl", type=str, help="Seed URL to crawl")
    parser.add_argument("--max_pages", type=int, default=5, help="Max pages to crawl")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--build_index", action="store_true", help="Build and rank index after crawling")
    
    args = parser.parse_args()
    
    builder = IndexBuilder("cli_index.json")
    ranker = Ranker()

    crawled_data = {}
    if args.crawl:
        print(f"Starting crawl at {args.crawl} for {args.max_pages} pages...")
        crawler = WebCrawler(max_pages=args.max_pages)
        crawler.add_seed(args.crawl)
        crawled_data = crawler.crawl()
        print(f"Crawled {len(crawled_data)} pages.")
        
    if args.build_index and crawled_data:
        print("Building index and parsing documents...")
        parsed_docs = {}
        for url, html in crawled_data.items():
            tokens = parse_document(html)
            builder.add_document(url, tokens)
            parsed_docs[url] = tokens
            
        builder.save()
        print("Index saved to disk.")
        
        print("Building Ranker graph and TF-IDF...")
        crawler = WebCrawler()
        ranker.build_graph(crawled_data, crawler.extract_links)
        ranker.fit_tfidf(parsed_docs)
        print("Ranker ready.")
        
    if args.search:
        # Load index if not just built
        if not args.build_index:
            builder.load()
        engine = SearchEngine(builder, ranker)
        print(f"\nSearching for: '{args.search}'")
        results = engine.search(args.search)
        if results:
            for i, res in enumerate(results, 1):
                if isinstance(res, dict):
                    print(f"{i}. {res['url']} (Score: {res['score']:.4f})")
                else:
                    print(f"{i}. {res}")
        else:
            print("No results found.")

if __name__ == "__main__":
    main()
