"""
Web Crawler Module using Priority Queue and Bloom Filter
"""

import sys
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_structures.priority_queue import PriorityQueue
from data_structures.bloom_filter import BloomFilter

class WebCrawler:
    def __init__(self, max_pages=50):
        self.frontier = PriorityQueue()
        self.visited = BloomFilter(size=10000, hash_count=5)
        self.max_pages = max_pages
        self.pages_crawled = 0
        self.crawled_data = {} # doc_id (url) -> html content

    def add_seed(self, url: str, priority: int = 0):
        if url not in self.visited:
            # We use priority directly here. Min-Heap puts lowest priority value first.
            self.frontier.push(url, priority)
            self.visited.add(url)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for anchor in soup.find_all("a"):
            href = anchor.get("href")
            if href:
                full_url = urljoin(base_url, href)
                # basic normalization to ignore fragments
                full_url = full_url.split('#')[0] 
                if self.is_valid_url(full_url):
                    links.append(full_url)
        return links

    def crawl(self):
        while not self.frontier.is_empty() and self.pages_crawled < self.max_pages:
            current_url = self.frontier.pop()
            
            try:
                print(f"Crawling: {current_url}")
                # Provide a user-agent to avoid simple blocks
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; SearchEngineBot/1.0)'}
                response = requests.get(current_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    html_content = response.text
                    self.crawled_data[current_url] = html_content
                    self.pages_crawled += 1
                    
                    # Extract links and add to frontier
                    links = self.extract_links(html_content, current_url)
                    for link in links:
                        if link not in self.visited:
                            # Lower priority number => higher priority (visited sooner)
                            self.frontier.push(link, priority=self.pages_crawled)
                            self.visited.add(link)
                            
            except Exception as e:
                print(f"Failed to crawl {current_url}: {e}")

        return self.crawled_data

if __name__ == "__main__":
    crawler = WebCrawler(max_pages=2)
    crawler.add_seed("http://quotes.toscrape.com/")
    data = crawler.crawl()
    print(f"Crawled {len(data)} pages.")
