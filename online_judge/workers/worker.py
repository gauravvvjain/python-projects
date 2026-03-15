import sys
import os
from rq import Worker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from queue.connection import redis_conn, high_queue, default_queue, low_queue

def run_worker():
    """
    Start an RQ worker process.
    """
    print("Starting Worker Node...")
    # Listen to queues in order of priority
    queues = [high_queue, default_queue, low_queue]
    
    worker = Worker(queues, connection=redis_conn)
    worker.work(with_scheduler=True)

if __name__ == '__main__':
    run_worker()
