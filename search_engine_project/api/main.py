"""
FastAPI Server
"""

import sys
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from rq.job import Job

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler.crawler import WebCrawler
from parser.html_parser import parse_document
from indexer.builder import IndexBuilder
from ranking.ranker import Ranker
from search.engine import SearchEngine
from workers.tasks import run_crawl_job, run_index_job

app = FastAPI(title="Distributed Search Engine API")

# Setup Redis connection (will gracefully fallback if not running locally)
try:
    redis_conn = Redis(host='localhost', port=6379)
    q = Queue(connection=redis_conn)
except Exception:
    q = None

# Initialize local components
builder = IndexBuilder("global_index.json")
builder.load()
ranker = Ranker()
search_engine = SearchEngine(builder, ranker)

class CrawlRequest(BaseModel):
    url: str
    max_pages: int = 10

@app.post("/crawl")
def crawl_endpoint(req: CrawlRequest):
    if q is None:
        raise HTTPException(status_code=500, detail="Redis queue not configured or Redis is down.")
    job = q.enqueue(run_crawl_job, req.url, req.max_pages)
    return {"message": "Crawl job enqueued", "job_id": job.id}

@app.post("/index")
def index_endpoint(job_id: str):
    """Takes a completed crawl job ID and indexes its results."""
    if q is None:
        raise HTTPException(status_code=500, detail="Redis queue not configured or Redis is down.")
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        if job.is_finished:
            crawled_data = job.result
            index_job = q.enqueue(run_index_job, crawled_data, "global_index.json")
            return {"message": "Index job enqueued", "index_job_id": index_job.id}
        else:
            return {"message": "Crawl job not finished yet", "status": job.get_status()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/refresh_search_engine")
def refresh_engine():
    """Reloads index from disk and clears cache."""
    builder.load()
    search_engine.cache.cache.clear()
    return {"message": "Search engine refreshed with latest index"}

@app.get("/search")
def search_endpoint(q: str):
    results = search_engine.search(q, top_k=10)
    return {"query": q, "results": results}

@app.get("/stats")
def stats_endpoint():
    return {
        "index_size": len(builder.index.index),
        "cached_queries": len(search_engine.cache.cache)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
