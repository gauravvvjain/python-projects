# Distributed Search Engine

A scalable, modular distributed search engine written from scratch in Python. It includes custom implementations of core data structures, algorithms (PageRank, TF-IDF), and a distributed crawling and indexing pipeline.

## Structure
- `data_structures/`: Core data structures (Trie, Inverted Index, Bloom Filter, LRU Cache, Graph, Hash Table, Priority Queue).
- `algorithms/`: PageRank, TF-IDF, graph traversals, topological sort, Dijkstra.
- `crawler/`: Web crawler module with Redis queue integration.
- `parser/`: HTML and text processing.
- `indexer/`: Index builder.
- `ranking/`: Document ranking combining PageRank and TF-IDF.
- `search/`: Search engine querying logic.
- `api/`: FastAPI web server.
- `workers/`: Distributed worker nodes.

## Running Tests
```bash
pytest
```
