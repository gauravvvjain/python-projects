import os
import redis
from rq import Queue

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Setup Redis connection
redis_conn = redis.from_url(REDIS_URL)

# Setup RQ Queues
# High priority for real-time evaluations
high_queue = Queue('high', connection=redis_conn)
# Default for normal submissions
default_queue = Queue('default', connection=redis_conn)
# Low for bulk re-evaluations
low_queue = Queue('low', connection=redis_conn)

def enqueue_submission(submission_id: str, problem_id: int, language: str, code: str):
    """
    Enqueues a code execution job to the Redis queue.
    """
    job = high_queue.enqueue(
        'workers.tasks.execute_submission_job',
        submission_id=submission_id,
        problem_id=problem_id,
        language=language,
        code=code,
        job_timeout='10m'
    )
    return job.id
